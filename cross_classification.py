"""Train and evaluate household trip-rate cross-classification on the shared split.

Run from the project root with /home/mst_lab/geo_env/bin/python cross_classification.py.
The held-out workbook is opened only after all rate models have been fitted.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cycler import cycler
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
BLUE, GOLD, TEAL, CORAL, INK = "#2673B8", "#E9A23B", "#2E9B8A", "#D96B55", "#253746"
WARM_HEAT = LinearSegmentedColormap.from_list(
    "trip_warm", ["#FFF7E8", "#FBE0A3", "#F2B75F", "#D9843D", "#A95532"]
)
WARM_HEAT.set_bad("#F2EFE8")
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "#FFFCF7",
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.prop_cycle": cycler(color=[BLUE, GOLD, TEAL, CORAL, "#8A914B"]),
    "pdf.fonttype": 42,
})

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


# Recreate the seeded split and verify it against the EDA assignment.
source_ids = pd.read_excel(ROOT / "inputs" / "households.xlsx",
                           sheet_name="2006-hhld", usecols="B", engine="openpyxl")["hnum"]
split = assign_household_split(source_ids)
saved_split = pd.read_excel(TRAIN_BOOK, sheet_name="Split")
pd.testing.assert_frame_equal(split, saved_split[["hnum", "split"]], check_dtype=False)
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
fig, ax = plt.subplots(figsize=(8.5, 5.8))
image = ax.imshow(visible_rates, cmap=WARM_HEAT, aspect="auto")
ax.set(xticks=range(4), xticklabels=["0", "1", "2", "3+"],
       yticks=range(5), yticklabels=["1", "2", "3", "4", "5+"],
       xlabel="Licensed drivers", ylabel="Household persons",
       title="Training trip rates by household size and licensed drivers")
for row in range(5):
    for col in range(4):
        n = int(support.iat[row, col])
        label = f"{rates.iat[row, col]:.1f}\n(n={n:,})" if n else ""
        ax.text(col, row, label, ha="center", va="center", fontsize=9,
                color="white" if n and image.norm(rates.iat[row, col]) > .68 else INK)
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
test = test.merge(regression[["hnum", "predicted_trips",
                              "size_driver_regression_predicted",
                              "simple_regression_predicted"]], on="hnum",
                  validate="one_to_one", sort=False)
assert set(test["hnum"]).isdisjoint(set(split.loc[split["split"].eq("train"), "hnum"]))
actual = test["nhhldtrip"].to_numpy(float)
weights = test["expf"].to_numpy(float)
regression_pred = test["predicted_trips"].to_numpy(float)
same_input_pred = test["size_driver_regression_predicted"].to_numpy(float)
simple_pred = test["simple_regression_predicted"].to_numpy(float)
primary_pred, primary_lookup = predict(fitted[PRIMARY[0]], test)
baseline_pred = np.full(len(test), train_mean)

benchmark = pd.DataFrame([
    metrics("Training mean", actual, baseline_pred, weights),
    metrics("Cross-classification", actual, primary_pred, weights),
    metrics("Regression (size and drivers)", actual, same_input_pred, weights),
    metrics("Simple four-predictor regression", actual, simple_pred, weights),
    metrics("Multiple linear regression", actual, regression_pred, weights),
])
regression_benchmarks = pd.read_excel(REGRESSION_BOOK, sheet_name="MLR10_benchmarks")
for source_name, comparison_name in [
    ("Size and licensed drivers", "Regression (size and drivers)"),
    ("Simple four-predictor model", "Simple four-predictor regression"),
    ("Selected alternative model", "Multiple linear regression"),
]:
    recorded = regression_benchmarks.set_index("model").loc[source_name]
    calculated = benchmark.set_index("model").loc[comparison_name]
    assert np.isclose(recorded["test_rmse"], calculated["RMSE"])
    assert np.isclose(recorded["test_mae"], calculated["MAE"])
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
predictions["same_input_regression_predicted"] = same_input_pred
predictions["simple_regression_predicted"] = simple_pred
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
        display_level = f"{level}+" if ((field == "size_band" and level == 5)
                                         or (field == "driver_band" and level == 3)) else str(level)
        row = {"grouping": field, "level": display_level,
               "n": len(block), "observed_mean": y.mean()}
        for prefix, column in [("cross_class", "cross_class_predicted"),
                               ("same_input_regression", "same_input_regression_predicted"),
                               ("selected_regression", "regression_predicted")]:
            error = block[column].to_numpy(float) - y
            row[f"{prefix}_MAE"] = np.mean(np.abs(error))
            row[f"{prefix}_RMSE"] = np.sqrt(np.mean(error ** 2))
            row[f"{prefix}_mean_error"] = np.mean(error)
        group_rows.append(row)
group_performance = pd.DataFrame(group_rows)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].hexbin(primary_pred, actual, gridsize=45, mincnt=1, bins="log", cmap=WARM_HEAT)
axes[0].plot([0, 55], [0, 55], "--", color=BLUE)
axes[0].set(xlabel="Cross-classification predicted trips", ylabel="Observed trips",
            title="Held-out households")
axes[1].scatter(zone["actual_sample"], zone["cross_sample"], s=12, alpha=.4, color=BLUE)
limit = max(zone["actual_sample"].max(), zone["cross_sample"].max())
axes[1].plot([0, limit], [0, limit], "--", color=GOLD)
axes[1].set(xlabel="Observed sample trips", ylabel="Predicted sample trips",
            title="Held-out traffic-zone totals")
fig.tight_layout()
fig.savefig(FIGURES / "CC_01_heldout_agreement.png", dpi=220)
plt.close(fig)


derived_rows = []
def derive(quantity, value, unit, reference, sample, source):
    derived_rows.append(dict(quantity=quantity, value=value, unit=unit,
        reference_or_denominator=reference, sample=sample, source=source))
def derived_markdown(frame):
    lines = ['| Quantity | Value | Unit | Reference / denominator | Sample | Source / formula |',
             '| --- | ---: | --- | --- | --- | --- |']
    for r in frame.itertuples(index=False):
        value = f'{r.value:.7g}' if isinstance(r.value, (float, int, np.number)) else str(r.value)
        lines.append(f'| {r.quantity} | {value} | {r.unit} | {r.reference_or_denominator} | {r.sample} | {r.source} |')
    return '\n'.join(lines)

b = benchmark.set_index('model')
base=b.loc['Training mean']; cc=b.loc['Cross-classification']; selected=b.loc['Multiple linear regression']
two=b.loc['Regression (size and drivers)']; simple=b.loc['Simple four-predictor regression']
for model,row in b.iterrows():
    for metric in ['MAE','RMSE']:
        derive(f'{model}: {metric} reduction vs training-mean benchmark',100*(base[metric]-row[metric])/base[metric],
            'percent','training-mean benchmark '+metric,'test','100 * (benchmark - model) / benchmark')
    derive(f'{model}: MAE as percent of test mean trips',100*row.MAE/actual.mean(),'percent','test mean observed trips','test','100 * MAE / mean(nhhldtrip)')
for metric in ['MAE','RMSE']:
    derive(f'Selected regression: {metric} change vs CC',100*(selected[metric]-cc[metric])/cc[metric],
        'percent','cross-classification '+metric,'test','100 * (selected - CC) / CC')
    derive(f'CC minus two-variable regression: {metric}',cc[metric]-two[metric],'trips','two-variable regression','test','CC metric - two-variable metric')
    derive(f'Max absolute weighted minus unweighted {metric}',np.abs(b['weighted_'+metric]-b[metric]).max(),
        'trips','unweighted metric','test','max across models of abs(weighted metric - metric)')
num=two.RMSE-simple.RMSE; den=two.RMSE-selected.RMSE
for label,value,unit in [('two-variable minus simple',num,'trips'),('simple minus selected',simple.RMSE-selected.RMSE,'trips'),
                         ('two-variable minus selected',den,'trips'),('first-step fraction',num/den if den else np.nan,'proportion')]:
    derive('RMSE arithmetic decomposition: '+label,value,unit,'two-variable minus selected for fraction','test',
        'Differences between model RMSEs; descriptive arithmetic, not a causal attribution')
assert np.isclose(num+simple.RMSE-selected.RMSE,den)
group_performance['cc_minus_two_variable_MAE']=group_performance.cross_class_MAE-group_performance.same_input_regression_MAE
group_performance['selected_minus_cc_MAE']=group_performance.selected_regression_MAE-group_performance.cross_class_MAE
for r in group_performance.itertuples():
    for label,value in [('CC minus two-variable MAE',r.cc_minus_two_variable_MAE),('selected minus CC MAE',r.selected_minus_cc_MAE)]:
        derive(f'{r.grouping} {r.level}: {label}',value,'trips','second named model','test','HouseholdGroups: first MAE minus second MAE')
for model in ['cross_class','same_input_regression','selected_regression']:
    for stat in ['min','max']:
        derive(f'{model}: group mean error {stat}',getattr(group_performance[model+'_mean_error'],stat)(),
            'trips','nine overlapping size/driver groups','test','HouseholdGroups mean errors: predicted minus observed')
assert zone.households.sum()==len(actual)
assert np.isclose(zone.actual_sample.sum(),actual.sum())
for label,value,unit in [('Zone count',len(zone),'zones'),('Zones with fewer than 5 test households',int(zone.households.lt(5).sum()),'zones'),
                       ('Mean expf',weights.mean(),'expansion factor'),('Mean observed sample zone total',zone.actual_sample.mean(),'trips')]:
    derive(label,value,unit,'test records','test','ZoneComparison / test expf')
for stat in ['median','min','max']:
    derive('Test households per zone: '+stat,getattr(zone.households,stat)(),'households','zone','test','ZoneComparison.households')
for prefix,model in [('cross','Cross-classification'),('regression','Selected regression')]:
    error=zone[prefix+'_sample']-zone.actual_sample
    expanded_error=zone[prefix+'_expanded']-zone.actual_expanded
    for label,value,unit,ref,formula in [
        ('zone MAE',abs(error).mean(),'trips','zone','mean(abs(predicted - observed))'),
        ('zone MAE as percent of mean observed total',100*abs(error).mean()/zone.actual_sample.mean(),'percent','mean observed sample zone total','100 * zone MAE / mean observed zone total'),
        ('predicted total',zone[prefix+'_sample'].sum(),'trips','test records','sum predicted sample zone totals'),
        ('observed total',zone.actual_sample.sum(),'trips','test records','sum observed sample zone totals'),
        ('total overprediction',100*error.sum()/zone.actual_sample.sum(),'percent','observed total','100 * (predicted total - observed total) / observed total'),
        ('expanded-to-sample zone MAE ratio',abs(expanded_error).mean()/abs(error).mean(),'ratio','sample zone MAE','expanded zone MAE / sample zone MAE')]:
        derive(f'{model}: {label}',value,unit,ref,'test',formula)
    assert np.isclose(zone[prefix+'_sample'].sum(),(primary_pred if prefix=='cross' else regression_pred).sum())
better=(abs(zone.regression_sample-zone.actual_sample)<abs(zone.cross_sample-zone.actual_sample)).mean()
derive('Zones with smaller absolute regression error than CC',100*better,'percent','all test zones','test','100 * mean(abs(regression error) < abs(CC error)); ties excluded from numerator')
negative_zones=zone.loc[zone.regression_sample.lt(0)].copy()
derive('Zones with negative regression total',len(negative_zones),'zones','all test zones','test','Count regression_sample < 0')
for r in negative_zones.itertuples():
    derive(f'Negative regression zone {r.gta01hhld}: total',r.regression_sample,'trips','zone','test','ZoneComparison.regression_sample')
    derive(f'Negative regression zone {r.gta01hhld}: support',r.households,'households','zone','test','ZoneComparison.households')
primary_boundary=boundary_sensitivity.iloc[0]
for metric in ['MAE','RMSE']:
    boundary_sensitivity[metric+'_minus_primary']=boundary_sensitivity[metric]-primary_boundary[metric]
for r in boundary_sensitivity.itertuples():
    for metric in ['MAE','RMSE']:
        derive(f'{r.model}: {metric} minus primary boundaries',getattr(r,metric+'_minus_primary'),'trips',PRIMARY[0],'test','alternative metric - primary metric')
derived_comparison=pd.DataFrame(derived_rows)
print('Derived quantities');print(derived_comparison.to_string(index=False))

sheets = {
    "ModelComparison": benchmark,
    "Derived_Comparison": derived_comparison,
    "NegativeZones": negative_zones,
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
    "Derived_Comparison": derived_comparison,
    "NegativeZones": negative_zones,
    "HouseholdGroups": group_performance,
    "ZoneSummary": zone_summary,
    "ZoneComparison": zone,
})
cross = benchmark.set_index("model").loc["Cross-classification"]
same = benchmark.set_index("model").loc["Regression (size and drivers)"]
linear = benchmark.set_index("model").loc["Multiple linear regression"]
group_mae_table = "\n".join(
    f"| {row.grouping} | {row.level} | {row.n:,} | {row.cross_class_MAE:.3f} | "
    f"{row.same_input_regression_MAE:.3f} | {row.selected_regression_MAE:.3f} |"
    for row in group_performance.itertuples())
COMPARISON_REPORT.write_text(f"""# Held-out model comparison

