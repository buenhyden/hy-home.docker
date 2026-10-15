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
FUNCTION_KINDS = ("owner", "migrator", "ingest", "notifier", "reader")
FUNCTION_LOGIN_KINDS = FUNCTION_KINDS[1:]
FUNCTION_CONNECTION_LIMITS = {
    "migrator": 2,
    "ingest": 10,
    "notifier": 5,
    "reader": 5,
}
OPSFLOW_IDENTITY = {
    "project_id": "hyhome-opsflow",
    "database": "opsflow_dev",
    "schema": "ops_flow",
    "roles": {
        "owner": "opsflow_owner",
        "migrator": "opsflow_migrator",
        "ingest": "opsflow_ingest",
        "notifier": "opsflow_notifier",
        "reader": "opsflow_reader",
    },
}
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


def _validate_v1(value):
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


def _validate_function_only(value):
    _keys(value, FIELDS, "manifest")
    if type(value["schema_version"]) is not int or value["schema_version"] != 2:
        raise ValueError("unsupported manifest schema")
    if value["environment"] != "development":
        raise ValueError("dev-pg only accepts the development environment")
    project = _name(value["project_id"], PROJECT_ID, "project_id")
    database = _name(value["database"], IDENT, "database")
    schema = _name(value["schema"], IDENT, "schema")
    if (project, database, schema) != (
        OPSFLOW_IDENTITY["project_id"],
        OPSFLOW_IDENTITY["database"],
        OPSFLOW_IDENTITY["schema"],
    ):
        raise ValueError("function-only identity does not match opsflow contract")
    _keys(value["roles"], FUNCTION_KINDS, "roles")
    roles = {kind: _name(value["roles"][kind], IDENT, kind) for kind in FUNCTION_KINDS}
    if roles != OPSFLOW_IDENTITY["roles"]:
        raise ValueError("function-only roles do not match opsflow contract")
    raw_secrets = value["password_secrets"]
    secrets = None
    if raw_secrets is not None:
        _keys(raw_secrets, FUNCTION_LOGIN_KINDS, "password_secrets")
        secrets = {
            kind: _name(raw_secrets[kind], SECRET, kind + " secret")
            for kind in FUNCTION_LOGIN_KINDS
        }
        if len(set(secrets.values())) != len(FUNCTION_LOGIN_KINDS):
            raise ValueError("login roles need distinct secret references")
    return {
        "schema_version": 2,
        "project_id": project,
        "environment": "development",
        "database": database,
        "schema": schema,
        "roles": roles,
        "password_secrets": secrets,
    }


def validate(value):
    """Return a fresh validated manifest or fail before reading secrets/connecting."""
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int:
        raise ValueError("unsupported manifest schema")
    if value["schema_version"] == 1:
        return _validate_v1(value)
    if value["schema_version"] == 2:
        return _validate_function_only(value)
    raise ValueError("unsupported manifest schema")


def _sql_v1(project):
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
                f"ALTER ROLE {role} WITH PASSWORD " + f":'{kind}_password' LOGIN;",
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


