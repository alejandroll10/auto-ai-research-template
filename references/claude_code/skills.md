# Claude Code Skills & Slash Commands

**Source**: https://code.claude.com/docs/en/skills.md

## What are Skills?

Skills are specialized instruction sets that Claude can invoke automatically (when relevant) or you trigger with `/skill-name`. They follow the **Agent Skills open standard** (agentskills.io).

## Where Skills Live

| Location | Scope | Path |
|----------|-------|------|
| Enterprise | All org users | Managed settings |
| Personal | All your projects | `~/.claude/skills/<name>/SKILL.md` |
| Project | This project only | `.claude/skills/<name>/SKILL.md` |
| Plugin | Where plugin enabled | `<plugin>/skills/<name>/SKILL.md` |

Priority: Enterprise > Personal > Project > Plugin

## SKILL.md Structure

Every skill is a directory with a `SKILL.md` file:

```
my-skill/
├── SKILL.md              # Required: frontmatter + instructions
├── reference.md          # Optional: detailed docs
├── examples/             # Optional
└── scripts/              # Optional
```

### Complete Frontmatter Reference

```yaml
---
name: my-skill                    # Display name, becomes /slash-command
description: When to use this     # Claude uses for auto-invocation
argument-hint: [endpoint-path]    # Shown in autocomplete
disable-model-invocation: false   # true = only manual /slash invocation
user-invocable: true              # false = only Claude can invoke
allowed-tools: Read, Grep, Bash   # Pre-approved tools
model: sonnet                     # sonnet, opus, haiku, or inherit
context: default                  # "fork" runs in isolated subagent
agent: Explore                    # Subagent type for context: fork
---
```

## Invocation

### Manual (Slash Commands)
```bash
/explain-code
/fix-issue 123
/migrate-component SearchBar React Vue
```

### Automatic
Claude reads `description` and invokes when relevant. Add "Use proactively" or "Use when" in description to encourage auto-invocation.

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$ARGUMENTS[N]` / `$N` | Specific argument by index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing SKILL.md |

## Dynamic Context Injection

Use backticks with `!` to run shell commands as preprocessing:

```yaml
## PR Context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

## Running Skills in Subagents

```yaml
---
context: fork
agent: Explore
---
```

Runs in isolated context. Results summarized back to main conversation.

## Built-in Skills

| Skill | Purpose |
|-------|---------|
| `/batch <instruction>` | Large-scale changes across 5-30 isolated worktrees |
| `/simplify [focus]` | Review changed files for quality |
| `/loop [interval] <prompt>` | Recurring prompts |
| `/debug [description]` | Troubleshoot session |
| `/claude-api` | Load Claude API reference |

## Skills vs. Subagents

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| Invocation | `/skill-name` or automatic | Automatic delegation |
| Context | Inline in main conversation | Isolated context window |
| Use Case | Reusable instructions | Self-contained tasks, parallel research |
| Output | Stays in main conversation | Summarized back |

## Creating a Skill

1. Create directory: `.claude/skills/my-skill/`
2. Create `SKILL.md` with frontmatter + instructions
3. Add optional supporting files (reference.md, scripts/)
4. Test with `/my-skill`
