from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-agentic-audit-semantic-freshness.py"
CONTRACT = pathlib.Path("scripts/validation/agentic-audit-semantic-contract.json")
sys.path.insert(0, str(SCRIPT.parent))

spec = importlib.util.spec_from_file_location(
    "agentic_audit_semantic_freshness", SCRIPT
)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load semantic validator: {SCRIPT}")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class AgenticAuditSemanticFreshnessTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tempdir.name)
        self.contract_path = self.repo / CONTRACT
        contract = json.loads((ROOT / CONTRACT).read_text(encoding="utf-8"))

        required_paths = {
            pathlib.Path(contract["audit_index"]),
            pathlib.Path(contract["overview"]),
            pathlib.Path(contract["task_evidence"]),
            pathlib.Path(contract["canonical_pack"]) / "README.md",
            pathlib.Path(
                "docs/90.references/audits/"
                "2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md"
            ),
            CONTRACT,
        }
        required_paths.update(
            path.relative_to(ROOT)
            for path in (ROOT / contract["canonical_pack"]).glob("*.md")
        )
        for assertion in contract["assertions"]:
            required_paths.add(pathlib.Path(assertion["report"]))
            required_paths.update(
                pathlib.Path(path) for path in assertion["required_evidence_paths"]
            )

        for relative_path in sorted(required_paths):
            destination = self.repo / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative_path, destination)

        self.contract = json.loads(self.contract_path.read_text(encoding="utf-8"))
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_contract(self) -> None:
        self.contract_path.write_text(
            json.dumps(self.contract, indent=2) + "\n", encoding="utf-8"
        )

    def assertion(self, criterion_id: str) -> dict[str, object]:
        return next(
            assertion
            for assertion in self.contract["assertions"]
            if assertion["criterion_id"] == criterion_id
        )

    def report_path(self, criterion_id: str) -> pathlib.Path:
        return self.repo / str(self.assertion(criterion_id)["report"])

    def rewrite_row(self, criterion_id: str, old: str, new: str) -> None:
        path = self.report_path(criterion_id)
        text = path.read_text(encoding="utf-8")
        line = next(
            line for line in text.splitlines() if line.startswith(f"| {criterion_id} |")
        )
        self.assertIn(old, line)
        path.write_text(
            text.replace(line, line.replace(old, new, 1), 1), encoding="utf-8"
        )

    def append_to_report(self, criterion_id: str, text: str) -> None:
        path = self.report_path(criterion_id)
        path.write_text(
            path.read_text(encoding="utf-8") + f"\n{text}\n", encoding="utf-8"
        )

    def assert_failure(self, *expected_text: str) -> None:
        with self.assertRaises(module.AuditSemanticContractError) as context:
            module.validate_semantics(self.repo, CONTRACT)
        rendered = "\n".join(context.exception.errors)
        for expected in expected_text:
            self.assertIn(expected, rendered)

    def test_current_repository_contract_passes(self) -> None:
        result = module.validate_semantics(ROOT, CONTRACT)
        self.assertEqual(11, result.assertion_count)

    def test_wrong_required_state_fails(self) -> None:
        self.rewrite_row("QAF-12", "Implemented", "Missing")
        self.assert_failure("QAF-12", "required state Implemented")

    def test_missing_required_evidence_fails(self) -> None:
        path = self.repo / "scripts/validation/run-agent-precommit-all-files.sh"
        path.unlink()
        self.assert_failure("QAF-12", "required tracked evidence")

    def test_untracked_required_evidence_fails(self) -> None:
        path = self.repo / "untracked-evidence.txt"
        path.write_text("not in the index\n", encoding="utf-8")
        self.assertion("QAF-12")["required_evidence_paths"] = ["untracked-evidence.txt"]
        self.write_contract()
        self.assert_failure("QAF-12", "required tracked evidence")

    def test_completed_task_described_as_future_fails(self) -> None:
        self.append_to_report("QAF-12", "Task 9 will add wrapper")
        self.assert_failure("QAF-12", "forbidden stale phrase")

    def test_missing_completed_task_id_fails(self) -> None:
        task_path = self.repo / self.contract["task_evidence"]
        text = task_path.read_text(encoding="utf-8")
        task_path.write_text(text.replace("T-AER-009", "T-AER-X09"), encoding="utf-8")
        self.assert_failure("QAF-12", "completed task T-AER-009")

    def test_wrong_lifecycle_heading_fails(self) -> None:
        path = self.repo / self.contract["audit_index"]
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("## Canonical Current Audit", "## Current References"),
            encoding="utf-8",
        )
        self.assert_failure("audit index", "required heading")

    def test_non_active_canonical_readme_fails(self) -> None:
        path = self.repo / self.contract["canonical_pack"] / "README.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("status: active", "status: superseded", 1), encoding="utf-8"
        )
        self.assert_failure("canonical README", "status: active")

    def test_non_superseded_2026_07_07_readme_fails(self) -> None:
        path = self.repo / (
            "docs/90.references/audits/"
            "2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md"
        )
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("status: superseded", "status: active", 1), encoding="utf-8"
        )
        self.assert_failure("2026-07-07 README", "status: superseded")

    def test_path_escape_is_rejected(self) -> None:
        self.contract["assertions"][0]["required_evidence_paths"] = ["../outside"]
        self.write_contract()
        self.assert_failure("unsafe repository-relative path")

    def test_absolute_path_is_rejected(self) -> None:
        self.contract["assertions"][0]["report"] = "/tmp/outside.md"
        self.write_contract()
        self.assert_failure("unsafe repository-relative path")

    def test_duplicate_json_key_is_rejected(self) -> None:
        text = self.contract_path.read_text(encoding="utf-8")
        self.contract_path.write_text(
            text.replace(
                '"schema_version": 1,',
                '"schema_version": 1,\n  "schema_version": 1,',
                1,
            ),
            encoding="utf-8",
        )
        self.assert_failure("duplicate JSON key", "schema_version")

    def test_wrong_schema_version_is_rejected(self) -> None:
        self.contract["schema_version"] = 2
        self.write_contract()
        self.assert_failure("schema_version must be 1")

    def test_unknown_top_level_key_is_rejected(self) -> None:
        self.contract["unexpected"] = True
        self.write_contract()
        self.assert_failure("unknown contract keys", "unexpected")

    def test_missing_top_level_key_is_rejected(self) -> None:
        del self.contract["overview"]
        self.write_contract()
        self.assert_failure("missing contract keys", "overview")

    def test_unknown_assertion_key_is_rejected(self) -> None:
        self.contract["assertions"][0]["unexpected"] = True
        self.write_contract()
        self.assert_failure("unknown assertion keys", "unexpected")

    def test_duplicate_assertion_id_is_rejected(self) -> None:
        self.contract["assertions"][1]["criterion_id"] = self.contract["assertions"][0][
            "criterion_id"
        ]
        self.write_contract()
        self.assert_failure("duplicate assertion IDs")

    def test_unknown_assertion_id_is_rejected(self) -> None:
        self.contract["assertions"][0]["criterion_id"] = "DML-99"
        self.write_contract()
        self.assert_failure("assertion IDs must be exactly")

    def test_non_implemented_contract_state_is_rejected(self) -> None:
        self.contract["assertions"][0]["required_state"] = "Partial"
        self.write_contract()
        self.assert_failure("required_state must be Implemented")

    def test_wrong_report_mapping_fails(self) -> None:
        self.assertion("QAF-12")["report"] = self.assertion("AUT-09")["report"]
        self.write_contract()
        self.assert_failure("QAF-12", "report mismatch")

    def test_empty_assertion_array_is_rejected(self) -> None:
        self.contract["assertions"][0]["completed_task_ids"] = []
        self.write_contract()
        self.assert_failure("completed_task_ids", "non-empty array")

    def test_non_string_assertion_array_item_is_rejected(self) -> None:
        self.contract["assertions"][0]["forbidden_stale_phrases"] = [7]
        self.write_contract()
        self.assert_failure("forbidden_stale_phrases", "non-empty strings")

    def test_duplicate_assertion_array_item_is_rejected(self) -> None:
        evidence = self.contract["assertions"][0]["required_evidence_paths"][0]
        self.contract["assertions"][0]["required_evidence_paths"] = [evidence, evidence]
        self.write_contract()
        self.assert_failure("required_evidence_paths", "duplicate values")

    def test_structurally_invalid_report_is_fail_closed(self) -> None:
        path = self.report_path("QAF-12")
        lines = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("| QAF-16 |")
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assert_failure("audit criterion contract", "missing criterion IDs: QAF-16")


if __name__ == "__main__":
    unittest.main()
