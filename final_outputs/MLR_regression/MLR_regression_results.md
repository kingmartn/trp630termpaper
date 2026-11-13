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

The declared effect space contains household size, vehicles, licensed drivers, separate or total employment counts, home workers, students, dwelling type, weekday, region, optional size-by-driver and size-by-vehicle interactions. Every main effect, including household size, is optional. Categorical levels move as whole factors, workers cannot accompany separate employment counts, and hierarchy is enforced. All 2,080 valid effect subsets were scored on training data by Gaussian OLS AIC and BIC. Interactions are optional predictors in a model that remains linear in coefficients. The squared terms were removed after the first evaluation because their parabolic form made predicted trips fall at high vehicle counts and produced negative predictions.

The primary choice is the lowest-BIC valid subset whose removable whole effects have zone-clustered p<0.01. It has BIC rank 1 among all scored models. 1 BIC-ranked model(s) required clustered screening. AIC/BIC are working unweighted Gaussian criteria. The 99% clustered intervals below are exploratory after selection, and none is claimed to have selection-adjusted coverage.

## Selected equation and performance

Retained effects: size, vehicles, drivers, full_time, part_time, home_workers, students, dwelling, weekday.

Predicted trips = 3.38628 +0.21418 * size_c +0.51867 * vehicles_c +0.60043 * drivers_c +0.98897 * full_time +1.13838 * part_time -0.17641 * home_workers +1.56346 * students -0.63920 * dwelling_Apartment -0.20850 * dwelling_Townhouse +0.11539 * weekday_Tuesday +0.13771 * weekday_Wednesday +0.16044 * weekday_Thursday +0.27748 * weekday_Friday

Here `size_c = size - 3`, `vehicles_c = vehicles - 1`, and `drivers_c = licensed drivers - 2`; interaction columns use these centered values. The model has 14 coefficients including its intercept. Training R-squared is 0.4631. Training RMSE is 3.3330; reserved-test RMSE is 3.3683 and reserved-test MAE is 2.4102. These are household trip-count errors, not causal effects. The best additive linear model, which contains no interactions, has reserved-test RMSE 3.3683.

| model | effects | parameters | train_rmse | train_mae | test_rmse | test_mae | test_mean_prediction_error | test_negative_predictions | n_train | n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept-only mean |  | 1 | 4.5489 | 3.43358 | 4.59316 | 3.45047 | -0.00189 | 0 | 65287 | 27978 |
| Simple four-predictor model | size + vehicles + full_time + students | 5 | 3.41932 | 2.45838 | 3.46114 | 2.48271 | 0.01753 | 0 | 65287 | 27978 |
| Size and licensed drivers | size + drivers | 3 | 3.60181 | 2.57804 | 3.64754 | 2.60237 | 0.01653 | 0 | 65287 | 27978 |
| Best additive linear model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday | 14 | 3.33298 | 2.39163 | 3.36827 | 2.41015 | 0.01757 | 0 | 65287 | 27978 |
| Selected alternative model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday | 14 | 3.33298 | 2.39163 | 3.36827 | 2.41015 | 0.01757 | 0 | 65287 | 27978 |

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
| Minimum prediction | 0.5991799 | trips | training | training | Selected prediction minimum across all households |
| Minimum negative prediction | nan | trips | negative predictions | training | Minimum restricted to prediction < 0; NA if none |
| Negative prediction vehicle min | nan | vehicles | negative predictions | training | nvehicle among negative predictions; NA if none |
| Negative prediction vehicle max | nan | vehicles | negative predictions | training | nvehicle among negative predictions; NA if none |
| Outcome n | 27978 | households | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome mean | 5.644256 | trips | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome SD | 4.593239 | trips | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero count | 3200 | households | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Outcome zero share | 0.1143756 | proportion | test households | test | nhhldtrip; sample SD uses ddof=1 |
| Negative prediction count | 0 | households | test | test | Selected model: prediction < 0 |
| Minimum prediction | 0.5991799 | trips | test | test | Selected prediction minimum across all households |
| Minimum negative prediction | nan | trips | negative predictions | test | Minimum restricted to prediction < 0; NA if none |
| Negative prediction vehicle min | nan | vehicles | negative predictions | test | nvehicle among negative predictions; NA if none |
| Negative prediction vehicle max | nan | vehicles | negative predictions | test | nvehicle among negative predictions; NA if none |
| BIC rank 2 minus rank 1 | 2.499442 | BIC | rank 1 | training | MLR04: BIC[2] - BIC[1] |
| Rank 2 omits from rank 1 | weekday | effects | rank 1 | training | Set difference of candidate effects |
| Best additive BIC rank | 1 | rank | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Best additive BIC gap to rank 1 | 0 | BIC | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Best additive R squared | 0.4631485 | R squared | rank 1 for gap | training | MLR04: lowest BIC without interactions |
| Licence-holder slope; persons=1 | 0.6004314 | trips per unit | persons=1; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=1 | 0.5186692 | trips per unit | persons=1; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=2 | 0.6004314 | trips per unit | persons=2; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=2 | 0.5186692 | trips per unit | persons=2; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=3 | 0.6004314 | trips per unit | persons=3; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=3 | 0.5186692 | trips per unit | persons=3; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=4 | 0.6004314 | trips per unit | persons=4; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=4 | 0.5186692 | trips per unit | persons=4; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Licence-holder slope; persons=5 | 0.6004314 | trips per unit | persons=5; other predictors fixed | training | drivers_c + size_x_drivers * (persons - 3); absent effects = 0 |
| Vehicle slope; persons=5 | 0.5186692 | trips per unit | persons=5; other predictors fixed | training | vehicles_c + size_x_vehicles * (persons - 3); absent effects = 0 |
| Unadjusted Durham minus Toronto | 1.39489 | trips | Toronto | training | Regional means difference |
| Adjusted Durham minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |
| Unadjusted York minus Toronto | 1.773869 | trips | Toronto | training | Regional means difference |
| Adjusted York minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |
| Unadjusted Peel minus Toronto | 1.570548 | trips | Toronto | training | Regional means difference |
| Adjusted Peel minus Toronto | 0 | trips | Toronto | training | Selected region coefficient; zero if region omitted |

