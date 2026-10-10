"""Opt-in synthetic DEV/MNG datastore rehearsal with exact-owned-ID cleanup.
Enable with ``HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1``."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import secrets
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.validation.test_datastore_rehearsal_boundary import (
    CLEANUP_CALL_SECONDS,
    AttemptResources,
    CleanupFailure,
    DockerClientBoundary,
    OwnedContainer,
    OwnedNetwork,
    new_attempt_prefix,
    write_private_fixture,
)

ROOT = Path(__file__).resolve().parents[2]
PG = "postgres:18.6-alpine"
VALKEY = "valkey/valkey:9.1.2-alpine"
PROMETHEUS = "prom/prometheus:v3.15.0@sha256:efd719c99d83b060d9daefdcf00360461adf279f45ef5391f8d111892118753e"
PREFIX = ""
DOCKER_BINARY = Path("/usr/bin/docker")
DOCKER_SOCKET = Path("/run/docker.sock")
ATTEMPT_SECONDS = 15 * 60
EXPORTERS = (
    ("mng-pg-exporter", "mng", 9187),
    ("mng-valkey-exporter", "mng", 9121),
    ("dev-pg-exporter", "dev", 9187),
    ("dev-valkey-exporter", "dev", 9121),
)
SEEDED_KEY = "rehearsal:customer:4711"
SEEDED_VALUE = "rehearsal-private-value"
CONTAINER_IMAGES = frozenset((PG, VALKEY, PROMETHEUS))
COMPOSE_RENDER_ARGS = ("compose", "--env-file", str(ROOT / ".env.example"), "--profile", "mng", "--profile", "dev-data", "--profile", "obs", "config", "--format", "json")  # fmt: skip


def replace_private_fixture(directory: Path, name: str, content: str) -> Path:
    """Atomically replace one runner-owned synthetic fixture."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", name):
        raise ValueError("synthetic fixture file name must be a safe basename")
    target = directory / name
    if not target.exists():
        return write_private_fixture(directory, name, content)
    current = target.stat(follow_symlinks=False)
    if (
        not stat.S_ISREG(current.st_mode)
        or current.st_uid != os.geteuid()
        or current.st_gid != os.getegid()
        or current.st_nlink != 1
        or stat.S_IMODE(current.st_mode) != 0o640
    ):
        raise PermissionError("existing synthetic fixture metadata is invalid")
    temporary = f"{name}.tmp-{secrets.token_hex(12)}"
    staged = write_private_fixture(directory, temporary, content)
    directory_fd = os.open(
        directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    )
    try:
        os.replace(temporary, name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
        os.fsync(directory_fd)
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    finally:
        os.close(directory_fd)
    return target


ALERT_TESTS = """
rule_files: [alert_rules.local.datastores.yml]
evaluation_interval: 30s
tests:
  - interval: 30s
    input_series:
      - {series: 'up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="off"}', values: '0x40'}
      - {series: 'pg_up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="off"}', values: '0x40'}
      - {series: 'up{job="manage-postgres",instance="m",db_scope="mng",db_engine="postgresql",expected_state="on"}', values: '1x40'}
      - {series: 'up{job="mng-valkey-exporter",instance="v",db_scope="mng",db_engine="valkey",expected_state="on"}', values: '1x40'}
      - {series: 'up{job="dev-valkey-exporter",instance="w",db_scope="dev",db_engine="valkey",expected_state="off"}', values: '0x40'}
    alert_rule_test:
      - {eval_time: 15m, alertname: DevDatastoreExporterDown, exp_alerts: []}
      - {eval_time: 15m, alertname: DevPostgresDown, exp_alerts: []}
      - {eval_time: 15m, alertname: DatastoreScrapeTargetMissing, exp_alerts: []}
  - interval: 30s
    input_series:
      - {series: 'up{job="dev-pg-exporter",instance="d",db_scope="dev",db_engine="postgresql",expected_state="on"}', values: '0x40'}
      - {series: 'pg_up{job="dev-pg-exporter",instance="e",db_scope="dev",db_engine="postgresql",expected_state="on"}', values: '0x40'}
      - {series: 'up{job="mng-valkey-exporter",instance="v",db_scope="mng",db_engine="valkey",expected_state="on"}', values: '0x40'}
      - {series: 'redis_up{job="mng-valkey-exporter",instance="r",db_scope="mng",db_engine="valkey",expected_state="on"}', values: '0x40'}
      - {series: 'pg_scrape_collector_success{job="manage-postgres",instance="m",collector="wal",db_scope="mng",db_engine="postgresql",expected_state="on"}', values: '0x40'}
      - {series: 'scrape_duration_seconds{job="manage-postgres",instance="m",db_scope="mng",db_engine="postgresql",expected_state="on"}', values: '7x40'}
      - {series: 'pg_up{job="manage-postgres",instance="p",db_scope="mng",db_engine="postgresql",expected_state="on"}', values: '0x40'}
      - {series: 'pg_exporter_last_scrape_error{job="manage-postgres",instance="p",db_scope="mng",db_engine="postgresql",expected_state="on"}', values: '1x40'}
      - {series: 'redis_up{job="dev-valkey-exporter",instance="dv",db_scope="dev",db_engine="valkey",expected_state="on"}', values: '0x40'}
      - {series: 'redis_rejected_connections_total{job="dev-valkey-exporter",instance="dv",db_scope="dev",db_engine="valkey",expected_state="on"}', values: '0+1x40'}
      - {series: 'up{job="dev-valkey-exporter",instance="dw",db_scope="dev",db_engine="valkey",expected_state="off"}', values: '1x200'}
    promql_expr_test:
      - expr: sort(count by (alertname, severity) (ALERTS{alertstate="firing"}))
        eval_time: 15m
        exp_samples:
          - {labels: '{alertname="DatastoreCollectorFailed",severity="warning"}', value: 1}
          - {labels: '{alertname="DatastoreScrapeSlow",severity="warning"}', value: 1}
          - {labels: '{alertname="DatastoreScrapeTargetMissing",severity="warning"}', value: 1}
          - {labels: '{alertname="DevDatastoreExporterDown",severity="warning"}', value: 1}
          - {labels: '{alertname="DevPostgresDown",severity="warning"}', value: 1}
          - {labels: '{alertname="DevValkeyDown",severity="warning"}', value: 1}
          - {labels: '{alertname="MngDatastoreExporterDown",severity="critical"}', value: 1}
          - {labels: '{alertname="PostgresDown",severity="critical"}', value: 1}
          - {labels: '{alertname="ValkeyDown",severity="critical"}', value: 1}
          - {labels: '{alertname="ValkeyRejectedConnections",severity="warning"}', value: 1}
      # A MNG outage pages once: the exporter error is folded into PostgresDown.
      - expr: count(ALERTS{alertname="PostgresqlExporterError"})
        eval_time: 15m
        exp_samples: []
      - expr: count(ALERTS{alertname="DevDatastoreUpWhileDeclaredOff",alertstate="firing"})
        eval_time: 90m
        exp_samples: [{labels: '{}', value: 1}]
"""


_DOCKER_CLIENT: DockerClientBoundary | None = None
_RESOURCES: AttemptResources | None = None


def docker(*args: str, check: bool = True, input_: str | None = None) -> str:
    if _DOCKER_CLIENT is None or _RESOURCES is None:
        raise AssertionError("Docker rehearsal boundary is not initialized")
    if args and args[0] == "run":
        return _RESOURCES.run_container(*args[1:], check=check, input_=input_)
    if args == COMPOSE_RENDER_ARGS:
        return _DOCKER_CLIENT.run(*args, check=check, input_=input_)
    if input_ is not None:
        raise AssertionError("input is restricted to tracked container runs")
    return _RESOURCES.run_owned(*args, check=check)


def docker_result(*args: str, input_: str | None = None) -> subprocess.CompletedProcess[str]:  # fmt: skip
    if _RESOURCES is None or not args or args[0] != "run":
        raise AssertionError("result capture is restricted to tracked containers")
    return _RESOURCES.run_container_result(*args[1:], input_=input_)


class DatastoreBoundaryAdditionalTests(unittest.TestCase):
    IMAGE_ID = "sha256:" + "1" * 64
    REPO_DIGEST = "postgres@sha256:" + "2" * 64

    @staticmethod
    def result(returncode: int, stdout: str = "", stderr: str = ""):
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    @classmethod
    def container_payload(cls, record: OwnedContainer) -> str:
        labels = {"hyhome.rehearsal.attempt": "attempt", "hyhome.rehearsal.invocation": record.invocation, "hyhome.rehearsal.image": record.image, "hyhome.rehearsal.image-id": record.image_id}  # fmt: skip
        payload = {"Id": record.container_id, "Name": f"/{record.name}", "Image": record.image_id, "Config": {"Image": record.image_id, "Labels": labels}}  # fmt: skip
        return json.dumps(payload)

    @staticmethod
    def network_payload(record: OwnedNetwork) -> str:
        return json.dumps(
            {
                "Id": record.network_id,
                "Name": record.name,
                "Internal": True,
                "Labels": {"hyhome.rehearsal.attempt": "attempt"},
            }
        )

    def bound_resources(self, directory: Path | None = None):
        client = mock.Mock()
        client.run_result.return_value = self.result(
            0,
            json.dumps({"Id": self.IMAGE_ID, "RepoDigests": [self.REPO_DIGEST]}),
        )
        resources = AttemptResources("attempt", client, directory)
        resources.register_images({PG}, require_repo_digests={PG})
        client.reset_mock()
        return resources, client

    @staticmethod
    def track_network(resources: AttemptResources, network: OwnedNetwork) -> None:
        resources.network_ids.add(network.network_id)
        resources.network_names[network.name] = network.network_id
        resources.network_records[network.network_id] = network

    def test_private_docker_config_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            binary = root / "docker"
            binary.write_bytes(b"fixture")
            binary.chmod(0o755)
            endpoint = root / "docker.sock"
            listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            listener.bind(str(endpoint))
            config = root / "config"
            config.mkdir(mode=0o755)
            try:
                with self.assertRaisesRegex(PermissionError, "new, empty and private"):
                    DockerClientBoundary(
                        binary=binary,
                        socket_path=endpoint,
                        config_dir=config,
                        deadline_seconds=30,
                    )
            finally:
                listener.close()

    def test_container_boundary_rejects_unowned_runtime_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            resources, _ = self.bound_resources(directory)
            cases = (
                ("--publish=5432:5432", PG),
                ("--net", "host", PG),
                ("-P", PG),
                ("--volumes-from", "foreign", PG),
                ("--env-file", "/tmp/foreign", PG),
                ("foreign:latest", PG, "true"),
                ("--network", "foreign", PG),
                ("--mount", "type=bind,src=/,dst=/host", PG),
            )
            for case in cases:
                with self.subTest(case=case), self.assertRaises(AssertionError):
                    resources.run_container(*case)

    def test_invalid_environment_assignments_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            resources = AttemptResources("attempt", mock.Mock(), directory)
            for case in (("-e",), ("-e", "MISSING"), ("-e", "BAD-NAME=x")):
                with self.subTest(case=case), self.assertRaises(AssertionError):
                    resources._private_environment_args(case, 1)

    def test_boundary_metadata_is_typed_and_image_allowlisted(self) -> None:
        resources, _ = self.bound_resources()
        self.assertEqual(resources._object('[{"x":1}]'), {"x": 1})
        for payload in ("[]", "null"):
            with self.subTest(payload=payload), self.assertRaises(AssertionError):
                resources._object(payload)
        with self.assertRaises(ValueError):
            resources.register_images(set())

    def test_completed_auto_remove_container_is_retired_after_exact_absence(self) -> None:  # fmt: skip
        container_id = "a" * 64
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            write_private_fixture(directory, "replace", "old\n")
            self.assertEqual(replace_private_fixture(directory, "replace", "new\n").read_text(), "new\n")  # fmt: skip
            resources, client = self.bound_resources(directory)

            def run(*args, **_kwargs):
                if args[0] == "ps":
                    return ""
                cidfile = Path(args[args.index("--cidfile") + 1])
                cidfile.write_text(container_id + "\n", encoding="ascii")
                self.assertIn(self.IMAGE_ID, args)
                return "done\n"

            client.run.side_effect = run
            client.run_result.side_effect = [self.result(1, stderr=f"Error response from daemon: No such container: {container_id}\n")]  # fmt: skip
            resources.run_container("--rm", PG, "true")
        self.assertEqual(resources.container_ids, set())
        self.assertEqual(resources.container_records, {})

    def test_malformed_cidfile_recovers_owned_persistent_container(self) -> None:
        container_id = "0" * 64
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            resources, client = self.bound_resources(directory)
            network = OwnedNetwork("7" * 64, "attempt-net")
            self.track_network(resources, network)
            created: dict[str, OwnedContainer] = {}

            def run(*args, **_kwargs):
                if args[0] == "ps":
                    return container_id + "\n"
                if args[0] == "inspect":
                    return self.container_payload(created["record"])
                Path(args[args.index("--cidfile") + 1]).write_text("partial\n")
                labels = [
                    args[i + 1]
                    for i, value in enumerate(args[:-1])
                    if value == "--label"
                ]
                invocation = next(
                    value.split("=", 1)[1] for value in labels if "invocation=" in value
                )
                created["record"] = OwnedContainer(
                    container_id,
                    "attempt-pg",
                    invocation,
                    PG,
                    self.IMAGE_ID,
                    False,
                )
                return container_id + "\n"

            def inspect(*args, **_kwargs):
                if args[:2] == ("network", "inspect"):
                    return self.result(0, self.network_payload(network))
                return self.result(0, self.container_payload(created["record"]))

            client.run.side_effect = run
            client.run_result.side_effect = inspect
            mounted = write_private_fixture(directory, "mounted", "synthetic\n")
            resources.run_container(
                "-d",
                "--name",
                "attempt-pg",
                "--network",
                network.name,
                "-e",
                "PASSWORD=synthetic",
                "-v",
                f"{mounted}:/fixture:ro",
                PG,
            )
        command = next(call.args for call in client.run.call_args_list if call.args[0] == "run")  # fmt: skip
        self.assertIn(self.IMAGE_ID, command)
        self.assertIn(network.network_id, command)
        self.assertNotIn(network.name, command)
        self.assertNotIn("PASSWORD=synthetic", command)
        self.assertTrue(
            {"--pull", "--cpus", "--memory", "--pids-limit"}.issubset(command)
        )
        self.assertEqual(resources.container_ids, {container_id})

    def test_network_create_recovers_lost_output_and_revalidates_exact_id(self) -> None:
        network_id = "a" * 64
        resources, client = self.bound_resources()
        network = OwnedNetwork(network_id, "attempt-obs")
        client.run.side_effect = [
            "lost\n",
            network_id + "\n",
            self.network_payload(network),
        ]
        client.run_result.return_value = self.result(0, self.network_payload(network))
        self.assertEqual(resources.create_network("obs"), network.name)
        self.assertEqual(resources.network_ids, {network_id})

    def test_remove_container_requires_post_remove_exact_absence(self) -> None:
        resources, client = self.bound_resources()
        record = OwnedContainer("9" * 64, "attempt-job", "i9", PG, self.IMAGE_ID, False)
        resources._track_container(record)
        missing = f"Error response from daemon: No such container: {record.container_id}\n"  # fmt: skip
        client.run_result.side_effect = [
            self.result(0, self.container_payload(record)),
            self.result(0),
            self.result(1, stderr=missing),
        ]
        resources.remove_container(record.name)
        self.assertEqual(resources.container_ids, set())

    def test_owned_operations_replace_reusable_names_with_validated_ids(self) -> None:
        resources, client = self.bound_resources()
        record = OwnedContainer("b" * 64, "attempt-pg", "i1", PG, self.IMAGE_ID, False)
        resources._track_container(record)
        client.run_result.return_value = self.result(0, self.container_payload(record))
        client.run.return_value = "ok"
        self.assertEqual(resources.run_owned("restart", record.name), "ok")
        self.assertEqual(client.run.call_args.args, ("restart", record.container_id))
        client.reset_mock()
        client.run_result.side_effect = [self.result(1), self.result(0)]
        with self.assertRaisesRegex(AssertionError, "absence check failed closed"):
            resources.run_owned("stop", record.name)
        client.run.assert_not_called()

    def test_network_connect_uses_validated_exact_ids(self) -> None:
        resources, client = self.bound_resources()
        container = OwnedContainer(
            "c" * 64, "attempt-exporter", "i2", PG, self.IMAGE_ID, False
        )
        network = OwnedNetwork("d" * 64, "attempt-obs")
        resources._track_container(container)
        self.track_network(resources, network)
        client.run_result.side_effect = [
            self.result(0, self.network_payload(network)),
            self.result(0, self.container_payload(container)),
        ]
        client.run.return_value = "connected"
        self.assertEqual(
            resources.run_owned(
                "network",
                "connect",
                "--alias",
                "exporter",
                network.name,
                container.name,
            ),
            "connected",
        )
        self.assertEqual(
            client.run.call_args.args,
            (
                "network",
                "connect",
                "--alias",
                "exporter",
                network.network_id,
                container.container_id,
            ),
        )

    def test_failed_remove_and_post_present_preserve_owned_references(self) -> None:
        resources, client = self.bound_resources()
        container = OwnedContainer(
            "e" * 64, "attempt-pg", "i3", PG, self.IMAGE_ID, False
        )
        network = OwnedNetwork("f" * 64, "attempt-net")
        resources._track_container(container)
        self.track_network(resources, network)
        client.run_result.side_effect = [
            self.result(0, self.container_payload(container)),
            self.result(7),
            self.result(0, self.container_payload(container)),
            self.result(0, self.network_payload(network)),
            self.result(8),
            self.result(0, self.network_payload(network)),
        ]
        with self.assertRaises(CleanupFailure) as caught:
            resources.cleanup()
        self.assertEqual(resources.container_ids, {container.container_id})
        self.assertEqual(resources.network_ids, {network.network_id})
        self.assertEqual(
            {issue.category for issue in caught.exception.issues},
            {"rm_failed", "post_remove_present"},
        )

    def test_cleanup_budget_attempts_all_nine_containers_and_three_networks(self) -> None:  # fmt: skip
        resources, client = self.bound_resources()
        containers = [
            OwnedContainer(
                str(index) * 64,
                f"attempt-c{index}",
                f"i{index}",
                PG,
                self.IMAGE_ID,
                False,
            )
            for index in range(1, 10)
        ]
        networks = [OwnedNetwork(letter * 64, f"attempt-n{letter}") for letter in "abc"]
        for record in containers:
            resources._track_container(record)
        for record in networks:
            self.track_network(resources, record)
        removed: set[str] = set()

        def result(*args, **_kwargs):
            network = args[0] == "network"
            action = args[1] if network else args[0]
            if action in ("ls", "ps"):
                return self.result(0)
            resource_id = args[2] if network or action == "rm" else args[1]
            if action == "rm":
                removed.add(resource_id)
                return self.result(0)
            records = (
                resources.network_records if network else resources.container_records
            )
            record = records[resource_id]
            payload = (
                self.network_payload(record)
                if network
                else self.container_payload(record)
            )
            if resource_id in removed and not network:
                return self.result(1, stderr=f"Error response from daemon: No such container: {resource_id}\n")  # fmt: skip
            return self.result(1) if resource_id in removed else self.result(0, payload)

        client.run_result.side_effect = result
        resources.cleanup()
        calls = client.run_result.call_args_list
        self.assertEqual(
            removed,
            {r.container_id for r in containers} | {r.network_id for r in networks},
        )
        self.assertLessEqual(len(calls) * CLEANUP_CALL_SECONDS, 120)
        first_network = next(
            i for i, call in enumerate(calls) if call.args[0] == "network"
        )
        self.assertTrue(
            all(call.args[0] != "network" for call in calls[:first_network])
        )

    def test_invalid_bindings_owned_shapes_and_absence_fail_closed(self) -> None:
        resources, client = self.bound_resources()
        for payload in (
            self.result(4),
            self.result(0, '{"Id":"bad","RepoDigests":[]}'),
            self.result(0, json.dumps({"Id": self.IMAGE_ID, "RepoDigests": ["bad"]})),
        ):
            client.run_result.return_value = payload
            with self.assertRaises(AssertionError):
                resources.register_images({"other:image"})
        with self.assertRaises(ValueError):
            resources.register_images({PG}, require_repo_digests={"other:image"})
        for args in (
            (),
            ("logs", "a", "b"),
            ("exec", "a"),
            ("network", "connect", "a"),
            ("rm", "foreign"),
        ):
            with self.subTest(args=args), self.assertRaises(AssertionError):
                resources.run_owned(*args)
        record = OwnedContainer("8" * 64, "attempt-x", "i8", PG, self.IMAGE_ID, False)
        resources._track_container(record)
        client.reset_mock()
        messages = (f"Error: No such object: {record.container_id}", f"Error response from daemon: No such container: {record.container_id}")  # fmt: skip
        for message in messages:
            client.run_result.return_value = self.result(1, stderr=message)
            self.assertFalse(resources._container_present(record))
            self.assertEqual(client.run_result.mock_calls, [mock.call("inspect", record.container_id)])  # fmt: skip
            client.reset_mock()
        rejected = (self.result(2, stderr=messages[0]), self.result(1, "unexpected", messages[0]), self.result(1, stderr="Error: No such object: " + "7" * 64), self.result(1, stderr="prefix " + messages[0]), self.result(1, stderr=messages[0] + " suffix"))  # fmt: skip
        for response in rejected:
            client.run_result.return_value = response
            with self.subTest(response=response), self.assertRaises(AssertionError):
                resources._container_present(record)
            client.reset_mock()
        client.run_result.side_effect = subprocess.TimeoutExpired([], 1)
        with self.assertRaises(CleanupFailure) as timeout:
            resources.cleanup()
        self.assertEqual(timeout.exception.container_ids, (record.container_id,))
        orphan = AttemptResources("attempt", mock.Mock())
        orphan.container_ids.add("orphan")
        with self.assertRaisesRegex(CleanupFailure, "record_missing"):
            orphan.cleanup()


def rendered_services() -> dict[str, dict]:
    out = docker(*COMPOSE_RENDER_ARGS)
    services = json.loads(out)["services"]
    return {
        name: services[name] for name in [n for n, _, _ in EXPORTERS] + ["prometheus"]
    }


def dev_monitor_sql() -> str:
    provision = ROOT / "infra/04-data/dev-db/pg/provision"
    sys.path.insert(0, str(provision))
    try:
        spec = importlib.util.spec_from_file_location(
            "dev_monitor", provision / "monitor.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(provision))
    return module.sql()


@unittest.skipUnless(
    os.environ.get("HYHOME_DATASTORE_OBSERVATION_REHEARSAL") == "1",
    "set HYHOME_DATASTORE_OBSERVATION_REHEARSAL=1 to run the isolated rehearsal",
)
class DatastoreObservationRehearsalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        global PREFIX, _DOCKER_CLIENT, _RESOURCES

        PREFIX = new_attempt_prefix()
        cls.scratch = tempfile.TemporaryDirectory(prefix=f"{PREFIX}-")
        cls.dir = Path(cls.scratch.name)
        cls.dir.chmod(0o700)
        cls.docker_config = cls.dir / "docker-client"
        cls.docker_config.mkdir(mode=0o700)
        _DOCKER_CLIENT = DockerClientBoundary(
            binary=DOCKER_BINARY,
            socket_path=DOCKER_SOCKET,
            config_dir=cls.docker_config,
            deadline_seconds=ATTEMPT_SECONDS,
        )
        _RESOURCES = AttemptResources(
            PREFIX,
            _DOCKER_CLIENT,
            cls.dir,
        )
        cls.secret: dict[str, str] = {}
        for name in (
            "mng_postgres_password", "mng_pg_monitor_password",
            "dev_postgres_password", "dev_pg_monitor_password",
            "mng_valkey_password", "mng_valkey_monitor_password",
            "mng_valkey_inspector_password",
            "dev_valkey_admin_password", "dev_valkey_monitor_password",
            "dev_valkey_inspector_password",
        ):  # fmt: skip
            cls.write_secret(name, secrets.token_urlsafe(24))
        for name in (
            "openbao_token",
            "qdrant_read_only_api_key",
            "opensearch_exporter_password",
        ):
            cls.write_secret(name, "synthetic-unused")
        write_private_fixture(cls.dir, "projects.tsv", "# none\n")
        (cls.dir / "project-secrets").mkdir(mode=0o750)
        cls.services = rendered_services()
        _RESOURCES.register_images(
            set(CONTAINER_IMAGES)
            | {service["image"] for service in cls.services.values()},
            require_repo_digests={PG, VALKEY},
        )
        cls.prometheus_tmpfs = next(
            t
            for t in cls.services["prometheus"]["tmpfs"]
            if t.startswith("/etc/prometheus")
        )
        try:
            cls.start()
        except BaseException:
            try:
                cls.cleanup()
            finally:
                _RESOURCES = None
                _DOCKER_CLIENT = None
                cls.scratch.cleanup()
            raise

    @classmethod
    def tearDownClass(cls) -> None:
        global _DOCKER_CLIENT, _RESOURCES

        try:
            cls.cleanup()
        finally:
            _RESOURCES = None
            _DOCKER_CLIENT = None
            cls.scratch.cleanup()

    @classmethod
    def write_secret(cls, name: str, value: str) -> None:
        replace_private_fixture(cls.dir, name, value + "\n")
        cls.secret[name] = value

    @classmethod
    def cleanup(cls) -> None:
        if _RESOURCES is not None:
            _RESOURCES.cleanup()

    # -- startup -----------------------------------------------------------

    @classmethod
    def start(cls) -> None:
        for net in ("mng", "dev", "obs"):
            if _RESOURCES is None:
                raise AssertionError("attempt resources are not initialized")
            _RESOURCES.create_network(net)
        for scope in ("mng", "dev"):
            docker(
                "run", "-d", "--name", f"{PREFIX}-{scope}-pg",
                "--network", f"{PREFIX}-{scope}", "--network-alias", f"{scope}-pg",
                "-e", "POSTGRES_PASSWORD_FILE=/run/secrets/admin",
                "-v", f"{cls.dir}/{scope}_postgres_password:/run/secrets/admin:ro",
                PG,
            )  # fmt: skip
        cls.start_valkey("mng")
        cls.start_valkey("dev")
        for scope in ("mng", "dev"):
            cls.wait(
                lambda s=scope: (
                    cls.psql_admin(s, "SELECT 1", check=False).strip() == "1"
                )
            )
            cls.psql_admin(scope, "CREATE DATABASE app")
            cls.psql_admin(scope, "CREATE TABLE private (v text)", db="app")
        cls.provision("mng")
        cls.provision("dev")
        for scope in ("mng", "dev"):
            cls.valkey_admin(scope, "SET", SEEDED_KEY, SEEDED_VALUE)
        for name, _, _ in EXPORTERS:
            cls.start_exporter(name)
        cls.start_prometheus()
        for name, _, _ in EXPORTERS:
            cls.wait(lambda n=name: "_up 1" in cls.metrics(n))

    @classmethod
    def start_valkey(cls, scope: str) -> None:
        base = ROOT / f"infra/04-data/{scope}-db/valkey"
        mounts = ["-v", f"{base}/scripts:/usr/local/libexec/{scope}-valkey:ro"]
        if scope == "dev":
            mounts += [
                "-v", f"{base}/config/valkey.conf:/etc/dev-valkey/valkey.conf:ro",
                "-v", f"{cls.dir}/projects.tsv:/etc/dev-valkey/projects.tsv:ro",
                "-v", f"{cls.dir}/project-secrets:/run/valkey-project-secrets:ro",
            ]  # fmt: skip
            names = ("dev_valkey_admin_password", "dev_valkey_monitor_password",
                     "dev_valkey_inspector_password")  # fmt: skip
        else:
            names = ("mng_valkey_password", "mng_valkey_monitor_password",
                     "mng_valkey_inspector_password")  # fmt: skip
        for name in names:
            mounts += ["-v", f"{cls.dir}/{name}:/run/secrets/{name}:ro"]
        docker(
            "run", "-d", "--name", f"{PREFIX}-{scope}-valkey",
            "--network", f"{PREFIX}-{scope}", "--network-alias", f"{scope}-valkey",
            "--user", "999:999", "--tmpfs", "/run/valkey:uid=999,gid=999,mode=0700",
            *mounts, "--entrypoint", "/bin/sh", VALKEY,
            f"/usr/local/libexec/{scope}-valkey/start.sh",
        )  # fmt: skip
        cls.wait(lambda: cls.valkey_admin(scope, "PING", check=False).strip() == "PONG")

    @classmethod
    def start_exporter(cls, name: str, secret_file: Path | None = None, suffix: str = "") -> str:  # fmt: skip
        """Run the exporter exactly as Compose renders it, with a synthetic secret."""
        service = cls.services[name]
        scope = name.split("-")[0]
        secret = service["secrets"][0]["source"]
        source = secret_file or cls.dir / secret
        container = f"{PREFIX}-{name}{suffix}"
        args = [
            "run", "-d", "--name", container, "--network", f"{PREFIX}-{scope}",
            "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges:true",
            "-v", f"{source}:/run/secrets/{secret}:ro",
        ]  # fmt: skip
        for key, value in (service.get("environment") or {}).items():
            args += ["-e", f"{key}={value}"]
        entrypoint = service.get("entrypoint") or []
        if entrypoint:
            args += ["--entrypoint", entrypoint[0]]
        args.append(service["image"])
        args += entrypoint[1:]
        args += [part.replace("$$", "$") for part in service.get("command") or []]
        docker(*args)
        if not suffix:
            docker("network", "connect", "--alias", name, f"{PREFIX}-obs", container)
        return container

    @classmethod
    def start_prometheus(cls) -> None:
        config = ROOT / "infra/06-observability/prometheus"
        mounts = [
            "-v", f"{config}/config/prometheus.dev.yml:/etc/prometheus/prometheus.yml:ro",
            "-v", f"{config}/config/alert_rules:/etc/prometheus/alert_rules:ro",
            "-v", f"{config}/scripts:/usr/local/libexec/prometheus:ro",
        ]  # fmt: skip
        for name in (
            "openbao_token",
            "qdrant_read_only_api_key",
            "opensearch_exporter_password",
        ):
            mounts += ["-v", f"{cls.dir}/{name}:/run/secrets/{name}:ro"]
        docker(
            "run", "-d", "--name", f"{PREFIX}-prometheus",
            "--network", f"{PREFIX}-obs", "--tmpfs", cls.prometheus_tmpfs,
            "-e", "PROMETHEUS_DEV_DATA_EXPECTED=on", *mounts,
            "--entrypoint", "/bin/sh", PROMETHEUS,
            "/usr/local/libexec/prometheus/start.sh",
            "--config.file=/etc/prometheus/prometheus.yml",
            "--storage.tsdb.path=/prometheus",
        )  # fmt: skip

    @classmethod
    def provision(cls, scope: str) -> str:
        if scope == "mng":
            provision = ROOT / "infra/04-data/mng-db/pg/provision"
            return docker(
                "run", "--rm", "--network", f"{PREFIX}-mng",
                "-e", "PGHOST=mng-pg", "-e", "PGPORT=5432", "-e", "PGUSER=postgres",
                "-e", "PGDATABASE=postgres",
                "-e", "PROVISION_ADMIN_PASSWORD_FILE=/run/secrets/mng_postgres_password",
                "-e", "PROVISION_SQL=/provision/monitor.sql",
                "-e", "PROVISION_SECRETS=MNG_PG_MONITOR_PASSWORD="
                "/run/secrets/mng_pg_monitor_password",
                "-v", f"{provision}:/provision:ro",
                "-v", f"{cls.dir}/mng_postgres_password:"
                "/run/secrets/mng_postgres_password:ro",
                "-v", f"{cls.dir}/mng_pg_monitor_password:"
                "/run/secrets/mng_pg_monitor_password:ro",
                "--entrypoint", "/bin/sh", PG, "/provision/run-feature-provision.sh",
            )  # fmt: skip
        return docker(
            "run", "--rm", "-i", "--network", f"{PREFIX}-dev",
            "-e", f"PGPASSWORD={cls.secret['dev_postgres_password']}",
            "-e", f"DEV_MONITOR_PASSWORD={cls.secret['dev_pg_monitor_password']}",
            PG, "psql", "-X", "-q", "-h", "dev-pg", "-U", "postgres", "-d", "postgres",
            input_=dev_monitor_sql(),
        )  # fmt: skip

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def wait(predicate, attempts: int = 60, delay: float = 2.0) -> None:
        for _ in range(attempts):
            if predicate():
                return
            time.sleep(delay)
        raise AssertionError("condition not reached")

    @classmethod
    def psql_admin(cls, scope: str, sql: str, db: str = "postgres", check: bool = True) -> str:  # fmt: skip
        password = cls.secret[f"{scope}_postgres_password"]
        return docker(
            "run", "--rm", "--network", f"{PREFIX}-{scope}",
            "-e", f"PGPASSWORD={password}", PG, "psql", "-X", "-At",
            "-h", f"{scope}-pg", "-U", "postgres", "-d", db, "-c", sql, check=check,
        )  # fmt: skip

    @classmethod
    def psql_result(cls, scope, user, password, sql, db="postgres"):
        """A login from a separate client container over the network."""
        return docker_result(
            "run", "--rm", "--network", f"{PREFIX}-{scope}",
            "-e", f"PGPASSWORD={password}", PG, "psql", "-X", "-At",
            "-h", f"{scope}-pg", "-U", user, "-d", db, "-c", sql,
        )  # fmt: skip

    @classmethod
    def valkey(cls, scope, user, password, *command, check=True) -> str:
        return docker(
            "run", "--rm", "--network", f"{PREFIX}-{scope}",
            "-e", f"REDISCLI_AUTH={password}", VALKEY, "valkey-cli",
            "--no-auth-warning", "-h", f"{scope}-valkey", "--user", user,
            *command, check=check,
        )  # fmt: skip

    @classmethod
    def valkey_admin(cls, scope, *command, check=True) -> str:
        if scope == "mng":
            user, secret = "default", "mng_valkey_password"
        else:
            user, secret = "devadmin", "dev_valkey_admin_password"
        return cls.valkey(scope, user, cls.secret[secret], *command, check=check)

    @classmethod
    def metrics(cls, name: str, container: str | None = None) -> str:
        port = {n: p for n, _, p in EXPORTERS}[name]
        return docker(
            "exec", container or f"{PREFIX}-{name}", "wget", "-qO-",
            f"http://127.0.0.1:{port}/metrics", check=False,
        )  # fmt: skip

    @staticmethod
    def value(text: str, metric: str) -> str | None:
        match = re.search(rf"(?m)^{re.escape(metric)} (\S+)$", text)
        return match.group(1) if match else None

    def scrape_states(self) -> dict[str, tuple[str, str, str, str]]:
        out = docker(
            "exec", f"{PREFIX}-prometheus", "wget", "-qO-",
            "http://127.0.0.1:9090/api/v1/query?query=up%7Bdomain%3D%22datastores%22%7D",
            check=False,
        )  # fmt: skip
        result = json.loads(out or '{"data":{"result":[]}}')["data"]["result"]
        return {
            r["metric"]["job"]: (
                r["metric"].get("db_scope"),
                r["metric"].get("db_engine"),
                r["metric"].get("expected_state"),
                r["value"][1],
            )
            for r in result
            if "db_scope" in r["metric"]
        }

    # -- tests -------------------------------------------------------------

    def test_exporters_read_every_collector_through_the_monitor_roles(self) -> None:
        for name, _, _ in EXPORTERS:
            body = self.metrics(name)
            with self.subTest(exporter=name):
                if "pg" in name:
                    self.assertEqual(self.value(body, "pg_up"), "1")
                    failed = re.findall(
                        r'(?m)^pg_scrape_collector_success\{collector="(\w+)"\} 0$',
                        body,
                    )
                    self.assertEqual(failed, [])
                    self.assertEqual(
                        self.value(body, "pg_exporter_last_scrape_error"), "0"
                    )
                else:
                    self.assertEqual(self.value(body, "redis_up"), "1")
                    self.assertEqual(
                        self.value(body, 'redis_exporter_last_scrape_error{err=""}'),
                        "0",
                    )

    def test_metrics_and_logs_carry_no_secret_key_name_or_value(self) -> None:
        for name, _, _ in EXPORTERS:
            body = self.metrics(name)
            logs = docker("logs", f"{PREFIX}-{name}", check=False)
            with self.subTest(exporter=name):
                for value in self.secret.values():
                    self.assertNotIn(value, body)
                    self.assertNotIn(value, logs)
                self.assertNotIn(SEEDED_KEY, body)
                self.assertNotIn(SEEDED_VALUE, body)

    def test_pg_monitor_roles_authenticate_over_the_network_and_cannot_write(self) -> None:  # fmt: skip
        for scope in ("mng", "dev"):
            role = f"{scope}_pg_monitor"
            password = self.secret[f"{scope}_pg_monitor_password"]
            with self.subTest(scope=scope):
                ok = self.psql_result(
                    scope,
                    role,
                    password,
                    "SELECT current_setting('default_transaction_read_only')",
                )
                self.assertEqual(ok.stdout.strip(), "on", ok.stderr)
                wrong = self.psql_result(scope, role, password + "x", "SELECT 1")
                self.assertIn("password authentication failed", wrong.stderr)
                ddl = self.psql_result(scope, role, password, "CREATE TABLE t (v int)")
                self.assertIn("read-only transaction", ddl.stderr)
                read = self.psql_result(
                    scope, role, password, "SELECT * FROM private", db="app"
                )
                self.assertIn("permission denied", read.stderr)
                attrs = self.psql_admin(
                    scope,
                    "SELECT rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication"
                    f" OR rolbypassrls, pg_has_role('{role}', 'pg_monitor', 'MEMBER'),"
                    f" rolconnlimit FROM pg_roles WHERE rolname = '{role}'",
                )
                self.assertEqual(attrs.strip(), "f|f|3")

    def test_valkey_monitor_roles_cannot_read_keys_or_config(self) -> None:
        refused = (
            ("GET", SEEDED_KEY),
            ("KEYS", "*"),
            ("SCAN", "0"),
            ("CONFIG", "GET", "*"),
            ("SLOWLOG", "GET"),
            ("SET", "k", "v"),
        )
        for scope in ("mng", "dev"):
            user = f"{scope}monitor"
            password = self.secret[f"{scope}_valkey_monitor_password"]
            with self.subTest(scope=scope):
                # Only the exporter talks to the server between the reset and
                # the read, so the log shows exactly what it is refused.
                self.valkey_admin(scope, "ACL", "LOG", "RESET")
                exporter = f"{scope}-valkey-exporter"
                self.wait(lambda e=exporter: self.metrics(e) != "")
                self.wait(
                    lambda s=scope: "object" in self.valkey_admin(s, "ACL", "LOG")
                )
                log = self.valkey_admin(scope, "ACL", "LOG", "100")
                self.assertEqual(
                    set(re.findall(r"(?m)^object\n(.+)$", log)), {"slowlog|get"}
                )
                info = self.valkey(scope, user, password, "INFO", "server")
                self.assertIn("redis_version", info)
                for command in refused:
                    out = self.valkey(scope, user, password, *command, check=False)
                    self.assertIn("NOPERM", out, command)
                wrong = self.valkey(scope, user, password + "x", "PING", check=False)
                self.assertNotIn("PONG", wrong)

    def test_wrong_password_keeps_the_exporter_up_and_reports_the_database_down(self) -> None:  # fmt: skip
        wrong = self.dir / "wrong"
        wrong_value = secrets.token_urlsafe(24)
        write_private_fixture(self.dir, wrong.name, wrong_value + "\n")
        for name in ("mng-pg-exporter", "mng-valkey-exporter"):
            metric = "pg_up" if "pg" in name else "redis_up"
            container = self.start_exporter(name, wrong, suffix="-wrongpw")
            try:
                self.wait(
                    lambda c=container, n=name, m=metric: (
                        self.value(self.metrics(n, c), m) == "0"
                    )
                )
                logs = docker("logs", container, check=False)
                self.assertNotIn(wrong_value, logs + self.metrics(name, container))
            finally:
                if _RESOURCES is None:
                    raise AssertionError("attempt resources are not initialized")
                _RESOURCES.remove_container(container)

    def test_lost_collector_grant_is_reported_and_restored_by_the_job(self) -> None:
        self.psql_admin(
            "mng",
            "REVOKE EXECUTE ON FUNCTION pg_catalog.pg_ls_waldir() FROM mng_pg_monitor",
        )
        wal = 'pg_scrape_collector_success{collector="wal"}'
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), wal) == "0")
        self.assertEqual(self.value(self.metrics("mng-pg-exporter"), "pg_up"), "1")
        self.provision("mng")
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), wal) == "1")

    def test_database_stop_and_recovery(self) -> None:
        for engine, metric in (("pg", "pg_up"), ("valkey", "redis_up")):
            exporter = f"dev-{engine}-exporter"
            docker("stop", f"{PREFIX}-dev-{engine}")
            try:
                self.wait(
                    lambda e=exporter, m=metric: self.value(self.metrics(e), m) == "0"
                )
            finally:
                docker("start", f"{PREFIX}-dev-{engine}")
            self.wait(
                lambda e=exporter, m=metric: self.value(self.metrics(e), m) == "1"
            )

    def test_rotation_follows_the_secret_and_refuses_the_old_password(self) -> None:
        old = self.secret["mng_pg_monitor_password"]
        self.write_secret("mng_pg_monitor_password", secrets.token_urlsafe(24))
        self.provision("mng")
        docker("restart", f"{PREFIX}-mng-pg-exporter")
        self.wait(lambda: self.value(self.metrics("mng-pg-exporter"), "pg_up") == "1")
        stale = self.psql_result("mng", "mng_pg_monitor", old, "SELECT 1")
        self.assertIn("password authentication failed", stale.stderr)
        old = self.secret["mng_valkey_monitor_password"]
        self.write_secret("mng_valkey_monitor_password", secrets.token_urlsafe(24))
        docker("restart", f"{PREFIX}-mng-valkey")
        self.wait(
            lambda: self.valkey_admin("mng", "PING", check=False).strip() == "PONG"
        )
        docker("restart", f"{PREFIX}-mng-valkey-exporter")
        self.wait(
            lambda: self.value(self.metrics("mng-valkey-exporter"), "redis_up") == "1"
        )
        self.assertNotIn(
            "PONG", self.valkey("mng", "mngmonitor", old, "PING", check=False)
        )

    def test_non_base64_monitor_secret_is_refused_before_any_change(self) -> None:
        name = "mng_pg_monitor_password"
        good, original = self.secret[name], (self.dir / name).read_bytes()
        bad = "quote'and\\backslash\"" + secrets.token_hex(8)
        self.write_secret(name, bad)
        try:
            with self.assertRaises(AssertionError):
                self.provision("mng")
            refused = self.psql_result("mng", "mng_pg_monitor", bad, "SELECT 1")
            self.assertIn("password authentication failed", refused.stderr)
        finally:
            replace_private_fixture(self.dir, name, original.decode("utf-8"))
            self.secret[name] = good
        self.assertNotIn(bad, docker("logs", f"{PREFIX}-mng-pg", check=False))

    def test_prometheus_labels_targets_by_scope_engine_and_expected_state(self) -> None:  # fmt: skip
        self.wait(
            lambda: (
                len(self.scrape_states()) == 4
                and all(v[3] == "1" for v in self.scrape_states().values())
            ),
            attempts=45,
        )
        self.assertEqual(
            {job: value[:3] for job, value in self.scrape_states().items()},
            {
                "manage-postgres": ("mng", "postgresql", "on"),
                "mng-valkey-exporter": ("mng", "valkey", "on"),
                "dev-pg-exporter": ("dev", "postgresql", "on"),
                "dev-valkey-exporter": ("dev", "valkey", "on"),
            },
        )
        docker("stop", f"{PREFIX}-dev-valkey-exporter")
        try:
            self.wait(
                lambda: (
                    self.scrape_states().get("dev-valkey-exporter", "1111")[3] == "0"
                ),
                attempts=45,
            )
        finally:
            docker("start", f"{PREFIX}-dev-valkey-exporter")
        self.wait(
            lambda: self.scrape_states().get("dev-valkey-exporter", "0000")[3] == "1",
            attempts=45,
        )

    def test_promtool_accepts_the_config_and_the_alert_scenarios(self) -> None:
        rules = ROOT / "infra/06-observability/prometheus/config/alert_rules"
        scenarios = self.dir / "alerts.test.yml"
        write_private_fixture(self.dir, scenarios.name, ALERT_TESTS)
        out = docker(
            "run", "--rm", "--entrypoint", "/bin/promtool",
            "-v", f"{rules}/alert_rules.local.datastores.yml:"
            "/t/alert_rules.local.datastores.yml:ro",
            "-v", f"{scenarios}:/t/alerts.test.yml:ro", "-w", "/t",
            PROMETHEUS, "test", "rules", "alerts.test.yml",
        )  # fmt: skip
        self.assertIn("SUCCESS", out)
        check = docker(
            "exec", f"{PREFIX}-prometheus", "promtool", "check", "config",
            "/etc/prometheus/prometheus.yml",
        )  # fmt: skip
        self.assertIn("SUCCESS", check)
