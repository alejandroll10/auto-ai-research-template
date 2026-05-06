# CLAUDE.md — Meta Project: Pipeline Template Development

AFTER EVERY BIG CHANGE  SPAN A SONNET AGENT TO REVIEW YOUR CHANGES FOR ISSUES. IF ANY ISSUES ARE FOUND, ADD A NEW ROUND OF AUDITING AFTER FIXING THE CURRENT ROUND'S ISSUES (EVEN IF THERE ARE ONLY MINOR CHANGES). ITERATE UNTIL DONE.

WHEN ADDING A NEW INFRASTRUCTURE PATH TO `setup.sh` (DIR OR FILE THAT GETS DEPLOYED), ALSO ADD IT TO THE `candidate_dirs` / `candidate_files` LIST IN THE MANIFEST EMISSION BLOCK (`setup.sh:1184`); OTHERWISE `update.sh` WILL SILENTLY SKIP IT WHEN REFRESHING EXISTING DEPLOYMENTS.

WHEN ADDING A NEW `{{KEY}}` PLACEHOLDER TO ANY AGENT BODY (SHARED, VARIANT, OR EXTENSION), ADD A DEFAULT VALUE FOR THE KEY TO EVERY EXISTING VARIANT vocab.json (`templates/agents/{finance,macro}/vocab.json` AT MINIMUM). THE LOADER (`scripts/agent_body_loader.py`) RAISES `KeyError` ON UNRESOLVED PLACEHOLDERS, SO A MISSING DEFAULT BREAKS ASSEMBLY FOR ANY VARIANT THAT DOESN'T DEFINE THE KEY — FAIL-LOUD IS THE CORRECT BEHAVIOR, BUT IT MEANS A VARIANT-ONLY EDIT WILL BREAK SETUP FOR THE OTHER VARIANTS UNTIL THE KEY IS BACKFILLED. EXTENSION-AGENT PLACEHOLDERS HAVE THE SAME RULE — ANY NEW KEY IN AN EXTENSION BODY MUST APPEAR IN EVERY VARIANT VOCAB THE EXTENSION CAN COMPOSE WITH (CURRENTLY BOTH FINANCE AND MACRO).

## What this is

This is the **template repository** for the autonomous research paper pipeline. We are building and iterating on the pipeline infrastructure itself — agents, setup scripts, CLAUDE.md templates, dashboard, etc.

This file is tracked in git but **overwritten by `setup.sh`** in cloned projects. It is for our development work only. The pipeline's CLAUDE.md that end users see is assembled by `setup.sh` from `templates/shared/core.md` + `templates/runtime/claude/session.md` + per-variant vocab substitution. (Variant-specific scorer calibrations live in `templates/agents/{variant}/vocab.json` and are substituted into the scorer agent body, not appended as a separate block.)

## Working principle: no unsolved or undocumented architectural limits

When auditing or editing the pipeline, if a known architectural limit is identified (e.g., a self-referential check, a subjective rule, an enforcement gap, a missing producer for a consumed artifact), do not leave it acknowledged-and-moved-on. Either (a) solve it in the same pass, or (b) document it explicitly — in the relevant agent body, doc file, or a dedicated `LIMITATIONS.md` — with the failure mode it can produce and what would be needed to close it. Acknowledged-but-undocumented limits accumulate silently and produce surprises in future runs.

## Working principle: no complexity budget — do what is best for the pipeline

There is no complexity budget, no edit-cost ceiling, no "this change is too big" threshold. The pipeline is designed to be run millions of times; any one-time cost of editing the template — updating three runtime assemblers, reshaping `pipeline_state.json`, rewriting the escalation table, expanding the orchestrator prompt, adding agents, writing new tests — is trivially amortized against that. Do not reject or water down a structural proposal because it is expensive to *implement*; reject it only if it is worse for the pipeline on the merits.

Concretely:
- If a change makes the pipeline produce better papers, do it — even if it touches every runtime, rewrites state, and requires new agents.
- Do not propose a "narrower variant" to save implementation effort. Propose the narrower variant only if it is genuinely better for the output.
- Do not invoke "complexity cost," "maintenance burden," or "surface area" as reasons to decline. These are real for a one-shot project; here they are rounding errors against millions of runs.
- The only legitimate reasons to decline a structural proposal are: it makes the output worse, it introduces a correctness/safety regression, or a strictly better alternative exists on the merits.

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

# Light mode (sonnet for all subagents — cheaper/faster, orchestrator unchanged)
./setup.sh <project-name> --variant finance --light

# Seeded idea (creates output/seed/ — drop your files there before launching)
./setup.sh <project-name> --variant finance --seed

