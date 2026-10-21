"""Structural contract syntax checks; not numerical simulation tests."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

class ContractsTests(unittest.TestCase):
    def test_study_run_schema_declares_required_fields(self):
        src=ROOT / "contracts/schemas/json/study-run.schema.json"
        schema=json.loads(src.read_text(encoding="utf-8"))
        self.assertEqual(schema["type"], "object")
        self.assertIn("snapshot_sha256", schema["required"])
        self.assertIn("converged", schema["required"])

if __name__ == "__main__":
    unittest.main()
