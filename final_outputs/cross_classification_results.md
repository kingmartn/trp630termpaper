# Cross-classification: held-out evaluation

The primary model uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+. Each supported cell uses its unweighted training mean trip rate. Cells with fewer than 30 training households use the training mean for that size band; 0 held-out households used this fallback. The model and fallback rule were fixed before the held-out workbook was opened.

The common training set has 65,283 households and the reserved test set has 27,982. The source and exclusion rules match the regression trial. The [results workbook](cross_classification_results.xlsx) contains cell rates, support, boundary sensitivity, household and zone comparisons, and test predictions.

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Cross-classification | 2.5546 | 3.5837 | 0.0139 |
| Multiple linear regression | 2.3749 | 3.3200 | 0.0181 |

Sample and expansion-weighted traffic-zone totals are evaluated on the same held-out households. `expf` is applied to observed and predicted trips alike. The boundary alternatives are reported as sensitivity checks; the test set was not used to select the primary boundaries. These are predictive comparisons, not causal claims.
