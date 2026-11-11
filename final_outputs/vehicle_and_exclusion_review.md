# Vehicle values, missing data, and predictor checks

All 93,307 households remain in EDA. These checks do not fit a trip-outcome regression, delete rows, or impute measurements. The supplied [2006 TTS Version 1.0 Data Guide](../inputs/dataguide2006_v1.pdf) supersedes the earlier provisional missing-value interpretation of vehicle 99. The workbook and historical split artifacts remain unchanged.

## Dictionary correction and exclusions

Printed page 18 (PDF page 23) defines n_vehicle as a numeric 0-99 count. Printed page 51 (PDF page 56) lists 99 with numeric description 99 and one 2006 record, alongside values including 21, 23, and 36. Vehicle 99 is retained numerically. Its source row, hnum=422873 at Excel row 27629, is a high-count sensitivity/influence case, not a missing-data omission candidate. Publication in the guide documents source occurrence; it does not independently validate each respondent's reported count.

There are 0 missing vehicle measurements in this file. Dwelling code 9 is explicitly Unknown (printed p. 17 / PDF p. 22), affecting 9 households:

| source_excel_row | hnum | dwelltype | nperson | nvehicle | nlicence | nhhldtrip |
| --- | --- | --- | --- | --- | --- | --- |
| 13194 | 219233 | 9 | 1 | 0 | 0 | 0 |
| 22221 | 444203 | 9 | 5 | 1 | 2 | 12 |
| 28420 | 316142 | 9 | 1 | 0 | 0 | 0 |
| 32459 | 212025 | 9 | 1 | 0 | 0 | 0 |
| 40439 | 218906 | 9 | 2 | 1 | 2 | 4 |
| 43331 | 247658 | 9 | 1 | 0 | 0 | 0 |
| 52427 | 265046 | 9 | 2 | 1 | 2 | 11 |
| 60235 | 234107 | 9 | 2 | 3 | 2 | 7 |
| 66462 | 511057 | 9 | 2 | 1 | 1 | 6 |

Complete-case models using dwelling have 93,298 households. Without that requirement, all 93,307 remain available for the checked numeric predictors. There is no automatic vehicle-missingness reduction. Unknown advance-letter code 9 does not require deletion when that survey-process variable is excluded. Do not generalize the meaning of 9/99 across fields: licence, employment, and student counts have documented numeric ranges including 9.

## Recorded vehicle tail

There are 33 recorded vehicle counts of at least 10 (0.0354% of the supplied sample), ranging from 10 to 99. Their households contain 1-5 residents and 1-5 licensed drivers, with 0-23 trips. Dwelling counts: House: 27, Townhouse: 3, Apartment: 3.

Each record has an exact-size/licence/dwelling peer group restricted to fewer than 10 vehicles, with peer n ranging from 102 to 12,968. Trips for 25 of 33 records fall within the peers' descriptive 5th-95th percentile range. That range is not a confidence interval or statistical outlier test, and peers are truncated on vehicle values by design. Ordinary trips do not establish whether a high recorded vehicle count is accurate. Having more vehicles than residents/drivers is not logically impossible.

The guide's published extreme tail weakens the earlier suggestion that unusual counts alone indicate coding errors in this workbook. Keep the dictionary-consistent baseline. Examine influence, flexible vehicle forms, or explicitly labeled exclusion sensitivities; do not replace 99, 36, or 21 with guessed smaller values. The existing 10+ review threshold is not a verified boundary between valid and invalid observations.

## Leverage and VIF

The exact-vehicle design uses 93,298 complete cases and 17 parameters including its intercept. It includes numeric 99. 33 of the 33 high-vehicle households exceed the descriptive review line 3p/n. Maximum leverage is 0.18450, about 1012.5 times average leverage. There are 635 records above the review line overall. These are review markers, not deletion instructions.

| source_excel_row | hnum | nperson | nvehicle | nlicence | nhhldtrip | dwelling | leverage_over_average |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 27629 | 422873 | 2 | 99 | 2 | 13 | House | 1012.5467 |
| 47598 | 405266 | 4 | 36 | 4 | 4 | House | 120.9356 |
| 435 | 425500 | 2 | 23 | 2 | 3 | Townhouse | 51.4498 |
| 20874 | 383423 | 4 | 23 | 2 | 12 | House | 49.9072 |
| 62490 | 279731 | 4 | 23 | 2 | 8 | House | 48.8257 |

The maximum column VIF is 3.159; the 10+ omission sensitivity gives 3.160. Low/moderate VIF cannot establish that individual extreme values are harmless. Leverage identifies unusual predictor combinations; influence on fitted coefficients also depends on residuals. Omitting 10+ values as a sensitivity reduces maximum leverage to 0.00458, but removes source-recorded values and changes the analytical population. No such exclusion has been adopted.

Matrix rank and VIF should accompany substantive variable selection after categorical encoding. Do not include workers together with both nempft and nemppt: workers is their exact sum. The guide confirms home workers are already included in full-/part-time counts (p. 18), so a separate home-work coefficient is a conditional association, not an extra group to add into total workers. Employment and student statuses may overlap, and ages 6-10 are assumed students (p. 2); trips cover ages 11+ (pp. 1, 51).

## Other tails and fair model comparison

There are 58 households with size at least 10 and 112 with at least 30 trips. The guide's household/person-trip tables document rare large values as numeric counts. Keep zero-trip households and do not delete high outcomes to improve fit. Verify data where possible and assess residual/influence diagnostics after fitting.

