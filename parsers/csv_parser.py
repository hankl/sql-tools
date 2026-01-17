#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV file format parser
"""

import csv
import sys
from typing import List, Dict, Any
from .base import BaseParser


class CSVParser(BaseParser):
    """Parser for CSV files with header row"""

    format_name = "csv"
    file_extensions = ['.csv', '.tsv']
    mime_types = ['text/csv', 'text/tab-separated-values']

    def supports_format(self, file_path: str) -> bool:
        """Check if file is CSV"""
        ext = file_path.lower().split('.')[-1]
        return ext in ['csv', 'tsv']

    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """Load CSV file and convert to list of dictionaries"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Auto-detect delimiter
                sample = f.read(1024)
                f.seek(0)

                delimiter = ','
                try:
                    sniffer = csv.Sniffer()
                    if sniffer.has_header(sample):
                        delimiter = sniffer.sniff(sample).delimiter
                except csv.Error:
                    delimiter = ','

                # Read with detected delimiter
                reader = csv.DictReader(f, delimiter=delimiter)
                data = list(reader)

                # Type inference: try to convert strings to numbers
                for row in data:
                    for key, value in row.items():
                        row[key] = self._infer_type(value)

                return data

        except FileNotFoundError:
            print(f"错误: 文件 {file_path} 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"读取CSV错误: {e}")
            sys.exit(1)

    def _infer_type(self, value: str) -> Any:
        """Try to convert string to int, float, or keep as string"""
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except (ValueError, TypeError):
            return value
