# SQL Tools - 多格式 SQL 查询工具

一个强大的插件化工具，允许您使用 SQL 语句查询 JSON、CSV、Nginx 日志等多种文件格式。

## 功能特点

- **多格式支持**：JSON、CSV、Nginx access log，易于扩展
- **插件化架构**：通过简单的插件机制添加新的文件格式支持
- **自动表结构创建**：根据文件数据自动推断表结构和列类型
- **交互式查询**：提供命令行交互式 SQL 查询界面
- **格式自动检测**：根据文件扩展名自动选择合适的解析器
- **内存数据库**：使用 SQLite 内存数据库，无需持久化存储
- **零外部依赖**：仅使用 Python 标准库

## 安装

该工具仅需要 Python 3.x，无需安装额外依赖。

```bash
# 克隆或下载本项目
git clone <repository-url>
cd sql-tools
```

## 使用方法

### 基本用法

```bash
# 自动检测格式（推荐）
python3 sqltools.py <文件路径>

# 列出所有支持的格式
python3 sqltools.py --list-formats

# 强制指定格式
python3 sqltools.py <文件路径> --format json|csv|nginx

# 自定义表名
python3 sqltools.py <文件路径> --table <表名>
```

### JSON 查询示例

```bash
python3 sqltools.py test.json
```

```sql
-- 查询所有记录
SELECT * FROM test;

-- 按条件筛选
SELECT * FROM test WHERE type = 'PROJECT';

-- 分组统计
SELECT type, COUNT(*) FROM test GROUP BY type;
```

### CSV 查询示例

```bash
python3 sqltools.py test.csv
```

```sql
-- 查看前 5 条记录
SELECT * FROM test LIMIT 5;

-- 按部门统计
SELECT department, COUNT(*) FROM test GROUP BY department;

-- 计算平均薪资
SELECT department, AVG(salary) FROM test GROUP BY department;
```

### Nginx 日志查询示例

```bash
python3 sqltools.py access.log
```

```sql
-- 统计状态码分布
SELECT status, COUNT(*) FROM test GROUP BY status;

-- 查找 4xx/5xx 错误
SELECT * FROM test WHERE status >= 400;

-- 统计访问最多的 IP
SELECT remote_addr, COUNT(*) FROM test GROUP BY remote_addr ORDER BY COUNT(*) DESC LIMIT 10;

-- 按路径统计请求量
SELECT path, COUNT(*) FROM test GROUP BY path ORDER BY COUNT(*) DESC;
```

## 支持的文件格式

### JSON (.json)

支持三种 JSON 格式：

**1. 包含 data 数组的 JSON 对象**
```json
{
  "code": "success",
  "data": [
    {"id": 1, "name": "项目1", "type": "PROJECT"},
    {"id": 2, "name": "项目2", "type": "PROJECT"}
  ]
}
```

**2. 直接的 JSON 数组**
```json
[
  {"id": 1, "name": "项目1", "type": "PROJECT"},
  {"id": 2, "name": "项目2", "type": "PROJECT"}
]
```

**3. 单个 JSON 对象**
```json
{"id": 1, "name": "项目1", "type": "PROJECT"}
```

### CSV (.csv, .tsv)

支持标准的 CSV/TSV 文件：

```csv
id,name,age,department,salary
1,Alice,28,Engineering,95000
2,Bob,32,Marketing,87000
3,Charlie,25,Engineering,82000
```

- 自动检测分隔符（逗号、制表符）
- 自动推断数据类型（整数、浮点数、文本）
- 支持带 header 的格式

### Nginx 日志 (.log, .access.log)

支持 Nginx Combined 格式：

```
127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/test HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.100 - - [10/Oct/2023:13:55:37 +0000] "POST /api/login HTTP/1.1" 200 567 "http://example.com" "curl/7.68.0"
```

解析字段包括：
- `remote_addr` - 客户端 IP 地址
- `time_local` - 访问时间（转换为 ISO 格式）
- `request` / `method` / `path` / `protocol` - 请求详情
- `status` - HTTP 状态码（整数）
- `body_bytes_sent` - 响应字节数（整数）
- `http_referer` - 来源页面
- `http_user_agent` - 用户代理

## 项目结构

```
sql-tools/
├── sqltools.py              # 主入口程序
├── core/
│   ├── engine.py            # SQL 查询执行引擎
│   ├── schema.py            # 表结构推断模块
│   └── registry.py          # 插件注册表
├── parsers/
│   ├── base.py              # 解析器基类
│   ├── json_parser.py       # JSON 解析器
│   ├── csv_parser.py        # CSV 解析器
│   └── nginx_parser.py      # Nginx 日志解析器
└── jsonsql.py               # 旧版入口（向后兼容）
```

## 扩展开发

添加新文件格式支持非常简单，只需创建一个新的解析器类：

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
        # 解析 XML 并返回字典列表
        pass
```

然后在 `sqltools.py` 中注册：

```python
from parsers.xml_parser import XMLParser
registry.register(XMLParser)
```

## 技术实现

- **架构模式**：插件化架构，策略模式 + 注册表模式
- **数据解析**：使用 Python 标准库（json、csv、re）
- **SQL 引擎**：使用 `sqlite3` 内存数据库
- **类型推断**：自动推断列类型（INTEGER、REAL、BOOLEAN、TEXT）
- **CLI**：使用 `argparse` 处理命令行参数

## 注意事项

1. 大型文件会占用较多内存，因为工具会将整个文件加载到内存中
2. 列类型根据第一个数据项推断，后续不同类型可能导致转换问题
3. 表名自动从文件名生成，特殊字符会被替换为下划线
4. 支持的 SQL 功能取决于 SQLite 实现

## 向后兼容

旧版 `jsonsql.py` 仍然可用，功能保持不变：

```bash
python3 jsonsql.py test.json
```

## 示例输出

```bash
$ python3 sqltools.py test.log

检测到格式: nginx
已加载 12 条记录到表 'test' 中
请输入SQL查询语句，输入 'exit' 或 'quit' 退出程序

SQL> SELECT status, COUNT(*) FROM test GROUP BY status;

列名: ['status', 'COUNT(*)']
找到 6 条记录:
记录 1: {'status': 200, 'COUNT(*)': 6}
记录 2: {'status': 304, 'COUNT(*)': 1}
记录 3: {'status': 401, 'COUNT(*)': 1}
记录 4: {'status': 403, 'COUNT(*)': 1}
记录 5: {'status': 404, 'COUNT(*)': 2}
记录 6: {'status': 500, 'COUNT(*)': 1}

SQL> exit
```

## 许可证

本项目采用 MIT 许可证。
