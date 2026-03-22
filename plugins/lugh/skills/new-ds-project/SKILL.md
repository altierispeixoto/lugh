---
name: new-ds-project
description: Use when the user wants to create a new data science project, scaffold a DS project, start a new ML project, or set up a data science repository from scratch. Creates the full directory structure and all standard files including pyproject.toml, Dockerfile, ruff config, pre-commit hooks, DVC data folders, Jupyter templates, and pytest setup.
argument-hint: <project-name>
allowed-tools: [Bash, Write]
---

# New Data Science Project

Scaffold a complete, production-ready data science project from scratch.

## Instructions

### Step 1 — Parse Arguments

Extract `<project-name>` from the skill argument. Derive the three variables used in templates:

- **`NAME`** = the project name as provided (e.g., `my-ds-project`)
- **`PACKAGE`** = NAME with hyphens replaced by underscores — this is the Python package name (e.g., `my_ds_project`)
- **`TITLE`** = NAME with hyphens replaced by spaces, title-cased (e.g., `My Ds Project`)

If no argument is provided, ask the user for a project name before proceeding.

### Step 2 — Create Directory Tree

Run this single Bash command (replace `NAME` and `PACKAGE` with actual values):

```bash
mkdir -p NAME/{src/PACKAGE,tests,notebooks,data/{raw,processed,staging,model_features},sql}
```

### Step 3 — Write All Files

Write each file below using the Write tool. Replace every occurrence of `${name}` with NAME, `${package}` with PACKAGE, and `${title}` with TITLE in the file contents.

---

#### `NAME/.gitignore`

```
# Ignore everything in this directory
*
# Except this file
!.gitignore
```

---

#### `NAME/ruff.toml`

```toml
# Enable Ruff's default rules plus additional ones
lint.select = [
    "ALL",            # All rules
    "ASYNC",          # Additional async/await checks
    "B",             # Bugbear: detecting potential bugs
    "C4",            # Flake8 comprehensions
    "DTZ",           # Datetime checks
    "EM",            # Error messages
    "ERA",           # Commented-out code detection
    "INT",           # gettext functions
    "NPY",           # NumPy-specific rules
    "PD",            # Pandas-specific rules
    "PT",            # pytest-specific rules
    "RUF",           # Ruff-specific rules
    "S",             # Security checks
    "SIM",           # Code simplification
    "SLOT",          # __slots__ checks
]

# Ignore specific rules
lint.ignore = [
    "D100",          # Missing docstring in public module
    "D104",          # Missing docstring in public package
    "D203",          # One blank line before class docstring
    "D212",          # Multi-line docstring should start at the first line
    "E501",          # Line too long (handled by formatter)
    "PLR0913",       # Too many arguments to function call
    "PD901",         # DataFrame variable name should be df
    "S101",          # Use of assert detected (pytest needs this)
]

# Allow autofix for all enabled rules (when `--fix` is provided)
lint.fixable = ["ALL"]
lint.unfixable = []

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]

# Same as Black.
line-length = 120

# Allow unused variables when underscore-prefixed.
lint.dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Assume Python 3.12.
target-version = "py312"

[lint.per-file-ignores]
# Tests can use assert statements and relative imports
"tests/**/*" = ["S101", "TID252"]

[lint.mccabe]
# Unlike Flake8, default to a complexity level of 10.
max-complexity = 10

[lint.pycodestyle]
max-doc-length = 120

[lint.pydocstyle]
convention = "google"

[lint.isort]
force-single-line = true
combine-as-imports = true
known-first-party = ["${name}"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[lint.flake8-bugbear]
extend-immutable-calls = ["fastapi.Depends", "fastapi.Query", "fastapi.Body"]

[lint.pyupgrade]
# Preserve types, even if a file imports `from __future__ import annotations`.
keep-runtime-typing = true

[lint.pylint]
max-args = 8

[format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"
```

**Important**: In this file, replace `${name}` in `known-first-party` with PACKAGE.

---

#### `NAME/.env-template`

