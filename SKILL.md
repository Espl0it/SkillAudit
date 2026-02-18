---
name: skill-audit
description: Security audit tool for OpenClaw Skills. Detects hardcoded secrets, command injection risks, and other vulnerabilities.
metadata: {"openclaw":{"emoji":"🔒","requires":{"bins":["node"]}}}
---

# Skill Audit

Security audit tool for OpenClaw Skills. Detects hardcoded secrets, command injection risks, file operation vulnerabilities, and other security issues.

## Quick Start

```bash
# Audit all skills in workspace
skill-audit

# Audit a specific skill
skill-audit /path/to/skill

# Audit specific rule types
skill-audit --type secrets,commands

# Generate detailed report
skill-audit --verbose --output report.json
```

## Features

- **Secrets Detection**: Hardcoded API keys, tokens, passwords
- **Command Injection**: Unsafe `eval`, `exec`, shell command construction
- **File Security**: Path traversal, sensitive file access
- **Network Security**: Insecure HTTP, disabled SSL verification
- **Permission Analysis**: Excessive permissions in skill metadata

## Supported Languages

- JavaScript/Node.js
- Python
- Bash scripts

## Rule Types

- `secrets`: Hardcoded credentials
- `commands`: Command injection risks
- `files`: File operation vulnerabilities
- `network`: Network security issues
- `permissions`: Excessive skill permissions

## Output

Generates JSON reports with:
- Issue severity levels (critical/high/medium/low/info)
- File locations and line numbers
- Vulnerable code snippets
- Remediation suggestions