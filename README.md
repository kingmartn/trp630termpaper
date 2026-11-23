# Household trip generation analysis

This project analyzes the household records in `inputs/households.xlsx` using exploratory analysis, multiple linear regression, and cross-classification.

## Setup

From the project directory, create a Python 3.13 environment and install the dependencies:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt jupyterlab
jupyter lab
```

If you use another notebook editor, install `requirements.txt` and select the `.venv` Python interpreter as the kernel. Run all commands from the project directory.

## Run the analysis

1. Run `Household_EDA.ipynb` from top to bottom. It reads the source workbook, creates the training and test split, and saves the EDA results and figures.
2. Run `MLR_regression.ipynb` from top to bottom using the same kernel. It fits the regression models and saves their results, figures, and selected model.
3. In a terminal with the environment active, run:

   ```bash
   python cross_classification.py
   ```

   This saves the cross-classification results and model comparison.

## Project files

| Path | Contents |
| --- | --- |
| `inputs/` | Source household workbook and 2006 TTS data guide. |
| `split_policy.py` | Shared, reproducible household split used by all three analyses. |
| `intermediaries/` | Training and test workbooks created by the EDA notebook. |
| `final_outputs/EDA/` | EDA workbook and figures, including PDF figures. |
| `final_outputs/MLR_regression/` | Regression workbook, figures, and selected model JSON. |
| `final_outputs/cross_classification/` | Cross-classification workbook and figures. |
| `final_outputs/model_comparison.xlsx` | Side-by-side model results. |
