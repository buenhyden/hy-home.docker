"""Synthetic registration and overlay contracts; native acceptance is separate."""

import builtins
import importlib
import io
import os
import socket
import ssl
import sys
import tempfile
import types
import unittest
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

import yaml

WORKLOAD = (
    Path(__file__).resolve().parents[2]
    / "infra/07-workflow/airflow/workloads/manifest-pipeline"
)
sys.path.insert(0, str(WORKLOAD))
adapters = importlib.import_module("workflow_lib.adapters")
tls = importlib.import_module("workflow_lib.tls")
ContractError = adapters.ContractError
SYNTHETIC_CREDENTIAL = "synthetic-only"
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


class OverlayLoader(yaml.SafeLoader):
    pass


OverlayLoader.add_constructor("!reset", lambda loader, node: None)


class PinnedCAFiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.directory.chmod(0o700)
        self.file = self.directory / "ca.pem"
        self.original = test_ca_bytes()
        self.file.write_bytes(self.original)
        self.file.chmod(0o600)

    def pin(self):
        with patch.object(adapters, "PRIVATE_DIRECTORY", str(self.directory)):
            return adapters._pin_ca(str(self.file))

    def reset_file(self, body=None):
        if self.file.exists() or self.file.is_symlink():
            self.file.unlink()
        self.file.write_bytes(self.original if body is None else body)
        self.file.chmod(0o600)

    def test_snapshot_is_sealed_immutable_and_explicitly_closed(self):
        pinned = self.pin()
        descriptor = int(pinned.path.rsplit("/", 1)[1])
        self.file.write_bytes(b"changed-after-validation")
        self.assertEqual(Path(pinned.path).read_bytes(), self.original)
        with self.assertRaises(OSError):
            os.write(descriptor, b"x")
        with self.assertRaises(OSError):
            os.ftruncate(descriptor, len(self.original) + 1)
        pinned.close()
        pinned.close()
        with self.assertRaises(FileNotFoundError):
            Path(pinned.path).read_bytes()

    def test_rejects_missing_modes_links_special_files_and_size(self):
        self.file.unlink()
        with self.assertRaises(ContractError):
            self.pin()
        self.reset_file()
        for mode in (0o400, 0o644, 0o660, 0o700):
            with self.subTest(mode=mode):
                self.file.chmod(mode)
                with self.assertRaises(ContractError):
                    self.pin()
        self.reset_file()
        linked = self.directory / "linked.pem"
        os.link(self.file, linked)
        with self.assertRaises(ContractError):
            self.pin()
        linked.unlink()
        original = self.directory / "original.pem"
        self.file.rename(original)
        self.file.symlink_to(original)
        with self.assertRaises(ContractError):
            self.pin()
        self.file.unlink()
        original.unlink()
        os.mkfifo(self.file, 0o600)
        with self.assertRaises(ContractError):
            self.pin()
        self.file.unlink()
        self.reset_file(b"x" * (MAX_CA_BYTES + 1))
        with self.assertRaises(ContractError):
            self.pin()

    def test_rejects_owner_group_change_and_concurrent_write(self):
        original_fstat = adapters.os.fstat
        source_inode = self.file.stat().st_ino

        def changed_identity(field):
            def change(fd):
                info = original_fstat(fd)
                if info.st_ino != source_inode:
                    return info
                fields = {
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
                fields[field] += 100000
                return types.SimpleNamespace(**fields)

            return change

        for field in ("st_uid", "st_gid"):
            with self.subTest(field=field):
                with patch.object(
                    adapters.os, "fstat", side_effect=changed_identity(field)
                ):
                    with self.assertRaises(ContractError):
                        self.pin()

        changed = False

        def overwrite_during_read(fd):
            nonlocal changed
            info = original_fstat(fd)
            if info.st_ino == source_inode and not changed:
                changed = True
                self.file.write_bytes(self.original + b"\n")
            return info

        with patch.object(adapters.os, "fstat", side_effect=overwrite_during_read):
            with self.assertRaises(ContractError):
                self.pin()

    def test_rejects_non_certificate_pem_junk_and_unavailable_memfd(self):
        for body in (
            b"-----BEGIN PRIVATE KEY-----\nY2FuYXJ5\n-----END PRIVATE KEY-----\n",
            self.original + b"not-a-certificate",
            b"-----BEGIN CERTIFICATE-----\ninvalid\n-----END CERTIFICATE-----\n",
        ):
            with self.subTest(body=body[:30]):
                self.file.write_bytes(body)
                with self.assertRaises(ContractError):
                    self.pin()
        self.reset_file()
        with patch.object(adapters.os, "memfd_create", side_effect=OSError("blocked")):
            with self.assertRaises(ContractError):
                self.pin()

    def test_rejects_unavailable_procfd_readback(self):
        original_open = adapters.os.open

        def open_file(path, *args, **kwargs):
            if isinstance(path, str) and path.startswith("/proc/self/fd/"):
                raise OSError("procfd unavailable")
            return original_open(path, *args, **kwargs)

        with patch.object(adapters.os, "open", side_effect=open_file):
            with self.assertRaises(ContractError):
                self.pin()

    def test_tls_helper_import_has_no_driver_or_protected_file_io(self):
        original = __import__

        def importing(name, *args, **kwargs):
            if name in ("boto3", "botocore.config", "psycopg2", "psycopg2.extras"):
                raise AssertionError("optional_driver_import")
            return original(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=importing),
            patch.object(tls.os, "open", side_effect=AssertionError("file_io")),
        ):
            importlib.reload(tls)


