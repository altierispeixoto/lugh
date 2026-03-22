---
name: ml-api
description: Use when the user wants to serve a trained model as a REST API. Scaffolds a FastAPI application with predict, health, and info endpoints inside the project's source package. Must be run from inside a project created by lugh:new-ds-project. Covers the Model Serving phase of the ML lifecycle.
argument-hint: <model-name>
allowed-tools: [Bash, Write]
---

# Lugh: ML API

Scaffold a FastAPI serving endpoint for a trained model.

## Instructions

### Step 1 — Detect project context

```bash
NAME=$(grep '^name = ' pyproject.toml 2>/dev/null | head -1 | sed 's/name = "\(.*\)"/\1/')
PACKAGE=$(grep -A1 '\[project.scripts\]' pyproject.toml 2>/dev/null | tail -1 | cut -d'"' -f1 | tr -d ' ')
```

If `pyproject.toml` not found, stop with: "Run /lugh:ml-api from the root of a lugh project."

Extract `<model-name>` from the argument. If none, ask the user.

Check if `models/<model-name>/model-card.md` exists. If not, warn: "No model card found for <model-name>. Consider running /lugh:model-card first."

### Step 2 — Write API files

Create `src/PACKAGE/api/` directory.

**`src/PACKAGE/api/__init__.py`** — empty

**`src/PACKAGE/api/schemas.py`**
```python
"""Request and response schemas for the MODEL_NAME API."""

from pydantic import BaseModel, Field
from typing import Any


class PredictRequest(BaseModel):
    """Input features for prediction."""
    # TODO: replace with your actual feature fields
    features: dict[str, Any] = Field(..., description="Feature dictionary")


class PredictResponse(BaseModel):
    """Prediction output."""
    prediction: Any = Field(..., description="Model prediction")
    probability: float | None = Field(None, description="Confidence score (if applicable)")
    model_name: str
    model_version: str
```

**`src/PACKAGE/api/model_loader.py`**
```python
"""Model loading utilities."""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_model = None
MODEL_NAME = "MODEL_NAME"
MODEL_VERSION = "1.0.0"


def load_model():
    """Load the model from the path specified in MODEL_PATH env var."""
    global _model
    if _model is not None:
        return _model

    model_path = os.getenv("MODEL_PATH", f"models/{MODEL_NAME}/model.pkl")
    path = Path(model_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Set the MODEL_PATH environment variable or run `dvc pull`."
        )

    import joblib
    _model = joblib.load(path)
    logger.info("Model loaded from %s", model_path)
    return _model


def get_model():
    """FastAPI dependency: return loaded model."""
    return load_model()
```

**`src/PACKAGE/api/app.py`**
```python
"""FastAPI application for MODEL_NAME serving."""

from fastapi import FastAPI, Depends, HTTPException
from .schemas import PredictRequest, PredictResponse
from .model_loader import get_model, MODEL_NAME, MODEL_VERSION

app = FastAPI(
    title="NAME — MODEL_NAME API",
    description="REST API for MODEL_NAME predictions",
    version=MODEL_VERSION,
)


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/info")
def info() -> dict:
    """Model metadata."""
    return {"model_name": MODEL_NAME, "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest, model=Depends(get_model)) -> PredictResponse:
    """Run model inference on input features."""
    try:
        # TODO: adapt feature extraction to your model's expected input format
        import pandas as pd
        features = pd.DataFrame([request.features])
        prediction = model.predict(features)[0]
        probability = None
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(features)[0].max())
        return PredictResponse(
            prediction=prediction,
            probability=probability,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
```

Replace `MODEL_NAME` with `<model-name>` and `NAME` with `NAME` and `PACKAGE` with `PACKAGE` throughout.

### Step 3 — Write docker-compose.yml at project root

**`docker-compose.yml`**
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=models/MODEL_NAME/model.pkl
    volumes:
      - ./models:/app/models:ro
    command: ["uvicorn", "PACKAGE.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Replace `MODEL_NAME` and `PACKAGE` with actual values.

### Step 4 — Add fastapi and uvicorn to pyproject.toml

Check if `fastapi` and `uvicorn` are in `pyproject.toml`. If not, add them to a new `[project.optional-dependencies]` group called `api`:
```toml
api = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "joblib>=1.3.0",
]
```

### Step 5 — Print summary

```
✔ API scaffolded:
    src/PACKAGE/api/
    ├── __init__.py
    ├── app.py
    ├── model_loader.py
    └── schemas.py
  docker-compose.yml

Install API dependencies:
  uv sync --extra api

Run locally:
  uv run uvicorn PACKAGE.api.app:app --reload

Or with Docker:
  docker compose up

API docs available at: http://localhost:8000/docs

Next step → /lugh:monitor <model-name>
  Set up drift detection and production monitoring for the deployed model.
```
