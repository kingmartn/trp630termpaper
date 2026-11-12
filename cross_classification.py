"""Train and evaluate household trip-rate cross-classification on the shared split.

Run from the project root with /home/mst_lab/geo_env/bin/python cross_classification.py.
The held-out workbook is opened only after all rate models have been fitted.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
TRAIN_BOOK = ROOT / "intermediaries" / "EDA_training.xlsx"
TEST_BOOK = ROOT / "intermediaries" / "EDA_heldout_test.xlsx"
REGRESSION_BOOK = ROOT / "final_outputs" / "trial_mode" / "trial_results.xlsx"
OUTPUT_BOOK = ROOT / "final_outputs" / "cross_classification_results.xlsx"
REPORT = ROOT / "final_outputs" / "cross_classification_results.md"
FIGURES = ROOT / "final_outputs" / "figures"
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
    assert cells["effective_rate"].notna().all()
    assert cells["cell_n"].sum() == len(train)
    return {"cells": cells, "size_rates": size_rates,
            "overall_rate": train["nhhldtrip"].mean(),
            "size_top": size_top, "driver_top": driver_top}


def predict(model, frame):
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


def main():
    split = pd.read_excel(TRAIN_BOOK, sheet_name="Split")
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
    del train

    test = pd.read_excel(TEST_BOOK, sheet_name="Test")
    regression = pd.read_excel(REGRESSION_BOOK, sheet_name="Test_predictions")
    assert test["hnum"].is_unique and regression["hnum"].is_unique
    assert set(test["hnum"]) <= set(split.loc[split["split"].eq("test"), "hnum"])
    assert set(test["hnum"]) == set(regression["hnum"])
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
            fitted[name]["cells"]["cell_n"].lt(MIN_CELL_N).sum())
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
                               "RMSE": np.sqrt(np.mean((p-y)**2))})
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

    cross = benchmark.set_index("model").loc["Cross-classification"]
    linear = benchmark.set_index("model").loc["Multiple linear regression"]
    fallback_n = int(primary_lookup["rule"].eq("Size-band fallback").sum())
    REPORT.write_text(f"""# Cross-classification: held-out evaluation

The primary model uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+. Each supported cell uses its unweighted training mean trip rate. Cells with fewer than {MIN_CELL_N} training households use the training mean for that size band; {fallback_n:,} held-out households used this fallback. The model and fallback rule were fixed before the held-out workbook was opened.

The common training set has {train_n:,} households and the reserved test set has {len(test):,}. The source and exclusion rules match the regression trial. The [results workbook](cross_classification_results.xlsx) contains cell rates, support, boundary sensitivity, household and zone comparisons, and test predictions.

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Cross-classification | {cross['MAE']:.4f} | {cross['RMSE']:.4f} | {cross['mean_error_pred_minus_obs']:.4f} |
| Multiple linear regression | {linear['MAE']:.4f} | {linear['RMSE']:.4f} | {linear['mean_error_pred_minus_obs']:.4f} |

Sample and expansion-weighted traffic-zone totals are evaluated on the same held-out households. `expf` is applied to observed and predicted trips alike. The boundary alternatives are reported as sensitivity checks; the test set was not used to select the primary boundaries. These are predictive comparisons, not causal claims.
""", encoding="utf-8")
    print(benchmark.round(4).to_string(index=False))
    print(f"Saved {OUTPUT_BOOK} and {REPORT}")


if __name__ == "__main__":
    main()
