# Trial mode: broad linear-regression search

## Assignment alignment and sample

The supplied project assignment requires a common, reproducible training/test split for multiple linear regression and cross-classification, model refinement using training data, and evaluation on reserved test data. This notebook reuses `intermediaries/EDA_training.xlsx` by household ID. It applies the previously chosen vehicle >=10 and unknown-dwelling exclusions to both partitions. The eligible sample is 93,265 households: 65,283 training and 27,982 reserved test. Zero-trip households are retained. The source workbook remains unchanged.

## Model search

The declared effect space contains household size, vehicles, licensed drivers, separate or total employment counts, home workers, students, dwelling type, weekday, region, optional size and vehicle squares, and optional size-by-driver and size-by-vehicle interactions. Household size is required. Categorical levels move as whole factors, workers cannot accompany separate employment counts, and hierarchy is enforced. All 4,800 valid effect subsets were scored on training data by Gaussian OLS AIC and BIC. Squared terms and interactions are optional predictors in a model that remains linear in coefficients.

The primary choice is the lowest-BIC valid subset whose removable whole effects have zone-clustered p<0.01. It has BIC rank 1 among all scored models. 1 BIC-ranked model(s) required clustered screening. AIC/BIC are working unweighted Gaussian criteria. The 99% clustered intervals below are exploratory after selection, and none is claimed to have selection-adjusted coverage.

## Selected equation and performance

Retained effects: size, vehicles, drivers, full_time, part_time, home_workers, students, dwelling, weekday, size_squared, vehicles_squared, size_by_drivers, size_by_vehicles.

Predicted trips = 3.41432 +0.23963 * size_c +0.83491 * vehicles_c +0.48299 * drivers_c +0.97067 * full_time +1.16695 * part_time -0.21181 * home_workers +1.58012 * students -0.55246 * dwelling_Apartment -0.16865 * dwelling_Townhouse +0.13455 * weekday_Tuesday +0.18250 * weekday_Wednesday +0.15706 * weekday_Thursday +0.29995 * weekday_Friday -0.06538 * size_c_squared -0.17201 * vehicles_c_squared +0.04643 * size_x_drivers +0.11467 * size_x_vehicles

Here `size_c = size - 3`, `vehicles_c = vehicles - 1`, and `drivers_c = licensed drivers - 2`; squared and interaction columns use these centered values. The model has 18 coefficients including its intercept. Training R-squared is 0.4679. Training RMSE is 3.3407; reserved-test RMSE is 3.3200 and reserved-test MAE is 2.3749. These are household trip-count errors, not causal effects. The best additive linear model, which contains no squares or interactions, has reserved-test RMSE 3.3290.

| model | effects | parameters | train_rmse | train_mae | test_rmse | test_mae | test_mean_prediction_error | test_negative_predictions | n_train | n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept-only mean |  | 1 | 4.57989 | 3.45137 | 4.52075 | 3.41264 | 0.03045 | 0 | 65283 | 27982 |
| Size and licensed drivers | size + drivers | 3 | 3.62349 | 2.59393 | 3.59716 | 2.56427 | 0.01006 | 0 | 65283 | 27982 |
| Best additive linear model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday | 14 | 3.34983 | 2.40417 | 3.32902 | 2.38181 | 0.0175 | 0 | 65283 | 27982 |
| Primary trial model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 18 | 3.34071 | 2.39707 | 3.31998 | 2.37489 | 0.0181 | 2 | 65283 | 27982 |

## Candidate leaders and coefficient uncertainty

