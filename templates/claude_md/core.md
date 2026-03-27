# CLAUDE.md — Autonomous Theory Paper Pipeline

## Purpose

This project autonomously produces a **{{PAPER_TYPE}}** suitable for submission to a {{TARGET_JOURNALS}}. The system runs end-to-end with no human intervention after launch. Quality is enforced by adversarial evaluation at every stage.

The project also produces a **process log** documenting how the autonomous system worked, as a pedagogical record.

---

## Pipeline overview

```
Stage 0: Problem Discovery   ──→ Gate 0: Problem Viability
Stage 1: Idea Generation     ──→ Gate 1: Idea Review (iterates with generator)
                                   └── ADVANCE → best idea selected
                                Gate 1b: Novelty Check on idea
                                   ├── KNOWN → kill idea, back to Stage 1
                                   ├── INCREMENTAL → flag, proceed with caution
                                   └── NOVEL → Gate 1c
                                Gate 1c: Idea Prototype (tractability)
                                   ├── BLOCKED → try next idea or back to Stage 1
                                   └── TRACTABLE → proceed to Stage 2
Stage 2: Theory Development  ──→ Gate 2: Math Audit (structured then free-form)
                                   Gate 3: Novelty Check on full theory
                                   Gate 3b: Empirical Feasibility (falsify-first, optional)
                                      ├── FALSIFIED → back to Stage 1
                                      └── OK → proceed
Stage 3: Implications        ──→ Stage 3c/3d: LLM Experiments (optional)
                                   Stage 3e: Full Empirical Analysis (optional)
Stage 4: Self-Attack          ──→ Gate 4: Scorer Decision (trajectory-based)
                                   ├── ADVANCE (75+) → Stage 5
                                   ├── REVISE  → back to Stage 2 (continue if Δ≥3, else escalate)
                                   ├── REWORK  → back to Stage 1 (continue if Δ≥3, else escalate)
                                   └── ABANDON → back to Stage 0 (max 3×)
Stage 5: Paper Writing        ──→
Stage 6: Referee Simulation   ──→ Gate 5: Referee Decision
                                   ├── Minor/Accept → Stage 7
                                   ├── Major Revision → revise, re-run Stage 6 (max 2×)
                                   └── Reject → back to Stage 1
Stage 7: Style Check          ──→ Done
```

---

## Pipeline state

State is tracked in `process_log/pipeline_state.json`. Read this file at session start. Update it after every stage transition. Commit after every update.

Initial state (created by setup.sh):
```json
{
  "current_stage": "stage_0",
  "problem_attempt": 1,
  "idea_round": 0,
  "theory_attempt": 1,
  "revision_round": 0,
  "referee_round": 0,
  "status": "not_started",
  "scores": {},
  "history": []
}
```

When you start the pipeline, set `"status": "running"` and begin appending to the history array.

**History array:** Append a `{ "timestamp": "ISO-8601", "event": "description" }` entry for every pipeline event. This feeds the dashboard. Use `date -u +%Y-%m-%dT%H:%M:%SZ` to get the timestamp. Never truncate or clear the history array.

---

## Stage 0: Problem Discovery

**Agent:** `literature-scout`

1. Choose a domain within {{DOMAIN_AREAS}}
2. Launch literature-scout to search for open questions, puzzles, or gaps
3. Save results to `output/stage0/literature_map.md`
4. Write a problem statement to `output/stage0/problem_statement.md`
5. Commit: `pipeline: stage 0 complete — problem identified`

### Gate 0: Problem Viability

The orchestrator (you) evaluates:
- Is this question important enough for a top journal?
- Is there actually a gap?
- Is it tractable as a pure theory paper?

Score 0-100. If below 50, re-run Stage 0 with different search terms. After 3 failures, pick the best problem and proceed.

---

## Stage 1: Idea Generation

**Agents:** `idea-generator` + `idea-reviewer` (iterating)

**How many ideas to generate:** The number of candidates should increase when the pool is weaker — more failed attempts mean more draws are needed to find a good one.

| Context | Ideas per round |
|---------|----------------|
| First time entering Stage 1 | 5 |
| Returning from a failed theory (scorer REWORK/ABANDON) | 10 |
| Returning from a problem-level failure (Stage 0 re-run) | 10, and explicitly explore different territory |

