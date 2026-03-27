# CLAUDE.md — Meta Project: Pipeline Template Development

## What this is

This is the **template repository** for the autonomous research paper pipeline. We are building and iterating on the pipeline infrastructure itself — agents, setup scripts, CLAUDE.md templates, dashboard, etc.

This file is tracked in git but **overwritten by `setup.sh`** in cloned projects. It is for our development work only. The pipeline's CLAUDE.md that end users see is assembled by `setup.sh` from `templates/claude_md/core.md` + variant-specific domain/scoring blocks.

## Setting up a new project

If a user asks to create/set up/start a new research project, run `setup.sh` for them:

```bash
# Basic finance theory
./setup.sh <project-name> --variant finance

# Finance theory + empirical data (CRSP, Compustat, FRED, WRDS)
./setup.sh <project-name> --variant finance --ext empirical

# Macro theory
./setup.sh <project-name> --variant macro

# Finance theory + LLM experiments
./setup.sh <project-name> --variant finance --ext theory_llm

# Combine extensions
./setup.sh <project-name> --variant finance --ext empirical --ext theory_llm
```

This creates a standalone project folder with assembled CLAUDE.md, agents, and skills. After setup, tell the user to:

1. `cd <project-name>`
2. Edit `.env` with any required API keys (FRED, WRDS, etc.)
3. Run `claude --dangerously-skip-permissions`
4. Say "Run the pipeline."

## Repository structure

```
templates/
├── agents/
│   ├── shared/          # Agents used by all variants (literature-scout, math-auditor, etc.)
│   ├── finance/         # Finance theory variant agents (idea-generator, scorer, etc.)
│   └── macro/           # Macro variant agents
├── domains/
│   ├── finance.md       # Domain knowledge reference (not injected — for dev reference only)
│   └── macro.md         # Domain knowledge reference (not injected — for dev reference only)
├── scoring/
│   ├── finance.md       # Scoring calibrations for finance
│   └── macro.md         # Scoring calibrations for macro
└── claude_md/
    └── core.md          # Pipeline orchestrator template (with {{SCORING}}, {{PAPER_TYPE}}, etc.)

extensions/              # Optional extensions (empirical, theory_llm)
setup.sh                 # Clones repo, assembles CLAUDE.md + agents for chosen variant
dashboard.html           # Live progress dashboard
test_scripts/            # Skill verification scripts (removed on deploy)
```

## Supported variants

| Variant | Flag | Status | Target journals |
|---------|------|--------|-----------------|
| `finance` | `--variant finance` (default) | Working (v2) | JF, JFE, RFS |
| `macro` | `--variant macro` | In development | AER, Econometrica, QJE, JPE, ReStud, JME |

## Supported extensions

| Extension | Flag | Status |
|-----------|------|--------|
| `empirical` | `--ext empirical` | Working |
| `theory_llm` | `--ext theory_llm` | Working (v1) |

Legacy: `--variant finance_llm` is shorthand for `--variant finance --ext theory_llm`.

## How setup.sh works

1. Clones this repo into a new project folder
2. Reads `--variant` flag (default: `finance`)
3. Assembles CLAUDE.md:
   - Reads `templates/claude_md/core.md`
   - Replaces `{{SCORING}}` with contents of `templates/scoring/{variant}.md`
   - Replaces `{{PAPER_TYPE}}`, `{{TARGET_JOURNALS}}`, `{{DOMAIN_AREAS}}` with variant-specific strings
4. Copies agents: `templates/agents/shared/*` + `templates/agents/{variant}/*` → `.claude/agents/`
5. Injects variant context (paper type, journal list, domain) into key agents
6. Applies extensions (`--ext empirical`, `--ext theory_llm`) — copies skills, agents, creates dirs
7. Creates project structure (output/, paper/, code/, etc.) and initial pipeline state
8. Removes template infrastructure, detaches from origin, commits initial state

## Adding a new variant

1. Create `templates/agents/{variant}/` with variant-specific agents
2. Create `templates/scoring/{variant}.md` with scoring calibrations
3. Add variant config to `setup.sh` (paper type, target journals, journal list, domain areas)
4. Test: `./setup.sh --variant {variant} --local`

## Agent classification

Agents are either **shared** (identical across variants) or **variant-specific** (different prompts per domain).

**Shared** (domain-agnostic, receive variant context via injection):
- `literature-scout` — searches for papers (variant context provides target journals)
- `idea-prototyper` — quick math feasibility check
- `theory-explorer` — computational verification, calibration, parameter exploration, plots
- `math-auditor` — checks derivations step-by-step
- `math-auditor-freeform` — reads as skeptical reader
- `novelty-checker` — searches web for prior work
- `paper-writer` — writes LaTeX from inputs
- `style` — checks writing style
- `scribe` — documents the process

**Variant-specific** (different prompts per domain):
- `idea-generator` — needs domain-specific brainstorming patterns
- `idea-reviewer` — needs domain-specific evaluation criteria
- `theory-generator` — needs domain-specific model structure guidance
- `scorer` — needs domain-specific calibrations
- `self-attacker` — needs domain-specific attack vectors
- `referee` — needs domain-specific journal standards

**Extension agents** (added by `--ext` flags):
- `empiricist` — empirical analysis (variant-specific, `--ext empirical`)
- `empirics-auditor` — verifies empirical code/results (shared, `--ext empirical`)
- `experiment-designer` — LLM experiments (shared, `--ext theory_llm`)
- `experiment-reviewer` — validates experiment methodology (shared, `--ext theory_llm`)
