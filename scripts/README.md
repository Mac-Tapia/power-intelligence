# Local development helpers

`scripts/verify_structure.py` and `scripts/dev/worktree.py` run on Python stdlib. The latter calls installed Git; no hidden resets, force deletes or branch pruning.

Future scripts must have documentation, explicit dry-run where they can destroy data, timeouts and unit tests. Do not store credentials inside scripts.
