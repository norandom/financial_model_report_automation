"""
HTML formatter for styled tables.

Converts DataFrames to HTML with inline CSS styles for Jupyter/Quarto.
Also provides LaTeX output with proper color commands for PDF.
"""

import pandas as pd
from .styles import TableStyle
from .config import Config


def format_table(df: pd.DataFrame, style: TableStyle, assertion_columns=None) -> str:
    """
    Format a DataFrame as HTML with inline styles.
    
    Args:
        df: pandas DataFrame
        style: TableStyle object with styling rules
        assertion_columns: List of column names that contain assertion results (Ok/No)
    
    Returns:
        HTML string with inline CSS
    """
    if df.empty:
        return "<p>Empty table</p>"
    
    if assertion_columns is None:
        assertion_columns = []
    
    # Start HTML
    html = [f'<table style="border-collapse: collapse; font-family: {Config.TABLE_FONT_FAMILY}; font-size: 10pt; margin: 1em 0;">']
    
    # Add header row
    html.append('  <thead>')
    html.append('    <tr>')
    
    # Index column header (if index has a name)
    if df.index.name:
        header_css = style.header_style.to_css()
        html.append(f'      <th style="{header_css}; padding: 8px; border: 1px solid #000;">{df.index.name}</th>')
    elif df.index.name is None:
        # Empty index column header
        header_css = style.header_style.to_css()
        html.append(f'      <th style="{header_css}; padding: 8px; border: 1px solid #000;"></th>')
    
    # Regular column headers
    header_css = style.header_style.to_css()
    for col in df.columns:
        html.append(f'      <th style="{header_css}; padding: 8px; border: 1px solid #000;">{col}</th>')
    
    html.append('    </tr>')
    html.append('  </thead>')
    
    # Add body rows
    html.append('  <tbody>')
    
    for idx, row in df.iterrows():
        html.append('    <tr>')
        
        # Index column (Column A)
        index_css = style.index_style.to_css()
        html.append(f'      <td style="{index_css}; padding: 8px; border: 1px solid #000;">{idx}</td>')
        
        # Data columns
        for col_name, value in row.items():
            # Check if this is an assertion column
            if col_name in assertion_columns:
                # Assertion columns get special styling
                if value == 'Ok':
                    cell_css = f"background-color: {Config.ASSERTION_OK_COLOR}; color: #000000; text-align: center; font-weight: bold"
                elif value == 'No':
                    cell_css = f"background-color: {Config.ASSERTION_NO_COLOR}; color: #000000; text-align: center; font-weight: bold"
                else:
                    cell_css = style.data_style.to_css()
                formatted = str(value) if value is not None else ""
            else:
                # Regular data column
                cell_css = style.data_style.to_css()
                # Format numbers nicely
                if isinstance(value, (int, float)):
                    if isinstance(value, float):
                        # Check if it's a percentage (small values)
                        if abs(value) < 1 and value != 0:
                            formatted = f"{value:.4f}"
                        else:
                            formatted = f"{value:,.2f}"
                    else:
                        formatted = f"{value:,}"
                else:
                    formatted = str(value) if value is not None else ""
            
            html.append(f'      <td style="{cell_css}; padding: 8px; border: 1px solid #000;">{formatted}</td>')
        
        html.append('    </tr>')
    
    html.append('  </tbody>')
    html.append('</table>')
    
    return '\n'.join(html)


