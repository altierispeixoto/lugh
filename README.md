<div align="center">
  <img src="assets/lugh.jpg" alt="Lugh — Celtic master of all crafts" width="200"/>

  # Lugh

  **A Claude Code marketplace for data science workflows**

  *Named after Lugh, the Celtic master-craftsman god — master of all skills and arts.*
</div>

---

## Installation

### Add the marketplace

```bash
claude plugins marketplace add altierispeixoto/lugh
```

### Install the plugin

```bash
claude plugins add lugh lugh
```

---

## Available Skills

### `lugh:new-ds-project`

Scaffold a complete, production-ready data science project from scratch.

**Usage:**

```
/new-ds-project <project-name>
```

**What it creates:**

```
my-project/
├── src/my_project/          # Python package (main.py, py.typed)
├── tests/                   # pytest test suite
├── notebooks/               # Marimo notebook template
├── conf/                    # Hydra configuration
├── data/{raw,processed,staging,model_features}/
├── models/                  # Trained model artifacts (DVC-tracked)
├── sql/                     # SQL linting config
├── dvc.yaml                 # DVC pipeline (prepare/featurize/train/evaluate)
├── params.yaml              # Experiment parameters
├── pyproject.toml           # Dependencies (uv)
├── ruff.toml                # Linter & formatter config
├── Dockerfile               # Multi-stage Docker build
├── justfile                 # Task runner
├── .github/workflows/ci.yml # GitHub Actions CI
├── .pre-commit-config.yaml  # Code quality hooks
├── .editorconfig            # Editor formatting rules
├── .env-template            # Environment variables
└── README.md
```

**Stack**: Python 3.12, uv, DVC, Hydra, Marimo, Ruff, mypy, pre-commit, pytest, Docker, SQLFluff, GitHub Actions

---

## Roadmap

Future skills planned for the `lugh` plugin:

- `eda-report` — Generate an EDA report from a CSV/parquet file
- `dvc-pipeline` — Scaffold a DVC pipeline with stages
- `model-card` — Generate a model card markdown template

---

## License

MIT
