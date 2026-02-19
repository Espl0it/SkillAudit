#!/bin/bash

# Skill Audit - Main Entry Point
# Usage: skill-audit [options] [path]

set -euo pipefail

# Default values
TARGET_PATH=""
OUTPUT_FILE=""
VERBOSE=false
RULE_TYPES=""

# Print usage
print_usage() {
  cat << EOF
Usage: skill-audit [options] [path]

Options:
  -t, --type TYPES    Comma-separated rule types (secrets,commands,files,network,permissions,web,crypto)
  -o, --output FILE   Output JSON report to file
  -v, --verbose       Verbose output with code snippets
  -h, --help          Show this help message

Examples:
  skill-audit                           # Audit all skills in workspace
  skill-audit /path/to/skill           # Audit specific skill
  skill-audit --type secrets,commands  # Audit specific rule types
  skill-audit --output report.json     # Save report to file
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--type)
      RULE_TYPES="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    -*)
      echo "Unknown option $1"
      print_usage
      exit 1
      ;;
    *)
      TARGET_PATH="$1"
      shift
      ;;
  esac
done

# Determine target path
if [ -z "$TARGET_PATH" ]; then
  # Try to find skills directory in common locations
  if [ -d "./skills" ]; then
    TARGET_PATH="./skills"
  elif [ -d "../skills" ]; then
    TARGET_PATH="../skills"
  else
    echo "Error: No target path specified and no skills directory found"
    exit 1
  fi
fi

# Validate target path
if [ ! -e "$TARGET_PATH" ]; then
  echo "Error: Target path does not exist: $TARGET_PATH"
  exit 1
fi

# Resolve symlinks
REAL_TARGET=$(realpath "$TARGET_PATH")

# Prepare arguments for scanner
ARGS=()
[ -n "$RULE_TYPES" ] && ARGS+=("--types" "$RULE_TYPES")
[ "$VERBOSE" = true ] && ARGS+=("--verbose")
ARGS+=("$REAL_TARGET")

# Run scanner and capture output
if [ -n "$OUTPUT_FILE" ]; then
  node "$(dirname "$0")/scanner.js" "${ARGS[@]}" > "$OUTPUT_FILE"
  echo "Report saved to $OUTPUT_FILE"
else
  node "$(dirname "$0")/scanner.js" "${ARGS[@]}"
fi