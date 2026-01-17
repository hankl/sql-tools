import initSqlJs, { Database, SqlJsStatic } from 'sql.js';
import * as readline from 'readline';
import { ParserData } from '../parsers/base';
import { SchemaInference } from './schema';

export class SQLEngine {
  private db: Database | null = null;
  private SQL: SqlJsStatic | null = null;

  async init(): Promise<void> {
    this.SQL = await initSqlJs();
    this.db = new this.SQL.Database();
  }

  async loadData(data: ParserData[], tableName: string = 'data'): Promise<void> {
    if (!this.SQL) {
      await this.init();
    }
    if (!this.db) {
      throw new Error('Database not initialized');
    }

    await SchemaInference.createTableFromData(this.db, tableName, data);
    console.log(`Loaded ${data.length} records into table '${tableName}'`);
  }

  executeQuery(sqlQuery: string): any[] | null {
    if (!this.db) {
      throw new Error('No data loaded. Call loadData() first.');
    }

    const trimmedQuery = sqlQuery.trim().toUpperCase();
    const isSelect = trimmedQuery.startsWith('SELECT');

    if (isSelect) {
      const stmt = this.db.exec(sqlQuery);
      if (stmt.length === 0) {
        return [];
      }

      const columns = stmt[0].columns;
      const values = stmt[0].values;

      return values.map((row: any[]) => {
        const obj: any = {};
        columns.forEach((col: string, index: number) => {
          obj[col] = row[index];
        });
        return obj;
      });
    } else {
      this.db.run(sqlQuery);
      return null;
    }
  }

  getColumnNames(lastQuery: string): string[] | null {
    if (!this.db) {
      return null;
    }

    try {
      const stmt = this.db.exec(lastQuery);
      if (stmt.length === 0) {
        return null;
      }
      return stmt[0].columns;
    } catch {
      return null;
    }
  }

  async runRepl(tableName: string = 'data'): Promise<void> {
    console.log('\nEnter SQL queries, type \'exit\' or \'quit\' to exit\n');

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const askQuestion = (query: string): Promise<string> => {
      return new Promise((resolve) => {
        rl.question(query, (answer: string) => {
          resolve(answer);
        });
      });
    };

    while (true) {
      try {
        const sqlQuery = await askQuestion('SQL> ');
        const trimmedQuery = sqlQuery.trim();

        if (trimmedQuery.toLowerCase() === 'exit' || trimmedQuery.toLowerCase() === 'quit' || trimmedQuery === '') {
          break;
        }

        const results = this.executeQuery(sqlQuery);

        if (trimmedQuery.toUpperCase().startsWith('SELECT')) {
          const columnNames = this.getColumnNames(sqlQuery);

          if (columnNames) {
            console.log(`\nColumns: [${columnNames.join(', ')}]`);
          }

          if (results && results.length > 0) {
            console.log(`Found ${results.length} records:`);
            for (let i = 0; i < results.length; i++) {
              console.log(`Record ${i + 1}: ${JSON.stringify(results[i])}`);
            }
          } else {
            console.log('No matching records found');
          }
        } else {
          console.log('Execution completed');
        }
      } catch (error) {
        console.error(`SQL Error: ${error instanceof Error ? error.message : String(error)}`);
      }
    }

    rl.close();
  }

  close(): void {
    if (this.db) {
      this.db.close();
      this.db = null;
    }
  }
}
