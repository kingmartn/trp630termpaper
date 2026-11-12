# Held-out model comparison

Both models and the training-mean benchmark use the same 27,978 eligible test households. Household IDs are assigned with NumPy PCG64 seed 42, with 30% reserved for test before exclusions. The regression specification was selected using training data; cross-classification category boundaries were specified before evaluation. The detailed calculations are in [model_comparison.xlsx](model_comparison.xlsx).

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Training mean | 3.4505 | 4.5932 | -0.0019 |
| Cross-classification | 2.5939 | 3.6390 | 0.0233 |
| Multiple linear regression | 2.4045 | 3.3631 | 0.0174 |

Zone totals use the same test records and show sample and expansion-weighted results separately. See the [regression report](MLR_regression/MLR_regression_results.md) and [cross-classification report](cross_classification/cross_classification_results.md) for model-specific details. These are predictive results, not causal effects.