## Candidate leaders and coefficient uncertainty

| bic_rank | aic_rank | effects | parameters | aic | bic | selected_alternative |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 14 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday | 14 | 342498.3 | 342625.5 | 1 |
| 2 | 42 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling | 10 | 342537.2 | 342628 | 0 |
| 3 | 3 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region | 17 | 342474.9 | 342629.3 | 0 |
| 4 | 10 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_by_drivers | 15 | 342494.4 | 342630.7 | 0 |
| 5 | 37 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_drivers | 11 | 342533 | 342633 | 0 |
| 6 | 24 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region | 13 | 342515.4 | 342633.5 | 0 |
| 7 | 2 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_by_drivers | 18 | 342471.2 | 342634.8 | 0 |
| 8 | 16 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_by_vehicles | 15 | 342500.2 | 342636.4 | 0 |
| 9 | 28 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday | 13 | 342518.4 | 342636.6 | 0 |
| 10 | 7 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_by_drivers + size_by_vehicles | 16 | 342492.3 | 342637.7 | 0 |
| 11 | 19 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_by_drivers | 14 | 342511.5 | 342638.7 | 0 |
| 12 | 46 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_vehicles | 11 | 342538.9 | 342638.9 | 0 |
| 13 | 57 | size + vehicles + drivers + full_time + part_time + students + dwelling | 9 | 342557.5 | 342639.3 | 0 |
| 14 | 31 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday | 13 | 342521.6 | 342639.7 | 0 |
| 15 | 34 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_by_drivers + size_by_vehicles | 12 | 342531.1 | 342640.1 | 0 |
| 16 | 4 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_by_vehicles | 18 | 342476.7 | 342640.3 | 0 |
| 17 | 11 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + region | 16 | 342495.1 | 342640.5 | 0 |
| 18 | 1 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_by_drivers + size_by_vehicles | 19 | 342469.2 | 342641.8 | 0 |
| 19 | 12 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + region | 16 | 342496.5 | 342641.9 | 0 |
| 20 | 59 | size + vehicles + drivers + workers + home_workers + students + dwelling | 9 | 342560.2 | 342642 | 0 |

| effect | df_effect | clustered_F | p_clustered | p_classical | df_cluster_denominator | protected_or_hierarchy |
| --- | --- | --- | --- | --- | --- | --- |
| size | 1 | 110.9678 | 7.68e-25 | 3.18e-39 | 1157 | Eligible for removal |
| vehicles | 1 | 489.8241 | 8.72e-91 | 5.69e-132 | 1157 | Eligible for removal |
| drivers | 1 | 529.6789 | 8.34e-97 | 1.76e-157 | 1157 | Eligible for removal |
| full_time | 1 | 2080.789 | 8.42e-261 | <1e-300 | 1157 | Eligible for removal |
| part_time | 1 | 1006.14 | 2.13e-159 | <1e-300 | 1157 | Eligible for removal |
| home_workers | 1 | 12.06333 | 0.00053 | 2.54e-06 | 1157 | Eligible for removal |
| students | 1 | 3257.65 | <1e-300 | <1e-300 | 1157 | Eligible for removal |
| dwelling | 2 | 197.0948 | 2.18e-74 | 1.24e-81 | 1157 | Eligible for removal |
| weekday | 4 | 11.7877 | 2.18e-09 | 1.65e-09 | 1157 | Eligible for removal |

