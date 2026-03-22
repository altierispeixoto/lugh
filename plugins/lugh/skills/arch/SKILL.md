---
name: arch
description: Use when the user wants to define, document, or review the MLOps infrastructure stack for an ML project. Guides through 12 stack layers (cloud, data, training, serving, orchestration, monitoring, CI/CD, etc.) and writes a structured architecture document. Works standalone or inside a lugh project. Covers the MLOps Engineering layer that underpins the CRISP-DM lifecycle.
argument-hint: (optional: project context or notes)
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Lugh: MLOps Architecture

Define and document the MLOps infrastructure stack for your ML project.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
```

If `pyproject.toml` is found, use NAME as the project name and write to `docs/mlops-architecture.md`.
If not found, ask the user for the project name and write `mlops-architecture.md` in the current directory.

Check if `specs/` directory exists and contains any files — if so, note that specs are available as context for architecture decisions.

### Step 2 — Guided conversation

Ask the following questions using AskUserQuestion, one at a time. For each layer, offer the listed options as suggestions but accept any answer.

1. **Cloud platform**: Where will this project run?
   Options: GCP · AWS · Azure · on-premise · cloud-agnostic · hybrid

2. **Data platform**: What is the primary data storage and query layer?
   Options: BigQuery · Snowflake · Redshift · Databricks · DuckDB + object storage · PostgreSQL · other

3. **Data versioning**: How will data and model artifacts be versioned?
   Options: DVC · Delta Lake · LakeFS · Pachyderm · cloud-native (S3 versioning / GCS) · none

4. **Training infrastructure**: Where will model training run?
   Options: Local machine · Cloud VMs (EC2/Compute Engine) · Vertex AI Training · SageMaker · Azure ML · Kubeflow · custom Kubernetes · Databricks

5. **Experiment tracking**: How will experiments be logged and compared?
   Options: MLflow · Weights & Biases · Neptune · Comet · Vertex AI Experiments · DVC Experiments · none

6. **Model registry**: Where will trained models be stored and versioned?
   Options: MLflow Model Registry · Vertex AI Model Registry · SageMaker Model Registry · W&B Artifacts · Hugging Face Hub · custom object storage · none

7. **Feature store**: Is a feature store needed?
   Options: Feast · Vertex AI Feature Store · Tecton · Hopsworks · none (features computed at training time)

8. **Model serving**: How will models be deployed for inference?
   Options: FastAPI (self-hosted) · BentoML · Triton Inference Server · Ray Serve · Vertex AI Endpoints · SageMaker Endpoints · KServe · batch only (no online serving)

9. **Pipeline orchestration**: How will the ML pipeline be orchestrated?
   Options: Airflow · Prefect · Kubeflow Pipelines · Vertex AI Pipelines · Metaflow · Dagster · ZenML · GitHub Actions · DVC (repro) · none

10. **Monitoring**: How will model and data quality be monitored in production?
    Options: Evidently · WhyLogs · Arize · Grafana + Prometheus · Vertex AI Model Monitoring · SageMaker Model Monitor · custom · none

11. **CI/CD**: What CI/CD system will automate testing and deployment?
    Options: GitHub Actions · GitLab CI · Jenkins · Cloud Build · Azure DevOps · CircleCI · none

12. **Container registry**: Where will Docker images be stored?
    Options: GCR (Google Container Registry) · ECR (AWS) · ACR (Azure) · Docker Hub · GitHub Container Registry · self-hosted

### Step 3 — Write architecture document

Create the `docs/` directory if it doesn't exist.

Write `docs/mlops-architecture.md` (or `mlops-architecture.md` if outside a project):

```markdown
# MLOps Architecture: NAME

**Date:** YYYY-MM-DD

---

## Platform

**Cloud:** [Q1]

---

## Data Layer

**Warehouse / Query Engine:** [Q2]
**Data Versioning:** [Q3]

---

## Training

**Infrastructure:** [Q4]
**Experiment Tracking:** [Q5]

---

## Model Registry

[Q6]

---

## Feature Store

[Q7]

---

## Serving

**Online Inference:** [Q8]

---

## Orchestration

[Q9]

---

## Monitoring

[Q10]

---

## CI/CD

[Q11]

---

## Container Registry

[Q12]

---

## Architecture Decisions

Key decisions are documented as Architecture Decision Records (ADRs).
See `docs/adr/` for individual records.

Run `/lugh:adr <decision-slug>` to document a specific architecture choice.
```

### Step 4 — Print summary

```
✔ Architecture document: docs/mlops-architecture.md

Next step → /lugh:data-profile <data-source>
  Profile your data source to understand schema, distributions, and quality.

To document individual decisions → /lugh:adr <decision-slug>
  Example: /lugh:adr use-mlflow-for-experiment-tracking
```
