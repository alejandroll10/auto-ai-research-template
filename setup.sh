#!/bin/bash
# Auto AI Research Template — Setup & Launch
# Usage: ./setup.sh [project-name] [--variant finance|macro|finance_llm]

set -e

# ── Parse arguments ──
PROJECT_NAME=""
VARIANT="finance"

for arg in "$@"; do
    case "$arg" in
        --variant)   NEXT_IS_VARIANT=1 ;;
        --theory-llm) VARIANT="finance_llm" ;;  # legacy flag
        -*)          echo "Unknown option: $arg"; exit 1 ;;
        *)
            if [ "$NEXT_IS_VARIANT" = "1" ]; then
                VARIANT="$arg"
                NEXT_IS_VARIANT=0
            else
                PROJECT_NAME="$arg"
            fi
            ;;
    esac
done

PROJECT_NAME="${PROJECT_NAME:-my-research-paper}"

# ── Variant configuration ──
case "$VARIANT" in
    finance)
        PAPER_TYPE="finance theory paper"
        TARGET_JOURNALS="top-3 finance journal (JF, JFE, RFS)"
        DOMAIN_AREAS="asset pricing or corporate finance"
        AGENT_DIR="finance"
        ;;
    macro)
        PAPER_TYPE="macroeconomics theory paper"
        TARGET_JOURNALS="top-5 economics journal (AER, Econometrica, QJE, JPE, ReStud) or leading macro field journal (JME, JEDC, AEJ:Macro)"
        DOMAIN_AREAS="monetary policy, fiscal policy, business cycles, inequality and macro, or expectations"
        AGENT_DIR="macro"
        ;;
    finance_llm)
        PAPER_TYPE="finance theory paper with LLM experiments"
        TARGET_JOURNALS="top-3 finance journal (JF, JFE, RFS)"
        DOMAIN_AREAS="asset pricing or corporate finance"
        AGENT_DIR="finance"
        ;;
    *)
        echo "Unknown variant: $VARIANT"
        echo "Available variants: finance, macro, finance_llm"
        exit 1
        ;;
esac

# ── Check prerequisites ──
echo "Checking prerequisites..."

missing=()

command -v python3 >/dev/null 2>&1 || missing+=("python3")
command -v git >/dev/null 2>&1 || missing+=("git")
command -v claude >/dev/null 2>&1 || missing+=("claude (npm install -g @anthropic-ai/claude-code)")
command -v uv >/dev/null 2>&1 || missing+=("uv (curl -LsSf https://astral.sh/uv/install.sh | sh)")

# Check bubblewrap (Linux only)
if [[ "$(uname)" == "Linux" ]]; then
    command -v bwrap >/dev/null 2>&1 || missing+=("bubblewrap (sudo apt-get install bubblewrap)")
fi

if [ ${#missing[@]} -gt 0 ]; then
    echo "Missing dependencies:"
    for dep in "${missing[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "Install them and re-run this script."
    exit 1
fi

echo "All prerequisites found."

# ── Clone template ──
echo "Cloning template into $PROJECT_NAME..."
git clone https://github.com/alejandroll10/auto-ai-research-template.git "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Remove template remote, start fresh
git remote remove origin

# ── Assemble CLAUDE.md ──
echo "Assembling CLAUDE.md for variant: $VARIANT..."

CORE="templates/claude_md/core.md"
DOMAIN_FILE="templates/domains/${AGENT_DIR}.md"
SCORING_FILE="templates/scoring/${AGENT_DIR}.md"

for f in "$CORE" "$DOMAIN_FILE" "$SCORING_FILE"; do
    if [ ! -f "$f" ]; then
        echo "Error: $f not found"
        exit 1
    fi
done

# Build CLAUDE.md from template — single Python pass, all replacements
python3 - "$CORE" "$DOMAIN_FILE" "$SCORING_FILE" "$PAPER_TYPE" "$TARGET_JOURNALS" "$DOMAIN_AREAS" <<'PYEOF'
import sys

core_path, domain_path, scoring_path, paper_type, target_journals, domain_areas = sys.argv[1:7]

with open(core_path) as f:
    content = f.read()
with open(domain_path) as f:
    domain = f.read()
with open(scoring_path) as f:
    scoring = f.read()

content = content.replace('{{PAPER_TYPE}}', paper_type)
content = content.replace('{{TARGET_JOURNALS}}', target_journals)
content = content.replace('{{DOMAIN_AREAS}}', domain_areas)
content = content.replace('{{DOMAIN}}', domain)
content = content.replace('{{SCORING}}', scoring)

with open('CLAUDE.md', 'w') as f:
    f.write(content)
PYEOF

echo "  ✓ CLAUDE.md assembled"

# ── Assemble agents ──
echo "Copying agents..."

# Clear default agents
rm -f .claude/agents/*.md

# Copy shared agents
cp templates/agents/shared/*.md .claude/agents/

# Copy variant-specific agents (overrides shared if same name)
if [ -d "templates/agents/${AGENT_DIR}" ]; then
    cp templates/agents/${AGENT_DIR}/*.md .claude/agents/
fi

echo "  ✓ Agents copied (shared + ${AGENT_DIR})"

# ── Apply finance_llm extension if needed ──
if [ "$VARIANT" = "finance_llm" ]; then
    echo "Applying LLM experiment extension..."

    # Copy LLM client
    cp extensions/theory_llm/llm_client.py .

    # Copy experiment agents
    cp extensions/theory_llm/agents/*.md .claude/agents/

    # Create .env placeholder
    if [ ! -f .env ]; then
        echo "# Get API key from https://api.ai.it.ufl.edu" > .env
        echo "UF_API_KEY=your-key-here" >> .env
    fi

    # Create experiment output directory
    mkdir -p output/stage3b_experiments

    # Install Python deps
    pip install openai python-dotenv -q 2>/dev/null || echo "Note: install openai and python-dotenv manually"

    echo "  ✓ LLM experiment extension applied"
fi

# ── Clean up template infrastructure ──
echo "Cleaning up template files..."
rm -rf templates/
# Remove .gitignore entry for CLAUDE.md (it's now a real file, not our meta one)
sed -i '/^CLAUDE\.md$/d' .gitignore
echo "  ✓ Template files removed"

# ── Commit initial state ──
git add -A
git commit -m "setup: initialized ${VARIANT} variant pipeline" -q

echo ""
echo "============================================"
echo "  Setup complete: $PROJECT_NAME ($VARIANT)"
echo "============================================"
echo ""
echo "To run the autonomous pipeline:"
echo ""
echo "  cd $PROJECT_NAME"
echo "  claude --dangerously-skip-permissions"
echo ""
echo "Then say: \"Run the pipeline.\""
echo ""
if [ "$VARIANT" = "finance_llm" ]; then
    echo "NOTE: Edit .env and add your UF_API_KEY before running."
    echo "Test connection: python llm_client.py"
    echo ""
fi
echo "Variant: $VARIANT"
echo "Sandbox is pre-configured in .claude/settings.json"
echo "(Bash restricted to project folder, web access works freely)"
