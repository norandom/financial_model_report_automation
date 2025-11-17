"""
Example usage of finmodel library in Jupyter notebook.

Copy these examples into your notebook cells.
"""

# ═══════════════════════════════════════════════════════════════════════════
# Example 1: Read all tables from BASF Excel file
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader

# Read Excel and detect all tables automatically
reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
tables = reader.read_all_tables('BASF Optionsdaten', style='assumptions')

# Display all tables
for name, table in tables:
    print(f"\n{name}")
    table.display()


# ═══════════════════════════════════════════════════════════════════════════
# Example 2: Display specific table
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
tables = reader.read_all_tables('BASF Optionsdaten', style='assumptions')

# Get just the options data table (second table)
options_name, options_table = tables[1]
options_table  # Auto-displays in Jupyter


# ═══════════════════════════════════════════════════════════════════════════
# Example 3: Use different style presets
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader, FinancialTable

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')

# Get just the tables
stock_tables = reader.read_all_tables('BASF Optionsdaten')

# Display with different styles
stock_name, stock_table_obj = stock_tables[0]

# Assumptions style (grey)
print("As assumptions:")
FinancialTable(stock_table_obj.df, style='assumptions').display()

# Calculations style (blue)
print("\nAs calculations:")
FinancialTable(stock_table_obj.df, style='calculations').display()

# Outputs style (yellow)
print("\nAs outputs:")
FinancialTable(stock_table_obj.df, style='outputs').display()


# ═══════════════════════════════════════════════════════════════════════════
# Example 4: Create table from dict
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import FinancialTable
import pandas as pd

# Create DataFrame manually
df = pd.DataFrame({
    'Value': [48, 52, 50, 0.0489, 0.4],
    'Unit': ['EUR', 'EUR', 'EUR', '%', '%']
}, index=['Strike Call', 'Strike Put', 'Spot', 'Div Yield', 'Volatility'])

# Apply assumptions styling
FinancialTable(df, style='assumptions')


# ═══════════════════════════════════════════════════════════════════════════
# Example 5: Accessing the DataFrame
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')
tables = reader.read_all_tables('BASF Optionsdaten', style='assumptions')

# Get the options data
options_name, options_table = tables[1]

# Access the underlying DataFrame
df = options_table.df

# Use pandas operations
print("Strike Call:", df.loc['Ausübungspreis Call', 'Value'])
print("Volatility:", df.loc['Implizite Volatilität', 'Value'])

# Filter rows
print("\nOnly EUR values:")
print(df[df['Unit'] == 'EUR'])

# Then display styled
options_table.display()


# ═══════════════════════════════════════════════════════════════════════════
# Example 6: Detect tables programmatically
# ═══════════════════════════════════════════════════════════════════════════

import sys
sys.path.insert(0, '/home/jovyan/projects/MBA_S3')

from finmodel import ExcelReader

reader = ExcelReader('Datasets/Options_BASF/basf_optionsdaten.xlsx')

# Detect table regions
regions = reader.detect_key_value_tables('BASF Optionsdaten')

print(f"Found {len(regions)} tables:")
for region in regions:
    print(f"  - {region.name}: rows {region.start_row}-{region.end_row}")
