#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   formula_processor.py
@Time    :   2026/01/29 14:46:34
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------
"""
通用数学公式处理器
智能识别并修复任意函数名中的空格问题，无需预定义映射
"""

import re
from typing import Tuple, List, Dict


class FormulaProcessor:
    """通用数学公式处理器 - 智能修复任意函数名空格问题"""
    
    def __init__(self):
        # LaTeX公式模式
        self.inline_patterns = [r'\$(.*?)\$', r'\\\((.*?)\\\)',]
        self.display_patterns = [r'\$\$(.*?)\$\$', r'\\\[([\s\S]*?)\\\]',]
    
    def extract_formulas(self, markdown_content: str) -> Tuple[str, List[Dict], int]:
        """提取Markdown中的所有数学公式"""
        formulas = []
        content = markdown_content
        
        # 处理行间公式
        display_formulas = []
        for pattern in self.display_patterns:
            matches = list(re.finditer(pattern, content, re.DOTALL))
            for match in matches:
                formula_text = match.group(1).strip()
                if formula_text:
                    formula_info = {
                        'type': 'display',
                        'original': match.group(0),
                        'content': formula_text,
                        'start': match.start(),
                        'end': match.end()
                    }
                    display_formulas.append(formula_info)
        
        display_formulas.sort(key=lambda x: x['start'], reverse=True)
        
        # 替换为占位符
        for i, formula in enumerate(display_formulas):
            placeholder = f"__FORMULA_DISPLAY_{i}__"
            content = content[:formula['start']] + placeholder + content[formula['end']:]
        
        # 处理行内公式
        inline_formulas = []
        for pattern in self.inline_patterns:
            matches = list(re.finditer(pattern, content))
            for match in matches:
                formula_text = match.group(1).strip()
                if formula_text:
                    formula_info = {
                        'type': 'inline',
                        'original': match.group(0),
                        'content': formula_text,
                        'start': match.start(),
                        'end': match.end()
                    }
                    inline_formulas.append(formula_info)
        
        inline_formulas.sort(key=lambda x: x['start'], reverse=True)
        
        for i, formula in enumerate(inline_formulas):
            placeholder = f"__FORMULA_INLINE_{i}__"
            content = content[:formula['start']] + placeholder + content[formula['end']:]
        
        all_formulas = display_formulas + inline_formulas
        return content, all_formulas, len(all_formulas)
    
    def clean_formula_content(self, formula_content: str) -> str:
        """
        通用清理公式内容 - 智能修复任意函数名空格问题
        """
        cleaned = formula_content
        
        # 1. 修复HTML实体和转义字符
        cleaned = (cleaned.replace('&lt;', '<')
                          .replace('&gt;', '>')
                          .replace('&amp;', '&')
                          .replace('&nbsp;', ' ')
                          .replace('\\$', '$'))
        
        # 2. 智能修复函数名中的空格（核心逻辑）
        cleaned = self._fix_spaced_identifiers(cleaned)
        
        # 3. 移除所有剩余空格（在数学模式下是安全的）
        cleaned = re.sub(r'\s+', '', cleaned)
        
        # 4. 修复LaTeX语法细节
        cleaned = self._fix_latex_syntax(cleaned)
        
        return cleaned.strip()
    
    def _fix_spaced_identifiers(self, formula: str) -> str:
        """
        智能修复间隔字母组成的标识符
        识别模式：连续的字母序列，每个字母后可能跟空格
        例如: "M u l t i H e a d" -> "MultiHead"
        """
        # 这个正则表达式匹配连续的字母序列（至少2个字母）
        # 每个字母后可以跟任意空白字符
        # 要求序列以大写字母开头（典型的函数名模式）
        # 或者是全小写的合理长度序列（3-15个字母）
        
        def merge_spaced_letters(match):
            """将匹配到的间隔字母合并成连续字符串"""
            spaced_text = match.group(0)
            # 移除所有空白字符，只保留字母
            merged = re.sub(r'\s+', '', spaced_protected_text)
            return merged
        
        # 保护 \text{} 内容，避免误处理
        text_blocks = {}
        def protect_text_blocks(text):
            def replace_text(match):
                key = f"__TEXT_BLOCK_{len(text_blocks)}__"
                text_blocks[key] = match.group(0)
                return key
            return re.sub(r'\\text\s*\{[^}]*\}', replace_text, text)
        
        def restore_text_blocks(text):
            for key, value in text_blocks.items():
                text = text.replace(key, value)
            return text
        
        # 先保护 \text{} 块
        protected_formula = protect_text_blocks(formula)
        
        # 匹配以大写字母开头的间隔字母序列（最可能是函数名）
        # 模式：大写字母 + (空格 + 字母)* ，至少2个字母
        protected_formula = re.sub(
            r'[A-Z](?:\s+[a-zA-Z]){1,20}',
            lambda m: re.sub(r'\s+', '', m.group(0)),
            protected_formula
        )
        
        # 匹配全小写的间隔字母序列（长度3-15，避免误伤单字母变量）
        protected_formula = re.sub(
            r'[a-z](?:\s+[a-z]){2,14}',
            lambda m: re.sub(r'\s+', '', m.group(0)),
            protected_formula
        )
        
        # 恢复 \text{} 块
        result = restore_text_blocks(protected_formula)
        
        return result
    
    def _fix_latex_syntax(self, formula: str) -> str:
        """修复LaTeX语法细节"""
        fixed = formula
        
        # 修复 \text 命令（确保花括号紧贴）
        fixed = re.sub(r'\\text\{', r'\\text{', fixed)
        
        # 修复下标和上标（虽然空格已移除，但确保语法正确）
        fixed = re.sub(r'_\{', r'_{', fixed)
        fixed = re.sub(r'\^\{', r'^{', fixed)
        
        # 修复多余的花括号
        fixed = re.sub(r'\{+', r'{', fixed)
        fixed = re.sub(r'\}+', r'}', fixed)
        
        return fixed
    
    def restore_formulas(self, cleaned_content: str, formulas: List[Dict]) -> str:
        """恢复修正后的公式"""
        result = cleaned_content
        placeholder_to_formula = {}
        
        for i, formula in enumerate(formulas):
            cleaned_text = self.clean_formula_content(formula['content'])
            
            if formula['type'] == 'display':
                restored = f"$${cleaned_text}$$"
                placeholder = f"__FORMULA_DISPLAY_{i}__"
            else:
                restored = f"${cleaned_text}$"
                placeholder = f"__FORMULA_INLINE_{i}__"
            
            placeholder_to_formula[placeholder] = restored
        
        # 按长度排序替换（避免冲突）
        for placeholder in sorted(placeholder_to_formula.keys(), key=len, reverse=True):
            result = result.replace(placeholder, placeholder_to_formula[placeholder])
        
        return result
    
    def fix_unclosed_formulas(self, markdown_content: str) -> str:
        """修复未闭合的公式"""
        content = markdown_content
        dollar_positions = [i for i, char in enumerate(content) 
                           if char == '$' and (i == 0 or content[i-1] != '\\')]
        
        if len(dollar_positions) % 2 == 1:
            last_pos = dollar_positions[-1]
            content = content[:last_pos] + content[last_pos+1:]
        
        return content
    
    def process_formulas(self, markdown_content: str) -> Tuple[str, int]:
        """主处理方法"""
        content = self.fix_unclosed_formulas(markdown_content)
        extracted_content, formulas, formula_count = self.extract_formulas(content)
        
        if formula_count == 0:
            return markdown_content, 0
        
        final_content = self.restore_formulas(extracted_content, formulas)
        return final_content, formula_count