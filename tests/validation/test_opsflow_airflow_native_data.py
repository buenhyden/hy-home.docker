"""Docker-free proofs for exact object metadata recovery and scoped identities."""

import copy
import hashlib
import io
import json
import unittest
from unittest import mock
from urllib.parse import parse_qsl

from tests.validation import _opsflow_airflow_native_data as data
from tests.validation import _opsflow_airflow_native_fixture as fixture
from tests.validation import _opsflow_airflow_native_guards as guards


class MemoryObjects:
    def __init__(self):
        self.objects = {}
        self.truncated = False

    def list_objects_v2(self, **_):
        return {
            "Contents": [{"Key": key} for key in self.objects],
            "IsTruncated": self.truncated,
        }

    def get_object(self, *, Key, **_):
        item = self.objects[Key]
        return {
            "Body": io.BytesIO(item["Body"]),
            "ContentLength": len(item["Body"]),
            "ContentType": item["ContentType"],
            "Metadata": dict(item["Metadata"]),
        }

    def get_object_tagging(self, *, Key, **_):
        return {"TagSet": copy.deepcopy(self.objects[Key]["Tags"])}

    def put_object(
        self, *, Key, Body, ContentType, Metadata, Tagging, IfNoneMatch, **_
    ):
        if IfNoneMatch != "*" or Key in self.objects:
            raise ValueError("immutable destination")
        self.objects[Key] = {
            "Body": Body,
            "ContentType": ContentType,
            "Metadata": dict(Metadata),
            "Tags": [{"Key": k, "Value": v} for k, v in parse_qsl(Tagging)],
        }


