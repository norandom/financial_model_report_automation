# finmodel_output() -- multiple columns guide

## Overview

`finmodel_output()` supports multiple columns with custom headers.

## Basic usage

### Single column (default)

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

### Single column with custom header

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

## Multiple columns

### Method 1: dict of lists

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

### Method 2: list of tuples

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

## Complete example: Black-Scholes Greeks

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

## Format reference

### 1. Simple dict (single value)

```python
data = {'Label 1': value1, 'Label 2': value2}
finmodel_output(data)
# OR
finmodel_output(data, columns=['Custom Header'])
```

### 2. Dict of lists (multiple columns)

```python
data = {
    'Row1': [val1, val2, val3],
    'Row2': [val4, val5, val6]
}
finmodel_output(data, columns=['Col1', 'Col2', 'Col3'])
```

Row names come from dict keys, column values from list items. You must specify the `columns` parameter.

### 3. List of tuples (single value)

```python
data = [
    ('Label 1', value1),
    ('Label 2', value2)
]
finmodel_output(data)
# OR
finmodel_output(data, columns=['Custom Header'])
```

### 4. List of tuples (multiple columns)

```python
data = [
    ('Row1', val1, val2, val3),
    ('Row2', val4, val5, val6)
]
finmodel_output(data, columns=['Col1', 'Col2', 'Col3'])
```

The first element of each tuple becomes the row label, the rest are column values. You must specify the `columns` parameter.

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

All formats produce yellow tables (Excel output style):

- Labels (index): bold, light yellow background (#FFF2CC)
- Values: light yellow background (#FFF2CC), right-aligned
- Headers: bold, orange background (#FFC000)

## Tips

### Round your values

```python
results = {
    'Call': [round(call_price, 4), round(call_delta, 4)],
    'Put': [round(put_price, 4), round(put_delta, 4)]
}
finmodel_output(results, columns=['Preis', 'Delta'])
```

### Use German headers

```python
finmodel_output(results, columns=['Preis (EUR)', 'Delta', 'Gamma'])
```

### Organize results

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

### Add units in headers

```python
finmodel_output(results, columns=['Preis (EUR)', 'Delta (%)', 'Vega (EUR/sigma)'])
```

## Error handling

### Wrong number of columns

```python
# ERROR: 3 values but only 2 column names
results = {
    'Call': [5.24, 0.68, 0.042],
    'Put': [2.85, -0.32, 0.042]
}
finmodel_output(results, columns=['Preis', 'Delta'])  # ValueError
```

Fix:
```python
finmodel_output(results, columns=['Preis', 'Delta', 'Gamma'])  # OK
```

### Empty data

```python
finmodel_output([])  # ValueError: data list cannot be empty
```

### Invalid format

```python
finmodel_output([1, 2, 3])  # ValueError: List items must be tuples or lists
```

Fix:
```python
finmodel_output([('Value 1', 1), ('Value 2', 2)])  # OK
```

## Comparison with other styles

```python
from finmodel import FinancialTable

# Grey (assumptions) - for inputs
FinancialTable(df, style='assumptions')

# Blue (calculations) - for intermediate results
FinancialTable(df, style='calculations')

# Yellow (outputs) - for final results
finmodel_output(df)  # Same as FinancialTable(df, style='outputs')
```

## Dynamic columns

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

The `columns` parameter controls column headers.
