---
name: data-quality
description: Use when the user wants to validate data quality, define data contracts, catch schema drift, or document data quality rules before feature engineering or model training. Generates executable validation code and a rules document. Must be run from inside a project created by lugh:new-ds-project. Covers CRISP-DM Data Preparation phase.
argument-hint: <data-source>
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: Data Quality

Define data quality rules and generate executable validation for your dataset.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` not found, stop with: "Run /lugh:data-quality from the root of a lugh project."

Extract `<data-source>` from the argument. If none provided, ask the user. Derive a `SLUG` from the source (filename without extension, or table name).

Check if `docs/data-dictionary-SLUG.md` exists from a prior `data-profile` run — if so, read it to pre-populate column names and types for the conversation.

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Required columns**: Which columns must always be present and non-null? (critical fields — missing these should fail the pipeline)

2. **Value constraints**: Are there columns with restricted valid ranges or value sets?
   - Numeric ranges (e.g., `age` must be 0–120, `price` must be > 0)
   - Categorical sets (e.g., `status` must be in {active, inactive, churned})
   - Date ranges (e.g., `event_date` must not be in the future)

3. **Null rate thresholds**: For columns that are nullable — what is the maximum acceptable null percentage before the pipeline should warn or fail? (e.g., `phone_number` < 30% nulls is a warning; > 50% is a failure)

4. **Uniqueness constraints**: Which columns or column combinations must be unique? (e.g., `transaction_id` must be unique; `customer_id` + `date` combination must be unique)

5. **Cross-column constraints**: Are there relationships between columns that must hold? (e.g., `end_date >= start_date`, `discount_amount <= total_amount`, `quantity > 0 when order_status = 'shipped'`)

6. **Row count expectations**: What is the expected row count range for a valid batch? (e.g., between 10,000 and 2,000,000 rows — helps catch upstream truncations or duplicate loads)

7. **Validation library**: Which library fits your stack?
   - **Pandera** — Pythonic schema validation for DataFrames (recommended for scikit-learn projects)
   - **Great Expectations** — enterprise-grade with data docs and data stores
   - **Pydantic v2** — row-level validation (good for API inputs or document stores)
   - **Custom assertions** — simple Python assert statements (no extra dependency)

### Step 3 — Write data quality rules document

Create `docs/` if it doesn't exist.

Write `docs/data-quality-rules-SLUG.md`:

```markdown
# Data Quality Rules: SLUG

**Project:** NAME
**Source:** SOURCE_ARG
**Date:** YYYY-MM-DD
**Library:** [Q7]

---

## Required Fields (non-null)

| Column | Type | Failure Action |
|--------|------|----------------|
[one row per column from Q1]

---

## Value Constraints

| Column | Rule | Failure Action |
|--------|------|----------------|
[one row per constraint from Q2]

---

## Null Rate Thresholds

| Column | Warning Threshold | Failure Threshold |
|--------|------------------|-------------------|
[one row per column from Q3]

---

## Uniqueness Constraints

| Columns | Scope | Failure Action |
|---------|-------|----------------|
[one row per constraint from Q4]

---

## Cross-Column Constraints

| Rule | Expression | Failure Action |
|------|-----------|----------------|
[one row per constraint from Q5]

---

## Row Count Expectations

| Metric | Min | Max |
|--------|-----|-----|
| Row count | [Q6 min] | [Q6 max] |

---

## Rationale

[Brief explanation of why these rules matter for this dataset — drawn from the conversation]
```

### Step 4 — Write validation module

Create `src/PACKAGE/data/` if it doesn't exist.

Write `src/PACKAGE/data/validate.py` using the chosen library. Below are templates for each library choice — adapt column names and rules from the conversation.

**If Pandera:**
```python
"""Data validation schema for SLUG."""

import pandera as pa
from pandera import Column, DataFrameSchema, Check
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Define schema based on data quality rules
schema = DataFrameSchema(
    columns={
        # Required non-null columns
        # "column_name": Column(pa.String, nullable=False),
        # "amount": Column(pa.Float, checks=[Check.greater_than(0)], nullable=False),
        # "status": Column(pa.String, checks=[Check.isin(["active", "inactive"])]),
    },
    checks=[
        # Row count check
        # Check(lambda df: len(df) >= MIN_ROWS, error="Row count below minimum"),
        # Cross-column checks
        # Check(lambda df: (df["end_date"] >= df["start_date"]).all(), error="end_date must be >= start_date"),
    ],
    # Uniqueness
    # unique=["transaction_id"],
)


def validate(df: pd.DataFrame, source: str = "SLUG") -> pd.DataFrame:
    """Validate DataFrame against the SLUG schema.

    Args:
        df: Input DataFrame to validate.
        source: Source identifier for logging.

    Returns:
        Validated DataFrame (unchanged if valid).

    Raises:
        pandera.errors.SchemaError: If validation fails.
    """
    logger.info("Validating %s (%d rows, %d columns)", source, len(df), len(df.columns))
    validated = schema.validate(df, lazy=True)
    logger.info("Validation passed for %s", source)
    return validated


if __name__ == "__main__":
    import duckdb
    import sys

    source = "SOURCE_ARG"
    df = duckdb.connect().execute(f"SELECT * FROM read_auto('{source}')").df()
    try:
        validate(df, source)
        print(f"✔ Validation passed: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        print(f"✘ Validation failed:\n{e}", file=sys.stderr)
        sys.exit(1)
```

**If Great Expectations:** scaffold a `great_expectations/` directory with a basic expectation suite. Write `src/PACKAGE/data/validate.py` that loads and runs the suite.

**If custom assertions:** write a `validate.py` with explicit `assert` statements and a summary report.

Replace all column names, rules, and source references with actual values from the conversation.

### Step 5 — Write Hydra config for thresholds

Write `conf/validate.yaml`:

```yaml
# Data quality thresholds for SLUG
# Values here are version-controlled alongside code — change them deliberately.
source: SOURCE_ARG
null_rate_warning: 0.30   # warn if null rate exceeds this
null_rate_failure: 0.50   # fail if null rate exceeds this
min_rows: MIN_FROM_Q6
max_rows: MAX_FROM_Q6
```

### Step 6 — Add validate stage to dvc.yaml

Check if `dvc.yaml` exists. If it has a `prepare` stage, insert a `validate` stage after `prepare`:

```yaml
  validate:
    cmd: python src/PACKAGE/data/validate.py
    deps:
      - src/PACKAGE/data/validate.py
      - data/processed
    params:
      - validate
    outs: []
    metrics:
      - metrics/validation.json:
          cache: false
```

### Step 7 — Print summary

```
✔ Rules document:    docs/data-quality-rules-SLUG.md
✔ Validation module: src/PACKAGE/data/validate.py
✔ Hydra config:      conf/validate.yaml
✔ DVC stage added:   validate (runs after prepare)

Run validation:
  uv run python src/PACKAGE/data/validate.py

Or via DVC:
  dvc repro validate

Next step → /lugh:featurize
  Define and scaffold your feature engineering pipeline.
```
