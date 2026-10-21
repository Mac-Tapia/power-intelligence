"""ADR-0010 guard: the core runtime never imports or drives CYME/PowerFactory APIs."""

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIRS = ("packages", "apps", "scripts", "tools", "workers")
FORBIDDEN_MODULES = {"cympy", "powerfactory", "win32com", "comtypes", "pythoncom"}
FORBIDDEN_CALLS = re.compile(r"\b(ComLdf|ComShc|GetApplicationExt|GetApplication|cympy\.\w+)\s*\(")


def runtime_python_files():
    for top in RUNTIME_DIRS:
        for path in sorted((ROOT / top).rglob("*.py")):
            if "__pycache__" not in path.parts:
                yield path


def imported_roots(tree: ast.AST) -> set[str]:
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
        elif (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "__import__"
              and node.args and isinstance(node.args[0], ast.Constant)):
            roots.add(str(node.args[0].value).split(".")[0])
    return roots


class NoProprietaryEnginesTest(unittest.TestCase):
    def test_runtime_has_python_files(self):
        self.assertGreater(len(list(runtime_python_files())), 20)

    def test_no_forbidden_imports_or_calls(self):
        offenders = []
        for path in runtime_python_files():
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            bad = imported_roots(ast.parse(text)) & FORBIDDEN_MODULES
            if bad:
                offenders.append(f"{rel}: imports {sorted(bad)}")
            for match in FORBIDDEN_CALLS.finditer(text):
                offenders.append(f"{rel}: calls {match.group(1)}")
        self.assertEqual(offenders, [])

    def test_detector_catches_violations(self):
        tree = ast.parse("import cympy\nfrom powerfactory import x\n__import__('win32com')")
        self.assertEqual(
            imported_roots(tree) & FORBIDDEN_MODULES, {"cympy", "powerfactory", "win32com"}
        )
        self.assertIsNotNone(FORBIDDEN_CALLS.search("ldf = app.ComLdf()"))
        self.assertIsNotNone(FORBIDDEN_CALLS.search("app = GetApplication()"))
        self.assertIsNone(FORBIDDEN_CALLS.search("def complex_load(): pass"))


if __name__ == "__main__":
    unittest.main()
