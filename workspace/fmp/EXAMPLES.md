# FMP Skill Example Usage

Once you have set your FMP_API_KEY environment variable, you can use the FMP skill as follows:

## Setting up the API Key

```bash
export FMP_API_KEY=your_actual_api_key_here
```

## Basic Usage Examples

### 1. Getting Stock Quotes
```bash
# Single stock quote
fmp quote AAPL

# Multiple stock quotes
fmp quote AAPL,MSFT,GOOG

# Export to CSV
fmp quote AAPL,MSFT --csv --output quotes.csv
```

### 2. Company Profile
```bash
# Get company profile
fmp profile AAPL

# Export profile to CSV
fmp profile AAPL --csv --output profile.csv
```

### 3. Financial Statements
```bash
# Annual income statements
fmp income AAPL

# Quarterly balance sheets
fmp balance AAPL --period quarterly

# Cash flow statements with custom limit
fmp cashflow AAPL --limit 10

# Export financial statements to CSV
fmp income AAPL --csv --output income.csv
```

### 4. Key Metrics
```bash
# Annual key metrics
fmp metrics AAPL

# Quarterly key metrics
fmp metrics AAPL --period quarterly

# Export to CSV
fmp metrics AAPL --csv --output metrics.csv
```

### 5. Searching for Stocks
```bash
# Search by company name
fmp search "Apple"

# Export search results
fmp search "Technology" --csv --output tech_stocks.csv
```

### 6. Cache Management
```bash
# View cache statistics
fmp cache stats

# Clear cache when needed
fmp cache clear
```

## Output Format Options

### JSON (Default)
```bash
fmp quote AAPL
```

### Table Format
```bash
fmp quote AAPL --format table
fmp profile AAPL --format table
```

### CSV Export
```bash
fmp quote AAPL,MSFT --csv --output quotes.csv
fmp profile AAPL --csv --output profile.csv
fmp income AAPL --csv --output income.csv
```

## Advanced Usage

### Batch Operations
The skill supports batch operations for multiple symbols:

```bash
# Get quotes for multiple stocks
fmp quote AAPL,MSFT,GOOG,TSLA

# Get profiles for multiple companies
fmp profile AAPL,MSFT,GOOG,TSLA

# Export batch data to CSV
fmp quote AAPL,MSFT,GOOG,TSLA --csv --output batch_quotes.csv
```

### Time Period Options
For financial statements and metrics:

```bash
# Annual data (default)
fmp income AAPL --period annual

# Quarterly data
fmp income AAPL --period quarterly

# Limit number of periods
fmp income AAPL --limit 3
```

## Error Handling

Common scenarios:

1. **Missing API Key**:
   ```
   Error: FMP_API_KEY environment variable is required
   ```
   Solution: Set your API key with `export FMP_API_KEY=your_key`

2. **Invalid Symbol**:
   ```
   Error: API Error: 404 - {"Error Message": "Symbol not found"}
   ```
   Solution: Check the symbol spelling

3. **Rate Limit Exceeded**:
   ```
   Error: API Error: 429 - {"Error Message": "Too many requests"}
   ```
   Solution: Wait and try again, or upgrade your plan

## Configuration

The skill uses caching by default to reduce API calls. Cache files are stored in the `cache/` directory and automatically expire based on data type:

- Quotes: 1 minute
- Profiles: 1 hour
- Financial statements: 24 hours
- Historical data: 1 hour

You can disable caching with the `--no-cache` flag or clear the cache with `fmp cache clear`.