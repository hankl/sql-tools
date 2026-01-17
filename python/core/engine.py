#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL query execution engine with interactive REPL
"""

import sqlite3
from typing import List, Dict, Any, Optional
from .schema import SchemaInference


class SQLEngine:
    """
    SQL query execution engine with interactive REPL.
    Extracted from query_json_with_sql() in jsonsql.py
    """

    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def load_data(self, data: List[Dict[str, Any]], table_name: str = "data") -> None:
        """
        Load data into in-memory SQLite database.

        Args:
            data: List of dictionaries to load
            table_name: Name for the table
        """
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        SchemaInference.create_table_from_data(
            self.cursor,
            table_name,
            data
        )

        print(f"已加载 {len(data)} 条记录到表 '{table_name}' 中")

    def execute_query(self, sql_query: str) -> Optional[List[tuple]]:
        """
        Execute a SQL query.

        Args:
            sql_query: SQL query string

        Returns:
            Query results or None for non-SELECT queries
        """
        if not self.cursor:
            raise RuntimeError("No data loaded. Call load_data() first.")

        self.cursor.execute(sql_query)

        if sql_query.strip().upper().startswith('SELECT'):
            return self.cursor.fetchall()
        else:
            self.conn.commit()
            return None

    def get_column_names(self) -> Optional[List[str]]:
        """Get column names from last query"""
        if self.cursor and self.cursor.description:
            return [desc[0] for desc in self.cursor.description]
        return None

    def run_repl(self, table_name: str = "data") -> None:
        """
        Run interactive REPL for SQL queries.

        This is extracted from the main loop in query_json_with_sql()

        Args:
            table_name: Default table name for queries
        """
        print("请输入SQL查询语句，输入 'exit' 或 'quit' 退出程序\n")

        while True:
            try:
                sql_query = input("SQL> ").strip()

                if sql_query.lower() in ['exit', 'quit', '']:
                    break

                results = self.execute_query(sql_query)

                if sql_query.strip().upper().startswith('SELECT'):
                    column_names = self.get_column_names()

                    if column_names:
                        print(f"\n列名: {column_names}")

                    if results:
                        print(f"找到 {len(results)} 条记录:")
                        for i, row in enumerate(results, 1):
                            print(f"记录 {i}: {dict(zip(column_names, row))}")
                    else:
                        print("未找到匹配的记录")
                else:
                    print(f"执行完成，影响了 {self.cursor.rowcount} 行")

            except sqlite3.Error as e:
                print(f"SQL错误: {e}")
            except KeyboardInterrupt:
                print("\n程序被中断")
                break
            except Exception as e:
                print(f"错误: {e}")

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
