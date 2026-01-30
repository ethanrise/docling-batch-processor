#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   batch_convert.py
@Time    :   2026/01/29 10:26:51
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------



"""
主程序入口
"""

import argparse
from pathlib import Path
from typing import List
from core.batch_converter import BatchConverter


def find_files_in_directory(directory: str, extensions: set = None) -> List[str]:
    """
    在目录中查找指定扩展名的文件
    
    Args:
        directory: 目录路径
        extensions: 文件扩展名集合
        
    Returns:
        文件路径列表
    """
    if extensions is None:
        extensions = {'.pdf', '.docx', '.doc', '.txt', '.pptx', '.html', '.xml', '.xlsx', '.xls'}
    
    directory_path = Path(directory)
    found_files = []
    
    for ext in extensions:
        found_files.extend(directory_path.glob(f"*{ext}"))
        found_files.extend(directory_path.glob(f"*{ext.upper()}"))  # 同时匹配大写扩展名
    
    return [str(f) for f in found_files]


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量转换文档文件为Markdown格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 转换多个文件
  python batch_convert.py file1.pdf file2.docx file3.txt
  
  # 转换目录中的所有支持文件
  python batch_convert.py -d /path/to/documents
  
  # 转换文件到指定目录
  python batch_convert.py file1.pdf file2.docx -o ./output
  
  # 指定并发数和Docling服务地址
  python batch_convert.py -d ./docs --workers 5 --url http://localhost:9969/v1/convert/file
  
支持的文件格式:
  .pdf, .docx, .doc, .txt, .pptx, .html, .xml, .xlsx, .xls
        """
    )
    
    parser.add_argument(
        'input_files', 
        nargs='*', 
        help='要转换的文件路径列表'
    )
    parser.add_argument(
        '-d', '--directory',
        help='要转换的目录路径（自动查找支持的文件）'
    )
    parser.add_argument(
        '-o', '--output', 
        help='输出目录（默认为第一个输入文件所在目录）',
        default=None
    )
    parser.add_argument(
        '--workers', 
        type=int,
        default=3,
        help='并发处理数（默认: 3）'
    )
    parser.add_argument(
        '--url', 
        default='http://localhost:9969/v1/convert/file',
        help='Docling服务URL (默认: http://localhost:9969/v1/convert/file)'
    )
    
    args = parser.parse_args()
    
    # 确定输入文件列表
    input_files = []
    
    if args.directory:
        # 从目录中查找文件
        input_files = find_files_in_directory(args.directory)
        if not input_files:
            print(f"在目录 {args.directory} 中没有找到支持的文件")
            return
        print(f"在目录 {args.directory} 中找到 {len(input_files)} 个文件")
    
    if args.input_files:
        # 添加命令行指定的文件
        input_files.extend(args.input_files)
    
    if not input_files:
        print("请指定要转换的文件或目录")
        parser.print_help()
        return
    
    # 去重并移除重复项
    input_files = list(set(input_files))
    
    print(f"总共需要处理 {len(input_files)} 个文件")
    
    # 创建批量转换器并执行转换
    converter = BatchConverter(
        service_url=args.url,
        max_workers=args.workers
    )
    
    try:
        results = converter.batch_convert(input_files, args.output)
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        print(f"\n批量转换完成!")
        print(f"成功: {len(successful)}, 失败: {len(failed)}")
        
        if failed:
            print("\n失败的文件:")
            for result in failed:
                print(f"  - {result['input_file']}: {result['error']}")
        
    except KeyboardInterrupt:
        print("\n转换被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n处理失败: {str(e)}")
        exit(1)


if __name__ == '__main__':
    main()