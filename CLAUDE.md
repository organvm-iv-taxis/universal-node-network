# CLAUDE.md — universal-node-network

**ORGAN IV** (Orchestration) · `organvm-iv-taxis/universal-node-network`
**Status:** ACTIVE · **Branch:** `main`

## What This Repo Is

Distributed node network infrastructure for decentralized systems

## Stack

**Languages:** Python
**Build:** Python (pip/setuptools)
**Testing:** pytest (likely)

## Directory Structure

```
📁 .github/
📁 docs/
    adr
📁 src/
    __init__.py
    discovery.py
    network.py
    node.py
📁 tests/
    __init__.py
    test_network.py
    test_node.py
  .gitignore
  CHANGELOG.md
  LICENSE
  README.md
  pyproject.toml
  seed.yaml
```

## Key Files

- `README.md` — Project documentation
- `pyproject.toml` — Python project config
- `seed.yaml` — ORGANVM orchestration metadata
- `src/` — Main source code
- `tests/` — Test suite

## Development

```bash
pip install -e .    # Install in development mode
pytest              # Run tests
```

## ORGANVM Context

This repository is part of the **ORGANVM** eight-organ creative-institutional system.
It belongs to **ORGAN IV (Orchestration)** under the `organvm-iv-taxis` GitHub organization.

**Registry:** [`registry-v2.json`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/registry-v2.json)
**Corpus:** [`organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm)

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-IV (Orchestration) | **Tier:** standard | **Status:** LOCAL
**Org:** `organvm-iv-taxis` | **Repo:** `universal-node-network`

### Edges
- **Produces** → `all`: Governance policy and node network infrastructure
- **Consumes** ← `META-ORGANVM`: Registry data for orchestration

### Siblings in Orchestration
`orchestration-start-here`, `petasum-super-petasum`, `.github`, `agentic-titan`, `agent--claude-smith`, `a-i--skills`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-02-24T01:01:15Z*
<!-- ORGANVM:AUTO:END -->
