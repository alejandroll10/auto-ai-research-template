# Identification Strategies in Empirical Finance: 2020–2026 Literature Review

*For use in identification-designer and identification-auditor agent prompts.*
*Covers JF / JFE / RFS top-journal practice; focuses on what has changed since ~2019.*

---

## 1. Staggered DiD Revolution Post-2020

### Key Papers

- **Goodman-Bacon (2021)**, *Journal of Econometrics* 225(2): 254–277. TWFE in staggered designs is a weighted average of all 2×2 DiD comparisons across treatment-timing cohorts; some weights are *negative* when treatment effects are heterogeneous over cohorts or over time. Already-treated units serve as "controls" for later-treated units — they should not.

- **de Chaisemartin & D'Haultfoeuille (2020)**, *American Economic Review* 110(9): 2964–96. TWFE estimates a weighted sum of ATEs with possibly negative weights; proposes the `did_multiplegt` estimator robust to heterogeneous effects.

- **Sun & Abraham (2021)**, *Journal of Econometrics* 225(2): 175–199. Leads/lags in TWFE event-study regressions are contaminated by effects from other periods; apparent pre-trends can arise purely from treatment effect heterogeneity. Proposes interaction-weighted (IW) estimator.

- **Callaway & Sant'Anna (2021)**, *Journal of Econometrics* 225(2): 200–230. Identifies cohort-specific average treatment effects on the treated (ATT(g,t)); aggregates them into interpretable parameters under parallel trends conditional on covariates. R package `did`.

- **Borusyak, Jaravel & Spiess (2024)**, *Review of Economic Studies* 91(6): 3253–85. Imputation estimator: computes counterfactual outcomes for treated cells by imputing from untreated cells under the no-treatment model; efficient and unbiased under unrestricted heterogeneity. Stata/R package `did_imputation`.

- **Baker, Larcker & Wang (2022)**, *Journal of Financial Economics* 144(2): 370–395. **Finance-specific diagnosis.** Staggered DiD constitutes ~50% of published DiD papers in top finance and accounting journals. The authors re-examine three canonical finance papers (bank deregulation, board reform, state disclosure laws) using robust estimators; in all three cases the original positive findings become indistinguishable from null. This is the paper referees now cite.

- **Roth, Sant'Anna, Bilinski & Poe (2023)**, *Journal of Econometrics* 235(2): 2218–44. Synthesis of the DiD revolution: what canonical assumptions are relaxed by each new estimator; practical guide.

### New Standard vs. 2019 Practice

| Dimension | 2019 practice | 2026 standard |
|---|---|---|
| Estimator | Vanilla TWFE with treatment dummy | Callaway-Sant'Anna, Sun-Abraham, or Borusyak-Jaravel-Spiess as primary or robustness check |
| Pre-trends | Plot raw event-study TWFE coefficients | Report event-study plot using robust estimator; separate pre-trends from contaminated TWFE leads |
| Parallel trends | Assumed binary (pass/fail pre-trend test) | Roth (2022) power analysis; Rambachan-Roth (2023) sensitivity analysis (HonestDiD) |
| Weighting | Implicit TWFE weights accepted | Report Goodman-Bacon decomposition; flag negative weights |

### Common Referee Failure Modes

1. **Using TWFE with staggered treatment and claiming robustness only via clustering.** Referees now routinely ask: "Did you check for negative weights? Have you run Callaway-Sant'Anna or Borusyak-Jaravel-Spiess?"
2. **Showing TWFE event-study leads/lags as a pre-trends test without acknowledging Sun-Abraham contamination.** The apparent pre-trend may be an artifact of treatment effect heterogeneity.
3. **Passing a pre-trend test and treating parallel trends as established.** Roth (2022) shows pre-trend tests have low power; the *absence* of significance is not evidence of absence. Sensitivity analysis (HonestDiD) is increasingly expected.
4. **Functional form of parallel trends.** Roth (2023, *Econometrica*) shows parallel trends in levels does not imply parallel trends in logs and vice versa; referees in corporate finance now ask whether the parallel-trends assumption is plausible in the researcher's chosen functional form.

