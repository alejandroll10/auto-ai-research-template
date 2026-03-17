# Claude Code Sandbox & Permissions

**Sources**:
- https://code.claude.com/docs/en/sandboxing.md
- https://code.claude.com/docs/en/permissions.md
- https://code.claude.com/docs/en/security.md
- https://code.claude.com/docs/en/settings.md

## Overview

Two complementary security layers:

| Layer | Controls | Applies To | Enforcement |
|-------|----------|-----------|-------------|
| **Permissions** | Which tools Claude can use | All tools | User prompt allow/deny |
| **Sandboxing** | What Bash commands can access | **Bash + child processes only** | OS-level (bubblewrap on Linux) |

### Critical distinction: Sandbox does NOT affect WebFetch/WebSearch

The sandbox only restricts **Bash commands and their child processes**. Claude's built-in tools like `WebFetch`, `WebSearch`, `Read`, `Edit`, and `Write` operate **outside the sandbox** and are controlled only by the permissions layer.

This means:
- **No network sandbox needed** for web browsing — `WebFetch` and `WebSearch` always work
- **`socat` is only needed** if you want to sandbox network access from Bash commands (e.g., `curl`, `wget`, `pip install`)
- **Filesystem sandbox** is the main protection: locks Bash to writing only inside your project folder
- You can safely use `--dangerously-skip-permissions` on your host machine if the filesystem sandbox prevents Bash from touching sensitive files

## Linux/Ubuntu Setup

**Filesystem sandbox only** (no network sandbox for Bash):
```bash
sudo apt-get update
sudo apt-get install bubblewrap
```

**Full sandbox** (filesystem + network restriction on Bash commands):
```bash
sudo apt-get install bubblewrap socat
```

| Platform | Technology | Status |
|----------|-----------|--------|
| macOS | Seatbelt | Works out of the box |
| Linux | bubblewrap | Requires `bubblewrap` (+ `socat` for network sandbox) |
| WSL2 | bubblewrap | Requires installation |
| WSL1 | N/A | Not supported |

## 5 Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Standard: prompts for permission on first use |
| `acceptEdits` | Auto-accept file edits; prompts for bash |
| `plan` | Read-only analysis, no modifications |
| `dontAsk` | Auto-deny unless pre-approved via allow rules |
| `bypassPermissions` | Skip ALL permission prompts |

Set via CLI: `claude --permission-mode plan`
Set via settings: `"defaultMode": "acceptEdits"`

## --dangerously-skip-permissions

```bash
claude --dangerously-skip-permissions
```

Skips ALL permission prompts. Auto-approves everything.

### Two safe approaches:

**Option A: Filesystem sandbox on host (simpler, keeps web access)**

With the sandbox restricting Bash to your project folder, you can run on the host. WebFetch/WebSearch still work for literature search, paper fetching, etc.

```bash
# Just need bubblewrap installed (no socat, no Docker)
claude --dangerously-skip-permissions
```

With this settings.json:
```json
{
  "sandbox": {
    "enabled": true,
    "mode": "auto-allow",
    "filesystem": {
      "allowWrite": ["./"],
      "denyWrite": ["~/.ssh", "~/.aws", "~/.claude", "//etc", "//root"],
      "denyRead": ["~/.ssh", "~/.aws"]
    }
  }
}
```

**Option B: Docker container (maximum isolation, no web unless configured)**

```bash
docker run --rm --network none \
  -v "$(pwd):/work" \
  my-claude-sandbox \
  --dangerously-skip-permissions
```

### Risks without ANY isolation:
- File modification/deletion without confirmation
- Irreversible changes
- Data exfiltration via Bash (SSH keys, credentials)
- Prompt injection attacks execute without approval

## Sandbox Configuration

### Enable
```bash
/sandbox
```

### Full settings.json config

```json
{
  "sandbox": {
    "enabled": true,
    "mode": "auto-allow",
    "filesystem": {
      "allowWrite": ["./", "//tmp/build"],
      "denyWrite": ["~/.ssh", "~/.aws", "//etc"],
      "allowRead": ["."],
      "denyRead": ["~/secrets"]
    },
    "network": {
      "allowedDomains": ["github.com", "npm.org"],
      "deniedDomains": ["malicious.com"],
      "httpProxyPort": 8080,
      "socksProxyPort": 8081,
      "allowUnixSockets": [],
      "allowLocalBinding": false
    },
    "allowManagedDomainsOnly": false,
    "allowUnsandboxedCommands": true,
    "excludedCommands": ["docker", "watchman"],
    "enableWeakerNestedSandbox": false
  }
}
```

