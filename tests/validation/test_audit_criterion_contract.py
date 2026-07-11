from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATION_DIR = ROOT / "scripts" / "validation"
sys.path.insert(0, str(VALIDATION_DIR))

from audit_criterion_contract import (  # noqa: E402
    AuditCriterionContractError,
    DEFAULT_PACK,
    EXPECTED_TOTAL,
    REPORT_PREFIX_COUNTS,
    split_row,
    validate_pack,
)


class AuditCriterionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.pack = pathlib.Path(self.tempdir.name) / "audit-pack"
        shutil.copytree(ROOT / DEFAULT_PACK, self.pack)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _report(self, name: str = "sdlc-quality-formatting-implementation.md") -> pathlib.Path:
        return self.pack / name

    def _rewrite_criterion(self, criterion_id: str, mutate) -> None:
        report = self._report()
        lines = report.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if line.startswith(f"| {criterion_id} |"):
                cells = split_row(line)
                mutate(cells)
                lines[index] = "| " + " | ".join(cells) + " |"
                report.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return
        self.fail(f"criterion not found in fixture: {criterion_id}")

    def _assert_contract_error(self, expected_text: str) -> None:
        with self.assertRaises(AuditCriterionContractError) as context:
            validate_pack(self.pack)
        self.assertIn(expected_text, "\n".join(context.exception.errors))

    def test_valid_baseline_has_exact_manifest(self) -> None:
        contract = validate_pack(self.pack)
        self.assertEqual(EXPECTED_TOTAL, len(contract.rows))
        self.assertEqual(len(REPORT_PREFIX_COUNTS), len(contract.per_report_counts))
        self.assertEqual(EXPECTED_TOTAL, len({row.criterion_id for row in contract.rows}))

    def test_deleted_row_is_rejected(self) -> None:
        report = self._report()
        lines = [
            line
            for line in report.read_text(encoding="utf-8").splitlines()
            if not line.startswith("| QAF-16 |")
        ]
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self._assert_contract_error("missing criterion IDs: QAF-16")

    def test_malformed_row_is_rejected(self) -> None:
        report = self._report()
        text = report.read_text(encoding="utf-8")
        original = next(line for line in text.splitlines() if line.startswith("| QAF-01 |"))
        report.write_text(text.replace(original, "| QAF-01 | malformed |", 1), encoding="utf-8")
        self._assert_contract_error("malformed criterion row has 2 fields; expected 10")

    def test_blank_field_is_rejected(self) -> None:
        self._rewrite_criterion("QAF-01", lambda cells: cells.__setitem__(1, ""))
        self._assert_contract_error("empty criterion fields: external criterion")

    def test_duplicate_id_is_rejected(self) -> None:
        self._rewrite_criterion("QAF-02", lambda cells: cells.__setitem__(0, "QAF-01"))
        self._assert_contract_error("duplicate criterion IDs: QAF-01")

    def test_generator_rejects_structurally_incomplete_temp_pack(self) -> None:
        report = self._report()
        lines = [
            line
            for line in report.read_text(encoding="utf-8").splitlines()
            if not line.startswith("| QAF-16 |")
        ]
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        env = os.environ.copy()
        env["AUDIT_PACK_DIR"] = str(self.pack)
        result = subprocess.run(
            ["bash", "scripts/validation/generate-audit-implementation-matrix.sh", "--dry-run"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing criterion IDs: QAF-16", result.stderr)

    def test_coverage_check_rejects_blank_field_in_temp_pack(self) -> None:
        self._rewrite_criterion("QAF-01", lambda cells: cells.__setitem__(1, ""))
        result = subprocess.run(
            [
                "bash",
                "scripts/validation/report-audit-pack-coverage.sh",
                "--pack",
                str(self.pack),
                "--check",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("empty criterion fields: external criterion", result.stderr)


if __name__ == "__main__":
    unittest.main()
