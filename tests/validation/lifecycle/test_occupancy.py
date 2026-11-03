"""Active-stage occupancy, including the empty Stage 98 rule."""

import contextlib
import io
import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance.lifecycle import occupancy

ROOT = pathlib.Path(__file__).resolve().parents[3]


class OccupancyTests(unittest.TestCase):
    def test_repository_active_stages_hold_no_misplaced_terminal_document(self) -> None:
        self.assertEqual((), occupancy.validate_active_stage_occupancy(ROOT))

    def test_run_reports_the_count_and_exit_code(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = occupancy.run(ROOT)
        self.assertEqual(0, code)
        self.assertIn("active stage occupancy: violations=0", output.getvalue())

    def test_any_tracked_stage_98_file_but_its_readme_is_a_violation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            archive = root / "docs/98.archive"
            (archive / "superseded/03.specs/0245-x").mkdir(parents=True)
            (archive / "README.md").write_text("# 98.archive\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            self.assertEqual((), occupancy.validate_active_stage_occupancy(root))

            record = archive / "superseded/03.specs/0245-x/spec.md"
            record.write_text("---\nstatus: superseded\n---\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            self.assertEqual(
                (
                    "docs/98.archive/superseded/03.specs/0245-x/spec.md: "
                    "Stage 98 holds no records",
                ),
                occupancy.validate_active_stage_occupancy(root),
            )

    def test_stage_03_membership_comes_from_the_registry(self) -> None:
        self.assertEqual(
            "docs/03.specs/0001-example",
            occupancy._stage_03_package("docs/03.specs/0001-example/spec.md"),
        )
        self.assertIsNone(occupancy._stage_03_package("docs/03.specs/README.md"))


if __name__ == "__main__":
    unittest.main()
