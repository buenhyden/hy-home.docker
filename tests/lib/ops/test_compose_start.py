"""Synthetic, non-operational contract tests for companion selection."""

from __future__ import annotations

import json
import subprocess
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
            / "docs/05.operations/02.policies/01.common/0078-compose-profile-vocabulary.md"
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
            "  prometheus:\n    profiles: [obs-core]\n"
            "  dev-pg:\n    profiles: [dev-data]\n",
            encoding="utf-8",
        )
        self.inspect = mock.patch.object(
            compose_start, "_inspect_targets", return_value=[]
        )
        self.inspect.start()
        self.addCleanup(self.inspect.stop)
        admission = mock.Mock()
        admission.release.return_value = True
        self.admission = mock.patch.object(
            compose_start,
            "_operating_admission",
            return_value=(admission, {"token": "fixture-start"}, mock.Mock()),
        )
        self.admission.start()
        self.addCleanup(self.admission.stop)

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

    def test_same_host_binding_in_one_selection_is_rejected(self):
        gateway = (
            "    ports:\n"
            "      - ${HOST_LAN_BIND_IP:-192.168.0.13}:${HTTP_HOST_PORT:-80}:${HTTP_PORT:-80}\n"
        )
        (self.root / "infra/services.yml").write_text(
            "services:\n"
            "  traefik:\n    profiles: [core]\n"
            + gateway
            + "  nginx:\n    profiles: [nginx]\n"
            + gateway
            + "  other-port:\n    profiles: [nginx]\n    ports:\n"
            "      - ${HOST_LAN_BIND_IP:-192.168.0.13}:${HTTPS_HOST_PORT:-443}:443/tcp\n"
            "  udp-only:\n    profiles: [core]\n    ports:\n"
            "      - ${HOST_LAN_BIND_IP:-192.168.0.13}:${HTTP_HOST_PORT:-80}:80/udp\n"
            "  prometheus:\n    profiles: [obs-core]\n",
            encoding="utf-8",
        )
        with mock.patch.object(compose_start, "_sources") as sources:
            services = compose_start.yaml.safe_load(
                (self.root / "infra/services.yml").read_text()
            )["services"]
            sources.return_value = (services, ["core"], {}, {})
            self.assertIn("traefik", self.plan("profile", ["core"], "off")["targets"])
            self.assertIn("nginx", self.plan("profile", ["nginx"], "off")["targets"])
            for mode, values, expected in [
                ("profile", ["core", "nginx"], "off"),
                ("target", ["traefik", "nginx"], None),
            ]:
                with self.assertRaisesRegex(ValueError, "host_port_conflict"):
                    self.plan(mode, values, expected)

    def test_home_adds_dev_data_only_when_declared_on(self):
        on = self.plan("home", [], "on")
        self.assertIn("dev-data", on["profiles"])
        self.assertIn("dev-pg", on["targets"])
        off = self.plan("home", [], "off")
        self.assertNotIn("dev-data", off["profiles"])
        self.assertNotIn("dev-pg", off["targets"])

    def test_unknown_selection_and_invalid_expected_fail(self):
        for mode, values, expected in [
            ("target", ["--help"], None),
            ("target", ["unknown"], None),
            ("profile", ["missing"], "off"),
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

    def test_p07_up_reserves_before_start_and_verifies_handoff(self):
        plan = self.plan("target", ["db"])
        admission, verifier = mock.Mock(), mock.Mock()
        claimed = {"token": "owned-start"}

        def start(*args, **kwargs):
            admission.attach.assert_called_once_with(
                "owned-start", identity=None, resource_type="operating-start"
            )
            return mock.Mock(returncode=0)

        with mock.patch.object(
            compose_start,
            "_operating_admission",
            return_value=(admission, claimed, verifier),
            create=True,
        ):
            self.assertEqual(
                "STARTED",
                compose_start.execute_plan(self.root, plan, runner=start)["result"],
            )
        admission.release.assert_called_once_with("owned-start", verify=verifier)

    def test_closed_controller_cleanup_failure_does_not_claim_start_failed(self):
        from scripts.lib.ops import dispatch_process

        plan = self.plan("target", ["db"])
        admission = mock.Mock()
        admission.release.return_value = True
        with (
            mock.patch.object(
                compose_start,
                "_operating_admission",
                return_value=(admission, {"token": "owned-start"}, mock.Mock()),
            ),
            mock.patch.object(
                dispatch_process,
                "run_registered_docker",
                return_value=mock.Mock(returncode=0),
            ),
            mock.patch.object(
                dispatch_process, "cleanup_registered_docker", return_value=False
            ),
        ):
            result = compose_start.execute_plan(self.root, plan)
        self.assertEqual("STARTED", result["result"])
        self.assertFalse(result["recovery_required"])
        self.assertTrue(result["cleanup_pending"])

    def test_p07_partial_or_unknown_start_keeps_reservation(self):
        plan = self.plan("target", ["db"])
        admission = mock.Mock()
        with mock.patch.object(
            compose_start,
            "_operating_admission",
            return_value=(admission, {"token": "owned-start"}, mock.Mock()),
            create=True,
        ):
            result = compose_start.execute_plan(
                self.root, plan, runner=mock.Mock(return_value=mock.Mock(returncode=1))
            )
        self.assertTrue(result["recovery_required"])
        admission.release.assert_not_called()

    def test_nonzero_controller_result_returns_only_a_bounded_failure_code(self):
        plan = self.plan("target", ["db"])
        admission = mock.Mock()
        with mock.patch.object(
            compose_start,
            "_operating_admission",
            return_value=(admission, {"token": "owned-start"}, mock.Mock()),
        ):
            result = compose_start.execute_plan(
                self.root,
                plan,
                runner=mock.Mock(
                    return_value=mock.Mock(
                        returncode=7,
                        stderr="private-secret-must-not-escape",
                    )
                ),
            )
        self.assertEqual("controller_exit_7", result["failure"])
        self.assertNotIn("private-secret", str(result))

    def test_any_error_or_interrupt_after_the_claim_keeps_its_token(self):
        for error, failure in ((KeyError("x"), "controller_error"),
                               (subprocess.TimeoutExpired("docker", 300), "controller_error"),
                               (KeyboardInterrupt(), "interrupted")):  # fmt: skip
            with self.subTest(error=type(error).__name__):
                plan = self.plan("target", ["db"])
                with (
                    mock.patch.object(
                        compose_start,
                        "_operating_admission",
                        return_value=(
                            mock.Mock(),
                            {"token": "owned-start"},
                            mock.Mock(),
                        ),
                    ),
                    mock.patch(
                        "scripts.lib.ops.dispatch_process.run_registered_docker",
                        side_effect=error,
                    ),
                ):
                    result = compose_start.execute_plan(self.root, plan)
                self.assertEqual("owned-start", result["recovery_token"])
                self.assertEqual(failure, result["failure"])

    def test_registered_process_and_lab_errors_return_recovery_result(self):
        from scripts.lib.ops.dispatch_process import ProcessError
        from scripts.operations.lab import LabError

        for error in (ProcessError("spawn failed"), LabError("observe failed")):
            with self.subTest(error=type(error).__name__):
                plan = self.plan("target", ["db"])
                admission = mock.Mock()
                with (
                    mock.patch.object(
                        compose_start,
                        "_operating_admission",
                        return_value=(admission, {"token": "owned-start"}, mock.Mock()),
                    ),
                    mock.patch(
                        "scripts.lib.ops.dispatch_process.run_registered_docker",
                        side_effect=error,
                    ),
                ):
                    result = compose_start.execute_plan(self.root, plan)
                self.assertEqual(
                    {
                        "result": "START_FAILED",
                        "recovery_required": True,
                        "recovery_token": "owned-start",
                        "failure": "controller_error",
                    },
                    result,
                )
                admission.release.assert_not_called()

    def test_recover_releases_only_absent_or_fully_accounted_owned_resources(self):
        from scripts.lib.ops import dispatch_process

        record = {
            "token": "a" * 32,
            "kind": "compose-start",
            "workspace_id": "workspace",
            "binding_id": "binding",
            "daemon_id": "daemon",
            "project": "hy-home-operating",
            "services": ["db", "api"],
            "owner": {"pid": 1, "start_ticks": 1, "boot_id": "boot", "pgid": 1},
            "metadata": {
                "docker_operation_dir": "/private/operations/" + "a" * 32,
                "docker_operation_token": "b" * 32,
                "one_shot_services": ["api"],
            },
        }
        admission = mock.Mock(
            workspace_id="workspace",
            binding_id="binding",
            daemon_id="daemon",
        )
        admission.records.return_value = [record]
        admission.release.side_effect = lambda token, verify: verify(record)
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch("scripts.operations.lab.running_containers", return_value=[]),
            mock.patch.object(
                dispatch_process, "verify_registered_docker_absent", return_value=True
            ) as verify,
            mock.patch.object(
                dispatch_process, "cleanup_registered_docker", return_value=True
            ),
        ):
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {
                "result": "RECOVERED",
                "cleanup_pending": False,
                "incomplete_services": ["api", "db"],
            },
            result,
        )
        verify.assert_any_call(record, stop=True)
        admission.release.assert_called_once()

        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch(
                "scripts.operations.lab.running_containers",
                return_value=[
                    {
                        "project": record["project"],
                        "service": "db",
                        "running": True,
                    }
                ],
            ),
            mock.patch.object(
                dispatch_process, "verify_registered_docker_absent", return_value=True
            ),
            mock.patch.object(
                dispatch_process, "cleanup_registered_docker", return_value=True
            ),
        ):
            admission.release.reset_mock()
            admission.release.side_effect = lambda token, verify: verify(record)
            # A running container the live inventory does not account for.
            admission.observe.return_value = {"services": []}
            result = compose_start.recover_start(self.root, record["token"])
            self.assertEqual(
                {
                    "result": "RECOVERY_BLOCKED",
                    "reason": "resources_partial_or_unknown",
                },
                result,
            )
            # A partial start whose running containers are accounted releases.
            admission.observe.return_value = {"services": ["db"]}
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {
                "result": "RECOVERED",
                "cleanup_pending": False,
                "incomplete_services": ["api"],
            },
            result,
        )

        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch(
                "scripts.operations.lab.running_containers",
                return_value=[
                    {"project": record["project"], "service": "db", "running": True},
                    {
                        "project": record["project"],
                        "service": "api",
                        "running": False,
                        "status": "exited",
                        "exit_code": 0,
                    },
                ],
            ),
            mock.patch.object(
                dispatch_process, "verify_registered_docker_absent", return_value=True
            ),
            mock.patch.object(
                dispatch_process, "cleanup_registered_docker", return_value=True
            ),
        ):
            admission.observe.return_value = {
                "services": ["db"],
                "budget": {"cpus": 1, "memory_bytes": 1, "disk_bytes": 1},
            }
            admission.release.reset_mock()
            admission.release.side_effect = lambda token, verify: verify(record)
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual({"result": "RECOVERED", "cleanup_pending": False}, result)

    def test_recover_refuses_a_start_whose_process_is_still_running(self):
        record = {
            "token": "a" * 32,
            "kind": "compose-start",
            "workspace_id": "workspace",
            "binding_id": "binding",
            "daemon_id": "daemon",
            "project": "hy-home-operating",
            "services": ["db"],
            "owner": {"pid": 1, "start_ticks": 1, "boot_id": "boot", "pgid": 1},
            "metadata": {"one_shot_services": []},
        }
        admission = mock.Mock(
            workspace_id="workspace", binding_id="binding", daemon_id="daemon"
        )
        admission.records.return_value = [record]
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch(
                "scripts.lib.ops.environment_admission.process_status",
                return_value="alive",
            ),
        ):
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {"result": "RECOVERY_BLOCKED", "reason": "start_still_running"}, result
        )
        admission.release.assert_not_called()

    def test_recover_without_a_token_finds_only_owned_abandoned_starts(self):
        def claim(token, kind="compose-start", workspace="workspace"):
            return {
                "token": token,
                "kind": kind,
                "workspace_id": workspace,
                "binding_id": "binding",
                "daemon_id": "daemon",
                "owner": {"pid": int(token[0], 16) + 1},
            }

        dead, live = claim("a" * 32), claim("b" * 32)
        lab_claim, foreign = claim("c" * 32, kind="lab"), claim("d" * 32, "x", "other")
        admission = mock.Mock(
            workspace_id="workspace", binding_id="binding", daemon_id="daemon"
        )
        admission.records.return_value = [dead, live, lab_claim, foreign]
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch(
                "scripts.lib.ops.environment_admission.process_status",
                side_effect=lambda owner: "alive" if owner["pid"] == 12 else "absent",
            ),
            mock.patch.object(
                compose_start,
                "recover_start",
                return_value={"result": "RECOVERED", "cleanup_pending": False},
            ) as recover,
        ):
            result = compose_start.recover_abandoned(self.root)
        recover.assert_called_once_with(self.root, dead["token"])
        self.assertEqual("RECOVERED", result["result"])
        self.assertEqual([dead["token"]], list(result["claims"]))

    def test_recover_releases_a_claim_that_never_recorded_its_job_policy(self):
        # admission.update failed before any Docker effect, so there is no
        # one_shot_services, no operation directory and nothing to account.
        record = {
            "token": "d" * 32,
            "kind": "compose-start",
            "workspace_id": "workspace",
            "binding_id": "binding",
            "daemon_id": "daemon",
            "project": "hy-home-operating",
            "services": ["db"],
            "owner": {"pid": 1, "start_ticks": 1, "boot_id": "boot", "pgid": 1},
            "metadata": {},
        }
        admission = mock.Mock(
            workspace_id="workspace", binding_id="binding", daemon_id="daemon"
        )
        admission.records.return_value = [record]
        admission.release.side_effect = lambda token, verify: verify(record)
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch("scripts.operations.lab.running_containers", return_value=[]),
            mock.patch(
                "scripts.lib.ops.environment_admission.process_status",
                return_value="absent",
            ),
            mock.patch(
                "scripts.lib.ops.dispatch_process.cleanup_unstarted_registered_docker",
                return_value=True,
            ),
        ):
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {
                "result": "RECOVERED",
                "cleanup_pending": False,
                "incomplete_services": ["db"],
            },
            result,
        )

    def test_recover_cleans_a_pre_controller_setup_failure_before_release(self):
        from scripts.lib.ops import dispatch_process

        record = {
            "token": "c" * 32,
            "kind": "compose-start",
            "workspace_id": "workspace",
            "binding_id": "binding",
            "daemon_id": "daemon",
            "project": "hy-home-operating",
            "services": ["db"],
            "owner": {"pid": 1, "start_ticks": 1, "boot_id": "boot", "pgid": 1},
            "metadata": {
                "docker_operation_dir": "/private/operations/" + "c" * 32,
                "one_shot_services": [],
            },
        }
        admission = mock.Mock(
            workspace_id="workspace",
            binding_id="binding",
            daemon_id="daemon",
        )
        admission.records.return_value = [record]
        admission.release.side_effect = lambda token, verify: verify(record)
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch(
                "scripts.lib.ops.environment_admission.process_status",
                return_value="absent",
            ),
            mock.patch("scripts.operations.lab.running_containers", return_value=[]),
            mock.patch.object(
                dispatch_process,
                "cleanup_unstarted_registered_docker",
                return_value=True,
            ) as cleanup,
        ):
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {
                "result": "RECOVERED",
                "cleanup_pending": False,
                "incomplete_services": ["db"],
            },
            result,
        )
        cleanup.assert_called_once_with(record)
        admission.release.assert_called_once()

        record["metadata"] = {"one_shot_services": []}
        with (
            mock.patch(
                "scripts.operations.lab.execution_admission", return_value=admission
            ),
            mock.patch("scripts.operations.lab.running_containers", return_value=[]),
            mock.patch(
                "scripts.lib.ops.environment_admission.process_status",
                return_value="absent",
            ),
        ):
            admission.release.reset_mock()
            admission.release.side_effect = lambda token, verify: verify(record)
            result = compose_start.recover_start(self.root, record["token"])
        self.assertEqual(
            {
                "result": "RECOVERED",
                "cleanup_pending": False,
                "incomplete_services": ["db"],
            },
            result,
        )

    def write_env(self, value):
        (self.root / "infra/overlay.yml").write_text(
            "services:\n  db:\n    environment:\n      MODE: overlay\n",
            encoding="utf-8",
        )
        (self.root / ".env").write_text(
            "OTHER_SECRET=private-canary\n" + f"COMPOSE_FILE={value}\n",
            encoding="utf-8",
        )

    def test_root_file_only_compose_file_is_accepted(self):
        for value in ('"docker-compose.yml"', "docker-compose.yml"):
            with self.subTest(value=value):
                self.write_env(value)
                plan = self.plan("target", ["db"])
                self.assertEqual(["docker-compose.yml"], plan["compose_files"])
                self.assertNotIn("private-canary", json.dumps(plan))

    def test_missing_dotenv_keeps_the_root_file_only(self):
        self.assertEqual(
            ["docker-compose.yml"], self.plan("target", ["db"])["compose_files"]
        )

    def test_any_compose_file_overlay_is_rejected(self):
        for value in (
            "docker-compose.yml:infra/overlay.yml",
            "infra/overlay.yml",
            "infra/overlay.yml:docker-compose.yml",
            "docker-compose.yml:/etc/evil.yml",
            "docker-compose.yml:../evil.yml",
            "docker-compose.yml:infra/absent.yml",
        ):
            with self.subTest(value=value):
                self.write_env(value)
                with self.assertRaisesRegex(
                    ValueError, "compose_file_overlay_forbidden"
                ):
                    self.plan("target", ["db"])

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
            {
                "result": "START_FAILED",
                "recovery_required": True,
                "recovery_token": "fixture-start",
                "failure": "controller_error",
            },
        )
        run.assert_called_once()

    def test_full_plan_binds_validated_overlay_before_execution(self):
        from scripts.lib.ops import compose_observation

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
            compose_observation.overlay_root(),
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

    def test_every_airflow_metrics_producer_brings_the_statsd_exporter(self):
        workspace = Path(__file__).resolve().parents[3]
        self.inspect.stop()
        for producer in (
            "airflow-apiserver",
            "airflow-scheduler",
            "airflow-triggerer",
            "airflow-dag-processor",
            "airflow-worker",
        ):
            with self.subTest(producer=producer):
                plan = compose_start.create_plan(
                    workspace, mode="target", values=[producer]
                )
                self.assertIn("airflow-statsd-exporter", plan["targets"])
        # A direct scheduler start adds its exporter, not the whole Airflow stack.
        plan = compose_start.create_plan(
            workspace, mode="target", values=["airflow-scheduler"]
        )
        self.assertNotIn("airflow-apiserver", plan["targets"])
        self.assertNotIn("airflow-worker", plan["targets"])

    def test_public_workspace_full_plan_and_synthetic_runner(self):
        from scripts.lib.ops import compose_observation

        workspace = Path(__file__).resolve().parents[3]
        self.inspect.stop()
        plan = compose_start.create_plan(
            workspace, mode="home", values=[], dev_data_expected="off"
        )
        expected_dir = compose_observation.overlay_root() / plan["fingerprint"]
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
        interrupted = io.StringIO()
        with (
            contextlib.redirect_stdout(interrupted),
            mock.patch.object(module, "create_plan", side_effect=KeyboardInterrupt),
        ):
            # Before any claim exists an interrupt leaves nothing to recover.
            self.assertEqual(module.main(["plan", "--target", "db"]), 130)
        self.assertEqual('{"result": "BLOCKED"}\n', interrupted.getvalue())
        failed_output = io.StringIO()
        with (
            contextlib.redirect_stdout(failed_output),
            mock.patch.object(module, "load_plan", return_value={}),
            mock.patch.object(
                module,
                "execute_plan",
                return_value={
                    "result": "START_FAILED",
                    "failure": "controller_exit_7",
                },
            ),
        ):
            self.assertEqual(module.main(["up", "--plan", "ignored"]), 1)
        self.assertIn("controller_exit_7", failed_output.getvalue())
        from scripts.operations.lab import LabError

        blocked = io.StringIO()
        with (
            contextlib.redirect_stdout(blocked),
            mock.patch.object(module, "load_plan", return_value={}),
            mock.patch.object(
                module, "execute_plan", side_effect=LabError("daemon unavailable")
            ),
        ):
            # A failure before any claim exists is a structured BLOCKED.
            self.assertEqual(module.main(["up", "--plan", "ignored"]), 2)
        self.assertEqual('{"result": "BLOCKED"}', blocked.getvalue().strip())
        with (
            contextlib.redirect_stdout(io.StringIO()),
            mock.patch.object(
                module,
                "recover_start",
                return_value={"result": "RECOVERED", "cleanup_pending": False},
            ) as recover,
        ):
            self.assertEqual(module.main(["recover", "--token", "a" * 32]), 0)
        recover.assert_called_once_with(module.ROOT, "a" * 32)


