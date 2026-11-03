"""Actual owned Celery publication and metadata-preserving restore scenario."""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
from pathlib import Path

from tests.validation import _opsflow_airflow_native_data as data
from tests.validation import _opsflow_airflow_native_evidence as evidence
from tests.validation import _opsflow_airflow_native_fixture as fixture
from tests.validation import test_opsflow_database_rehearsal as database

NATIVE_DATA_SOURCE_ID = "tests/validation/_opsflow_airflow_native_data.py"


class PublicationScenario:
    """Runs frozen repository DAG bytes; no replacement miniature DAG."""

    def __init__(self, owned):
        self.f = owned
        self.user = f"{owned.uid}:{owned.gid}"
        self.meta_password = " '한글@:/?#%40+ " + secrets.token_hex(24) + " "
        self.valkey_password = " valkey@:/?#%40+ " + secrets.token_hex(24) + " "
        self.s3_key = "synthetic-" + secrets.token_hex(12)
        self.s3_secret = secrets.token_hex(24)
        self.s3_admin_key = "synthetic-admin-" + secrets.token_hex(12)
        self.s3_admin_secret = secrets.token_hex(24)
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
                    "s3_admin_key": self.s3_admin_key,
                    "s3_admin_secret": self.s3_admin_secret,
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
        self.storage_ready()
        self.initialize_storage()
        self.initialize_airflow()
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
        self.verify_database_contract()
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
        self.postgres("metadata-pg", "control", "mng-pg")
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
                + self.meta_password.replace("'", "''")
                + "';CREATE DATABASE airflow OWNER airflow;",
                database="postgres",
            )
            self.f.psql("dev-pg", database.provision_sql(), database="postgres")
            for name in (
                "001_opsflow.sql",
                "003_business_date.sql",
                "004_notification_quarantine.sql",
                "005_data_version.sql",
            ):
                source = fixture.WORKLOAD / "sql" / name
                if name == "005_data_version.sql":
                    rejected = self.f.psql(
                        "dev-pg",
                        "SET ROLE opsflow_reader; SELECT data_version FROM ops_flow.published_documents;",
                        check=False,
                    )
                    if rejected.returncode == 0:
                        raise fixture.RehearsalFailure(
                            "v3 unexpectedly exposes data_version"
                        )
                    self.f.receipt["data_version_red"] = (
                        "v3 reader column rejected before migration005"
                    )
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
            'bind 0.0.0.0\nprotected-mode yes\nport 6389\nsave ""\nappendonly no\nmaxmemory 32mb\nuser default on #'
            + hashlib.sha256(self.valkey_password.encode()).hexdigest()
            + " ~* &* +@all\n",
            ("valkey-server", "/data/valkey.conf"),
        )
        self.storage_backend()

    def storage_backend(self):
        s3_config = json.dumps(
            data.s3_configuration(
                self.s3_key, self.s3_secret, self.s3_admin_key, self.s3_admin_secret
            )
        )
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

    def storage_permission_rehearsal(self):
        """One narrow old-principal RED to corrected-principal GREEN probe."""
        self.f.create_networks()
        self.storage_backend()
        files = self.worker_files()
        self.f.create(
            "worker",
            fixture.AIRFLOW_ID,
            self.user,
            ("data",),
            ("python", "-c", "import time; time.sleep(180)"),
        )
        self.f.start("worker")
        self.f.put(
            "worker",
            {
                "/run/opsflow/s3.json": files["/run/opsflow/s3.json"],
                "/opt/airflow/dags/p04_native_data.py": files[
                    "/opt/airflow/dags/p04_native_data.py"
                ],
            },
        )
        self.storage_administrator(files["/run/opsflow/s3.json"])
        self.storage_ready()
        self.s3(
            "s.create_bucket(Bucket=b); s.create_bucket(Bucket='p04-foreign-bucket')"
        )
        correct = data.worker_bucket_policy()
        old = {
            **correct,
            "Statement": [
                {
                    **row,
                    "Principal": {
                        "AWS": "arn:aws:iam::111111111111:user/synthetic-worker"
                    },
                }
                for row in correct["Statement"]
            ],
        }
        self.s3("s.put_bucket_policy(Bucket=b,Policy=" + repr(json.dumps(old)) + ")")
        self.permission_canaries()
        before = self.permission_observations()
        self.f.receipt["storage_permission_red"] = {
            "status": "FAIL" if not data.permissions_passed(before) else "PASS",
            "observations": before,
        }
        if before.get("delete", {}).get("observed_http") not in {200, 204}:
            raise fixture.RehearsalFailure(
                "old principal delete gap was not reproduced"
            )
        self.s3(
            "s.put_bucket_policy(Bucket=b,Policy=" + repr(json.dumps(correct)) + ")"
        )
        self.permission_canaries()
        self.assert_storage_permissions()
        self.f.receipt["scope"] = (
            "S3 authorization only; no PG, Celery DAG publication or restore"
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
        env = data.production_environment()
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
        self.storage_administrator(files["/run/opsflow/s3.json"])

    def storage_administrator(self, worker_config):
        self.f.create(
            "storage-admin",
            fixture.AIRFLOW_ID,
            self.user,
            ("data",),
            ("python", "-c", "import time; time.sleep(780)"),
        )
        self.f.start("storage-admin")
        config = json.loads(worker_config)
        config.update(
            access_key_id=self.s3_admin_key, secret_access_key=self.s3_admin_secret
        )
        source = Path(data.__file__)
        self.f.put(
            "storage-admin",
            {
                "/run/opsflow/s3.json": json.dumps(config),
                "/opt/airflow/dags/p04_native_data.py": source.read_text(),
            },
        )
        self.source_hashes[NATIVE_DATA_SOURCE_ID] = fixture.sha256(source)

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
        files = {
            "/run/opsflow/pg.json": json.dumps(pg),
            "/run/opsflow/s3.json": json.dumps(s3),
            "/run/secrets/airflow_db_password": self.meta_password + "\n",
            "/run/secrets/mng_valkey_password": self.valkey_password + "\n",
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
        helper = fixture.ROOT / "infra/07-workflow/airflow/connection_uri.py"
        files["/opt/airflow/bin/connection_uri.py"] = helper.read_text()
        self.source_hashes[str(helper.relative_to(fixture.ROOT))] = fixture.sha256(
            helper
        )
        native_data = Path(data.__file__)
        files["/opt/airflow/dags/p04_native_data.py"] = native_data.read_text()
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

    def storage_ready(self):
        self.f.wait(
            lambda: (
                self.f.exec_result(
                    "storage-admin",
                    "python",
                    "-c",
                    fixture.S3_CLIENT + "s.list_buckets()",
                ).returncode
                == 0
            ),
            "isolated S3 unavailable",
        )
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
        return self.f.execute("storage-admin", "python", "-c", fixture.S3_CLIENT + code)

    def initialize_storage(self):
        self.s3("s.create_bucket(Bucket=b)")
        self.s3(
            "s.put_bucket_policy(Bucket=b,Policy="
            + repr(json.dumps(data.worker_bucket_policy()))
            + ")"
        )
        self.s3("s.create_bucket(Bucket='p04-foreign-bucket')")
        self.permission_canaries()
        self.assert_storage_permissions()
        self.s3(
            "s.delete_object(Bucket=b,Key='manifest-validated/permission-canary'); "
            "s.delete_object(Bucket=b,Key='foreign-prefix/denied'); "
            "s.delete_object(Bucket=b,Key='manifest-input/permission-canary'); "
            "s.delete_object(Bucket=b,Key='manifest-validated/permission-write')"
        )
        invalid = b'{"invalid":"synthetic"}'
        digest = hashlib.sha256(invalid).hexdigest()
        self.quarantine = (
            "manifest-quarantine/hy-home.docker/2026-10-10/" + digest + ".json"
        )
        self.install_input(invalid)
        code = """import sys
sys.path.insert(0,'/opt/airflow/dags')
from workflow_lib.adapters import S3Store,PgPublisher,read_private_json
from workflow_lib.manifest import ingest,ContractError
try:
 with S3Store(read_private_json('/run/opsflow/s3.json')) as store:
  ingest(store,PgPublisher(read_private_json('/run/opsflow/pg.json')),'hy-home.docker','2026-10-10')
except ContractError:
 print('rejected')
else:
 raise AssertionError('invalid fixture input was published')
"""
        if self.f.execute("worker", "python", "-c", code).strip() != "rejected":
            raise fixture.RehearsalFailure("invalid input rejection not observed")
        self.assert_database(0)
        observed = json.loads(
            self.s3(
                "x=s.get_object(Bucket=b,Key=" + repr(self.quarantine) + "); "
                "print(json.dumps({'digest':hashlib.sha256(x['Body'].read()).hexdigest(),'metadata':x['Metadata'],'type':x['ContentType']}))"
            )
        )
        if observed != {
            "digest": digest,
            "metadata": {"reason": "manifest_invalid", "data-version": digest},
            "type": "application/octet-stream",
        }:
            raise fixture.RehearsalFailure("quarantine metadata changed")
        self.install_input(self.raw, capture_context=True)
        self.f.receipt["invalid_input_quarantine"] = {
            "status": "PASS",
            "execution": "actual Worker container adapter process",
            "celery_invalid_input": "NOT_RUN",
            "publication": "absent",
        }

    def install_input(self, raw, capture_context=False):
        code = (
            "s.put_object(Bucket=b,Key='manifest-input/hy-home.docker/2026-10-10.json',Body=base64.b64decode("
            + repr(base64.b64encode(raw).decode())
            + "),ContentType='application/json',Metadata={'source':'synthetic'},Tagging='scope=p04-recovery')"
        )
        if capture_context:
            self.f.execute(
                "storage-admin",
                "python",
                "-c",
                fixture.S3_CLIENT + code,
                s3_failure_logs=True,
            )
        else:
            self.s3(code)

    def permission_canaries(self):
        self.s3(
            "s.put_object(Bucket=b,Key='manifest-validated/permission-canary',Body=b'synthetic'); "
            "s.put_object(Bucket=b,Key='manifest-input/permission-canary',Body=b'synthetic'); "
            "s.put_object(Bucket=b,Key='foreign-prefix/denied',Body=b'synthetic'); "
            "s.delete_object(Bucket=b,Key='manifest-validated/permission-write')"
        )

    def permission_observations(self):
        code = "sys.path.insert(0,'/opt/airflow/dags'); import p04_native_data as d; print(json.dumps(d.permission_observations(s,b)))"
        return data.parse_permission_observations(
            self.f.execute("worker", "python", "-c", fixture.S3_CLIENT + code)
        )

    def assert_storage_permissions(self):
        observed = self.permission_observations()
        passed = data.permissions_passed(observed)
        self.f.receipt["storage_permissions"] = {
            "status": "PASS" if passed else "FAIL",
            "observations": observed,
        }
        if not passed:
            raise fixture.RehearsalFailure("storage permission denial not observed")

    def assert_database(self, expected):
        sql = "SELECT (SELECT count(*) FROM ops_flow.runs)||':'||(SELECT count(*) FROM ops_flow.outbox)||':'||(SELECT count(*) FROM ops_flow.current_runs);"
        if self.f.psql("dev-pg", sql).stdout.strip() != ":".join([str(expected)] * 3):
            raise fixture.RehearsalFailure("manifest/outbox idempotency violated")
        if expected:
            current = self.f.psql(
                "dev-pg",
                "SET ROLE opsflow_reader; SELECT DISTINCT data_version FROM ops_flow.published_documents;",
            ).stdout.strip()
            if current != self.digest:
                raise fixture.RehearsalFailure("published data_version changed")

    def assert_s3(self):
        code = (
            "items=s.list_objects_v2(Bucket=b).get('Contents',[]); assert sorted(x['Key'] for x in items)=="
            + repr(
                sorted(
                    [
                        "manifest-input/hy-home.docker/2026-10-10.json",
                        self.artifact,
                        self.quarantine,
                    ]
                )
            )
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
        extensions_before = self.f.psql(
            "dev-pg",
            "SELECT extname||':'||extversion FROM pg_extension ORDER BY extname;",
        ).stdout
        snapshots = json.loads(
            self.s3(
                "sys.path.insert(0,'/opt/airflow/dags'); import p04_native_data as d; "
                "print(json.dumps(d.capture_objects(s,b)))"
            )
        )
        data.validate_snapshot(snapshots)
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
            "ALTER ROLE airflow PASSWORD '"
            + self.meta_password.replace("'", "''")
            + "';",
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
                    "storage-admin",
                    "python",
                    "-c",
                    fixture.S3_CLIENT + "s.list_buckets()",
                ).returncode
                == 0
            ),
            "replacement S3 unavailable",
        )
        self.f.configure_s3()
        self.s3("s.create_bucket(Bucket=b)")
        self.s3(
            "s.put_bucket_policy(Bucket=b,Policy="
            + repr(json.dumps(data.worker_bucket_policy()))
            + ")"
        )
        if fixture.private_identity(s3_path) != self.f.files[s3_path]:
            raise fixture.RehearsalFailure("S3 snapshot changed")
        data.restore_snapshot(self.f, json.loads(s3_path.read_text()))
        self.initialize_airflow(restored=True)
        self.assert_database(1)
        self.assert_s3()
        self.verify_database_contract()
        if (
            self.f.psql(
                "dev-pg",
                "SELECT extname||':'||extversion FROM pg_extension ORDER BY extname;",
            ).stdout
            != extensions_before
        ):
            raise fixture.RehearsalFailure("restored extensions changed")
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
            "object_metadata": "body,size,ContentType,user metadata,tags read back",
            "home": "NOT_RUN",
            "timescaledb": "NOT_RUN",
            "oidc": "NOT_RUN",
        }

    def verify_database_contract(self):
        migration = fixture.WORKLOAD / "sql/005_data_version.sql"
        checker = fixture.WORKLOAD / "sql/006_checks.sql"
        self.source_hashes[str(checker.relative_to(fixture.ROOT))] = fixture.sha256(
            checker
        )
        sql = (
            "\\set migration_sha256 '"
            + fixture.sha256(migration)
            + "'\n"
            + checker.read_text()
        )
        self.f.psql("dev-pg", sql)
