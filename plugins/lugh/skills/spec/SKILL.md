---
name: spec
description: Use when the user wants to define scope, success criteria, or structure a plan before starting ML work. Creates a timestamped spec directory with plan, decisions, and success metrics. Must be run from inside a project created by lugh:new-ds-project. Inspired by CRISP-DM Business Understanding phase and Agent OS /shape-spec.
argument-hint: <spec-name>
allowed-tools: [Bash, Write]
---

# Lugh: Spec

Define scope and success criteria before writing any code.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
```

If `pyproject.toml` not found, stop with: "Run /lugh:spec from the root of a lugh project."

Extract `<spec-name>` from the argument. If none provided, ask the user for one.

Generate a slug: lowercase, hyphens for spaces.
Generate a timestamp: `date +%Y-%m-%d`
Set `SPEC_DIR=specs/$(date +%Y-%m-%d)-<slug>`

### Step 2 — Guided conversation

Ask the user the following questions one at a time using AskUserQuestion:

1. **Problem statement**: What problem are we solving? What decision or action will this model/analysis enable?
2. **Data sources**: What data is available? Where does it live? Any access constraints?
3. **Business success metrics**: How will stakeholders know this succeeded? (e.g. reduce churn by 5%, automate X reports)
4. **Technical success metrics**: What model performance thresholds are acceptable? (e.g. AUC > 0.85, precision > 0.9 at recall 0.7)
5. **Constraints and risks**: Timeline, compute budget, regulatory, privacy, data quality concerns?
6. **Key decisions already made**: Any constraints on model type, deployment target, or tech stack?

### Step 3 — Write spec files

Create `SPEC_DIR/` and write three files:

**`SPEC_DIR/plan.md`**
```markdown
# Spec: <spec-name>
**Project:** NAME
**Date:** YYYY-MM-DD

## Problem Statement
[answer from Q1]

## Data Sources
[answer from Q2]

## Scope
[derived from answers — what is IN scope, what is OUT of scope]
```

**`SPEC_DIR/success-metrics.md`**
```markdown
# Success Metrics: <spec-name>

## Business Metrics
[answer from Q3]

## Technical Metrics
[answer from Q4]

## Evaluation Plan
[how and when metrics will be measured]
```

**`SPEC_DIR/decisions.md`**
```markdown
# Decisions & Constraints: <spec-name>

## Constraints
[answer from Q5]

## Key Decisions
[answer from Q6]

## Open Questions
[anything unresolved that needs follow-up]
```

### Step 4 — Print summary

```
✔ Spec created: SPEC_DIR/

Next step → /lugh:data-profile <data-source>
  Profile your data to complete CRISP-DM Data Understanding.
```
