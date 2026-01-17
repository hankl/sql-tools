#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nginx access log parser (Combined format)
"""

import re
import sys
from typing import List, Dict, Any
from datetime import datetime
from .base import BaseParser


class NginxParser(BaseParser):
    """Parser for Nginx access logs (combined format)"""

    format_name = "nginx"
    file_extensions = ['.log', '.access.log']
    mime_types = ['text/plain']

    # Combined log format regex pattern
    # Example: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /path HTTP/1.1" 200 1234 "http://referer" "Mozilla/5.0"
    LOG_PATTERN = re.compile(
        r'(?P<remote_addr>\S+) '                    # IP address
        r'(?P<remote_user>\S+) '                    # Remote user (usually -)
        r'(?P<auth_user>\S+) '                      # Auth user (usually -)
        r'\[(?P<time_local>[^\]]+)\] '              # Timestamp
        r'"(?P<request>(?P<method>\S+) '            # HTTP method
        r'(?P<path>\S+) '                           # Request path
        r'(?P<protocol>\S+))" '                     # HTTP protocol
        r'(?P<status>\d+) '                         # Status code
        r'(?P<body_bytes_sent>\d+) '                # Response size
        r'"(?P<http_referer>[^"]*)" '               # Referer
        r'"(?P<http_user_agent>[^"]*)"'             # User agent
    )

    def supports_format(self, file_path: str) -> bool:
        """Check if file looks like Nginx log"""
        if not file_path.lower().endswith(('.log', '.access.log')):
            return False

        # Try to parse first line to confirm format
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                return bool(self.LOG_PATTERN.match(first_line))
        except Exception:
            return False

    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse Nginx access log into structured data"""
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    match = self.LOG_PATTERN.match(line)
                    if match:
                        log_entry = match.groupdict()

                        # Convert types
                        log_entry['status'] = int(log_entry['status'])
                        log_entry['body_bytes_sent'] = int(log_entry['body_bytes_sent'])

                        # Parse timestamp
                        try:
                            log_entry['time_local'] = self._parse_nginx_timestamp(
                                log_entry['time_local']
                            )
                        except ValueError:
                            pass  # Keep as string if parsing fails

                        # Handle empty strings
                        for key, value in log_entry.items():
                            if value == '-':
                                log_entry[key] = None

                        data.append(log_entry)
                    else:
                        print(f"警告: 无法解析第 {line_num} 行")

            return data

        except FileNotFoundError:
            print(f"错误: 文件 {file_path} 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"读取日志文件错误: {e}")
            sys.exit(1)

    def _parse_nginx_timestamp(self, timestamp_str: str) -> str:
        """
        Parse Nginx timestamp format.
        Input: 10/Oct/2023:13:55:36 +0000
        Output: ISO format string
        """
        # Parse and convert to ISO format for easier SQL queries
        try:
            dt = datetime.strptime(timestamp_str.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
            return dt.isoformat()
        except ValueError:
            return timestamp_str
