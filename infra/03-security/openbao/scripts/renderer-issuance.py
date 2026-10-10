"""Explicit operator issuance with durable, secret-free reconciliation state.

Only the CLI adapter performs I/O. API responses and credentials remain in memory.
A journal is evidence of uncertainty, never proof that authentication succeeded.
"""

from __future__ import annotations

import fcntl
import hashlib
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
IMAGE = "openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf"
MANIFEST = "sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005"
SAFE = re.compile(r"[a-zA-Z0-9._-]+")
REVISION = re.compile(r"[a-f0-9]{40}")


class Blocked(Exception):
    """Deliberately carries no server response, credential, or subprocess output."""


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Blocked()
        result = {**result, key: value}
    return result


def utc(seconds):
    return datetime.fromtimestamp(seconds, UTC).isoformat()


@dataclass(frozen=True)
class Record:
    nonce: str
    started_at: str
    role: str
    source_revision: str
    image_manifest: str
    state: str = "issuing"
    agent_started_at: str | None = None

    def metadata(self):
        return {
            "sec01_nonce": self.nonce,
            "sec01_role": self.role,
            "sec01_issued_at": self.started_at,
        }

    def validate(self):
        if (
            not re.fullmatch(r"[a-f0-9]{32}", self.nonce)
            or self.role != ROLE
            or not REVISION.fullmatch(self.source_revision)
            or self.image_manifest != MANIFEST
            or self.state not in {"issuing", "delivered"}
        ):
            raise Blocked()
        try:
            when = datetime.fromisoformat(self.started_at)
            if when.tzinfo is None:
                raise ValueError()
        except (ValueError, TypeError):
            raise Blocked() from None
        if self.agent_started_at is not None:
            try:
                generation = datetime.fromisoformat(
                    self.agent_started_at.replace("Z", "+00:00")
                )
                if self.state != "delivered" or generation.tzinfo is None:
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
            if (
                not isinstance(anchor, dict)
                or set(anchor) != {"nonce", "state"}
                or anchor["state"] not in {"active", "complete"}
                or not re.fullmatch(r"[a-f0-9]{32}", str(anchor["nonce"]))
            ):
                raise Blocked()
        if raw is None:
            if anchor is not None and anchor["state"] != "complete":
                raise Blocked()  # Lost active journal never means fresh issuance.
            return None
        try:
            record = Record(**raw).validate()
        except (ValueError, TypeError):
            raise Blocked() from None
        if anchor == {"nonce": record.nonce, "state": "complete"}:
            # Finish an interrupted clear using the independently durable witness.
            os.unlink("issuance.json", dir_fd=self.fd)
            os.fsync(self.fd)
            return None
        if anchor != {"nonce": record.nonce, "state": "active"}:
            raise Blocked()
        return record

    def _write_json(self, name, document):
        pending = name + ".pending"
        fd = self._open(pending, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        with os.fdopen(fd, "w") as stream:
            json.dump(document, stream, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
        os.fsync(self.fd)

    def save(self, record):
        record.validate()
        self._write_json("issuance.anchor", {"nonce": record.nonce, "state": "active"})
        self._write_json("issuance.json", record.__dict__)

    def clear(self):
        record = self.load()
        if record is None:
            raise Blocked()
        # Retain a durable completion witness separately from the active journal.
        self._write_json(
            "issuance.anchor", {"nonce": record.nonce, "state": "complete"}
        )
        os.unlink("issuance.json", dir_fd=self.fd)
        os.fsync(self.fd)


def matching_accessors(api, record):
    """API adapter scopes every request to ROLE; metadata narrows cleanup further."""
    matches = []
    start = datetime.fromisoformat(record.started_at).timestamp()
    for accessor in api.accessors():
        data = api.lookup(accessor)
        if not isinstance(data, dict) or not isinstance(data.get("metadata"), dict):
            raise Blocked()
        if data["metadata"].get("sec01_nonce") != record.nonce:
            continue
        if any(data["metadata"].get(k) != v for k, v in record.metadata().items()):
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


def reconcile(api, journal, record, *, ready=False, stopped=False):
    matches = matching_accessors(api, record)
    if not matches:
        # Issuing without a matching accessor is ambiguous (including expired ID).
        if record.state != "delivered" or not ready:
            raise Blocked()
    else:
        if record.state == "delivered" and not (ready or stopped):
            raise Blocked()
        api.destroy(matches[0])
        if matching_accessors(api, record):
            raise Blocked()
    journal.clear()


def run_issuance(api, journal, *, revision, clock=time.time, nonce=secrets.token_hex):
    previous = journal.load()
    if previous is not None:
        stopped = False
        ready = False
        if previous.state == "delivered":
            generation = previous.agent_started_at
            if generation is None:
                generation = api.recovery_generation(previous.started_at)
                if generation is not None:
                    previous = replace(previous, agent_started_at=generation)
                    journal.save(previous)
                else:
                    stopped = api.stopped()
            if generation is not None:
                ready = api.ready(generation)
        reconcile(api, journal, previous, ready=ready, stopped=stopped)
        # Reconciliation is a distinct result; do not mint another ID on this run.
        return "reconciled"
    record = Record(nonce(16), utc(clock()), ROLE, revision, MANIFEST).validate()
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
        reconcile(api, journal, delivered, ready=True)
        return "authenticated"
    except Exception:
        # A failed delivery may have issued an ID. Revoke only an exact single match.
        # Delivered IDs await current-process authentication proof on the next run.
        current = journal.load()
        if current is not None and current.state == "issuing":
            reconcile(api, journal, current)
        raise Blocked() from None


class DockerAPI:
    """No host env/credentials in argv; credentials go through receiving stdin."""

    def __init__(self, server, volume, agent, issuer, cleanup):
        self.server, self.volume, self.agent = server, volume, agent
        self.issuer, self.cleanup = issuer, cleanup
        self.started_at = None
        self.deadline = time.monotonic() + 240

    @staticmethod
    def command(argv, *, payload=None, seconds=20, empty_list_path=None):
        try:
            done = subprocess.run(
                argv, input=payload, capture_output=True, timeout=seconds, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            raise Blocked() from None
        if done.returncode:
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

    def request(self, operation, path, payload=None, *, issuer=False):
        # Leave renewal-free token lifetime margin; never turn a large LIST into an unbounded run.
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise Blocked()
        # The public operation and exact public role path are constant at callers.
        token = self.issuer if issuer else self.cleanup
        script = (
            "set +x; set -eu; IFS= read -r BAO_TOKEN; export BAO_TOKEN; "
            'unset VAULT_TOKEN; case "${BAO_ADDR:-}" in https://?*) ;; *) exit 1;; esac; '
            '[ -n "${BAO_CACERT:-}" ] && [ -r "$BAO_CACERT" ]; '
            '[ -z "${BAO_SKIP_VERIFY:-}${VAULT_SKIP_VERIFY:-}" ]; '
            "exec bao " + operation + " -format=json " + path
        )
        body = (token + "\n").encode()
        if payload is not None:
            body += json.dumps(payload).encode()
            script += " -"
        destroying = path == PREFIX + "/secret-id-accessor/destroy"
        if destroying:
            script += " >/dev/null"
        raw = self.command(
            ["docker", "exec", "-i", self.server, "sh", "-c", script],
            payload=body,
            seconds=min(20, remaining),
            empty_list_path=path if operation == "list" else None,
        )
        if destroying:
            return {}
        try:
            return json.loads(raw, object_pairs_hook=unique_fields)
        except (ValueError, TypeError):
            raise Blocked() from None

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
        )

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
        self.command(["docker", "start", self.agent])
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
    files = {"issue-renderer-secret-id.sh", "renderer-issuance.py"}

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
        for name in files:
            if (
                not isinstance(hashes[name], str)
                or not re.fullmatch(r"[a-f0-9]{64}", hashes[name])
                or hashlib.sha256(read_private(name)).hexdigest() != hashes[name]
            ):
                raise Blocked()
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
    validate_receipt(revision)
    tokens = [sys.stdin.readline(1025).strip() for _ in range(2)]
    if any(not SAFE.fullmatch(t) or len(t) > 1024 for t in tokens):
        raise Blocked()
    validate_binding(server, volume, agent, directory)
    api = DockerAPI(server, volume, agent, *tokens)
    if not (Path(directory) / "issuance.json").exists():
        running = api.command(
            [
                "docker",
                "inspect",
                "--type=container",
                "--format",
                "{{.State.Running}}",
                agent,
            ]
        ).strip()
        if running != b"false":
            raise Blocked()
    api.validate_tokens()
    with Journal(directory) as journal:
        if journal.load() is None:
            running = api.command(
                [
                    "docker",
                    "inspect",
                    "--type=container",
                    "--format",
                    "{{.State.Running}}",
                    agent,
                ]
            ).strip()
            if running != b"false":
                raise Blocked()
        run_issuance(api, journal, revision=revision)
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
