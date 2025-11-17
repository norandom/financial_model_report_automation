# BASF Options Data - Quick Usage

## The Easy Way (Recommended)

Use the convenience function that returns two separate DataFrames:

```python
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import read_basf_options

# Load data
data = read_basf_options()

# Access stock data
spot_stock = data.stock_df.loc['Kurs (Spotpreis)', 'Value']
dividende = data.stock_df.loc['Dividende', 'Value']

# Access options data (completely separate!)
spot_options = data.options_df.loc['Kurs (Spotpreis)', 'Value']
volatility = data.options_df.loc['Implizite Volatilität', 'Value']
strike_call = data.options_df.loc['Ausübungspreis Call', 'Value']

# Display styled tables
data.stock_table      # Auto-displays BASF Aktie
data.options_table    # Auto-displays Optionsdaten
```

## What You Get

`read_basf_options()` returns a `BASFData` named tuple with 4 attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `stock_df` | DataFrame | BASF Aktie data (WKN, ISIN, Spot, Dividende) |
| `options_df` | DataFrame | Optionsdaten (Strike, Spot, Vol, etc.) |
| `stock_table` | FinancialTable | Styled table for stock data |
| `options_table` | FinancialTable | Styled table for options data |

## Complete Example

```python
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import read_basf_options

# Load
data = read_basf_options()

# ============================================================
# Access BASF Aktie data
# ============================================================
print("BASF Stock Data:")
print(data.stock_df)

wkn = data.stock_df.loc['WKN', 'Value']
spot = data.stock_df.loc['Kurs (Spotpreis)', 'Value']
div = data.stock_df.loc['Dividende', 'Value']

print(f"WKN: {wkn}")
print(f"Spot: {spot} EUR")
print(f"Dividend: {div} EUR")

# ============================================================
# Access Optionsdaten (completely separate!)
# ============================================================
print("\nOptions Data:")
print(data.options_df)

strike_call = data.options_df.loc['Ausübungspreis Call', 'Value']
strike_put = data.options_df.loc['Ausübungspreis Put', 'Value']
vol = data.options_df.loc['Implizite Volatilität', 'Value']
rate = data.options_df.loc['Risikoloser Zins', 'Value']
maturity = data.options_df.loc['Laufzeit', 'Value']

print(f"Call Strike: {strike_call} EUR")
print(f"Put Strike: {strike_put} EUR")
print(f"Volatility: {vol}")
print(f"Risk-free rate: {rate}")
print(f"Maturity: {maturity} Jahre")

# ============================================================
# Display styled tables in Jupyter
# ============================================================
print("\nBASF Aktie:")
data.stock_table

print("\nOptionsdaten:")
data.options_table
```

## Output

```
BASF Stock Data:
                         Value  Unit
WKN                     BASF11  None
ISIN              DE000BASF111  None
Kurs (Spotpreis)            50   EUR
Dividende                  3.3   EUR

WKN: BASF11
Spot: 50 EUR
Dividend: 3.3 EUR

Options Data:
                         Value   Unit
Ausübungspreis Call    48.0000    EUR
Ausübungspreis Put     52.0000    EUR
Kurs (Spotpreis)       50.0000    EUR
Dividendenrendite       0.0489      %
Implizite Volatilität   0.4000      %
Laufzeit                1.0000  Jahre
Risikoloser Zins        0.0050      %

Call Strike: 48.0 EUR
Put Strike: 52.0 EUR
Volatility: 0.4
Risk-free rate: 0.005
Maturity: 1.0 Jahre
```

## Why This Approach?

✅ **Clear separation**: `data.stock_df` vs `data.options_df` - no confusion  
✅ **No duplicate names**: "Kurs (Spotpreis)" appears in both, but accessed separately  
✅ **Type hints**: IDE autocomplete shows `.stock_df`, `.options_df`, etc.  
✅ **Both raw and styled**: DataFrames for calculations, tables for display  
✅ **One line to load**: `data = read_basf_options()` - that's it!

## Alternative: Manual Approach

If you need more control:

```python
from finmodel import ExcelReader

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
tables = reader.read_all_tables('BASF Optionsdaten', style='assumptions')

# Unpack
stock_name, stock_table = tables[0]
options_name, options_table = tables[1]

# Access
stock_df = stock_table.df
options_df = options_table.df
```

But `read_basf_options()` is cleaner!

## Index Values Reference

### BASF Aktie (stock_df)
- `'WKN'`
- `'ISIN'`
- `'Kurs (Spotpreis)'`
- `'Dividende'`

### Optionsdaten (options_df)
- `'Ausübungspreis Call'`
- `'Ausübungspreis Put'`
- `'Kurs (Spotpreis)'`
- `'Dividendenrendite'`
- `'Implizite Volatilität'`
- `'Laufzeit'`
- `'Risikoloser Zins'`

## Pro Tips

### 1. Extract values with units
```python
value = data.options_df.loc['Implizite Volatilität', 'Value']
unit = data.options_df.loc['Implizite Volatilität', 'Unit']
print(f"Volatility: {value} {unit}")  # 0.4 %
```

### 2. Filter by unit
```python
# Get all EUR values from options
eur_params = data.options_df[data.options_df['Unit'] == 'EUR']
print(eur_params)
```

### 3. Use in calculations
```python
S = data.options_df.loc['Kurs (Spotpreis)', 'Value']
K = data.options_df.loc['Ausübungspreis Call', 'Value']
sigma = data.options_df.loc['Implizite Volatilität', 'Value']
T = data.options_df.loc['Laufzeit', 'Value']
r = data.options_df.loc['Risikoloser Zins', 'Value']

# Now use in Black-Scholes, etc.
```

### 4. Display side by side
```python
from IPython.display import display, HTML

display(HTML("<h3>BASF Aktie</h3>"))
data.stock_table.display()

display(HTML("<h3>Optionsdaten</h3>"))
data.options_table.display()
```

## Remember: Auto-reload

Add this at the top of your notebook to pick up library changes:

```python
%load_ext autoreload
%autoreload 2
```
