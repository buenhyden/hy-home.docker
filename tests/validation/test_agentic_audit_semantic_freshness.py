from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-agentic-audit-semantic-freshness.py"
CONTRACT = pathlib.Path("scripts/validation/agentic-audit-semantic-contract.json")
TASK_EVIDENCE_FIXTURE = ROOT / "tests/fixtures/agentic-audit/task-evidence.md"
sys.path.insert(0, str(SCRIPT.parent))

spec = importlib.util.spec_from_file_location(
    "agentic_audit_semantic_freshness", SCRIPT
)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load semantic validator: {SCRIPT}")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def _assert_task5_integration_contract(
    case: unittest.TestCase,
    workflow: str,
    workflow_contract: str,
    manifest: str,
    generator: str,
    matrix: str,
) -> None:
    changed_command = "python3 scripts/validation/run-ci-gate.py --profile changed"
    full_command = "python3 scripts/validation/run-ci-gate.py --profile full"
    semantic_command = (
        "python3 scripts/validation/check-agentic-audit-semantic-freshness.py"
    )
    workflow_data = yaml.safe_load(workflow)
    jobs = workflow_data["jobs"]
    case.assertEqual(
        ("validation-changed", "validation-full"),
        tuple(jobs),
    )
    commands = [
        step.get("run")
        for job in jobs.values()
        for step in job.get("steps", ())
        if isinstance(step, dict) and isinstance(step.get("run"), str)
    ]
    case.assertEqual(1, workflow.count(changed_command))
    case.assertEqual(1, workflow.count(full_command))
    case.assertEqual(0, workflow.count(semantic_command))
    case.assertIn(changed_command, commands)
    case.assertIn(full_command, commands)

    contract_data = json.loads(workflow_contract)
    public_gate = contract_data["public_gate"]
    case.assertEqual(["changed", "full"], public_gate["profiles"])
    integrity_roots = public_gate["suite_roots"]["repository-integrity"]
    case.assertEqual(1, integrity_roots.count("local.workflow-harness"))

    manifest_data = yaml.safe_load(manifest)
    semantic_rows = [
        row
        for row in manifest_data["files"]
        if row.get("path")
        == "scripts/validation/check-agentic-audit-semantic-freshness.py"
    ]
    case.assertEqual(1, len(semantic_rows))
    case.assertEqual(
        ["repository-integrity"],
        semantic_rows[0].get("public_suites"),
    )

    build_start = generator.index("def build_output() -> tuple[str, list[str]]:")
    validate_call = generator.index(
        "semantic_result = validate_semantics(", build_start
    )
    render_start = generator.index("lines: list[str] = [", build_start)
    case.assertLess(validate_call, render_start)
    generator_metric_fragments = [
        "EXPECTED_SEMANTIC_ASSERTIONS = 11",
        'f"| Semantic closure assertions expected | {EXPECTED_SEMANTIC_ASSERTIONS} |",',
        'f"| Semantic closure assertions passed | '
        '{semantic_result.assertion_count} |",',
        '"| Semantic closure assertion failures | 0 |",',
    ]
    for fragment in generator_metric_fragments:
        case.assertIn(fragment, generator)

    expected_matrix_metrics = [
        "| Semantic closure assertions expected | 11 |",
        "| Semantic closure assertions passed | 11 |",
        "| Semantic closure assertion failures | 0 |",
    ]
    actual_matrix_metrics = [
        line
        for line in matrix.splitlines()
        if line.startswith("| Semantic closure assertion")
    ]
    case.assertEqual(expected_matrix_metrics, actual_matrix_metrics)


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
            pathlib.Path(contract["canonical_pack"]) / "0019-readme/README.md",
            # The superseded snapshot is preserved under the archive, so its
            # location comes from the checker rather than being spelled twice.
            module.SUPERSEDED_2026_07_07_README,
            CONTRACT,
        }
        required_paths.update(
            path.relative_to(ROOT)
            for path in (ROOT / contract["canonical_pack"]).glob("*/README.md")
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

        task_evidence = self.repo / contract["task_evidence"]
        task_evidence.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TASK_EVIDENCE_FIXTURE, task_evidence)

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

    def integration_surfaces(self) -> tuple[str, str, str, str, str]:
        workflow = (ROOT / ".github/workflows/ci-quality.yml").read_text(
            encoding="utf-8"
        )
        workflow_contract = (ROOT / ".github/workflow-contract.yml").read_text(
            encoding="utf-8"
        )
        manifest = (ROOT / "scripts/manifest.yaml").read_text(encoding="utf-8")
        generator = (
            ROOT / "scripts/validation/generate-audit-implementation-matrix.sh"
        ).read_text(encoding="utf-8")
        matrix = (
            ROOT / "docs/90.references/data/0065-audit-implementation-matrix/README.md"
        ).read_text(encoding="utf-8")
        return workflow, workflow_contract, manifest, generator, matrix

    def test_task5_integration_contract_is_exact(self) -> None:
        _assert_task5_integration_contract(self, *self.integration_surfaces())

    def test_task5_integration_contract_rejects_regressions(self) -> None:
        workflow, workflow_contract, manifest, generator, matrix = (
            self.integration_surfaces()
        )
        semantic_call = (
            "    semantic_result = validate_semantics(\n"
            '        pathlib.Path("."),\n'
            "        pathlib.Path("
            '"scripts/validation/agentic-audit-semantic-contract.json"),\n'
            "    )\n"
        )
        late_generator = generator.replace(semantic_call, "", 1).replace(
            '    return "\\n".join(lines), failures\n',
            f'{semantic_call}\n    return "\\n".join(lines), failures\n',
            1,
        )
        semantic_row = (
            "- path: scripts/validation/check-agentic-audit-semantic-freshness.py\n"
            "  kind: validator\n"
            "  public_suites:\n"
            "  - repository-integrity\n"
        )
        missing_workflow_root = json.loads(workflow_contract)
        missing_workflow_root["public_gate"]["suite_roots"][
            "repository-integrity"
        ].remove("local.workflow-harness")
        mutations = {
            "duplicate changed workflow route": (
                workflow
                + "\n# python3 scripts/validation/run-ci-gate.py --profile changed\n",
                workflow_contract,
                manifest,
                generator,
                matrix,
            ),
            "copied atomic workflow command": (
                workflow + "\n# python3 scripts/validation/"
                "check-agentic-audit-semantic-freshness.py\n",
                workflow_contract,
                manifest,
                generator,
                matrix,
            ),
            "missing public workflow root": (
                workflow,
                json.dumps(missing_workflow_root),
                manifest,
                generator,
                matrix,
            ),
            "missing validator ownership": (
                workflow,
                workflow_contract,
                manifest.replace(
                    "scripts/validation/check-agentic-audit-semantic-freshness.py",
                    "scripts/validation/missing-agentic-audit-semantic.py",
                    1,
                ),
                generator,
                matrix,
            ),
            "duplicate validator ownership": (
                workflow,
                workflow_contract,
                manifest + semantic_row,
                generator,
                matrix,
            ),
            "wrong validator suite": (
                workflow,
                workflow_contract,
                manifest.replace(
                    "- path: scripts/validation/"
                    "check-agentic-audit-semantic-freshness.py\n"
                    "  kind: validator\n"
                    "  public_suites:\n"
                    "  - repository-integrity\n",
                    "- path: scripts/validation/"
                    "check-agentic-audit-semantic-freshness.py\n"
                    "  kind: validator\n"
                    "  public_suites:\n"
                    "  - operations\n",
                    1,
                ),
                generator,
                matrix,
            ),
            "semantic validation after rendering": (
                workflow,
                workflow_contract,
                manifest,
                late_generator,
                matrix,
            ),
            "generated metric drift": (
                workflow,
                workflow_contract,
                manifest,
                generator,
                matrix.replace(
                    "| Semantic closure assertions passed | 11 |",
                    "| Semantic closure assertions passed | 10 |",
                    1,
                ),
            ),
        }
        canonical = (workflow, workflow_contract, manifest, generator, matrix)
        for name, surfaces in mutations.items():
            with self.subTest(name=name):
                self.assertNotEqual(canonical, surfaces)
                with self.assertRaises(AssertionError):
                    _assert_task5_integration_contract(self, *surfaces)

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

    def test_aut_09_exact_pre_remediation_phrase_fails(self) -> None:
        self.append_to_report("AUT-09", "the controlled wrapper is absent until Task 9")
        self.assert_failure("AUT-09", "forbidden stale phrase")

    def test_missing_completed_task_id_fails(self) -> None:
        task_path = self.repo / self.contract["task_evidence"]
        text = task_path.read_text(encoding="utf-8")
        task_path.write_text(text.replace("T-AER-009", "T-AER-X09"), encoding="utf-8")
        self.assert_failure("QAF-12", "completed task T-AER-009")

    def test_retired_task_evidence_requires_explicit_compact_regular_git_recovery(
        self,
    ) -> None:
        from scripts.lib.document_governance import archive

        task_path = self.repo / self.contract["task_evidence"]
        expected = task_path.read_text(encoding="utf-8")
        subprocess.run(
            ["git", "add", "--", self.contract["task_evidence"]],
            cwd=self.repo,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-qm",
                "task evidence",
            ],
            cwd=self.repo,
            check=True,
        )
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.repo, text=True
        ).strip()
        task_path.unlink()
        row = {
            "source_path": self.contract["task_evidence"],
            "target_path": None,
            "artifact_id": None,
            "action": "delete",
            "recovery_commit": commit,
        }
        compact = {"schema_version": 3, "migration_id": "mig-0003", "rows": [row]}
        with mock.patch.object(archive, "_migration_document", return_value=compact):
            errors = []
            self.assertEqual(
                expected, module._read_task_evidence(self.repo, self.contract, errors)
            )
            self.assertEqual([], errors)
            for key, value in (
                ("action", "rename"),
                ("recovery_commit", None),
                ("recovery_commit", "0" * 40),
                ("source_path", "../outside"),
            ):
                original = row[key]
                row[key] = value
                with self.subTest(field=key):
                    errors = []
                    self.assertIsNone(
                        module._read_task_evidence(self.repo, self.contract, errors)
                    )
                    self.assertTrue(errors)
                row[key] = original

    def test_wrong_lifecycle_heading_fails(self) -> None:
        path = self.repo / self.contract["audit_index"]
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("## Canonical Current Audit", "## Current References"),
            encoding="utf-8",
        )
        self.assert_failure("audit index", "required heading")

    def test_non_published_canonical_readme_fails(self) -> None:
        path = self.repo / self.contract["canonical_pack"] / "0019-readme/README.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace('status: "published"', 'status: "superseded"', 1),
            encoding="utf-8",
        )
        self.assert_failure("canonical README", "status: published")

    def test_non_superseded_2026_07_07_readme_fails(self) -> None:
        path = self.repo / module.SUPERSEDED_2026_07_07_README
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("status: superseded", "status: active", 1), encoding="utf-8"
        )
        self.assert_failure("2026-07-07 README", "status: superseded")

    def test_path_escape_is_rejected(self) -> None:
        self.contract["assertions"][0]["required_evidence_paths"] = ["../outside"]
        self.write_contract()
        self.assert_failure("unsafe repository-relative path")

    def test_tracked_symlink_evidence_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            outside_path = pathlib.Path(outside) / "evidence.txt"
            outside_path.write_text("outside repository\n", encoding="utf-8")
            link = self.repo / "external-evidence"
            link.symlink_to(outside_path)
            subprocess.run(
                ["git", "add", "external-evidence"], cwd=self.repo, check=True
            )
            self.assertion("QAF-12")["required_evidence_paths"] = ["external-evidence"]
            self.write_contract()
            self.assert_failure("QAF-12", "symlink", "external-evidence")

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
        self.assert_failure("schema_version must be integer 1")

    def test_float_schema_version_is_rejected(self) -> None:
        self.contract["schema_version"] = 1.0
        self.write_contract()
        self.assert_failure("schema_version must be integer 1")

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

    def test_canonical_audit_index_redirect_is_rejected(self) -> None:
        canonical = self.repo / self.contract["audit_index"]
        redirect = self.repo / "redirected-audit-index.md"
        shutil.copy2(canonical, redirect)
        subprocess.run(
            ["git", "add", "redirected-audit-index.md"], cwd=self.repo, check=True
        )
        canonical.write_text(
            canonical.read_text(encoding="utf-8").replace(
                "## Canonical Current Audit", "## Current References"
            ),
            encoding="utf-8",
        )
        self.contract["audit_index"] = "redirected-audit-index.md"
        self.write_contract()
        self.assert_failure("audit_index", "fixed canonical path")

    def test_untracked_assertion_report_fails(self) -> None:
        report = str(self.assertion("AUT-09")["report"])
        subprocess.run(
            ["git", "rm", "--cached", "-q", "--", report],
            cwd=self.repo,
            check=True,
        )
        self.assert_failure("AUT-09", "required tracked report")

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

    def test_invalid_utf8_report_is_fail_closed(self) -> None:
        self.report_path("AUT-09").write_bytes(b"\xff")
        self.assert_failure("audit criterion contract", "invalid UTF-8")


if __name__ == "__main__":
    unittest.main()