1. Read `output/stage0/problem_statement.md`, `output/stage0/literature_map.md`, and `output/data_inventory.md`
2. If returning from a failed attempt, also read the previous scorer feedback and/or failed theory to understand what went wrong — instruct the idea-generator to avoid the same failure mode
3. Launch idea-generator with the problem statement, literature map, **and data inventory** to brainstorm candidate mechanisms (see table above for count)
4. Save sketches to `output/stage1/idea_sketches_rN.md` (N = round number)
5. Commit: `artifact: idea sketches round {N}`

### Gate 1: Idea Review

**Agent:** `idea-reviewer`

1. Launch idea-reviewer on the sketches + problem statement + literature map
2. If this is a return visit to Stage 1, also provide the previous scorer feedback so the reviewer knows what to screen against
3. Save review to `output/stage1/idea_review_rN.md`
4. Commit: `artifact: idea review round {N}`
5. Read the decision:

| Decision | Action |
|----------|--------|
| **ADVANCE** | Best idea identified. Proceed to Stage 2 with the reviewer's instructions for theory development. |
| **ITERATE** | Re-launch idea-generator with the reviewer's feedback. Max 3 rounds of iteration. |
| **REJECT ALL** | All ideas are weak. Return to Stage 0 for a different problem. |

6. After 3 rounds without ADVANCE, pick the highest-scored idea and advance it anyway.
7. Save the winning idea summary to `output/stage1/selected_idea.md`
8. Commit: `artifact: selected idea saved`

### Gate 1b: Novelty Check on Selected Idea

**Agent:** `novelty-checker`

This is the first of two deep novelty checks. It runs on the selected idea *before* investing in theory development.

1. Launch novelty-checker on `output/stage1/selected_idea.md` + `output/stage0/literature_map.md`
2. Save result to `output/stage1/novelty_check_idea.md`
3. Read the verdict:

| Verdict | Action |
|---------|--------|
| **KNOWN** | Kill this idea. Pick the next-best idea from the current round's sketches (per idea-reviewer rankings) and re-run Gate 1b on it. If no viable ideas remain in the current round, re-run Stage 1 with a new round of idea generation (counts toward the 3-round limit). |
| **INCREMENTAL** | Flag it. Proceed to Stage 2 but the scorer will weigh this at Gate 4. |
| **NOVEL** | Proceed to Stage 2. |

4. Commit: `pipeline: gate 1b — novelty check on idea {NOVEL/INCREMENTAL/KNOWN}`

### Gate 1c: Idea Prototype (tractability check)

**Agent:** `idea-prototyper`

Quick mathematical feasibility check — attempt the key derivation before investing in full theory development. **Always runs** (not optional), because even first-attempt ideas can have hidden tractability issues that the sketch doesn't reveal.

1. Launch idea-prototyper on `output/stage1/selected_idea.md` + `output/stage0/problem_statement.md`
2. Save result to `output/stage1/idea_prototype.md`
3. Read the verdict:

| Verdict | Action |
|---------|--------|
| **TRACTABLE** | The main result goes through. Proceed to Stage 2 — pass the prototype to the theory-generator as a head start. |
| **BLOCKED** | The derivation hit a wall. Read where it got stuck. If fixable: pick the next-best idea from the reviewer's rankings and re-run Gates 1b+1c. If fundamental: return to Stage 1 for a new round. |

4. Commit: `pipeline: gate 1c — idea prototype {TRACTABLE/BLOCKED}`
5. Update pipeline_state.json and commit: `pipeline: stage 1 complete — idea selected, novelty-checked, and prototyped`

---

## Stage 2: Theory Development

**Agent:** `theory-generator`

1. Read `output/stage1/selected_idea.md`, `output/stage1/idea_prototype.md`, `output/stage0/problem_statement.md`, and `output/stage0/literature_map.md`
2. Choose strategy:
   - Attempt 1: develop the selected idea into a full theory, building on the prototype's derivation
   - Attempt 2+: mutate (if previous attempt had good elements) or fresh with different approach
3. Launch theory-generator with the selected idea, problem statement, literature map, and strategy
4. Save result to `output/stage2/theory_draft_vN.md` (N = attempt number)
5. Commit: `artifact: theory draft v{N}`

