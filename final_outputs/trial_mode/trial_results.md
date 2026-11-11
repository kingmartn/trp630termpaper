# Trial mode: regression search results

## Data and agreed exclusions

The notebook reads inputs/households.xlsx, sheet 2006-hhld, named fields B:P, and creates an independent working copy. All source values and files remain intact. Recorded vehicles >=10 remove 33 households, and dwelling code 9 removes 9, with 0 overlapping households. The fixed estimation sample has 93,265 households in 1,179 residential zones. It retains 10,474 zero-trip households. Excluded records and reasons are saved in intermediaries/trial_mode/excluded_households.csv; the actual estimation data are households_trial.csv in that folder.

Numeric vehicle 99 is source-documented and is removed under the requested outlier policy, not converted to missing. The main EDA still describes the full source sample. No other row-exclusion rule was introduced.

## What was searched

Five starting families cover separate employment counts, total workers, size/vehicle quadratics, size-by-licensed-driver interaction, and size-by-vehicle interaction. Each has a p<0.01 backward path, a separate AIC-improving path, and a separate BIC-improving path. There are 15 terminal comparisons and 88 unique predictor designs evaluated including benchmarks. The three rules can converge to identical models. This is a defined backward search, not an exhaustive search of all possible models.

Household size remains as a prespecified core variable. Categorical factors are tested and removed as blocks, and interaction/quadratic hierarchy is preserved. workers never appears together with nempft/nemppt. Reference categories are House, Monday, and Toronto. Numeric centers are size 3, vehicles 1, and licensed drivers 2. No train/test split or cross-validation is performed.

Selection uses whole-effect F tests with covariance clustered by traffic zone, with denominator degrees of freedom 1178. The p<0.01 requirement applies to removable whole effects, not every individual indicator coefficient. Classical p-values are recorded separately. AIC/BIC-only paths can retain terms not meeting the p rule. AIC/BIC are working Gaussian OLS comparisons on identical records and are not a full correlated-error or survey likelihood. The criterion does not account for the adaptive search.

## Primary trial result

The lowest-BIC terminal p<0.01 path starts from **Size and vehicle curvature**. It retains:

size, vehicles, drivers, full_time, part_time, home_workers, students, dwelling, weekday, size_squared, vehicles_squared.

Effects removed along that primary p-value path: region.

| step | action | dropped_effect | dropped_effect_p_clustered | parameters | aic | bic |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | remove | region | 0.02476 | 19 | 489535.3 | 489714.7 |
| 1 | stop |  |  | 16 | 489548.5 | 489699.5 |

It has 16 fitted coefficients including the intercept, R-squared 0.4646, adjusted R-squared 0.4646, in-sample RMSE 3.3381, in-sample MAE 2.3903, working AIC 489548.457, and BIC 489699.548. Residual standard error sqrt(SSE/(n-p)) is 3.3384; prediction-error RMSE instead uses n. Mean prediction error is predicted minus observed.

| model | parameters | r_squared | adjusted_r_squared | rmse_in_sample | mae_in_sample | negative_predictions_n |
| --- | --- | --- | --- | --- | --- | --- |
| Intercept-only mean | 1 | 0 | 0 | 4.56222 | 3.43871 | 0 |
| Size and licensed drivers | 3 | 0.37193 | 0.37192 | 3.61558 | 2.58465 | 0 |
| Primary trial model | 16 | 0.46465 | 0.46456 | 3.33807 | 2.39031 | 0 |

## All terminal comparisons

