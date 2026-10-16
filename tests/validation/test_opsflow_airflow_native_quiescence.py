"""Docker-free guards for actual Celery quiescence output and failure custody."""

import base64
import contextlib
import inspect
import io
import json
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from tests.validation import _opsflow_airflow_native_evidence as evidence
from tests.validation import _opsflow_airflow_native_fixture as fixture
from tests.validation import test_opsflow_airflow_native_evidence as evidence_tests


class AirflowNativeQuiescenceTests(unittest.TestCase):
    @staticmethod
    def owned(result):
        return SimpleNamespace(
            containers={"worker": SimpleNamespace(name="actual-g1-worker")},
            exec_result=mock.Mock(return_value=result),
        )

    @staticmethod
    def result(stdout, code=0, stderr=""):
        return SimpleNamespace(returncode=code, stdout=stdout, stderr=stderr)

    def test_noisy_import_and_inspect_emit_only_one_json_stdout(self):
        original_import = __import__
        state = {"celery@actual-g1-worker": []}

        def noisy_value():
            print("public third-party inspect output")
            return state

        inspector = SimpleNamespace(active=noisy_value, reserved=noisy_value)
        app = SimpleNamespace(control=SimpleNamespace(inspect=lambda **_: inspector))

        def noisy_import(name, *args, **kwargs):
            if name == "airflow.providers.celery.executors.celery_executor_utils":
                print("public third-party import output")
                return SimpleNamespace(app=app)
            return original_import(name, *args, **kwargs)

        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            mock.patch("builtins.__import__", side_effect=noisy_import),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exec(evidence.CELERY_IDLE, {})
        self.assertEqual(
            {"active": state, "reserved": state}, json.loads(stdout.getvalue())
        )
        self.assertEqual(1, stdout.getvalue().count("\n"))
        self.assertIn("public third-party import output", stderr.getvalue())
        self.assertEqual(
            2, stderr.getvalue().count("public third-party inspect output")
        )

    def test_exact_actual_host_and_empty_states_are_required(self):
        good = {key: {"celery@actual-g1-worker": []} for key in ("active", "reserved")}
        owned = self.owned(self.result(json.dumps(good)))
        with mock.patch.object(evidence, "capture_failure") as captured:
            self.assertEqual(good, evidence.inspect_celery_idle(owned))
        captured.assert_not_called()
        for key in good:
            for wrong in (
                {},
                {"celery@configured-worker": []},
                {"celery@actual-g1-worker": ["busy"]},
            ):
                bad = {**good, key: wrong}
                owned = self.owned(self.result(json.dumps(bad)))
                with mock.patch.object(evidence, "capture_failure") as captured:
                    with self.assertRaises(fixture.RehearsalFailure):
                        evidence.inspect_celery_idle(owned)
                captured.assert_called_once()

    def test_nonzero_and_unparseable_results_are_captured_without_rc_rewrite(self):
        for result, error in (
            (self.result("{}", code=7), fixture.RehearsalFailure),
            (self.result("2026 public output\n{}"), json.JSONDecodeError),
            (self.result("[]"), fixture.RehearsalFailure),
            (self.result("{}"), fixture.RehearsalFailure),
            (self.result('{"active":{},"active":{}}'), fixture.RehearsalFailure),
        ):
            owned = self.owned(result)
            with mock.patch.object(evidence, "capture_failure") as captured:
                with self.assertRaises(error):
                    evidence.inspect_celery_idle(owned)
            self.assertIs(result, captured.call_args.args[3])
            self.assertEqual("worker", captured.call_args.args[1])
            self.assertEqual(
                ("python", "-c", evidence.CELERY_IDLE), captured.call_args.args[2]
            )

    def test_rc_zero_parse_failure_is_redacted_before_private_retention(self):
        with tempfile.TemporaryDirectory() as temporary:
            owned = evidence_tests.AirflowNativeEvidenceTests.base_owned(temporary)
            values = json.loads(
                (owned.directory / "synthetic-secrets.json").read_text()
            )
            secret = values["s3_secret"]
            encoded = base64.b64encode(secret.encode()).decode()
            owned.containers = {"worker": SimpleNamespace(name="actual-g1-worker")}
            owned.exec_result = mock.Mock(return_value=self.result(secret + encoded))
            with self.assertRaises(json.JSONDecodeError):
                evidence.inspect_celery_idle(owned)
            fact = owned.receipt["command_failure"]
            self.assertEqual(
                (0, "success", True),
                (fact["exit_code"], fact["exit_class"], fact["capture_complete"]),
            )
            self.assertEqual("before-retention", fact["redaction"])
            output = (owned.directory / "failure-stdout.txt").read_text()
            self.assertNotIn(secret, output)
            self.assertNotIn(encoded, output)
            fixture.retained_failure_evidence(
                owned.directory, fact["metadata_identity"]
            )

    def test_original_parse_error_and_first_cancellation_are_preserved(self):
        for capture_error, expected in (
            (OSError("public capture failure"), json.JSONDecodeError),
            (KeyboardInterrupt(), KeyboardInterrupt),
            (SystemExit(9), SystemExit),
        ):
            owned = self.owned(self.result("not JSON"))
            with mock.patch.object(
                evidence, "capture_failure", side_effect=capture_error
            ):
                with self.assertRaises(expected):
                    evidence.inspect_celery_idle(owned)
        owned = self.owned(self.result("{}"))
        with (
            mock.patch.object(evidence.json, "loads", side_effect=KeyboardInterrupt()),
            mock.patch.object(evidence, "capture_failure") as captured,
        ):
            with self.assertRaises(KeyboardInterrupt):
                evidence.inspect_celery_idle(owned)
        captured.assert_not_called()
        owned.exec_result.side_effect = KeyboardInterrupt()
        with mock.patch.object(evidence, "capture_failure") as captured:
            with self.assertRaises(KeyboardInterrupt):
                evidence.inspect_celery_idle(owned)
        captured.assert_not_called()

    def test_registered_lifecycle_preserves_primary_and_cancellation_through_finalization(
        self,
    ):
        from tests.validation import test_opsflow_airflow_native_rehearsal as native

        ordinary = ValueError("public scenario failure")
        cleanup = fixture.RehearsalFailure("public cleanup failure")
        output = BrokenPipeError("public output failure")
        first_cancel, second_cancel = KeyboardInterrupt(), SystemExit(7)
        for original, cleanup_error, print_error, expected in (
            (ordinary, cleanup, None, ordinary),
            (None, cleanup, None, cleanup),
            (None, None, output, output),
            (ordinary, None, output, ordinary),
            (ordinary, cleanup, output, ordinary),
            (ordinary, first_cancel, output, first_cancel),
            (first_cancel, cleanup, output, first_cancel),
            (first_cancel, second_cancel, output, first_cancel),
            (None, None, None, None),
        ):
            owned = mock.Mock(receipt={"cleanup": "FAIL" if cleanup_error else "PASS"})
            owned.cleanup.side_effect = cleanup_error
            scenario = mock.Mock()
            scenario.run.side_effect = original
            with (
                self.subTest(
                    original=type(original).__name__,
                    cleanup=type(cleanup_error).__name__,
                ),
                mock.patch.object(native.fixture, "AirflowFixture", return_value=owned),
                mock.patch.object(native, "PublicationScenario", return_value=scenario),
                mock.patch("builtins.print", side_effect=print_error) as emitted,
            ):
                target = native.AirflowNativeRehearsal()
                if expected is None:
                    target.test_actual_celery_publication_retry_replay_and_empty_restore()
                else:
                    with self.assertRaises(type(expected)) as raised:
                        target.test_actual_celery_publication_retry_replay_and_empty_restore()
                    self.assertIs(expected, raised.exception)
                owned.cleanup.assert_called_once_with()
                emitted.assert_called_once_with(
                    json.dumps(owned.receipt, sort_keys=True)
                )

    def test_role_dump_accepts_digit_after_identifier_start_and_rejects_extra_sql(self):
        for role, names in (
            ("metadata-pg", ("p04_audit", "airflow")),
            (
                "dev-pg",
                (
                    "p04_audit",
                    "opsflow_owner",
                    "opsflow_migrator",
                    "opsflow_ingest",
                    "opsflow_notifier",
                    "opsflow_reader",
                ),
            ),
        ):
            raw = "-- public pg_dumpall roles\n" + "".join(
                f"CREATE ROLE {name};\n" for name in names
            )
            owned = SimpleNamespace(
                execute=mock.Mock(return_value=raw), private=mock.Mock()
            )
            fixture.AirflowFixture.dump_roles(owned, role)
            owned.private.assert_called_once_with(
                role + "-roles", raw.replace("CREATE ROLE p04_audit;", "")
            )
            for extra in (
                "CREATE ROLE foreign;\n",
                "CREATE ROLE 4bad;\n",
                'CREATE ROLE "foreign";\n',
                "CREATE ROLE airflow; SELECT 1;\n",
                "CREATE ROLE p04_audit;\n",
                " CREATE ROLE foreign;\n",
                "\tCREATE ROLE foreign;\n",
                "CREATE\tROLE foreign;\n",
                "CREATE\nROLE foreign;\n",
                "create role foreign;\n",
            ):
                owned.execute.return_value = raw + extra
                with (
                    self.subTest(role=role, extra=extra),
                    self.assertRaises(fixture.RehearsalFailure),
                ):
                    fixture.AirflowFixture.dump_roles(owned, role)

    def test_registered_recovery_uses_only_the_reviewed_idle_helper(self):
        from tests.validation.test_opsflow_airflow_native_rehearsal import (
            PublicationScenario,
        )

        source = inspect.getsource(PublicationScenario.recover)
        self.assertEqual(1, source.count("evidence.inspect_celery_idle(self.f)"))
        self.assertNotIn("app.control.inspect", source)


if __name__ == "__main__":
    unittest.main()
