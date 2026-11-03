"""P05 source/guard tests and an explicit current-artifact native rehearsal."""

import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.validation import _p05_opsflow_native as native
from tests.validation import _p05_opsflow_recovery as recovery


class P05NativeGuards(unittest.TestCase):
    def test_registration_uses_authenticated_personal_project_rest_and_rejects_mismatch(
        self,
    ):
        from tests.validation import _p05_opsflow_registration as registration

        for change in (
            {},
            {"active": True},
            {"project_id": "foreign"},
            {"personal": False},
            {"id": "bad/id"},
            {"unexpected": "private-canary"},
        ):
            calls = []
            fixture = SimpleNamespace(
                attempt="opsflow-native-" + "a" * 24, receipt={}, private=mock.Mock()
            )
            scenario = SimpleNamespace(
                fixture=fixture,
                secrets={"notifier": ("synthetic", None)},
                credential_ids={},
                postgres_credential=lambda _value: {"type": "postgres"},
            )

            def api(action, _calls=calls, _change=change, _fixture=fixture, **payload):
                _calls.append((action, payload))
                if action == "setup":
                    return {"id": "00000000-0000-4000-8000-000000000001"}
                if action == "credential":
                    return {
                        "id": "pg-id"
                        if payload["credential"]["type"] == "postgres"
                        else "smtp-id"
                    }
                if action == "workflow_create":
                    return {
                        "id": "workflow-id",
                        "active": False,
                        "project_id": "personal-id",
                        "personal_project_id": "personal-id",
                        "personal": True,
                        **_change,
                    }
                if action == "workflows":
                    return {
                        "rows": [
                            {
                                "id": "workflow-id",
                                "active": False,
                                "name": "Opsflow native " + _fixture.attempt,
                            }
                        ]
                    }
                raise AssertionError("unexpected API action")

            scenario.api = api
            if change:
                with (
                    self.subTest(fields=tuple(change)),
                    self.assertRaises(native.RehearsalFailure),
                ):
                    registration.register(scenario)
            else:
                identifier, name = registration.register(scenario)
                self.assertEqual("workflow-id", identifier)
                self.assertEqual("Opsflow native " + fixture.attempt, name)
                body = next(
                    payload["workflow"]
                    for action, payload in calls
                    if action == "workflow_create"
                )
                self.assertEqual(
                    {"name", "nodes", "connections", "settings"}, set(body)
                )
                self.assertEqual(
                    "EDITOR_REST_PINNED_2_43_6",
                    fixture.receipt["workflow_registration"]["transport"],
                )

    def test_deployed_public_tree_requires_root_ownership_modes_and_exact_hashes(self):
        expected = {"package.json": "a" * 64}
        rows = [
            {"name": "opsflow", "kind": "directory", "uid": 0, "gid": 0, "mode": 0o755},
            {
                "name": "opsflow/package.json",
                "kind": "file",
                "uid": 0,
                "gid": 0,
                "mode": 0o644,
                "sha256": "a" * 64,
            },
        ]
        self.assertEqual(
            {"files": 1, "directories": 1}, native.validate_deployment(rows, expected)
        )
        for change in (
            {"uid": 1000},
            {"gid": 1000},
            {"mode": 0o664},
            {"sha256": "b" * 64},
            {"kind": "symlink"},
            {"name": "opsflow/../secret"},
        ):
            with (
                self.subTest(fields=tuple(change)),
                self.assertRaises(native.RehearsalFailure),
            ):
                native.validate_deployment([rows[0], {**rows[1], **change}], expected)
        for changed in (
            rows + rows[1:],
            rows[:1],
            [*rows, {**rows[1], "name": "opsflow/extra"}],
        ):
            with self.assertRaises(native.RehearsalFailure):
                native.validate_deployment(changed, expected)

    def test_already_inactive_workflow_fence_uses_verified_state(self):
        scenario = native.P05Scenario(
            "test_actual_queue_runner_capture_unknown_reconcile_and_restore"
        )
        scenario.execution_ids = ["42"]
        scenario.fixture = SimpleNamespace(
            stop=mock.Mock(),
            containers={role: role for role in ("runner", "worker", "mailpit")},
            _verify_owned=lambda _record: {
                "State": {"Status": "exited", "Running": False, "Pid": 0}
            },
            exec_result=lambda *args, **kwargs: SimpleNamespace(
                returncode=0, stdout='{"scanned":true,"matching":0,"ids":["42"]}'
            ),
            receipt={},
            attempt="opsflow-native-" + "a" * 24,
        )

        def api(action, **payload):
            self.assertEqual("workflows", action)
            return {"rows": [{"id": "owned", "active": False, "versionId": "v"}]}

        scenario.api = api
        scenario.fence("owned")
        self.assertTrue(
            scenario.fixture.receipt["recovery_barrier"]["workflow_inactive"]
        )

    def test_mailpit_key_uses_filename_flag_and_keeps_secret_environment_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = object.__new__(native.P05Fixture)
            fixture.directory = Path(directory)
            fixture.generation = 1
            fixture.host_uid = os.geteuid()
            fixture.mailpit_dirs = {}
            fixture.smtp_epoch = 1
            fixture.smtp_files = {1: Path(directory) / "synthetic-auth"}
            fixture.create = mock.Mock()
            fixture.start = mock.Mock()
            fixture.start_mailpit()
            call = fixture.create.call_args
            self.assertIn(
                "--smtp-tls-key=/run/secrets/server.key", call.kwargs.get("command", ())
            )
            self.assertFalse(
                any(
                    "KEY=" in value or "PASSWORD=" in value or "TOKEN=" in value
                    for value in call.kwargs["env"]
                )
            )
            self.assertIn(
                native.inputs.bind_mount(
                    Path(directory) / "p05-server.key", "/run/secrets/server.key"
                ),
                call.kwargs["mounts"],
            )
            fixture.start.assert_called_once_with("mailpit")

    def test_public_artifact_reader_rejects_symlinks_and_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "public.js"
            source.write_bytes(b"public code")
            self.assertEqual(
                hashlib.sha256(b"public code").hexdigest(), native.public_digest(source)
            )
            linked = root / "linked.js"
            linked.symlink_to(source)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(linked)
            (root / "linked-dir").symlink_to(root, target_is_directory=True)
            with self.assertRaises(native.RehearsalFailure):
                native.public_digest(root / "linked-dir/public.js")
            original = os.read

            def changed(descriptor, count):
                result = original(descriptor, count)
                if result:
                    source.write_bytes(b"changed")
                return result

            with mock.patch.object(native.os, "read", side_effect=changed):
                with self.assertRaises(native.RehearsalFailure):
                    native.public_digest(source)

    def test_candidate_is_bound_to_independent_current_dist_and_exact_base(self):
        expected = {"OpsflowSmtp.node.js": "a" * 64, "transport.js": "b" * 64}
        value = {
            "reference": "hy-home/p05-n8n-fixture:" + "c" * 12,
            "image_id": "sha256:" + "d" * 64,
            "base_id": native.inputs.N8N_ID,
            "binding": "c" * 64,
            "dist_sha256": expected,
        }
        self.assertEqual(value, native.validate_artifact(value, "c" * 64, expected))
        for change in (
            {"image_id": "latest"},
            {"base_id": "sha256:" + "e" * 64},
            {"binding": "f" * 64},
            {"dist_sha256": {**expected, "transport.js": "f" * 64}},
            {"unexpected": "private-payload"},
        ):
            with (
                self.subTest(change=tuple(change)),
                self.assertRaises(native.RehearsalFailure),
            ):
                native.validate_artifact({**value, **change}, "c" * 64, expected)

    def test_recovery_requires_real_process_socket_and_exact_job_barriers(self):
        good = {
            "smtp_egress_held": True,
            "workflow_inactive": True,
            "old_execution_ids": ["42"],
            "old_processes_absent": True,
            "old_sockets_absent": True,
            "old_broker_jobs_absent": True,
            "owned_attempt": "opsflow-native-" + "a" * 24,
        }
        self.assertEqual(good, recovery.validate_barrier(good))
        for field in (
            "smtp_egress_held",
            "workflow_inactive",
            "old_processes_absent",
            "old_sockets_absent",
            "old_broker_jobs_absent",
        ):
            for value in (False, 1, None):
                with (
                    self.subTest(field=field, value=value),
                    self.assertRaises(recovery.RehearsalFailure),
                ):
                    recovery.validate_barrier({**good, field: value})
        for change in (
            {"old_execution_ids": []},
            {"old_execution_ids": ["42", "42"]},
            {"cancel_response": True},
            {"old_execution_ids": ["private-payload"]},
        ):
            with self.assertRaises(recovery.RehearsalFailure):
                recovery.validate_barrier({**good, **change})


@unittest.skipUnless(
    os.environ.get("P05_OPSFLOW_NATIVE") == "1",
    "exact current candidate and owned isolated runtime required",
)
class P05NativeRehearsal(unittest.TestCase):
    def test_current_notifier_queue_credentials_and_recovery(self):
        native.run_current_rehearsal()


if __name__ == "__main__":
    unittest.main()
