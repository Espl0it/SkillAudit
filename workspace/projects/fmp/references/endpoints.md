# FMP API Endpoints Mapping

This document maps FMP API endpoints to skill commands.

## Search & Directory

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/search` | `fmp search` | ✅ Implemented | Symbol search |
| `/search-name` | `fmp search-name` | ❌ Planned | Name search |
| `/search-cik` | `fmp search-cik` | ❌ Planned | CIK search |
| `/search-cusip` | `fmp search-cusip` | ❌ Planned | CUSIP search |
| `/search-isin` | `fmp search-isin` | ❌ Planned | ISIN search |
| `/company-screener` | `fmp screener` | ❌ Planned | Stock screener |
| `/stock-list` | `fmp stock-list` | ❌ Planned | Stock symbols |
| `/financial-statement-symbol-list` | `fmp statement-list` | ❌ Planned | Financial symbols |
| `/cik-list` | `fmp cik-list` | ❌ Planned | CIK numbers |
| `/etf-list` | `fmp etf-list` | ❌ Planned | ETF symbols |
| `/actively-trading-list` | `fmp active-list` | ❌ Planned | Active stocks |

## Company Information

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/profile` | `fmp profile` | ✅ Implemented | Company profile |
| `/profile-cik` | `fmp profile-cik` | ❌ Planned | Profile by CIK |
| `/company-notes` | `fmp company-notes` | ❌ Planned | Company notes |
| `/stock-peers` | `fmp peers` | ❌ Planned | Peer comparison |
| `/delisted-companies` | `fmp delisted` | ❌ Planned | Delisted companies |
| `/employee-count` | `fmp employees` | ❌ Planned | Employee count |
| `/market-capitalization` | `fmp market-cap` | ❌ Planned | Market cap |
| `/shares-float` | `fmp float` | ❌ Planned | Share float |
| `/key-executives` | `fmp executives` | ❌ Planned | Executives info |
| `/executive-compensation` | `fmp compensation` | ❌ Planned | Executive pay |

## Market Data - Quotes

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/quote` | `fmp quote` | ✅ Implemented | Real-time quote |
| `/quote-short` | `fmp quote-short` | ❌ Planned | Short quote |
| `/aftermarket-trade` | `fmp aftermarket` | ❌ Planned | Aftermarket trade |
| `/stock-price-change` | `fmp price-change` | ❌ Planned | Price changes |
| `/batch-quote` | `fmp quote` | ✅ Implemented | Batch quotes |
| `/batch-quote-short` | `fmp quote-short` | ❌ Planned | Batch short quotes |

## Financial Statements

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/income-statement` | `fmp income` | ✅ Implemented | Income statement |
| `/balance-sheet-statement` | `fmp balance` | ✅ Implemented | Balance sheet |
| `/cash-flow-statement` | `fmp cashflow` | ✅ Implemented | Cash flow |
| `/income-statement-ttm` | `fmp income-ttm` | ❌ Planned | TTM income |
| `/balance-sheet-ttm` | `fmp balance-ttm` | ❌ Planned | TTM balance |
| `/cash-flow-ttm` | `fmp cashflow-ttm` | ❌ Planned | TTM cash flow |
| `/key-metrics` | `fmp metrics` | ✅ Implemented | Key metrics |
| `/ratios` | `fmp ratios` | ❌ Planned | Financial ratios |
| `/financial-scores` | `fmp scores` | ❌ Planned | Financial scores |
| `/enterprise-values` | `fmp enterprise` | ❌ Planned | Enterprise value |

## Historical Data

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/historical-price-full` | `fmp history` | ❌ Planned | Historical prices |
| `/historical-chart/1min` | `fmp chart-1min` | ❌ Planned | 1-min charts |
| `/historical-chart/5min` | `fmp chart-5min` | ❌ Planned | 5-min charts |
| `/historical-chart/15min` | `fmp chart-15min` | ❌ Planned | 15-min charts |
| `/historical-chart/30min` | `fmp chart-30min` | ❌ Planned | 30-min charts |
| `/historical-chart/1hour` | `fmp chart-1hour` | ❌ Planned | 1-hour charts |
| `/historical-chart/4hour` | `fmp chart-4hour` | ❌ Planned | 4-hour charts |

## Corporate Events

| Endpoint | Command | Status | Notes |
|----------|---------|--------|-------|
| `/dividends` | `fmp dividends` | ❌ Planned | Dividend data |
| `/dividends-calendar` | `fmp div-calendar` | ❌ Planned | Dividend calendar |
| `/earnings` | `fmp earnings` | ❌ Planned | Earnings data |
| `/earnings-calendar` | `fmp earn-calendar` | ❌ Planned | Earnings calendar |
| `/splits` | `fmp splits` | ❌ Planned | Stock splits |
| `/splits-calendar` | `fmp split-calendar` | ❌ Planned | Split calendar |

## Extended Data

| Category | Endpoint | Command | Status | Notes |
|----------|----------|---------|--------|-------|
| **ETF** | `/etf-list` | `fmp etf-list` | ❌ Planned | ETF list |
| | `/etf-holdings` | `fmp etf-holdings` | ❌ Planned | ETF holdings |
| | `/etf-sector-weightings` | `fmp etf-sectors` | ❌ Planned | Sector weights |
| **Crypto** | `/quotes/crypto` | `fmp crypto` | ❌ Planned | Crypto quotes |
| | `/historical-price-full/crypto` | `fmp crypto-history` | ❌ Planned | Crypto history |
| **Forex** | `/quotes/forex` | `fmp forex` | ❌ Planned | Forex quotes |
| | `/historical-price-full/forex` | `fmp forex-history` | ❌ Planned | Forex history |
| **Commodities** | `/quotes/commodity` | `fmp commodity` | ❌ Planned | Commodity quotes |
| **Indices** | `/quotes/index` | `fmp index` | ❌ Planned | Index quotes |
| | `/historical-price-full/index` | `fmp index-history` | ❌ Planned | Index history |
| **SEC** | `/form-13f` | `fmp form-13f` | ❌ Planned | 13F filings |
| | `/insider-trading` | `fmp insider` | ❌ Planned | Insider trades |
| **Analyst** | `/analyst-estimates` | `fmp estimates` | ❌ Planned | Analyst estimates |
| | `/price-target` | `fmp target` | ❌ Planned | Price targets |
| | `/rating` | `fmp rating` | ❌ Planned | Analyst ratings |
| **News** | `/stock_news` | `fmp news` | ❌ Planned | Stock news |
| **Economics** | `/economic-indicators` | `fmp economics` | ❌ Planned | Economic data |
| | `/treasury-rates` | `fmp treasury` | ❌ Planned | Treasury rates |

## Implementation Priority

### Phase 1 (Completed)
- ✅ Basic API framework
- ✅ Quote functionality
- ✅ Profile functionality
- ✅ Financial statements
- ✅ Key metrics
- ✅ Search functionality
- ✅ CSV export
- ✅ Caching

### Phase 2 (Planned)
- ❌ Historical data
- ❌ Corporate events
- ❌ Additional search endpoints
- ❌ Extended company info
- ❌ Batch operations enhancements

### Phase 3 (Future)
- ❌ Professional API features
- ❌ Real-time streaming
- ❌ Technical indicators
- ❌ Bulk data download
- ❌ Advanced analytics