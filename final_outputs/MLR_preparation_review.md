# Full-dataset EDA and regression preparation review

The EDA retains all 93,307 supplied households across 1,179 zones. No training/test partition is used. The original workbook and historical split artifacts are preserved. No final regression sample, variable set, or row-deletion rule has been selected. This review diagnoses data and candidate predictor matrices; it does not fit a trip-outcome regression.

## Data findings

- Source checks find no blank analytical cells, duplicate household IDs, or failures of the existing numeric/code/within-household consistency checks. These checks do not establish that every unusual recorded value is correct.
- Vehicle code 99 is provisionally treated as unknown (1 household); known vehicle values reach 36. The existing interpretation of code 99 needs a source/class clarification before final modeling.
- Dwelling code 9 is Unknown (9 households), retained as a category in EDA. Unknown advance-letter responses do not justify dropping households when that survey-process field is excluded from a model.
- Trips average 5.643, with median 4, standard deviation 4.562, maximum 55, and 10,480 zero-trip households (11.23%). Retain zero-trip households. Outcome skewness alone is not a row-deletion rule.
- There are 32 households with at least 10 known vehicles. Inspect their source rows and later influence measures; the threshold is a review marker, not evidence that the records are wrong. Large households and high trip counts are also marked for inspection, without removal.
- Employment/student statuses can overlap. `workers = nempft + nemppt` exactly. Home workers are already included in those employment counts; adding them to the total would double count people. A separate home-worker regressor can instead estimate a conditional association.
- Household size includes residents under 11, and student counts include ages 6-10, while recorded person trips cover ages 11+. This limits interpretation of size/student coefficients and cannot be corrected by deleting arbitrary rows.

## Provisional variable and encoding choices

| variable | provisional_role | reason | encoding |
| --- | --- | --- | --- |
| hnum | Exclude from predictors | Household ID for traceability | No encoding |
| gta01hhld | Aggregation / clustering | Zone identifier; numerical spacing has no quantitative meaning; consider zone-clustered uncertainty later | Do not enter as a numeric slope or blindly create 1,178 dummies |
| nperson | Core candidate | Retain exact counts initially; inspect diminishing increments; includes children under 11 | Numeric count; do not automatically one-hot encode |
| nvehicle_clean | Core candidate / alternative access measure | One unknown; extreme known counts require source review; compare with licensed drivers | Numeric count; consider justified nonlinear specification later |
| nlicence | Core candidate / alternative access measure | Shares household-size and mobility-access information; use design VIF rather than marginal correlations alone | Numeric count |
| nempft | Composition candidate | Use with nemppt OR replace both by workers; not all three | Numeric count |
| nemppt | Composition candidate | Separate coefficient can represent a different association from full-time employment | Numeric count |
| workers | Alternative to nempft + nemppt | Exact arithmetic sum; including all three creates perfect collinearity | Numeric count |
| nemphome | Optional composition refinement | Already included in employment totals; adding as a separate regressor is a conditional contrast, not adding people; do not add again to workers | Numeric count; assess adjusted contribution later |
| nstudent | Composition candidate | Can overlap employment; includes ages 6-10 while trips are recorded for ages 11+; interpret association carefully | Numeric count |
| dwelltype_clean / dwelling | Candidate categorical control | House, Apartment, Townhouse; nine unknowns need a missing-data decision; never treat code 9 as a dwelling magnitude | Known categories: 2 indicators plus intercept, House reference; Unknown fourth level only as explicit sensitivity |
| tripday / weekday | Candidate categorical control | Monday-Friday are categories; coding 1-5 numerically would impose an equal linear daily increment | 4 indicators plus intercept, Monday reference |
| region | Optional geographic control | Derived from documented zone ranges; broad geographic differences can confound household associations | 3 indicators plus intercept, Toronto reference |
| rec-mail | Exclude from substantive predictor set | Advance-letter receipt describes survey administration; code 9 is unknown; optional nonresponse/survey sensitivity only | If explicitly studied later: Y/N indicator and separate unknown handling |
| n-call | Exclude from substantive predictor set | Interview completion / edits describe survey process rather than a household travel-generating characteristic | No main-model encoding |
| expf | Weight / expansion | Not a trip-generating predictor; state an explicit weighting convention and use it consistently for observed and predicted totals | Not an explanatory variable |
| nhhldtrip | Outcome | Recorded weekday person trips; retain zeros; count-valued/skewed outcome does not by itself forbid assigned linear regression | Numeric outcome; do not one-hot encode |
| split / flags / display categories | Exclude from substantive predictor set | Historical partition labels, diagnostic flags, and display caps are not substantive regressors; do not include both raw and derived copies | No automatic encoding |

For ordinary linear regression with an intercept, use reference-category coding (k-1 indicator columns) for included nominal factors. Do not put dwelling codes 1/2/3 or weekdays 1-5 directly into a numeric slope. Suggested references are House, Monday, and Toronto; the reference choice changes coefficient interpretation, not fitted values for an otherwise identical full-rank design. Formula interfaces can generate indicators automatically, so a separately saved one-hot-encoded dataset is unnecessary. Counts can start as numeric predictors; investigate functional form in the regression stage instead of automatically converting each count to dummies.

