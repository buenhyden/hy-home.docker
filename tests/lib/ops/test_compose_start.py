"""Synthetic, non-operational contract tests for companion selection."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.lib.ops import compose_start


class ComposeStartTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "infra").mkdir()
        config = self.root / "infra/06-observability/prometheus/config"
        config.mkdir(parents=True)
        for name in ("prometheus.yml", "prometheus.dev.yml"):
            (config / name).write_text("scrape_configs: []\n", encoding="utf-8")
        scripts = self.root / "infra/06-observability/prometheus/scripts"
        scripts.mkdir(parents=True)
        (scripts / "start.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        policy = (
            self.root
            / "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md"
        )
        policy.parent.mkdir(parents=True)
        policy.write_text(
            "| HOME | `core`, `obs-core` | `automation`, `lifecycle`, `topology` |\n"
            "### Companion, exclusion and side effects\n"
            "| Producer | Explicit targets |\n| --- | --- |\n"
            "| `db` | `db db-provision db-exporter` |\n"
            "| `broker` | `broker broker-exporter` |\n"
            "### Following section\n",
            encoding="utf-8",
        )
        (self.root / "docker-compose.yml").write_text(
            "name: sample-fixture\ninclude:\n  - infra/services.yml\n", encoding="utf-8"
        )
        (self.root / "infra/services.yml").write_text(
            "services:\n"
            "  db:\n    profiles: [core]\n"
            "  db-provision:\n    profiles: [core]\n    depends_on: [db]\n"
            "  db-exporter:\n    profiles: [core]\n    depends_on: [db-provision]\n"
            "  broker:\n    profiles: [other]\n"
            "  broker-exporter:\n    profiles: [other]\n    depends_on: [broker]\n"
            "  importer:\n    profiles: [other]\n    depends_on: [db]\n"
            "  unrelated:\n    profiles: [other]\n"
            "  prometheus:\n    profiles: [obs-core]\n",
            encoding="utf-8",
        )
        self.inspect = mock.patch.object(
            compose_start, "_inspect_targets", return_value=[]
        )
        self.inspect.start()
        self.addCleanup(self.inspect.stop)

    def plan(self, mode, values, expected=None):
        return compose_start.create_plan(
            self.root, mode=mode, values=values, dev_data_expected=expected
        )

    def test_direct_and_indirect_companions_close_without_profile_siblings(self):
        plan = self.plan("target", ["importer"])
        self.assertEqual(
            set(plan["targets"]), {"importer", "db", "db-provision", "db-exporter"}
        )
        self.assertNotIn("unrelated", plan["targets"])
        self.assertEqual(len(plan["targets"]), len(set(plan["targets"])))

    def test_complete_profile_and_home_selections(self):
        home = self.plan("home", [], "off")
        self.assertEqual(set(home["profiles"]), {"core", "obs-core"})
        self.assertIn("prometheus", home["targets"])
        self.assertNotIn("broker", home["targets"])
        profile = self.plan("profile", ["other"], "off")
        self.assertIn("broker-exporter", profile["targets"])
        self.assertIn("db-exporter", profile["targets"])

    def test_unknown_selection_and_invalid_expected_fail(self):
        for mode, values, expected in [
            ("target", ["--help"], None),
            ("target", ["unknown"], None),
            ("profile", ["missing"], "off"),
            ("home", [], "on"),
            ("home", [], None),
        ]:
            with (
                self.subTest(mode=mode, values=values, expected=expected),
                self.assertRaises(ValueError),
            ):
                self.plan(mode, values, expected)

    def test_changed_source_and_tampered_targets_fail_revalidation(self):
        plan = self.plan("target", ["db"])
        altered = {**plan, "targets": ["db"]}
        with self.assertRaises(ValueError):
            compose_start.validate_plan(self.root, altered)
        file = self.root / "infra/services.yml"
        file.write_text(file.read_text() + "# changed\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            compose_start.validate_plan(self.root, plan)

    def test_missing_companion_and_dependency_cycle_rejected(self):
        file = self.root / "infra/services.yml"
        original = file.read_text()
        file.write_text(original.replace("  db-exporter:", "  unknown-exporter:"))
        with self.assertRaises(ValueError):
            self.plan("target", ["db"])
        file.write_text(
            original.replace(
                "  db:\n    profiles: [core]",
                "  db:\n    profiles: [core]\n    depends_on: [db-exporter]",
            )
        )
        with self.assertRaises(ValueError):
            self.plan("target", ["db"])

    def test_parent_directory_symlink_is_not_followed(self):
        path = self.root / "infra/services.yml"
        path.unlink()
        path.symlink_to("/etc/passwd")
        with self.assertRaises((OSError, ValueError)):
            self.plan("target", ["db"])

    def test_malformed_or_duplicate_selection_authority_is_rejected(self):
        path = self.root / "infra/services.yml"
        original = path.read_text()
        mutations = [
            original.replace("depends_on: [db]", "depends_on: forbidden"),
            original.replace("depends_on: [db]", "depends_on: [db, db]"),
            original.replace("depends_on: [db]", "depends_on: {db: {required: maybe}}"),
            original.replace(
                "depends_on: [db]", "depends_on: {db: {condition: invalid}}"
            ),
            original.replace("profiles: [core]", "profiles: [core, core]", 1),
            original.replace("profiles: [core]", "profiles: !override [core]", 1),
            original + "  db:\n    profiles: [other]\n",
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutations.index(mutation)):
                path.write_text(mutation)
                with self.assertRaises(ValueError):
                    self.plan("target", ["db"])

    def test_optional_dependency_never_starts_outside_plan(self):
        import subprocess

        import yaml

        path = self.root / "infra/services.yml"
        original = path.read_text().replace(
            "  importer:\n    profiles: [other]\n    depends_on: [db]",
            "  importer:\n    profiles: [other]\n    depends_on: {db: {condition: service_started}, broker: {condition: service_started, required: false}}",
            1,
        )
        path.write_text(original)
        plan = self.plan("target", ["importer"])
        self.assertIn("broker", plan["targets"])
        self.assertIn("broker-exporter", plan["targets"])
        self.assertIn("optional-dependency:importer", plan["reasons"]["broker"])
        for active in (True, False):
            source = (
                original
                if active
                else original.replace(
                    "  broker:\n    profiles: [other]",
                    "  broker:\n    profiles: [isolated]",
                )
            )
            path.write_text(source)
            plan = self.plan("target", ["importer"])
            self.assertEqual("broker" in plan["targets"], active)
            data = yaml.safe_load(source)
            data["services"] = {
                name: data["services"][name] for name in ("importer", "db", "broker")
            }
            for service in data["services"].values():
                service["image"] = "synthetic/example"
            render = self.root / "render.yml"
            render.write_text(yaml.safe_dump(data))
            result = subprocess.run(
                [
                    "/usr/bin/docker",
                    "compose",
                    "--env-file",
                    "/dev/null",
                    "-f",
                    str(render),
                    "--profile",
                    "core",
                    "--profile",
                    "other",
                    "config",
                    "--services",
                    "importer",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual("broker" in result.stdout.splitlines(), active)
            self.assertTrue(
                set(result.stdout.splitlines()) <= set(plan["targets"]),
                (result.stdout, plan["targets"]),
            )

    def test_up_recomputes_plan_and_uses_only_explicit_targets(self):
        plan = self.plan("target", ["importer"])
        run = mock.Mock(return_value=mock.Mock(returncode=0))
        with mock.patch.dict(
            "os.environ",
            {
                "COMPOSE_FILE": "/outside/evil.yml",
                "COMPOSE_PROFILES": "all",
                "DOCKER_HOST": "tcp://outside:2375",
                "SECRET_VALUE": "private-canary",
            },
        ):
            result = compose_start.execute_plan(self.root, plan, runner=run)
        self.assertEqual(result["result"], "STARTED")
        argv = run.call_args.args[0]
        self.assertEqual(
            argv[:5],
            [
                "/usr/bin/docker",
                "--host",
                "unix:///var/run/docker.sock",
                "compose",
                "--project-name",
            ],
        )
        self.assertIn("--no-build", argv)
        self.assertEqual(argv[argv.index("--pull") + 1], "never")
        self.assertEqual(set(argv[argv.index("never") + 1 :]), set(plan["targets"]))
        env = run.call_args.kwargs["env"]
        self.assertNotIn("COMPOSE_FILE", env)
        self.assertNotIn("COMPOSE_PROFILES", env)
        self.assertNotIn("DOCKER_HOST", env)
        self.assertNotIn("SECRET_VALUE", env)

    def test_partial_prometheus_and_stale_plan_never_execute(self):
        run = mock.Mock()
        plan = self.plan("target", ["prometheus"])
        with self.assertRaises(ValueError):
            compose_start.execute_plan(self.root, plan, runner=run)
        stale = self.plan("target", ["db"])
        changed = self.root / "infra/services.yml"
        changed.write_text(changed.read_text() + "# stale\n")
        with self.assertRaises(ValueError):
            compose_start.execute_plan(self.root, stale, runner=run)
        run.assert_not_called()

    def test_failed_execution_is_redacted_and_no_retries_occur(self):
        plan = self.plan("target", ["db"])
        run = mock.Mock(
            return_value=mock.Mock(
                returncode=17, stdout=b"secret-canary", stderr=b"secret-canary"
            )
        )
        result = compose_start.execute_plan(self.root, plan, runner=run)
        self.assertEqual(result["result"], "START_FAILED")
        self.assertNotIn("secret-canary", repr(result))
        self.assertTrue(result["recovery_required"])
        run.assert_called_once()

    def test_plan_file_is_bounded_confined_and_rejects_duplicate_json(self):
        folder = self.root / "_workspace/repo-support/analysis/p07/plans"
        folder.mkdir(parents=True)
        path = folder / "plan.json"
        path.write_text('{"mode":"target","mode":"home"}')
        with self.assertRaises(ValueError):
            compose_start.load_plan(self.root, path)
        path.write_text('{"mode":"target"}')
        self.assertEqual(compose_start.load_plan(self.root, path), {"mode": "target"})
        with self.assertRaises(ValueError):
            compose_start.load_plan(self.root, self.root / "docker-compose.yml")
        path.unlink()
        path.symlink_to(self.root / "docker-compose.yml")
        with self.assertRaises((OSError, ValueError)):
            compose_start.load_plan(self.root, path)

    def test_timeout_requires_recovery_without_retry(self):
        import subprocess

        plan = self.plan("target", ["db"])
        run = mock.Mock(side_effect=subprocess.TimeoutExpired("ignored", 300))
        self.assertEqual(
            compose_start.execute_plan(self.root, plan, runner=run),
            {"result": "START_FAILED", "recovery_required": True},
        )
        run.assert_called_once()

    def test_full_plan_binds_validated_overlay_before_execution(self):
        import os

        plan = self.plan("home", [], "off")
        overlay = self.root / "synthetic-overlay.yml"
        run = mock.Mock(return_value=mock.Mock(returncode=0))
        with (
            mock.patch(
                "scripts.lib.ops.compose_observation.materialize", return_value=overlay
            ) as materialize,
            mock.patch(
                "scripts.lib.ops.compose_observation.validate_materialized"
            ) as validate,
        ):
            result = compose_start.execute_plan(self.root, plan, runner=run)
        self.assertEqual(result["result"], "STARTED")
        self.assertEqual(materialize.call_args.args[2].name, plan["fingerprint"])
        self.assertEqual(
            materialize.call_args.args[2].parent,
            Path("/tmp") / f"hyhome-p07-{os.geteuid()}",
        )
        validate.assert_called_once_with(self.root, plan, overlay)
        self.assertIn(str(overlay), run.call_args.args[0])

    def test_overlay_failure_preserves_execution_boundary(self):
        plan = self.plan("home", [], "off")
        run = mock.Mock()
        with mock.patch(
            "scripts.lib.ops.compose_observation.materialize",
            side_effect=ValueError("failure"),
        ):
            with self.assertRaises(ValueError):
                compose_start.execute_plan(self.root, plan, runner=run)
        run.assert_not_called()

    def test_public_workspace_full_plan_and_synthetic_runner(self):
        import os

        workspace = Path(__file__).resolve().parents[3]
        self.inspect.stop()
        plan = compose_start.create_plan(
            workspace, mode="home", values=[], dev_data_expected="off"
        )
        expected_dir = Path("/tmp") / f"hyhome-p07-{os.geteuid()}" / plan["fingerprint"]
        overlay = expected_dir / "overlay.yml"
        runner = mock.Mock(return_value=mock.Mock(returncode=0))
        with (
            mock.patch(
                "scripts.lib.ops.compose_observation.materialize", return_value=overlay
            ) as materialize,
            mock.patch(
                "scripts.lib.ops.compose_observation.validate_materialized"
            ) as validate,
        ):
            result = compose_start.execute_plan(workspace, plan, runner=runner)
        self.assertEqual(result["result"], "STARTED")
        materialize.assert_called_once_with(workspace, plan, expected_dir)
        validate.assert_called_once_with(workspace, plan, overlay)
        self.assertIn(str(overlay), runner.call_args.args[0])

        runner.reset_mock()
        with mock.patch(
            "scripts.lib.ops.compose_observation.materialize",
            side_effect=ValueError("unsafe_parent"),
        ):
            with self.assertRaises(ValueError):
                compose_start.execute_plan(workspace, plan, runner=runner)
        runner.assert_not_called()

    def test_cli_rejects_bad_input_without_echoing_it(self):
        import subprocess
        import sys

        script = (
            Path(__file__).resolve().parents[3] / "scripts/operations/compose-start.py"
        )
        result = subprocess.run(
            [sys.executable, str(script), "plan", "--selection", "secret-canary"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("secret-canary", result.stdout + result.stderr)

    def test_real_public_source_cli_plan(self):
        import json
        import subprocess
        import sys

        script = (
            Path(__file__).resolve().parents[3] / "scripts/operations/compose-start.py"
        )
        result = subprocess.run(
            [sys.executable, str(script), "plan", "--target", "mng-pg-init"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        plan = json.loads(result.stdout)
        self.assertIn("mng-pg-init", plan["targets"])
        self.assertIn("mng-pg-exporter", plan["targets"])

    def test_cli_main_success_failure_and_up_dispatch(self):
        import contextlib
        import importlib.util
        import io

        script = (
            Path(__file__).resolve().parents[3] / "scripts/operations/compose-start.py"
        )
        spec = importlib.util.spec_from_file_location("p07_cli_test", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            mock.patch.object(module, "create_plan", return_value={"targets": ["db"]}),
        ):
            self.assertEqual(module.main(["plan", "--target", "db"]), 0)
        self.assertIn("db", output.getvalue())
        with (
            contextlib.redirect_stdout(io.StringIO()),
            mock.patch.object(module, "create_plan", side_effect=ValueError("secret")),
        ):
            self.assertEqual(module.main(["plan", "--target", "db"]), 2)
        with (
            contextlib.redirect_stdout(io.StringIO()),
            mock.patch.object(module, "load_plan", return_value={}),
            mock.patch.object(
                module, "execute_plan", return_value={"result": "START_FAILED"}
            ),
        ):
            self.assertEqual(module.main(["up", "--plan", "ignored"]), 1)


if __name__ == "__main__":
    unittest.main()