---

## 2. Shift-Share / Bartik Instruments

### Key Papers

- **Goldsmith-Pinkham, Sorkin & Swift (2020)**, *American Economic Review* 110(8): 2586–2624. Decomposes SSIV into a weighted sum of share-instrument estimators ("Rotemberg weights"); identification rests on exogeneity of the *shares*, not the shocks. Required diagnostic: compute Rotemberg weights, report the top-weight shares, and test them individually for exogeneity/overidentification.

- **Borusyak, Hull & Jaravel (2022)**, *Review of Economic Studies* 89(1): 181–213. Alternative: identification from quasi-random assignment of *shocks* (not shares); shares can be endogenous. Provides shock-level regression equivalence and overidentification test across shocks.

- **Borusyak & Hull (2023)**, "A Practical Guide to Shift-Share Instruments," NBER WP 33236. Step-by-step implementation guide; clarifies when each approach is appropriate.

### New Standard vs. 2019 Practice

2019: A researcher constructs a Bartik instrument and reports a strong first stage; identification is asserted by verbal argument about exogeneity. 2026: The paper must commit to whether identification comes from shocks (BHJ) or shares (GPS), then provide the appropriate diagnostic table. For GPS: Rotemberg weight table + Hausman overidentification test. For BHJ: shock-level balance tests and overidentification.

### Common Referee Failure Modes

1. Claiming the instrument is "Bartik-style" without specifying which identifying variation (shocks vs. shares).
2. Omitting the Rotemberg weight decomposition; referees at JFE/RFS now expect this as a table.
3. Using shares from the outcome period (endogenous by construction in GPS framework).
4. Not reporting whether the instrument is valid under either framework separately.

---

## 3. Event Studies in Finance

### Key Papers

- **Kolari & Pynnonen (2010)**, *Review of Financial Studies* 23(11): 3996–4025. Cross-sectional correlation of abnormal returns inflates rejection rates even at low average correlation; provides corrected test statistics. This is now a standard reference but compliance in published papers is still uneven.

- **Kolari, Pape & Pynnonen (2018)**, SSRN. Extension to *partially* overlapping event windows; more common in practice.

- **Borusyak, Jaravel & Spiess (2024)** (same paper as §1). The "event-study design" framing in this paper applies not just to policy DiD but to any relative-time analysis; their imputation approach is cleaner than raw leads/lags.

### New Standard vs. 2019 Practice

2019: Market-model OLS in 250-day estimation window, standardized CARs, Patell test, maybe BMP correction. 2026 additional expectations: (a) If events cluster in calendar time (e.g., all firms react to a macro announcement), apply Kolari-Pynnonen correction or portfolio-based test. (b) For long-horizon BHARs: calendar-time portfolio approach (Fama 1998) preferred over buy-and-hold matching, especially for datasets with overlapping windows. (c) Use of Fama-French 5-factor or q-factor benchmarks rather than market model for alpha estimation.

### Common Referee Failure Modes

1. Ignoring cross-sectional correlation when events are date-clustered; patently violates test assumptions.
2. Using BHARs for multi-year windows without accounting for new-listing bias or skewness.
3. Estimation window overlapping the treatment period (look-ahead bias).
4. Reporting t-tests without checking whether the distribution of CARs is driven by a small number of outlier events.

---

## 4. High-Frequency Identification

### Key Papers

- **Nakamura & Steinsson (2018)**, *Quarterly Journal of Economics* 133(3): 1283–1330. 30-minute window around FOMC announcements; interest rate surprises are exogenous; real rates and output forecasts co-move positively (the "information effect"). This paper introduced the methodology now used across finance.

- **Jarocinski & Karadi (2020)**, *AEJ: Macroeconomics* 12(2): 1–43. Sign restriction on co-movement of rates and stock prices in FOMC window decomposes surprises into pure monetary policy shocks (rates up, stocks down) and central bank information shocks (rates up, stocks up). Ignoring this decomposition biases inference on monetary non-neutrality. Won 2021 AEJ Best Paper Award.

