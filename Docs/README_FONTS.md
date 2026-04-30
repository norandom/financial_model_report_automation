# Font configuration

This directory contains the font configuration for PDF generation from Jupyter notebooks using Quarto. You can switch between font profiles (licensed fonts for personal use, free fonts for distribution) without editing code.

## Files

- `preamble.tex` -- generated LaTeX preamble (do not edit directly)
- `preamble.tex.template` -- template with font variables (`{{MATH_FONT}}`, `{{TABLE_FONT}}`, etc.)
- `font_config.env` -- current font configuration (defaults to free/open source fonts)
- `apply_fonts.py` -- generates `preamble.tex` from the template using the font config

## Quick start

### Using the default free fonts

Run `make_pdf.sh`. It uses `font_config.env`, which is configured for:

- Main: Palatino (system font)
- Mono: Fira Code (system font)
- Math: Euler-Math (TeX font)
- Table: Inconsolata (system font)

```bash
./make_pdf.sh
```

### Creating custom font profiles

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

## Font requirements

For the default configuration, these fonts need to be installed:

Ubuntu/Debian:
```bash
sudo apt-get install fonts-inconsolata fonts-firacode texlive-fonts-extra
```

macOS (Homebrew):
```bash
brew tap homebrew/cask-fonts
brew install --cask font-inconsolata font-fira-code
```

Manual installation:
- Palatino: usually included with the OS (or use TeX Gyre Pagella)
- Fira Code: https://github.com/tonsky/FiraCode
- Inconsolata: https://fonts.google.com/specimen/Inconsolata
- Euler Math: included in TeXLive (`texlive-fonts-extra`)

## Notebook YAML fonts

The notebook's YAML front matter also specifies `mainfont` and `monofont`. Make sure these match your configuration.

## GitHub Actions integration

For GitHub Actions workflows, set the `FONT_CONFIG` environment variable in `.github/workflows/build-pdf.yml`.

## Troubleshooting

### Font not found error

If you get "font not found" errors during PDF compilation:

1. Check if the font is installed:
   ```bash
   fc-list | grep -i "font-name"
   ```

2. Install missing fonts (see font requirements above)

3. Update font cache:
   ```bash
   fc-cache -f -v
   ```
