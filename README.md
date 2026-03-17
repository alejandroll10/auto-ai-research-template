# Auto AI Research Template

An enhanced template for AI-assisted academic research using Claude Code with agentic capabilities (subagents, skills, sandbox, web search).

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

## Setup

```bash
git clone https://github.com/alejandroll10/auto-ai-research-template.git
cd auto-ai-research-template
uv venv .venv
source .venv/bin/activate
```

## Usage

```bash
# Standard mode (with permission prompts)
claude

# Autonomous mode (sandbox restricts Bash to project folder)
claude --dangerously-skip-permissions
```

## Project Structure

```
├── CLAUDE.md              # Project instructions for Claude
├── .claude/
│   ├── settings.json      # Sandbox & permission config
│   └── agents/            # Custom subagents (scribe, referee, style)
├── code/                  # Analysis code
├── data/                  # Raw and processed data
├── paper/                 # LaTeX paper drafts
├── output/                # Figures, tables, results
├── process_log/           # Documentation & research log
└── references/            # Papers, data sources, Claude Code docs
```

## License

MIT
