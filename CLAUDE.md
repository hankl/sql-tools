# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

SQL Tools is a plugin-based Python tool that enables SQL queries on multiple file formats (JSON, CSV, Nginx logs). It loads files into an in-memory SQLite database and provides an interactive REPL for querying.

## Running the Tool

```bash
# New main entry point (auto-detects format)
python3 sqltools.py <file>

# List supported formats
python3 sqltools.py --list-formats

# Specify custom table name (default: auto-generated from filename)
python3 sqltools.py <file> --table <table_name>

# Force specific format parser
python3 sqltools.py <file> --format json|csv|nginx

# Legacy entry point (still works for backward compatibility)
python3 jsonsql.py <json_file>
```

## Code Architecture

The tool uses a plugin-based architecture:

```
sql-tools/
├── sqltools.py              # Main entry point (CLI)
├── core/
│   ├── engine.py            # SQLEngine - query execution & REPL
│   ├── schema.py            # SchemaInference - table schema creation
│   └── registry.py          # ParserRegistry - plugin management
├── parsers/
│   ├── base.py              # BaseParser abstract class
│   ├── json_parser.py       # JSON format parser
│   ├── csv_parser.py        # CSV format parser
│   └── nginx_parser.py      # Nginx access log parser
└── jsonsql.py               # Legacy: backward compatible wrapper
```

### Core Components

**`core/registry.py`** - ParserRegistry
- `register(parser_class)` - Register a parser plugin
- `detect_format(file_path)` - Auto-detect format by extension
- `find_parser_for_file(file_path, format_hint)` - Get appropriate parser
- `list_supported_formats()` - Return all registered formats

**`core/engine.py`** - SQLEngine
- `load_data(data, table_name)` - Load dict list into SQLite
- `execute_query(sql)` - Execute SQL and return results
- `run_repl(table_name)` - Interactive query loop
- `close()` - Cleanup database connection

**`core/schema.py`** - SchemaInference
- `infer_column_type(value)` - Map Python type → SQLite type
- `get_all_keys(data)` - Extract all unique keys from dict list
- `create_table_from_data(cursor, table_name, data)` - Create table and insert rows

### Parser Plugins

All parsers extend `parsers/base.py:BaseParser`:

```python
class BaseParser(ABC):
    format_name: str              # e.g., "json"
    file_extensions: List[str]    # e.g., [".json"]

    @abstractmethod
    def supports_format(self, file_path: str) -> bool: ...

    @abstractmethod
    def load(self, file_path: str) -> List[Dict[str, Any]]: ...

    def get_table_name(self, file_path: str) -> str: ...  # Optional override
```

**Supported Formats:**
- **JSON** (`.json`) - Handles wrapped `{"data": [...]}`, direct arrays, single objects
- **CSV** (`.csv`, `.tsv`) - Header row detection, auto-detect delimiter, type inference
- **Nginx** (`.log`, `.access.log`) - Combined log format with regex parsing

### Data Flow

1. CLI argument parsing → `sqltools.py:main()`
2. Format detection → `registry.find_parser_for_file()`
3. Data loading → `parser.load()` returns `List[Dict]`
4. Schema inference → `SchemaInference.create_table_from_data()`
5. SQLite table creation in memory
6. Interactive REPL → `SQLEngine.run_repl()`

## Adding a New Parser

1. Create `parsers/<name>_parser.py` extending `BaseParser`
2. Implement `supports_format()` and `load()`
3. Import and register in `sqltools.py:register_builtin_parsers()`
4. Add to `parsers/__init__.py` exports

Example:
```python
# parsers/xml_parser.py
class XMLParser(BaseParser):
    format_name = "xml"
    file_extensions = ['.xml']

    def supports_format(self, file_path: str) -> bool:
        return file_path.lower().endswith('.xml')

    def load(self, file_path: str) -> List[Dict[str, Any]]:
        # Parse XML and return list of dicts
        pass

# In sqltools.py
from parsers.xml_parser import XMLParser
registry.register(XMLParser)
```

## Design Notes

- **Table names** are auto-generated from filename (sanitized: `-`, ` `, `.` → `_`)
- **Column types** are inferred from the first data item only
- **Bracket notation** `[{column_name}]` handles special characters in keys
- **Type inference** converts strings to int/float when possible (CSV, Nginx)
- **Nginx logs** parse Combined format, convert timestamps to ISO, `-` → NULL
- **Backward compatibility** - `jsonsql.py` remains functional
- **No external dependencies** - uses only Python standard library
