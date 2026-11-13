# Held-out model comparison

All models use the same 27,978 eligible test households. Household IDs are assigned with NumPy PCG64 seed 42, with 30% reserved for test before exclusions. The regenerated assignment matches the EDA split exactly. The regression specification was selected using training data; cross-classification category boundaries were specified before evaluation. The detailed calculations are in [model_comparison.xlsx](model_comparison.xlsx).

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Training mean | 3.4505 | 4.5932 | -0.0019 |
| Cross-classification | 2.5939 | 3.6390 | 0.0233 |
| Regression (size and drivers) | 2.6024 | 3.6475 | 0.0165 |
| Simple four-predictor regression | 2.4827 | 3.4611 | 0.0175 |
| Multiple linear regression | 2.4102 | 3.3683 | 0.0176 |

Cross-classification and the size-and-drivers regression use the same two household characteristics. Cross-classification groups the upper counts, while regression retains their exact values. Their test RMSE values are 3.6390 and 3.6475, respectively. The selected regression uses additional household characteristics; its RMSE is 3.3683. The comparison with cross-classification therefore reflects both model form and available information.

The table below compares household MAE within identical size and driver groups. The workbook also contains RMSE and signed mean error for every group and model.

| Group | Level | Households | Cross-classification MAE | Size-and-drivers regression MAE | Selected regression MAE |
| --- | --- | ---: | ---: | ---: | ---: |
| size_band | 1 | 5,763 | 1.348 | 1.353 | 1.310 |
| size_band | 2 | 8,490 | 2.195 | 2.215 | 2.147 |
| size_band | 3 | 5,308 | 2.722 | 2.717 | 2.495 |
| size_band | 4 | 5,278 | 3.448 | 3.442 | 3.126 |
| size_band | 5+ | 3,139 | 4.309 | 4.337 | 3.793 |
| driver_band | 0 | 2,699 | 1.441 | 1.478 | 1.238 |
| driver_band | 1 | 8,247 | 1.987 | 1.993 | 1.857 |
| driver_band | 2 | 12,521 | 2.870 | 2.872 | 2.687 |
| driver_band | 3+ | 4,511 | 3.626 | 3.642 | 3.355 |

## Derived quantities

