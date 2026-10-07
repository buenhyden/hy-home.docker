#!/usr/bin/env python3
"""Validate an approved dev-pg project manifest, then provision it with psql.

No database is created by the dev-pg server's first-boot entrypoint. This job
runs only when selected by an explicit profile and manifest. Existing role and
database comments bind names to a project; a rerun never rotates passwords.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

IDENT = re.compile(r"[a-z_][a-z0-9_]{0,62}\Z")
PROJECT_ID = re.compile(r"[a-z][a-z0-9-]{0,62}\Z")
SECRET = re.compile(r"[a-z][a-z0-9_]{0,90}\Z")
KINDS = ("owner", "migrator", "runtime", "reader")
LOGIN_KINDS = KINDS[1:]
# Per-role connection budgets inside dev-pg max_connections=100.
CONNECTION_LIMITS = {"migrator": 2, "runtime": 10, "reader": 5}
FIELDS = {
    "schema_version",
    "project_id",
    "environment",
    "database",
    "schema",
    "roles",
    "password_secrets",
}


def _keys(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f"{label} fields do not match schema")


def _name(value, pattern, label):
    if (
        not isinstance(value, str)
        or not pattern.fullmatch(value)
        or value.startswith("pg_")
    ):
        raise ValueError(f"invalid {label}")
    return value


def validate(value):
    """Return a fresh validated manifest or fail before reading secrets/connecting."""
    _keys(value, FIELDS, "manifest")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported manifest schema")
    if value["environment"] != "development":
        raise ValueError("dev-pg only accepts the development environment")
    project = _name(value["project_id"], PROJECT_ID, "project_id")
    database = _name(value["database"], IDENT, "database")
    schema = _name(value["schema"], IDENT, "schema")
    if database in {"postgres", "template0", "template1", "app_db"} or schema in {
        "public",
        "pg_catalog",
        "information_schema",
    }:
        raise ValueError("reserved database or schema")
    _keys(value["roles"], KINDS, "roles")
    roles = {kind: _name(value["roles"][kind], IDENT, kind) for kind in KINDS}
    if len(set(roles.values())) != len(KINDS) or set(roles.values()) & {
        database,
        schema,
        "postgres",
    }:
        raise ValueError("roles must be distinct from each other and reserved names")
    _keys(value["password_secrets"], LOGIN_KINDS, "password_secrets")
    secrets = {
        kind: _name(value["password_secrets"][kind], SECRET, kind + " secret")
        for kind in LOGIN_KINDS
    }
    if len(set(secrets.values())) != len(LOGIN_KINDS):
        raise ValueError("login roles need distinct secret references")
    return {
        "project_id": project,
        "environment": "development",
        "database": database,
        "schema": schema,
        "roles": roles,
        "password_secrets": secrets,
    }


def sql_for(project):
    """Generate psql input only from validated identifier-shaped metadata."""
    p = validate({"schema_version": 1, **project})
    db, schema = p["database"], p["schema"]
    roles = p["roles"]
    marker = f"dev-pg:{p['environment']}:{p['project_id']}"
    lines = [
        "\\set ON_ERROR_STOP on",
        "SET log_statement = 'none';",
        "SET log_min_error_statement = 'panic';",
        f"SELECT pg_advisory_lock(hashtext('dev-pg:{db}'));",
    ]
    for kind in KINDS:
        role = roles[kind]
        role_marker = f"{marker}:{kind}"
        lines += [
            f"SELECT CASE WHEN EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{role}') THEN 'false' ELSE 'true' END AS create_{kind} \\gset",
            f"\\if :create_{kind}",
            "BEGIN;",
            f"CREATE ROLE {role} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;",
            f"COMMENT ON ROLE {role} IS '{role_marker}';",
            "COMMIT;",
            "\\endif",
            "DO $check$ BEGIN",
            f"  IF NOT EXISTS (SELECT 1 FROM pg_roles r WHERE r.rolname = '{role}' AND {'NOT r.rolcanlogin AND ' if kind == 'owner' else ''}NOT (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolreplication OR r.rolbypassrls) AND shobj_description(r.oid, 'pg_authid') = '{role_marker}') THEN",
            "    RAISE EXCEPTION 'role ownership mismatch';",
            "  END IF;",
            "END $check$;",
        ]
        if kind != "owner":
            # A crash before LOGIN leaves a marked NOLOGIN role that reruns safely.
            # Existing LOGIN roles are never silently rotated.
            lines += [
                f"SELECT CASE WHEN rolcanlogin THEN 'false' ELSE 'true' END AS activate_{kind} FROM pg_roles WHERE rolname = '{role}' \\gset",
                f"\\if :activate_{kind}",
                f"\\getenv {kind}_password DEV_{kind.upper()}_PASSWORD",
                (f"ALTER ROLE {role} WITH PASSWORD :'{kind}_password' LOGIN;"),
                f"\\unset {kind}_password",
                "\\endif",
                f"ALTER ROLE {role} CONNECTION LIMIT {CONNECTION_LIMITS[kind]};",
            ]
    owner = roles["owner"]
    lines += [
        f"SELECT CASE WHEN EXISTS (SELECT 1 FROM pg_database WHERE datname = '{db}') THEN 'false' ELSE 'true' END AS create_db \\gset",
        "\\if :create_db",
        f"SELECT 'CREATE DATABASE {db} OWNER {owner} TEMPLATE template0' \\gexec",
        "\\endif",
        f"\\connect {db}",
        f"SELECT pg_advisory_lock(hashtext('dev-pg:{db}'));",
        # CREATE DATABASE cannot run inside a transaction. After a crash,
        # claim an unmarked DB only if the marked owner still owns a fresh,
        # ungranted database with no user objects.
        f"SELECT COALESCE(shobj_description(d.oid, 'pg_database') = '{marker}', false) AS database_marked,",
        "       (shobj_description(d.oid, 'pg_database') IS NULL",
        f"        AND pg_get_userbyid(d.datdba) = '{owner}'",
        "        AND d.datacl IS NULL",
        "        AND NOT EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname NOT IN ('pg_catalog', 'information_schema', 'public') AND n.nspname NOT LIKE 'pg_toast%' AND n.nspname NOT LIKE 'pg_temp_%')",
        "        AND NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public')",
        "        AND NOT EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = 'public')) AS database_recoverable",
        f"  FROM pg_database d WHERE d.datname = '{db}' \\gset",
        "\\if :database_marked",
        "\\else",
        "  \\if :database_recoverable",
        f"    COMMENT ON DATABASE {db} IS '{marker}';",
        "  \\else",
        "    \\echo 'unmarked database is not a fresh project-owned creation; manual review required'",
        "    SELECT 'database ownership mismatch'::int;",
        "  \\endif",
        "\\endif",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_database d WHERE d.datname = '{db}' AND pg_get_userbyid(d.datdba) = '{owner}' AND shobj_description(d.oid, 'pg_database') = '{marker}') THEN",
        "    RAISE EXCEPTION 'database ownership mismatch';",
        "  END IF;",
        "END $check$;",
        f"REVOKE ALL ON DATABASE {db} FROM PUBLIC;",
        f"GRANT CONNECT ON DATABASE {db} TO {roles['migrator']}, {roles['runtime']}, {roles['reader']};",
        f"GRANT {owner} TO {roles['migrator']} WITH INHERIT FALSE, SET TRUE;",
        "CREATE EXTENSION IF NOT EXISTS timescaledb;",
        f"CREATE SCHEMA IF NOT EXISTS {schema} AUTHORIZATION {owner};",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname = '{schema}' AND pg_get_userbyid(n.nspowner) = '{owner}') THEN",
        "    RAISE EXCEPTION 'schema ownership mismatch';",
        "  END IF;",
        "END $check$;",
        "REVOKE ALL ON SCHEMA public FROM PUBLIC;",
        f"REVOKE ALL ON SCHEMA {schema} FROM PUBLIC;",
        f"GRANT USAGE ON SCHEMA {schema} TO {roles['runtime']}, {roles['reader']};",
        f"REVOKE ALL ON ALL TABLES IN SCHEMA {schema} FROM PUBLIC;",
        f"REVOKE ALL ON ALL SEQUENCES IN SCHEMA {schema} FROM PUBLIC;",
        f"REVOKE ALL ON ALL FUNCTIONS IN SCHEMA {schema} FROM PUBLIC;",
        f"GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA {schema} TO {roles['runtime']};",
        f"GRANT SELECT ON ALL TABLES IN SCHEMA {schema} TO {roles['reader']};",
        f"GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA {schema} TO {roles['runtime']};",
        f"ALTER DEFAULT PRIVILEGES FOR ROLE {owner} REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;",
        f"ALTER DEFAULT PRIVILEGES FOR ROLE {owner} IN SCHEMA {schema} GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {roles['runtime']};",
        f"ALTER DEFAULT PRIVILEGES FOR ROLE {owner} IN SCHEMA {schema} GRANT SELECT ON TABLES TO {roles['reader']};",
        f"ALTER DEFAULT PRIVILEGES FOR ROLE {owner} IN SCHEMA {schema} GRANT USAGE, SELECT ON SEQUENCES TO {roles['runtime']};",
        f"ALTER ROLE {roles['migrator']} IN DATABASE {db} SET search_path = {schema}, pg_catalog;",
        f"ALTER ROLE {roles['runtime']} IN DATABASE {db} SET search_path = {schema}, pg_catalog;",
        f"ALTER ROLE {roles['reader']} IN DATABASE {db} SET search_path = {schema}, pg_catalog;",
        f"ALTER ROLE {roles['runtime']} IN DATABASE {db} SET statement_timeout = '30s';",
        f"ALTER ROLE {roles['reader']} IN DATABASE {db} SET statement_timeout = '30s';",
        # Migrations must SET ROLE owner before DDL so owner default privileges apply.
        "-- default privileges apply to objects created after SET ROLE owner.",
    ]
    return "\n".join(lines) + "\n"


def read_secret(path):
    if (
        path.is_symlink()
        or not path.is_file()
        or not str(path).startswith("/run/secrets/")
    ):
        raise ValueError("secret reference is unavailable")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("secret reference is not a regular file")
    data = path.read_bytes()
    if data.endswith(b"\n"):
        data = data[:-1]
    if not data or len(data) > 512 or any(c in data for c in (b"\x00", b"\r", b"\n")):
        raise ValueError("secret format is invalid")
    return data.decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        project = validate(json.loads(args.manifest.read_text(encoding="utf-8")))
        sql = sql_for(project)
        if args.validate_only:
            print("project manifest valid")
            return 0
        env = os.environ.copy()
        env["PGPASSWORD"] = read_secret(Path("/run/secrets/dev_pg_admin_password"))
        for kind in LOGIN_KINDS:
            env[f"DEV_{kind.upper()}_PASSWORD"] = read_secret(
                Path("/run/secrets") / project["password_secrets"][kind]
            )
        command = [
            "psql",
            "-X",
            "-q",
            "-v",
            "ON_ERROR_STOP=1",
            "-h",
            "dev-pg",
            "-U",
            env.get("DEV_PG_ADMIN_USER", "postgres"),
            "-d",
            "postgres",
        ]
        result = subprocess.run(
            command, input=sql, text=True, env=env, capture_output=True, check=False
        )
        if result.returncode:
            print(
                "project provisioning failed; inspect approved isolated logs",
                file=sys.stderr,
            )
        return result.returncode
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError):
        print("invalid project manifest or secret reference", file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main())
