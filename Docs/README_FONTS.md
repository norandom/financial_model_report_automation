# Font Configuration System

This directory contains a flexible font configuration system for PDF generation from Jupyter notebooks using Quarto.

## Overview

The font system allows you to easily switch between different font profiles (e.g., licensed fonts for personal use, free fonts for public distribution) without modifying code.

## Files

- **`preamble.tex`** - Generated LaTeX preamble (do not edit directly)
- **`preamble.tex.template`** - Template with font variables (`{{MATH_FONT}}`, `{{TABLE_FONT}}`, etc.)
- **`font_config.env`** - Current font configuration (Default: Free/Open Source fonts)
- **`apply_fonts.py`** - Script to generate `preamble.tex` from template using font config

## Quick Start

### Using Default Free Fonts

Just run `make_pdf.sh`. It uses `font_config.env` which is configured for:
- **Main**: Palatino (System font)
- **Mono**: Fira Code (System font)
- **Math**: Euler-Math (TeX font)
- **Table**: Inconsolata (System font)

```bash
./make_pdf.sh
```

### Creating Custom Font Profiles

1. Create a new config file:
   ```bash
   cp buildfiles/font_config.env buildfiles/font_config_custom.env
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

## Font Requirements

For the default configuration, ensure these fonts are installed on your system:

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
- **Palatino**: Usually included with OS (or use TeX Gyre Pagella)
- **Fira Code**: https://github.com/tonsky/FiraCode
- **Inconsolata**: https://fonts.google.com/specimen/Inconsolata
- **Euler Math**: Included in TeXLive (`texlive-fonts-extra`)

## Notebook YAML Fonts

The notebook's YAML front matter also specifies `mainfont` and `monofont`. You should ensure these match your configuration.

## GitHub Actions Integration

For GitHub Actions workflows, you can set the `FONT_CONFIG` environment variable in `.github/workflows/build-pdf.yml`.

## Troubleshooting

### Font Not Found Error

If you get "font not found" errors during PDF compilation:

1. Check if the font is installed:
   ```bash
   fc-list | grep -i "font-name"
   ```

2. Install missing fonts (see Font Requirements above)

3. Update font cache:
   ```bash
   fc-cache -f -v
   ```
