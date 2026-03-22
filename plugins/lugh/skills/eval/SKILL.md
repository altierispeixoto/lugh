---
name: eval
description: Use when the user wants to run a structured evaluation of a trained model — beyond just overall metrics. Guides through threshold selection, slice analysis, baseline comparison, and generates an evaluation notebook and go/no-go report. Must be run from inside a project created by lugh:new-ds-project. Covers CRISP-DM Evaluation phase.
argument-hint: <model-name>
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: Model Evaluation

Run structured evaluation and produce a go/no-go recommendation against project success criteria.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
DATE=$(date +%Y-%m-%d)
```

If `pyproject.toml` not found, stop with: "Run /lugh:eval from the root of a lugh project."

Extract `<model-name>` from the argument. If none, ask the user.

Check for existing artifacts to pre-populate the conversation:
- `metrics.json` or `models/<model-name>/metrics.json` — read if found, display to user
- `specs/` — read `success-metrics.md` from the most recent spec to get the agreed thresholds
- `experiments/` — detect if on an active experiment branch to offer to fill in Results section
- `models/<model-name>/model-card.md` — note if a model card already exists

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Task type**: What is the prediction task?
   - Binary classification
   - Multiclass classification
   - Regression
   - Ranking / recommendation
   - Time-series forecasting

2. **Predictions location**: Where are the test set predictions?
   - Path to a CSV/Parquet file with `y_true` and `y_pred` (and optionally `y_score`) columns
   - DVC metrics.json (already parsed in Step 1)
   - Run `dvc repro evaluate` now to generate them

3. **Class imbalance** (classification only): What is the positive class prevalence in the test set? (e.g., 5% churn rate) — affects which metrics are most meaningful.

4. **Operating threshold** (classification only): How should the decision threshold be chosen?
   - Fixed business threshold (e.g., "flag anyone with probability > 0.3")
   - Optimize for a specific metric (e.g., maximize F1, achieve recall ≥ 0.85)
   - Plot the full curve and let the team decide

5. **Subgroup slices**: Are there subgroups that must be evaluated separately? (e.g., by customer segment, geography, product category, time period, age group)
   - If yes: which column defines the subgroup, and what are the expected groups?

6. **Fairness requirements**: Are there protected attributes that require fairness evaluation? (e.g., gender, ethnicity, age bracket) — if yes, which fairness metric? (equalized odds, demographic parity, predictive parity)

7. **Baseline comparison**: What is the comparison baseline?
   - Previous model version (specify metric values)
   - Simple heuristic (e.g., "predict the majority class", "predict the historical mean")
   - No previous model — this is the first version

8. **Cost asymmetry**: What is more costly — a false positive or a false negative? (e.g., "missing a fraud case is 10× more costly than a false flag") — used to weight the threshold recommendation.

### Step 3 — Write Marimo evaluation notebook

Write `notebooks/eval-MODEL_NAME-DATE.py` as a Marimo notebook. The notebook must:

- Load predictions from the path specified in Q2
- **For classification:**
  - Overall metrics table: accuracy, precision, recall, F1, AUC-ROC, AUC-PR, log loss
  - Confusion matrix heatmap
  - ROC curve and Precision-Recall curve
  - Calibration plot (reliability diagram)
  - Threshold sensitivity plot (precision, recall, F1 vs. threshold)
  - Recommended threshold with justification based on Q4 and Q8
  - Slice analysis table: each subgroup from Q5 with all key metrics
  - Fairness metrics table if Q6 applies
- **For regression:**
  - Overall metrics: MAE, RMSE, MAPE, R²
  - Residuals distribution plot
  - Predicted vs. actual scatter plot
  - Error by subgroup from Q5
- **For all tasks:** comparison to baseline from Q7 (table showing delta per metric)
- Use `mo.md()` for section headers and interpretation notes

### Step 4 — Write evaluation report

Write `docs/evaluation-report-MODEL_NAME.md`:

```markdown
# Evaluation Report: MODEL_NAME

**Project:** NAME
**Date:** DATE
**Task:** [Q1]
**Test set size:** [from predictions]

---

## Overall Performance

| Metric | Value | vs. Baseline [Q7] |
|--------|-------|------------------|
[metrics table]

---

## Threshold Analysis

**Selected threshold:** [value]
**Rationale:** [from Q4 and Q8 — e.g., "threshold of 0.35 achieves recall ≥ 0.85 per spec requirement while minimizing false positives"]

---

## Subgroup Performance

| Subgroup | [Metric 1] | [Metric 2] | Delta vs. Overall |
|----------|-----------|-----------|------------------|
[from Q5]

---

## Fairness Assessment

[from Q6 — or "Not applicable" if no protected attributes identified]

---

## Success Criteria Check

[Read from specs/*/success-metrics.md if available — for each criterion, state: MET / NOT MET / BORDERLINE]

| Success Criterion | Target | Achieved | Status |
|------------------|--------|----------|--------|
[one row per criterion from spec]

---

## Go / No-Go Recommendation

**Recommendation:** GO / NO-GO / CONDITIONAL GO

**Rationale:** [1–3 sentences — references the success criteria check above and notes any subgroup concerns]

**Conditions (if applicable):** [what must be addressed before deployment]

---

## Known Limitations

[failure modes, distribution shift risks, subgroups with degraded performance]

---

## Next Steps

- [action item 1]
- [action item 2]
```

### Step 5 — Update experiment log if applicable

If currently on an `experiment/*` branch, offer to fill in the Results section of `experiments/<name>.md` with the evaluated metrics. If the user confirms, update the file.

### Step 6 — Print summary

```
✔ Evaluation notebook: notebooks/eval-MODEL_NAME-DATE.py
✔ Evaluation report:   docs/evaluation-report-MODEL_NAME.md

Run the notebook:
  uv run marimo edit notebooks/eval-MODEL_NAME-DATE.py

Next step → /lugh:model-card MODEL_NAME
  Document the model for governance and team handoff.
```