### Gate 2: Math Audit (structured + free-form)

**Agents:** `math-auditor` then `math-auditor-freeform`

Two audits run sequentially. The structured audit checks every derivation step-by-step. The free-form audit reads the theory as a skeptical reader and catches conceptual issues that step-by-step verification misses. Both must PASS before advancing.

**Step 1: Structured audit**

1. Launch math-auditor on `output/stage2/theory_draft_vN.md`
2. Save result to `output/stage2/math_audit_vN.md`
3. Commit: `artifact: math audit v{N} — {PASS/FAIL}`
4. If FAIL:
   - Read the specific errors from the audit
   - Re-launch theory-generator in **mutate** mode with the draft + audit feedback
   - Keep iterating as long as the error count is decreasing (making progress). Escalate only if errors plateau or increase across two consecutive attempts — treat as theory failure, increment theory_attempt
5. If PASS: proceed to Step 2

**Step 2: Free-form audit**

1. Launch math-auditor-freeform on `output/stage2/theory_draft_vN.md`
2. Save result to `output/stage2/freeform_audit_vN.md`
3. Commit: `artifact: freeform audit v{N} — {PASS/FAIL}`
4. If FAIL:
   - Read the concerns from the free-form audit
   - Re-launch theory-generator in **mutate** mode with the draft + free-form audit feedback
   - After mutation, re-run **both** audits from Step 1 (the fix may have introduced new algebraic errors)
   - Same rule: keep iterating while progress is being made, escalate if concerns plateau or increase
5. If PASS: proceed to Gate 3

### Gate 3: Novelty Check on Full Theory

**Agent:** `novelty-checker`

This is the second of two deep novelty checks. The idea was already checked at Gate 1b, but the full theory may overlap with prior work in ways the sketch did not reveal — the mechanism may be novel while the result is not, or the developed model may converge to a known framework.

1. Launch novelty-checker on `output/stage2/theory_draft_vN.md`
2. Save result to `output/stage2/novelty_check_vN.md`
3. If KNOWN: abandon this theory, return to Stage 2 with new approach
4. If INCREMENTAL: flag it, proceed with caution (scorer will weigh this)
5. If NOVEL: proceed to empirical feasibility check (if empirical extension) or Stage 3
6. Commit: `artifact: novelty check v{N} — {NOVEL/INCREMENTAL/KNOWN}`

### Gate 3b: Empirical Feasibility (optional — empirical extension, falsify-first)

**This gate runs only if** `empiricist` agent exists in `.claude/agents/`. If not present, skip to Stage 3.

Quick falsification check: can this theory be calibrated at all? Do the key empirical moments exist? A theory that predicts the wrong sign on a well-measured moment is dead regardless of how elegant the implications are. Check this BEFORE investing in implications.

1. Launch `empiricist` with a focused instruction: "Quick feasibility check only — download the 2-3 key moments this theory needs to match. Report whether the theory's predictions are in the right ballpark. Do NOT run a full analysis."
2. Save to `output/stage3b/empirical_feasibility.md`
3. If the key moments contradict the theory (wrong sign, off by an order of magnitude): flag as **FALSIFIED** — return to Stage 1 for a new idea. Don't waste time on implications for a theory the data already rejects.
4. If moments are roughly consistent or unavailable: proceed to Stage 3.
5. Commit: `artifact: empirical feasibility — {OK/FALSIFIED}`

---

## Stage 3: Implications

**Orchestrator task** (no separate agent needed — you do this)

1. Read the theory draft
2. Work out:
   - Testable predictions
   - Comparative statics
   - Special cases that recover known results
   - Economic intuition for each result
3. Append to the theory draft or write to `output/stage3/implications.md`
4. Commit: `pipeline: stage 3 — implications developed`

---

## Stage 3c/3d: LLM Experiments (optional — theory_llm extension)

**These stages run only if** `llm_client.py` exists in the project root and `experiment-designer` agent exists in `.claude/agents/`. If not present, skip to the next optional stage or Stage 4.