The nine unknown dwellings could be handled by a small complete-case reduction or an explicit Unknown-category sensitivity, depending on the final model. An Unknown coefficient supported by nine households would be weakly supported. Do not silently code an unknown dwelling as House. The one unknown vehicle needs a deliberate strategy if vehicles are included; omitting the vehicle predictor would remove that particular completeness requirement. No imputation has been performed.

## Predictor matrix checks

| scenario | available_n | unavailable_n | columns_including_intercept | rank | full_rank | standardized_condition_number | max_column_VIF | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Size and licensed drivers | 93307 | 0 | 3 | 3 | True | 1.9962 | 1.559 | Candidate design only; no outcome model fitted |
| Size and vehicles | 93306 | 1 | 3 | 3 | True | 1.575 | 1.2209 | Candidate design only; no outcome model fitted |
| Size, drivers and vehicles | 93306 | 1 | 4 | 4 | True | 2.7776 | 2.3727 | Candidate design only; no outcome model fitted |
| Separate employment counts + controls | 93297 | 10 | 17 | 17 | True | 4.0187 | 3.1598 | Candidate design only; no outcome model fitted |
| Total workers alternative + controls | 93297 | 10 | 16 | 16 | True | 3.9515 | 3.1027 | Candidate design only; no outcome model fitted |
| Invalid: workers and both employment components | 93306 | 1 | 8 | 7 | False | inf |  | Do not fit: exact linear dependence |

These samples are diagnostic availability counts only. The full main EDA sample remains 93,307. VIFs describe overlap in the specified predictor matrix, including correctly encoded categorical controls. They are not tests of causation or standalone criteria for deleting predictors. Indicator-column VIFs are not factor-level generalized VIFs. The standardized condition number uses centered/scaled predictor columns and an intercept; the invalid design has an exact arithmetic dependency.

Do not include workers, full-time workers, and part-time workers together. Compare a specification with separate full-/part-time coefficients against one using total workers. Compare vehicles and licensed drivers separately and together, guided by the access concept and these design checks. Marginal outcome correlations alone cannot decide which correlated or overlapping predictor adds adjusted information. Final model selection also needs coefficient stability, residual patterns, and influence checks after fitting.

## Rows and weighting: decisions still open

| flag | households | decision |
| --- | --- | --- |
| unknown_vehicle_99 | 1 | Review only; no deletion |
| unknown_dwelling_9 | 9 | Review only; no deletion |
| known_vehicles_at_least_10 | 32 | Review only; no deletion |
| household_size_at_least_10 | 58 | Review only; no deletion |
| recorded_trips_at_least_30 | 112 | Review only; no deletion |

Flag counts overlap. `MLR03_rows_for_review.csv` identifies individual households and reasons, without deleting records. Missing/unknown handling should depend on the chosen predictor set. Do not require known dwelling or vehicles for a model that does not use them. Do not drop respondents for unknown advance-letter receipt, zero trips, overlapping statuses, or an IQR flag alone.

`expf` is an expansion factor, not a substantive predictor. The EDA reports both weighted and unweighted trip means; similar overall means do not establish equal regression slopes. Decide explicitly whether estimation is unweighted OLS, expansion-weighted least squares, or an OLS primary analysis with weighting sensitivity. Later zone totals must apply the same weights to observed and predicted trips. Consider uncertainty clustered by residential zone, subject to the available survey-design information; the weight-only effective n is not a full survey-design effective sample size.

Using the whole dataset for estimation means fitted error measures describe in-sample fit. They must not be labeled held-out predictive performance. The previous assignment brief required a held-out comparison; the current notebook follows the user's revised full-data direction. No new validation partition has been introduced.

## Next regression stage

After agreeing on predictor roles and the small number of unresolved unknown/unusual records, create the separate multiple-linear-regression notebook. Fit a simple substantive specification and justified alternatives; then check functional form, residual variance, influential observations, implausible predictions, coefficient uncertainty, and zone-level agreement. Diagnose residual behavior after fitting rather than deciding exclusions from outcome tails beforehand. No original data rows have been removed.

## Method references

- [Statsmodels: contrasts and treatment coding](https://www.statsmodels.org/v0.12.2/examples/notebooks/generated/contrasts.html).
- [Statsmodels: variance inflation factor](https://www.statsmodels.org/dev/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html).

## Reproducing the analysis

From the project root, install `requirements_eda.txt` into the Python environment used by Jupyter and run `Household_EDA_updated.ipynb` from top to bottom. The notebook writes the prepared master, updated EDA figures/tables, these MLR preparation checks, and this report. It does not read, rewrite, or delete the historical split assignment, `traiining.csv`, `testing.csv`, or `DP04_split_summary.csv`; those files describe the earlier partitioned workflow. `DP04_sample_summary.csv` is the current full-data summary. No separate regression notebook exists yet.
