# Models

Trained model artifacts are tracked with DVC, not stored in git.

## Adding a model

```bash
dvc add models/model.pkl
git add models/model.pkl.dvc .gitignore
git commit -m "feat: add trained model v1.0"
dvc push
```

## Model Cards

Document each production model below:

### model.pkl

- **Version:**
- **Trained:**
- **Dataset:**
- **Metrics:**
- **Notes:**
