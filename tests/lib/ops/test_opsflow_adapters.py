"""Synthetic adapter contract tests; no real protected files or endpoints."""

from __future__ import annotations

import importlib
import io
import json
import os
import stat
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

WORKLOAD = (
    Path(__file__).resolve().parents[3]
    / "infra/07-workflow/airflow/workloads/manifest-pipeline"
)
sys.path.insert(0, str(WORKLOAD))
adapters = importlib.import_module("workflow_lib.adapters")
ContractError = adapters.ContractError
SYNTHETIC_CREDENTIAL = "synthetic-only"
SYNTHETIC_CHANGED_CREDENTIAL = "changed-only"
SYNTHETIC_REPR_CANARY = "private-repr-canary"


def pg_config():
    return dict(
        host="dev-pg",
        port=5432,
        dbname="opsflow_dev",
        user="opsflow_ingest",
        password=SYNTHETIC_CREDENTIAL,
        connect_timeout=5,
        statement_timeout_ms=30000,
        lock_timeout_ms=5000,
        sslmode="disable",
        sslrootcert=None,
    )


def s3_config():
    return dict(
        endpoint_url="http://seaweedfs-s3:8333",
        access_key_id=SYNTHETIC_CREDENTIAL,
        secret_access_key=SYNTHETIC_CREDENTIAL,
        bucket="opsflow-dev",
        region="us-east-1",
        addressing_style="path",
        ca_bundle=None,
        connect_timeout=5,
        read_timeout=20,
        endpoint_contract="seaweedfs-s3-internal-v1",
    )


class PrivateFiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.directory.chmod(0o700)
        self.file = self.directory / "pg.json"
        self.file.write_text(json.dumps(pg_config()))
        self.file.chmod(0o600)

    def read(self, **kwargs):
        return adapters.read_private_json(
            str(self.file),
            expected_directory=str(self.directory),
            schema="pg",
            **kwargs,
        )

    def test_exact_schema_and_no_input_mutation(self):
        self.assertEqual(self.read(), pg_config())
        for mode in (0o600, 0o640):
            with self.subTest(mode=mode):
                self.file.chmod(mode)
                self.assertEqual(self.read()["host"], "dev-pg")

    def test_schema_rejects_unknown_duplicate_empty_and_types(self):
        for payload in (
            '{"password":"secret-canary","password":"x"}',
            "[]",
            "{}",
            json.dumps(dict(pg_config(), unapproved="secret-canary")),
            json.dumps(dict(pg_config(), password="")),
            json.dumps(dict(pg_config(), port=True)),
        ):
            with self.subTest(payload_kind=payload[:1]):
                self.file.write_text(payload)
                with self.assertRaises(ContractError) as caught:
                    self.read()
                self.assertNotIn("secret-canary", str(caught.exception))
                self.assertIsNone(caught.exception.__cause__)
                self.assertIsNone(caught.exception.__context__)

    def test_modes_links_escape_and_parent(self):
        for mode in (0o644, 0o660, 0o400, 0o700):
            with self.subTest(mode=mode):
                self.file.chmod(mode)
                with self.assertRaises(ContractError):
                    self.read()
        self.file.chmod(0o600)
        link = self.directory / "linked.json"
        os.link(self.file, link)
        with self.assertRaises(ContractError):
            self.read()
        link.unlink()
        self.file.rename(self.directory / "original")
        self.file.symlink_to(self.directory / "original")
        with self.assertRaises(ContractError):
            self.read()
        self.file.unlink()
        (self.directory / "original").rename(self.file)
        self.directory.chmod(0o770)
        with self.assertRaises(ContractError):
            self.read()
        self.directory.chmod(0o700)
        with self.assertRaises(ContractError):
            adapters.read_private_json(
                str(self.file), expected_directory="/run/opsflow", schema="pg"
            )

    def test_parent_symlink_and_special_files(self):
        alias = self.directory / "alias"
        alias.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaises(ContractError):
            adapters.read_private_json(
                str(alias / "pg.json"), expected_directory=str(alias), schema="pg"
            )
        self.file.unlink()
        os.mkfifo(self.file, 0o600)
        with self.assertRaises(ContractError):
            self.read()

    def test_identity_missing_size_utf8_and_schema_errors_are_redacted(self):
        with self.assertRaises(ContractError):
            self.read(expected_uid=os.geteuid() + 100000)
        with self.assertRaises(ContractError):
            self.read(expected_gid=os.getegid() + 100000)
        for identity in (True, -1, 1.5):
            with self.assertRaises(ContractError):
                self.read(expected_uid=identity)
            with self.assertRaises(ContractError):
                self.read(expected_gid=identity)
        for payload in (b"x" * 16385, b"\xff", b"{"):
            self.file.write_bytes(payload)
            with self.assertRaises(ContractError):
                self.read()
        self.file.unlink()
        with self.assertRaises(ContractError) as caught:
            self.read()
        self.assertIsNone(caught.exception.__context__)
        with self.assertRaises(ContractError):
            adapters.read_private_json("/run/opsflow/no.json", schema="other")

    def test_verified_supplementary_worker_group_default(self):
        original_fstat = os.fstat
        original_stat = os.stat
        directory_inode = self.directory.stat().st_ino
        synthetic_gid = os.getegid() + 123456

        def protected_group(info):
            if info.st_ino == directory_inode or stat.S_ISREG(info.st_mode):
                values = {
                    key: getattr(info, key)
                    for key in (
                        "st_dev",
                        "st_ino",
                        "st_mode",
                        "st_uid",
                        "st_gid",
                        "st_nlink",
                        "st_size",
                        "st_mtime_ns",
                        "st_ctime_ns",
                    )
                }
                return types.SimpleNamespace(**dict(values, st_gid=synthetic_gid))
            return info

        def descriptor(fd):
            return protected_group(original_fstat(fd))

        def named(*args, **kwargs):
            return protected_group(original_stat(*args, **kwargs))

        with (
            patch.object(adapters.os, "fstat", side_effect=descriptor),
            patch.object(adapters.os, "stat", side_effect=named),
        ):
            with patch.object(adapters.os, "getgroups", return_value=[synthetic_gid]):
                self.assertEqual(self.read(), pg_config())
            with patch.object(adapters.os, "getgroups", return_value=[]):
                with self.assertRaises(ContractError):
                    self.read()

    def test_worker_parent_replacement_during_read_fails_closed(self):
        original = os.fstat
        moved = self.directory.with_name(self.directory.name + "-moved")
        changed = False

        def replace(fd):
            nonlocal changed
            info = original(fd)
            if stat.S_ISREG(info.st_mode) and not changed:
                self.directory.rename(moved)
                changed = True
            return info

        try:
            with patch.object(adapters.os, "fstat", side_effect=replace):
                with self.assertRaises(ContractError):
                    self.read()
        finally:
            if changed:
                moved.rename(self.directory)

    def test_import_has_no_optional_driver_or_protected_file_io(self):
        original = __import__

        def importing(name, *args, **kwargs):
            if name in ("boto3", "botocore.config", "psycopg2", "psycopg2.extras"):
                raise AssertionError("optional_driver_import")
            return original(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=importing),
            patch.object(adapters.os, "open", side_effect=AssertionError("file_io")),
        ):
            importlib.reload(adapters)
        global ContractError
        ContractError = adapters.ContractError

    def test_config_file_identity_and_concurrent_fd_change(self):
        self.file.write_text(json.dumps(s3_config()))
        with self.assertRaises(ContractError):
            adapters.read_private_json(
                str(self.file), expected_directory=str(self.directory), schema="s3"
            )
        self.file.write_text(json.dumps(pg_config()))
        original = os.fstat

        def change(fd):
            info = original(fd)
            if stat.S_ISREG(info.st_mode):
                self.file.write_text(
                    json.dumps(dict(pg_config(), password=SYNTHETIC_CHANGED_CREDENTIAL))
                )
            return info

        with patch.object(adapters.os, "fstat", side_effect=change):
            with self.assertRaises(ContractError):
                self.read()
        for path in (
            "relative.json",
            str(self.directory / "../pg.json"),
            str(self.directory / "pg.json") + "\x00",
        ):
            with self.assertRaises(ContractError):
                adapters.read_private_json(
                    path, expected_directory=str(self.directory), schema="pg"
                )


class S3Error(Exception):
    def __init__(self, code):
        self.response = {"Error": {"Code": code}}
        super().__init__("sensitive-driver-canary")


class Body(io.BytesIO):
    pass


