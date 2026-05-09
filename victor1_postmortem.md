# Victor-1 Post-Mortem Audit

Template HEAD at deploy: `70e908b`. Project ran 2026-05-05 to 2026-05-09 (commit `9048e48`). `update.sh` never run.

---

## 1. The Actual Failure Mode

The pipeline produced a paper whose two "contributions" are (a) an EDGAR text-mining pipeline with precision 0.80 / recall 0.31 / F1 0.44, and (b) a per-cohort random-event-date placebo showing 14/16 cells fail their own benchmark — framed as "a property of the design" of cross-sectional moderator-DiD. This is exactly what the empirical-first guard in `scorer-core.md` is supposed to block: a measurement note plus an empirical critique of the paper's own design, dressed as the paper. The wrong turn happened at two moments. First, at Gate 4 (v3/v4 scorer), the empirical-first guard was never triggered because the theory's H1–H5 all passed — the paper still had an active causal claim (ERP reduces IVOL via a timing channel) and the guard language does not fire until the contribution *is* primarily a measurement note or methods critique. By the time the contribution had drifted to that shape (around r6–r7), the pipeline was past Stage 5 and the guard only runs at Gate 4. Second, the puzzle-triager at p1 issued RECONCILE (widen scope from ERP to IT-disclosure) rather than flagging that no ERP-specific economic identification survived — a verdict that was technically defensible but opened the door to a paper with no falsifiable causal claim. The result was 10 referee rounds, 5 Rejects, 2 Major Revisions, and a ship under the r10 cap with two referees permanently unpersuaded.

---

## 2. Pipeline-Side Issues

### HIGH SEVERITY

**H1. Empirical-first guard fires too late — only at Gate 4.**

- *Diagnosis:* The guard in `scorer-core.md` (EMPIRICAL_FIRST block) runs only at Gate 4. By Stage 6 the paper had drifted to a measurement-note + design-critique shape, but there is no re-evaluation gate that reapplies the H1/H5 guard to the *current stated contribution* after a seeded-mode deepen cycle.
- *Template:* `templates/agent_bodies/shared/scorer-core.md`, plus the Stage 6 triage logic in `templates/shared/core.md`.
- *Direction:* Add a lightweight contribution-shape check to the Stage 6 triage agent (or the editor agent): "Does the paper's current primary contribution still match the causal estimand committed to in `output/stage1/identification_design.md`? If not, flag as empirical-first violation before routing the deepen mandate." This mirrors the scorer's guard but runs at Stage 6 when the contribution shape is re-evaluated anyway.

**H2. RECONCILE verdict at puzzle-triage did not require a surviving causal claim.**

- *Diagnosis:* The p1 triage correctly applied RECONCILE (scope broadening from ERP to IT-disclosure) because the math holds for any signal-noise-reducing IT event. But RECONCILE did not require demonstrating that the broadened claim still has an identifiable causal estimand — and the empirical result was that the pooled IT-disclosure effect also fails parallel trends and is null on average.
- *Template:* `templates/agent_bodies/shared/puzzle-triager.md`.
- *Direction:* Add a hard rule to the RECONCILE branch: after scope broadening, require a sentence verifying that the identification strategy in `output/stage1/identification_design.md` still applies to the broadened universe. If the broadened universe has the same identification problems as the original (same pre-trend, same null ATT), RECONCILE is the wrong verdict; route to HONEST-NULL instead.

**H3. No gate reapplies H1/H5 after seeded-mode deepen cycles.**

- *Diagnosis:* After each Stage 6 Reject → deepen cycle, the paper's contribution shape evolved materially (v4 timing channel → v12 random-pseudo-event as the contribution → v13 per-cohort placebos as the contribution). None of these transitions triggered a re-scoring at Gate 4. The scorer only ran twice (v3, v4). For seeded-mode runs with deep deepen cycles, the scorer's guard becomes stale.
- *Template:* `templates/shared/core.md` (orchestrator routing), `templates/shared/docs/stage_6.md`.
- *Direction:* After a Stage 6 deepen that produces a substantive contribution-shape change (empiricist introduces a new primary result), require a mini-Gate-4 recheck: rerun only the H1/H5 hard requirements and the empirical-first guard (not the full 0-100 scoring). Block the Stage 6 re-fire if H1 or H5 fail.

### MEDIUM SEVERITY

**M1. CRM/BI panel-vs-event count anomaly undetected for ~5 rounds.**