All models use the same {len(test):,} eligible test households. Household IDs are assigned with NumPy PCG64 seed {SPLIT_SEED}, with {TEST_FRACTION:.0%} reserved for test before exclusions. The regenerated assignment matches the EDA split exactly. The regression specification was selected using training data; cross-classification category boundaries were specified before evaluation. The detailed calculations are in [model_comparison.xlsx](model_comparison.xlsx).

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
""" + "\n".join(
    f"| {row.model} | {row.MAE:.4f} | {row.RMSE:.4f} | {row.mean_error_pred_minus_obs:.4f} |"
    for row in benchmark.itertuples()) + f"""

Cross-classification and the size-and-drivers regression use the same two household characteristics. Cross-classification groups the upper counts, while regression retains their exact values. Their test RMSE values are {cross['RMSE']:.4f} and {same['RMSE']:.4f}, respectively. The selected regression uses additional household characteristics; its RMSE is {linear['RMSE']:.4f}. The comparison with cross-classification therefore reflects both model form and available information.

The table below compares household MAE within identical size and driver groups. The workbook also contains RMSE and signed mean error for every group and model.

| Group | Level | Households | Cross-classification MAE | Size-and-drivers regression MAE | Selected regression MAE |
| --- | --- | ---: | ---: | ---: | ---: |
{group_mae_table}

