# Financial Model Styling Library

A Python library for declarative styling of financial tables in Jupyter notebooks with Quarto/LaTeX output.

## Features

- **Declarative styling**: Just say `style="assumptions"` instead of specifying individual cell styles
- **Financial model color codes**: Pre-defined color schemes (grey for assumptions, blue for calculations, yellow for outputs)
- **Excel table detection**: Automatically detect multiple tables in a single sheet
- **Jupyter-ready**: Outputs styled HTML that renders in notebooks and compiles through Quarto to PDF
- **Index column styling**: Column A (index) gets special formatting

## Installation

The library is part of the MBA_S3 project. Install dependencies:

```bash
cd /home/jovyan/projects/MBA_S3
source ~/venvs/mba/bin/activate
pip install -e .
```

## Quick Start

### Reading Excel and Styling Tables

```python
from finmodel import ExcelReader, FinancialTable

# Read Excel file
reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')

# Read key-value table (assumptions format)
df = reader.read_key_value_table('BASF Optionsdaten')

# Apply declarative styling
table = FinancialTable(df, style="assumptions")
table.display()  # Shows styled table in Jupyter
```

### Using Different Style Presets

```python
# Grey background for assumptions/inputs
table = FinancialTable(df, style="assumptions")

# Blue for calculations
table = FinancialTable(df, style="calculations")

# Yellow for outputs/results
table = FinancialTable(df, style="outputs")
```

### Detecting Multiple Tables

```python
# Automatically detect all tables in a sheet
reader = ExcelReader('data.xlsx')
tables = reader.read_all_tables('Sheet1', style="assumptions")

for table in tables:
    table.display()
```

### Direct Display in Jupyter

```python
# The table object has _repr_html_() so it displays automatically
from finmodel import ExcelReader, FinancialTable

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
df = reader.read_key_value_table('BASF Optionsdaten')

# Just put the table as last line in cell - it will display
FinancialTable(df, style="assumptions")
```

## Style Presets

### Assumptions (Grey)
- **Use for**: Input parameters, assumptions, constants
- **Colors**: Light grey background (#D9D9D9)
- **Index (Column A)**: Grey background, left-aligned
- **Headers**: Grey background, bold, left-aligned
- **Data**: Grey background, right-aligned

### Calculations (Blue)
- **Use for**: Intermediate calculations, formulas
- **Colors**: Blue headers (#4472C4), light blue index (#D9E2F3)
- **Index (Column A)**: Light blue background
- **Headers**: Blue background with white text, bold
- **Data**: White background, right-aligned

### Outputs (Yellow/Orange)
- **Use for**: Final results, outputs, key metrics
- **Colors**: Orange headers (#FFC000), light yellow cells (#FFF2CC)
- **Index (Column A)**: Light yellow background
- **Headers**: Orange background, bold
- **Data**: Light yellow background, right-aligned

## API Reference

### ExcelReader

```python
reader = ExcelReader(filepath: str)
```

**Methods:**
- `sheet_names` - List available sheets
- `detect_tables(sheet_name, min_rows=2)` - Detect table regions
- `read_table(region, has_header=True)` - Read a specific table region
- `read_key_value_table(sheet_name, start_row=None, end_row=None)` - Read key-value format
- `read_all_tables(sheet_name, style="assumptions")` - Read all tables with styling

### FinancialTable

```python
table = FinancialTable(data, style="assumptions")
```

**Parameters:**
- `data`: pandas DataFrame or dict
- `style`: One of "assumptions", "calculations", "outputs"

**Methods:**
- `display()` - Display in Jupyter
- `_repr_html_()` - HTML representation (automatic in Jupyter)

### StylePreset

```python
from finmodel import StylePreset

# Get a preset
preset = StylePreset.get("assumptions")
```

**Available presets:**
- `"assumptions"` - Grey for inputs
- `"calculations"` - Blue for calculations
- `"outputs"` - Yellow for results

## Excel Format Requirements

### Key-Value Tables (Assumptions)

```
Column A: Parameter name (becomes index)
Column B: Value
Column C: Unit (optional)
```

Example:
```
| Parameter          | Value | Unit  |
|--------------------|-------|-------|
| Kurs (Spotpreis)   | 50    | EUR   |
| Dividende          | 3.3   | EUR   |
| Implizite Vol.     | 0.4   | %     |
```

### Regular Tables

```
Row 1: Column headers
Row 2+: Data rows
```

The library will automatically:
- Use first row as column headers
- Create an index column (Column A)
- Apply formatting to all cells

## Styling Details

### Number Formatting

- **Integers**: Comma separators (1,000)
- **Floats < 1**: 4 decimal places (0.0489)
- **Floats ≥ 1**: 2 decimal places with commas (1,234.56)
- **Null values**: Empty string

### Cell Styling

All styles are applied as **inline CSS** so they work with:
- Jupyter notebook HTML display
- Quarto conversion to LaTeX
- PDF output via LaTeX

### Font

Default: Berkeley Mono (monospace)
- Size: 10pt
- Can be overridden in Quarto preamble

## Quarto/LaTeX Integration

The library outputs HTML with inline styles. When Quarto processes the notebook:

1. Jupyter displays styled HTML tables
2. Quarto converts HTML to LaTeX
3. LaTeX compiles to PDF with styles preserved

**Important**: This library handles the Jupyter → HTML step. Your `preamble.tex` handles LaTeX-level styling.

## Example Workflow

```python
# In your Jupyter notebook
from finmodel import ExcelReader, FinancialTable

# 1. Read Excel
reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
df = reader.read_key_value_table('BASF Optionsdaten')

# 2. Apply declarative styling
assumptions = FinancialTable(df, style="assumptions")

# 3. Display (renders in Jupyter, processes through Quarto to PDF)
assumptions
```

Then compile with Quarto:
```bash
./make_pdf.sh
```

## Advanced Usage

### Custom DataFrame Styling

```python
import pandas as pd
from finmodel import FinancialTable

# Create DataFrame manually
df = pd.DataFrame({
    'Strike': [45, 50, 55],
    'Call Price': [5.2, 2.8, 1.1],
    'Put Price': [0.3, 1.5, 4.8]
})

# Apply styling
table = FinancialTable(df, style="calculations")
table.display()
```

### Multiple Tables in Sequence

```python
reader = ExcelReader('data.xlsx')

# Read different sections with different styles
assumptions = FinancialTable(
    reader.read_key_value_table('Inputs'), 
    style="assumptions"
)

calculations = FinancialTable(
    reader.read_table('Calcs'), 
    style="calculations"
)

outputs = FinancialTable(
    reader.read_table('Results'), 
    style="outputs"
)

# Display all
assumptions.display()
calculations.display()
outputs.display()
```

## Troubleshooting

### "No module named finmodel"

Make sure you're in the MBA_S3 directory and it's in Python path:
```python
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')
from finmodel import ExcelReader, FinancialTable
```

### "No module named openpyxl"

Install dependencies:
```bash
source ~/venvs/mba/bin/activate
pip install openpyxl
```

### Styles not showing in PDF

The library outputs HTML for Jupyter. Make sure:
1. Styles show correctly in Jupyter notebook
2. Your `preamble.tex` doesn't override HTML table styles
3. Quarto is processing with `keep-tex: true` to debug LaTeX

### Table borders not showing

Borders are defined in inline CSS. If they don't appear:
- Check Jupyter display first
- Verify Quarto HTML → LaTeX conversion
- May need additional LaTeX packages in preamble

## License

Part of MBA S3 Assignment project. For educational use.
