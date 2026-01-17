#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON file format parser
"""

import json
import sys
from typing import List, Dict, Any
from .base import BaseParser


class JSONParser(BaseParser):
    """Parser for JSON files"""

    format_name = "json"
    file_extensions = ['.json']
    mime_types = ['application/json']

    def supports_format(self, file_path: str) -> bool:
        """Check if file is valid JSON"""
        return file_path.lower().endswith('.json')

    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """Load JSON file and extract data array"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # Extract "data" array if present (backward compatibility)
            if "data" in json_data and isinstance(json_data["data"], list):
                return json_data["data"]

            # Handle direct array
            if isinstance(json_data, list):
                return json_data

            # Handle single object - wrap in list
            if isinstance(json_data, dict):
                return [json_data]

            raise ValueError("Unsupported JSON structure")

        except FileNotFoundError:
            print(f"错误: 文件 {file_path} 不存在")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"错误: 文件 {file_path} 不是有效的JSON格式: {e}")
            sys.exit(1)
