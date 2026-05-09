# Split-Guard Audit — Round 4

## Verdict

PASS — ready to close. All three round-3 LOW issues are confirmed fixed. The canonical (c) wording is now a single merged sentence that eliminates both the motivated re-framing gap (Issue 1) and the implied-permission problem from two partially-overlapping sentences (Issue 2). Cross-file alignment is achieved (Issue 3): puzzle-triager.md and stage_puzzle_triage.md now both carry the full canonical phrasing. The benchmark walkthrough produces no over-rejections or under-rejections. No new substantive issues were found.

---

## Round-3 fix verification

**Issue 1 (motivated re-framing — "applicable beyond this paper's own design" loophole).** Fixed. The prior two-sentence form left a gap where a "general placebo battery" could argue it was not tied to "this paper's own design." The new merged sentence closes this by naming the exclusion unconditionally: "not a simulation rejection rate, placebo battery, or debugging insight even framed as a general claim." The phrase "even framed as a general claim" is exactly the categorical closure that round 3 called for. A scorer cannot grant (c) to a placebo battery by accepting the author's framing that it is general; the clause explicitly addresses and rejects that move.

**Issue 2 (redundancy / implied-permission gap).** Fixed. The two sentences ("applicable beyond this paper's specific analysis or dataset" + "A simulation-based rejection rate or placebo battery on this paper's own design does not qualify") have been merged into one. The merged sentence states the positive requirement (stated theorem with proof, applicable beyond this paper's specific analysis or dataset), gives positive exemplars in the parenthetical, and ends with the negative exemplars (simulation rejection rate, placebo battery, debugging insight even framed as a general claim). No second sentence with "own design" remains to imply that a "general design" placebo battery passes. The redundancy and the implied-permission gap are both gone.

**Issue 3 (cross-file divergence).** Fixed. `puzzle-triager.md` line 83 and `stage_puzzle_triage.md` line 9 both now read "a stated theorem with proof, applicable beyond this paper's specific analysis or dataset (e.g., a new estimator's consistency, an identification theorem)" — matching the structure of the canonical scorer-core.md universal block. The old phrasing "with proved properties (e.g., a new estimator or identification theorem) — not an empirical critique of this paper's own design" is gone from both files. The two files' (c) clauses are naturally shorter than scorer-core.md's (they omit the "diagnostic's stated size/power" exemplar and the full negative list), but the core requirement — stated theorem with proof, applicable beyond this paper's specific analysis or dataset — is now verbatim consistent.

---

## Final benchmark walkthrough

| Paper / Contribution | Guard verdict | Determining phrase |
|---|---|---|
| Goodman-Bacon 2021 — TWFE decomposition theorem | PASS (c) | "stated theorem with proof, applicable beyond this paper's specific analysis or dataset" — algebraic decomposition is general and proved |
| Sun-Abraham 2021 — IW estimator with bias theorem | PASS (c) | Same; convexity / consistency result is a stated theorem with proof, not tied to any single dataset |
| Borusyak-Jaravel-Spiess 2024 — imputation estimator with asymptotic theory | PASS (c) | Asymptotic theory is a stated theorem with proof (efficiency, consistency), general across DiD designs |
| Roth 2022 — pre-trends power propositions | PASS (c) | Propositions on size distortion / power are stated theorems with proof, applicable to any pre-trend test |
| Calonico-Cattaneo-Titiunik 2014 — robust RD CIs with stated coverage | PASS (c) | "diagnostic's stated size/power" exemplar is live; MSE-optimal bandwidth result is a stated theorem with proof |
| Newey-West 1987 — HAC SE consistency | PASS (c) | "new estimator's consistency" exemplar is live; HAC consistency result is the canonical instance |
| Hansen 1982 — GMM consistency | PASS (c) | GMM consistency and asymptotic normality are stated theorems with proof, general across moment-condition models |
| Victor-1 contribution (1): EDGAR pipeline, F1=0.44 | FAIL guard fires | "dataset/pipeline release where the release itself is the claimed contribution" — trigger list; no (c) exit because F1 is not a stated theorem with proof |
| Victor-1 contribution (2): 14/16 placebos fail | FAIL guard fires | "not a simulation rejection rate, placebo battery, or debugging insight even framed as a general claim" — categorical exclusion regardless of framing |
| Hypothetical: placebo battery framed as "general claim about all event-clustered designs" without theorem | FAIL guard fires | "even framed as a general claim" — this is precisely the re-framing the clause was written to deny; no theorem, no (c) |

No over-rejections (all seven canonical methods papers pass). No under-rejections (all three negative cases correctly hit the guard). The benchmark is clean.

---

## Remaining issues

None — ready to close.

---

## Em-dash rendering note (Section D)

The three "—" em-dashes in the canonical (c) appear in `.md` agent body files that are read at runtime by language models, not compiled as LaTeX source. They do not pass through a LaTeX typesetter as raw characters; the paper-writer agent receives natural-language instructions and writes its own LaTeX. No typesetting issue arises from em-dashes in agent prompt bodies. If scorer-core.md were ever included verbatim in a LaTeX document, `—` is not a valid LaTeX construct and would require `---` or `\textemdash`, but that path does not exist in this pipeline.