# Seeded idea + empirical
./setup.sh <project-name> --variant finance --seed --ext empirical

# Faithful mode (stricter --seed: implement the seed as a contract)
./setup.sh <project-name> --variant finance --faithful

# Faithful + empirical
./setup.sh <project-name> --variant finance --faithful --ext empirical

# Manual mode (research toolkit — agents and skills only, no autonomous pipeline)
./setup.sh <project-name> --variant finance --manual

# Manual mode + empirical extension
./setup.sh <project-name> --variant finance --manual --ext empirical
```

`--manual` is mutually exclusive with `--seed` and `--faithful`. It assembles `core_manual.md` instead of `core.md`, auto-generates an agent/skill catalog from the metadata files, swaps in per-runtime `session_manual.md` files, and skips creating `process_log/pipeline_state.json`, the `output/stage*` subdirs, and `dashboard.html`. Pipeline-only agents (`scribe`, `triager`, `puzzle-triager`, `branch-manager`) are still assembled into `.claude/agents/` etc. but flagged `pipeline_only: true` in metadata so `scripts/generate_catalog.py` hides them from the user-facing catalog.

`--faithful` is a stricter variant of `--seed`; pass one or the other, not both. The flag implies `--seed`'s folder structure (creates `output/seed/`, starts at `seed_triage`) but supersedes its semantics with the faithful contract. At seed_triage the orchestrator extracts `output/seed/mechanism_contract.md` (the seed's named mechanism, structural invariants, theorem-statement constraints, identification strategy, stated contribution); developing agents must respect every invariant. Substitution / pivot / headline-replacement are forbidden; additions on top of the faithfully-implemented contract (extra theorems, comparative statics, robustness checks) are encouraged. Genuine impossibilities get documented in `output/seed/limitations.md` and the paper ships documenting them honestly. Evaluators (scorer, scorer-freeform, math-auditor, math-auditor-freeform, novelty-checker, referee, referee-freeform, referee-mechanism, self-attacker, idea-prototyper, idea-reviewer, branch-manager, plus the extension evaluators empirics-auditor, identification-auditor under `--ext empirical` and experiment-reviewer under `--ext theory_llm`) stay impartial — corrupting the evaluation signal corrupts the paper. The faithful constraint enters at the orchestrator's routing of evaluator verdicts (per `templates/shared/faithful.md`) and via a static "read `mechanism_contract.md` first" pointer appended to each developing agent body. A `process_log/pivot_log.md` is seeded for auditing every potentially-mechanism-affecting routing decision.

This creates a standalone project folder with assembled CLAUDE.md, AGENTS.md, GEMINI.md, agents for all runtimes, and skills. After setup, tell the user to:

1. `cd <project-name>`
2. Edit `.env` with any required API keys (FRED, WRDS, etc.)
3. Launch any runtime: `claude --dangerously-skip-permissions` / `codex --sandbox danger-full-access --ask-for-approval never` / `gemini --yolo`
4. Say "Run the pipeline."

### WRDS server (only with `--ext empirical`)

The empirical extension talks to WRDS through a long-running local socket server (port 23847) so the Duo 2FA push happens once per session, not per query. The pipeline's data-inventory step starts it automatically (`templates/runtime/claude/session.md` runs `code/utils/start_services.sh` before Stage 0), but you can also start it manually:

```bash
cd <project-name>
bash code/utils/start_services.sh   # idempotent; reuses an existing server if one is up
```

The server is per-host, not per-project — once it's running, every project that has the WRDS skill reuses it. If you are working in the template repo itself (no `.env`, no `code/utils/`), `cd` into any existing deployed empirical project on this host and run `bash code/utils/start_services.sh` from there; the resulting server will serve the template's future deployments too.

To check if it's already running on this machine:

```bash
ss -tlnp | grep 23847                                                  # is anything listening?
PYTHONPATH=code python3 -c "from utils.wrds_client import wrds_ping; print(wrds_ping())"
```

`True` from the ping means it's healthy.

## Repository structure

```
templates/
├── shared/
│   ├── core.md              # Runtime-agnostic pipeline orchestrator template
│   ├── core_manual.md       # Slim manual-mode runtime doc (no pipeline, just catalogs)
│   ├── seed.md              # Seeded-idea override block (injected when --seed is used)
│   ├── faithful.md          # Stricter seeded-mode block (injected when --faithful is used)
│   ├── faithful_inject.md   # Short pointer appended to developing-agent bodies under --faithful
│   ├── seed_overrides/      # Per-stage overrides for --seed (gate doc placeholders)
│   └── faithful_overrides/  # Per-stage overrides for --faithful (supersedes seed_overrides)
├── runtime/
│   ├── claude/
│   │   ├── session.md           # Claude-specific session guidance (autonomous mode)
│   │   └── session_manual.md    # Claude-specific session guidance (manual mode)
│   ├── codex/
│   │   ├── session.md           # Codex orchestration discipline (autonomous mode)
│   │   └── session_manual.md    # Codex toolkit guidance (manual mode)
│   └── gemini/
│       ├── session.md           # Gemini orchestration discipline (autonomous mode)
│       └── session_manual.md    # Gemini toolkit guidance (manual mode)
├── agent_metadata/          # JSON metadata for agent assembly (tools, model, description)
│   ├── claude_shared_agents.json
│   ├── claude_finance_agents.json
│   └── claude_macro_agents.json
├── agent_bodies/            # Shared/extension agent prompt bodies (plain markdown)
│   └── shared/              # Domain-agnostic shared agent prompts
├── skill_metadata/          # JSON metadata for skill assembly
│   ├── codex_math_skills.json
│   ├── empirical_skills.json
│   └── theory_llm_skills.json
├── skill_bodies/            # Skill prompt bodies (plain markdown)
│   ├── codex_math/
│   ├── empirical/
│   └── theory_llm/
├── utils/                   # Utility scripts copied into deployed projects
│   └── codex_math/          # Codex proof verification/writing/exploration scripts
├── agents/                  # Variant agent prompt bodies (source of truth; no frontmatter)
│   ├── shared/
│   ├── finance/
│   └── macro/
└── gitignore_project        # .gitignore template for deployed projects