- **Bauer & Swanson (2023)**, *NBER Macroeconomics Annual* 37: 87–155. Challenges prior results: monetary policy surprises are predictable from publicly available macro/financial data *before* the FOMC meeting ("Fed response to news" channel); orthogonalizing against this pre-meeting information substantially changes macroeconomic estimates. Doubles usable observations by including Fed Chair speeches.

- **Miranda-Agrippino & Ricco (2021)**, *AEJ: Macroeconomics* 13(3): 58–87. Purifies HFI surprises by removing Fed's own information advantage ("information effect"); residual surprise is more plausibly exogenous for causal inference.

### New Standard vs. 2019 Practice

2019: Use raw FOMC window rate surprises as external instruments (proxy SVAR or IV-LP). 2026: (a) Must account for information effect; Jarocinski-Karadi sign restriction or Miranda-Agrippino-Ricco purified series expected as robustness. (b) Bauer-Swanson critique is now live: must argue or test that surprises are not predictable from pre-meeting data, or orthogonalize explicitly. (c) Gertler-Karadi (2015) instrument still commonly used but now paired with the above checks.

### Common Referee Failure Modes

1. Using raw 30-minute rate surprises without checking information-effect contamination.
2. Using only scheduled FOMC dates when unscheduled meetings or Fed Chair speeches are plausibly relevant.
3. Treating the instrument as strong without testing; weak-IV diagnostics apply (see §6).
4. Not controlling for realized macro data released simultaneously with FOMC statement.

---

## 5. Bad Controls / Post-Treatment Bias

### Key Papers

- **Cinelli, Forney & Pearl (2024)**, *Sociological Methods & Research* 53(3): 1071–1104. "A Crash Course in Good and Bad Controls." DAG-based taxonomy of when adding a variable creates rather than removes bias; collider bias, M-bias, proxy variables as controls. Accessible to practitioners; widely cited in referee reports.

- **Oster (2019)**, *Journal of Business & Economic Statistics*. Coefficient stability under selection on unobservables; δ parameter for how much unobserved selection exceeds observed. R package `psacalc`. Heavily used but fragile—sensitivity to δ assumptions is itself under critique (Diegert, Masten & Poirier 2022).

- **Cinelli & Hazlett (2020)**, *Journal of the Royal Statistical Society B* 82(1): 39–67. `sensemakr`: formal omitted-variable bias sensitivity analysis; robustness value, partial R² benchmarks against named controls. Increasingly expected in top-journal corporate finance papers that lack a clean quasi-experiment.

### New Standard vs. 2019 Practice

2019: Include "control variables" from prior literature without checking whether they are post-treatment or colliders. 2026: Referees at JF/RFS now explicitly flag post-treatment controls. Expected practice: (a) justify each control in the DAG / sequential ignorability framework; (b) show results drop or add controls that are plausibly post-treatment; (c) for OLS papers without an instrument, report sensemakr or Oster bounds.

### Common Referee Failure Modes

1. Controlling for a variable that is itself affected by the treatment (post-treatment bias).
2. Controlling for an intermediate outcome variable (mediation contamination).
3. Including leverage or cash holdings as controls in regressions where the outcome is leverage or investment — these are often simultaneous or post-treatment.
4. Citing Oster (2019) without checking the fragility of the δ assumption.

---

## 6. Weak IV / Weak Identification

### Key Papers

- **Andrews, Stock & Sun (2019)**, *Annual Review of Economics* 11: 727–53. Comprehensive review; recommends Montiel Olea & Pflueger (2013) effective F-statistic (robust to heteroskedasticity and clustering) rather than Stock-Yogo critical values (assume homoskedasticity). Effective F threshold for 5% maximal size distortion: ~23.11 for one instrument (not the old "F > 10" rule).

- **Lee, McCrary, Moreira & Porter (2022)**, *American Economic Review* 112(10): 3260–90. "Valid t-ratio Inference for IV." Introduces the tF critical value function: standard error adjustment based on first-stage F. Key empirical finding: for one-quarter of specifications in 61 AER papers, corrected SEs are at least 49% larger than conventional 2SLS SEs at 5% level.

