.PHONY: doctor inventory test test-governance lint serve list-worktrees

PY ?= .venv/Scripts/python

doctor:
	$(PY) scripts/verify_structure.py

inventory:
	$(PY) scripts/dev/project_inventory.py --root . --output local-data/diagnostics/inventory.json

test:
	$(PY) -m pytest -q

test-governance:
	$(PY) -m pytest -q tests/governance

serve:
	$(PY) scripts/unitesis.py serve

list-worktrees:
	$(PY) scripts/dev/worktree.py list
