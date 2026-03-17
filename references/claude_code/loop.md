# Claude Code /loop Feature

**Source**: https://code.claude.com/docs/en/skills.md

## Overview

The `/loop` skill schedules recurring prompts or commands at specified intervals. Tasks are session-scoped and run in the background. Ideal for polling deployments, monitoring builds, checking PR status, or reminders.

**Minimum requirement:** Claude Code v2.1.72+

## Basic Syntax

```bash
/loop [interval] [prompt or command]
```

Examples:
```bash
/loop 5m check if the deployment finished and tell me what happened
/loop check the build every 2 hours
/loop check the build                # defaults to 10 minutes
/loop 20m /review-pr 1234            # loop over a skill
```

## Interval Syntax

**As leading token:** `/loop 30m check the build`
**As trailing clause:** `/loop check the build every 2 hours`
**Default (10 min):** `/loop check the build`

| Unit | Syntax | Examples |
|------|--------|----------|
| Seconds | `s` | `30s`, `45s` |
| Minutes | `m` | `5m`, `30m` |
| Hours | `h` | `1h`, `2h` |
| Days | `d` | `1d`, `7d` |

Seconds are rounded up to nearest minute (cron granularity).

## One-Time Reminders

```bash
remind me at 3pm to push the release branch
in 45 minutes, check whether the integration tests passed
```

## Managing Tasks

```bash
what scheduled tasks do I have?
cancel the deploy check job
```

### Underlying Tools

| Tool | Purpose |
|------|---------|
| `CronCreate` | Schedule new task with cron expression |
| `CronList` | List all scheduled tasks |
| `CronDelete` | Cancel a task by ID |

Max 50 scheduled tasks per session.

## Cron Expression Reference

5-field format: `minute hour day-of-month month day-of-week`

| Expression | Meaning |
|-----------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `0 9 * * *` | Every day at 9am |
| `0 9 * * 1-5` | Weekdays at 9am |

All times in **local timezone**.

## Execution Model

- Scheduler checks every second, enqueues at low priority
- Fires **between your turns**, not during Claude's response
- If Claude is busy, waits until current turn ends
- **3-day expiry** on recurring tasks (prevents forgotten loops)

## Limitations

- **Session-scoped**: closing terminal cancels all tasks
- **No catch-up**: missed intervals fire once when idle
- **No persistence**: restarting clears all tasks

## Disable

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```
