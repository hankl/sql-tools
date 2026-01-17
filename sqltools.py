#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Tools - Multi-format file query tool with plugin architecture
"""

import argparse
import sys
from core.registry import registry
from core.engine import SQLEngine
from parsers.json_parser import JSONParser
from parsers.csv_parser import CSVParser
from parsers.nginx_parser import NginxParser


def register_builtin_parsers():
    """Register built-in parsers"""
    registry.register(JSONParser)
    registry.register(CSVParser)
    registry.register(NginxParser)


def list_formats():
    """Display all supported formats"""
    formats = registry.list_supported_formats()
    print("\n支持的文件格式:")
    print("-" * 50)
    for fmt in formats:
        extensions = ', '.join(fmt['extensions']) if fmt['extensions'] else 'N/A'
        print(f"\n{fmt['display_name']} ({fmt['name']})")
        print(f"  扩展名: {extensions}")
    print()


def query_file(file_path: str, table_name: str = None, format_override: str = None):
    """
    Main function: Load file and start SQL query REPL

    Args:
        file_path: Path to file to query
        table_name: Custom table name (auto-generated if None)
        format_override: Force specific format parser
    """
    # Find appropriate parser
    parser = registry.find_parser_for_file(file_path, format_override)

    if not parser:
        print(f"错误: 未找到适合该文件的解析器: {file_path}")
        print("使用 --list-formats 查看支持的格式")
        sys.exit(1)

    print(f"检测到格式: {parser.get_display_name()}")

    # Load data
    data = parser.load(file_path)

    if not data:
        print("错误: 未能从文件加载任何数据")
        sys.exit(1)

    # Generate table name if not provided
    if not table_name:
        table_name = parser.get_table_name(file_path)

    # Create engine and load data
    engine = SQLEngine()
    engine.load_data(data, table_name)

    # Start interactive REPL
    engine.run_repl(table_name)

    # Cleanup
    engine.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SQL Tools - 使用 SQL 查询 JSON、CSV 和日志文件",
        epilog="示例:\n"
               "  %(prog)s data.json\n"
               "  %(prog)s access.log --table nginx_logs\n"
               "  %(prog)s data.csv --format csv\n"
               "  %(prog)s --list-formats",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="要查询的文件路径"
    )
    parser.add_argument(
        "--table", "-t",
        default=None,
        help="自定义表名 (默认: 从文件名自动生成)"
    )
    parser.add_argument(
        "--format", "-f",
        dest="format_override",
        choices=['json', 'csv', 'nginx'],
        help="强制指定格式解析器 (默认: 自动检测)"
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="列出所有支持的文件格式"
    )

    args = parser.parse_args()

    # Register built-in parsers
    register_builtin_parsers()

    # Handle --list-formats
    if args.list_formats:
        list_formats()
        return

    # Require file argument for normal operation
    if not args.file:
        parser.error("需要参数: file")

    # Run query
    query_file(args.file, args.table, args.format_override)


if __name__ == "__main__":
    main()
