# SQL Tools - Multi-Format SQL Query Tool

<div align="center">
  <img src="logo.jpg" alt="SQL Tools Logo" width="200">
</div>

<div align="center">
  <a href="README.md">English</a> | <a href="README_zh.md">简体中文</a>
</div>



A powerful plugin-based tool that allows you to query multiple file formats including JSON, CSV, and Nginx logs using SQL statements.


## Features

- **Multiple Format Support**: JSON, CSV, Nginx access log, easily extensible
- **Plugin Architecture**: Add new file format support through simple plugin mechanism
- **Automatic Schema Creation**: Automatically infer table schema and column types from file data
- **Interactive Query**: Command-line interactive SQL query interface
- **Format Auto-Detection**: Automatically select appropriate parser based on file extension
- **In-Memory Database**: Uses SQLite in-memory database, no persistent storage required
- **Multi-Language Support**: Available in both Python and Node.js versions

## Installation

### Python Version

This tool only requires Python 3.x, no additional dependencies needed.

```bash
# Clone or download this project
git clone <repository-url>
cd sql-tools
```

### Node.js Version

```bash
# Clone or download this project
git clone <repository-url>
cd sql-tools/nodejs

# Install dependencies
npm install

# Build the project
npm run build

# Install globally (optional)
npm install -g .
```

## Usage

### Python Version

#### Basic Usage

```bash
# Auto-detect format (recommended)
python3 python/sqltools.py <file_path>

# List all supported formats
python3 python/sqltools.py --list-formats

# Force specific format
python3 python/sqltools.py <file_path> --format json|csv|nginx

# Custom table name
python3 python/sqltools.py <file_path> --table <table_name>

# Execute SQL query directly (non-interactive mode, ideal for AI agents)
python3 python/sqltools.py <file_path> --query 'SELECT COUNT(*) FROM table_name'
```

#### Non-Interactive Mode (for AI Agents)

The `--query` option allows you to execute SQL queries directly without entering interactive mode. This is particularly useful for AI agents and automation:

```bash
# Count records
python3 python/sqltools.py data.json --query 'SELECT COUNT(*) FROM data'

# Filter and aggregate
python3 python/sqltools.py data.json --query 'SELECT type, COUNT(*) FROM data GROUP BY type'

# Complex queries
python3 python/sqltools.py data.csv --query 'SELECT department, AVG(salary) as avg_salary FROM data GROUP BY department ORDER BY avg_salary DESC'
```

The output is returned as JSON, making it easy to parse programmatically.

#### JSON Query Example

```bash
python3 python/sqltools.py test.json
```

```sql
-- Query all records
SELECT * FROM test;

-- Filter by condition
SELECT * FROM test WHERE type = 'PROJECT';

-- Group by statistics
SELECT type, COUNT(*) FROM test GROUP BY type;
```

#### CSV Query Example

```bash
python3 python/sqltools.py test.csv
```

```sql
-- View first 5 records
SELECT * FROM test LIMIT 5;

-- Group by department
SELECT department, COUNT(*) FROM test GROUP BY department;

-- Calculate average salary
SELECT department, AVG(salary) FROM test GROUP BY department;
```

#### Nginx Log Query Example

```bash
python3 python/sqltools.py access.log
```

```sql
-- Status code distribution
SELECT status, COUNT(*) FROM test GROUP BY status;

-- Find 4xx/5xx errors
SELECT * FROM test WHERE status >= 400;

-- Top IPs by request count
SELECT remote_addr, COUNT(*) FROM test GROUP BY remote_addr ORDER BY COUNT(*) DESC LIMIT 10;

-- Request count by path
SELECT path, COUNT(*) FROM test GROUP BY path ORDER BY COUNT(*) DESC;
```

### Node.js Version

#### Basic Usage

```bash
# Auto-detect format (recommended)
sqltools <file_path>

# List all supported formats
sqltools --list-formats

# Force specific format
sqltools <file_path> --format json|csv|nginx

# Custom table name
sqltools <file_path> --table <table_name>

# Execute SQL query directly (non-interactive mode, ideal for AI agents)
sqltools <file_path> --query 'SELECT COUNT(*) FROM table_name'
```

