import * as fs from 'fs';
import { BaseParser, ParserData } from './base';

export class JSONParser extends BaseParser {
  formatName = 'json';
  fileExtensions = ['.json'];
  mimeTypes = ['application/json'];

  supportsFormat(filePath: string): boolean {
    return filePath.toLowerCase().endsWith('.json');
  }

  load(filePath: string): ParserData[] {
    const validation = this.validateFile(filePath);
    if (!validation.isValid) {
      console.error(`Error: ${validation.error}`);
      process.exit(1);
    }

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const jsonData = JSON.parse(content);

      if ('data' in jsonData && Array.isArray(jsonData.data)) {
        return jsonData.data;
      }

      if (Array.isArray(jsonData)) {
        return jsonData;
      }

      if (typeof jsonData === 'object' && jsonData !== null) {
        return [jsonData];
      }

      throw new Error('Unsupported JSON structure');
    } catch (error) {
      if (error instanceof SyntaxError) {
        console.error(`Error: File ${filePath} is not valid JSON format: ${error.message}`);
      } else {
        console.error(`Error: ${error instanceof Error ? error.message : String(error)}`);
      }
      process.exit(1);
    }
  }
}