| Quantity | Value | Unit | Reference / denominator | Sample | Source / formula |
| --- | ---: | --- | --- | --- | --- |
| Training mean: MAE reduction vs training-mean benchmark | 0 | percent | training-mean benchmark MAE | test | 100 * (benchmark - model) / benchmark |
| Training mean: RMSE reduction vs training-mean benchmark | 0 | percent | training-mean benchmark RMSE | test | 100 * (benchmark - model) / benchmark |
| Training mean: MAE as percent of test mean trips | 61.13234 | percent | test mean observed trips | test | 100 * MAE / mean(nhhldtrip) |
| Cross-classification: MAE reduction vs training-mean benchmark | 24.82427 | percent | training-mean benchmark MAE | test | 100 * (benchmark - model) / benchmark |
| Cross-classification: RMSE reduction vs training-mean benchmark | 20.77391 | percent | training-mean benchmark RMSE | test | 100 * (benchmark - model) / benchmark |
| Cross-classification: MAE as percent of test mean trips | 45.95668 | percent | test mean observed trips | test | 100 * MAE / mean(nhhldtrip) |
| Regression (size and drivers): MAE reduction vs training-mean benchmark | 24.57903 | percent | training-mean benchmark MAE | test | 100 * (benchmark - model) / benchmark |
| Regression (size and drivers): RMSE reduction vs training-mean benchmark | 20.58743 | percent | training-mean benchmark RMSE | test | 100 * (benchmark - model) / benchmark |
| Regression (size and drivers): MAE as percent of test mean trips | 46.10661 | percent | test mean observed trips | test | 100 * MAE / mean(nhhldtrip) |
| Simple four-predictor regression: MAE reduction vs training-mean benchmark | 28.0471 | percent | training-mean benchmark MAE | test | 100 * (benchmark - model) / benchmark |
| Simple four-predictor regression: RMSE reduction vs training-mean benchmark | 24.64569 | percent | training-mean benchmark RMSE | test | 100 * (benchmark - model) / benchmark |
| Simple four-predictor regression: MAE as percent of test mean trips | 43.98649 | percent | test mean observed trips | test | 100 * MAE / mean(nhhldtrip) |
| Multiple linear regression: MAE reduction vs training-mean benchmark | 30.14996 | percent | training-mean benchmark MAE | test | 100 * (benchmark - model) / benchmark |
| Multiple linear regression: RMSE reduction vs training-mean benchmark | 26.6677 | percent | training-mean benchmark RMSE | test | 100 * (benchmark - model) / benchmark |
| Multiple linear regression: MAE as percent of test mean trips | 42.70097 | percent | test mean observed trips | test | 100 * MAE / mean(nhhldtrip) |
| Selected regression: MAE change vs CC | -7.084315 | percent | cross-classification MAE | test | 100 * (selected - CC) / CC |
| CC minus two-variable regression: MAE | -0.008462077 | trips | two-variable regression | test | CC metric - two-variable metric |
| Max absolute weighted minus unweighted MAE | 0.002082244 | trips | unweighted metric | test | max across models of abs(weighted metric - metric) |
| Selected regression: RMSE change vs CC | -7.439199 | percent | cross-classification RMSE | test | 100 * (selected - CC) / CC |
| CC minus two-variable regression: RMSE | -0.008565219 | trips | two-variable regression | test | CC metric - two-variable metric |
| Max absolute weighted minus unweighted RMSE | 0.001788691 | trips | unweighted metric | test | max across models of abs(weighted metric - metric) |
| RMSE arithmetic decomposition: two-variable minus simple | 0.1864019 | trips | two-variable minus selected for fraction | test | Differences between model RMSEs; descriptive arithmetic, not a causal attribution |
| RMSE arithmetic decomposition: simple minus selected | 0.09287415 | trips | two-variable minus selected for fraction | test | Differences between model RMSEs; descriptive arithmetic, not a causal attribution |
| RMSE arithmetic decomposition: two-variable minus selected | 0.2792761 | trips | two-variable minus selected for fraction | test | Differences between model RMSEs; descriptive arithmetic, not a causal attribution |
| RMSE arithmetic decomposition: first-step fraction | 0.6674468 | proportion | two-variable minus selected for fraction | test | Differences between model RMSEs; descriptive arithmetic, not a causal attribution |
| size_band 1: CC minus two-variable MAE | -0.005150345 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 1: selected minus CC MAE | -0.03802705 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 2: CC minus two-variable MAE | -0.02082299 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 2: selected minus CC MAE | -0.04718073 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 3: CC minus two-variable MAE | 0.005381899 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 3: selected minus CC MAE | -0.2267297 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 4: CC minus two-variable MAE | 0.00564325 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 4: selected minus CC MAE | -0.3216229 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 5+: CC minus two-variable MAE | -0.02823687 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| size_band 5+: selected minus CC MAE | -0.5162609 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 0: CC minus two-variable MAE | -0.03689088 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 0: selected minus CC MAE | -0.203542 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 1: CC minus two-variable MAE | -0.005555271 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 1: selected minus CC MAE | -0.1305277 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 2: CC minus two-variable MAE | -0.001250638 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 2: selected minus CC MAE | -0.1830881 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 3+: CC minus two-variable MAE | -0.01678341 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| driver_band 3+: selected minus CC MAE | -0.2711141 | trips | second named model | test | HouseholdGroups: first MAE minus second MAE |
| cross_class: group mean error min | -0.006353742 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| cross_class: group mean error max | 0.1015399 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| same_input_regression: group mean error min | -0.3230689 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| same_input_regression: group mean error max | 0.2278498 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| selected_regression: group mean error min | -0.1258817 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| selected_regression: group mean error max | 0.2015628 | trips | nine overlapping size/driver groups | test | HouseholdGroups mean errors: predicted minus observed |
| Zone count | 1081 | zones | test records | test | ZoneComparison / test expf |
| Zones with fewer than 5 test households | 177 | zones | test records | test | ZoneComparison / test expf |
| Mean expf | 19.36622 | expansion factor | test records | test | ZoneComparison / test expf |
| Mean observed sample zone total | 146.0823 | trips | test records | test | ZoneComparison / test expf |
| Test households per zone: median | 23 | households | zone | test | ZoneComparison.households |
| Test households per zone: min | 1 | households | zone | test | ZoneComparison.households |
| Test households per zone: max | 173 | households | zone | test | ZoneComparison.households |
| Cross-classification: zone MAE | 16.85504 | trips | zone | test | mean(abs(predicted - observed)) |
| Cross-classification: zone MAE as percent of mean observed total | 11.53804 | percent | mean observed sample zone total | test | 100 * zone MAE / mean observed zone total |
| Cross-classification: predicted total | 158566.2 | trips | test records | test | sum predicted sample zone totals |
| Cross-classification: observed total | 157915 | trips | test records | test | sum observed sample zone totals |
| Cross-classification: total overprediction | 0.412391 | percent | observed total | test | 100 * (predicted total - observed total) / observed total |
| Cross-classification: expanded-to-sample zone MAE ratio | 19.42861 | ratio | sample zone MAE | test | expanded zone MAE / sample zone MAE |
| Selected regression: zone MAE | 14.45885 | trips | zone | test | mean(abs(predicted - observed)) |
| Selected regression: zone MAE as percent of mean observed total | 9.897741 | percent | mean observed sample zone total | test | 100 * zone MAE / mean observed zone total |
| Selected regression: predicted total | 158406.5 | trips | test records | test | sum predicted sample zone totals |
| Selected regression: observed total | 157915 | trips | test records | test | sum observed sample zone totals |
| Selected regression: total overprediction | 0.3112504 | percent | observed total | test | 100 * (predicted total - observed total) / observed total |
| Selected regression: expanded-to-sample zone MAE ratio | 19.33775 | ratio | sample zone MAE | test | expanded zone MAE / sample zone MAE |
| Zones with smaller absolute regression error than CC | 59.38945 | percent | all test zones | test | 100 * mean(abs(regression error) < abs(CC error)); ties excluded from numerator |
| Zones with negative regression total | 0 | zones | all test zones | test | Count regression_sample < 0 |
| Size 5+ × drivers 3+: MAE minus primary boundaries | 0 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |
| Size 5+ × drivers 3+: RMSE minus primary boundaries | 0 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |
| Size 4+ × drivers 3+: MAE minus primary boundaries | 0.0149602 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |
| Size 4+ × drivers 3+: RMSE minus primary boundaries | 0.02361537 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |
| Size 5+ × drivers 4+: MAE minus primary boundaries | -0.0005614427 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |
| Size 5+ × drivers 4+: RMSE minus primary boundaries | -0.001684928 | trips | Size 5+ × drivers 3+ | test | alternative metric - primary metric |

Zone totals use the same test records and show sample and expansion-weighted results separately. See the [regression report](MLR_regression/MLR_regression_results.md) and [cross-classification report](cross_classification/cross_classification_results.md) for model-specific details. These are predictive results, not causal effects.