class OperatingAdmissionHandoffTests(unittest.TestCase):
    def test_pre_controller_setup_failure_releases_the_exact_pending_claim(self):
        from scripts.lib.ops.dispatch_process import ProcessError
        from scripts.lib.ops.environment_admission import Admission
        from scripts.operations import lab

        with tempfile.TemporaryDirectory() as folder:
            admission = Admission(
                Path(folder) / "state",
                namespace="handoff",
                workspace_id=folder,
                inventory=("app", "job", "other"),
                limits={
                    "cpus": 8,
                    "memory_bytes": 8 * 2**30,
                    "disk_bytes": 2**30,
                    "runtime_seconds": 300,
                },
                observe=lambda: {
                    "services": [],
                    "budget": {
                        "cpus": 0,
                        "memory_bytes": 0,
                        "disk_bytes": 0,
                    },
                },
            )
            service = {
                "cpus": 0.5,
                "mem_limit": str(256 * 2**20),
                "deploy": {
                    "resources": {
                        "reservations": {
                            "cpus": 0.1,
                            "memory": str(128 * 2**20),
                        }
                    }
                },
            }
            model = {
                "name": "hy-home-infra",
                "services": {
                    "app": service,
                    "job": {
                        **service,
                        "restart": "no",
                        "labels": {"hy-home.role": "job"},
                    },
                    "other": service,
                },
            }
            with (
                mock.patch.object(lab, "execution_admission", return_value=admission),
                mock.patch.object(lab, "render", return_value=model),
                mock.patch(
                    "scripts.lib.ops.dispatch_process.prepare_registered_docker",
                    side_effect=ProcessError("private setup failed"),
                ),
            ):
                with self.assertRaises(compose_start._OperatingSetupError) as caught:
                    compose_start._operating_admission(
                        Path(folder),
                        {"project": "hy-home-infra", "targets": ["app", "job"]},
                    )
            self.assertTrue(caught.exception.released)
            self.assertFalse(caught.exception.cleanup_pending)
            self.assertEqual([], admission.records())

    def test_a_state_read_failure_after_setup_still_returns_the_claim(self):
        # The fill-disk claim exists once admit returns; a busy admission store
        # on the next read must surface as a setup failure, not escape.
        from scripts.lib.ops.environment_admission import Admission, AdmissionError
        from scripts.operations import lab

        with tempfile.TemporaryDirectory() as folder:
            admission = Admission(
                Path(folder) / "state",
                namespace="handoff",
                workspace_id=folder,
                inventory=("app", "other"),
                limits={
                    "cpus": 8,
                    "memory_bytes": 8 * 2**30,
                    "disk_bytes": 2**30,
                    "runtime_seconds": 300,
                },
                observe=lambda: {
                    "services": [],
                    "budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0},
                },
            )
            service = {
                "cpus": 0.5,
                "mem_limit": str(256 * 2**20),
                "deploy": {
                    "resources": {
                        "reservations": {"cpus": 0.1, "memory": str(128 * 2**20)}
                    }
                },
            }
            real = admission.records
            reads = []

            def busy_once():
                reads.append(1)
                if len(reads) == 1:
                    raise AdmissionError("admission_state_unavailable")
                return real()

            with (
                mock.patch.object(lab, "execution_admission", return_value=admission),
                mock.patch.object(
                    lab,
                    "render",
                    return_value={"name": "p", "services": {"app": service}},
                ),
                mock.patch(
                    "scripts.lib.ops.dispatch_process.prepare_registered_docker"
                ),
                mock.patch.object(admission, "records", side_effect=busy_once),
            ):
                with self.assertRaises(compose_start._OperatingSetupError) as caught:
                    compose_start._operating_admission(
                        Path(folder), {"project": "p", "targets": ["app"]}
                    )
            self.assertTrue(caught.exception.token)
            if not caught.exception.released:
                self.assertEqual([caught.exception.token], [r["token"] for r in real()])

    def test_an_interrupt_after_setup_still_returns_the_claim(self):
        # The fill-disk claim exists once admit returns; a busy admission store
        # on the next read must surface as a setup failure, not escape.
        from scripts.lib.ops.environment_admission import Admission
        from scripts.operations import lab

        with tempfile.TemporaryDirectory() as folder:
            admission = Admission(
                Path(folder) / "state",
                namespace="handoff",
                workspace_id=folder,
                inventory=("app", "other"),
                limits={
                    "cpus": 8,
                    "memory_bytes": 8 * 2**30,
                    "disk_bytes": 2**30,
                    "runtime_seconds": 300,
                },
                observe=lambda: {
                    "services": [],
                    "budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0},
                },
            )
            service = {
                "cpus": 0.5,
                "mem_limit": str(256 * 2**20),
                "deploy": {
                    "resources": {
                        "reservations": {"cpus": 0.1, "memory": str(128 * 2**20)}
                    }
                },
            }
            real = admission.records
            reads = []

            def busy_once():
                reads.append(1)
                if len(reads) == 1:
                    raise KeyboardInterrupt
                return real()

            with (
                mock.patch.object(lab, "execution_admission", return_value=admission),
                mock.patch.object(
                    lab,
                    "render",
                    return_value={"name": "p", "services": {"app": service}},
                ),
                mock.patch(
                    "scripts.lib.ops.dispatch_process.prepare_registered_docker"
                ),
                mock.patch.object(admission, "records", side_effect=busy_once),
            ):
                with self.assertRaises(compose_start._OperatingSetupError) as caught:
                    compose_start._operating_admission(
                        Path(folder), {"project": "p", "targets": ["app"]}
                    )
            self.assertTrue(caught.exception.token)
            if not caught.exception.released:
                self.assertEqual([caught.exception.token], [r["token"] for r in real()])

    def test_partial_and_unaccounted_runtime_cannot_release_start_intent(self):
        from scripts.lib.ops.dispatch_process import cleanup_registered_docker
        from scripts.lib.ops.environment_admission import Admission
        from scripts.operations import lab

        with tempfile.TemporaryDirectory() as folder:
            observed = mock.Mock(
                return_value={
                    "services": [],
                    "budget": {"cpus": 0, "memory_bytes": 0, "disk_bytes": 0},
                }
            )
            admission = Admission(
                Path(folder) / "state",
                namespace="handoff",
                workspace_id=folder,
                inventory=("app", "job", "other"),
                limits={
                    "cpus": 8,
                    "memory_bytes": 8 * 2**30,
                    "disk_bytes": 2**30,
                    "runtime_seconds": 300,
                },
                observe=observed,
            )
            service = {
                "cpus": 0.5,
                "mem_limit": str(256 * 2**20),
                "deploy": {
                    "resources": {
                        "reservations": {"cpus": 0.1, "memory": str(128 * 2**20)}
                    }
                },
            }
            model = {
                "name": "hy-home-infra",
                "services": {
                    "app": {**service, "restart": "no"},  # no label: a service
                    "job": {
                        **service,
                        "restart": "no",
                        "labels": {"hy-home.role": "job"},
                    },
                    "other": service,
                },
            }
            plan = {"project": "hy-home-infra", "targets": ["app", "job"]}
            with (
                mock.patch.object(lab, "execution_admission", return_value=admission),
                mock.patch.object(lab, "render", return_value=model),
            ):
                _, claimed, verify = compose_start._operating_admission(
                    Path(folder), plan
                )
            self.assertAlmostEqual(0.45, claimed["budget"]["cpus"])
            self.assertEqual(2**30, claimed["budget"]["disk_bytes"])
            self.assertEqual(["job"], claimed["metadata"]["one_shot_services"])
            self.assertEqual(1, observed.call_count)
            app = {"project": "hy-home-infra", "service": "app", "running": True}
            job = {
                "project": "hy-home-infra",
                "service": "job",
                "running": False,
                "status": "exited",
                "exit_code": 0,
            }
            with mock.patch.object(
                lab, "running_containers", return_value=[app]
            ) as running:
                self.assertFalse(admission.release(claimed["token"], verify=verify))
                running.return_value = [app, job]
                self.assertFalse(admission.release(claimed["token"], verify=verify))
                self.assertEqual(1, len(admission.records()))
                observed.return_value = {
                    "services": ["app"],
                    "budget": {
                        "cpus": 0.1,
                        "memory_bytes": 128 * 2**20,
                        "disk_bytes": 0,
                    },
                }
                self.assertTrue(admission.release(claimed["token"], verify=verify))
            self.assertEqual([], admission.records())
            self.assertTrue(cleanup_registered_docker(claimed))


if __name__ == "__main__":
    unittest.main()
