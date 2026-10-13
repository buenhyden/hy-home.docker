"""Opt-in isolated PostgreSQL rehearsal using synthetic data and owned tmpfs."""

from __future__ import annotations

import concurrent.futures
import hashlib
import importlib.util
import json
import os
import re
import secrets
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

# fmt: off

ROOT = Path(__file__).resolve().parents[2]
WORKLOAD = ROOT / "infra/07-workflow/airflow/workloads/manifest-pipeline"
PROVISIONER = ROOT / "infra/04-data/dev-db/pg/provision/project.py"
MANIFEST = ROOT / "infra/04-data/dev-db/pg/provision/opsflow.json"
MIGRATION_1 = WORKLOAD / "sql/001_opsflow.sql"
MIGRATION_2 = WORKLOAD / "sql/003_business_date.sql"
CHECKS = WORKLOAD / "sql/002_checks.sql"
IMAGE_ENV = "OPSFLOW_PG_REHEARSAL_IMAGE"
CONTEXT_ENV = "OPSFLOW_PG_REHEARSAL_CONTEXT"
EXPECTED_IMAGE = "sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873"
EXPECTED_CONTEXT = "default"
CONTAINER_ID = re.compile(r"[0-9a-f]{64}\Z")
OWNER_LABEL = "hyhome.opsflow.rehearsal-owner"
ATTEMPT_LABEL = "hyhome.opsflow.rehearsal-attempt"
OWNER = "test_opsflow_database_rehearsal"
PSQL = "psql -X -qAt -v ON_ERROR_STOP=1 -v VERBOSITY=verbose".split()


class RehearsalFailure(AssertionError):
    pass
def psql_diagnostic(stderr: bytes):
    match = re.search(rb"(?:psql:<stdin>:(\d+): )?ERROR:\s+([0-9A-Z]{5}):", stderr)
    return None if match is None else {"sqlstate": match[2].decode(), "statement_line": int(match[1]) if match[1] else None}
