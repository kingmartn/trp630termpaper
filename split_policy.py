"""Reproducible household train/test assignment shared by all analyses."""

import numpy as np
import pandas as pd


SPLIT_SEED = 42
TEST_FRACTION = 0.30


def assign_household_split(household_ids):
    ids = np.sort(np.asarray(household_ids, dtype=np.int64))
    if len(ids) != len(np.unique(ids)):
        raise ValueError("Household IDs must be unique")
    test_count = round(TEST_FRACTION * len(ids))
    shuffled = np.random.Generator(np.random.PCG64(SPLIT_SEED)).permutation(ids)
    test_ids = set(shuffled[:test_count])
    return pd.DataFrame({
        "hnum": ids,
        "split": np.where(np.isin(ids, list(test_ids)), "test", "train"),
    })