| scenario | households_available | households_not_available | actual_rows_removed_from_EDA | status |
| --- | --- | --- | --- | --- |
| Size and licensed drivers; no vehicles or dwelling required | 93307 | 0 | 0 | Illustrative model availability; no final exclusions |
| Known vehicles required, dwelling not required | 93307 | 0 | 0 | Illustrative model availability; no final exclusions |
| Known dwelling required, vehicles not required | 93298 | 9 | 0 | Illustrative model availability; no final exclusions |
| Known vehicles and dwelling required | 93298 | 9 | 0 | Illustrative model availability; no final exclusions |
| Known vehicles/dwelling; exclude vehicles >=10 (sensitivity only) | 93265 | 42 | 0 | Illustrative model availability; no final exclusions |
| Known vehicles/dwelling; exclude vehicles >=7 (exploratory sensitivity only) | 93231 | 76 | 0 | Illustrative model availability; no final exclusions |

Use the same agreed eligibility rule to compare regression and cross-classification. Size-by-licensed-driver classification does not itself require dwelling or vehicle data. Vehicle-based categories place recorded extremes in the top class; this limits numerical magnitude effects but does not validate the underlying measurement.

## Candidate-design sensitivities

| scenario | vehicle_form | n | unavailable_or_sensitivity_omitted_n | p_including_intercept | full_rank | max_column_VIF | standardized_condition_number | mean_leverage_p_over_n | max_leverage | max_leverage_over_average | n_above_3p_over_n | high_vehicle_n_in_design | high_vehicle_n_above_3p_over_n | high_vehicle_max_leverage_over_average |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Exact vehicles: all known values | exact | 93298 | 9 | 17 | True | 3.15931 | 3.98708 | 0.00018 | 0.1845 | 1012.54667 | 635 | 33 | 33 | 1012.54667 |
| Exact vehicles: omit >=10 sensitivity | exact | 93265 | 42 | 17 | True | 3.16032 | 4.05758 | 0.00018 | 0.00458 | 25.13558 | 688 | 0 | 0 |  |
| Exact vehicles: omit >=7 exploratory sensitivity | exact | 93231 | 76 | 17 | True | 3.15939 | 4.06113 | 0.00018 | 0.00459 | 25.15653 | 669 | 0 | 0 |  |
| Exact vehicles: omit >=5 exploratory sensitivity | exact | 92898 | 409 | 17 | True | 3.14747 | 4.05049 | 0.00018 | 0.00464 | 25.32946 | 600 | 0 | 0 |  |
| Log1p vehicles: same complete cases | log1p | 93298 | 9 | 17 | True | 3.15897 | 4.07607 | 0.00018 | 0.00456 | 25.03199 | 598 | 33 | 24 | 11.27959 |
| Grouped vehicles 0/1/2/3/4+: same complete cases | grouped | 93298 | 9 | 20 | True | 3.95525 | 5.47425 | 0.00021 | 0.00459 | 21.41683 | 2062 | 33 | 30 | 5.45929 |
| Vehicles omitted: same complete cases | omitted | 93298 | 9 | 16 | True | 3.15797 | 3.70369 | 0.00017 | 0.00445 | 25.9561 | 641 | 33 | 0 | 2.25245 |
| Vehicles omitted: all known dwellings | omitted | 93298 | 9 | 16 | True | 3.15797 | 3.70369 | 0.00017 | 0.00445 | 25.9561 | 641 | 33 | 0 | 2.25245 |

Log1p/grouped vehicles and omission of vehicles are diagnostic alternatives, not selected final models. Most scenarios use identical complete cases. With the corrected coding there are no missing vehicle values, so the two vehicle-omission availability scenarios have the same sample size. Categorical controls use k-1 indicators with an intercept. Indicator-column VIFs are not factor-level generalized VIFs.

Next, fitted models require residual-versus-fitted/predictor checks, nonlinear alternatives, heteroskedasticity and appropriate uncertainty, studentized residuals, Cook's distance/DFBETAs, coefficient stability, implausible predictions, and household/zone agreement. Full-data fitting yields in-sample fit/error measures. The guide describes census-based expansion zones and later-phase multi-unit sampling adjustments (pp. 2, 4); state weighting conventions explicitly and apply expansion consistently to observed and predicted totals.

## Reproducible supporting files

RV01-RV02 contain vehicle-band and dwelling profiles; RV03 lists all high-vehicle households and peers; RV04 is the provisional decision ledger; RV05 gives availability counts; RV06 lists other extreme counts; RV07-RV10 give design/VIF/leverage sensitivities. Figure_RV01 plots the vehicle tail, including 99 on logarithmic scatter axes. Section 20 and DI01-DI03 reconcile the coding with the supplied guide and compare published full-survey frequencies with this four-region extract.

## Subsequent explicit modeling decision

The user has requested exclusion of hnum=422873 (recorded nvehicle=99; House; Excel row 27629) from modeling. The current input is intermediaries/households_modeling.csv with 93,306 households; modeling_exclusions.csv records the reason. If known dwelling is required, 93,297 are available. The full-source EDA and prepared master above retain all 93,307 source households, and earlier diagnostic samples retain their stated definitions. Recompute model-selection diagnostics on the final agreed common modeling sample. Broader vehicle-tail exclusions and the feature-selection procedure remain undecided; no regression has been fitted.