- **Mikusheva & Sun (2022)**, *Review of Economic Studies*. Classical F-test can misidentify weak instruments; improved concentration parameter tests.

### New Standard vs. 2019 Practice

2019: Report first-stage F > 10, claim "strong instruments." 2026: Report Montiel-Olea-Pflueger effective F (heteroskedasticity/cluster-robust); compare to MOP critical values (≈23 for one IV). For a single instrument, apply tF correction (Lee et al. 2022) or Anderson-Rubin confidence intervals. Report Stock-Yogo only as legacy context.

### Common Referee Failure Modes

1. Citing the old "F > 10" threshold without reporting heteroskedasticity-robust effective F.
2. Many instruments but low effective F; many weak instruments can produce a high Kleibergen-Paap F but large maximal size distortions.
3. Not reporting Anderson-Rubin or conditional LR confidence sets for IV specifications that may be near the weak-IV boundary.
4. Using 2SLS without checking that the first-stage F exceeds MOP thresholds after clustering at the relevant level.

---

## 7. Machine Learning for Causal Inference in Finance

### Key Papers

- **Chernozhukov et al. (2018)**, *Econometrics Journal* 21(1): C1–C68. Double/debiased ML (DML): Neyman-orthogonal moments + cross-fitting removes regularization bias in high-dimensional nuisance estimation; valid inference on low-dimensional treatment parameters.

- **Wager & Athey (2018)**, *Journal of the American Statistical Association* 113(523): 1228–42. Causal forests for heterogeneous treatment effects; honest inference via sample splitting.

- **Giglio, Kelly & Xiu (2022)**, *Annual Review of Financial Economics* 14: 337–68. Survey of ML in asset pricing; argues the field has moved from prediction to estimation/inference; reviews PCA, IPCA (Kelly-Pruitt-Su), autoencoders, RP-PCA (Lettau-Pelger). Defines best practices for using ML in factor pricing.

- **Gu, Kelly & Xiu (2020)**, *Review of Financial Studies* 33(5): 2223–73. Neural networks, LASSO, gradient boosting for return prediction; pure ML prediction, not causal inference, but sets benchmark for signal extraction.

### Status in Top Finance Journals (2026)

DML and causal forests are **accepted** in JF/JFE/RFS when: (a) the research question is genuinely about heterogeneous treatment effects (e.g., heterogeneous responses to credit supply shocks across firm types); (b) the researcher has a credible identification design underlying the DML (DML does not solve endogeneity — it solves regularization bias conditional on a valid identifying assumption); (c) inference follows the asymptotic theory (cross-fitting, standard errors).

ML for causal inference is **seen as gimmicky** when: (a) it is applied to a question answerable with standard OLS/IV but with ML added for novelty; (b) the identifying assumption is just OLS-under-selection-on-observables — ML amplifies but does not validate this; (c) the paper reports heterogeneous treatment effects without a formal testing procedure (CLAN tests or omnibus balance tests required).

### Common Referee Failure Modes

1. Applying DML without a credible identification strategy; reviewers note DML removes regularization bias, not endogeneity.
2. Reporting causal forest heterogeneity results without testing for significant heterogeneity (Chernozhukov-Demirer-Duflo-Fernandez-Val 2020 omnibus test).
3. Confusing prediction performance (out-of-sample R²) with causal identification.
4. Using ML-generated propensity scores for matching without checking overlap/positivity.

---

## 8. Identification in Asset Pricing

### Key Papers

- **Giglio & Xiu (2021)**, *Journal of Political Economy* 129(7): 1947–90. "Asset Pricing with Omitted Factors." Three-pass regression filter: estimates risk premia of an observable factor even when other priced factors are unspecified; addresses misspecification bias in standard two-pass Fama-MacBeth.

- **Kelly, Pruitt & Su (2019)**, *Journal of Financial Economics* 134(3): 501–24. Instrumented PCA (IPCA): characteristics are covariances; latent factor loadings are linear in observable characteristics. Challenges anomaly literature: characteristics predict returns through loadings, not alphas.

