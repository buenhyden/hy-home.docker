#!/usr/bin/env python3
"""Owner-run RUN-0021 step 5a: selected-backup immediate consistency rehearsal.

Restores one verified pgBackRest set of `mng-pg` with `--type=immediate` into a new
scratch PGDATA, starts a network-less clone, and checks that the clone is the same
cluster and is usable. SPEC-0182 W7. Nothing here touches the source database
except read-only catalog queries and `pgbackrest verify`.

Order: refuse bad input (including DOCKER_HOST or a non-default docker context),
read the source container, take the backup scheduler's host lock, `pgbackrest
verify --set` (continue only on rc 0), restore, start the clone, release the lock
once recovery has finished, compare, probe, clean up. `mng-pg` trusts loopback, so
the probe prepends one `scram-sha-256` rule for its one-time role to the restored
clone `pg_hba.conf` only (UID 70 in the clone, then reload and a
`pg_hba_file_rules` check); the source is never touched and the scratch keeps it. The clone mounts the
repository read-only because recovery needs `archive-get` even for `immediate`.
Only containers this run created (name and ID both match) are stopped and removed,
and `removed` is reported only after a by-ID `docker ps -a` shows them absent.
The scratch PGDATA is kept, mode 0700, for the 7-day owner review.

Output is a fixed list of `key=value` lines: no rows, secrets or raw logs.
Exit 0 PASS, 1 FAIL (reason `io_error` for a file or lock OSError), 2 refused
input, 75 backup lock busy.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

SOURCE = "mng-pg"
SOURCE_IMAGE_TAG = "hy-home/mng-pg:18.6-pgbackrest"
STANZA = "mng"
UID = "70"
LABEL_KEY = "hy.rehearsal"
LABEL = f"{LABEL_KEY}=mng-pg-immediate-5a"
REPO_TARGET = "/var/lib/pgbackrest"
SECRET_TARGET = "/run/secrets/pgbackrest_cipher_pass"
DATA_TARGET = "/var/lib/postgresql/data"
HBA_FILE = DATA_TARGET + "/pgdata/pg_hba.conf"
LOCK_NAME = ".hyhome-backup.lock"
PROBE_DB = "app_db"
REQUIRED_DBS = ("app_db", "mlflow")
FORBIDDEN_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")
LABEL_RE = re.compile(r"^\d{8}-\d{6}F(_\d{8}-\d{6}[DI])?$")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
ID_RE = re.compile(r"^[0-9a-f]{64}$")
CAPS = ("CHOWN", "DAC_OVERRIDE", "FOWNER", "SETGID", "SETUID")
FIELDS = (
    "result",
    "reason",
    "verify_rc",
    "restore_rc",
    "elapsed_seconds",
    "system_id_match",
    "db_list_match",
    "app_db_present",
    "mlflow_present",
    "heartbeat_present",
    "dbt_present",
    "count_stable",
    "extension_count",
    "sequence_count",
    "probe_result",
    "clone_hba_probe_rule",
    "scratch_mode_0700",
    "cleanup_status",
)
EXIT = {"PASS": 0, "FAIL": 1, "REFUSED": 2}
VERIFY_TIMEOUT = 900
RESTORE_TIMEOUT = 3600
READY_TIMEOUT = 300
MEMORY = "2g"  # database is about 126 MB; the host has 32 GB
CPUS = "2"


class Refused(Exception):
    """Input refused before anything ran."""


class Stop(Exception):
    """A gate failed; the reason is a fixed token."""


def _run(argv, *, timeout, input=None):
    try:
        done = subprocess.run(
            argv,
            input=None if input is None else input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""
    return done.returncode, done.stdout.decode(errors="replace")


def _ident(value: str, what: str) -> str:
    if not IDENT_RE.fullmatch(value):
        raise Refused(f"{what}_identifier")
    return value


def _dotted(value: str, parts: tuple[int, ...], what: str) -> list[str]:
    names = value.split(".")
    if len(names) not in parts:
        raise Refused(f"{what}_shape")
    return [_ident(name, what) for name in names]


def check_inputs(args, *, forbidden=None) -> Path:
    """Return the resolved scratch root or raise Refused."""
    if not LABEL_RE.fullmatch(args.label):
        raise Refused("label")
    root = Path(args.scratch_root)
    if (
        not root.is_absolute()
        or root.is_symlink()
        or os.path.realpath(root) != str(root)
    ):
        raise Refused("scratch_path")
    for bad in FORBIDDEN_ROOTS if forbidden is None else forbidden:
        if str(root) == bad or str(root).startswith(bad + "/"):
            raise Refused("scratch_forbidden_root")
    if not root.is_dir():
        raise Refused("scratch_missing")
    status = root.stat()
    if status.st_uid != os.getuid() or status.st_mode & 0o077:
        raise Refused("scratch_owner_or_mode")
    if any(root.iterdir()):
        raise Refused("scratch_not_empty")
    if shutil.disk_usage(root).free < args.min_free_gib * 2**30:
        raise Refused("scratch_free_space")
    _dotted(args.heartbeat, (2, 3), "heartbeat")
    _dotted(args.dbt, (2, 3), "dbt")
    if not args.count_table:
        raise Refused("count_table_missing")
    for table in args.count_table:
        _dotted(table, (3,), "count_table")
    return root


def read_source(run) -> dict:
    code, out = run(["docker", "inspect", SOURCE], timeout=60)
    try:
        info = json.loads(out)[0]
        mounts = {m["Destination"]: m for m in info["Mounts"]}
        env = dict(e.partition("=")[::2] for e in info["Config"]["Env"])
        source = {
            "image_id": info["Image"],
            "image_tag": info["Config"]["Image"],
            "running": info["State"]["Running"],
            "admin": env["POSTGRES_USER"],
            "repo": mounts[REPO_TARGET]["Source"],
            "secret": mounts[SECRET_TARGET]["Source"],
        }
    except (ValueError, KeyError, IndexError, TypeError):
        raise Stop("source_inspect") from None
    if code or not source["running"] or source["image_tag"] != SOURCE_IMAGE_TAG:
        raise Stop("source_state")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", source["image_id"]):
        raise Stop("source_image_id")
    _ident(source["admin"], "admin")
    for key in ("repo", "secret"):
        if not os.path.isabs(source[key]) or os.path.islink(source[key]):
            raise Stop("source_mount")
    return source


def _sql(run, container, admin, db, sql, *, timeout=120):
    argv = ["docker", "exec", "-i", "--user", UID, container, "psql", "-X", "-q"]
    argv += ["-At", "-v", "ON_ERROR_STOP=1", "-U", admin, "-d", db]
    code, out = run(argv, timeout=timeout, input=sql)
    return code, out.strip().splitlines()


def _kv(lines) -> dict:
    return dict(line.partition("=")[::2] for line in lines if "=" in line)


class Owned:
    """Containers this run created; removal needs the name and the ID to match."""

    def __init__(self, run):
        self.run, self.items = run, {}

    def create(self, name, argv) -> str:
        code, out = self.run(["docker", "create", f"--name={name}", *argv], timeout=120)
        cid = out.strip()
        if code or not ID_RE.fullmatch(cid):
            raise Stop("docker_create")
        self.items[name] = cid
        return cid

    def running(self, cid) -> bool:
        fmt = "{{.State.Running}}"
        code, out = self.run(["docker", "inspect", "--format", fmt, cid], timeout=30)
        return code == 0 and out.strip() == "true"

    def absent(self, cid) -> bool:
        """True only when `docker ps -a` answers and lists nothing for the ID."""
        argv = ["docker", "ps", "-a", "--no-trunc", f"--filter=id={cid}"]
        code, out = self.run([*argv, "--format", "{{.ID}}"], timeout=30)
        return code == 0 and not out.strip()

    def remove_all(self) -> str:
        if not self.items:
            return "none_created"
        failed = []
        for name, cid in self.items.items():
            code, out = self.run(
                ["docker", "inspect", "--format", "{{.Id}}", name], timeout=30
            )
            if not code and out.strip() != cid:
                failed.append("id_mismatch")
                continue
            # a failed inspect is unknown, not gone: stop and remove by our own ID
            self.run(["docker", "stop", "--time=60", cid], timeout=120)
            self.run(["docker", "rm", "--force", cid], timeout=60)
            if not self.absent(cid):
                failed.append("rm_unconfirmed")
        return "failed:" + ",".join(failed) if failed else "removed"


def _container_argv(source, root: Path, *, command: list[str]) -> list[str]:
    argv = [f"--label={LABEL}", "--network=none", "--pull=never", "--cap-drop=ALL"]
    argv += [f"--memory={MEMORY}", f"--memory-swap={MEMORY}", f"--cpus={CPUS}"]
    argv += [f"--cap-add={cap}" for cap in CAPS]
    argv += ["--security-opt=no-new-privileges", "--pids-limit=512", "--shm-size=256m"]
    argv += ["--env=PGDATA=" + DATA_TARGET + "/pgdata"]
    argv += ["--env=PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d"]
    argv += [f"--mount=type=bind,src={root}/data,dst={DATA_TARGET}"]
    argv += [f"--mount=type=bind,src={source['secret']},dst={SECRET_TARGET},readonly"]
    argv += [f"--mount=type=bind,src={source['repo']},dst={REPO_TARGET},readonly"]
    return [*argv, source["image_id"], *command]


def restore_command(label: str) -> list[str]:
    pgdata = DATA_TARGET + "/pgdata"
    script = (
        f"install -d -o postgres -g postgres -m 0700 {pgdata}; "
        f"chown postgres:postgres {DATA_TARGET}; chmod 0700 {DATA_TARGET}; "
        f"exec gosu postgres pgbackrest --stanza={STANZA} "
        f"--set={shlex.quote(label)} --type=immediate --target-action=promote "
        f"--archive-mode=off --pg1-path={pgdata} restore"
    )
    return ["sh", "-ec", script]


def clone_command() -> list[str]:
    return ["postgres", "-c", "archive_mode=off", "-c", "listen_addresses=127.0.0.1"]


def _probe_sql(role: str, password: str) -> str:
    return (
        "SET password_encryption = 'scram-sha-256';\n"
        "SET log_statement = none;\n"
        "SET log_min_duration_statement = -1;\n"
        "SET log_min_error_statement = panic;\n"
        f"CREATE ROLE \"{role}\" LOGIN PASSWORD '{password}' NOSUPERUSER NOCREATEDB "
        "NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS CONNECTION LIMIT 2;\n"
        f'GRANT CONNECT, TEMP ON DATABASE "{PROBE_DB}" TO "{role}";\n'
    )


def _grant_check_sql(role: str) -> str:
    r = f"'{role}'::regrole"
    priv = " OR ".join(
        f"has_table_privilege({r}, c.oid, '{p}')"
        for p in ("INSERT", "UPDATE", "DELETE", "TRUNCATE")
    )
    return (
        "SELECT 'acl=' || COALESCE(string_agg(a.privilege_type, ',' ORDER BY "
        "a.privilege_type), '') FROM pg_database d CROSS JOIN LATERAL "
        f"aclexplode(d.datacl) a WHERE d.datname = current_database() AND "
        f"a.grantee = {r};\n"
        "SELECT 'other_deps=' || count(*) FROM pg_shdepend WHERE "
        f"refclassid = 'pg_authid'::regclass AND refobjid = {r} AND NOT "
        "(deptype = 'a' AND classid = 'pg_database'::regclass);\n"
        f"SELECT 'members=' || count(*) FROM pg_auth_members WHERE member = {r};\n"
        # PUBLIC holds UPDATE on the pg_settings view by default; that only
        # changes session settings (SET), so it is not a persistent write.
        "SELECT 'table_writes=' || count(*) FROM pg_class c WHERE "
        "c.oid <> 'pg_catalog.pg_settings'::regclass AND ("
        f"(c.relkind IN ('r','p','v','m','f') AND ({priv})) OR "
        f"(c.relkind = 'S' AND has_sequence_privilege({r}, c.oid, 'UPDATE')));\n"
        "SELECT 'schema_create=' || count(*) FROM pg_namespace WHERE "
        f"has_schema_privilege({r}, oid, 'CREATE') AND nspname NOT LIKE 'pg\\_%temp\\_%';\n"
        f"SELECT 'db_create=' || has_database_privilege({r}, current_database(), "
        "'CREATE');\n"
    )


GRANTS_OK = {
    "acl": "CONNECT,TEMPORARY",
    "other_deps": "0",
    "members": "0",
    "table_writes": "0",
    "schema_create": "0",
    "db_create": "false",
}


def _probe_session_sql() -> str:
    return (
        "BEGIN;\n"
        "CREATE TEMP TABLE hy_5a_probe (n int);\n"
        "INSERT INTO hy_5a_probe VALUES (1);\n"
        "SELECT 'rows=' || count(*) FROM hy_5a_probe;\n"
        "SELECT 'tcp=' || (inet_client_addr() IS NOT NULL);\n"
        "ROLLBACK;\n"
        "SELECT 'temp_after=' || count(*) FROM pg_class WHERE relname = 'hy_5a_probe';\n"
    )


def hba_rule(role: str) -> str:
    if not IDENT_RE.fullmatch(role):
        raise Stop("probe_identifier")
    return f"host {PROBE_DB} {role} 127.0.0.1/32 scram-sha-256"


# in place (`cat >`) so the file keeps its inode, mode and owner
HBA_PREPEND = (
    '{ printf "%s\\n" "$2"; cat "$1"; } > "$1.probe"; cat "$1.probe" > "$1"; '
    'rm -f "$1.probe"'
)


def _hba_check_sql(role: str) -> str:
    return (
        "SELECT 'reload=' || pg_reload_conf();\n"
        "SELECT 'rule1=' || concat_ws('|', type, array_to_string(database, ','), "
        "array_to_string(user_name, ','), address, netmask, auth_method, "
        "COALESCE(error, '')) FROM pg_hba_file_rules WHERE rule_number = 1;\n"
        "SELECT 'errors=' || count(*) FROM pg_hba_file_rules WHERE error IS NOT NULL;\n"
    )


def _tcp_psql(run, clone, role, password, sql):
    """Authenticate over TCP; the password travels on stdin, never argv."""
    script = (
        "IFS= read -r PGPASSWORD; export PGPASSWORD; exec psql -X -q -At "
        f"-v ON_ERROR_STOP=1 -h 127.0.0.1 -p 5432 -U {role} -d {PROBE_DB} -f -"
    )
    argv = ["docker", "exec", "-i", "--user", UID, clone, "sh", "-ec", script]
    code, out = run(argv, timeout=120, input=password + "\n" + sql)
    return code, out.strip().splitlines()


def _drop_role_sql(role: str) -> str:
    return (
        "DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = "
        f"'{role}') THEN PERFORM pg_terminate_backend(pid) FROM pg_stat_activity "
        f"WHERE usename = '{role}'; REVOKE ALL ON DATABASE \"{PROBE_DB}\" FROM "
        f'"{role}"; DROP ROLE "{role}"; END IF; END $$;\n'
    )


def add_hba_rule(run, clone, admin, role, state) -> None:
    """Prepend the probe-only rule to the clone's scratch pg_hba.conf, reload, check."""
    rule = hba_rule(role)
    code, lines = _sql(
        run, clone, admin, "postgres", "SELECT 'hba=' || current_setting('hba_file');\n"
    )
    if code or _kv(lines).get("hba") != HBA_FILE:
        raise Stop("probe_hba_path")
    state["clone_hba_probe_rule"] = "unknown"  # the scratch may now be changed
    argv = ["docker", "exec", "--user", UID, clone, "sh", "-ec", HBA_PREPEND]
    code, _ = run([*argv, "sh", HBA_FILE, rule], timeout=60)
    if code:
        raise Stop("probe_hba_write")
    state["clone_hba_probe_rule"] = "added"
    code, lines = _sql(run, clone, admin, "postgres", _hba_check_sql(role))
    rule1 = f"host|{PROBE_DB}|{role}|127.0.0.1|255.255.255.255|scram-sha-256|"
    want = {"reload": "true", "rule1": rule1, "errors": "0"}
    if code or _kv(lines) != want:
        raise Stop("probe_hba_check")


