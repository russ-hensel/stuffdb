#!/bin/bash

# Get the directory this script is located in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Print it
echo "Directory:"
echo "$SCRIPT_DIR"

# Build the activate path
ACTIVATE_SCRIPT="$SCRIPT_DIR/bin/activate"

echo
echo "Activate script:"
echo "$ACTIVATE_SCRIPT"

# Check that it exists
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo
    echo "Could not find:"
    echo "$ACTIVATE_SCRIPT"
    exit 1
fi

echo
echo "Activating virtual environment..."

# Activate the environment
source "$ACTIVATE_SCRIPT"

echo
echo "Virtual environment is active."
echo "Which Python:"
which python
echo "Shell remains open 🌿"

# Keep an interactive shell running
exec bash
