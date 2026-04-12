# Stage 7: Style Check

**Agent:** `style`

1. Launch style agent on the paper. It edits mechanical violations directly in `paper/sections/*.tex` and writes flagged judgment calls to `paper/style_report.md`.
2. Commit: `pipeline: stage 7 — mechanical style edits applied`
3. Read `paper/style_report.md`. For each flagged item, decide whether to act — edit the section file if the fix is clear, leave it if the original reads better. Commit any follow-up edits: `paper: style flags resolved`
4. Update `process_log/pipeline_state.json` with `"status": "complete"`. Final commit: `pipeline: COMPLETE — paper ready for submission`
