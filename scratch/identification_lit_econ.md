# Identification Frontier in Applied Micro / Labor / Development / Public Econ (2020–2026)
## Reference Document for identification-designer + identification-auditor Agents

*Compiled May 2026. Covers AER, QJE, Econometrica, ReStud, JPE, JEL, JEP, ARE, and NBER WPs.*

---

## 1. Difference-in-Differences: The Post-TWFE World

### What broke (and when)

Two-way fixed effects (TWFE) with a single treatment indicator was the dominant DiD estimator for 20+ years. Four papers published together in the *Journal of Econometrics* in 2021 showed it is generically biased when treatment effects are heterogeneous across cohorts or time: the TWFE estimate is a weighted average of "clean" 2x2 DiD comparisons, but some weights are **negative** (late-adopters used as implicit controls for early-adopters, then roles reversed). The entire staggered-adoption literature post-2021 is a response to this.

### Key papers

| Paper | Journal | Year | Takeaway |
|---|---|---|---|
| Callaway & Sant'Anna | *J Econometrics* 225(2):200-230 | 2021 | Defines group-time ATTs; aggregates them without negative weights; requires never-treated or not-yet-treated controls |
| Goodman-Bacon | *J Econometrics* 225(2):254-277 | 2021 | Variance-weighted decomposition of TWFE into clean 2x2s; use as a diagnostic, not an estimator |
| Sun & Abraham | *J Econometrics* 225(2):175-199 | 2021 | Interaction-weighted estimator; clean identification of dynamic effects; nearly identical to CS in large samples |
| de Chaisemartin & D'Haultfoeuille | *AER* 110(9):2964-2996 | 2020 | First formal proof of negative weights in TWFE; proposes did_multiplegt estimator |
| Borusyak, Jaravel & Spiess | *ReStud* 91(6):3253-3285 | 2024 | "Imputation estimator": fit Y(0) on never/not-yet-treated, impute counterfactuals; efficient under parallel trends |
| Roth, Sant'Anna, Bilinski & Poe | *J Econometrics* 235(2):2218-2244 | 2023 | **The synthesis survey**; practitioners' guide to the whole literature |

### Current standard (2024+)

- **Must** use one of the heterogeneity-robust estimators: Callaway-Sant'Anna (`csdid`), Sun-Abraham (`eventstudyinteract`), Borusyak-Jaravel-Spiess (`did_imputation`), or de Chaisemartin-D'Haultfoeuille (`did_multiplegt`). TWFE event-study alone is now insufficient.
- **Must** present a **Goodman-Bacon decomposition** as a diagnostic to show the weight structure.
- For continuous treatments: Callaway, Goodman-Bacon & Sant'Anna (NBER WP 32117, 2024) extends the framework; using log-log specifications and controlling for dose with a single OLS coefficient is no longer acceptable.
- **Stacked DiD** (Cengiz et al. 2019 popularized; Wing et al. NBER WP 32054, 2024 formalizes): builds clean 2x2 cohort datasets and stacks them; widely used as robustness, especially in labor/public econ.

### Pre-trends: the testing trap

- Roth (2022, *AER:Insights* 4(3):305-322): pre-trends tests have **low power** in most empirical applications; passing a pre-trend test does not validate parallel trends. Conditioning analysis on passing a pre-test distorts inference (biases estimates, under-covers). Report the `pretrends` power calculations.
- Rambachan & Roth (2023, *ReStud* 90(5):2555-2591): **Honest DiD** / HonestDiD package. Replace "parallel trends holds exactly" with "post-treatment trend violations are bounded relative to pre-treatment violations." Report sensitivity to M (the smoothness parameter). This is now expected in top journals.
- Extended event windows: present relative-time coefficients for at least 4 periods before and after treatment; normalize to -1; do NOT normalize to 0 or drop the first pre-period as "the" base.

### Red-flag phrases

- "We verify parallel trends by testing pre-trends" (fails Roth 2022 critique)
- "We use a two-way fixed effects model with a post x treated indicator" (TWFE without heterogeneity-robustness)
- "We include unit and time fixed effects" (same)
- "The coefficient is negative, but [economic rationale]" without checking for negative weights
- "We stack clean 2x2 designs" without a formal stacking procedure
- Presenting only the time-average treatment effect without decomposing by cohort

