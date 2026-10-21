.PHONY: doctor test list-worktrees

doctor:
	python scripts/verify_structure.py

test:
	python -m unittest discover -s tests/bootstrap -v

list-worktrees:
	python scripts/dev/worktree.py list
