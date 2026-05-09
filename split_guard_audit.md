# Split-Guard Audit — scorer-core.md third pass

**Verdict: PASS-WITH-FIXES**

---

## Issue List

### ISSUE 1 — Severity: HIGH — Exception-scope ambiguity under empirical-first + formal methods paper

**Location:** `scorer-core.md` lines 28–33 (both injected blocks)

Under empirical-first mode, both blocks fire. The universal block says exceptions (a)(b)(c) can save a paper. The empirical-first block says "(a)/(b)/(c) exceptions do not apply for non-causal-estimand drift."

The critical collision: a paper under empirical-first whose contribution is a formal methodological result (exception c — a new estimator with proved properties) simultaneously:
- Passes the universal guard (exception c exempts it from own-design-critique fail)
- Fails the empirical-first guard ("(a)/(b)/(c) exceptions do not apply")

The two blocks produce contradictory verdicts for this paper class. The scorer has no tiebreaker. In practice the scorer will likely resolve this by reading the empirical-first block last and treating it as overriding — failing the paper. But that may not be the intended outcome: a paper proving a new DID estimator under empirical-first is a legitimate contribution, and the empirical-first block should arguably exempt formal methods results even there.

**Fix direction:** Either (a) add a carve-out to the empirical-first block: "Exception: (c) still applies — a formal methodological result with proved properties is not causal-estimand drift even under empirical-first"; or (b) make the empirical-first block's prohibition explicit about the non-(c) drift classes only ("drift to descriptive fact, calibration, predictive horserace, or dataset release — exceptions (a)/(b) do not apply"). Option (b) is cleaner and closes the issue without weakening empirical-first for the cases that actually matter.

---

### ISSUE 2 — Severity: LOW — Missing blank line between EXT_EMPIRICAL_END and EMPIRICAL_FIRST_START markers

**Location:** `scorer-core.md` lines 30–31

The two marker pairs are adjacent with no separator:

```
<!-- EXT_EMPIRICAL_END -->
<!-- EMPIRICAL_FIRST_START -->
```

The resolver strips both sets of markers independently, in order. In the `finance + ext empirical` deploy (xe=1, ef=0): the EXT_EMPIRICAL markers are stripped (content kept), then the entire EMPIRICAL_FIRST block is strip-removed. This leaves the kept EXT_EMPIRICAL content abutting whatever follows — no blank line between the own-design-critique paragraph and "If ANY hard requirement fails." This is cosmetic but can read as one run-on block. Low priority.

---

### ISSUE 3 — Severity: MEDIUM — "dataset release" not explicitly named in universal guard

**Location:** `scorer-core.md` line 28 (universal block)

Victor-1's structure was: (1) we release an EDGAR pipeline (precision 0.80, recall 0.31, F1 0.44); (2) per-cohort placebos show 14/16 cells fail their own benchmark.

Walk-through against the new universal text: "If the paper's main contribution is primarily a methodological warning, measurement caveat, standard-error correction, or methods checklist about *this paper's own analysis or data pipeline*..."

- Contribution (2) — "our placebos fail" — is a methodological warning about this paper's own analysis. **Caught.** H1/H5 fail unless exception applies. Exception (c) requires "formal methodological result with proved properties" — a failure rate of 14/16 placebos is not a proved theorem. Exceptions (a) and (b) require operator opt-in or external replication changing a published conclusion. Neither applies. **Guard fires correctly for contribution (2).**

- Contribution (1) — "we release a pipeline with precision 0.80" — is a dataset/pipeline release. The current text does not name "dataset release" as a trigger. "Methods checklist about this paper's own data pipeline" is close, but a scorer could read the EDGAR pipeline as a standalone reusable tool (not exclusively about "this paper's analysis") and let it through. The prior text explicitly named "dataset release as a headline" as a failure mode; removing it creates an ambiguity.

**Fix direction:** Add "dataset or pipeline release (where the release itself is the claimed contribution)" to the list of trigger modes in the universal block. This closes the gap without resurrecting the prior "descriptive fact" language.

---

### ISSUE 4 — Severity: LOW — Cross-file coherence for exception (c): fully consistent

**Location:** `puzzle-triager.md` line 83, `stage_puzzle_triage.md` line 9, `scorer-core.md` line 28

Exception (c) is ungated in both puzzle-triager files and ungated in the universal block of scorer-core.md. The empirical-first block in scorer-core.md does not redefine (c) for the triager — the triager files do not carry EMPIRICAL_FIRST markers. So (c) at triager level is universally available, which matches (c) being in the universal scorer block. The only inconsistency is the collision in Issue 1 above, which is confined to the scorer. No spurious gating found.

---

### ISSUE 5 — Severity: NONE — Resolver behavior: correct

**Location:** `setup.sh` lines 1542–1551

Three deploy classes:

- **Finance only** (xe=0, ef=0): EMPIRICAL_FIRST block stripped entirely, EXT_EMPIRICAL block stripped entirely. Both guards disappear. Correct — theory-first, no empirical extension.
- **Finance + ext empirical** (xe=1, ef=0): EXT_EMPIRICAL markers stripped (content kept), EMPIRICAL_FIRST block stripped entirely. Universal guard present, causal-estimand guard absent. Correct — this is the victor-1 target scenario.
- **Finance + mode empirical-first** (ef=1, xe=1 — the comment at line 1521 confirms ef=1 implies xe=1): THEORY_FIRST block stripped, EMPIRICAL_FIRST markers stripped (content kept), EXT_EMPIRICAL markers stripped (content kept). Both guards present. Correct.

No double-removal or marker leak. The patterns are applied in order, and no pattern's output is an input to a subsequent pattern (markers are stripped by separate regexes). The `\n{0,2}` optional-newline suffix handles EOF edge cases correctly.

---

## Victor-1 walkthrough summary

| Contribution | Guard triggered? | Exception available? | Outcome |
|---|---|---|---|
| (2) "14/16 placebos fail own benchmark" | Yes — "methodological warning about this paper's own analysis" | No (c) requires proved theorem) | H1/H5 FAIL — correct |
| (1) "EDGAR pipeline, F1=0.44" | Ambiguous — "dataset release" not named explicitly | No | Depends on scorer's reading — **gap (Issue 3)** |

The guard catches the primary victor-1 failure (contribution 2). Contribution 1 is only partially caught. Issue 3 is the remaining leak.

---

## Required fixes (priority order)

1. **Issue 1 (HIGH):** Resolve exception-(c) collision under empirical-first. Add "this prohibition does not apply to exception (c) — a formal methodological result with proved properties is not causal-estimand drift" to the empirical-first block, or restrict the prohibition explicitly to non-(c) drift classes.

2. **Issue 3 (MEDIUM):** Re-add "dataset or pipeline release as the paper's primary claimed contribution" to the universal block trigger list. One phrase, not a paragraph.

3. **Issue 2 (LOW):** Add a blank line between `<!-- EXT_EMPIRICAL_END -->` and `<!-- EMPIRICAL_FIRST_START -->` in scorer-core.md for readability.