---

## 2. Regression Discontinuity: The Full Toolkit

### What the literature requires now

Calonico, Cattaneo & Titiunik (2014, *Econometrica*) established robust bias-corrected (RBC) inference as the default. The 2022 Annual Review of Economics survey (Cattaneo & Titiunik, *ARE* 14:821-851) codifies current best practice. A paper that does not implement RBC is immediately flagged.

### Key papers

| Paper | Journal | Year | Takeaway |
|---|---|---|---|
| Calonico, Cattaneo & Titiunik | *Econometrica* 82(6):2295-2326 | 2014 | RBC inference: use MSE-optimal bandwidth but report bias-corrected CIs; `rdrobust` |
| Calonico, Cattaneo & Farrell | *Econometrics Journal* 23(2):192-210 | 2020 | Inference-optimal bandwidth; separates bandwidth for estimation vs. inference |
| Cattaneo, Jansson & Ma | *JASA* 115(531):1449-1455 | 2020 | Local polynomial density estimator; supersedes McCrary (2008) for manipulation testing; `rddensity` |
| Cattaneo & Titiunik | *ARE* 14:821-851 | 2022 | **Full review**; continuity vs. local randomization frameworks; validation toolkit |
| Keele & Titiunik | *Political Analysis* 23(1):127-155 | 2015 | Geographic RD critiques; multiple simultaneous boundary discontinuities; sorting along boundary |

### Current standard

- Use `rdrobust` with `rdbwselect` (MSE-optimal or CER-optimal bandwidth). Report both conventional and RBC CIs.
- **Always** run `rddensity` (Cattaneo-Jansson-Ma) to test for density discontinuity at the cutoff. McCrary (2008) test alone is now considered outdated (worse size properties).
- Report a **covariate balance table** at the cutoff: baseline characteristics should be continuous through the cutoff.
- Report sensitivity to bandwidth: half-bandwidth, double-bandwidth, and the donut-hole test (dropping observations very close to the cutoff to address heaping/bunching).
- **Fuzzy RD** with weak first stage: must test instrument strength at the cutoff; cannot have F-stat < 10 in the local window. If first stage is weak in the relevant bandwidth, the fuzzy RD is invalid.
- **Geographic/spatial RD**: must address (a) multiple laws changing at the boundary simultaneously (boundary composition critique), (b) spatial spillovers across the boundary, (c) sorting along the boundary. Geographic RD papers without placebo boundaries or falsification with non-discontinuous outcomes face high rejection risk.
- **Multi-cutoff RD**: normalize scores across cutoffs or analyze each cutoff separately; pooling without normalization conflates different local populations.

### Red-flag phrases

- "We use a local linear regression at the discontinuity" without specifying bias correction or bandwidth selection procedure
- "We conduct a McCrary density test" (replaced by rddensity)
- "The treatment effect is identified by the sharp discontinuity" without any manipulation test
- Bandwidth selected by eye or rule of thumb (e.g., ±5 percentile points) without MSE/CER-optimal method
- No donut-hole sensitivity test in settings with obvious heaping (round numbers, age cutoffs, test scores)

---

## 3. Instrumental Variables: Frontier Practice

### Weak instruments: the current standard

Andrews, Stock & Sun (2019, *Annual Review of Economics* 11:727-753): the definitive survey. Key update: **heteroskedasticity-robust first-stage F-statistics matter differently from the Staiger-Stock (1997) F>10 rule**. With heteroskedastic/clustered errors, the effective F-statistic (Olea-Pflueger 2013 or Andrews 2018 "non-homoskedastic" critical values) should be used. The F>10 rule applies only under homoskedasticity.

Angrist & Kolesár (2024, *J Econometrics* 240): "One Instrument to Rule Them All." In **just-identified IV** (one instrument), median bias is small and conventional inference likely reliable; the problem is primarily with over-identified or many-instrument settings. Pretesting on first-stage F exacerbates bias.