- **Lettau & Pelger (2020)**, *Journal of Econometrics* 218(1): 1–31. RP-PCA: uses cross-sectional variation in risk premia (not just variance) to identify factors; recovers factors that explain expected returns, not just covariance.

- **Giglio, Kelly & Xiu (2022)** (see §7). Comprehensive framework for when PCA, IPCA, autoencoder, or Fama-MacBeth is appropriate; inference theory for each.

- **Haddad, He, Huebner, Kondor & Loualiche (2025)**, WP. "Causal Inference for Asset Pricing." Cross-sectional IV / DiD regressions mechanically absorb substitution patterns across assets (missing coefficient problem); recovering causal demand elasticities requires time-series exogenous variation. Won SFI Outstanding Paper Award 2025.

### Long-Horizon Predictability

Known problems (Stambaugh 1999 bias, Valkanov 2003 t-stat) remain. Recent additional critique: small-sample bias in long-horizon coefficients is analytically derived and substantial (Boudoukh et al. 2022). Referees now expect: (a) bias-adjusted estimates for horizons beyond 1–2 years; (b) bootstrap p-values rather than asymptotic t-stats; (c) out-of-sample R² as a robustness check on in-sample predictability.

### Factor Zoo / Multiple Testing

Harvey, Liu & Zhu (2016) raised the bar on t-statistics to ~3.0 for new factors. Harvey & Liu (2020), *Journal of Finance*: false discovery rate (FDR) framework for factor and fund selection. Feng, Giglio & Xiu (2020), *Journal of Finance*: double-selection LASSO to identify which new factors survive controlling for the existing factor zoo. Papers proposing a new factor without the Feng-Giglio-Xiu double-selection test routinely get this as a referee comment.

### Common Referee Failure Modes

1. Two-pass Fama-MacBeth without addressing the EIV problem (Shanken 1992 correction minimum; Giglio-Xiu three-pass preferred).
2. Claiming a new factor is priced without the Feng-Giglio-Xiu zoo test.
3. Long-horizon regressions with overlapping observations without using Hodrick (1992) standard errors or Hansen-Hodrick.
4. Ignoring weak factor problem: Giglio-Xiu-Zhang (2022) show factors with small cross-sectional R² inflate risk premium estimates; must check.

---

## 9. Banking / Regulation Natural Experiments

### Key Papers

- **Garcia & Steele (2022)**, *Journal of Banking & Finance* 135. Stress testing (DFAST/CCAR) as RD: banks just above the $50B/$250B CCAR threshold vs. just below. Finds stress tests reduce risk-weighted assets without reducing lending. Identification challenge: banks self-select near thresholds; McCrary density test required.

- **Acharya, Berger & Roman (2018)** / subsequent **2020–23 literature**: TARP, Dodd-Frank, Basel III as staggered treatment. Post-Baker-Larcker-Wang (2022), all such papers must now use robust staggered DiD estimators. Papers reexamining canonical Dodd-Frank results using Callaway-Sant'Anna often find attenuated or null effects.

- General RD in banking: Calonico-Cattaneo-Titiunik (2014) bias-corrected RD estimates are now the minimum bar. Referees expect rdrobust output with triangular kernel, MSE-optimal bandwidth, and CER-optimal bandwidth as robustness.

### Identification Critiques for Regulation Studies

1. **Manipulation at threshold**: Banks anticipate regulatory thresholds; McCrary (2008) density test around the asset threshold is expected.
2. **Multiple thresholds / threshold changes**: CCAR moved from $50B to $100B to $250B; papers pooling across threshold regimes conflate different treatments.
3. **Confounding with other regulatory events**: Basel III, TARP repayment, Fed supervision changes happened simultaneously with Dodd-Frank; diff-in-diff designs must argue against confounders.
4. **Staggered Dodd-Frank rollout**: Provisions phased in over 2010–2014; treating the whole Act as a single treatment date is now rejected by referees.

### Common Referee Failure Modes

1. Using the $50B or $10B threshold without testing for manipulation (density test).
2. Running TWFE for staggered Dodd-Frank provisions without robust DiD estimator (Baker-Larcker-Wang critique applies directly).
3. Not controlling for bank size polynomials when using size thresholds as RD running variable.
4. Treating stress test "failure" as exogenous without arguing against strategic behavior near failure cutoff.

