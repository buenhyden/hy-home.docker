"""P02 value-free catalog and staging views; no credential or runtime authority.

Inputs are fixed tracked public metadata. Classification and generation guards
are source contracts only, never proof of issuance, delivery or consumption.
The operator must create the .agent-work family and its regular README first.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from contextlib import ExitStack
from datetime import date
from pathlib import Path, PurePosixPath

from scripts.lib.ops._secret_catalog_io import (
    CATALOG_PATH,
    MAX_BYTES,
    METADATA_PATH,
    SCHEMA_PATH,
    SUPPORT_PATH,
    CatalogError,
    _output,
    _public_bytes,
    _read_file,
    _root,
    _staging_fd,
    _target_safe,
    _unique_object,
)
from scripts.lib.ops._secret_catalog_io import DIR_FLAGS as DIR_FLAGS
from scripts.lib.ops._secret_catalog_io import FILE_FLAGS as FILE_FLAGS
from scripts.lib.ops._secret_catalog_io import OUTPUT_PATH as OUTPUT_PATH
from scripts.lib.ops._secret_catalog_io import _directory as _directory
from scripts.lib.ops.smtp_contract import (
    CANONICAL_PATH,
    metadata_retired,
    root_identity,
)

VIEW_NAMES = (
    "SENSITIVE_ENV_VARS.md.example",
    "secret-catalog-summary.json",
    "README.md",
    "SENSITIVE_ENV_VARS.md",
)
IDENTIFIER = re.compile(r"[A-Z][A-Z0-9]{1,15}-[0-9]{3}\Z")
FIELD = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")
ENTRY_FIELDS = frozenset(
    {
        "id",
        "scope",
        "classification",
        "automation",
        "value_type",
        "env_key",
        "source_path",
        "source_recorded_at",
        "purpose",
        "consumers",
        "consumer_status",
        "disposition",
        "destination_plan",
        "recovery",
        "lifecycle",
        "owner",
        "action",
        "evidence_ref",
        "runtime_evidence",
    }
)
METADATA_FIELDS = (
    "id",
    "automation",
    "value_type",
    "env_key",
    "source_path",
    "source_recorded_at",
    "purpose",
)
CLASSIFICATIONS = {
    "kv_static",
    "stable_crypto",
    "bootstrap_external",
    "public_configuration",
    "derived_runtime",
    "unused_delete",
    "lab_excluded",
}
VALUE_TYPES = frozenset(
    "Cookie DB ID Key PW Pass Recovery Secret Token URL User".split()
)
DISPOSITIONS = {
    "ACTIVE_KEEP",
    "RETAINED_FOR_RECOVERY",
    "UNKNOWN_BLOCKED",
    "UNUSED_DELETE",
    "LAB_EXCLUDED",
}
LIFECYCLE_FIELDS = {
    "declared",
    "observed",
    "imported",
    "delivered",
    "consumed",
    "rotated",
    "recovered",
    "retired",
}
SECRET_TEXT = re.compile(
    r"-----BEGIN [A-Z ]+-----|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b|\b(?:value|password|passwd|token|secret|api[_-]?key)\s*[:=]\s*\S+",
    re.I,
)


def _text(value, maximum=1000):
    return (
        isinstance(value, str)
        and bool(value.strip())
        and len(value) <= maximum
        and not any(unicodedata.category(char).startswith("C") for char in value)
        and not SECRET_TEXT.search(value)
    )


def _path(value, nullable=False):
    if value is None and nullable:
        return
    if not _text(value, 512):
        raise CatalogError("unsafe_metadata_path")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or str(path) != value
        or ".." in path.parts
        or "\\" in value
        or any(char in value for char in "*?[]|")
        or not path.parts
    ):
        raise CatalogError("unsafe_metadata_path")


def _closed(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise CatalogError("invalid_closed_metadata")


def _identifier(value):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise CatalogError("invalid_identifier")


def _date(value):
    try:
        if not isinstance(value, str) or len(value) != 10:
            raise ValueError
        date.fromisoformat(value)
    except ValueError as error:
        raise CatalogError("invalid_source_recorded_date") from error


def _clean(cell):
    return cell.strip().strip("*`").strip()


def parse_public_table(data: bytes):
    """Parse the existing ten pipe-cell table and reuse SMTP alias validation."""
    if not isinstance(data, bytes) or len(data) > MAX_BYTES:
        raise CatalogError("invalid_public_metadata")
    try:
        if metadata_retired(data) != data:
            raise CatalogError("public_smtp_source_not_retired")
        text = data.decode("utf-8")
    except (ValueError, UnicodeError) as error:
        raise CatalogError("invalid_public_metadata") from error
    entries, aliases, seen = [], [], set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [_clean(cell) for cell in line.split("|")]
        if len(cells) == 4:
            if cells[1:3] in [["Retired ID", "Canonical ID"], ["---", "---"]]:
                continue
            _identifier(cells[1])
            _identifier(cells[2])
            aliases.append(
                {"id": cells[1], "canonical_id": cells[2], "state": "source_retired"}
            )
            continue
        if len(cells) != 10:
            raise CatalogError("invalid_public_table_shape")
        if cells[1] == "ID" or re.fullmatch(r":?-{3,}:?", cells[1]):
            continue
        _identifier(cells[1])
        if (
            cells[1] in seen
            or cells[2] not in {"O", "X"}
            or cells[3] not in VALUE_TYPES
        ):
            raise CatalogError("invalid_public_table_row")
        if cells[4] not in {"(비어있음)", "-", ""}:
            raise CatalogError("public_value_cell_not_placeholder")
        seen.add(cells[1])
        env_key = None if cells[5] in {"", "-"} else cells[5]
        source_path = None if cells[6] in {"", "-"} else cells[6]
        _path(source_path, nullable=True)
        _date(cells[7])
        if env_key is not None and not re.fullmatch(r"[A-Z][A-Z0-9_]*", env_key):
            raise CatalogError("invalid_environment_key")
        if not _text(cells[8]) or "|" in cells[8]:
            raise CatalogError("unsafe_public_purpose")
        entries.append(
            dict(
                zip(
                    METADATA_FIELDS,
                    [
                        cells[1],
                        cells[2],
                        cells[3],
                        env_key,
                        source_path,
                        cells[7],
                        cells[8],
                    ],
                    strict=True,
                )
            )
        )
    return {"entries": entries, "aliases": aliases}


def _validate_entry(entry):
    _closed(entry, ENTRY_FIELDS)
    _identifier(entry["id"])
    if any(
        not isinstance(entry[key], str)
        for key in (
            "scope",
            "classification",
            "automation",
            "value_type",
            "consumer_status",
            "disposition",
        )
    ):
        raise CatalogError("invalid_entry_category")
    if (
        entry["scope"] not in {"root", "lab"}
        or entry["classification"] not in CLASSIFICATIONS
        or entry["automation"] not in {"O", "X"}
        or entry["value_type"] not in VALUE_TYPES
        or entry["consumer_status"] not in {"DECLARED", "BLOCKED_FACTS"}
        or entry["disposition"] not in DISPOSITIONS
    ):
        raise CatalogError("invalid_entry_category")
    _path(entry["source_path"], nullable=True)
    if entry["source_path"] is not None and not entry["source_path"].startswith(
        "secrets/"
    ):
        raise CatalogError("source_path_outside_secret_metadata")
    _date(entry["source_recorded_at"])
    if entry["env_key"] is not None and (
        not isinstance(entry["env_key"], str)
        or not re.fullmatch(r"[A-Z][A-Z0-9_]*", entry["env_key"])
    ):
        raise CatalogError("invalid_environment_key")
    if not _text(entry["purpose"]) or "|" in entry["purpose"]:
        raise CatalogError("unsafe_public_purpose")
    if (
        not isinstance(entry["consumers"], list)
        or any(not isinstance(item, str) for item in entry["consumers"])
        or len(set(entry["consumers"])) != len(entry["consumers"])
    ):
        raise CatalogError("invalid_consumer_references")
    if (
        entry["consumer_status"] == "DECLARED"
        and not entry["consumers"]
        and not (
            entry["classification"] == "unused_delete"
            and entry["disposition"] == "UNUSED_DELETE"
            and entry["action"] == "DELETE"
        )
    ):
        raise CatalogError("declared_consumer_references_required")
    for consumer in entry["consumers"]:
        _path(consumer)
    _validate_plans(entry)
    _validate_governance(entry)
    is_lab = (
        entry["scope"] == "lab"
        or entry["id"].startswith("LAB-")
        or str(entry["source_path"]).startswith("secrets/labs/")
    )
    if is_lab != (
        entry["classification"] == "lab_excluded"
        and entry["disposition"] == "LAB_EXCLUDED"
    ):
        raise CatalogError("lab_exclusion_mismatch")
    if (
        entry["id"] in {"PG-020", "SEC-003"} or entry["id"].startswith("BKP-")
    ) and entry["disposition"] != "RETAINED_FOR_RECOVERY":
        raise CatalogError("recovery_hold_required")
    if (
        entry["classification"] == "stable_crypto"
        and entry["recovery"]["custody"] == "not_applicable"
    ):
        raise CatalogError("crypto_custody_required")
    unused = entry["classification"] == "unused_delete"
    if unused != (entry["disposition"] == "UNUSED_DELETE"):
        raise CatalogError("deletion_classification_mismatch")
    if unused:
        from scripts.lib.ops.retire_materials import PROTECTED_IDS

        tokens = set(re.split(r"[^a-z0-9]+", str(entry["source_path"]).lower()))
        crypto = {
            "key",
            "jwt",
            "fernet",
            "encryption",
            "unseal",
            "cookie",
            "cert",
            "snapshot",
        }
        if (
            entry["consumers"]
            or entry["consumer_status"] != "DECLARED"
            or entry["recovery"]["custody"] != "not_applicable"
            or entry["id"] in PROTECTED_IDS
            or tokens & crypto
        ):
            raise CatalogError("unused_metadata_has_protected_dependency")


def _validate_plans(entry):
    plan = entry["destination_plan"]
    _closed(
        plan,
        "status kv_path acl delivery reload mount field uid gid mode restart rotation".split(),
    )
    if plan["status"] == "DEPLOYED":
        # A rendered OpenBao Agent file proven by the evidence Task; no value.
        if (
            entry["action"] != "IMPLEMENT"
            or entry["lifecycle"].get("delivered") != "CONFIRMED"
            or plan["delivery"] != "openbao_agent"
            or plan["mount"] != "secret"
            or not isinstance(plan["kv_path"], str)
            or not plan["kv_path"].startswith("hy-home/")
            or not isinstance(plan["field"], str)
            or not FIELD.fullmatch(plan["field"])
            or any(
                type(plan[key]) is not int or not 0 <= plan[key] <= 65535
                for key in ("uid", "gid")
            )
            or plan["mode"] not in {"0600", "0640"}
        ):
            raise CatalogError("invalid_deployed_destination")
        contract = ("acl", "reload", "restart", "rotation")
    else:
        if any(
            plan[key] is not None for key in ("mount", "field", "uid", "gid", "mode")
        ):
            raise CatalogError("unapproved_delivery_binding")
        contract = ("status", "acl", "delivery", "reload", "restart", "rotation")
    if (
        entry["classification"] != "kv_static"
        or entry["disposition"] == "RETAINED_FOR_RECOVERY"
    ) and plan["kv_path"] is not None:
        raise CatalogError("destination_not_applicable")
    if any(plan[key] != "BLOCKED_P01" for key in contract):
        raise CatalogError("unapproved_delivery_contract")
    _path(plan["kv_path"], nullable=True)
    recovery = entry["recovery"]
    _closed(recovery, {"history", "custody", "status"})
    if (
        recovery["history"] != "retain"
        or recovery["status"] != "UNKNOWN"
        or not isinstance(recovery["custody"], str)
        or recovery["custody"]
        not in {"independent_required", "consumer_owned", "not_applicable"}
    ):
        raise CatalogError("invalid_recovery_contract")
    lifecycle = entry["lifecycle"]
    _closed(lifecycle, LIFECYCLE_FIELDS)
    if lifecycle["declared"] != "CONFIRMED":
        raise CatalogError("invalid_declared_state")
    for key in LIFECYCLE_FIELDS - {"declared"}:
        allowed = (
            {"UNKNOWN", "CONFIRMED"}
            if key in {"observed", "consumed"}
            else {"NOT_RUN", "CONFIRMED"}
        )
        if not isinstance(lifecycle[key], str) or lifecycle[key] not in allowed:
            raise CatalogError("invalid_lifecycle_state")


def _validate_governance(entry):
    allowed = {
        "ACTIVE_KEEP": {"NO_CHANGE", "IMPLEMENT", "VERIFY_RUNTIME"},
        "RETAINED_FOR_RECOVERY": {"NO_CHANGE", "VERIFY_RUNTIME"},
        "UNKNOWN_BLOCKED": {"BLOCKED_FACTS"},
        "UNUSED_DELETE": {"DELETE"},
        "LAB_EXCLUDED": {"OUT_OF_SCOPE"},
    }
    action = entry["action"]
    if (
        entry["owner"] != "@buenhyden"
        or not isinstance(action, str)
        or action not in allowed[entry["disposition"]]
    ):
        raise CatalogError("invalid_metadata_governance")
    if (action == "OUT_OF_SCOPE") != (entry["scope"] == "lab"):
        raise CatalogError("scope_action_mismatch")
    if action == "IMPLEMENT" and entry["classification"] != "kv_static":
        raise CatalogError("implementation_classification_mismatch")
    if (
        action in {"IMPLEMENT", "VERIFY_RUNTIME"}
        or entry["disposition"] == "ACTIVE_KEEP"
    ) and entry["consumer_status"] != "DECLARED":
        raise CatalogError("action_requires_declared_consumers")
    if (
        entry["disposition"] == "UNKNOWN_BLOCKED"
        and entry["consumer_status"] != "BLOCKED_FACTS"
    ):
        raise CatalogError("blocked_action_requires_unknown_facts")
    _path(entry["evidence_ref"])
    if not entry["evidence_ref"].startswith("docs/"):
        raise CatalogError("unsafe_evidence_reference")
    evidence = entry["runtime_evidence"]
    _closed(evidence, LIFECYCLE_FIELDS - {"declared"})
    for lane, reference in evidence.items():
        _path(reference, nullable=True)
        if reference is not None and not reference.startswith("docs/"):
            raise CatalogError("unsafe_runtime_evidence")
        if entry["lifecycle"][lane] == "CONFIRMED" and reference is None:
            raise CatalogError("confirmed_lane_without_reference")
    if entry["lifecycle"]["consumed"] == "CONFIRMED" and not entry["consumers"]:
        raise CatalogError("confirmed_consumption_without_consumer")


def _schema_references(schema):
    pending = [(schema, 0)]
    while pending:
        node, depth = pending.pop()
        if depth > 64:
            raise CatalogError("schema_depth_exceeded")
        if isinstance(node, dict):
            for name in ("$ref", "$dynamicRef"):
                if name in node and (
                    not isinstance(node[name], str) or not node[name].startswith("#")
                ):
                    raise CatalogError("external_schema_reference")
            pending.extend((value, depth + 1) for value in node.values())
        elif isinstance(node, list):
            pending.extend((value, depth + 1) for value in node)


def validate_catalog(catalog, schema=None):
    _closed(
        catalog,
        {
            "schema_version",
            "owner_task",
            "metadata_source",
            "support_matrix",
            "entries",
            "aliases",
        },
    )
    if (
        catalog["schema_version"] != "1.0.0"
        or catalog["owner_task"] != "SPEC-0204-TSK-0010"
        or catalog["metadata_source"] != METADATA_PATH
        or catalog["support_matrix"] != SUPPORT_PATH
    ):
        raise CatalogError("invalid_catalog_owner")
    if not isinstance(catalog["entries"], list) or not isinstance(
        catalog["aliases"], list
    ):
        raise CatalogError("invalid_catalog_rows")
    identifiers, paths, destinations = set(), set(), set()
    for entry in catalog["entries"]:
        _validate_entry(entry)
        if entry["id"] in identifiers or (
            entry["source_path"] is not None and entry["source_path"] in paths
        ):
            raise CatalogError("duplicate_catalog_owner")
        plan = entry["destination_plan"]
        destination = (plan["mount"], plan["kv_path"], plan["field"])
        if plan["kv_path"] is not None and destination in destinations:
            raise CatalogError("duplicate_planned_destination")
        if plan["kv_path"] is not None:
            destinations.add(destination)
        identifiers.add(entry["id"])
        if entry["source_path"] is not None:
            paths.add(entry["source_path"])
    _validate_aliases(catalog, identifiers)
    if schema is not None:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
        from referencing.exceptions import Unresolvable

        try:
            _schema_references(schema)
            Draft202012Validator.check_schema(schema)
            if (
                next(Draft202012Validator(schema).iter_errors(catalog), None)
                is not None
            ):
                raise CatalogError("schema_validation_failed")
        except (
            TypeError,
            ValueError,
            SchemaError,
            Unresolvable,
            RecursionError,
        ) as error:
            raise CatalogError("schema_validation_failed") from error


def _validate_aliases(catalog, identifiers):
    mapping = {}
    for alias in catalog["aliases"]:
        _closed(alias, {"id", "canonical_id", "state"})
        _identifier(alias["id"])
        _identifier(alias["canonical_id"])
        if (
            alias["state"] != "source_retired"
            or alias["id"] in identifiers
            or alias["id"] in mapping
        ):
            raise CatalogError("duplicate_or_invalid_alias")
        mapping[alias["id"]] = alias["canonical_id"]
    for identifier in mapping:
        seen, current = set(), identifier
        while current in mapping:
            if current in seen:
                raise CatalogError("alias_cycle")
            seen.add(current)
            current = mapping[current]
        if current not in identifiers:
            raise CatalogError("missing_canonical_identifier")
    smtp = next(
        (entry for entry in catalog["entries"] if entry["id"] == "COMM-002"), None
    )
    if (
        smtp is None
        or smtp["source_path"] != CANONICAL_PATH
        or mapping.get("COMM-003") != "COMM-002"
    ):
        raise CatalogError("canonical_smtp_mismatch")


def generation_allowed(catalog, identifier):
    """Metadata eligibility only; this API never generates or accesses a value."""
    try:
        validate_catalog(catalog)
        _identifier(identifier)
        entry = next(
            (item for item in catalog["entries"] if item["id"] == identifier), None
        )
        if entry is None or identifier == "COMM-002":
            return False
        return (
            entry["scope"] == "root"
            and entry["classification"] == "kv_static"
            and entry["automation"] == "O"
            and entry["action"] == "IMPLEMENT"
            and entry["disposition"] == "ACTIVE_KEEP"
            and entry["consumer_status"] == "DECLARED"
            and bool(entry["consumers"])
            and entry["source_path"] is not None
            and not any(
                entry["lifecycle"][lane] == "CONFIRMED"
                for lane in LIFECYCLE_FIELDS - {"declared"}
            )
        )
    except (ValueError, TypeError, KeyError):
        return False


def generation_binding_allowed(catalog, identifier, source_path, env_key, automation):
    """Eligibility binds exact public metadata; it grants no private mutation."""
    if not generation_allowed(catalog, identifier):
        return False
    entry = next(item for item in catalog["entries"] if item["id"] == identifier)
    expected = (entry["source_path"], entry["env_key"], entry["automation"])
    actual = (source_path, env_key, automation)
    return all(
        type(left) is type(right) and left == right
        for left, right in zip(expected, actual, strict=True)
    )


def _destination_cell(plan):
    if plan["status"] == "DEPLOYED":
        return f"{plan['mount']}/{plan['kv_path']}#{plan['field']}"
    return plan["kv_path"] or "BLOCKED_P01"


def render_views(catalog):
    validate_catalog(catalog)
    lines = [
        "# P02 공개 메타데이터 staging view",
        "",
        "| ID | 자동화 | 유형 | 값 | .env 변수 | 파일 경로 | 원본기록일 | 용도 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in catalog["entries"]:
        cells = [
            entry["id"],
            entry["automation"],
            entry["value_type"],
            "(비어있음)",
            entry["env_key"] or "-",
            entry["source_path"] or "-",
            entry["source_recorded_at"],
            entry["purpose"],
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.extend(["", "| Retired ID | Canonical ID |", "| --- | --- |"])
    lines.extend(
        "| " + item["id"] + " | " + item["canonical_id"] + " |"
        for item in catalog["aliases"]
    )
    summary = {
        "schema_version": catalog["schema_version"],
        "owner_task": catalog["owner_task"],
        "entries": [
            {
                "id": entry["id"],
                "classification": entry["classification"],
                "consumer_status": entry["consumer_status"],
                "disposition": entry["disposition"],
            }
            for entry in catalog["entries"]
        ],
        "aliases": catalog["aliases"],
    }
    readme = """# P02 공개 메타데이터 뷰

