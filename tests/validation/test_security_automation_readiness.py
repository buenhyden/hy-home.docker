from __future__ import annotations

import copy
import json
import pathlib
import re
import subprocess
import tempfile
import unittest


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
            files = {
                GENERATOR: (ROOT / GENERATOR).read_text(encoding="utf-8"),
                "scripts/validation/ci_gate_contract.py": (
                    ROOT / "scripts/validation/ci_gate_contract.py"
                ).read_text(encoding="utf-8"),
                "scripts/validation/github_workflow_contract.py": (
                    ROOT / "scripts/validation/github_workflow_contract.py"
                ).read_text(encoding="utf-8"),
                ".github/workflow-contract.yml": json.dumps(
                    workflow_contract, indent=2
                ),
                ".github/workflows/ci-quality.yml": workflow_text,
                ".github/SECURITY.md": "# Security\n",
                ".github/dependabot.yml": "package-ecosystem: npm\n",
                ".gitleaks.toml": "[allowlist]\n",
                ".pre-commit-config.yaml": "- id: gitleaks\n",
                "scripts/validation/check-repo-contracts.sh": "# workflow security\n",
                "scripts/validation/check-template-security-baseline.sh": "#!/bin/sh\n",
                "scripts/hardening/check-all-hardening.sh": "#!/bin/sh\n",
                "scripts/validation/ci_gate_adapters.py": "# typed adapter\n",
                "scripts/validation/unwired.py": "# intentionally unwired\n",
            }
            for relative, content in files.items():
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
        upload_sha = "a" * 40
        workflow_text = f"""\
name: Typed security gate fixture
"on":
  pull_request:
permissions:
  contents: read
jobs:
  security:
    permissions:
      actions: read
      contents: read
      security-events: write
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Run typed security gate
        run: python3 scripts/validation/run-ci-gate.py --gate ci.security
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@{upload_sha}
"""

        def leaf(
            suite_key: str,
            entrypoint: str,
            argv: list[str],
        ) -> dict[str, object]:
            return {
                "gate_id": f"leaf.{suite_key}",
                "kind": "leaf",
                "suite_key": suite_key,
                "entrypoint": entrypoint,
                "argv": argv,
                "cwd": ".",
                "allowed_env_keys": [],
                "timeout_minutes": 10,
                "profiles": ["ci"],
                "opaque": True,
            }

        contract: dict[str, object] = {
            "schema_version": 2,
            "workflows": {
                ".github/workflows/ci-quality.yml": {
                    "name": "Typed security gate fixture",
                    "classification": "required-quality",
                    "triggers": {"pull_request": None},
                    "permissions": {"contents": "read"},
                    "concurrency": None,
                    "jobs": {
                        "security": {
                            "permissions": {
                                "actions": "read",
                                "contents": "read",
                                "security-events": "write",
                            },
                            "runs_on": "ubuntu-latest",
                            "timeout_minutes": 10,
                        }
                    },
                }
            },
            "gate_nodes": [
                {
                    "gate_id": "ci.security",
                    "kind": "aggregate",
                    "profiles": ["ci"],
                    "opaque": False,
                    "children": [
                        "leaf.zizmor",
                        "leaf.repo-contracts",
                        "leaf.hardening",
                        "leaf.template-security",
                        "leaf.scoped-npm-audit",
                    ],
                },
                leaf(
                    "zizmor",
                    "scripts/validation/ci_gate_adapters.py",
                    ["run-zizmor-sarif"],
                ),
                leaf(
                    "repo-contracts",
                    "scripts/validation/check-repo-contracts.sh",
                    [],
                ),
                leaf(
                    "hardening",
                    "scripts/hardening/check-all-hardening.sh",
                    [],
                ),
                leaf(
                    "template-security",
                    "scripts/validation/check-template-security-baseline.sh",
                    [],
                ),
                leaf(
                    "scoped-npm-audit",
                    "scripts/validation/ci_gate_adapters.py",
                    [
                        "run-npm",
                        "audit",
                        "--audit-level=high",
                        "--prefix",
                        "projects/storybook/nextjs",
                    ],
                ),
                leaf(
                    "unwired-broad-sca",
                    "scripts/validation/unwired.py",
                    ["osv-scanner"],
                ),
            ],
            "job_roots": [
                {
                    "workflow": ".github/workflows/ci-quality.yml",
                    "job_id": "security",
                    "root_gate_id": "ci.security",
                    "classification": "required-quality",
                }
            ],
            "profile_roots": [],
            "actions": {
                "github/codeql-action/upload-sarif": {
                    "sha": upload_sha,
                    "runtime": "node24",
                    "manifest_url": "https://example.invalid/action.yml",
                    "retrieved_at": "2026-08-08T00:00:00Z",
                    "consumers": [".github/workflows/ci-quality.yml"],
                    "security_disposition": "fixture-only",
                }
            },
        }
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

        cycle = copy.deepcopy(base_contract)
        cycle["gate_nodes"][0]["children"].append("ci.security")

        non_string_child = copy.deepcopy(base_contract)
        non_string_child["gate_nodes"][0]["children"].append(42)

        absent_actual_job_workflow = base_workflow.replace(
            "  security:\n", "  actual-security:\n", 1
        )

        duplicate_gate = copy.deepcopy(base_contract)
        duplicate_gate["gate_nodes"].append(
            copy.deepcopy(duplicate_gate["gate_nodes"][-1])
        )

        duplicate_root = copy.deepcopy(base_contract)
        duplicate_root["job_roots"].append(
            copy.deepcopy(duplicate_root["job_roots"][0])
        )

        cases = (
            ("aggregate cycle", cycle, base_workflow),
            ("non-string aggregate child", non_string_child, base_workflow),
            ("job absent from actual workflow", base_contract, absent_actual_job_workflow),
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

        invalid_sha_contract = copy.deepcopy(base_contract)
        invalid_sha_contract["actions"]["github/codeql-action/upload-sarif"][
            "sha"
        ] = "v4"
        invalid_sha_workflow = base_workflow.replace("@" + "a" * 40, "@v4")

        comment_only_workflow = base_workflow.replace(
            "        uses: github/codeql-action/upload-sarif@" + "a" * 40,
            "        run: echo no-action\n"
            "        # uses: github/codeql-action/upload-sarif@" + "a" * 40,
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