- *Diagnosis:* 802 panel firms vs 554 events — stale-data bookkeeping bug — undetected from v7 to v13 (caught by polish-numerics at Stage 9). Empirics-auditor cross-checks ATT numbers but does not cross-check post-merge firm counts against pre-merge event counts.
- *Template:* `templates/agent_bodies/shared/empirics-auditor.md` (or `extensions/empirical/agent_bodies/shared/empirics-auditor.md`).
- *Direction:* Add a count-consistency check to the empirics-auditor output template: "Post-merge panel firm count N\_panel vs pre-merge event count N\_events. If N\_panel > N\_events by more than 20%, flag as potential merge-key ambiguity or stale-panel bug."

**M2. Empiricist prompts have no partial-state-save requirement.**

- *Diagnosis:* v13 empiricist was killed mid-run after completing DIV\_INIT; required manual relaunch. The 10h TWFE hang produced no intermediate output. No agent prompt requires checkpointing at task boundaries.
- *Template:* `extensions/empirical/agent_bodies/shared/empiricist.md` (or variant-specific equivalents).
- *Direction:* Add a mandatory "save partial results to `output/stage3a/checkpoint_{task_name}.md` before proceeding to the next task" instruction at the top of the empiricist agent body. Each named task (e.g., TWFE, CS-DR, per-cohort-placebo) is a checkpoint boundary.

**M3. Stall-check loop cron cadence too aggressive for long empirical runs.**

- *Diagnosis:* 1h `/loop` stall-check fired ~30 times over the run; each fire after >5 min reads full context cold (cache miss). For empirical runs with multi-hour tasks, a 2–3h cadence is appropriate.
- *Template:* `templates/runtime/claude/session.md` (the stall-check loop setup instruction).
- *Direction:* Add guidance: "For runs with `--ext empirical`, set stall-check cadence to 150–180 minutes, not 60 minutes. Empiricist tasks routinely exceed 90 minutes; a 60-minute check generates unnecessary cache misses without safety benefit."

### ALREADY PATCHED (known)

- Empirical-first (c)-clause exception tightened in `scorer-core.md` and `puzzle-triager.md`. Confirmed present in current template HEAD.

---

## 3. Paper-Side Issues

**Empiricist (v12–v13) produced the per-cohort random-event-date placebo battery as new empirical work and framed it as a "property of the design" finding.** This is methodologically legitimate but crosses the line from "empirical deepening of the causal claim" to "empirical critique of the paper's own design." The empiricist's prompt does not distinguish between those two classes of output. A different agent — either empirics-auditor or the Stage 6 triage — should have flagged that framing 14/16-cells-fail-placebo as the paper's primary contribution is an empirical-first violation, not a causal deepening.

**Paper-writer (r6–r10) accepted the contribution-shape pivot** from causal claim to methodological caution without checking against the identification design. In seeded mode, the paper-writer's mandate is to faithfully implement the current outputs — but this produces a paper that systematically misrepresents its contribution class (causal → methods note). The paper-writer should have flagged the gap between `output/stage1/identification_design.md`'s committed estimand and the current stated contribution.

**Theory-generator produced a model (v3/v4) whose central distinguishing test (Imp 7, CFvol orthogonality) is mechanical by construction**, not an economic prediction. The mechanism referee caught this at r1, but the scorer passed it because the mechanism check in `scorer-core.md` asks whether the mechanism is "clear," not whether it is distinguishable from a purely definitional claim. Earlier detection would have required the math-auditor-freeform to check whether any implication is "trivially guaranteed by the measurement-model definitions rather than by the theory's economic content."

---

## 4. Evaluator-Signal Failures

**Scorer (v3, v4):** Gave 52 / 55 (MAJOR REWORK / REVISE). Should have: triggered the empirical-first guard on the contribution-as-stated. Did not trigger it because at v3/v4 the paper still had an active causal claim; the guard was correctly not fired. No failure here — the guard logic was working as designed at the time it ran. The failure is that it never ran again.

**Scorer-freeform (v4):** Gave 52, Reject, "null average + fragile pre-trends." Correct diagnosis. Explicitly said "field-tier honest." The signal was right; the orchestrator's seeded-mode never-abandon rule overrode it. No evaluator failure — the routing failure is in the orchestrator.

