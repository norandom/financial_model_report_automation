# finmodel Style Reference

## Available Styles

### 1. **standard** (default)
- **Color**: Light blue headers (#8FAADC), white data cells
- **Use case**: Default table style, general purpose
- **Example**:
  ```python
  FinancialTable(df)  # Uses standard by default
  FinancialTable(df, style='standard')
  ```

### 2. **input_data**
- **Color**: Light orange (#FDE9D9) data cells, white headers
- **Use case**: Input data tables
- **Example**:
  ```python
  FinancialTable(df, style='input_data')
  ```

### 3. **calc_and_output**
- **Color**: Light grey (#F2F2F2) data cells, white headers
- **Use case**: Calculations and intermediate outputs
- **Example**:
  ```python
  FinancialTable(df, style='calc_and_output')
  ```

### 4. **formulas_or_refs**
- **Color**: Light green (#E2EFDA) data cells, white headers
- **Use case**: Formula tables or reference data
- **Example**:
  ```python
  FinancialTable(df, style='formulas_or_refs')
  ```

### 5. **plausibility**
- **Color**: Light violet (#E9D7F3) data cells, white headers
- **Use case**: Plausibility checks and validation tables
- **Example**:
  ```python
  FinancialTable(df, style='plausibility')
  ```

### 6. **results**
- **Color**: Yellow (#FFF2CC) data cells, orange/yellow headers (#FFC000)
- **Use case**: Final results and key outputs
- **Example**:
  ```python
  FinancialTable(df, style='results')
  finmodel_output(data)  # Uses results style by default
  ```

### 7. **assumptions**
- **Color**: Grey (#D9D9D9) data cells, no header background
- **Use case**: Model assumptions and input parameters
- **Example**:
  ```python
  FinancialTable(df, style='assumptions')
  ```

## Backwards Compatibility

Old style names still work as aliases:
- `'calculations'` → maps to `'standard'`
- `'outputs'` → maps to `'results'`

## Color Palette

| Style | Header BG | Data BG | Description |
|-------|-----------|---------|-------------|
| standard | #8FAADC (light blue) | #FFFFFF (white) | Default |
| input_data | #FFFFFF (white) | #FDE9D9 (light orange) | Inputs |
| calc_and_output | #FFFFFF (white) | #F2F2F2 (light grey) | Calculations |
| formulas_or_refs | #FFFFFF (white) | #E2EFDA (light green) | Formulas |
| plausibility | #FFFFFF (white) | #E9D7F3 (light violet) | Checks |
| results | #FFC000 (orange/yellow) | #FFF2CC (light yellow) | Outputs |
| assumptions | None | #D9D9D9 (grey) | Assumptions |

## Usage Examples

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
finmodel_output(results)  # Automatically uses 'results' style
```

## LaTeX Color Codes

All styles render with proper color codes in both HTML (Jupyter) and LaTeX (PDF) output:
- HTML: Uses inline `background-color` styles
- LaTeX: Uses `\cellcolor[HTML]{...}` commands
