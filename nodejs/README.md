# sql-tools

A powerful plugin-based tool that allows you to query multiple file formats including JSON, CSV, and Nginx logs using SQL statements.

## Features

- **Multiple Format Support**: JSON, CSV, Nginx access log, easily extensible
- **Plugin Architecture**: Add new file format support through simple plugin mechanism
- **Automatic Schema Creation**: Automatically infer table schema and column types from file data
- **Interactive Query**: Command-line interactive SQL query interface
- **Format Auto-Detection**: Automatically select appropriate parser based on file extension
- **In-Memory Database**: Uses SQLite in-memory database, no persistent storage required

## Installation

```bash
npm install -g sql-tools
```

Or use with npx (no installation required):

```bash
npx sql-tools <file_path>
```

## Usage

### Basic Usage

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

# Show help
sqltools --help
```

### Non-Interactive Mode (for AI Agents)

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

### JSON Query Example

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

### CSV Query Example

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

### Nginx Log Query Example

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

## Notes

1. Large files consume significant memory as the tool loads the entire file into memory
2. Column types are inferred from the first data item, subsequent different types may cause conversion issues
3. Table names are auto-generated from filename, special characters are replaced with underscores
4. Supported SQL features depend on SQLite implementation

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues

If you find a bug or have a feature request, please [create an issue](https://github.com/yourusername/sql-tools/issues).
