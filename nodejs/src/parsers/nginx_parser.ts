import * as fs from 'fs';
import { BaseParser, ParserData } from './base';

export class NginxParser extends BaseParser {
  formatName = 'nginx';
  fileExtensions = ['.log', '.access.log'];
  mimeTypes = ['text/plain'];

  private readonly LOG_PATTERN = /^(\S+) (\S+) (\S+) \[([^\]]+)\] "((\S+) (\S+) (\S+))" (\d+) (\d+) "([^"]*)" "([^"]*)"$/;

  supportsFormat(filePath: string): boolean {
    if (!filePath.toLowerCase().endsWith('.log') && !filePath.toLowerCase().endsWith('.access.log')) {
      return false;
    }

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const firstLine = content.split('\n')[0].trim();
      return this.LOG_PATTERN.test(firstLine);
    } catch {
      return false;
    }
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
      const data: ParserData[] = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        const match = line.match(this.LOG_PATTERN);
        if (match) {
          const logEntry: ParserData = {
            remote_addr: match[1],
            remote_user: match[2],
            auth_user: match[3],
            time_local: this.parseNginxTimestamp(match[4]),
            request: match[5],
            method: match[6],
            path: match[7],
            protocol: match[8],
            status: parseInt(match[9], 10),
            body_bytes_sent: parseInt(match[10], 10),
            http_referer: match[11] === '-' ? null : match[11],
            http_user_agent: match[12] === '-' ? null : match[12],
          };

          data.push(logEntry);
        } else {
          console.warn(`Warning: Unable to parse line ${i + 1}`);
        }
      }

      return data;
    } catch (error) {
      console.error(`Error reading log file: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(1);
    }
  }

  private parseNginxTimestamp(timestampStr: string): string {
    try {
      const parts = timestampStr.split(' ');
      const datePart = parts[0];
      
      const [day, month, yearTime] = datePart.split('/');
      const [year, time] = yearTime.split(':');
      const [hour, minute, second] = time.split(':');
      
      const monthMap: { [key: string]: number } = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
      };
      
      const monthNum = monthMap[month];
      const date = new Date(
        parseInt(year, 10),
        monthNum,
        parseInt(day, 10),
        parseInt(hour, 10),
        parseInt(minute, 10),
        parseInt(second, 10)
      );
      
      return date.toISOString();
    } catch {
      return timestampStr;
    }
  }
}