---

## 10. What Top Finance Referees Are Rejecting On (2022–2026)

### Documented Methodological Critiques in Top Journals

- **Baker, Larcker & Wang (2022)**, *JFE*: Directly overturned results in prior JF/JFE/RFS papers using staggered DiD. Referees cite this constantly for corporate governance, banking deregulation, and disclosure law papers.

- **Roth (2022)**, *AEA: Insights*: "Pretest with Caution" — pre-trends tests have low power and conditioning on them distorts inference. Referees now ask for power calculations for pre-trends tests (Roth's `pretrends` package) and often require HonestDiD sensitivity analysis.

- **Lee, McCrary, Moreira & Porter (2022)**, *AER*: The tF paper. Finance papers with single instruments and F-stats in the 10–30 range are now routinely asked to report tF-corrected SEs.

- **Feng, Giglio & Xiu (2020)**, *Journal of Finance* 75(3): 1327–70. Double-selection LASSO factor test. New factor papers that do not run this test receive it as first-round referee comment.

### Recurring Referee Comments (Based on Methodological Consensus)

1. **DiD:** "Please report Callaway-Sant'Anna and/or Borusyak-Jaravel-Spiess estimates alongside TWFE. Report the Goodman-Bacon decomposition and check for negative weights."

2. **Event studies:** "Are events clustered in calendar time? If so, apply Kolari-Pynnonen (2010) correction. Please confirm the estimation window does not overlap with other major events in your sample."

3. **IV:** "Please report the Montiel-Olea-Pflueger effective F-statistic (not the Kleibergen-Paap F alone) and compare to the 5% maximal size distortion critical value. Report Anderson-Rubin confidence intervals."

4. **Bad controls:** "Variable X appears to be a post-treatment outcome. Please show results excluding it, or justify why it is a pre-determined covariate."

5. **Bartik:** "Please include the Rotemberg weight table (Goldsmith-Pinkham et al. 2020) and clarify whether identification comes from shocks or shares."

6. **High-frequency:** "Please address the Bauer-Swanson (2023) predictability critique and/or show results using the Miranda-Agrippino-Ricco purified surprise series."

7. **Asset pricing / new factor:** "Please run the Feng-Giglio-Xiu (2020) double-selection test to verify the factor survives controlling for the factor zoo."

8. **ML:** "DML removes regularization bias, not endogeneity. What is the identifying assumption? Please clarify."

9. **Parallel trends:** "Passing a pre-trends test does not establish parallel trends. Please provide HonestDiD sensitivity analysis showing the breakdown value."

10. **Long-horizon predictability:** "Please report bias-adjusted estimates following Boudoukh et al. (2022) / Stambaugh (1999) correction and bootstrap p-values."

---

## Summary Table: Core Method Shifts

| Method | Old standard (pre-2020) | Current standard (2026) |
|---|---|---|
| Staggered DiD | TWFE with clustering | CS, SA, or BJS estimators; Goodman-Bacon decomp; HonestDiD |
| Shift-share IV | "Bartik instrument + strong F" | GPS Rotemberg weights OR BHJ shock-level tests; must commit to one |
| Event study | Patell / BMP t-test | Kolari-Pynnonen for clustered events; F5F or q-factor benchmark |
| HFI monetary | Raw 30-min rate surprise | JK decomposition or MAP-purified series; Bauer-Swanson predictability check |
| Bad controls | Include standard control set | DAG check; show results with/without post-treatment controls; sensemakr |
| Weak IV | F > 10 (Stock-Yogo homoskedastic) | MOP effective F > 23; tF correction; Anderson-Rubin CIs |
| ML causal | DML as black-box causal estimator | DML requires separate valid identifying assumption; heterogeneity needs omnibus test |
| Asset pricing factor | Fama-MacBeth + t > 2 | Feng-Giglio-Xiu zoo test; Giglio-Xiu three-pass for risk premia |
| Banking RD | Simple RD at threshold | CCT bias-corrected; McCrary density test; staggered-robust DiD for regulation |

---

## References (Compact)

- Andrews, Stock & Sun (2019). "Weak Instruments in IV Regression." *Annual Review of Economics* 11: 727–53.
- Baker, Larcker & Wang (2022). "How Much Should We Trust Staggered DiD?" *JFE* 144(2): 370–395.
- Bauer & Swanson (2023). "A Reassessment of Monetary Policy Surprises." *NBER Macroeconomics Annual* 37.
- Borusyak, Hull & Jaravel (2022). "Quasi-Experimental Shift-Share Research Designs." *ReStud* 89(1): 181–213.
- Borusyak, Jaravel & Spiess (2024). "Revisiting Event-Study Designs." *ReStud* 91(6): 3253–85.
- Callaway & Sant'Anna (2021). "DiD with Multiple Time Periods." *Journal of Econometrics* 225(2): 200–230.
- Chernozhukov et al. (2018). "Double/Debiased ML." *Econometrics Journal* 21(1): C1–C68.
- Cinelli, Forney & Pearl (2024). "A Crash Course in Good and Bad Controls." *Sociological Methods & Research* 53(3).
- Cinelli & Hazlett (2020). "sensemakr." *JRSS-B* 82(1): 39–67.
- de Chaisemartin & D'Haultfoeuille (2020). "TWFE Estimators with Heterogeneous Treatment Effects." *AER* 110(9): 2964–96.
- Feng, Giglio & Xiu (2020). "Taming the Factor Zoo." *Journal of Finance* 75(3): 1327–70.
- Giglio & Xiu (2021). "Asset Pricing with Omitted Factors." *JPE* 129(7): 1947–90.
- Giglio, Kelly & Xiu (2022). "Factor Models, ML, and Asset Pricing." *Annual Review of Financial Economics* 14: 337–68.
- Goldsmith-Pinkham, Sorkin & Swift (2020). "Bartik Instruments." *AER* 110(8): 2586–2624.
- Goodman-Bacon (2021). "DiD with Variation in Treatment Timing." *Journal of Econometrics* 225(2): 254–77.
- Gu, Kelly & Xiu (2020). "Empirical Asset Pricing via Machine Learning." *RFS* 33(5): 2223–73.
- Haddad, He, Huebner, Kondor & Loualiche (2025). "Causal Inference for Asset Pricing." WP (SFI Outstanding Paper 2025).
- Jarocinski & Karadi (2020). "Deconstructing Monetary Policy Surprises." *AEJ: Macroeconomics* 12(2): 1–43.
- Kelly, Pruitt & Su (2019). "Characteristics Are Covariances." *JFE* 134(3): 501–24.
- Kolari & Pynnonen (2010). "Event Study Testing with Cross-Sectional Correlation." *RFS* 23(11): 3996–4025.
- Lee, McCrary, Moreira & Porter (2022). "Valid t-Ratio Inference for IV." *AER* 112(10): 3260–90.
- Lettau & Pelger (2020). "Estimating Latent Asset-Pricing Factors." *Journal of Econometrics* 218(1): 1–31.
- Miranda-Agrippino & Ricco (2021). "The Transmission of Monetary Policy Shocks." *AEJ: Macroeconomics* 13(3): 58–87.
- Nakamura & Steinsson (2018). "High-Frequency Identification of Monetary Non-Neutrality." *QJE* 133(3): 1283–1330.
- Oster (2019). "Unobservable Selection and Coefficient Stability." *JBES* 37(2): 187–204.
- Rambachan & Roth (2023). "A More Credible Approach to Parallel Trends." *ReStud* 90(5): 2555–91.
- Roth (2022). "Pretest with Caution." *AEA: Insights* 4(2): 177–92.
- Roth, Sant'Anna, Bilinski & Poe (2023). "What's Trending in DiD?" *Journal of Econometrics* 235(2): 2218–44.
- Sun & Abraham (2021). "Estimating Dynamic Treatment Effects in Event Studies." *Journal of Econometrics* 225(2): 175–199.
