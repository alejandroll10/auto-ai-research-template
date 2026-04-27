## Self-review after big changes

AFTER EVERY BIG CHANGE SPAWN A SONNET AGENT TO REVIEW YOUR CHANGES FOR ISSUES. IF ANY ISSUES ARE FOUND, ADD A NEW ROUND OF AUDITING AFTER FIXING THE CURRENT ROUND'S ISSUES (EVEN IF THERE ARE ONLY MINOR CHANGES). ITERATE UNTIL DONE.

"Big change" here means substantive research output — a new theory draft, a major theory revision, a paper section rewrite, a non-trivial empirical pipeline edit, or any multi-file restructuring. Use the `general-purpose` subagent on the `sonnet` model with a prompt that names the changed files and asks for issues, inconsistencies, or missed implications.

## How to use this toolkit

When the user gives you a research task:

1. Pick the right agent or skill from the catalog above.
2. Invoke it via the Agent tool with a self-contained prompt — the subagent does not see this conversation.
3. Read its output file, decide what to do next, and either invoke another agent or return to the user.

When the user is unsure what to do next, do not guess. Read `paper/main.tex`, list `paper/sections/`, list `output/`, and list `references/`. Use what you find to propose two or three concrete next steps from the catalog (e.g., "theory draft exists but no math audit — launch `math-auditor`?"; "paper draft exists, no referee report — launch `referee` + `referee-mechanism` + `referee-freeform` in parallel?"; "no paper draft yet — launch `literature-scout` to start a fresh project?").

Also detect which "shape" the paper is in by checking `paper/`:
- **Empty `paper/sections/`, no `paper/.git`** → ask the user whether to import an existing paper into `paper/` or launch `paper-writer` to create one from scratch.
- **`paper/.git` exists** → user has dropped in a separate paper repo. Confirm `.gitignore` has a bare `paper/` line; if not, propose adding it so the outer git stops seeing the nested repo as untracked (the existing `paper/*.foo` lines become harmless once `paper/` is excluded). Then proceed.
- **`paper/sections/*.tex` files exist, no `paper/.git`** → paper is in place as flat files. Proceed.

### Agent launch and monitoring

Subagents can hang indefinitely. Launch web-dependent agents (`literature-scout`, `novelty-checker`, `gap-scout`) in the background. Check their output file every few minutes — if empty or not growing after a few checks, re-launch with the same prompt.

### Skills

User-invocable skills in `{{SKILL_DIR}}/` (and `.agents/skills/` for Codex/Gemini) can be triggered directly with `/skill-name <args>` syntax in supporting runtimes, or invoked programmatically via the Skill tool.
