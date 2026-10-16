"""Opt-in actual Celery publication; default runs validate only fixture boundaries."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tests.validation import _opsflow_airflow_native_evidence as evidence
from tests.validation import _opsflow_airflow_native_fixture as fixture
from tests.validation import test_opsflow_database_rehearsal as database


class AirflowNativeBoundaryTests(unittest.TestCase):
    def test_exact_image_context_and_no_docker_override(self):
        selected = {
            "OPSFLOW_AIRFLOW_NATIVE_IMAGE": "sha256:8c139dddc7fcb484970340045848ae9f4d8d09f5b5444762e96f5b80504886f2",
            "OPSFLOW_AIRFLOW_NATIVE_CONTEXT": "default",
        }
        fixture.validate_target(selected)
        for changed in (
            {},
            {**selected, "OPSFLOW_AIRFLOW_NATIVE_IMAGE": "latest"},
            {**selected, "DOCKER_HOST": "tcp://untrusted:2375"},
        ):
            with (
                self.subTest(changed=tuple(changed)),
                self.assertRaises(fixture.RehearsalFailure),
            ):
                fixture.validate_target(changed)

    def test_airflow_digest_types_and_old_root_selection_are_closed(self):
        descriptor = {
            "digest": fixture.AIRFLOW_MANIFEST_ID,
            "mediaType": "application/vnd.oci.image.manifest.v1+json",
            "platform": {"os": "linux", "architecture": "amd64"},
        }
        fixture.validate_airflow_platform(descriptor)
        for wrong in (fixture.AIRFLOW_ID, fixture.AIRFLOW_CONFIG_ID):
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.validate_airflow_platform({**descriptor, "digest": wrong})
        self.assertEqual(
            "image config", fixture.airflow_runtime_identity(fixture.AIRFLOW_CONFIG_ID)
        )
        with self.assertRaises(fixture.RehearsalFailure):
            fixture.validate_target(
                {
                    "OPSFLOW_AIRFLOW_NATIVE_IMAGE": "sha256:0388863fe9964d7f2d0d8bacc26dcae0ad5888eadd275c10086a7683bfe46c56",
                    "OPSFLOW_AIRFLOW_NATIVE_CONTEXT": "default",
                }
            )

    def test_resource_budget_and_no_public_or_host_mount_options(self):
        self.assertEqual(3648, sum(row[0] for row in fixture.CAPS.values()))
        self.assertEqual(2000, sum(row[1] for row in fixture.CAPS.values()))
        for role in fixture.CAPS:
            options = fixture.create_options(role, "50000:0")
            self.assertIn("--read-only", options)
            self.assertIn("--memory-swap", options)
            self.assertIn("no-new-privileges=true", options)
            self.assertNotIn("--publish", options)
            self.assertNotIn("--volume", options)
            self.assertNotIn("--mount", options)
            if role.endswith("-pg"):
                self.assertTrue(
                    any(value.startswith("/var/lib/postgresql:") for value in options)
                )

    def test_private_file_rejects_links_permissions_and_identity_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "synthetic"
            target.write_text("synthetic-only")
            target.chmod(0o600)
            expected = fixture.private_identity(target)
            self.assertEqual(expected, fixture.private_identity(target))
            target.chmod(0o644)
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.private_identity(target)
            target.chmod(0o600)
            link = Path(directory) / "alias"
            link.symlink_to(target)
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.private_identity(link)
            link.unlink()
            target.write_text("modified-synthetic")
            self.assertNotEqual(expected, fixture.private_identity(target))
            os.link(target, link)
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.private_identity(target)

    def test_private_read_ignores_atime_but_binds_stable_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "synthetic"
            target.write_text("synthetic-only")
            target.chmod(0o600)
            before = target.stat()
            fields = "st_mode st_nlink st_uid st_size st_dev st_ino st_mtime_ns st_ctime_ns".split()
            after = SimpleNamespace(
                **{key: getattr(before, key) for key in fields},
                st_atime_ns=before.st_atime_ns + 120000000000,
            )
            with mock.patch.object(fixture.os, "fstat", side_effect=[before, after]):
                observed = fixture.private_identity(target)
            self.assertEqual(
                hashlib.sha256(b"synthetic-only").hexdigest(), observed[-1]
            )

    def test_probe_requires_actual_runtime_versions_and_nonroot_uid(self):
        observed = json.loads("""{"uid":50000,"gid":0,"airflow":"3.3.2","celery":"3.24.1",
"boto3":true,"psycopg2":true,"sdk":true,"forbidden_env":[]}""")
        self.assertEqual((50000, 0), fixture.validate_probe(observed))
        safe = fixture.probe_observations({**observed, "token": "must-not-print"})
        self.assertNotIn("must-not-print", json.dumps(safe))
        self.assertEqual("3.3.2", safe["airflow"])
        for key, value in (
            ("uid", 0),
            ("uid", True),
            ("airflow", "3.3.1"),
            ("boto3", False),
            ("forbidden_env", ["PGPASSWORD"]),
        ):
            with self.subTest(key=key), self.assertRaises(fixture.RehearsalFailure):
                fixture.validate_probe({**observed, key: value})

    def test_partial_create_is_retained_for_identity_checked_cleanup(self):
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        f.attempt, f.generation, f.receipt = "synthetic", 1, {}
        f.containers, f.pending_containers, f.networks = {}, {}, {}
        f.remaining = mock.Mock()
        f.verify = mock.Mock()
        cid = "a" * 64
        f.client = mock.Mock()
        f.client.run_result.return_value = SimpleNamespace(returncode=1, stdout=cid)
        f.client.run.return_value = cid
        with self.assertRaises(fixture.RehearsalFailure):
            f.create(
                "probe", fixture.AIRFLOW_ID, "airflow", (), ("python", "-c", "pass")
            )
        self.assertEqual(cid, f.containers["probe"].cid)
        f.verify.side_effect = fixture.RehearsalFailure("changed")
        f.client.reset_mock()
        with self.assertRaises(fixture.RehearsalFailure):
            f.remove("probe")
        f.client.run.assert_not_called()
        f.verify.side_effect = None
        f.client.deadline, f.client.cleanup_deadline = float("inf"), None
        for error, status, removed in (
            (OSError(), 1, True),
            (OSError(), 0, False),
            (KeyboardInterrupt(), 1, False),
        ):
            f.containers["probe"] = SimpleNamespace(cid=cid)
            f.client.reset_mock()
            f.client.run.side_effect = error
            f.client.run_result.return_value = SimpleNamespace(
                returncode=status,
                stdout="",
                stderr="error: no such object: " + cid if status == 1 else "",
            )
            if removed:
                f.remove("probe")
            else:
                with self.assertRaises(
                    KeyboardInterrupt
                    if isinstance(error, KeyboardInterrupt)
                    else fixture.RehearsalFailure
                ):
                    f.remove("probe")
            self.assertEqual(not removed, "probe" in f.containers)
            if isinstance(error, KeyboardInterrupt):
                f.client.run_result.assert_not_called()
            else:
                f.client.run_result.assert_called_once_with(
                    "inspect", "--format", "{{.Id}}", cid
                )

    def test_unreviewed_target_and_unknown_roles_never_create(self):
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        f.containers = {}
        f.remaining = mock.Mock()
        f.client = mock.Mock()
        for role, image in (("probe", "latest"), ("unknown", fixture.AIRFLOW_ID)):
            with self.assertRaises(fixture.RehearsalFailure):
                f.create(role, image, "airflow", (), ("python", "-c", "pass"))
        f.client.run_result.assert_not_called()

    def test_empty_cluster_bootstrap_precedes_guarded_project_provision(self):
        scenario = PublicationScenario.__new__(PublicationScenario)
        scenario.f = mock.Mock()
        scenario.postgres = mock.Mock()
        scenario.create_file_backend = mock.Mock()
        scenario.meta_password = scenario.valkey_password = "public-synthetic-only"
        scenario.s3_key = scenario.s3_secret = "public-synthetic-only"
        scenario.source_hashes = {}
        scenario.backends()
        self.assertEqual(
            fixture.S3_SERVER_COMMAND, scenario.create_file_backend.call_args.args[6]
        )
        calls = [
            item for item in scenario.f.psql.call_args_list if item.args[0] == "dev-pg"
        ]
        self.assertTrue(
            "reviewed_connect_consumers 'reviewed'" in calls[0].args[1],
            "empty fixture cluster review acknowledgment missing",
        )
        self.assertIn(
            "REVOKE CONNECT ON DATABASE postgres, template1 FROM PUBLIC",
            calls[0].args[1],
        )
        self.assertEqual(database.provision_sql(), calls[1].args[1])
        self.assertEqual(3, len(scenario.source_hashes))
        self.assertEqual(
            ["opsflow_migrator"] * 3, [c.kwargs.get("user") for c in calls[2:]]
        )
        for relative, digest in scenario.source_hashes.items():
            self.assertEqual(digest, fixture.sha256(fixture.ROOT / relative))

    def test_empty_restored_cluster_keeps_reviewed_connect_boundary(self):
        scenario = PublicationScenario.__new__(PublicationScenario)
        scenario.f = mock.Mock()
        scenario.postgres = mock.Mock()
        scenario.create_file_backend = mock.Mock()
        synthetic = "public-synthetic-only"
        for name in ("valkey_password", "s3_key", "s3_secret"):
            setattr(scenario, name, synthetic)
        scenario.backends(restore=True)
        self.assertEqual(
            fixture.S3_SERVER_COMMAND, scenario.create_file_backend.call_args.args[6]
        )
        calls = [
            item for item in scenario.f.psql.call_args_list if item.args[0] == "dev-pg"
        ]
        self.assertEqual(1, len(calls), "fresh restored cluster ACL bootstrap missing")
        self.assertTrue(
            "reviewed_connect_consumers 'reviewed'" in calls[0].args[1],
            "replacement fixture cluster review acknowledgment missing",
        )

    def test_prechange_resource_and_owner_network_guards(self):
        healthy = dict(
            memory=8 * 1024**3, swap=2 * 1024**3, disk=11 * 1024**3, inode_ratio=0.2
        )
        fixture.validate_resources(healthy, prestart=True)
        fixture.validate_resources({**healthy, "swap": 0}, prestart=True)
        for key, value in (
            ("memory", 6 * 1024**3),
            ("disk", 9 * 1024**3),
            ("inode_ratio", 0.09),
        ):
            with self.subTest(key=key), self.assertRaises(fixture.RehearsalFailure):
                fixture.validate_resources({**healthy, key: value}, prestart=True)
        f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
        f.work_deadline, f.containers, f.client = float("inf"), {}, mock.Mock()
        with mock.patch.object(
            fixture, "host_resources", return_value={**healthy, "memory": 2 * 1024**3}
        ):
            for call in (
                lambda: f.create(
                    "probe", fixture.AIRFLOW_ID, "airflow", (), ("python",)
                ),
                lambda: f.start("probe"),
                lambda: f.exec_result("probe", "true"),
                lambda: f.wait(lambda: True, "must fail"),
            ):
                with self.assertRaises(fixture.RehearsalFailure):
                    call()
        f.remaining = mock.Mock()
        f.client.run.side_effect = ["", "a" * 64]
        with self.assertRaises(fixture.RehearsalFailure):
            f.prerequisites()
        self.assertEqual("network", f.client.run.call_args.args[0])

    def test_ordinary_networks_follow_observed_container_lifecycle(self):
        match = fixture.ordinary_networks_match
        want = {"owned": ("a" * 64, ["worker"])}
        for state, network, endpoint in (
            ("created", "", ""),
            ("running", "a" * 64, "b" * 64),
            ("exited", "a" * 64, ""),
        ):
            ep = dict(NetworkID=network, EndpointID=endpoint, Aliases=["worker"])
            self.assertTrue(match(state, {"owned": ep}, want))
            for key in ("NetworkID", "EndpointID", "Aliases"):
                bad = {**ep, key: "wrong"}
                self.assertFalse(match(state, {"owned": bad}, want))
            self.assertFalse(match(state, {"foreign": ep}, want))
        self.assertFalse(match("restarting", {"owned": ep}, want))

    def test_cleanup_failure_retains_host_and_always_emits_receipt(self):
        for begin_error in (False, True):
            f = fixture.AirflowFixture.__new__(fixture.AirflowFixture)
            f.client, f._cleanup_host, f._unlock = mock.Mock(), mock.Mock(), mock.Mock()
            f.client.cleanup_deadline = f.deadline = float("inf")
            f.attempt = "synthetic"
            f.directory, f.dir_identity = Path("/tmp/owned"), (1, 2)
            f.containers, f.networks, f.pending_containers, f.pending_networks = (
                dict() for _ in range(4)
            )
            f.receipt, f.runtime_images = {}, {}
            f.client.run.side_effect = ["a" * 64, ""]
            if begin_error:
                f.client.begin_cleanup.side_effect = RuntimeError("synthetic")
            with self.assertRaises(fixture.RehearsalFailure):
                f.cleanup()
            f._cleanup_host.assert_not_called()
            self.assertEqual("FAIL", f.receipt["cleanup"])
            if begin_error:
                self.assertIsNone(f.receipt["retained"]["swept_container_ids"])
            self.assertEqual(
                str(f.directory), f.receipt["retained"]["attempt_directory"]
            )
            f.prerequisites = mock.Mock(side_effect=fixture.RehearsalFailure("stop"))
            with (
                mock.patch.object(fixture, "AirflowFixture", return_value=f),
                mock.patch("builtins.print") as printed,
            ):
                with self.assertRaises(fixture.RehearsalFailure):
                    AirflowNativeRehearsal().test_actual_celery_publication_retry_replay_and_empty_restore()
                printed.assert_called_once()

    def test_seaweed_startup_bounds_both_collections_before_ready(self):
        import subprocess
        import tomllib

        scenario = PublicationScenario.__new__(PublicationScenario)
        scenario.f = mock.Mock()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)

            def stage(*args, input_):
                command = args[3].replace("/data", str(directory))
                subprocess.run(
                    ["/bin/sh", "-ceu", command], input=input_, text=True, check=True
                )

            scenario.f.execute.side_effect = stage
            scenario.create_file_backend(
                "s3",
                fixture.S3_ID,
                "65532:65532",
                ("data",),
                "/data/s3.json",
                "{}",
                fixture.S3_SERVER_COMMAND,
            )
            self.assertEqual(
                {"master": {"volume_growth": {"copy_1": 1}}},
                tomllib.loads((directory / "master.toml").read_text()),
            )
            self.assertTrue((directory / "ready").is_file())
            command = scenario.f.execute.call_args.args[3]
            self.assertLess(
                command.index("master.toml"), command.index("touch /data/ready")
            )
        self.assertEqual(
            ("weed", "-config_dir=/data", "server"), fixture.S3_SERVER_COMMAND[:3]
        )
        self.assertEqual(1, fixture.S3_SERVER_COMMAND.count("-volume.max=2"))
        self.assertIn("-master.volumeSizeLimitMB=64", fixture.S3_SERVER_COMMAND)

    def test_driver_payloads_and_embedded_commands_compile_without_runtime(self):
        for source in (
            fixture.PROBE,
            fixture.WRITE_FILES,
            fixture.WAIT.format(command=repr(["airflow", "scheduler"])),
            fixture.S3_CLIENT,
        ):
            compile(source, "synthetic-fixture-payload", "exec")
        for selected in (
            {"OPSFLOW_AIRFLOW_NATIVE_CONTEXT": "default"},
            {"OPSFLOW_AIRFLOW_NATIVE_FLAG": ""},
            {"OPSFLOW_AIRFLOW_NATIVE_IMAGE": ""},
        ):
            with self.assertRaises(fixture.RehearsalFailure):
                fixture.validate_target(selected)


@unittest.skipUnless(
    any(key.startswith("OPSFLOW_AIRFLOW_NATIVE_") for key in os.environ),
    "exact cached image and isolated serial runtime required",
)
class AirflowNativeRehearsal(unittest.TestCase):
    def test_actual_celery_publication_retry_replay_and_empty_restore(self):
        owned = fixture.AirflowFixture()
        failure = None
        try:
            owned.prerequisites()
            owned.probe()
            scenario = PublicationScenario(owned)
            scenario.run()
        except BaseException as error:
            failure = error
        finally:
            for finalize in (
                owned.cleanup,
                lambda: print(json.dumps(owned.receipt, sort_keys=True)),
            ):
                try:
                    finalize()
                except BaseException as error:
                    if failure is None or (
                        isinstance(failure, Exception)
                        and not isinstance(error, Exception)
                    ):
                        failure = error
        if failure is not None:
            raise failure


class PublicationScenario:
    """Runs frozen repository DAG bytes; no replacement miniature DAG."""

    def __init__(self, owned):
        self.f = owned
        self.user = f"{owned.uid}:{owned.gid}"
        self.meta_password = secrets.token_hex(24)
        self.valkey_password = secrets.token_hex(24)
        self.s3_key = "synthetic-" + secrets.token_hex(12)
        self.s3_secret = secrets.token_hex(24)
        self.fernet = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        self.jwt = secrets.token_hex(32)
        self.raw = (fixture.WORKLOAD / "fixtures/2026-10-10.json").read_bytes()
        self.digest = hashlib.sha256(self.raw).hexdigest()
        self.run_id = hashlib.sha256(
            f"hy-home.docker:{self.digest}".encode()
        ).hexdigest()
        self.artifact = f"manifest-validated/hy-home.docker/{self.run_id}.json"
        self.source_hashes = {}
        self.f.private("synthetic-input.json", self.raw.decode())
        self.f.private(
            "synthetic-secrets.json",
            json.dumps(
                {
                    "metadata": self.meta_password,
                    "valkey": self.valkey_password,
                    "s3_key": self.s3_key,
                    "s3_secret": self.s3_secret,
                    "fernet": self.fernet,
                    "jwt": self.jwt,
                    "ingest": "p04-ingest-synthetic-only",
                }
            ),
        )

    def run(self):
        self.f.create_networks()
        self.backends()
        self.airflow()
        self.initialize_airflow()
        self.s3("s.create_bucket(Bucket=b)")
        self.f.execute(
            "worker",
            "python",
            "-c",
            fixture.S3_CLIENT
            + "s.put_object(Bucket=b,Key='manifest-input/hy-home.docker/2026-10-10.json',Body=base64.b64decode("
            + repr(base64.b64encode(self.raw).decode())
            + "))",
            s3_failure_logs=True,
        )
        self.f.psql(
            "dev-pg",
            "REVOKE EXECUTE ON FUNCTION " + fixture.FUNCTION + " FROM opsflow_ingest;",
        )
        self.trigger("synthetic-retry")
        self.wait_state("synthetic-retry", "up_for_retry")
        self.assert_database(0)
        self.object_digest = self.s3(
            "print(hashlib.sha256(s.get_object(Bucket=b,Key="
            + repr(self.artifact)
            + ")['Body'].read()).hexdigest())"
        ).strip()
        self.f.psql(
            "dev-pg",
            "GRANT EXECUTE ON FUNCTION " + fixture.FUNCTION + " TO opsflow_ingest;",
        )
        self.wait_state("synthetic-retry", "success")
        self.assert_worker("synthetic-retry")
        row = self.metadata(
            "SELECT try_number FROM task_instance WHERE run_id='synthetic-retry';"
        ).strip()
        if int(row) < 2:
            raise fixture.RehearsalFailure("Celery retry was not observed")
        self.assert_database(1)
        self.trigger("synthetic-replay")
        self.wait_state("synthetic-replay", "success")
        self.assert_database(1)
        self.assert_s3()
        self.f.receipt["publication"] = {
            "status": "PASS",
            "celery_retry_try_number": int(row),
            "replay": "PASS",
            "source_sha256": self.source_hashes,
            "manifest_sha256": self.digest,
            "artifact_sha256": self.object_digest,
        }
        self.recover()

    def postgres(self, role, network, alias):
        command = fixture.postgres_command(role)
        self.f.create(role, fixture.PG_ID, "70:70", (network,), command, alias=alias)
        self.f.start(role)
        self.f.wait(
            lambda: (
                self.f.psql(role, "SELECT 1", "postgres", check=False).returncode == 0
            ),
            "isolated PostgreSQL readiness failed",
        )

    def backends(self, restore=False):
        self.postgres("metadata-pg", "control", "metadata-pg")
        self.postgres("dev-pg", "data", "dev-pg")
        self.f.psql(
            "dev-pg",
            "\\set reviewed_connect_consumers 'reviewed'\n"
            + database.CLUSTER_CONNECT.read_text(),
            database="postgres",
        )
        if not restore:
            self.f.psql(
                "metadata-pg",
                "CREATE ROLE airflow LOGIN PASSWORD '"
                + self.meta_password
                + "';CREATE DATABASE airflow OWNER airflow;",
                database="postgres",
            )
            self.f.psql("dev-pg", database.provision_sql(), database="postgres")
            for name in (
                "001_opsflow.sql",
                "003_business_date.sql",
                "004_notification_quarantine.sql",
            ):
                source = fixture.WORKLOAD / "sql" / name
                self.source_hashes[str(source.relative_to(fixture.ROOT))] = (
                    fixture.sha256(source)
                )
                self.f.psql(
                    "dev-pg", database.migration_sql(source), user="opsflow_migrator"
                )
        self.create_file_backend(
            "valkey",
            fixture.VALKEY_ID,
            "999:999",
            ("control",),
            "/data/valkey.conf",
            'bind 0.0.0.0\nprotected-mode yes\nport 6379\nsave ""\nappendonly no\nmaxmemory 32mb\nrequirepass '
            + self.valkey_password
            + "\n",
            ("valkey-server", "/data/valkey.conf"),
        )
        identity = {
            "name": "synthetic-fixture",
            "credentials": [{"accessKey": self.s3_key, "secretKey": self.s3_secret}],
            "actions": "Admin Read Write List Tagging".split(),
        }
        s3_config = json.dumps({"identities": [identity]})
        self.create_file_backend(
            "s3",
            fixture.S3_ID,
            "65532:65532",
            ("data",),
            "/data/s3.json",
            s3_config,
            fixture.S3_SERVER_COMMAND,
            alias="seaweedfs-s3",
        )

    def create_file_backend(
        self, role, image, user, networks, path, contents, command, alias=None
    ):
        fixture.stage_file_backend(
            self.f, role, image, user, networks, path, contents, command, alias
        )

    def airflow(self):
        commands = {
            "api": "airflow api-server --apps execution -w 1".split(),
            "scheduler": ["airflow", "scheduler"],
            "processor": ["airflow", "dag-processor"],
            "worker": "airflow celery worker -c 1 --without-mingle --without-gossip -s".split(),
        }
        env = fixture.airflow_environment()
        files = self.worker_files()
        for role in fixture.AF_ROLES:
            networks = ("control", "data") if role == "worker" else ("control",)
            self.f.create(
                role,
                fixture.AIRFLOW_ID,
                self.user,
                networks,
                ("python", "-c", fixture.WAIT.format(command=repr(commands[role]))),
                alias="airflow-apiserver" if role == "api" else role,
                env=env,
            )
            self.f.start(role)
            self.f.put(
                role,
                files
                if role == "worker"
                else {
                    k: v for k, v in files.items() if not k.startswith("/run/opsflow/")
                },
            )

    def worker_files(self):
        pg = json.loads("""{"host":"dev-pg","port":5432,"dbname":"opsflow_dev","user":"opsflow_ingest",
"password":"p04-ingest-synthetic-only","connect_timeout":5,"statement_timeout_ms":10000,
"lock_timeout_ms":5000,"sslmode":"disable","sslrootcert":null}""")
        s3 = {
            **json.loads("""{"endpoint_url":"http://seaweedfs-s3:8333","bucket":"opsflow-dev","region":"us-east-1",
"addressing_style":"path","ca_bundle":null,"connect_timeout":2,"read_timeout":3,
"endpoint_contract":"seaweedfs-s3-internal-v1"}"""),
            "access_key_id": self.s3_key,
            "secret_access_key": self.s3_secret,
        }
        uri = (
            "postgresql+psycopg2://airflow:"
            + self.meta_password
            + "@metadata-pg:5432/airflow"
        )
        files = {
            "/run/opsflow/pg.json": json.dumps(pg),
            "/run/opsflow/s3.json": json.dumps(s3),
            "/run/airflow-fixture/database": uri,
            "/run/airflow-fixture/result": uri.replace(
                "postgresql+psycopg2", "db+postgresql"
            ),
            "/run/airflow-fixture/broker": "redis://:"
            + self.valkey_password
            + "@valkey:6379/0",
            "/run/airflow-fixture/fernet": self.fernet,
            "/run/airflow-fixture/jwt": self.jwt,
            "/run/airflow-fixture/simple-passwords.json": "{}",
        }
        paths = [
            fixture.WORKLOAD / "dags/source_manifest_ingest.py",
            *sorted((fixture.WORKLOAD / "workflow_lib").glob("*.py")),
        ]
        for path in paths:
            destination = "/opt/airflow/dags/" + (
                path.name if path.parent.name == "dags" else "workflow_lib/" + path.name
            )
            files[destination] = path.read_text()
            self.source_hashes[str(path.relative_to(fixture.ROOT))] = fixture.sha256(
                path
            )
        return files

    def cli(self, *args):
        return self.f.execute("scheduler", "airflow", *args)

    def initialize_airflow(self, restored=False):
        self.cli("db", "check") if restored else self.cli("db", "migrate")
        if not restored:
            self.cli("pools", "set", "manifest_ingest", "1", "synthetic fixture")
        for role in fixture.AF_ROLES:
            self.f.put(role, {"/tmp/fixture-ready": "ready"})
        self.f.wait(
            lambda: (
                self.metadata(
                    "SELECT count(*) FROM dag WHERE dag_id='source_manifest_ingest';"
                ).strip()
                == "1"
            ),
            "frozen DAG was not registered",
            seconds=120,
        )
        self.cli("dags", "unpause", "source_manifest_ingest")
        self.f.wait(
            lambda: (
                self.f.exec_result(
                    "worker", "python", "-c", fixture.S3_CLIENT + "s.list_buckets()"
                ).returncode
                == 0
            ),
            "isolated S3 unavailable",
        )
        if not restored:
            self.f.configure_s3()

    def metadata(self, sql):
        return self.f.psql("metadata-pg", sql, database="airflow").stdout

    def trigger(self, run):
        self.cli(
            "dags",
            "trigger",
            "-r",
            run,
            "-c",
            '{"source":"hy-home.docker","business_date":"2026-10-10"}',
            "source_manifest_ingest",
        )

    def wait_state(self, run, state):
        query = (
            "SELECT state FROM task_instance WHERE dag_id='source_manifest_ingest' AND task_id='validate_store_publish' AND run_id='"
            + run
            + "';"
        )
        self.f.wait(
            lambda: self.metadata(query).strip() == state,
            "actual Celery task did not reach " + state,
            seconds=180,
        )
        if state == "success":
            self.f.wait(
                lambda: (
                    self.metadata(
                        "SELECT state FROM dag_run WHERE dag_id='source_manifest_ingest' AND run_id='"
                        + run
                        + "';"
                    ).strip()
                    == "success"
                ),
                "DagRun did not reach terminal success",
                seconds=30,
            )

    def assert_worker(self, run):
        row = self.metadata(
            "SELECT hostname||':'||coalesce(external_executor_id,'') FROM task_instance WHERE run_id='"
            + run
            + "';"
        ).strip()
        hostname = self.f.containers["worker"].name
        if not row.startswith(hostname + ":") or not row.removeprefix(hostname + ":"):
            raise fixture.RehearsalFailure(
                "actual Celery executor/worker identity missing"
            )
        self.f.receipt["worker_identity"] = {
            "hostname": hostname,
            "executor": "CeleryExecutor",
            "task_external_executor_id_present": True,
        }

    def s3(self, code):
        return self.f.execute("worker", "python", "-c", fixture.S3_CLIENT + code)

    def assert_database(self, expected):
        sql = "SELECT (SELECT count(*) FROM ops_flow.runs)||':'||(SELECT count(*) FROM ops_flow.outbox)||':'||(SELECT count(*) FROM ops_flow.current_runs);"
        if self.f.psql("dev-pg", sql).stdout.strip() != ":".join([str(expected)] * 3):
            raise fixture.RehearsalFailure("manifest/outbox idempotency violated")

    def assert_s3(self):
        code = (
            "items=s.list_objects_v2(Bucket=b).get('Contents',[]); assert sorted(x['Key'] for x in items)=="
            + repr(["manifest-input/hy-home.docker/2026-10-10.json", self.artifact])
            + "; print(hashlib.sha256(s.get_object(Bucket=b,Key="
            + repr(self.artifact)
            + ")['Body'].read()).hexdigest())"
        )
        if self.s3(code).strip() != self.object_digest:
            raise fixture.RehearsalFailure("S3 readback changed")

    def recover(self):
        for role in ("scheduler", "processor", "api"):
            self.f.stop(role)
        if (
            self.metadata(
                "SELECT count(*) FROM dag_run WHERE state IN ('queued','running');"
            ).strip()
            != "0"
        ):
            raise fixture.RehearsalFailure("metadata writers not quiesced")
        evidence.inspect_celery_idle(self.f)
        snapshots = json.loads(
            self.s3(
                "print(json.dumps({x['Key']:base64.b64encode(s.get_object(Bucket=b,Key=x['Key'])[\"Body\"].read()).decode() for x in s.list_objects_v2(Bucket=b).get('Contents',[])}))"
            )
        )
        self.f.stop("worker")
        meta = self.f.dump("metadata-pg", "airflow")
        dev = self.f.dump("dev-pg", "opsflow_dev")
        roles = {role: self.f.dump_roles(role) for role in ("metadata-pg", "dev-pg")}
        s3_path = self.f.private("s3-snapshot.json", json.dumps(snapshots))
        for role in reversed(tuple(self.f.containers)):
            self.f.remove(role)
        self.f.generation += 1
        self.backends(restore=True)
        for role, path in roles.items():
            self.f.restore_roles(role, path)
        self.f.psql(
            "metadata-pg",
            "ALTER ROLE airflow PASSWORD '" + self.meta_password + "';",
            database="postgres",
        )
        for kind in ("migrator", "ingest", "notifier", "reader"):
            self.f.psql(
                "dev-pg",
                "ALTER ROLE opsflow_"
                + kind
                + " PASSWORD 'p04-"
                + kind
                + "-synthetic-only';",
                database="postgres",
            )
        self.f.restore("metadata-pg", meta)
        self.f.restore("dev-pg", dev)
        self.airflow()
        # Install objects before releasing scheduler/worker processes.
        self.f.wait(
            lambda: (
                self.f.exec_result(
                    "worker", "python", "-c", fixture.S3_CLIENT + "s.list_buckets()"
                ).returncode
                == 0
            ),
            "replacement S3 unavailable",
        )
        self.f.configure_s3()
        self.s3("s.create_bucket(Bucket=b)")
        if fixture.private_identity(s3_path) != self.f.files[s3_path]:
            raise fixture.RehearsalFailure("S3 snapshot changed")
        for key, encoded in json.loads(s3_path.read_text()).items():
            self.s3(
                "s.put_object(Bucket=b,Key="
                + repr(key)
                + ",Body=base64.b64decode("
                + repr(encoded)
                + "))"
            )
        self.initialize_airflow(restored=True)
        self.assert_database(1)
        self.assert_s3()
        self.trigger("synthetic-restored-replay")
        self.wait_state("synthetic-restored-replay", "success")
        self.assert_worker("synthetic-restored-replay")
        self.assert_database(1)
        self.assert_s3()
        self.f.receipt["recovery"] = {
            "status": "PASS",
            "metadata": "serial empty physical PG18.6",
            "dev": "serial empty physical PG18.6",
            "s3": "serial empty SeaweedFS",
            "worker_replay": "PASS",
            "home": "NOT_RUN",
            "timescaledb": "NOT_RUN",
            "oidc": "NOT_RUN",
        }


if __name__ == "__main__":
    unittest.main()
