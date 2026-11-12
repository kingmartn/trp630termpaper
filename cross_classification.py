"""Train and evaluate household trip-rate cross-classification on the shared split.

Run from the project root with /home/mst_lab/geo_env/bin/python cross_classification.py.
The held-out workbook is opened only after all rate models have been fitted.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from split_policy import assign_household_split, SPLIT_SEED, TEST_FRACTION


ROOT = Path(__file__).resolve().parent
TRAIN_BOOK = ROOT / "intermediaries" / "EDA_training.xlsx"
TEST_BOOK = ROOT / "intermediaries" / "EDA_heldout_test.xlsx"
REGRESSION_BOOK = ROOT / "final_outputs" / "MLR_regression" / "MLR_regression_results.xlsx"
OUTPUT_DIR = ROOT / "final_outputs" / "cross_classification"
OUTPUT_BOOK = OUTPUT_DIR / "cross_classification_results.xlsx"
REPORT = OUTPUT_DIR / "cross_classification_results.md"
COMPARISON_BOOK = ROOT / "final_outputs" / "model_comparison.xlsx"
COMPARISON_REPORT = ROOT / "final_outputs" / "model_comparison.md"
FIGURES = OUTPUT_DIR / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

MIN_CELL_N = 30
PRIMARY = ("Size 5+ × drivers 3+", 5, 3)
ALTERNATIVES = [("Size 4+ × drivers 3+", 4, 3),
                ("Size 5+ × drivers 4+", 5, 4)]


def categories(frame, size_top, driver_top):
    return pd.DataFrame({
        "size_band": frame["nperson"].clip(upper=size_top).astype(int),
        "driver_band": frame["nlicence"].clip(upper=driver_top).astype(int),
    }, index=frame.index)


def fit_rates(train, size_top, driver_top):
    classified = categories(train, size_top, driver_top)
    data = pd.concat([classified, train[["nhhldtrip"]]], axis=1)
    observed = data.groupby(["size_band", "driver_band"], observed=True).agg(
        cell_n=("nhhldtrip", "size"), cell_rate=("nhhldtrip", "mean")
    ).reset_index()
    grid = pd.MultiIndex.from_product(
        [range(1, size_top + 1), range(driver_top + 1)],
        names=["size_band", "driver_band"]
    ).to_frame(index=False)
    cells = grid.merge(observed, on=["size_band", "driver_band"], how="left")
    cells["cell_n"] = cells["cell_n"].fillna(0).astype(int)
    size_rates = data.groupby("size_band", observed=True).agg(
        size_n=("nhhldtrip", "size"), size_rate=("nhhldtrip", "mean")
    ).reset_index()
    cells = cells.merge(size_rates, on="size_band", validate="many_to_one")
    cells["rule"] = np.where(cells["cell_n"].ge(MIN_CELL_N),
                             "Cell rate", "Size-band fallback")
    cells["effective_rate"] = np.where(
        cells["cell_n"].ge(MIN_CELL_N), cells["cell_rate"], cells["size_rate"])
    cells["structurally_possible"] = (
        cells["size_band"].eq(size_top)
        | cells["driver_band"].le(cells["size_band"])
    )
    impossible = ~cells["structurally_possible"]
    assert cells.loc[impossible, "cell_n"].eq(0).all()
    cells.loc[impossible, "effective_rate"] = np.nan
    cells.loc[impossible, "rule"] = "Structurally impossible"
    assert cells.loc[~impossible, "effective_rate"].notna().all()
    assert cells["cell_n"].sum() == len(train)
    return {"cells": cells, "size_rates": size_rates,
            "overall_rate": train["nhhldtrip"].mean(),
            "size_top": size_top, "driver_top": driver_top}


def predict(model, frame):
    assert frame["nlicence"].le(frame["nperson"]).all()
    classified = categories(frame, model["size_top"], model["driver_top"])
    lookup = classified.merge(
        model["cells"][["size_band", "driver_band", "cell_n", "effective_rate", "rule"]],
        on=["size_band", "driver_band"], how="left", validate="many_to_one", sort=False)
    assert len(lookup) == len(frame) and lookup["effective_rate"].notna().all()
    return lookup["effective_rate"].to_numpy(float), lookup


def metrics(label, actual, predicted, weights):
    error = predicted - actual
    return {"model": label, "n": len(actual),
            "MAE": np.mean(np.abs(error)),
            "RMSE": np.sqrt(np.mean(error ** 2)),
            "mean_error_pred_minus_obs": np.mean(error),
            "weighted_MAE": np.average(np.abs(error), weights=weights),
            "weighted_RMSE": np.sqrt(np.average(error ** 2, weights=weights)),
            "weighted_mean_error": np.average(error, weights=weights)}


def zone_metrics(label, actual, predicted):
    error = predicted - actual
    return {"model": label, "zones": len(actual),
            "MAE": np.mean(np.abs(error)),
            "RMSE": np.sqrt(np.mean(error ** 2)),
            "mean_error_pred_minus_obs": np.mean(error)}


def write_workbook(path, sheets):
    temporary = path.with_name(path.stem + "_building.xlsx")
    names = [name[:31] for name in sheets]
    assert len(names) == len(set(names))
    with pd.ExcelWriter(temporary, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name[:31], index=False)
            sheet = writer.sheets[name[:31]]
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
    temporary.replace(path)


# Recreate the seeded split; the saved Split sheet is only an audit output.
source_ids = pd.read_excel(ROOT / "inputs" / "households.xlsx",
                           sheet_name="2006-hhld", usecols="B", engine="openpyxl")["hnum"]
split = assign_household_split(source_ids)
del source_ids
train = pd.read_excel(TRAIN_BOOK, sheet_name="Train")
assert train["hnum"].is_unique
assert set(train["hnum"]) <= set(split.loc[split["split"].eq("train"), "hnum"])
assert train["nvehicle"].lt(10).all() and train["dwelltype"].ne(9).all()
train_n = len(train)

# All specifications and fallback rates are fixed before opening held-out records.
model_specs = [PRIMARY] + ALTERNATIVES
fitted = {name: fit_rates(train, size_top, driver_top)
          for name, size_top, driver_top in model_specs}
train_mean = train["nhhldtrip"].mean()

# Training cell rates and support for the primary classification.
cells = fitted[PRIMARY[0]]["cells"]
rates = cells.pivot(index="size_band", columns="driver_band", values="effective_rate")
support = cells.pivot(index="size_band", columns="driver_band", values="cell_n")
visible_rates = np.ma.masked_where(support.to_numpy() == 0, rates.to_numpy())
palette = plt.colormaps["Blues"].copy()
palette.set_bad("#eeeeee")
fig, ax = plt.subplots(figsize=(8.5, 5.8))
image = ax.imshow(visible_rates, cmap=palette, aspect="auto")
ax.set(xticks=range(4), xticklabels=["0", "1", "2", "3+"],
       yticks=range(5), yticklabels=["1", "2", "3", "4", "5+"],
       xlabel="Licensed drivers", ylabel="Household persons",
       title="Training trip rates by household size and licensed drivers")
for row in range(5):
    for col in range(4):
        n = int(support.iat[row, col])
        label = f"{rates.iat[row, col]:.1f}\n(n={n:,})" if n else ""
        ax.text(col, row, label, ha="center", va="center", fontsize=9,
                color="white" if n and rates.iat[row, col] > 7 else "#17212b")
fig.colorbar(image, ax=ax, label="Mean weekday trips per household", shrink=.85)
fig.tight_layout()
fig.savefig(FIGURES / "CC_02_training_cell_rates.png", dpi=220, facecolor="white")
plt.close(fig)
del train

test = pd.read_excel(TEST_BOOK, sheet_name="Test")
regression = pd.read_excel(REGRESSION_BOOK, sheet_name="Test_predictions")
assert test["hnum"].is_unique and regression["hnum"].is_unique
assert set(test["hnum"]) <= set(split.loc[split["split"].eq("test"), "hnum"])
assert set(test["hnum"]) == set(regression["hnum"])
for field in ["nhhldtrip", "gta01hhld", "expf"]:
    assert np.allclose(test.set_index("hnum")[field].sort_index(),
                       regression.set_index("hnum")[field].sort_index())
assert test["nvehicle"].lt(10).all() and test["dwelltype"].ne(9).all()
test = test.merge(regression[["hnum", "predicted_trips"]], on="hnum",
                  validate="one_to_one", sort=False)
assert set(test["hnum"]).isdisjoint(set(split.loc[split["split"].eq("train"), "hnum"]))
actual = test["nhhldtrip"].to_numpy(float)
weights = test["expf"].to_numpy(float)
regression_pred = test["predicted_trips"].to_numpy(float)
primary_pred, primary_lookup = predict(fitted[PRIMARY[0]], test)
baseline_pred = np.full(len(test), train_mean)

benchmark = pd.DataFrame([
    metrics("Training mean", actual, baseline_pred, weights),
    metrics("Cross-classification", actual, primary_pred, weights),
    metrics("Multiple linear regression", actual, regression_pred, weights),
])
boundary_rows = []
for name, _, _ in model_specs:
    alternative_pred, lookup = predict(fitted[name], test)
    row = metrics(name, actual, alternative_pred, weights)
    row["test_households_using_fallback"] = int(
        lookup["rule"].eq("Size-band fallback").sum())
    row["training_cells_below_30"] = int(
        (fitted[name]["cells"]["cell_n"].lt(MIN_CELL_N)
         & fitted[name]["cells"]["structurally_possible"]).sum())
    boundary_rows.append(row)
boundary_sensitivity = pd.DataFrame(boundary_rows)

predictions = test[["hnum", "gta01hhld", "nperson", "nlicence",
                    "nhhldtrip", "expf"]].copy()
predictions["size_band"] = primary_lookup["size_band"]
predictions["driver_band"] = primary_lookup["driver_band"]
predictions["training_cell_n"] = primary_lookup["cell_n"]
predictions["rate_rule"] = primary_lookup["rule"]
predictions["cross_class_predicted"] = primary_pred
predictions["regression_predicted"] = regression_pred
predictions["training_mean_predicted"] = baseline_pred
predictions["cross_class_error"] = primary_pred - actual

zone = predictions.assign(
    expanded_actual=predictions["nhhldtrip"] * predictions["expf"],
    expanded_cross=predictions["cross_class_predicted"] * predictions["expf"],
    expanded_regression=predictions["regression_predicted"] * predictions["expf"]
).groupby("gta01hhld").agg(
    households=("hnum", "size"), actual_sample=("nhhldtrip", "sum"),
    cross_sample=("cross_class_predicted", "sum"),
    regression_sample=("regression_predicted", "sum"),
    actual_expanded=("expanded_actual", "sum"),
    cross_expanded=("expanded_cross", "sum"),
    regression_expanded=("expanded_regression", "sum")
).reset_index()
zone_summary = pd.DataFrame([
    zone_metrics("Cross-classification sample zone totals",
            zone["actual_sample"].to_numpy(), zone["cross_sample"].to_numpy()),
    zone_metrics("Regression sample zone totals",
            zone["actual_sample"].to_numpy(), zone["regression_sample"].to_numpy()),
    zone_metrics("Cross-classification expanded zone totals",
            zone["actual_expanded"].to_numpy(), zone["cross_expanded"].to_numpy()),
    zone_metrics("Regression expanded zone totals",
            zone["actual_expanded"].to_numpy(), zone["regression_expanded"].to_numpy()),
])

group_rows = []
for field in ["size_band", "driver_band"]:
    for level, block in predictions.groupby(field):
        y = block["nhhldtrip"].to_numpy(float)
        p = block["cross_class_predicted"].to_numpy(float)
        group_rows.append({"grouping": field, "level": str(level),
                           "n": len(block), "observed_mean": y.mean(),
                           "predicted_mean": p.mean(),
                           "MAE": np.mean(np.abs(p-y)),
                               "RMSE": np.sqrt(np.mean((p-y)**2)),
                               "mean_error_pred_minus_obs": np.mean(p-y)})
group_performance = pd.DataFrame(group_rows)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].hexbin(primary_pred, actual, gridsize=45, mincnt=1, bins="log", cmap="Blues")
axes[0].plot([0, 55], [0, 55], "--", color="orange")
axes[0].set(xlabel="Cross-classification predicted trips", ylabel="Observed trips",
            title="Held-out households")
axes[1].scatter(zone["actual_sample"], zone["cross_sample"], s=12, alpha=.4)
limit = max(zone["actual_sample"].max(), zone["cross_sample"].max())
axes[1].plot([0, limit], [0, limit], "--", color="orange")
axes[1].set(xlabel="Observed sample trips", ylabel="Predicted sample trips",
            title="Held-out traffic-zone totals")
fig.tight_layout()
fig.savefig(FIGURES / "CC_01_heldout_agreement.png", dpi=220)
plt.close(fig)

sheets = {
    "ModelComparison": benchmark,
    "PrimaryCellRates": fitted[PRIMARY[0]]["cells"],
    "SizeFallbackRates": fitted[PRIMARY[0]]["size_rates"],
    "BoundarySensitivity": boundary_sensitivity,
    "HouseholdGroups": group_performance,
    "ZoneSummary": zone_summary,
    "ZoneComparison": zone,
    "TestPredictions": predictions,
}
contents = pd.DataFrame([{"sheet": name, "rows": len(frame),
                          "columns": len(frame.columns)}
                         for name, frame in sheets.items()])
write_workbook(OUTPUT_BOOK, {"Contents": contents, **sheets})

write_workbook(COMPARISON_BOOK, {
    "ModelComparison": benchmark,
    "HouseholdGroups": group_performance,
    "ZoneSummary": zone_summary,
    "ZoneComparison": zone,
})
COMPARISON_REPORT.write_text(f"""# Held-out model comparison

