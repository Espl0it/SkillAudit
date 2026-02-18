#!/usr/bin/env node

// Skill Audit Scanner
// Multi-language security scanner for OpenClaw Skills

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Helper to walk directory tree and resolve symlinks
function* walkDirectory(dir, visited = new Set()) {
  const realPath = fs.realpathSync(dir);
  
  // Prevent infinite loops from circular symlinks
  if (visited.has(realPath)) return;
  visited.add(realPath);
  
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const realEntryPath = fs.realpathSync(fullPath);
    
    if (entry.isDirectory()) {
      yield* walkDirectory(fullPath, visited);
    } else {
      yield { path: fullPath, realPath: realEntryPath };
    }
  }
}

// Load all rules from YAML files
function loadRules(rulesDir) {
  const ruleTypes = ['secrets', 'commands', 'files', 'network', 'permissions'];
  const rules = {};
  
  for (const type of ruleTypes) {
    try {
      const ruleFile = path.join(rulesDir, `${type}.yaml`);
      if (fs.existsSync(ruleFile)) {
        const content = fs.readFileSync(ruleFile, 'utf8');
        rules[type] = yaml.load(content);
      }
    } catch (err) {
      console.error(`Warning: Failed to load rules from ${type}.yaml:`, err.message);
    }
  }
  
  return rules;
}

// Match rules against content
function matchRules(content, rules, filePath, verbose = false) {
  const issues = [];
  const lines = content.split('\n');
  
  for (const [type, typeRules] of Object.entries(rules)) {
    if (!typeRules || !Array.isArray(typeRules)) continue;
    
    for (const rule of typeRules) {
      if (!rule.pattern) continue;
      
      try {
        const regex = new RegExp(rule.pattern, 'gi');
        let match;
        
        while ((match = regex.exec(content)) !== null) {
          const lineNumber = content.substring(0, match.index).split('\n').length;
          const lineContent = lines[lineNumber - 1] || '';
          
          // Skip if line is commented out
          if (isCommentedLine(lineContent, filePath)) continue;
          
          // Skip if line matches exclude pattern
          if (rule.exclude && new RegExp(rule.exclude).test(lineContent)) continue;
          
          const issue = {
            rule_id: rule.id,
            severity: rule.severity || 'medium',
            title: rule.title,
            file: path.relative(process.cwd(), filePath),
            line: lineNumber,
            recommendation: rule.recommendation || ''
          };
          
          if (verbose) {
            issue.code = lineContent.trim();
          }
          
          issues.push(issue);
        }
      } catch (err) {
        console.error(`Warning: Invalid regex in rule ${rule.id}:`, rule.pattern);
      }
    }
  }
  
  return issues;
}

// Check if line is commented out
function isCommentedLine(line, filePath) {
  const trimmed = line.trim();
  
  // JavaScript/TypeScript comments
  if (filePath.endsWith('.js') || filePath.endsWith('.ts') || filePath.endsWith('.mjs')) {
    return trimmed.startsWith('//') || trimmed.startsWith('/*');
  }
  
  // Python comments
  if (filePath.endsWith('.py')) {
    return trimmed.startsWith('#');
  }
  
  // Bash comments
  if (filePath.endsWith('.sh') || filePath.endsWith('.bash')) {
    return trimmed.startsWith('#');
  }
  
  // YAML comments
  if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
    return trimmed.startsWith('#');
  }
  
  return false;
}

