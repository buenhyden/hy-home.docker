#!/usr/bin/env python3
"""Validate credential-free external project registration metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "infra/09-platform-ops/project-registration/schema.json"
SECRET_REF = re.compile(r"^[a-z][a-z0-9_]{2,63}$")


class RegistrationError(ValueError):
    """A bounded validation failure with a fixed, non-value-bearing reason."""


SERVICE_SCHEMES = {
    "api": {"http", "https"},
    "db": {"postgresql"},
    "valkey": {"redis", "rediss"},
    "s3": {"http", "https"},
    "oidc": {"http", "https"},
    "search": {"http", "https"},
    "telemetry": {"http", "https"},
}


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise RegistrationError("duplicate JSON member")
        result[key] = value
    return result


def validate(path: Path, allowed_secret_refs: set[str]) -> None:
    if not allowed_secret_refs or any(
        not SECRET_REF.fullmatch(name) for name in allowed_secret_refs
    ):
        raise RegistrationError("explicit valid secret reference allowlist required")
    if path.stat().st_size > 65536:
        raise RegistrationError("registration exceeds 64 KiB")
    document = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys
    )
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(document))
    if errors:
        raise RegistrationError("schema violation")
    if any(ref not in allowed_secret_refs for ref in document["secret_refs"]):
        raise RegistrationError("secret reference not allowed")
    for location in document["endpoints"].values():
        for service, endpoint in location.items():
            if endpoint["scheme"] not in SERVICE_SCHEMES[service]:
                raise RegistrationError("endpoint scheme does not match service")
            if service == "db" and endpoint["path"] != f"/{document['db']['name']}":
                raise RegistrationError("DB endpoint path must match database name")
            if any(segment in {".", ".."} for segment in endpoint["path"].split("/")):
                raise RegistrationError("endpoint path traversal")
    db = document["db"]
    roles = [
        db[key]
        for key in ("owner_role", "migrator_role", "runtime_role", "reader_role")
    ]
    if db["name"] in {"postgres", "template0", "template1", "app_db"} or db[
        "name"
    ].startswith("pg_"):
        raise RegistrationError("reserved DB name")
    if db["schema"] in {"public", "pg_catalog", "information_schema"} or db[
        "schema"
    ].startswith("pg_"):
        raise RegistrationError("reserved schema name")
    if len(roles) != len(set(roles)) or any(
        role in {db["name"], db["schema"], "postgres"} or role.startswith("pg_")
        for role in roles
    ):
        raise RegistrationError("DB roles must be distinct and nonreserved")
    project_id = document["project_id"]
    if document["valkey"]["acl_user"] in {"default", "devadmin"}:
        raise RegistrationError("reserved Valkey ACL user")
    if document["valkey"]["acl_prefix"] != project_id:
        raise RegistrationError("Valkey ACL prefix must match project_id")
    if not document["s3"]["prefix"].startswith(f"{project_id}/"):
        raise RegistrationError("S3 prefix must match project_id")
    search_path = document["search"]["authorization_path"]
    if search_path != f"/projects/{project_id}" and not search_path.startswith(
        f"/projects/{project_id}/"
    ):
        raise RegistrationError("search authorization path must match project_id")
    if any(name in {"host", "none", "bridge"} for name in document["allowed_networks"]):
        raise RegistrationError("built-in Docker networks are not project boundaries")
    if any(
        not re.fullmatch(r"[a-z][a-z0-9-]{0,62}", endpoint["host"])
        or endpoint["host"] == "localhost"
        for endpoint in document["endpoints"].get("same_daemon", {}).values()
    ):
        raise RegistrationError("same-daemon endpoints require a Docker service name")
    if any(
        "." not in endpoint["host"] and endpoint["host"] != "localhost"
        for endpoint in document["endpoints"].get("host", {}).values()
    ):
        raise RegistrationError("host endpoints cannot use daemon-only service names")
    for service, endpoint in document["endpoints"].get("external", {}).items():
        if not re.fullmatch(
            r"[a-z][a-z0-9-]*(?:\.[a-z0-9-]+)*\.[a-z][a-z0-9-]*", endpoint["host"]
        ):
            raise RegistrationError(
                "external endpoints require an ASCII-letter-first DNS FQDN"
            )
        if service == "db" or endpoint["scheme"] not in {"https", "rediss"}:
            raise RegistrationError("external endpoint transport is not approved")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registration", type=Path)
    parser.add_argument(
        "--allow-secret-ref", action="append", default=[], metavar="NAME"
    )
    args = parser.parse_args()
    try:
        validate(args.registration, set(args.allow_secret_ref))
    except RegistrationError as error:
        print(f"project-registration: FAIL ({error})")
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        # Unexpected parser or filesystem errors never echo input or path values.
        print("project-registration: FAIL (invalid input)")
        return 1
    print("project-registration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