class S3Double:
    def __init__(self):
        self.objects = {}
        self.requests = []
        self.bodies = []
        self.failure = None
        self.corrupt = False
        self.race = False

    def head_object(self, **kwargs):
        self.requests.append(("head", kwargs))
        if self.failure:
            raise S3Error(self.failure)
        if kwargs["Key"] not in self.objects:
            raise S3Error("NoSuchKey")
        return {"ContentLength": len(self.objects[kwargs["Key"]]), "ETag": '"fixed"'}

    def get_object(self, **kwargs):
        self.requests.append(("get", kwargs))
        if self.failure:
            raise S3Error(self.failure)
        if kwargs["Key"] not in self.objects:
            raise S3Error("NoSuchKey")
        body = Body(b"corrupted" if self.corrupt else self.objects[kwargs["Key"]])
        self.bodies.append(body)
        return {"Body": body, "ETag": '"fixed"'}

    def put_object(self, **kwargs):
        self.requests.append(("put", kwargs))
        if self.race:
            self.objects[kwargs["Key"]] = kwargs["Body"]
            raise S3Error("PreconditionFailed")
        self.objects[kwargs["Key"]] = kwargs["Body"]
        return {"ETag": '"fixed"'}


class ObjectAdapter(unittest.TestCase):
    def setUp(self):
        self.client = S3Double()
        self.factory = unittest.mock.Mock(return_value=self.client)
        self.config_factory = unittest.mock.Mock(side_effect=lambda **kwargs: kwargs)
        self.modules = patch.dict(
            sys.modules,
            {
                "boto3": types.SimpleNamespace(client=self.factory),
                "botocore.config": types.SimpleNamespace(Config=self.config_factory),
            },
        )
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.store = adapters.S3Store(s3_config())

    def test_tls_delivery_is_blocked_before_s3_driver_use(self):
        self.factory.reset_mock()
        config = dict(
            s3_config(),
            endpoint_url="https://objects.internal:443",
            endpoint_contract="https:objects.internal:443",
            ca_bundle="/run/opsflow/ca.pem",
        )
        with self.assertRaises(ContractError) as caught:
            adapters.S3Store(config)
        self.assertEqual(str(caught.exception), "tls_delivery_not_ready")
        self.factory.assert_not_called()

    def test_explicit_credentials_path_style_timeouts_and_input_etag(self):
        kwargs = self.factory.call_args.kwargs
        self.assertEqual(kwargs["aws_secret_access_key"], "synthetic-only")
        self.assertTrue(kwargs["verify"])
        self.assertEqual(kwargs["config"]["s3"]["addressing_style"], "path")
        self.client.objects["manifest-input/day.json"] = b"{}"
        self.assertEqual(self.store.read_input("manifest-input/day.json"), b"{}")
        self.assertEqual(self.client.requests[-1][1]["IfMatch"], '"fixed"')
        self.assertTrue(self.client.bodies[-1].closed)

    def test_closed_config_endpoint_types_and_timeouts(self):
        for delta in (
            {"bucket": "foreign"},
            {"addressing_style": "virtual"},
            {"extra": "canary"},
            {"region": ""},
            {"connect_timeout": True},
            {"read_timeout": -1},
            {"endpoint_url": "http://external:8333"},
            {"endpoint_url": "http://seaweedfs-s3:8333/?x=1"},
            {"endpoint_url": "http://user:canary@seaweedfs-s3:8333"},
            {"endpoint_url": "http://seaweedfs-s3:wrong"},
            {"endpoint_contract": "unapproved"},
            {"endpoint_url": "https://seaweedfs-s3", "ca_bundle": None},
        ):
            with self.subTest(delta_keys=tuple(delta)):
                with self.assertRaises(ContractError):
                    adapters.S3Store(dict(s3_config(), **delta))
        config = dict(
            s3_config(),
            endpoint_url="https://objects.internal:443",
            endpoint_contract="https:objects.internal:443",
            ca_bundle="/run/opsflow/ca.pem",
        )
        with self.assertRaises(ContractError):
            adapters.S3Store(config)

    def test_key_restrictions_and_size_guards(self):
        for key in (
            "other/a",
            "manifest-input/../x",
            "manifest-input//x",
            "manifest-input/.env",
            "manifest-input/SECRET/a",
            "manifest-input/x\n",
            "/manifest-input/a",
        ):
            with self.subTest(key=key):
                with self.assertRaises(ContractError):
                    self.store.read_input(key)
        with self.assertRaises(ContractError):
            self.store.put_verified("manifest-input/x.json", b"{}")
        with self.assertRaises(ContractError):
            self.store.put_verified("manifest-validated/x.json", b"x" * 1048577)
        self.client.objects["manifest-input/large.json"] = b"x" * 1048577
        with self.assertRaises(ContractError):
            self.store.read_input("manifest-input/large.json")

    def test_verified_create_replay_conflict_and_race(self):
        key = "manifest-validated/a.json"
        self.store.put_verified(key, b"{}")
        puts = [kwargs for kind, kwargs in self.client.requests if kind == "put"]
        self.assertEqual(puts[0]["IfNoneMatch"], "*")
        self.store.put_verified(key, b"{}")
        self.assertEqual(len([r for r in self.client.requests if r[0] == "put"]), 1)
        with self.assertRaises(adapters.DependencyError):
            self.store.put_verified(key, b"conflict")
        self.assertEqual(self.client.objects[key], b"{}")
        self.client.race = True
        self.store.put_verified("manifest-validated/race.json", b"{}")

    def test_corruption_and_driver_errors_have_no_sensitive_chain(self):
        self.client.objects["manifest-validated/x.json"] = b"{}"
        self.client.corrupt = True
        with self.assertRaises(adapters.DependencyError):
            self.store.put_verified("manifest-validated/x.json", b"{}")
        self.assertTrue(self.client.bodies[-1].closed)
        for code in ("AccessDenied", "RequestTimeout"):
            self.client.failure = code
            with self.assertRaises(adapters.DependencyError) as caught:
                self.store.read_input("manifest-input/x.json")
            self.assertNotIn("sensitive-driver-canary", str(caught.exception))
            self.assertIsNone(caught.exception.__context__)

    def test_metadata_stream_and_missing_failures(self):
        with self.assertRaises(adapters.DependencyError):
            self.store.read_input("manifest-input/missing.json")
        key = "manifest-input/x.json"
        self.client.objects[key] = b"{}"
        for head in (
            {"ContentLength": True, "ETag": "x"},
            {"ContentLength": 2},
            {"ContentLength": -1, "ETag": "x"},
            {"ContentLength": 1, "ETag": '"fixed"'},
        ):
            with patch.object(self.client, "head_object", return_value=head):
                with self.assertRaises((adapters.DependencyError, ContractError)):
                    self.store.read_input(key)
        body = Body(b"x" * 1048577)
        with patch.object(
            self.client, "get_object", return_value={"Body": body, "ETag": '"fixed"'}
        ):
            with self.assertRaises(ContractError):
                self.store.read_input(key)
        self.assertTrue(body.closed)
        body = Body(b"{}")
        with patch.object(
            self.client, "get_object", return_value={"Body": body, "ETag": "changed"}
        ):
            with self.assertRaises(adapters.DependencyError):
                self.store.read_input(key)
        for method in ("head_object", "put_object"):
            self.client.objects.clear()
            with patch.object(self.client, method, side_effect=S3Error("AccessDenied")):
                with self.assertRaises(adapters.DependencyError) as caught:
                    self.store.put_verified("manifest-validated/new.json", b"{}")
                self.assertIsNone(caught.exception.__context__)
        with patch.object(
            self.client, "put_object", side_effect=S3Error("PreconditionFailed")
        ):
            with self.assertRaises(adapters.DependencyError):
                self.store.put_verified("manifest-validated/missing.json", b"{}")
        with patch.dict(sys.modules, {"boto3": None}):
            with self.assertRaises(adapters.DependencyError) as caught:
                adapters.S3Store(s3_config())
            self.assertIsNone(caught.exception.__context__)