| Paper | Journal | Year | Takeaway |
|---|---|---|---|
| Andrews, Stock & Sun | *ARE* 11:727-753 | 2019 | Survey; use effective F, not Staiger-Stock; AR test for weak-IV-robust inference |
| Olea & Pflueger | *J Business & Econ Stat* 31(3) | 2013 | Effective F-statistic robust to heteroskedasticity and clustering |
| Angrist & Kolesár | *J Econometrics* 240 | 2024 | Just-ID IV bias is small; do not pretest on F |
| Lee, McCrary, Moreira & Porter | *J Econometrics* | 2022 | Valid t-tests after weak-instrument pretesting; confidence sets always valid |

### Shift-share (Bartik) instruments: now requires full disclosure

Two competing identification frameworks, now mandatory to state which one you're using:

**Exogenous shocks view (BHJ)**: Borusyak, Hull & Jaravel (*ReStud* 89(1):181-213, 2022). Identification from quasi-random shock assignment; shares can be endogenous. Must: (a) show shocks are plausibly exogenous, (b) run shock-level balance tests, (c) cluster at the shock level. Practical guide: Borusyak, Hull & Jaravel (*JEP* 39(1):181-204, 2025).

**Exogenous shares view (GPSS)**: Goldsmith-Pinkham, Sorkin & Swift (*AER* 110(8):2586-2624, 2020). Identification from plausibly exogenous initial shares; shocks affect weighting. Must: (a) use Rotemberg weights to see which industries drive identification, (b) test share exogeneity for the dominant industries, (c) run industry-level balance.

A paper that uses a Bartik instrument and does not explicitly address which identification view it takes **will be rejected at top journals**.

### Judge/examiner designs

Frandsen, Lefgren & Leslie (*AER* 113(1):253-277, 2023): "Judging Judge Fixed Effects." Proposes a nonparametric test of **both** the exclusion restriction and monotonicity for judge IV designs. Key finding: the standard "residualized judge leniency" approach fails when judges differ on case types, not just stringency. The test examines whether the conditional expectation of outcome given judge propensity is continuous with bounded slope.

Chyn, Frandsen & Leslie (*JEL* 63(2):401-439, 2025): comprehensive practitioner's guide to examiner/judge designs. Now the required reference for any such paper.

| Paper | Journal | Year | Takeaway |
|---|---|---|---|
| Frandsen, Lefgren & Leslie | *AER* 113(1):253-277 | 2023 | Nonparametric test of exclusion + monotonicity in judge designs |
| Chyn, Frandsen & Leslie | *JEL* 63(2):401-439 | 2025 | Full practitioner guide to examiner designs |
| Borusyak, Hull & Jaravel | *ReStud* 89(1):181-213 | 2022 | Shift-share: exogenous-shocks identification framework |
| Goldsmith-Pinkham, Sorkin & Swift | *AER* 110(8):2586-2624 | 2020 | Shift-share: exogenous-shares (Rotemberg weights) framework |

### Red-flag phrases

- "First-stage F = 12, so instruments are not weak" (Staiger-Stock with clustered/heterosk. data; must use effective F or AR test)
- "We use the Bartik instrument, which is exogenous because national trends are exogenous" (neither framework properly stated)
- "We use multiple judges as instruments" without testing exclusion/monotonicity (Frandsen et al. critique)
- "We instrument with [variable] which is exogenous because of geography" without any test of the exclusion restriction
- Reporting only the reduced-form and first-stage without discussing the structural interpretation

---

## 4. Sensitivity Analysis and Partial Identification

### Omitted variable bias sensitivity: now expected

Oster (2019, *J Business & Econ Stat* 37:187-204): `psacalc` in Stata. Estimates the degree of selection on unobservables relative to observables required to explain away the result, assuming proportional selection. Widely used but has known limitations.

Cinelli & Hazlett (2020, *J Royal Stat Soc Series B* 82(1):39-67): `sensemakr` package. More general framework: the **robustness value (RV)** is the minimum partial R² that confounders must have with both treatment and outcome to change conclusions. Allows formal benchmarking against observed covariates. This is increasingly preferred over Oster at top journals because it does not require the proportional selection assumption and gives intuitive partial R² interpretations.

### Partial identification (Manski-style bounds)

When point identification fails or assumptions are questionable, Manski-style bounds are acceptable if stated clearly. Key principle: **report worst-case bounds first, then progressively tighten under additional assumptions**. The common failure mode is assuming point identification when only interval identification holds (e.g., with attrition or missing data).

