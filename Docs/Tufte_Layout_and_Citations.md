# Tufte-Style Layout and Citations in Quarto

Complete guide to using margin notes, full-width content, and citation management in your Quarto notebooks.

## Table of Contents

1. [Tufte Layout Overview](#tufte-layout-overview)
2. [YAML Configuration](#yaml-configuration)
3. [Margin Content](#margin-content)
4. [Column Layout Options](#column-layout-options)
5. [Citation Management](#citation-management)
6. [Complete Examples](#complete-examples)

---

## Tufte Layout Overview

The Tufte style, named after Edward Tufte, emphasizes:
- **Wide margins** for annotations and notes
- **Sidenotes** instead of footnotes
- **Margin figures** for supporting visuals
- **Full-width content** when needed for complex material
- **Clean reading experience** with minimal interruptions

Benefits:
- Explanatory notes don't interrupt main text flow
- Readers can glance at annotations without losing place
- Complex code/tables can use full page width when needed
- Better use of page real estate

---

## YAML Configuration

### Basic Tufte Setup

Add to your notebook's YAML frontmatter:

```yaml
---
title: "Your Document Title"
format:
  pdf:
    # Tufte-style margin settings
    reference-location: margin
    citation-location: margin

    # Standard document settings
    documentclass: scrreprt
    classoption:
      - DIV=11
      - headings=small
      - parskip=half
---
```

### With Citations Enabled

```yaml
---
title: "Your Document Title"
bibliography: references.bib
format:
  pdf:
    reference-location: margin
    citation-location: margin
    documentclass: scrreprt
---
```

### Configuration Options

| Setting | Values | Effect |
|---------|--------|--------|
| `reference-location` | `margin`, `document`, `section`, `block` | Where footnotes appear |
| `citation-location` | `margin`, `document` | Where citations appear |

**Recommended for Tufte style:**
- `reference-location: margin` - Footnotes in margin
- `citation-location: margin` - Citations in margin

---

## Margin Content

### Inline Margin Notes

**Syntax:**
```markdown
This is main text. [This is a margin note]{.aside}
```

**Output:**
- Main text flows normally
- Note appears in margin alongside text
- No footnote number or mark

**Example:**
```markdown
The Black-Scholes model assumes constant volatility.
[BS assumes lognormal returns]{.aside}
```

### Block Margin Content

**Syntax:**
```markdown
::: {.column-margin}
Your margin content here.

Can include multiple paragraphs.

**Bold text**, *italics*, and even lists.
:::
```

**Use for:**
- Longer explanations
- Multiple paragraphs
- Formatted content
- Small figures or tables

**Example:**
```markdown
The Greeks measure option sensitivities.

::: {.column-margin}
**Common Greeks:**
- Delta (Δ): Price sensitivity
- Gamma (Γ): Delta sensitivity
- Theta (Θ): Time decay
- Vega (ν): Volatility sensitivity
:::
```

### Margin Links

**Syntax:**
```markdown
::: {.column-margin}
[Link text](https://example.com)
:::
```

**Example:**
```markdown
## Introduction

::: {.column-margin}
[Course Portal](https://eiqf.de/kursinhalte-mba/)
:::

Main content starts here.
```

---

## Column Layout Options

### For Markdown Content

**Wrap content in div with column class:**

```markdown
::: {.column-body}
Regular width content (default)
:::

::: {.column-page}
Full-width content (body + margin)
:::

::: {.column-margin}
Margin-only content
:::
```

### For Code Cells

**Add directive at top of cell:**

```python
#| column: body
# Regular width (default) - margin available for notes
import pandas as pd
```

```python
#| column: page
# Full width - uses body + margin space
very_long_line = some_function(param1, param2, param3, param4, param5)
```

```python
#| column: margin
# Output only in margin
print("Small result")
```

### Column Width Reference

| Directive | Width | Margin Available | Use Case |
|-----------|-------|------------------|----------|
| `column: body` | ~65% page | ✓ Yes | Default - short code, text |
| `column: page` | ~100% page | ✗ No | Long lines, wide tables |
| `column: margin` | Margin only | N/A | Small outputs, notes |

### When to Use Each

**Use `column: body` (default):**
- Short imports and assignments
- Regular text paragraphs
- Code that fits in ~80 characters
- When you want margin available for notes

**Use `column: page`:**
- Long function calls (QuantLib, complex APIs)
- Wide pandas DataFrames
- Complex nested expressions
- plotext charts needing horizontal space
- Any line > 80 characters

**Use `column: margin`:**
- Small outputs or summaries
- Quick reference information
- Supplementary data

---

## Citation Management

### Setting Up Citations

**1. Create Bibliography File (`references.bib`):**

```bibtex
@book{hull2018options,
  title={Options, Futures, and Other Derivatives},
  author={Hull, John C},
  edition={10},
  year={2018},
  publisher={Pearson}
}

@article{black1973pricing,
  title={The Pricing of Options and Corporate Liabilities},
  author={Black, Fischer and Scholes, Myron},
  journal={Journal of Political Economy},
  volume={81},
  number={3},
  pages={637--654},
  year={1973}
}

@article{hagan2002managing,
  title={Managing smile risk},
  author={Hagan, Patrick S and Kumar, Deep and Lesniewski, Andrew S and Woodward, Diana E},
  journal={Wilmott Magazine},
  pages={84--108},
  year={2002}
}
```

**2. Reference in YAML:**

```yaml
---
bibliography: references.bib
citation-location: margin
---
```

### Citation Syntax

| Syntax | Output | Use Case |
|--------|--------|----------|
| `[@black1973pricing]` | (Black and Scholes 1973) | Parenthetical citation |
| `@black1973pricing` | Black and Scholes (1973) | In-text citation |
| `[-@black1973pricing]` | (1973) | Suppress author |
| `[@black1973pricing, p. 42]` | (Black and Scholes 1973, 42) | With page number |
| `[@black1973pricing; @hagan2002managing]` | (Black and Scholes 1973; Hagan et al. 2002) | Multiple citations |

### Citation Behavior with Margins

**What happens:**
1. **In main text:** Brief reference appears (author, year)
2. **In margin:** Same citation appears as sidenote
3. **At document end:** Full bibliography with complete details

**Example:**

**Your markdown:**
```markdown
The Black-Scholes model [@black1973pricing] assumes constant volatility,
but the SABR model [@hagan2002managing] addresses the volatility smile.
```

**Rendered output:**

**Main text:**
> The Black-Scholes model assumes constant volatility, but the SABR model addresses the volatility smile.

**Margin:**
> (Black and Scholes 1973)
> (Hagan et al. 2002)

**Bibliography section (end of document):**
> **References**
>
> Black, Fischer, and Myron Scholes. 1973. "The Pricing of Options and Corporate Liabilities." *Journal of Political Economy* 81 (3): 637–654.
>
> Hagan, Patrick S., Deep Kumar, Andrew S. Lesniewski, and Diana E. Woodward. 2002. "Managing Smile Risk." *Wilmott Magazine*, 84–108.

### Citation Styles

Quarto supports thousands of citation styles via CSL (Citation Style Language):

```yaml
---
bibliography: references.bib
csl: https://www.zotero.org/styles/apa  # APA style
---
```

**Popular styles:**
- `apa` - American Psychological Association
- `chicago-author-date` - Chicago Manual of Style
- `ieee` - IEEE
- `nature` - Nature journal
- `vancouver` - Vancouver system

**Or use local file:**
```yaml
csl: chicago-author-date.csl
```

---

## Complete Examples

### Example 1: Technical Section with Margin Notes

```markdown
## Black-Scholes Option Pricing

The Black-Scholes model provides an analytical solution for European options.
[Analytical = closed-form formula, no iteration needed]{.aside}

The model makes several key assumptions [@black1973pricing]:

- Constant volatility σ
- Lognormal stock price distribution
- No transaction costs
- Continuous trading

::: {.column-margin}
**Model Limitations:**
These assumptions often fail in real markets, leading to pricing errors.
:::
```

### Example 2: Code Cell with Full Width

**In Jupyter code cell:**

```python
#| label: quantlib-setup
#| column: page

# Full-width code for long QuantLib setup
import QuantLib as ql

# Create option objects with full parameter specification
call_option = ql.EuropeanOption(
    ql.PlainVanillaPayoff(ql.Option.Call, strike_price),
    ql.EuropeanExercise(maturity_date)
)

# Build Black-Scholes-Merton process with all market data handles
bsm_process = ql.BlackScholesMertonProcess(
    spot_price_handle,
    dividend_yield_handle,
    risk_free_rate_handle,
    volatility_handle
)
```

### Example 3: Mixed Regular and Full-Width

```markdown
## Assignment 9: Greeks Calculation

We calculate option sensitivities using QuantLib's analytical engine.
[Greeks measure how option prices change with market conditions]{.aside}
```

**Regular width code (margin available):**
```python
# Import libraries
import QuantLib as ql
import numpy as np

# Set parameters
S0 = 50.0
K = 48.0
```

**Full width code (needs space):**
```python
#| column: page

# Complex Greeks calculation
delta_call = call_option.delta()
gamma_call = call_option.gamma()
theta_call = call_option.theta()
vega_call = call_option.vega()
rho_call = call_option.rho()

# Create results DataFrame
results = pd.DataFrame({
    'Greek': ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
    'Call': [delta_call, gamma_call, theta_call, vega_call, rho_call],
    'Put': [delta_put, gamma_put, theta_put, vega_put, rho_put]
})
```

### Example 4: Margin Figure with Citation

```markdown
## Volatility Smile Analysis

The SABR model [@hagan2002managing] captures the volatility smile phenomenon.

::: {.column-margin}
![Volatility Smile](images/sabr_smile.png)

*Figure: Implied volatility varies with strike price, creating a "smile" shape.*
:::

Our analysis shows significant deviation from Black-Scholes assumptions.
```

### Example 5: Combining Everything

```markdown
## Assignment 10: Black-Scholes Critique

The Black-Scholes model has several known limitations [@hull2018options, ch. 19].

### Critique 1: Constant Volatility

::: {.column-margin}
**Historical Evidence:**
Market volatility is stochastic, not constant [@heston1993closed].
:::

The BS model assumes σ is constant over the option's life.
[In reality, volatility clusters and mean-reverts]{.aside}

We demonstrate this with SABR model comparison [@hagan2002managing]:
```

**Full-width code:**
```python
#| column: page
#| label: sabr-comparison

# SABR model setup with stochastic volatility
from pysabr import Hagan2002LognormalSABR

sabr = Hagan2002LognormalSABR(
    f=spot_price,
    shift=0,
    t=time_to_maturity,
    v_atm_n=atm_volatility,
    beta=0.7,
    rho=-0.3,
    volvol=0.4
)
```

```markdown
Results show the volatility smile that BS cannot explain.
```

---

## Quick Reference

### Essential Syntax

```markdown
# Margin note
[Note text]{.aside}

# Margin block
::: {.column-margin}
Content here
:::

# Full-width code cell
#| column: page

# Citation
[@citation_key]

# Multiple citations
[@key1; @key2]
```

### YAML Checklist

```yaml
---
title: "Your Title"
bibliography: references.bib  # If using citations
format:
  pdf:
    reference-location: margin  # Footnotes in margin
    citation-location: margin   # Citations in margin
---
```

### Decision Tree: Which Column Width?

```
Is this code/content?
├─ Short code/text (< 80 chars)
│  └─ Use default (column: body) - margin available
├─ Long lines or wide tables
│  └─ Use column: page - full width
└─ Supplementary info
   └─ Use column: margin - margin only
```

---

## Tips and Best Practices

### Margin Notes

✅ **Do:**
- Keep margin notes brief (1-3 sentences)
- Use for definitions, context, cross-references
- Explain terminology or abbreviations
- Add quick clarifications

❌ **Don't:**
- Write long paragraphs in margins
- Duplicate main text content
- Overuse - becomes cluttered

### Full-Width Content

✅ **Do:**
- Use for QuantLib code (long function names)
- Use for wide DataFrames/tables
- Use for complex nested expressions
- Add `#| column: page` proactively for readability

❌ **Don't:**
- Use full-width for short, simple code
- Use when margin notes are more important
- Mix full-width and margin content on same section

### Citations

✅ **Do:**
- Cite primary sources for models/methods
- Use consistent citation style
- Include page numbers for specific claims
- Maintain complete `.bib` file

❌ **Don't:**
- Over-cite common knowledge
- Mix citation styles manually
- Forget to add new sources to `.bib`

---

## Troubleshooting

### Margin Note Not Appearing

**Problem:** `[Text](link){.aside}` doesn't go to margin

**Solution:** Wrap in additional element:
```markdown
::: {.column-margin}
[Text](link)
:::
```

### Code Cell Too Wide

**Problem:** Code wraps badly or overflows

**Solution:** Add full-width directive:
```python
#| column: page

# Long code here
```

### Citations Not In Margin

**Problem:** Citations appear as footnotes at page bottom

**Solution:** Check YAML has:
```yaml
citation-location: margin
```

### Bibliography Not Appearing

**Problem:** No references section at end

**Solution:** Ensure:
1. `bibliography: references.bib` in YAML
2. `.bib` file exists and has entries
3. At least one citation `[@key]` in document

---

## Resources

### Official Documentation

- [Quarto Page Layout](https://quarto.org/docs/authoring/article-layout.html)
- [Quarto Citations](https://quarto.org/docs/authoring/footnotes-and-citations.html)
- [CSL Citation Styles](https://citationstyles.org/)

### Bibliography Management

- [Zotero](https://www.zotero.org/) - Free reference manager
- [JabRef](https://www.jabref.org/) - BibTeX editor
- [Google Scholar](https://scholar.google.com/) - BibTeX export from "Cite"

### Example Files

In this project:
- `Modul_8_Derivate.ipynb` - Full example with Tufte layout
- `buildfiles/README_FONTS.md` - Font configuration
- `Docs/` - Additional documentation

---

## Summary

**Tufte Layout = Better Academic Documents**

1. **YAML:** Add `reference-location: margin` and `citation-location: margin`
2. **Margin Notes:** Use `[text]{.aside}` or `::: {.column-margin}`
3. **Full Width:** Add `#| column: page` to code cells with long lines
4. **Citations:** Create `.bib` file, add `bibliography:` to YAML, cite with `[@key]`

**Result:**
- Clean main text flow
- Helpful annotations in margins
- Full width when needed
- Professional academic presentation
- Automatic citation management

---

*Last updated: 2025-01-17*
