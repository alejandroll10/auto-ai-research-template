# Stage 8: Bibliography Verification

**Agent:** `bib-verifier`

Sanity-check every citation in the paper before marking the pipeline complete. Catches hallucinated, mistitled, or wrong-year references that may have slipped past the scouts, novelty-checker, paper-writer, or referee revisions.

1. Launch `bib-verifier`. It runs `code/utils/bib_verify/verify_bib.sh` (OpenAlex lookup), then runs a WebSearch fallback on every MISS to distinguish SSRN-only working papers from fabrications. It writes `output/bib_verification.md` and returns a triage summary (counts + fix list).
2. Commit: `pipeline: stage 8 — bibliography verified`
3. **If `LIKELY FABRICATIONS > 0` or `CITE FIXES NEEDED > 0`:** increment `bib_verify_round` in `pipeline_state.json`, then re-launch `paper-writer` with the fix list. Have it remove fabricated cites (or replace with verified equivalents from the literature map) and apply the title/year/venue corrections. Commit: `paper: bibliography fixes applied`. Re-launch `bib-verifier` to confirm. Stop when `bib_verify_round >= 2` even if issues remain — drop unresolvable cites rather than loop indefinitely.
4. When the report shows zero `LIKELY FABRICATIONS` and zero `CITE FIXES NEEDED`, update `process_log/pipeline_state.json` with `"status": "complete"`. Final commit: `pipeline: COMPLETE — paper ready for submission`

## Notes

- This stage replaces the `"status": "complete"` step previously at the end of Stage 7. Stage 7 now ends after style edits are committed; the pipeline is marked complete only after Stage 8 passes.
- A MISS that survives the WebSearch fallback is treated as a fabrication — do not rationalize it as "probably real but uncovered." The whole point of this check is to catch hallucinations.
- For seeded papers (`--seed`) where the user supplies references, this stage still runs — the user-provided references get verified the same way.
