from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


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


def _assert_task5_integration_contract(
    case: unittest.TestCase,
    workflow: str,
    repo_contracts: str,
    generator: str,
    matrix: str,
) -> None:
    command = "python3 scripts/validation/check-agentic-audit-semantic-freshness.py"
    semantic_step = {
        "name": "Check canonical audit semantic freshness",
        "run": command,
    }
    workflow_data = yaml.safe_load(workflow)
    jobs = workflow_data["jobs"]
    semantic_name_matches: list[tuple[str, dict[str, object]]] = []
    semantic_command_matches: list[tuple[str, dict[str, object]]] = []
    for job_name, job in jobs.items():
        for step in job.get("steps", []):
            if not isinstance(step, dict):
                continue
            if step.get("name") == semantic_step["name"]:
                semantic_name_matches.append((job_name, step))
            if step.get("run") == command:
                semantic_command_matches.append((job_name, step))
    expected_ci_match = [("repo-contracts", semantic_step)]
    case.assertEqual(expected_ci_match, semantic_name_matches)
    case.assertEqual(expected_ci_match, semantic_command_matches)

    repo_steps = jobs["repo-contracts"]["steps"]
    step_names = [
        step.get("name") if isinstance(step, dict) else None for step in repo_steps
    ]
    metadata_name = "Check changed and new document metadata"
    repository_contracts_name = "Check repository contracts"
    case.assertEqual(1, step_names.count(metadata_name))
    case.assertEqual(1, step_names.count(semantic_step["name"]))
    case.assertEqual(1, step_names.count(repository_contracts_name))
    case.assertLess(
        step_names.index(metadata_name), step_names.index(semantic_step["name"])
    )
    case.assertLess(
        step_names.index(semantic_step["name"]),
        step_names.index(repository_contracts_name),
    )

    section_heading = 'section "Agentic audit semantic freshness"'
    case.assertEqual(1, repo_contracts.count(section_heading))
    section_start = repo_contracts.index(section_heading)
    section_end = repo_contracts.index('\nsection "', section_start + 1)
    section = repo_contracts[section_start:section_end]
    marker = "audit_semantic_freshness: PASS assertions=11 failures=0"
    mktemp_line = (
        'semantic_audit_output="$(mktemp "${TMPDIR:-/tmp}/'
        'check-repo-contracts-agentic-audit-semantic.XXXXXX")"'
    )
    required_fragments = [
        mktemp_line,
        'rm -f -- "$semantic_audit_output"',
        f'if ! {command} >"$semantic_audit_output" 2>&1; then',
        'fail "agentic audit semantic freshness failed"',
        f"elif ! grep -Fxq '{marker}' \"$semantic_audit_output\"; then",
        'fail "agentic audit semantic validator did not print the exact pass marker"',
        "trap cleanup_semantic_audit_output EXIT",
        "trap 'handle_semantic_audit_signal 129' HUP",
        "trap 'handle_semantic_audit_signal 130' INT",
        "trap 'handle_semantic_audit_signal 143' TERM",
        "trap - EXIT HUP INT TERM",
    ]
    for fragment in required_fragments:
        case.assertIn(fragment, section)
    case.assertEqual(1, repo_contracts.count(mktemp_line))
    case.assertEqual(1, section.count(command))
    case.assertEqual(2, section.count('cat "$semantic_audit_output" >&2'))

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

    def integration_surfaces(self) -> tuple[str, str, str, str]:
        repo_contracts = (
            ROOT / "scripts/validation/check-repo-contracts.sh"
        ).read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/ci-quality.yml").read_text(
            encoding="utf-8"
        )
        generator = (
            ROOT / "scripts/validation/generate-audit-implementation-matrix.sh"
        ).read_text(encoding="utf-8")
        matrix = (
            ROOT / "docs/90.references/data/governance/audit-implementation-matrix.md"
        ).read_text(encoding="utf-8")
        return workflow, repo_contracts, generator, matrix

    def test_task5_integration_contract_is_exact(self) -> None:
        _assert_task5_integration_contract(self, *self.integration_surfaces())

    def test_task5_integration_contract_rejects_regressions(self) -> None:
        workflow, repo_contracts, generator, matrix = self.integration_surfaces()
        semantic_step = (
            "      - name: Check canonical audit semantic freshness\n"
            "        run: python3 scripts/validation/"
            "check-agentic-audit-semantic-freshness.py\n"
        )
        ordered_steps = (
            "      - name: Check changed and new document metadata\n"
            "        run: python3 scripts/validation/check-document-metadata.py "
            "--mode check-changed\n"
            f"{semantic_step}"
            "      - name: Check repository contracts\n"
            "        run: bash scripts/validation/check-repo-contracts.sh\n"
        )
        reordered_steps = ordered_steps.replace(
            semantic_step,
            "",
            1,
        ).replace(
            "      - name: Check repository contracts\n"
            "        run: bash scripts/validation/check-repo-contracts.sh\n",
            "      - name: Check repository contracts\n"
            "        run: bash scripts/validation/check-repo-contracts.sh\n"
            f"{semantic_step}",
            1,
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
        mutations = {
            "duplicate CI step": (
                workflow.replace(semantic_step, semantic_step * 2, 1),
                repo_contracts,
                generator,
                matrix,
            ),
            "misordered CI step": (
                workflow.replace(ordered_steps, reordered_steps, 1),
                repo_contracts,
                generator,
                matrix,
            ),
            "unguarded validator exit": (
                workflow,
                repo_contracts.replace(
                    "if ! python3 scripts/validation/"
                    "check-agentic-audit-semantic-freshness.py",
                    "python3 scripts/validation/"
                    "check-agentic-audit-semantic-freshness.py",
                    1,
                ),
                generator,
                matrix,
            ),
            "non-exact pass marker": (
                workflow,
                repo_contracts.replace(
                    "elif ! grep -Fxq 'audit_semantic_freshness: PASS "
                    "assertions=11 failures=0'",
                    "elif ! grep -q 'audit_semantic_freshness: PASS "
                    "assertions=11 failures=0'",
                    1,
                ),
                generator,
                matrix,
            ),
            "missing signal cleanup": (
                workflow,
                repo_contracts.replace(
                    "trap 'handle_semantic_audit_signal 130' INT\n", "", 1
                ),
                generator,
                matrix,
            ),
            "semantic validation after rendering": (
                workflow,
                repo_contracts,
                late_generator,
                matrix,
            ),
            "generated metric drift": (
                workflow,
                repo_contracts,
                generator,
                matrix.replace(
                    "| Semantic closure assertions passed | 11 |",
                    "| Semantic closure assertions passed | 10 |",
                    1,
                ),
            ),
        }
        for name, surfaces in mutations.items():
            with self.subTest(name=name):
                self.assertNotEqual(
                    (workflow, repo_contracts, generator, matrix), surfaces
                )
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