### Path Prefixes

| Prefix | Meaning | Example |
|--------|---------|---------|
| `//` | Absolute from root | `//tmp/build` → `/tmp/build` |
| `~/` | Home directory | `~/.kube` → `$HOME/.kube` |
| `/` | Relative to settings file | `/build` → `$SETTINGS_DIR/build` |
| `./` | Relative path | `./output` |

### Sandbox Modes
- **auto-allow**: Bash commands auto-allowed inside sandbox; unsandboxable commands fall back to permission flow
- **Regular**: All bash commands go through standard permission flow

## Permission Rules

### Syntax: `Tool` or `Tool(specifier)`

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build)",
      "Bash(git *)",
      "Read(./.env)",
      "WebFetch(domain:example.com)",
      "Edit(/src/**/*.ts)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ],
    "ask": [
      "Bash(curl *)"
    ]
  }
}
```

### Evaluation Order: Deny → Ask → Allow
First matching rule wins. Deny always takes precedence.

### Wildcards
- `Bash(npm run *)` — matches commands starting with `npm run `
- `Edit(/src/**/*.ts)` — gitignore-style patterns
- `Bash(git * main)` — multiple wildcards

## Docker-Based Safe Sandbox for Ubuntu

### Dockerfile

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    bubblewrap socat git curl nodejs npm

RUN useradd -m claude
USER claude
WORKDIR /home/claude

ENTRYPOINT ["claude"]
```

### Run with full isolation

```bash
docker build -t claude-safe .

docker run --rm \
  --network none \
  -v /safe/project:/home/claude/project \
  claude-safe --dangerously-skip-permissions
```

### Defense-in-depth: container + sandbox + permissions

```json
{
  "defaultMode": "acceptEdits",
  "sandbox": {
    "enabled": true,
    "mode": "auto-allow",
    "filesystem": {
      "allowWrite": ["./"],
      "denyWrite": ["~/.ssh", "~/.aws", "~/.claude"]
    },
    "network": {
      "allowedDomains": ["github.com", "npm.org"]
    }
  },
  "permissions": {
    "allow": ["Read", "Bash(git *)", "Bash(npm run *)"],
    "deny": ["Bash(rm -rf *)", "Bash(sudo *)"]
  }
}
```

## Settings Precedence (highest to lowest)

1. **Managed settings** (cannot be overridden)
2. **CLI arguments** (`--permission-mode`, `--dangerously-skip-permissions`)
3. **Local project** (`.claude/settings.local.json`)
4. **Shared project** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`)

## Excluded Commands

Some tools are incompatible with sandbox:

```json
{
  "sandbox": {
    "excludedCommands": ["docker", "watchman"]
  }
}
```

These run outside sandbox with normal permission flow.

## Recommended Setup: AI Research Project

For an AI-assisted research project that needs web search, paper fetching, and code execution but should stay safe:

**Prerequisites (Ubuntu):**
```bash
sudo apt-get install bubblewrap
```

**`.claude/settings.json`** (shared with team via git):
```json
{
  "sandbox": {
    "enabled": true,
    "mode": "auto-allow",
    "filesystem": {
      "allowWrite": ["./"],
      "denyWrite": ["~/.ssh", "~/.aws", "~/.claude", "//etc", "//root"],
      "denyRead": ["~/.ssh", "~/.aws"]
    }
  }
}
```

**Run:**
```bash
claude --dangerously-skip-permissions
```

**What this gives you:**
- WebSearch and WebFetch work freely (literature search, paper fetching)
- Bash can only write inside the project folder
- Bash cannot read SSH keys or AWS credentials
- All file edits auto-approved (within project)
- Git works normally (reads ~/.gitconfig, writes inside project)
- Python/R scripts run fine (write output to project folder)

**What it blocks:**
- `rm -rf ~/*` — sandbox prevents writes outside project
- `cat ~/.ssh/id_rsa` — sandbox denies read
- `pip install --user malware` — writes to ~/.local, blocked
- Any Bash command touching system files

## Open Source Sandbox Runtime

```bash
npx @anthropic-ai/sandbox-runtime <command>
```

GitHub: https://github.com/anthropic-experimental/sandbox-runtime
