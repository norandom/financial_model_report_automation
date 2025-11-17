# finmodel_output() - Multiple Columns Guide

## Overview

`finmodel_output()` now supports **multiple columns** with **custom headers**.

## Basic Usage

### Single Column (Default)

```python
from finmodel import finmodel_output

# Simple dict
results = {'Call Preis': 5.24, 'Put Preis': 2.85}
finmodel_output(results)
```

Output:
```
            Value
Call Preis   5.24
Put Preis    2.85
```

### Single Column with Custom Header

```python
results = {'Call Preis': 5.24, 'Put Preis': 2.85}
finmodel_output(results, columns=['Preis (EUR)'])
```

Output:
```
            Preis (EUR)
Call Preis         5.24
Put Preis          2.85
```

## Multiple Columns

### Method 1: Dict of Lists

```python
results = {
    'Call': [5.24, 0.68, 0.042],
    'Put': [2.85, -0.32, 0.042]
}
finmodel_output(results, columns=['Preis', 'Delta', 'Gamma'])
```

Output:
```
      Preis  Delta  Gamma
Call   5.24   0.68  0.042
Put    2.85  -0.32  0.042
```

### Method 2: List of Tuples

```python
results = [
    ('Call', 5.24, 0.68, 0.042),
    ('Put', 2.85, -0.32, 0.042)
]
finmodel_output(results, columns=['Preis', 'Delta', 'Gamma'])
```

Output:
```
      Preis  Delta  Gamma
Call   5.24   0.68  0.042
Put    2.85  -0.32  0.042
```

### Method 3: DataFrame

```python
import pandas as pd

df = pd.DataFrame({
    'Price': [5.24, 2.85],
    'Delta': [0.68, -0.32],
    'Gamma': [0.042, 0.042]
}, index=['Call', 'Put'])

finmodel_output(df)  # Uses existing column names
```

Or rename columns:

```python
finmodel_output(df, columns=['Preis (EUR)', 'Delta', 'Gamma'])
```

## Complete Example: Black-Scholes Greeks

```python
from finmodel import read_basf_options, finmodel_output
import numpy as np
from scipy.stats import norm

# Load inputs
data = read_basf_options()
S = data.options_df.loc['Kurs (Spotpreis)', 'Value']
K_call = data.options_df.loc['Ausübungspreis Call', 'Value']
K_put = data.options_df.loc['Ausübungspreis Put', 'Value']
sigma = data.options_df.loc['Implizite Volatilität', 'Value']
T = data.options_df.loc['Laufzeit', 'Value']
r = data.options_df.loc['Risikoloser Zins', 'Value']

# Calculate Black-Scholes
d1_call = (np.log(S/K_call) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2_call = d1_call - sigma*np.sqrt(T)
d1_put = (np.log(S/K_put) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2_put = d1_put - sigma*np.sqrt(T)

call_price = S * norm.cdf(d1_call) - K_call * np.exp(-r*T) * norm.cdf(d2_call)
put_price = K_put * np.exp(-r*T) * norm.cdf(-d2_put) - S * norm.cdf(-d1_put)

call_delta = norm.cdf(d1_call)
put_delta = call_delta - 1

gamma = norm.pdf(d1_call) / (S * sigma * np.sqrt(T))
vega = S * norm.pdf(d1_call) * np.sqrt(T)

call_theta = (-S * norm.pdf(d1_call) * sigma / (2*np.sqrt(T)) 
              - r * K_call * np.exp(-r*T) * norm.cdf(d2_call))
put_theta = (-S * norm.pdf(d1_put) * sigma / (2*np.sqrt(T)) 
             + r * K_put * np.exp(-r*T) * norm.cdf(-d2_put))

# Display results with multiple columns
results = {
    'Call': [call_price, call_delta, gamma, vega, call_theta],
    'Put': [put_price, put_delta, gamma, vega, put_theta]
}

finmodel_output(results, columns=['Preis', 'Delta', 'Gamma', 'Vega', 'Theta'])
```

Output (yellow table):
```
      Preis   Delta   Gamma    Vega   Theta
Call   8.92    0.62    0.019    19.9  -0.012
Put    6.74   -0.38    0.019    19.9  -0.008
```

## Format Reference

### 1. Simple Dict (Single Value)

```python
data = {'Label 1': value1, 'Label 2': value2}
finmodel_output(data)
# OR
finmodel_output(data, columns=['Custom Header'])
```

### 2. Dict of Lists (Multiple Columns)

