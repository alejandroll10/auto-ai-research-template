# Audit: EXT_EMPIRICAL resolver change

## Verdict

**PASS-WITH-FIXES.** The change is structurally correct: `EXT_EMPIRICAL_ON` is derived from `EXTENSIONS` (not `MODE`), the resolver pattern list handles both keep and strip cases without double-resolution or cross-marker interference, `update.sh` round-trips the new marker transparently because it reconstructs the flag set from the manifest and re-runs `setup.sh`, and the file paths in the guard text are consistent with every source in `extensions/empirical/`. One existing regex edge case (markers at EOF with no trailing newline) leaves residual HTML in the output, and one pre-existing misclassification in `stage_4.md` becomes more visible now that the EXT_EMPIRICAL path exists.

---

## Issues found

**1. [minor] EOF no-trailing-newline regex miss — `setup.sh:~1546–1548`**

All three strip-mode patterns (`EMPIRICAL_FIRST`, `THEORY_FIRST`, `EXT_EMPIRICAL`) require a `\n` after the closing marker: `<!-- …_END -->\n\n?`. If a marker appears at the very end of a file with no trailing newline, neither the strip-case nor the keep-case pattern matches the END marker, leaving `<!-- EXT_EMPIRICAL_END -->` (or its siblings) as literal HTML in the deployed file. The current `scorer-core.md` is safe (has `\nIf ANY…` after the END marker), but any future agent body that puts an `EXT_EMPIRICAL` block at EOF will silently leak the marker. This bug predates this change (same pattern used for `EMPIRICAL_FIRST`/`THEORY_FIRST`); the new `EXT_EMPIRICAL` inherits it.

**Fix direction:** change the END-line patterns to `\n?` (optional newline) both in the keep variant (`<!-- EXT_EMPIRICAL_(?:START|END) -->\n?`) and the strip variant (`<!-- EXT_EMPIRICAL_END -->\n?\n?`). Apply the same fix to all three marker families for consistency.

**2. [minor] `stage_4.md` branch-manager inputs missing under theory-first `--ext empirical` — `templates/shared/docs/stage_4.md:55–57`**

Lines 55–57 tell the orchestrator to pass `identification_audit.md` and `empirics_audit.md` to `branch-manager`, but this block is wrapped in `<!-- EMPIRICAL_FIRST_START/END -->` so it is stripped in theory-first deploys. Under theory-first `--ext empirical` those files are produced at Stage 3a and are material inputs for the branch-manager decision. The omission predates this change; this change makes it more conspicuous because the scorer now correctly fires its causal-design guard while branch-manager is simultaneously blind to the audits.

**Fix direction:** replace the `EMPIRICAL_FIRST` marker on that block with `EXT_EMPIRICAL`, since the empirical audit inputs exist whenever the empirical extension is present regardless of mode. The wording "(the freeform-audit equivalent under empirical-first; no `output/stage2/freeform_audit_*.md` exists)" is mode-specific; under theory-first both audit files and freeform audit exist, so the text would need a minor adjustment.

---

## Notes

- **No double-resolution risk.** No file in `templates/` or `extensions/` carries both `EXT_EMPIRICAL` and `EMPIRICAL_FIRST` markers. The resolver is called exactly once (line 1533). Assembly runs at line 681, placeholder injection at ~1348, resolver at 1533 — ordering is correct.
- **`ef=1` implies `xe=1`.** `--mode empirical-first` auto-adds `--ext empirical` at line 124, so `EMPIRICAL_FIRST_ON=1` always implies `EXT_EMPIRICAL_ON=1`. The causal-design guard is therefore kept under empirical-first and the block's internal `--mode empirical-first` path hint fires correctly.
- **update.sh round-trip is clean.** The manifest records both `mode` and `extensions` (lines 1633, 1635). `update.sh` reads both and passes them back to `setup.sh` as `--mode` and `--ext` flags (lines 215–216), so `EXT_EMPIRICAL_ON` is re-derived correctly on every update.
- **Guard paths are correct.** `output/stage1/identification_design.md` (empirical-first) and `output/stage3a/identification_menu.md` (theory-first ext empirical) are confirmed against `extensions/empirical/docs/stage_3a_empirical.md` lines 35, 43, and `extensions/empirical/agent_bodies/finance/identification-designer.md` line 15.
- **All `EMPIRICAL_FIRST` blocks reviewed (question 4).** Every block examined is genuinely mode-specific: Gate 2 skip, mechanism-mode theory-generator notes, Stage 1 identification design step, Stage 2b skip, LaTeX section differences, and branch-manager audit inputs. None carries logic that should activate for all `--ext empirical` deploys — except item 2 above.
