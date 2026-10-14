"""Produce the W3a inputs that protected-semantic-restore.py consumes (RUN-0085).

Operations, each writing new owner-private files and never overwriting:

- lease-start: record when writers stopped, before the W3 snapshot is saved.
- lease-bind: after W3, write the quiescence lease bound to the snapshot.
- bundle: extract the seven Agent bundle files from one reviewed commit.
- security-receipt: freeze the OpenBao rows of the security ledger.
- contract: assemble and self-check the restore contract.

The restore program re-validates every input; these producers hold no secret
and print only paths and SHA-256 values.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import secrets
import stat
import subprocess
import sys
from pathlib import Path

HEX64 = re.compile(r"[a-f0-9]{64}")
REVISION = re.compile(r"[a-f0-9]{40}")
SOURCE = "infra/03-security/openbao/"
BUNDLE = (
    "scripts/start-agent.sh",
    "scripts/health-agent.sh",
    "config/agent.hcl",
    "config/templates/keycloak_admin_password.ctmpl",
    "config/templates/grafana_admin_password.ctmpl",
    "config/templates/keycloak_admin_password_version.ctmpl",
    "config/templates/grafana_admin_password_version.ctmpl",
)
LEASE_PENDING = "lease.pending.json"
LEASE = "quiescence-lease.json"
MAX_LEASE_MINUTES = 90
# Writers stop just before the save; a longer gap is not one quiescent window.
MAX_START_TO_SAVE = datetime.timedelta(minutes=30)
COMPOSE = SOURCE + "docker-compose.yml"
CANDIDATE = re.compile(
    r"^\s*image:\s*(hy-home/openbao:[^\s@]+@sha256:[a-f0-9]{64})\s*$", re.M
)
LEDGER_SERVICES = ("openbao", "openbao-agent")
LEDGER = "infra/09-platform-ops/security-updates/update-ledger.json"


class Blocked(Exception):
    """A sanitized precondition failure; nothing was overwritten."""


def load_restore():
    sys.dont_write_bytecode = True  # Never leave .pyc next to the manifest copy.
    path = Path(__file__).absolute().with_name("protected-semantic-restore.py")
    spec = importlib.util.spec_from_file_location("_restore_inputs_target", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def private_directory(path):
    path = Path(path)
    info = os.lstat(path)
    if (
        not path.is_absolute()
        or not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.getuid()
        or stat.S_IMODE(info.st_mode) != 0o700
    ):
        raise Blocked()
    return path


def write_new(path, raw, mode=0o600):
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, mode
    )
    try:
        os.fchmod(descriptor, mode)
        view = memoryview(raw)
        while view:
            view = view[os.write(descriptor, view) :]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return hashlib.sha256(raw).hexdigest()


def read_regular(path, maximum=1024 * 1024):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or not 1 <= info.st_size <= maximum:
            raise Blocked()
        return os.read(descriptor, maximum + 1), info
    finally:
        os.close(descriptor)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def utc_now():
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0)


def lease_start(directory, now=None):
    directory = private_directory(directory)
    moment = now or utc_now()
    pending = {
        "lease_id": secrets.token_hex(16),
        "started_at_utc": moment.isoformat(),
    }
    write_new(directory / LEASE_PENDING, canonical(pending))
    return pending["lease_id"]


def lease_bind(directory, snapshot_receipt, minutes, now=None):
    directory = private_directory(directory)
    if type(minutes) is not int or not 1 <= minutes <= MAX_LEASE_MINUTES:
        raise Blocked()
    pending = json.loads(read_regular(directory / LEASE_PENDING, 4096)[0])
    receipt = json.loads(read_regular(snapshot_receipt, 65536)[0])
    started = datetime.datetime.fromisoformat(pending["started_at_utc"])
    saved = datetime.datetime.fromisoformat(receipt["saved_at_utc"])
    # Not truncated: the receipt's save time keeps microseconds.
    moment = now or datetime.datetime.now(datetime.UTC)
    # The lease must cover the save: a snapshot taken before writers stopped is
    # not quiescent, and one from the future is not this attempt's.
    if (
        started > saved
        or saved - started > MAX_START_TO_SAVE
        or saved > moment
        or not HEX64.fullmatch(receipt["sha256"])
    ):
        raise Blocked()
    lease = {
        "schema_version": 1,
        "lease_id": pending["lease_id"],
        "started_at_utc": pending["started_at_utc"],
        "expires_at_utc": (moment + datetime.timedelta(minutes=minutes)).isoformat(),
        "released_at_utc": None,
        "snapshot_sha256": receipt["sha256"],
    }
    return pending["lease_id"], write_new(directory / LEASE, canonical(lease))


class Repository:
    """The checkout and its .git held by descriptor, as install-renderer-issuer.sh."""

    def __init__(self, path, revision):
        path = Path(path)
        if not REVISION.fullmatch(revision) or path.resolve(strict=True) != path:
            raise Blocked()
        self.path, self.revision = path, revision
        self.root = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.git = None
        try:
            self.git = os.open(
                ".git", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=self.root
            )
            self.held = [os.fstat(fd) for fd in (self.root, self.git)]
            if any(info.st_uid != os.getuid() for info in self.held):
                raise Blocked()
            verified = self.run("rev-parse", "--verify", revision + "^{commit}")
            if verified.strip() != revision.encode():
                raise Blocked()
        except BaseException:
            self.close()
            raise

    def run(self, *arguments):
        done = subprocess.run(
            [
                "/usr/bin/git",
                "--no-pager",
                "--git-dir=/proc/self/fd/" + str(self.git),
                *arguments,
            ],
            env={
                "PATH": "/usr/bin:/bin",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_NO_REPLACE_OBJECTS": "1",
            },
            pass_fds=(self.git,),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=10,
            check=False,
        )
        if done.returncode:
            raise Blocked()
        return done.stdout

    def blob(self, path, maximum=100000):
        raw = self.run("show", "--no-textconv", self.revision + ":" + path)
        if not 1 <= len(raw) <= maximum:
            raise Blocked()
        return raw

    def recheck(self):
        for named, held in zip((self.path, self.path / ".git"), self.held, strict=True):
            current = os.lstat(named)
            if not stat.S_ISDIR(current.st_mode) or (
                current.st_dev,
                current.st_ino,
                current.st_uid,
            ) != (held.st_dev, held.st_ino, held.st_uid):
                raise Blocked()

    def close(self):
        for descriptor in (self.git, self.root):
            if descriptor is not None:
                os.close(descriptor)
        self.git = self.root = None


def bundle(repository, revision, target):
    target = Path(target)
    if not REVISION.fullmatch(revision) or os.path.lexists(target):
        raise Blocked()
    private_directory(target.parent)
    held = Repository(repository, revision)
    try:
        blobs = {name: held.blob(SOURCE + name) for name in BUNDLE}
        held.recheck()
    finally:
        held.close()
    target.mkdir(mode=0o700)
    for name, blob in blobs.items():
        for parent in reversed((target / name).relative_to(target).parents[:-1]):
            (target / parent).mkdir(mode=0o700, exist_ok=True)
        write_new(target / name, blob, 0o400)
    receipt = {
        "source_revision": revision,
        "sha256": {
            name: hashlib.sha256(blob).hexdigest() for name, blob in blobs.items()
        },
    }
    return write_new(target / "source-receipt.json", canonical(receipt), 0o400)


def security_receipt(repository, revision, output):
    # Read at the approved revision, not from a working-tree or copied file.
    held = Repository(repository, revision)
    try:
        raw = held.blob(LEDGER, 16 * 1024 * 1024)
        held.recheck()
    finally:
        held.close()
    rows = [
        entry
        for entry in json.loads(raw)["entries"]
        if entry.get("service") in LEDGER_SERVICES
    ]
    if sorted(row["service"] for row in rows) != sorted(LEDGER_SERVICES):
        raise Blocked()
    receipt = {
        "schema_version": 1,
        "source_revision": revision,
        "ledger_sha256": hashlib.sha256(raw).hexdigest(),
        "rows": sorted(rows, key=lambda row: row["service"]),
    }
    return write_new(Path(output), canonical(receipt))


def candidate_reference(repository, revision):
    """The one owned server image Compose pins at the approved commit."""
    held = Repository(repository, revision)
    try:
        compose = held.blob(COMPOSE, 1024 * 1024).decode()
        held.recheck()
    finally:
        held.close()
    found = set(CANDIDATE.findall(compose))
    if len(found) != 1:
        raise Blocked()
    return found.pop()


def image_id(reference):
    # --platform would name a multi-arch tag's platform manifest under the
    # containerd store; read the local image ID and check its platform.
    done = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            "--format",
            "{{.Id}} {{.Os}}/{{.Architecture}}",
            reference,
        ],
        env={"PATH": "/usr/bin:/bin"},  # The same Docker endpoint the restore uses.
        capture_output=True,
        timeout=30,
        check=False,
    )
    value, _space, platform = done.stdout.decode().strip().partition(" ")
    if (
        done.returncode
        or platform != "linux/amd64"
        or not re.fullmatch(r"sha256:[a-f0-9]{64}", value)
    ):
        raise Blocked()
    return value


def sha256_file(path):
    return hashlib.sha256(read_regular(path, 32 * 1024 * 1024)[0]).hexdigest()


def receipt_revision(path, revision):
    raw = read_regular(path, 65536)[0]  # One read: check and hash the same bytes.
    value = json.loads(raw)
    if not isinstance(value, dict) or value.get("source_revision") != revision:
        raise Blocked()
    return hashlib.sha256(raw).hexdigest()


def contract(options, restore=None, inspect=image_id, reference=candidate_reference):
    restore = restore or load_restore()
    _parent, archive, execution = restore.load_dependencies()
    receipt_raw, _ = read_regular(options.snapshot_receipt, 65536)
    receipt = json.loads(receipt_raw)
    descriptor = os.open(options.snapshot, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        try:
            validation = archive.validate_archive(descriptor)
        except archive.ArchiveBlocked:
            raise Blocked() from None
    finally:
        os.close(descriptor)
    if (
        validation["sha256"] != receipt.get("sha256")
        or validation["size"] != receipt.get("size")
        or (info.st_dev, info.st_ino) != (receipt.get("dev"), receipt.get("ino"))
    ):
        raise Blocked()
    lease_raw, _ = read_regular(options.lease, 8192)
    lease = json.loads(lease_raw)
    if lease.get("snapshot_sha256") != validation["sha256"]:
        raise Blocked()
    helper = Path(options.helper_directory)
    bundle_directory = Path(options.bundle)
    candidate = reference(options.repository, options.revision)
    dev, ino, uid, gid = restore.PARENT_IDENTITY
    value = {
        "schema_version": 1,
        "attempt": restore.ATTEMPT,
        "target": str(restore.TARGET),
        "parent": {"dev": dev, "ino": ino, "uid": uid, "gid": gid},
        "snapshot": {
            "sha256": validation["sha256"],
            "receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "dev": info.st_dev,
            "ino": info.st_ino,
            "size": validation["size"],
            "cluster_id": receipt.get("cluster_id"),
            "version": receipt.get("version"),
            "raft_index": validation["metadata"]["Index"],
            "raft_term": validation["metadata"]["Term"],
        },
        "quiescence": {
            "lease_id": lease.get("lease_id"),
            "lease_sha256": hashlib.sha256(lease_raw).hexdigest(),
        },
        "candidate": {
            "reference": candidate,
            "image_id": inspect(candidate),
            "version": restore.OWNED_VERSION,
        },
        "renderer": {
            "helper": str(helper / "issue-renderer-secret-id.sh"),
            "bundle": str(bundle_directory),
            "revision": options.revision,
            # Both receipts must name this revision, or restore preflight refuses.
            "helper_receipt_sha256": receipt_revision(
                helper / "source-receipt.json", options.revision
            ),
            "bundle_receipt_sha256": receipt_revision(
                bundle_directory / "source-receipt.json", options.revision
            ),
        },
        "security_receipt_sha256": sha256_file(options.security_receipt),
    }
    output = Path(options.output)
    digest = write_new(output, canonical(value))
    # Self-check with the consumer's own schema validation.
    try:
        _value, held = restore._contract(output, digest, execution)
        held.close()
    except Exception:
        os.unlink(output)  # A refused contract must not be left for W3a.
        raise Blocked() from None
    return digest


class Parser(argparse.ArgumentParser):
    def error(self, _message):
        raise Blocked()


def main(arguments=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("lease-start").add_argument("--directory", required=True)
    bind = commands.add_parser("lease-bind")
    for name in ("directory", "snapshot-receipt"):
        bind.add_argument("--" + name, required=True)
    bind.add_argument("--minutes", type=int, required=True)
    extract = commands.add_parser("bundle")
    for name in ("repository", "revision", "target"):
        extract.add_argument("--" + name, required=True)
    frozen = commands.add_parser("security-receipt")
    for name in ("repository", "revision", "output"):
        frozen.add_argument("--" + name, required=True)
    assemble = commands.add_parser("contract")
    for name in (
        "output",
        "snapshot",
        "snapshot-receipt",
        "lease",
        "helper-directory",
        "bundle",
        "revision",
        "security-receipt",
        "repository",
    ):
        assemble.add_argument("--" + name, required=True)
    try:
        options = parser.parse_args(arguments)
        if options.operation == "lease-start":
            print("LEASE_STARTED " + lease_start(options.directory))
        elif options.operation == "lease-bind":
            lease_id, digest = lease_bind(
                options.directory, options.snapshot_receipt, options.minutes
            )
            print("LEASE_BOUND " + lease_id + " " + digest)
        elif options.operation == "bundle":
            digest = bundle(options.repository, options.revision, options.target)
            print("BUNDLE_WRITTEN " + digest)
        elif options.operation == "security-receipt":
            digest = security_receipt(
                options.repository, options.revision, options.output
            )
            print("SECURITY_RECEIPT " + digest)
        else:
            if not REVISION.fullmatch(options.revision):
                raise Blocked()
            print("CONTRACT_WRITTEN " + contract(options))
        return 0
    except Exception:
        print("BLOCKED: no input written beyond what already exists", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