// Scan YAML files for permission issues
function scanYAMLRules(content, rules, filePath) {
  const issues = [];
  
  if (!rules.permissions) return issues;
  
  try {
    const doc = yaml.load(content);
    
    // Check for excessive permissions
    if (doc.metadata && doc.metadata.openclaw) {
      const meta = doc.metadata.openclaw;
      
      // Check always: true
      if (meta.always === true) {
        const alwaysRule = rules.permissions.find(r => r.id === 'P001');
        if (alwaysRule) {
          issues.push({
            rule_id: alwaysRule.id,
            severity: alwaysRule.severity || 'low',
            title: alwaysRule.title,
            file: path.relative(process.cwd(), filePath),
            line: 1,
            recommendation: alwaysRule.recommendation || ''
          });
        }
      }
      
      // Check excessive env requirements
      if (meta.requires && meta.requires.env && Array.isArray(meta.requires.env)) {
        if (meta.requires.env.length > 3) {
          const envRule = rules.permissions.find(r => r.id === 'P002');
          if (envRule) {
            issues.push({
              rule_id: envRule.id,
              severity: envRule.severity || 'low',
              title: envRule.title,
              file: path.relative(process.cwd(), filePath),
              line: 1,
              recommendation: envRule.recommendation || ''
            });
          }
        }
      }
      
      // Check excessive bin requirements
      if (meta.requires && meta.requires.bins && Array.isArray(meta.requires.bins)) {
        if (meta.requires.bins.length > 5) {
          const binRule = rules.permissions.find(r => r.id === 'P003');
          if (binRule) {
            issues.push({
              rule_id: binRule.id,
              severity: binRule.severity || 'low',
              title: binRule.title,
              file: path.relative(process.cwd(), filePath),
              line: 1,
              recommendation: binRule.recommendation || ''
            });
          }
        }
      }
    }
  } catch (err) {
    // Ignore YAML parse errors for non-YAML files
  }
  
  return issues;
}

// Main scanning function
function scanTarget(targetPath, rules, options = {}) {
  const { types = [], verbose = false } = options;
  const issues = [];
  const filteredRules = types.length > 0 ? 
    Object.fromEntries(Object.entries(rules).filter(([key]) => types.includes(key))) : 
    rules;
  
  // Handle single file
  if (fs.statSync(targetPath).isFile()) {
    const content = fs.readFileSync(targetPath, 'utf8');
    const ext = path.extname(targetPath).toLowerCase();
    
    if (ext === '.yaml' || ext === '.yml') {
      issues.push(...scanYAMLRules(content, rules, targetPath));
    }
    
    issues.push(...matchRules(content, filteredRules, targetPath, verbose));
    return issues;
  }
  
  // Handle directory
  for (const { path: filePath } of walkDirectory(targetPath)) {
    const ext = path.extname(filePath).toLowerCase();
    
    // Skip non-code files
    if (!['.js', '.ts', '.mjs', '.py', '.sh', '.bash', '.yaml', '.yml'].includes(ext)) {
      continue;
    }
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Special handling for YAML files (permission checks)
      if (ext === '.yaml' || ext === '.yml') {
        issues.push(...scanYAMLRules(content, rules, filePath));
      }
      
      // Apply pattern matching rules
      issues.push(...matchRules(content, filteredRules, filePath, verbose));
    } catch (err) {
      // Skip files that can't be read
      continue;
    }
  }
  
  return issues;
}

// Generate summary statistics
function generateSummary(issues) {
  const summary = {
    total_issues: issues.length,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
    info: 0
  };
  
  for (const issue of issues) {
    const severity = issue.severity.toLowerCase();
    if (summary.hasOwnProperty(severity)) {
      summary[severity]++;
    } else {
      summary.info++;
    }
  }
  
  return summary;
}

// Main function
function main() {
  const args = process.argv.slice(2);
  let targetPath = '';
  let ruleTypes = [];
  let verbose = false;
  
  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--types':
        ruleTypes = args[++i].split(',').map(t => t.trim());
        break;
      case '--verbose':
        verbose = true;
        break;
      default:
        if (!args[i].startsWith('-')) {
          targetPath = args[i];
        }
        break;
    }
  }
  
  if (!targetPath) {
    console.error('Error: No target path specified');
    process.exit(1);
  }
  
  if (!fs.existsSync(targetPath)) {
    console.error(`Error: Target path does not exist: ${targetPath}`);
    process.exit(1);
  }
  
  // Load rules
  const rulesDir = path.join(__dirname, 'rules');
  const rules = loadRules(rulesDir);
  
  // Perform scan
  const issues = scanTarget(targetPath, rules, { types: ruleTypes, verbose });
  
  // Generate report
  const report = {
    audit_time: new Date().toISOString(),
    target: path.resolve(targetPath),
    summary: generateSummary(issues),
    issues: issues.sort((a, b) => {
      // Sort by severity (critical first)
      const severityOrder = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };
      return severityOrder[a.severity] - severityOrder[b.severity];
    })
  };
  
  // Output JSON
  console.log(JSON.stringify(report, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = { scanTarget, loadRules, matchRules };