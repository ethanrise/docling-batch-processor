"""
文件验证器模块
负责验证输入文件的有效性
"""

from pathlib import Path
from typing import List, Tuple


class FileValidator:
    """文件验证器 - 负责验证输入文件的有效性"""
    
    def __init__(self):
        self.supported_extensions = {'.pdf', '.docx', '.doc', '.txt', '.pptx', '.html', '.xml', '.xlsx', '.xls'}
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """
        验证单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            (是否有效, 错误信息)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, f"文件不存在: {path}"
        
        if path.suffix.lower() not in self.supported_extensions:
            return False, f"不支持的文件格式: {path.suffix} (支持: {', '.join(self.supported_extensions)})"
        
        if path.stat().st_size == 0:
            return False, f"文件为空: {path}"
        
        return True, ""
    
    def validate_files(self, file_paths: List[str]) -> List[Tuple[str, bool, str]]:
        """
        批量验证文件
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            [(文件路径, 是否有效, 错误信息)]
        """
        results = []
        for file_path in file_paths:
            is_valid, error_msg = self.validate_file(file_path)
            results.append((file_path, is_valid, error_msg))
        return results