# Contributing Guidelines

Thank you for your interest in contributing to __TITLE__!

## Getting Started

```bash
git clone git@github.com:your-username/__NAME__.git
cd __NAME__
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

## Development Workflow

1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make changes following our coding standards (type hints, Google docstrings, ruff)
3. Run tests and linting:
   ```bash
   just test
   just lint
   just format
   ```
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: your descriptive commit message"
   ```
5. Open a Pull Request

## Data Science Guidelines

- **Notebooks**: Use marimo; notebooks are `.py` files and version-control cleanly
- **Models**: Version with DVC; include model cards in `models/README.md`
- **Experiments**: Log with MLflow; document configs in `params.yaml`
- **Data**: Never commit raw data — use `dvc add` + `dvc push`

## Questions?

Open an issue for bug reports, feature requests, or questions.