이 폴더는 secret-catalog.json에서 생성한 공개 메타데이터 staging 산출물을 보관합니다.
SENSITIVE_ENV_VARS.md.example은 기존 표 형태를 유지하며 실제 값은 포함하지 않습니다.
SENSITIVE_ENV_VARS.md는 값 열 없이 분류·계획·소유자·수명주기·근거를 보여 줍니다.
이 파일명은 staging 안에서만 사용하며 실제 private 메타데이터 파일을 읽거나 변경하지 않습니다.
secret-catalog-summary.json은 분류와 보존 판단을 요약합니다.
원본기록일은 공개 원본 표의 날짜이며 검토·회전·복구 확인 시각이 아닙니다.
근거 경로는 확인 대상 메타데이터이며 경로만으로 실제 런타임 검증을 인정하지 않습니다.
검사는 secret-catalog.py check-views로 수행합니다. 원본 갱신은 owning Task에서 검토합니다.
이 산출물은 실제 발급·이관·전달·회전·복구·서비스 사용의 증거가 아닙니다.
운영자가 상위 .agent-work 폴더와 README.md를 먼저 준비해야 합니다.
"""
    return {
        VIEW_NAMES[0]: ("\n".join(lines) + "\n").encode(),
        VIEW_NAMES[1]: (
            json.dumps(summary, ensure_ascii=True, indent=2) + "\n"
        ).encode(),
        VIEW_NAMES[2]: readme.encode(),
        VIEW_NAMES[3]: _local_view(catalog),
    }


def _local_view(catalog):
    lines = [
        "# P02 값 없는 로컬 staging 메타데이터",
        "",
        "| ID | 분류 | 원본 경로 | 계획 KV | 작업 | 소유자 | 수명주기 | 근거 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in catalog["entries"]:
        lifecycle = "; ".join(
            f"{lane}:{state}" for lane, state in sorted(entry["lifecycle"].items())
        )
        evidence = [entry["evidence_ref"]] + [
            f"{lane}:{reference}"
            for lane, reference in sorted(entry["runtime_evidence"].items())
            if reference is not None
        ]
        cells = [
            entry["id"],
            entry["classification"],
            entry["source_path"] or "-",
            _destination_cell(entry["destination_plan"]),
            entry["action"],
            entry["owner"],
            lifecycle,
            "; ".join(evidence),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return ("\n".join(lines) + "\n").encode()


def load_catalog(root):
    path, expected, environment = _root(root)
    inputs = {
        relative: _public_bytes(path, relative, environment)
        for relative in (CATALOG_PATH, SCHEMA_PATH, METADATA_PATH, SUPPORT_PATH)
    }
    catalog = json.loads(inputs[CATALOG_PATH], object_pairs_hook=_unique_object)
    schema = json.loads(inputs[SCHEMA_PATH], object_pairs_hook=_unique_object)
    support = json.loads(inputs[SUPPORT_PATH], object_pairs_hook=_unique_object)
    if not isinstance(support, dict):
        raise CatalogError("invalid_support_matrix")
    validate_catalog(catalog, schema)
    public = parse_public_table(inputs[METADATA_PATH])
    actual = [
        {field: entry[field] for field in METADATA_FIELDS}
        for entry in catalog["entries"]
    ]

    def by_id(rows):
        return {row["id"]: row for row in rows}

    if (
        by_id(actual) != by_id(public["entries"])
        or catalog["aliases"] != public["aliases"]
    ):
        raise CatalogError("catalog_public_source_drift")
    if root_identity(path) != expected:
        raise CatalogError("repository_identity_changed")
    return catalog


def write_views(root, output=None):
    path, expected, _ = _root(root)
    _output(path, output)
    views = render_views(load_catalog(path))
    with ExitStack() as stack:
        fd = _staging_fd(path, stack, create=True)
        for name in views:
            _target_safe(fd, name, required_mode=0o600)
        if root_identity(path) != expected:
            raise CatalogError("repository_identity_changed")
        for index, (name, data) in enumerate(views.items()):
            temporary = f".p02-{os.getpid()}-{index}"
            opened = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=fd,
            )
            try:
                with os.fdopen(opened, "wb") as stream:
                    os.fchmod(stream.fileno(), 0o600)
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                _target_safe(fd, name, required_mode=0o600)
                os.replace(temporary, name, src_dir_fd=fd, dst_dir_fd=fd)
                os.fsync(fd)
            finally:
                try:
                    os.unlink(temporary, dir_fd=fd)
                except FileNotFoundError:
                    pass
    return tuple(views)


def check_views(root, output=None):
    path, expected, _ = _root(root)
    _output(path, output)
    views = render_views(load_catalog(path))
    try:
        with ExitStack() as stack:
            fd = _staging_fd(path, stack, create=False)
            for name, expected_bytes in views.items():
                _target_safe(fd, name, required_mode=0o600)
                if _read_file(fd, name) != expected_bytes:
                    return False
    except FileNotFoundError:
        return False
    if root_identity(path) != expected:
        raise CatalogError("repository_identity_changed")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "render", "check-views"):
        commands.add_parser(command)
    generation = commands.add_parser("check-generation")
    generation.add_argument("identifier")
    args = parser.parse_args(argv)
    try:
        if args.command == "render":
            names = write_views(args.root)
            print(
                json.dumps(
                    {"result": "STAGING_RENDERED", "files": names}, ensure_ascii=True
                )
            )
        elif args.command == "check-views":
            if not check_views(args.root):
                print("P02_VIEW_DRIFT")
                return 2
            print("P02_VIEWS_MATCH")
        else:
            catalog = load_catalog(args.root)
            if args.command == "check-generation" and not generation_allowed(
                catalog, args.identifier
            ):
                print("P02_GENERATION_BLOCKED")
                return 2
            print(
                json.dumps(
                    {
                        "result": "P02_METADATA_VALID",
                        "entries": len(catalog["entries"]),
                        "aliases": len(catalog["aliases"]),
                    },
                    ensure_ascii=True,
                )
            )
        return 0
    except (ValueError, TypeError, KeyError, OSError, ImportError):
        print("P02_METADATA_BLOCKED", file=sys.stderr)
        return 2