## Derived quantities

{derived_markdown(derived_comparison)}

Zone totals use the same test records and show sample and expansion-weighted results separately. See the [regression report](MLR_regression/MLR_regression_results.md) and [cross-classification report](cross_classification/cross_classification_results.md) for model-specific details. These are predictive results, not causal effects.
""", encoding="utf-8")

fallback_n = int(primary_lookup["rule"].eq("Size-band fallback").sum())
REPORT.write_text(f"""# Cross-classification: held-out evaluation

The primary model uses household size 1/2/3/4/5+ and licensed drivers 0/1/2/3+. Each supported cell uses its unweighted training mean trip rate. Cells with fewer than {MIN_CELL_N} training households use the training mean for that size band; {fallback_n:,} held-out households used this fallback. The model and fallback rule were fixed before the held-out workbook was opened.

Household size represents the number of residents who may participate in daily activities; licensed-driver count represents the household's capacity for independent motorized travel. Crossing them allows driver availability to have different trip rates at different household sizes. The 5+ and 3+ top categories pool sparse tails, and the reported alternative boundaries test whether those choices matter. Children under 11 contribute to household size but their trips are not recorded; these rates describe associations, not causal effects. The [training cell-rate figure](figures/CC_02_training_cell_rates.png) shows each observed cell's rate and supporting household count. Structurally impossible cells are blank and do not receive fallback rates.