class NativeDataTests(unittest.TestCase):
    def test_permission_acceptance_requires_all_eight_consistent_observations(self):
        names = (
            "allowed_read",
            "allowed_write",
            "foreign_bucket",
            "foreign_prefix",
            "input_write",
            "foreign_write",
            "delete",
            "list",
        )
        good = {
            name: {
                "expected_http": 200 if name.startswith("allowed") else 403,
                "observed_http": 200 if name.startswith("allowed") else 403,
                "passed": True,
            }
            for name in names
        }
        self.assertTrue(data.permissions_passed(good))
        for broken in (
            {},
            {"delete": good["delete"]},
            {k: v for k, v in good.items() if k != "allowed_read"},
            {**good, "allowed_write": {**good["allowed_write"], "observed_http": 403}},
        ):
            with self.subTest(keys=tuple(broken)):
                self.assertFalse(data.permissions_passed(broken))
        self.assertFalse(
            data.permissions_passed(
                {
                    **good,
                    "allowed_read": {**good["allowed_read"], "observed_http": True},
                }
            )
        )
        duplicate = (
            json.dumps(good)[:-1] + ',"delete":' + json.dumps(good["delete"]) + "}"
        )
        with self.assertRaises(data.RehearsalFailure):
            data.parse_permission_observations(duplicate)
        for broken in (
            {"unexpected": "private-payload"},
            {**good, "delete": {**good["delete"], "extra": "private-payload"}},
            {**good, "delete": {**good["delete"], "observed_http": "private-payload"}},
        ):
            with self.assertRaises(data.RehearsalFailure) as raised:
                data.parse_permission_observations(json.dumps(broken))
            self.assertNotIn("private-payload", str(raised.exception))
        for raw in (
            " " * 8193,
            json.dumps(
                {**good, "delete": {**good["delete"], "observed_http": float("nan")}}
            ),
            json.dumps({**good, "delete": {**good["delete"], "observed_http": True}}),
        ):
            with self.assertRaises(data.RehearsalFailure):
                data.parse_permission_observations(raw)

    def test_cleanup_call_budget_respects_existing_final_deadline(self):
        client = fixture.AirflowDockerBoundary.__new__(fixture.AirflowDockerBoundary)
        client.deadline, client.cleanup_deadline = 1000.0, 130.0
        with mock.patch.object(fixture.time, "monotonic", return_value=100.0):
            self.assertEqual(10.0, client._remaining_timeout())
        with mock.patch.object(fixture.time, "monotonic", return_value=128.0):
            self.assertEqual(2.0, client._remaining_timeout())
        with mock.patch.object(fixture.time, "monotonic", return_value=130.0):
            with self.assertRaises(TimeoutError):
                client._remaining_timeout()

    def test_permission_receipt_keeps_each_failure_and_requires_valid_auth(self):
        class Denied(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.response = {"ResponseMetadata": {"HTTPStatusCode": 403}}

        def denied(**_):
            raise Denied("private error must not enter receipt")

        client = mock.Mock()
        client.list_objects_v2.side_effect = denied
        client.delete_object.return_value = {
            "ResponseMetadata": {"HTTPStatusCode": 204}
        }

        def get(*, Bucket, Key):
            if Key == "manifest-input/permission-canary":
                return {
                    "Body": io.BytesIO(b"synthetic"),
                    "ResponseMetadata": {"HTTPStatusCode": 200},
                }
            return denied()

        def put(*, Bucket, Key, Body):
            if Key == "manifest-validated/permission-write":
                return {"ResponseMetadata": {"HTTPStatusCode": 200}}
            return denied()

        client.get_object.side_effect = get
        client.put_object.side_effect = put
        observed = data.permission_observations(client, "opsflow-dev")
        self.assertTrue(observed["allowed_read"]["passed"])
        self.assertTrue(observed["allowed_write"]["passed"])
        self.assertEqual(204, observed["delete"]["observed_http"])
        self.assertFalse(observed["delete"]["passed"])
        self.assertTrue(observed["foreign_prefix"]["passed"])
        self.assertNotIn("private error", json.dumps(observed))
        client.get_object.side_effect = denied
        client.put_object.side_effect = denied
        client.delete_object.side_effect = denied
        observed = data.permission_observations(client, "opsflow-dev")
        self.assertFalse(observed["allowed_read"]["passed"])
        self.assertFalse(observed["allowed_write"]["passed"])
        self.assertTrue(
            all(
                row["passed"]
                for key, row in observed.items()
                if key not in {"allowed_read", "allowed_write"}
            )
        )

    def test_large_legal_snapshot_uses_stdin_instead_of_exec_argument(self):
        original = self.original()
        first = next(iter(original.objects))
        original.objects[first]["Body"] = b"x" * (96 * 1024)
        original.objects["manifest-validated/second"] = copy.deepcopy(
            original.objects[first]
        )
        snapshot = data.capture_objects(original, "opsflow-dev")
        owned = mock.Mock()
        data.restore_snapshot(owned, snapshot)
        call = owned.execute.call_args
        self.assertLess(len(call.args[3].encode()), 4096)
        self.assertEqual(snapshot, json.loads(call.kwargs["input_"]))
        restored = MemoryObjects()
        data.restore_stdin(restored, "opsflow-dev", io.StringIO(call.kwargs["input_"]))
        self.assertEqual(original.objects, restored.objects)

    def test_encoded_and_aggregate_caps_reject_before_decode_or_write(self):
        snapshot = data.capture_objects(self.original(), "opsflow-dev")
        key = next(iter(snapshot))
        snapshot[key]["body"] = "A" * (4 * ((data.MAX_OBJECT_BYTES + 2) // 3) + 1)
        with mock.patch.object(data.base64, "b64decode") as decode:
            with self.assertRaises(data.RehearsalFailure):
                data.restore_objects(MemoryObjects(), "opsflow-dev", snapshot)
            decode.assert_not_called()
        original = self.original()
        first = next(iter(original.objects))
        original.objects[first]["Body"] = b"x" * data.MAX_OBJECT_BYTES
        original.objects["manifest-validated/second"] = copy.deepcopy(
            original.objects[first]
        )
        with self.assertRaises(data.RehearsalFailure):
            data.capture_objects(original, "opsflow-dev")
        with self.assertRaises(data.RehearsalFailure):
            data.restore_stdin(
                MemoryObjects(),
                "opsflow-dev",
                io.StringIO(" " * (data.MAX_SNAPSHOT_BYTES + 1)),
            )

    @staticmethod
    def original():
        client = MemoryObjects()
        client.objects["manifest-input/hy-home.docker/2026-10-10.json"] = {
            "Body": b'{"synthetic":true}',
            "ContentType": "application/json",
            "Metadata": {"source": "synthetic", "data-version": "a" * 64},
            "Tags": [{"Key": "scope", "Value": "synthetic + recovery"}],
        }
        return client

    def test_restore_preserves_body_type_metadata_tags_and_size(self):
        original = self.original()
        snapshot = data.capture_objects(original, "opsflow-dev")
        target = MemoryObjects()
        data.restore_objects(target, "opsflow-dev", snapshot)
        self.assertEqual(original.objects, target.objects)
        row = next(iter(snapshot.values()))
        self.assertEqual(len(b'{"synthetic":true}'), row["size"])
        self.assertEqual(
            hashlib.sha256(b'{"synthetic":true}').hexdigest(), row["sha256"]
        )

    def test_bad_snapshot_is_rejected_before_any_write(self):
        snapshot = data.capture_objects(self.original(), "opsflow-dev")
        key = next(iter(snapshot))
        for field, value in (
            ("body", "not-base64"),
            ("sha256", "b" * 64),
            ("size", 999),
            ("content_type", ""),
            ("metadata", {"invalid": 42}),
            (
                "tags",
                [
                    {"Key": "duplicate", "Value": "a"},
                    {"Key": "duplicate", "Value": "b"},
                ],
            ),
        ):
            broken = {key: {**snapshot[key], field: value}}
            target = MemoryObjects()
            with self.subTest(field=field), self.assertRaises(data.RehearsalFailure):
                data.restore_objects(target, "opsflow-dev", broken)
            self.assertEqual({}, target.objects)

    def test_oversized_truncated_and_foreign_snapshots_fail_closed(self):
        original = self.original()
        original.truncated = True
        with self.assertRaises(data.RehearsalFailure):
            data.capture_objects(original, "opsflow-dev")
        original.truncated = False
        key = next(iter(original.objects))
        original.objects[key]["Body"] = b"x" * (data.MAX_OBJECT_BYTES + 1)
        with self.assertRaises(data.RehearsalFailure):
            data.capture_objects(original, "opsflow-dev")
        for wrong in ("foreign-bucket", "", None):
            with self.subTest(bucket=wrong), self.assertRaises(data.RehearsalFailure):
                data.capture_objects(self.original(), wrong)

    def test_restore_detects_changed_metadata_and_existing_destination(self):
        snapshot = data.capture_objects(self.original(), "opsflow-dev")
        with self.assertRaises(ValueError):
            data.restore_objects(self.original(), "opsflow-dev", snapshot)
        target = MemoryObjects()
        original_put = target.put_object

        def changed(**values):
            original_put(**{**values, "Metadata": {"tampered": "true"}})

        target.put_object = changed
        with self.assertRaises(data.RehearsalFailure):
            data.restore_objects(target, "opsflow-dev", snapshot)

    def test_all_rows_are_validated_before_write_and_cancel_closes_body(self):
        snapshot = data.capture_objects(self.original(), "opsflow-dev")
        key = next(iter(snapshot))
        snapshot["manifest-validated/rejected"] = {**snapshot[key], "sha256": "0" * 64}
        target = MemoryObjects()
        with self.assertRaises(data.RehearsalFailure):
            data.restore_objects(target, "opsflow-dev", snapshot)
        self.assertEqual({}, target.objects)
        original = self.original()
        body = io.BytesIO(b"synthetic")

        class Interrupted:
            def read(self, _):
                raise KeyboardInterrupt()

            def close(self):
                body.close()

        original.get_object = lambda **_: {"Body": Interrupted()}
        with self.assertRaises(KeyboardInterrupt):
            data.capture_objects(original, "opsflow-dev")
        self.assertTrue(body.closed)

    def test_exact_storage_admin_and_nondefault_listener_admission(self):
        options = guards.create_options("storage-admin", "50000:0")
        self.assertIn("--read-only", options)
        self.assertIn("128m", options)
        self.assertNotIn("--publish", options)
        self.assertNotIn("--mount", options)
        self.assertEqual("mng-pg", guards.network_alias("metadata-pg"))
        self.assertEqual("mng-valkey", guards.network_alias("valkey"))
        self.assertIn("-p 55432", guards.postgres_command("metadata-pg")[-1])
        self.assertIn("-p 5432", guards.postgres_command("dev-pg")[-1])
        for assignment in (
            "POSTGRES_PORT=1",
            "VALKEY_PORT=6379",
            "AIRFLOW_VALKEY_SECRET=foreign",
        ):
            with self.assertRaises(guards.RehearsalFailure):
                guards.validate_airflow_environment(assignment)

    def test_worker_and_admin_credentials_have_separate_capabilities(self):
        config = data.s3_configuration(
            "worker-key", "worker-secret", "admin-key", "admin-secret"
        )
        worker, admin = config["identities"]
        self.assertNotEqual(worker["credentials"], admin["credentials"])
        self.assertNotIn("Admin", worker["actions"])
        self.assertTrue(all(":" in action for action in worker["actions"]))
        self.assertEqual(
            ["Admin", "Read", "Write", "List", "Tagging"], admin["actions"]
        )
        statement = data.worker_bucket_policy()["Statement"]
        self.assertEqual(
            "arn:aws:iam::000000000000:user/synthetic-worker",
            statement[0]["Principal"]["AWS"],
        )
        self.assertTrue(
            any(
                row["Effect"] == "Deny" and "s3:DeleteObject" in row["Action"]
                for row in statement
            )
        )

    def test_production_uri_environment_uses_raw_files_and_fixed_ports(self):
        values = dict(row.split("=", 1) for row in data.production_environment())
        self.assertEqual("55432", values["POSTGRES_PORT"])
        self.assertEqual("6389", values["VALKEY_PORT"])
        self.assertEqual("mng-valkey", values["AIRFLOW_VALKEY_HOST"])
        for mode, field in (
            ("metadata", "DATABASE__SQL_ALCHEMY_CONN_CMD"),
            ("result", "CELERY__RESULT_BACKEND_CMD"),
            ("broker", "CELERY__BROKER_URL_CMD"),
        ):
            self.assertEqual(
                "python3 /opt/airflow/bin/connection_uri.py " + mode,
                values["AIRFLOW__" + field],
            )
        for assignment in data.production_environment():
            guards.validate_airflow_environment(assignment)


if __name__ == "__main__":
    unittest.main()
