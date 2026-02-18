---
name: fmp
description: Financial Modeling Prep API - Comprehensive financial data including stock quotes, financial statements, and market data
homepage: https://site.financialmodelingprep.com/
metadata: {"openclaw":{"emoji":"💰","requires":{"bins":["node"],"env":["FMP_API_KEY"]},"primaryEnv":"FMP_API_KEY"}}
---

# Financial Modeling Prep (FMP)

Access comprehensive financial data through the Financial Modeling Prep API. Get real-time stock quotes, historical data, financial statements, company profiles, and much more.

## Quick Start

```bash
# Get stock quote
fmp quote AAPL

# Get company profile
fmp profile AAPL

# Get financial statements
fmp income AAPL
fmp balance AAPL
fmp cashflow AAPL

# Get historical data
fmp history AAPL --days 30

# Search for stocks
fmp search "Apple"

# Export to CSV
fmp quote AAPL,MSFT --csv --output quotes.csv
```

## Features

- **Real-time Data**: Stock quotes, company profiles, and financial metrics
- **Financial Statements**: Income statements, balance sheets, and cash flow statements
- **Historical Data**: End-of-day and intraday price data
- **Market Data**: Indices, ETFs, cryptocurrencies, forex, and commodities
- **Corporate Data**: Earnings, dividends, stock splits, and IPOs
- **Analytics**: Financial ratios, key metrics, and technical indicators
- **Caching**: Built-in caching for improved performance
- **Export**: Export data to CSV format
- **Batch Operations**: Query multiple symbols at once

## Environment Variables

- `FMP_API_KEY` - Your Financial Modeling Prep API key (required)

Get your API key at: https://site.financialmodelingprep.com/

## Output Formats

- JSON (default)
- Table
- CSV

## Cache

Data is cached locally in the `cache/` directory to improve performance and reduce API usage.