def format_key_value_table(df: pd.DataFrame, style: TableStyle) -> str:
    """
    Format a key-value table (special case with index as labels).
    
    This is optimized for assumption-style tables where:
    - Column A (index) contains parameter names
    - Columns B+ contain values and units
    
    Args:
        df: pandas DataFrame with index as keys
        style: TableStyle object
    
    Returns:
        HTML string
    """
    if df.empty:
        return "<p>Empty table</p>"
    
    html = [f'<table style="border-collapse: collapse; font-family: {Config.TABLE_FONT_FAMILY}; font-size: 10pt; margin: 1em 0;">']
    
    # Header row (column names)
    if df.columns.notna().any():
        html.append('  <thead>')
        html.append('    <tr>')
        
        # First column header (empty for index)
        header_css = style.header_style.to_css()
        html.append(f'      <th style="{header_css}; padding: 8px; border: 1px solid #000;"></th>')
        
        for col in df.columns:
            col_name = str(col) if pd.notna(col) else ""
            html.append(f'      <th style="{header_css}; padding: 8px; border: 1px solid #000;">{col_name}</th>')
        
        html.append('    </tr>')
        html.append('  </thead>')
    
    # Body rows
    html.append('  <tbody>')
    
    for idx, row in df.iterrows():
        html.append('    <tr>')
        
        # Index cell (parameter name)
        index_css = style.index_style.to_css()
        html.append(f'      <td style="{index_css}; padding: 8px; border: 1px solid #000;">{idx}</td>')
        
        # Value cells
        data_css = style.data_style.to_css()
        for value in row:
            if isinstance(value, (int, float)):
                if isinstance(value, float):
                    if abs(value) < 1 and value != 0:
                        formatted = f"{value:.4f}"
                    else:
                        formatted = f"{value:,.2f}"
                else:
                    formatted = f"{value:,}"
            else:
                formatted = str(value) if pd.notna(value) else ""
            
            html.append(f'      <td style="{data_css}; padding: 8px; border: 1px solid #000;">{formatted}</td>')
        
        html.append('    </tr>')
    
    html.append('  </tbody>')
    html.append('</table>')
    
    return '\n'.join(html)


