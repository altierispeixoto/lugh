<div align="center">
  <img src="assets/logo.png" alt="Lugh — Celtic master of all crafts" width="200"/>

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
├── src/my_project/          # Python package
├── tests/                   # pytest test suite
├── notebooks/               # Jupyter notebook template
├── data/{raw,processed,staging,model_features}/
├── sql/                     # SQL linting config
├── pyproject.toml           # Dependencies (uv)
├── ruff.toml                # Linter & formatter config
├── Dockerfile               # Multi-stage Docker build
├── justfile                 # Task runner
├── .pre-commit-config.yaml  # Code quality hooks
├── .env-template            # Environment variables
└── README.md
```

**Stack**: Python 3.12, uv, DVC, Hydra, Ruff, pre-commit, pytest, Docker, SQLFluff

---

## Roadmap

Future skills planned for the `lugh` plugin:

- `eda-report` — Generate an EDA report from a CSV/parquet file
- `dvc-pipeline` — Scaffold a DVC pipeline with stages
- `model-card` — Generate a model card markdown template

---

## License

MIT