#### Non-Interactive Mode (for AI Agents)

The `--query` option allows you to execute SQL queries directly without entering interactive mode. This is particularly useful for AI agents and automation:

```bash
# Count records
sqltools data.json --query 'SELECT COUNT(*) FROM data'

# Filter and aggregate
sqltools data.json --query 'SELECT type, COUNT(*) FROM data GROUP BY type'

# Complex queries
sqltools data.csv --query 'SELECT department, AVG(salary) as avg_salary FROM data GROUP BY department ORDER BY avg_salary DESC'
```

The output is returned as JSON, making it easy to parse programmatically.

#### JSON Query Example

```bash
sqltools test.json
```

```sql
-- Query all records
SELECT * FROM test;

-- Filter by condition
SELECT * FROM test WHERE type = 'PROJECT';

-- Group by statistics
SELECT type, COUNT(*) FROM test GROUP BY type;
```

#### CSV Query Example

```bash
sqltools test.csv
```

```sql
-- View first 5 records
SELECT * FROM test LIMIT 5;

-- Group by department
SELECT department, COUNT(*) FROM test GROUP BY department;

-- Calculate average salary
SELECT department, AVG(salary) FROM test GROUP BY department;
```

#### Nginx Log Query Example

```bash
sqltools access.log
```

```sql
-- Status code distribution
SELECT status, COUNT(*) FROM test GROUP BY status;

-- Find 4xx/5xx errors
SELECT * FROM test WHERE status >= 400;

-- Top IPs by request count
SELECT remote_addr, COUNT(*) FROM test GROUP BY remote_addr ORDER BY COUNT(*) DESC LIMIT 10;

-- Request count by path
SELECT path, COUNT(*) FROM test GROUP BY path ORDER BY COUNT(*) DESC;
```

## Supported File Formats

### JSON (.json)

Supports three JSON formats:

**1. JSON object containing data array**
```json
{
  "code": "success",
  "data": [
    {"id": 1, "name": "Project 1", "type": "PROJECT"},
    {"id": 2, "name": "Project 2", "type": "PROJECT"}
  ]
}
```

**2. Direct JSON array**
```json
[
  {"id": 1, "name": "Project 1", "type": "PROJECT"},
  {"id": 2, "name": "Project 2", "type": "PROJECT"}
]
```

**3. Single JSON object**
```json
{"id": 1, "name": "Project 1", "type": "PROJECT"}
```

### CSV (.csv, .tsv)

Supports standard CSV/TSV files:

```csv
id,name,age,department,salary
1,Alice,28,Engineering,95000
2,Bob,32,Marketing,87000
3,Charlie,25,Engineering,82000
```

- Auto-detect delimiter (comma, tab)
- Auto-infer data types (integer, float, text)
- Supports header format

### Nginx Log (.log, .access.log)

Supports Nginx Combined format:

```
127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/test HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.100 - - [10/Oct/2023:13:55:37 +0000] "POST /api/login HTTP/1.1" 200 567 "http://example.com" "curl/7.68.0"
```

Parsed fields include:
- `remote_addr` - Client IP address
- `time_local` - Access time (converted to ISO format)
- `request` / `method` / `path` / `protocol` - Request details
- `status` - HTTP status code (integer)
- `body_bytes_sent` - Response bytes sent (integer)
- `http_referer` - Referrer page
- `http_user_agent` - User agent

## Project Structure

