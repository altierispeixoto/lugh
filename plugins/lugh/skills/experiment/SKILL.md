---
name: experiment
description: Use when the user wants to run a new ML experiment in a reproducible way. Creates a git branch, updates params.yaml with new parameter values, and creates a lightweight experiment log. Complements git and DVC — does not duplicate code that is already version-controlled. Must be run from inside a project created by lugh:new-ds-project. Covers CRISP-DM Modeling phase.
argument-hint: <experiment-name>
allowed-tools: [Bash, Write]
---

# Lugh: Experiment

Set up a reproducible ML experiment using git + DVC.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
```

If `pyproject.toml` not found, stop with: "Run /lugh:experiment from the root of a lugh project."

Extract `<experiment-name>` from the argument. If none, ask the user.

Generate:
- `BRANCH=experiment/<experiment-name>`
- `DATE=$(date +%Y-%m-%d)`
- `LOG_FILE=experiments/<experiment-name>.md`

### Step 2 — Create git branch

```bash
git checkout -b experiment/<experiment-name>
mkdir -p experiments
```

If the branch already exists, stop and tell the user: "Branch `experiment/<experiment-name>` already exists. Choose a different name or switch to it manually."

### Step 3 — Show current params and ask what to change

Read `params.yaml` and display it. Then use AskUserQuestion to ask:

1. **Hypothesis**: What do you expect this experiment to show?
2. **Parameters to change**: Which params from `params.yaml` should be different in this experiment? (e.g. `train.n_estimators: 200`, `train.max_depth: 8`)
3. **DVC stage to run**: Which stage(s) from `dvc.yaml` will this experiment exercise? (e.g. `train`, `evaluate`, or `all`)

### Step 4 — Update params.yaml

Apply the parameter changes the user specified to `params.yaml` using Bash/Write. Preserve all other values unchanged.

### Step 5 — Write experiment log

Write `experiments/<experiment-name>.md`:

```markdown
# Experiment: <experiment-name>

**Date:** DATE
**Branch:** BRANCH
**Project:** NAME

## Hypothesis
[answer from Q1]

## Parameter Changes
| Parameter | Original | New |
|-----------|----------|-----|
[one row per changed param]

## Run Command
```bash
dvc repro <stage>
# or: dvc exp run
```

## Results
<!-- Fill in after running -->

| Metric | Value |
|--------|-------|
|        |       |

## Conclusions
<!-- Fill in after reviewing results -->

## Next Steps
<!-- What to try next based on these results -->
```

### Step 6 — Print summary

```
✔ Branch created:   BRANCH
✔ params.yaml updated
✔ Experiment log:   experiments/<experiment-name>.md

Run your experiment:
  dvc repro <stage>

Fill in the Results section of experiments/<experiment-name>.md when done.

Next step → /lugh:model-card <model-name>
  Document your best model for evaluation and deployment.
```
