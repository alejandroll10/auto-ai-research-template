
## Background jobs

Never launch a long-running job with `nohup` or a detached `&` — it escapes harness tracking and stall detection. Use a harness-tracked background job instead (the Bash tool's `run_in_background`) so the job stays monitored and its output remains retrievable.
