#!/usr/bin/env node

const yargs = require('yargs');
const fs = require('fs');
const path = require('path');
const FMPApi = require('./lib/api');
const Formatter = require('./lib/formatter');

// Load configuration
let config = {};
try {
  const configPath = path.join(__dirname, '../config.json');
  if (fs.existsSync(configPath)) {
    const configContent = fs.readFileSync(configPath, 'utf8');
    config = JSON.parse(configContent);
  }
} catch (error) {
  console.error('Warning: Could not load config file:', error.message);
}

// Initialize API client
let api;
try {
  api = new FMPApi(config);
} catch (error) {
  if (error.message.includes('FMP_API_KEY')) {
    console.error('Error: FMP_API_KEY environment variable is required');
    console.error('Please set it using: export FMP_API_KEY=your_api_key');
    process.exit(1);
  }
  console.error('Error initializing FMP API:', error.message);
  process.exit(1);
}

// Main CLI
const argv = yargs
  .usage('Usage: $0 <command> [options]')
  .command('quote [symbols]', 'Get stock quote(s)', (yargs) => {
    return yargs
      .positional('symbols', {
        describe: 'Stock symbol(s) - comma separated for multiple',
        type: 'string'
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbols) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const symbols = argv.symbols.split(',');
      let result;
      
      if (symbols.length === 1) {
        result = await api.getQuote(symbols[0]);
      } else {
        result = await api.getBatchQuotes(symbols);
      }
      
      if (argv.csv) {
        const outputFile = argv.output || 'quotes.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('profile [symbol]', 'Get company profile', (yargs) => {
    return yargs
      .positional('symbol', {
        describe: 'Stock symbol',
        type: 'string'
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbol) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const result = await api.getProfile(argv.symbol);
      
      if (argv.csv) {
        const outputFile = argv.output || 'profile.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('income [symbol]', 'Get income statement', (yargs) => {
    return yargs
      .positional('symbol', {
        describe: 'Stock symbol',
        type: 'string'
      })
      .option('period', {
        describe: 'Period type',
        choices: ['annual', 'quarterly'],
        default: 'annual'
      })
      .option('limit', {
        describe: 'Number of periods to return',
        type: 'number',
        default: 5
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbol) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const result = await api.getIncomeStatement(argv.symbol, argv.period, argv.limit);
      
      if (argv.csv) {
        const outputFile = argv.output || 'income.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('balance [symbol]', 'Get balance sheet', (yargs) => {
    return yargs
      .positional('symbol', {
        describe: 'Stock symbol',
        type: 'string'
      })
      .option('period', {
        describe: 'Period type',
        choices: ['annual', 'quarterly'],
        default: 'annual'
      })
      .option('limit', {
        describe: 'Number of periods to return',
        type: 'number',
        default: 5
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbol) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const result = await api.getBalanceSheet(argv.symbol, argv.period, argv.limit);
      
      if (argv.csv) {
        const outputFile = argv.output || 'balance.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('cashflow [symbol]', 'Get cash flow statement', (yargs) => {
    return yargs
      .positional('symbol', {
        describe: 'Stock symbol',
        type: 'string'
      })
      .option('period', {
        describe: 'Period type',
        choices: ['annual', 'quarterly'],
        default: 'annual'
      })
      .option('limit', {
        describe: 'Number of periods to return',
        type: 'number',
        default: 5
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbol) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const result = await api.getCashFlow(argv.symbol, argv.period, argv.limit);
      
      if (argv.csv) {
        const outputFile = argv.output || 'cashflow.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('metrics [symbol]', 'Get key metrics', (yargs) => {
    return yargs
      .positional('symbol', {
        describe: 'Stock symbol',
        type: 'string'
      })
      .option('period', {
        describe: 'Period type',
        choices: ['annual', 'quarterly'],
        default: 'annual'
      })
      .option('limit', {
        describe: 'Number of periods to return',
        type: 'number',
        default: 5
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.symbol) {
        console.error('Error: Symbol is required');
        process.exit(1);
      }
      
      const result = await api.getKeyMetrics(argv.symbol, argv.period, argv.limit);
      
      if (argv.csv) {
        const outputFile = argv.output || 'metrics.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('search <query>', 'Search for stocks', (yargs) => {
    return yargs
      .positional('query', {
        describe: 'Search query',
        type: 'string'
      })
      .option('csv', {
        describe: 'Export to CSV',
        type: 'boolean'
      })
      .option('output', {
        describe: 'Output file for CSV export',
        type: 'string'
      });
  }, async (argv) => {
    try {
      if (!argv.query) {
        console.error('Error: Query is required');
        process.exit(1);
      }
      
      const result = await api.searchSymbol(argv.query);
      
      if (argv.csv) {
        const outputFile = argv.output || 'search.csv';
        const message = await Formatter.exportToCsv(result, outputFile);
        console.log(message);
      } else {
        console.log(Formatter.formatJson(result, true));
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .command('cache <action>', 'Manage cache', (yargs) => {
    return yargs
      .positional('action', {
        describe: 'Cache action',
        choices: ['clear', 'stats'],
        type: 'string'
      });
  }, (argv) => {
    try {
      if (argv.action === 'clear') {
        api.clearCache();
        console.log('Cache cleared successfully');
      } else if (argv.action === 'stats') {
        const stats = api.getCacheStats();
        console.log(`Cache Stats:
  Files: ${stats.files}
  Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })
  .option('format', {
    describe: 'Output format',
    choices: ['json', 'table'],
    default: 'json'
  })
  .option('no-cache', {
    describe: 'Disable caching',
    type: 'boolean'
  })
  .help()
  .alias('help', 'h')
  .argv;

// If no command was provided, show help
if (!argv._[0]) {
  yargs.showHelp();
}