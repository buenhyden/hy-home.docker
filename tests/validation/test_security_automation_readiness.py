from __future__ import annotations

import pathlib
import re
import subprocess
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

    def test_scoped_gate_does_not_close_broad_scanning(self) -> None:
        output = self.render()
        self.assertIn(
            "| SEC-AUTO-008 | Scoped ecosystem vulnerability gate | Implemented |",
            output,
        )
        self.assertIn("| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |", output)
        self.assertIn(
            "| SEC-AUTO-013 | Container/image vulnerability scanning | Gap |", output
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
        self.assertIn("| Implemented | 7 |", output)
        self.assertIn("| Partially Implemented | 1 |", output)
        self.assertIn("| Gap | 5 |", output)

    def test_broad_supply_chain_gaps_route_to_draft_spec_126(self) -> None:
        output = self.render()
        spec_126 = (
            "[Draft Spec 126]"
            "(../../../03.specs/126-security-supply-chain-remediation/spec.md)"
        )
        for control_id in (
            "SEC-AUTO-009",
            "SEC-AUTO-010",
            "SEC-AUTO-011",
            "SEC-AUTO-012",
            "SEC-AUTO-013",
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
            "(../../../03.specs/126-security-supply-chain-remediation/spec.md)",
            automation_audit,
        )


if __name__ == "__main__":
    unittest.main()
