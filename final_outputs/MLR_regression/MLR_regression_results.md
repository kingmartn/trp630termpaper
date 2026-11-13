# Multiple linear regression: simple and alternative specifications

## Sample and split

This notebook regenerates the common split from sorted source household IDs with NumPy PCG64 seed 42 and 30% assigned to test before exclusions. It verifies exact agreement with the split saved by EDA. It applies the previously chosen vehicle >=10 and unknown-dwelling exclusions to both partitions. The eligible sample is 93,265 households: 65,287 training and 27,978 reserved test. Zero-trip households are retained. The source workbook remains unchanged.

## Simple starting specification

The prespecified starting model uses household persons (`nperson`), vehicles (`nvehicle`), full-time workers (`nempft`), and students (`nstudent`). These four predictors were fixed before the broader search. Its fitted equation is:

Predicted trips = 3.30267 +0.46646 * size_c +1.05203 * vehicles_c +0.93750 * full_time +1.61535 * students

Here `size_c = nperson - 3` and `vehicles_c = nvehicle - 1`. The simple model has training R-squared 0.4350, reserved-test RMSE 3.4611, and reserved-test MAE 2.4827. Its coefficients and exploratory 99% zone-clustered intervals are below.

| column | estimate | SE_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered |
| --- | --- | --- | --- | --- | --- |
| Intercept | 3.302668 | 0.04083345 | <1e-300 | 3.197314 | 3.408022 |
| size_c | 0.466461 | 0.02079633 | 8.29e-93 | 0.4128047 | 0.5201173 |
| vehicles_c | 1.052029 | 0.02119723 | 7.35e-289 | 0.9973381 | 1.106719 |
| full_time | 0.9375002 | 0.02121198 | 1.04e-250 | 0.8827715 | 0.9922289 |
| students | 1.615346 | 0.0278474 | <1e-300 | 1.543497 | 1.687194 |

The transportation basis and interpretation limits for all candidate effects are in [feature_rationale.md](feature_rationale.md).

## Model search

Survey weekday was removed from the alternative predictor set after the earlier evaluation to simplify the specification; the revised test results remain internal validation.

The declared effect space contains household size, vehicles, licensed drivers, separate or total employment counts, home workers, students, dwelling type, region, optional size-by-driver and size-by-vehicle interactions. Every main effect, including household size, is optional. Categorical levels move as whole factors, workers cannot accompany separate employment counts, and hierarchy is enforced. All 1,040 valid effect subsets were scored on training data by Gaussian OLS AIC and BIC. Interactions are optional predictors in a model that remains linear in coefficients. The squared terms were removed after the first evaluation because their parabolic form made predicted trips fall at high vehicle counts and produced negative predictions.

The primary choice is the lowest-BIC valid subset whose removable whole effects have zone-clustered p<0.01. It has BIC rank 1 among all scored models. 1 BIC-ranked model(s) required clustered screening. AIC/BIC are working unweighted Gaussian criteria. The 99% clustered intervals below are exploratory after selection, and none is claimed to have selection-adjusted coverage.

## Selected equation and performance

Retained effects: size, vehicles, drivers, full_time, part_time, home_workers, students, dwelling.

Predicted trips = 3.52734 +0.21385 * size_c +0.51966 * vehicles_c +0.59950 * drivers_c +0.99144 * full_time +1.14031 * part_time -0.17730 * home_workers +1.56390 * students -0.63837 * dwelling_Apartment -0.20557 * dwelling_Townhouse

Here `size_c = size - 3`, `vehicles_c = vehicles - 1`, and `drivers_c = licensed drivers - 2`; interaction columns use these centered values. The model has 10 coefficients including its intercept. Training R-squared is 0.4628. Training RMSE is 3.3342; reserved-test RMSE is 3.3695 and reserved-test MAE is 2.4117. These are household trip-count errors, not causal effects. The best additive linear model, which contains no interactions, has reserved-test RMSE 3.3695.