```python
data = {
    'Row1': [val1, val2, val3],
    'Row2': [val4, val5, val6]
}
finmodel_output(data, columns=['Col1', 'Col2', 'Col3'])
```

Row names = dict keys  
Column values = list items  
**Must specify `columns` parameter!**

### 3. List of Tuples (Single Value)

```python
data = [
    ('Label 1', value1),
    ('Label 2', value2)
]
finmodel_output(data)
# OR
finmodel_output(data, columns=['Custom Header'])
```

### 4. List of Tuples (Multiple Columns)

```python
data = [
    ('Row1', val1, val2, val3),
    ('Row2', val4, val5, val6)
]
finmodel_output(data, columns=['Col1', 'Col2', 'Col3'])
```

First tuple element = row label  
Remaining elements = column values  
**Must specify `columns` parameter!**

### 5. DataFrame

```python
df = pd.DataFrame({
    'Col1': [val1, val2],
    'Col2': [val3, val4]
}, index=['Row1', 'Row2'])

finmodel_output(df)  # Uses existing columns
# OR
finmodel_output(df, columns=['New Col1', 'New Col2'])  # Rename
```

## Styling

All formats produce **yellow tables** (Excel output style):

- **Labels (index)**: Bold, light yellow background (#FFF2CC)
- **Values**: Light yellow background (#FFF2CC), right-aligned
- **Headers**: Bold, orange background (#FFC000)

## Tips

### Tip 1: Round Your Values

```python
results = {
    'Call': [round(call_price, 4), round(call_delta, 4)],
    'Put': [round(put_price, 4), round(put_delta, 4)]
}
finmodel_output(results, columns=['Preis', 'Delta'])
```

### Tip 2: Use German Headers

```python
finmodel_output(results, columns=['Preis (EUR)', 'Delta', 'Gamma'])
```

### Tip 3: Organize Results

```python
# Group by metric (rows = options, cols = greeks)
results_by_option = {
    'Call': [price_call, delta_call, gamma],
    'Put': [price_put, delta_put, gamma]
}
finmodel_output(results_by_option, columns=['Preis', 'Delta', 'Gamma'])

# OR group by greek (rows = greeks, cols = options)
results_by_greek = [
    ('Preis', price_call, price_put),
    ('Delta', delta_call, delta_put),
    ('Gamma', gamma, gamma)
]
finmodel_output(results_by_greek, columns=['Call', 'Put'])
```

### Tip 4: Add Units in Headers

```python
finmodel_output(results, columns=['Preis (EUR)', 'Delta (%)', 'Vega (EUR/σ)'])
```

## Error Handling

### Wrong Number of Columns

```python
# ERROR: 3 values but only 2 column names
results = {
    'Call': [5.24, 0.68, 0.042],
    'Put': [2.85, -0.32, 0.042]
}
finmodel_output(results, columns=['Preis', 'Delta'])  # ❌ ValueError
```

Fix:
```python
finmodel_output(results, columns=['Preis', 'Delta', 'Gamma'])  # ✅
```

### Empty Data

```python
finmodel_output([])  # ❌ ValueError: data list cannot be empty
```

### Invalid Format

```python
finmodel_output([1, 2, 3])  # ❌ ValueError: List items must be tuples or lists
```

Fix:
```python
finmodel_output([('Value 1', 1), ('Value 2', 2)])  # ✅
```

## Comparison with Other Styles

```python
from finmodel import FinancialTable

# Grey (assumptions) - for inputs
FinancialTable(df, style='assumptions')

# Blue (calculations) - for intermediate results
FinancialTable(df, style='calculations')

# Yellow (outputs) - for final results
finmodel_output(df)  # Same as FinancialTable(df, style='outputs')
```

## Advanced: Dynamic Columns

```python
# Calculate variable number of Greeks
greeks = ['Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
call_values = [calculate_greek(greek, 'call') for greek in greeks]
put_values = [calculate_greek(greek, 'put') for greek in greeks]

results = {
    'Call': call_values,
    'Put': put_values
}

finmodel_output(results, columns=greeks)
```

## Summary

| Feature | Syntax |
|---------|--------|
| Single value | `finmodel_output({'Label': value})` |
| Custom single column | `finmodel_output(data, columns=['Header'])` |
| Multiple columns (dict) | `finmodel_output({'Row': [v1, v2]}, columns=['C1', 'C2'])` |
| Multiple columns (list) | `finmodel_output([('Row', v1, v2)], columns=['C1', 'C2'])` |
| From DataFrame | `finmodel_output(df)` or `finmodel_output(df, columns=[...])` |

The `columns` parameter lets you define **any column headers** you want! 🎉
