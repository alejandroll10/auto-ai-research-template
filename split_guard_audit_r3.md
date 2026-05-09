# Split-Guard Audit — Round 3

## Verdict

PASS-WITH-FIXES. Both r2 issues are confirmed fixed, but three minor residual issues were found: one LOW (placebo-as-(c) escape is closed in the universal block but not fully by the exact wording — detailed below), one LOW (redundancy between the two new sentences in the universal block), and one LOW (cross-file (c) wording divergence in puzzle-triager.md and stage_puzzle_triage.md). None are MEDIUM or HIGH. All have a one-line fix direction.

---

## Fix verification (r2 issues A and B)

**Fix A (LOW — placebo-battery (c) escape).** Confirmed fixed and correctly tightened. The new phrase "that is general — applicable beyond this paper's specific analysis or dataset" is appended directly to (c)'s definition. The follow-on sentence "A simulation-based rejection rate or placebo battery on this paper's own design does not qualify as (c); a useful debugging insight is not, by itself, the paper's contribution" provides a concrete worked example of the exclusion. Victor-1's two contributions: the EDGAR F1=0.44 pipeline release is still caught by the trigger list; the placebo rejection-rate simulation fails (c) because it is by definition not "applicable beyond this paper's specific analysis or dataset." Both contributions correctly hit H1/H5 FAIL. Fix is effective.

**Fix B (MEDIUM — empirical-first (c) carve-out ambiguity).** Confirmed fixed. The phrase "Exception (c) applies identically in both blocks: a paper that satisfies (c) above is exempt here too" is explicit and unambiguous. "Above" refers unambiguously to the universal block, which is the only prior block. "Applies identically" means the same (c) — now including the generality requirement from Fix A — is in force; it does not require (c) to be satisfied independently in each block. A scorer reading "applies identically in both blocks" and "a paper that satisfies (c) above is exempt here too" cannot read the blocks as independent filters with an AND-of-two-independent-(c)s. Fix is effective.

---

## New issues

**ISSUE 1 — Severity: LOW — "Applicable beyond this paper" is still arguable for a broad placebo design.**
Location: `templates/agent_bodies/shared/scorer-core.md` line 28.

The wording "applicable beyond this paper's specific analysis or dataset" is intended to exclude single-paper placebos. But a savvy agent could argue: "Our event-study placebo design is a general battery usable by any event-study researcher — it is explicitly not tied to our specific analysis." The follow-on sentence partially closes this: "A simulation-based rejection rate or placebo battery on this paper's own design does not qualify as (c)." However, "on this paper's own design" leaves open "on a design we also propose as general." The two sentences are not fully redundant (see issue 2), but this gap is partially closed by the follow-on sentence only if a scorer reads it as categorically excluding all placebo batteries. The fix is to add "regardless of how the design is framed" or replace "on this paper's own design" with "on any single paper's design, whether framed as specific or general." Alternatively, anchor (c) to requiring a *formal proof of an asymptotic or finite-sample property* (not a simulation statistic), which is what Goodman-Bacon, Sun-Abraham, and Newey-West actually have. The current wording is close but not airtight against a motivated re-framing.

**ISSUE 2 — Severity: LOW — Redundancy between the two new sentences.**
Location: `templates/agent_bodies/shared/scorer-core.md` line 28.

"applicable beyond this paper's specific analysis or dataset" and "A simulation-based rejection rate or placebo battery on this paper's own design does not qualify as (c)" partially overlap. The second sentence is a specific instance of the first. Neither is fully redundant because: the first (generality clause) handles the re-framing attack from issue 1 only partially; the second (placebo-battery exclusion) adds a concrete exemplar that pre-empts the most likely attempted loophole. So both earn their keep. The risk is that the second sentence, by naming "own design," implicitly suggests that a placebo battery on a general design *does* qualify — which is the issue-1 gap. Suggested fix: revise the second sentence to "A simulation-based rejection rate or placebo battery — whether framed as paper-specific or general — does not qualify as (c) unless the paper proves a formal asymptotic or finite-sample property of an estimator or test." This merges the two sentences' intent and closes the re-framing gap.

**ISSUE 3 — Severity: LOW — Cross-file (c) wording divergence.**
Location: `templates/agent_bodies/shared/puzzle-triager.md` line 83; `templates/shared/docs/stage_puzzle_triage.md` line 9.

Both files still use the old (c) wording: "a formal methodological result with proved properties (e.g., a new estimator or identification theorem) — not an empirical critique of this paper's own design." The new generality qualifier ("general — applicable beyond this paper's specific analysis or dataset") is absent. The same placebo-battery re-framing attack (issue 1) is therefore possible at the puzzle-triage stage. Suggested fix: in both files, replace "with proved properties (e.g., a new estimator or identification theorem)" with "with proved properties that is general — applicable beyond this paper's specific analysis or dataset (e.g., a new estimator or identification theorem)." One-line change in each file.

---

## Benchmark walkthrough (c) — all should pass

All six papers have formal proofs of asymptotic or finite-sample properties of a general estimator or test, and all are by definition applicable beyond any single paper's analysis. All pass (c) under the new wording, including the generality qualifier: Goodman-Bacon (algebraic decomposition of two-way FE, applicable to any staggered DiD); Sun-Abraham (interaction-weighted estimator with proved convexity properties); Borusyak-Jaravel-Spiess (imputation estimator with proved efficiency); Roth (pre-trend testing framework, proved size distortion formula); Calonico-Cattaneo-Titiunik (bias-corrected RD bandwidth, proved MSE optimality); Newey-West (HAC covariance estimator, proved consistency under heteroskedasticity and autocorrelation). No over-tightening regression.

---

## Top-level question for the principal

Not ready to close. Three LOW issues remain, all fixable in one pass: (1) tighten the "own design" language in the follow-on sentence to close the motivated-re-framing attack, (2) optionally merge the two sentences to eliminate the implied-permission gap, (3) propagate the generality qualifier to puzzle-triager.md and stage_puzzle_triage.md. After those three edits, the guard is airtight and the cross-file vocabulary is consistent. A round-4 spot-check of only those three locations would suffice to close.
