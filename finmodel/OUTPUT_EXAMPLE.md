# Financial Model Output Formatting

## Overview

The library provides three color-coded styles following Excel financial modeling conventions:

| Style | Color | Use Case | Function |
|-------|-------|----------|----------|
| **assumptions** | Grey | Inputs/parameters | `read_basf_options()` |
| **calculations** | Blue | Intermediate results | `FinancialTable(df, style='calculations')` |
| **outputs** | Yellow | Final results | `finmodel_output()` |

## Complete Example: Black-Scholes Model

```python
import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import read_basf_options, finmodel_output, FinancialTable
import pandas as pd
import numpy as np
from scipy.stats import norm

# ═══════════════════════════════════════════════════════════════
# 1. INPUTS (Grey - Assumptions)
# ═══════════════════════════════════════════════════════════════

data = read_basf_options()

# Display inputs with grey styling
print("## Eingabeparameter")
data.options_table

# Extract values for calculations
S = data.options_df.loc['Kurs (Spotpreis)', 'Value']
K_call = data.options_df.loc['Ausübungspreis Call', 'Value']
K_put = data.options_df.loc['Ausübungspreis Put', 'Value']
sigma = data.options_df.loc['Implizite Volatilität', 'Value']
T = data.options_df.loc['Laufzeit', 'Value']
r = data.options_df.loc['Risikoloser Zins', 'Value']

# ═══════════════════════════════════════════════════════════════
# 2. CALCULATIONS (Blue - Intermediate)
# ═══════════════════════════════════════════════════════════════

# Black-Scholes calculations
d1_call = (np.log(S/K_call) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2_call = d1_call - sigma*np.sqrt(T)

d1_put = (np.log(S/K_put) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
d2_put = d1_put - sigma*np.sqrt(T)

# Display intermediate calculations with blue styling
calc_data = pd.DataFrame({
    'Value': [d1_call, d2_call, norm.cdf(d1_call), norm.cdf(d2_call)]
}, index=['d1 (Call)', 'd2 (Call)', 'N(d1)', 'N(d2)'])

print("\n## Zwischenrechnungen")
FinancialTable(calc_data, style='calculations')

# ═══════════════════════════════════════════════════════════════
# 3. OUTPUTS (Yellow - Results)
# ═══════════════════════════════════════════════════════════════

# Calculate final prices
call_price = S * norm.cdf(d1_call) - K_call * np.exp(-r*T) * norm.cdf(d2_call)
put_price = K_put * np.exp(-r*T) * norm.cdf(-d2_put) - S * norm.cdf(-d1_put)

# Calculate Greeks
call_delta = norm.cdf(d1_call)
put_delta = call_delta - 1
gamma = norm.pdf(d1_call) / (S * sigma * np.sqrt(T))
vega = S * norm.pdf(d1_call) * np.sqrt(T)
call_theta = (-S * norm.pdf(d1_call) * sigma / (2*np.sqrt(T)) 
              - r * K_call * np.exp(-r*T) * norm.cdf(d2_call))

# Display final results with yellow styling
results = {
    'Call Preis': call_price,
    'Put Preis': put_price,
    'Call Delta': call_delta,
    'Put Delta': put_delta,
    'Gamma': gamma,
    'Vega': vega,
    'Call Theta': call_theta
}

print("\n## Ausgabe")
finmodel_output(results)
```

## Expected Output

### 1. Eingabeparameter (Grey)
```
                         Value   Unit
Ausübungspreis Call    48.0000    EUR  ← Grey background
Ausübungspreis Put     52.0000    EUR  ← Grey background
Kurs (Spotpreis)       50.0000    EUR  ← Grey background
...
```

### 2. Zwischenrechnungen (Blue)
```
           Value
d1 (Call)  0.523  ← Light blue background
d2 (Call)  0.123  ← Light blue background
N(d1)      0.699  ← Light blue background
N(d2)      0.549  ← Light blue background
```

