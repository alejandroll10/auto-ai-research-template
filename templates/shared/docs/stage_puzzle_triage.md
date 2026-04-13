# Stage: Puzzle Triage

**Agent:** `puzzle-triager`

**Fires only when:** an empirical analysis (`output/stage3b/empirical_analysis.md`) or experimental result (`output/stage3b_experiments/`) **contradicts** at least one prediction in `output/stage3/implications.md`. If results confirm the theory or are silent on its predictions, **skip this stage** — proceed directly to Stage 4.

This stage operationalizes the principle that surprises are discoveries: when a well-grounded theory predicts X and well-measured data shows not-X, the contradiction itself is often the most valuable contribution. The triager decides whether to pivot the paper around that puzzle, fix the empirics, restrict the theory's scope, abandon the idea, or ship an honest null.

## Entry check

Before launching the triager, verify the contradiction is real:

1. Read `output/stage3/implications.md` and identify which implications were tested.
2. Read every result file that exists:
   - `output/stage3b/empirical_analysis.md` (if `--ext empirical`)
   - `output/stage3b_experiments/experiment_results.md` (if `--ext theory_llm`)
   Both may exist when both extensions are enabled — use all of them.
3. For each tested implication: did the data contradict it (sign reversal, magnitude mismatch outside predicted range)?
4. If no contradiction across any result source: **skip this stage**, proceed to Stage 4.
5. If at least one tested implication was contradicted by at least one result source: launch the puzzle-triager.

## Procedure

1. Read `pipeline_state.json` for current `pivot_round` (default 0).
2. Launch `puzzle-triager` with: theory draft, `implications.md`, **every result file that showed a contradiction** (both empirical and experimental, if both apply), literature map, math audit results, pipeline state. If empirical and experimental results contradict each other (e.g., empirics confirm, experiments contradict), note the disagreement in the input — the triager should flag this in its rationale and typically recommend FIX-EMPIRICS rather than PIVOT until the measurement conflict is resolved.
3. Triager saves to `output/puzzle_triage/triage_pN.md` where N = `pivot_round + 1`.
4. Commit: `artifact: puzzle triage round {N+1} — {VERDICT}`.

## Acting on the verdict

| Verdict | Pipeline action |
|---------|----------------|
| **NORMAL-PROCEED** | (Triager flags an inconsistency — empirics did not actually contradict.) Proceed to Stage 4 and review the entry check. |
| **FIX-EMPIRICS** | Re-launch `empiricist` with the triager's notes on what to improve. Re-enter at `empirical_analysis`. Theory unchanged. Do not increment `pivot_round`. |
| **RECONCILE** | Launch `theory-generator` in `mutate` mode with instruction: "Add an explicit scope condition stating where the result holds. Empirical results show data sits outside that scope." Re-run Gate 2 (math audit) on the revised theory. Do not increment `pivot_round`. |
| **BACK-TO-IDEA** | Return to Stage 1 with the triager report as input to the idea-reviewer. Increment `problem_attempt`. Skip if Stage 5 has begun (paper exists) — use HONEST-NULL instead. |
| **PIVOT** | Run the **pivot sequence** documented below. |
| **HONEST-NULL** | Set `pivot_resolved: false` in pipeline state (see State updates). Then two paths: (a) if Stage 5 has begun, document the failed prediction in the limitations section and proceed; (b) if no paper exists yet, return to Stage 0 with the failure notes. Do not pivot a third time. |

## Pivot sequence (when verdict is PIVOT)

A pivot is a full theory revision. The new theory needs new implications, lit-checks, and validation — not just empirical re-run. Follow this sequence end-to-end:

1. **Update state.** Increment `pivot_round`. Append to `pivot_history`. Set `pivot_resolved: null` (will be set true/false after the pivoted theory's empirical run).
2. **Pivoted theory.** Launch `theory-generator` in `pivot` strategy mode with: original theory, contradicted finding, triager report, literature map. The agent rebuilds around explaining the contradiction; original theory becomes a nested case.
3. **Re-run Gate 2.** Math audit (structured + freeform) on the pivoted theory. Iterate as in Stage 2.
4. **Re-run Gate 3.** Novelty check on the pivoted theory. KNOWN/INCREMENTAL → escalate.
5. **Re-run Stage 3a.** Theory exploration on the pivoted theory.
6. **Re-run Stage 3 (implications) IN FULL.** Derive new implications from the pivoted theory and gap-scout each one for the NOVEL/PUZZLE-CANDIDATE/SUPPORTED/DEAD tag. **Do not reuse the previous theory's implications.md** — overwrite it. Downstream agents (paper-writer, scorer, empiricist) read the current `implications.md` and assume it describes the current theory.
7. **Re-run empirical_analysis (and experiments, if applicable)** against the new predictions. Run the puzzle-triage entry check again at the end.
8. **Set both `pivot_resolved` (top-level) AND `pivot_history[N].resolved` for this round's entry.** Set the same value to both:
   - `true` if the pivoted theory's empirics confirm its (new) predictions — the puzzle is resolved.
   - `false` if the pivoted theory's empirics also contradict, AND the triager (re-fired) returns HONEST-NULL or another non-PIVOT verdict.
   - If the triager returns PIVOT again, leave both fields `null` for this round and re-enter the pivot sequence (this is the second pivot; cap is 2).
9. **Proceed to Stage 4** once `pivot_resolved` is set (true or false).

## State updates

When PIVOT verdict fires, update `pipeline_state.json`:

```json
{
  "pivot_round": <previous + 1>,
  "pivot_resolved": null,    // set true/false after pivoted theory's empirical run
  "pivot_history": [
    ...,
    {
      "round": <new round>,
      "contradiction": "<one sentence>",
      "prior_source": "<which paper / data source set the prior>",
      "new_mechanism_hint": "<what the triager suggested>",
      "resolved": null         // set true/false at end of pivot sequence
    }
  ]
}
```

**Two fields — don't confuse them:**

- **Top-level `pivot_resolved`** — overall current state. Reflects the most recent pivot's outcome. This is the **single signal** downstream agents (paper-writer, scorer) read. Values:
  - `null` — no pivot has occurred yet, or the most recent pivot is still in progress
  - `true` — the latest pivoted theory's empirics confirmed its predictions; the puzzle is resolved
  - `false` — the latest pivoted theory also contradicted, ended in HONEST-NULL or escalated; the puzzle was not solved
- **Per-round `pivot_history[N].resolved`** — the resolution of pivot round N specifically. Useful for auditing history across multiple pivots. Set to the same `true`/`false` value at the same time as `pivot_resolved`; the top-level field mirrors the latest entry.

Paper-writer and scorer should gate their puzzle-framing logic on **top-level `pivot_resolved == true`**, NOT on `pivot_round > 0`. A failed pivot is not a resolved puzzle.

Append to `history` array as usual:
```json
{ "timestamp": "...", "event": "puzzle-pivot round N — <new mechanism hint>" }
```

## Hard cap

`pivot_round` ≥ 2 → triager is forbidden from recommending PIVOT. Two pivots without resolution means the problem is not tractable on this approach. Default to HONEST-NULL.

## Downstream effects

When `pivot_round > 0`:
- **Paper-writer**: frames the introduction around the puzzle, not the original prediction. The original theory becomes a baseline / null; the new mechanism is the contribution.
- **Scorer**: Surprise dimension floor is 70 (resolved puzzle is by construction surprising). Importance benefits if the puzzle was field-visible.
- **Referee simulation**: should specifically probe whether the resolving mechanism is principled (falls out of economics) vs. ad-hoc (curve-fit to the data). This is the main failure mode of pivot papers.
