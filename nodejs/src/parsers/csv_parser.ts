import * as fs from 'fs';
import { BaseParser, ParserData } from './base';

export class CSVParser extends BaseParser {
  formatName = 'csv';
  fileExtensions = ['.csv', '.tsv'];
  mimeTypes = ['text/csv', 'text/tab-separated-values'];

  supportsFormat(filePath: string): boolean {
    const ext = filePath.toLowerCase().split('.').pop();
    return ext === 'csv' || ext === 'tsv';
  }

  load(filePath: string): ParserData[] {
    const validation = this.validateFile(filePath);
    if (!validation.isValid) {
      console.error(`Error: ${validation.error}`);
      process.exit(1);
    }

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.trim().split('\n');
      
      if (lines.length === 0) {
        return [];
      }

      const delimiter = this.detectDelimiter(lines[0]);
      const headers = lines[0].split(delimiter);
      const data: ParserData[] = [];

      for (let i = 1; i < lines.length; i++) {
        const values = this.parseCSVLine(lines[i], delimiter);
        const row: ParserData = {};
        
        for (let j = 0; j < headers.length; j++) {
          const header = headers[j].trim();
          const value = values[j] !== undefined ? values[j].trim() : '';
          row[header] = this.inferType(value);
        }
        
        data.push(row);
      }

      return data;
    } catch (error) {
      console.error(`Error reading CSV: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(1);
    }
  }

  private detectDelimiter(line: string): string {
    if (line.includes('\t')) return '\t';
    if (line.includes(',')) return ',';
    return ',';
  }

  private parseCSVLine(line: string, delimiter: string): string[] {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === delimiter && !inQuotes) {
        result.push(current);
        current = '';
      } else {
        current += char;
      }
    }
    
    result.push(current);
    return result;
  }

  private inferType(value: string): any {
    if (value === '') return null;
    
    if (!isNaN(Number(value)) && value.trim() !== '') {
      if (value.includes('.')) {
        return parseFloat(value);
      }
      return parseInt(value, 10);
    }
    
    return value;
  }
}