1. **Stage 3c:** Launch `experiment-designer` on the theory draft + implications. The agent identifies predictions testable via LLM calls, designs controlled experiments with ground truth and controls, writes and executes code using `llm_client.py`. Saves to `output/stage3b_experiments/`.
2. **Stage 3d:** Launch `experiment-reviewer` on the design, code, raw results, and analysis. Evaluates methodology (internal validity, controls, sample size, statistical tests) and interpretation.

| Decision | Action |
|----------|--------|
| **ACCEPT** | Proceed to Stage 4 (self-attacker receives experiment results too) |
| **REVISE** | Re-run specific experiments or re-analyze. Max 2 revision rounds. |
| **REDESIGN** | Fundamental methodology problem. Redesign and re-run. Max 1 redesign. |

3. Commit: `artifact: experiments — {ACCEPT/REVISE/REDESIGN}`

---

## Stage 3e: Full Empirical Analysis (optional — empirical extension)

**This stage runs only if** `empiricist` agent exists in `.claude/agents/` and `.claude/skills/fred/` exists. If not present, skip to Stage 4.

This is the full empirical analysis — deeper than the feasibility check at Gate 3b. Now that implications are developed, the empiricist can design proper tests, calibrations, and portfolio sorts.

1. Launch `empiricist` on the theory draft + implications + feasibility results (if any). The agent reads the theory, decides what empirical work is appropriate, fetches data via skills (FRED, Ken French, Chen-Zimmerman, WRDS, EDGAR), and executes it. Saves to `output/stage3b/empirical_analysis.md` and `code/empirical.py`.
2. All code must be written to files (`code/` for final, `code/tmp/` for scratch). Never run inline `python3 -c`.
3. **Empirics audit.** Launch `empirics-auditor` on the empirical analysis + code + theory draft. The auditor runs the code, verifies results, checks methodology.
   - If **PASS**: proceed to Stage 4. Self-attacker and scorer receive empirical results alongside the theory.
   - If **FAIL**: re-launch `empiricist` with the audit feedback. Keep iterating as long as the number of issues is decreasing (the empiricist is making progress). Escalate only if the issue count plateaus or increases across two consecutive attempts.
4. Commit: `artifact: empirics audit — {PASS/FAIL}`

---

## Stage 4: Self-Attack

**Agent:** `self-attacker`

1. Launch self-attacker on the theory draft + implications
2. Save result to `output/stage4/self_attack_vN.md`
3. Commit: `artifact: self-attack v{N}`

### Gate 4: Scorer Decision

**Agent:** `scorer`

1. Launch scorer with:
   - Theory draft: `output/stage2/theory_draft_vN.md`
   - Math audit (structured): `output/stage2/math_audit_vN.md`
   - Math audit (free-form): `output/stage2/freeform_audit_vN.md`
   - Novelty check (idea): `output/stage1/novelty_check_idea.md`
   - Novelty check (theory): `output/stage2/novelty_check_vN.md`
   - Self-attack: `output/stage4/self_attack_vN.md`
2. Save result to `output/stage4/scorer_decision_vN.md`
3. Read the decision using **state-dependent escalation**:

**First scorer evaluation** (no prior score): use band logic.

| Decision | Action |
|----------|--------|
| **ADVANCE** (75+) | Proceed to Stage 5 |
| **REVISE** (55-74) | Return to Stage 2 in mutate mode with scorer feedback. |
| **MAJOR REWORK** (35-54) | Return to Stage 1 to generate new ideas with scorer feedback. |
| **ABANDON** (<35) | Increment theory_attempt. Return to Stage 1. After 3 abandons on same problem, return to Stage 0. |

**Subsequent scorer evaluations** (has prior score): use score trajectory.

| Condition | Action |
|-----------|--------|
| Score ≥ 75 | **ADVANCE** — always, regardless of trajectory |
| Score < 35 | **ABANDON** — always, regardless of trajectory |
| Delta ≥ 3 points | **CONTINUE** — one more iteration in current band: REVISE returns to Stage 2, MAJOR REWORK returns to Stage 1 (improving, worth continuing) |
| Delta < 3 points | **ESCALATE** — move up one level: REVISE → MAJOR REWORK (Stage 1) → ABANDON (plateau or decline, not converging) |
| Score < 60 on attempt 3+ | **ESCALATE** — regardless of delta. A score below 60 after two revisions suggests a ceiling on this idea. Repair can't fix it; regenerate. |

