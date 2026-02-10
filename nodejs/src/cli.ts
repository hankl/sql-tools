#!/usr/bin/env node

import { Command } from 'commander';
import { registry } from './core/registry';
import { SQLEngine } from './core/engine';
import * as path from 'path';

const program = new Command();

program
  .name('sqltools')
  .description('A powerful plugin-based tool that allows you to query multiple file formats including JSON, CSV, and Nginx logs using SQL statements')
  .version('1.0.0');

program
  .argument('[file_path]', 'Path to the file to query')
  .option('-f, --format <format>', 'Force specific format (json, csv, nginx)')
  .option('-t, --table <table_name>', 'Custom table name')
  .option('-q, --query <sql_query>', 'Execute SQL query directly (non-interactive mode)')
  .option('-l, --list-formats', 'List all supported formats')
  .action(async (filePath: string | undefined, options: any) => {
    if (options.listFormats) {
      const formats = registry.listSupportedFormats();
      console.log('\nSupported formats:');
      for (const format of formats) {
        console.log(`  ${format.displayName} (${format.name}): ${format.extensions.join(', ')}`);
      }
      console.log();
      return;
    }

    if (!filePath) {
      program.outputHelp();
      return;
    }

    const absolutePath = path.resolve(filePath);

    const parser = registry.findParserForFile(absolutePath, options.format);
    if (!parser) {
      console.error(`Error: No suitable parser found for file: ${filePath}`);
      console.error('Use --list-formats to see supported formats');
      process.exit(1);
    }

    console.log(`Detected format: ${parser.formatName}`);

    const data = parser.load(absolutePath);
    const tableName = options.table || parser.getTableName(absolutePath);

    const engine = new SQLEngine();
    await engine.loadData(data, tableName);

    if (options.query) {
      const results = engine.executeQuery(options.query);
      if (results !== null) {
        console.log(JSON.stringify(results, null, 2));
      }
    } else {
      await engine.runRepl(tableName);
    }

    engine.close();
  });

program.parse(process.argv);