| model | effects | parameters | train_rmse | train_mae | test_rmse | test_mae | test_mean_prediction_error | test_negative_predictions | n_train | n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept-only mean |  | 1 | 4.5489 | 3.43358 | 4.59316 | 3.45047 | -0.00189 | 0 | 65287 | 27978 |
| Simple four-predictor model | size + vehicles + full_time + students | 5 | 3.41932 | 2.45838 | 3.46114 | 2.48271 | 0.01753 | 0 | 65287 | 27978 |
| Size and licensed drivers | size + drivers | 3 | 3.60181 | 2.57804 | 3.64754 | 2.60237 | 0.01653 | 0 | 65287 | 27978 |
| Best additive linear model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling | 10 | 3.33418 | 2.39338 | 3.36947 | 2.41174 | 0.0186 | 0 | 65287 | 27978 |
| Selected alternative model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling | 10 | 3.33418 | 2.39338 | 3.36947 | 2.41174 | 0.0186 | 0 | 65287 | 27978 |

The centered main coefficients describe conditional slopes at three persons, one vehicle, and two licensed drivers. When retained, interactions allow the licence-holder and vehicle slopes to vary with household size. [The vehicle-response figure](figures/MLR_04_vehicle_response.png) uses the revised model. The `Derived_MLR` sheet reports these slopes, and `Negative_predictions` lists every negative prediction without clipping.

## Derived quantities

| Quantity | Value | Unit | Reference / denominator | Sample | Source / formula |
| --- | ---: | --- | --- | --- | --- |
| Outcome n | 65287 | households | training households | training | nhhldtrip; sample SD uses ddof=1 |
| Outcome mean | 5.642364 | trips | training households | training | nhhldtrip; sample SD uses ddof=1 |
| Outcome SD | 4.548931 | trips | training households | training | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero count | 7274 | households | training households | training | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero share | 0.1114157 | proportion | training households | training | nhhldtrip; sample SD uses ddof=1 |
| Negative prediction count | 0 | households | training | training | Selected model: prediction < 0 |
| Minimum prediction | 0.7426105 | trips | training | training | Selected prediction minimum across all households |
| Minimum negative prediction | nan | trips | negative predictions | training | Minimum restricted to prediction < 0; NA if none |
| Negative prediction vehicle min | nan | vehicles | negative predictions | training | nvehicle among negative predictions; NA if none |
| Negative prediction vehicle max | nan | vehicles | negative predictions | training | nvehicle among negative predictions; NA if none |
| Outcome n | 27978 | households | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome mean | 5.644256 | trips | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome SD | 4.593239 | trips | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero count | 3200 | households | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero share | 0.1143756 | proportion | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Negative prediction count | 0 | households | test | test | Selected model: prediction < 0 |
| Minimum prediction | 0.7426105 | trips | test | test | Selected prediction minimum across all households |
| Minimum negative prediction | nan | trips | negative predictions | test | Minimum restricted to prediction < 0; NA if none |
| Negative prediction vehicle min | nan | vehicles | negative predictions | test | nvehicle among negative predictions; NA if none |
| Negative prediction vehicle max | nan | vehicles | negative predictions | test | nvehicle among negative predictions; NA if none |
| BIC rank 2 minus rank 1 | 4.968416 | BIC | rank 1 | training | MLR04: BIC[2] - BIC[1] |
| Rank 2 omits from rank 1 | none | effects | rank 1 | training | Set difference of candidate effects |
| Best additive BIC rank | 1 | rank | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Best additive BIC gap to rank 1 | 0 | BIC | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Best additive R squared | 0.4627632 | R squared | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Licence-holder slope; persons=1 | 0.5995043 | trips per unit | persons=1; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=1 | 0.5196567 | trips per unit | persons=1; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=2 | 0.5995043 | trips per unit | persons=2; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=2 | 0.5196567 | trips per unit | persons=2; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=3 | 0.5995043 | trips per unit | persons=3; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=3 | 0.5196567 | trips per unit | persons=3; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=4 | 0.5995043 | trips per unit | persons=4; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=4 | 0.5196567 | trips per unit | persons=4; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=5 | 0.5995043 | trips per unit | persons=5; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=5 | 0.5196567 | trips per unit | persons=5; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Unadjusted Durham minus Toronto | 1.39489 | trips | Toronto | training | Regional means difference |
| Adjusted Durham minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |
| Unadjusted York minus Toronto | 1.773869 | trips | Toronto | training | Regional means difference |
| Adjusted York minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |
| Unadjusted Peel minus Toronto | 1.570548 | trips | Toronto | training | Regional means difference |
| Adjusted Peel minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |

