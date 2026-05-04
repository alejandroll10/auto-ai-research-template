# Identification Agent Pair — Design Spec

Synthesis of `identification_lit_finance.md` + `identification_lit_econ.md` into a concrete spec for the two new agents (issue #17).

## Where they live

- `extensions/empirical/agent_bodies/finance/identification-designer.md`
- `extensions/empirical/agent_bodies/finance/identification-auditor.md`
- Metadata: `extensions/empirical/agent_metadata/finance_agents.json` (alongside the existing `empiricist`)

These are finance-specific (variant: finance) per the architectural decision in issues #17/#18. Macro version is tracked separately in #18 and noted in `LIMITATIONS.md`.

## Where they fit in the pipeline

Stage 3a currently runs (per `extensions/empirical/docs/stage_3a_empirical.md`):

1. Plan: `empiricist` writes `empirical_plan.md`
2. Plan review (orchestrator judgment call — *this is the gap*)
3. Execute: `empiricist` runs analysis
4. Audit: `empirics-auditor` runs code, verifies results

New flow:

1. Plan: `empiricist` writes `empirical_plan.md` (unchanged; can reference designer's menu if available)
2. **Identification design** (new, optional first pass): `identification-designer` reads implications + data inventory + plan; produces `output/stage3a/identification_menu.md` — a ranked menu of identification strategies with assumptions, diagnostics, and estimands. The empiricist consumes this and revises the plan. Optional because for some plans (calibration-only, descriptive stats) identification is moot; the designer can return "N/A — no causal claim made."
3. **Identification audit** (new, gating): `identification-auditor` reads the (possibly revised) plan and returns PASS / REVISE / FAIL with a severity-ranked list of failure modes. FAIL/REVISE kicks back to empiricist for plan revision. PASS allows execute.
4. Execute: unchanged
5. Empirics audit: unchanged (runs code, checks results, checks methodology — but not identification, that's already gated)

This keeps `empiricist` and `empirics-auditor` doing what they're doing today; the new agents handle the identification layer that currently has no dedicated check.

## Auditor: scope of failure modes (extracted from lit scans)

These are the failure modes the auditor must check for, organized by design class. Each entry references the lit-scan source for the agent prompt.

### DiD (any flavor, including event studies in finance)
- TWFE with staggered adoption and no robust estimator (CS / Sun-Abraham / BJS / dCDH); no Goodman-Bacon decomposition (Baker-Larcker-Wang 2022)
- Pre-trends test treated as validation of parallel trends (Roth 2022); no power analysis; no HonestDiD sensitivity (Rambachan-Roth 2023)
- Functional-form-dependent parallel trends not addressed (Roth 2023)
- Continuous-treatment DiD without Callaway-Goodman-Bacon-Sant'Anna (2024) treatment

### Event studies (finance-specific)
- Cross-sectional dependence under date-clustered events without Kolari-Pynnonen correction
- Long-horizon BHARs without calendar-time portfolio approach (Fama 1998)
- Estimation window overlapping treatment / look-ahead bias

### Shift-share / Bartik
- No commitment to BHJ (shocks-view) vs. GPSS (shares-view); no diagnostic for whichever is claimed
- GPSS without Rotemberg weight table; BHJ without shock-level balance and shock-level clustering

### IV
- F > 10 cited under heteroskedasticity / clustering (use Olea-Pflueger effective F, ~23 threshold)
- Single IV without tF correction (Lee-McCrary-Moreira-Porter 2022) or Anderson-Rubin CIs
- Judge/examiner designs without Frandsen-Lefgren-Leslie exclusion + monotonicity test
- Verbal-only defense of exclusion restriction; no testable implication offered

### RD
- No manipulation test (rddensity, Cattaneo-Jansson-Ma 2020 — McCrary alone is now stale)
- Bandwidth selected ad hoc (no MSE-optimal / CER-optimal); no robust bias-corrected CIs (rdrobust)
- No covariate balance at cutoff
- No donut-hole / bandwidth-sensitivity robustness
- Geographic RD with multiple simultaneous boundary discontinuities not addressed
- Fuzzy RD with weak first stage at the bandwidth

### High-frequency identification (FOMC etc.)
- Raw rate surprises without information-effect handling (Jarociński-Karadi or Miranda-Agrippino-Ricco)
- No Bauer-Swanson (2023) predictability check / orthogonalization

### Bad controls / OLS without quasi-experiment
- Post-treatment / collider controls (Cinelli-Forney-Pearl 2024)
- No sensitivity analysis (Cinelli-Hazlett `sensemakr` preferred over Oster `psacalc`)
- "Robust to adding controls" treated as identification

### Synthetic control
- SC with many treated units (>10) without shift to synthetic DiD (Arkhangelsky et al. 2021) or gsynth
- Pre-period RMSPE not reported
- No permutation / placebo inference
- Treated unit poorly represented by convex combination of controls

### ML for causal inference
- DML used without a separate valid identifying assumption ("DML solves regularization bias, not endogeneity")
- Causal forest HTE without omnibus test (Chernozhukov-Demirer-Duflo-Fernández-Val GenericML)
- Heterogeneity exploration via sample splits without multiple-testing correction

### Asset pricing identification
- New factor proposed without Feng-Giglio-Xiu (2020) double-selection LASSO zoo test
- Two-pass Fama-MacBeth without Shanken correction or Giglio-Xiu three-pass for omitted factors
- Long-horizon predictability without bias adjustment (Stambaugh, Boudoukh et al. 2022) and bootstrap p-values
- Cross-sectional IV/DiD treating substitution patterns as exogenous (Haddad et al. 2025)

### Banking / regulation
- Threshold-based regulation (CCAR, SIFI) without manipulation test on running variable
- Staggered Dodd-Frank / Basel rollout treated as single date (Baker-Larcker-Wang)

### General hygiene
- Standard errors not clustered at treatment-assignment level
- Multiple outcomes with Bonferroni only (Romano-Wolf preferred)
- Attrition >5% without Lee bounds
- SUTVA assumed without spillover discussion

### Estimand vs. economic question
- LATE reported when ATE/ATT is what the theory predicts; no monotonicity discussion
- Sloczynski (2022) OLS-with-HTE weighting critique not addressed when groups are unbalanced
- "We identify the causal effect" without specifying *which* causal effect

## Designer: menu structure

Each strategy in the menu is one entry with:

- **Strategy name** (e.g., "Staggered DiD with Borusyak-Jaravel-Spiess imputation")
- **What variation it exploits** in the data inventory
- **Identifying assumptions** (each stated as something a referee can challenge)
- **Diagnostics required** (concrete tests the empiricist must run)
- **Estimand** (LATE / ATT / ATE / structural parameter — explicit)
- **What the theory actually predicts** (and whether the estimand matches)
- **Likely failure modes** (proactive — what the auditor would flag)
- **Software / code references** (rdrobust, did_imputation, sensemakr, etc.)
- **Confidence ranking** (1–5: how strong is this design for this question on this data?)

The designer must rank ≥3 strategies when feasible. If only one is workable (e.g., the data only supports a calibration check), the designer says so explicitly and explains why alternatives fail.

## Verdicts (auditor)

Match math-auditor's PASS/FAIL grammar with severity tiers (matches self-attacker convention):

- **PASS** — all design choices justified; assumptions explicit and testable; diagnostics specified; estimand matches theory's predicted object
- **REVISE** — fixable issues; specific concerns enumerated; empiricist re-plans
- **FAIL** — design cannot be fixed within the chosen strategy; recommend a different strategy from the designer's menu, or note that the question is not identifiable from the available data

For each concern: severity 1–10, the specific failure mode (named: e.g., "TWFE-staggered-no-robust-estimator", "weak-IV-stockyogo-misuse"), the quoted plan text, the fix.

## Notes
- Both agents are advisory-on-identification only. They do not run code, fetch data, or estimate anything (that's empiricist + empirics-auditor).
- Macro identification is explicitly out of scope (issue #18). If the auditor encounters a macro-style design (SVAR, sign restrictions, narrative shocks, calibrated DSGE-as-identification), it must flag "out of scope — macro identification not yet supported in this variant" rather than apply finance/applied-micro standards inappropriately.
