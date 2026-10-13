"""Synthetic adapter contract tests; no real protected files or endpoints."""

from __future__ import annotations

import importlib
import io
import json
import os
import ssl
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
MAX_CA_BYTES = 1024 * 1024


def test_ca_bytes():
    """Return one public system trust anchor as a certificate-only PEM bundle."""
    certificates = ssl.create_default_context().get_ca_certs(binary_form=True)
    if not certificates:
        raise RuntimeError("test_ca_unavailable")
    return ssl.DER_cert_to_PEM_cert(certificates[0]).encode("ascii")


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


def secure_s3_config(directory):
    return dict(
        s3_config(),
        endpoint_url="https://seaweedfs-s3:443",
        endpoint_contract="https:seaweedfs-s3:443",
        ca_bundle=str(directory / "ca.pem"),
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


class EventsDouble:
    def __init__(self):
        self.handlers = {}

    def register_first(self, name, handler, **kwargs):
        self.handlers[name] = handler


class S3Double:
    def __init__(self):
        self.objects = {}
        self.requests = []
        self.bodies = []
        self.failure = None
        self.corrupt = False
        self.race = False
        self.closed = False
        self.meta = types.SimpleNamespace(events=EventsDouble())

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

    def close(self):
        self.closed = True


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
        self.addCleanup(self.store.close)

    def test_https_uses_sealed_ca_disables_proxy_and_closes_deterministically(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            ca = directory / "ca.pem"
            original = test_ca_bytes()
            ca.write_bytes(original)
            ca.chmod(0o600)
            with (
                patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)),
                patch.dict(os.environ, {"HTTPS_PROXY": "http://proxy.invalid:8080"}),
            ):
                store = adapters.S3Store(secure_s3_config(directory))
            verify_path = self.factory.call_args.kwargs["verify"]
            self.assertRegex(verify_path, r"^/proc/self/fd/[0-9]+$")
            ca.write_bytes(b"changed-after-client")
            self.assertEqual(Path(verify_path).read_bytes(), original)
            self.assertEqual(self.config_factory.call_args.kwargs["proxies"], {})
            self.assertIn("before-send.s3", self.client.meta.events.handlers)
            self.assertIn("needs-retry.s3", self.client.meta.events.handlers)
            store.close()
            store.close()
            self.assertTrue(self.client.closed)
            with self.assertRaises(FileNotFoundError):
                Path(verify_path).read_bytes()

    def test_https_endpoint_and_redirects_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            ca = directory / "ca.pem"
            ca.write_bytes(test_ca_bytes())
            ca.chmod(0o600)
            with patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)):
                for endpoint in (
                    "https://evil.example:443",
                    "https://seaweedfs-s3",
                    "https://seaweedfs-s3.:443",
                    "https://127.0.0.1:443",
                    "https://seaweedfs-s3:443/path",
                    "https://user@seaweedfs-s3:443",
                ):
                    with self.subTest(endpoint=endpoint):
                        with self.assertRaises(ContractError):
                            adapters.S3Store(
                                dict(secure_s3_config(directory), endpoint_url=endpoint)
                            )
                store = adapters.S3Store(secure_s3_config(directory))
            before_send = self.client.meta.events.handlers["before-send.s3"]
            needs_retry = self.client.meta.events.handlers["needs-retry.s3"]
            before_send(
                request=types.SimpleNamespace(
                    url="https://seaweedfs-s3:443/opsflow-dev/key"
                )
            )
            for url in (
                "https://evil.example:443/opsflow-dev/key",
                "http://seaweedfs-s3:443/opsflow-dev/key",
                "https://seaweedfs-s3:444/opsflow-dev/key",
            ):
                with self.subTest(url=url):
                    with self.assertRaises(adapters.DependencyError):
                        before_send(request=types.SimpleNamespace(url=url))
            for status, headers in ((301, {}), (200, {"Location": "/other"})):
                response = (
                    types.SimpleNamespace(status_code=status, headers=headers),
                    {},
                )
                with self.assertRaises(adapters.DependencyError):
                    needs_retry(response=response)
            store.close()

    def test_https_creation_and_close_failures_still_close_ca(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            ca = directory / "ca.pem"
            ca.write_bytes(test_ca_bytes())
            ca.chmod(0o600)
            observed = {}

            def fail_create(*args, **kwargs):
                observed["path"] = kwargs["verify"]
                raise RuntimeError("synthetic-client-failure")

            self.factory.side_effect = fail_create
            with patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)):
                with self.assertRaises(adapters.DependencyError):
                    adapters.S3Store(secure_s3_config(directory))
            with self.assertRaises(FileNotFoundError):
                Path(observed["path"]).read_bytes()

            self.factory.side_effect = None
            self.factory.return_value = self.client
            with patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)):
                store = adapters.S3Store(secure_s3_config(directory))
            verify_path = self.factory.call_args.kwargs["verify"]
            with patch.object(self.client, "close", side_effect=RuntimeError("close")):
                with self.assertRaises(adapters.DependencyError):
                    store.close()
            with self.assertRaises(FileNotFoundError):
                Path(verify_path).read_bytes()

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
            {
                "endpoint_url": "https://evil.example:443",
                "endpoint_contract": "https:evil.example:443",
                "ca_bundle": "/run/opsflow/ca.pem",
            },
        ):
            with self.subTest(delta_keys=tuple(delta)):
                with self.assertRaises(ContractError):
                    adapters.S3Store(dict(s3_config(), **delta))
        config = dict(
            s3_config(),
            endpoint_url="https://seaweedfs-s3:443",
            endpoint_contract="https:seaweedfs-s3:443",
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
    """Shared offline fixture imported by the registered P04/P05 seam tests."""

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


if __name__ == "__main__":
    unittest.main()