def native_selection() -> tuple[str, str] | None:
    image, context = os.environ.get(IMAGE_ENV), os.environ.get(CONTEXT_ENV)
    if image is None and context is None:
        return None
    if any(os.environ.get(key) for key in ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH")):
        raise RehearsalFailure("Docker environment overrides are not allowed")
    if image != EXPECTED_IMAGE:
        raise RehearsalFailure(f"{IMAGE_ENV} must select the reviewed image ID")
    if context != EXPECTED_CONTEXT:
        raise RehearsalFailure(f"{CONTEXT_ENV} must select the reviewed context")
    return image, context
def validate_context(item):
    actual = (item.get("Name"), item.get("DockerHost"), item.get("SkipTLSVerify"))
    if actual != (EXPECTED_CONTEXT, "unix:///var/run/docker.sock", False):
        raise RehearsalFailure("Docker context endpoint is not the reviewed local socket")
def create_argv(image: str, name: str, cidfile: Path, attempt: str, bootstrap: str):
    identity = (
        f"create --cidfile {cidfile} --name {name} --label {OWNER_LABEL}={OWNER} "
        f"--label {ATTEMPT_LABEL}={attempt}"
    ).split()
    limits = (
        "--network none --read-only --user postgres --cap-drop ALL "
        "--security-opt no-new-privileges=true --pids-limit 128 --memory 768m "
        "--memory-swap 768m --cpus 1 --stop-timeout 10"
    ).split()
    tmpfs = (
        "--tmpfs /var/lib/postgresql:rw,nosuid,nodev,noexec,mode=1777,size=512m "
        "--tmpfs /var/run/postgresql:rw,nosuid,nodev,noexec,mode=1777,size=16m "
        "--tmpfs /tmp:rw,nosuid,nodev,noexec,mode=1777,size=16m"
    ).split()
    command = (
        "--entrypoint",
        "/bin/sh",
        image,
        "-ceu",
        "initdb -D /var/lib/postgresql/data --auth-local=trust --auth-host=reject "
        f"--username={bootstrap}; exec postgres -D /var/lib/postgresql/data "
        "-c listen_addresses='' -c unix_socket_directories=/var/run/postgresql "
        "-c max_connections=40 -c shared_buffers=64MB",
    )
    return tuple(identity + limits + tmpfs) + command
class PgFixture:
    def __init__(self, image: str, context: str, bootstrap: str):
        self.image, self.context, self.bootstrap = image, context, bootstrap
        self.attempt = secrets.token_hex(12)
        self.name = f"p04-pg-{self.attempt}"
        self.container_id: str | None = None
        self.scratch = tempfile.TemporaryDirectory(prefix="p04-pg-")
        self.deadline = time.monotonic() + 6 * 60

    def docker(self, *args: str, input_: bytes | None = None, check: bool = True):
        timeout = max(1, min(60, int(self.deadline - time.monotonic())))
        if timeout <= 1 and time.monotonic() >= self.deadline:
            raise RehearsalFailure("isolated PostgreSQL rehearsal timed out")
        try:
            result = subprocess.run(
                ("docker", "--context", self.context, *args), input=input_,
                capture_output=True, timeout=timeout, check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise RehearsalFailure("Docker command unavailable/timed out") from None
        if check and result.returncode:
            diagnostic = psql_diagnostic(result.stderr)
            suffix = "" if diagnostic is None else f" (SQLSTATE {diagnostic['sqlstate']}" + (f", psql line {diagnostic['statement_line']}" if diagnostic["statement_line"] else "") + ")"
            raise RehearsalFailure("Docker command failed (output withheld)" + suffix)
        return result

    def create(self):
        context_fmt = '{"Name":{{json .Name}},"DockerHost":{{json .Endpoints.docker.Host}},"SkipTLSVerify":{{json .Endpoints.docker.SkipTLSVerify}}}'
        context = self.docker("context", "inspect", "--format", context_fmt, self.context)
        try:
            validate_context(json.loads(context.stdout))
        except (json.JSONDecodeError, TypeError):
            raise RehearsalFailure("Docker context metadata is invalid") from None
        fmt = '{"Id":{{json .Id}},"Os":{{json .Os}},"Architecture":{{json .Architecture}}}'
        inspected = self.docker("image", "inspect", "--format", fmt, self.image)
        try:
            item = json.loads(inspected.stdout)
        except (json.JSONDecodeError, KeyError, TypeError):
            raise RehearsalFailure("cached image metadata is invalid") from None
        if (item.get("Id"), item.get("Os"), item.get("Architecture")) != (self.image, "linux", "amd64"):
            raise RehearsalFailure("cached image identity/platform mismatch")
        cidfile = Path(self.scratch.name) / "container.id"
        args = create_argv(self.image, self.name, cidfile, self.attempt, self.bootstrap)
        failure = None
        result = None
        try:
            result = self.docker(*args)
        except RehearsalFailure as error:
            failure = error
            self.deadline = time.monotonic() + 2 * 60
        candidates = [result.stdout.decode().strip()] if result else []
        if cidfile.is_file():
            candidates.append(cidfile.read_text(encoding="ascii").strip())
        found = self.docker(
            "ps", "-aq", "--no-trunc", "--filter", f"name=^/{self.name}$",
            "--filter", f"label={OWNER_LABEL}={OWNER}",
            "--filter", f"label={ATTEMPT_LABEL}={self.attempt}", check=False,
        ).stdout.decode().splitlines()
        valid = {value for value in candidates if CONTAINER_ID.fullmatch(value)}
        if len(found) == 1 and CONTAINER_ID.fullmatch(found[0]):
            self.container_id = found[0]
        if self.container_id is None or valid - {self.container_id}:
            raise RehearsalFailure("owned container identity is ambiguous")
        if failure:
            raise failure
        if self.container_id is None:
            raise RehearsalFailure("owned container ID was not recorded")
        self.docker("start", self.container_id)
        for _ in range(60):
            ready = self.docker("exec", self.container_id, "pg_isready", "-U", self.bootstrap, "-d", "postgres", check=False)
            if ready.returncode == 0:
                return
            time.sleep(0.25)
        raise RehearsalFailure("isolated PostgreSQL did not become ready")

    def psql(self, role: str, database: str, sql: str, *, check: bool = True):
        return self.pipe(*PSQL, "-U", role, "-d", database, input_=sql.encode(), check=check)

    def pipe(self, *args: str, input_: bytes | None = None, check: bool = True):
        return self.docker("exec", "-i", self.container_id, *args, input_=input_, check=check)

    def cleanup(self):
        self.deadline = time.monotonic() + 2 * 60
        try:
            if self.container_id is None:
                return
            fmt = '{"Id":{{json .Id}},"Name":{{json .Name}},"Image":{{json .Image}},"Labels":{{json .Config.Labels}}}'
            result = self.docker("inspect", "--format", fmt, self.container_id, check=False)
            if result.returncode:
                raise RehearsalFailure("owned container disappeared before cleanup")
            try:
                item = json.loads(result.stdout)
                labels = item["Labels"]
            except (json.JSONDecodeError, KeyError, TypeError):
                raise RehearsalFailure("owned container cleanup metadata invalid") from None
            if (
                item.get("Id") != self.container_id
                or item.get("Name") != "/" + self.name
                or item.get("Image") != self.image
                or labels.get(OWNER_LABEL) != OWNER
                or labels.get(ATTEMPT_LABEL) != self.attempt
            ):
                raise RehearsalFailure("container ownership changed; cleanup refused")
            self.docker("rm", "-f", self.container_id)
            if not self.docker("inspect", self.container_id, check=False).returncode:
                raise RehearsalFailure("owned container cleanup was not confirmed")
            self.container_id = None
        finally:
            self.scratch.cleanup()
def provision_sql() -> str:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    kinds = ("migrator", "ingest", "notifier", "reader")
    manifest["password_secrets"] = {kind: f"p04_{kind}" for kind in kinds}
    spec = importlib.util.spec_from_file_location("p04_project", PROVISIONER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sql = module.sql_for(manifest)
    for kind in kinds:
        source = f"\\getenv {kind}_password DEV_{kind.upper()}_PASSWORD"
        target = f"\\set {kind}_password 'p04-{kind}-synthetic-only'"
        if sql.count(source) != 1:
            raise RehearsalFailure("provision credential input contract changed")
        sql = sql.replace(source, target)
    return sql
def migration_sql(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return (
        f"\\set migration_sha256 '{digest}'\nSET lock_timeout='5s';"
        f"SET statement_timeout='30s';SET ROLE opsflow_owner;\n{content}"
    )
def publish_sql(source: str, digest: str, captured: str) -> tuple[str, str]:
    run_id = hashlib.sha256(f"{source}:{digest}".encode()).hexdigest()
    row = {"path": "docs/synthetic.md", "revision": "a" * 40,
           "content_sha256": "b" * 64, "title": "Synthetic"}
    rows = json.dumps([row], separators=(",", ":"))
    artifact = f"manifest-validated/{source}/{run_id}.json"
    sql = (
        "SELECT ops_flow.publish_manifest("
        f"'{source}','{run_id}','{digest}','{captured}'::timestamptz,"
        f"$rows${rows}$rows$::jsonb,'{artifact}');"
    )
    return run_id, sql
class OpsflowDatabaseRehearsalBoundaryTests(unittest.TestCase):
    def test_native_selection_is_explicit_and_immutable(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(native_selection())
        with mock.patch.dict(os.environ, {IMAGE_ENV: "postgres:18.6-alpine", CONTEXT_ENV: "default"}, clear=True):
            with self.assertRaises(RehearsalFailure):
                native_selection()
        with self.assertRaisesRegex(RehearsalFailure, "local socket"):
            validate_context({"Name": "default", "DockerHost": "tcp://remote:2376", "SkipTLSVerify": False})
        with mock.patch.dict(os.environ, {IMAGE_ENV: EXPECTED_IMAGE, CONTEXT_ENV: EXPECTED_CONTEXT, "DOCKER_HOST": "tcp://remote"}, clear=True):
            with self.assertRaisesRegex(RehearsalFailure, "overrides"):
                native_selection()
    def test_container_has_no_port_mount_secret_or_network_access(self):
        args = create_argv("sha256:" + "1" * 64, "p04-pg-attempt", Path("/tmp/owned.id"), "attempt", "p04_audit")
        joined = " ".join(args)
        for forbidden in ("--privileged", "--publish", "--volume", "--mount", "--env"):
            self.assertNotIn(forbidden, args)
        self.assertIn("--network none", joined)
        self.assertIn("--read-only", args)
        self.assertEqual(args.count("--tmpfs"), 3)
        self.assertNotIn("password", joined.lower())
        self.assertTrue(MIGRATION_2.is_file())
        sql = provision_sql()
        self.assertNotIn("\\getenv", sql)
        self.assertIn("opsflow_ingest", sql)
    def test_cleanup_refuses_changed_container_identity(self):
        fixture = PgFixture(EXPECTED_IMAGE, EXPECTED_CONTEXT, "p04_audit")
        fixture.container_id = "a" * 64
        payload = b'{"Id":"wrong","Name":"/wrong","Image":"wrong","Labels":{}}'
        fixture.docker = mock.Mock(return_value=subprocess.CompletedProcess([], 0, payload, b""))
        with self.assertRaisesRegex(RehearsalFailure, "ownership changed"):
            fixture.cleanup()
        with mock.patch("subprocess.run", return_value=subprocess.CompletedProcess([], 1, b"secret-out", b"ERROR:  42501: secret-like")), self.assertRaisesRegex(RehearsalFailure, "SQLSTATE 42501") as caught:
            PgFixture.docker(fixture, "exec")
        self.assertNotIn("secret-like", str(caught.exception))
    def test_cleanup_removes_only_the_bound_container(self):
        fixture = PgFixture(EXPECTED_IMAGE, EXPECTED_CONTEXT, "p04_audit")
        fixture.container_id = "a" * 64
        labels = {OWNER_LABEL: OWNER, ATTEMPT_LABEL: fixture.attempt}
        payload = json.dumps({"Id": fixture.container_id, "Name": "/" + fixture.name, "Image": EXPECTED_IMAGE, "Labels": labels}).encode()
        fixture.docker = mock.Mock(side_effect=[subprocess.CompletedProcess([], 0, payload, b""), subprocess.CompletedProcess([], 0, b"", b""), subprocess.CompletedProcess([], 1, b"", b"missing")])
        fixture.cleanup()
        self.assertIsNone(fixture.container_id)
@unittest.skipUnless(native_selection() is not None, "exact isolated PG opt-in required")
class OpsflowDatabaseNativeRehearsal(unittest.TestCase):
    def setUp(self):
        self.fixtures = []
        image, context = native_selection()
        self.receipt = {"case": self._testMethodName, "image_id": image, "context": context, "containers": []}

    def fixture(self, bootstrap):
        image, context = native_selection()
        fixture = PgFixture(image, context, bootstrap)
        self.fixtures.append(fixture)
        record = {"id": None, "attempt": fixture.attempt,
                  "name": fixture.name, "bootstrap": bootstrap}
        self.receipt["containers"].append(record)
        fixture.create()
        record["id"] = fixture.container_id
        return fixture

    def tearDown(self):
        failures = []
        for fixture in reversed(self.fixtures):
            try:
                fixture.cleanup()
            except RehearsalFailure:
                failures.append(fixture.name)
        self.receipt["cleanup"] = "PASS" if not failures else "FAIL"
        print("OPSFLOW_PG_REHEARSAL_RECEIPT " + json.dumps(self.receipt, sort_keys=True))
        if failures:
            raise RehearsalFailure("owned container cleanup failed (details withheld)")

    @staticmethod
    def output(fixture, role, sql, database="opsflow_dev"):
        return fixture.psql(role, database, sql).stdout.strip()

    def ack_all(self, fixture):
        accepted = set()
        claim = "SELECT id||'|'||run_id||'|'||lease_token FROM ops_flow.claim_notification();"
        while receipt := self.output(fixture, "opsflow_notifier", claim):
            outbox_id, run_id, token = receipt.decode().split("|")
            ack = f"SELECT ops_flow.ack_notification({int(outbox_id)},'{token}'::uuid);"
            self.assertEqual(b"t", self.output(fixture, "opsflow_notifier", ack))
            accepted.add(run_id)
        return accepted
    def test_roles_transactions_restore_and_denials(self):
        source = self.fixture("p04_audit")
        inventory = self.output(
            source, "p04_audit",
            "SHOW server_version;SELECT string_agg(extname,',' ORDER BY extname) FROM pg_extension;",
            "postgres",
        ).decode().splitlines()
        self.assertEqual(["18.6", "plpgsql"], inventory)
        self.receipt["postgres"] = {"version": inventory[0], "extensions": inventory[1]}
        source.psql("p04_audit", "postgres", provision_sql())
        source.psql("opsflow_migrator", "opsflow_dev", migration_sql(MIGRATION_1))
        digest1 = hashlib.sha256(MIGRATION_1.read_bytes()).hexdigest()
        checks = f"\\set migration_sha256 '{digest1}'\n{CHECKS.read_text()}"
        source.psql("p04_audit", "opsflow_dev", checks)
        with self.subTest(case="positive_native"):
            first_id, first = publish_sql("hy-home.k8s", "1" * 64, "2026-02-02T00:00:00Z")
            offset_id, offset = publish_sql("hy-home.k8s", "2" * 64, "2026-02-03T00:00:00+01:00")
            red = source.psql("opsflow_ingest", "opsflow_dev", f"BEGIN;{first}{offset}ROLLBACK;")
            if len(red.stdout.decode().splitlines()) != 2:
                raise RehearsalFailure("v1 business-date RED was not reproduced")
            source.psql("opsflow_migrator", "opsflow_dev", migration_sql(MIGRATION_2))
            digest2 = hashlib.sha256(MIGRATION_2.read_bytes()).hexdigest()
            checks2 = f"\\set migration_sha256 '{digest2}'\n{CHECKS.read_text()}"
            source.psql("p04_audit", "opsflow_dev", checks2)
            receipt = "SELECT count(*) FROM ops_flow.schema_version WHERE version=2;SELECT to_regclass('ops_flow.runs_source_business_date_uidx') IS NOT NULL;"
            self.assertEqual(b"1\nt", self.output(source, "p04_audit", receipt))
            self.assertEqual(b"published", self.output(source, "opsflow_ingest", first))
            green = source.psql("opsflow_ingest", "opsflow_dev", offset, check=False)
            if green.returncode == 0 or b"runs_source_business_date_uidx" not in green.stderr:
                raise RehearsalFailure("business-date GREEN denial missing")
            untouched = f"SELECT (SELECT count(*) FROM ops_flow.runs WHERE run_id='{offset_id}')+(SELECT count(*) FROM ops_flow.documents WHERE run_id='{offset_id}')+(SELECT count(*) FROM ops_flow.current_runs WHERE run_id='{offset_id}')+(SELECT count(*) FROM ops_flow.outbox WHERE run_id='{offset_id}');"
            self.assertEqual(b"0", self.output(source, "p04_audit", untouched))
            self.receipt["business_date"] = "RED_V1_GREEN_V2"

            latest_id, latest = publish_sql("hy-home.docker", "3" * 64, "2026-03-03T00:00:00Z")
            self.assertEqual(b"published", self.output(source, "opsflow_ingest", latest))
            self.assertEqual(b"replayed", self.output(source, "opsflow_ingest", latest))
            _, backfill = publish_sql("hy-home.docker", "4" * 64, "2026-03-01T00:00:00Z")
            self.assertEqual(b"historical", self.output(source, "opsflow_ingest", backfill))
            concurrent_id, concurrent_sql = publish_sql("Project-Template", "5" * 64, "2026-03-04T00:00:00Z")
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _: self.output(source, "opsflow_ingest", concurrent_sql), range(2)))
            self.assertEqual([b"published", b"replayed"], sorted(results))
            pointer = "SELECT run_id FROM ops_flow.published_documents WHERE source='hy-home.docker' LIMIT 1;"
            self.assertEqual(latest_id.encode(), self.output(source, "opsflow_reader", pointer))
            self.assertEqual({first_id, latest_id, concurrent_id}, self.ack_all(source))
            for role, sql in (
                ("opsflow_ingest", "UPDATE ops_flow.runs SET status=status;"),
                ("opsflow_notifier", "SELECT count(*) FROM ops_flow.runs;"),
                ("opsflow_reader", concurrent_sql),
            ):
                if source.psql(role, "opsflow_dev", sql, check=False).returncode == 0:
                    raise RehearsalFailure("wrong-role operation was allowed")

            roles = source.pipe(
                "pg_dumpall", "--roles-only", "--no-role-passwords", "-U", "p04_audit"
            ).stdout
            dump = source.pipe(
                "pg_dump", "-Fc", "--create", "-U", "p04_audit", "-d", "opsflow_dev"
            ).stdout
            self.receipt["dump"] = {
                "roles_sha256": hashlib.sha256(roles).hexdigest(),
                "roles_bytes": len(roles),
                "data_sha256": hashlib.sha256(dump).hexdigest(),
                "data_bytes": len(dump),
            }
            restore = self.fixture("p04_restore")
            restore.pipe(*PSQL, "-U", "p04_restore", "-d", "postgres", input_=roles)
            restore.pipe("pg_restore", "--exit-on-error", "--create", "-U", "p04_restore", "-d", "postgres", input_=dump)
            state = "SELECT count(*) FROM ops_flow.published_documents;SELECT count(*)=count(*) FILTER(WHERE state='accepted_by_smtp') FROM ops_flow.delivery_status;"
            restored = self.output(restore, "opsflow_reader", state).decode().splitlines()
            self.assertGreater(int(restored[0]), 0)
            self.assertEqual("t", restored[1])
            count = "SELECT count(*) FROM ops_flow.delivery_status;"
            before = self.output(restore, "opsflow_reader", count)
            self.assertEqual(b"replayed", self.output(restore, "opsflow_ingest", latest))
            self.assertEqual(before, self.output(restore, "opsflow_reader", count))
            self.assertEqual(set(), self.ack_all(restore))
            project_pointer = pointer.replace("hy-home.docker", "Project-Template")
            self.assertEqual(concurrent_id.encode(), self.output(restore, "opsflow_reader", project_pointer))

    def test_cross_database_connect_is_denied(self):
        source = self.fixture("p04_audit")
        source.psql("p04_audit", "postgres", provision_sql())
        result = source.psql("opsflow_ingest", "postgres", "SELECT 1;", check=False)
        self.receipt["cross_database_denial"] = "PASS" if result.returncode else "FAIL_ALLOWED"
        self.assertNotEqual(0, result.returncode)

# fmt: on
