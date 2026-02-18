# FMP Skill User Guide

## Overview

The FMP (Financial Modeling Prep) Skill provides access to comprehensive financial data through the Financial Modeling Prep API. It includes real-time stock quotes, historical data, financial statements, company profiles, and much more.

## Prerequisites

1. **API Key**: You need to register at [Financial Modeling Prep](https://site.financialmodelingprep.com/) to get an API key.
2. **Environment Variable**: Set the `FMP_API_KEY` environment variable with your API key.

```bash
export FMP_API_KEY=your_actual_api_key_here
```

## Installation

The skill is ready to use after cloning. All dependencies are managed through npm.

## Usage

### Basic Commands

#### Get Stock Quote
```bash
# Single stock quote
fmp quote AAPL

# Multiple stock quotes
fmp quote AAPL,MSFT,GOOG

# Export quotes to CSV
fmp quote AAPL,MSFT --csv --output quotes.csv
```

#### Company Profile
```bash
# Get company profile
fmp profile AAPL

# Export profile to CSV
fmp profile AAPL --csv --output profile.csv
```

#### Financial Statements

##### Income Statement
```bash
# Annual income statements (default: last 5 years)
fmp income AAPL

# Quarterly income statements
fmp income AAPL --period quarterly

# Limit to 10 periods
fmp income AAPL --limit 10

# Export to CSV
fmp income AAPL --csv --output income.csv
```

##### Balance Sheet
```bash
# Annual balance sheets
fmp balance AAPL

# Quarterly balance sheets
fmp balance AAPL --period quarterly

# Export to CSV
fmp balance AAPL --csv --output balance.csv
```

##### Cash Flow Statement
```bash
# Annual cash flow statements
fmp cashflow AAPL

# Quarterly cash flow statements
fmp cashflow AAPL --period quarterly

# Export to CSV
fmp cashflow AAPL --csv --output cashflow.csv
```

#### Key Metrics
```bash
# Annual key metrics
fmp metrics AAPL

# Quarterly key metrics
fmp metrics AAPL --period quarterly

# Export to CSV
fmp metrics AAPL --csv --output metrics.csv
```

#### Search Stocks
```bash
# Search by symbol or company name
fmp search Apple

# Export search results to CSV
fmp search Apple --csv --output search_results.csv
```

### Cache Management

The skill includes built-in caching to improve performance and reduce API usage.

```bash
# View cache statistics
fmp cache stats

# Clear cache
fmp cache clear
```

### Output Formats

#### JSON (Default)
```bash
fmp quote AAPL
```

#### Table Format
```bash
fmp quote AAPL --format table
```

#### CSV Export
```bash
fmp quote AAPL,MSFT --csv --output quotes.csv
```

## API Rate Limits

Depending on your FMP subscription tier:
- Free: 250 requests/minute
- Starter: 1,500 requests/minute
- Professional: 15,000 requests/minute
- Enterprise: Unlimited

## Supported Endpoints

### Search & Directory
- `/search` - Symbol search
- `/search-name` - Name search
- `/stock-list` - Stock symbols list
- And more...

### Company Information
- `/profile` - Company profile
- `/stock-peers` - Peer comparison
- `/key-executives` - Executive information
- And more...

### Market Data
- `/quote` - Real-time quotes
- `/historical-price-full` - Historical prices
- `/historical-chart` - Intraday charts
- And more...

### Financial Statements
- `/income-statement` - Income statements
- `/balance-sheet-statement` - Balance sheets
- `/cash-flow-statement` - Cash flow statements
- And more...

### Analytics
- `/key-metrics` - Key metrics
- `/ratios` - Financial ratios
- `/financial-scores` - Financial scores
- And more...

## Error Handling

Common error messages:
- `FMP_API_KEY environment variable is required` - Set your API key
- `API Error: 401` - Invalid API key
- `API Error: 429` - Rate limit exceeded
- `API Error: 404` - Symbol not found

## Configuration

The skill can be configured through `config.json`:

```json
{
  "api_key": "${FMP_API_KEY}",
  "tier": "free",
  "cache": {
    "enabled": true,
    "dir": "./cache/",
    "ttl": {
      "quote": 60,
      "profile": 3600,
      "statements": 86400,
      "history": 3600,
      "default": 1800
    },
    "max_size_mb": 100
  },
  "output": {
    "default_format": "json",
    "pretty": true,
    "color": true,
    "csv_delimiter": ","
  }
}
```

## Troubleshooting

1. **API Key Issues**:
   - Ensure `FMP_API_KEY` is set in your environment
   - Verify your API key at FMP dashboard

2. **Connection Problems**:
   - Check internet connectivity
   - Verify FMP API status

3. **Rate Limiting**:
   - Use cache to reduce API calls
   - Upgrade your FMP subscription if needed

4. **Data Issues**:
   - Some endpoints require Professional/Enterprise plans
   - Check FMP documentation for endpoint availability