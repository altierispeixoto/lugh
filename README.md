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

## Workflow

Skills follow the CRISP-DM lifecycle. Run them in order inside a lugh project, or use `/lugh:next` to see where you are.

```
new-ds-project → spec → data-profile → experiment → model-card → ml-api
   scaffold        plan    understand     model &      document     deploy
                           data           iterate
```

---

## Available Skills

### `lugh:new-ds-project`

Scaffold a complete, production-ready data science project from scratch.

```
/lugh:new-ds-project <project-name>
```

Creates: Python package, Marimo notebooks, DVC pipeline, Hydra config, GitHub Actions CI, Docker, pre-commit, pytest, SQLFluff.

**Stack**: Python 3.12, uv, DuckDB, DVC, Hydra, Marimo, Ruff, mypy, pre-commit, pytest, Docker, SQLFluff, GitHub Actions

---

### `lugh:next`

Show project lifecycle status and recommend what to do next.

```
/lugh:next
```

Inspects the project directory and prints a status board of completed CRISP-DM phases.

---

### `lugh:spec`

Define scope and success criteria before writing code. *(CRISP-DM: Business Understanding)*

```
/lugh:spec <spec-name>
```

Guided conversation → creates `specs/YYYY-MM-DD-<name>/` with `plan.md`, `decisions.md`, `success-metrics.md`.

---

### `lugh:data-profile`

Understand a dataset before modeling. *(CRISP-DM: Data Understanding)*

```
/lugh:data-profile <source>
```

Accepts CSV, Parquet, DuckDB table, or SQL connection string. Generates a Marimo EDA notebook and a data dictionary.

---

### `lugh:experiment`

Set up a reproducible ML experiment. *(CRISP-DM: Modeling)*

```
/lugh:experiment <experiment-name>
```

Creates a git branch, updates `params.yaml`, and writes a lightweight experiment log. Works with DVC and git — no duplicate code.

---

### `lugh:model-card`

Document a trained model for governance and deployment. *(CRISP-DM: Evaluation)*

```
/lugh:model-card <model-name>
```

Guided conversation → `models/<model-name>/model-card.md` following the Google Model Card standard.

---

### `lugh:ml-api`

Serve a trained model as a REST API. *(CRISP-DM: Deployment)*

```
/lugh:ml-api <model-name>
```

Scaffolds FastAPI app with `/predict`, `/health`, `/info` endpoints inside the project package + `docker-compose.yml`.

---

## License

MIT
