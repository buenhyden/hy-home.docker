"""Docker-free control-flow regressions; these are not native acceptance."""

from __future__ import annotations

import base64
import copy
import hashlib
import importlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qsl

from tests.lib.ops import test_opsflow_manifest as manifest_tests
from tests.validation import _opsflow_airflow_native_data as data
from tests.validation import _opsflow_airflow_native_scenario as scenario

adapters = importlib.import_module("workflow_lib.adapters")


class ObjectError(Exception):
    def __init__(self, code, status):
        self.response = {
            "Error": {"Code": code},
            "ResponseMetadata": {"HTTPStatusCode": status},
        }


class MemoryS3:
    """Stateful transport double, not an emulation proof of SeaweedFS IAM."""

    def __init__(self, buckets, policies, worker=False):
        self.buckets, self.policies, self.worker = buckets, policies, worker

    def _authorize(self, operation, bucket, key=""):
        if not self.worker:
            return
        allowed = bucket == data.BUCKET
        if operation == "read":
            allowed &= key.startswith(
                ("manifest-input/", "manifest-validated/", "manifest-quarantine/")
            )
        elif operation == "write":
            allowed &= key.startswith(("manifest-validated/", "manifest-quarantine/"))
        elif operation == "delete":
            principal = (
                self.policies.get(bucket, {})
                .get("Statement", [{}])[0]
                .get("Principal", {})
            )
            allowed &= principal.get("AWS") != data.WORKER_PRINCIPAL
        else:
            allowed = False
        if not allowed:
            raise ObjectError("AccessDenied", 403)

    def create_bucket(self, *, Bucket):
        self.buckets.setdefault(Bucket, {})

    def put_bucket_policy(self, *, Bucket, Policy):
        self.policies[Bucket] = json.loads(Policy)

    def list_buckets(self):
        return {"Buckets": [{"Name": name} for name in self.buckets]}

    def list_objects_v2(self, *, Bucket, **_):
        self._authorize("list", Bucket)
        return {
            "Contents": [{"Key": key} for key in sorted(self.buckets[Bucket])],
            "IsTruncated": False,
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

    def put_object(self, *, Bucket, Key, Body, **options):
        self._authorize("write", Bucket, Key)
        objects = self.buckets[Bucket]
        if options.get("IfNoneMatch") == "*" and Key in objects:
            raise ObjectError("PreconditionFailed", 412)
        objects[Key] = {
            "Body": Body,
            "ContentType": options.get("ContentType", "application/octet-stream"),
            "Metadata": dict(options.get("Metadata", {})),
            "Tags": [
                {"Key": key, "Value": value}
                for key, value in parse_qsl(options.get("Tagging", ""))
            ],
        }
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def head_object(self, *, Bucket, Key):
        self._authorize("read", Bucket, Key)
        try:
            row = self.buckets[Bucket][Key]
        except KeyError:
            raise ObjectError("NoSuchKey", 404) from None
        return {
            "ContentLength": len(row["Body"]),
            "ContentType": row["ContentType"],
            "Metadata": dict(row["Metadata"]),
            "ETag": '"' + hashlib.sha256(row["Body"]).hexdigest() + '"',
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }

    def get_object(self, *, Bucket, Key, **_):
        return {
            **self.head_object(Bucket=Bucket, Key=Key),
            "Body": io.BytesIO(self.buckets[Bucket][Key]["Body"]),
        }

    def get_object_tagging(self, *, Bucket, Key):
        return {"TagSet": copy.deepcopy(self.buckets[Bucket][Key]["Tags"])}

    def delete_object(self, *, Bucket, Key):
        self._authorize("delete", Bucket, Key)
        self.buckets[Bucket].pop(Key, None)
        return {"ResponseMetadata": {"HTTPStatusCode": 204}}

    def close(self):
        pass


class MemoryFixture:
    """Run scenario control flow with in-memory queues/DB and owned local files.

    Generated Python storage programs execute against MemoryS3 and the real
    bounded snapshot helpers. SQL/queue effects are explicitly doubles, so no
    native Worker, PostgreSQL, IAM or restore acceptance is inferred.
    """

    def __init__(self, directory):
        self.directory = directory
        self.uid, self.gid = os.geteuid(), os.getegid()
        self.receipt, self.containers, self.files, self.installed = {}, {}, {}, {}
        self.events, self.commands, self.migrations = [], [], []
        self.generation, self.schema_version = 1, 0
        self.buckets, self.policies, self.runs, self.ledger = {}, {}, {}, {}
        self.allowed, self.pending, self.not_idle = True, False, False
        self.executor_identity, self.extension = "executor-id", "plpgsql:1.0\n"
        self.retry_number = 2
        self.fail_remove = None
        self.metadata_present = False

    def private(self, name, body):
        path = self.directory / name
        path.write_text(body)
        path.chmod(0o600)
        self.files[path] = scenario.fixture.private_identity(path)
        return path

    def create_networks(self):
        self.events.append(("networks", self.generation))

    def create(self, role, image, user, networks, command, **options):
        if role in self.containers:
            raise AssertionError("duplicate owned role")
        self.containers[role] = SimpleNamespace(name=f"unit-{role}-{self.generation}")
        self.events.append(("create", role, self.generation))
        self.commands.append((role, command, options))

    def start(self, role):
        self.events.append(("start", role))

    def put(self, role, files):
        self.installed.setdefault(role, {}).update(files)
        self.events.append(("put", role))

    def stop(self, role):
        self.events.append(("stop", role))

    def remove(self, role):
        if role == self.fail_remove:
            raise scenario.fixture.RehearsalFailure("owned cleanup failed")
        self.events.append(("remove", role))
        self.containers.pop(role)
        self.installed.pop(role, None)
        if role == "s3":
            self.buckets.clear()
            self.policies.clear()
        elif role == "dev-pg":
            self.ledger.clear()
            self.schema_version = 0
        elif role == "metadata-pg":
            self.runs.clear()
            self.metadata_present = False

    def wait(self, operation, message, **_):
        if not operation():
            raise scenario.fixture.RehearsalFailure(message)

    def configure_s3(self):
        self.events.append(("configure-s3", self.generation))

    def _store(self):
        store = adapters.S3Store.__new__(adapters.S3Store)
        store.client = MemoryS3(self.buckets, self.policies, worker=True)
        store.bucket, store._ca, store._closed = data.BUCKET, None, False
        return store

    def publish(self, manifest, identifier, digest, artifact):
        if not self.allowed:
            raise PermissionError("synthetic denied publication")
        replay = identifier in self.ledger
        self.ledger.setdefault(identifier, digest)
        return "replayed" if replay else "published"

    def _attempt(self, run):
        with self._store() as store:
            try:
                manifest_tests.ingest(store, self, "hy-home.docker", "2026-10-10")
            except manifest_tests.ContractError:
                self.runs[run] = "up_for_retry"
            else:
                self.runs[run] = "success"

    def psql(self, role, sql, *args, **options):
        self.events.append(("sql", role))
        output, code = "", 0
        if sql.startswith("REVOKE EXECUTE"):
            self.allowed = False
        elif role == "metadata-pg" and "CREATE DATABASE airflow" in sql:
            self.metadata_present = True
        elif sql.startswith("GRANT EXECUTE"):
            self.allowed = True
            for run, state in tuple(self.runs.items()):
                if state == "up_for_retry":
                    self._attempt(run)
        elif "INSERT INTO ops_flow.schema_version SELECT" in sql:
            version = re.findall(
                r"INSERT INTO ops_flow.schema_version SELECT ([0-9])", sql
            )
            self.schema_version = int(version[-1])
            self.migrations.append(self.schema_version)
        elif "SELECT data_version FROM ops_flow.published_documents" in sql:
            code = int(self.schema_version < 4)
        elif "SELECT DISTINCT data_version" in sql:
            output = "\n".join(set(self.ledger.values()))
        elif "SELECT (SELECT count(*) FROM ops_flow.runs)" in sql:
            output = ":".join([str(len(self.ledger))] * 3)
        elif "SELECT extname||" in sql:
            output = self.extension
        elif "count(*) FROM dag WHERE" in sql:
            output = "1"
        elif "count(*) FROM dag_run WHERE state" in sql:
            output = "1" if self.pending else "0"
        elif "SELECT try_number" in sql:
            output = str(self.retry_number)
        elif "hostname||" in sql:
            output = self.containers["worker"].name + ":" + self.executor_identity
        elif "SELECT state FROM" in sql:
            run = sql.rsplit("run_id='", 1)[1].split("'", 1)[0]
            output = self.runs.get(run, "missing")
        if options.get("check", True) and code:
            raise scenario.fixture.RehearsalFailure("synthetic SQL rejected")
        return SimpleNamespace(stdout=output, returncode=code)

    def execute(self, role, *command, input_=None, **options):
        self.commands.append((role, command, options))
        if command == ("airflow", "db", "check") and not self.metadata_present:
            raise scenario.fixture.RehearsalFailure("empty metadata target")
        if command[:3] == ("airflow", "dags", "trigger"):
            self._attempt(command[command.index("-r") + 1])
            return ""
        if command[:1] == ("airflow",) or command[:1] == ("sh",):
            return ""
        if command[:2] != ("python", "-c"):
            raise AssertionError("unexpected unit execution")
        code = command[2]
        if code.startswith(scenario.fixture.S3_CLIENT):
            code = code[len(scenario.fixture.S3_CLIENT) :]
        namespace = {
            "s": MemoryS3(self.buckets, self.policies, worker=role == "worker"),
            "b": data.BUCKET,
            "base64": base64,
            "hashlib": hashlib,
            "json": json,
            "sys": sys,
        }
        replacement = SimpleNamespace(
            S3Store=lambda _: self._store(),
            PgPublisher=lambda _: self,
            read_private_json=lambda _: {},
        )
        output = io.StringIO()
        with (
            patch.dict(
                sys.modules,
                {"p04_native_data": data, "workflow_lib.adapters": replacement},
            ),
            patch.object(sys, "path", list(sys.path)),
            patch.object(sys, "stdin", io.StringIO(input_ or "")),
            redirect_stdout(output),
        ):
            exec(compile(code, "<synthetic-storage-transport>", "exec"), namespace)
        return output.getvalue()

    def exec_result(self, role, *command):
        return SimpleNamespace(stdout=self.execute(role, *command), returncode=0)

    def dump(self, role, database):
        payload = self.ledger if role == "dev-pg" else self.runs
        return self.private(role + "-dump.json", json.dumps(payload))

    def dump_roles(self, role):
        return self.private(role + "-roles.json", json.dumps({"role": role}))

    def restore_roles(self, role, path):
        self.events.append(("restore-roles", role))
        if scenario.fixture.private_identity(path) != self.files[path]:
            raise AssertionError("unit role receipt changed")

    def restore(self, role, path):
        self.events.append(("restore-db", role))
        restored = json.loads(path.read_text())
        if role == "dev-pg":
            self.ledger, self.schema_version = restored, 4
        else:
            self.runs = restored
            self.metadata_present = True


class ScenarioControlFlowTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="p04-unit-scenario-")
        self.addCleanup(temporary.cleanup)
        self.owned = MemoryFixture(Path(temporary.name))
        self.publication = scenario.PublicationScenario(self.owned)

    def test_run_retries_replays_and_restores_same_version_with_real_snapshot_codec(
        self,
    ):
        with patch.object(scenario.evidence, "inspect_celery_idle"):
            self.publication.run()
        self.assertEqual(2, self.owned.generation)
        self.assertEqual(
            {self.publication.run_id: self.publication.digest}, self.owned.ledger
        )
        self.assertEqual("success", self.owned.runs["synthetic-restored-replay"])
        self.assertEqual([1, 2, 3, 4], self.owned.migrations)
        self.assertEqual(
            2, self.owned.receipt["publication"]["celery_retry_try_number"]
        )
        snapshot = json.loads((self.owned.directory / "s3-snapshot.json").read_text())
        restored = data.capture_objects(
            MemoryS3(self.owned.buckets, self.owned.policies), data.BUCKET
        )
        self.assertEqual(snapshot, restored)
        self.assertEqual(
            self.publication.raw,
            base64.b64decode(
                snapshot["manifest-input/hy-home.docker/2026-10-10.json"]["body"]
            ),
        )
        restore_calls = [
            command
            for role, command, _ in self.owned.commands
            if role == "storage-admin"
            and len(command) == 3
            and "restore_stdin" in command[-1]
        ]
        self.assertEqual(1, len(restore_calls))
        self.assertLess(len(restore_calls[0][-1].encode()), 4096)
        for operation in ("restore-db", "restore-roles"):
            self.assertEqual(
                {(operation, "metadata-pg"), (operation, "dev-pg")},
                {event for event in self.owned.events if event[0] == operation},
            )

    def test_omitting_either_database_restore_cannot_report_recovery_success(self):
        for omitted in ("metadata-pg", "dev-pg"):
            with self.subTest(omitted=omitted), tempfile.TemporaryDirectory() as raw:
                owned = MemoryFixture(Path(raw))
                publication = scenario.PublicationScenario(owned)
                restore = owned.restore

                def restore_other_database(
                    role, path, omitted=omitted, restore=restore
                ):
                    if role != omitted:
                        restore(role, path)

                with (
                    patch.object(owned, "restore", side_effect=restore_other_database),
                    patch.object(scenario.evidence, "inspect_celery_idle"),
                    self.assertRaises(scenario.fixture.RehearsalFailure),
                ):
                    publication.run()
                self.assertNotIn("recovery", owned.receipt)

    def test_worker_receives_only_worker_storage_identity_and_exact_frozen_sources(
        self,
    ):
        self.publication.airflow()
        worker = self.owned.installed["worker"]
        admin = self.owned.installed["storage-admin"]
        worker_config, admin_config = (
            json.loads(rows["/run/opsflow/s3.json"]) for rows in (worker, admin)
        )
        self.assertEqual(self.publication.s3_key, worker_config["access_key_id"])
        self.assertEqual(self.publication.s3_admin_key, admin_config["access_key_id"])
        self.assertNotIn(self.publication.s3_admin_secret, json.dumps(worker))
        for role in ("api", "scheduler", "processor"):
            self.assertFalse(
                any(
                    key.startswith("/run/opsflow/")
                    for key in self.owned.installed[role]
                )
            )
        helper = "infra/07-workflow/airflow/connection_uri.py"
        self.assertEqual(
            scenario.fixture.sha256(scenario.fixture.ROOT / helper),
            self.publication.source_hashes[helper],
        )
        for _, command, _ in self.owned.commands:
            self.assertNotIn(self.publication.meta_password, str(command))
            self.assertNotIn(self.publication.s3_admin_secret, str(command))

    def test_narrow_storage_permission_probe_changes_only_policy_and_preserves_each_observation(
        self,
    ):
        self.publication.storage_permission_rehearsal()
        before = self.owned.receipt["storage_permission_red"]["observations"]
        after = self.owned.receipt["storage_permissions"]["observations"]
        self.assertEqual(204, before["delete"]["observed_http"])
        self.assertEqual(403, after["delete"]["observed_http"])
        self.assertTrue(data.permissions_passed(after))
        self.assertNotIn("metadata-pg", self.owned.containers)
        self.assertNotIn("publication", self.owned.receipt)
        self.assertEqual(1, self.owned.generation)

    def test_incomplete_permission_receipt_never_becomes_pass(self):
        complete = data.permission_observations(self._ready_storage(), data.BUCKET)
        for observed in (
            {},
            {"delete": complete["delete"]},
            {key: row for key, row in complete.items() if key != "allowed_read"},
        ):
            with self.subTest(keys=sorted(observed)):
                with patch.object(
                    self.publication, "permission_observations", return_value=observed
                ):
                    with self.assertRaises(scenario.fixture.RehearsalFailure):
                        self.publication.assert_storage_permissions()
                self.assertEqual(
                    "FAIL", self.owned.receipt["storage_permissions"]["status"]
                )

    def _ready_storage(self):
        self.owned.buckets[data.BUCKET] = {}
        self.owned.policies[data.BUCKET] = data.worker_bucket_policy()
        self.publication.permission_canaries()
        return MemoryS3(self.owned.buckets, self.owned.policies, worker=True)

    def test_retry_must_be_observed_before_any_publication_receipt(self):
        self.owned.retry_number = 1
        with self.assertRaisesRegex(
            scenario.fixture.RehearsalFailure, "retry was not observed"
        ):
            self.publication.run()
        self.assertNotIn("publication", self.owned.receipt)
        self.assertEqual(1, self.owned.generation)

    def test_count_version_executor_and_object_mismatch_stop_without_success(self):
        self.publication.airflow()
        self._ready_storage()
        for expected in (1,):
            with self.assertRaises(scenario.fixture.RehearsalFailure):
                self.publication.assert_database(expected)
        self.owned.ledger["synthetic"] = "0" * 64
        with self.assertRaisesRegex(scenario.fixture.RehearsalFailure, "data_version"):
            self.publication.assert_database(1)
        self.owned.executor_identity = ""
        with self.assertRaises(scenario.fixture.RehearsalFailure):
            self.publication.assert_worker("synthetic")
        self.publication.quarantine = "manifest-quarantine/synthetic"
        self.publication.object_digest = self.publication.digest
        with self.assertRaises(AssertionError):
            self.publication.assert_s3()

    def test_pending_or_nonidle_workers_stop_recovery_without_teardown(self):
        self.publication.airflow()
        for pending in (True, False):
            self.owned.pending = pending
            with patch.object(
                scenario.evidence,
                "inspect_celery_idle",
                side_effect=scenario.fixture.RehearsalFailure("not idle"),
            ):
                with self.assertRaises(scenario.fixture.RehearsalFailure):
                    self.publication.recover()
            self.assertFalse(any(event[0] == "remove" for event in self.owned.events))
            self.assertEqual(1, self.owned.generation)

    def test_owned_cleanup_failure_does_not_start_replacement_generation(self):
        self.publication.airflow()
        self._ready_storage()
        self.owned.buckets[data.BUCKET].clear()
        self.owned.fail_remove = "storage-admin"
        with patch.object(scenario.evidence, "inspect_celery_idle"):
            with self.assertRaisesRegex(
                scenario.fixture.RehearsalFailure, "cleanup failed"
            ):
                self.publication.recover()
        self.assertEqual(1, self.owned.generation)
        self.assertNotIn("recovery", self.owned.receipt)