| column | effect | estimate | SE_zone_clustered | t_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered | p_classical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept | Intercept | 3.386277 | 0.05306155 | 63.81792 | <1e-300 | 3.249374 | 3.523181 | <1e-300 |
| size_c | size | 0.2141806 | 0.02033207 | 10.53413 | 7.68e-25 | 0.1617221 | 0.2666391 | 3.18e-39 |
| vehicles_c | vehicles | 0.5186692 | 0.02343529 | 22.13197 | 8.72e-91 | 0.4582041 | 0.5791342 | 5.69e-132 |
| drivers_c | drivers | 0.6004314 | 0.02608898 | 23.01475 | 8.34e-97 | 0.5331196 | 0.6677432 | 1.76e-157 |
| full_time | full_time | 0.9889744 | 0.02168059 | 45.61567 | 8.42e-261 | 0.9330367 | 1.044912 | <1e-300 |
| part_time | part_time | 1.138379 | 0.03588868 | 31.71971 | 2.13e-159 | 1.045783 | 1.230974 | <1e-300 |
| home_workers | home_workers | -0.1764105 | 0.05079148 | -3.473231 | 0.00053 | -0.3074569 | -0.04536418 | 2.54e-06 |
| students | students | 1.563465 | 0.02739276 | 57.07583 | <1e-300 | 1.492789 | 1.63414 | <1e-300 |
| dwelling_Apartment | dwelling | -0.6392045 | 0.03255571 | -19.63417 | 2.63e-74 | -0.723201 | -0.555208 | 5.13e-83 |
| dwelling_Townhouse | dwelling | -0.2084959 | 0.05546056 | -3.759354 | 0.00018 | -0.3515888 | -0.06540288 | 3.9e-05 |
| weekday_Tuesday | weekday | 0.1153949 | 0.04096143 | 2.817161 | 0.00493 | 0.009710967 | 0.2210789 | 0.00688 |
| weekday_Wednesday | weekday | 0.1377126 | 0.04123515 | 3.339689 | 0.00087 | 0.03132237 | 0.2441027 | 0.00141 |
| weekday_Thursday | weekday | 0.1604371 | 0.04135849 | 3.879182 | 0.00011 | 0.0537287 | 0.2671456 | 0.00014 |
| weekday_Friday | weekday | 0.2774774 | 0.04077163 | 6.805649 | 1.61e-11 | 0.1722831 | 0.3826717 | 1.81e-11 |

## Diagnostics and zone evaluation

Training residual skewness is 1.465 and excess kurtosis is 5.822. 982 training records have absolute externally studentized residuals above 3; these are review markers and are retained. There are 0 negative reserved-test predictions. Count-outcome and survey-weight limitations remain relevant. The data guide records trips only for persons aged 11+, while the student count includes assumed students aged 6-10.

| evaluation | zones | MAE | RMSE | mean_prediction_error_pred_minus_obs | status |
| --- | --- | --- | --- | --- | --- |
| Sample zone totals | 1081 | 14.4589 | 20.3315 | 0.4547 | Reserved-test zone agreement |
| Expansion-weighted zone totals | 1081 | 279.6017 | 396.1838 | 10.7359 | Reserved-test zone agreement |

| evaluation | observed_mean | predicted_mean | MAE | RMSE | mean_prediction_error |
| --- | --- | --- | --- | --- | --- |
| Unweighted reserved-test households | 5.6443 | 5.6618 | 2.4102 | 3.3683 | 0.0176 |
| Expansion-weighted reserved-test households; coefficients still unweighted OLS | 5.643 | 5.6644 | 2.4081 | 3.3665 | 0.0214 |

Traffic-zone sample and expanded totals use the same reserved-test records. Expansion factors are applied consistently to observed and predicted totals. The expanded sums cover the test subset and are not full-population zone totals. Coefficients are unweighted OLS. The cross-classification comparison uses the same eligible IDs and seeded split.

## Reproduction and files

Run `MLR_regression.ipynb` top to bottom from the project root with the requirements in requirements.txt. `final_outputs/MLR_regression/MLR_regression_results.xlsx` contains the full candidate list, coefficient and diagnostic tables, the vehicle-response table, working sample, exclusions, and both prediction sets. `selected_MLR_regression_model.json` records the equation, selection settings, source hash, and split hashes. Figures are saved in `final_outputs/MLR_regression/figures`.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90

Training ID SHA256: 33d1751c366913aa05976c98b1413a4ebc17b61e62cdba8c341555c2a2214c46

Test ID SHA256: 2f1bc1fc90f8e2a1a7c4c9f226d3e118ec37957be6cb0a30dfe42dace9b1e9de