**Hard ceiling:** After 4 total scorer evaluations on the same problem, escalate one level regardless of trajectory. This prevents slow-but-never-arriving loops (e.g., +3, +3, +3 but still at 69).

Record all scores in `pipeline_state.json` under `"scores"` so the trajectory can be computed: `"scores": { "v1": 60, "v2": 63, "v3": 67 }`.

4. Update pipeline_state.json accordingly
5. Commit: `pipeline: gate 4 — scorer {DECISION} (score: {N})`

---

## Stage 5: Paper Writing

**Agent:** `paper-writer`

1. Launch paper-writer with:
   - Theory draft (latest version)
   - Literature map
   - Scorer assessment
   - Self-attack report (so the paper preemptively addresses weaknesses)
2. Paper-writer creates files in `paper/sections/`:
   - `introduction.tex`
   - `model.tex`
   - `results.tex`
   - `discussion.tex`
   - `conclusion.tex`
   - `appendix.tex` (if needed)
3. Paper-writer creates `paper/main.tex` with `\input` commands
4. Commit: `pipeline: stage 5 — paper draft written`

---

## Stage 6: Referee Simulation

**Agent:** `referee`

1. Delete any previous reports in `paper/referee_reports/`
2. Launch referee agent (fresh context, no knowledge of development process)
3. Save report to `paper/referee_reports/YYYY-MM-DD_vN.md`
4. Commit: `pipeline: stage 6 — referee report received`

### Gate 5: Referee Decision

Read the referee's recommendation:

| Recommendation | Action |
|---------------|--------|
| **Accept / Minor Revision** | Fix minor comments, proceed to Stage 7 (style check). |
| **Major Revision** | Revise the paper addressing major comments. Re-run Stage 6. Max 2 referee rounds. |
| **Reject** | Read the rejection reasons. If fixable: return to Stage 2 with referee feedback. If fundamental: return to Stage 0. |

---

## Stage 7: Style Check

**Agent:** `style`

1. Launch style agent on the paper
2. Read the style report
3. Fix all violations by editing the section files directly
4. Commit: `pipeline: stage 7 — style violations fixed`
5. Pipeline complete. Final commit: `pipeline: COMPLETE — paper ready for submission`

Update pipeline_state.json with `"status": "complete"` when done.

Final commit: `pipeline: COMPLETE — paper ready for submission`

---

## Post-pipeline math audit rule

After the pipeline is complete (`"status": "complete"`), any new or modified proposition, lemma, or corollary in `paper/sections/*.tex` must pass a math audit before being committed. This applies to all post-pipeline edits — referee response fixes, manual revisions, additions requested by co-authors, etc.

**Procedure:**
1. Write the new/modified content to a temporary file: `output/post_pipeline/pending_audit_N.md`
2. Launch `math-auditor` on that file
3. Save result to `output/post_pipeline/audit_result_N.md`
4. If FAIL: fix the content and re-audit. Do not commit to `paper/sections/` until it passes.
5. If PASS: commit the content to the paper section file.
6. Commit format: `paper: post-pipeline edit — [description] (audited)`

**Never commit unaudited mathematical content to paper sections after pipeline completion.** The pipeline's v1 runs showed 3/3 post-pipeline audits failed — this rule exists to prevent that.

---

## Never-abandon rule

**Once a paper draft exists (Stage 5+), the pipeline must produce a finished paper.** Do not loop back to Stage 0 after investing in paper writing. Instead, use the extension playbook below to strengthen the paper.

If the scorer plateaus in the 55-74 range or the referee gives Major Revision with structural concerns (result is fragile, too narrow, or shallow):

### Extension playbook — economically substantive mathematical extensions

When the core result is correct but thin, the path to a journal paper is through extensions that are both mathematically hard and economically interesting. The goal is not robustness-checking — it's discovering new economic content that the simple model hid. Hard math often delivers surprising insights: a continuous-time formulation reveals a new channel, incomplete markets create an amplification mechanism, learning generates endogenous cycles. The extension should either (a) uncover new economics that changes the story, or (b) introduce a new concept or technique that helps tackle existing puzzles in the literature.