class RecoveryBoundaryTests(unittest.TestCase):
    def test_bad_integrity_shape_and_aggregate_budget_keep_old_worker_and_databases(
        self,
    ):
        raw = b"p04-synthetic-object"
        row = {
            "body": base64.b64encode(raw).decode(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size": len(raw),
            "content_type": "application/json",
            "metadata": {"source": "synthetic"},
            "tags": [{"Key": "scope", "Value": "p04"}],
        }
        large = b"x" * (data.MAX_OBJECT_BYTES // 2)
        large_row = {
            **row,
            "body": base64.b64encode(large).decode(),
            "sha256": hashlib.sha256(large).hexdigest(),
            "size": len(large),
        }
        snapshots = (
            [],
            {"manifest-input/test.json": {**row, "size": len(raw) + 1}},
            {"manifest-input/test.json": {**row, "sha256": "0" * 64}},
            {"manifest-input/test.json": {**row, "metadata": {"source": 7}}},
            {f"manifest-input/{number}.json": large_row for number in range(3)},
        )
        for snapshot in snapshots:
            with (
                self.subTest(kind=type(snapshot).__name__),
                tempfile.TemporaryDirectory() as temporary,
            ):
                owned = MemoryFixture(Path(temporary))
                publication = scenario.PublicationScenario(owned)
                publication.airflow()
                with (
                    patch.object(publication, "s3", return_value=json.dumps(snapshot)),
                    patch.object(scenario.evidence, "inspect_celery_idle"),
                    self.assertRaises(data.RehearsalFailure),
                ):
                    publication.recover()
                self.assertNotIn(("stop", "worker"), owned.events)
                self.assertFalse(any(event[0] == "remove" for event in owned.events))
                self.assertEqual(1, owned.generation)
                self.assertEqual([], list(owned.directory.glob("*-dump.json")))
                self.assertNotIn("recovery", owned.receipt)

    def test_invalid_snapshot_stops_before_generation_teardown(self):
        for snapshot in ({"foreign-prefix/rejected": {}}, {"manifest-input/x": {}}):
            with self.subTest(snapshot=snapshot), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                removed = []

                def private(name, body, directory=directory):
                    path = directory / name
                    path.write_text(body)
                    return path

                owned = SimpleNamespace(
                    uid=1000,
                    gid=1000,
                    receipt={},
                    containers={"worker": SimpleNamespace(name="synthetic-worker")},
                    generation=1,
                    private=private,
                    stop=lambda _: None,
                    psql=lambda *_, **__: SimpleNamespace(stdout="plpgsql:1.0\n"),
                    dump=lambda *args, directory=directory: (
                        directory / (args[0] + ".dump")
                    ),
                    dump_roles=lambda role, directory=directory: (
                        directory / (role + ".roles")
                    ),
                )

                def remove(role, removed=removed):
                    removed.append(role)
                    raise AssertionError("teardown reached before snapshot validation")

                owned.remove = remove
                publication = scenario.PublicationScenario(owned)
                with (
                    patch.object(publication, "metadata", return_value="0"),
                    patch.object(publication, "s3", return_value=json.dumps(snapshot)),
                    patch.object(scenario.evidence, "inspect_celery_idle"),
                    self.assertRaises(data.RehearsalFailure),
                ):
                    publication.recover()
                self.assertEqual([], removed)
                self.assertEqual(1, owned.generation)
                self.assertNotIn("recovery", owned.receipt)


if __name__ == "__main__":
    unittest.main()
