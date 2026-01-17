import initSqlJs, { Database, SqlJsStatic } from 'sql.js';
import { ParserData } from '../parsers/base';

export interface ColumnInfo {
  name: string;
  type: string;
}

export class SchemaInference {
  static inferColumnType(value: any): string {
    if (value === null || value === undefined) {
      return 'TEXT';
    }
    if (typeof value === 'boolean') {
      return 'INTEGER';
    }
    if (typeof value === 'number') {
      return Number.isInteger(value) ? 'INTEGER' : 'REAL';
    }
    return 'TEXT';
  }

  static getAllKeys(data: ParserData[]): Set<string> {
    const allKeys = new Set<string>();
    for (const item of data) {
      for (const key of Object.keys(item)) {
        allKeys.add(key);
      }
    }
    return allKeys;
  }

  static async createTableFromData(db: Database, tableName: string, data: ParserData[]): Promise<void> {
    if (data.length === 0) {
      return;
    }

    const allKeys = Array.from(this.getAllKeys(data)).sort();

    const columns = allKeys.map(key => {
      const firstValue = data[0][key];
      const colType = this.inferColumnType(firstValue);
      return `[${key}] ${colType}`;
    });

    const createSQL = `CREATE TABLE [${tableName}] (${columns.join(', ')})`;
    db.run(createSQL);

    const insertSQL = `INSERT INTO [${tableName}] VALUES (${allKeys.map(() => '?').join(', ')})`;

    for (const item of data) {
      const values = allKeys.map(key => item[key]);
      db.run(insertSQL, values);
    }
  }

  static getTableInfo(db: Database, tableName: string): ColumnInfo[] {
    const stmt = db.exec(`PRAGMA table_info([${tableName}])`);
    if (stmt.length === 0) {
      return [];
    }

    const columns = stmt[0].columns;
    const values = stmt[0].values;

    return values.map((row: any[]) => ({
      name: row[1] as string,
      type: row[2] as string
    }));
  }
}