scripts/
├── assemble_claude_agents.py   # Combines agent metadata + bodies → .claude/agents/*.md
├── assemble_claude_skills.py   # Combines skill metadata + skill bodies → .claude/skills/*/SKILL.md
├── assemble_codex_skills.py    # Combines skill metadata + skill bodies → .agents/skills/*/SKILL.md
├── assemble_codex_subagents.py # Combines agent metadata + bodies → .codex/agents/*.toml
├── assemble_gemini_agents.py   # Combines agent metadata + bodies → .gemini/agents/*.md
└── generate_catalog.py         # Manual mode: emits agent/skill catalog markdown from metadata

extensions/                  # Optional extensions (empirical, theory_llm)
├── empirical/
│   ├── agent_metadata/      # shared_agents.json, finance_agents.json, macro_agents.json
│   ├── agent_bodies/        # shared/, finance/, macro/
│   └── utils/               # Python/shell utilities copied into project
└── theory_llm/
    ├── agent_metadata/      # agents.json
    ├── agent_bodies/        # Agent prompt bodies
    └── llm_client.py        # LLM client copied into project

setup.sh                     # Clones repo, assembles CLAUDE.md + AGENTS.md + GEMINI.md + agents + skills
dashboard.html               # Live progress dashboard
test_scripts/                # Skill verification scripts (removed on deploy)
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

## Core skills (all variants)

| Skill | Description |
|-------|-------------|
| `codex-math` | OpenAI Codex (gpt-5.5) for proof verification, writing, and exploration. Erratic genius — substantial false-positive rate, always triage. Scripts at `code/utils/codex_math/`. |

## How setup.sh works

1. Clones this repo into a new project folder
2. Reads `--variant` flag (default: `finance`)
3. Assembles runtime docs (CLAUDE.md, AGENTS.md, GEMINI.md):
   - Reads `templates/shared/core.md` (runtime-agnostic orchestrator)
   - Injects runtime-specific session guidance from `templates/runtime/{runtime}/session.md`
   - Substitutes per-variant scorer calibrations from `templates/agents/{variant}/vocab.json` into the scorer agent body
   - If `--seed`: injects `templates/shared/seed.md` as `{{SEED_OVERRIDE}}`
   - If `--faithful`: injects `templates/shared/faithful.md` instead (supersedes seed.md at the same placeholder)
   - Replaces `{{PAPER_TYPE}}`, `{{TARGET_JOURNALS}}`, `{{DOMAIN_AREAS}}`, `{{RUNTIME_DOC_NAME}}`, `{{AGENT_DIR}}`, `{{SKILL_DIR}}`
4. Assembles agents from metadata + prompt bodies:
   - Shared: `agent_metadata/claude_shared_agents.json` + `agent_bodies/shared/*.md`
   - Variant: `agent_metadata/claude_{variant}_agents.json` + `agents/{variant}/*.md`
   - Claude agents → `.claude/agents/*.md`, Codex → `.codex/agents/*.toml`, Gemini → `.gemini/agents/*.md`
