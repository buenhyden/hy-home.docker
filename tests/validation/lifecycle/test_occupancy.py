"""Active-stage occupancy runs without the Stage 98 archive gate."""

import contextlib
import io
import pathlib
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

    def test_stage_03_membership_comes_from_the_registry(self) -> None:
        self.assertEqual(
            "docs/03.specs/0001-example",
            occupancy._stage_03_package("docs/03.specs/0001-example/spec.md"),
        )
        self.assertIsNone(occupancy._stage_03_package("docs/03.specs/README.md"))


if __name__ == "__main__":
    unittest.main()
