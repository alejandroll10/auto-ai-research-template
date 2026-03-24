# Empirical Extension — Stage 3b

## Overview

This extension adds data-driven empirical analysis to the theory pipeline. It runs after Stage 3 (implications) and before Stage 4 (self-attack). A single agent decides what empirical work the theory needs and executes it.

## Prerequisites

- Python 3 with pandas, numpy, statsmodels, scipy
- For FRED data: API key in `.env` as `FRED_API_KEY=your-key` (free from https://fred.stlouisfed.org/docs/api/api_key.html)
- Ken French and Chen-Zimmerman data require no authentication

Install dependencies:
```bash
pip install pandas numpy statsmodels scipy fredapi pandas-datareader python-dotenv
```

## Stage 3b: Empirical Analysis

**Agent:** `empiricist`

1. Read the theory draft, implications, and problem statement
2. Launch empiricist agent
3. Empiricist reads the theory, decides what empirical work is appropriate (calibration, tests, portfolio sorts, descriptive stats, or a combination), fetches data via skills, and executes it
4. Save results to `output/stage3b/empirical_analysis.md`
5. Save code to `code/empirical.py`
6. Commit: `artifact: empirical analysis — [brief description]`

## Integration with pipeline

After Stage 3b completes:
- Self-attacker (Stage 4) receives empirical results alongside the theory
- Scorer evaluates empirical grounding as part of Fertility dimension
- Paper-writer includes empirical evidence sections

## Data skills

Skills are installed to `.claude/skills/` and injected into agent context via the `skills:` frontmatter field.

| Skill | What | Auth |
|-------|------|------|
| `fred` | Macro/financial time series (800K+ series) | API key (free) |
| `ken-french` | Factor returns, portfolios, breakpoints | None |
| `chen-zimmerman` | 200+ firm-level anomaly signals | None |

Researchers can add more data skills by creating `.claude/skills/{name}/SKILL.md`.
