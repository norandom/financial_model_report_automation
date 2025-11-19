#!/bin/bash

# Script to compile Jupyter notebook to PDF using Quarto
# The notebook already includes preamble.tex via YAML front matter

set -e  # Exit on error

# Use provided notebook or default to Modul_8_Derivate.ipynb
NOTEBOOK="${1:-Financial_Report_Example.ipynb}"

# Add TinyTeX to PATH if it exists (search for architecture-specific directory)
if [ -d "$HOME/.TinyTeX/bin" ]; then
    for bin_dir in "$HOME/.TinyTeX/bin/"*-linux; do
        if [ -d "$bin_dir" ]; then
            export PATH="$bin_dir:$PATH"
            break
        fi
    done
fi

echo "Compiling $NOTEBOOK to PDF with Quarto..."
echo "Using buildfiles/preamble.tex for LaTeX customization"
echo ""

# Check if quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "Error: Quarto is not installed or not in PATH"
    echo "Please install Quarto from: https://quarto.org/docs/get-started/"
    exit 1
fi

# Check if notebook exists
if [ ! -f "$NOTEBOOK" ]; then
    echo "Error: $NOTEBOOK not found"
    exit 1
fi

# Set Python environment (default to venv if exists, else python3)
if [ -z "$QUARTO_PYTHON" ]; then
    if [ -d "venv" ]; then
        export QUARTO_PYTHON="$PWD/venv/bin/python"
    elif [ -d "$HOME/venvs/mba" ]; then
        export QUARTO_PYTHON="$HOME/venvs/mba/bin/python"
    else
        export QUARTO_PYTHON="python3"
    fi
fi

# Default FONT_CONFIG if not set but file exists
if [ -z "$FONT_CONFIG" ] && [ -f "buildfiles/font_config.env" ]; then
    export FONT_CONFIG="buildfiles/font_config.env"
fi

# Optional: Apply font configuration (for public/template projects)
# Set FONT_CONFIG environment variable to use custom fonts
# Example: FONT_CONFIG=buildfiles/font_config_free.env ./make_pdf.sh
if [ -n "$FONT_CONFIG" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Step 0: Applying font configuration from $FONT_CONFIG"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    "${QUARTO_PYTHON:-python3}" buildfiles/apply_fonts.py "$FONT_CONFIG"
    echo ""
else
    # Check if preamble exists (when not using font config)
    if [ ! -f "buildfiles/preamble.tex" ]; then
        echo "Warning: buildfiles/preamble.tex not found"
        echo "Hint: Set FONT_CONFIG to generate from template"
    fi
fi

# First render to get the .tex file (keep-tex is set in YAML)
# Note: Initial compilation may fail due to duplicate \listoflistings command
# This is EXPECTED and will be fixed by post-processing
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Initial Quarto render (may show LaTeX errors - normal)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
quarto render "$NOTEBOOK" --to pdf 2>&1 | grep -v "^$" || true
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Post-processing .tex file..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if .tex file was generated
TEX_FILE="${NOTEBOOK%.ipynb}.tex"
if [ ! -f "$TEX_FILE" ]; then
    echo "Error: .tex file not generated"
    exit 1
fi

echo "  → Fixing duplicate \\listoflistings commands..."
# Fix \listoflistings command conflicts between preamble.tex and Quarto's template
# Change all \newcommand*\listoflistings to \providecommand*\listoflistings to avoid redefinition errors
sed -i 's/\\newcommand\*\\listoflistings/\\providecommand*\\listoflistings/g' "$TEX_FILE"

# Fix code listing captions
echo "  → Fixing code listing captions..."
"${QUARTO_PYTHON:-python3}" buildfiles/fix_listing_captions.py "$NOTEBOOK"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Final LaTeX compilation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for lualatex
if ! command -v lualatex &> /dev/null; then
    echo "Error: lualatex not found in PATH"
    echo "Please install TinyTeX or a LaTeX distribution"
    exit 1
fi

# Run lualatex and capture exit code
if ! lualatex -interaction=nonstopmode "$TEX_FILE" 2>&1 | tail -20; then
    echo ""
    echo "Warning: LaTeX compilation reported errors."
    echo "Check ${NOTEBOOK%.ipynb}.log for details."
fi

# Run again for references (if needed)
lualatex -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || true

PDF_FILE="${NOTEBOOK%.ipynb}.pdf"
if [ -f "$PDF_FILE" ]; then
    echo ""
    echo "Done! PDF generated successfully."
    echo "Output: $PDF_FILE"
else
    echo ""
    echo "Error: PDF file was not generated."
    exit 1
fi