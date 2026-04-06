# Auto AI Research Template

Autonomous research paper generator. Set up a project, launch Claude Code, Codex, or Gemini CLI, walk away. The system discovers a problem, generates a theory, verifies it adversarially, and writes a publication-ready paper.

## How it works

1. You clone this template repo once
2. You run `setup.sh` to create a new project — each run creates an independent project folder with its own git repo
3. You open the project folder in Claude Code, Codex, or Gemini CLI and say "Run the pipeline"
4. The pipeline runs autonomously: problem discovery → idea generation → theory development → math verification → paper writing → referee simulation

## Prerequisites

```bash
# System packages (Ubuntu/Debian)
sudo apt-get install python3 python3-pip git bubblewrap

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Claude Code
npm install -g @anthropic-ai/claude-code

# Codex
npm install -g @openai/codex

# Gemini CLI
npm install -g @google/gemini-cli
```

## Quick start

### Step 1: Clone this template (once)

```bash
git clone https://github.com/alejandroll10/auto-ai-research-template.git
cd auto-ai-research-template
```

### Step 2: Create a project

```bash
# Pure finance theory (default)
./setup.sh my-paper

# Finance theory + empirical analysis (CRSP, Compustat, FRED, etc.)
./setup.sh my-paper --variant finance --ext empirical

# Macro theory
./setup.sh my-paper --variant macro

# Finance theory + LLM experiments
./setup.sh my-paper --variant finance --ext theory_llm

# Combine extensions
./setup.sh my-paper --variant finance --ext empirical --ext theory_llm
```

This creates `my-paper/` with everything assembled and ready — `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, agents for all three runtimes, skills, and pipeline state. The folder is a standalone git repo detached from this template.

You can create as many projects as you want from the same template.

### Step 3: Configure credentials (if using extensions)

```bash
cd my-paper
# Edit .env with your API keys (created by setup.sh)
nano .env
```

| Extension | Credentials needed |
|-----------|-------------------|
| `--ext empirical` | `FRED_API_KEY` (free, from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)), `WRDS_USER` + `WRDS_PASS` (from [WRDS](https://wrds-www.wharton.upenn.edu/)) |
| `--ext theory_llm` | `UF_API_KEY` (from [UF NaviGator](https://api.ai.it.ufl.edu)) |

### Step 4: Launch

Claude Code:

```bash
cd my-paper
claude --dangerously-skip-permissions
```

Codex:

```bash
cd my-paper
codex --sandbox danger-full-access --ask-for-approval never
```

Gemini CLI:

```bash
cd my-paper
gemini --yolo
```

Then say: **"Run the pipeline."**

That's it. Claude Code reads `CLAUDE.md`; Codex reads `AGENTS.md`; Gemini reads `GEMINI.md`. In any runtime, the pipeline checks its state and runs autonomously from there. If the session ends mid-pipeline, relaunch the runtime and say "Run the pipeline" — it picks up where it left off.

## Watch progress

Open a second terminal:

```bash
cd my-paper
python3 -m http.server 8000
```

Open `http://localhost:8000/dashboard.html`. It auto-refreshes every 5 seconds showing current stage, scores, gate results, and event history.

You can also watch files appear in real time in your editor, or run `git log --oneline` to see the commit history (the pipeline commits at stage transitions and gate decisions).

## Variants

| Variant | Flag | Target journals | What it does |
|---------|------|-----------------|-------------|
| **finance** | `--variant finance` (default) | JF, JFE, RFS | Pure finance theory paper |
| **macro** | `--variant macro` | AER, Econometrica, QJE, JPE, ReStud, JME | Macro theory paper |

## Extensions

| Extension | Flag | What it adds |
|-----------|------|-------------|
| **empirical** | `--ext empirical` | Stage 3b: empirical analysis with real data (CRSP, Compustat, FRED, Ken French, Chen-Zimmerman, WRDS) |
| **theory_llm** | `--ext theory_llm` | Stage 3b/3c: test predictions via LLM experiments using gpt-oss models (UF NaviGator) |

Extensions are additive and combinable — they inject extra agents and skills without changing the core pipeline. Use multiple `--ext` flags to combine them.

## Pipeline stages

```
Stage 0: Problem Discovery   → Gate 0: Problem Viability
Stage 1: Idea Generation     → Gate 1: Idea Review (iterates)
                                Gate 1b: Novelty Check on idea
                                Gate 1c: Idea Prototype (tractability)
Stage 2: Theory Development  → Gate 2: Math Audit (structured + free-form)
                                Gate 3: Novelty Check on theory
                                Stage 3a: Theory Exploration (compute, verify, plot)
                                Gate 3b: Empirical Feasibility (optional)
Stage 3: Implications
Stage 3e: Full Empirical Analysis (optional, if --ext empirical)
Stage 4: Self-Attack          → Gate 4: Scorer Decision
Stage 5: Paper Writing
Stage 6: Referee Simulation   → Gate 5: Referee Decision
Stage 7: Style Check          → Done
```

