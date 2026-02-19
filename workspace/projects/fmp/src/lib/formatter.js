const { createObjectCsvWriter } = require('csv-writer');

class Formatter {
  static formatJson(data, pretty = true) {
    return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  }

  static formatTable(data, options = {}) {
    if (!data) return '';
    
    // Handle array data
    if (Array.isArray(data)) {
      if (data.length === 0) return 'No data found';
      
      // For single object, convert to array format
      if (data.length === 1 && typeof data[0] === 'object' && !Array.isArray(data[0])) {
        return this.formatSingleObjectAsTable(data[0], options);
      }
      
      return this.formatArrayAsTable(data, options);
    }
    
    // Handle single object
    if (typeof data === 'object') {
      return this.formatSingleObjectAsTable(data, options);
    }
    
    // Handle primitive values
    return String(data);
  }

  static formatSingleObjectAsTable(obj, options = {}) {
    const lines = [];
    const keys = Object.keys(obj);
    
    // Calculate column widths
    const keyWidth = Math.max(15, ...keys.map(k => k.length));
    const valueWidth = options.valueWidth || 30;
    
    // Header
    if (options.showHeader !== false) {
      lines.push(`${'Key'.padEnd(keyWidth)} | ${'Value'.padEnd(valueWidth)}`);
      lines.push('-'.repeat(keyWidth) + '-+-' + '-'.repeat(valueWidth));
    }
    
    // Rows
    keys.forEach(key => {
      const value = this.formatValue(obj[key]);
      const valueLines = this.wrapText(value, valueWidth);
      
      // First line
      lines.push(`${key.padEnd(keyWidth)} | ${valueLines[0].padEnd(valueWidth)}`);
      
      // Additional lines for wrapped text
      for (let i = 1; i < valueLines.length; i++) {
        lines.push(`${''.padEnd(keyWidth)} | ${valueLines[i].padEnd(valueWidth)}`);
      }
    });
    
    return lines.join('\n');
  }

  static formatArrayAsTable(arr, options = {}) {
    if (arr.length === 0) return 'No data found';
    
    // Get all unique keys
    const allKeys = new Set();
    arr.forEach(item => {
      if (typeof item === 'object' && item !== null) {
        Object.keys(item).forEach(key => allKeys.add(key));
      }
    });
    
    const keys = Array.from(allKeys);
    if (keys.length === 0) {
      // Handle array of primitives
      return arr.map((item, index) => `${index}: ${this.formatValue(item)}`).join('\n');
    }
    
    // Calculate column widths
    const maxWidth = options.maxWidth || 20;
    const widths = {};
    keys.forEach(key => {
      widths[key] = Math.min(maxWidth, Math.max(
        key.length,
        ...arr.map(item => 
          item && typeof item === 'object' && item[key] !== undefined 
            ? this.formatValue(item[key]).length 
            : 0
        )
      ));
    });
    
    const lines = [];
    
    // Header
    const header = keys.map(key => key.padEnd(widths[key])).join(' | ');
    lines.push(header);
    lines.push(keys.map(key => '-'.repeat(widths[key])).join('-+-'));
    
    // Rows
    arr.forEach(item => {
      if (typeof item === 'object' && item !== null) {
        const row = keys.map(key => {
          const value = item[key] !== undefined ? this.formatValue(item[key]) : '';
          return value.padEnd(widths[key]).substring(0, widths[key]);
        }).join(' | ');
        lines.push(row);
      } else {
        lines.push(this.formatValue(item));
      }
    });
    
    return lines.join('\n');
  }

  static formatValue(value) {
    if (value === null || value === undefined) return 'null';
    if (typeof value === 'object') return JSON.stringify(value);
    if (typeof value === 'boolean') return value.toString();
    if (typeof value === 'number') return value.toLocaleString();
    return String(value);
  }

  static wrapText(text, width) {
    const lines = [];
    const str = String(text);
    
    if (str.length <= width) {
      lines.push(str);
      return lines;
    }
    
    let currentLine = '';
    const words = str.split(' ');
    
    words.forEach(word => {
      if (currentLine.length + word.length + 1 <= width) {
        currentLine += (currentLine ? ' ' : '') + word;
      } else {
        if (currentLine) lines.push(currentLine);
        currentLine = word;
      }
    });
    
    if (currentLine) lines.push(currentLine);
    
    return lines.length > 0 ? lines : [''];
  }

  static async exportToCsv(data, filepath, options = {}) {
    if (!data) throw new Error('No data to export');
    
    let records = [];
    let headers = [];
    
    if (Array.isArray(data)) {
      if (data.length === 0) {
        records = [];
        headers = [];
      } else if (typeof data[0] === 'object' && data[0] !== null) {
        // Array of objects
        records = data;
        const allKeys = new Set();
        data.forEach(item => {
          Object.keys(item).forEach(key => allKeys.add(key));
        });
        headers = Array.from(allKeys).map(key => ({ id: key, title: key }));
      } else {
        // Array of primitives
        records = data.map((item, index) => ({ index, value: item }));
        headers = [
          { id: 'index', title: 'Index' },
          { id: 'value', title: 'Value' }
        ];
      }
    } else if (typeof data === 'object' && data !== null) {
      // Single object
      records = [data];
      headers = Object.keys(data).map(key => ({ id: key, title: key }));
    } else {
      // Primitive value
      records = [{ value: data }];
      headers = [{ id: 'value', title: 'Value' }];
    }
    
    const csvWriter = createObjectCsvWriter({
      path: filepath,
      header: headers,
      fieldDelimiter: options.delimiter || ','
    });
    
    await csvWriter.writeRecords(records);
    return `Data exported to ${filepath}`;
  }
}

module.exports = Formatter;