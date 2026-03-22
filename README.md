<div align="center">
  <img src="assets/lugh.jpg" alt="Lugh" width="180"/>

  <h1>Lugh</h1>

  <p><strong>Claude Code skills for the full data science and machine learning lifecycle</strong></p>

  <p>
    <a href="https://github.com/altierispeixoto/lugh/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
    <a href="https://github.com/anthropics/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-plugin-blueviolet" alt="Claude Code"></a>
    <a href="https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining"><img src="https://img.shields.io/badge/CRISP--DM-lifecycle-orange" alt="CRISP-DM"></a>
    <a href="https://github.com/altierispeixoto/lugh"><img src="https://img.shields.io/badge/MLOps-architecture-green" alt="MLOps"></a>
  </p>

  <p><em>Named after Lugh, the Celtic god of craftsmanship — master of all skills and arts.</em></p>
</div>

---

## Overview

Lugh is a [Claude Code](https://github.com/anthropics/claude-code) plugin that provides AI-assisted skills covering the complete data science and ML engineering lifecycle — from initial scaffolding through production deployment.

Skills are organized across two layers:

- **CRISP-DM lifecycle** — structured phases from business understanding through deployment
- **MLOps Engineering** — infrastructure, architecture decisions, and operational tooling

The stack integrates `uv`, `DuckDB`, `DVC`, `Hydra`, `Marimo`, `FastAPI`, and `Docker`.

---

## Installation

```bash
# Add the marketplace
claude plugins marketplace add altierispeixoto/lugh

# Install the plugin
claude plugins add lugh lugh
```

---

## Lifecycle

Skills are designed to be used in sequence inside a project created by `lugh:new-ds-project`. Run `/lugh:next` at any point to see your current phase and what to do next.

```
  scaffold → spec → arch → data-profile → experiment → model-card → ml-api
                      ↑
              /lugh:adr available at any phase to document decisions
```

| Phase | Skill | Description |
|-------|-------|-------------|
| Setup | `new-ds-project` | Scaffold a production-ready DS project |
| Business Understanding | `spec` | Define scope, success metrics, and key decisions |
| MLOps Architecture | `arch` | Define the infrastructure and tooling stack |
| Data Understanding | `data-profile` | EDA notebook + data dictionary |
| Modeling | `experiment` | Git branch + params update + experiment log |
| Evaluation | `model-card` | Document a trained model for governance and handoff |
| Deployment | `ml-api` | Scaffold a FastAPI serving endpoint |
| Utility (any phase) | `adr` | Architecture Decision Record (MADR format) |
| Navigator | `next` | Show lifecycle status and recommend the next step |

---

## Skills

### `lugh:new-ds-project` — Project Scaffold

Bootstrap a production-ready data science repository in seconds.

```bash
/lugh:new-ds-project <project-name>
```

**What gets created:**

```
my-project/
├── src/my_project/           # Python package with typed entrypoint
├── tests/                    # pytest suite
├── notebooks/                # Marimo reactive notebook template
├── conf/                     # Hydra configuration
├── data/{raw,processed,staging,model_features}/
├── models/                   # DVC-tracked model artifacts
├── experiments/              # Experiment logs
├── specs/                    # Project specs (created by lugh:spec)
├── docs/                     # Architecture docs and ADRs (created by lugh:arch / lugh:adr)
├── sql/                      # SQLFluff configuration
├── dvc.yaml                  # Pipeline: prepare → featurize → train → evaluate
├── params.yaml               # Experiment parameters
├── pyproject.toml            # uv-managed dependencies
├── ruff.toml                 # Linter and formatter
├── Dockerfile                # Multi-stage production image
├── justfile                  # Task runner
├── .github/workflows/ci.yml  # GitHub Actions (pytest + ruff + mypy)
├── .pre-commit-config.yaml   # Code quality hooks
└── .env-template             # Environment variable template
```

**Stack:** Python 3.12 · uv · DuckDB · DVC · Hydra · Marimo · Ruff · mypy · pre-commit · pytest · Docker · SQLFluff · GitHub Actions

---

### `lugh:next` — Lifecycle Navigator

See where you are in the project lifecycle and get a concrete recommendation.

```bash
/lugh:next
```

Inspects the project for phase completion signals and prints a status board:

```
Project: my-project

✔ new-ds-project    scaffolded
✔ lugh:spec         specs/2026-03-23-customer-churn/ found
○ lugh:arch         docs/mlops-architecture.md not found
○ lugh:data-profile no EDA notebooks found yet

➡ Recommended next step:
   /lugh:arch
   Define your MLOps infrastructure stack before working with data.
```

---

### `lugh:spec` — Project Specification

*CRISP-DM: Business Understanding*

Define the problem, success criteria, and key decisions before touching data.

```bash
/lugh:spec <spec-name>
```

Guides you through a structured conversation and writes to `specs/YYYY-MM-DD-<name>/`:

| File | Contents |
|------|----------|
| `plan.md` | Problem statement, data sources, scope |
| `success-metrics.md` | Business and technical success criteria |
| `decisions.md` | Constraints, trade-offs, open questions |

---

### `lugh:arch` — MLOps Architecture

*MLOps Engineering: Infrastructure & Platform*

Define and document the MLOps infrastructure stack for your project.

```bash
/lugh:arch
```

Guided conversation across 12 stack layers — cloud platform, data warehouse, data versioning, training infrastructure, experiment tracking, model registry, feature store, model serving, pipeline orchestration, monitoring, CI/CD, and container registry.

Writes `docs/mlops-architecture.md` with every layer documented and a pointer to ADRs for individual decisions.

---

### `lugh:adr` — Architecture Decision Record

*Utility: any phase*

Document a specific architecture or technology choice using the [MADR](https://adr.github.io/madr/) standard.

```bash
/lugh:adr <decision-slug>
```

Auto-increments ADR number by scanning `docs/adr/`. Guided conversation covering context, decision, alternatives considered, rationale, and consequences (positive and trade-offs). Writes `docs/adr/NNNN-<slug>.md`.

---

### `lugh:data-profile` — Data Understanding

*CRISP-DM: Data Understanding*

Explore any data source and generate EDA and documentation in one pass.

```bash
/lugh:data-profile <source>
```

**Supported sources:**

| Format | Example |
|--------|---------|
| CSV | `data/raw/customers.csv` |
| Parquet | `data/raw/features.parquet` |
| DuckDB | `data/raw/store.duckdb::orders` |
| SQL database | `postgresql://user:pass@host/db::SELECT * FROM orders` |

Uses DuckDB as the query engine throughout. Generates:

- **`notebooks/eda-<source>.py`** — Marimo notebook with schema, missing values, distributions, correlations, outlier detection, and cardinality analysis
- **`docs/data-dictionary-<source>.md`** — Column reference table pre-populated with names and types, ready for business definitions

---

### `lugh:experiment` — Experiment Tracking

*CRISP-DM: Modeling*

Set up a reproducible ML experiment that complements git and DVC — no duplicate code.

```bash
/lugh:experiment <experiment-name>
```

1. Creates a git branch `experiment/<name>` for code isolation
2. Guides you through parameter changes and updates `params.yaml`
3. Writes `experiments/<name>.md` — a lightweight log (hypothesis, changed parameters, results, conclusions)
4. Prints the `dvc repro` command to run

---

### `lugh:model-card` — Model Documentation

*CRISP-DM: Evaluation*

Document a trained model for governance, team handoff, and deployment readiness.

```bash
/lugh:model-card <model-name>
```

Follows the [Google Model Card](https://modelcards.withgoogle.com/about) standard. Guided conversation covering intended use, training data, evaluation metrics (overall and per-slice), limitations, and ethical considerations. Writes `models/<model-name>/model-card.md`.

---

### `lugh:ml-api` — Model Serving

*CRISP-DM: Deployment*

Scaffold a production-ready REST API for model serving.

```bash
/lugh:ml-api <model-name>
```

Generates inside `src/<package>/api/`:

| File | Description |
|------|-------------|
| `app.py` | FastAPI app with `/predict`, `/health`, `/info` |
| `schemas.py` | Pydantic request/response models |
| `model_loader.py` | Model loading with env-var path configuration |

Also writes a `docker-compose.yml` at the project root for local testing.

---

## Requirements

- [Claude Code](https://github.com/anthropics/claude-code) CLI
- All lifecycle skills require a project created by `lugh:new-ds-project`

---

## License

[MIT](LICENSE)
