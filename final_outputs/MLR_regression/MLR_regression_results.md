# Multiple linear regression: simple and alternative specifications

## Sample and split

This notebook regenerates the common split from sorted source household IDs with NumPy PCG64 seed 42 and 30% assigned to test before exclusions. EDA independently uses the same rule. It applies the previously chosen vehicle >=10 and unknown-dwelling exclusions to both partitions. The eligible sample is 93,265 households: 65,287 training and 27,978 reserved test. Zero-trip households are retained. The source workbook remains unchanged.

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

The declared effect space contains household size, vehicles, licensed drivers, separate or total employment counts, home workers, students, dwelling type, weekday, region, optional size and vehicle squares, and optional size-by-driver and size-by-vehicle interactions. Household size is required. Categorical levels move as whole factors, workers cannot accompany separate employment counts, and hierarchy is enforced. All 4,800 valid effect subsets were scored on training data by Gaussian OLS AIC and BIC. Squared terms and interactions are optional predictors in a model that remains linear in coefficients.

The primary choice is the lowest-BIC valid subset whose removable whole effects have zone-clustered p<0.01. It has BIC rank 1 among all scored models. 1 BIC-ranked model(s) required clustered screening. AIC/BIC are working unweighted Gaussian criteria. The 99% clustered intervals below are exploratory after selection, and none is claimed to have selection-adjusted coverage.

## Selected equation and performance

Retained effects: size, vehicles, drivers, full_time, part_time, home_workers, students, dwelling, weekday, region, size_squared, vehicles_squared, size_by_drivers, size_by_vehicles.

Predicted trips = 3.48625 +0.25510 * size_c +0.83947 * vehicles_c +0.48274 * drivers_c +0.97595 * full_time +1.13933 * part_time -0.17504 * home_workers +1.56276 * students -0.54525 * dwelling_Apartment -0.18491 * dwelling_Townhouse +0.11562 * weekday_Tuesday +0.13503 * weekday_Wednesday +0.17031 * weekday_Thursday +0.28278 * weekday_Friday +0.14866 * region_Durham -0.10686 * region_York -0.12074 * region_Peel -0.07529 * size_c_squared -0.18241 * vehicles_c_squared +0.05213 * size_x_drivers +0.11677 * size_x_vehicles

Here `size_c = size - 3`, `vehicles_c = vehicles - 1`, and `drivers_c = licensed drivers - 2`; squared and interaction columns use these centered values. The model has 21 coefficients including its intercept. Training R-squared is 0.4667. Training RMSE is 3.3218; reserved-test RMSE is 3.3631 and reserved-test MAE is 2.4045. These are household trip-count errors, not causal effects. The best additive linear model, which contains no squares or interactions, has reserved-test RMSE 3.3683.

| model | effects | parameters | train_rmse | train_mae | test_rmse | test_mae | test_mean_prediction_error | test_negative_predictions | n_train | n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept-only mean |  | 1 | 4.5489 | 3.43358 | 4.59316 | 3.45047 | -0.00189 | 0 | 65287 | 27978 |
| Simple four-predictor model | size + vehicles + full_time + students | 5 | 3.41932 | 2.45838 | 3.46114 | 2.48271 | 0.01753 | 0 | 65287 | 27978 |
| Size and licensed drivers | size + drivers | 3 | 3.60181 | 2.57804 | 3.64754 | 2.60237 | 0.01653 | 0 | 65287 | 27978 |
| Best additive linear model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday | 14 | 3.33298 | 2.39163 | 3.36827 | 2.41015 | 0.01757 | 0 | 65287 | 27978 |
| Selected alternative model | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 21 | 3.32184 | 2.38351 | 3.36305 | 2.40445 | 0.01741 | 3 | 65287 | 27978 |

## Candidate leaders and coefficient uncertainty