```
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
API_WORKERS=4
API_TIMEOUT=30

# Model Configuration
MODEL_PATH=models/production
MODEL_VERSION=latest
BATCH_SIZE=32
NUM_WORKERS=4

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=${name}
MLFLOW_REGISTRY_URI=sqlite:///mlflow.db

# DVC Configuration
DVC_REMOTE=s3://your-bucket/path
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region

# Monitoring & Logging
LOG_LEVEL=INFO
MONITORING_PORT=9090
ENABLE_METRICS=true

# Security & Authentication
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=60

# Feature Store (Optional)
FEAST_ONLINE_STORE=redis://localhost:6379
FEAST_REGISTRY=data/registry.db

# Cache Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_password

# Development Settings
DEBUG=false
ENVIRONMENT=development  # development, staging, production
```

**Important**: In this file, replace `${name}` in `MLFLOW_EXPERIMENT_NAME` with NAME.

---

#### `NAME/Dockerfile`

```dockerfile
# syntax=docker/dockerfile:1.4

# Use a multi-stage build for efficiency
FROM python:3.12-slim-bookworm AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/opt/uv-cache/

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv using official install script
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# Create non-root user
RUN useradd -m -s /bin/bash app-user

# Set working directory and ownership
WORKDIR /app
RUN chown app-user:app-user /app

# Switch to non-root user
USER app-user

# Copy dependency files with explicit ownership
COPY --chown=app-user:app-user pyproject.toml uv.lock ./

# Install dependencies using mount cache
RUN --mount=type=cache,target=/opt/uv-cache,uid=$(id -u app-user) \
    /root/.cargo/bin/uv sync --no-install-project --frozen

# Copy the rest of the application code
COPY --chown=app-user:app-user . .

# Final stage
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd -m -s /bin/bash app-user

# Set working directory and ownership
WORKDIR /app
RUN chown app-user:app-user /app

# Copy the installed dependencies and application from the builder stage
COPY --from=builder --chown=app-user:app-user /app /app

# Switch to non-root user
USER app-user

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Default command
ENTRYPOINT ["uv", "run"]
CMD ["my_app"]
```

---

#### `NAME/.dockerignore`

```
# Version control
.git
.gitignore
.gitattributes

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env*
.venv
venv/
ENV/
env.bak/
venv.bak/
uv.lock

# Testing
.tox/
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.hypothesis/
coverage.xml
*.cover
pytest-report.xml
nosetests.xml

# Development
*.log
*.swp
*.swo
.DS_Store
.idea/
.vscode/
.vs/
*.sublime-*
.mypy_cache/
.ruff_cache/

# Build and distribution
*.egg-info/
dist/
build/
*.egg

# Project specific
data/
logs/
*.db
*.sqlite3
.dvc/
tmp/
temp/

# Documentation
docs/_build/
site/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Local development configuration
*.local
.env.local
config.local.*
```

---

#### `NAME/justfile`

```makefile
# Set the Python version
python_version := "3.12"

# Default recipe to display available commands
default:
    @just --list

# Create a virtual environment using uv with specified Python version and set up pre-commit
setup:
    @echo "Creating virtual environment using Python {{python_version}}..."
    uv venv --python {{python_version}}
    @echo "Virtual environment created."
    @echo "Installing pre-commit hooks..."
    @just run uv sync
    @just run pre-commit install && pre-commit autoupdate && pre-commit run -a -v
    @echo "Pre-commit hooks installed."
    @echo "To activate the environment, run: just activate"


# Run a command in the virtual environment
run *ARGS:
    @if [ ! -d ".venv" ]; then \
        echo "Virtual environment not found. Creating one..."; \
        uv venv --python {{python_version}}; \
    fi
    @source .venv/bin/activate && {{ ARGS }}

# Activate the virtual environment
activate:
    #!/usr/bin/env bash
    source .venv/bin/activate
    echo "Virtual environment activated. Run 'deactivate' to exit."
    $SHELL

# Deactivate the virtual environment
deactivate:
    @echo "To deactivate the virtual environment, simply run 'deactivate' in your shell."
    @echo "If you're in a subshell created by 'just activate', type 'exit' to leave it."


# Install project dependencies using uv sync
install:
    @echo "Installing project dependencies..."
    @just run uv sync

# Update project dependencies using uv sync with upgrade
update:
    @echo "Updating project dependencies..."
    @just run uv sync --upgrade

# Clean up the virtual environment
clean:
    @echo "Removing virtual environment..."
    rm -rf .venv
    @echo "Virtual environment removed."
```

