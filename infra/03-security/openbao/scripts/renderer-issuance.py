"""Durable, secret-free renderer issuance; a journal records uncertainty, not success.

Journal v3 phases: prepared -> issuing -> delivered -> verified -> revoking ->
complete, or rolled_back. The old Agent token lives only in owner-only tmpfs
custody, never in the journal; custody is destroyed once that token is revoked
or denied. Rollback keeps the old token and revokes only this run's new one.
v1/v2 journals are still read and reconciled.
"""

from __future__ import annotations

import fcntl
import hashlib
import hmac
import json
import os
import re
import secrets
import signal
import stat
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path

ROLE = "hy-home-renderer"
PREFIX = "auth/approle/role/" + ROLE
IMAGE = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"
MANIFEST = "sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"
SAFE = re.compile(r"[a-zA-Z0-9._-]+")
REVISION = re.compile(r"[a-f0-9]{40}")


class Blocked(Exception):
    """Deliberately carries no server response, credential, or subprocess output."""


class Uncertain(Blocked):
    """A request may have succeeded; retain its journal for explicit reconciliation."""


class Denied(Blocked):
    """The server refused a self-token request with 403: that token is unusable."""


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Blocked()
        result = {**result, key: value}
    return result


def utc(seconds):
    return datetime.fromtimestamp(seconds, UTC).isoformat()


V1_FIELDS = (
    "nonce",
    "started_at",
    "role",
    "source_revision",
    "image_manifest",
    "state",
    "agent_started_at",
)
VERSION_FIELDS = {
    1: set(),
    2: {"schema_version", "issuance_id"},
    3: {"schema_version", "issuance_id", "old_created"},
}
STATES = {
    1: {"issuing", "delivered"},
    2: {"issuing", "delivered"},
    3: {"prepared", "issuing", "delivered", "verified", "revoking", "rolling_back"},
}


@dataclass(frozen=True)
class Record:
    nonce: str
    started_at: str
    role: str
    source_revision: str
    image_manifest: str
    state: str = "issuing"
    agent_started_at: str | None = None
    schema_version: int = 1
    # v3: creation time of the captured old Agent token; None when none is live.
    old_created: int | None = None

    @property
    def issuance_id(self):
        return self.nonce

    @property
    def terminal(self):
        # A v3 run that never revoked the old token ends rolled_back.
        return "rolled_back" if self.schema_version == 3 else "complete"

    @classmethod
    def from_document(cls, raw):
        if not isinstance(raw, dict):
            raise Blocked()
        version = raw.get("schema_version", 1)
        if (
            type(version) is not int
            or version not in VERSION_FIELDS
            or set(raw) != set(V1_FIELDS) | VERSION_FIELDS[version]
            or raw.get("issuance_id", raw["nonce"]) != raw["nonce"]
        ):
            raise Blocked()
        try:
            return cls(
                **{k: raw[k] for k in V1_FIELDS},
                schema_version=version,
                old_created=raw.get("old_created"),
            ).validate()
        except (ValueError, TypeError):
            raise Blocked() from None

    def document(self):
        fields = {k: getattr(self, k) for k in V1_FIELDS}
        if self.schema_version == 1:
            return fields
        fields = {**fields, "schema_version": self.schema_version}
        if self.schema_version == 3:
            fields = {**fields, "old_created": self.old_created}
        return {**fields, "issuance_id": self.nonce}

    def anchor(self, state):
        fields = {"nonce": self.nonce, "state": state}
        return (
            fields
            if self.schema_version == 1
            else {
                **fields,
                "schema_version": self.schema_version,
                "issuance_id": self.nonce,
            }
        )

    def metadata(self):
        fields = {
            "sec01_nonce": self.nonce,
            "sec01_role": self.role,
            "sec01_issued_at": self.started_at,
        }
        return (
            fields
            if self.schema_version == 1
            else {
                **fields,
                "issuance_schema": str(self.schema_version),
                "issuance_id": self.nonce,
            }
        )

    def validate(self):
        if (
            type(self.schema_version) is not int
            or self.schema_version not in STATES
            or not isinstance(self.nonce, str)
            or not re.fullmatch(r"[a-f0-9]{32}", self.nonce)
            or self.role != ROLE
            or not isinstance(self.source_revision, str)
            or not REVISION.fullmatch(self.source_revision)
            or self.image_manifest != MANIFEST
            or self.state not in STATES[self.schema_version]
        ):
            raise Blocked()
        try:
            when = datetime.fromisoformat(self.started_at)
            if when.tzinfo is None:
                raise ValueError()
        except (ValueError, TypeError):
            raise Blocked() from None
        if self.old_created is not None and (
            self.schema_version != 3
            or type(self.old_created) is not int
            or not 0 < self.old_created < when.timestamp()
        ):
            raise Blocked()
        if self.agent_started_at is not None:
            try:
                generation = datetime.fromisoformat(
                    self.agent_started_at.replace("Z", "+00:00")
                )
                if self.state in {"prepared", "issuing"} or generation.tzinfo is None:
                    raise ValueError()
            except (AttributeError, ValueError, TypeError):
                raise Blocked() from None
        return self


