const axios = require('axios');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class FMPCache {
  constructor(config) {
    this.config = config.cache || { enabled: true, dir: './cache/', ttl: {} };
    this.ensureCacheDir();
  }

  ensureCacheDir() {
    if (!fs.existsSync(this.config.dir)) {
      fs.mkdirSync(this.config.dir, { recursive: true });
    }
  }

  getCacheKey(url, params) {
    const keyString = url + JSON.stringify(params);
    return crypto.createHash('md5').update(keyString).digest('hex');
  }

  getTTL(endpoint) {
    return this.config.ttl[endpoint] || this.config.ttl.default || 1800;
  }

  getFilepath(cacheKey) {
    return path.join(this.config.dir, `${cacheKey}.json`);
  }

  isExpired(filepath, ttl) {
    if (!fs.existsSync(filepath)) return true;
    
    const stats = fs.statSync(filepath);
    const now = new Date().getTime();
    const modified = new Date(stats.mtime).getTime();
    return (now - modified) > (ttl * 1000);
  }

  get(endpoint, url, params = {}) {
    if (!this.config.enabled) return null;

    const cacheKey = this.getCacheKey(url, params);
    const filepath = this.getFilepath(cacheKey);
    const ttl = this.getTTL(endpoint);

    if (this.isExpired(filepath, ttl)) {
      return null;
    }

    try {
      const data = fs.readFileSync(filepath, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      // If cache file is corrupted, remove it
      if (fs.existsSync(filepath)) {
        fs.unlinkSync(filepath);
      }
      return null;
    }
  }

  set(endpoint, url, params, data) {
    if (!this.config.enabled) return;

    const cacheKey = this.getCacheKey(url, params);
    const filepath = this.getFilepath(cacheKey);
    
    try {
      fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Failed to write cache:', error.message);
    }
  }

  clear() {
    if (!fs.existsSync(this.config.dir)) return;
    
    const files = fs.readdirSync(this.config.dir);
    files.forEach(file => {
      if (file.endsWith('.json')) {
        fs.unlinkSync(path.join(this.config.dir, file));
      }
    });
  }

  stats() {
    if (!fs.existsSync(this.config.dir)) {
      return { files: 0, size: 0 };
    }

    const files = fs.readdirSync(this.config.dir);
    let totalSize = 0;
    
    files.forEach(file => {
      if (file.endsWith('.json')) {
        const stats = fs.statSync(path.join(this.config.dir, file));
        totalSize += stats.size;
      }
    });

    return {
      files: files.filter(f => f.endsWith('.json')).length,
      size: totalSize
    };
  }
}

class FMPApi {
  constructor(config) {
    this.config = config;
    this.apiKey = process.env.FMP_API_KEY || config.api_key;
    this.baseUrl = 'https://financialmodelingprep.com/api/v3';
    this.cache = new FMPCache(config);
    
    if (!this.apiKey || this.apiKey === '${FMP_API_KEY}') {
      throw new Error('FMP_API_KEY environment variable is required');
    }
  }

  async request(endpoint, params = {}, useCache = true) {
    // Check cache first
    if (useCache) {
      const cached = this.cache.get(endpoint, `${this.baseUrl}/${endpoint}`, params);
      if (cached) {
        return cached;
      }
    }

    // Prepare request
    const url = `${this.baseUrl}/${endpoint}`;
    const config = {
      params: {
        ...params,
        apikey: this.apiKey
      },
      timeout: 10000
    };

    try {
      const response = await axios.get(url, config);
      const data = response.data;
      
      // Cache the response
      if (useCache) {
        this.cache.set(endpoint, url, params, data);
      }
      
      return data;
    } catch (error) {
      if (error.response) {
        throw new Error(`API Error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        throw new Error('API Error: No response received');
      } else {
        throw new Error(`API Error: ${error.message}`);
      }
    }
  }

  // Search endpoints
  async searchSymbol(query) {
    return this.request('search', { query });
  }

  async searchName(query) {
    return this.request('search-name', { query });
  }

  // Quote endpoints
  async getQuote(symbol) {
    const data = await this.request(`quote/${symbol}`);
    return Array.isArray(data) ? data[0] : data;
  }

  async getBatchQuotes(symbols) {
    return this.request('quote', { symbols: Array.isArray(symbols) ? symbols.join(',') : symbols });
  }

  // Profile endpoints
  async getProfile(symbol) {
    const data = await this.request(`profile/${symbol}`);
    return Array.isArray(data) ? data[0] : data;
  }

  // Financial statements
  async getIncomeStatement(symbol, period = 'annual', limit = 5) {
    return this.request(`${period === 'quarterly' ? 'income-statement' : 'income-statement'}/${symbol}`, { 
      period: period === 'quarterly' ? 'quarter' : 'annual',
      limit 
    });
  }

  async getBalanceSheet(symbol, period = 'annual', limit = 5) {
    return this.request(`${period === 'quarterly' ? 'balance-sheet-statement' : 'balance-sheet-statement'}/${symbol}`, { 
      period: period === 'quarterly' ? 'quarter' : 'annual',
      limit 
    });
  }

  async getCashFlow(symbol, period = 'annual', limit = 5) {
    return this.request(`${period === 'quarterly' ? 'cash-flow-statement' : 'cash-flow-statement'}/${symbol}`, { 
      period: period === 'quarterly' ? 'quarter' : 'annual',
      limit 
    });
  }

  // Key metrics
  async getKeyMetrics(symbol, period = 'annual', limit = 5) {
    return this.request(`key-metrics/${symbol}`, { 
      period: period === 'quarterly' ? 'quarter' : 'annual',
      limit 
    });
  }

  // Historical data
  async getHistoricalPrice(symbol, options = {}) {
    const { from, to, serietype = 'line' } = options;
    return this.request(`historical-price-full/${symbol}`, { from, to, serietype });
  }

  // Clear cache
  clearCache() {
    this.cache.clear();
  }

  // Get cache stats
  getCacheStats() {
    return this.cache.stats();
  }
}

module.exports = FMPApi;