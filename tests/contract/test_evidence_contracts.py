"""Real evidence payloads validate against the versioned JSON contracts (I03/I04).

A deliberately small stdlib validator covers the keywords used by these schemas
(type, const, enum, required, properties, items, minItems, minLength, pattern), so the
check runs without third-party packages. Unknown keywords fail loudly instead of being
silently ignored.
"""

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_application.alternatives import run_conductor_alternatives  # noqa: E402
from unitesis_application.study import run_new_load_study, run_study  # noqa: E402
from unitesis_application.unbalanced_study import run_unbalanced_study  # noqa: E402
from unitesis_simulation import RadialBFSEngine  # noqa: E402

SCHEMAS = ROOT / "contracts/schemas/json"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"
_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
_KNOWN = {"$schema", "$id", "title", "description", "type", "const", "enum", "required",
          "properties", "items", "minItems", "minLength", "pattern"}


def _is_type(value, name):
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, _TYPES[name])


def validate(value, schema, path="$"):
    unknown = set(schema) - _KNOWN
    if unknown:
        raise AssertionError(f"{path}: validator does not support {sorted(unknown)}")
    errors = []
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(value, t) for t in types):
            return [f"{path}: expected {types}, got {type(value).__name__}"]
    if "const" in schema and (value != schema["const"] or type(value) is not type(schema["const"])):
        errors.append(f"{path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(value, dict):
        errors += [f"{path}: missing {k}" for k in schema.get("required", []) if k not in value]
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors += validate(value[key], sub, f"{path}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                errors += validate(item, schema["items"], f"{path}[{i}]")
    return errors


def load(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class _SecondBFS(RadialBFSEngine):
    name = "second-bfs-reference"


class EvidenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = Path(cls.tmp.name)
        ref = _SecondBFS()
        cls.study = run_study(FEEDER, out / "s.json", reference=ref)
        cls.new_load = run_new_load_study(FEEDER, out / "n.json", load_id="NL", bus="B3",
                                          p_mw=0.5, q_mvar=0.1, reference=ref)
        cls.alternatives = run_conductor_alternatives(
            FEEDER, out / "a.json", line_id="L13",
            catalog_path=ROOT / "config/catalogs/conductors/aaac6201_nexans_reference.json",
            basis_path=ROOT / "fixtures/economics/conductor_alternatives_synthetic.json",
            operating_temperature_c=75.0, phase_gmd_m=1.2, reference=ref)
        cls.unbalanced = run_unbalanced_study(
            ROOT / "fixtures/networks/ieee13_kersting.json", out / "u.json")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_payloads_match_their_contracts(self):
        cases = {"study-evidence.v1.schema.json": self.study,
                 "new-load-evidence.v1.schema.json": self.new_load,
                 "alternatives-evidence.v1.schema.json": self.alternatives,
                 "unbalanced-study-evidence.v1.schema.json": self.unbalanced}
        for name, payload in cases.items():
            with self.subTest(schema=name):
                self.assertEqual(validate(payload, load(name)), [])

    def test_contract_rejects_acceptance_and_bad_digests(self):
        schema = load("study-evidence.v1.schema.json")
        tampered = json.loads(json.dumps(self.study))
        tampered["technical_acceptance"] = True
        tampered["snapshot_sha256"] = "XYZ"
        tampered["comparison"]["status"] = "ok"
        del tampered["limitations"]
        errors = "\n".join(validate(tampered, schema))
        for fragment in ("technical_acceptance", "snapshot_sha256", "comparison.status",
                         "missing limitations"):
            self.assertIn(fragment, errors)

    def test_truthy_strings_are_not_booleans(self):
        schema = load("alternatives-evidence.v1.schema.json")
        tampered = json.loads(json.dumps(self.alternatives))
        tampered["alternatives"][0]["technical_feasible"] = "false"
        self.assertTrue(validate(tampered, schema))

    def test_validator_refuses_unknown_keywords(self):
        with self.assertRaises(AssertionError):
            validate({}, {"oneOf": []})


if __name__ == "__main__":
    unittest.main()