Both models and the training-mean benchmark use the same {len(test):,} eligible test households. Household IDs are assigned with NumPy PCG64 seed {SPLIT_SEED}, with {TEST_FRACTION:.0%} reserved for test before exclusions. The regression specification was selected using training data; cross-classification category boundaries were specified before evaluation. The detailed calculations are in [model_comparison.xlsx](model_comparison.xlsx).

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
""" + "\n".join(
    f"| {row.model} | {row.MAE:.4f} | {row.RMSE:.4f} | {row.mean_error_pred_minus_obs:.4f} |"
    for row in benchmark.itertuples()) + """

Zone totals use the same test records and show sample and expansion-weighted results separately. See the [regression report](MLR_regression/MLR_regression_results.md) and [cross-classification report](cross_classification/cross_classification_results.md) for model-specific details. These are predictive results, not causal effects.
""", encoding="utf-8")

cross = benchmark.set_index("model").loc["Cross-classification"]
linear = benchmark.set_index("model").loc["Multiple linear regression"]
fallback_n = int(primary_lookup["rule"].eq("Size-band fallback").sum())
REPORT.write_text(f"""# Cross-classification: held-out evaluation

The primary model uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+. Each supported cell uses its unweighted training mean trip rate. Cells with fewer than {MIN_CELL_N} training households use the training mean for that size band; {fallback_n:,} held-out households used this fallback. The model and fallback rule were fixed before the held-out workbook was opened.

