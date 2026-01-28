"""
Docling客户端模块
负责与Docling服务通信
"""

import requests
import json
import mimetypes
from pathlib import Path
from typing import Dict


class DoclingClient:
    """Docling客户端 - 负责与Docling服务通信"""
    
    def __init__(self, service_url: str = "http://localhost:9969/v1/convert/file"):
        """
        初始化Docling客户端
        
        Args:
            service_url: Docling服务的URL
        """
        self.service_url = service_url
        self.session = requests.Session()
        # 设置连接池和重试策略
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def convert_file(self, file_path: str) -> Dict:
        """
        调用Docling服务转换单个文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            转换结果字典
        """
        file_path = Path(file_path)
        
        try:
            # 读取文件
            with open(file_path, 'rb') as f:
                files = {
                    'files': (file_path.name, f, self._get_mime_type(file_path))
                }
                
                # 设置转换参数
                data = {
                    'output_format': 'markdown',
                    'image_mode': 'base64',
                }
                
                # 发送请求
                response = self.session.post(
                    self.service_url,
                    files=files,
                    data=data,
                    timeout=300  # 5分钟超时
                )

                response.raise_for_status()
                result = response.json()
                return result
                
        except requests.exceptions.ConnectionError:
            raise Exception(f"无法连接到Docling服务 ({self.service_url})，请确认服务是否正在运行")
        except requests.exceptions.Timeout:
            raise Exception("请求超时，文件可能过大或服务响应缓慢")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("服务返回的不是有效的JSON格式")
        except Exception as e:
            raise Exception(f"转换失败: {str(e)}")
    
    def _get_mime_type(self, file_path: Path) -> str:
        """获取文件的MIME类型"""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'