| family | rule | steps_removed | parameters | adjusted_r_squared | rmse_in_sample | mae_in_sample | aic | bic | p01_satisfied_for_removable_effects |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Size and vehicle curvature | bic | 1 | 16 | 0.46456 | 3.33807 | 2.39031 | 489548.5 | 489699.5 | 1 |
| Size and vehicle curvature | p01 | 1 | 16 | 0.46456 | 3.33807 | 2.39031 | 489548.5 | 489699.5 | 1 |
| Size and vehicle curvature | aic | 0 | 19 | 0.46466 | 3.33773 | 2.39018 | 489535.3 | 489714.7 | 0 |
| Separate employment main effects | bic | 1 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Separate employment main effects | p01 | 1 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Size by licensed drivers | bic | 2 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Size by licensed drivers | p01 | 2 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Size by vehicles | bic | 2 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Size by vehicles | p01 | 2 | 14 | 0.46282 | 3.34352 | 2.39646 | 489849.1 | 489981.3 | 1 |
| Separate employment main effects | aic | 0 | 17 | 0.4629 | 3.34322 | 2.39639 | 489837.9 | 489998.5 | 0 |
| Size by vehicles | aic | 1 | 17 | 0.4629 | 3.34322 | 2.39639 | 489837.9 | 489998.5 | 0 |
| Size by licensed drivers | aic | 0 | 18 | 0.46295 | 3.34306 | 2.39601 | 489831.2 | 490001.1 | 0 |
| Total workers main effects | bic | 1 | 13 | 0.46253 | 3.34445 | 2.39725 | 489899 | 490021.7 | 1 |
| Total workers main effects | p01 | 1 | 13 | 0.46253 | 3.34445 | 2.39725 | 489899 | 490021.7 | 1 |
| Total workers main effects | aic | 0 | 16 | 0.46262 | 3.34412 | 2.39713 | 489886 | 490037.1 | 0 |

## Selected effects and coefficients

| effect | df_effect | clustered_F | p_clustered | p_classical | df_cluster_denominator | protected_or_hierarchy |
| --- | --- | --- | --- | --- | --- | --- |
| size | 1 | 235.1288 | 1.59e-48 | 5.73e-65 | 1178 | Prespecified substantive core |
| vehicles | 1 | 1102.772 | 3.3e-171 | 3.8e-234 | 1178 | Required by hierarchy: vehicles_squared |
| drivers | 1 | 603.3691 | 6.47e-108 | 2.43e-175 | 1178 | Eligible for removal |
| full_time | 1 | 2796.729 | <1e-300 | <1e-300 | 1178 | Eligible for removal |
| part_time | 1 | 1470.717 | 1.7e-209 | <1e-300 | 1178 | Eligible for removal |
| home_workers | 1 | 27.56572 | 1.8e-07 | 2e-12 | 1178 | Eligible for removal |
| students | 1 | 4781.81 | <1e-300 | <1e-300 | 1178 | Eligible for removal |
| dwelling | 2 | 177.8616 | 3.16e-68 | 5.07e-86 | 1178 | Eligible for removal |
| weekday | 4 | 17.69064 | 4.11e-14 | 1.8e-13 | 1178 | Eligible for removal |
| size_squared | 1 | 17.90784 | 2.5e-05 | 6.71e-13 | 1178 | Eligible for removal |
| vehicles_squared | 1 | 148.9338 | 2.42e-32 | 2.47e-49 | 1178 | Eligible for removal |

| column | effect | estimate | SE_zone_clustered | t_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered | p_classical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept | Intercept | 3.434713 | 0.04701701 | 73.05255 | <1e-300 | 3.313409 | 3.556017 | <1e-300 |
| size_c | size | 0.2429034 | 0.01584093 | 15.33391 | 1.59e-48 | 0.2020337 | 0.2837732 | 5.73e-65 |
| vehicles_c | vehicles | 0.7187033 | 0.02164247 | 33.20801 | 3.3e-171 | 0.6628655 | 0.7745411 | 3.8e-234 |
| drivers_c | drivers | 0.5368592 | 0.02185591 | 24.56357 | 6.47e-108 | 0.4804708 | 0.5932477 | 2.43e-175 |
| full_time | full_time | 0.9881935 | 0.01868602 | 52.88411 | <1e-300 | 0.9399834 | 1.036404 | <1e-300 |
| part_time | part_time | 1.186155 | 0.03092979 | 38.34993 | 1.7e-209 | 1.106356 | 1.265955 | <1e-300 |
| home_workers | home_workers | -0.2218902 | 0.04226233 | -5.250307 | 1.8e-07 | -0.3309274 | -0.112853 | 2e-12 |
| students | students | 1.557624 | 0.02252508 | 69.15063 | <1e-300 | 1.499509 | 1.615739 | <1e-300 |
| dwelling_Apartment | dwelling | -0.5601677 | 0.0298823 | -18.7458 | 8.04e-69 | -0.6372643 | -0.4830711 | 2.63e-87 |
| dwelling_Townhouse | dwelling | -0.2047667 | 0.04812837 | -4.254595 | 2.26e-05 | -0.3289384 | -0.08059508 | 1.63e-06 |
| weekday_Tuesday | weekday | 0.1317894 | 0.03535515 | 3.727589 | 0.00020 | 0.04057283 | 0.223006 | 0.00023 |
| weekday_Wednesday | weekday | 0.1518836 | 0.03377905 | 4.496386 | 7.59e-06 | 0.06473338 | 0.2390339 | 2.52e-05 |
| weekday_Thursday | weekday | 0.1578951 | 0.0329116 | 4.797551 | 1.81e-06 | 0.07298285 | 0.2428073 | 7.6e-06 |
| weekday_Friday | weekday | 0.2786816 | 0.03339327 | 8.345443 | 1.97e-16 | 0.1925267 | 0.3648366 | 7.65e-16 |
| size_c_squared | size_squared | -0.02794807 | 0.006604352 | -4.231765 | 2.5e-05 | -0.04498736 | -0.01090878 | 6.71e-13 |
| vehicles_c_squared | vehicles_squared | -0.1115848 | 0.009143415 | -12.20384 | 2.42e-32 | -0.1351749 | -0.08799471 | 2.47e-49 |