### 3. Ausgabe (Yellow)
```
              Value
Call Preis    5.24  ← Yellow background
Put Preis     2.85  ← Yellow background
Call Delta    0.68  ← Yellow background
Put Delta    -0.32  ← Yellow background
Gamma         0.04  ← Yellow background
Vega          0.15  ← Yellow background
Call Theta   -0.01  ← Yellow background
```

## API Reference

### `finmodel_output(data, title="Ausgabe")`

Creates yellow-styled output table for final results.

**Parameters:**
- `data`: Dict, list of tuples, or DataFrame
- `title`: Section title (default: "Ausgabe")

**Returns:** `FinancialTable` with yellow styling

**Accepts:**

```python
# From dict
results = {'Call Preis': 5.24, 'Put Preis': 2.85}
finmodel_output(results)

# From list of tuples
results = [('Call Preis', 5.24), ('Put Preis', 2.85)]
finmodel_output(results)

# From DataFrame
df = pd.DataFrame({'Value': [5.24, 2.85]}, index=['Call', 'Put'])
finmodel_output(df)
```

## Styling Details

### Assumptions (Grey - `style='assumptions'`)
- **Labels:** Bold, no background
- **Values:** Grey background (#D9D9D9)
- **Use for:** Input parameters, constants

### Calculations (Blue - `style='calculations'`)
- **Labels:** Bold, light blue background (#D9E2F3)
- **Values:** White background
- **Headers:** Blue (#4472C4)
- **Use for:** Intermediate calculations, formulas

### Outputs (Yellow - `style='outputs'`)
- **Labels:** Bold, light yellow background (#FFF2CC)
- **Values:** Light yellow background (#FFF2CC)
- **Headers:** Orange (#FFC000)
- **Use for:** Final results, model outputs

## Complete Workflow

```python
from finmodel import read_basf_options, finmodel_output, FinancialTable

# 1. Load inputs (grey)
data = read_basf_options()
data.options_table

# 2. Do calculations
# ... your model code ...

# 3. Show intermediate results (blue)
intermediate = pd.DataFrame({'Value': [d1, d2]}, index=['d1', 'd2'])
FinancialTable(intermediate, style='calculations')

# 4. Show final results (yellow)
results = {'Call Preis': call_price, 'Put Preis': put_price}
finmodel_output(results)
```

## Visual Guide

```
┌─────────────────────────────────────────────────┐
│  EINGABEPARAMETER (Grey)                        │
├─────────────────────────────────────────────────┤
│  Parameter               │ Value  │ Unit        │
│  Kurs (Spotpreis)        │ 50     │ EUR   ← Grey│
│  Implizite Volatilität   │ 0.4    │ %     ← Grey│
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  ZWISCHENRECHNUNGEN (Blue)                      │
├─────────────────────────────────────────────────┤
│  Calculation    │ Value                         │
│  d1             │ 0.523    ← Light blue         │
│  d2             │ 0.123    ← Light blue         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  AUSGABE (Yellow)                               │
├─────────────────────────────────────────────────┤
│  Result         │ Value                         │
│  Call Preis     │ 5.24     ← Yellow             │
│  Put Preis      │ 2.85     ← Yellow             │
└─────────────────────────────────────────────────┘
```

## Tips

1. **Consistent colors** help readers understand data flow:
   - Grey → you input this
   - Blue → model calculates this
   - Yellow → final answer

2. **Keep output tables focused** - only show key results, not intermediate steps

3. **Use meaningful labels** in German or English:
   ```python
   results = {
       'Call-Option Preis': call_price,
       'Put-Option Preis': put_price
   }
   ```

4. **Round values appropriately**:
   ```python
   results = {
       'Call Preis': round(call_price, 4),
       'Put Preis': round(put_price, 4)
   }
   ```

5. **Add units if needed**:
   ```python
   df = pd.DataFrame({
       'Value': [5.24, 2.85],
       'Unit': ['EUR', 'EUR']
   }, index=['Call Preis', 'Put Preis'])
   finmodel_output(df)
   ```