class AirflowContractTests(unittest.TestCase):
    def register(self):
        source = (WORKLOAD / "dags/source_manifest_ingest.py").read_text()
        declarations = {"tasks": []}
        sdk = types.ModuleType("airflow.sdk")
        sdk.Param = lambda default, **rules: {"default": default, **rules}
        sdk.get_current_context = lambda: (_ for _ in ()).throw(
            AssertionError("parse_context_io")
        )

        def dag(**settings):
            declarations["dag"] = settings
            return lambda function: function

        def task(**settings):
            def decorate(function):
                declarations["tasks"].append((settings, function))
                return lambda: None

            return decorate

        sdk.dag, sdk.task = dag, task
        airflow = types.ModuleType("airflow")
        airflow.sdk = sdk
        # Preserve the source filename for coverage while the SDK remains a double.
        code = compile(source, str(WORKLOAD / "dags/source_manifest_ingest.py"), "exec")
        with patch.dict(sys.modules, {"airflow": airflow, "airflow.sdk": sdk}):
            with (
                patch.object(
                    builtins, "open", side_effect=AssertionError("parse_file_io")
                ),
                patch.object(io, "open", side_effect=AssertionError("parse_file_io")),
            ):
                with patch("os.open", side_effect=AssertionError("parse_file_io")):
                    with patch.object(
                        socket,
                        "create_connection",
                        side_effect=AssertionError("parse_network_io"),
                    ):
                        exec(code, {})
        return source, declarations

    def test_registration_is_io_free_manual_paused_and_bounded(self):
        _, value = self.register()
        settings = value["dag"]
        self.assertEqual(settings["dag_id"], "source_manifest_ingest")
        self.assertIsNone(settings["schedule"])
        self.assertTrue(settings["is_paused_upon_creation"])
        self.assertFalse(settings["catchup"])
        self.assertEqual(settings["max_active_runs"], 1)
        self.assertEqual(settings["max_active_tasks"], 1)
        self.assertEqual(len(value["tasks"]), 1)
        task_settings = value["tasks"][0][0]
        self.assertEqual(task_settings["pool"], "manifest_ingest")
        self.assertEqual(task_settings["pool_slots"], 1)
        self.assertEqual(task_settings["execution_timeout"], timedelta(minutes=3))
        self.assertFalse(task_settings["show_return_value_in_logs"])
        self.assertFalse(task_settings["multiple_outputs"])
        defaults = settings["default_args"]
        self.assertEqual(defaults["retries"], 2)
        self.assertTrue(defaults["retry_exponential_backoff"])
        self.assertLessEqual(defaults["max_retry_delay"], timedelta(minutes=5))

    def test_public_sdk_and_lazy_adapters(self):
        source, _ = self.register()
        self.assertIn("from airflow.sdk import", source)
        self.assertNotIn("airflow.models", source)
        self.assertNotIn("sqlalchemy", source)
        self.assertNotIn("smtp", source.lower())
        task_line = source.index("def validate_store_publish")
        self.assertGreater(source.index("from workflow_lib.adapters import"), task_line)

    def run_task(self, failure=None, ingest_failure=False):
        _, value = self.register()
        function = value["tasks"][0][1]
        function.__globals__["get_current_context"] = lambda: {
            "params": {"source": "hy-home.docker", "business_date": "2026-10-10"}
        }
        calls = []
        adapters = types.ModuleType("workflow_lib.adapters")
        manifest = types.ModuleType("workflow_lib.manifest")

        def read_config(path, *, schema):
            calls.append(("file", path, schema))
            if failure:
                raise ValueError(failure)
            return {"synthetic": schema}

        adapters.read_private_json = read_config

        class Store:
            def __enter__(self):
                calls.append(("store", "enter"))
                return "synthetic_store"

            def __exit__(self, *args):
                calls.append(("store", "exit"))
                return False

        adapters.S3Store = lambda config: Store()
        adapters.PgPublisher = lambda config: "synthetic_publisher"

        def ingest(store, publisher, source, day):
            if ingest_failure:
                raise RuntimeError("synthetic-driver-canary")
            return {"run_id": "a" * 64, "status": "published", "records": 1}

        manifest.ingest = ingest
        package = types.ModuleType("workflow_lib")
        package.__path__ = []
        with patch.dict(
            sys.modules,
            {
                "workflow_lib": package,
                "workflow_lib.adapters": adapters,
                "workflow_lib.manifest": manifest,
            },
        ):
            self.task_calls = calls
            return function(), calls

    def test_task_reads_only_two_ingest_configs_and_returns_bounded_metadata(self):
        result, calls = self.run_task()
        self.assertEqual(
            calls,
            [
                ("file", "/run/opsflow/s3.json", "s3"),
                ("store", "enter"),
                ("file", "/run/opsflow/pg.json", "pg"),
                ("store", "exit"),
            ],
        )
        self.assertEqual(set(result), {"run_id", "status", "records"})

    def test_task_sanitizes_driver_failure_before_airflow_records_it(self):
        with self.assertRaises(RuntimeError) as caught:
            self.run_task("synthetic-private-error")
        self.assertEqual(str(caught.exception), "manifest_task_failed")
        self.assertTrue(caught.exception.__suppress_context__)

    def test_task_closes_s3_client_when_ingest_fails(self):
        with self.assertRaises(RuntimeError) as caught:
            self.run_task(ingest_failure=True)
        self.assertEqual(str(caught.exception), "manifest_task_failed")
        self.assertTrue(caught.exception.__suppress_context__)
        self.assertEqual(self.task_calls[-1], ("store", "exit"))

    def test_overlay_preserves_roles_and_worker_only_access(self):
        overlay = yaml.load(
            (WORKLOAD / "compose.workflow.override.yml").read_text(),
            Loader=OverlayLoader,
        )
        roles = {
            "airflow-apiserver",
            "airflow-scheduler",
            "airflow-dag-processor",
            "airflow-worker",
            "airflow-triggerer",
            "airflow-init",
            "flower",
        }
        self.assertEqual(set(overlay["services"]), roles)
        for role, model in overlay["services"].items():
            self.assertEqual(model["image"], "${OPSFLOW_AIRFLOW_IMAGE:?}")
            self.assertIsNone(model["build"])
            self.assertEqual(model["pull_policy"], "never")
            for key in ("user", "command", "entrypoint"):
                self.assertNotIn(key, model)
            mounts = model.get("volumes", [])
            self.assertEqual(
                sum(mount["target"] == "/run/opsflow" for mount in mounts),
                int(role == "airflow-worker"),
            )
            for mount in mounts:
                self.assertTrue(mount["read_only"])
                self.assertFalse(mount["bind"]["create_host_path"])
            if role == "airflow-worker":
                self.assertEqual(set(model["networks"]), {"dev_data_net", "object_net"})
                self.assertNotIn("secrets", model)
            else:
                self.assertNotIn("networks", model)
        self.assertNotIn("networks", overlay)
        self.assertNotIn("secrets", overlay)


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

    def test_verify_full_driver_reads_sealed_ca_and_closes_it_after_connect(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            ca = directory / "ca.pem"
            original = test_ca_bytes()
            ca.write_bytes(original)
            ca.chmod(0o600)
            observed = {}

            def connect(**kwargs):
                observed["path"] = kwargs["sslrootcert"]
                ca.write_bytes(b"changed-before-driver-read")
                observed["body"] = Path(kwargs["sslrootcert"]).read_bytes()
                return self.connection

            self.connect.side_effect = connect
            config = dict(pg_config(), sslmode="verify-full", sslrootcert=str(ca))
            with patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)):
                publisher = adapters.PgPublisher(config)
                self.assertEqual(
                    publisher.publish(
                        self.manifest,
                        "a" * 64,
                        "b" * 64,
                        "manifest-validated/a.json",
                    ),
                    "published",
                )
            self.assertEqual(observed["body"], original)
            self.assertEqual(self.connect.call_args.kwargs["host"], "dev-pg")
            self.assertEqual(self.connect.call_args.kwargs["sslmode"], "verify-full")
            self.assertEqual(self.connect.call_args.kwargs["gssencmode"], "disable")
            self.assertRegex(observed["path"], r"^/proc/self/fd/[0-9]+$")
            with self.assertRaises(FileNotFoundError):
                Path(observed["path"]).read_bytes()

    def test_libpq_environment_is_rejected_before_driver_use(self):
        publisher = adapters.PgPublisher(pg_config())
        for key in (
            "PGHOSTADDR",
            "PGSERVICE",
            "PGSSLMODE",
            "PGSSLROOTCERT",
            "PGSSLNEGOTIATION",
            "PGSSLCERTMODE",
            "PGGSSENCMODE",
            "PGGSSDELEGATION",
            "PGOPTIONS",
            "SSL_CERT_FILE",
        ):
            with self.subTest(key=key):
                self.connect.reset_mock()
                with patch.dict(os.environ, {key: "poisoned"}):
                    with self.assertRaises(adapters.DependencyError):
                        publisher.publish(
                            self.manifest,
                            "a" * 64,
                            "b" * 64,
                            "manifest-validated/a.json",
                        )
                self.connect.assert_not_called()

    def test_verify_full_connect_failure_closes_sealed_ca(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.chmod(0o700)
            ca = directory / "ca.pem"
            ca.write_bytes(test_ca_bytes())
            ca.chmod(0o600)
            observed = {}

            def fail_connect(**kwargs):
                observed["path"] = kwargs["sslrootcert"]
                self.assertEqual(Path(observed["path"]).read_bytes(), test_ca_bytes())
                raise RuntimeError("sensitive-driver-canary")

            self.connect.side_effect = fail_connect
            config = dict(pg_config(), sslmode="verify-full", sslrootcert=str(ca))
            with patch.object(adapters, "PRIVATE_DIRECTORY", str(directory)):
                with self.assertRaises(adapters.DependencyError):
                    adapters.PgPublisher(config).publish(
                        self.manifest,
                        "a" * 64,
                        "b" * 64,
                        "manifest-validated/a.json",
                    )
            with self.assertRaises(FileNotFoundError):
                Path(observed["path"]).read_bytes()

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
        self.assertNotIn(SYNTHETIC_CREDENTIAL, self.connection.query)
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