| bic_rank | aic_rank | effects | parameters | aic | bic | selected_alternative |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 21 | 342075.1 | 342265.9 | 1 |
| 2 | 5 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 18 | 342104.9 | 342268.5 | 0 |
| 3 | 2 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_vehicles | 20 | 342088.5 | 342270.2 | 0 |
| 4 | 7 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342116.6 | 342271 | 0 |
| 5 | 18 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 14 | 342144.6 | 342271.8 | 0 |
| 6 | 8 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_vehicles | 17 | 342117.6 | 342272.1 | 0 |
| 7 | 12 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + region + size_squared + vehicles_squared + size_by_vehicles | 16 | 342129.7 | 342275.1 | 0 |
| 8 | 24 | size + vehicles + drivers + full_time + part_time + home_workers + students + dwelling + size_squared + vehicles_squared + size_by_vehicles | 13 | 342157 | 342275.2 | 0 |
| 9 | 3 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 20 | 342094.9 | 342276.7 | 0 |
| 10 | 11 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342124.5 | 342279 | 0 |
| 11 | 14 | size + vehicles + drivers + full_time + part_time + students + dwelling + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 16 | 342136.7 | 342282.1 | 0 |
| 12 | 6 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_vehicles | 19 | 342109.5 | 342282.2 | 0 |
| 13 | 28 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 13 | 342164.5 | 342282.6 | 0 |
| 14 | 17 | size + vehicles + drivers + full_time + part_time + students + dwelling + weekday + size_squared + vehicles_squared + size_by_vehicles | 16 | 342138.4 | 342283.7 | 0 |
| 15 | 4 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 20 | 342103.3 | 342285 | 0 |
| 16 | 32 | size + vehicles + drivers + full_time + part_time + students + dwelling + size_squared + vehicles_squared + size_by_vehicles | 12 | 342178 | 342287.1 | 0 |
| 17 | 21 | size + vehicles + drivers + full_time + part_time + students + dwelling + region + size_squared + vehicles_squared + size_by_vehicles | 15 | 342151 | 342287.3 | 0 |
| 18 | 13 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 17 | 342135.1 | 342289.5 | 0 |
| 19 | 19 | size + vehicles + drivers + workers + home_workers + students + dwelling + region + size_squared + vehicles_squared + size_by_drivers + size_by_vehicles | 16 | 342144.7 | 342290 | 0 |
| 20 | 9 | size + vehicles + drivers + workers + home_workers + students + dwelling + weekday + region + size_squared + vehicles_squared + size_by_vehicles | 19 | 342119.4 | 342292 | 0 |

| effect | df_effect | clustered_F | p_clustered | p_classical | df_cluster_denominator | protected_or_hierarchy |
| --- | --- | --- | --- | --- | --- | --- |
| size | 1 | 147.6086 | 4.72e-32 | 5.33e-38 | 1157 | Prespecified substantive core |
| vehicles | 1 | 831.6999 | 2.99e-138 | 4.8e-191 | 1157 | Required by hierarchy: vehicles_squared, size_by_vehicles |
| drivers | 1 | 367.7616 | 2.16e-71 | 3.9e-91 | 1157 | Required by hierarchy: size_by_drivers |
| full_time | 1 | 2038.697 | 1.64e-257 | <1e-300 | 1157 | Eligible for removal |
| part_time | 1 | 1000.997 | 8.44e-159 | <1e-300 | 1157 | Eligible for removal |
| home_workers | 1 | 12.05452 | 0.00054 | 2.89e-06 | 1157 | Eligible for removal |
| students | 1 | 3420.336 | <1e-300 | <1e-300 | 1157 | Eligible for removal |
| dwelling | 2 | 143.0475 | 3.06e-56 | 2.67e-56 | 1157 | Eligible for removal |
| weekday | 4 | 12.56641 | 5.19e-10 | 4.57e-10 | 1157 | Eligible for removal |
| region | 3 | 6.685428 | 0.00018 | 8.1e-08 | 1157 | Eligible for removal |
| size_squared | 1 | 60.04891 | 2.02e-14 | 1.02e-33 | 1157 | Eligible for removal |
| vehicles_squared | 1 | 181.8394 | 1.34e-38 | 1.53e-68 | 1157 | Eligible for removal |
| size_by_drivers | 1 | 9.719783 | 0.00187 | 8.7e-05 | 1157 | Eligible for removal |
| size_by_vehicles | 1 | 36.97118 | 1.63e-09 | 1.1e-15 | 1157 | Eligible for removal |

