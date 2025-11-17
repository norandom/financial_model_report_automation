# Financial Report Document Pipeline

Professional financial reports from Jupyter notebooks with Tufte-style layout, margin notes, and automated PDF generation.

## Features

- **Tufte-Style Layout** - Margin notes and annotations alongside main content
- **Full-Width Code Blocks** - Flexible layout for complex code and wide tables
- **Citation Management** - BibTeX integration with margin citations
- **Professional Typography** - Free/open-source fonts (Palatino, Fira Code, Inconsolata)
- **Automated PDF Generation** - GitHub Actions builds PDFs automatically
- **Virtual Environment** - Reproducible Python environment with Jupyter kernel

## Quick Start

### 1. Clone or Use as Template

```bash
# Clone this repository
git clone <your-repo-url>
cd Financial_Report_Document_Pipeline

# Or use as GitHub template (recommended)
# Click "Use this template" button on GitHub
```

### 2. Setup Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run setup script
./setup_venv.sh

# Load environment
source load_venv.sh
```

### 3. Build PDF

```bash
# Build the example notebook
./make_pdf.sh Financial_Report_Example.ipynb

# Or build all notebooks
./make_pdf.sh *.ipynb
```

## Project Structure

```
Financial_Report_Document_Pipeline/
├── Financial_Report_Example.ipynb  # Sample notebook demonstrating all features
├── references.bib                   # Bibliography for citations
├── make_pdf.sh                      # PDF build script
├── setup_venv.sh                    # Initial environment setup
├── sync_venv.sh                     # Update dependencies
├── load_venv.sh                     # Activate environment
├── pyproject.toml                   # Python dependencies
├── buildfiles/
│   ├── preamble.tex.template        # LaTeX preamble template
│   ├── font_config.env              # Font configuration (free fonts)
│   ├── apply_fonts.py               # Font substitution script
│   └── fix_listing_captions.py      # Caption processing script
├── Docs/
│   ├── Tufte_Layout_and_Citations.md  # Complete guide to Tufte layout
│   └── README_FONTS.md                # Font configuration guide
└── .github/workflows/
    └── build-pdf.yml                # Automated PDF builds
```

## Creating Your Report

### 1. Create a New Notebook

Copy `Financial_Report_Example.ipynb` as a starting point:

```bash
cp Financial_Report_Example.ipynb My_Report.ipynb
```

### 2. Update YAML Frontmatter

```yaml
---
title: "Your Report Title"
author: "Your Name"
date: today
bibliography: references.bib  # If using citations
format:
  pdf:
    reference-location: margin  # Footnotes in margin
    citation-location: margin   # Citations in margin
---
```

### 3. Add Content with Margin Notes

**Inline margin note:**
```markdown
This is main text. [This is a margin note]{.aside}
```

**Block margin content:**
```markdown
::: {.column-margin}
**Key Point:**
Extended explanation in margin.
:::
```

### 4. Full-Width Code Blocks

For code that needs more horizontal space:

```python
#| column: page

# This code uses full page width (body + margin)
very_long_function_call(parameter1, parameter2, parameter3, parameter4)
```

### 5. Add Citations

**Create/Update references.bib:**

```bibtex
@article{your2024citation,
  title={Your Article Title},
  author={Author Name},
  journal={Journal Name},
  year={2024}
}
```

**Cite in your notebook:**

```markdown
Modern portfolio theory [@markowitz1952portfolio] revolutionized finance.
```

### 6. Build PDF

```bash
./make_pdf.sh My_Report.ipynb
```

## Font Configuration

This template uses **free/open-source fonts** by default:

- **Main text**: Palatino
- **Code**: Fira Code
- **Tables**: Inconsolata
- **Math**: Euler Math

### Customizing Fonts

Edit `buildfiles/font_config.env`:

```env
MAIN_FONT="Your Main Font"
MONO_FONT="Your Code Font"
TABLE_FONT="Your Table Font"
MATH_FONT="YourMath-Font.otf"
TABLE_FONT_SCALE="1.0"
```

See `Docs/README_FONTS.md` for details.

## GitHub Actions - Automated PDF Builds

PDFs are automatically built when you push to GitHub:

### Setup

1. **Enable GitHub Actions** in your repository settings
2. **Push to main branch** - workflow triggers automatically
3. **Download PDFs** from:
   - Actions → Artifacts
   - Releases → Latest build

### What It Does

- Installs all dependencies
- Sets up free fonts
- Builds all `.ipynb` files
- Uploads PDFs as artifacts
- Creates releases with PDFs attached

### Manual Trigger

Go to Actions → Build PDF → Run workflow

## Documentation

Comprehensive guides in `Docs/`:

- **`Tufte_Layout_and_Citations.md`** - Complete guide to:
  - Margin notes syntax
  - Column layout options (body, page, margin)
  - Citation management
  - Full examples and troubleshooting

- **`README_FONTS.md`** - Font configuration system:
  - Creating custom font profiles
  - Switching between licensed and free fonts
  - Font installation instructions

## Dependencies

Defined in `pyproject.toml`:

**Core:**
- pandas, numpy, matplotlib
- jupyter, ipykernel

**Financial (optional):**
- QuantLib, pysabr, riskfolio-lib (if needed for your reports)

**Build tools:**
- Quarto (install separately)
- TinyTeX (LaTeX distribution)
- uv (Python package manager)

## Requirements

- **Python** 3.10+
- **Quarto** 1.4+ ([install](https://quarto.org/docs/get-started/))
- **uv** (Python package manager)

Install Quarto:
```bash
# macOS
brew install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.25/quarto-1.8.25-linux-amd64.deb
sudo dpkg -i quarto-1.8.25-linux-amd64.deb