def probe(run, clone, admin, role, state, sleep=time.sleep) -> None:
    hba_rule(role)  # refuse an unsafe role name before anything runs
    password = secrets.token_hex(16)
    code, _ = _sql(run, clone, admin, PROBE_DB, _probe_sql(role, password))
    if code:
        raise Stop("probe_create")
    code, lines = _sql(run, clone, admin, PROBE_DB, _grant_check_sql(role))
    if code:
        raise Stop("probe_privileges")
    got = _kv(lines)
    for key in GRANTS_OK:  # name the first failing fixed check, never its value
        if got.get(key) != GRANTS_OK[key]:
            raise Stop(f"probe_privileges_{key}")
    if set(got) != set(GRANTS_OK):
        raise Stop("probe_privileges")
    add_hba_rule(run, clone, admin, role, state)
    for _ in range(5):  # the reload is asynchronous; fail closed if never refused
        bad, _ = _tcp_psql(run, clone, role, secrets.token_hex(16), "SELECT 1;\n")
        if bad:
            break
        sleep(1)
    else:
        raise Stop("probe_auth_not_enforced")
    code, lines = _tcp_psql(run, clone, role, password, _probe_session_sql())
    if code or _kv(lines) != {"rows": "1", "tcp": "true", "temp_after": "0"}:
        raise Stop("probe_session")
    code, _ = _sql(run, clone, admin, PROBE_DB, _drop_role_sql(role))
    code2, lines = _sql(
        run,
        clone,
        admin,
        PROBE_DB,
        f"SELECT 'role=' || count(*) FROM pg_roles WHERE rolname = '{role}';\n"
        "SELECT 'temp=' || count(*) FROM pg_class WHERE relname = 'hy_5a_probe';\n",
    )
    if code or code2 or _kv(lines) != {"role": "0", "temp": "0"}:
        raise Stop("probe_cleanup")
    state["probe_result"] = "PASS"