| Extension type | Economic question it answers | What makes it hard and valuable |
|---------------|-----------|-------------|
| **Continuous time** | How do the dynamics and transition paths work? What are the impulse responses? Does the result hold off steady state? | HJB equations, Kolmogorov forward equations, SDEs. Yields sharper results than discrete time and connects to literatures (intermediary pricing, slow-moving capital) that discrete models cannot reach. Humans avoid the PDE work; the economics is often surprising. |
| **Incomplete markets / heterogeneity** | Does the result survive when agents face idiosyncratic risk and borrowing constraints? How does the wealth distribution shape the aggregate outcome? | Bewley/Aiyagari/HANK models with analytical results are rare and highly valued. The aggregation problem is genuinely hard. When a result holds with heterogeneity, that's a much stronger paper. |
| **Learning and incomplete information** | What happens when agents don't observe the state and must learn? Does the result hold under signal extraction? Do beliefs become a state variable? | Bayesian updating in equilibrium creates feedback loops between beliefs and prices. The filtering algebra is hard but the economic content is rich — you get belief-driven dynamics, information cascades, and endogenous uncertainty. |
| **General preferences** | Is the result an artifact of CARA/log/linear-quadratic, or does it hold for CRRA, Epstein-Zin, habits? Where exactly does it break and why? | Moving beyond tractable preferences requires perturbation methods, envelope arguments, or duality tricks. The economic content is in *why* it breaks — what economic force does the tractable case suppress? A characterization of "holds if and only if [condition]" is a real theorem. |
| **Higher dimensions** | Does the 2-asset result extend to N assets? The 2-agent result to a continuum? Does the structure of the solution change qualitatively? | N-dimensional results often reveal structure invisible in low dimensions (e.g., factor structure, spanning, aggregation). The algebra is harder but the results are more general and the economic content richer. |
| **Perturbation and approximation** | When exact results need strong assumptions, how far do they extend? What's the formal error bound? | A bound like "welfare cost deviates by O(σ⁴)" is a theorem, not a robustness check. It tells you which assumptions are load-bearing and which are cosmetic. Addresses referee concerns about fragility with mathematical precision. |
| **Dynamic / stochastic extensions** | What happens with persistence, regime-switching, time-varying parameters? Does the static intuition survive? | Dynamic models generate testable predictions (forecastability, autocorrelation structure, crisis behavior) that static models cannot. The economics often changes qualitatively — mean-reversion vs. unit root matters for policy. |
| **Moral hazard / agency** | Does the result change when agents have hidden actions? What if effort is unobservable or risk-taking is private? | Principal-agent structure interacts with market outcomes in non-trivial ways. Incentive constraints reshape equilibrium prices, capital allocation, and welfare. Often generates new policy implications. |
| **Adverse selection** | What if agents have private information about quality, type, or fundamentals? Does the mechanism survive screening or signaling? | Adverse selection creates market breakdown, pooling, or separation that can overturn competitive results. Rich interaction with market design and regulation. |
| **Market design / mechanism design** | Can you design a market, contract, or institution that implements the efficient outcome? What's the optimal mechanism given the friction? | Connects theory to practice. Auction design, information disclosure, platform design. Results here have direct policy and institutional implications. |
| **Network and contagion effects** | What happens when agents are connected through a network (interbank, supply chain, information)? Does the result amplify or dampen? | Network structure creates systemic risk, cascades, and amplification. The math (spectral methods, fixed points on graphs) is hard but reveals when local shocks become aggregate. |

### How to apply

1. Read the scorer feedback and self-attack report. Identify the specific economic weakness — not "the result is narrow" but "the result only holds under CARA-normal, and the economic channel may depend on the absence of wealth effects."
2. Pick 1-2 extensions that directly address that economic question. Each extension should answer: "Does the economic channel survive when [realistic feature] is present?"
3. For each extension: state the economic question, set up the model, prove the result (or prove it breaks — a clean counterexample is as valuable as a positive result). Explain the economics of why.
4. A paper with a **core result + 2-3 substantive extensions** that map out when the result holds and fails is a characterization. That is a journal paper.
5. Re-run Gate 2 (math audit) on the new results, then Gate 4 (scorer).

### When to use this vs. starting over

