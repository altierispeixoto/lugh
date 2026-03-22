# lugh plugin

Data science project scaffolding and workflow skills for Claude Code.
Skills follow the CRISP-DM lifecycle — from project setup through deployment.

## Workflow

```
/lugh:new-ds-project → /lugh:spec → /lugh:arch → /lugh:data-profile → /lugh:data-quality → /lugh:featurize
     scaffold              plan      infrastructure   understand data      validate rules      engineer features

→ /lugh:experiment → /lugh:eval → /lugh:model-card → /lugh:ml-api → /lugh:monitor
   model & iterate    evaluate      document            deploy          observe
```

Not sure where you are? Run `/lugh:next` from inside any lugh project.

## Skills

| Skill | Phase | Description |
|---|---|---|
| [`new-ds-project`](skills/new-ds-project/SKILL.md) | Setup | Scaffold a complete DS project structure |
| [`next`](skills/next/SKILL.md) | All | Show project lifecycle status and recommend next step |
| [`spec`](skills/spec/SKILL.md) | Business Understanding | Define scope, success metrics, and key decisions |
| [`arch`](skills/arch/SKILL.md) | MLOps Architecture | Define the infrastructure stack across 12 layers (cloud, serving, orchestration, monitoring, etc.) |
| [`adr`](skills/adr/SKILL.md) | Any | Document an architecture decision using the MADR standard |
| [`data-profile`](skills/data-profile/SKILL.md) | Data Understanding | EDA notebook + data dictionary from CSV, Parquet, DuckDB, or SQL |
| [`data-quality`](skills/data-quality/SKILL.md) | Data Preparation | Define validation rules and generate executable data quality checks |
| [`featurize`](skills/featurize/SKILL.md) | Data Preparation | Design feature engineering pipeline + populate featurize.py DVC stage |
| [`experiment`](skills/experiment/SKILL.md) | Modeling | Create git branch, update params, log experiment hypothesis |
| [`eval`](skills/eval/SKILL.md) | Evaluation | Structured evaluation: slice analysis, threshold selection, go/no-go report |
| [`model-card`](skills/model-card/SKILL.md) | Evaluation | Document a trained model following Google Model Card standard |
| [`ml-api`](skills/ml-api/SKILL.md) | Deployment | Scaffold FastAPI serving endpoint for a trained model |
| [`monitor`](skills/monitor/SKILL.md) | Production | Drift detection, prediction logging, monitoring dashboard + runbook |
