"""
PlotextChart wrapper for dual Jupyter/PDF rendering.

Provides automatic ANSI → HTML (Jupyter) and ANSI → LaTeX (PDF) conversion
for plotext terminal charts, maintaining Berkeley Mono font styling.
"""

from typing import Literal, Optional
from ansi2html import Ansi2HTMLConverter


# Font size mappings for LaTeX
LATEX_FONT_SIZES = {
    'tiny': r'\tiny',
    'small': r'\small',
    'medium': r'\normalsize',
    'large': r'\large',
}


class PlotextChart:
    """
    Wrapper for plotext ANSI output with Jupyter + PDF support.

    Usage in notebook cell (mark with #:: ANSI):
        import plotext as plt
        from finmodel import PlotextChart

        plt.scatter(data)
        ansi_output = plt.build()
        PlotextChart(ansi_output, size='medium')

    Or with font size marker in cell:
        #:: ANSI small
        PlotextChart(ansi_output, size='small')
    """

    def __init__(
        self,
        ansi_output: str,
        size: Literal['tiny', 'small', 'medium', 'large'] = 'medium'
    ):
        """
        Initialize PlotextChart with ANSI terminal output.

        Args:
            ansi_output: Raw ANSI escape sequence string from plotext
            size: Font size for LaTeX output (tiny/small/medium/large)
        """
        self.ansi_output = ansi_output
        self.size = size
        self.html_converter = Ansi2HTMLConverter(inline=True, scheme='ansi2html')

    def _repr_html_(self) -> str:
        """
        Jupyter HTML representation.

        Returns:
            HTML string with inline CSS for ANSI colors
        """
        return self.to_html()

    def to_html(self) -> str:
        """
        Export as standalone HTML.

        Returns:
            HTML string with inline CSS for ANSI colors
        """
        # Convert ANSI to HTML with inline styles
        html_output = self.html_converter.convert(self.ansi_output, full=False)

        # Wrap in pre with Berkeley Mono font (preserves plotext theme colors)
        return f'''<pre style="
            font-family: 'Berkeley Mono', 'Courier New', monospace;
            padding: 1em;
            overflow-x: auto;
            line-height: 1.2;
        ">{html_output}</pre>'''

    def _repr_latex_(self) -> str:
        """
        LaTeX representation for PDF output.

        Returns:
            LaTeX verbatim environment with ANSI colors converted to xcolor
        """
        # Convert ANSI to LaTeX
        latex_output = self._ansi_to_latex(self.ansi_output)

        # Get font size command
        font_size = LATEX_FONT_SIZES.get(self.size, r'\normalsize')

        # Wrap in Verbatim environment with Berkeley Mono font
        # Using raw strings and concatenation to avoid f-string escaping issues
        result = r'\begin{Verbatim}[commandchars=\\\{\}]' + '\n'
        result += font_size + '\n'
        result += r'\fontfamily{Berkeley Mono}\selectfont' + '\n'
        result += latex_output + '\n'
        result += r'\end{Verbatim}'
        return result

    def _ansi_to_latex(self, text: str) -> str:
        """
        Convert ANSI escape sequences to LaTeX xcolor commands.

        Args:
            text: ANSI formatted text

        Returns:
            LaTeX formatted text with textcolor commands
        """
        import re

        # ANSI color code to LaTeX xcolor mapping
        ANSI_TO_LATEX = {
            '30': 'black', '31': 'red', '32': 'green', '33': 'yellow',
            '34': 'blue', '35': 'magenta', '36': 'cyan', '37': 'white',
            '90': 'darkgray', '91': 'red!80!white', '92': 'green!80!white',
            '93': 'yellow!80!white', '94': 'blue!80!white',
            '95': 'magenta!80!white', '96': 'cyan!80!white', '97': 'lightgray',
            # Bold variants (1;3x)
            '1;30': 'black', '1;31': 'red', '1;32': 'green', '1;33': 'yellow',
            '1;34': 'blue', '1;35': 'magenta', '1;36': 'cyan', '1;37': 'white',
        }

        # 256-color palette mapping (common colors used by plotext themes)
        # Format: 38;5;XXX or 48;5;XXX (foreground/background)
        COLOR_256_TO_LATEX = {
            '0': 'black', '1': 'red', '2': 'green', '3': 'yellow',
            '4': 'blue', '5': 'magenta', '6': 'cyan', '7': 'white',
            '8': 'darkgray', '9': 'red!80', '10': 'green!80', '11': 'yellow!80',
            '12': 'blue!80', '13': 'magenta!80', '14': 'cyan!80', '15': 'lightgray',
            # Extended colors (approximate xcolor equivalents)
            '16': 'black', '17': 'blue!20!black', '18': 'blue!40!black',
            '19': 'blue!60!black', '20': 'blue!80!black', '21': 'blue',
            '196': 'red', '226': 'yellow', '46': 'green', '51': 'cyan',
            '201': 'magenta', '208': 'orange', '220': 'yellow!80',
        }

        # Parse ANSI codes FIRST (before escaping LaTeX characters)
        # Split by ANSI escape sequences: \033[XXm or \x1b[XXm
        result = []
        current_color = None
        parts = re.split(r'\x1b\[([0-9;]+)m', text)

        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text content
                if part:
                    # Escape LaTeX special characters in the text content
                    escaped = part
                    escaped = escaped.replace('\\', r'\textbackslash{}')
                    escaped = escaped.replace('{', r'\{')
                    escaped = escaped.replace('}', r'\}')
                    escaped = escaped.replace('_', r'\_')
                    escaped = escaped.replace('^', r'\textasciicircum{}')
                    escaped = escaped.replace('~', r'\textasciitilde{}')
                    escaped = escaped.replace('#', r'\#')
                    escaped = escaped.replace('$', r'\$')
                    escaped = escaped.replace('%', r'\%')
                    escaped = escaped.replace('&', r'\&')

                    if current_color:
                        result.append(f'\\textcolor{{{current_color}}}{{{escaped}}}')
                    else:
                        result.append(escaped)
            else:  # ANSI code
                if part == '0' or part == '':  # Reset
                    current_color = None
                # Check for 256-color format: 38;5;XXX (foreground) or 48;5;XXX (background)
                elif part.startswith('38;5;'):
                    color_num = part.split(';')[2]
                    current_color = COLOR_256_TO_LATEX.get(color_num, f'black!{int(color_num)*100//255}!white')
                elif part.startswith('48;5;'):
                    # Background color - skip for now (could add background support later)
                    pass
                elif part in ANSI_TO_LATEX:
                    current_color = ANSI_TO_LATEX[part]
                # Ignore unrecognized codes

        return ''.join(result)


def plotext_chart(
    ansi_output: str,
    size: Literal['tiny', 'small', 'medium', 'large'] = 'medium'
) -> PlotextChart:
    """
    Convenience function to create PlotextChart.

    Args:
        ansi_output: Raw ANSI output from plotext.build()
        size: Font size (tiny/small/medium/large)

    Returns:
        PlotextChart instance for display

    Example (Jupyter):
        import plotext as plt
        from finmodel import plotext_chart

        plt.scatter(data)
        plotext_chart(plt.build(), size='small')

    Example (HTML export):
        import plotext as plt
        from finmodel import plotext_chart

        plt.scatter(data)
        chart = plotext_chart(plt.build())
        html_output = chart.to_html()
        # Save or serve html_output
    """
    return PlotextChart(ansi_output, size=size)