- Score 55+ with correct core result → **Extend.** The economic idea is right, the paper needs more results. Build the characterization.
- Score < 35 or core result is wrong → **Start over.** Extensions can't fix broken economics.
- Novelty check KNOWN → **Start over.** Extensions won't create novelty that isn't there.

---

## Escalation rules (prevent infinite loops)

| Situation | After N failures | Action |
|-----------|-----------------|--------|
| Idea review iterates | 3 rounds | Pick the best idea and advance to Gate 1b |
| Idea review rejects all | 1 rejection | Return to Stage 0 for a different problem |
| Idea novelty check (Gate 1b) KNOWN | All ideas from current round exhausted | New round of Stage 1 (counts toward 3-round limit) |
| Math audit fails | 3 attempts | Abandon this theory version |
| Scorer: delta ≥ 3 | — | Allow one more iteration in current band |
| Scorer: delta < 3 (plateau/decline) | — | Escalate one level (REVISE → MAJOR REWORK → ABANDON) |
| Scorer: hard ceiling | 4 total evaluations on same problem | If score ≥ 55: switch to extension playbook. If score < 55: escalate one level. |
| Scorer plateau 55-74 | 2 consecutive delta < 3 | Switch to extension playbook — the core idea works, it needs mathematical depth, not reworking. |
| Theory scored ABANDON | 3 theories on same problem | Change the problem (Stage 0) |
| Problem viability fails | 3 problems | Pick the best scoring problem and proceed anyway |
| Referee: Major Revision | Structural concerns (fragile, narrow, shallow) | Use extension playbook to strengthen before resubmitting. Do not loop back to Stage 0. |
| Referee rejects | 2 rejections with "fundamental flaw" | Return to Stage 0 with entirely new topic |

---

## File organization

```
dashboard.html              # Live progress dashboard (serve with python3 -m http.server)
output/
├── stage0/
│   ├── problem_statement.md
│   └── literature_map.md
├── data_inventory.md               # available data sources (written at startup)
├── stage0/
│   ├── problem_statement.md
│   └── literature_map.md
├── stage1/
│   ├── idea_sketches_r1.md
│   ├── idea_review_r1.md
│   ├── idea_sketches_r2.md
│   ├── idea_review_r2.md
│   ├── selected_idea.md
│   ├── novelty_check_idea.md
│   └── idea_prototype.md
├── stage2/
│   ├── theory_draft_v1.md
│   ├── theory_draft_v2.md
│   ├── math_audit_v1.md
│   ├── math_audit_v2.md
│   ├── freeform_audit_v1.md
│   ├── freeform_audit_v2.md
│   ├── novelty_check_v1.md
│   └── novelty_check_v2.md
├── stage3/
│   └── implications.md
├── stage3b/
│   ├── empirical_feasibility.md    # Gate 3b quick falsification check
│   └── empirical_analysis.md       # Stage 3e full empirical analysis
├── stage3b_experiments/             # LLM experiments (--ext theory_llm)
│   ├── experiment_design.md
│   └── experiment_analysis.md
├── stage4/
│   ├── self_attack_v1.md
│   └── scorer_decision_v1.md
├── post_pipeline/
│   ├── pending_audit_1.md
│   └── audit_result_1.md
paper/
├── main.tex
├── sections/
│   ├── introduction.tex
│   ├── model.tex
│   ├── results.tex
│   ├── discussion.tex
│   ├── conclusion.tex
│   └── appendix.tex
├── referee_reports/
│   └── YYYY-MM-DD_v1.md
process_log/
├── pipeline_state.json
├── history.md
├── sessions/
├── discussions/
├── decisions/
└── patterns/
```

---

## Commit protocol — COMPULSIVE COMMITS

**Commit early, commit often.** This pipeline runs autonomously and may be interrupted at any time. Every piece of work that hits disk must be committed immediately so progress is never lost and the dashboard stays current.

### When to commit

- **After every file write.** If you wrote or updated a file, commit it. Do not batch.
- **After every stage transition.** Update `pipeline_state.json` first, then commit.
- **After every gate decision.** The gate result file + updated state = one commit.
- **After every agent output.** When a subagent returns and you save its output, commit immediately.
- **After every edit to the paper.** Each section edit gets its own commit.
- **Before launching a subagent.** If you updated state or wrote input files, commit first so the state on disk matches reality if the session dies mid-agent.

