# Claude Refactor Plan

## Goal

Finish modularizing the currently implemented Claude runtime path before adding support for additional runtimes.

Current principle:
- preserve generated Claude output exactly
- move shared logic out of `setup.sh`
- separate runtime-specific packaging from shared content
- treat agents, skills, utilities, and workflow logic as shared capabilities, even if Claude is the only implemented runtime today

## Current status

Interpretation:
- the research workflow content is not Claude-specific in principle
- it is only packaged for Claude right now because Claude is the only implemented runtime
- future runtimes should reuse the same shared capabilities and content, with runtime-specific adapters handling packaging

Completed:
- `CLAUDE.md` assembly split into:
  - `templates/shared/core.md`
  - `templates/runtime/claude/session.md`
  - `templates/scoring/*.md`
- Claude path conventions centralized in `setup.sh`
- helper functions added for copying agents
- shared Claude agents modularized into:
  - `templates/agent_metadata/claude_shared_agents.json`
  - `templates/agent_bodies/shared/*.md`
  - `scripts/assemble_claude_agents.py`
- `setup.sh` now assembles shared Claude agents from metadata + bodies
- Claude variant agents modularized into:
  - `templates/agent_metadata/claude_finance_agents.json`
  - `templates/agent_metadata/claude_macro_agents.json`
  - `templates/agent_bodies/finance/*.md`
  - `templates/agent_bodies/macro/*.md`
- `setup.sh` now assembles variant agents from metadata + bodies
- Claude extension agents modularized into:
  - `extensions/empirical/agent_metadata/*.json`
  - `extensions/empirical/agent_bodies/{shared,finance,macro}/*.md`
  - `extensions/theory_llm/agent_metadata/agents.json`
  - `extensions/theory_llm/agent_bodies/*.md`
- `setup.sh` now assembles extension agents from metadata + bodies
- Claude extension skills modularized into:
  - `templates/skill_metadata/claude_empirical_skills.json`
  - `templates/skill_metadata/claude_theory_llm_skills.json`
  - `templates/skill_bodies/empirical/*.md`
  - `templates/skill_bodies/theory_llm/*.md`
  - `scripts/assemble_claude_skills.py`
- `setup.sh` now assembles extension skills from metadata + bodies

Verified:
- generated `CLAUDE.md` matches `codex_inspect/CLAUDE.md`
- generated shared `.claude/agents/*.md` match `codex_inspect/.claude/agents/*.md`
- generated finance variant agents match baseline output after refactor
- generated macro variant agents match baseline output after refactor
- generated finance extension agents match baseline output after refactor
- generated macro extension agents match baseline output after refactor
- generated `.claude/skills/*/SKILL.md` match `codex_inspect/.claude/skills/*/SKILL.md`
- full local regeneration passed:
  - `./setup.sh test_output/refactor_compare --variant finance --ext empirical --ext theory_llm --local`
- variant parity checks passed:
  - `diff -ru test_output/variant_baseline_finance/.claude/agents test_output/variant_compare_finance/.claude/agents`
  - `diff -ru test_output/variant_baseline_macro/.claude/agents test_output/variant_compare_macro/.claude/agents`
- extension parity checks passed:
  - `diff -ru test_output/ext_agent_baseline_finance/.claude/agents test_output/ext_agent_compare_finance/.claude/agents`
  - `diff -ru test_output/ext_agent_baseline_macro/.claude/agents test_output/ext_agent_compare_macro/.claude/agents`
- committed and pushed:
  - `72ac58c` (`Modularize Claude skill assembly`)
  - `62ddb52` (`Modularize Claude variant agents`)
  - `643621d` (`Modularize Claude extension agents`)

Not done yet:
- none for the current Claude runtime packaging path

Not started yet:
- runtime packaging support beyond Claude

## Recommended next steps

### 1. Add support for additional runtimes

Current status:
- the currently implemented Claude runtime path is modularized end to end
- shared capabilities and content are now separated from most runtime packaging concerns

Recommended structure:
- keep shared capabilities in reusable metadata/body/utils layers
- add runtime-specific adapters for each new runtime
- avoid duplicating shared content across runtimes

Goal:
- implement a second runtime without disturbing Claude parity
- prove the architecture supports multiple runtimes cleanly

## Constraints

- Do not modify or overwrite `codex_inspect/`
- Use `test_output/` for regeneration and diff checks
- Preserve generated Claude output exactly at each step
- Keep unrelated worktree changes untouched

## Verification checklist

After each refactor:

1. Run:
```bash
./setup.sh test_output/refactor_compare --variant finance --ext empirical --ext theory_llm --local
```

2. Diff orchestrator:
```bash
diff -u codex_inspect/CLAUDE.md test_output/refactor_compare/CLAUDE.md
```

3. Diff generated agent/skill outputs affected by the refactor.

4. Only commit after output parity is confirmed.

## Suggested order for the next session

1. commit the extension-installer extraction
2. add support for an additional runtime using the shared capability layer