Each gate is adversarial. Failed theories get revised, reworked, or abandoned. The system loops until it produces a paper that passes simulated referee review.

## Agents

| Agent | Role |
|-------|------|
| `literature-scout` | Web search for papers, builds literature map |
| `idea-generator` | Brainstorms candidate mechanisms |
| `idea-reviewer` | Evaluates and ranks idea sketches |
| `idea-prototyper` | Quick math feasibility check before full theory |
| `theory-generator` | Develops selected idea into full model with proofs |
| `math-auditor` | Step-by-step derivation verification |
| `math-auditor-freeform` | Skeptical reader audit |
| `novelty-checker` | Web search to verify result is genuinely new |
| `theory-explorer` | Computational verification — calibration, parameter space, plots |
| `self-attacker` | Finds every possible weakness |
| `scorer` | Quality gate: advance/revise/abandon decisions |
| `paper-writer` | Assembles LaTeX paper |
| `referee` | Simulates top-journal R1 review |
| `style` | Enforces writing style guide |
| `scribe` | Background documentation of the process |
| `empiricist` | Empirical analysis (if `--ext empirical`) |
| `empirics-auditor` | Verifies empirical code and results (if `--ext empirical`) |
| `experiment-designer` | Designs and runs LLM experiments (if `--ext theory_llm`) |
| `experiment-reviewer` | Verifies experiment design and results (if `--ext theory_llm`) |

## Core skills

| Skill | Runtime | Purpose |
|-------|---------|---------|
| `codex-math` | Claude + Codex | OpenAI Codex (gpt-5.4) for proof verification, proof writing, derivation checking, and conjecture exploration |

## Data skills (with `--ext empirical`)

| Skill | Source | Auth |
|-------|--------|------|
| `edgar` | SEC EDGAR filings, statements, and full-text filing search | None (identity header required) |
| `flex-mining` | Flexible empirical spec and robustness workflow support | None |
| `fred` | FRED — 800K+ macro/financial time series | API key (free) |
| `ken-french` | Ken French Data Library — factor returns, portfolios | None |
| `chen-zimmerman` | Open Source Asset Pricing — 200+ anomaly signals | None |
| `mutual-funds` | Mutual fund holdings and fund-level empirical workflows | None |
| `wrds` | WRDS — CRSP, Compustat, IBES, options, insider trading | Username + password |

## Project structure (after setup)

```
my-paper/
├── CLAUDE.md                 # Claude Code orchestration (assembled by setup.sh)
├── AGENTS.md                 # Codex orchestration (assembled by setup.sh)
├── GEMINI.md                 # Gemini CLI orchestration (assembled by setup.sh)
├── .env                      # API keys (gitignored)
├── dashboard.html            # Live progress dashboard
├── .claude/
│   ├── settings.json         # Sandbox config
│   ├── agents/               # Claude subagents (.md)
│   └── skills/               # Claude skills
├── .codex/
│   └── agents/               # Codex custom agents (.toml)
├── .gemini/
│   ├── settings.json         # Gemini config
│   └── agents/               # Gemini subagents (.md)
├── .agents/
│   └── skills/               # Shared skills (Codex + Gemini)
├── output/                   # Pipeline outputs by stage
├── paper/                    # LaTeX paper
│   ├── main.tex
│   ├── sections/
│   └── referee_reports/
├── code/
│   ├── analysis/             # Analysis and verification scripts
│   ├── download/             # Data download helpers
│   ├── explore/              # Exploration scripts and diagnostics
│   ├── tmp/                  # Scratch files
│   └── utils/                # Utility scripts (including codex-math; more with extensions)
└── process_log/
    ├── pipeline_state.json   # Current stage, scores, history
    └── history.md
```

## Runtime notes

- Claude Code: `claude --dangerously-skip-permissions`
- Codex: `codex --sandbox danger-full-access --ask-for-approval never`
- Gemini CLI: `gemini --yolo`
- All runtimes read the same pipeline state and produce identical artifacts — you can switch runtimes mid-pipeline.

## Safety

Sandbox is pre-configured in `.claude/settings.json`:
- Bash restricted to project folder only
- Cannot read SSH keys or AWS credentials
- WebSearch and WebFetch work freely (for literature search)
- `bubblewrap` enforces restrictions at OS level

## License

Copyright (c) 2026 Alejandro Lopez-Lira (alejandroll10@gmail.com)

All rights reserved.

This software and associated documentation files (the "Software") are for
private use only. No permission is granted to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software without
explicit written permission from the copyright holder.

For licensing inquiries, contact: alejandroll10@gmail.com