class CursorDouble:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, query, params):
        self.connection.query = query
        self.connection.params = params
        if self.connection.fail:
            raise RuntimeError("sensitive-driver-canary")

    def fetchone(self):
        return (self.connection.status,)


class ConnectionDouble:
    def __init__(self):
        self.closed = False
        self.committed = False
        self.rolled_back = False
        self.fail = False
        self.status = "published"

    def __enter__(self):
        return self

    def __exit__(self, kind, *args):
        self.rolled_back = kind is not None
        self.committed = kind is None
        return False

    def cursor(self):
        return CursorDouble(self)

    def close(self):
        self.closed = True


class PostgresAdapter(unittest.TestCase):
    def setUp(self):
        self.connection = ConnectionDouble()
        self.connect = unittest.mock.Mock(return_value=self.connection)
        self.modules = patch.dict(
            sys.modules,
            {
                "psycopg2": types.SimpleNamespace(connect=self.connect),
                "psycopg2.extras": types.SimpleNamespace(Json=lambda value: value),
            },
        )
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.manifest = types.SimpleNamespace(
            source="hy-home", captured_at="2026-10-11", records=({"path": "x"},)
        )

    def test_publisher_config_repr_is_redacted(self):
        config = dict(pg_config(), password=SYNTHETIC_REPR_CANARY)
        publisher = adapters.PgPublisher(config)
        self.assertNotIn(SYNTHETIC_REPR_CANARY, repr(publisher))
        self.assertNotIn(SYNTHETIC_REPR_CANARY, repr(publisher.config))
        self.assertNotIn(SYNTHETIC_REPR_CANARY, str(publisher.config))

    def test_tls_delivery_is_blocked_before_pg_driver_use(self):
        with self.assertRaises(ContractError) as caught:
            adapters.PgPublisher(
                dict(
                    pg_config(),
                    sslmode="verify-full",
                    sslrootcert="/run/opsflow/ca.pem",
                )
            )
        self.assertEqual(str(caught.exception), "tls_delivery_not_ready")
        self.connect.assert_not_called()

    def test_exact_target_closed_schema_and_no_constructor_connect(self):
        config = pg_config()
        publisher = adapters.PgPublisher(config)
        config["host"] = "elsewhere"
        self.connect.assert_not_called()
        for delta in (
            {"host": "mng-pg"},
            {"port": True},
            {"port": 5433},
            {"user": "admin"},
            {"dbname": "postgres"},
            {"password": ""},
            {"connect_timeout": 0},
            {"sslmode": "allow"},
            {"extra": "canary"},
            {"statement_timeout_ms": False},
        ):
            with self.subTest(keys=tuple(delta)):
                with self.assertRaises(ContractError):
                    adapters.PgPublisher(dict(pg_config(), **delta))
        self.assertEqual(
            publisher.publish(
                self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
            ),
            "published",
        )
        self.assertEqual(self.connect.call_args.kwargs["host"], "dev-pg")

    def test_parameterized_transaction_and_immutable_records_to_json(self):
        publisher = adapters.PgPublisher(pg_config())
        self.assertEqual(
            publisher.publish(
                self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
            ),
            "published",
        )
        self.assertIn("%s", self.connection.query)
        self.assertNotIn("synthetic-only", self.connection.query)
        self.assertEqual(self.connection.params[4], [{"path": "x"}])
        self.assertTrue(self.connection.closed and self.connection.committed)
        self.assertIn(
            "statement_timeout=30000", self.connect.call_args.kwargs["options"]
        )

    def test_failure_rolls_back_closes_and_redacts(self):
        self.connection.fail = True
        with self.assertRaises(adapters.DependencyError) as caught:
            adapters.PgPublisher(pg_config()).publish(
                self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
            )
        self.assertTrue(self.connection.closed and self.connection.rolled_back)
        self.assertNotIn("sensitive-driver-canary", str(caught.exception))
        self.assertIsNone(caught.exception.__context__)

    def test_invalid_status_and_publish_inputs_fail_closed(self):
        self.connection.status = "unexpected-canary"
        with self.assertRaises(adapters.DependencyError):
            adapters.PgPublisher(pg_config()).publish(
                self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
            )
        self.assertTrue(self.connection.rolled_back)
        for identifier, digest, artifact in (
            ("short", "b" * 64, "manifest-validated/a.json"),
            ("a" * 64, "UPPER", "manifest-validated/a.json"),
            ("a" * 64, "b" * 64, "other/a"),
        ):
            with self.assertRaises(ContractError):
                adapters.PgPublisher(pg_config()).publish(
                    self.manifest, identifier, digest, artifact
                )

    def test_status_and_connection_failure(self):
        publisher = adapters.PgPublisher(pg_config())
        for status in ("historical", "replayed"):
            self.connection.status = status
            self.assertEqual(
                publisher.publish(
                    self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
                ),
                status,
            )
        with self.assertRaises(TypeError):
            publisher.config["password"] = "different-only"
        for config in (
            dict(pg_config(), sslmode="verify-full"),
            dict(pg_config(), sslrootcert="/tmp/ca.pem"),
            [],
            dict(pg_config(), lock_timeout_ms=-1),
        ):
            with self.assertRaises(ContractError):
                adapters.PgPublisher(config)
        self.connect.side_effect = RuntimeError("sensitive-driver-canary")
        with self.assertRaises(adapters.DependencyError) as caught:
            publisher.publish(
                self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
            )
        self.assertIsNone(caught.exception.__context__)
        with patch.dict(sys.modules, {"psycopg2": None}):
            with self.assertRaises(adapters.DependencyError):
                publisher.publish(
                    self.manifest, "a" * 64, "b" * 64, "manifest-validated/a.json"
                )


if __name__ == "__main__":
    unittest.main()