| column | effect | estimate | SE_zone_clustered | t_zone_clustered | p_zone_clustered | CI99_lower_zone_clustered | CI99_upper_zone_clustered | p_classical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intercept | Intercept | 3.486251 | 0.0589896 | 59.09941 | <1e-300 | 3.334053 | 3.638449 | <1e-300 |
| size_c | size | 0.2550988 | 0.02099678 | 12.14943 | 4.72e-32 | 0.2009254 | 0.3092723 | 5.33e-38 |
| vehicles_c | vehicles | 0.8394729 | 0.02910874 | 28.83921 | 2.99e-138 | 0.7643699 | 0.9145759 | 4.8e-191 |
| drivers_c | drivers | 0.4827431 | 0.02517288 | 19.17711 | 2.16e-71 | 0.4177949 | 0.5476912 | 3.9e-91 |
| full_time | full_time | 0.9759466 | 0.02161472 | 45.15194 | 1.64e-257 | 0.9201788 | 1.031714 | <1e-300 |
| part_time | part_time | 1.139327 | 0.03601072 | 31.63854 | 8.44e-159 | 1.046416 | 1.232237 | <1e-300 |
| home_workers | home_workers | -0.1750368 | 0.05041438 | -3.471962 | 0.00054 | -0.3051102 | -0.04496342 | 2.89e-06 |
| students | students | 1.562756 | 0.02672125 | 58.48364 | <1e-300 | 1.493813 | 1.631699 | <1e-300 |
| dwelling_Apartment | dwelling | -0.5452467 | 0.03252404 | -16.76442 | 1.23e-56 | -0.6291615 | -0.4613319 | 1.49e-57 |
| dwelling_Townhouse | dwelling | -0.1849086 | 0.0549565 | -3.364636 | 0.00079 | -0.3267011 | -0.04311617 | 0.00027 |
| weekday_Tuesday | weekday | 0.115616 | 0.04090418 | 2.826508 | 0.00479 | 0.01007971 | 0.2211523 | 0.00660 |
| weekday_Wednesday | weekday | 0.1350292 | 0.04106803 | 3.287939 | 0.00104 | 0.02907015 | 0.2409882 | 0.00169 |
| weekday_Thursday | weekday | 0.1703092 | 0.04119788 | 4.13393 | 3.82e-05 | 0.06401511 | 0.2766032 | 5.24e-05 |
| weekday_Friday | weekday | 0.2827831 | 0.04040298 | 6.999064 | 4.36e-12 | 0.1785399 | 0.3870262 | 6.41e-12 |
| region_Durham | region | 0.1486629 | 0.05966814 | 2.491495 | 0.01286 | -0.005285991 | 0.3026118 | 0.00120 |
| region_York | region | -0.1068555 | 0.05844652 | -1.82826 | 0.06777 | -0.2576525 | 0.04394155 | 0.00733 |
| region_Peel | region | -0.120737 | 0.05016805 | -2.406652 | 0.01626 | -0.2501749 | 0.008700806 | 0.00082 |
| size_c_squared | size_squared | -0.07528981 | 0.009715913 | -7.749123 | 2.02e-14 | -0.1003577 | -0.05022192 | 1.02e-33 |
| vehicles_c_squared | vehicles_squared | -0.1824129 | 0.01352731 | -13.48478 | 1.34e-38 | -0.2173145 | -0.1475113 | 1.53e-68 |
| size_x_drivers | size_by_drivers | 0.05212784 | 0.0167202 | 3.117657 | 0.00187 | 0.0089883 | 0.09526738 | 8.7e-05 |
| size_x_vehicles | size_by_vehicles | 0.1167696 | 0.01920429 | 6.080393 | 1.63e-09 | 0.06722092 | 0.1663183 | 1.1e-15 |

## Diagnostics and zone evaluation

Training residual skewness is 1.456 and excess kurtosis is 5.849. 970 training records have absolute externally studentized residuals above 3; these are review markers and are retained. There are 3 negative reserved-test predictions. Count-outcome and survey-weight limitations remain relevant. The data guide records trips only for persons aged 11+, while the student count includes assumed students aged 6-10.

| evaluation | zones | MAE | RMSE | mean_prediction_error_pred_minus_obs | status |
| --- | --- | --- | --- | --- | --- |
| Sample zone totals | 1081 | 14.3863 | 20.2717 | 0.4506 | Reserved-test zone agreement |
| Expansion-weighted zone totals | 1081 | 278.3034 | 395.2696 | 11.0595 | Reserved-test zone agreement |

| evaluation | observed_mean | predicted_mean | MAE | RMSE | mean_prediction_error |
| --- | --- | --- | --- | --- | --- |
| Unweighted reserved-test households | 5.6443 | 5.6617 | 2.4045 | 3.3631 | 0.0174 |
| Expansion-weighted reserved-test households; coefficients still unweighted OLS | 5.643 | 5.6651 | 2.4028 | 3.3615 | 0.0221 |

Traffic-zone sample and expanded totals use the same reserved-test records. Expansion factors are applied consistently to observed and predicted totals. Coefficients are unweighted OLS. The cross-classification comparison uses the same eligible IDs and seeded split.

## Reproduction and files

Run `MLR_regression.ipynb` top to bottom from the project root with the requirements in requirements.txt. `final_outputs/MLR_regression/MLR_regression_results.xlsx` contains the full candidate list, coefficient and diagnostic tables, working sample, exclusions, and both prediction sets. `selected_MLR_regression_model.json` records the equation, selection settings, source hash, and split hashes. Figures are saved in `final_outputs/MLR_regression/figures`.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90

Training ID SHA256: 33d1751c366913aa05976c98b1413a4ebc17b61e62cdba8c341555c2a2214c46

Test ID SHA256: 2f1bc1fc90f8e2a1a7c4c9f226d3e118ec37957be6cb0a30dfe42dace9b1e9de
