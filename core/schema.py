#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schema inference module - extracts schema from data and creates SQLite tables
"""

import sqlite3
from typing import List, Dict, Any, Set


class SchemaInference:
    """Extract schema inference logic from original jsonsql.py"""

    @staticmethod
    def infer_column_type(value: Any) -> str:
        """
        Infer SQLite column type from Python value.

        Args:
            value: Python value to analyze

        Returns:
            SQLite type name (TEXT, INTEGER, REAL, BOOLEAN)
        """
        if value is None:
            return "TEXT"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        else:
            return "TEXT"

    @staticmethod
    def get_all_keys(data: List[Dict[str, Any]]) -> Set[str]:
        """
        Extract all unique keys from a list of dictionaries.

        Args:
            data: List of dictionaries

        Returns:
            Set of all unique keys
        """
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        return all_keys

    @staticmethod
    def create_table_from_data(cursor: sqlite3.Cursor, table_name: str,
                               data: List[Dict[str, Any]]) -> None:
        """
        Create SQLite table from list of dictionaries.

        This is the refactored version of create_table_from_data() from jsonsql.py

        Args:
            cursor: SQLite cursor
            table_name: Name of the table to create
            data: List of dictionaries containing the data
        """
        if not data:
            return

        all_keys = SchemaInference.get_all_keys(data)

        # Sort keys for consistent column order
        sorted_keys = sorted(all_keys)

        # Create table structure
        columns = []
        for key in sorted_keys:
            first_value = data[0].get(key)
            col_type = SchemaInference.infer_column_type(first_value)
            columns.append(f"[{key}] {col_type}")

        # Create table
        create_sql = f"CREATE TABLE [{table_name}] ({', '.join(columns)})"
        cursor.execute(create_sql)

        # Insert data
        for item in data:
            row_values = [item.get(key) for key in sorted_keys]
            placeholders = ','.join(['?' for _ in range(len(sorted_keys))])
            insert_sql = f"INSERT INTO [{table_name}] VALUES ({placeholders})"
            cursor.execute(insert_sql, row_values)

    @staticmethod
    def get_table_info(cursor: sqlite3.Cursor, table_name: str) -> List[Dict[str, str]]:
        """
        Get table schema information.

        Args:
            cursor: SQLite cursor
            table_name: Name of the table

        Returns:
            List of column info dictionaries
        """
        cursor.execute(f"PRAGMA table_info([{table_name}])")
        return [{'name': row[1], 'type': row[2]} for row in cursor.fetchall()]
