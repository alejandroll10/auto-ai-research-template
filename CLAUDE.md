# CLAUDE.md — Autonomous Theory Paper Pipeline

## Purpose

This project autonomously produces a **finance theory paper** suitable for submission to a top-3 finance journal (JF, JFE, RFS). The system runs end-to-end with no human intervention after launch. Quality is enforced by adversarial evaluation at every stage.

The project also produces a **process log** documenting how the autonomous system worked, as a pedagogical record.

---

## How to launch

```bash
claude --dangerously-skip-permissions
```

Then say: **"Run the pipeline."**

The system reads this file, checks pipeline state, and continues from where it left off.

---

## Pipeline overview

```
Stage 0: Problem Discovery ──→ Gate 0: Problem Viability
Stage 1: Theory Generation  ──→ Gate 1: Math Audit
                                 Gate 2: Novelty Check
Stage 2: Implications       ──→
Stage 3: Self-Attack         ──→ Gate 3: Scorer Decision
                                   ├── ADVANCE → Stage 4
                                   ├── REVISE  → back to Stage 1 (max 2×)
                                   ├── REWORK  → back to Stage 1 new approach (max 2×)
                                   └── ABANDON → back to Stage 0 (max 3×)
Stage 4: Paper Writing       ──→
Stage 5: Style Check         ──→
Stage 6: Referee Simulation  ──→ Gate 4: Referee Decision
                                   ├── Minor/Accept → Done
                                   ├── Major Revision → back to Stage 4 (max 2×)
                                   └── Reject → back to Stage 1
```

---

## Pipeline state

State is tracked in `process_log/pipeline_state.json`. Read this file at session start. Update it after every stage transition. Commit after every update.

```json
{
  "current_stage": "stage_0",
  "problem_attempt": 1,
  "theory_attempt": 1,
  "revision_round": 0,
  "referee_round": 0,
  "status": "running",
  "scores": {},
  "history": []
}
```

---

## Stage 0: Problem Discovery

**Agent:** `literature-scout`

1. Choose a domain: asset pricing or corporate finance
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

## Stage 1: Theory Generation

**Agent:** `theory-generator`

1. Read `output/stage0/problem_statement.md` and `output/stage0/literature_map.md`
2. Choose strategy:
   - Attempt 1: fresh proposal
   - Attempt 2+: mutate (if previous attempt had good elements) or fresh with different approach
3. Launch theory-generator with the problem statement, literature map, and strategy
4. Save result to `output/stage1/theory_draft_vN.md` (N = attempt number)
5. Commit: `pipeline: stage 1 — theory v{N} generated`

### Gate 1: Math Audit

**Agent:** `math-auditor`

1. Launch math-auditor on `output/stage1/theory_draft_vN.md`
2. Save result to `output/stage1/math_audit_vN.md`
3. If FAIL:
   - Read the specific errors from the audit
   - Re-launch theory-generator in **mutate** mode with the draft + audit feedback
   - Max 3 audit attempts per theory version
   - If still failing after 3: treat as theory failure, increment theory_attempt
4. If PASS: proceed to Gate 2
5. Commit: `pipeline: gate 1 — math audit {PASS/FAIL}`

### Gate 2: Novelty Check

**Agent:** `novelty-checker`

1. Launch novelty-checker on `output/stage1/theory_draft_vN.md`
2. Save result to `output/stage1/novelty_check_vN.md`
3. If KNOWN: abandon this theory, return to Stage 1 with new approach
4. If INCREMENTAL: flag it, proceed with caution (scorer will weigh this)
5. If NOVEL: proceed to Stage 2
6. Commit: `pipeline: gate 2 — novelty {NOVEL/INCREMENTAL/KNOWN}`

---

## Stage 2: Implications

**Orchestrator task** (no separate agent needed — you do this)

1. Read the theory draft
2. Work out:
   - Testable predictions
   - Comparative statics
   - Special cases that recover known results
   - Economic intuition for each result
3. Append to the theory draft or write to `output/stage2/implications.md`
4. Commit: `pipeline: stage 2 — implications developed`

---

## Stage 3: Self-Attack

**Agent:** `self-attacker`

1. Launch self-attacker on the theory draft + implications
2. Save result to `output/stage3/self_attack_vN.md`
3. Commit: `pipeline: stage 3 — self-attack complete`

### Gate 3: Scorer Decision

**Agent:** `scorer`

1. Launch scorer with:
   - Theory draft: `output/stage1/theory_draft_vN.md`
   - Math audit: `output/stage1/math_audit_vN.md`
   - Novelty check: `output/stage1/novelty_check_vN.md`
   - Self-attack: `output/stage3/self_attack_vN.md`
2. Save result to `output/stage3/scorer_decision_vN.md`
3. Read the decision:

| Decision | Action |
|----------|--------|
| **ADVANCE** (75+) | Proceed to Stage 4 |
| **REVISE** (55-74) | Return to Stage 1 in mutate mode with scorer feedback. Max 2 revision rounds. |
| **MAJOR REWORK** (35-54) | Return to Stage 1 with fresh approach + scorer feedback. Max 2 rework rounds. |
| **ABANDON** (<35) | Increment theory_attempt. Return to Stage 1. After 3 abandons on same problem, return to Stage 0. |

4. Update pipeline_state.json accordingly
5. Commit: `pipeline: gate 3 — scorer {DECISION} (score: {N})`

---

## Stage 4: Paper Writing

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
3. Paper-writer updates `paper/main.tex` with `\input` commands
4. Commit: `pipeline: stage 4 — paper draft written`

---

## Stage 5: Style Check

**Agent:** `style`

1. Launch style agent on the paper
2. Read the style report
3. Fix all violations by editing the section files directly
4. Commit: `pipeline: stage 5 — style violations fixed`

---

## Stage 6: Referee Simulation

**Agent:** `referee`

1. Delete any previous reports in `paper/referee_reports/`
2. Launch referee agent (fresh context, no knowledge of development process)
3. Save report to `paper/referee_reports/YYYY-MM-DD_vN.md`
4. Commit: `pipeline: stage 6 — referee report received`

### Gate 4: Referee Decision

Read the referee's recommendation:

| Recommendation | Action |
|---------------|--------|
| **Accept / Minor Revision** | Fix minor comments, commit final version. Pipeline complete. |
| **Major Revision** | Revise the paper addressing major comments. Re-run Stages 5-6. Max 2 referee rounds. |
| **Reject** | Read the rejection reasons. If fixable: return to Stage 1 with referee feedback. If fundamental: return to Stage 0. |

Update pipeline_state.json with `"status": "complete"` when done.

Final commit: `pipeline: COMPLETE — paper ready for submission`

---

## Escalation rules (prevent infinite loops)

| Situation | After N failures | Action |
|-----------|-----------------|--------|
| Math audit fails | 3 attempts | Abandon this theory version |
| Theory scored REVISE | 2 rounds | Escalate to MAJOR REWORK |
| Theory scored MAJOR REWORK | 2 rounds | Escalate to ABANDON |
| Theory scored ABANDON | 3 theories on same problem | Change the problem (Stage 0) |
| Problem viability fails | 3 problems | Pick the best scoring problem and proceed anyway |
| Referee rejects | 2 rejections | Return to Stage 0 with entirely new topic |

---

## File organization

```
output/
├── stage0/
│   ├── problem_statement.md
│   └── literature_map.md
├── stage1/
│   ├── theory_draft_v1.md
│   ├── theory_draft_v2.md
│   ├── math_audit_v1.md
│   ├── math_audit_v2.md
│   ├── novelty_check_v1.md
│   └── novelty_check_v2.md
├── stage2/
│   └── implications.md
├── stage3/
│   ├── self_attack_v1.md
│   └── scorer_decision_v1.md
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

## Commit protocol

Commit after every stage transition. Commit messages use the prefix `pipeline:` so the full history is readable in `git log --oneline`.

The scribe agent runs in the background and commits with `scribe:` prefix for documentation updates.

---

## Domain: Finance Theory

### Asset pricing
- No-arbitrage / SDF framework as benchmark
- Risk premia must have an economic explanation
- Connection to observable objects (factors, portfolios, returns)
- Key question: what risk is being priced, and why?

### Corporate finance
- Modigliani-Miller as benchmark (what friction breaks it?)
- Standard frictions: agency, asymmetric info, incomplete contracts
- One friction at a time for clarity
- Key question: what friction matters, and what does it imply?

---

## Scoring criteria (used by scorer agent)

### Hard requirements (binary PASS/FAIL)

| # | Requirement |
|---|------------|
| H1 | One clear idea — contribution statable in one sentence |
| H2 | Well-defined setup — a reader can write down the agents' problem |
| H3 | Key result is mathematically correct (math audit passed) |
| H4 | The result is new (novelty check passed) |
| H5 | Economic mechanism is clear — why the result holds, in economics not algebra |

### Scored dimensions

| Dimension | Weight | Calibration |
|-----------|--------|-------------|
| Importance | 30% | CAPM-level = 100, minor extension = 20 |
| Novelty | 25% | New mechanism = 100, known mechanism in new setting = 40 |
| Rigor | 20% | Full proof = 100, clear with small gaps = 60, hand-waving = 20 |
| Parsimony | 15% | One-friction model = 100, kitchen-sink = 20 |
| Fertility | 10% | Reframes a literature = 100, dead-end result = 20 |

Threshold to advance: 75+

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
2. If state exists: report current stage and continue
3. If no state exists: initialize state and begin Stage 0
4. No human confirmation needed — just run

---

## Documentation

The **scribe** agent runs in the background after each stage, logging:
- What happened (discussions, decisions)
- What was tried and failed (dead ends)
- The full pipeline history (`process_log/history.md`)

The scribe's role is pedagogical — recording the process for the AI-assisted research guide.
