# Auto AI Research Template

Autonomous finance theory paper generator. Clone, launch, walk away. The system discovers a problem, generates a theory, verifies it adversarially, and writes a publication-ready paper.

## Quick start

### Option A: From Cursor (recommended)

1. Create a new empty folder and open it in Cursor
2. Open the Claude Code terminal (`claude --dangerously-skip-permissions`)
3. Say:

```
Clone https://github.com/alejandroll10/auto-ai-research-template.git into this folder. Then read CLAUDE.md and run the pipeline.
```

4. Watch files appear in the file tree as the pipeline runs

### Option B: From terminal

```bash
./setup.sh my-paper                   # pure theory (default)
./setup.sh my-paper --theory-llm      # theory + LLM experiments
cd my-paper
claude --dangerously-skip-permissions
```

Then say: **"Run the pipeline."**

### Variants

| Variant | Flag | What it adds |
|---------|------|-------------|
| **Pure theory** | (default) | Standard pipeline: problem → theory → paper |
| **theory_llm** | `--theory-llm` | Adds LLM experiment stages: tests predictions using gpt-oss models via UF NaviGator. Requires `UF_API_KEY`. |

## Prerequisites

### System packages (Ubuntu/Debian)

```bash
sudo apt-get install python3 python3-pip git bubblewrap
```

### Python tools

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

## Watch progress (dashboard)

In a second terminal:

```bash
cd my-paper
python3 -m http.server 8000
```

Open `http://localhost:8000/dashboard.html` in a browser. It auto-refreshes every 5 seconds showing current stage, scores, gate results, and event history.

## What happens

The pipeline runs autonomously through these stages:

```
Problem Discovery → Idea Generation (iterates) → Theory Development
→ Math Audit → Novelty Check → Implications → Self-Attack
→ Scorer Gate → Paper Writing → Referee Simulation → Style Check → Done
```

Each stage has adversarial quality gates. Failed theories get revised, reworked, or abandoned. The system loops until it produces a paper that passes a simulated referee review.

## Agents

| Agent | Role |
|-------|------|
| `literature-scout` | Web search for papers, builds literature map |
| `idea-generator` | Brainstorms candidate mechanisms and model ideas |
| `idea-reviewer` | Evaluates and ranks idea sketches, iterates with generator |
| `theory-generator` | Develops selected idea into full model with proofs |
| `math-auditor` | Adversarial step-by-step derivation verification |
| `novelty-checker` | Web search to verify result is genuinely new |
| `self-attacker` | Hostile weakness finder, severity-ranked attacks |
| `scorer` | Quality gate: advance/revise/abandon decisions |
| `paper-writer` | Assembles LaTeX paper from scored theory |
| `referee` | Simulates top-journal R1 review |
| `style` | Enforces writing style guide |
| `scribe` | Background documentation of the process |

## Safety

Sandbox is pre-configured in `.claude/settings.json`:
- Bash restricted to project folder only
- Cannot read SSH keys or AWS credentials
- WebSearch and WebFetch work freely (for literature)
- `bubblewrap` enforces restrictions at OS level

## Project structure

```
├── CLAUDE.md                 # Pipeline orchestration logic
├── setup.sh                  # One-command setup
├── .claude/
│   ├── settings.json         # Sandbox config
│   └── agents/               # 12 custom subagents
├── output/
│   ├── stage0/               # Problem discovery
│   ├── stage1/               # Idea sketches and reviews
│   ├── stage2/               # Theory drafts, audits, novelty checks
│   ├── stage3/               # Implications
│   └── stage4/               # Self-attack, scorer decisions
├── paper/
│   ├── main.tex
│   ├── sections/             # One .tex file per section
│   └── referee_reports/
├── process_log/
│   ├── pipeline_state.json   # Current stage, attempt counts
│   └── history.md            # Full narrative record
└── references/
```

## License

For Private use until further notice.
