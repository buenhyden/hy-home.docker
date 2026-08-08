from __future__ import annotations

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

    def test_typed_workflow_evidence_requires_reachable_gates_and_actions(
        self,
    ) -> None:
        upload_sha = "a" * 40
        workflow_text = f"""\
name: Typed security gate fixture
on: [pull_request]
permissions:
  contents: read
jobs:
  security:
    permissions:
      actions: read
      contents: read
      security-events: write
    steps:
      - run: python3 scripts/validation/run-ci-gate.py --gate ci.security
      - uses: github/codeql-action/upload-sarif@{upload_sha}
"""
        for raw_literal in (
            "run-zizmor-sarif",
            "check-all-hardening.sh",
            "check-template-security-baseline.sh",
            "npm audit",
        ):
            self.assertNotIn(raw_literal, workflow_text)

        contract = {
            "schema_version": 2,
            "workflows": {
                ".github/workflows/ci-quality.yml": {
                    "jobs": {"security": {}}
                }
            },
            "gate_nodes": [
                {
                    "gate_id": "ci.security",
                    "kind": "aggregate",
                    "children": [
                        "leaf.zizmor",
                        "leaf.repo-contracts",
                        "leaf.hardening",
                        "leaf.template-security",
                        "leaf.scoped-npm-audit",
                    ],
                },
                {
                    "gate_id": "leaf.zizmor",
                    "kind": "leaf",
                    "entrypoint": "scripts/validation/ci_gate_adapters.py",
                    "argv": ["run-zizmor-sarif"],
                },
                {
                    "gate_id": "leaf.repo-contracts",
                    "kind": "leaf",
                    "entrypoint": "scripts/validation/check-repo-contracts.sh",
                    "argv": [],
                },
                {
                    "gate_id": "leaf.hardening",
                    "kind": "leaf",
                    "entrypoint": "scripts/hardening/check-all-hardening.sh",
                    "argv": [],
                },
                {
                    "gate_id": "leaf.template-security",
                    "kind": "leaf",
                    "entrypoint": "scripts/validation/check-template-security-baseline.sh",
                    "argv": [],
                },
                {
                    "gate_id": "leaf.scoped-npm-audit",
                    "kind": "leaf",
                    "entrypoint": "scripts/validation/ci_gate_adapters.py",
                    "argv": [
                        "run-npm",
                        "audit",
                        "--audit-level=high",
                        "--prefix",
                        "projects/storybook/nextjs",
                    ],
                },
                {
                    "gate_id": "leaf.unwired-broad-sca",
                    "kind": "leaf",
                    "entrypoint": "scripts/validation/unwired.py",
                    "argv": ["osv-scanner"],
                },
            ],
            "job_roots": [
                {
                    "workflow": ".github/workflows/ci-quality.yml",
                    "job_id": "security",
                    "root_gate_id": "ci.security",
                }
            ],
            "profile_roots": [],
            "actions": {
                "github/codeql-action/upload-sarif": {
                    "sha": upload_sha,
                    "consumers": [".github/workflows/ci-quality.yml"],
                }
            },
        }
        output = self.render_fixture(contract, workflow_text)

        for control_id in ("002", "003", "005", "008"):
            self.assertRegex(
                output,
                rf"(?m)^\| SEC-AUTO-{control_id} \|.*\| Implemented \|",
            )
        self.assertIn(
            "| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |", output
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

    def test_broad_supply_chain_gaps_route_to_draft_spec_126(self) -> None:
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

    def test_canonical_automation_leaf_routes_broad_gaps_to_spec_126(self) -> None:
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
