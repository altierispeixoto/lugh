---
name: monitor
description: Use when the user wants to set up drift detection, data quality monitoring, or performance monitoring for a deployed model. Scaffolds monitoring middleware for the FastAPI app, a Marimo monitoring dashboard, and a runbook for incident response. Must be run from inside a project created by lugh:new-ds-project. Covers production monitoring after ml-api deployment.
argument-hint: <model-name>
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: Model Monitoring

Set up drift detection and production monitoring for a deployed model.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` not found, stop with: "Run /lugh:monitor from the root of a lugh project."

Extract `<model-name>` from the argument. If none, ask the user.

Check for existing artifacts:
- `docs/mlops-architecture.md` — read Monitoring section if available to pre-fill Q1
- `docs/feature-catalog.md` — read feature names for Q3
- `src/${PACKAGE}/api/app.py` — confirm ml-api was run; warn if not found

If `src/${PACKAGE}/api/app.py` does not exist, warn: "No API found. Consider running /lugh:ml-api first to scaffold the serving endpoint."

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Monitoring tool**: Which monitoring approach fits your stack?
   - **Evidently** — open-source, generates HTML reports and JSON metrics; good for batch monitoring
   - **WhyLogs** — statistical summaries (profiles) per batch; integrates with MLflow
   - **Custom** — Prometheus metrics exposed via FastAPI `/metrics` endpoint + Grafana dashboards
   - **Managed** — Arize, Aporia, or Fiddler (SaaS; skip code scaffolding, output config guide only)
   - **Minimal** — log prediction inputs/outputs to a database table; inspect manually

2. **Reference dataset**: What is the reference distribution to compare against?
   - Training set (most common)
   - A specific held-out validation set
   - Last month's production data (sliding baseline)
   Path or DVC reference to the reference dataset.

3. **High-risk features**: Which input features are most likely to drift or most critical to monitor? (e.g., features derived from external data sources, user behavior signals, economic indicators)

4. **Monitoring cadence**: How often should monitoring run?
   - Real-time: check each prediction batch as it arrives
   - Hourly batch: aggregate predictions each hour
   - Daily batch: aggregate predictions each day
   - Weekly: scheduled report

5. **Alert thresholds**: What drift level should trigger an alert?
   - PSI (Population Stability Index): typically warn at 0.1, alert at 0.2
   - KS test p-value: alert if p < 0.05
   - JS divergence threshold
   - Or: "use Evidently/WhyLogs defaults"

6. **Ground truth availability**: Is ground truth (actual outcomes) available in production?
   - Yes, immediately (e.g., click/no-click, transaction approval)
   - Yes, with a delay (e.g., churn observed after 30 days)
   - No (enables drift monitoring only, not performance monitoring)
   If yes: which column in the prediction log stores ground truth, and when is it available?

7. **Prediction log storage**: Where should prediction inputs and outputs be logged?
   - SQLite file (simple; good for low-volume or development)
   - PostgreSQL table (production-grade)
   - Object storage (S3/GCS/Azure Blob) as Parquet files
   - MLflow (if using MLflow for experiment tracking)

8. **Alert channel**: How should monitoring alerts be delivered?
   - Slack webhook URL
   - Email (SMTP)
   - PagerDuty
   - GitHub Actions issue (opens an issue on threshold breach)
   - Log only (no external notifications)

### Step 3 — Write monitoring middleware

Write `src/PACKAGE/api/monitoring.py`:

```python
"""Prediction logging and monitoring middleware for MODEL_NAME."""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Prediction log location — configure via PREDICTION_LOG_PATH env var
LOG_PATH = Path("data/prediction_logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)


def log_prediction(
    request_id: str,
    features: dict[str, Any],
    prediction: Any,
    probability: float | None,
    latency_ms: float,
) -> None:
    """Log a prediction to the prediction store.

    Args:
        request_id: Unique identifier for this prediction request.
        features: Input feature dictionary.
        prediction: Model prediction output.
        probability: Confidence score if available.
        latency_ms: Inference latency in milliseconds.
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "features": features,
        "prediction": prediction,
        "probability": probability,
        "latency_ms": latency_ms,
        "ground_truth": None,  # filled in later when available
    }

    log_file = LOG_PATH / f"predictions-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(record) + "\n")


def load_prediction_log(date: str | None = None) -> list[dict]:
    """Load prediction log entries for a given date (defaults to today)."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_file = LOG_PATH / f"predictions-{date}.jsonl"
    if not log_file.exists():
        return []
    with open(log_file) as f:
        return [json.loads(line) for line in f if line.strip()]
```

Update `src/PACKAGE/api/app.py` to call `log_prediction` inside the `/predict` endpoint. Add the import and the call after a successful prediction:

```python
# In the predict endpoint, after computing prediction:
import uuid
from .monitoring import log_prediction
request_id = str(uuid.uuid4())
log_prediction(
    request_id=request_id,
    features=request.features,
    prediction=prediction,
    probability=probability,
    latency_ms=latency_ms,
)
```

### Step 4 — Write monitoring dashboard notebook

Write `notebooks/monitoring-dashboard.py` as a Marimo notebook that:

- Loads prediction logs from `data/prediction_logs/`
- Loads the reference dataset from Q2
- **Input drift section:**
  - For each high-risk feature from Q3: distribution comparison plot (reference vs. recent production)
  - PSI / KS statistic per feature with color-coded status (green/yellow/red vs. thresholds from Q5)
- **Prediction drift section:**
  - Distribution of model output scores/predictions over time
  - Rolling mean prediction vs. reference mean
- **Performance section** (if ground truth available per Q6):
  - Rolling metrics over time (daily precision, recall, or MAE)
  - Alert line at the minimum acceptable metric from specs success-metrics.md
- **Volume section:**
  - Daily prediction count, p99 latency trend
- **Alerts summary:** table of any threshold breaches with timestamps

Use `mo.md()` for section headers. Use `mo.ui.date_range()` for date filtering.

### Step 5 — Write monitoring runbook

Write `docs/monitoring-runbook.md`:

```markdown
# Monitoring Runbook: MODEL_NAME

**Project:** NAME
**Monitoring tool:** [Q1]
**Alert channel:** [Q8]

---

## Scheduled Monitoring

**Cadence:** [Q4]
**Command:**
```bash
uv run marimo run notebooks/monitoring-dashboard.py
```
or (for Evidently batch report):
```bash
uv run python src/PACKAGE/monitoring/report.py
```

---

## Alert Thresholds

| Signal | Warning | Alert | Action |
|--------|---------|-------|--------|
| PSI (input features) | 0.10 | 0.20 | Investigate upstream data changes |
| Prediction distribution shift | [Q5] | [Q5 × 2] | Check model and data jointly |
| [Performance metric] | [from spec] | [spec × 0.9] | Trigger retraining evaluation |
| Daily prediction volume | −30% | −50% | Check API health and upstream traffic |

---

## Incident Response Decision Tree

```
Alert fires
  ├── Is the API responding? → NO → Check deployment, restart container
  └── YES
      ├── Is prediction volume normal? → NO → Check upstream traffic / data pipeline
      └── YES
          ├── Is input data drifting? → YES → Identify drifted features
          │     ├── External data source changed? → Contact data team
          │     └── Seasonal / expected? → Update reference baseline, silence alert
          └── NO → Prediction distribution shifted without input drift
                → Model degradation likely → evaluate retrain
```

---

## Retraining Triggers

Initiate a retraining evaluation if any of the following occur:
- PSI > 0.20 for any high-risk feature for 3 consecutive days
- [Performance metric] drops below [threshold from spec] for 2 consecutive days
- Prediction distribution mean shifts by > [threshold] from reference

Retraining steps:
1. Collect new labeled data (minimum N examples per policy)
2. Run `/lugh:experiment retrain-YYYY-MM`
3. Run `/lugh:eval` on the candidate model
4. If evaluation passes go/no-go: promote and redeploy
5. Update reference baseline in `conf/monitor.yaml`

---

## Contacts

| Role | Name | Contact |
|------|------|---------|
| Model owner | [fill in] | |
| Data engineering | [fill in] | |
| On-call | [fill in] | |
```

### Step 6 — Write Hydra monitor config

Write `conf/monitor.yaml`:

```yaml
# Monitoring configuration for MODEL_NAME
model_name: MODEL_NAME
reference_dataset: [Q2 path]
monitoring_tool: [Q1]
cadence: [Q4]

# Drift thresholds
psi_warning: 0.10
psi_alert: 0.20

# High-risk features to monitor closely
priority_features: [Q3 list]

# Ground truth
ground_truth_available: [Q6 yes/no]
ground_truth_delay_days: [Q6 delay if applicable]

# Log storage
log_path: data/prediction_logs
```

### Step 7 — Print summary

```
✔ Monitoring middleware: src/PACKAGE/api/monitoring.py
✔ Dashboard notebook:   notebooks/monitoring-dashboard.py
✔ Monitoring runbook:   docs/monitoring-runbook.md
✔ Hydra config:         conf/monitor.yaml

Run the monitoring dashboard:
  uv run marimo edit notebooks/monitoring-dashboard.py

Add to docker-compose.yml to persist prediction logs:
  volumes:
    - ./data/prediction_logs:/app/data/prediction_logs

Next steps:
  - Set a calendar reminder to review the monitoring dashboard [cadence]
  - Share docs/monitoring-runbook.md with the on-call team
```