5. Injects variant context (paper type, journal list, domain) into key agents
   - If `--faithful`: also appends `templates/shared/faithful_inject.md` (a short "read `output/seed/mechanism_contract.md` first" pointer) to *developing* agent bodies only — theory-generator, idea-generator, paper-writer, polish-* (all 8: prose, consistency, equilibria, formula, numerics, institutions, bibliography, identification), bib-verifier, plus extension developers (empiricist, identification-designer under `--ext empirical`; experiment-designer under `--ext theory_llm`). Evaluators (scorer, scorer-freeform, math-auditor, math-auditor-freeform, novelty-checker, referee, referee-freeform, referee-mechanism, self-attacker, idea-prototyper, idea-reviewer, branch-manager, plus extension evaluators empirics-auditor, identification-auditor, experiment-reviewer) explicitly do **not** receive the pointer — corrupting the evaluation signal corrupts the paper.
6. Creates project structure (output/, paper/, code/, etc.) and initial pipeline state
   - If `--seed`: creates `output/seed/` with a README, sets `pipeline_state.json` to start at `seed_triage` with `"seeded": true, "faithful": false`
   - If `--faithful`: creates `output/seed/` with a faithful-mode README, sets `pipeline_state.json` to start at `seed_triage` with `"seeded": true, "faithful": true`, and seeds `process_log/pivot_log.md` with a header + table skeleton for auditing routing decisions
7. Installs core Python deps (sympy, matplotlib) via `uv pip install`
8. Assembles core skills:
   - Claude skills into `.claude/skills/`
   - Codex/Gemini skills into `.agents/skills/` (shared)
   - Copies utility scripts to `code/utils/`
9. Applies extensions (`--ext empirical`, `--ext theory_llm`):
   - Assembles extension agents for all three runtimes
   - Assembles extension skills from shared skill metadata + bodies
   - Copies utilities, creates dirs, appends API keys to `.env`
10. Removes template infrastructure, detaches from origin, commits initial state

## Adding a new variant

1. Create agent metadata: `templates/agent_metadata/claude_{variant}_agents.json`
2. Create agent bodies: `templates/agents/{variant}/` with markdown prompts
3. Create `templates/agents/{variant}/vocab.json` with the per-variant vocabulary keys (scorer calibrations, importance/novelty/surprise rubrics, mechanism term, referee role, etc.) — see `templates/agents/finance/vocab.json` for the full set.
4. Add variant config to `setup.sh` (paper type, target journals, journal list, domain areas)
5. Test: `./setup.sh --variant {variant} --local`

## Architecture: runtime-agnostic core + runtime-specific packaging

The pipeline is split into two layers:

- **Runtime-agnostic**: `templates/shared/core.md` (orchestrator logic, pipeline stages), `templates/agent_bodies/shared/` and `templates/agents/{variant}/` (agent prompts and per-variant vocab including scorer calibrations) — these are the same regardless of runtime.
- **Runtime-specific**: `templates/runtime/{claude,codex,gemini}/session.md` (session guidance per runtime), `templates/agent_metadata/claude_*.json` (shared metadata with per-runtime overrides via `codex` and `gemini` keys), `scripts/assemble_{claude_agents,codex_subagents,gemini_agents}.py`.

Three runtimes share the same core + agent bodies, with runtime-specific packaging.

## Agent classification

Agents are either **shared** (identical across variants) or **variant-specific** (different prompts per domain). Each agent is defined as:
- **Metadata** (`agent_metadata/claude_*.json`): Claude frontmatter plus Codex and Gemini overrides
- **Body** (`agent_bodies/shared/*.md`, `agents/{variant}/*.md`): runtime-agnostic prompt content

**Shared** (domain-agnostic, receive variant context via injection):
- `literature-scout` — broad literature survey (variant context provides target journals)
- `gap-scout` — deep search on a pre-selected gap (adjacent literatures, closest competitor, gap validation)
- `idea-prototyper` — quick math feasibility + surprise check
- `theory-explorer` — computational verification, calibration, parameter exploration, plots
- `math-auditor` — checks derivations step-by-step
- `math-auditor-freeform` — reads as skeptical reader
- `scorer-freeform` — free-form quality assessment at Gate 4 (holistic read, no rubric)
- `referee-freeform` — free-form referee report at Stage 6 (editorial assessment)
- `novelty-checker` — searches web for prior work
- `paper-writer` — writes LaTeX from inputs
- `style` — checks writing style
- `branch-manager` — strategic advisor at Gate 4 + Stage 2 audit loop (every 3rd theory version); diagnoses ceiling/alternatives
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