| bic_rank | aic_rank | effects | parameters | aic | bic | selected_primary_trial |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 18 | 342787.8 | 342951.4 | 1 |
| 2 | 4 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_vehicles | 17 | 342797.9 | 342952.4 | 0 |
| 3 | 13 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 14 | 342834 | 342961.2 | 0 |
| 4 | 17 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_vehicles | 13 | 342843.6 | 342961.7 | 0 |
| 5 | 1 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 21 | 342780 | 342970.8 | 0 |
| 6 | 6 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342817.3 | 342971.8 | 0 |
| 7 | 3 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_vehicles | 20 | 342790.5 | 342972.2 | 0 |
| 8 | 10 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + size_squared + vehicles_squared + size_by_vehicles | 16 | 342828.6 | 342974 | 0 |
| 9 | 9 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342827.2 | 342981.7 | 0 |
| 10 | 23 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 13 | 342863.7 | 342981.9 | 0 |
| 11 | 14 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_squared + vehicles_squared + size_by_vehicles | 16 | 342837.1 | 342982.5 | 0 |
| 12 | 28 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_squared + vehicles_squared + size_by_vehicles | 12 | 342874.6 | 342983.6 | 0 |
| 13 | 11 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342829.2 | 342983.6 | 0 |
| 14 | 15 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_vehicles | 16 | 342842.2 | 342987.6 | 0 |
| 15 | 5 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 20 | 342808.9 | 342990.7 | 0 |
| 16 | 29 | size + vehicles + drivers + workers + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 13 | 342874.9 | 342993 | 0 |
| 17 | 8 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_vehicles | 19 | 342820.6 | 342993.3 | 0 |
| 18 | 34 | size + vehicles + drivers + workers + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_vehicles | 12 | 342887.4 | 342996.4 | 0 |
| 19 | 20 | size + vehicles + drivers + workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 16 | 342855.5 | 343000.9 | 0 |
| 20 | 7 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 20 | 342820 | 343001.7 | 0 |

| effect | df_effect | clustered_F | p_clustered | p_classical | df_cluster_denominator | protected_or_hierarchy |
| --- | --- | --- | --- | --- | --- | --- |
| size | 1 | 128.1397 | 3.02e-28 | 1.49e-33 | 1155 | Prespecified substantive core |
| vehicles | 1 | 739.1604 | 3.22e-126 | 6.6e-197 | 1155 | Required by hierarchy: vehicles_squared, size_by_vehicles |
| drivers | 1 | 386.8067 | 1.67e-74 | 1.86e-90 | 1155 | Required by hierarchy: size_by_drivers |
| full_time | 1 | 1914.96 | 1.97e-247 | <1e-300 | 1155 | Eligible for removal |
| part_time | 1 | 1001.62 | 8.38e-159 | <1e-300 | 1155 | Eligible for removal |
| home_workers | 1 | 18.29243 | 2.05e-05 | 2.07e-08 | 1155 | Eligible for removal |
| students | 1 | 3526.366 | <1e-300 | <1e-300 | 1155 | Eligible for removal |
| dwelling | 2 | 132.8503 | 1.18e-52 | 2.23e-58 | 1155 | Eligible for removal |
| weekday | 4 | 15.82256 | 1.29e-12 | 4.86e-11 | 1155 | Eligible for removal |
| size_squared | 1 | 41.04717 | 2.16e-10 | 7.21e-26 | 1155 | Eligible for removal |
| vehicles_squared | 1 | 122.6514 | 3.66e-27 | 1.06e-62 | 1155 | Eligible for removal |
| size_by_drivers | 1 | 7.700429 | 0.00561 | 0.00051 | 1155 | Eligible for removal |
| size_by_vehicles | 1 | 32.92021 | 1.23e-08 | 1.77e-15 | 1155 | Eligible for removal |

