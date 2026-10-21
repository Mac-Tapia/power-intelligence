"""Durable jobs, atomic claims and terminal integrity over real SQLite files."""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/python/power-adapters/src"))


def test_reopen_and_terminal_immutability(tmp_path):
    from unitesis_adapters.job_repository import SqliteJobRepository

    path = tmp_path / "jobs.sqlite"
    repo = SqliteJobRepository(path)
    request = {"snapshot_sha256": "a" * 64, "scenario_id": "base"}
    repo.enqueue("j", "study", request)
    with pytest.raises(ValueError):
        repo.finish("j", {})
    assert repo.claim("j")
    repo.finish("j", {"comparison": "passed", "result_sha256": ["b" * 64]})
    repo.close()
    reopened = SqliteJobRepository(path)
    assert reopened.get("j")["request"] == request
    assert reopened.get("j")["comparison"] == "passed"
    assert reopened.enqueue("j", "study", request)["status"] == "finished"
    with pytest.raises(ValueError):
        reopened.fail("j", "execution_failed")
    with pytest.raises(ValueError):
        reopened.enqueue("j", "study", {"other": True})
    with pytest.raises(ValueError):
        reopened.finish("j", {})
    with pytest.raises(KeyError):
        reopened.get("unknown")
    reopened.close()


def test_claim_atomic_and_recovery_only_running(tmp_path):
    from unitesis_adapters.job_repository import SqliteJobRepository

    path = tmp_path / "jobs.sqlite"
    a, b = SqliteJobRepository(path), SqliteJobRepository(path)
    a.enqueue("j", "study", {})
    a.enqueue("q", "study", {})
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(lambda r: r.claim("j"), [a, b]))
    assert sorted(results) == [False, True]
    assert a.recover_interrupted() == 1
    assert a.get("j")["error_code"] == "interrupted"
    assert a.get("q")["status"] == "queued"
    assert a.recover_interrupted() == 0
    a.close()
    b.close()


def test_rejects_nonfinite_and_reserved_outcome_fields(tmp_path):
    from unitesis_adapters.job_repository import SqliteJobRepository

    repo = SqliteJobRepository(tmp_path / "jobs.sqlite")
    with pytest.raises(ValueError):
        repo.enqueue("bad", "study", {"p": float("nan")})
    repo.enqueue("j", "study", {})
    assert repo.claim("j")
    with pytest.raises(ValueError):
        repo.finish("j", {"status": "queued"})
    with pytest.raises(ValueError):
        repo.fail("j", "secret-token-value")
    repo.fail("j", "execution_failed")
    assert "secret" not in str(repo.get("j"))
    repo.close()
