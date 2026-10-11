"""Static public schema and fixture contracts for P07 W10."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.lib.ops import root_resource_assessment as assessment

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "infra/09-platform-ops/resource-optimization"
SCHEMA = CONTRACT / "measurement.schema.json"
FIXTURES = CONTRACT / "fixtures"


def _unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON field")
        value[key] = item
    return value


class RootResourceContractTests(unittest.TestCase):
    def test_tracked_fixtures_produce_exact_blockers_and_cli_refusal(self) -> None:
        expected = {
            "idle-unknown.synthetic.json": [
                "SYNTHETIC_EVIDENCE",
                "UNKNOWN_FACTS",
                "IDLE_ONLY_LOWERING",
            ],
            "identity-budget-mismatch.synthetic.json": [
                "SYNTHETIC_EVIDENCE",
                "SOURCE_DEPLOYED_MISMATCH",
                "CONTRADICTORY_FACTS",
            ],
        }
        for name, blockers in expected.items():
            with self.subTest(name=name):
                path = FIXTURES / name
                output = assessment.evaluate_file(path)
                self.assertEqual("BLOCKED", output["status"])
                self.assertEqual(blockers, output["blockers"])
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                    output["input_sha256"],
                )
                self.assertTrue(output["synthetic"])
                self.assertFalse(output["runtime_acceptance"])
                self.assertFalse(output["mutation_authorized"])
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts/operations/root-resource-assessment.py"),
                        str(path),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertEqual(output, json.loads(result.stdout))
                self.assertEqual("", result.stderr)

    def test_schema_is_closed_offline_draft_2020_12(self) -> None:
        schema = json.loads(
            SCHEMA.read_text(encoding="utf-8"), object_pairs_hook=_unique
        )
        Draft202012Validator.check_schema(schema)

        self.assertEqual(
            "https://json-schema.org/draft/2020-12/schema", schema["$schema"]
        )
        refs: list[str] = []

        def collect(value: object) -> None:
            if isinstance(value, dict):
                refs.extend(item for key, item in value.items() if key == "$ref")
                for item in value.values():
                    collect(item)
            elif isinstance(value, list):
                for item in value:
                    collect(item)

        collect(schema)
        self.assertTrue(all(ref.startswith("#/") for ref in refs), refs)
        self.assertEqual(False, schema["additionalProperties"])

    def test_all_synthetic_fixtures_validate_and_cannot_claim_runtime_acceptance(
        self,
    ) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        fixtures = sorted(FIXTURES.glob("*.synthetic.json"))
        self.assertGreaterEqual(len(fixtures), 2)

        for path in fixtures:
            with self.subTest(path=path.name):
                document = json.loads(
                    path.read_text(encoding="utf-8"), object_pairs_hook=_unique
                )
                self.assertEqual([], list(validator.iter_errors(document)))
                self.assertEqual("synthetic", document["evidence_kind"])
                self.assertEqual("assessment_only", document["proposal"]["kind"])

    def test_schema_requires_complete_metric_and_budget_vocabulary(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        metrics = schema["$defs"]["metrics"]
        budgets = schema["$defs"]["budgets"]

        self.assertEqual(set(metrics["required"]), set(metrics["properties"]))
        self.assertEqual(set(budgets["required"]), set(budgets["properties"]))
        self.assertIn("resource_overhead_bytes", metrics["required"])
        self.assertIn("gpu_utilization_ratio", metrics["required"])
        self.assertIn("recovery_budget_seconds", budgets["required"])

    def test_metric_units_are_fixed_by_the_schema(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        fixture = json.loads(next(FIXTURES.glob("*.synthetic.json")).read_text())
        fixture["metrics"]["rss_bytes"]["unit"] = "count"

        self.assertFalse(Draft202012Validator(schema).is_valid(fixture))

    def test_contract_contains_no_fixed_service_count_or_external_reference(
        self,
    ) -> None:
        sources = [
            SCHEMA,
            ROOT / "scripts/lib/ops/root_resource_assessment.py",
            ROOT / "scripts/operations/root-resource-assessment.py",
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in sources)
        self.assertNotIn("service_count", text)
        self.assertNotIn("urlopen", text)
        self.assertNotIn("requests.", text)


if __name__ == "__main__":
    unittest.main()
