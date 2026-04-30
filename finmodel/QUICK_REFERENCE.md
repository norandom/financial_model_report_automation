# finmodel -- quick reference

## One-line usage

```python
import sys; sys.path.append('/path/to/project')
from finmodel import ExcelReader, FinancialTable

# Read Excel and display with grey styling (assumptions)
FinancialTable(
    ExcelReader('data/model.xlsx')
    .read_key_value_table('Assumptions'),
    style="assumptions"
)
```

## API cheat sheet

### ExcelReader

| Method | Usage | Returns |
|--------|-------|---------|
| `ExcelReader(filepath)` | Open Excel file | Reader object |
| `.sheet_names` | List sheets | `['Sheet1', ...]` |
| `.read_key_value_table(sheet, start_row, end_row)` | Read key-value format | DataFrame |
| `.read_table(region)` | Read table region | DataFrame |
| `.detect_tables(sheet)` | Find tables | List[TableRegion] |

### FinancialTable

| Method | Usage | Returns |
|--------|-------|---------|
| `FinancialTable(df, style="assumptions")` | Create styled table | Table object |
| `.display()` | Show in Jupyter | None (displays) |
| Just type the object | Auto-display | None (displays) |

### Style presets

| Preset | Color | Use for |
|--------|-------|---------|
| `"assumptions"` | Grey (#D9D9D9) | Inputs, parameters |
| `"calculations"` | Blue (#4472C4) | Formulas, calcs |
| `"outputs"` | Yellow (#FFC000) | Results, metrics |

## Common patterns

### Pattern 1: single table
```python
reader = ExcelReader('data.xlsx')
df = reader.read_key_value_table('Sheet1')
FinancialTable(df, style="assumptions")
```

### Pattern 2: multiple tables
```python
reader = ExcelReader('data.xlsx')

inputs = FinancialTable(
    reader.read_key_value_table('Data', start_row=1, end_row=10),
    style="assumptions"
)

results = FinancialTable(
    reader.read_key_value_table('Data', start_row=15, end_row=20),
    style="outputs"
)

inputs.display()
results.display()
```

### Pattern 3: from dict
```python
import pandas as pd

df = pd.DataFrame({
    'Strike': [45, 50, 55],
    'Call': [5.2, 2.8, 1.1]
})

FinancialTable(df, style="calculations")
```

## Styling details

### Assumptions (grey)
```
+----------------------------------+
| Parameter        | Value | Unit  | <- Bold, grey bg
|----------------------------------|
| Spot Price       | 50    | EUR   | <- Grey bg
| Strike           | 48    | EUR   | <- Grey bg
+----------------------------------+
     ^                ^
   Left align     Right align
   (index)        (data)
```

### What gets styled

- Headers: bold, left-aligned
- Index (Column A): same background as data, left-aligned
- Data cells: right-aligned
- Borders: black, 1px solid
- Font: configurable (default Inconsolata), 10pt
- Numbers: formatted with commas and decimals

## Excel format expected

### Key-value tables
```
Column A: Label/parameter name -> becomes index
Column B: Value
Column C: Unit (optional)
```

Example:
```
WKN              | BASF11        |
ISIN             | DE000BASF111  |
Kurs (Spotpreis) | 50            | EUR
```

### Regular tables
```
Row 1: Headers
Row 2+: Data
First column -> index
```

## Tips

1. Always add the project to your path first:
   ```python
   import sys
   sys.path.append('/path/to/project')
   ```

2. The last line in a Jupyter cell auto-displays:
   ```python
   FinancialTable(df, style="assumptions")  # Shows automatically
   ```

3. Works with `./make_pdf.sh` for PDF output.

4. Number formatting is automatic based on value type:
   - Integers: `1,000`
   - Floats >= 1: `1,234.56`
   - Floats < 1: `0.0489`

## Color codes

```python
# Grey (Assumptions)
"#D9D9D9"  # Background
"#000000"  # Text (black)

# Blue (Calculations)
"#4472C4"  # Header
"#D9E2F3"  # Index/light blue
"#FFFFFF"  # Data (white)

# Yellow (Outputs)
"#FFC000"  # Header (orange)
"#FFF2CC"  # Cells (light yellow)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named finmodel` | Add path: `sys.path.append(...)` |
| `No module named openpyxl` | Install openpyxl |
| Styles not showing | Check HTML output first, then Quarto conversion |
| Wrong colors | Verify style name: `"assumptions"`, `"calculations"`, or `"outputs"` |

## Example output

```python
# This code:
reader = ExcelReader('data.xlsx')
df = reader.read_key_value_table('Sheet1')
FinancialTable(df, style="assumptions")

# Produces:
# +-------------------------------------------+
# |                           | Value | Unit  |
# |-------------------------------------------|
# | Optionsdaten              |       |       |
# | Ausübungspreis Call       | 48    | EUR   |
# | Ausübungspreis Put        | 52    | EUR   |
# | Kurs (Spotpreis)          | 50    | EUR   |
# | Dividendenrendite         | 0.0489| %     |
# | Implizite Volatilitat     | 0.4   | %     |
# | Laufzeit                  | 1     | Jahre |
# | Risikoloser Zins          | 0.005 | %     |
# +-------------------------------------------+
#   All cells get grey background and proper formatting.
```
