# TRP 630 Semester Course Project

## Household Trip Generation Analysis

**Instructor: Dr. Anthony Dontoh**

You will use the supplied household travel dataset to investigate how household characteristics relate to trip making. You will develop and compare two trip-generation models: multiple linear regression and cross-classification. You will communicate your findings through a written report and an in-class presentation.

The project is intended to demonstrate your understanding of the entire analytical process, including data preparation, model development, evaluation, and interpretation.

### Project objectives

By completing this project, you should be able to:

- Formulate clear transportation-planning questions.
- Examine and prepare household survey data for analysis.
- Explain and justify the variables and methods you select.
- Develop regression and cross-classification models.
- Evaluate model performance at household and traffic-zone levels.
- Interpret findings, acknowledge limitations, and explain their planning relevance.
- Present and defend your work in class.

### Dataset and scope

The supplied Excel workbook contains household characteristics, the number of trips reported for a survey weekday, a traffic-zone identifier, and a household expansion factor.

Your principal outcome variable is `nhhldtrip`, the number of household trips on the recorded survey day. Potential explanatory variables include household size, vehicle availability, licensed drivers, employment characteristics, student counts, dwelling type, and survey weekday.

Use the named data fields in columns B–P. Exclude the partially populated, unlabeled columns unless their purpose is clarified in class. Preserve the original dataset and conduct your analysis in a separate working copy.

The project focuses on household trip generation. The supplied data do not support separate analyses of trip purpose, travel mode, trip distance, or destination.

### Required work

1. **Define your research questions.**

   Develop two or three questions that can be answered using the dataset. Explain their transportation-planning relevance and state your expected relationships before estimating models.

2. **Review relevant literature.**

   Provide a focused review of household trip generation, multiple linear regression, and cross-classification. Use relevant academic or professional sources to support your approach and variable selection.

3. **Inspect and prepare the data.**

   Identify what each variable represents and distinguish counts, categories, identifiers, and survey-related fields. Check for duplicates, coded unknowns, unusual values, and inconsistencies. Document all exclusions, recoding, and other changes, including their effect on the analytical sample.

   Do not assume that every numerical value is suitable for analysis. Seek clarification on uncertain codes before treating them as valid measurements. Retain zero-trip households unless you justify a narrower study population.

4. **Conduct exploratory analysis.**

   Describe the distribution of household trips and the main household characteristics. Examine trip rates across relevant groups and relationships among potential explanatory variables. Use clearly labeled tables and figures, and explain how the findings inform your modeling choices.

5. **Develop a multiple linear regression model.**

   Begin with a simple specification and evaluate at least one justified alternative. Select a final model based on transportation reasoning, statistical evidence, and predictive performance.

   Present the model equation, variable definitions, coefficient estimates, uncertainty measures, sample size, and goodness-of-fit statistics. Discuss coefficient signs and magnitudes, correlated predictors, residual patterns, influential observations, and implausible predictions. Treat categorical variables appropriately.

6. **Develop a cross-classification model.**

   Select two household characteristics and justify the categories used. Calculate a trip rate for each household category and show the number of observations supporting each rate.

   Explain how you handle sparse or empty categories. Assess how an alternative set of category boundaries affects your results.

7. **Validate and compare both models.**

   Use a common, reproducible training/test split and the same eligible observations for both methods. Develop and refine the models using training data, then evaluate their performance on the reserved test data.

   Compare both models with a simple benchmark, such as the training-sample mean trip rate. Report household-level mean absolute error, root mean square error, and mean prediction error. Include observed-versus-predicted figures and examine performance for selected household groups.

   Compare results at the traffic-zone level by aggregating household predictions and observed trips over the same evaluation records. Clearly distinguish sample totals from expanded population estimates.

   Explain the role of the household expansion factor, `expf`, and state whether and how you use it. Apply consistent weighting conventions to observed and predicted values. Further guidance on expansion factors will be provided in class.

8. **Interpret your findings.**

   Explain which model performs better for your stated purpose and support your conclusion with evidence. Discuss practical usefulness, limitations, and additional data that could improve the analysis. Do not assume that one method must outperform the other.

### Written report

Organize your report using the following structure:

1. Executive summary.
2. Introduction: background, research questions, objectives, and scope.
3. Literature review.
4. Data description, preparation, and exploratory analysis.
5. Methodology: variable selection, model specifications, cross-classification design, and validation approach.
6. Results and discussion: estimates, diagnostics, model comparisons, and planning interpretation.
7. Conclusions, limitations, and recommendations.
8. References.
9. Appendices containing supporting calculations and supplementary results.

Aim for approximately 15–20 pages of main text, excluding references and appendices. Include only tables and figures that contribute to your argument. Explain results in your own words rather than reproducing unexplained software output.

### In-class presentation and questions

The in-class presentation will account for **50% of the project grade**. It is a central part of the assessment and will be used to judge your understanding of the work submitted.

Your presentation should explain:

- Your research questions and why they matter.
- The data you used and the main preparation decisions.
- Your choice of explanatory variables and expected relationships.
- How you developed each model.
- How you tested and compared the models.
- Your principal findings, limitations, and conclusions.

Be prepared to explain calculations, interpret coefficients and error measures, justify category boundaries, and discuss how different assumptions could affect your conclusions. You may be asked to explain a table, figure, equation, or decision from your report or analysis files.

Presentation assessment will emphasize **understanding, reasoning, and responses to questions**, alongside clarity and organization. Reading slides or displaying software output without explanation will not demonstrate sufficient understanding.

For group submissions, every member must present and answer questions. Each member is expected to understand the complete project, including work undertaken by other members. Individual presentation grades may differ according to demonstrated understanding and contribution.

Presentation duration, dates, and submission deadlines will be announced in class.

### Deliverables

Submit the following:

- A final written report.
- Presentation slides.
- Analysis files containing the calculations or code used to produce your results.
- A brief explanation of how to reproduce the analysis.
- A contribution statement for group submissions.

You may use Excel, R, Python, or another suitable analytical package. Regardless of the software used, your work must be traceable and you must be able to explain it.

Progress checkpoints will be announced during the semester so that you can receive feedback before the final submission.

### Assessment

| Component | Weight |
|---|---:|
| In-class presentation and responses to questions | 50% |
| Written report | 40% |
| Analysis files, documentation, and reproducibility | 10% |
| Total | **100%** |

The presentation component will assess demonstrated understanding, justification of analytical decisions, interpretation of findings, responses to questions, and clarity of communication.

The written report will assess the quality of the research questions, data preparation, model development, validation, interpretation, and supporting literature.

The analysis files will be assessed for correctness, organization, transparency, and reproducibility.

### Flexibility and boundaries

You may choose your explanatory variables, cross-classification categories, and justified model refinements. An optional extension may examine a count model, a household subgroup, weighting sensitivity, or another relevant question. Extensions must supplement the required two-model comparison.

Your conclusions must remain within what the data and methods support. Distinguish association from causation, acknowledge the historical context of the dataset, and avoid presenting hypothetical scenarios as validated forecasts.

All sources and assistance must be acknowledged in accordance with course and university requirements. You are responsible for the accuracy of everything submitted and for explaining your work during the presentation.
