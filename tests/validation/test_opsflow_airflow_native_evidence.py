"""Docker-free failure evidence and exact Airflow config boundaries."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.validation import _opsflow_airflow_native_fixture as fixture
from tests.validation import _opsflow_airflow_native_guards as guards


class AirflowNativeEvidenceTests(unittest.TestCase):
    def test_s3_policy_denials_survive_optimized_python(self):
        import subprocess

        code = """from tests.validation._opsflow_airflow_native_guards import validate_s3_policy, RehearsalFailure
for raw in ['{}', '{"locations":[{"locationPrefix":"/buckets/other","volumeGrowthCount":7}]}', '{"locations":[{"locationPrefix":"/buckets/opsflow-dev","volumeGrowthCount":7}]}']:
 try: validate_s3_policy(raw)
 except RehearsalFailure: continue
 raise SystemExit('invalid policy accepted')
"""
        result = subprocess.run(
            ["/usr/bin/python3", "-O", "-B", "-s", "-S", "-P", "-c", code],
            env={
                "PATH": "/usr/bin:/bin",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "PYTHONPATH": str(fixture.ROOT),
            },
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(
            0, result.returncode, "optimized policy guard accepted invalid input"
        )

    def test_seaweed_policy_is_read_back_before_acceptance(self):
        good = {
            "locations": [
                {"locationPrefix": "/buckets/opsflow-dev", "volumeGrowthCount": 1}
            ],
            "version": 1,
        }
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        f.execute = mock.Mock(
            side_effect=["", "shell> " + json.dumps(good) + "\nshell> "]
        )
        f.configure_s3()
        calls = f.execute.call_args_list
        self.assertEqual(2, len(calls))
        self.assertIn("-volumeGrowthCount=1 -apply", calls[0].args[3])
        self.assertIn("printf 'fs.configure\\n'", calls[1].args[3])
        for bad in (
            {"locations": []},
            {"locations": good["locations"] * 2},
            {
                "locations": [
                    {"locationPrefix": "/buckets/other", "volumeGrowthCount": 1}
                ]
            },
            {
                "locations": [
                    {
                        "locationPrefix": "/buckets/opsflow-dev",
                        "volumeGrowthCount": True,
                    }
                ]
            },
            {
                "locations": [
                    {"locationPrefix": "/buckets/opsflow-dev", "volumeGrowthCount": 7}
                ]
            },
        ):
            with self.subTest(bad=bad), self.assertRaises(fixture.RehearsalFailure):
                guards.validate_s3_policy(json.dumps(bad))
        for bad in (
            "Running in simulation mode. " + json.dumps(good),
            '{"locations":[],"locations":[]}',
            "not JSON",
            "x" * 65537,
        ):
            with (
                self.subTest(bad=bad[:30]),
                self.assertRaises(fixture.RehearsalFailure),
            ):
                guards.validate_s3_policy(bad)

    def test_seaweed_volume_policy_is_applied_initially_and_after_restore(self):
        import ast
        import inspect

        from tests.validation.test_opsflow_airflow_native_rehearsal import (
            PublicationScenario,
        )

        tree = ast.parse(inspect.getsource(PublicationScenario))
        callers = {
            method.name: [
                node
                for node in ast.walk(method)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "configure_s3"
            ]
            for method in tree.body[0].body
            if isinstance(method, ast.FunctionDef)
        }
        for method in ("initialize_airflow", "recover"):
            with self.subTest(method=method):
                self.assertEqual(1, len(callers[method]))

    def test_probe_uses_image_default_user_and_no_writable_airflow_home(self):
        args = fixture.create_options("probe", "airflow")
        self.assertNotIn("--user", args)
        self.assertEqual(1, args.count("--tmpfs"))

    def test_postgres_host_rules_are_exact_per_cluster(self):
        from tests.validation.test_opsflow_airflow_native_rehearsal import (
            PublicationScenario,
        )

        for role, expected in (
            ("metadata-pg", "host airflow airflow samenet scram-sha-256"),
            ("dev-pg", "host opsflow_dev opsflow_ingest samenet scram-sha-256"),
        ):
            for generation in (1, 2):
                with self.subTest(role=role, generation=generation):
                    scenario = PublicationScenario.__new__(PublicationScenario)
                    scenario.f = mock.Mock(generation=generation)
                    scenario.postgres(role, "owned", role)
                    command = scenario.f.create.call_args.args[4][2]
                    self.assertEqual(1, command.count(expected))
                    self.assertLess(command.index("initdb "), command.index(expected))
                    self.assertLess(
                        command.index(expected), command.index("exec postgres")
                    )
                    self.assertIn(
                        "--auth-local=trust --auth-host=scram-sha-256", command
                    )
                    self.assertIn("listen_addresses='*'", command)
                    self.assertEqual(
                        [expected],
                        [
                            line
                            for line in command.split("'")
                            if line.startswith("host ")
                        ],
                    )
        for role in ("unknown", "airflow", "p04_audit", "metadata-pg; true"):
            with self.subTest(role=role), self.assertRaises(fixture.RehearsalFailure):
                guards.postgres_command(role)

    def test_removal_waits_for_exact_absence_within_existing_deadline(self):
        cid = "a" * 64
        present = SimpleNamespace(returncode=0, stdout=cid + "\n", stderr="")
        absent = SimpleNamespace(
            returncode=1, stdout="\n", stderr="error: no such object: " + cid + "\n"
        )
        for outcomes, succeeds in (
            ([present, absent], True),
            ([present] * 20, False),
            (
                [SimpleNamespace(returncode=1, stdout="", stderr="permission denied")],
                False,
            ),
        ):
            with self.subTest(succeeds=succeeds, first=outcomes[0].returncode):
                f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
                f.containers, f.receipt = {"scheduler": SimpleNamespace(cid=cid)}, {}
                f.verify, f.client = mock.Mock(), mock.Mock()
                f.client.deadline, f.client.cleanup_deadline = 500.0, 104.0
                f.client.run.side_effect = OSError("synthetic rm timeout")
                remaining = iter(outcomes)

                def inspect(*_, f=f, remaining=remaining):
                    self.assertEqual(104.0, f.client.cleanup_deadline)
                    return next(remaining)

                f.client.run_result.side_effect = inspect
                with (
                    mock.patch.object(
                        fixture.time, "monotonic", side_effect=range(100, 150)
                    ),
                    mock.patch.object(fixture.time, "sleep"),
                ):
                    if succeeds:
                        f.remove("scheduler")
                    else:
                        with self.assertRaises(fixture.RehearsalFailure):
                            f.remove("scheduler")
                self.assertEqual(not succeeds, "scheduler" in f.containers)
                self.assertEqual(104.0, f.client.cleanup_deadline)
                f.client.run.assert_called_once_with("rm", "-f", "-v", cid)
                for call in f.client.run_result.call_args_list:
                    self.assertEqual(("inspect", "--format", "{{.Id}}", cid), call.args)
                if succeeds:
                    self.assertEqual(2, f.client.run_result.call_count)

    def test_absence_classifier_rejects_unrelated_errors_and_identifiers(self):
        cid = "a" * 64
        for status, stdout, stderr in (
            (1, "", "permission denied"),
            (1, "", "error: no such object: " + "b" * 64),
            (1, "unexpected", "error: no such object: " + cid),
            (125, "", "error: no such object: " + cid),
            (0, "b" * 64, ""),
        ):
            with (
                self.subTest(status=status, stdout=stdout),
                self.assertRaises(fixture.RehearsalFailure),
            ):
                guards.exact_container_absent(
                    SimpleNamespace(returncode=status, stdout=stdout, stderr=stderr),
                    cid,
                )

    def test_removal_poll_cancellation_preserves_record_and_deadline(self):
        for error in (KeyboardInterrupt(), SystemExit(7)):
            f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
            f.containers, f.receipt = {"scheduler": SimpleNamespace(cid="a" * 64)}, {}
            f.verify, f.client = mock.Mock(), mock.Mock()
            f.client.deadline, f.client.cleanup_deadline = 500.0, None

            def inspect(*_, f=f, error=error):
                self.assertEqual(105.0, f.client.deadline)
                raise error

            f.client.run_result.side_effect = inspect
            with mock.patch.object(fixture.time, "monotonic", return_value=100.0):
                with self.assertRaises(type(error)) as caught:
                    f.remove("scheduler")
            self.assertIs(error, caught.exception)
            self.assertIn("scheduler", f.containers)
            self.assertEqual(500.0, f.client.deadline)
            f.client.run_result.assert_called_once()

    def test_registered_lifecycle_preserves_first_scenario_cancellation(self):
        from tests.validation.test_opsflow_airflow_native_rehearsal import (
            AirflowNativeRehearsal,
            PublicationScenario,
        )

        for original in (KeyboardInterrupt(), SystemExit(7)):
            for cleanup_error in (
                fixture.RehearsalFailure("cleanup failed"),
                KeyboardInterrupt(),
                SystemExit(9),
            ):
                owned = mock.Mock(receipt={"cleanup": "FAIL"})
                owned.cleanup.side_effect = cleanup_error
                with (
                    mock.patch.object(fixture, "AirflowFixture", return_value=owned),
                    mock.patch.object(
                        PublicationScenario, "__init__", return_value=None
                    ),
                    mock.patch.object(PublicationScenario, "run", side_effect=original),
                    mock.patch("builtins.print") as printed,
                ):
                    with self.assertRaises(type(original)) as caught:
                        AirflowNativeRehearsal().test_actual_celery_publication_retry_replay_and_empty_restore()
                    self.assertIs(original, caught.exception)
                    owned.cleanup.assert_called_once()
                    printed.assert_called_once_with(
                        json.dumps(owned.receipt, sort_keys=True)
                    )

    def test_failure_output_is_private_bounded_and_retained(self):
        with tempfile.TemporaryDirectory() as directory:
            f = self.base_owned(directory)
            f.exec_result = mock.Mock(
                return_value=SimpleNamespace(
                    returncode=7,
                    stdout="synthetic-secret-" + "public " * 50000,
                    stderr="synthetic-secret-stderr",
                )
            )
            with self.assertRaises(fixture.RehearsalFailure):
                f.execute(
                    "scheduler", "airflow", "db", "migrate", input_="secret-input"
                )
            evidence = f.receipt["command_failure"]
            self.assertTrue(evidence["capture_complete"])
            self.assertEqual(
                ("scheduler", "airflow-db-migrate", 7),
                (evidence["role"], evidence["command"], evidence["exit_code"]),
            )
            self.assertNotIn("synthetic-secret", json.dumps(f.receipt))
            self.assertNotIn("secret-input", json.dumps(f.receipt))
            for stream in ("stdout", "stderr"):
                path = f.directory / ("failure-" + stream + ".txt")
                self.assertLessEqual(path.stat().st_size, 256 * 1024)
                self.assertEqual(0o600, path.stat().st_mode & 0o777)
                self.assertEqual(evidence[stream]["sha256"], fixture.sha256(path))
            self.assertTrue(evidence["stdout"]["truncated"])
            self.assertEqual(5, len(f.files))
            f.client, f._cleanup_host, f._unlock = mock.Mock(), mock.Mock(), mock.Mock()
            f.deadline = f.client.cleanup_deadline = float("inf")
            f.containers, f.networks, f.pending_containers, f.pending_networks = (
                {} for _ in range(4)
            )
            f.runtime_images, f.attempt, f.dir_identity = {}, "synthetic", (1, 2)
            f.client.run.return_value = ""
            with self.assertRaises(fixture.RehearsalFailure):
                f.cleanup()
            f._cleanup_host.assert_not_called()
            self.assertIn(
                "protected failure evidence retained", f.receipt["cleanup_failures"]
            )

    def test_cleanup_observes_safe_stage_and_exact_absence(self):
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        record = SimpleNamespace(cid="a" * 64)
        f.containers, f.receipt, f.verify, f.client = (
            {"scheduler": record},
            {},
            mock.Mock(),
            mock.Mock(),
        )
        f.verify.side_effect = PermissionError("synthetic-secret-message")
        with self.assertRaises(PermissionError):
            f.remove("scheduler")
        observed = f.receipt["cleanup_observations"][-1]
        self.assertEqual(
            ("scheduler", "verify", "PermissionError", None),
            (
                observed["role"],
                observed["stage"],
                observed["exception"],
                observed["absent"],
            ),
        )
        self.assertNotIn("synthetic-secret", json.dumps(observed))
        f.verify.side_effect = None
        f.client.deadline, f.client.cleanup_deadline = float("inf"), None
        f.client.run.side_effect = OSError("synthetic-secret-message")
        f.client.run_result.return_value = SimpleNamespace(
            returncode=1, stdout="", stderr="error: no such object: " + record.cid
        )
        f.remove("scheduler")
        observed = f.receipt["cleanup_observations"][-1]
        self.assertEqual(
            ("removed", "OSError", 1, True),
            (
                observed["stage"],
                observed["rm_exception"],
                observed["inspect_exit"],
                observed["absent"],
            ),
        )

    def test_evidence_is_exclusive_and_unchecked_sql_does_not_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            f = self.base_owned(directory)
            f.exec_result = mock.Mock(
                return_value=SimpleNamespace(
                    returncode=2, stdout="synthetic-private", stderr=""
                )
            )
            f.psql("dev-pg", "public-synthetic", check=False)
            self.assertEqual({}, f.receipt)
            target = f.directory / "existing-synthetic"
            target.write_text("unchanged-public-synthetic")
            (f.directory / "failure-stdout.txt").symlink_to(target)
            original_files = dict(f.files)
            with self.assertRaises(OSError):
                f.psql("dev-pg", "public-synthetic")
            self.assertEqual("unchanged-public-synthetic", target.read_text())
            self.assertEqual(original_files, f.files)
            self.assertFalse(f.receipt["command_failure"]["capture_complete"])
            self.assertEqual(
                {path.name: identity for path, identity in original_files.items()},
                f.receipt["command_failure"]["partial_file_identities"],
            )
            self.assertNotIn("synthetic-private", json.dumps(f.receipt))

    def test_evidence_rejects_nonprivate_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            f = self.base_owned(directory)
            f.exec_result = mock.Mock(
                return_value=SimpleNamespace(
                    returncode=1, stdout="synthetic", stderr=""
                )
            )
            f.directory.chmod(0o755)
            try:
                with self.assertRaises(fixture.RehearsalFailure):
                    f.execute("scheduler", "airflow", "db", "migrate")
                self.assertEqual(
                    {"docker-config", "synthetic-input.json", "synthetic-secrets.json"},
                    {p.name for p in f.directory.iterdir()},
                )
                self.assertFalse(f.receipt["command_failure"]["capture_complete"])
            finally:
                f.directory.chmod(0o700)

    def test_evidence_caps_both_streams_and_rejects_identity_drift(self):
        result = SimpleNamespace(
            returncode=-9,
            stdout="HEAD" + "x" * 300000 + "TAIL",
            stderr="한" * 100000 + "END-PUBLIC",
        )
        fact, streams = fixture.failure_evidence(
            "scheduler", ("airflow", "db", "migrate"), result
        )
        self.assertEqual("signal", fact["exit_class"])
        self.assertTrue(streams["stdout"].startswith("HEAD"))
        self.assertTrue(streams["stdout"].endswith("TAIL"))
        self.assertTrue(streams["stderr"].endswith("END-PUBLIC"))
        for name in ("stdout", "stderr"):
            self.assertLessEqual(len(streams[name].encode()), 256 * 1024)
            self.assertTrue(fact[name]["truncated"])
        for role, code in (
            ("secret-role", 1),
            ("scheduler", True),
            ("scheduler", 1000),
        ):
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.failure_evidence(
                    role, ("secret-argv",), SimpleNamespace(returncode=code)
                )
        error = type("secret-exception-name", (Exception,), {})("secret-message")
        self.assertEqual("OtherException", fixture.safe_exception(error))
        observed = fixture.cleanup_observation("secret-stage", "secret-role", error)
        self.assertNotIn("secret", json.dumps(observed))

    @staticmethod
    def base_owned(directory):
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        f.directory, f.files, f.receipt = Path(directory), {}, {}
        info = f.directory.stat()
        f.dir_identity = (info.st_dev, info.st_ino)
        (f.directory / "docker-config").mkdir(mode=0o700)
        values = {
            key: "synthetic-" + key + "-" + "a" * 40
            for key in "metadata valkey s3_key s3_secret fernet jwt".split()
        }
        values["ingest"] = "p04-ingest-synthetic-only"
        f.private("synthetic-input.json", "public-input")
        f.private("synthetic-secrets.json", json.dumps(values))
        return f

    @classmethod
    def captured(cls, directory):
        f = cls.base_owned(directory)
        f.exec_result = mock.Mock(
            return_value=SimpleNamespace(
                returncode=1, stdout="private-out", stderr="private-error"
            )
        )
        try:
            f.execute("scheduler", "airflow", "db", "migrate")
        except fixture.RehearsalFailure:
            pass
        return f

    def test_capture_manifest_binds_all_files_and_rejects_restart_tamper(self):
        self.assertEqual(
            {
                "synthetic-input.json",
                "synthetic-secrets.json",
                "failure-stdout.txt",
                "failure-stderr.txt",
                "metadata-pg-snapshot",
                "dev-pg-snapshot",
                "metadata-pg-roles",
                "dev-pg-roles",
                "s3-snapshot.json",
            },
            guards._RETAINED_FILES,
        )
        for change in (
            "none",
            "stream",
            "metadata-replace",
            "metadata-link",
            "extra",
            "missing",
            "config-replace",
        ):
            with (
                self.subTest(change=change),
                tempfile.TemporaryDirectory() as directory,
            ):
                f = self.captured(directory)
                identity = f.receipt["command_failure"]["metadata_identity"]
                value = fixture.retained_failure_evidence(f.directory, identity)
                self.assertEqual(
                    set(f.files) - {f.directory / "failure-metadata.json"},
                    {f.directory / name for name in value["file_identities"]},
                )
                self.assertNotIn("synthetic-only-private", json.dumps(value))
                self.assertNotIn("private-error", json.dumps(f.receipt))
                metadata = f.directory / "failure-metadata.json"
                if change == "none":
                    continue
                if change == "stream":
                    (f.directory / "failure-stderr.txt").write_text("changed")
                elif change == "metadata-replace":
                    body = metadata.read_bytes()
                    metadata.unlink()
                    metadata.write_bytes(body)
                    metadata.chmod(0o600)
                elif change == "metadata-link":
                    metadata.unlink()
                    metadata.symlink_to(f.directory / "synthetic-secrets.json")
                elif change == "extra":
                    (f.directory / "unexpected.txt").write_text("public")
                elif change == "missing":
                    (f.directory / "failure-stdout.txt").unlink()
                else:
                    (f.directory / "docker-config").rmdir()
                    (f.directory / "docker-config").mkdir(mode=0o700)
                with self.assertRaises((fixture.RehearsalFailure, OSError)):
                    fixture.retained_failure_evidence(f.directory, identity)

    def test_cleanup_finalizes_receipt_then_preserves_original_cancellation(self):
        for stage in ("begin", "container-remove", "unlock"):
            for kind in (KeyboardInterrupt, SystemExit):
                with self.subTest(stage=stage, kind=kind.__name__):
                    f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
                    error = kind("synthetic-cancel")
                    f.client, f._cleanup_host, f._unlock = (
                        mock.Mock(),
                        mock.Mock(),
                        mock.Mock(),
                    )
                    f.deadline = f.client.cleanup_deadline = float("inf")
                    f.directory, f.dir_identity = Path("/tmp/owned"), (1, 2)
                    (
                        f.containers,
                        f.networks,
                        f.pending_containers,
                        f.pending_networks,
                    ) = ({} for _ in range(4))
                    f.runtime_images, f.receipt, f.attempt = {}, {}, "synthetic"
                    f.client.run.return_value = ""
                    if stage == "begin":
                        f.client.begin_cleanup.side_effect = error
                        f._unlock.side_effect = SystemExit("second-cancel")
                    elif stage == "container-remove":
                        f.containers["scheduler"] = SimpleNamespace(cid="a" * 64)
                        f.remove = mock.Mock(side_effect=error)
                    else:
                        f._unlock.side_effect = error
                    with self.assertRaises(kind) as caught:
                        f.cleanup()
                    self.assertIs(error, caught.exception)
                    self.assertEqual("FAIL", f.receipt["cleanup"])
                    self.assertTrue(
                        any(
                            o["stage"] == stage and o["exception"] == kind.__name__
                            for o in f.receipt["cleanup_observations"]
                        )
                    )
                    f._unlock.assert_called_once()
                    if stage != "unlock":
                        f._cleanup_host.assert_not_called()
                        self.assertIsNone(f.receipt["retained"]["swept_container_ids"])

    def test_simple_auth_passwords_key_uses_existing_private_tmpfs(self):
        env = dict(value.split("=", 1) for value in fixture.airflow_environment())
        key = "AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE"
        self.assertEqual("/run/airflow-fixture/simple-passwords.json", env.get(key))
        self.assertNotIn("AIRFLOW__SIMPLE_AUTH_MANAGER__PASSWORDS_FILE", env)
        options = fixture.create_options("api", "50000:0")
        self.assertIn("--read-only", options)
        self.assertTrue(
            any(value.startswith("/run/airflow-fixture:") for value in options)
        )

    def test_config_override_is_exact_and_uses_existing_tmpfs(self):
        self.assertIn("AIRFLOW_CONFIG=/tmp/airflow.cfg", fixture.airflow_environment())
        fixture.validate_airflow_environment("AIRFLOW_CONFIG=/tmp/airflow.cfg")
        for assignment in (
            "AIRFLOW_CONFIG=/etc/airflow.cfg",
            "AIRFLOW_CONFIG=",
            "AIRFLOW_HOME=/tmp",
            "AIRFLOW__API__TOKEN=secret",
        ):
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.validate_airflow_environment(assignment)


class AirflowUploadContextTests(unittest.TestCase):
    @staticmethod
    def owned(directory):
        f = AirflowNativeEvidenceTests.base_owned(directory)
        values = json.loads((f.directory / "synthetic-secrets.json").read_text())
        f.client, f.verify, f.remaining = mock.Mock(), mock.Mock(), mock.Mock()
        f.client.deadline = 500.0
        f.containers = {"s3": SimpleNamespace(cid="a" * 64)}
        f.exec_result = mock.Mock()
        return f, values

    @staticmethod
    def result(code=1, stdout="client", stderr="original client"):
        return SimpleNamespace(returncode=code, stdout=stdout, stderr=stderr)

    def test_prewrite_redaction_covers_variants_generic_tokens_and_boundary(self):
        import base64
        import urllib.parse

        with tempfile.TemporaryDirectory() as directory:
            f, values = self.owned(directory)
            secret = values["s3_secret"]
            variants = {
                v
                for value in values.values()
                for v in (
                    value,
                    urllib.parse.quote(value, safe=""),
                    base64.b64encode(value.encode()).decode(),
                    base64.urlsafe_b64encode(value.encode()).decode(),
                    json.dumps(value)[1:-1],
                )
            }
            scheme = "postgresql"
            generic = (
                f"{scheme}://different-user:other-pass@example.invalid/ "
                'Bearer not-a-real-access-value {"password":"other-password"} '
                "token=other-token eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwdWJsaWMifQ.signature "
                "UnregisteredOpaqueValueForThisTest0123456789"
            )
            raw = (
                "public " * 21844
                + secret
                + " public " * 30000
                + " ".join(variants)
                + generic
            )
            f.exec_result.return_value = self.result(stdout=raw, stderr=raw)
            writes = []
            private = f.private

            def observed(name, body):
                if name.startswith("failure-"):
                    writes.append(body)
                return private(name, body)

            f.private = observed
            with self.assertRaises(fixture.RehearsalFailure):
                f.execute("worker", "python", "-c", "public-command")
            self.assertTrue(writes)
            for stream in ("stdout", "stderr"):
                self.assertEqual(
                    len(raw.encode()),
                    f.receipt["command_failure"][stream]["raw_source_bytes"],
                )
            for text in writes:
                for value in variants | {
                    "other-pass",
                    "other-password",
                    "other-token",
                    "not-a-real-access-value",
                    "UnregisteredOpaqueValueForThisTest0123456789",
                }:
                    self.assertFalse(
                        value in text, "pre-write redaction left a sensitive test value"
                    )
            for name in ("failure-stdout.txt", "failure-stderr.txt"):
                body = (f.directory / name).read_bytes()
                self.assertLessEqual(len(body), 256 * 1024)
                self.assertNotIn(secret[:32].encode(), body)
            self.assertEqual(
                "before-retention", f.receipt["command_failure"]["redaction"]
            )
            fixture.retained_failure_evidence(
                f.directory, f.receipt["command_failure"]["metadata_identity"]
            )

    def test_registry_replacement_fails_before_any_stream_write(self):
        for mutation in ("missing", "replacement", "symlink"):
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                f, _ = self.owned(directory)
                path = f.directory / "synthetic-secrets.json"
                path.unlink()
                if mutation == "replacement":
                    path.write_text("{}")
                    path.chmod(0o600)
                elif mutation == "symlink":
                    path.symlink_to(f.directory / "synthetic-input.json")
                with self.assertRaises((fixture.RehearsalFailure, OSError)):
                    f.capture_failure(
                        "worker",
                        ("python",),
                        self.result(stdout="withheld", stderr="withheld"),
                    )
                self.assertFalse((f.directory / "failure-stdout.txt").exists())
                self.assertFalse((f.directory / "failure-stderr.txt").exists())
                self.assertFalse(f.receipt["command_failure"]["capture_complete"])

    def test_only_initial_full_upload_opts_into_server_context(self):
        import inspect

        from tests.validation.test_opsflow_airflow_native_rehearsal import (
            PublicationScenario,
        )

        source = inspect.getsource(PublicationScenario.run)
        self.assertEqual(1, source.count("s3_failure_logs=True"))
        self.assertEqual(
            1, inspect.getsource(PublicationScenario).count("s3_failure_logs=True")
        )
        self.assertIn("manifest-input/hy-home.docker/2026-10-10.json", source)

    def test_success_has_no_additional_docker_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            f, _ = self.owned(directory)
            f.exec_result.return_value = self.result(0, "public-ok", "")
            self.assertEqual(
                "public-ok",
                f.execute("worker", "python", "-c", "public", s3_failure_logs=True),
            )
            f.verify.assert_not_called()
            f.client.run_result.assert_not_called()

    def test_failed_upload_preserves_client_and_exact_bounded_server_context(self):
        with tempfile.TemporaryDirectory() as directory:
            f, values = self.owned(directory)
            f.exec_result.return_value = self.result(
                7, "public-client", "ClientError InternalError " + values["ingest"]
            )
            f.client.run_result.return_value = self.result(
                0, "server public cause " + values["s3_secret"], ""
            )

            def verify(*_, **__):
                self.assertEqual(105.0, f.client.deadline)

            f.verify.side_effect = verify
            with mock.patch.object(fixture.time, "monotonic", return_value=100.0):
                with self.assertRaises(fixture.RehearsalFailure):
                    f.execute("worker", "python", "-c", "public", s3_failure_logs=True)
            f.client.run_result.assert_called_once_with(
                "logs", "--tail", "100", "a" * 64
            )
            self.assertEqual(500.0, f.client.deadline)
            fact = f.receipt["command_failure"]
            self.assertEqual(
                (7, "COMPLETE"), (fact["exit_code"], fact["s3_log_capture"])
            )
            body = (f.directory / "failure-stderr.txt").read_text()
            self.assertIn("ClientError InternalError", body)
            self.assertIn("server public cause", body)
            self.assertNotIn(values["ingest"], body)
            self.assertNotIn(values["s3_secret"], body)

    def test_partial_logs_low_memory_and_first_cancellation(self):
        for cause in ("logs", "memory", "cancel", "cancel-write"):
            with self.subTest(cause=cause), tempfile.TemporaryDirectory() as directory:
                f, _ = self.owned(directory)
                f.exec_result.return_value = self.result(9)
                cancellation = KeyboardInterrupt()
                if cause == "memory":
                    f.remaining.side_effect = fixture.RehearsalFailure("low RAM")
                else:
                    f.client.run_result.side_effect = (
                        cancellation
                        if cause.startswith("cancel")
                        else OSError("withheld")
                    )
                expected = (
                    KeyboardInterrupt
                    if cause.startswith("cancel")
                    else fixture.RehearsalFailure
                )
                if cause == "cancel-write":
                    f.private = mock.Mock(side_effect=OSError("capture write failed"))
                with self.assertRaises(expected) as caught:
                    f.execute("worker", "python", "-c", "public", s3_failure_logs=True)
                if cause.startswith("cancel"):
                    self.assertIs(cancellation, caught.exception)
                if cause == "memory":
                    f.verify.assert_not_called()
                    f.client.run_result.assert_not_called()
                self.assertEqual(500.0, f.client.deadline)
                fact = f.receipt["command_failure"]
                self.assertEqual(9, fact["exit_code"])
                self.assertEqual("PARTIAL", fact["s3_log_capture"])
                if cause == "cancel-write":
                    self.assertFalse(fact["capture_complete"])
                    self.assertEqual("OSError", fact["capture_exception"])
                else:
                    self.assertIn(
                        "original client",
                        (f.directory / "failure-stderr.txt").read_text(),
                    )


if __name__ == "__main__":
    unittest.main()
