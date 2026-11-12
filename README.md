# Household trip generation analysis

Run the analysis from this project folder with the `geo_env` Python environment:

```bash
source /home/mst_lab/geo_env/bin/activate
```

1. Run `Household_EDA_updated.ipynb` from top to bottom. It checks the source workbook, uses the saved household split, and writes 23 EDA tables to one Excel workbook and 16 EDA figures to `final_outputs/figures`. The tables include detailed quantiles, exact and grouped trip rates, zero-trip shares, joint trip frequencies, correlations, cross-classification cells, and pre-exclusion vehicle reviews. All modeling summaries use eligible training households; the vehicle reviews use training-assigned households before exclusions. The held-out records go to `intermediaries/EDA_heldout_test.xlsx`; they are not used for EDA summaries.
2. Run `trial mode.ipynb` from top to bottom. It searches linear-regression specifications using training households and evaluates the selected model on the reserved test households.
3. Run `python cross_classification.py`. It fits trip-rate cells on training households, then evaluates on the same test households and compares with the regression.

The common split and eligible training records are in `intermediaries/EDA_training.xlsx`. Keep that workbook: the EDA notebook reads its `Split` sheet on later runs. Intermediate records and final results are separate Excel workbooks; figures and short result summaries are in `final_outputs`.

| Analysis | Final workbook | Summary |
| --- | --- | --- |
| Training EDA | `final_outputs/Household_EDA_results.xlsx` | `final_outputs/EDA_results.md` |
| Regression trial | `final_outputs/trial_mode/trial_results.xlsx` | `final_outputs/trial_mode/trial_results.md` |
| Cross-classification | `final_outputs/cross_classification_results.xlsx` | `final_outputs/cross_classification_results.md` |

The supplied `inputs/households.xlsx` is never modified. The project assignment is `intermediaries/trial_mode/Dontoh Project.pdf`.
