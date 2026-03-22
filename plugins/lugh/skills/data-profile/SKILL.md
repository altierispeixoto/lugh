---
name: data-profile
description: Use when the user wants to understand a dataset before modeling. Generates a Marimo EDA notebook and a data dictionary from any data source (CSV, Parquet, DuckDB, or SQL database). Must be run from inside a project created by lugh:new-ds-project. Covers the Data Understanding phase of the ML lifecycle.
argument-hint: <source>
allowed-tools: [Bash, Write]
---

# Lugh: Data Profile

Generate an EDA notebook and data dictionary for any data source.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` not found, stop with: "Run /lugh:data-profile from the root of a lugh project."

Extract `<source>` from the argument. Supported formats:
- CSV: `data/raw/customers.csv`
- Parquet: `data/raw/features.parquet`
- DuckDB table: `data/raw/store.duckdb::orders`
- SQL (via DuckDB connector): `postgresql://user:pass@host/db::SELECT * FROM orders LIMIT 10000`

Derive a `SLUG` from the source (filename without extension, or table name).

### Step 2 — Introspect the data source via DuckDB

Run a Python one-liner via Bash to get schema and summary stats:

```bash
uv run python -c "
import duckdb, json, sys

source = 'SOURCE_ARG'

# Parse source type
if '::' in source:
    path, table_or_query = source.split('::', 1)
    if source.startswith(('postgresql://', 'mysql://', 'duckdb://')):
        con = duckdb.connect()
        con.execute(f\"INSTALL postgres; LOAD postgres;\")
        query = f'SELECT * FROM postgres_scan(\"{path}\", \\'public\\', \\'{table_or_query}\\') LIMIT 10000'
    else:
        con = duckdb.connect(path)
        query = f'SELECT * FROM {table_or_query}'
else:
    con = duckdb.connect()
    query = f\"SELECT * FROM read_auto('{source}')\"

rel = con.sql(query)
schema = con.sql(f'DESCRIBE ({query})').fetchall()
summary = con.sql(f'SUMMARIZE ({query})').fetchall()
schema_cols = [r[0] for r in con.sql(f'DESCRIBE ({query})').description]
summary_cols = [r[0] for r in con.sql(f'SUMMARIZE ({query})').description]
print(json.dumps({'schema': [dict(zip(schema_cols, r)) for r in schema], 'summary': [dict(zip(summary_cols, r)) for r in summary]}))
" 2>&1
```

Capture the JSON output as `SCHEMA_JSON`. If it fails, print the error and ask the user to check the source path/connection.

### Step 3 — Write Marimo EDA notebook

Write `notebooks/eda-SLUG.py` as a Marimo notebook. The notebook must:

- Import `duckdb`, `marimo`, `pandas`, `matplotlib`, `seaborn` and `PACKAGE`
- Load data from the same source using DuckDB (replicate the query from Step 2)
- Include cells for: schema display, missing values table, univariate distributions (histograms for numerics, bar charts for categoricals), correlation heatmap for numeric columns, outlier detection (IQR method), top-N cardinality for categorical columns
- Use `mo.md()` for section headers

### Step 4 — Write data dictionary

Create `docs/` if it doesn't exist.

Write `docs/data-dictionary-SLUG.md` as a markdown table pre-populated from `SCHEMA_JSON`:

```markdown
# Data Dictionary: SLUG

**Source:** SOURCE_ARG
**Profiled:** YYYY-MM-DD
**Project:** NAME

| Column | Type | Nulls% | Description | Example Values | Notes |
|--------|------|--------|-------------|----------------|-------|
[one row per column from schema, nulls% from summary]
```

### Step 5 — Print summary

```
✔ EDA notebook:     notebooks/eda-SLUG.py
✔ Data dictionary:  docs/data-dictionary-SLUG.md

Run the notebook:
  uv run marimo edit notebooks/eda-SLUG.py

Next step → /lugh:experiment <experiment-name>
  Design and track your first modeling experiment.
```
