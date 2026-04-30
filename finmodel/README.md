# finmodel

A Python library for styling financial tables in Jupyter notebooks. Outputs HTML that compiles through Quarto to PDF.

## Features

- Style tables with `style="assumptions"` instead of specifying individual cells
- Color coded by role: grey for assumptions, blue for calculations, yellow for outputs (follows Excel financial modeling conventions)
- Detects multiple tables in a single Excel sheet
- Column A (index) gets distinct formatting
- Renders in Jupyter and compiles to PDF through Quarto

## Installation

```bash
pip install -e .
```

## Quick start

### Reading Excel and styling tables

```python
from finmodel import ExcelReader, FinancialTable

# Read Excel file
reader = ExcelReader('data/model.xlsx')

# Read key-value table (assumptions format)
df = reader.read_key_value_table('Assumptions')

# Apply styling
table = FinancialTable(df, style="assumptions")
table.display()  # Shows styled table in Jupyter
```

### Style presets

```python
# Grey background for assumptions/inputs
table = FinancialTable(df, style="assumptions")

# Blue for calculations
table = FinancialTable(df, style="calculations")

# Yellow for outputs/results
table = FinancialTable(df, style="outputs")
```

### Detecting multiple tables

```python
reader = ExcelReader('data.xlsx')
tables = reader.read_all_tables('Sheet1', style="assumptions")

for table in tables:
    table.display()
```

### Display in Jupyter

The table object implements `_repr_html_()`, so putting it as the last line in a cell displays it automatically:

```python
from finmodel import ExcelReader, FinancialTable

reader = ExcelReader('data/model.xlsx')
df = reader.read_key_value_table('Assumptions')

# Last line in cell -- displays automatically
FinancialTable(df, style="assumptions")
```

## Style presets

### Assumptions (grey)

For input parameters, assumptions, constants. Light grey background (#D9D9D9) on all cells. Index left-aligned, data right-aligned, headers bold.

### Calculations (blue)

For intermediate calculations and formulas. Blue headers (#4472C4) with white text, light blue index (#D9E2F3), white data cells.

### Outputs (yellow/orange)

For final results and output metrics. Orange headers (#FFC000), light yellow cells (#FFF2CC) on both index and data.

## API reference

### ExcelReader

```python
reader = ExcelReader(filepath: str)
```

Methods:
- `sheet_names` -- list available sheets
- `detect_tables(sheet_name, min_rows=2)` -- detect table regions
- `read_table(region, has_header=True)` -- read a specific table region
- `read_key_value_table(sheet_name, start_row=None, end_row=None)` -- read key-value format
- `read_all_tables(sheet_name, style="assumptions")` -- read all tables with styling

### FinancialTable

```python
table = FinancialTable(data, style="assumptions")
```

Parameters:
- `data`: pandas DataFrame or dict
- `style`: one of `"assumptions"`, `"calculations"`, `"outputs"`

Methods:
- `display()` -- display in Jupyter
- `_repr_html_()` -- HTML representation (automatic in Jupyter)

### StylePreset

```python
from finmodel import StylePreset

preset = StylePreset.get("assumptions")
```

Available presets: `"assumptions"` (grey), `"calculations"` (blue), `"outputs"` (yellow).

## Excel format requirements

### Key-value tables (assumptions)

```
Column A: Parameter name (becomes index)
Column B: Value
Column C: Unit (optional)
```

Example:
```
| Parameter          | Value | Unit  |
|--------------------|-------|-------|
| Spot Price         | 50    | EUR   |
| Dividend           | 3.3   | EUR   |
| Implied Vol        | 0.4   | %     |
```

### Regular tables

```
Row 1: Column headers
Row 2+: Data rows
```

The library uses the first row as column headers, creates an index from Column A, and applies formatting to all cells.

## Styling details

### Number formatting

- Integers: comma separators (1,000)
- Floats < 1: 4 decimal places (0.0489)
- Floats >= 1: 2 decimal places with commas (1,234.56)
- Null values: empty string

### Cell styling

All styles are applied as inline CSS, so they work in Jupyter notebook HTML display, Quarto conversion to LaTeX, and PDF output via LaTeX.

### Font

Default fonts (configurable): Palatino (text), Inconsolata (tables), Fira Code (code).

## Quarto/LaTeX integration

The library outputs HTML with inline styles. When Quarto processes the notebook:

1. Jupyter displays styled HTML tables
2. Quarto converts HTML to LaTeX
3. LaTeX compiles to PDF with styles preserved

Note: this library handles the Jupyter to HTML step. Your `preamble.tex` handles LaTeX-level styling.

## Example workflow

```python
# In your Jupyter notebook
from finmodel import ExcelReader, FinancialTable

# 1. Read Excel
reader = ExcelReader('data/model.xlsx')
df = reader.read_key_value_table('Assumptions')

# 2. Apply styling
assumptions = FinancialTable(df, style="assumptions")

# 3. Display (renders in Jupyter, compiles through Quarto to PDF)
assumptions
```

## Advanced usage

### Custom DataFrame styling

```python
import pandas as pd
from finmodel import FinancialTable

df = pd.DataFrame({
    'Strike': [45, 50, 55],
    'Call Price': [5.2, 2.8, 1.1],
    'Put Price': [0.3, 1.5, 4.8]
})

table = FinancialTable(df, style="calculations")
table.display()
```

### Multiple tables in sequence

```python
reader = ExcelReader('data.xlsx')

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

assumptions.display()
calculations.display()
outputs.display()
```

## Troubleshooting

### "No module named finmodel"

Make sure the directory is in your Python path:
```python
import sys
sys.path.append('/path/to/financial_model_report_automation')
from finmodel import ExcelReader, FinancialTable
```

### Styles not showing in PDF

Check that:
1. Styles render correctly in the Jupyter notebook first
2. Your `preamble.tex` does not override HTML table styles
3. Quarto is processing with `keep-tex: true` to debug LaTeX

## License

For educational and professional use.
