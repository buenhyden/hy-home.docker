#!/usr/bin/env python3
"""Provision the dev-pg metrics role used by dev-pg-exporter.

The role is a marked LOGIN member of pg_monitor only. It never gets CONNECT on
project databases (they revoke PUBLIC), and a rerun never rotates its password.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from project import read_secret

ROLE = "dev_pg_monitor"
MARKER = "dev-pg:development:monitor"
CONNECTION_LIMIT = 3
PW_VAR = "monitor_secret"


def sql():
    return (
        "\n".join(
            [
                "\\set ON_ERROR_STOP on",
                "SET log_statement = 'none';",
                "SET log_min_error_statement = 'panic';",
                "SELECT pg_advisory_lock(hashtext('dev-pg:monitor'));",
                f"SELECT NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{ROLE}') AS create_role \\gset",
                "\\if :create_role",
                "BEGIN;",
                f"CREATE ROLE {ROLE} NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;",
                f"COMMENT ON ROLE {ROLE} IS '{MARKER}';",
                "COMMIT;",
                "\\endif",
                "DO $check$ BEGIN",
                f"  IF NOT EXISTS (SELECT 1 FROM pg_roles r WHERE r.rolname = '{ROLE}' AND NOT (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolreplication OR r.rolbypassrls) AND shobj_description(r.oid, 'pg_authid') = '{MARKER}') THEN",
                "    RAISE EXCEPTION 'role ownership mismatch';",
                "  END IF;",
                "END $check$;",
                f"SELECT NOT rolcanlogin AS activate FROM pg_roles WHERE rolname = '{ROLE}' \\gset",
                "\\if :activate",
                f"\\getenv {PW_VAR} DEV_MONITOR_PASSWORD",
                f"ALTER ROLE {ROLE} WITH PASSWORD :'{PW_VAR}' LOGIN;",
                f"\\unset {PW_VAR}",
                "\\endif",
                f"GRANT pg_monitor TO {ROLE};",
                f"ALTER ROLE {ROLE} CONNECTION LIMIT {CONNECTION_LIMIT};",
                f"ALTER ROLE {ROLE} SET statement_timeout = '10s';",
            ]
        )
        + "\n"
    )


def main():
    try:
        admin = read_secret(Path("/run/secrets/dev_pg_admin_password"))
        monitor = read_secret(Path("/run/secrets/dev_pg_monitor_password"))
        if monitor == admin:
            raise ValueError("monitor secret reuses the admin secret")
    except (ValueError, OSError, UnicodeError):
        print("invalid monitor secret reference", file=sys.stderr)
        return 64
    env = {**os.environ, "PGPASSWORD": admin, "DEV_MONITOR_PASSWORD": monitor}
    command = ["psql", "-X", "-q", "-h", "dev-pg", "-U"]
    command += [env.get("DEV_PG_ADMIN_USER", "postgres"), "-d", "postgres"]
    result = subprocess.run(
        command, input=sql(), text=True, env=env, capture_output=True, check=False
    )
    if result.returncode:
        print("monitor role provisioning failed", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