def count_stable(run, clone, admin, tables) -> bool:
    by_db: dict[str, list[tuple[str, str]]] = {}
    for table in tables:
        db, schema, name = table.split(".")
        by_db.setdefault(db, []).append((schema, name))
    for db, items in by_db.items():
        body = ["BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;"]
        for tag in ("a", "b"):
            for i, (schema, name) in enumerate(items):
                body.append(
                    f'SELECT \'t{i}{tag}=\' || count(*) FROM "{schema}"."{name}";'
                )
        body.append("COMMIT;")
        code, lines = _sql(run, clone, admin, db, "\n".join(body) + "\n")
        got = _kv(lines)
        if code:
            return False
        for i in range(len(items)):
            first, second = got.get(f"t{i}a", ""), got.get(f"t{i}b", "")
            if not (first.isdigit() and first == second):
                return False
    return True


def object_present(run, clone, admin, dbs, dotted) -> bool:
    names = dotted.split(".")
    if names[0] not in dbs:
        return False
    if len(names) == 2:
        expr = f"to_regnamespace('\"{names[1]}\"') IS NOT NULL"
    else:
        expr = f'to_regclass(\'"{names[1]}"."{names[2]}"\') IS NOT NULL'
    code, lines = _sql(run, clone, admin, names[0], f"SELECT {expr};\n")
    return code == 0 and lines == ["t"]


