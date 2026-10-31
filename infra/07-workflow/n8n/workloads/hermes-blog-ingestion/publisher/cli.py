"""Staging, status and bounded dispatch CLI for the Hermes Publisher.

dispatch performs at most one operation per record per invocation; the caller's
timer re-invokes it, so retry stays here and never in n8n. Credentials arrive
only through a private file, never argv, environment or output.
"""

import argparse
import hashlib
import json
import os
import sqlite3
import stat
from pathlib import Path

from . import trust
from .candidates import EXPORT_NAME, JOBS, load_candidate, load_validator
from .delivery import TransportFailure, process_one
from .files import InputError, open_directory, safe_read
from .gateway_adapter import DESTINATION, GatewayAdapter
from .gateway_transport import GatewayReplayTransport
from .http_transport import HttpTransport
from .outbox import Outbox, OutboxError

OPEN_STATES = ("awaiting_contract", "pending", "sending", "uncertain")
# Outlasts the workflow executionTimeout (30 s), which outlasts its Gateway
# request (20 s), and stays under the Traefik v3 default readTimeout (60 s).
# Queue wait beyond the margin ends uncertain and reconciles idempotently.
HTTP_TIMEOUT = 45


def _scan(args, box):
    validator = load_validator(args.validator, args.validator_sha256)
    counts = dict(staged=0, duplicate=0, conflict=0, rejected=0)
    evidence_root = getattr(args, "evidence_root", None)
    if evidence_root is not None:
        counts["evidence_stored"] = 0
        with open_directory(evidence_root):
            pass
    with open_directory(args.exports):
        pass
    for job in JOBS:
        try:
            with open_directory(args.exports / job) as descriptor:
                names = []
                with os.scandir(descriptor) as entries:
                    for entry in entries:
                        if EXPORT_NAME.fullmatch(entry.name):
                            names.append(entry.name)
                            if len(names) > 1000:
                                raise InputError("scan_limit")
        except InputError as error:
            if str(error) == "directory_missing":
                continue
            raise
        for name in sorted(names):
            try:
                snapshot = load_candidate(
                    args.exports, job, name, args.source_root, args.item_root, validator
                )
                evidence = signature = None
                if evidence_root is not None:
                    evidence_name = (
                        hashlib.sha256(
                            (job + "\0" + snapshot.run_id).encode("ascii")
                        ).hexdigest()
                        + ".json"
                    )
                    evidence = safe_read(evidence_root, evidence_name)
                    if not evidence:
                        raise InputError("empty_evidence")
                    # The producer writes the detached signature before the
                    # evidence file; an absent signature stays unauthenticated.
                    if os.path.lexists(evidence_root / (evidence_name + ".sig")):
                        signature = safe_read(
                            evidence_root, evidence_name + ".sig", limit=4096
                        )
                outcome = (
                    box.stage(snapshot)
                    if evidence is None
                    else box.stage_with_unverified_evidence(
                        snapshot, evidence, signature
                    )
                )
                if evidence is not None and outcome != "conflict":
                    counts["evidence_stored"] += 1
                counts[outcome] += 1
            except (InputError, OutboxError):
                counts["rejected"] += 1
    return counts


def _auth(path):
    """Read one 'Name: value' header from a private, owner-only regular file."""
    path = Path(path)
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
    with open_directory(path.parent) as directory:
        parent = os.fstat(directory)
        descriptor = os.open(path.name, flags, dir_fd=directory)
    try:
        # Check the descriptor actually read, so a swapped path cannot pass.
        info = os.fstat(descriptor)
        if (
            parent.st_uid != os.getuid()
            or stat.S_IMODE(parent.st_mode) & 0o022
            or not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) & 0o077
            or info.st_nlink != 1
            or info.st_size > 4096
        ):
            raise InputError("credential_permissions")
        raw = os.read(descriptor, 4097)
    finally:
        os.close(descriptor)
    try:
        name, value = raw.decode("ascii").strip().split(":", 1)
    except (UnicodeError, ValueError):
        raise InputError("credential_format") from None
    return name.strip(), value.strip()


def _dispatch(args, box):
    counts = {}
    transport = None
    for key in box.keys():
        row = box.get(key)
        if row["status"] not in OPEN_STATES:
            continue
        try:
            # The same trust decision process_one, bind_request and the replay
            # boundary consume; it precedes any credential I/O.
            authorization = trust.authorize(box, key)
            if authorization is None:
                raise trust.TrustError("evidence_missing")
            times = authorization.times
            generated = json.loads(row["candidate"])["generated_at"]
            adapter = GatewayAdapter(times.scheduled_at, generated, times.collected_at)
        except (trust.TrustError, OutboxError, KeyError, ValueError):
            # A possibly durable in-flight record must stay visible to operators.
            name = (
                "uncertain" if row["status"] in ("sending", "uncertain") else "blocked"
            )
            counts[name] = counts.get(name, 0) + 1
            continue
        if transport is None:
            # Configuration and credential errors reject the whole run.
            try:
                http = HttpTransport(
                    endpoint=args.endpoint,
                    destination=DESTINATION,
                    auth=_auth(args.auth_header_file),
                    timeout=HTTP_TIMEOUT,
                    content_type="application/json",
                )
            except TransportFailure:
                raise InputError("credential_rejected") from None
            transport = GatewayReplayTransport(
                box, http, allow_idempotent_replay=args.allow_replay
            )
        result = process_one(box, key, adapter, transport)
        counts[result] = counts.get(result, 0) + 1
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    stage = sub.add_parser("stage")
    for name in ("exports", "source-root", "item-root", "validator"):
        stage.add_argument("--" + name, type=Path, required=True)
    stage.add_argument("--validator-sha256", required=True)
    stage.add_argument("--evidence-root", type=Path)
    stage.add_argument("--outbox", type=Path, required=True)
    status = sub.add_parser("status")
    status.add_argument("--outbox", type=Path, required=True)
    dispatch = sub.add_parser("dispatch")
    dispatch.add_argument("--outbox", type=Path, required=True)
    dispatch.add_argument("--endpoint", required=True)
    dispatch.add_argument("--auth-header-file", type=Path, required=True)
    dispatch.add_argument("--allow-replay", action="store_true")
    sub.add_parser("verify-install")
    args = parser.parse_args(argv)
    if args.command == "verify-install":
        # Run as the dedicated account: proves `python3 -I` loads a protected
        # install and parses the key store, without printing any key.
        try:
            keys = len(trust.store_entries())
        except trust.TrustError as error:
            print(json.dumps({"error": str(error)}))
            return 1
        print(json.dumps({"keys": keys, "runtime": "protected"}, sort_keys=True))
        return 0
    box = None
    try:
        box = Outbox(args.outbox)
        if args.command == "stage":
            result = _scan(args, box)
        elif args.command == "dispatch":
            result = _dispatch(args, box)
        else:
            result = box.counts()
        print(json.dumps(result, sort_keys=True))
        failed = ("rejected", "conflict")
        if args.command == "dispatch":
            failed = ("failed", "uncertain")
        return 1 if any(result.get(name, 0) for name in failed) else 0
    except (ValueError, OSError, sqlite3.Error):
        print('{"error":"operation_rejected"}')
        return 1
    finally:
        if box is not None:
            box.close()


if __name__ == "__main__":
    raise SystemExit(main())
