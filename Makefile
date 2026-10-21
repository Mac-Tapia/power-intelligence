.PHONY: doctor test test-governance lint serve list-worktrees

PY ?= .venv/Scripts/python

doctor:
	$(PY) scripts/verify_structure.py

test:
	$(PY) -m pytest -q

test-governance:
	$(PY) -m pytest -q tests/governance

serve:
	$(PY) scripts/unitesis.py serve

list-worktrees:
	$(PY) scripts/dev/worktree.py list
