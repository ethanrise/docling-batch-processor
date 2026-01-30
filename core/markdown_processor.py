#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   markdown_processor.py
@Time    :   2026/01/30 16:20:19
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------



import base64
import requests
import os
import json
from pathlib import Path
import time

class MarkdownProcessor:
    def __init__(self, api_url, input_folder, output_folder):
        """
        初始化文档处理器
        
        Args:
            api_url (str): 文档处理API的URL
            input_folder (str): 输入文件夹路径
            output_folder (str): 输出文件夹路径
        """
        self.api_url = api_url
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def file_to_base64(self, file_path):
        """
        将文件转换为Base64字符串
        
        Args:
            file_path (Path): 文件路径
            
        Returns:
            str: Base64编码的字符串
        """
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
                base64_string = base64.b64encode(file_content).decode('utf-8')
                print(f"文件 {file_path.name} Base64 字符串长度: {len(base64_string)}")
                return base64_string
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在！")
            raise
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            raise

    def send_chunk_request(self, file_path):
        """
        发送文档切片请求
        
        Args:
            file_path (Path): 要处理的文件路径
            
        Returns:
            dict or None: API响应结果，失败时返回None
        """
        try:
            # 获取文件的 Base64 编码
            base64_string = self.file_to_base64(file_path)
            
            # 获取文件名
            filename = file_path.name
            
            # 构建请求数据
            payload = {
                "sources": [
                    {
                        "kind": "file",
                        "base64_string": base64_string,
                        "filename": filename
                    }
                ],
                "chunking_options": {
                    "chunker": "hybrid",
                    "use_markdown_tables": False,
                    "include_raw_text": True,
                    "max_tokens": 500,
                    "tokenizer": "Qwen/Qwen3-Embedding-0.6B",
                    "merge_peers": False
                }
            }

            # 发送请求
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"文件 {filename} 处理成功！获得 {len(result.get('chunks', []))} 个切片")
                return result
            else:
                print(f"文件 {filename} 处理失败，状态码: {response.status_code}")
                print("错误信息：", response.text)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求过程中出现问题: {e}")
            return None
        except Exception as e:
            print(f"处理文件 {file_path} 时发生未知错误: {e}")
            return None

    def clean_chunk_text(self, text):
        """
        清理切片文本，只移除纯空白行
        
        Args:
            text (str): 原始切片文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 移除首尾空白字符并规范化换行
        lines = text.splitlines()
        cleaned_lines = [line.rstrip() for line in lines if line.rstrip()]
        
        # 重新组合文本，确保每段之间只有一个空行
        cleaned_text = '\n'.join(cleaned_lines)
        
        return cleaned_text

    def save_chunks_to_single_file(self, chunks, original_filename):
        """
        将所有切片保存到单个文件中，保持原文档结构
        
        Args:
            chunks (list): 切片列表
            original_filename (str): 原始文件名
        """
        if not chunks:
            print(f"警告：{original_filename} 没有获得任何切片")
            return

        # 生成输出文件名
        file_stem = Path(original_filename).stem
        output_filename = f"{file_stem}_processed.txt"
        output_path = self.output_folder / output_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks):
                chunk_text = chunk.get('text', '')
                
                # 清理切片内容（只移除多余空白）
                cleaned_text = self.clean_chunk_text(chunk_text)
                
                if cleaned_text.strip():  # 只写入非空内容
                    f.write(cleaned_text)
                    f.write("\n\n")  # 用两个换行符分隔不同切片
        
        print(f"已保存 {len([c for c in chunks if self.clean_chunk_text(c.get('text', ''))])} 个有效切片到文件: {output_path}")

    def process_all_markdown_files(self):
        """
        处理输入文件夹中的所有Markdown文件
        """
        md_files = list(self.input_folder.glob("*.md"))
        
        if not md_files:
            print(f"在 {self.input_folder} 中没有找到任何 .md 文件")
            return
        
        print(f"找到 {len(md_files)} 个 Markdown 文件待处理")
        
        for i, md_file in enumerate(md_files):
            print(f"\n处理第 {i+1}/{len(md_files)} 个文件: {md_file.name}")
            
            # 发送切片请求
            result = self.send_chunk_request(md_file)
            
            if result:
                # 提取切片数据
                chunks = result.get('chunks', [])
                
                # 将切片保存到单个文件
                self.save_chunks_to_single_file(chunks, md_file.name)
                
                print(f"已完成 {md_file.name} 的处理")
            else:
                print(f"跳过文件 {md_file.name}，因为处理失败")
            
            # 添加短暂延迟，避免请求过于频繁
            time.sleep(1)