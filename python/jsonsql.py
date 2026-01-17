
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple JSON SQL Query Tool - 简化版JSON SQL查询工具
"""

import json
import sqlite3
import argparse
import sys
from typing import Dict, Any, List


def load_json_file(file_path: str) -> Dict[str, Any]:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: 文件 {file_path} 不是有效的JSON格式")
        sys.exit(1)


def create_table_from_data(cursor: sqlite3.Cursor, table_name: str, data: List[Dict]):
    """根据JSON数据创建数据库表"""
    if not data:
        return

    # 获取所有可能的键
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    # 创建表结构
    columns = []
    for key in all_keys:
        # 根据第一个数据项的值类型确定列类型
        first_value = data[0].get(key)
        if isinstance(first_value, int):
            col_type = "INTEGER"
        elif isinstance(first_value, float):
            col_type = "REAL"
        elif isinstance(first_value, bool):
            col_type = "BOOLEAN"
        else:
            col_type = "TEXT"

        columns.append(f"[{key}] {col_type}")

    # 创建表
    create_sql = f"CREATE TABLE [{table_name}] ({', '.join(columns)})"
    cursor.execute(create_sql)

    # 插入数据
    for item in data:
        # 确保所有键都有值，缺失的设为NULL
        row_values = [item.get(key) for key in all_keys]
        placeholders = ','.join(['?' for _ in range(len(all_keys))])
        insert_sql = f"INSERT INTO [{table_name}] VALUES ({placeholders})"
        cursor.execute(insert_sql, row_values)


def query_json_with_sql(json_file: str, table_name: str = "data"):
    """主函数：加载JSON并启动SQL查询交互"""
    # 加载JSON数据
    json_data = load_json_file(json_file)

    # 提取"data"数组（如果存在）
    if "data" in json_data and isinstance(json_data["data"], list):
        data_to_process = json_data["data"]
    else:
        # 如果没有data数组，则尝试直接处理整个JSON对象
        if isinstance(json_data, list):
            data_to_process = json_data
        else:
            # 如果是单个对象，转换为列表
            data_to_process = [json_data]

    # 创建内存数据库连接
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建表并插入数据
    create_table_from_data(cursor, table_name, data_to_process)

    print(f"已加载 {len(data_to_process)} 条记录到表 '{table_name}' 中")
    print("请输入SQL查询语句，输入 'exit' 或 'quit' 退出程序\n")

    # 进入交互式查询循环
    while True:
        try:
            sql_query = input("SQL> ").strip()

            if sql_query.lower() in ['exit', 'quit', '']:
                break

            # 执行查询
            cursor.execute(sql_query)

            # 检查是否为SELECT查询
            if sql_query.strip().upper().startswith('SELECT'):
                # 获取结果
                rows = cursor.fetchall()

                # 获取列名
                if cursor.description:
                    column_names = [description[0] for description in cursor.description]
                    print(f"\n列名: {column_names}")

                    # 显示结果
                    if rows:
                        print(f"找到 {len(rows)} 条记录:")
                        for i, row in enumerate(rows):
                            print(f"记录 {i+1}: {dict(zip(column_names, row))}")
                    else:
                        print("未找到匹配的记录")
            else:
                # 对于非SELECT语句（如INSERT, UPDATE, DELETE）
                conn.commit()
                print(f"执行完成，影响了 {cursor.rowcount} 行")

        except sqlite3.Error as e:
            print(f"SQL错误: {e}")
        except KeyboardInterrupt:
            print("\n程序被中断")
            break
        except Exception as e:
            print(f"错误: {e}")

    # 关闭数据库连接
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="JSON SQL Query Tool - 对JSON文件执行SQL查询")
    parser.add_argument("file", help="要查询的JSON文件路径")
    parser.add_argument("--table", default="data", help="数据库表名 (默认: data)")

    args = parser.parse_args()

    query_json_with_sql(args.file, args.table)


if __name__ == "__main__":
    main()

