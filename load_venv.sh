#!/bin/bash

# Script to activate the Python virtual environment
# Usage: ./load_venv.sh (starts a new shell with venv activated)

VENV_PATH="$HOME/venvs/mba"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

echo "Starting new shell with virtual environment activated..."
echo "Virtual environment: $VENV_PATH"
echo ""

# Start a new bash shell with the venv activated
# The --rcfile option runs the activation and then provides an interactive prompt
bash --rcfile <(cat <<EOF
# Source the user's bashrc if it exists
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Show info
echo "✓ Virtual environment activated"
echo "  Python: \$(which python)"
echo "  Version: \$(python --version)"
echo ""
echo "Type 'exit' or press Ctrl+D to deactivate and return to your original shell"
echo ""
EOF
)
