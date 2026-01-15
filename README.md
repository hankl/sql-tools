# JSON SQL 查询工具

一个简单但强大的工具，允许您使用SQL语句查询JSON文件中的数据。

## 功能特点

- **自动表结构创建**：根据JSON数据自动推断表结构和列类型
- **交互式查询**：提供命令行交互式SQL查询界面
- **支持多种JSON格式**：
  - 包含`data`数组的JSON对象
  - 直接的JSON数组
  - 单个JSON对象（会自动转换为单元素数组）
- **内存数据库**：使用SQLite内存数据库，无需持久化存储
- **错误处理**：提供友好的错误提示

## 安装

该工具是一个独立的Python脚本，只需确保您的系统已安装Python 3。

1. 克隆或下载本项目到本地
2. 确保`jsonsql.py`文件有执行权限

## 使用方法

### 基本用法

```bash
python3 jsonsql.py <json文件路径>
```

### 示例

使用默认表名（data）查询JSON文件：

```bash
python3 jsonsql.py test.json
```

指定自定义表名：

```bash
python3 jsonsql.py test.json --table projects
```

### 交互式查询

运行工具后，您将进入交互式SQL查询界面。在提示符`SQL>`后输入SQL查询语句，例如：

```sql
-- 查询所有记录
SELECT * FROM data;

-- 按条件筛选
SELECT * FROM data WHERE type = 'PROJECT';

-- 统计记录数
SELECT COUNT(*) FROM data;

-- 分组统计
SELECT type, COUNT(*) FROM data GROUP BY type;
```

输入`exit`、`quit`或直接按回车键退出程序。

## 支持的JSON格式

### 1. 包含data数组的JSON对象

```json
{
  "code": "success",
  "data": [
    {"id": 1, "name": "项目1", "type": "PROJECT"},
    {"id": 2, "name": "项目2", "type": "PROJECT"}
  ],
  "message": ""
}
```

### 2. 直接的JSON数组

```json
[
  {"id": 1, "name": "项目1", "type": "PROJECT"},
  {"id": 2, "name": "项目2", "type": "PROJECT"}
]
```

### 3. 单个JSON对象

```json
{"id": 1, "name": "项目1", "type": "PROJECT"}
```

## 技术实现

- 使用Python标准库中的`json`模块解析JSON文件
- 使用`sqlite3`模块创建内存数据库和执行SQL查询
- 使用`argparse`模块处理命令行参数
- 自动根据JSON数据类型推断SQLite列类型

## 注意事项

1. 对于大型JSON文件，可能会占用较多内存，因为工具会将整个JSON加载到内存中
2. 列类型是根据第一个数据项的值类型推断的，如果后续数据项的类型与第一个不同，可能会导致类型转换
3. 支持的SQL语句取决于SQLite的实现

## 示例输出

```
已加载 1000 条记录到表 'data' 中
请输入SQL查询语句，输入 'exit' 或 'quit' 退出程序

SQL> SELECT type, COUNT(*) FROM data GROUP BY type;

列名: ['type', 'COUNT(*)']
找到 2 条记录:
记录 1: {'type': 'ORG', 'COUNT(*)': 41}
记录 2: {'type': 'PROJECT', 'COUNT(*)': 959}

SQL> exit
```

## 许可证

本项目采用MIT许可证。