def _sql_function_only(project):
    p = validate(project)
    if p["password_secrets"] is None:
        raise ValueError("credential bindings pending")
    db, schema = p["database"], p["schema"]
    roles = p["roles"]
    marker = f"dev-pg:{p['environment']}:{p['project_id']}"
    client_roles = ", ".join(roles[kind] for kind in FUNCTION_LOGIN_KINDS)
    runtime_roles = ", ".join(roles[kind] for kind in ("ingest", "notifier", "reader"))
    role_names = ",".join(f"'{roles[kind]}'" for kind in FUNCTION_KINDS)
    lines = [
        "\\set ON_ERROR_STOP on",
        "SET log_statement = 'none';",
        "SET log_min_error_statement = 'panic';",
        "SET search_path = pg_catalog;",
        f"SELECT pg_advisory_lock(hashtext('dev-pg:{db}'));",
        "DO $check$ BEGIN",
        "  IF EXISTS (SELECT 1 FROM pg_roles r",
        f"      WHERE r.rolname IN ({role_names}) AND",
        "        (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolreplication OR r.rolbypassrls",
        f"         OR (r.rolname='{roles['owner']}' AND r.rolcanlogin)",
        f"         OR shobj_description(r.oid, 'pg_authid') IS DISTINCT FROM '{marker}:' || substring(r.rolname from length('opsflow_') + 1)))",
        "     OR EXISTS (SELECT 1 FROM pg_auth_members m",
        f"      WHERE (m.roleid IN (SELECT oid FROM pg_roles WHERE rolname IN ({role_names}))",
        f"         OR m.member IN (SELECT oid FROM pg_roles WHERE rolname IN ({role_names})))",
        f"        AND NOT (m.roleid=(SELECT oid FROM pg_roles WHERE rolname='{roles['owner']}')",
        f"          AND m.member=(SELECT oid FROM pg_roles WHERE rolname='{roles['migrator']}')",
        "          AND NOT m.inherit_option AND NOT m.admin_option AND m.set_option)) THEN",
        "    RAISE EXCEPTION 'existing role or membership conflict';",
        "  END IF;",
        "END $check$;",
    ]
    for kind in FUNCTION_KINDS:
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
    lines += [
        "DO $check$ BEGIN",
        "  IF EXISTS (SELECT 1 FROM pg_database d CROSS JOIN pg_roles r",
        f"      WHERE d.datallowconn AND d.datname<>'{db}'",
        f"        AND r.rolname IN ({','.join(repr(roles[k]) for k in FUNCTION_LOGIN_KINDS)})",
        "        AND has_database_privilege(r.oid,d.oid,'CONNECT')) THEN",
        "    RAISE EXCEPTION 'cross_database_connect_requires_cluster_review';",
        "  END IF;",
        "END $check$;",
    ]
    owner, migrator = roles["owner"], roles["migrator"]
    lines += [
        "DO $check$ BEGIN",
        "  IF EXISTS (SELECT 1 FROM pg_auth_members m",
        f"      WHERE (m.roleid IN (SELECT oid FROM pg_roles WHERE rolname IN ({role_names}))",
        f"         OR m.member IN (SELECT oid FROM pg_roles WHERE rolname IN ({role_names})))",
        f"        AND NOT (m.roleid=(SELECT oid FROM pg_roles WHERE rolname='{owner}')",
        f"          AND m.member=(SELECT oid FROM pg_roles WHERE rolname='{migrator}')",
        "          AND NOT m.inherit_option AND NOT m.admin_option AND m.set_option)) THEN",
        "    RAISE EXCEPTION 'unknown role membership';",
        "  END IF;",
        "END $check$;",
        f"SELECT CASE WHEN EXISTS (SELECT 1 FROM pg_database WHERE datname = '{db}') THEN 'false' ELSE 'true' END AS create_db \\gset",
        "\\if :create_db",
        f"SELECT 'CREATE DATABASE {db} OWNER {owner} TEMPLATE template0' \\gexec",
        "\\endif",
        f"\\connect {db}",
        "SET search_path = pg_catalog;",
        f"SELECT pg_advisory_lock(hashtext('dev-pg:{db}'));",
        "SELECT CASE WHEN :'create_db'::boolean THEN 'true' ELSE 'false' END AS initialize_db \\gset",
        "\\if :create_db",
        f"COMMENT ON DATABASE {db} IS '{marker}';",
        "\\else",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_database d WHERE d.datname='{db}' AND shobj_description(d.oid, 'pg_database')='{marker}') THEN",
        "    RAISE EXCEPTION 'unmarked database requires reviewed recovery';",
        "  END IF;",
        "END $check$;",
        "\\endif",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_database d WHERE d.datname = '{db}' AND pg_get_userbyid(d.datdba) = '{owner}' AND shobj_description(d.oid, 'pg_database') = '{marker}') THEN",
        "    RAISE EXCEPTION 'database ownership mismatch';",
        "  END IF;",
        "END $check$;",
        "\\if :initialize_db",
        "\\else",
        "DO $check$ BEGIN",
        "  IF EXISTS (SELECT 1 FROM pg_database d, LATERAL aclexplode(COALESCE(d.datacl,acldefault('d',d.datdba))) a",
        f"      WHERE d.datname='{db}' AND a.grantee<>d.datdba AND",
        f"        (a.grantee NOT IN (SELECT oid FROM pg_roles WHERE rolname IN ({','.join(repr(roles[k]) for k in FUNCTION_LOGIN_KINDS)}))",
        "         OR a.privilege_type<>'CONNECT' OR a.is_grantable))",
        f"     OR EXISTS (SELECT 1 FROM pg_roles r WHERE r.rolname IN ({','.join(repr(roles[k]) for k in FUNCTION_LOGIN_KINDS)})",
        f"        AND (NOT has_database_privilege(r.rolname,'{db}','CONNECT')",
        f"          OR has_database_privilege(r.rolname,'{db}','CREATE')",
        f"          OR has_database_privilege(r.rolname,'{db}','TEMP'))) THEN",
        "    RAISE EXCEPTION 'database ACL mismatch';",
        "  END IF;",
        "END $check$;",
        "\\endif",
        "\\if :initialize_db",
        f"REVOKE ALL ON DATABASE {db} FROM PUBLIC;",
        f"GRANT CONNECT ON DATABASE {db} TO {client_roles};",
        "\\endif",
        "DO $check$ BEGIN",
        "  IF NOT EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname='public' AND pg_get_userbyid(n.nspowner)='pg_database_owner')",
        "     OR EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname NOT IN ('public','information_schema') AND n.nspname !~ '^pg_'",
        f"        AND n.nspname<>'{schema}')",
        "     OR EXISTS (SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public')",
        "     OR EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public')",
        "     OR EXISTS (SELECT 1 FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='public') THEN",
        "    RAISE EXCEPTION 'public schema contains objects or has unexpected owner';",
        "  END IF;",
        "  IF EXISTS (SELECT 1 FROM pg_default_acl d, LATERAL aclexplode(d.defaclacl) a",
        f"      WHERE d.defaclrole=(SELECT oid FROM pg_roles WHERE rolname='{owner}') AND a.grantee<>d.defaclrole) THEN",
        "    RAISE EXCEPTION 'default ACL mismatch';",
        "  END IF;",
        "END $check$;",
        f"SELECT CASE WHEN EXISTS (SELECT 1 FROM pg_namespace WHERE nspname='{schema}') THEN 'false' ELSE 'true' END AS create_schema \\gset",
        "DO $check$ BEGIN",
        "  IF EXISTS (SELECT 1 FROM pg_namespace n, LATERAL aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a",
        "      WHERE n.nspname='public' AND a.grantee<>n.nspowner",
        f"        AND (a.grantee<>0 OR EXISTS (SELECT 1 FROM pg_namespace WHERE nspname='{schema}'))) THEN",
        "    RAISE EXCEPTION 'public schema ACL mismatch';",
        "  END IF;",
        "END $check$;",
        "\\if :create_schema",
        "\\else",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname='{schema}' AND pg_get_userbyid(n.nspowner)='{owner}' AND obj_description(n.oid,'pg_namespace')='{marker}:schema')",
        "     OR EXISTS (SELECT 1 FROM pg_namespace n, LATERAL aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a",
        f"      WHERE n.nspname='{schema}' AND a.grantee<>n.nspowner AND",
        f"        (a.grantee NOT IN (SELECT oid FROM pg_roles WHERE rolname IN ('{roles['ingest']}','{roles['notifier']}','{roles['reader']}'))",
        "         OR a.privilege_type<>'USAGE' OR a.is_grantable))",
        f"     OR EXISTS (SELECT 1 FROM pg_roles r WHERE r.rolname IN ('{roles['ingest']}','{roles['notifier']}','{roles['reader']}')",
        f"        AND (NOT has_schema_privilege(r.rolname,'{schema}','USAGE') OR has_schema_privilege(r.rolname,'{schema}','CREATE')))",
        "     OR EXISTS (SELECT 1 FROM pg_namespace n, LATERAL aclexplode(COALESCE(n.nspacl,acldefault('n',n.nspowner))) a WHERE n.nspname='public' AND a.grantee<>n.nspowner) THEN",
        "    RAISE EXCEPTION 'schema ACL mismatch';",
        "  END IF;",
        "END $check$;",
        "\\endif",
        "\\if :create_schema",
        "BEGIN;",
        f"CREATE SCHEMA {schema} AUTHORIZATION {owner};",
        f"COMMENT ON SCHEMA {schema} IS '{marker}:schema';",
        "REVOKE ALL ON SCHEMA public FROM PUBLIC;",
        f"REVOKE ALL ON SCHEMA {schema} FROM PUBLIC;",
        f"GRANT USAGE ON SCHEMA {schema} TO {runtime_roles};",
        "COMMIT;",
        "\\endif",
        "DO $check$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_namespace n WHERE n.nspname='{schema}' AND pg_get_userbyid(n.nspowner)='{owner}' AND obj_description(n.oid,'pg_namespace')='{marker}:schema') THEN",
        "    RAISE EXCEPTION 'schema ownership mismatch';",
        "  END IF;",
        "END $check$;",
        f"ALTER DEFAULT PRIVILEGES FOR ROLE {owner} REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;",
        f"SELECT CASE WHEN EXISTS (SELECT 1 FROM pg_auth_members WHERE roleid=(SELECT oid FROM pg_roles WHERE rolname='{owner}') AND member=(SELECT oid FROM pg_roles WHERE rolname='{migrator}') AND NOT inherit_option AND NOT admin_option AND set_option) THEN 'false' ELSE 'true' END AS create_owner_membership \\gset",
        "\\if :create_owner_membership",
        f"GRANT {owner} TO {migrator} WITH INHERIT FALSE, SET TRUE;",
        "\\endif",
    ]
    for kind in FUNCTION_LOGIN_KINDS:
        role = roles[kind]
        lines += [
            f"SELECT CASE WHEN rolcanlogin THEN 'false' ELSE 'true' END AS activate_{kind} FROM pg_roles WHERE rolname = '{role}' \\gset",
            f"\\if :activate_{kind}",
            f"\\getenv {kind}_password DEV_{kind.upper()}_PASSWORD",
            f"ALTER ROLE {role} WITH PASSWORD " + f":'{kind}_password' LOGIN;",
            f"\\unset {kind}_password",
            "\\endif",
            f"ALTER ROLE {role} CONNECTION LIMIT {FUNCTION_CONNECTION_LIMITS[kind]};",
            "DO $check$ BEGIN",
            f"  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='{role}' AND rolcanlogin AND rolconnlimit={FUNCTION_CONNECTION_LIMITS[kind]}) THEN",
            "    RAISE EXCEPTION 'login role activation mismatch';",
            "  END IF;",
            "END $check$;",
            f"ALTER ROLE {role} IN DATABASE {db} SET search_path = {schema}, pg_catalog;",
            f"ALTER ROLE {role} IN DATABASE {db} SET statement_timeout = '30s';",
        ]
    return "\n".join(lines) + "\n"


def sql_for(project):
    """Generate psql input only from validated identifier-shaped metadata."""
    if project.get("schema_version", 1) == 2:
        return _sql_function_only(project)
    return _sql_v1(project)


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
        if args.validate_only:
            if (
                project.get("schema_version") == 2
                and project["password_secrets"] is None
            ):
                print(
                    "project manifest structurally valid; credential bindings pending"
                )
            else:
                print("project manifest valid")
            return 0
        sql = sql_for(project)
        env = os.environ.copy()
        env["PGPASSWORD"] = read_secret(Path("/run/secrets/dev_pg_admin_password"))
        login_kinds = (
            FUNCTION_LOGIN_KINDS if project.get("schema_version") == 2 else LOGIN_KINDS
        )
        for kind in login_kinds:
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
