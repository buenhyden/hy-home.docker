"""Synthetic and public-source tests for expected observation generation."""

import os
import secrets
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops import compose_observation

ROOT = Path(__file__).resolve().parents[3]


class ObservationTests(unittest.TestCase):
    def test_public_targets_are_derived_and_selection_is_explicit(self):
        rows = compose_observation.inspect_targets(
            ROOT, {"prometheus", "mng-pg-exporter"}
        )
        by_job = {row["job"]: row for row in rows}
        self.assertTrue(by_job["prometheus"]["selected"])
        self.assertTrue(by_job["manage-postgres"]["selected"])
        self.assertFalse(by_job["dev-pg-exporter"]["selected"])
        self.assertGreater(by_job["manage-postgres"]["target_count"], 0)
        self.assertEqual(by_job["prometheus"]["scrape_interval_seconds"], 15)

    def test_duplicate_target_is_rejected_and_distinct_ports_counted(self):
        cfg = {
            "scrape_configs": [
                {
                    "job_name": "web",
                    "static_configs": [{"targets": ["web:80", "web:80"]}],
                }
            ]
        }
        with (
            patch.object(compose_observation, "_configuration", return_value=cfg),
            patch.object(
                compose_observation, "expected_from_root", return_value=(["web"], {})
            ),
            patch.object(compose_observation, "_public", return_value=b""),
        ):
            with self.assertRaisesRegex(
                compose_observation.ObservationError, "duplicate_scrape_target"
            ):
                compose_observation.inspect_targets(ROOT, {"web"})
            cfg["scrape_configs"][0]["static_configs"][0]["targets"][1] = "web:81"
            self.assertEqual(
                compose_observation.inspect_targets(ROOT, {"web"})[0]["target_count"], 2
            )

    def test_invalid_selections_and_intervals_are_rejected(self):
        with self.assertRaisesRegex(
            compose_observation.ObservationError, "unknown_selected_service"
        ):
            compose_observation.inspect_targets(ROOT, {"missing-service"})
        for value in ("0s", "3d", "", 1, "90000s"):
            with (
                self.subTest(value=value),
                self.assertRaises(compose_observation.ObservationError),
            ):
                compose_observation._seconds(value)
        self.assertEqual(compose_observation._seconds("1m"), 60)

    def test_render_rejects_partial_plan(self):
        with patch(
            "scripts.lib.ops.compose_start.validate_plan",
            return_value={"mode": "target"},
        ):
            with self.assertRaisesRegex(
                compose_observation.ObservationError, "partial_selection"
            ):
                compose_observation.render(ROOT, {})

    def test_materialization_preserves_existing_and_rejects_tampering(self):
        fingerprint = "a" * 64
        plan = {"fingerprint": fingerprint}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / "_workspace/repo-support/analysis/p07/selections"
            parent.mkdir(parents=True)
            dest = parent / fingerprint
            with patch.object(
                compose_observation, "render", return_value=(b"config", b"rules", {})
            ):
                plan["dev_data_expected"] = "off"
                overlay = compose_observation.materialize(root, plan, dest)
                self.assertEqual(
                    compose_observation.materialize(root, plan, dest), overlay
                )
                self.assertEqual(
                    compose_observation.validate_materialized(root, plan, overlay),
                    overlay,
                )
                (dest / "selection.yml").write_bytes(b"tampered")
                with self.assertRaisesRegex(
                    compose_observation.ObservationError, "output_mismatch"
                ):
                    compose_observation.materialize(root, plan, dest)
                self.assertEqual((dest / "selection.yml").read_bytes(), b"tampered")

    def test_render_complete_selection(self):
        import yaml

        row = {
            "job": "web",
            "selected_count": 1,
            "target_count": 1,
            "scrape_interval_seconds": 60,
            "selected": True,
        }
        plan = {
            "mode": "profile",
            "observations": [row],
            "fingerprint": "a" * 64,
            "dev_data_expected": "off",
        }
        config = {"scrape_configs": [{"job_name": "web"}], "rule_files": []}
        with (
            patch("scripts.lib.ops.compose_start.validate_plan", return_value=plan),
            patch.object(compose_observation, "_configuration", return_value=config),
        ):
            rendered, rules, meta = compose_observation.render(ROOT, plan)
        self.assertEqual(
            yaml.safe_load(rendered)["scrape_configs"][0]["relabel_configs"][0][
                "replacement"
            ],
            "on",
        )
        self.assertEqual(len(yaml.safe_load(rules)["groups"][0]["rules"]), 5)
        self.assertEqual(meta["dev_data_expected"], "off")
        row["target_count"] = 2
        with (
            patch("scripts.lib.ops.compose_start.validate_plan", return_value=plan),
            patch.object(compose_observation, "_configuration", return_value=config),
        ):
            with self.assertRaisesRegex(
                compose_observation.ObservationError, "mixed_selection_job"
            ):
                compose_observation.render(ROOT, plan)

    def test_new_output_parent_is_created_and_rejects_symlink(self):
        fingerprint = "c" * 64
        plan = {"fingerprint": fingerprint, "dev_data_expected": "off"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = (
                root / "_workspace/repo-support/analysis/p07/selections" / fingerprint
            )
            with patch.object(
                compose_observation, "render", return_value=(b"config", b"rules", {})
            ):
                self.assertTrue(
                    compose_observation.materialize(root, plan, dest).is_file()
                )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_workspace").symlink_to("/tmp", target_is_directory=True)
            dest = (
                root / "_workspace/repo-support/analysis/p07/selections" / fingerprint
            )
            with (
                patch.object(
                    compose_observation,
                    "render",
                    return_value=(b"config", b"rules", {}),
                ),
                self.assertRaises(OSError),
            ):
                compose_observation.materialize(root, plan, dest)

    def test_temporary_output_accepts_group_writable_workspace(self):
        fingerprint = secrets.token_hex(32)
        parent = Path("/tmp") / f"hyhome-p07-{os.geteuid()}"
        parent_existed = parent.exists()
        dest = parent / fingerprint
        plan = {"fingerprint": fingerprint, "dev_data_expected": "off"}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                root.chmod(0o775)
                with patch.object(
                    compose_observation,
                    "render",
                    return_value=(b"config", b"rules", {}),
                ):
                    if Path("/tmp").stat().st_uid != 0:
                        with self.assertRaisesRegex(
                            compose_observation.ObservationError,
                            "unsafe_temporary_root",
                        ):
                            compose_observation.materialize(root, plan, dest)
                        return
                    overlay = compose_observation.materialize(root, plan, dest)
                    self.assertEqual(
                        compose_observation.validate_materialized(root, plan, overlay),
                        overlay,
                    )
                    self.assertEqual(parent.stat().st_mode & 0o777, 0o700)
                    self.assertEqual(dest.stat().st_mode & 0o777, 0o700)
                    dest.chmod(0o755)
                    try:
                        with self.assertRaisesRegex(
                            compose_observation.ObservationError,
                            "unsafe_output_directory",
                        ):
                            compose_observation.validate_materialized(
                                root, plan, overlay
                            )
                    finally:
                        dest.chmod(0o700)
        finally:
            if dest.is_dir():
                for name in ("prometheus.yml", "selection.yml", "overlay.yml"):
                    (dest / name).unlink(missing_ok=True)
                dest.rmdir()
            if not parent_existed and parent.exists():
                try:
                    parent.rmdir()
                except OSError:
                    pass

    def test_group_writable_root_is_rejected_without_changing_mode(self):
        fingerprint = "d" * 64
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.chmod(0o775)
            dest = (
                root / "_workspace/repo-support/analysis/p07/selections" / fingerprint
            )
            plan = {"fingerprint": fingerprint, "dev_data_expected": "off"}
            with patch.object(
                compose_observation, "render", return_value=(b"config", b"rules", {})
            ):
                with self.assertRaisesRegex(
                    compose_observation.ObservationError, "unsafe_output_directory"
                ):
                    compose_observation.materialize(root, plan, dest)
            self.assertEqual(root.stat().st_mode & 0o777, 0o775)
            self.assertFalse(dest.exists())

    def test_materialization_rejects_symlink_output(self):
        fingerprint = "b" * 64
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / "_workspace/repo-support/analysis/p07/selections"
            parent.mkdir(parents=True)
            dest = parent / fingerprint
            dest.symlink_to(root, target_is_directory=True)
            plan = {"fingerprint": fingerprint, "dev_data_expected": "on"}
            with patch.object(
                compose_observation, "render", return_value=(b"config", b"rules", {})
            ):
                with self.assertRaises(OSError):
                    compose_observation.materialize(root, plan, dest)


if __name__ == "__main__":
    unittest.main()