These 99% intervals and conventional p-values are exploratory and conditional on an adaptively selected model; nominal selection-adjusted coverage is not claimed. Extremely small p-values are printed as <1e-300 rather than an exact zero; CSV zeros can reflect numerical underflow. Substantive interpretation and practical magnitudes matter with this sample size. Estimated associations are not causal effects.

- Apartment versus House: -0.560 adjusted trips per weekday, 99% clustered interval [-0.637, -0.483], holding included covariates fixed.
- Townhouse versus House: -0.205 adjusted trips per weekday, 99% clustered interval [-0.329, -0.081], holding included covariates fixed.
- Tuesday versus Monday: +0.132 adjusted trips per weekday, holding included covariates fixed.
- Wednesday versus Monday: +0.152 adjusted trips per weekday, holding included covariates fixed.
- Thursday versus Monday: +0.158 adjusted trips per weekday, holding included covariates fixed.
- Friday versus Monday: +0.279 adjusted trips per weekday, holding included covariates fixed.
- With a retained size quadratic, the change for one additional resident varies with size. For the size-only polynomial component at size s it is b_size + b_size_squared * [2(s-3)+1]; add any retained size-interaction contribution.
- With a retained vehicle quadratic, the change for one additional vehicle at v is b_vehicles + b_vehicles_squared * [2(v-1)+1], plus any retained size-by-vehicle interaction contribution.

## Diagnostics and limits

There are 0 negative fitted trip counts; predictions were not clipped. The maximum classical Cook distance is 0.01672; 0 records exceed 1, and 5228 exceed the large-sample 4/n review marker. There are 1403 absolute externally studentized residuals above 3. These markers do not delete additional observations. The largest column VIF is 3.478; indicator-column VIFs are not generalized factor VIFs. Quadratic/interaction columns can share information with their supporting main effects.

Residual plots, Q-Q quantiles, and household group results must be inspected. The Koenker BP nominal p-value is <1e-300, a screen that is not adjusted for within-zone dependence. Primary uncertainty is zone-clustered. Classical influence measures are individual-case sensitivity diagnostics, not full cluster/survey influence calculations. Count outcomes and skewed residuals do not by themselves forbid OLS, but nonlinear misspecification, heteroskedasticity, heavy tails, negative predictions, and coefficient stability constrain interpretation. No model is declared a validated final forecasting model.

## Household groups and zones

