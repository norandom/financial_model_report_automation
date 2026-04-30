# Tufte-style layout and citations in Quarto

How to use margin notes, full-width content, and citations in your Quarto notebooks.

## Table of contents

1. [Tufte layout overview](#tufte-layout-overview)
2. [YAML configuration](#yaml-configuration)
3. [Margin content](#margin-content)
4. [Column layout options](#column-layout-options)
5. [Citation management](#citation-management)
6. [Examples](#examples)

---

## Tufte layout overview

The Tufte style, named after Edward Tufte, puts annotations in wide margins instead of in footnotes. Notes sit next to the text they refer to, so readers don't lose their place. Code and tables can expand to full page width when they need the room.

---

## YAML configuration

### Basic Tufte setup

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

### With citations enabled

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

### Configuration options

| Setting | Values | Effect |
|---------|--------|--------|
| `reference-location` | `margin`, `document`, `section`, `block` | Where footnotes appear |
| `citation-location` | `margin`, `document` | Where citations appear |

For Tufte style, set both to `margin`.

---

## Margin content

### Inline margin notes

Syntax:
```markdown
This is main text. [This is a margin note]{.aside}
```

The main text flows normally. The note appears in the margin alongside it, without a footnote number.

Example:
```markdown
The Black-Scholes model assumes constant volatility.
[BS assumes lognormal returns]{.aside}
```

### Block margin content

Syntax:
```markdown
::: {.column-margin}
Your margin content here.

Can include multiple paragraphs.

**Bold text**, *italics*, and even lists.
:::
```

Use this for longer explanations, formatted content, or small figures.

Example:
```markdown
The Greeks measure option sensitivities.

::: {.column-margin}
**Common Greeks:**
- Delta: Price sensitivity
- Gamma: Delta sensitivity
- Theta: Time decay
- Vega: Volatility sensitivity
:::
```

### Margin links

```markdown
::: {.column-margin}
[Link text](https://example.com)
:::
```

Example:
```markdown
## Introduction

::: {.column-margin}
[Course Portal](https://eiqf.de/kursinhalte-mba/)
:::

Main content starts here.
```

---

## Column layout options

### For markdown content

Wrap content in a div with a column class:

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

### For code cells

Add a directive at the top of the cell:

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

### Column width reference

| Directive | Width | Margin available | When to use |
|-----------|-------|------------------|-------------|
| `column: body` | ~65% page | Yes | Default -- short code, text |
| `column: page` | ~100% page | No | Long lines, wide tables |
| `column: margin` | Margin only | N/A | Small outputs, notes |

### When to use each

`column: body` (default) -- short imports, assignments, code under ~80 characters, anything where you want the margin free for notes.

`column: page` -- long function calls (QuantLib, complex APIs), wide DataFrames, nested expressions, plotext charts, any line over 80 characters.

`column: margin` -- small outputs, quick reference info, supplementary data.

---

## Citation management

### Setting up citations

1. Create a bibliography file (`references.bib`):

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

2. Reference it in YAML:

```yaml
---
bibliography: references.bib
citation-location: margin
---
```

### Citation syntax

| Syntax | Output | When to use |
|--------|--------|-------------|
| `[@black1973pricing]` | (Black and Scholes 1973) | Parenthetical citation |
| `@black1973pricing` | Black and Scholes (1973) | In-text citation |
| `[-@black1973pricing]` | (1973) | Suppress author |
| `[@black1973pricing, p. 42]` | (Black and Scholes 1973, 42) | With page number |
| `[@black1973pricing; @hagan2002managing]` | (Black and Scholes 1973; Hagan et al. 2002) | Multiple citations |

### How margin citations render

With `citation-location: margin`, a brief reference (author, year) appears in the main text and the same citation shows as a sidenote. A full bibliography appears at the end of the document.

Example markdown:
```markdown
The Black-Scholes model [@black1973pricing] assumes constant volatility,
but the SABR model [@hagan2002managing] addresses the volatility smile.
```

Main text renders inline references. The margin shows:
> (Black and Scholes 1973)
> (Hagan et al. 2002)

The bibliography at the end contains full details.

### Citation styles

Quarto supports CSL (Citation Style Language) styles:

```yaml
---
bibliography: references.bib
csl: https://www.zotero.org/styles/apa  # APA style
---
```

Some common styles: `apa`, `chicago-author-date`, `ieee`, `nature`, `vancouver`.

You can also point to a local file:
```yaml
csl: chicago-author-date.csl
```

---

## Examples

### Example 1: Technical section with margin notes

```markdown
## Black-Scholes option pricing

The Black-Scholes model provides an analytical solution for European options.
[Analytical = closed-form formula, no iteration needed]{.aside}

The model makes several key assumptions [@black1973pricing]:

- Constant volatility
- Lognormal stock price distribution
- No transaction costs
- Continuous trading

::: {.column-margin}
**Model limitations:**
These assumptions often fail in real markets, leading to pricing errors.
:::
```

### Example 2: Code cell with full width

In a Jupyter code cell:

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

### Example 3: Mixed regular and full-width

```markdown
## Assignment 9: Greeks calculation

We calculate option sensitivities using QuantLib's analytical engine.
[Greeks measure how option prices change with market conditions]{.aside}
```

Regular width code (margin available):
```python
# Import libraries
import QuantLib as ql
import numpy as np

# Set parameters
S0 = 50.0
K = 48.0
```

Full width code (needs space):
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

### Example 4: Margin figure with citation

```markdown
## Volatility smile analysis

The SABR model [@hagan2002managing] captures the volatility smile phenomenon.

::: {.column-margin}
![Volatility Smile](images/sabr_smile.png)

*Figure: Implied volatility varies with strike price, creating a "smile" shape.*
:::

Our analysis shows significant deviation from Black-Scholes assumptions.
```

### Example 5: Combining everything

```markdown
## Assignment 10: Black-Scholes critique

The Black-Scholes model has several known limitations [@hull2018options, ch. 19].

### Critique 1: Constant volatility

::: {.column-margin}
**Historical evidence:**
Market volatility is stochastic, not constant [@heston1993closed].
:::

The BS model assumes sigma is constant over the option's life.
[In reality, volatility clusters and mean-reverts]{.aside}

We demonstrate this with SABR model comparison [@hagan2002managing]:
```

Full-width code:
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

## Quick reference

### Syntax

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

### YAML checklist

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

### Which column width?

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

## Tips

### Margin notes

Do:
- Keep margin notes brief (1-3 sentences)
- Use for definitions, context, cross-references
- Explain terminology or abbreviations

Avoid:
- Long paragraphs in margins
- Duplicating main text content
- Overusing them -- the margin gets cluttered fast

### Full-width content

Do:
- Use for QuantLib code (long function names)
- Use for wide DataFrames/tables
- Use for complex nested expressions

Avoid:
- Using full-width for short, simple code
- Using it when margin notes are more important nearby

### Citations

Do:
- Cite primary sources for models and methods
- Use consistent citation style
- Include page numbers for specific claims

Avoid:
- Over-citing common knowledge
- Mixing citation styles manually
- Forgetting to add new sources to `.bib`

---

## Troubleshooting

### Margin note not appearing

If `[Text](link){.aside}` doesn't go to the margin, wrap it instead:
```markdown
::: {.column-margin}
[Text](link)
:::
```

### Code cell too wide

If code wraps badly or overflows, add the full-width directive:
```python
#| column: page

# Long code here
```

### Citations not in margin

Check that your YAML has:
```yaml
citation-location: margin
```

### Bibliography not appearing

Make sure:
1. `bibliography: references.bib` is in your YAML
2. The `.bib` file exists and has entries
3. At least one citation `[@key]` appears in the document

---

## Resources

### Official documentation

- [Quarto Page Layout](https://quarto.org/docs/authoring/article-layout.html)
- [Quarto Citations](https://quarto.org/docs/authoring/footnotes-and-citations.html)
- [CSL Citation Styles](https://citationstyles.org/)

### Bibliography management

- [Zotero](https://www.zotero.org/) -- free reference manager
- [JabRef](https://www.jabref.org/) -- BibTeX editor
- [Google Scholar](https://scholar.google.com/) -- BibTeX export from "Cite"

### Example files

In this project:
- `Modul_8_Derivate.ipynb` -- full example with Tufte layout
- `buildfiles/README_FONTS.md` -- font configuration
- `Docs/` -- additional documentation

---

## Summary

1. Add `reference-location: margin` and `citation-location: margin` to your YAML
2. Use `[text]{.aside}` or `::: {.column-margin}` for margin notes
3. Add `#| column: page` to code cells with long lines
4. Create a `.bib` file, add `bibliography:` to YAML, cite with `[@key]`

---

*Last updated: 2025-01-17*
