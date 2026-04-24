# Stage 6: Referee Simulation

**Agents:** `referee` + `referee-freeform` + `referee-mechanism` (launched in parallel — none sees the others' output)

Three referees with distinct mandates read the same paper cold. The structured `referee` gives a top-journal referee report with numbered comments and action tags. The `referee-freeform` gives an editorial publishability assessment — forest, not trees. The `referee-mechanism` evaluates whether the paper's economic mechanism actually delivers the claimed result through the claimed channel (complementary to math-auditor, which checks proof correctness at Gate 2 — mechanism referee checks whether the economics the paper invokes is the economics the math supports).

1. Delete any previous referee reports in `paper/referee_reports/` matching the pattern `*_v*.md` (i.e., `YYYY-MM-DD_vN.md`, `..._vN_freeform.md`, and `..._vN_mechanism.md`).
2. Launch all three referees in parallel (fresh context, no knowledge of development process). Provide save paths:
   - structured → `paper/referee_reports/YYYY-MM-DD_vN.md`
   - freeform → `paper/referee_reports/YYYY-MM-DD_vN_freeform.md`
   - mechanism → `paper/referee_reports/YYYY-MM-DD_vN_mechanism.md`
3. Commit after all three complete.
4. Commit: `pipeline: stage 6 — referee reports received (structured + freeform + mechanism)`

## Gate 5: Referee Decision

Read all three referee reports. The structured referee provides numbered comments with action tags; the free-form referee provides editorial assessment and publishability verdict; the mechanism referee provides a verdict on whether the paper's economic mechanism is valid / partial / misattributed / decorative, plus tagged comments of its own.

**Hard rules driven by the mechanism verdict.** The mechanism verdict interacts with core.md's never-abandon rule (once a paper exists at Stage 5+, the pipeline must produce a finished paper via the extension playbook, not loop back to Stage 0). The rules below are compatible with never-abandon: neither MECHANISM-MISATTRIBUTED nor MECHANISM-DECORATIVE forces Stage 0. Instead, both route the paper through a mandated restructure-or-narrow path that respects the never-abandon envelope.

- **MECHANISM-VALID** — normal Gate 5 flow.
- **MECHANISM-PARTIAL** — normal Gate 5 flow; the mechanism referee's `[FIX]` items join the other two reports' `[FIX]` items in triage.
- **MECHANISM-MISATTRIBUTED** — forces **Major Revision** as the Gate 5 recommendation, overriding Minor/Accept from the other two referees. The paper must be rewritten around the actual driver the mechanism referee identified. The mechanism report's `[FIX]` items are **locked** — the triager cannot downgrade them under this verdict (see triager rule 3). Revision happens within the never-abandon envelope: the existing paper draft is restructured, not discarded. Extension playbook applies if the new driver needs added mathematical content.
- **MECHANISM-DECORATIVE** — forces **Major Revision with restructure-or-narrow mandate**, overriding Minor/Accept. DECORATIVE does NOT force Reject, and does NOT route to Stage 0 — both would violate never-abandon. Instead, the theory-generator is given one of two explicit mandates (orchestrator chooses based on content the paper delivers): (a) **restructure** — use the extension playbook to find real economic content the simple model was hiding, and rebuild the paper's mechanism claim around it; or (b) **narrow** — strip the mechanism framing and present the paper as a structural characterization of the identity the math actually delivers (scientist-first: a correct narrow claim beats a broad decorative one). If after the 10-round cap the verdict remains DECORATIVE, the paper ships with the narrow framing per (b) and a limitations paragraph documenting the original mechanism claim's failure. All mechanism `[FIX]` items are locked (see triager rule 3).

| Recommendation (from structured + freeform, subject to mechanism overrides above) | Action |
|---------------|--------|
| **Accept / Minor Revision** | Fix minor comments, proceed to Stage 7 (style check). Only reachable with MECHANISM-VALID or MECHANISM-PARTIAL. Under MISATTRIBUTED or DECORATIVE, the mechanism override promotes this recommendation to Major Revision. |
| **Major Revision / Revise and Resubmit** | **Triage first.** Launch `triager` with: inputs = all three current-round referee reports (structured + freeform + mechanism), output path = `paper/referee_reports/triage_rN.md` (N = `referee_round`), context = `gate-5`. Triager applies the rules (no silent downgrade of referee `[FIX]`, written justifications for downgrades, mechanism-report `[FIX]` items under MECHANISM-MISATTRIBUTED or MECHANISM-DECORATIVE are locked per triager rule 3) and judges each round on its merits. Do not edit the triager's output — if you disagree, re-launch with explicit instructions, do not silently override. Then revise only the `[FIX]` items. Under MISATTRIBUTED, the revision must rewrite around the actual driver. Under DECORATIVE, pick the restructure-or-narrow path from the rules above and pass the chosen mandate to the theory-generator / paper-writer. When a referee challenges an assumption, first try to prove the result without it or characterize exactly when it fails — weakening claims is the last resort (per "characterize, don't just prove"). **Increment `referee_round` in `pipeline_state.json` before re-running Stage 6.** Re-run Stage 6. Max 10 rounds (i.e., stop when `referee_round >= 10`); keep going as long as the triager reports any `[FIX]` items in the current round (the triager is stateless — it does not distinguish "new" from "carried forward"; any `[FIX]` indicates outstanding work). |
| **Reject** | Read the rejection reasons. If fixable and no paper draft exists yet: return to Stage 2 with referee feedback. If a paper draft exists (Stage 5+): never-abandon applies — treat Reject as Major Revision with extension-playbook mandate instead. If fundamental *and* no paper draft exists: return to Stage 0. MECHANISM-DECORATIVE does NOT route here; it is handled by the Major Revision row above. |

{{SEED_OVERRIDE_STAGE_6_GATE_5}}
