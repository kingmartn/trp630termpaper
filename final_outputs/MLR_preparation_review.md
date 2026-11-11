# Full-dataset EDA and regression preparation review

All 93,307 households remain in the EDA, without a training/test partition. Original source files and historical split artifacts are preserved. These are descriptive and predictor-design checks; no trip-outcome regression is fitted and no final row-exclusion rule is selected.

## Source-dictionary correction

The supplied [2006 TTS Version 1.0 Data Guide](../inputs/dataguide2006_v1.pdf), printed page 18 (PDF page 23), defines n_vehicle as a 0-99 count. Printed page 51 (PDF page 56) explicitly tabulates 99 with description 99 and one 2006 record. The earlier provisional assumption that 99 meant missing has been withdrawn. It is retained numerically in nvehicle_clean. There are 0 unavailable vehicle measurements in this file, 1 numeric value of 99, and 33 records with at least 10 vehicles.

The guide also publishes extreme counts such as 21, 23, and 36. This supports treating them as source-recorded values rather than errors inferred from rarity; it does not prove each response is accurate or that a linear vehicle effect is appropriate. The main analysis retains them, with explicit influence/functional-form sensitivity checks. The numeric 99 record is not a missing-data exclusion candidate.

Dwelling code 9 is explicitly Unknown (printed p. 17 / PDF p. 22); 9 such records remain labeled Unknown in EDA. Complete-case models requiring a known dwelling have 93,298 households. Models without dwelling need not exclude them. Advance-letter code 9 is also Unknown but does not require row exclusion when that survey-process field is not a predictor.

The guide confirms home workers are already included in full-/part-time employment counts (p. 18), separate employment/student statuses can overlap and ages 6-10 are assumed full-time students (p. 2), and 2006 recorded trips cover ages 11+ (pp. 1, 51). Numeric 9 in licence, employment, or student counts is not automatically an unknown code. Region mapping correctly uses the 2001 zone system for gta01hhld (p. 14), even though the survey is from 2006.

## Full-data findings and variable roles

Trips average 5.643, with median 4, maximum 55, and 10,480 zero-trip households (11.23%). Keep zeros, overlapping statuses, and high outcomes unless independent evidence justifies a narrower study population. All existing raw numeric/code and within-household consistency checks pass.

| variable | provisional_role | reason | encoding |
| --- | --- | --- | --- |
| hnum | Exclude from predictors | Household ID for traceability | No encoding |
| gta01hhld | Aggregation / clustering | Zone identifier; numerical spacing has no quantitative meaning; consider zone-clustered uncertainty later | Do not enter as a numeric slope or blindly create 1,178 dummies |
| nperson | Core candidate | Retain exact counts initially; inspect diminishing increments; includes children under 11 | Numeric count; do not automatically one-hot encode |
| nvehicle_clean | Core candidate / alternative access measure | All recorded counts 0-99 retained per guide; extreme values are numeric influence/sensitivity candidates; compare with licensed drivers | Numeric count; consider justified nonlinear specification later |
| nlicence | Core candidate / alternative access measure | Shares household-size and mobility-access information; use design VIF rather than marginal correlations alone | Numeric count |
| nempft | Composition candidate | Use with nemppt OR replace both by workers; not all three | Numeric count |
| nemppt | Composition candidate | Separate coefficient can represent a different association from full-time employment | Numeric count |
| workers | Alternative to nempft + nemppt | Exact arithmetic sum; including all three creates perfect collinearity | Numeric count |
| nemphome | Optional composition refinement | Already included in employment totals; adding as a separate regressor is a conditional contrast, not adding people; do not add again to workers | Numeric count; assess adjusted contribution later |
| nstudent | Composition candidate | Can overlap employment; includes ages 6-10 while trips are recorded for ages 11+; interpret association carefully | Numeric count |
| dwelltype_clean / dwelling | Candidate categorical control | House, Apartment, Townhouse; nine source-documented unknowns need a missing-data decision; never treat code 9 as a dwelling magnitude | Known categories: 2 indicators plus intercept, House reference; Unknown fourth level only as explicit sensitivity |
| tripday / weekday | Candidate categorical control | Monday-Friday are categories; coding 1-5 numerically would impose an equal linear daily increment | 4 indicators plus intercept, Monday reference |
| region | Optional geographic control | Derived from documented zone ranges; broad geographic differences can confound household associations | 3 indicators plus intercept, Toronto reference |
| rec-mail | Exclude from substantive predictor set | Advance-letter receipt describes survey administration; code 9 is unknown; optional nonresponse/survey sensitivity only | If explicitly studied later: Y/N indicator and separate unknown handling |
| n-call | Exclude from substantive predictor set | Interview completion / edits describe survey process rather than a household travel-generating characteristic | No main-model encoding |
| expf | Weight / expansion | Not a trip-generating predictor; state an explicit weighting convention and use it consistently for observed and predicted totals | Not an explanatory variable |
| nhhldtrip | Outcome | Recorded weekday person trips; retain zeros; count-valued/skewed outcome does not by itself forbid assigned linear regression | Numeric outcome; do not one-hot encode |
| split / flags / display categories | Exclude from substantive predictor set | Historical partition labels, diagnostic flags, and display caps are not substantive regressors; do not include both raw and derived copies | No automatic encoding |