Molinari (2020, *Handbook of Econometrics* Vol. 7A): comprehensive review of partial identification. Tamer (*Annual Review of Economics* 2010) is the accessible introduction.

Kline & Tamer (*Annual Review of Economics* 2023): "Recent Developments in Partial Identification." Covers sharp bounds, inference in partially identified models, and when credible intervals are achievable.

### Inference on winners / multiple testing and specification search

Andrews, Kitagawa & McCloskey (*ReStud* 2023): "Inference on Winners." When the empirical strategy was selected (e.g., best instrument, best specification) from a set of candidates, standard inference is invalid. Provides uniformly valid confidence sets post-selection. Relevant for papers where identification strategy was chosen because it "worked."

### What top journals now expect in robustness

1. Oster (2019) or Cinelli-Hazlett (2020) sensitivity for OLS-based estimates.
2. HonestDiD sensitivity (Rambachan-Roth) for DiD estimates.
3. For RD: donut-hole, bandwidth sensitivity, placebo cutoffs.
4. For IV: Anderson-Rubin confidence sets (weak-IV-robust), or at minimum the effective F-statistic.
5. Placebo/falsification tests with outcomes that should NOT be affected.

### Red-flag phrases

- "Results are robust to adding controls" (adding controls does not address selection on unobservables)
- Sensitivity analysis limited to "coefficient stable across specifications" without Oster/Cinelli-Hazlett
- Bounds reported but no inference procedure given for the identified set
- "The instrument is strong" (F=15) without effective F or AR test

---

## 5. Synthetic Control Methods

### Current practice

Abadie (*JEL* 59(2):391-425, 2021): **the definitive practitioner's guide**. When to use SC vs. DiD: SC is preferred when (a) a small number of treated units (1-5), (b) pre-treatment period is long (many pre-periods), (c) the synthetic control achieves good pre-treatment fit. If fit is poor, SC estimates are unreliable. SC is not suitable for many treated units.

Arkhangelsky, Athey, Hirshberg, Imbens & Wager (*AER* 111(12):4088-4118, 2021): **Synthetic DiD**. Combines SC unit weights with DiD time weights. Key advantage: valid when neither pure SC nor pure DiD holds alone; provides a regularized estimator with formal large-sample inference. Does NOT require a single treated unit; works with multiple treated units.

Ben-Michael, Feller & Rothstein (*JASA* 116(536):1789-1803, 2021): **Augmented SC (ASCm)**. When pre-treatment fit is imperfect, debias the SC estimate using an outcome model. Bridges SC and synthetic DiD.

Xu (*Political Analysis* 25(1):57-76, 2017): **Generalized SC (gsynth)**. Factor model allowing multiple treated units and time-varying confounders. Widely used in political science; now common in economics.

| Paper | Journal | Year | When to use |
|---|---|---|---|
| Abadie | *JEL* 59(2):391-425 | 2021 | Guide; use SC when N_treated = 1-5, long pre-period |
| Arkhangelsky et al. | *AER* 111(12):4088-4118 | 2021 | Synthetic DiD: multiple treated, formal inference |
| Ben-Michael et al. | *JASA* 116(536):1789-1803 | 2021 | Augmented SC: debias when pre-fit is imperfect |
| Xu | *Political Analysis* 25(1):57-76 | 2017 | gsynth: many treated, factor model |

### When SC beats DiD, and vice versa

SC beats DiD: single/few treated units, long pre-period, post-treatment extrapolation well-grounded in pre-period fit. DiD beats SC: many treated units, short pre-period, parallel trends more plausible than factor model. Synthetic DiD: the middle ground when neither assumption fully holds.

### Red-flag phrases

- Using SC with many treated units (>10) without noting the shift to synthetic DiD or gsynth
- Reporting SC estimates without showing the pre-period fit quality (RMSPE)
- Claiming SC "validates" the counterfactual without permutation inference (placebo tests)
- Using SC when the treated unit is not well-represented by convex combinations of control units

---

## 6. Heterogeneous Treatment Effects and Machine Learning

### The double ML revolution

Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey & Robins (*Econometrics Journal* 21:C1-C68, 2018): **Double/Debiased ML (DML)**. Removes regularization bias from ML estimators for low-dimensional target parameters (ATE, LATE, PLM coefficients) by using cross-fitting and orthogonal scores. Now a mainstream tool for estimating ATEs when many covariates are present. The `DoubleML` package (Python/R) implements this.

