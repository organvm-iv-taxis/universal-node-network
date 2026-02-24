# Contributing to universal-node-network

Thank you for your interest in contributing to universal-node-network.

## Getting Started

This repository is part of **ORGAN-IV (Orchestration)** in the ORGANVM system. For organization-wide contribution guidelines, see the [`.github` repository](https://github.com/organvm-iv-taxis/.github/blob/main/CONTRIBUTING.md).

## Development

```bash
cd universal-node-network
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## Pull Requests

- Branch from `main` using `feature/your-feature` or `fix/your-fix`
- Follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`
- Ensure tests pass before submitting
- Keep commits atomic and focused
