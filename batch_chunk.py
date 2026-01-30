#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@File    :   chunk.py
@Time    :   2026/01/30 15:57:42
@Author  :   Ethan
@Email   :   ethanrise.ai@gmail.com
@Version :   1.0
@Desc    :   
@Note    :   None
'''

# ---------------------- Third-party Library Imports ----------------------


import argparse
from pathlib import Path
from core.markdown_processor import MarkdownProcessor

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量处理Markdown文档并为Dify准备',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 处理目录中的所有Markdown文件
  python batch_chunk.py -d /path/to/markdown/files
  
  # 指定输出目录和API地址
  python batch_chunk.py -d ./docs -o ./output --url http://localhost:9969/v1/chunk/hybrid/source

支持的文件格式:
  .md (Markdown files)
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        required=True,
        help='要处理的Markdown文件目录路径（自动查找.md文件）'
    )
    parser.add_argument(
        '-o', '--output', 
        help='输出目录（默认为输入目录同级的dify_ready文件夹）',
        default=None
    )
    parser.add_argument(
        '--url', 
        default='http://127.0.0.1:9969/v1/chunk/hybrid/source',
        help='文档切片服务URL (默认: http://127.0.0.1:9969/v1/chunk/hybrid/source)'
    )
    
    args = parser.parse_args()
    
    # 确定输出目录
    if args.output is None:
        input_dir = Path(args.directory)
        output_dir = input_dir.parent / "dify_ready" if input_dir.parent != input_dir else input_dir / "dify_ready"
    else:
        output_dir = Path(args.output)
    
    print(f"输入目录: {args.directory}")
    print(f"输出目录: {output_dir}")
    print(f"API地址: {args.url}")
    
    # 创建处理器并执行处理
    processor = MarkdownProcessor(
        api_url=args.url,
        input_folder=args.directory,
        output_folder=output_dir
    )
    
    try:
        processor.process_all_markdown_files()
        print(f"\n处理完成！切片文件已保存到: {output_dir}")
        print("现在你可以直接将这些文件导入到 Dify 中使用。")
        
    except KeyboardInterrupt:
        print("\n处理被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n处理失败: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()