---

#### `NAME/pyproject.toml`

```toml
[project]
name = "${name}"
version = "0.1.0"
description = "My Data Science Project"
readme = "README.md"
license = { text = "MIT" }
authors = [{ name = "firstname.lastname", email = "firstname.lastname@example.com" }]
requires-python = ">=3.10"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

dependencies = [
    "hydra-core>=1.3.2",
    "numpy>=1.26.0",
    "pandas>=2.2.0",
    "scikit-learn>=1.4.0",
    "dvc>=3.30.0",
]

[project.optional-dependencies]
dev = [
    "ipykernel>=6.29.0",
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "pytest-xdist>=3.5.0",
    "pre-commit>=3.6.0",
    "ruff>=0.2.0",
]

viz = [
    "matplotlib>=3.8.0",
    "seaborn>=0.13.0",
    "plotly>=5.18.0",
]

notebook = [
    "jupyter>=1.0.0",
    "nbconvert>=7.14.0",
    "nbformat>=5.9.0",
]

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
    "integration",
]

[project.scripts]
${name} = "${name}.main:run"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Important**: Replace both `${name}` occurrences with NAME.

---

#### `NAME/README.md`

```markdown
# ${title}

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6)](https://dvc.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## 🌟 Project Overview

[Provide a brief, engaging introduction to your project. What problem does it solve? Why is it valuable?]

### Key Features

- 🔍 [Key Feature 1]
- 📊 [Key Feature 2]
- 🤖 [Key Feature 3]

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) for package management
- [Docker](https://www.docker.com/) (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/${title}.git
   cd ${title}
   ```

2. Set up the development environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` with your configurations following [twelve-factor](https://12factor.net/) methodology.

## 📊 Data Pipeline

### Data Version Control

We use [DVC](https://dvc.org/) for data and model versioning:

```bash
# Pull latest data
dvc pull

# Track new data
dvc add data/raw/new_dataset.csv
dvc push
```

### Training Pipeline

1. Prepare data:
   ```bash
   python src/data/make_dataset.py
   ```

2. Train model:
   ```bash
   python src/models/train_model.py
   ```

3. Evaluate results:
   ```bash
   python src/models/evaluate.py
   ```

## 🗂️ Project Structure

```
├── data/               # Data directory (DVC tracked)
│   ├── raw/           # Raw, immutable data
│   ├── processed/     # Cleaned, transformed data
│   └── features/      # Engineered features
├── models/            # Trained models
├── notebooks/         # Jupyter notebooks
├── src/              # Source code
│   ├── data/         # Data processing scripts
│   ├── features/     # Feature engineering
│   └── models/       # Model training and inference
├── tests/            # Unit and integration tests
├── .env.template     # Environment variables template
├── .gitignore       # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hooks
├── pyproject.toml    # Project dependencies
└── README.md         # Project documentation
```


## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 0.XX |
| F1 Score | 0.XX |
| AUC-ROC | 0.XX |

## 🚀 Deployment

### Docker

Build and run the Docker container:
```bash
docker build -t ${title} .
docker run -p 8000:8000 ${title}
```

### Model Versioning

1. Version your model with DVC:
   ```bash
   dvc add models/model.joblib
   git add models/model.joblib.dvc
   dvc push
   ```

2. Tag the release:
   ```bash
   git tag -a v1.0.0 -m "Release model v1.0.0"
   git push origin v1.0.0
   ```

### CI/CD Pipeline

This project uses automated CI/CD pipelines that are triggered by git tags. The pipeline:

1. Runs all tests
2. Validates code quality
3. Builds Docker container
4. Deploys to staging/production

> ⚠️ **Important**: Always push model updates to DVC before creating git tags

For more information on our deployment strategy, see [12factor - build release run](https://12factor.net/build-release-run).

## 👥 Contact

### Project Maintainers
* **[Your Name]** - Lead Data Scientist - [email@example.com](mailto:email@example.com)

### Contributors
See the [CONTRIBUTORS.md](CONTRIBUTORS.md) file for the list of contributors to this project.
```

**Important**: Replace all `${title}` occurrences with TITLE.

---

#### `NAME/CONTRIBUTING.md`

```markdown
# Contributing Guidelines

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing.

## Code of Conduct

Please note that this project is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone git@github.com:your-username/${name}.git
   cd ${name}
   ```
3. Set up your development environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following our coding standards:
   - Use type hints
   - Follow PEP 8 style guide (enforced by Ruff)
   - Write docstrings in Google format
   - Include tests for new functionality

3. Run tests and linting:
   ```bash
   pytest
   ruff check .
   ruff format .
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: your descriptive commit message"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request

## Pull Request Guidelines

- Fill out the PR template completely
- Include tests for new functionality
- Update documentation as needed
- Ensure CI passes (tests, linting, type checking)
- Keep PRs focused and reasonably sized

## Data Science Specific Guidelines

### Notebooks
- Clean notebooks before committing (clear outputs)
- Move reusable code to Python modules
- Use DVC for data versioning

### Models
- Version models with DVC
- Document model parameters and metrics
- Include model cards for production models

### Experiments
- Log experiments with MLflow or similar
- Document experiment configurations
- Save experiment results and artifacts

## Questions or Suggestions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Documentation improvements
- General questions

Thank you for contributing!
```

**Important**: Replace `${name}` with NAME.

---

#### `NAME/.pre-commit-config.yaml`

```yaml
# Pre-commit configuration for data science projects
# This configuration includes hooks for code quality, security, and data science specific checks

default_language_version:
    python: python3.12
default_stages: [commit, push]

ci:
    autofix_commit_msg: 'style: auto fixes from pre-commit hooks'
    autoupdate_commit_msg: 'chore: update pre-commit hooks'
repos:
  # pre-commit-hooks repository contains a collection of git hooks for pre-commit
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0  # The version of the pre-commit-hooks to use
    hooks:
      - id: trailing-whitespace  # Removes trailing whitespace
      - id: check-added-large-files  # Prevents adding large files to the git repository
      - id: check-ast  # Validates Python abstract syntax trees
      - id: check-json  # Checks JSON file syntax
      - id: check-merge-conflict  # Checks for unresolved merge conflicts
      - id: check-xml  # Checks XML file syntax
      - id: check-yaml  # Checks YAML file syntax
      - id: debug-statements  # Checks for debug statements
      - id: end-of-file-fixer  # Ensures files end with a newline
      - id: mixed-line-ending
        args: ['--fix=auto']  # Automatically fixes line endings (can be set to 'lf' or 'crlf')

  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.7.2
    hooks:
      # Run the linter.
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      # Run the formatter.
      - id: ruff-format

  - repo: https://github.com/kynan/nbstripout
    rev: 0.8.0
    hooks:
      - id: nbstripout
        files: ".ipynb"

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2  # Specify the desired version of Gitleaks
    hooks:
      - id: gitleaks

  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.5
    hooks:
      - id: sqlfluff-lint
        additional_dependencies: ['dbt-postgres', 'sqlfluff-templater-dbt']
      - id: sqlfluff-fix
        additional_dependencies: ['dbt-postgres', 'sqlfluff-templater-dbt']

  # Check for common data science issues
  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.8.4
    hooks:
      - id: nbqa-ruff
        additional_dependencies: [ruff==0.2.0]
      - id: nbqa-isort
        additional_dependencies: [isort==5.13.2]

  # DVC validation
  - repo: https://github.com/iterative/dvc
    rev: 3.30.1
    hooks:
      - id: dvc-pre-commit
        additional_dependencies: ['.[all]']
        stages: [commit]
        verbose: true

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-all
          - pandas-stubs
          - types-requests
        args: [--ignore-missing-imports, --disallow-untyped-defs]

  # Check requirements files
  - repo: https://github.com/python-poetry/poetry
    rev: 1.7.0
    hooks:
      - id: poetry-check
      - id: poetry-lock
```

---

#### `NAME/sql/.sqlfluff`

```ini
#------------------------------------------------------------------------------#
# Setup
#------------------------------------------------------------------------------#
[sqlfluff]
dialect = snowflake
templater = dbt
exclude_rules = L034

# Allow fix commands to run on files
fix_even_unparsable = True

# Output message formats
output_line_length = 120
max_line_length = 120

# Ignore certain file types
ignore = templated_file_name,parsing
ignore_templated_areas = True

# Ignore specific paths
exclude_path = target/,macros/,logs/

[sqlfluff:templater:jinja]
apply_dbt_builtins = True
load_macros_from_path = macros

[sqlfluff:templater:dbt]
project_dir = .
profiles_dir = ~/.dbt
profile = default

[sqlfluff:templater:dbt:context]
DBT_ENVIRONMENT = QA
schema = YOUR_SCHEMA  # Replace with your actual schema
database = YOUR_DB    # Replace with your actual database

#------------------------------------------------------------------------------#
# Custom Settings
#------------------------------------------------------------------------------#
[sqlfluff:indentation]
indented_joins = False
indented_ctes = False
indented_using_on = True
indented_on_contents = False
template_blocks_indent = True

[sqlfluff:rules]
tab_space_size = 4
max_line_length = 120
indent_unit = space
comma_style = trailing
allow_scalar = True
single_table_references = consistent
unquoted_identifiers_policy = aliases
```

---

#### `NAME/notebooks/template.ipynb`

Write this exact JSON content:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Notebook Title\n",
    "\n",
    "**Author:** [Your Name]  \n",
    "**Date:** [Date]  \n",
    "**Purpose:** Brief description of the notebook's purpose\n",
    "\n",
    "## Table of Contents\n",
    "1. [Setup](#Setup)\n",
    "2. [Data Loading](#Data-Loading)\n",
    "3. [Exploratory Data Analysis](#EDA)\n",
    "4. [Analysis](#Analysis)\n",
    "5. [Results](#Results)\n",
    "6. [Conclusions](#Conclusions)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Setup\n",
    "\n",
    "Import required libraries and set up the environment"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "tags": [
     "setup"
    ]
   },
   "outputs": [],
   "source": [
    "# Standard imports\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Project imports\n",
    "import PACKAGE  # noqa: F401\n",
    "\n",
    "# Notebook settings\n",
    "%load_ext autoreload\n",
    "%autoreload 2\n",
    "\n",
    "# Display settings\n",
    "%matplotlib inline\n",
    "plt.style.use('seaborn')\n",
    "sns.set_theme()\n",
    "pd.set_option('display.max_columns', None)\n",
    "\n",
    "# Optional: for reproducibility\n",
    "np.random.seed(42)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Loading\n",
    "\n",
    "Load and prepare the data for analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "tags": [
     "data-loading"
    ]
   },
   "outputs": [],
   "source": [
    "# Load your data here\n",
    "# Example:\n",
    "# df = pd.read_csv('path/to/data.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Exploratory Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "tags": [
     "eda"
    ]
   },
   "outputs": [],
   "source": [
    "# Basic data exploration\n",
    "# df.info()\n",
    "# df.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Analysis\n",
    "\n",
    "Main analysis section"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "tags": [
     "analysis"
    ]
   },
   "outputs": [],
   "source": [
    "# Your analysis code here"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Results\n",
    "\n",
    "Summary of key findings"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "- Key conclusion 1\n",
    "- Key conclusion 2\n",
    "- Next steps"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbformat_minor": 4,
   "pygments_lexer": "ipython3",
   "version": "3.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
```

**Important**: Replace `PACKAGE` in `import PACKAGE` with the actual PACKAGE value.

---

#### `NAME/data/.gitignore`

```
# Ignore all files in this directory by default
*

# Keep directories but ignore their contents
# Data directories
!raw/
raw/*
!raw/.gitkeep

!interim/
interim/*
!interim/.gitkeep

!processed/
processed/*
!processed/.gitkeep

!external/
external/*
!external/.gitkeep

# Model directories
!models/
models/*
!models/.gitkeep
!models/README.md

# Features
!features/
features/*
!features/.gitkeep

# DVC files
!*.dvc
!.dvcignore
!dvc.yaml
!dvc.lock

# Experiment tracking
!mlruns/
mlruns/*
!mlruns/.gitkeep

# Documentation about data
!README.md
!DATACARD.md
!CHANGELOG.md
```

---

#### `NAME/data/raw/.gitignore`, `NAME/data/processed/.gitignore`, `NAME/data/staging/.gitignore`, `NAME/data/model_features/.gitignore`

All four have identical content:

```
# Ignore everything in this directory
*
# Except this file
!.gitignore
```

---

#### `NAME/tests/__init__.py`

Empty file.

---

#### `NAME/tests/test_my_module.py`

```python
"""Example test module demonstrating testing best practices."""

import pytest
from typing import List, Tuple
import numpy as np
import pandas as pd


@pytest.fixture
def sample_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Create sample data for testing.

    Returns:
        Tuple containing features DataFrame and target Series.
    """
    np.random.seed(42)
    n_samples = 100

    # Generate synthetic data
    X = pd.DataFrame({
        'feature1': np.random.normal(0, 1, n_samples),
        'feature2': np.random.uniform(-1, 1, n_samples)
    })
    y = pd.Series(np.random.binomial(1, 0.5, n_samples), name='target')

    return X, y


def test_data_preparation(sample_data: Tuple[pd.DataFrame, pd.Series]) -> None:
    """Test data preparation functionality.

    Args:
        sample_data: Fixture providing test data.
    """
    X, y = sample_data

    # Test data shape
    assert X.shape[0] == y.shape[0], "Features and target must have same number of samples"
    assert X.shape[1] == 2, "Expected 2 features"

    # Test data types
    assert X.dtypes.all() == np.float64, "Features should be float64"
    assert y.dtype == np.int64, "Target should be int64"

    # Test for missing values
    assert not X.isna().any().any(), "Features should not contain missing values"
    assert not y.isna().any(), "Target should not contain missing values"


@pytest.mark.parametrize("threshold", [-0.5, 0.0, 0.5])
def test_feature_threshold(sample_data: Tuple[pd.DataFrame, pd.Series], threshold: float) -> None:
    """Test feature thresholding with different values.

    Args:
        sample_data: Fixture providing test data.
        threshold: Value to test for thresholding.
    """
    X, _ = sample_data
    feature1_above_threshold = X['feature1'] > threshold

    assert isinstance(feature1_above_threshold, pd.Series), "Result should be a pandas Series"
    assert feature1_above_threshold.dtype == bool, "Result should be boolean"
```

---

#### `NAME/src/PACKAGE/__init__.py`

Empty file. (Note: the actual path uses PACKAGE as the directory name.)

---

### Step 4 — Print Summary

After all files are written, print:

```
✓ Created project: NAME

Directory structure:
  NAME/
  ├── src/PACKAGE/
  ├── tests/
  ├── notebooks/
  ├── data/{raw,processed,staging,model_features}/
  └── sql/

Next steps:
  cd NAME
  git init && git add . && git commit -m "chore: initial project scaffold"
  uv venv && source .venv/bin/activate
  uv sync
  pre-commit install
  dvc init        # optional: enable data versioning
```