The common training set has {train_n:,} households and the reserved test set has {len(test):,}. The split was regenerated from source household IDs with seed {SPLIT_SEED}, reserving {TEST_FRACTION:.0%} before exclusions. The source and exclusion rules match the regression analysis. The [results workbook](cross_classification_results.xlsx) contains cell rates, support, boundary sensitivity, household and zone comparisons, and test predictions. The side-by-side [model comparison](../model_comparison.md) is in the root final-output folder.

| Method | Test MAE | Test RMSE | Mean error (predicted − observed) |
| --- | ---: | ---: | ---: |
| Cross-classification | {cross['MAE']:.4f} | {cross['RMSE']:.4f} | {cross['mean_error_pred_minus_obs']:.4f} |
| Regression (size and drivers) | {same['MAE']:.4f} | {same['RMSE']:.4f} | {same['mean_error_pred_minus_obs']:.4f} |
| Multiple linear regression | {linear['MAE']:.4f} | {linear['RMSE']:.4f} | {linear['mean_error_pred_minus_obs']:.4f} |

The first two model rows use only household size and licensed-driver count; cross-classification pools their upper categories, while regression uses exact counts. The selected regression effects are {regression_benchmarks.set_index('model').loc['Selected alternative model', 'effects']}. The [common-group comparison](../model_comparison.md) reports household-size and driver-band errors for both methods. Sample and expansion-weighted traffic-zone totals are evaluated on the same held-out households. `expf` is applied to observed and predicted trips alike. The boundary alternatives are reported as sensitivity checks; the test set was not used to select the primary boundaries. The weighted zone sums describe the evaluation records only; they are not full-population totals because no inverse test-selection adjustment is applied. These are predictive comparisons, not causal claims.
""", encoding="utf-8")
print(benchmark.round(4).to_string(index=False))
print(f"Saved {OUTPUT_BOOK} and {REPORT}")




with REPORT.open("a", encoding="utf-8") as report_file:
    report_file.write("\n## Derived quantities\n\n" + derived_markdown(derived_comparison) + "\n")