| column | effect | estimate | SE_zone_clustered | t_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered | p_classical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept | Intercept | 3.414319 | 0.05444546 | 62.71082 | <1e-300 | 3.273845 | 3.554794 | <1e-300 |
| size_c | size | 0.2396269 | 0.02116868 | 11.31988 | 3.02e-28 | 0.1850097 | 0.294244 | 1.49e-33 |
| vehicles_c | vehicles | 0.8349126 | 0.03070942 | 27.1875 | 3.22e-126 | 0.7556795 | 0.9141458 | 6.6e-197 |
| drivers_c | drivers | 0.4829886 | 0.02455782 | 19.6674 | 1.67e-74 | 0.4196271 | 0.54635 | 1.86e-90 |
| full_time | full_time | 0.9706698 | 0.02218154 | 43.76025 | 1.97e-247 | 0.9134394 | 1.0279 | <1e-300 |
| part_time | part_time | 1.16695 | 0.03687234 | 31.64839 | 8.38e-159 | 1.071816 | 1.262084 | <1e-300 |
| home_workers | home_workers | -0.2118128 | 0.04952408 | -4.276965 | 2.05e-05 | -0.3395895 | -0.08403605 | 2.07e-08 |
| students | students | 1.580119 | 0.02660886 | 59.38321 | <1e-300 | 1.511466 | 1.648773 | <1e-300 |
| dwelling_Apartment | dwelling | -0.5524632 | 0.03429903 | -16.10725 | 8.22e-53 | -0.6409579 | -0.4639686 | 1.1e-59 |
| dwelling_Townhouse | dwelling | -0.1686516 | 0.05457416 | -3.090319 | 0.00205 | -0.309458 | -0.02784515 | 0.00106 |
| weekday_Tuesday | weekday | 0.1345487 | 0.04212569 | 3.193982 | 0.00144 | 0.02586053 | 0.2432369 | 0.00171 |
| weekday_Wednesday | weekday | 0.1825025 | 0.04014671 | 4.545889 | 6.05e-06 | 0.07892025 | 0.2860847 | 2.38e-05 |
| weekday_Thursday | weekday | 0.15706 | 0.0408738 | 3.842559 | 0.00013 | 0.05160181 | 0.2625182 | 0.00020 |
| weekday_Friday | weekday | 0.2999455 | 0.03847832 | 7.795183 | 1.43e-14 | 0.2006679 | 0.3992231 | 3.9e-13 |
| size_c_squared | size_squared | -0.06537814 | 0.01020448 | -6.406807 | 2.16e-10 | -0.09170665 | -0.03904963 | 7.21e-26 |
| vehicles_c_squared | vehicles_squared | -0.1720144 | 0.01553204 | -11.07481 | 3.66e-27 | -0.2120885 | -0.1319403 | 1.06e-62 |
| size_x_drivers | size_by_drivers | 0.04642596 | 0.01673029 | 2.774965 | 0.00561 | 0.003260265 | 0.08959166 | 0.00051 |
| size_x_vehicles | size_by_vehicles | 0.114668 | 0.01998531 | 5.737614 | 1.23e-08 | 0.06310404 | 0.1662319 | 1.77e-15 |

## Diagnostics and zone evaluation

Training residual skewness is 1.427 and excess kurtosis is 5.442. 977 training records have absolute externally studentized residuals above 3; these are review markers and are retained. There are 2 negative reserved-test predictions. Count-outcome and survey-weight limitations remain relevant. The data guide records trips only for persons aged 11+, while the student count includes assumed students aged 6-10.

| evaluation | zones | MAE | RMSE | mean_prediction_error_pred_minus_obs | status |
| --- | --- | --- | --- | --- | --- |
| Sample zone totals | 1085 | 14.3652 | 19.9326 | 0.4669 | Reserved-test zone agreement |
| Expansion-weighted zone totals | 1085 | 277.8136 | 387.733 | 12.0551 | Reserved-test zone agreement |

| evaluation | observed_mean | predicted_mean | MAE | RMSE | mean_prediction_error |
| --- | --- | --- | --- | --- | --- |
| Unweighted reserved-test households | 5.6216 | 5.6397 | 2.3749 | 3.32 | 0.0181 |
| Expansion-weighted reserved-test households; coefficients still unweighted OLS | 5.6208 | 5.6449 | 2.3742 | 3.3189 | 0.0241 |

Traffic-zone sample and expanded totals use the same reserved-test records. Expansion factors are applied consistently to observed and predicted totals. Coefficients are unweighted OLS. The cross-classification comparison uses the same eligible IDs and split.

## Reproduction and files

Run `trial mode.ipynb` top to bottom from the project root with the requirements in requirements.txt. `final_outputs/trial_mode/trial_results.xlsx` contains the full candidate list, coefficient and diagnostic tables, working sample, exclusions, and both prediction sets. `selected_trial_model.json` records the equation, selection settings, source hash, and split hashes. Figures are saved in `final_outputs/trial_mode/figures`.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90

Training ID SHA256: bb94289bdbf54f5e1e0bf11f495a50ebf8e436e0f7602d41e9a24661bc14578a

Test ID SHA256: c88e225e3431d11c93be36b4616c52f99274554b9aceca236e26d60f0683ccce