Chernozhukov, Demirer, Duflo & Fernández-Val (NBER WP 24678; published *ECMA* 2024): **Generic ML (GenericML)**. Tests for heterogeneous treatment effects using ML proxies; constructs best linear predictors of CATEs; valid inference on heterogeneous effects in RCTs. Key: produces valid standard errors via half-sample cross-fitting.

Athey & Wager (*JASA* 113(523), 2018; *Annals of Statistics* 47(2), 2019): **Causal forests** via the `grf` package. Pointwise consistent, asymptotically normal CATE estimators. Valid Neyman-orthogonal local regression. Now widely used for heterogeneity exploration in RCTs and observational studies.

### What is publishable vs. exploratory

**Publishable at top journals**: (1) Testing *whether* HTE exist using Chernozhukov et al. generic ML with valid inference; (2) Estimating CATE as a secondary finding conditional on the main ATE result; (3) Policy learning (Athey-Wager 2021 *ReStud*) for optimal treatment assignment. **Not yet standard**: causal forest as the primary identification strategy in observational settings without strong unconfoundedness assumption.

### The OLS weighting critique

Sloczynski (*ReStat* 104(3):501-509, 2022): OLS treatment coefficients with heterogeneous effects place **higher weight on minority groups** (inversely proportional to group size). If treated and untreated groups are very different in size, the OLS estimand may be far from any policy-relevant parameter. Use `hettreatreg` to diagnose.

### Red-flag phrases

- "We explore heterogeneity by splitting the sample" (data mining; multiple testing concerns without correction)
- "We run a causal forest and find HTE" without reporting the best linear predictor test or confidence intervals
- "OLS estimates the ATE under heterogeneous effects" (Sloczynski critique: depends on group sizes and effect heterogeneity)
- Using Lasso for variable selection in the first stage without DML cross-fitting (regularization bias in second stage)

---

## 7. Network Effects, Spillovers, and SUTVA Violations

### The interference problem is now a required discussion

Papers with any plausible spillover mechanism must now explicitly address SUTVA. The default "stable unit treatment value assumption" is no longer automatically granted by reviewers.