Household size represents the number of residents who may participate in daily activities; licensed-driver count represents the household's capacity for independent motorized travel. Crossing them allows driver availability to have different trip rates at different household sizes. The 5+ and 3+ top categories pool sparse tails, and the reported alternative boundaries test whether those choices matter. Children under 11 contribute to household size but their trips are not recorded; these rates describe associations, not causal effects. The [training cell-rate figure](figures/CC_02_training_cell_rates.png) shows each observed cell's rate and supporting household count. Structurally impossible cells are blank and do not receive fallback rates.

The common training set has {train_n:,} households and the reserved test set has {len(test):,}. The split was regenerated from source household IDs with seed {SPLIT_SEED}, reserving {TEST_FRACTION:.0%} before exclusions. The source and exclusion rules match the regression analysis. The [results workbook](cross_classification_results.xlsx) contains cell rates, support, boundary sensitivity, household and zone comparisons, and test predictions. The side-by-side [model comparison](../model_comparison.md) is in the root final-output folder.

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Cross-classification | {cross['MAE']:.4f} | {cross['RMSE']:.4f} | {cross['mean_error_pred_minus_obs']:.4f} |
| Multiple linear regression | {linear['MAE']:.4f} | {linear['RMSE']:.4f} | {linear['mean_error_pred_minus_obs']:.4f} |

Sample and expansion-weighted traffic-zone totals are evaluated on the same held-out households. `expf` is applied to observed and predicted trips alike. The boundary alternatives are reported as sensitivity checks; the test set was not used to select the primary boundaries. The weighted zone sums describe the evaluation records only; they are not full-population totals because no inverse test-selection adjustment is applied. These are predictive comparisons, not causal claims.
""", encoding="utf-8")
print(benchmark.round(4).to_string(index=False))
print(f"Saved {OUTPUT_BOOK} and {REPORT}")