class Journal:
    """Exact private directory; caller must provision it outside the Agent volume."""

    def __init__(self, directory):
        self.directory = Path(directory)
        info = self.directory.lstat()
        if (
            not stat.S_ISDIR(info.st_mode)
            or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) != 0o700
        ):
            raise Blocked()
        self.fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.lock = None

    def _open(self, name, flags):
        fd = os.open(name, flags | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
        info = os.fstat(fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_nlink != 1
            or stat.S_IMODE(info.st_mode) != 0o600
        ):
            os.close(fd)
            raise Blocked()
        return fd

    def __enter__(self):
        self.lock = self._open("issuance.lock", os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise Blocked() from None
        return self

    def __exit__(self, *_):
        if self.lock is not None:
            os.close(self.lock)
        os.close(self.fd)

    def _read_json(self, name):
        try:
            fd = self._open(name, os.O_RDONLY)
        except FileNotFoundError:
            if name + ".pending" in os.listdir(self.fd):
                raise Blocked() from None
            return None
        with os.fdopen(fd) as stream:
            raw = stream.read(4097)
        if len(raw) > 4096:
            raise Blocked()
        try:
            return json.loads(raw, object_pairs_hook=unique_fields)
        except (ValueError, TypeError):
            raise Blocked() from None

    def load(self):
        if any(name.endswith(".pending") for name in os.listdir(self.fd)):
            raise Blocked()  # Interrupted atomic update is retained for explicit recovery.
        raw = self._read_json("issuance.json")
        anchor = self._read_json("issuance.anchor")
        if anchor is not None:
            version = anchor.get("schema_version", 1) if isinstance(anchor, dict) else 0
            keys = (
                {"nonce", "state"}
                if version == 1
                else {"nonce", "state", "schema_version", "issuance_id"}
            )
            states = {"active", "complete"} | (
                {"rolled_back"} if version == 3 else set()
            )
            if (
                not isinstance(anchor, dict)
                or type(version) is not int
                or version not in STATES
                or set(anchor) != keys
                or anchor["state"] not in states
                or not isinstance(anchor["nonce"], str)
                or not re.fullmatch(r"[a-f0-9]{32}", anchor["nonce"])
                or (version != 1 and anchor["issuance_id"] != anchor["nonce"])
            ):
                raise Blocked()
        if raw is None:
            if anchor is not None and anchor["state"] == "active":
                raise Blocked()  # Lost active journal never means fresh issuance.
            return None
        record = Record.from_document(raw)
        if anchor in (record.anchor("complete"), record.anchor("rolled_back")):
            # Finish an interrupted clear using the independently durable witness.
            os.unlink("issuance.json", dir_fd=self.fd)
            os.fsync(self.fd)
            return None
        if anchor != record.anchor("active"):
            raise Blocked()
        return record

    def _write_json(self, name, document):
        self._write(name, json.dumps(document, sort_keys=True))

    def _write(self, name, text):
        pending = name + ".pending"
        fd = self._open(pending, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        with os.fdopen(fd, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
        os.fsync(self.fd)

    def save(self, record):
        record.validate()
        self._write_json("issuance.anchor", record.anchor("active"))
        self._write_json("issuance.json", record.document())

    def clear(self, state="complete"):
        record = self.load()
        if record is None:
            raise Blocked()
        # Retain a durable completion witness separately from the active journal.
        self._write_json("issuance.anchor", record.anchor(state))
        os.unlink("issuance.json", dir_fd=self.fd)
        os.fsync(self.fd)


def token_text(raw):
    token = raw.decode("ascii", "replace")
    if not raw or len(raw) > 1024 or not SAFE.fullmatch(token):
        raise Blocked()
    return token


class Custody(Journal):
    """Old Agent token in owner-only 0600 tmpfs custody; never printed or journaled.

    The file name binds server, volume and journal, so a restore rehearsal with
    its own journal never reads or destroys HOME's custody. The journal lock
    serializes every run that shares one binding.
    """

    def __init__(self, directory, binding):
        super().__init__(directory)
        digest = hashlib.sha256("\0".join(binding).encode()).hexdigest()[:16]
        self.name = "hy-home-renderer-old-token-" + digest

    def read(self):
        try:
            fd = self._open(self.name, os.O_RDONLY)
        except FileNotFoundError:
            return None
        with os.fdopen(fd, "rb") as stream:
            return token_text(stream.read(1025))

    def write(self, token):
        self._unlink(self.name + ".pending")  # An interrupted earlier write.
        self._write(self.name, token_text(token.encode()))

    def destroy(self):
        self._unlink(self.name + ".pending")
        self._unlink(self.name)

    def _unlink(self, name):
        try:
            os.unlink(name, dir_fd=self.fd)
        except FileNotFoundError:
            return
        os.fsync(self.fd)


def custody_directory():
    # The approved custody is owner-only tmpfs under XDG_RUNTIME_DIR; a reboot
    # destroys it, which leaves an interrupted revoke INDETERMINATE (Blocked).
    directory = f"/run/user/{os.getuid()}"
    with open("/proc/self/mounts") as mounts:
        if not any(line.split()[1:3] == [directory, "tmpfs"] for line in mounts):
            raise Blocked()
    return directory


def matching_accessors(api, record):
    """API adapter scopes every request to ROLE; metadata narrows cleanup further."""
    matches = []
    start = datetime.fromisoformat(record.started_at).timestamp()
    for accessor in api.accessors():
        data = api.lookup(accessor)
        if not isinstance(data, dict) or not isinstance(data.get("metadata"), dict):
            raise Blocked()
        metadata = data["metadata"]
        if record.nonce not in (
            metadata.get("sec01_nonce"),
            metadata.get("issuance_id"),
        ):
            continue
        if metadata != record.metadata():
            raise Blocked()
        try:
            created = datetime.fromisoformat(
                data["creation_time"].replace("Z", "+00:00")
            )
            if created.tzinfo is None or not start <= created.timestamp() <= start + 60:
                raise ValueError()
        except (KeyError, ValueError, TypeError, AttributeError):
            raise Blocked() from None
        matches.append(accessor)
    if len(matches) > 1:
        raise Blocked()
    return matches


def settle_secret_id(api, record, *, ready=False, stopped=False):
    matches = matching_accessors(api, record)
    if not matches:
        # Issuing without a matching accessor is ambiguous (including expired ID).
        # A delivered ID is consumed or expired once its generation is ready or
        # stopped; a rollback then revokes a token it minted into the sink.
        if record.state != "delivered" or not (ready or stopped):
            raise Blocked()
        return
    if record.state == "delivered" and not (ready or stopped):
        raise Blocked()
    api.destroy(matches[0])
    if matching_accessors(api, record):
        raise Blocked()


def reconcile(api, journal, record, *, ready=False, stopped=False):
    settle_secret_id(api, record, ready=ready, stopped=stopped)
    journal.clear(record.terminal)


def renderer_token(api, token):
    """Creation time of a live renderer login token; None once the server denies it."""
    data = api.lookup_self(token)
    if data is None:
        return None
    created = data.get("creation_time")
    if (
        data.get("policies") != ["default", "renderer"]
        or data.get("path") != "auth/approle/login"
        or not isinstance(data.get("meta"), dict)
        or data["meta"].get("role_name") != ROLE
        or type(created) is not int
        or created <= 0
    ):
        raise Blocked()
    return created


def revoke(api, token):
    # Pre-flight: the selected server must grant revoke-self to this token.
    if not api.revoke_self_allowed(token):
        raise Blocked()
    api.revoke_self(token)
    if renderer_token(api, token) is not None:
        raise Blocked()


def prepare(api, custody, record):
    """Capture the one live old generation before any new SecretID exists."""
    candidates = {t for t in (custody.read(), api.sink()) if t}
    live = {}
    for token in candidates:
        created = renderer_token(api, token)
        if created is not None:
            live = {**live, token: created}
    if len(live) > 1:
        raise Blocked()  # Several live generations: never guess which to revoke.
    if not live:
        custody.destroy()  # Anything held is already unusable.
        return replace(record, state="issuing")
    ((token, created),) = live.items()
    record = replace(record, state="issuing", old_created=created).validate()
    if not api.revoke_self_allowed(token):
        raise Blocked()
    custody.write(token)
    return record


def rollback(api, journal, custody, record):
    """New generation failed: keep the old token, revoke only this run's token."""
    if record.schema_version == 3 and record.state != "rolling_back":
        record = replace(record, state="rolling_back")
        journal.save(record)
    if not api.stopped():
        generation = api.recovery_generation(record.started_at)
        if record.agent_started_at not in (None, generation):
            raise Blocked()  # A later start is not this issuance's to stop.
    api.stop()
    settle_secret_id(api, replace(record, state="delivered"), stopped=True)
    token = api.sink()
    held = custody.read() if record.schema_version == 3 else None
    if token is not None and not (held and hmac.compare_digest(token, held)):
        created = renderer_token(api, token)
        start = int(datetime.fromisoformat(record.started_at).timestamp())
        # An older sink token is not this run's; the rollback leaves it alone.
        if created is not None and created >= start:
            revoke(api, token)
    journal.clear(record.terminal)


def revoke_old(api, journal, custody, record):
    """Durable intent first; a timeout stays INDETERMINATE for the next run."""
    if record.old_created is not None:
        token = custody.read()
        if token is None:
            raise Blocked()  # Custody lost (reboot): owner reconciliation.
        created = renderer_token(api, token)
        if record.state != "revoking":
            # Before the intent a 403 is not proof: the token must be live,
            # exactly the captured generation, and allowed to revoke itself.
            if created != record.old_created or not api.revoke_self_allowed(token):
                raise Blocked()
            record = replace(record, state="revoking")
            journal.save(record)
            api.revoke_self(token)
            if renderer_token(api, token) is not None:
                raise Blocked()
        elif created is not None:
            # Denied only once revoking was durable, right after the checks
            # above: the revoke landed or the token expired; it is unusable.
            if created != record.old_created:
                raise Blocked()
            revoke(api, token)
    journal.clear("complete")
    custody.destroy()


def finish(api, journal, custody, record):
    """Verify a distinct new generation, then revoke the old one."""
    settle_secret_id(api, record, ready=True)
    held = custody.read() if record.old_created is not None else None
    current = api.sink()
    start = int(datetime.fromisoformat(record.started_at).timestamp())
    if (
        current is None
        or (held is not None and hmac.compare_digest(current, held))
        or (renderer_token(api, current) or 0) < start
    ):
        rollback(api, journal, custody, record)
        raise Blocked()
    record = replace(record, state="verified")
    journal.save(record)
    revoke_old(api, journal, custody, record)


def resume(api, journal, custody, record):
    if record.state == "prepared":
        journal.clear("rolled_back")  # Nothing was issued.
    elif record.state == "issuing":
        reconcile(api, journal, record)
    elif record.state in {"verified", "revoking"}:
        revoke_old(api, journal, custody, record)
    elif record.state == "rolling_back":
        rollback(api, journal, custody, record)
    else:
        ready = False
        if not api.stopped():
            generation = api.recovery_generation(record.started_at)
            if record.agent_started_at not in (None, generation):
                raise Blocked()  # A later start is not this issuance's to judge.
            if record.agent_started_at is None and generation is not None:
                record = replace(record, agent_started_at=generation)
                journal.save(record)
            ready = generation is not None and api.ready(generation)
        if not ready:
            rollback(api, journal, custody, record)
        elif record.schema_version == 3:
            finish(api, journal, custody, record)
        else:
            reconcile(api, journal, record, ready=True)


def run_issuance(
    api, journal, *, revision, custody, clock=time.time, nonce=secrets.token_hex
):
    previous = journal.load()
    if previous is not None:
        resume(api, journal, custody, previous)
        # Reconciliation is a distinct result; do not mint another ID on this run.
        return "reconciled"
    record = Record(
        nonce(16),
        utc(clock()),
        ROLE,
        revision,
        MANIFEST,
        state="prepared",
        schema_version=3,
    ).validate()
    journal.save(record)  # Durable before the old token is captured.
    try:
        record = prepare(api, custody, record)
    except Exception:
        journal.clear("rolled_back")  # No server mutation yet.
        raise Blocked() from None
    journal.save(record)  # Durable before any potentially successful server call.
    try:
        wrapped = api.issue(record.metadata())
        api.deliver(wrapped)
        delivered = replace(record, state="delivered")
        journal.save(delivered)  # Delivery alone never clears uncertainty.
        started_at = api.start()
        delivered = replace(delivered, agent_started_at=started_at)
        journal.save(delivered)
        if not api.ready(started_at):
            raise Blocked()
        finish(api, journal, custody, delivered)
        return "authenticated"
    except Uncertain:
        raise
    except Exception:
        # A failed delivery may have issued an ID. Revoke only an exact single match.
        # A delivered generation that fails verification is rolled back.
        current = journal.load()
        if current is not None and current.state == "issuing":
            reconcile(api, journal, current)
        elif current is not None and current.state == "delivered":
            rollback(api, journal, custody, current)
        raise Blocked() from None


class DockerAPI:
    """No host env/credentials in argv; credentials go through receiving stdin."""

    def __init__(self, server, volume, agent, issuer, cleanup, *, request_script):
        self.server, self.volume, self.agent = server, volume, agent
        self.issuer, self.cleanup = issuer, cleanup
        self.request_script = request_script
        self.started_at = None
        self.deadline = time.monotonic() + 240
        self.wrap_deadline = self.deadline  # set by issue()

    @staticmethod
    def command(argv, *, payload=None, seconds=20, empty_list_path=None, denied=False):
        try:
            done = subprocess.run(
                argv, input=payload, capture_output=True, timeout=seconds, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            raise Blocked() from None
        if done.returncode:
            # Only self-token requests map a server 403 to Denied.
            if denied and done.returncode == 2 and b"Code: 403." in done.stderr:
                raise Denied()
            # The verified 2.7.1 JSON CLI renders a LIST HTTP 404 as stdout {}.
            # ACL/transport failures and any unknown output still block recovery.
            absent_json = not done.stderr and done.stdout.strip() == b"{}"
            absent_text = not done.stdout and done.stderr.decode(
                errors="replace"
            ).strip() == "No value found at " + (empty_list_path or "")
            if (
                empty_list_path == PREFIX + "/secret-id"
                and done.returncode == 2
                and (absent_json or absent_text)
            ):
                return b'{"data":{"keys":[]}}'
            raise Blocked()
        return done.stdout

    # The 60 s wrap TTL covers deliver, start and the Agent's own unwrap
    # together. Spend at most 45 s of it on deliver plus start, counted from
    # before the issue request, and leave the rest for the unwrap.
    WRAP_BUDGET = 45
    UNWRAP_RESERVE = 8

    def _container_seconds(self):
        # docker run --rm/start took 11-19 s under host load on 2026-10-27.
        seconds = min(self.wrap_deadline, self.deadline) - time.monotonic()
        if seconds < 4:
            raise Blocked()
        return seconds

    def request(self, operation, path, payload=None, *, issuer=False, token=None):
        # Leave renewal-free token lifetime margin; never turn a large LIST into an unbounded run.
        # A renderer token's own requests do not spend the short tokens' deadline.
        self_token = token is not None
        seconds = 20 if self_token else min(20, self.deadline - time.monotonic())
        if seconds < 4:
            raise Blocked()
        if not self_token:
            token = self.issuer if issuer else self.cleanup
        body = (token + "\n").encode()
        arguments = [*operation.split(), "-format=json", path]
        if payload is not None:
            body += json.dumps(payload).encode()
            arguments.append("-")
        silent = path in {
            PREFIX + "/secret-id-accessor/destroy",
            "auth/token/revoke-self",
        }
        argv = [
            "docker",
            "exec",
            "-i",
            self.server,
            "/bin/sh",
            "-c",
            self.request_script,
        ]
        try:
            raw = self.command(
                [*argv, "renderer-request", str(int(seconds) - 3), *arguments],
                payload=body,
                seconds=seconds,
                empty_list_path=path if operation == "list" else None,
                denied=self_token,
            )
        except Denied:
            raise
        except (Blocked, InterruptedError):
            raise Uncertain() from None
        if silent:
            return {}
        try:
            return json.loads(raw, object_pairs_hook=unique_fields)
        except (ValueError, TypeError):
            raise Uncertain() from None

    def validate_tokens(self):
        for issuer, policy in ((True, "renderer-issuer"), (False, "renderer-cleanup")):
            response = self.request("read", "auth/token/lookup-self", issuer=issuer)
            data = response.get("data", {})
            ttl = data.get("ttl")
            if (
                data.get("policies") != [policy]
                or data.get("identity_policies", [])
                or data.get("renewable") is not False
                or type(ttl) is not int
                or not 0 < ttl <= 300
                or data.get("explicit_max_ttl") != 300
                or data.get("type") != "service"
                or data.get("path") != "auth/token/create/" + policy
            ):
                raise Blocked()

    def issue(self, metadata):
        self.wrap_deadline = time.monotonic() + self.WRAP_BUDGET
        response = self.request(
            "write -wrap-ttl=60s",
            PREFIX + "/secret-id",
            {"metadata": json.dumps(metadata)},
            issuer=True,
        )
        try:
            token = response["wrap_info"]["token"]
            if not isinstance(token, str) or not SAFE.fullmatch(token):
                raise ValueError()
            return token
        except (KeyError, TypeError, ValueError):
            raise Blocked() from None

    def accessors(self):
        response = self.request("list", PREFIX + "/secret-id")
        # bao -format=json projects a successful LIST to a bare array; the
        # synthesized, exact absent-list sentinel retains an API-shaped envelope.
        keys = response if isinstance(response, list) else None
        if isinstance(response, dict) and isinstance(response.get("data"), dict):
            keys = response["data"].get("keys")
        if not isinstance(keys, list) or len(keys) > 1000:
            raise Blocked()
        if any(not isinstance(k, str) or not SAFE.fullmatch(k) for k in keys):
            raise Blocked()
        if len(keys) != len(set(keys)):
            raise Blocked()
        return keys

    def lookup(self, accessor):
        return self.request(
            "write",
            PREFIX + "/secret-id-accessor/lookup",
            {"secret_id_accessor": accessor},
        ).get("data")

    def destroy(self, accessor):
        # bao write returns no JSON on successful destroy.
        self.request(
            "write",
            PREFIX + "/secret-id-accessor/destroy",
            {"secret_id_accessor": accessor},
        )

    def lookup_self(self, token):
        try:
            response = self.request("read", "auth/token/lookup-self", token=token)
        except Denied:
            return None
        if not isinstance(response, dict) or not isinstance(response.get("data"), dict):
            raise Blocked()
        return response["data"]

    def revoke_self_allowed(self, token):
        path = "auth/token/revoke-self"
        response = self.request(
            "write", "sys/capabilities-self", {"paths": [path]}, token=token
        )
        data = response.get("data") if isinstance(response, dict) else None
        allowed = data.get(path) if isinstance(data, dict) else None
        return isinstance(allowed, list) and "update" in allowed

    def revoke_self(self, token):
        # bao write returns no JSON on a successful revoke-self.
        self.request("write -force", "auth/token/revoke-self", token=token)

    def sink(self):
        """Read the Agent sink token through a no-network, read-only container."""
        script = (
            "set +x; set -eu; f=/openbao/agent/token; "
            '[ -e "$f" ] || [ -L "$f" ] || exit 0; '
            '[ -f "$f" ] && [ ! -L "$f" ]; '
            '[ "$(stat -c %a:%h "$f")" = 600:1 ]; head -c 1025 "$f"'
        )
        raw = self.command(
            [
                "docker",
                "run",
                "--rm",
                "--pull=never",
                "--network=none",
                "--log-driver=none",
                "--user=100:1000",
                "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "--read-only",
                "--mount",
                "type=volume,source=" + self.volume + ",target=/openbao/agent,readonly",
                "--entrypoint",
                "sh",
                IMAGE,
                "-c",
                script,
            ],
            seconds=45,
        )
        return token_text(raw) if raw else None

    def stop(self):
        self.command(["docker", "stop", "--time=10", self.agent], seconds=30)

    def deliver(self, wrapped):
        script = (
            "set +x; set -eu; umask 077; "
            "[ -d /openbao/agent ] && [ ! -L /openbao/agent ]; "
            "[ ! -L /openbao/agent/secret_id ]; "
            "partial=$(mktemp /openbao/agent/.wrapped-secret-id.XXXXXX); "
            "trap 'rm -f \"$partial\"' EXIT; trap 'exit 1' HUP INT TERM; "
            'IFS= read -r wrapped; printf %s "$wrapped" >"$partial"; '
            'chmod 600 "$partial"; mv -f "$partial" /openbao/agent/secret_id'
        )
        self.command(
            [
                "docker",
                "run",
                "--rm",
                "--pull=never",
                "--network=none",
                "-i",
                "--user=100:1000",
                "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "--read-only",
                "--mount",
                "type=volume,source=" + self.volume + ",target=/openbao/agent",
                "--entrypoint",
                "sh",
                IMAGE,
                "-c",
                script,
            ],
            payload=(wrapped + "\n").encode(),
            seconds=self._container_seconds(),
        )
        # Still journaled as issuing: a raise here destroys the exact SecretID
        # instead of recording a delivery the Agent can no longer unwrap.
        if self.wrap_deadline - time.monotonic() < self.UNWRAP_RESERVE:
            raise Blocked()

    def stopped(self):
        return (
            self.command(
                [
                    "docker",
                    "inspect",
                    "--type=container",
                    "--format",
                    "{{.State.Running}}",
                    self.agent,
                ]
            ).strip()
            == b"false"
        )

    def recovery_generation(self, issued_at):
        if self.stopped():
            return None
        generation = self._started_at()
        try:
            started = datetime.fromisoformat(generation.replace("Z", "+00:00"))
            issued = datetime.fromisoformat(issued_at)
            if started.tzinfo is None or started < issued:
                raise ValueError()
        except (ValueError, TypeError):
            raise Blocked() from None
        return generation

    def start(self):
        self.command(["docker", "start", self.agent], seconds=self._container_seconds())
        # Start script removes the old sink; Docker StartedAt identifies this start.
        self.started_at = self._started_at()
        return self.started_at

    def _started_at(self):
        return (
            self.command(
                [
                    "docker",
                    "inspect",
                    "--type=container",
                    "--format",
                    "{{.State.StartedAt}}",
                    self.agent,
                ]
            )
            .decode()
            .strip()
        )

    def ready(self, expected_started_at):
        deadline = min(self.deadline, time.monotonic() + 90)
        for _ in range(30):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            try:
                self.command(
                    [
                        "docker",
                        "exec",
                        self.agent,
                        "/bin/sh",
                        "/openbao/scripts/health-agent.sh",
                    ],
                    seconds=min(35, remaining),
                )
                if expected_started_at == self._started_at():
                    return True
                return False
            except Blocked:
                time.sleep(1)
        return False


def validate_binding(server, volume, agent, journal_path):
    call = DockerAPI.command
    image = (
        call(
            [
                "docker",
                "image",
                "inspect",
                "--platform=linux/amd64",
                "--format",
                "{{.Id}}",
                IMAGE,
            ]
        )
        .decode()
        .strip()
    )
    if image != MANIFEST:
        raise Blocked()
    server_binding = (
        call(
            [
                "docker",
                "inspect",
                "--type=container",
                "--format",
                "{{.Image}} {{.State.Running}}",
                server,
            ]
        )
        .decode()
        .strip()
    )
    if server_binding != MANIFEST + " true":
        raise Blocked()
    binding = (
        call(
            [
                "docker",
                "inspect",
                "--type=container",
                "--format",
                '{{.Image}} {{range .Mounts}}{{if eq .Destination "/openbao/agent"}}'
                "{{.Type}} {{.Name}}{{end}}{{end}}",
                agent,
            ]
        )
        .decode()
        .strip()
    )
    if binding != MANIFEST + " volume " + volume:
        raise Blocked()
    launch = call(
        [
            "docker",
            "inspect",
            "--type=container",
            "--format",
            '{"entrypoint":{{json .Config.Entrypoint}},"cmd":{{json .Config.Cmd}}}',
            agent,
        ]
    )
    try:
        configuration = json.loads(launch, object_pairs_hook=unique_fields)
        entrypoint = configuration["entrypoint"] or []
        command = configuration["cmd"] or []
        if (
            not isinstance(entrypoint, list)
            or not isinstance(command, list)
            or entrypoint + command != ["/bin/sh", "/openbao/scripts/start-agent.sh"]
        ):
            raise Blocked()
    except (KeyError, ValueError, TypeError):
        raise Blocked() from None
    device = (
        call(
            [
                "docker",
                "volume",
                "inspect",
                "--format",
                '{{index .Options "device"}}',
                volume,
            ]
        )
        .decode()
        .strip()
    )
    if not device or device == "<no value>":
        raise Blocked()
    journal = Path(journal_path).resolve(strict=True)
    try:
        agent_directory = Path(device).resolve(strict=True)
    except OSError:
        raise Blocked() from None
    if (
        journal == agent_directory
        or agent_directory in journal.parents
        or journal in agent_directory.parents
    ):
        raise Blocked()


def validate_receipt(revision):
    directory = Path(__file__).parent
    files = {
        "issue-renderer-secret-id.sh",
        "renderer-issuance.py",
        "renderer-request.sh",
    }

    def signature(info):
        return info.st_dev, info.st_ino, info.st_mtime_ns, info.st_ctime_ns

    def read_private(name, *, receipt=False):
        fd = os.open(directory / name, os.O_RDONLY | os.O_NOFOLLOW)
        info = os.fstat(fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or info.st_uid not in {0, os.getuid()}
            or stat.S_IMODE(info.st_mode) & 0o022
            or (receipt and stat.S_IMODE(info.st_mode) != 0o400)
        ):
            os.close(fd)
            raise Blocked()
        with os.fdopen(fd, "rb") as stream:
            raw = stream.read(100001)
            if signature(info) != signature(os.fstat(stream.fileno())) or signature(
                info
            ) != signature((directory / name).lstat()):
                raise Blocked()
        if len(raw) > 100000:
            raise Blocked()
        return raw

    try:
        receipt = json.loads(
            read_private("source-receipt.json", receipt=True),
            object_pairs_hook=unique_fields,
        )
        hashes = receipt["sha256"]
        if (
            set(receipt) != {"source_revision", "sha256"}
            or receipt["source_revision"] != revision
            or set(hashes) != files
        ):
            raise Blocked()
        blobs = {name: read_private(name) for name in files}
        for name in files:
            if (
                not isinstance(hashes[name], str)
                or not re.fullmatch(r"[a-f0-9]{64}", hashes[name])
                or hashlib.sha256(blobs[name]).hexdigest() != hashes[name]
            ):
                raise Blocked()
        return blobs["renderer-request.sh"].decode()
    except (OSError, KeyError, ValueError, TypeError):
        raise Blocked() from None


def main(argv):
    if len(argv) != 6:
        raise Blocked()
    server, volume, image, agent, directory, revision = argv
    if image != IMAGE or not REVISION.fullmatch(revision):
        raise Blocked()
    if any(
        not SAFE.fullmatch(n) or not n[0].isalnum() for n in (server, volume, agent)
    ):
        raise Blocked()
    if not Path(directory).is_absolute() or Path(directory).is_symlink():
        raise Blocked()
    request_script = validate_receipt(revision)
    tokens = [sys.stdin.readline(1025).strip() for _ in range(2)]
    if any(not SAFE.fullmatch(t) or len(t) > 1024 for t in tokens):
        raise Blocked()
    validate_binding(server, volume, agent, directory)
    api = DockerAPI(server, volume, agent, *tokens, request_script=request_script)
    if not (Path(directory) / "issuance.json").exists() and not api.stopped():
        raise Blocked()
    api.validate_tokens()
    journal_info = Path(directory).stat()
    binding = (server, volume, f"{journal_info.st_dev}:{journal_info.st_ino}")
    custody = Custody(custody_directory(), binding)
    with Journal(directory) as journal:
        if journal.load() is None and not api.stopped():
            raise Blocked()
        run_issuance(api, journal, revision=revision, custody=custody)
    return 0


if __name__ == "__main__":

    def interrupted(*_):
        raise InterruptedError()

    for name in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(name, interrupted)
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception:
        # All subprocess stderr and original exceptions stay private.
        sys.exit(1)
