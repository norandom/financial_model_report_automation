"""
Global configuration for finmodel.
"""

class Config:
    """Global configuration settings."""
    
    # Fonts
    # User preference: Palatino for text, Inconsolata for tables, Fira Code for code
    TEXT_FONT_FAMILY = "Palatino, 'Palatino Linotype', 'Book Antiqua', serif"
    TABLE_FONT_FAMILY = "Inconsolata, monospace"
    CODE_FONT_FAMILY = "'Fira Code', 'Fira Mono', monospace"
    
    # Assertion colors
    ASSERTION_OK_COLOR = "#C6E0B4" # Light green
    ASSERTION_NO_COLOR = "#F4B084" # Light orange
    
    # Text detection thresholds
    LONG_TEXT_THRESHOLD = 30
    MEDIUM_TEXT_THRESHOLD = 15

    # Keywords for column type detection (English and German support)
    TEXT_HEAVY_KEYWORDS = {
        'name', 'description', 'title', 'label', 'comment', 'note',
        'produktname', 'beschreibung', 'bezeichnung', 'produkt', 'titel',
        'detail', 'summary', 'explanation'
    }
    
    CODE_KEYWORDS = {
        'wkn', 'isin', 'symbol', 'ticker', 'code', 'id', 'cusip'
    }
