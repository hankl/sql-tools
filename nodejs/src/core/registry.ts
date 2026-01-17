import * as path from 'path';
import { BaseParser, ParserData } from '../parsers/base';
import { JSONParser } from '../parsers/json_parser';
import { CSVParser } from '../parsers/csv_parser';
import { NginxParser } from '../parsers/nginx_parser';

export interface FormatInfo {
  name: string;
  displayName: string;
  extensions: string[];
  mimeTypes: string[];
}

export class ParserRegistry {
  private parsers: Map<string, typeof BaseParser> = new Map();
  private extensionMap: Map<string, string> = new Map();

  constructor() {
    this.register(JSONParser);
    this.register(CSVParser);
    this.register(NginxParser);
  }

  register(parserClass: any): void {
    const parser = new parserClass() as BaseParser;
    const formatName = parser.formatName;

    this.parsers.set(formatName, parserClass);

    for (const ext of parser.fileExtensions) {
      const normalizedExt = ext.startsWith('.') ? ext.toLowerCase() : '.' + ext.toLowerCase();
      this.extensionMap.set(normalizedExt, formatName);
    }
  }

  getParser(formatName: string): BaseParser | null {
    const parserClass = this.parsers.get(formatName);
    return parserClass ? new parserClass() as BaseParser : null;
  }

  detectFormat(filePath: string): string | null {
    const ext = path.extname(filePath).toLowerCase();
    return this.extensionMap.get(ext) || null;
  }

  findParserForFile(filePath: string, formatHint?: string): BaseParser | null {
    if (formatHint) {
      const parser = this.getParser(formatHint);
      if (parser && parser.supportsFormat(filePath)) {
        return parser;
      }
    }

    const formatName = this.detectFormat(filePath);
    if (formatName) {
      const parser = this.getParser(formatName);
      if (parser && parser.supportsFormat(filePath)) {
        return parser;
      }
    }

    for (const parserClass of this.parsers.values()) {
      const parser = new parserClass() as BaseParser;
      if (parser.supportsFormat(filePath)) {
        return parser;
      }
    }

    return null;
  }

  listSupportedFormats(): FormatInfo[] {
    const formats: FormatInfo[] = [];
    for (const [formatName, parserClass] of this.parsers) {
      const parser = new parserClass() as BaseParser;
      formats.push({
        name: formatName,
        displayName: parser.getDisplayName(),
        extensions: parser.fileExtensions,
        mimeTypes: parser.mimeTypes
      });
    }
    return formats;
  }
}

export const registry = new ParserRegistry();