def inventory(run, clone, admin, dbs, root: Path, state) -> None:
    """Record extension and sequence names as observations, never as a claim."""
    found = {"extensions": [], "sequences": []}
    for db in dbs:
        code, lines = _sql(
            run,
            clone,
            admin,
            db,
            "SELECT 'e=' || extname || ' ' || extversion FROM pg_extension "
            "ORDER BY 1;\nSELECT 's=' || schemaname || '.' || sequencename FROM "
            "pg_sequences ORDER BY 1;\n",
        )
        if code:
            continue
        for line in lines:
            kind = "extensions" if line.startswith("e=") else "sequences"
            found[kind].append(f"{db}: {line[2:]}")
    state["extension_count"] = len(found["extensions"])
    state["sequence_count"] = len(found["sequences"])
    note = root / "inventory-observations.json"
    note.write_text(json.dumps(found, indent=2) + "\n")
    note.chmod(0o600)


def wait_ready(run, owned, cid, clone, admin, *, sleep, clock) -> None:
    started = clock()
    while clock() - started < READY_TIMEOUT:
        code, lines = _sql(
            run, clone, admin, "postgres", "SELECT pg_is_in_recovery();\n", timeout=30
        )
        if code == 0 and lines == ["f"]:
            return
        if not owned.running(cid):
            raise Stop("clone_exited")
        sleep(3)
    raise Stop("clone_ready_timeout")