## Candidate leaders and coefficient uncertainty

| bic_rank | aic_rank | effects | parameters | aic | bic | selected_alternative |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 13 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling | 10 | 342537.2 | 342628 | 1 |
| 2 | 9 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_drivers | 11 | 342533 | 342633 | 0 |
| 3 | 3 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region | 13 | 342515.4 | 342633.5 | 0 |
| 4 | 2 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_by_drivers | 14 | 342511.5 | 342638.7 | 0 |
| 5 | 16 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_vehicles | 11 | 342538.9 | 342638.9 | 0 |
| 6 | 25 | size + vehicles + drivers + full_time + part_time + students + dwelling | 9 | 342557.5 | 342639.3 | 0 |
| 7 | 6 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_drivers + size_by_vehicles | 12 | 342531.1 | 342640.1 | 0 |
| 8 | 27 | size + vehicles + drivers + workers + home_workers + students + dwelling | 9 | 342560.2 | 342642 | 0 |
| 9 | 4 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_by_vehicles | 14 | 342517.2 | 342644.4 | 0 |
| 10 | 20 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_by_drivers | 10 | 342554 | 342644.9 | 0 |
| 11 | 11 | size + vehicles + drivers + full_time + part_time + students + dwelling + region | 12 | 342535.8 | 342644.9 | 0 |
| 12 | 1 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_by_drivers + size_by_vehicles | 15 | 342509.6 | 342645.9 | 0 |
| 13 | 12 | size + vehicles + drivers + workers + home_workers + students + dwelling + region | 12 | 342536.9 | 342645.9 | 0 |
| 14 | 23 | size + vehicles + drivers + workers + home_workers + students + dwelling + size_by_drivers | 10 | 342557.2 | 342648.1 | 0 |
| 15 | 26 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_by_vehicles | 10 | 342559.4 | 342650.2 | 0 |
| 16 | 7 | size + vehicles + drivers + full_time + part_time + students + dwelling + region + size_by_drivers | 13 | 342532.6 | 342650.7 | 0 |
| 17 | 31 | size + vehicles + drivers + workers + students + dwelling | 8 | 342578.5 | 342651.2 | 0 |
| 18 | 18 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_by_drivers + size_by_vehicles | 11 | 342552.1 | 342652.1 | 0 |
| 19 | 10 | size + vehicles + drivers + workers + home_workers + students + dwelling + region + size_by_drivers | 13 | 342534 | 342652.2 | 0 |
| 20 | 28 | size + vehicles + drivers + workers + home_workers + students + dwelling + size_by_vehicles | 10 | 342562 | 342652.9 | 0 |

| effect | df_effect | clustered_F | p_clustered | p_classical | df_cluster_denominator | protected_or_hierarchy |
| --- | --- | --- | --- | --- | --- | --- |
| size | 1 | 110.8179 | 8.23e-25 | 4.27e-39 | 1157 | Eligible for removal |
| vehicles | 1 | 492.4466 | 3.47e-91 | 2.15e-132 | 1157 | Eligible for removal |
| drivers | 1 | 528.6928 | 1.17e-96 | 6.53e-157 | 1157 | Eligible for removal |
| full_time | 1 | 2088.785 | 2.02e-261 | <1e-300 | 1157 | Eligible for removal |
| part_time | 1 | 1013.146 | 3.27e-160 | <1e-300 | 1157 | Eligible for removal |
| home_workers | 1 | 12.18507 | 0.00050 | 2.28e-06 | 1157 | Eligible for removal |
| students | 1 | 3253.881 | <1e-300 | <1e-300 | 1157 | Eligible for removal |
| dwelling | 2 | 196.6326 | 3.08e-74 | 2.2e-81 | 1157 | Eligible for removal |

