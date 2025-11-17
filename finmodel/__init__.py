"""
Financial Model Styling Library for Jupyter/Quarto

Provides declarative styling for financial models with presets like 'assumptions'.
Reads Excel files, detects tables, and outputs styled HTML for Jupyter notebooks.
"""

from .reader import ExcelReader, read_basf_options, read_basf_returns, list_sheets, list_tables, print_tables, glimpse_table, finmodel_output
from .styles import StylePreset, FinancialTable
from .formatter import format_table
from .plotext_wrapper import PlotextChart, plotext_chart

__all__ = [
    'ExcelReader', 'StylePreset', 'FinancialTable', 'format_table',
    'read_basf_options', 'read_basf_returns', 'list_sheets', 'list_tables', 'print_tables', 'glimpse_table',
    'finmodel_output', 'PlotextChart', 'plotext_chart'
]
