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

    def test_a_non_ascii_stage_98_name_is_still_a_violation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            record = root / "docs/98.archive/보존 기록.md"
            record.parent.mkdir(parents=True)
            record.write_text("# 기록\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            self.assertEqual(
                ("docs/98.archive/보존 기록.md: Stage 98 holds no records",),
                occupancy.validate_active_stage_occupancy(root),
            )

    def test_a_git_failure_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            # Not a repository: the tracked inventory cannot be read.
            self.assertEqual(
                ("docs: tracked file inventory is unavailable",),
                occupancy.validate_active_stage_occupancy(pathlib.Path(directory)),
            )

    def test_a_missing_git_binary_fails_closed(self) -> None:
        from unittest import mock

        with mock.patch.object(
            occupancy.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            self.assertEqual(
                ("docs: tracked file inventory is unavailable",),
                occupancy.validate_active_stage_occupancy(ROOT),
            )

    def _tracked(self, files: dict[str, str]) -> tuple[str, ...]:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            for relative, status in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"---\nstatus: {status}\n---\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            return occupancy.validate_active_stage_occupancy(root)

    def test_a_retired_standalone_document_cannot_stay_active(self) -> None:
        guide = "docs/05.operations/guides/02-gateway-and-networking/0999-x.md"
        self.assertEqual((), self._tracked({guide: "active"}))
        self.assertEqual(
            (f"{guide}: retired document remains in an active stage",),
            self._tracked({guide: "retired"}),
        )

    def test_a_cancelled_spec_package_keeps_no_member(self) -> None:
        package = "docs/03.specs/0999-x"
        self.assertEqual(
            (
                f"{package}/plan.md: package with a terminal Spec keeps no "
                "member in an active stage",
                f"{package}/spec.md: package with a terminal Spec keeps no "
                "member in an active stage",
            ),
            self._tracked(
                {f"{package}/spec.md": "cancelled", f"{package}/plan.md": "cancelled"}
            ),
        )

    def test_a_terminal_plan_cannot_sit_in_an_open_package(self) -> None:
        package = "docs/03.specs/0999-x"
        self.assertEqual(
            (),
            self._tracked(
                {f"{package}/spec.md": "approved", f"{package}/plan.md": "approved"}
            ),
        )
        self.assertEqual(
            (f"{package}/plan.md: cancelled member violates package occupancy",),
            self._tracked(
                {f"{package}/spec.md": "approved", f"{package}/plan.md": "cancelled"}
            ),
        )

    def test_stage_03_membership_comes_from_the_registry(self) -> None:
        self.assertEqual(
            "docs/03.specs/0001-example",
            occupancy._stage_03_package("docs/03.specs/0001-example/spec.md"),
        )
        self.assertIsNone(occupancy._stage_03_package("docs/03.specs/README.md"))


if __name__ == "__main__":
    unittest.main()
