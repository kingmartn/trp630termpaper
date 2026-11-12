# Methods section

`methods.tex` is an insertable Methods section describing the implemented seed-42 analysis. It requires `amsmath` and `amssymb` in the paper preamble. Include it with `\input{paper/methods}` when compiling the paper from the repository root, or copy its contents into the paper.

`methods_preview.tex` is a standalone wrapper; compile it from this directory with `pdflatex methods_preview.tex`. The compiled preview is `methods_preview.pdf`.

The text was checked against the assignment transcription, both current notebooks, `split_policy.py`, `cross_classification.py`, and the generated workbooks. It describes 65,287 training and 27,978 test households, the four-variable starting regression, the 4,800-model search, cross-classification, and the actual error and weighting conventions. Estimated coefficients and predictive scores belong in Results and are available in `final_outputs`.

The draft does not claim cross-validation, a spatial holdout, population recalibration, or selection-adjusted inference. Earlier exploration of this dataset is disclosed. Source citations should be aligned with the paper's bibliography; no unverified references have been inserted. The survey definitions come from `inputs/dataguide2006_v1.pdf`.

The workflow review also corrected impossible cross-classification cells (blank rates and heatmap cells, excluded from sparse-cell counts) and added signed mean prediction error to the cross-classification household-group table. These corrections do not alter predictions for valid households.