Aronow & Samii (*Annals of Applied Statistics* 11(4), 2017): **Exposure mapping framework**. Potential outcomes depend on a low-dimensional summary of the treatment vector (exposure). Valid estimation requires specifying the exposure model (which neighbors' treatments matter, through what channel).

Sävje, Aronow & Hudgens (*Annals of Statistics* 2021): Even under unknown interference, under-rejection of no-effect null hypotheses is possible; provides conditions for valid inference.

**Cluster randomization**: when spillovers are contained within clusters, cluster-randomized designs with proper cluster-level analysis are the solution. Papers that randomize at the individual level but have plausible within-cluster spillovers need to address this.

**Network experiments**: Athey, Eckles & Imbens (*JASA* 2018) design-based inference for networks; shows standard variance estimators understate uncertainty when network effects exist.

### Red-flag phrases

- "We assume SUTVA" with no discussion of spillover plausibility
- Individual-level randomization of a product/program with obvious social network effects
- "Standard errors are clustered at [unit] level" when treatment assignment was at a higher level (clustering too fine)
- Claiming a geographic control group is clean when it borders the treated area (spatial spillovers)

---

## 8. Field Experiments: Pre-registration, Multiple Testing, Attrition

### Pre-registration norms

Pre-registration is now essentially required for RCT-based papers at top journals. AEA RCT Registry is the standard. Papers without pre-registration face questions about: (a) was the outcome chosen ex-post, (b) were additional hypotheses added after seeing data, (c) were subgroup analyses pre-specified.

### Multiple hypothesis testing

Romano & Wolf (*Econometrica* 73(4):1237-1282, 2005; *J Applied Econometrics* 2016 update): stepwise procedure that controls familywise error rate (FWER). More powerful than Bonferroni/Holm because it accounts for dependence across tests via resampling. Implemented via `rwolf` in Stata (Clarke, Romano & Wolf, *Stata Journal* 20(4), 2020).

List, Shaikh & Xu (*J Econometrics* 210(1):209-228, 2019): multiple testing in experimental economics; recommends Romano-Wolf over Bonferroni; discusses when to group hypotheses into families.

Benjamini-Hochberg FDR control: acceptable in exploratory work but top journals generally prefer FWER control.

### Attrition and Lee bounds

Lee (2009, *ReStud* 76(3):1071-1102): worst-case bounds on treatment effects under monotone sample selection. **Lee bounds are now mandatory** when attrition >5% and differential across treatment arms.

Horowitz & Manski (*Journal of Business & Econ Statistics* 18(2):168-180, 2000): bounds when outcome data are missing.

### Red-flag phrases

- No pre-registration for a published RCT
- "Results survive Bonferroni correction" (less powerful than Romano-Wolf; also no longer sufficient if many outcomes)
- Attrition >5% with no bounds analysis
- "The attrition is balanced across arms" used as the only attrition response (balance does not rule out selective attrition within groups)
- Primary outcome changed from what was pre-registered without noting the change

---

## 9. Structural vs. Reduced-Form: When Top Journals Want What

### The current balance

Top micro journals (AER, QJE, Econometrica) publish both. The key question is not structural vs. RF but: **what does your identification strategy actually identify, and is that parameter economically interpretable?**

**When structural is preferred or required**:
- When the policy question requires counterfactual simulations (e.g., welfare analysis of a policy not yet implemented)
- When the structural parameter has a direct economic interpretation not recoverable from reduced-form (e.g., risk aversion, discount rates, markups)
- Industrial organization / dynamic discrete choice: *Econometrica*, *ReStud*, *RAND* essentially require structural models for questions about entry, pricing, mergers
- When the reduced-form LATE is not the policy-relevant parameter and extrapolation requires structure (Heckman-Vytlacil marginal treatment effects framework)

**When structural faces scrutiny**:
- When identification of structural parameters relies on distributional assumptions that cannot be tested
- When the counterfactual of interest could be recovered from reduced-form without the parametric overhead
- Whited (*J Financial Econometrics* 21(3):597-615, 2023): argues for integration — use RF to discipline structural models, and structural to extend RF external validity

**Dynamic discrete choice identification**:
Magnac & Thesmar (2002, *Econometrica*): discount factor is not separately identified from period payoffs without additional restrictions. Recent extensions: Abbring & Daljord (2020) exclusion restrictions; Kalouptsidi, Scott & Souza-Rodrigues (*QE* 2021) on identification of counterfactuals even when model is not point-identified.

**Identification at infinity**: Chamberlain (1986) / Heckman (1990): identification of selection models when instrument has large support. Requires the instrument to take extreme values with positive probability; rarely testable in finite samples. Papers invoking this need large-support argument.

### Red-flag phrases

- "The model is identified by functional form assumptions" (not a defense at top journals)
- "We calibrate the discount factor to 0.95" without discussing identification
- "Our structural estimates imply [large effect]" where the comparable reduced-form gives very different magnitudes without explanation
- Structural model with many free parameters, all justified by "we have many moments" (without formal identification proof)
- "We use a reduced-form result to validate our structural model" where validation amounts to fitting the reduced-form coefficient

---

## 10. What Top Journals Reject Papers For: Current Referee Practice

### The credibility-first filter

Since Angrist & Pischke's "Credibility Revolution" (2010, JEP) and reinforced by the 2021 Nobel to Card, Angrist & Imbens, **identification clarity is now the first editorial screen**. AER desk-rejects 65-75% of submissions; the main filter is identification credibility. A well-written paper with unclear identification will not survive triage at AER/QJE/Econometrica.

Angrist (2022, *Econometrica* 90(6)): Nobel lecture. Argument: "Exclusion restrictions formalize commitment to clear and consistent explanations of reduced-form causal effects." Papers that cannot state a clear exclusion restriction or natural experiment will not pass referee review.

### Common rejection grounds (2020-2025)

**DiD**:
- Using TWFE with staggered adoption without acknowledging the heterogeneous-effects critique
- Event study with only 1-2 pre-periods (insufficient pre-trends evidence)
- No sensitivity analysis for parallel trends (HonestDiD now expected)
- Pre-trends shown to be statistically significant without adjustment

**RD**:
- Missing manipulation test (rddensity)
- Bandwidth selected without explanation
- No covariate balance tests at the cutoff
- Geographic RD with no discussion of multiple simultaneous discontinuities

**IV**:
- Weak instrument by heteroskedasticity-robust standard (F<10 by effective F, not just conventional F)
- Shift-share without stating which identification framework (shocks vs. shares)
- Judge/examiner design without exclusion restriction test
- Exclusion restriction defended only verbally without any testable implication

**General**:
- Standard errors not clustered at treatment assignment level
- Multiple hypothesis testing with Bonferroni only (Romano-Wolf expected)
- Sensitivity analysis limited to "adding controls"; no Oster/Cinelli-Hazlett
- No discussion of SUTVA when spillovers are plausible
- Attrition >5% without Lee bounds

### Key methodological JEP / review articles for background

| Paper | Journal | Year | Role |
|---|---|---|---|
| Roth, Sant'Anna, Bilinski, Poe | *J Econometrics* 235(2) | 2023 | DiD synthesis |
| Abadie | *JEL* 59(2):391-425 | 2021 | SC practitioner guide |
| Cattaneo & Titiunik | *ARE* 14:821-851 | 2022 | RD review |
| Andrews, Stock & Sun | *ARE* 11:727-753 | 2019 | IV/weak instruments |
| Chyn, Frandsen & Leslie | *JEL* 63(2):401-439 | 2025 | Judge designs |
| Borusyak, Hull & Jaravel | *JEP* 39(1):181-204 | 2025 | Shift-share practical guide |
| Angrist | *Econometrica* 90(6) | 2022 | Nobel lecture; credibility philosophy |

---

## Summary Table: Old Standard vs. New Standard

| Issue | Acceptable 2015-2019 | Required 2022+ |
|---|---|---|
| Staggered DiD | TWFE + event study | CS/Sun-Abraham/BJS + Goodman-Bacon decomp |
| Pre-trends | Test pre-trends, claim support | Roth (2022) power analysis + HonestDiD sensitivity |
| RD manipulation | McCrary (2008) test | rddensity (Cattaneo-Jansson-Ma 2020) |
| RD inference | Local linear with ad-hoc bandwidth | rdrobust with MSE-optimal bandwidth + RBC CIs |
| IV strength | Staiger-Stock F>10 | Effective F (Olea-Pflueger) or AR confidence sets |
| Shift-share | "National trends are exogenous" | State shocks-view or shares-view explicitly; run balance tests |
| Judge IV | "Judges randomly assigned" | Frandsen-Lefgren-Leslie exclusion+monotonicity test |
| OVB sensitivity | "Coefficient stable across specs" | Oster (2019) or Cinelli-Hazlett (2020) robustness value |
| DiD with SC-like setting | DiD or simple SC | Synthetic DiD (Arkhangelsky et al.) or Augmented SC |
| Multiple outcomes | Bonferroni correction | Romano-Wolf stepdown procedure |
| Attrition | Balance test across arms | Lee bounds (mandatory if >5% differential attrition) |
| SUTVA | Assume away spillovers | Explicit discussion; exposure mapping if relevant |
| HTE exploration | Split-sample subgroup analysis | Generic ML (Chernozhukov et al.) with valid inference |

---

## Software Reference

| Method | Stata | R | Python |
|---|---|---|---|
| CS DiD | `csdid` | `did` (Callaway) | — |
| BJS imputation DiD | `did_imputation` | `didimputation` | — |
| Sun-Abraham | `eventstudyinteract` | `fixest` (`sunab`) | — |
| Honest DiD | `honestdid` | `HonestDiD` | — |
| Pretrends power | `pretrends` | `pretrends` | — |
| RD robust inference | `rdrobust` | `rdrobust` | `rdrobust` |
| RD density/manipulation | `rddensity` | `rddensity` | — |
| Synthetic DiD | — | `synthdid` | `synthdid` |
| Double ML | `ddml` | `DoubleML` | `DoubleML` |
| Causal forest | — | `grf` | `econml` |
| Romano-Wolf | `rwolf` | `WildBootTests.jl` | — |
| OVB sensitivity | `psacalc` (Oster) | `sensemakr` (C-H) | `sensemakr` |
| Shift-share (BHJ) | `ssaggregate` | `ssaggregate` | — |
| Shift-share Rotemberg | `bartik_weight` | `bartik_weight` | — |
