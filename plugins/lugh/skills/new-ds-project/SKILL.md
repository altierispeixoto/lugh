---
name: new-ds-project
description: Use when the user wants to create a new data science project, scaffold a DS project, start a new ML project, or set up a data science repository from scratch. Creates the full directory structure and all standard files including pyproject.toml, Dockerfile, ruff config, pre-commit hooks, DVC pipeline, Hydra config, Marimo notebooks, GitHub Actions CI, and pytest setup.
argument-hint: <project-name>
allowed-tools: [Bash, Write, AskUserQuestion]
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
find NAME/ -name "_gitignore" | while read f; do mv "$f" "$(dirname $f)/.gitignore"; done
```

### Step 3 — Replace placeholders in all files

```bash
find NAME/ -type f | xargs sed -i \
  -e 's/__NAME__/NAME/g' \
  -e 's/__PACKAGE__/PACKAGE/g' \
  -e 's/__TITLE__/TITLE/g'
```

### Step 4 — Initialize git, install dependencies, and set up pre-commit

Run the following commands in order:

```bash
cd NAME && git init && git add . && git commit -m "chore: initial project scaffold"
```

```bash
cd NAME && uv venv && uv sync
```

```bash
cd NAME && pre-commit install
```

If any command fails, report the error and stop.

### Step 5 — Ask about DVC

Use AskUserQuestion to ask:

> Would you like to initialize DVC for data versioning? (runs `dvc init`)

If yes:

```bash
cd NAME && dvc init
```

### Step 6 — Print summary

Print a summary reflecting what was completed. Adjust the DVC line based on the user's answer in Step 5.

```
✓ Created project: NAME
✓ Git repository initialized with initial commit
✓ Virtual environment created and dependencies installed
✓ Pre-commit hooks installed
✓ DVC initialized          ← omit if user declined

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

To start working:
  cd NAME
  source .venv/bin/activate
```
