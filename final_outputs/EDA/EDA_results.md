# Training-only household EDA

The 2006 household source contains 93,307 records. Applying the common vehicle >=10 and unknown-dwelling exclusions leaves 65,287 training households and 27,978 held-out households. 42 records are excluded from both methods; reasons are in the intermediate workbook. The source workbook is unchanged.

All trip summaries, group rates, cross-classification cells, correlations, and zone support in [Household_EDA_results.xlsx](Household_EDA_results.xlsx) use training records only. Mean recorded trips are 5.642; 7,274 training households report zero trips. The test records are stored in `../../intermediaries/EDA_heldout_test.xlsx` and were not read for EDA. The split is regenerated with NumPy PCG64 seed 42 on sorted household IDs, assigning 30% to test before exclusions. The resulting assignment and training records are audited in `../../intermediaries/EDA_training.xlsx`.

The workbook includes exact and grouped rates, detailed quantiles, zero-trip shares, joint trip frequencies, regional cells, and Pearson and Spearman correlations. Thirteen restored figures (`figures/Figure_ED01.png` through `figures/Figure_ED11.png`, `figures/S1_vehicle_frequencies.png`, and `figures/Figure_RV01_vehicle_household_review.png`) are available. The two vehicle review figures use training-assigned households before exclusions; all other figures use eligible training households. Display caps affect charts and grouped views only.

The proposed cross-classification uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+, with sparse cells flagged below 30 training records. The cross-classification model specifies its fallback rates from training data before evaluating the test set. `expf` is retained for expanded totals, while household-level unweighted results remain explicit.

The source [data guide](../../inputs/dataguide2006_v1.pdf) defines vehicle 99 as numeric, dwelling 9 as Unknown, and trips as recorded for household members aged 11+. Regression and cross-classification use the same held-out household IDs.

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90
