# Training-only household EDA

The 2006 household source contains 93,307 records. Applying the common vehicle >=10 and unknown-dwelling exclusions leaves 65,287 training households and 27,978 held-out households. 42 records are excluded from both methods; reasons are in the intermediate workbook. The source workbook is unchanged.

All trip summaries, group rates, cross-classification cells, correlations, and zone support in [Household_EDA_results.xlsx](Household_EDA_results.xlsx) use training records only. Mean recorded trips are 5.642; 7,274 training households report zero trips. The test records are stored in `../../intermediaries/EDA_heldout_test.xlsx` and were not read for EDA. The split is regenerated with NumPy PCG64 seed 42 on sorted household IDs, assigning 30% to test before exclusions. The resulting assignment and training records are audited in `../../intermediaries/EDA_training.xlsx`.

The workbook includes exact and grouped rates, detailed quantiles, zero-trip shares, joint trip frequencies, regional cells, and Pearson correlations. Thirteen detailed figures are available in `figures/`, with descriptive filenames indicating their purpose. The two vehicle review figures use training-assigned households before exclusions; all other figures use eligible training households. Display caps affect charts and grouped views only.

The proposed cross-classification uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+, with sparse cells flagged below 30 training records. The cross-classification model specifies its fallback rates from training data before evaluating the test set. `expf` is retained for expanded totals, while household-level unweighted results remain explicit.

The [2006 data guide](../../inputs/dataguide2006_v1.pdf) lists household vehicle count as 0-99 without identifying 99 as an unknown code for that field; dwelling 9 is Unknown, and trips cover members aged 11+. Across the full source, the value 99 appears in these checked household count fields: nvehicle (1). The common 10+ vehicle rule excludes any record with 99 vehicles. Regression and cross-classification use the same held-out household IDs.

## Derived quantities

| Quantity | Value | Unit | Reference / denominator | Sample | Source / formula |
| --- | ---: | --- | --- | --- | --- |
| Cell CV min | 0.4747014 | ratio | cell mean trips | training | SizeDriverCells: sample SD / mean |
| Cell CV max | 1.219056 | ratio | cell mean trips | training | SizeDriverCells: sample SD / mean |
| Licence increment 0 to 2; persons 2 | 2.718964 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 0 to 2; persons 3 | 2.446098 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 0 to 2; persons 4 | 3.265029 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 0 to 2; persons 5+ | 2.755778 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 2 to 3+; persons 3 | 0.8715304 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 2 to 3+; persons 4 | 1.664933 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Licence increment 2 to 3+; persons 5+ | 2.648621 | trips | lower licence group | training | SizeDriverCells: higher minus lower group mean |
| Training zones | 1158 | zones | eligible training | training | ZoneSupport: row count |
| Training households per zone: median | 52 | households | zone | training | ZoneSupport.households |
| Training households per zone: min | 1 | households | zone | training | ZoneSupport.households |
| Training households per zone: max | 329 | households | zone | training | ZoneSupport.households |
| Training household mean trips: weighted minus unweighted | -0.003851192 | trips | unweighted statistic | training | Weighting: weighted minus unweighted; shares multiplied by 100 |
| Training zero-trip share: weighted minus unweighted | -0.06524596 | percentage points | unweighted statistic | training | Weighting: weighted minus unweighted; shares multiplied by 100 |
| Vehicle tail 5-9 | 264 | households | eligible training | training | Count nvehicle within inclusive bounds |
| Vehicle tail 8-9 | 8 | households | eligible training | training | Count nvehicle within inclusive bounds |

Source workbook SHA256: 7bced1105d00a6b468289110a4a4d1684591e9bb74c878a927e3bec979efea90
