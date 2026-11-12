# Transportation rationale for regression features

These are hypotheses for selecting candidate predictors. They support a defensible model specification but do not establish causal effects. The course report still needs academic or professional citations.

The simple starting model uses household persons, vehicles, full-time workers, and students. The wider search considers the effects below. The exact zone ID is used for clustered uncertainty and zone aggregation, while the four-region category derived from zone ranges is a candidate predictor. Household ID and survey administration fields are not predictors; `expf` is used for expanded totals, not as an explanatory variable.

| Effect | Source field or term | Transportation reason | Interpretation limit |
| --- | --- | --- | --- |
| size | nperson | More residents create more potential daily activities and trips. | Includes children below the survey trip-recording age of 11. |
| vehicles | nvehicle | Vehicle availability can ease access to dispersed destinations and increase trip-making options. | Vehicle ownership also reflects income and location; association is not an ownership effect. |
| drivers | nlicence | Licensed household members can independently make motorized trips. | Strongly correlated with adults, household size, and vehicles. |
| full_time | nempft | Full-time employment adds regular out-of-home activity opportunities. | The data do not identify which reported trips are work trips. |
| part_time | nemppt | Part-time work adds travel activity with potentially different schedules from full-time work. | Employment counts may correlate with household size and each other. |
| workers | nempft + nemppt | Total workers provides a simpler measure of employment-related activity. | Alternative to, never simultaneous with, separate full-time and part-time effects. |
| home_workers | nemphome | Working at home may replace commuting yet change nearby nonwork travel. | Already included among employed people; its coefficient is conditional, not total. |
| students | nstudent | School and education participation creates scheduled activity and household travel. | Students aged 6–10 are counted, while their trips are not recorded in the outcome. |
| dwelling | dwelltype | Housing form can proxy density, parking, and local access conditions. | Categorical proxy; not a measured land-use or causal effect. |
| weekday | tripday | Daily schedules and activity patterns can vary from Monday to Friday. | Survey weekday is categorical and is not a household attribute. |
| region | gta01hhld ranges | Broad location may proxy differences in land use, transit access, and travel opportunities. | Four coarse regions derived from zone ID; exact zone ID is not a predictor. |
| size_squared | (nperson - 3)^2 | Trip growth may taper as household size rises. | Curvature is exploratory and may be unstable in rare large households. |
| vehicles_squared | (nvehicle - 1)^2 | The marginal association of another vehicle may diminish. | Curvature is exploratory; high-vehicle records are excluded by the common rule. |
| size_by_drivers | (nperson - 3) × (nlicence - 2) | Driver availability may matter differently in small and large households. | Interaction requires both main effects and is not causal. |
| size_by_vehicles | (nperson - 3) × (nvehicle - 1) | The usefulness of vehicles may depend on how many residents share them. | Interaction requires both main effects and is not causal. |
