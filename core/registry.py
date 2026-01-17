#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plugin registry for file format parsers
"""

from typing import Dict, List, Optional, Type
from pathlib import Path


class ParserRegistry:
    """Central registry for format parsers"""

    def __init__(self):
        self._parsers: Dict[str, Type['BaseParser']] = {}
        self._extension_map: Dict[str, str] = {}

    def register(self, parser_class: Type['BaseParser']) -> None:
        """
        Register a parser class.

        Args:
            parser_class: Parser class to register
        """
        parser = parser_class()
        format_name = parser.format_name

        self._parsers[format_name] = parser_class

        # Build extension map for auto-detection
        for ext in parser.file_extensions:
            # Normalize extension (with or without leading dot)
            if not ext.startswith('.'):
                ext = '.' + ext
            self._extension_map[ext.lower()] = format_name

    def get_parser(self, format_name: str) -> Optional['BaseParser']:
        """Get parser instance by format name"""
        parser_class = self._parsers.get(format_name)
        return parser_class() if parser_class else None

    def detect_format(self, file_path: str) -> Optional[str]:
        """
        Auto-detect format based on file extension.

        Args:
            file_path: Path to the file

        Returns:
            Format name or None if not detected
        """
        ext = Path(file_path).suffix.lower()
        return self._extension_map.get(ext)

    def find_parser_for_file(self, file_path: str, format_hint: Optional[str] = None) -> Optional['BaseParser']:
        """
        Find appropriate parser for a file.

        Args:
            file_path: Path to the file
            format_hint: Optional format override

        Returns:
            Parser instance or None if no suitable parser found
        """
        # Use manual override if provided
        if format_hint:
            parser = self.get_parser(format_hint)
            if parser and parser.supports_format(file_path):
                return parser

        # Try auto-detection
        format_name = self.detect_format(file_path)
        if format_name:
            parser = self.get_parser(format_name)
            if parser and parser.supports_format(file_path):
                return parser

        # Fallback: try all registered parsers
        for parser_class in self._parsers.values():
            parser = parser_class()
            if parser.supports_format(file_path):
                return parser

        return None

    def list_supported_formats(self) -> List[Dict[str, any]]:
        """Return list of all registered formats with metadata"""
        formats = []
        for format_name, parser_class in self._parsers.items():
            parser = parser_class()
            formats.append({
                'name': format_name,
                'display_name': parser.get_display_name(),
                'extensions': parser.file_extensions,
                'mime_types': parser.mime_types
            })
        return formats


# Global registry instance
registry = ParserRegistry()