**Math-auditor / math-auditor-freeform:** Both passed v3/v4 correctly. The freeform caught the "Prop 3 Imp 7 is mechanically guaranteed" issue at r1 as a Concern (framing, not math correctness). The prompt does not ask the freeform auditor to flag definitional-tautology implications — it asks about mathematical correctness and framing. This gap (definitional vs economic) was not caught at the math-auditor level.

**Novelty-checker:** Returned NOVEL for the combination; correct. Did not flag that the central distinguishing test is a definitional tautology rather than an empirical novelty. Novelty-checker checks prior work, not logical structure.

**Referee / referee-freeform:** Worked correctly. Both Reject r1 (freeform score 42, structured Reject) with the exact diagnosis ("null average + fragile ID + thin theory"). Freeform held Reject 28–38 through r10. These agents performed as intended — they were the ones generating the kill signal. The failure is that the seeded-mode constraint let the paper run 9 more rounds past the first correct Reject.

**Referee-mechanism:** Gave MECHANISM-PARTIAL at r1, MECHANISM-VALID from r6 onward (under substance-over-form leeway after the paper explicitly disavowed the mechanism). The r6+ MECHANISM-VALID verdict is the most consequential evaluator failure in this run: after the paper demoted the framework to "motivating apparatus," the mechanism referee applied substance-over-form leeway and held VALID — which anchored the orchestrator's deepen-path direction for rounds 6–10. The mechanism referee's VALID was technically defensible (the timing-channel force is real) but operationally misleading: VALID implies "the mechanism check is satisfied," which the orchestrator interpreted as "keep building toward this paper." A more granular mechanism verdict — e.g., VALID-BUT-DECORATIVE or VALID-GENERIC (mechanism is real but not model-specific) — would have changed the routing.

**Self-attacker:** Flagged correct concerns at v3/v4 (pre-trend, null ATT, SA demean). No failure.

**Empirics-auditor:** Caught real bugs at v3 (BJS-horizon, treated-only spec, SA hardcoded, TWFE-Spec-E), v6 (placebo 100%-amendments bug), v15 (SPLIT t-stat inconsistency). Did not catch the v7–v13 CRM/BI count anomaly. Did not flag that per-cohort placebos as the paper's headline constitutes an empirical-first violation. The auditor checks code correctness, not contribution-class appropriateness.

**Identification-auditor:** Ran once at Stage 1; gave PASS-with-severity-4–6 concerns. Never re-ran during the deepen cycles. The identification design was never re-evaluated after the contribution shifted from ERP→IVOL (causal) to random-event-date benchmark (methodological). This is the largest single evaluator gap: the identification-auditor should have re-fired when the primary estimand changed.

**Branch-manager:** Correctly diagnosed at v4 that the paper was at its top-3-fin ceiling and field-tier advance was achievable. Recommended ADVANCE to Stage 5. This was the right call given the evidence at v4. The branch-manager's subsequent gate-5-reject checks (r3–r7) also correctly kept classifying Rejects as SUBSTANTIVE-deepen. No failure in the branch-manager's own logic — the failure is that each round the substantive-deepen mandate pushed the empiricist toward contribution-shape drift rather than causal identification improvement.

---

## 5. Process / Orchestration Issues

**Stale-template lock-in.** Template was at `70e908b` for the full run. Any fixes to `scorer-core.md`, `puzzle-triager.md`, or the empirical-first guard that landed after `2026-05-05` did not flow in. The recently-patched (c)-clause tightening would have applied from r1 if `update.sh` had run.

**Seeded-mode never-abandon kept the paper running 6 rounds past when both scorers said Reject at top-3-fin.** The freeform referee held Reject 28–38 for rounds r1–r10 with the same structural diagnosis every time: "pick a lane / decide what the paper is." This is not a resolvable comment under seeded-mode fidelity constraints. The seeded-mode core principle ("fidelity to the seed beats any 'better' alternative") produced a permanent dissent that the gate-cap rule had to override to ship. This is a known and documented architectural limit, but its interaction with multi-round deepen cycles needs clearer escalation logic: if the freeform referee repeats the same structural Reject for 3+ consecutive rounds with no score improvement, the orchestrator should surface a "permanent-dissent cap" warning and let the operator decide whether to continue.

**Stage 6 r10 max-10 cap fires as a de facto SHIP override.** The paper shipped because it hit the round cap, not because it cleared the quality bar. The lessons file is honest about this. The pipeline's ship-under-cap mechanism is intentional, but the run shows that in seeded mode with a permanent-dissent evaluator, the cap is the only exit. This interacts with the stale-template issue: a later template version with the tightened (c)-clause would have triggered the empirical-first guard earlier and potentially changed the deepen direction before r6.

