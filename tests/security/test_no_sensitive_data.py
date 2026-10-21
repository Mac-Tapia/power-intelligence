"""AC-029-07: customer values, identifiers and local data never enter Git.

Uses structural patterns only (real names or values must not be written into this test).
"""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".py", ".md", ".json", ".csv", ".txt", ".yml", ".yaml", ".toml", ".html",
                 ".js", ".css", ".sql", ".mdc"}
PATTERNS = {
    "real CYME customer id": re.compile(r"\bCUST_\d{4}_\d{5,}"),
    "Peruvian RUC": re.compile(r"\b(?:10|20)\d{9}\b"),
    "billing amount column": re.compile(r"TotalFacturado\s*[:=,]\s*\d"),
    "e-mail address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
}
ALLOWED_EMAILS = {"noreply@anthropic.com", "copilot@github.com"}


def tracked_files() -> list[Path]:
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True,
                             check=True, timeout=60).stdout.decode("utf-8")
        return [ROOT / p for p in out.split("\0") if p]
    except (OSError, subprocess.SubprocessError):
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts
                and ".venv" not in p.parts and "local-data" not in p.parts]


class NoSensitiveDataTest(unittest.TestCase):
    def test_local_data_is_never_tracked(self):
        rels = [p.relative_to(ROOT).as_posix() for p in tracked_files()]
        self.assertEqual([r for r in rels if r.startswith("local-data/")], [])

    def test_no_sensitive_patterns_in_tracked_text(self):
        findings = []
        for path in tracked_files():
            if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
                continue
            if path.name == Path(__file__).name:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for label, pattern in PATTERNS.items():
                for match in pattern.finditer(text):
                    if label == "e-mail address" and match.group(0) in ALLOWED_EMAILS:
                        continue
                    findings.append(f"{path.relative_to(ROOT).as_posix()}: {label}")
                    break
        self.assertEqual(findings, [])

    def test_detectors_work(self):
        self.assertTrue(PATTERNS["real CYME customer id"].search("x,CUST_2010_962871_SE21161"))
        self.assertTrue(PATTERNS["Peruvian RUC"].search("RUC 20123456789"))
        self.assertFalse(PATTERNS["real CYME customer id"].search("C1,Otro"))


if __name__ == "__main__":
    unittest.main()
