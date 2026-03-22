---
name: next
description: Use when the user wants to know where they are in the DS/ML project lifecycle and what to do next. Shows a status board of completed phases and recommends the next lugh skill to run. Must be run from inside a project created by lugh:new-ds-project.
allowed-tools: [Bash]
---

# Lugh: What's Next?

Show project lifecycle status and recommend the next step.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` is not found, stop and print:
```
Error: Run /lugh:next from the root of a project created with /lugh:new-ds-project
```

### Step 2 — Inspect project phases

Run these checks via Bash:

```bash
# Phase signals
test -f pyproject.toml && echo "scaffold:done" || echo "scaffold:missing"
ls specs/ 2>/dev/null | grep -q . && echo "spec:done" || echo "spec:missing"
test -f docs/mlops-architecture.md && echo "arch:done" || echo "arch:missing"
ls notebooks/eda-*.py 2>/dev/null | grep -q . && echo "data-profile:done" || echo "data-profile:missing"
ls experiments/ 2>/dev/null | grep -q . && echo "experiment:done" || echo "experiment:missing"
find models/ -name "model-card.md" 2>/dev/null | grep -q . && echo "model-card:done" || echo "model-card:missing"
test -f "src/${PACKAGE}/api/app.py" && echo "ml-api:done" || echo "ml-api:missing"
```

### Step 3 — Print status board and recommendation

Print the status board using ✔ for done and ○ for missing. Then identify the first incomplete phase (in order) and print a concrete recommendation with the exact command and a one-line explanation.

Phase order and skill mapping:
1. scaffold → `new-ds-project` (always done if we got this far)
2. spec → `/lugh:spec <project-goal>`
3. arch → `/lugh:arch` (define the MLOps infrastructure stack)
4. data-profile → `/lugh:data-profile <data-source>`
5. experiment → `/lugh:experiment <experiment-name>`
6. model-card → `/lugh:model-card <model-name>`
7. ml-api → `/lugh:ml-api <model-name>`

Note: `/lugh:adr` is a utility skill for documenting individual decisions — it can be run at any time and is not part of the sequential lifecycle.

If all phases are complete, print: "All phases complete. Run /lugh:next anytime to review status."
