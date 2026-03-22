---
name: featurize
description: Use when the user wants to design, document, or scaffold the feature engineering pipeline. Creates a feature catalog, generates the featurize.py DVC stage with feature definitions, and documents feature lineage. Must be run from inside a project created by lugh:new-ds-project. Covers the Feature Engineering phase of the ML lifecycle.
argument-hint: (optional: data source or model name)
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: Feature Engineering

Design the feature engineering pipeline and generate the featurize module.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` not found, stop with: "Run /lugh:featurize from the root of a lugh project."

Check for existing artifacts that inform the conversation:
- `docs/data-dictionary-*.md` — read column names and types if available
- `specs/` — read success metrics to understand target variable if available
- `params.yaml` — read current featurize section

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Modeling task**: What type of ML task is this?
   - Binary classification (predict yes/no)
   - Multiclass classification
   - Regression (predict a numeric value)
   - Time-series forecasting
   - Ranking / recommendation
   - Clustering / unsupervised

2. **Target variable**: What column is the prediction target? What does it represent? (Knowing this enables leakage detection in later questions.)

3. **Primary entity and grain**: What does one row represent? (e.g., one customer per month, one transaction, one product per store per day) — determines whether aggregation or window features are needed.

4. **Datetime columns**: Are there date/timestamp columns? If yes, which ones, and should they generate:
   - Cyclical features (day of week, month, hour)
   - Lag features (value at t-1, t-7, t-30)
   - Rolling aggregates (7-day mean, 30-day max)
   - Time since an event (days since last purchase)

5. **Categorical columns**: Which columns are categorical? For each, what encoding makes sense?
   - Low cardinality (< 10 values) → one-hot encoding
   - High cardinality (> 50 values) → target encoding, frequency encoding, or embedding
   - Ordinal categories with natural order → ordinal encoding
   - Free text → TF-IDF, count vectorizer, or sentence embeddings

6. **Numeric columns**: Any numeric columns needing transformation?
   - Skewed distributions → log or Box-Cox transform
   - Different scales → StandardScaler, MinMaxScaler, RobustScaler
   - Interaction terms or polynomial features needed?

7. **Leakage check**: Looking at the full column list and the target `[Q2]` — are there any columns that could be derived from the target, come from after the prediction time, or that would not be available at inference time? List them to exclude.

8. **Serving availability**: Will this model be used for:
   - Batch predictions only (all features can be computed at training time)
   - Online predictions (features must be available at request time, within latency budget)
   If online: which features require a feature store or pre-computation?

9. **Output format**: What format should the featurize stage output for the train stage?
   - Parquet files in `data/model_features/`
   - DuckDB table in `data/model_features/features.duckdb`
   - Numpy arrays (`.npy`) — for deep learning

### Step 3 — Write feature catalog

Create `docs/` if it doesn't exist.

Write `docs/feature-catalog.md`:

```markdown
# Feature Catalog: NAME

**Date:** YYYY-MM-DD
**Task:** [Q1]
**Target:** [Q2]
**Entity grain:** [Q3]

---

## Features

| Feature Name | Source Column(s) | Transformation | Type | Leakage Risk | Available at Serving | Notes |
|-------------|-----------------|----------------|------|-------------|---------------------|-------|
[one row per feature — derived from all conversation answers]

---

## Excluded Columns

| Column | Reason for Exclusion |
|--------|---------------------|
[columns from Q7 leakage check]

---

## Serving Notes

[Q8 — if online serving: which features need pre-computation or a feature store]

---

## Output Format

[Q9 — format and location of featurize stage output]
```

### Step 4 — Write featurize module

Write `src/PACKAGE/features/featurize.py`. Generate actual feature logic (not a stub) based on the conversation. Structure:

```python
"""Feature engineering pipeline for NAME.

Transforms processed data from data/processed/ into model-ready features
saved to data/model_features/.
"""

import logging
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from hydra import compose, initialize_config_dir
from omegaconf import DictConfig

logger = logging.getLogger(__name__)


def load_data(cfg: DictConfig) -> pd.DataFrame:
    """Load processed data."""
    # TODO: adapt path from cfg
    con = duckdb.connect()
    return con.execute("SELECT * FROM read_parquet('data/processed/**/*.parquet')").df()


def build_features(df: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    """Apply all feature transformations.

    Args:
        df: Processed input DataFrame.
        cfg: Hydra config with featurize parameters.

    Returns:
        Feature DataFrame ready for model training.
    """
    features = df.copy()

    # --- Datetime features ---
    # [generated from Q4 answers]

    # --- Encoding ---
    # [generated from Q5 answers]

    # --- Numeric transforms ---
    # [generated from Q6 answers]

    # --- Drop leakage columns ---
    # [generated from Q7 answers]
    leakage_cols = []  # populate from Q7
    features = features.drop(columns=[c for c in leakage_cols if c in features.columns])

    logger.info("Feature matrix: %d rows x %d columns", len(features), len(features.columns))
    return features


def save_features(features: pd.DataFrame, cfg: DictConfig) -> None:
    """Save feature matrix to output path."""
    out_path = Path("data/model_features")
    out_path.mkdir(parents=True, exist_ok=True)
    features.to_parquet(out_path / "features.parquet", index=False)
    logger.info("Saved features to %s", out_path / "features.parquet")


def run(cfg: DictConfig) -> None:
    df = load_data(cfg)
    features = build_features(df, cfg)
    save_features(features, cfg)


if __name__ == "__main__":
    with initialize_config_dir(config_dir=str(Path("conf").resolve())):
        cfg = compose(config_name="config")
    run(cfg)
```

Populate the `build_features` function with actual transformation code derived from the conversation answers. Do not leave stubs for features the user explicitly described.

### Step 5 — Update params.yaml

Read the current `params.yaml`. Replace the featurize section with real parameters reflecting the actual transformations chosen:

```yaml
featurize:
  # [parameters derived from the conversation — e.g.:]
  # target_encoding_cols: [col1, col2]
  # log_transform_cols: [amount, revenue]
  # lag_days: [7, 30]
  # rolling_windows: [7, 14, 30]
  # scaler: standard  # standard | minmax | robust | none
```

### Step 6 — Update dvc.yaml featurize stage

Update the featurize stage in `dvc.yaml` to reflect actual deps and params:

```yaml
  featurize:
    cmd: python src/PACKAGE/features/featurize.py
    deps:
      - src/PACKAGE/features/featurize.py
      - data/processed
    params:
      - featurize
    outs:
      - data/model_features
```

### Step 7 — Print summary

```
✔ Feature catalog:  docs/feature-catalog.md  (FEATURE_COUNT features defined)
✔ Featurize module: src/PACKAGE/features/featurize.py
✔ params.yaml updated (featurize section)
✔ dvc.yaml updated  (featurize stage)

Run the featurize stage:
  dvc repro featurize

Next step → /lugh:experiment <experiment-name>
  Design and track your first modeling experiment.
```
