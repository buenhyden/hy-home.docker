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
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

# fmt: off

ROOT = Path(__file__).resolve().parents[2]
WORKLOAD = ROOT / "infra/07-workflow/airflow/workloads/manifest-pipeline"
PROVISIONER = ROOT / "infra/04-data/dev-db/pg/provision/project.py"
CLUSTER_CONNECT = PROVISIONER.parent / "cluster-connect.sql"
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
RESTORE_ERROR = re.compile(rb"psql:<stdin>:(\d+): ERROR:\s+([0-9A-Z]{5}):")
SCHEMA_DRIFT_ERROR = re.compile(rb"ERROR:\s+P0001:\s+schema_drift(?:\r?\n|$)")
ROLE_NAMES = ("p04_audit", "opsflow_owner", "opsflow_migrator", "opsflow_ingest", "opsflow_notifier", "opsflow_reader")


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
def monitor_sql() -> str:
    sys.path.insert(0, str(PROVISIONER.parent))
    try:
        spec = importlib.util.spec_from_file_location("p04_monitor", PROVISIONER.parent / "monitor.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.sql().replace("\\getenv monitor_secret DEV_MONITOR_PASSWORD", "\\set monitor_secret 'AAAAAAAAAAAAAAAAAAAAAAAA'")
    finally:
        sys.path.remove(str(PROVISIONER.parent))

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
def roles_restore_error_is_expected(roles: bytes, stderr: bytes, returncode: int) -> bool:
    errors = [(int(line), code) for line, code in RESTORE_ERROR.findall(stderr)]
    if returncode or stderr.count(b"ERROR:") != 1 or b"FATAL:" in stderr or b"PANIC:" in stderr:
        return False
    if len(errors) != 1 or errors[0][1] != b"42710":
        return False
    line = errors[0][0]
    statements = roles.splitlines()
    return 0 < line <= len(statements) and statements[line - 1].strip() == b"CREATE ROLE p04_audit;"
def execution_identity(fixture: PgFixture) -> str:
    uid = fixture.pipe("id", "-u").stdout.strip()
    gid = fixture.pipe("id", "-g").stdout.strip()
    if not re.fullmatch(rb"(?:0|[1-9][0-9]*)", uid) or not re.fullmatch(rb"(?:0|[1-9][0-9]*)", gid):
        raise RehearsalFailure("execution identity shape rejected")
    return f"{uid.decode()}:{gid.decode()}"
def role_state(fixture: PgFixture) -> bytes:
    quoted = ",".join(f"'{role}'" for role in ROLE_NAMES)
    sql = (
        "SELECT rolname::text||'|'||rolsuper::int::text||'|'||rolinherit::int::text||'|'||"
        "rolcreaterole::int::text||'|'||rolcreatedb::int::text||'|'||rolcanlogin::int::text||'|'||"
        "rolreplication::int::text||'|'||rolbypassrls::int::text||'|'||rolconnlimit::text "
        f"FROM pg_roles WHERE rolname=ANY(ARRAY[{quoted}]) ORDER BY rolname;"
        "SELECT grantor.rolname::text||'|'||m.admin_option::int::text||'|'||"
        "m.inherit_option::int::text||'|'||m.set_option::int::text FROM pg_auth_members m "
        "JOIN pg_roles granted ON granted.oid=m.roleid JOIN pg_roles member ON member.oid=m.member "
        "JOIN pg_roles grantor ON grantor.oid=m.grantor WHERE granted.rolname='opsflow_owner' "
        "AND member.rolname='opsflow_migrator';"
    )
    value = fixture.psql("p04_audit", "postgres", sql).stdout.strip()
    lines = value.splitlines()
    inventory = lines[: len(ROLE_NAMES)]
    pattern = rb"([a-z0-9_]+)(?:\|[01]){7}\|-?[0-9]+"
    matches = [re.fullmatch(pattern, line) for line in inventory]
    if len(lines) != len(ROLE_NAMES) + 1 or any(match is None for match in matches):
        raise RehearsalFailure("role inventory shape rejected")
    if [match[1].decode() for match in matches] != sorted(ROLE_NAMES):
        raise RehearsalFailure("role inventory names rejected")
    if lines[-1] != b"p04_audit|0|0|1":
        raise RehearsalFailure("role membership contract rejected")
    return value
def restored_schema_preflight(content: str, migration_digest: str) -> str:
    boundary = "\n IF EXISTS(SELECT 1 FROM ops_flow.runs)"
    if content.count(boundary) != 1:
        raise RehearsalFailure("restored schema preflight boundary changed")
    readonly, _ = content.split(boundary, 1)
    return f"\\set migration_sha256 '{migration_digest}'\n{readonly}\nEND $acl$;\nROLLBACK;\n"
def restored_acl_drift_probes(preflight: str):
    marker = "SET LOCAL ROLE opsflow_owner;\nDO $acl$"
    if preflight.count(marker) != 1:
        raise RehearsalFailure("restored ACL probe boundary changed")
    statements = (
        "GRANT SELECT ON ops_flow.runs TO opsflow_reader;",
        "REVOKE ALL ON ops_flow.runs FROM opsflow_owner;",
    )
    return tuple(preflight.replace(marker, f"SET LOCAL ROLE opsflow_owner;\n{statement}\nDO $acl$") for statement in statements)
def psql_error_is_expected(result: subprocess.CompletedProcess, sqlstate: str) -> bool:
    diagnostic = psql_diagnostic(result.stderr)
    return (
        result.returncode == 3
        and result.stderr.count(b"ERROR:") == 1
        and b"FATAL:" not in result.stderr
        and b"PANIC:" not in result.stderr
        and diagnostic is not None
        and diagnostic["sqlstate"] == sqlstate
    )
def schema_drift_is_expected(result: subprocess.CompletedProcess) -> bool:
    return (
        psql_error_is_expected(result, "P0001")
        and len(SCHEMA_DRIFT_ERROR.findall(result.stderr)) == 1
    )
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
    def test_roles_restore_allows_only_the_bootstrap_duplicate(self):
        roles = b"CREATE ROLE p04_audit;\nCREATE ROLE opsflow_owner;\n"
        expected = b"psql:<stdin>:1: ERROR:  42710: withheld\n"
        self.assertTrue(roles_restore_error_is_expected(roles, expected, 0))
        for stderr, returncode in (
            (expected + b"ERROR:  XX000: extra\n", 0),
            (expected + b"FATAL:  XX000: extra\n", 0),
            (b"psql:<stdin>:2: ERROR:  42710: withheld\n", 0),
            (expected, 1),
        ):
            self.assertFalse(roles_restore_error_is_expected(roles, stderr, returncode))
    def test_restored_schema_preflight_stops_before_workload_checks(self):
        content = CHECKS.read_text()
        preflight = restored_schema_preflight(content, "a" * 64)
        self.assertIn("schema_drift", preflight)
        self.assertIn("unsafe_postflight_roles", preflight)
        self.assertNotIn("IF EXISTS(SELECT 1 FROM ops_flow.runs)", preflight)
        self.assertNotIn("CREATE TEMP TABLE p04_case", preflight)
        self.assertTrue(preflight.endswith("END $acl$;\nROLLBACK;\n"))
        boundary = "\n IF EXISTS(SELECT 1 FROM ops_flow.runs)"
        for changed in (content.replace(boundary, ""), content.replace(boundary, boundary * 2)):
            with self.assertRaisesRegex(RehearsalFailure, "boundary changed"):
                restored_schema_preflight(changed, "a" * 64)
    def test_restored_acl_drift_probes_are_exact_and_fail_closed(self):
        preflight = restored_schema_preflight(CHECKS.read_text(), "a" * 64)
        probes = restored_acl_drift_probes(preflight)
        self.assertEqual(2, len(probes))
        for probe, statement in zip(probes, ("GRANT SELECT ON ops_flow.runs TO opsflow_reader;", "REVOKE ALL ON ops_flow.runs FROM opsflow_owner;"), strict=True):
            self.assertEqual(1, probe.count(statement))
            self.assertLess(probe.index(statement), probe.index("DO $acl$"))
        with self.assertRaisesRegex(RehearsalFailure, "probe boundary changed"):
            restored_acl_drift_probes(preflight.replace("DO $acl$", "DO $changed$"))
        expected = subprocess.CompletedProcess([], 3, b"", b"ERROR:  P0001: schema_drift\n")
        self.assertTrue(schema_drift_is_expected(expected))
        for changed in (
            subprocess.CompletedProcess([], 0, b"", expected.stderr),
            subprocess.CompletedProcess([], 1, b"", expected.stderr),
            subprocess.CompletedProcess([], 2, b"", expected.stderr),
            subprocess.CompletedProcess([], 3, b"", b"ERROR:  P0001: owner_mismatch\n"),
            subprocess.CompletedProcess([], 3, b"", b"ERROR:  42501: permission denied\n"),
            subprocess.CompletedProcess([], 3, b"", expected.stderr + b"ERROR:  XX000: extra\n"),
        ):
            self.assertFalse(schema_drift_is_expected(changed))
        reader = subprocess.CompletedProcess([], 3, b"", b"ERROR:  42501: permission denied for table runs\n")
        self.assertTrue(psql_error_is_expected(reader, "42501"))
        for returncode in (0, 1, 2):
            self.assertFalse(psql_error_is_expected(subprocess.CompletedProcess([], returncode, b"", reader.stderr), "42501"))
        self.assertFalse(psql_error_is_expected(expected, "42501"))
@unittest.skipUnless(native_selection() is not None, "exact isolated PG opt-in required")
class OpsflowDatabaseNativeRehearsal(unittest.TestCase):
    def setUp(self):
        self.fixtures = []
        image, context = native_selection()
        self.receipt = {"case": self._testMethodName, "image_id": image, "context": context, "containers": []}

    def fixture(self, bootstrap, *, reviewed_cluster=True):
        image, context = native_selection()
        fixture = PgFixture(image, context, bootstrap)
        self.fixtures.append(fixture)
        record = {"id": None, "attempt": fixture.attempt,
                  "name": fixture.name, "bootstrap": bootstrap}
        self.receipt["containers"].append(record)
        fixture.create()
        record["id"] = fixture.container_id
        if reviewed_cluster:
            self.cluster_connect(fixture)
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
    def cluster_connect(fixture):
        fixture.psql("p04_audit", "postgres", "\\set reviewed_connect_consumers 'reviewed'\n" + CLUSTER_CONNECT.read_text())

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
        self.receipt["execution_identity"] = {"source": execution_identity(source)}
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
            expected_role_state = role_state(source)
            dump = source.pipe(
                "pg_dump", "-Fc", "--create", "-U", "p04_audit", "-d", "opsflow_dev"
            ).stdout
            self.receipt["dump"] = {
                "roles_sha256": hashlib.sha256(roles).hexdigest(),
                "roles_bytes": len(roles),
                "data_sha256": hashlib.sha256(dump).hexdigest(),
                "data_bytes": len(dump),
            }
            restore = self.fixture("p04_audit")
            self.receipt["execution_identity"]["restore"] = execution_identity(restore)
            roles_result = restore.pipe(
                "psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=0", "-v", "VERBOSITY=verbose",
                "-U", "p04_audit", "-d", "postgres", "-f", "-", input_=roles, check=False,
            )
            if not roles_restore_error_is_expected(roles, roles_result.stderr, roles_result.returncode):
                raise RehearsalFailure("roles restore errors rejected")
            if role_state(restore) != expected_role_state:
                raise RehearsalFailure("restored role state changed")
            self.receipt["roles_restore"] = "PASS"
            restore.pipe("pg_restore", "--exit-on-error", "--create", "-U", "p04_audit", "-d", "postgres", input_=dump)
            restored_preflight = restored_schema_preflight(CHECKS.read_text(), digest2)
            restore.psql("p04_audit", "opsflow_dev", restored_preflight)
            self.receipt["restored_schema_preflight"] = "RESTORED_SCHEMA_PREFLIGHT"
            for probe in restored_acl_drift_probes(restored_preflight):
                if not schema_drift_is_expected(
                    restore.psql("p04_audit", "opsflow_dev", probe, check=False)
                ):
                    raise RehearsalFailure("restored ACL drift denial missing")
            reader_denial = restore.psql(
                "opsflow_reader", "opsflow_dev", "SELECT count(*) FROM ops_flow.runs;", check=False
            )
            if not psql_error_is_expected(reader_denial, "42501"):
                raise RehearsalFailure("restored reader denial missing")
            restore.psql("p04_audit", "opsflow_dev", restored_preflight)
            self.receipt["restored_acl_drift_denials"] = "PASS"
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

    def test_v2_unknown_retry_migrates_to_quarantine(self):
        source = self.fixture("p04_audit")
        source.psql("p04_audit", "postgres", provision_sql())
        for path in (MIGRATION_1, MIGRATION_2):
            source.psql("opsflow_migrator", "opsflow_dev", migration_sql(path))
        _, publication = publish_sql("hy-home.k8s", "7" * 64, "2026-04-02T00:00:00Z")
        self.assertEqual(b"published", self.output(source, "opsflow_ingest", publication))
        claim = "SELECT id||'|'||lease_token FROM ops_flow.claim_notification();"
        row = self.output(source, "opsflow_notifier", claim).decode().split("|")
        legacy_retry = f"SELECT ops_flow.retry_notification({int(row[0])},'{row[1]}'::uuid);"
        self.assertEqual(b"t", self.output(source, "opsflow_notifier", legacy_retry))
        source.psql("p04_audit", "opsflow_dev", "UPDATE ops_flow.outbox SET next_attempt_at=clock_timestamp()-interval '1 second';")
        source.psql("opsflow_migrator", "opsflow_dev", migration_sql(WORKLOAD / "sql/004_notification_quarantine.sql"))
        self.assertEqual(b"unknown", self.output(source, "opsflow_reader", "SELECT state FROM ops_flow.delivery_status;"))
        self.assertEqual(b"", self.output(source, "opsflow_notifier", claim))
        self.receipt["legacy_v2_retry_quarantined"] = "PASS"

    def test_notification_unknown_expiry_reconciliation_and_restore(self):
        source = self.fixture("p04_audit")
        source.psql("p04_audit", "postgres", provision_sql())
        for path in (MIGRATION_1, MIGRATION_2, WORKLOAD / "sql/004_notification_quarantine.sql"):
            source.psql("opsflow_migrator", "opsflow_dev", migration_sql(path))
        _, publication = publish_sql("hy-home.docker", "6" * 64, "2026-04-01T00:00:00Z")
        self.assertEqual(b"published", self.output(source, "opsflow_ingest", publication))
        claim = "SELECT id||'|'||lease_token FROM ops_flow.claim_notification();"
        row = self.output(source, "opsflow_notifier", claim).decode().split("|")
        outbox_id, token = int(row[0]), row[1]
        unknown = f"SELECT ops_flow.unknown_notification({outbox_id},'{token}'::uuid);"
        legacy = f"SELECT ops_flow.retry_notification({outbox_id},'{token}'::uuid);"
        self.assertEqual(b"t", self.output(source, "opsflow_notifier", legacy))
        self.assertEqual(b"", self.output(source, "opsflow_notifier", claim))
        self.assertEqual(b"unknown", self.output(source, "opsflow_reader", "SELECT state FROM ops_flow.delivery_status;"))
        rejected = source.psql("opsflow_notifier", "opsflow_dev", f"SELECT ops_flow.reconcile_notification({outbox_id},'not_sent','{'a' * 64}');", check=False)
        self.assertNotEqual(0, rejected.returncode)
        reconcile = f"SELECT ops_flow.reconcile_notification({outbox_id},'not_sent','{'a' * 64}');"
        self.assertEqual(b"t", self.output(source, "opsflow_migrator", "SET ROLE opsflow_owner;" + reconcile))
        row = self.output(source, "opsflow_notifier", claim).decode().split("|")
        new_token = row[1]
        self.assertNotEqual(token, new_token)
        self.assertEqual(b"f", self.output(source, "opsflow_notifier", unknown))
        event = f"SELECT evidence_sha256 FROM ops_flow.notification_reconciliations WHERE outbox_id={outbox_id} AND attempt=1;"
        self.assertEqual(b"a" * 64, self.output(source, "p04_audit", event))
        for statement in ("INSERT INTO ops_flow.notification_reconciliations VALUES (1,1,'not_sent','" + "a" * 64 + "',clock_timestamp());", "UPDATE ops_flow.notification_reconciliations SET result='not_sent';", "DELETE FROM ops_flow.notification_reconciliations;"):
            denied = source.psql("opsflow_notifier", "opsflow_dev", statement, check=False)
            self.assertTrue(psql_error_is_expected(denied, "42501"))
        source.psql("p04_audit", "opsflow_dev", f"UPDATE ops_flow.outbox SET lease_until=clock_timestamp()-interval '1 second' WHERE id={outbox_id};")
        self.assertEqual(b"f", self.output(source, "opsflow_notifier", f"SELECT ops_flow.ack_notification({outbox_id},'{new_token}'::uuid);"))
        self.assertEqual(b"", self.output(source, "opsflow_notifier", claim))
        self.assertEqual(b"unknown", self.output(source, "opsflow_reader", "SELECT state FROM ops_flow.delivery_status;"))
        # A simulated capture acceptance plus lost DB ack remains quarantined after dump/restore.
        roles = source.pipe("pg_dumpall", "--roles-only", "--no-role-passwords", "-U", "p04_audit").stdout
        dump = source.pipe("pg_dump", "-Fc", "--create", "-U", "p04_audit", "-d", "opsflow_dev").stdout
        restore = self.fixture("p04_audit")
        restored_roles = restore.pipe("psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=0", "-v", "VERBOSITY=verbose", "-U", "p04_audit", "-d", "postgres", "-f", "-", input_=roles, check=False)
        self.assertTrue(roles_restore_error_is_expected(roles, restored_roles.stderr, restored_roles.returncode))
        restore.pipe("pg_restore", "--exit-on-error", "--create", "-U", "p04_audit", "-d", "postgres", input_=dump)
        self.assertEqual(b"", self.output(restore, "opsflow_notifier", claim))
        self.assertEqual(b"a" * 64, self.output(restore, "p04_audit", event))
        accepted = f"SELECT ops_flow.reconcile_notification({outbox_id},'accepted_by_smtp','{'b' * 64}');"
        self.assertEqual(b"t", self.output(restore, "opsflow_migrator", "SET ROLE opsflow_owner;" + accepted))
        self.assertEqual(b"", self.output(restore, "opsflow_notifier", claim))
        self.assertEqual(b"accepted_by_smtp", self.output(restore, "opsflow_reader", "SELECT state FROM ops_flow.delivery_status;"))
        self.assertEqual(b"2", self.output(restore, "p04_audit", f"SELECT count(*) FROM ops_flow.notification_reconciliations WHERE outbox_id={outbox_id};"))
        self.assertEqual(b"a" * 64, self.output(restore, "p04_audit", event))
        _, next_publication = publish_sql("hy-home.k8s", "8" * 64, "2026-04-03T00:00:00Z")
        self.assertEqual(b"published", self.output(restore, "opsflow_ingest", next_publication))
        next_id, next_token = self.output(restore, "opsflow_notifier", claim).decode().split("|")
        self.assertEqual(b"t", self.output(restore, "opsflow_notifier", f"SELECT ops_flow.unknown_notification({int(next_id)},'{next_token}'::uuid);"))
        self.assertEqual(b"t", self.output(restore, "opsflow_migrator", f"SET ROLE opsflow_owner;SELECT ops_flow.reconcile_notification({int(next_id)},'not_sent','{'c' * 64}');"))
        retry_id, retry_token = self.output(restore, "opsflow_notifier", claim).decode().split("|")
        self.assertEqual(next_id, retry_id)
        self.assertEqual(b"t", self.output(restore, "opsflow_notifier", f"SELECT ops_flow.ack_notification({int(retry_id)},'{retry_token}'::uuid);"))
        self.assertEqual(b"c" * 64, self.output(restore, "p04_audit", f"SELECT evidence_sha256 FROM ops_flow.notification_reconciliations WHERE outbox_id={int(next_id)} AND attempt=1;"))
        self.receipt["reconciliation_history_restore"] = "PASS"
        self.receipt["quarantine_expiry_ack_loss_restore"] = "PASS"

    def test_monitor_admission_requires_reviewed_cluster_before_login(self):
        source = self.fixture("p04_audit", reviewed_cluster=False)
        blocked = source.psql("p04_audit", "postgres", monitor_sql(), check=False)
        self.assertNotEqual(0, blocked.returncode)
        self.assertIn(b"monitor_cross_database_connect_requires_cluster_review", blocked.stderr)
        self.assertEqual(b"f", self.output(source, "p04_audit", "SELECT rolcanlogin FROM pg_roles WHERE rolname='dev_pg_monitor';", "postgres"))
        self.cluster_connect(source)
        source.psql("p04_audit", "postgres", monitor_sql())
        self.assertEqual(b"1", self.output(source, "dev_pg_monitor", "SELECT 1;", "postgres"))
        self.assertEqual(2, source.psql("dev_pg_monitor", "template1", "SELECT 1;", check=False).returncode)
        self.receipt["monitor_cluster_admission"] = "PASS"

    def test_cross_database_connect_is_denied(self):
        source = self.fixture("p04_audit")
        source.psql("p04_audit", "postgres", provision_sql())
        for role in ("opsflow_migrator", "opsflow_ingest", "opsflow_notifier", "opsflow_reader"):
            for database in ("postgres", "template1"):
                result = source.psql(role, database, "SELECT 1;", check=False)
                self.assertEqual(2, result.returncode, (role, database))
                self.assertIn(f'FATAL:  permission denied for database "{database}"'.encode(), result.stderr)
                effective = f"SELECT has_database_privilege('{role}','{database}','CONNECT');"
                self.assertEqual(b"f", self.output(source, "p04_audit", effective, "postgres"))
            self.assertEqual(b"1", self.output(source, role, "SELECT 1;"))
        self.receipt["cross_database_denial"] = "PASS"

    def test_cross_database_admission_precedes_login_and_preserves_explicit_grants(self):
        source = self.fixture("p04_audit", reviewed_cluster=False)
        rejected = source.psql("p04_audit", "postgres", provision_sql(), check=False)
        self.assertNotEqual(0, rejected.returncode)
        self.assertIn(b"cross_database_connect_requires_cluster_review", rejected.stderr)
        self.assertEqual(b"0\n0", self.output(source, "p04_audit", "SELECT count(*) FROM pg_roles WHERE rolname LIKE 'opsflow_%' AND rolcanlogin;SELECT count(*) FROM pg_database WHERE datname='opsflow_dev';", "postgres"))
        source.psql("p04_audit", "postgres", "CREATE ROLE third_party LOGIN;GRANT CONNECT ON DATABASE postgres TO third_party;CREATE ROLE dev_pg_monitor LOGIN;COMMENT ON ROLE dev_pg_monitor IS 'dev-pg:development:monitor';")
        self.cluster_connect(source)
        self.cluster_connect(source)
        self.assertEqual(b"1", self.output(source, "third_party", "SELECT 1;", "postgres"))
        self.assertEqual(b"1", self.output(source, "dev_pg_monitor", "SELECT 1;", "postgres"))
        self.assertEqual(2, source.psql("dev_pg_monitor", "template1", "SELECT 1;", check=False).returncode)
        for grant, revoke in (
            ("GRANT CONNECT ON DATABASE postgres TO opsflow_ingest;", "REVOKE CONNECT ON DATABASE postgres FROM opsflow_ingest;"),
            ("CREATE ROLE other_reader;GRANT CONNECT ON DATABASE postgres TO other_reader;GRANT other_reader TO opsflow_ingest;", "REVOKE other_reader FROM opsflow_ingest;"),
        ):
            source.psql("p04_audit", "postgres", grant)
            denied = source.psql("p04_audit", "postgres", provision_sql(), check=False)
            self.assertNotEqual(0, denied.returncode)
            self.assertEqual(b"0\n0", self.output(source, "p04_audit", "SELECT count(*) FROM pg_roles WHERE rolname LIKE 'opsflow_%' AND rolcanlogin;SELECT count(*) FROM pg_database WHERE datname='opsflow_dev';", "postgres"))
            source.psql("p04_audit", "postgres", revoke)
        source.psql("p04_audit", "postgres", provision_sql())
        self.receipt["public_direct_inherited_admission"] = "PASS"

# fmt: on
