---
name: model-card
description: Use when the user has a trained model and wants to document it for governance, team handoff, or deployment. Creates a model card following the Google Model Card standard. Must be run from inside a project created by lugh:new-ds-project. Covers CRISP-DM Evaluation phase.
argument-hint: <model-name>
allowed-tools: [Bash, Write]
---

# Lugh: Model Card

Document a trained model for governance, evaluation, and deployment.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
```

If `pyproject.toml` not found, stop with: "Run /lugh:model-card from the root of a lugh project."

Extract `<model-name>` from the argument. If none, ask the user.

### Step 2 — Check for existing metrics

Look for `metrics.json` in the project root or `models/<model-name>/`. If found, read and display the metrics so the user can reference them during the conversation.

### Step 3 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Model version & type**: What version is this? What algorithm/architecture? (e.g. RandomForest v1.2, XGBoost, BERT fine-tune)
2. **Intended use cases**: What is this model designed to do? Who are the primary users?
3. **Out-of-scope uses**: What should this model NOT be used for?
4. **Training data**: What data was used for training? Time range, geography, population, any known biases?
5. **Evaluation results**: Key metrics overall (accuracy, AUC, F1, RMSE, etc.) and per important subgroup/slice if applicable
6. **Known limitations**: Where does the model struggle? Edge cases, distribution shift risks?
7. **Ethical considerations**: Any fairness concerns, privacy implications, or potential for misuse?

### Step 4 — Write model card

Create `models/<model-name>/` if it doesn't exist.

Write `models/<model-name>/model-card.md`:

```markdown
# Model Card: <model-name>

**Project:** NAME
**Version:** [Q1]
**Date:** YYYY-MM-DD
**Algorithm:** [Q1]

---

## Model Details

### Intended Use

**Primary use cases:** [Q2]

**Out-of-scope uses:** [Q3]

---

## Training Data

[Q4]

---

## Evaluation Results

### Overall Performance

| Metric | Value |
|--------|-------|
[from Q5 or metrics.json]

### Performance by Subgroup

| Subgroup | Metric | Value |
|----------|--------|-------|
[from Q5, or "Not yet evaluated — recommended before production"]

---

## Limitations

[Q6]

---

## Ethical Considerations

[Q7]

---

## Caveats and Recommendations

- Model performance may degrade on data from different time periods or geographies than the training set
- Monitor for data drift in production
- Re-evaluate metrics quarterly or after significant data changes
```

### Step 5 — Print summary

```
✔ Model card: models/<model-name>/model-card.md

Next step → /lugh:ml-api <model-name>
  Scaffold a REST API to serve this model in production.
```
