#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   output_manager.py
@Time    :   2026/01/29 10:27:32
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------


"""
输出管理器模块
负责文件保存和报告生成
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class OutputManager:
    """输出管理器 - 负责文件保存和报告生成"""
    
    def __init__(self):
        pass
    
    def save_markdown(self, content: str, output_path: Path):
        """
        保存Markdown内容到文件
        
        Args:
            content: Markdown内容
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"保存Markdown文件失败: {str(e)}")
    
    def generate_report(self, results: List[Dict], output_dir: Path):
        """
        生成转换报告
        
        Args:
            results: 转换结果列表
            output_dir: 输出目录
        """
        report_path = output_dir / "conversion_report.txt"
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("批量文档转换报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"总文件数: {len(results)}\n")
            f.write(f"成功转换: {len(successful)}\n")
            f.write(f"转换失败: {len(failed)}\n")
            f.write(f"转换时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if successful:
                f.write("成功转换的文件:\n")
                f.write("-" * 30 + "\n")
                for result in successful:
                    f.write(f"✓ {result['input_file']} -> {result['output_file']}\n")
                    f.write(f"  处理时间: {result.get('duration', 0):.2f}秒\n")
                    f.write(f"  图片数量: {result.get('image_count', 0)}\n\n")
                    f.write(f"  公式数量: {result.get('formula_count', 0)}\n\n")
            
            if failed:
                f.write("转换失败的文件:\n")
                f.write("-" * 30 + "\n")
                for result in failed:
                    f.write(f"✗ {result['input_file']}\n")
                    f.write(f"  错误: {result['error']}\n\n")
        
        print(f"\n转换报告已保存: {report_path}")