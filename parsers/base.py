#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base parser class for all file format parsers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import os


class BaseParser(ABC):
    """Abstract base class for all file format parsers"""

    # Class attributes for metadata
    format_name: str = "base"
    file_extensions: List[str] = []
    mime_types: List[str] = []

    @abstractmethod
    def supports_format(self, file_path: str) -> bool:
        """
        Check if this parser supports the given file.

        Args:
            file_path: Path to the file to check

        Returns:
            True if this parser can handle the file
        """
        pass

    @abstractmethod
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and parse the file into a list of dictionaries.

        Args:
            file_path: Path to the file to load

        Returns:
            List of dictionaries representing the data
        """
        pass

    def get_table_name(self, file_path: str) -> str:
        """
        Generate a default table name from the file path.

        Args:
            file_path: Path to the file

        Returns:
            Suggested table name (default: 'data')
        """
        basename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(basename)[0]
        # Sanitize: remove non-alphanumeric chars
        table_name = name_without_ext.replace('-', '_').replace(' ', '_').replace('.', '_')
        # Ensure it doesn't start with a digit (SQLite requirement)
        if table_name and table_name[0].isdigit():
            table_name = 't_' + table_name
        return table_name or 'data'

    def get_display_name(self) -> str:
        """Return human-readable format name"""
        return self.format_name

    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate the file before parsing.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        if not os.path.isfile(file_path):
            return False, f"Path is not a file: {file_path}"
        return True, ""
