from __future__ import annotations

import copy
import json
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = "scripts/validation/generate-security-automation-readiness.sh"
AUDIT_PACK = (
    ROOT
    / "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack"
)


class SecurityAutomationReadinessTests(unittest.TestCase):
    maxDiff = None

    def render(self) -> str:
        result = subprocess.run(
            ["bash", GENERATOR, "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def render_fixture(
        self,
        workflow_contract: dict[str, object],
        workflow_text: str,
    ) -> str:
        with tempfile.TemporaryDirectory(prefix="security-readiness-") as temporary:
            root = pathlib.Path(temporary)
            overrides = {
                GENERATOR: (ROOT / GENERATOR).read_text(encoding="utf-8"),
                ".github/workflow-contract.yml": json.dumps(
                    workflow_contract, indent=2
                ),
                ".github/workflows/ci-quality.yml": workflow_text,
                ".github/SECURITY.md": "# Security\n",
                ".github/dependabot.yml": "package-ecosystem: npm\n",
                ".gitleaks.toml": "[allowlist]\n",
                ".pre-commit-config.yaml": "- id: gitleaks\n",
            }
            fixture_paths = subprocess.run(
                [
                    "git",
                    "ls-files",
                    "scripts",
                    "tests/validation/test_run_ci_precommit.sh",
                    ".github/workflows",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.splitlines()
            for relative in fixture_paths:
                if relative in overrides:
                    continue
                source = ROOT / relative
                if not source.is_file():
                    continue
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            for relative, content in overrides.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(
                ["git", "init", "--quiet"], cwd=root, check=True
            )
            subprocess.run(
                ["git", "add", "."], cwd=root, check=True
            )
            result = subprocess.run(
                ["bash", GENERATOR, "--dry-run"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            return result.stdout

    def typed_fixture(self) -> tuple[dict[str, object], str]:
        loaded = yaml.safe_load(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
        )
        assert isinstance(loaded, dict)
        contract: dict[str, object] = loaded
        workflow_text = (
            ROOT / ".github/workflows/ci-quality.yml"
        ).read_text(encoding="utf-8")
        return contract, workflow_text

    def test_typed_workflow_evidence_requires_reachable_gates_and_actions(
        self,
    ) -> None:
        contract, workflow_text = self.typed_fixture()
        for raw_literal in (
            "run-zizmor-sarif",
            "check-all-hardening.sh",
            "check-template-security-baseline.sh",
            "npm audit",
        ):
            self.assertNotIn(raw_literal, workflow_text)
        output = self.render_fixture(contract, workflow_text)

        for control_id in ("002", "003", "005", "008"):
            self.assertRegex(
                output,
                rf"(?m)^\| SEC-AUTO-{control_id} \|.*\| Implemented \|",
            )
        self.assertIn(
            "| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |", output
        )

    def test_malformed_or_mismatched_gate_graph_fails_closed(self) -> None:
        base_contract, base_workflow = self.typed_fixture()

        def gate_node(contract: dict[str, object], gate_id: str) -> dict[str, object]:
            return next(
                node
                for node in contract["gate_nodes"]
                if node["gate_id"] == gate_id
            )

        gate_program = (
            "python3 scripts/validation/run-ci-gate.py "
            "--profile ci --gate ci.zizmor"
        )

        cycle = copy.deepcopy(base_contract)
        gate_node(cycle, "ci.zizmor")["children"].append("ci.zizmor")

        non_string_child = copy.deepcopy(base_contract)
        gate_node(non_string_child, "ci.zizmor")["children"].append(42)

        absent_actual_job_workflow = base_workflow.replace(
            "  zizmor:\n", "  actual-zizmor:\n", 1
        )

        missing_gate_projection_workflow = base_workflow.replace(
            "run: " + gate_program,
            "run: echo no-registered-gate",
        )

        wrong_gate_projection_workflow = base_workflow.replace(
            "--gate ci.zizmor",
            "--gate ci.infrastructure-hardening",
        )

        partial_gate_projection_workflow = base_workflow.replace(
            "--gate ci.infrastructure-hardening",
            "--gate leaf.infrastructure-hardening",
        )

        duplicate_gate_projection_workflow = base_workflow.replace(
            "      - name: Upload SARIF file\n",
            "      - name: Run zizmor gate again\n"
            f"        run: {gate_program}\n"
            "      - name: Upload SARIF file\n",
        )

        dynamic_gate_projection_workflow = base_workflow.replace(
            "--gate ci.zizmor",
            "--gate ${{ github.ref }}",
        )

        disabled_gate_step_workflow = base_workflow.replace(
            f"        run: {gate_program}",
            "        if: ${{ false }}\n" f"        run: {gate_program}",
        )

        disabled_gate_job_workflow = base_workflow.replace(
            "  zizmor:\n",
            "  zizmor:\n    if: ${{ false }}\n",
            1,
        )

        non_string_run_workflow = base_workflow.replace(
            "      - name: Upload SARIF file\n",
            "      - name: Invalid non-string program\n"
            "        run: 123\n"
            "      - name: Upload SARIF file\n",
        )

        explicit_shell_workflow = base_workflow.replace(
            gate_program + "\n",
            gate_program + "\n        shell: bash\n",
        )

        working_directory_workflow = base_workflow.replace(
            gate_program + "\n",
            gate_program + "\n"
            "        working-directory: scripts\n",
        )

        workflow_defaults_workflow = base_workflow.replace(
            "on:\n",
            "defaults:\n  run:\n    shell: bash\n"
            "on:\n",
        )

        job_defaults_workflow = base_workflow.replace(
            "  zizmor:\n",
            "  zizmor:\n    defaults:\n      run:\n        shell: bash\n",
            1,
        )

        failure_weakening_workflow = base_workflow.replace(
            gate_program + "\n",
            gate_program + "\n"
            "        continue-on-error: true\n",
        )

        disabled_sarif_action_workflow = base_workflow.replace(
            "      - name: Upload SARIF file\n",
            "      - name: Upload SARIF file\n        if: ${{ false }}\n",
        )

        missing_sarif_permission_workflow = base_workflow.replace(
            "      security-events: write\n",
            "",
            1,
        )

        duplicate_gate = copy.deepcopy(base_contract)
        duplicate_gate["gate_nodes"].append(
            copy.deepcopy(gate_node(duplicate_gate, "leaf.zizmor"))
        )

        duplicate_root = copy.deepcopy(base_contract)
        duplicate_root["job_roots"].append(
            copy.deepcopy(duplicate_root["job_roots"][0])
        )

        cases = (
            ("aggregate cycle", cycle, base_workflow),
            ("non-string aggregate child", non_string_child, base_workflow),
            ("job absent from actual workflow", base_contract, absent_actual_job_workflow),
            (
                "job does not project registered gate",
                base_contract,
                missing_gate_projection_workflow,
            ),
            (
                "job projects a gate outside its root",
                base_contract,
                wrong_gate_projection_workflow,
            ),
            (
                "job projects only part of its root",
                base_contract,
                partial_gate_projection_workflow,
            ),
            (
                "job projects its root more than once",
                base_contract,
                duplicate_gate_projection_workflow,
            ),
            (
                "job uses a dynamic gate expression",
                base_contract,
                dynamic_gate_projection_workflow,
            ),
            (
                "registered gate step is disabled",
                base_contract,
                disabled_gate_step_workflow,
            ),
            (
                "registered gate job is disabled",
                base_contract,
                disabled_gate_job_workflow,
            ),
            (
                "job includes a non-string run program",
                base_contract,
                non_string_run_workflow,
            ),
            (
                "gate step declares a shell",
                base_contract,
                explicit_shell_workflow,
            ),
            (
                "gate step declares a working directory",
                base_contract,
                working_directory_workflow,
            ),
            (
                "workflow declares run defaults",
                base_contract,
                workflow_defaults_workflow,
            ),
            (
                "job declares run defaults",
                base_contract,
                job_defaults_workflow,
            ),
            (
                "registered gate step weakens failures",
                base_contract,
                failure_weakening_workflow,
            ),
            (
                "SARIF action step is disabled",
                base_contract,
                disabled_sarif_action_workflow,
            ),
            (
                "SARIF permission is missing",
                base_contract,
                missing_sarif_permission_workflow,
            ),
            ("duplicate gate", duplicate_gate, base_workflow),
            ("duplicate root", duplicate_root, base_workflow),
        )
        for name, contract, workflow in cases:
            with self.subTest(name=name):
                output = self.render_fixture(contract, workflow)
                for control_id in ("002", "003", "005", "008"):
                    self.assertNotRegex(
                        output,
                        rf"(?m)^\| SEC-AUTO-{control_id} \|.*\| Implemented \|",
                    )
                self.assertIn(
                    "| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |",
                    output,
                )

    def test_invalid_or_comment_only_action_evidence_fails_closed(self) -> None:
        base_contract, base_workflow = self.typed_fixture()
        upload_sha = base_contract["actions"][
            "github/codeql-action/upload-sarif"
        ]["sha"]

        invalid_sha_contract = copy.deepcopy(base_contract)
        invalid_sha_contract["actions"]["github/codeql-action/upload-sarif"][
            "sha"
        ] = "v4"
        invalid_sha_workflow = base_workflow.replace("@" + upload_sha, "@v4")

        comment_only_workflow = base_workflow.replace(
            "        uses: github/codeql-action/upload-sarif@" + upload_sha,
            "        run: echo no-action\n"
            "        # uses: github/codeql-action/upload-sarif@" + upload_sha,
        )

        for name, contract, workflow in (
            ("non-40-hex action SHA", invalid_sha_contract, invalid_sha_workflow),
            ("action reference only in YAML comment", base_contract, comment_only_workflow),
        ):
            with self.subTest(name=name):
                output = self.render_fixture(contract, workflow)
                self.assertNotRegex(
                    output,
                    r"(?m)^\| SEC-AUTO-002 \|.*\| Implemented \|",
                )
                self.assertIn(
                    "| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |",
                    output,
                )

    def test_supply_chain_fixture_contract_keeps_broad_sca_open(self) -> None:
        output = self.render()
        self.assertIn(
            "| SEC-AUTO-008 | Scoped ecosystem vulnerability gate | Implemented |",
            output,
        )
        self.assertIn("| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |", output)
        for control_id in ("009", "010", "011", "013"):
            self.assertIn(
                f"| SEC-AUTO-{control_id} |",
                output,
            )
            self.assertRegex(
                output,
                rf"(?m)^\| SEC-AUTO-{control_id} \|.*\| Implemented \|",
            )
        self.assertNotIn(
            "| SEC-AUTO-008 | OSV/SCA vulnerability gate | Implemented |", output
        )

    def test_control_count_and_summary_are_precise(self) -> None:
        output = self.render()
        self.assertEqual(
            13,
            len(re.findall(r"^\| SEC-AUTO-[0-9]{3} \|", output, re.MULTILINE)),
        )
        self.assertIn("| Implemented | 11 |", output)
        self.assertIn("| Partially Implemented | 1 |", output)
        self.assertIn("| Gap | 1 |", output)

    def test_broad_supply_chain_gaps_route_to_archived_spec_126(self) -> None:
        output = self.render()
        spec_126 = (
            "[Spec 126]"
            "(../../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)"
        )
        for control_id in (
            "SEC-AUTO-012",
        ):
            self.assertRegex(
                output,
                rf"(?m)^\| `{control_id}` \|.*\| {re.escape(spec_126)} \|$",
            )

    def test_canonical_security_leaf_preserves_the_three_signal_boundary(self) -> None:
        security_audit = (AUDIT_PACK / "security-framework-maturity.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("satisfies only `SEC-AUTO-008`", security_audit)
        self.assertIn("broad dependency SCA (`SEC-AUTO-012`)", security_audit)
        self.assertIn(
            "container/image vulnerability scanning (`SEC-AUTO-013`)",
            security_audit,
        )

    def test_historical_audit_label_points_to_archived_spec_126(self) -> None:
        """The audited `draft` label is historical; its target is archived."""
        automation_audit = (AUDIT_PACK / "automation-candidates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "`SEC-AUTO-012` and `SEC-AUTO-013` remain `Gap`", automation_audit
        )
        self.assertIn(
            "[draft Spec 126]"
            "(../../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)",
            automation_audit,
        )


if __name__ == "__main__":
    unittest.main()