| grouping | level | n | observed_mean_trips | predicted_mean_trips | MAE_in_sample | RMSE_in_sample | mean_prediction_error_pred_minus_obs | negative_predictions_n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Household size (5+) | 4 | 17463 | 8.3081 | 8.3289 | 3.1116 | 4.1722 | 0.0208 | 0 |
| Household size (5+) | 2 | 28809 | 4.3551 | 4.271 | 2.1491 | 2.8406 | -0.0841 | 0 |
| Household size (5+) | 3 | 17466 | 6.3997 | 6.4395 | 2.5177 | 3.338 | 0.0398 | 0 |
| Household size (5+) | 5+ | 10333 | 10.1639 | 10.1653 | 3.7036 | 4.9639 | 0.0014 | 0 |
| Household size (5+) | 1 | 19194 | 2.0286 | 2.0989 | 1.2732 | 1.6704 | 0.0703 | 0 |
| Vehicles (4+) | 2 | 31136 | 7.326 | 7.2991 | 2.8998 | 3.9449 | -0.0269 | 0 |
| Vehicles (4+) | 1 | 38365 | 4.8507 | 4.8365 | 2.2425 | 3.0584 | -0.0142 | 0 |
| Vehicles (4+) | 0 | 15291 | 2.3446 | 2.38 | 1.2927 | 1.7326 | 0.0354 | 0 |
| Vehicles (4+) | 3 | 6591 | 8.7322 | 8.857 | 3.1198 | 4.1173 | 0.1247 | 0 |
| Vehicles (4+) | 4+ | 1882 | 9.9277 | 9.9384 | 3.3371 | 4.5047 | 0.0107 | 0 |
| Dwelling | House | 58333 | 6.5647 | 6.5647 | 2.7038 | 3.708 | -0 | 0 |
| Dwelling | Apartment | 27974 | 3.6213 | 3.6213 | 1.7299 | 2.4071 | -0 | 0 |
| Dwelling | Townhouse | 6958 | 6.0434 | 6.0434 | 2.4174 | 3.286 | -0 | 0 |
| Weekday | Thursday | 19406 | 5.6232 | 5.6232 | 2.3285 | 3.2495 | -0 | 0 |
| Weekday | Wednesday | 17722 | 5.6805 | 5.6805 | 2.373 | 3.302 | -0 | 0 |
| Weekday | Friday | 21230 | 5.8627 | 5.8627 | 2.5565 | 3.5798 | -0 | 0 |
| Weekday | Tuesday | 18263 | 5.5617 | 5.5617 | 2.3404 | 3.2641 | -0 | 0 |
| Weekday | Monday | 16644 | 5.4348 | 5.4348 | 2.3237 | 3.2376 | -0 | 0 |
| Region | Toronto | 51588 | 4.9178 | 4.9076 | 2.1666 | 3.0452 | -0.0102 | 0 |
| Region | Durham | 9522 | 6.2737 | 6.1599 | 2.6858 | 3.7492 | -0.1138 | 0 |
| Region | York | 14218 | 6.7033 | 6.7521 | 2.699 | 3.6844 | 0.0488 | 0 |
| Region | Peel | 17937 | 6.5532 | 6.6042 | 2.6323 | 3.6118 | 0.051 | 0 |

| evaluation | zones | MAE | RMSE | mean_prediction_error_pred_minus_obs | status |
| --- | --- | --- | --- | --- | --- |
| Sample zone totals | 1179 | 30.5359 | 44.9426 | -0 | In-sample zone agreement |
| Expansion-weighted zone totals | 1179 | 590.696 | 875.2988 | 7.7505 | In-sample zone agreement |

| evaluation | observed_mean | predicted_mean | MAE | RMSE | mean_prediction_error |
| --- | --- | --- | --- | --- | --- |
| Unweighted households | 5.6429 | 5.6429 | 2.3903 | 3.3381 | -0 |
| Expansion-weighted households; coefficients still unweighted OLS | 5.6399 | 5.6449 | 2.387 | 3.3334 | 0.0051 |

Zone results use observed and fitted trips over the same estimation records. Sample totals and expansion-weighted totals are distinct; expf is applied identically to observed and predicted values. Coefficients are unweighted OLS. This is in-sample agreement, not held-out accuracy. A fair later comparison with cross-classification must use the same eligible records and weighting conventions.

## Reproduction and outputs

Run trial mode.ipynb top to bottom from the project root using geo_env (or an environment satisfying requirements.txt). The notebook is self-contained and does not import scripts from intermediaries/chat. TM00 records package versions. TM04-TM06 record every reduction step, whole-effect test, and information-criterion deletion alternative. TM07 compares terminal models; TM08-TM13 provide effects, coefficients, benchmarks, and diagnostics; TM14-TM17 give household/zone results. Household predictions are saved in intermediaries/trial_mode/selected_model_household_predictions.csv. selected_trial_model.json records coefficients, centers, references, criteria, row IDs hash, and source workbook hash.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90

Estimation-row ID SHA256: 5cfd54ebbf3c1ca85110663baaa5fcad2995df87abc9f6c54185c2dcb8e73882

Sources: [JMP variable selection](https://www.jmp.com/en/statistics-knowledge-portal/linear-models/what-is-multiple-regression/variable-selection), [Statsmodels clustered covariance](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.get_robustcov_results.html), [Statsmodels joint F tests](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.f_test.html), and the project data guide in inputs/dataguide2006_v1.pdf.
