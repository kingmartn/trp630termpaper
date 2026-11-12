# Cross-classification: held-out evaluation

The primary model uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+. Each supported cell uses its unweighted training mean trip rate. Cells with fewer than 30 training households use the training mean for that size band; 0 held-out households used this fallback. The model and fallback rule were fixed before the held-out workbook was opened.

Household size represents the number of residents who may participate in daily activities; licensed-driver count represents the household's capacity for independent motorized travel. Crossing them allows driver availability to have different trip rates at different household sizes. The 5+ and 3+ top categories pool sparse tails, and the reported alternative boundaries test whether those choices matter. Children under 11 contribute to household size but their trips are not recorded; these rates describe associations, not causal effects. The [training cell-rate figure](figures/CC_02_training_cell_rates.png) shows each observed cell's rate and supporting household count. Structurally impossible cells are blank and do not receive fallback rates.

The common training set has 65,287 households and the reserved test set has 27,978. The split was regenerated from source household IDs with seed 42, reserving 30% before exclusions. The source and exclusion rules match the regression analysis. The [results workbook](cross_classification_results.xlsx) contains cell rates, support, boundary sensitivity, household and zone comparisons, and test predictions. The side-by-side [model comparison](../model_comparison.md) is in the root final-output folder.

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Cross-classification | 2.5939 | 3.6390 | 0.0233 |
| Multiple linear regression | 2.4045 | 3.3631 | 0.0174 |

Sample and expansion-weighted traffic-zone totals are evaluated on the same held-out households. `expf` is applied to observed and predicted trips alike. The boundary alternatives are reported as sensitivity checks; the test set was not used to select the primary boundaries. The weighted zone sums describe the evaluation records only; they are not full-population totals because no inverse test-selection adjustment is applied. These are predictive comparisons, not causal claims.
