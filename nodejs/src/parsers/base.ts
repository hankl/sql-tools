import * as fs from 'fs';
import * as path from 'path';

export interface ParserData {
  [key: string]: any;
}

export class BaseParser {
  formatName: string = 'base';
  fileExtensions: string[] = [];
  mimeTypes: string[] = [];

  supportsFormat(filePath: string): boolean {
    throw new Error('Method not implemented.');
  }

  load(filePath: string): ParserData[] {
    throw new Error('Method not implemented.');
  }

  getTableName(filePath: string): string {
    const basename = path.basename(filePath);
    const nameWithoutExt = path.parse(basename).name;
    
    let tableName = nameWithoutExt
      .replace(/-/g, '_')
      .replace(/ /g, '_')
      .replace(/\./g, '_');

    if (tableName && /^\d/.test(tableName)) {
      tableName = 't_' + tableName;
    }

    return tableName || 'data';
  }

  getDisplayName(): string {
    return this.formatName;
  }

  validateFile(filePath: string): { isValid: boolean; error: string } {
    if (!fs.existsSync(filePath)) {
      return { isValid: false, error: `File not found: ${filePath}` };
    }
    if (!fs.statSync(filePath).isFile()) {
      return { isValid: false, error: `Path is not a file: ${filePath}` };
    }
    return { isValid: true, error: '' };
  }
}