# Or follow: https://quarto.org/docs/get-started/
```

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage Workflow

### Local Development

```bash
# 1. Setup (first time only)
./setup_venv.sh

# 2. Activate environment
source load_venv.sh

# 3. Work in Jupyter
jupyter lab

# 4. Build PDF
./make_pdf.sh My_Notebook.ipynb

# 5. Update dependencies (as needed)
./sync_venv.sh
```

### GitHub Workflow

```bash
# 1. Create/edit notebooks locally
# 2. Commit and push
git add *.ipynb references.bib
git commit -m "Add financial analysis report"
git push

# 3. GitHub Actions builds PDFs automatically
# 4. Download from Releases or Actions artifacts
```

## Examples

### Margin Notes

```markdown
Portfolio optimization uses modern portfolio theory.
[MPT assumes normal returns]{.aside}

::: {.column-margin}
**Key Assumption:**
Returns are normally distributed - often violated in practice.
:::
```

### Full-Width Code

```python
#| column: page
#| label: correlation-matrix

# Wide correlation matrix needs full page width
correlation = returns[['Stock_A', 'Stock_B', 'Stock_C', 'Bond_A', 'Bond_B']].corr()
correlation
```

### Citations

```markdown
The Capital Asset Pricing Model [@sharpe1964capital] provides a framework
for asset valuation. Later work [@fama1992cross] extended this to multiple
factors.
```

## Customization

### Custom Styles

Edit `buildfiles/preamble.tex.template` for LaTeX customization:

- Colors
- Table styles
- Page layout
- Headers/footers

### Adding Dependencies

Edit `pyproject.toml`:

```toml
dependencies = [
    "pandas>=2.0.0",
    "your-package>=1.0.0",  # Add here
]
```

Then run:
```bash
./sync_venv.sh
```

## Troubleshooting

### PDF Build Fails

```bash
# Check Quarto installation
quarto --version

# Check TinyTeX
quarto install tinytex

# Regenerate preamble.tex
python3 buildfiles/apply_fonts.py buildfiles/font_config.env
```

### Fonts Not Found

```bash
# Install free fonts (Ubuntu/Debian)
sudo apt-get install fonts-inconsolata fonts-firacode texlive-fonts-extra

# macOS
brew tap homebrew/cask-fonts
brew install --cask font-inconsolata font-fira-code

# Update font cache
fc-cache -f -v
```

### Margin Notes Not Showing

Check YAML has:
```yaml
reference-location: margin
citation-location: margin
```

### Code Not Full Width

Add directive:
```python
#| column: page

# Your code here
```

## License

This template is provided as-is for creating financial reports. Modify freely for your needs.

## Credits

- Typography: Edward Tufte's design principles
- Fonts: Palatino, Fira Code, Inconsolata (all open-source)
- Build System: Quarto, LaTeX/LuaLaTeX
- Python: uv, pandas, numpy, matplotlib

---

For detailed documentation, see:
- `Docs/Tufte_Layout_and_Citations.md` - Complete Tufte guide
- `Docs/README_FONTS.md` - Font configuration system