```
sql-tools/
├── python/                  # Python implementation
│   ├── sqltools.py          # Main entry point
│   ├── core/
│   │   ├── engine.py        # SQL query execution engine
│   │   ├── schema.py        # Table schema inference module
│   │   └── registry.py      # Plugin registry
│   ├── parsers/
│   │   ├── base.py          # Parser base class
│   │   ├── json_parser.py   # JSON parser
│   │   ├── csv_parser.py    # CSV parser
│   │   └── nginx_parser.py  # Nginx log parser
│   └── jsonsql.py           # Legacy entry point (backward compatible)
├── nodejs/                  # Node.js implementation
│   ├── src/
│   │   ├── cli.ts           # CLI entry point
│   │   ├── core/
│   │   │   ├── engine.ts    # SQL query execution engine
│   │   │   ├── schema.ts    # Table schema inference module
│   │   │   └── registry.ts  # Plugin registry
│   │   └── parsers/
│   │       ├── base.ts      # Parser base class
│   │       ├── json_parser.ts   # JSON parser
│   │       ├── csv_parser.ts    # CSV parser
│   │       └── nginx_parser.ts  # Nginx log parser
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Extension Development

### Python Version

Adding new file format support is simple, just create a new parser class:

```python
# parsers/xml_parser.py
from parsers.base import BaseParser
from typing import List, Dict, Any

class XMLParser(BaseParser):
    format_name = "xml"
    file_extensions = ['.xml']

    def supports_format(self, file_path: str) -> bool:
        return file_path.lower().endswith('.xml')

    def load(self, file_path: str) -> List[Dict[str, Any]]:
        # Parse XML and return list of dicts
        pass
```

Then register in `sqltools.py`:

```python
from parsers.xml_parser import XMLParser
registry.register(XMLParser)
```

### Node.js Version

Adding new file format support is similar:

```typescript
// parsers/xml_parser.ts
import { BaseParser, ParserData } from './base';

export class XMLParser extends BaseParser {
  formatName = 'xml';
  fileExtensions = ['.xml'];
  mimeTypes = ['application/xml', 'text/xml'];

  supportsFormat(filePath: string): boolean {
    return filePath.toLowerCase().endsWith('.xml');
  }

  load(filePath: string): ParserData[] {
    // Parse XML and return list of objects
    return [];
  }
}
```

Then register in `core/registry.ts`:

```typescript
import { XMLParser } from '../parsers/xml_parser';

// In constructor
this.register(XMLParser);
```

## Technical Implementation

### Python Version

- **Architecture Pattern**: Plugin architecture, Strategy pattern + Registry pattern
- **Data Parsing**: Uses Python standard library (json, csv, re)
- **SQL Engine**: Uses `sqlite3` in-memory database
- **Type Inference**: Auto-infer column types (INTEGER, REAL, BOOLEAN, TEXT)
- **CLI**: Uses `argparse` for command-line argument handling

### Node.js Version

- **Architecture Pattern**: Plugin architecture, Strategy pattern + Registry pattern
- **Data Parsing**: Uses Node.js built-in modules (fs, path)
- **SQL Engine**: Uses `sql.js` (SQLite compiled to WebAssembly)
- **Type Inference**: Auto-infer column types (INTEGER, REAL, TEXT)
- **CLI**: Uses `commander` for command-line argument handling
- **Language**: TypeScript for type safety

## Notes

1. Large files consume significant memory as the tool loads the entire file into memory
2. Column types are inferred from the first data item, subsequent different types may cause conversion issues
3. Table names are auto-generated from filename, special characters are replaced with underscores
4. Supported SQL features depend on SQLite implementation

## Backward Compatibility

### Python Version

The old `jsonsql.py` remains available with unchanged functionality:

```bash
python3 python/jsonsql.py test.json
```

## Example Output

```bash
$ sqltools test.log

Detected format: nginx
Loaded 12 records into table 'test'
Enter SQL queries, type 'exit' or 'quit' to exit

SQL> SELECT status, COUNT(*) FROM test GROUP BY status;

Columns: [status, COUNT(*)]
Found 6 records:
Record 1: {"status":200,"COUNT(*)":6}
Record 2: {"status":304,"COUNT(*)":1}
Record 3: {"status":401,"COUNT(*)":1}
Record 4: {"status":403,"COUNT(*)":1}
Record 5: {"status":404,"COUNT(*)":2}
Record 6: {"status":500,"COUNT(*)":1}

SQL> exit
```

## License

This project is licensed under the MIT License.
