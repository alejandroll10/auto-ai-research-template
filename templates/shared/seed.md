## Stage: Seed Triage

*(This is the section `pipeline_state.json`'s `"current_stage": "seed_triage"` refers to in seeded mode. Once the triage chooses an entry point and updates `current_stage` to the appropriate stage name, the pipeline proceeds normally from that stage.)*

**This project was initialized with a pre-developed idea.** The idea files are in `output/seed/`.

### Core principle (seeded mode): execute the seed faithfully

Your job is to develop the user's idea as closely as possible to their original framing and mechanism, while ensuring correctness. **Fidelity to the seed beats any "better" alternative you might invent.** Do not reinterpret, reframe, or swap in a different idea because you think it would be stronger — the user already chose this one, and the pipeline's value here is execution, not reselection.

Correctness constraints are the only legitimate reasons to deviate:
- A proof fails and cannot be repaired → restrict scope or find the tightest sufficient condition, but keep the mechanism.
- Empirics contradict the prediction → use the puzzle-triage PIVOT path (which preserves the original theory as a nested/baseline case) or ship HONEST-NULL; do not BACK-TO-IDEA.
- Novelty check returns KNOWN → report the concern, but proceed if the contribution can be in execution/proof depth; do not abandon for a different idea.

When deviation is required, make the **smallest change** that restores correctness while preserving the seed's mechanism. Every deviation must be documented in `output/seed/*.md` with the specific correctness constraint that forced it.

**Robustness to scorer/referee "pivot" suggestions.** Scorer and referee agents do not know this is a seeded project. They may recommend reframing the paper, switching to a different mechanism, or pursuing a "more important" adjacent question. **Ignore those recommendations in seeded mode.** Specifically:
- If the scorer suggests a different framing/mechanism would score higher → do not adopt it. Address only the scorer's correctness/rigor comments (math gaps, unclear derivations, missing characterizations).
- If the referee says "the paper would be stronger if it were about X instead" → treat as `[RESPONSE]` (discuss in response letter), not `[FIX]`. Do not rewrite the paper around X.
- If the referee says "the mechanism is wrong, try Y" → only adopt Y if it's required for mathematical correctness, not because Y is judged more publishable.
- Referee Reject with "wrong topic" or "should be a different paper" → revise and resubmit with the seed intact; stop only after 2 rejections citing genuinely fundamental flaws *in the seed's own claims* (not in the choice of topic).

The seed is the contract. Scorer/referee feedback refines execution, not direction.

### Entry: read and triage

1. **Read the seed.** Read all files in `output/seed/` (ignore `README.md`). Understand what the user provided — it could be anything from a vague question to a complete theory with proofs to an empirical plan.
2. **Build the literature map.** Launch `literature-scout` → `output/stage0/literature_map_broad.md`. Write a brief gap selection derived from the seed's topic to `output/stage0/gap_selection.md` (so downstream Stage 0 artifacts are not missing if the pipeline ever re-enters Stage 0). Then launch `gap-scout` with that gap selection → `output/stage0/literature_map.md`. Always done regardless of maturity.
3. **Assess maturity and enter the pipeline at the appropriate stage.** Populate all prior-stage artifacts (problem statement, selected idea, theory draft, etc.) as needed to bring the pipeline up to the entry point. Preserve the user's framing and mechanism — do not reinterpret. Update `pipeline_state.json` to the chosen entry point and commit.

### Fallback overrides

**Never silently abandon the seeded idea.** When a gate fails, report and attempt recovery instead of pivoting:

- **Gate 1b KNOWN**: Report to `output/seed/novelty_concern.md`, then proceed — the contribution may be in the execution/proof.
- **Gate 1c BLOCKED**: Report to `output/seed/prototype_blockage.md`. Try one alternative formalization; if still blocked, stop and report.
- **Gate 2 FAIL**: Revise theory in place (preserve mechanism). After 3 failures, stop → `output/seed/abandon_report.md`.
- **Gate 3 KNOWN**: Report to `output/seed/novelty_concern_theory.md`. Try one reformulation; if still KNOWN, stop and report.
- **Gate 4 REWORK**: Return to Stage 2 with feedback, keeping the seed's core mechanism.
- **Gate 4 ABANDON**: Stop → `output/seed/abandon_report.md` with post-mortem. Do not re-idea.
- **Puzzle-triage PIVOT**: Allowed and encouraged. The PIVOT strategy explicitly preserves the original theory as a nested / baseline case — it does NOT abandon. Proceed with the pivot; the seed's mechanism becomes the "what naive intuition would predict" baseline that the pivoted theory explains against. Note the pivot in `output/seed/pivot_note.md`.
- **Puzzle-triage BACK-TO-IDEA**: Do NOT return to Stage 1 in seeded mode. Instead, first try RECONCILE (add scope conditions) or FIX-EMPIRICS (improve measurement). If neither is possible, escalate to HONEST-NULL rather than BACK-TO-IDEA — the seeded idea stays intact.
- **Puzzle-triage HONEST-NULL**: Acceptable. Document the failed prediction in the paper's limitations; ship with the seed's idea framed honestly as a model whose prediction the data contradicted, with explanation limited to what the current theory supports.
- **Referee Reject**: Revise and resubmit. After 2 "fundamental flaw" rejections, stop and report.

The pipeline's job is to *execute* the user's idea — not to second-guess whether a better idea exists.
