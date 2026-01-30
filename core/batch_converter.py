#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   batch_converter.py
@Time    :   2026/01/29 10:27:09
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------



"""
批量转换器模块
主控制器类，协调各组件工作
"""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict
from .file_validator import FileValidator
from .docling_client import DoclingClient
from .image_processor import ImageProcessor
from .table_processor import TableProcessor
from .formula_processor import FormulaProcessor
from .output_manager import OutputManager


class BatchConverter:
    """批量转换器 - 主控制器类"""
    
    def __init__(self, service_url: str = "http://localhost:9969/v1/convert/file", max_workers: int = 1):
        """
        初始化批量转换器
        
        Args:
            service_url: Docling服务URL
            max_workers: 最大并发数
        """
        self.validator = FileValidator()
        self.client = DoclingClient(service_url)
        self.image_processor = ImageProcessor()
        self.table_processor = TableProcessor()
        self.formula_processor = FormulaProcessor()  # 新增公式处理器
        self.output_manager = OutputManager()
        self.max_workers = max_workers
        self.lock = threading.Lock()
    
    def process_single_file(self, input_file: str, output_dir: Path) -> Dict:
        """
        处理单个文件
        
        Args:
            input_file: 输入文件路径
            output_dir: 输出目录
            
        Returns:
            处理结果字典
        """
        start_time = time.time()
        result = {
            'input_file': input_file,
            'output_file': '',
            'status': 'pending',
            'error': '',
            'image_count': 0,
            'formula_count': 0, 
            'duration': 0
        }
        
        try:
            input_path = Path(input_file)
            base_name = input_path.stem
            
            # 1. 调用Docling服务转换
            api_result = self.client.convert_file(input_path)
            
            # 2. 提取Markdown内容
            markdown_content = self._extract_markdown(api_result)
            
            if not markdown_content:
                raise Exception("无法从响应中提取Markdown内容")
            
            # 3. 生成输出文件名
            output_file = output_dir / f"{base_name}.md"
            result['output_file'] = str(output_file)
            
            # 4. 提取并保存图片，更新图片引用
            markdown_content, image_count = self.image_processor.extract_and_save_images(
                markdown_content, 
                output_dir, 
                base_name
            )
            result['image_count'] = image_count
            
            # 5. 处理表格格式
            markdown_content = self.table_processor.process_tables(markdown_content)
            
            # 6. 处理数学公式（新增步骤）
            markdown_content, formula_count = self.formula_processor.process_formulas(markdown_content)
            result['formula_count'] = formula_count
            
            # 7. 保存Markdown文件
            self.output_manager.save_markdown(markdown_content, output_file)
            
            result['status'] = 'success'
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
        
        result['duration'] = time.time() - start_time
        return result
    
    def _extract_markdown(self, result: dict) -> str:
        """
        从API响应中提取Markdown内容
        
        Args:
            result: API响应
            
        Returns:
            Markdown内容
        """
        if isinstance(result, dict):
            return result["document"]["md_content"]
        elif isinstance(result, str):
            return result
        return None
    
    def batch_convert(self, input_files: List[str], output_dir: str = None) -> List[Dict]:
        """
        批量转换文件
        
        Args:
            input_files: 输入文件路径列表
            output_dir: 输出目录
            
        Returns:
            转换结果列表
        """
        # 验证输入文件
        validation_results = self.validator.validate_files(input_files)
        
        valid_files = []
        for file_path, is_valid, error_msg in validation_results:
            if is_valid:
                valid_files.append(file_path)
                print(f"✓ 验证通过: {Path(file_path).name}")
            else:
                print(f"✗ 验证失败: {error_msg}")
        
        if not valid_files:
            print("没有有效的文件需要转换")
            return []
        
        # 确定输出目录
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = Path(valid_files[0]).parent
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n开始批量转换 {len(valid_files)} 个文件...")
        print(f"输出目录: {output_path.absolute()}")
        print(f"并发数: {self.max_workers}")
        
        # 并发处理文件
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务
            future_to_file = {
                executor.submit(self.process_single_file, file_path, output_path): file_path 
                for file_path in valid_files
            }
            
            # 收集结果
            completed = 0
            for future in as_completed(future_to_file):
                result = future.result()
                results.append(result)
                completed += 1
                
                # 显示进度
                status_symbol = "✓" if result['status'] == 'success' else "✗"
                print(f"[{completed}/{len(valid_files)}] {status_symbol} {Path(result['input_file']).name}")
        
        # 清理空的图片目录
        self.image_processor.cleanup_empty_image_dirs(output_path)
        
        # 生成报告
        self.output_manager.generate_report(results, output_path)
        
        return results