## How to start a session

1. If `code/utils/start_services.sh` exists, run it: `bash code/utils/start_services.sh`. This starts persistent data connections for the session.
2. Read `process_log/pipeline_state.json`
   - If `status` is `"not_started"` and `"seeded"` is `true`: run data inventory (below), set to `"running"`, then follow the **Seeded idea mode** entry sequence (see above)
   - If `status` is `"not_started"`: run data inventory (below), set to `"running"`, begin Stage 0
   - If `status` is `"running"`: read `current_stage` and continue from there
   - If `status` is `"complete"`: report that the pipeline is done
3. No human confirmation needed — just run

### Data inventory (runs once at pipeline start)

Before Stage 0, check what data sources are available. This prevents bad assumptions from cascading through the entire pipeline.

1. Read `.env` — check which credentials are present (non-placeholder values)
2. List `{{SKILL_DIR}}/` — check which data skills are installed
3. For each skill with authentication, verify credentials exist in `.env`:
   - FRED: `FRED_API_KEY` present and not `your-key-here`
   - WRDS: `WRDS_USER` and `WRDS_PASS` present and not placeholders
   - EDGAR: `SEC_EDGAR_NAME` and `SEC_EDGAR_EMAIL` present and not placeholders
   - Ken French: no auth needed (always available)
   - Chen-Zimmerman: no auth needed (always available)
4. Write results to `output/data_inventory.md` — table of sources, status (✓/✗), and what each provides. Include implications for research design.
5. Start data services:
   ```bash
   bash code/utils/start_services.sh
   ```
   This starts the persistent WRDS server (if credentials configured) — Duo 2FA fires once, then all queries go through instantly for the rest of the session.
6. Commit: `pipeline: data inventory complete`

**CRITICAL:** All downstream agents must read `output/data_inventory.md` when making decisions about empirical feasibility. The idea-generator and idea-reviewer must know what data is available so they design ideas that USE available data, not work around imagined limitations. Never assume a data source is unavailable without checking the inventory.

### Agent launch and monitoring

Subagents can hang indefinitely — there are no built-in timeouts. To prevent silent stalls:

1. **Launch web-dependent agents in the background.** Agents that use WebSearch or WebFetch (`literature-scout`, `novelty-checker`) should be launched with `run_in_background: true`. Continue with any independent work while they run.

2. **Monitor every 5 minutes.** After launching a background agent, check its output file after 5 minutes. If the file is empty or hasn't grown since your last check, the agent has likely hung. Re-launch it with the same prompt.

3. **Prefer incremental-writing agents.** Agents like `literature-scout` are designed to write after every search round. Use the output file as a heartbeat — if content stops appearing, the agent is stuck.

4. **Non-web agents can run in foreground.** Agents that don't use WebSearch (`math-auditor`, `theory-generator`, `scorer`, `self-attacker`, `paper-writer`) rarely hang. Launch these in the foreground as normal.

5. **Parallel agent launches.** When the pipeline calls for multiple independent agents (e.g., structured math audit + free-form math audit), launch them in parallel as background agents. Check both when done. Do not serialize independent work.
