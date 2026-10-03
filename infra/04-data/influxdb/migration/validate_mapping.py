"""Validate an explicit Influx-to-PostgreSQL mapping; never connect to a source."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
WRITER_ID = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
TYPES = {"boolean", "float", "integer", "string", "unsigned"}
PRECISIONS = {"ns", "us", "ms", "s"}
REQUIRED = {
    "schema_version",
    "measurement",
    "tags",
    "fields",
    "source_precision",
    "target_timestamp",
    "retain_source_ns",
    "retention",
    "query",
    "writers",
}


def _name(value: object) -> bool:
    return isinstance(value, str) and bool(NAME.fullmatch(value))


def validate(value: object) -> dict:
    if not isinstance(value, dict) or set(value) != REQUIRED:
        raise ValueError("mapping fields must match schema version 1 exactly")
    if value["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    if not _name(value["measurement"]) or not _name(value["target_timestamp"]):
        raise ValueError("measurement and target timestamp need safe names")
    if value["source_precision"] not in PRECISIONS:
        raise ValueError("source timestamp precision must be explicit")
    if type(value["retain_source_ns"]) is not bool or (
        value["source_precision"] == "ns" and not value["retain_source_ns"]
    ):
        raise ValueError(
            "nanosecond precision requires original timestamp preservation"
        )
    if value["retention"] != "source-unchanged":
        raise ValueError("source retention must remain unchanged")
    if not isinstance(value["query"], str) or not value["query"].strip():
        raise ValueError("query reference is required")
    if (
        not isinstance(value["writers"], list)
        or not value["writers"]
        or not all(
            isinstance(x, str) and WRITER_ID.fullmatch(x) for x in value["writers"]
        )
    ):
        raise ValueError("known writer identifiers are required")
    tags, fields = value["tags"], value["fields"]
    if not isinstance(tags, list) or not all(_name(x) for x in tags):
        raise ValueError("tags need explicit safe names")
    if not isinstance(fields, list) or not fields:
        raise ValueError("at least one typed field is required")
    for field in fields:
        if not isinstance(field, dict) or set(field) != {"name", "type", "unit"}:
            raise ValueError("field needs name, type and unit")
        if (
            not _name(field["name"])
            or field["type"] not in TYPES
            or not isinstance(field["unit"], str)
            or not field["unit"].strip()
        ):
            raise ValueError("invalid field name, type or unit")
    names = [value["target_timestamp"], *tags, *(f["name"] for f in fields)]
    if len(names) != len(set(names)) or len(value["writers"]) != len(
        set(value["writers"])
    ):
        raise ValueError("mapping names and writers must be unique")
    return dict(value)


def empty_source_result(mapping: object, row_count: int) -> dict:
    checked = validate(mapping)
    if type(row_count) is not int or row_count != 0:
        raise ValueError("NO_DATA route requires a verified zero row count")
    return {
        "status": "NO_DATA",
        "measurement": checked["measurement"],
        "source_rows": 0,
        "target_rows": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument(
        "--verified-empty",
        action="store_true",
        help="record a separately verified zero-row source",
    )
    args = parser.parse_args()
    mapping = validate(json.loads(args.mapping.read_text(encoding="utf-8")))
    result = (
        empty_source_result(mapping, 0)
        if args.verified_empty
        else {"status": "MAPPING_VALID", "measurement": mapping["measurement"]}
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
