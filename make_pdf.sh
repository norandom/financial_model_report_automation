#!/bin/bash

# Script to compile Jupyter notebook to PDF using Quarto
# The notebook already includes preamble.tex via YAML front matter

set -e  # Exit on error

# Use provided notebook or default to Modul_8_Derivate.ipynb
NOTEBOOK="${1:-Modul_8_Derivate.ipynb}"

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

# Set Python environment to use the mba venv (if not already set)
if [ -z "$QUARTO_PYTHON" ]; then
    export QUARTO_PYTHON="$HOME/venvs/mba/bin/python"
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

echo "  → Adding vertical lines to tables..."
# Post-process the .tex file to add vertical lines to longtable
# Replace the column spec @{}XXX@{} with |X|X|X| where X can be r, l, or c
# This adds vertical lines between columns and at edges
sed -i 's/\\begin{longtable}\[\]{@{}\([rlc]*\)@{}}/\\begin{longtable}[]{|\1|}/' "$TEX_FILE"
# Now add pipes between each column specifier within the already modified pattern
# Replace sequences like |rrr| with |r|r|r|
sed -i 's/\(\[]{|\)\([rlc]\)\([rlc]\)/\1\2|\3/g;s/\([rlc]\)\([rlc]|}\)/\1|\2/g' "$TEX_FILE"
# Repeat to handle all columns (for tables with more than 2 columns)
sed -i 's/\([rlc]\)\([rlc]|}\)/\1|\2/g;s/\([rlc]\)\([rlc]|}\)/\1|\2/g' "$TEX_FILE"

# Fix code listing captions
echo "  → Fixing code listing captions..."
"${QUARTO_PYTHON:-python3}" buildfiles/fix_listing_captions.py "$NOTEBOOK"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Final LaTeX compilation..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LUALATEX="$HOME/.TinyTeX/bin/x86_64-linux/lualatex"
"$LUALATEX" -interaction=nonstopmode "$TEX_FILE" 2>&1 | tail -20 || echo "Warning: LaTeX compilation had issues (non-fatal)"
# Run twice for references
"$LUALATEX" -interaction=nonstopmode "$TEX_FILE" > /dev/null 2>&1 || true

echo ""
echo "Done! PDF generated successfully."
PDF_FILE="${NOTEBOOK%.ipynb}.pdf"
echo "Output: $PDF_FILE"
