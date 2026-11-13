# Methods section

## Exploratory analysis subsection

`eda.tex` is a focused EDA subsection for the data/exploratory-analysis part of the paper. Include it with `\input{paper/eda}` from the repository root. It contains a compact descriptive table, four figures, and a short subsubsection on the modeling decisions supported by training EDA. `eda_preview.pdf` is the compiled preview; `eda_preview.tex` is its standalone wrapper. Add `\usepackage{graphicx}` to the paper preamble. The figure PDFs are in `paper/figures/`; when compiling outside the repository root, set `\newcommand{\EDAfigpath}{your/path/to/figures}` before including the subsection.

Run `Household_EDA_updated.ipynb` from the repository root to regenerate the training EDA workbook and these four paper figures. The figures show the trip distribution, the four starting regression predictor profiles, size–driver cell rates with sample support, and the full Pearson correlation heatmap. Compile the preview from `paper/` afterward.

All reported EDA statistics were checked against the current training-only `final_outputs/EDA/Household_EDA_results.xlsx`, specifically `NumericDetail`, `DisplayGroupRates`, `PairwiseCorrelations`, `SizeDriverCells`, and `Weighting`. The subsection does not use held-out model performance or claim that the initial four predictors were discovered through EDA.

## Methods section

`methods.tex` is an insertable Methods section describing the implemented seed-42 analysis. It requires `amsmath` and `amssymb` in the paper preamble. Include it with `\input{paper/methods}` when compiling the paper from the repository root, or copy its contents into the paper.

`methods_preview.tex` is a standalone wrapper. Compile either preview from `paper/` with `pdflatex <name>.tex`, `bibtex <name>`, then `pdflatex <name>.tex` twice more. The compiled previews are `methods_preview.pdf` and `eda_preview.pdf`. The verified references used in the two sections are in `references.bib`; merge these entries into the main paper's bibliography when inserting the sections.

The text was checked against the assignment transcription, both current notebooks, `split_policy.py`, `cross_classification.py`, and the generated workbooks. It describes 65,287 training and 27,978 test households, the four-variable starting regression, the 1,040-model search, cross-classification, and the actual error and weighting conventions. Estimated coefficients and predictive scores belong in Results and are available in `final_outputs`.

The draft describes the actual internal validation scope, including the shared-zone split and earlier exploration of this dataset. The survey definitions come from `inputs/dataguide2006_v1.pdf`.

The workflow review also corrected impossible cross-classification cells (blank rates and heatmap cells, excluded from sparse-cell counts) and added signed mean prediction error to the cross-classification household-group table. These corrections do not alter predictions for valid households.
