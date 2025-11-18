# finmodel - Quick Reference

## One-Line Usage

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

## API Cheat Sheet

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

### Style Presets

| Preset | Color | Use For |
|--------|-------|---------|
| `"assumptions"` | Grey (#D9D9D9) | Inputs, parameters |
| `"calculations"` | Blue (#4472C4) | Formulas, calcs |
| `"outputs"` | Yellow (#FFC000) | Results, metrics |

## Common Patterns

### Pattern 1: Single Table
```python
reader = ExcelReader('data.xlsx')
df = reader.read_key_value_table('Sheet1')
FinancialTable(df, style="assumptions")
```

### Pattern 2: Multiple Tables
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

### Pattern 3: From Dict
```python
import pandas as pd

df = pd.DataFrame({
    'Strike': [45, 50, 55],
    'Call': [5.2, 2.8, 1.1]
})

FinancialTable(df, style="calculations")
```

## Styling Details

### Assumptions (Grey)
```
┌─────────────────────────────────┐
│ Parameter        │ Value │ Unit │ ← Bold, grey bg
├─────────────────────────────────┤
│ Spot Price       │ 50    │ EUR  │ ← Grey bg
│ Strike           │ 48    │ EUR  │ ← Grey bg
└─────────────────────────────────┘
     ↑                ↑
   Left align     Right align
   (index)        (data)
```

### What Gets Styled

- ✅ Headers: Bold, left-aligned
- ✅ Index (Column A): Same background as data, left-aligned
- ✅ Data cells: Right-aligned
- ✅ Borders: Black, 1px solid
- ✅ Font: Configurable (Default: Inconsolata), 10pt
- ✅ Numbers: Formatted with commas and decimals

## Excel Format Expected

### Key-Value Tables
```
Column A: Label/parameter name → becomes index
Column B: Value
Column C: Unit (optional)
```

Example:
```
WKN              | BASF11        |
ISIN             | DE000BASF111  |
Kurs (Spotpreis) | 50            | EUR
```

### Regular Tables
```
Row 1: Headers
Row 2+: Data
First column → index
```

## Tips

1. **Path in Jupyter**: Always add project to path first
   ```python
   import sys
   sys.path.append('/path/to/project')
   ```

2. **Auto-display**: Last line in cell auto-displays
   ```python
   FinancialTable(df, style="assumptions")  # Shows automatically
   ```

3. **Quarto compatibility**: Works seamlessly with `./make_pdf.sh`

4. **Number formatting**: Automatic based on value type
   - Integers: `1,000`
   - Floats ≥ 1: `1,234.56`
   - Floats < 1: `0.0489`

## Color Codes

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

## Example Output

```python
# This code:
reader = ExcelReader('data.xlsx')
df = reader.read_key_value_table('Sheet1')
FinancialTable(df, style="assumptions")

# Produces:
# ┌──────────────────────────────────────────┐
# │                           │ Value │ Unit │
# ├──────────────────────────────────────────┤
# │ Optionsdaten              │       │      │
# │ Ausübungspreis Call       │ 48    │ EUR  │
# │ Ausübungspreis Put        │ 52    │ EUR  │
# │ Kurs (Spotpreis)          │ 50    │ EUR  │
# │ Dividendenrendite         │ 0.0489│ %    │
# │ Implizite Volatilität     │ 0.4   │ %    │
# │ Laufzeit                  │ 1     │ Jahre│
# │ Risikoloser Zins          │ 0.005 │ %    │
# └──────────────────────────────────────────┘
#   All with grey background and proper formatting!
```
