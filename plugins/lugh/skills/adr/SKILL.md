---
name: adr
description: Use when the user has made or is considering a specific architecture or technology choice and wants to document it as a formal Architecture Decision Record (ADR). Follows the MADR standard. Works standalone or inside a lugh project. Can be called at any time — not tied to a specific lifecycle phase.
argument-hint: <decision-slug>
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: Architecture Decision Record

Document an architecture or technology decision using the MADR standard.

## Instructions

### Step 1 — Detect project context and ADR number

Extract `<decision-slug>` from the argument. If none provided, ask the user for a short slug (e.g., `use-mlflow-for-experiment-tracking`).

```bash
# Create docs/adr/ if it doesn't exist
mkdir -p docs/adr

# Auto-increment: find the highest existing ADR number
LAST=$(ls docs/adr/*.md 2>/dev/null | grep -oP '^\d+' | sort -n | tail -1)
if [ -z "$LAST" ]; then
  NUM="0001"
else
  NUM=$(printf "%04d" $((10#$LAST + 1)))
fi
```

The output file will be `docs/adr/NUM-<slug>.md`.

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time:

1. **Title**: What is a human-readable title for this decision? (e.g., "Use MLflow for Experiment Tracking")

2. **Status**: What is the current status?
   Options: Proposed · Accepted · Deprecated · Superseded

3. **Context**: What situation, requirement, or constraint makes this decision necessary? What problem are you solving?

4. **Decision**: What was chosen or decided?

5. **Alternatives considered**: What other options were evaluated? (Can be brief — e.g., "Weights & Biases, Neptune, no tracking")

6. **Rationale**: Why was this option chosen over the alternatives?

7. **Consequences**: What are the positive outcomes? What are the trade-offs or negative consequences?

### Step 3 — Write ADR

Write `docs/adr/NUM-<slug>.md`:

```markdown
# NUM. TITLE

**Date:** YYYY-MM-DD
**Status:** [Q2]

---

## Context

[Q3]

---

## Decision

[Q4]

---

## Alternatives Considered

[Q5]

---

## Rationale

[Q6]

---

## Consequences

### Positive
[Q7 — positive outcomes]

### Trade-offs
[Q7 — negative outcomes or constraints introduced]
```

### Step 4 — Print summary

```
✔ ADR created: docs/adr/NUM-SLUG.md

To add another decision record:
  /lugh:adr <next-decision-slug>

To review your full architecture:
  cat docs/mlops-architecture.md
```
