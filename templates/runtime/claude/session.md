## How to start a session

1. Read `process_log/pipeline_state.json`
   - If `status` is `"not_started"` and `"seeded"` is `true`: run data inventory (below), set to `"running"`, then follow the **Seeded idea mode** entry sequence (see above)
   - If `status` is `"not_started"`: run data inventory (below), set to `"running"`, begin Stage 0
   - If `status` is `"running"`: read `current_stage` and continue from there
   - If `status` is `"complete"`: report that the pipeline is done
3. No human confirmation needed — just run

### Data inventory (runs once at pipeline start)

Before Stage 0, check what data sources are available. This prevents bad assumptions from cascading through the entire pipeline.

1. Read `.env` and list `{{SKILL_DIR}}/` — check which data skills are installed and which have valid credentials (not placeholders). Ken French and Chen-Zimmerman need no auth.
2. Write results to `output/data_inventory.md` — table of sources, status (✓/✗), what each provides, and implications for research design.
3. If `code/utils/start_services.sh` exists, run it to start persistent data connections.
4. Commit: `pipeline: data inventory complete`

**CRITICAL:** All downstream agents must read `output/data_inventory.md` when making decisions about empirical feasibility. The idea-generator and idea-reviewer must know what data is available so they design ideas that USE available data, not work around imagined limitations. Never assume a data source is unavailable without checking the inventory.

### Agent launch and monitoring

Subagents can hang indefinitely — there are no built-in timeouts. To prevent silent stalls:

1. **Launch web-dependent agents in the background.** Agents that use WebSearch or WebFetch (`literature-scout`, `novelty-checker`) should be launched with `run_in_background: true`. Continue with any independent work while they run.

2. **Monitor every 5 minutes.** After launching a background agent, check its output file after 5 minutes. If the file is empty or hasn't grown since your last check, check a couple more times every 5 minutes to see if it's hanging. Re-launch it with the same prompt.