_IDENTITY_SQL = (
    "SELECT 'sysid=' || system_identifier FROM pg_control_system();\n"
    "SELECT 'dbs=' || string_agg(datname, ',' ORDER BY datname) FROM pg_database "
    "WHERE NOT datistemplate;\n"
)


def check_docker_target(run, env) -> None:
    """Refuse a remote or non-default Docker target; bind mounts must be local."""
    if env.get("DOCKER_HOST"):
        raise Refused("docker_host_set")
    code, out = run(["docker", "context", "show"], timeout=30)
    if code or out.strip() != "default":
        raise Refused("docker_context")


def _release(lock) -> None:
    try:
        fcntl.flock(lock, fcntl.LOCK_UN)
    except OSError:
        pass  # closing the descriptor drops the lock either way
    finally:
        lock.close()


def rehearse(
    args, *, run=_run, sleep=time.sleep, clock=time.monotonic, env=os.environ
) -> dict:
    try:
        root = check_inputs(args)
    except OSError:
        raise Refused("scratch_io") from None
    check_docker_target(run, env)
    state = dict.fromkeys(FIELDS, "NOT_RUN")
    state.update(result="FAIL", reason="none", cleanup_status="none_created")
    started = clock()
    owned = Owned(run)
    lock = None
    role = "hy_5a_probe_" + uuid.uuid4().hex[:8]
    suffix = uuid.uuid4().hex[:12]
    clone, admin = f"hyhome-5a-clone-{suffix}", None
    try:
        source = read_source(run)
        admin = source["admin"]
        lock_path = Path(source["repo"]).parent / LOCK_NAME
        if lock_path.is_symlink() or not lock_path.parent.is_dir():
            raise Stop("lock_path")
        lock = open(lock_path, "a")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Stop("lock_busy") from None
        code, out = run(
            [
                "docker",
                "exec",
                "--user",
                UID,
                SOURCE,
                "pgbackrest",
                f"--stanza={STANZA}",
                "verify",
                f"--set={args.label}",
            ],
            timeout=VERIFY_TIMEOUT,
        )
        state["verify_rc"] = code
        if code:
            raise Stop("verify")
        code, lines = _sql(run, SOURCE, admin, "postgres", _IDENTITY_SQL, timeout=60)
        source_id = _kv(lines)
        if code or not source_id.get("sysid"):
            raise Stop("source_query")
        (root / "data").mkdir(mode=0o700)
        cid = owned.create(
            f"hyhome-5a-restore-{suffix}",
            _container_argv(source, root, command=restore_command(args.label)),
        )
        code, _ = run(["docker", "start", cid], timeout=60)
        if code:
            state["restore_rc"] = code
            raise Stop("restore_start")
        code, out = run(["docker", "wait", cid], timeout=RESTORE_TIMEOUT)
        state["restore_rc"] = (
            int(out.strip()) if out.strip().lstrip("-").isdigit() else 1
        )
        if code or state["restore_rc"]:
            raise Stop("restore")
        cid = owned.create(
            clone, _container_argv(source, root, command=clone_command())
        )
        if run(["docker", "start", cid], timeout=60)[0]:
            raise Stop("clone_start")
        wait_ready(run, owned, cid, clone, admin, sleep=sleep, clock=clock)
        _release(lock)
        lock = None
        code, lines = _sql(run, clone, admin, "postgres", _IDENTITY_SQL, timeout=60)
        clone_id = _kv(lines)
        state["system_id_match"] = (
            code == 0 and clone_id.get("sysid") == source_id["sysid"]
        )
        state["db_list_match"] = code == 0 and clone_id.get("dbs") == source_id["dbs"]
        if not (state["system_id_match"] and state["db_list_match"]):
            raise Stop("identity_mismatch")
        dbs = clone_id["dbs"].split(",")
        state["app_db_present"] = "app_db" in dbs
        state["mlflow_present"] = "mlflow" in dbs
        state["heartbeat_present"] = object_present(
            run, clone, admin, dbs, args.heartbeat
        )
        state["dbt_present"] = object_present(run, clone, admin, dbs, args.dbt)
        wanted = (
            "app_db_present",
            "mlflow_present",
            "heartbeat_present",
            "dbt_present",
        )
        if not all(state[key] is True for key in wanted):
            raise Stop("required_object_missing")
        state["count_stable"] = count_stable(run, clone, admin, args.count_table)
        if not state["count_stable"]:
            raise Stop("count_unstable")
        inventory(run, clone, admin, dbs, root, state)
        state["probe_result"] = "FAIL"
        probe(run, clone, admin, role, state, sleep)
        state["result"] = "PASS"
    except Stop as stop:
        state["reason"] = str(stop)
    except OSError:
        state["reason"] = "io_error"
    finally:
        if lock is not None:
            _release(lock)
        if admin and owned.items.get(clone):
            _sql(run, clone, admin, PROBE_DB, _drop_role_sql(role), timeout=60)
        state["cleanup_status"] = owned.remove_all()
        data = root / "data"
        try:
            mode = data.stat().st_mode
            state["scratch_mode_0700"] = data.is_dir() and (mode & 0o777) == 0o700
        except OSError:
            state["scratch_mode_0700"] = False
        state["elapsed_seconds"] = round(clock() - started, 1)
    if state["cleanup_status"] not in ("removed", "none_created"):
        state["result"] = "FAIL"
    return state


def render(state: dict) -> str:
    def text(value):
        return str(value).lower() if isinstance(value, bool) else str(value)

    return "".join(f"{key}={text(state[key])}\n" for key in FIELDS)


def main(argv=None, **kwargs) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True, help="verified backup set label")
    parser.add_argument("--scratch-root", required=True, type=Path)
    parser.add_argument("--heartbeat", required=True, help="DB.SCHEMA[.RELATION]")
    parser.add_argument("--dbt", required=True, help="DB.SCHEMA[.RELATION]")
    parser.add_argument("--count-table", action="append", help="DB.SCHEMA.TABLE")
    parser.add_argument("--min-free-gib", type=int, default=20)
    args = parser.parse_args(argv)
    try:
        state = rehearse(args, **kwargs)
    except Refused as refused:
        state = dict.fromkeys(FIELDS, "NOT_RUN")
        state.update(
            result="REFUSED", reason=str(refused), cleanup_status="none_created"
        )
    sys.stdout.write(render(state))
    if state["reason"] == "lock_busy":
        return 75
    return EXIT[state["result"]]


if __name__ == "__main__":
    sys.exit(main())
