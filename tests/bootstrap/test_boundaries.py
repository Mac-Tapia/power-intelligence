"""Small architecture fitness check for the pure domain package."""
import ast
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOMAIN=ROOT / "packages/python/power-domain/src/unitesis_domain"
BANNED={"fastapi","sqlalchemy","torch","pandas","pandapower","opendss","geoalchemy2","django"}

class BoundaryTests(unittest.TestCase):
    def test_domain_has_no_infrastructure_imports(self):
        for path in DOMAIN.rglob("*.py"):
            tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
            imports=[]
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):
                    imports.extend(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node,ast.ImportFrom) and node.module:
                    imports.append(node.module.split(".")[0])
            self.assertFalse(BANNED.intersection(imports),f"Forbidden import in {path}")

if __name__ == "__main__":
    unittest.main()
