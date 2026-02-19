#!/bin/bash

# FMP Skill Wrapper Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Export the project directory to NODE_PATH so our modules can be found
export NODE_PATH="$PROJECT_DIR/node_modules"

# Run the FMP skill with all arguments passed through
node "$PROJECT_DIR/src/index.js" "$@"