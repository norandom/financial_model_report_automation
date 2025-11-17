#!/bin/bash

# Setup script for MBA S3 Python virtual environment
# Uses uv for fast package installation

set -e

VENV_DIR="$HOME/venvs/mba"

echo "Setting up MBA S3 Python environment with uv..."

# Create venv directory if it doesn't exist
if [ ! -d "$HOME/projects/mba" ]; then
    echo "Creating directory: $HOME/projects/mba"
    mkdir -p "$HOME/projects/mba"
fi

# Create virtual environment with uv
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with uv..."
    cd "$HOME/venvs"
    uv venv
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Install dependencies from pyproject.toml
echo "Installing dependencies from pyproject.toml..."
cd "$(dirname "$0")"  # Go back to project directory

# Compile dependencies from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt

# Install from requirements.txt
uv pip install --python "$VENV_DIR/bin/python" -r requirements.txt

# Install PyOptionTree from test.pypi.org (not available on regular PyPI)
echo "Installing PyOptionTree dependencies..."
uv pip install --python "$VENV_DIR/bin/python" networkx python-dateutil matplotlib
echo "Installing PyOptionTree from test.pypi.org..."
uv pip install --python "$VENV_DIR/bin/python" --index-url https://test.pypi.org/simple/ --no-deps PyOptionTree

# Install optional interactive dependencies
read -p "Install optional dependencies (mitosheet, bpython, jupyterlab)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Compiling optional interactive dependencies..."
    uv pip compile pyproject.toml --extra interactive -o requirements-interactive.txt
    echo "Installing optional interactive dependencies..."
    uv pip install --python "$VENV_DIR/bin/python" -r requirements-interactive.txt
fi

# Register as Jupyter kernel
echo "Registering as Jupyter kernel..."
"$VENV_DIR/bin/python" -m ipykernel install --user --name=mba --display-name="MBA (Python)"

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the environment:"
echo "  ./load_venv.sh"
echo ""
echo "To compile the PDF:"
echo "  ./make_pdf.sh"
