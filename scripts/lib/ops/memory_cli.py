"""Argument handling for the sanctioned shared-memory writer."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from scripts.lib.ops.memory_backup import BackupError
from scripts.lib.ops.memory_capacity import CapacityError, MemoryCapacity
from scripts.lib.ops.memory_search import search_records


def _parser(memory):
    parser = argparse.ArgumentParser(description=memory.__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    get = commands.add_parser("get")
    get.add_argument("memory_id")
    get.add_argument("--historical", action="store_true")
    history = commands.add_parser("history")
    history.add_argument("memory_id")
    history.add_argument("--limit", type=int, default=10)
    listing = commands.add_parser("list")
    listing.add_argument("--tier", choices=memory.TIERS)
    listing.add_argument("--all", action="store_true")
    put = commands.add_parser("put")
    put.add_argument("memory_id")
    put.add_argument("--expected-revision", type=int, required=True)
    put.add_argument("--tier", choices=memory.TIERS, required=True)
    put.add_argument("--owner", required=True)
    put.add_argument("--source-ref", action="append", default=[])
    put.add_argument("--sensitivity", choices=memory.SENSITIVITY, default="internal")
    put.add_argument("--request-key")
    put.add_argument(
        "--review-state", choices=memory.REVIEW_STATES, default="candidate"
    )
    put.add_argument("--domain-id")
    eligibility = commands.add_parser("set-eligibility")
    eligibility.add_argument("memory_id")
    eligibility.add_argument("--expected-revision", type=int, required=True)
    eligibility.add_argument("--owner", required=True)
    eligibility.add_argument("eligibility", choices=memory.ELIGIBILITY)
    commands.add_parser("usage")
    commands.add_parser("export")
    backup = commands.add_parser("backup")
    backup.add_argument("--output", type=Path, required=True)
    restore = commands.add_parser("restore")
    restore.add_argument("--input", type=Path, required=True)
    search = commands.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    capacity = commands.add_parser("capacity").add_subparsers(
        dest="capacity_command", required=True
    )
    capacity.add_parser("status")
    reconcile = capacity.add_parser("reconcile")
    reconcile.add_argument("--expected-generation", type=int)
    reconcile.add_argument(
        "--legacy-output",
        type=Path,
        action="append",
        default=[],
        help="Known pre-upgrade backup output; metadata is verified without reading its body",
    )
    coordinated = commands.add_parser("backup-run")
    coordinated.add_argument("--target", choices=("state", "offsite"), required=True)
    coordinated.add_argument("--request-key")
    return parser


def readonly(memory, path):
    memory._refuse_symlink(path.parent)
    memory._refuse_symlink(path)
    connection = sqlite3.connect(path.absolute().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    return connection


def _dispatch(memory, connection, args, path):
    command = args.command
    if command == "get":
        result = memory.get(
            connection, args.memory_id, current_only=not args.historical
        )
        if result is None:
            raise memory.MemoryStoreError(
                1, "MEMORY_NOT_FOUND: no matching current record"
            )
        return result
    if command == "history":
        return memory.history(connection, args.memory_id, args.limit)
    if command in {"list", "export", "search"}:
        records = memory.current_records(
            connection,
            getattr(args, "tier", None),
            command == "export" or getattr(args, "all", False),
        )
        return (
            search_records(records, args.query, args.limit)
            if command == "search"
            else records
        )
    if command == "usage":
        try:
            aggregate = MemoryCapacity(path).status()
        except CapacityError:
            aggregate = {
                "inventory_state": "unverified",
                "reason": "capacity metadata unavailable; growth refused",
            }
        return {**memory.usage(connection), "aggregate_capacity": aggregate}
    if command == "backup":
        memory.backup(connection, args.output)
        return {"backup": args.output.as_posix()}
    identity = connection.execute(
        "SELECT workspace_id FROM revisions LIMIT 1"
    ).fetchone()
    workspace_id = identity[0] if identity else path.parent.parent.as_posix()
    if command == "put":
        revision = memory.put(
            connection,
            memory_id=args.memory_id,
            expected_revision=args.expected_revision,
            workspace_id=workspace_id,
            tier=args.tier,
            owner=args.owner,
            body=sys.stdin.read(memory.MAX_BODY_BYTES + 1),
            source_refs=[
                json.loads(ref) if ref.startswith("{") else ref
                for ref in args.source_ref
            ],
            sensitivity=args.sensitivity,
            request_key=args.request_key,
            review_state=args.review_state,
            domain_id=args.domain_id,
        )
    else:
        row = memory.get(connection, args.memory_id)
        if row is None:
            raise memory.MemoryStoreError(
                memory.EXIT_CONFLICT, "MEMORY_REVISION_CONFLICT: record missing"
            )
        revision = memory.put(
            connection,
            memory_id=args.memory_id,
            expected_revision=args.expected_revision,
            workspace_id=workspace_id,
            tier=str(row["tier"]),
            owner=args.owner,
            body=str(row["body"]),
            source_refs=list(row["source_refs"]),
            sensitivity=str(row["sensitivity"]),
            eligibility=args.eligibility,
            review_state="withdrawn"
            if args.eligibility == "ineligible"
            else "candidate",
            domain_id=row["provenance"]["domain_id"],
        )
    return {"memory_id": args.memory_id, "revision": revision}


def run(argv, memory):
    args = _parser(memory).parse_args(argv)
    connection = None
    try:
        path = memory.store_path()
        if args.command == "capacity":
            manager = MemoryCapacity(path)
            if args.capacity_command == "status":
                result = manager.status()
            else:
                from scripts.lib.ops.memory_backup import reconcile_backups

                result = reconcile_backups(
                    path,
                    expected_generation=args.expected_generation,
                    legacy_outputs=tuple(args.legacy_output),
                )
        elif args.command == "backup-run":
            from scripts.lib.ops.memory_backup import run_backup

            result = run_backup(path, args.target, request_key=args.request_key)
        elif args.command == "restore":
            memory.restore(args.input, path)
            result = {"restored": True}
        else:
            writing = args.command in {"put", "set-eligibility"}
            if (
                writing
                and MemoryCapacity(path).status()["inventory_state"] != "complete"
            ):
                raise CapacityError()
            connection = memory.connect(path) if writing else readonly(memory, path)
            result = _dispatch(memory, connection, args, path)
    except (memory.MemoryStoreError, CapacityError) as error:
        print(error, file=sys.stderr)
        if getattr(error, "details", None):
            print(json.dumps(error.details, sort_keys=True), file=sys.stderr)
        return error.code
    except BackupError as error:
        print(
            "MEMORY_BACKUP_REFUSED: metadata or backup operation failed; reservation retained",
            file=sys.stderr,
        )
        metric = getattr(error, "offsite_repo_bytes", None)
        if type(metric) is int and metric >= 0:
            print(json.dumps({"result": "FAIL", "offsite_repo_bytes": metric}))
        return error.code
    except (OSError, sqlite3.Error, ValueError, TypeError, RecursionError) as error:
        print(f"MEMORY_UNAVAILABLE: {type(error).__name__}", file=sys.stderr)
        return memory.EXIT_UNAVAILABLE
    finally:
        if connection is not None:
            connection.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
