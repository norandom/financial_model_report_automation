"""
Style presets for financial models.

Defines color schemes and formatting rules for different table types.
"""

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class CellStyle:
    """Style definition for a cell."""
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    font_weight: Optional[str] = None
    font_style: Optional[str] = None
    text_align: Optional[str] = None
    
    def to_css(self) -> str:
        """Convert to inline CSS string."""
        styles = []
        if self.background_color:
            styles.append(f"background-color: {self.background_color}")
        if self.text_color:
            styles.append(f"color: {self.text_color}")
        if self.font_weight:
            styles.append(f"font-weight: {self.font_weight}")
        if self.font_style:
            styles.append(f"font-style: {self.font_style}")
        if self.text_align:
            styles.append(f"text-align: {self.text_align}")
        return "; ".join(styles)


@dataclass
class TableStyle:
    """Style definition for a table type."""
    name: str
    header_style: CellStyle
    index_style: CellStyle
    data_style: CellStyle
    description: str = ""


class StylePreset:
    """Predefined style templates for financial models."""
    
    # Financial model color codes (grey scale for assumptions)
    ASSUMPTIONS = TableStyle(
        name="assumptions",
        header_style=CellStyle(
            background_color=None,  # No background
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color=None,  # No background for labels
            text_color="#000000",
            font_weight="bold",  # Labels are bold
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#D9D9D9",  # Light grey ONLY on value cells
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Grey background for assumption values (inputs/parameters)"
    )
    
    # Blue for calculations (common in financial models)
    CALCULATIONS = TableStyle(
        name="calculations",
        header_style=CellStyle(
            background_color="#8FAADC",  # Light blue
            text_color="#000000",  # Black text on light blue
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#D9E2F3",  # Light blue
            text_color="#000000",
            font_weight="normal",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Blue headers for calculated values"
    )
    
    # Standard/default style (light blue) - renamed from calculations
    STANDARD = TableStyle(
        name="standard",
        header_style=CellStyle(
            background_color="#8FAADC",  # Light blue
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#D9E2F3",  # Light blue
            text_color="#000000",
            font_weight="normal",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Standard blue headers (default style)"
    )
    
    # Keep CALCULATIONS as alias for backwards compatibility
    CALCULATIONS = STANDARD
    
    # Light orange for input data
    INPUT_DATA = TableStyle(
        name="input_data",
        header_style=CellStyle(
            background_color="#FFFFFF",  # White header
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#FDE9D9",  # Light orange
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Light orange for input data values"
    )
    
    # Light grey for calc_and_output
    CALC_AND_OUTPUT = TableStyle(
        name="calc_and_output",
        header_style=CellStyle(
            background_color="#FFFFFF",  # White header
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#F2F2F2",  # Light grey
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Light grey for calculations and output"
    )
    
    # Light green for formulas/references
    FORMULAS_OR_REFS = TableStyle(
        name="formulas_or_refs",
        header_style=CellStyle(
            background_color="#FFFFFF",  # White header
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#E2EFDA",  # Light green
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Light green for formulas or references"
    )
    
    # Light violet for plausibility checks
    PLAUSIBILITY = TableStyle(
        name="plausibility",
        header_style=CellStyle(
            background_color="#FFFFFF",  # White header
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#FFFFFF",  # White
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#E9D7F3",  # Light violet
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Light violet for plausibility checks"
    )
    
    # Yellow for results
    RESULTS = TableStyle(
        name="results",
        header_style=CellStyle(
            background_color="#FFC000",  # Orange/yellow
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        index_style=CellStyle(
            background_color="#FFF2CC",  # Light yellow
            text_color="#000000",
            font_weight="bold",
            text_align="left"
        ),
        data_style=CellStyle(
            background_color="#FFF2CC",  # Light yellow
            text_color="#000000",
            font_weight="normal",
            text_align="right"
        ),
        description="Yellow background for result values"
    )
    
    # Keep OUTPUTS as alias for backwards compatibility
    OUTPUTS = RESULTS
    
    @classmethod
    def get(cls, preset_name: str) -> TableStyle:
        """Get a style preset by name."""
        preset_map = {
            "assumptions": cls.ASSUMPTIONS,
            "standard": cls.STANDARD,
            "calculations": cls.CALCULATIONS,  # Alias for standard
            "input_data": cls.INPUT_DATA,
            "calc_and_output": cls.CALC_AND_OUTPUT,
            "formulas_or_refs": cls.FORMULAS_OR_REFS,
            "plausibility": cls.PLAUSIBILITY,
            "results": cls.RESULTS,
            "outputs": cls.OUTPUTS,  # Alias for results
        }
        
        if preset_name.lower() not in preset_map:
            raise ValueError(
                f"Unknown preset: {preset_name}. "
                f"Available: {', '.join(preset_map.keys())}"
            )
        
        return preset_map[preset_name.lower()]


class FinancialTable:
    """
    A styled financial table for Jupyter output.
    
    Usage:
        table = FinancialTable(df, style="assumptions")
        table.display()  # Shows in Jupyter
        
        # With assertions
        table = FinancialTable(
            df, 
            style="plausibility",
            assertions={
                'Valid': df['Expected'] == df['Actual'],
                'In Range': (df['Value'] >= 0) & (df['Value'] <= 100)
            }
        )
    """
    
    def __init__(self, data, style: str = "standard", assertions=None):
        """
        Initialize a financial table.

        Args:
            data: pandas DataFrame or dict
            style: Style preset name ("assumptions", "calculations", "outputs")
            assertions: Dict mapping assertion column names to boolean Series/conditions
                       Or a single boolean Series for a column named "Validation"

        Note: Use Quarto cell directives for captions and labels:
            #| label: tbl-name
            #| tbl-cap: "Caption text"
        """
        if isinstance(data, dict):
            self.df = pd.DataFrame(data)
        else:
            self.df = data.copy()
        
        self.style_preset = StylePreset.get(style)
        self.assertions = assertions
        
        # Add assertion columns if provided
        if assertions is not None:
            if isinstance(assertions, pd.Series):
                # Single assertion column
                self.df['Validation'] = assertions.map({True: 'Ok', False: 'No'})
            elif isinstance(assertions, dict):
                # Multiple assertion columns
                for col_name, condition in assertions.items():
                    self.df[col_name] = condition.map({True: 'Ok', False: 'No'})
            else:
                raise ValueError("assertions must be a pandas Series or dict of Series")
    
    def _repr_html_(self):
        """Return HTML representation for Jupyter."""
        from .formatter import format_table
        return format_table(self.df, self.style_preset, assertion_columns=self._get_assertion_columns())
    
    def _repr_latex_(self):
        """Return LaTeX representation with colors for PDF."""
        from .formatter import format_table_latex
        return format_table_latex(self.df, self.style_preset, assertion_columns=self._get_assertion_columns())
    
    def _get_assertion_columns(self):
        """Get list of assertion column names."""
        if self.assertions is None:
            return []
        elif isinstance(self.assertions, pd.Series):
            return ['Validation']
        else:
            return list(self.assertions.keys())
    
    def display(self):
        """Display the table in Jupyter (alias for IPython.display)."""
        from IPython.display import display, HTML
        display(HTML(self._repr_html_()))