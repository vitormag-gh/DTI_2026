from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd()
STATS_DIR = PROJECT_ROOT / "Stats"

# ============================================================
# INPUT FILES
# ============================================================

RUN_MAIN = (
    STATS_DIR /
    "dnn_11_17_run_metrics_checkpoint.csv"
)

RUN_LAST2 = (
    STATS_DIR /
    "dnn_11_17_run_metrics_checkpoint_last2.csv"
)

FOLD_MAIN = (
    STATS_DIR /
    "dnn_11_17_fold_audit_checkpoint.csv"
)

FOLD_LAST2 = (
    STATS_DIR /
    "dnn_11_17_fold_audit_checkpoint_last2.csv"
)

# ============================================================
# OUTPUT FILES
# ============================================================

RUN_MERGED = (
    STATS_DIR /
    "dnn_11_17_run_metrics_checkpoint_MERGED.csv"
)

FOLD_MERGED = (
    STATS_DIR /
    "dnn_11_17_fold_audit_checkpoint_MERGED.csv"
)

# ============================================================
# LOAD
# ============================================================

for path in [RUN_MAIN, RUN_LAST2, FOLD_MAIN, FOLD_LAST2]:
    assert path.exists(), f"Missing file: {path}"

run_main = pd.read_csv(RUN_MAIN)
run_last2 = pd.read_csv(RUN_LAST2)

fold_main = pd.read_csv(FOLD_MAIN)
fold_last2 = pd.read_csv(FOLD_LAST2)

print("Run rows:")
print("  main :", len(run_main))
print("  last2:", len(run_last2))

print("Fold rows:")
print("  main :", len(fold_main))
print("  last2:", len(fold_last2))

# ============================================================
# MERGE
# ============================================================

run_merged = pd.concat(
    [run_main, run_last2],
    ignore_index=True,
)

fold_merged = pd.concat(
    [fold_main, fold_last2],
    ignore_index=True,
)

# ============================================================
# DUPLICATE CHECKS
# ============================================================

run_keys = [
    "FamilyKey",
    "ConfigurationID",
    "Run",
]

fold_keys = [
    "FamilyKey",
    "ConfigurationID",
    "Run",
    "OuterFold",
]

run_duplicates = run_merged.duplicated(
    subset=run_keys,
    keep=False,
)

fold_duplicates = fold_merged.duplicated(
    subset=fold_keys,
    keep=False,
)

assert not run_duplicates.any(), (
    "Duplicate run-level records found."
)

assert not fold_duplicates.any(), (
    "Duplicate fold-level records found."
)

# ============================================================
# FAMILY CHECK
# ============================================================

expected_families = {
    "enzyme",
    "gpcr",
    "ion_channel",
    "nuclear_receptor",
}

run_families = set(
    run_merged["FamilyKey"]
    .astype(str)
    .unique()
)

fold_families = set(
    fold_merged["FamilyKey"]
    .astype(str)
    .unique()
)

assert run_families == expected_families, (
    f"Unexpected run families: {run_families}"
)

assert fold_families == expected_families, (
    f"Unexpected fold families: {fold_families}"
)

# ============================================================
# STATUS CHECK
# ============================================================

assert (
    run_merged["Status"].astype(str) == "PASS"
).all()

assert (
    fold_merged["Status"].astype(str) == "PASS"
).all()

# ============================================================
# EXPECTED FINAL COUNTS
# ============================================================

EXPECTED_RUN_ROWS = 4 * 73 * 10       # 2,920
EXPECTED_FOLD_ROWS = 4 * 73 * 10 * 5  # 14,600

print()
print("Merged run rows :", len(run_merged))
print("Expected        :", EXPECTED_RUN_ROWS)

print("Merged fold rows:", len(fold_merged))
print("Expected        :", EXPECTED_FOLD_ROWS)

assert len(run_merged) == EXPECTED_RUN_ROWS, (
    f"Expected {EXPECTED_RUN_ROWS:,} run rows, "
    f"found {len(run_merged):,}."
)

assert len(fold_merged) == EXPECTED_FOLD_ROWS, (
    f"Expected {EXPECTED_FOLD_ROWS:,} fold rows, "
    f"found {len(fold_merged):,}."
)

# ============================================================
# PER-FAMILY COUNTS
# ============================================================

print("\nRun rows by family:")
print(
    run_merged
    .groupby("FamilyKey")
    .size()
)

print("\nFold rows by family:")
print(
    fold_merged
    .groupby("FamilyKey")
    .size()
)

for family in expected_families:

    n_runs = (
        run_merged["FamilyKey"]
        .astype(str)
        .eq(family)
        .sum()
    )

    n_folds = (
        fold_merged["FamilyKey"]
        .astype(str)
        .eq(family)
        .sum()
    )

    assert n_runs == 730, (
        f"{family}: expected 730 runs, "
        f"found {n_runs}."
    )

    assert n_folds == 3650, (
        f"{family}: expected 3,650 folds, "
        f"found {n_folds}."
    )

# ============================================================
# SAVE
# ============================================================

run_merged.to_csv(
    RUN_MERGED,
    index=False,
)

fold_merged.to_csv(
    FOLD_MERGED,
    index=False,
)

print("\n" + "=" * 100)
print("PASS - FOUR-FAMILY CHECKPOINT MERGE")
print("=" * 100)
print("Run metrics :", RUN_MERGED)
print("Fold audit  :", FOLD_MERGED)
print("Run rows    :", f"{len(run_merged):,}")
print("Fold rows   :", f"{len(fold_merged):,}")
print("=" * 100)