### Commit message format

| Prefix | When |
|--------|------|
| `pipeline:` | Stage transitions, gate decisions, pipeline state changes |
| `artifact:` | Saving agent output (theory drafts, audits, novelty checks, etc.) |
| `paper:` | Paper section writes and edits |
| `scribe:` | Documentation updates (scribe agent) |

Examples:
- `pipeline: stage 0 complete — problem identified`
- `artifact: theory draft v2 saved`
- `artifact: math audit v2 — PASS`
- `pipeline: gate 4 — scorer ADVANCE (score: 78)`
- `paper: introduction.tex written`
- `pipeline: state updated — entering stage 4`

### Rules

- **Never batch commits.** One logical action = one commit.
- **Always update `pipeline_state.json` before committing stage transitions.**
- **Always update `pipeline_state.json` history array** with a timestamped entry for every event, so the dashboard can display progress.
- **If in doubt, commit.** An extra commit costs nothing. Lost work costs everything.

The scribe agent runs in the background and commits with `scribe:` prefix for documentation updates.

---

{{SCORING}}

---

## Paper Writing Style Guide

These rules apply when writing paper drafts.

- Active voice always. Passive voice is the enemy.
- No filler before "that": "It should be noted that X" → "X"
- No self-congratulatory adjectives (striking, novel, important)
- Clothe the naked "this" — always follow with a noun
- No em-dashes; use commas, colons, periods, or parentheses
- Don't "assume" model structure — state it: "Consumers have power utility"
- "I" is fine, but "I show that X" → just say X
- Make the object the subject: "Table 5 presents estimates" not "I present estimates in Table 5"
- No royal "we" — "we" means "you the reader and I"
- Simple words: "use" not "utilize," "several" not "diverse"
- No "I leave X for future research"
- Let the content speak for itself

---

## How to start a session

1. Read `process_log/pipeline_state.json`
   - If `status` is `"not_started"`: run data inventory (below), set to `"running"`, begin Stage 0
   - If `status` is `"running"`: read `current_stage` and continue from there
   - If `status` is `"complete"`: report that the pipeline is done
2. No human confirmation needed — just run

### Data inventory (runs once at pipeline start)

Before Stage 0, check what data sources are available. This prevents bad assumptions from cascading through the entire pipeline.

1. Read `.env` — check which credentials are present (non-placeholder values)
2. List `.claude/skills/` — check which data skills are installed
3. For each skill with authentication, verify credentials exist in `.env`:
   - FRED: `FRED_API_KEY` present and not `your-key-here`
   - WRDS: `WRDS_USER` and `WRDS_PASS` present and not placeholders
   - EDGAR: `SEC_EDGAR_NAME` and `SEC_EDGAR_EMAIL` present and not placeholders
   - Ken French: no auth needed (always available)
   - Chen-Zimmerman: no auth needed (always available)
4. Write results to `output/data_inventory.md`:

```markdown
# Data Inventory

## Available data sources
| Source | Status | What it provides |
|--------|--------|-----------------|
| FRED | ✓ configured | 800K+ macro/financial time series |
| WRDS | ✓ configured | CRSP (stock returns), Compustat (accounting), IBES (analysts), options, insider trading |
| EDGAR | ✓ configured | SEC filings (10-K, 10-Q, 8-K, proxy, insider trades) |
| Ken French | ✓ always available | Factor returns, portfolio sorts, breakpoints |
| Chen-Zimmerman | ✓ always available | 212 firm-level anomaly signals, portfolio returns |

## Implications for research design
[List what kinds of empirical work are possible given available data]
```

5. Commit: `pipeline: data inventory complete`

**CRITICAL:** All downstream agents must read `output/data_inventory.md` when making decisions about empirical feasibility. The idea-generator and idea-reviewer must know what data is available so they design ideas that USE available data, not work around imagined limitations. Never assume a data source is unavailable without checking the inventory.

---

## Documentation

The **scribe** agent runs in the background after each stage, logging:
- What happened (discussions, decisions)
- What was tried and failed (dead ends)
- The full pipeline history (`process_log/history.md`)

The scribe's role is pedagogical — recording the process for the AI-assisted research guide.
