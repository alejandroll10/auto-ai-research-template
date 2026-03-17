# Claude Code Custom Subagents

**Source**: https://code.claude.com/docs/en/sub-agents.md

## Overview

Subagents are specialized AI assistants that handle specific tasks. Each runs in its own context window with a custom system prompt, specific tool access, and independent permissions. Claude delegates to subagents when tasks match their description.

## Built-in Subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only | File discovery, code search, codebase exploration |
| **Plan** | Inherit | Read-only | Codebase research for planning |
| **General-purpose** | Inherit | All | Complex research, multi-step operations, code modifications |
| **Bash** | Inherit | Terminal | Running terminal commands in separate context |
| **Claude Code Guide** | Haiku | Read-only | Questions about Claude Code features |

## Where Subagents Live

| Location | Scope | Priority |
|----------|-------|----------|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All your projects | 3 |
| Plugin's `agents/` | Where plugin enabled | 4 (lowest) |

## Subagent File Format

Markdown files with YAML frontmatter:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

## Complete Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Tools subagent can use. Inherits all if omitted |
| `disallowedTools` | No | Tools to deny from inherited/specified list |
| `model` | No | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` (default) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Maximum agentic turns before stopping |
| `skills` | No | Skills to preload into subagent's context |
| `mcpServers` | No | MCP servers available to this subagent |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local` |
| `background` | No | `true` to always run as background task (default: `false`) |
| `isolation` | No | `worktree` for isolated git worktree copy |

## Available Tools

Subagents can use any Claude Code internal tools:
- `Read`, `Write`, `Edit` — file operations
- `Bash` — shell commands
- `Grep`, `Glob` — search
- `Agent` — spawn other subagents (main thread only)
- `WebFetch`, `WebSearch` — web access
- MCP tools

## Persistent Memory

```yaml
---
name: code-reviewer
memory: project
---
```

| Scope | Location | Use when |
|-------|----------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | Learnings across all projects |
| `project` | `.claude/agent-memory/<name>/` | Project-specific, shareable via VCS |
| `local` | `.claude/agent-memory-local/<name>/` | Project-specific, not in VCS |

When enabled:
- System prompt includes read/write instructions for memory directory
- First 200 lines of `MEMORY.md` included in context
- Read, Write, Edit tools auto-enabled

## Background vs Foreground

- **Foreground**: blocks main conversation; permission prompts pass through
- **Background**: runs concurrently; permissions pre-approved at launch; auto-denies unapproved

Set `background: true` in frontmatter, or ask Claude to "run this in the background", or press **Ctrl+B**.

## MCP Servers in Subagents

```yaml
---
name: browser-tester
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github   # references already-configured server
---
```

## Hooks in Subagents

```yaml
---
name: db-reader
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Supported hook events: `PreToolUse`, `PostToolUse`, `Stop` (converted to `SubagentStop`).

## Patterns

### Isolate High-Volume Operations
```
Use a subagent to run the test suite and report only failing tests
```

### Parallel Research
```
Research authentication, database, and API modules in parallel using separate subagents
```

### Chain Subagents
```
Use code-reviewer to find issues, then optimizer to fix them
```

### Resume Subagents
Each invocation creates fresh context. To continue existing work, ask Claude to resume — it uses `SendMessage` with the agent's ID.

## CLI-Defined Subagents

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

## Subagents Cannot Spawn Other Subagents

This is a hard constraint. If nested delegation is needed, use Skills or chain subagents from the main conversation.
