# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code **plugin** (marketplace package) named `lugh` — a suite of skills covering the data science and ML engineering lifecycle. It contains no Python source code; the entire repo is SKILL.md files, a template directory, and configuration JSON.

## Repository layout

```
.claude-plugin/marketplace.json     # Marketplace registration
plugins/lugh/
  .claude-plugin/plugin.json        # Plugin manifest
  README.md                         # Plugin-level skill reference
  skills/<skill-name>/SKILL.md      # One skill per subdirectory
  skills/new-ds-project/template/   # Files copied verbatim when scaffolding a project
README.md                           # Public-facing documentation
```

## Skills in the lifecycle

All skills (except `new-ds-project`) require a project created by `new-ds-project` and must be run from its root. The sequential order is:

1. `new-ds-project` — scaffold
2. `spec` — problem framing
3. `arch` — MLOps infrastructure
4. `data-profile` — EDA + data dictionary
5. `data-quality` — validation rules + executable checks
6. `featurize` — feature catalog + featurize.py DVC stage
7. `experiment` — git branch + params + log
8. `eval` — slice analysis, threshold selection, go/no-go report
9. `model-card` — model governance documentation
10. `ml-api` — FastAPI serving scaffold
11. `monitor` — drift detection + prediction logging + runbook

`next` is a navigator (any phase). `adr` is a utility skill (any phase, not sequential).

## SKILL.md format

Every `SKILL.md` has YAML frontmatter followed by markdown instructions:

```yaml
---
name: <skill-name>
description: <used by Claude to decide when to invoke this skill>
argument-hint: <displayed to user>
allowed-tools: [Bash, Write, AskUserQuestion]   # subset of Claude tools the skill may use
---
```

The `description` field is the most important part — it controls when Claude auto-triggers the skill. Keep it specific and action-oriented.

## Template placeholder system (`new-ds-project`)

The `template/` directory contains the project scaffold with three tokens:

- `__NAME__` → project name as given (e.g. `my-ds-project`)
- `__PACKAGE__` → hyphens replaced with underscores (e.g. `my_ds_project`)
- `__TITLE__` → title-cased with spaces (e.g. `My Ds Project`)

The Python package directory is `src/__PACKAGE__/` and gets renamed at scaffold time via `mv`. All `.gitignore` files in the template are stored as `_gitignore` — this prevents the template's root `_gitignore` (which contains `*`) from shadowing its own sibling files in git. The SKILL.md restores them with:

```bash
find NAME/ -name "_gitignore" | while read f; do mv "$f" "$(dirname $f)/.gitignore"; done
```

## Adding a new skill

1. Create `plugins/lugh/skills/<name>/SKILL.md`
2. Add a row to the skills table in `plugins/lugh/README.md`
3. Add a `### lugh:<name>` section to the root `README.md`
4. If the skill is a sequential lifecycle phase, add phase detection to `plugins/lugh/skills/next/SKILL.md` (Step 2 Bash block) and update the phase order list (Step 3)

## Project context detection pattern

All lifecycle skills auto-detect the project name the same way — copy this exactly:

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
```

If `pyproject.toml` is missing, stop with: `"Run /lugh:<skill> from the root of a lugh project."`
