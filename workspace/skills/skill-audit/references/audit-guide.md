# Skill Audit Guide

## Overview

Skill Audit is a security auditing tool for OpenClaw Skills that detects common security vulnerabilities including hardcoded secrets, command injection risks, and insecure file operations.

## Installation

The skill is automatically available in your OpenClaw workspace. No additional installation is required.

## Usage

### Basic Audit
```bash
# Audit all skills in the current workspace
skill-audit

# Audit a specific skill directory
skill-audit /path/to/skill-directory

# Audit a specific skill file
skill-audit /path/to/skill/SKILL.md
```

### Advanced Options
```bash
# Audit only specific rule types
skill-audit --type secrets,commands

# Generate verbose output with code snippets
skill-audit --verbose

# Save report to a file
skill-audit --output audit-report.json

# Combine options
skill-audit --type secrets,files --verbose --output report.json /path/to/skill
```

## Rule Types

### Secrets (secrets)
Detects hardcoded credentials:
- API keys and tokens
- Passwords
- Private keys
- Base64 encoded secrets
- Cloud provider credentials

### Commands (commands)
Identifies command injection vulnerabilities:
- Unsafe eval() and Function() usage
- Dangerous exec() and spawn() calls
- Shell command concatenation
- Child process injection risks

### Files (files)
Finds file operation security issues:
- Path traversal vulnerabilities
- Access to sensitive system files
- Insecure temporary file creation
- Writing to executable directories

### Network (network)
Detects network security problems:
- Disabled SSL verification
- Use of insecure HTTP protocol
- Unsafe redirect handling

### Permissions (permissions)
Analyzes skill permission declarations:
- Excessive "always: true" permissions
- Over-requested environment variables
- Unnecessary command-line tool requirements

## Output Format

The tool generates JSON reports with the following structure:

```json
{
  "audit_time": "2024-01-01T00:00:00Z",
  "target": "/path/to/skill",
  "summary": {
    "total_issues": 5,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  },
  "issues": [
    {
      "rule_id": "S001",
      "severity": "critical",
      "title": "Hardcoded API Key/Token",
      "file": "scripts/api.js",
      "line": 42,
      "code": "const apiKey = 'sk-xxx...'",
      "recommendation": "Use environment variables or secure credential storage instead"
    }
  ]
}
```

## Severity Levels

- **Critical**: Immediate security risk requiring urgent attention
- **High**: Significant security vulnerability that should be addressed
- **Medium**: Moderate security concern that should be reviewed
- **Low**: Minor security issue or best practice violation
- **Info**: Informational findings

## Best Practices

1. **Regular Auditing**: Run audits regularly during development
2. **Pre-commit Checks**: Integrate into your development workflow
3. **Remediation**: Address critical and high severity issues immediately
4. **Verification**: Re-audit after applying fixes to confirm resolution

## Limitations

- Static analysis only (no runtime behavior analysis)
- May produce false positives
- Limited to supported languages (JavaScript, Python, Bash)
- Does not check external dependencies for vulnerabilities

## Contributing

To add new rules:
1. Create a new rule in the appropriate YAML file in `scripts/rules/`
2. Follow the existing rule format
3. Test with sample vulnerable code
4. Submit a pull request