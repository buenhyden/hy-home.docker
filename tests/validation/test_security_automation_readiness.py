from __future__ import annotations

import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = "scripts/validation/generate-security-automation-readiness.sh"
AUTOMATION_AUDIT = (
    ROOT
    / "docs/90.references/audits/0021-automation-candidates/README.md"
)
SECURITY_AUDIT = (
    ROOT
    / "docs/90.references/audits/0031-security-framework-maturity/README.md"
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
            "(../../../03.specs/126-security-supply-chain-remediation/spec.md)"
        )
        for control_id in (
            "SEC-AUTO-012",
        ):
            self.assertRegex(
                output,
                rf"(?m)^\| `{control_id}` \|.*\| {re.escape(spec_126)} \|$",
            )

    def test_canonical_security_leaf_preserves_the_three_signal_boundary(self) -> None:
        security_audit = SECURITY_AUDIT.read_text(encoding="utf-8")
        self.assertIn("satisfies only `SEC-AUTO-008`", security_audit)
        self.assertIn("broad dependency SCA (`SEC-AUTO-012`)", security_audit)
        self.assertIn(
            "container/image vulnerability scanning (`SEC-AUTO-013`)",
            security_audit,
        )

    def test_canonical_automation_leaf_routes_broad_gaps_to_spec_126(self) -> None:
        automation_audit = AUTOMATION_AUDIT.read_text(encoding="utf-8")
        self.assertIn(
            "`SEC-AUTO-012` and `SEC-AUTO-013` remain `Gap`", automation_audit
        )
        self.assertIn(
            "`SEC-AUTO-012` and `SEC-AUTO-013` remain `Gap` and route to "
            "draft Spec 126",
            automation_audit,
        )


if __name__ == "__main__":
    unittest.main()
