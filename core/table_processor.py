#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   table_processor.py
@Time    :   2026/01/29 10:28:00
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------


"""
表格处理器模块
负责优化表格格式
"""

class TableProcessor:
    """表格处理器 - 负责优化表格格式"""
    
    def __init__(self):
        pass
    
    def process_tables(self, markdown_content: str) -> str:
        """
        处理Markdown中的表格格式，确保表格前后有空行
        
        Args:
            markdown_content: Markdown内容
            
        Returns:
            处理后的Markdown内容
        """
        lines = markdown_content.split('\n')
        processed_lines = []
        in_table = False
        
        for i, line in enumerate(lines):
            # 检测表格行（包含 | 符号）
            is_table_line = '|' in line and line.strip().startswith('|')
            
            if is_table_line and not in_table:
                # 表格开始，确保前面有空行
                if processed_lines and processed_lines[-1].strip():
                    processed_lines.append('')
                in_table = True
            elif not is_table_line and in_table:
                # 表格结束，确保后面有空行
                in_table = False
                processed_lines.append(line)
                if line.strip() and i < len(lines) - 1:
                    processed_lines.append('')
                continue
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)

