#!/usr/bin/env python3
"""Validate one perf_db project manifest and render idempotent registration SQL."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

IDENT = re.compile(r"[a-z_][a-z0-9_]{0,62}\Z")
PROJECT_ID = re.compile(r"[a-z][a-z0-9-]{0,62}\Z")
KINDS = ("reader", "writer", "verdict")
FIELDS = {"schema_version", "project_id", "roles"}
RESERVED_ROLES = {"perf_owner", "perf_migrator", "postgres"}


def _keys(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f"{label} fields do not match schema")


def _name(value, pattern, label):
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise ValueError(f"invalid {label}")
    return value


def validate(value):
    """Return a fresh project registration or fail before emitting SQL."""
    _keys(value, FIELDS, "manifest")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported manifest schema")
    project_id = _name(value["project_id"], PROJECT_ID, "project_id")
    _keys(value["roles"], KINDS, "roles")
    roles = {kind: _name(value["roles"][kind], IDENT, f"{kind} role") for kind in KINDS}
    if len(set(roles.values())) != len(KINDS):
        raise ValueError("project roles must be distinct")
    if set(roles.values()) & RESERVED_ROLES or any(
        role.startswith("pg_") for role in roles.values()
    ):
        raise ValueError("project role is reserved")
    return {"project_id": project_id, "roles": roles}


def _role_sql(project_id, kind, role):
    marker = f"dev-pg:development:perf_db:{project_id}:{kind}"
    return [
        "DO $role$ BEGIN",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{role}') THEN",
        f"    CREATE ROLE {role} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;",
        f"    COMMENT ON ROLE {role} IS '{marker}';",
        "  END IF;",
        f"  IF NOT EXISTS (SELECT 1 FROM pg_roles r WHERE r.rolname = '{role}'",
        "      AND NOT r.rolcanlogin AND NOT (r.rolsuper OR r.rolcreatedb",
        "        OR r.rolcreaterole OR r.rolreplication OR r.rolbypassrls)",
        "      AND NOT EXISTS (SELECT 1 FROM pg_auth_members m WHERE m.member = r.oid)",
        f"      AND shobj_description(r.oid, 'pg_authid') = '{marker}') THEN",
        "    RAISE EXCEPTION 'role ownership mismatch';",
        "  END IF;",
        "END $role$;",
    ]


def sql_for(project):
    """Render fixed-identifier SQL for one validated project."""
    p = validate({"schema_version": 1, **project})
    project_id, roles = p["project_id"], p["roles"]
    lines = [
        "\\set ON_ERROR_STOP on",
        "BEGIN;",
        "SELECT pg_advisory_xact_lock(hashtext('perf_db:project-registration'));",
    ]
    for kind in KINDS:
        lines.extend(_role_sql(project_id, kind, roles[kind]))
    lines.extend(
        [
            "SET ROLE perf_owner;",
            "DO $roles$ BEGIN",
            "  IF EXISTS (SELECT 1 FROM quality.projects p",
            f"      WHERE p.project_id <> '{project_id}'",
            "        AND (p.reader_role IN (",
            f"          '{roles['reader']}'::name, '{roles['writer']}'::name, '{roles['verdict']}'::name",
            "        ) OR p.writer_role IN (",
            f"          '{roles['reader']}'::name, '{roles['writer']}'::name, '{roles['verdict']}'::name",
            "        ) OR p.verdict_role IN (",
            f"          '{roles['reader']}'::name, '{roles['writer']}'::name, '{roles['verdict']}'::name",
            "        ))) THEN",
            "    RAISE EXCEPTION 'project role already assigned';",
            "  END IF;",
            "END $roles$;",
            "INSERT INTO quality.projects (project_id, reader_role, writer_role, verdict_role)",
            f"VALUES ('{project_id}', '{roles['reader']}', '{roles['writer']}', '{roles['verdict']}')",
            "ON CONFLICT (project_id) DO NOTHING;",
            "DO $project$ BEGIN",
            "  IF NOT EXISTS (SELECT 1 FROM quality.projects",
            f"      WHERE project_id = '{project_id}'",
            f"        AND reader_role = '{roles['reader']}'::name",
            f"        AND writer_role = '{roles['writer']}'::name",
            f"        AND verdict_role = '{roles['verdict']}'::name) THEN",
            "    RAISE EXCEPTION 'project authority mismatch';",
            "  END IF;",
            "END $project$;",
            f"GRANT CONNECT ON DATABASE perf_db TO {roles['reader']}, {roles['writer']}, {roles['verdict']};",
            f"GRANT USAGE ON SCHEMA quality TO {roles['reader']}, {roles['writer']}, {roles['verdict']};",
            "GRANT EXECUTE ON FUNCTION quality.has_project_access(text, name, text)",
            f"  TO {roles['reader']}, {roles['writer']}, {roles['verdict']};",
            "GRANT EXECUTE ON FUNCTION quality.import_payload(jsonb, bytea)",
            f"  TO {roles['writer']};",
            "GRANT SELECT ON quality.run_attempts, quality.artifacts, quality.metric_summaries, quality.verdict_events",
            f"  TO {roles['reader']}, {roles['writer']}, {roles['verdict']};",
            "GRANT SELECT ON quality.run_results",
            f"  TO {roles['reader']}, {roles['writer']}, {roles['verdict']};",
            "GRANT INSERT (decision_id, run_id, attempt, project_id, verdict, reason)",
            "  ON quality.verdict_events",
            f"  TO {roles['verdict']};",
            "RESET ROLE;",
            "COMMIT;",
        ]
    )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        project = validate(json.loads(args.manifest.read_text(encoding="utf-8")))
        if args.validate_only:
            print("perf_db project manifest valid")
        else:
            print(sql_for(project), end="")
        return 0
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError):
        print("invalid perf_db project manifest", file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main())
