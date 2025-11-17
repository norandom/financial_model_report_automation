# Font Configuration System

This directory contains a flexible font configuration system for PDF generation from Jupyter notebooks using Quarto.

## Overview

The font system allows you to easily switch between different font profiles (e.g., licensed fonts for personal use, free fonts for public distribution) without modifying code.

## Files

- **`preamble.tex`** - Current LaTeX preamble with hardcoded fonts (your working version)
- **`preamble.tex.template`** - Template with font variables (`{{MATH_FONT}}`, `{{TABLE_FONT}}`, etc.)
- **`font_config.env`** - Current font configuration (licensed fonts: Sys, PragmataPro Liga, Berkeley Mono)
- **`font_config_free.env`** - Free/open-source fonts (Palatino, Fira Code, Inconsolata, Euler Math)
- **`apply_fonts.py`** - Script to generate `preamble.tex` from template using font config

## Quick Start

### Using Your Current Fonts (Default)

Just run `make_pdf.sh` as usual - it uses the existing `preamble.tex` with your licensed fonts:

```bash
./make_pdf.sh
```

### Switching to Free Fonts (for Public Projects)

Set the `FONT_CONFIG` environment variable:

```bash
FONT_CONFIG=buildfiles/font_config_free.env ./make_pdf.sh
```

This will:
1. Generate `buildfiles/preamble.tex` from the template
2. Apply the free fonts configuration
3. Build the PDF

### Creating Custom Font Profiles

1. Copy an existing config file:
   ```bash
   cp buildfiles/font_config_free.env buildfiles/font_config_custom.env
   ```

2. Edit the font names:
   ```env
   MAIN_FONT="Your Main Font"
   MONO_FONT="Your Mono Font"
   MATH_FONT="YourMath-Font.otf"
   TABLE_FONT="Your Table Font"
   TABLE_FONT_SCALE="1.0"
   ```

3. Use it:
   ```bash
   FONT_CONFIG=buildfiles/font_config_custom.env ./make_pdf.sh
   ```

## Font Configuration Reference

### Current Fonts (Licensed)

**`font_config.env`** (default when no `FONT_CONFIG` set):
- **Main**: Sys - Clean, professional body text
- **Mono**: PragmataPro Liga - Premium code font with ligatures
- **Math**: Euler-Math.otf - Classic mathematical typography
- **Table**: Berkeley Mono - Monospace designed for data/tables

### Free Fonts (Public Distribution)

**`font_config_free.env`**:
- **Main**: Palatino - Classic serif font
- **Mono**: Fira Code - Modern code font with ligatures
- **Math**: Euler-Math.otf - Free mathematical font
- **Table**: Inconsolata - Monospace optimized for readability

## Notebook YAML Fonts

The notebook's YAML front matter also specifies `mainfont` and `monofont`. These are currently hardcoded in the notebook:

```yaml
mainfont: "Sys"
monofont: "PragmataPro Liga"
```

When switching font profiles for public distribution, you should also update these in your notebook to match your font config.

## GitHub Actions Integration

For GitHub Actions workflows, set the `FONT_CONFIG` environment variable in `.github/workflows/build-pdf.yml`:

```yaml
- name: Build PDF
  env:
    FONT_CONFIG: buildfiles/font_config_free.env
  run: |
    export QUARTO_PYTHON="$HOME/projects/mba/.venv/bin/python"
    ./make_pdf.sh
```

## Font Installation

### Licensed Fonts (Current Setup)

These fonts are installed in your user fonts directory (`~/.local/share/fonts/`):
- Sys
- PragmataPro Liga
- Berkeley Mono

### Free Fonts

For the free font profile, ensure these fonts are installed:

**Ubuntu/Debian:**
```bash
sudo apt-get install fonts-inconsolata fonts-firacode texlive-fonts-extra
```

**macOS (Homebrew):**
```bash
brew tap homebrew/cask-fonts
brew install --cask font-inconsolata font-fira-code
```

**Manual Installation:**
- Euler Math: Included in TeXLive (`texlive-fonts-extra`)
- Palatino: Usually included with OS
- Fira Code: https://github.com/tonsky/FiraCode
- Inconsolata: https://fonts.google.com/specimen/Inconsolata

## Troubleshooting

### Font Not Found Error

If you get "font not found" errors during PDF compilation:

1. Check if the font is installed:
   ```bash
   fc-list | grep -i "font-name"
   ```

2. Install missing fonts (see Font Installation above)

3. Update font cache:
   ```bash
   fc-cache -f -v
   ```

### Reverting to Hardcoded Fonts

If the font configuration system causes issues, you can always revert to the hardcoded preamble.tex by NOT setting `FONT_CONFIG`:

```bash
# This uses the existing preamble.tex (no font substitution)
./make_pdf.sh
```

## Best Practices

1. **Keep your working setup** - Don't modify `preamble.tex` or `font_config.env` if you're happy with your current fonts
2. **Use templates for sharing** - When creating public templates, use `font_config_free.env`
3. **Document font licenses** - Make it clear which fonts require licenses
4. **Test before distributing** - Always test PDFs with free fonts before sharing publicly

## Example Workflow for Public Template

```bash
# 1. Switch to free fonts
FONT_CONFIG=buildfiles/font_config_free.env ./make_pdf.sh

# 2. Verify PDF renders correctly
open Modul_8_Derivate.pdf  # or xdg-open on Linux

# 3. Update notebook YAML to match free fonts
# Edit notebook: mainfont: "Palatino", monofont: "Fira Code"

# 4. Commit for public repo
git add buildfiles/font_config_free.env buildfiles/preamble.tex.template
git commit -m "Add free font configuration for public distribution"
```