def format_table_latex(df, style, hide_index=False, assertion_columns=None):
    """Format DataFrame as LaTeX with aggressive space-saving.

    Args:
        df: DataFrame to format
        style: TableStyle object
        hide_index: If True, hide the index column (default: False)
        assertion_columns: List of column names that contain assertion results (Ok/No)
    """
    import pandas as pd
    import re

    if df.empty:
        return ""
    
    if assertion_columns is None:
        assertion_columns = []

    # Get background colors
    header_bg = (style.header_style.background_color or "").replace("#", "")
    index_bg = (style.index_style.background_color or "").replace("#", "")
    data_bg = (style.data_style.background_color or "").replace("#", "")
    
    # Assertion colors (strip #)
    ok_bg = Config.ASSERTION_OK_COLOR.replace("#", "")
    no_bg = Config.ASSERTION_NO_COLOR.replace("#", "")

    # Intelligent column type detection
    def detect_column_type(col_name, col_data):
        """Auto-detect column type."""
        col_name_lower = str(col_name).lower()
        
        # Check if this is an assertion column
        if col_name in assertion_columns:
            return 'assertion'

        # Check if numeric
        if pd.api.types.is_numeric_dtype(col_data):
            return 'numeric'

        # WKN/ISIN/Code detection
        if any(kw in col_name_lower for kw in Config.CODE_KEYWORDS):
            return 'code'

        # Text-heavy column detection
        if any(keyword in col_name_lower for keyword in Config.TEXT_HEAVY_KEYWORDS):
            return 'long_text'

        # Auto-detect by average text length
        avg_length = col_data.astype(str).str.len().mean()
        if avg_length > Config.LONG_TEXT_THRESHOLD:
            return 'long_text'
        elif avg_length > Config.MEDIUM_TEXT_THRESHOLD:
            return 'medium_text'
        else:
            return 'short_text'

    # Build intelligent column specifications
    col_specs = []

    # Add index column spec if not hidden
    if not hide_index:
        col_specs.append("l")  # Index column

    for col_name in df.columns:
        col_type = detect_column_type(col_name, df[col_name])

        if col_type == 'assertion':
            col_specs.append("c")  # Center-aligned for Ok/No
        elif col_type == 'numeric':
            col_specs.append("r")
        elif col_type == 'code':
            col_specs.append("p{1.5cm}")  # Small fixed width for WKN/ISIN
        elif col_type == 'long_text':
            col_specs.append("p{3.5cm}")  # Slightly smaller for produktname
        elif col_type == 'medium_text':
            col_specs.append("p{2.5cm}")
        else:
            col_specs.append("l")

    col_spec = "|" + "|".join(col_specs) + "|"

    # Use smaller font for wide tables
    use_small_font = len(df.columns) > 5 or any('p{' in spec for spec in col_specs)

    latex = []
    if use_small_font:
        latex.append("\\small")

    latex.append("\\begin{longtable}[]{" + col_spec + "}")
    latex.append("\\toprule")

    # Header row
    headers = []

    # Add index header if not hidden
    if not hide_index:
        index_name = str(df.index.name).replace("_", "\\_").replace("%", "\\%").replace("&", "\\&") if df.index.name else ""
        headers.append(index_name)

    # Add data column headers (with LaTeX escaping)
    headers.extend([str(c).replace("_", "\\_").replace("%", "\\%").replace("&", "\\&") for c in df.columns])

    if header_bg:
        latex.append("\\rowcolor[HTML]{" + header_bg + "}")
    latex.append("\\textbf{" + "} & \\textbf{".join(headers) + "} \\\\")
    latex.append("\\midrule")
    latex.append("\\endhead")
    
    # Data rows
    for idx, row in df.iterrows():
        cells = []

        # Add index cell if not hidden
        if not hide_index:
            index_val = str(idx) if pd.notna(idx) else ""
            # Escape special LaTeX characters
            index_val = index_val.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")
            if index_bg:
                cells.append("\\cellcolor[HTML]{" + index_bg + "}" + index_val)
            else:
                cells.append(index_val)

        # Data cells - apply intelligent formatting based on column type
        for i, val in enumerate(row):
            col_name = df.columns[i]
            col_type = detect_column_type(col_name, df.iloc[:, i])
            
            # Handle assertion columns
            if col_type == 'assertion':
                formatted = str(val) if pd.notna(val) else ""
                if val == 'Ok':
                    cells.append("\\cellcolor[HTML]{" + ok_bg + "}\\textbf{" + formatted + "}")
                elif val == 'No':
                    cells.append("\\cellcolor[HTML]{" + no_bg + "}\\textbf{" + formatted + "}")
                else:
                    if data_bg:
                        cells.append("\\cellcolor[HTML]{" + data_bg + "}" + formatted)
                    else:
                        cells.append(formatted)
                continue

            if isinstance(val, (int, float)):
                if isinstance(val, float) and abs(val) < 1 and val != 0:
                    formatted = f"{val:.4f}"
                elif isinstance(val, float):
                    formatted = f"{val:,.2f}"
                else:
                    formatted = f"{val:,}"
            else:
                formatted = str(val) if pd.notna(val) else ""
                # Escape special LaTeX characters
                formatted = formatted.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")

                # Apply small font to WKN/ISIN codes
                if col_type == 'code' and formatted:
                    formatted = "{\\small " + formatted + "}"

                # Apply tiny font + line breaks to long produktname text
                elif col_type == 'long_text' and len(formatted) > 20:
                    # Insert line break at spaces for long product names
                    words = formatted.split()
                    if len(words) > 1:
                        mid = len(words) // 2
                        formatted = ' '.join(words[:mid]) + " " + ' '.join(words[mid:])
                    formatted = "{\\tiny " + formatted + "}"

            if data_bg:
                cells.append("\\cellcolor[HTML]{" + data_bg + "}" + formatted)
            else:
                cells.append(formatted)

        latex.append(" & ".join(cells) + " \\\\")

    latex.append("\\bottomrule")
    latex.append("\\end{longtable}")

    return "\n".join(latex)