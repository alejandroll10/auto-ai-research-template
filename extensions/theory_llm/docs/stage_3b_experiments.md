# Stage 3b: LLM Experiments

1. **Experiment plan.** Launch `experiment-designer` with instruction: "Write an experiment plan only — do not execute yet." The agent identifies predictions testable via LLM calls and writes `output/stage3b/experiment_plan.md` with: hypotheses, experimental design, controls, sample sizes, and expected outcomes.
2. **Review the plan.** Check: does it test the right predictions? Are controls adequate? Is sample size sufficient? If not, provide feedback.
3. **Execute.** Launch `experiment-designer` with the approved plan. The agent runs experiments using `llm_client.py`. Saves results to `output/stage3b/experiment_results.md` (canonical summary file — needed by puzzle-triager).
4. **Stage 3b (review):** Launch `experiment-reviewer` on the design, code, raw results, and analysis. Evaluates methodology (internal validity, controls, sample size, statistical tests) and interpretation.

| Decision | Action |
|----------|--------|
| **ACCEPT** | Proceed to **puzzle-triage entry check** (next step). |
| **REVISE** | Re-run specific experiments or re-analyze. Max 2 revision rounds. |
| **REDESIGN** | Fundamental methodology problem. Redesign and re-run. Max 1 redesign. |

5. Commit: `artifact: experiments — {ACCEPT/REVISE/REDESIGN}`

## Puzzle-triage entry check (mandatory after experiment-reviewer ACCEPT)

Before proceeding to Stage 4, you must check whether the experiment results contradict any prediction in `output/stage3/implications.md`.

1. Read `output/stage3/implications.md` and identify which implications were tested experimentally.
2. Read `output/stage3b/experiment_results.md`.
3. For each tested implication: did the experiment contradict it (effect in the wrong direction, magnitude outside predicted range, condition that should hold but failed)?
4. Write `output/stage3b/contradiction_check.md` with one of:
   - **NONE** — experiments confirm or are silent on every tested implication. Proceed to Stage 4.
   - **CONTRADICTIONS FOUND** — list the contradicted implications and what the experiments show. **Proceed to puzzle triage** (`docs/stage_puzzle_triage.md`), not Stage 4.
5. Commit: `artifact: contradiction check — {NONE/CONTRADICTIONS FOUND}`

This step is mandatory and may not be skipped.

## Re-fire on theory revision

Stage 3b is not one-shot. When the theory revises after the first 3b pass — Gate 3 INCREMENTAL rework, Gate 4 REVISE→Stage 2, Stage 6 Major Revision triggering theory-generator work, or any substantive content change — the original `experiment_results.md` becomes stale relative to the current theory. The experiment-designer must re-run on the revised content before Gate 4 can advance again.

**Trigger.** Any of:
- `theory_version` advances and `stage3b_theory_version < theory_version`.
- `implications.md` is overwritten (Gate 3 INCREMENTAL rework, PIVOT, or any path that re-runs Stage 3) and the new file contains NOVEL or PUZZLE-CANDIDATE implications not present in the prior version.
- A referee identifies an experimental gap that wasn't addressed in the first 3b pass (e.g., "this prediction was deferred" or "the manipulation doesn't isolate X").
- Stage 6 Reject verdict triggers a deepen directive (see `docs/stage_6.md` Reject row): the deepen directive's experimental requirements become the focus of the re-fire.

**Procedure.**
1. Launch `experiment-designer` with: the revised theory, the current `implications.md`, the prior `experiment_results.md` (so the agent knows what's already been tested), and a focused instruction listing the specific new content to test.
2. Save targeted re-runs to `output/stage3b/experiment_results_vN.md` where N is the current `theory_version`. **Do not overwrite the original `experiment_results.md`** — combined coverage across files must span the version that will be written into the paper.
3. Run `experiment-reviewer` on the new analysis (same review loop as the first pass; same caps on REVISE/REDESIGN rounds).
4. **Re-run the puzzle-triage entry check** (above) on the combined evidence — a new contradiction triggers puzzle-triage as it would on the first pass.
5. On reviewer ACCEPT and contradiction-check complete, set `pipeline_state.json:stage3b_theory_version = theory_version`.

**Gate 4 enforcement.** Before any Gate 4 advance, the orchestrator must verify `stage3b_theory_version == theory_version`. Stale experiments are a hard block, parallel to the `stage2b_theory_version` rule for theory-explorer and the `stage3a_theory_version` rule for empirical analysis.

**Cap.** No hard cap on re-fires per problem — the constraint is the never-abandon rule plus the existing 10-round referee cap and the 8-evaluation hard ceiling. But re-fires that do not surface new evidence (reviewer ACCEPT with no new findings, no contradiction-check change) count toward the plateau-detection logic in Gate 4 (see `docs/stage_4.md`).
