#!/bin/bash

# Sync virtual environment with dependencies from pyproject.toml
# This ensures the venv matches exactly what's specified in pyproject.toml

set -e

VENV_DIR="$HOME/venvs/mba"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Syncing virtual environment with pyproject.toml..."

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Run ./setup_venv.sh first to create it."
    exit 1
fi

cd "$PROJECT_DIR"

# Compile dependencies from pyproject.toml
echo "Compiling dependencies from pyproject.toml..."
uv pip compile pyproject.toml -o requirements.txt

# Sync venv to match requirements.txt exactly
echo "Syncing virtual environment..."
uv pip sync --python "$VENV_DIR/bin/python" requirements.txt

# Install PyOptionTree from test.pypi.org (not available on regular PyPI)
echo "Installing PyOptionTree dependencies..."
uv pip install --python "$VENV_DIR/bin/python" networkx python-dateutil matplotlib
echo "Installing PyOptionTree from test.pypi.org..."
uv pip install --python "$VENV_DIR/bin/python" --index-url https://test.pypi.org/simple/ --no-deps PyOptionTree

echo ""
echo "✓ Virtual environment synced successfully!"
echo ""
echo "Installed packages match pyproject.toml"
echo ""
echo "To sync with optional dependencies:"
echo "  uv pip compile pyproject.toml --extra interactive -o requirements-interactive.txt"
echo "  uv pip sync --python $VENV_DIR/bin/python requirements-interactive.txt"