| column | effect | estimate | SE_zone_clustered | t_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered | p_classical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept | Intercept | 3.527341 | 0.04446833 | 79.32255 | <1e-300 | 3.412609 | 3.642074 | <1e-300 |
| size_c | size | 0.2138497 | 0.02031439 | 10.52701 | 8.23e-25 | 0.1614369 | 0.2662626 | 4.27e-39 |
| vehicles_c | vehicles | 0.5196567 | 0.02341731 | 22.19114 | 3.47e-91 | 0.459238 | 0.5800753 | 2.15e-132 |
| drivers_c | drivers | 0.5995043 | 0.02607298 | 22.99332 | 1.17e-96 | 0.5322338 | 0.6667748 | 6.53e-157 |
| full_time | full_time | 0.9914363 | 0.02169292 | 45.70323 | 2.02e-261 | 0.9354667 | 1.047406 | <1e-300 |
| part_time | part_time | 1.140308 | 0.03582499 | 31.82996 | 3.27e-160 | 1.047876 | 1.232739 | <1e-300 |
| home_workers | home_workers | -0.1773019 | 0.05079246 | -3.490712 | 0.00050 | -0.3083508 | -0.04625299 | 2.28e-06 |
| students | students | 1.563896 | 0.02741619 | 57.0428 | <1e-300 | 1.49316 | 1.634633 | <1e-300 |
| dwelling_Apartment | dwelling | -0.6383663 | 0.03257127 | -19.59906 | 4.42e-74 | -0.7224029 | -0.5543296 | 9.15e-83 |
| dwelling_Townhouse | dwelling | -0.2055706 | 0.05548989 | -3.704649 | 0.00022 | -0.3487392 | -0.06240192 | 5.02e-05 |

## Diagnostics and zone evaluation

Training residual skewness is 1.468 and excess kurtosis is 5.836. 977 training records have absolute externally studentized residuals above 3; these are review markers and are retained. There are 0 negative reserved-test predictions. Count-outcome and survey-weight limitations remain relevant. The data guide records trips only for persons aged 11+, while the student count includes assumed students aged 6-10.

| evaluation | zones | MAE | RMSE | mean_prediction_error_pred_minus_obs | status |
| --- | --- | --- | --- | --- | --- |
| Sample zone totals | 1081 | 14.4721 | 20.3464 | 0.4815 | Reserved-test zone agreement |
| Expansion-weighted zone totals | 1081 | 279.7824 | 396.3453 | 11.2632 | Reserved-test zone agreement |

| evaluation | observed_mean | predicted_mean | MAE | RMSE | mean_prediction_error |
| --- | --- | --- | --- | --- | --- |
| Unweighted reserved-test households | 5.6443 | 5.6629 | 2.4117 | 3.3695 | 0.0186 |
| Expansion-weighted reserved-test households; coefficients still unweighted OLS | 5.643 | 5.6655 | 2.4097 | 3.3678 | 0.0225 |

Traffic-zone sample and expanded totals use the same reserved-test records. Expansion factors are applied consistently to observed and predicted totals. The expanded sums cover the test subset and are not full-population zone totals. Coefficients are unweighted OLS. The cross-classification comparison uses the same eligible IDs and seeded split.

## Reproduction and files

Run `MLR_regression.ipynb` top to bottom from the project root with the requirements in requirements.txt. `final_outputs/MLR_regression/MLR_regression_results.xlsx` contains the full candidate list, coefficient and diagnostic tables, the vehicle-response table, working sample, exclusions, and both prediction sets. `selected_MLR_regression_model.json` records the equation, selection settings, source hash, and split hashes. Figures are saved in `final_outputs/MLR_regression/figures`.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90

Training ID SHA256: 33d1751c366913aa05976c98b1413a4ebc17b61e62cdba8c341555c2a2214c46

Test ID SHA256: 2f1bc1fc90f8e2a1a7c4c9f226d3e118ec37957be6cb0a30dfe42dace9b1e9de
