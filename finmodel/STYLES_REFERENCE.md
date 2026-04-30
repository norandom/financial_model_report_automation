# finmodel style reference

## Available styles

### 1. standard (default)
- Light blue headers (#8FAADC), white data cells
- General purpose table style
  ```python
  FinancialTable(df)  # Uses standard by default
  FinancialTable(df, style='standard')
  ```

### 2. input_data
- Light orange (#FDE9D9) data cells, white headers
- For input data tables
  ```python
  FinancialTable(df, style='input_data')
  ```

### 3. calc_and_output
- Light grey (#F2F2F2) data cells, white headers
- For calculations and intermediate outputs
  ```python
  FinancialTable(df, style='calc_and_output')
  ```

### 4. formulas_or_refs
- Light green (#E2EFDA) data cells, white headers
- For formula tables or reference data
  ```python
  FinancialTable(df, style='formulas_or_refs')
  ```

### 5. plausibility
- Light violet (#E9D7F3) data cells, white headers
- For plausibility checks and validation tables
  ```python
  FinancialTable(df, style='plausibility')
  ```

### 6. results
- Yellow (#FFF2CC) data cells, orange/yellow headers (#FFC000)
- For final results and outputs
  ```python
  FinancialTable(df, style='results')
  finmodel_output(data)  # Uses results style by default
  ```

### 7. assumptions
- Grey (#D9D9D9) data cells, no header background
- For model assumptions and input parameters
  ```python
  FinancialTable(df, style='assumptions')
  ```

## Backwards compatibility

Old style names still work as aliases:
- `'calculations'` maps to `'standard'`
- `'outputs'` maps to `'results'`

## Color palette

| Style | Header BG | Data BG | Description |
|-------|-----------|---------|-------------|
| standard | #8FAADC (light blue) | #FFFFFF (white) | Default |
| input_data | #FFFFFF (white) | #FDE9D9 (light orange) | Inputs |
| calc_and_output | #FFFFFF (white) | #F2F2F2 (light grey) | Calculations |
| formulas_or_refs | #FFFFFF (white) | #E2EFDA (light green) | Formulas |
| plausibility | #FFFFFF (white) | #E9D7F3 (light violet) | Checks |
| results | #FFC000 (orange/yellow) | #FFF2CC (light yellow) | Outputs |
| assumptions | None | #D9D9D9 (grey) | Assumptions |

## Usage examples

```python
from finmodel import FinancialTable, finmodel_output
import pandas as pd

# Input data table
input_df = pd.DataFrame({'Price': [50, 55], 'Quantity': [100, 90]}, 
                        index=['Stock A', 'Stock B'])
FinancialTable(input_df, style='input_data')

# Calculations table
calc_df = pd.DataFrame({'Total': [5000, 4950]}, 
                       index=['Stock A', 'Stock B'])
FinancialTable(calc_df, style='calc_and_output')

# Results table (using finmodel_output)
results = {
    'Total Revenue': 9950,
    'Average Price': 52.5
}
finmodel_output(results)  # Uses 'results' style
```

## LaTeX color codes

All styles render with proper color codes in both HTML (Jupyter) and LaTeX (PDF) output. HTML uses inline `background-color` styles; LaTeX uses `\cellcolor[HTML]{...}` commands.
