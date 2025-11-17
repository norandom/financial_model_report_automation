# finmodel Library - Usage Examples

## Basic Usage in Jupyter

### 1. Import the library

```python
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader, FinancialTable
```

### 2. Read the BASF options data

```python
# Read Excel file
reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')

# Read as key-value table (Column A = index)
df = reader.read_key_value_table('BASF Optionsdaten', start_row=3, end_row=17)
```

### 3. Apply declarative styling

```python
# Just say "assumptions" - all styling is applied automatically!
table = FinancialTable(df, style="assumptions")

# Display in Jupyter (works with Quarto)
table
```

That's it! The table will show with:
- ✅ Grey background (#D9D9D9)
- ✅ Column A (index) styled as labels
- ✅ Bold headers
- ✅ Right-aligned data
- ✅ Proper number formatting
- ✅ Black borders

## Complete Example

```python
# In your Jupyter notebook cell:
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader, FinancialTable

# Read and style in one go
reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
df = reader.read_key_value_table('BASF Optionsdaten', start_row=3, end_row=17)

# Display with assumptions styling
FinancialTable(df, style="assumptions")
```

## Reading Different Sections

```python
# BASF stock data (rows 3-7)
stock_data = reader.read_key_value_table('BASF Optionsdaten', start_row=3, end_row=7)
FinancialTable(stock_data, style="assumptions")

# Options data (rows 10-17)
options_data = reader.read_key_value_table('BASF Optionsdaten', start_row=10, end_row=17)
FinancialTable(options_data, style="assumptions")
```

## Using Different Style Presets

```python
from finmodel import FinancialTable
import pandas as pd

# Assumptions (grey) - for inputs
df_inputs = pd.DataFrame({
    'Parameter': ['Spot Price', 'Strike', 'Volatility'],
    'Value': [50, 48, 0.4]
})
df_inputs.set_index('Parameter', inplace=True)
FinancialTable(df_inputs, style="assumptions")

# Calculations (blue) - for intermediate results
df_calcs = pd.DataFrame({
    'd1': [0.523],
    'd2': [0.123],
    'N(d1)': [0.699]
})
FinancialTable(df_calcs, style="calculations")

# Outputs (yellow) - for final results
df_results = pd.DataFrame({
    'Call Price': [5.24],
    'Put Price': [2.85]
})
FinancialTable(df_results, style="outputs")
```

## Workflow for Quarto

1. **Write notebook** with finmodel tables
2. **Compile with Quarto**: `./make_pdf.sh`
3. **PDF output** preserves all styling

The library outputs HTML that Quarto converts to LaTeX automatically.

## Number Formatting

The library automatically formats numbers:

```python
# Integer with commas
1000 → "1,000"

# Float with 2 decimals
1234.5678 → "1,234.57"

# Small float with 4 decimals (percentages)
0.0489 → "0.0489"
```

## Tips

### Tip 1: Auto-display
Just put the table object as the last line in a cell - it displays automatically:
```python
reader = ExcelReader('data.xlsx')
df = reader.read_key_value_table('Sheet1')
FinancialTable(df, style="assumptions")  # ← No need for .display()
```

### Tip 2: Chain operations
```python
# One-liner
FinancialTable(
    ExcelReader('data.xlsx').read_key_value_table('Sheet1'),
    style="assumptions"
)
```

### Tip 3: Check available sheets
```python
reader = ExcelReader('data.xlsx')
print(reader.sheet_names)
```

## Color Reference

### Assumptions (Grey)
- Background: `#D9D9D9`
- Text: `#000000` (black)
- Use for: Inputs, parameters, constants

### Calculations (Blue)
- Header: `#4472C4`
- Index: `#D9E2F3` (light blue)
- Data: `#FFFFFF` (white)
- Use for: Formulas, intermediate calculations

### Outputs (Yellow/Orange)
- Header: `#FFC000`
- Cells: `#FFF2CC` (light yellow)
- Use for: Final results, key metrics