Use k-1 indicator columns with an intercept for included categorical controls: two for known dwelling types, four for weekdays, and three for region. Counts may start numeric, with justified nonlinear alternatives. The nine Unknown dwellings may be handled through a documented complete-case rule or a sparse Unknown-category sensitivity; do not silently map Unknown to House. No imputation is performed.

## Predictor matrix checks

| scenario | available_n | unavailable_n | columns_including_intercept | rank | full_rank | standardized_condition_number | max_column_VIF | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Size and licensed drivers | 93307 | 0 | 3 | 3 | True | 1.9962 | 1.559 | Candidate design only; no outcome model fitted |
| Size and vehicles | 93307 | 0 | 3 | 3 | True | 1.5343 | 1.1947 | Candidate design only; no outcome model fitted |
| Size, drivers and vehicles | 93307 | 0 | 4 | 4 | True | 2.6632 | 2.2396 | Candidate design only; no outcome model fitted |
| Separate employment counts + controls | 93298 | 9 | 17 | 17 | True | 3.9871 | 3.1593 | Candidate design only; no outcome model fitted |
| Total workers alternative + controls | 93298 | 9 | 16 | 16 | True | 3.9212 | 3.1018 | Candidate design only; no outcome model fitted |
| Invalid: workers and both employment components | 93307 | 0 | 8 | 7 | False | inf |  | Do not fit: exact linear dependence |

VIF measures predictor overlap in the specified design, not individual outliers. Check matrix rank as well. workers is exactly nempft + nemppt, so do not include all three. Separate home-worker counts can enter as conditional composition predictors but must not be added again to workers. Do not select variables from marginal correlations or VIF cutoffs alone. Full designs, leverage, and vehicle-form sensitivities appear in the later review sections. Residual patterns, influence on estimated coefficients, functional form, and appropriate uncertainty require fitted candidate models.

## Review flags and weighting

| flag | households | decision |
| --- | --- | --- |
| vehicle_numeric_99_review | 1 | Review only; no deletion |
| unknown_dwelling_9 | 9 | Review only; no deletion |
| known_vehicles_at_least_10 | 33 | Review only; no deletion |
| household_size_at_least_10 | 58 | Review only; no deletion |
| recorded_trips_at_least_30 | 112 | Review only; no deletion |

Flags overlap and never automatically delete rows. expf is an expansion factor, not a substantive predictor. Printed page 4 explains expansion using census dwelling-unit controls and common factors within expansion zones. Expansion zones need not equal the traffic zones used for model aggregation. The survey used later-phase sampling adjustments for multi-unit dwellings (p. 2), so similar weighted/unweighted overall means alone do not establish that weights can be ignored. State the estimation/expansion convention, apply weights consistently to observed and predicted totals, and consider zone-clustered uncertainty subject to available survey-design information.

Using the full dataset follows the revised project direction. Any fit/error measured on those same records is in-sample, not held-out predictive accuracy. No regression notebook exists yet.

## Reproducing and supporting sources

Run Household_EDA_updated.ipynb top to bottom using the selected geo_env kernel. The notebook regenerates these tables and reports; it does not read or overwrite the historical split assignment, traiining.csv, testing.csv, or DP04_split_summary.csv. DP04_sample_summary.csv contains current full-data counts. Section 20 records the dictionary reconciliation, including published versus project vehicle frequencies. The older split artifacts retain the prior workflow and should not be interpreted as current coding policy.

- [Source data guide](../inputs/dataguide2006_v1.pdf): printed pp. 1-4, 14, 16-18, 50-53.
- [Statsmodels treatment coding](https://www.statsmodels.org/v0.12.2/examples/notebooks/generated/contrasts.html).
- [Statsmodels VIF](https://www.statsmodels.org/dev/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html).

## Subsequent explicit modeling decision

The user has requested exclusion of hnum=422873 (recorded nvehicle=99; House; Excel row 27629) from modeling. The current input is intermediaries/households_modeling.csv with 93,306 households; modeling_exclusions.csv records the reason. If known dwelling is required, 93,297 are available. The full-source EDA and prepared master above retain all 93,307 source households, and earlier diagnostic samples retain their stated definitions. Recompute model-selection diagnostics on the final agreed common modeling sample. Broader vehicle-tail exclusions and the feature-selection procedure remain undecided; no regression has been fitted.
