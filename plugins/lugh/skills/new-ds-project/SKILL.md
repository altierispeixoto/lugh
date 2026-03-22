---
name: new-ds-project
description: Use when the user wants to create a new data science project, scaffold a DS project, start a new ML project, or set up a data science repository from scratch. Creates the full directory structure and all standard files including pyproject.toml, Dockerfile, ruff config, pre-commit hooks, DVC pipeline, Hydra config, Marimo notebooks, GitHub Actions CI, and pytest setup.
argument-hint: <project-name>
allowed-tools: [Bash, Write]
---

# New Data Science Project

Scaffold a complete, production-ready data science project from scratch.

## Instructions

### Step 1 — Parse Arguments

Extract `<project-name>` from the skill argument. Derive:

- **`NAME`** = project name as provided (e.g., `my-ds-project`)
- **`PACKAGE`** = NAME with hyphens replaced by underscores (e.g., `my_ds_project`)
- **`TITLE`** = NAME with hyphens replaced by spaces, title-cased (e.g., `My Ds Project`)

If no argument is provided, ask the user for a project name before proceeding.

### Step 2 — Copy template and rename package directory

The skill's base directory is provided at the top of this invocation as "Base directory for this skill: <path>". Use that path below.

```bash
cp -r <skill_base_dir>/template/ NAME/
mv NAME/src/__PACKAGE__ NAME/src/PACKAGE
```

### Step 3 — Replace placeholders in all files

```bash
find NAME/ -type f | xargs sed -i \
  -e 's/__NAME__/NAME/g' \
  -e 's/__PACKAGE__/PACKAGE/g' \
  -e 's/__TITLE__/TITLE/g'
```

### Step 4 — Print summary

```
✓ Created project: NAME

Directory structure:
  NAME/
  ├── src/PACKAGE/         Python package (main.py, py.typed)
  ├── tests/
  ├── notebooks/           Marimo notebooks
  ├── conf/                Hydra configuration
  ├── data/{raw,processed,staging,model_features}/
  ├── models/
  ├── sql/
  └── .github/workflows/  GitHub Actions CI

Next steps:
  cd NAME
  git init && git add . && git commit -m "chore: initial project scaffold"
  uv venv && source .venv/bin/activate
  uv sync
  pre-commit install
  dvc init        # enable data versioning
```
