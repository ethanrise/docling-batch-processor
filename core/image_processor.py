#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   image_processor.py
@Time    :   2026/01/29 10:27:25
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------


"""
图片处理器模块
负责处理和保存图片
"""

import base64
import re
from pathlib import Path
from datetime import datetime
from typing import Tuple


class ImageProcessor:
    """图片处理器 - 负责处理和保存图片"""
    
    def __init__(self):
        pass
    
    def extract_and_save_images(self, markdown_content: str, output_dir: Path, base_name: str) -> Tuple[str, int]:
        """
        从Markdown中提取base64图片并保存为文件，更新Markdown中的引用
        图片文件名包含时间戳，避免重复
        
        Args:
            markdown_content: Markdown内容
            output_dir: 输出目录
            base_name: 基础文件名
            
        Returns:
            (更新后的Markdown内容, 图片数量)
        """
        # 创建图片子目录
        images_dir = output_dir / f"{base_name}_images"
        images_dir.mkdir(exist_ok=True)
        
        # 匹配base64图片的正则表达式
        base64_pattern = r'!\[([^\]]*)\]\(data:image/([^;]+);base64,([^)]+)\)'
        
        image_count = 0
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        def replace_base64_image(match):
            nonlocal image_count
            alt_text = match.group(1)
            image_format = match.group(2)
            base64_data = match.group(3)
            
            try:
                # 解码base64数据
                image_data = base64.b64decode(base64_data)
                
                # 生成图片文件名，包含时间戳和序号
                image_count += 1
                image_filename = f"image_{timestamp}_{image_count:03d}.{image_format}"
                image_path = images_dir / image_filename
                
                # 保存图片
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                
                # 返回新的Markdown图片引用（相对路径）
                relative_path = f"{base_name}_images/{image_filename}"
                return f"![{alt_text}]({relative_path})"
                
            except base64.binascii.Error:
                return match.group(0)  # 保持原样
            except Exception as e:
                return match.group(0)  # 保持原样
        
        # 替换所有base64图片
        updated_content = re.sub(base64_pattern, replace_base64_image, markdown_content)
        
        return updated_content, image_count
    
    def cleanup_empty_image_dirs(self, output_dir: Path):
        """清理空的图片目录"""
        for item in output_dir.iterdir():
            if item.is_dir() and item.name.endswith('_images'):
                if not any(item.iterdir()):
                    item.rmdir()