**No `update.sh` run.** For a 4-day run with active template development, the principal should be prompted to run `update.sh` at least once per day. The session guidance (`templates/runtime/claude/session.md`) does not mention `update.sh` as a mid-run maintenance step.

---

## 6. Top 5 Highest-Leverage Fixes

**Ranked by (failure prevented × breadth of application):**

### 1. Contribution-shape re-check at Stage 6 deepen routing

**Failure it prevents:** The primary failure mode — contribution drifts from causal claim to measurement note / design critique across deepen cycles, with no gate to catch it. Catches the victor-1 trajectory at r6 instead of r10.

**Template files:** `templates/shared/core.md` (Stage 6 deepen routing logic), `templates/shared/docs/stage_6.md`.

**Difficulty:** One-section. Add a paragraph to the deepen-routing block: "Before issuing the deepen mandate, verify that the empirical work being requested deepens the causal estimand in `output/stage1/identification_design.md`, not just adds robustness to a methods critique. If the proposed new empirical work is primarily a critique of the paper's own design (placebo benchmark, power study, validation recall), check H1/H5 before routing."

---

### 2. Identification-auditor re-fires on contribution-shape change

**Failure it prevents:** The identification design was evaluated once (Stage 1) but the paper's primary estimand changed fundamentally during deepen cycles. The identification-auditor never reran; referees were the first to flag the identification mismatch.

**Template files:** `templates/shared/core.md` (orchestrator trigger conditions), `extensions/empirical/agent_bodies/shared/identification-auditor.md`.

**Difficulty:** One-section. Add a trigger condition: "Re-fire identification-auditor whenever the triage agent or paper-writer proposes a new primary estimand or a contribution-shape change from causal to descriptive/methodological. Pass the new estimand statement alongside `output/stage1/identification_design.md`."

---

### 3. RECONCILE verdict requires surviving causal claim verification

**Failure it prevents:** The p1 RECONCILE opened the door to a broader-scope paper (IT-disclosure instead of ERP) without verifying that the broadened scope had the same null ATT and identification problems. Earlier recognition of this would have routed to HONEST-NULL sooner.

**Template files:** `templates/agent_bodies/shared/puzzle-triager.md` (hard rules section).

**Difficulty:** One-line/one-section. Add to hard rules: "RECONCILE requires a one-sentence verification that the identification strategy in `output/stage1/identification_design.md` applies to the broadened universe. If the broadened universe inherits the same pre-trend, null-ATT, or instrument-absence problems as the original, route to FIX-EMPIRICS or HONEST-NULL instead."

---

### 4. Mechanism referee verdict granularity: add VALID-GENERIC category

**Failure it prevents:** MECHANISM-VALID from r6 onward (applied under substance-over-form leeway after the paper disavowed the framework) anchored the orchestrator's deepen direction for 5 rounds. A mechanism that is real but non-model-specific produces a different deepen mandate than a mechanism that is model-specific and validated.

**Template files:** `templates/agents/finance/referee-mechanism.md` (and macro equivalent). The verdict set and their orchestrator-routing consequences in `templates/shared/core.md`.

**Difficulty:** One-section. Add `VALID-GENERIC` as a verdict: "The economic force is real but the empirical tests do not pin down this model's structure against simpler alternatives. Orchestrator routing: treat as PARTIAL for deepen-mandate purposes — the mechanism check is satisfied but does not support top-3-fin tier claims that require model-distinctive tests."

---

### 5. Empiricist checkpoint saves + count-consistency check in empirics-auditor

**Failure it prevents:** (a) Two empiricist kills/hangs forced multi-hour reruns from scratch; (b) CRM/BI count anomaly went undetected for 5 rounds, silently contaminating reported event counts in the paper.

**Template files:** `extensions/empirical/agent_bodies/shared/empiricist.md`; `extensions/empirical/agent_bodies/shared/empirics-auditor.md`.

**Difficulty:** One-line each. Empiricist: add "save checkpoint to `output/stage3a/checkpoint_{task}.md` upon completing each named task before starting the next." Empirics-auditor: add "cross-check: post-merge panel firm count N\_panel vs pre-merge event count N\_events; flag if N\_panel > 1.2 × N\_events as potential merge-key or stale-panel bug."

---

*Total word count: ~1,480.*
