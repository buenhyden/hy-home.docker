#!/usr/bin/env python3
# fmt: off
"""One retained, isolated semantic restore of the selected HOME OpenBao snapshot.

The controller, not this program, owns authorization and writer quiescence. This
program consumes an exact reviewed recovery contract and a live lease FD. Secret
bytes stay on protected FDs/stdin or in memory. Any uncertainty after the durable
attempt ledger is created retains the target and ledger and forbids an automatic
retry.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import hmac
import http.client
import ipaddress
import json
import os
import re
import shutil
import ssl
import stat
import sys
import tempfile
import threading
import time
import types
from pathlib import Path

TARGET = Path("/home/hyunyoun/storage/volumes/security/openbao/p01-restore-20261014-05")
PARENT_IDENTITY = (2064, 115612004, 1000, 1000)
ATTEMPT = "p01-restore-20261014-05"
LEDGER = ".p01-restore-20261014-05.attempt.json"
CLUSTER = "51fbfa38-a715-7dca-629f-3f07233749f4"
OLD_IMAGE = "sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641"
OLD_VERSION = "2.6.2"
OWNED_VERSION = "2.7.1+hyhome.go1.27.2.net0.60.0.r1"
PARENT_NAME = "protected-maintenance.py"
PARENT_SHA256 = "2c6101572dca382752cc5cef25f9d5d1ed18804e40c43984f41ea6e5d80734a2"
ARCHIVE_NAME = "protected-snapshot-archive.py"
ARCHIVE_SHA256 = "48ff7d0e0ee6e39b00c5105df5fa20891b70ac5e0e820715aad0b675ab028868"
EXECUTION_NAME = "protected-semantic-execution.py"
EXECUTION_SHA256 = "137a8509f7e5180afad16008ca4c4903cc1386cdc3635e94d620d782dfd1d39b"
CANARY_FIELD_NAME = "admin_password"
CANARIES = (("secret/data/hy-home/02-auth/keycloak", CANARY_FIELD_NAME), ("secret/data/hy-home/06-observability/grafana", CANARY_FIELD_NAME))
SERVER_LIMITS = ("--memory", "512m", "--memory-swap", "512m", "--cpus", "1", "--pids-limit", "512")
SMALL_LIMITS = ("--memory", "32m", "--memory-swap", "32m", "--cpus", "0.25", "--pids-limit", "16")
HEX64 = re.compile(r"[a-f0-9]{64}")
MAX_JSON = 65536


class Blocked(Exception):
    """A sanitized precondition failure."""


class Indeterminate(Blocked):
    """An effect may have occurred; retain the attempt."""


def _signature(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Blocked()
        result[key] = value
    return result


def _json(raw, *, maximum=MAX_JSON):
    if not 1 <= len(raw) <= maximum:
        raise Blocked()
    try:
        value = json.loads(raw, object_pairs_hook=_unique)
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise Blocked() from None
    pending = [(value, 0)]
    count = 0
    while pending:
        node, depth = pending.pop()
        count += 1
        if count > 2048 or depth > 16:
            raise Blocked()
        if isinstance(node, dict):
            pending.extend((item, depth + 1) for item in node.values())
        elif isinstance(node, list):
            pending.extend((item, depth + 1) for item in node)
    return value


def _digest_fd(descriptor, size):
    digest = hashlib.sha256()
    offset = 0
    while offset < size:
        raw = os.pread(descriptor, min(65536, size - offset), offset)
        if not raw:
            raise Blocked()
        digest.update(raw)
        offset += len(raw)
    return digest.hexdigest()


def _open_held(path, expected_sha256, *, maximum=MAX_JSON, private=False):
    if not HEX64.fullmatch(expected_sha256):
        raise Blocked()
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        modes = {0o600} if private else {0o400, 0o440, 0o600, 0o640, 0o644}
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid not in {0, os.getuid()} or stat.S_IMODE(info.st_mode) not in modes or not 1 <= info.st_size <= maximum or not hmac.compare_digest(_digest_fd(descriptor, info.st_size), expected_sha256):
            raise Blocked()
        return descriptor, info
    except BaseException:
        os.close(descriptor)
        raise


def _open_directory(path):
    path = Path(path)
    if not path.is_absolute() or any(part in {".", ".."} for part in path.parts):
        raise Blocked()
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for component in path.parts[1:]:
            following = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = following
        return descriptor
    except OSError:
        os.close(descriptor)
        raise Blocked() from None


def _load_public(name, digest, required, module_name):
    path = Path(__file__).absolute().with_name(name)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_uid not in {0, os.getuid()} or stat.S_IMODE(before.st_mode) not in {0o400, 0o440, 0o500, 0o600, 0o640, 0o644} or not 1 <= before.st_size <= 1024 * 1024:
            raise Blocked()
        raw = os.pread(descriptor, before.st_size, 0)
        if len(raw) != before.st_size or _signature(before) != _signature(os.fstat(descriptor)) or _signature(before) != _signature(os.lstat(path)) or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), digest):
            raise Blocked()
        namespace = {"__builtins__": __builtins__, "__file__": str(path), "__name__": module_name}
        exec(compile(raw, str(path), "exec"), namespace)
        if any(name not in namespace for name in required):
            raise Blocked()
        return types.SimpleNamespace(**namespace)
    except (OSError, SyntaxError, ValueError, TypeError):
        raise Blocked() from None
    finally:
        os.close(descriptor)


def load_dependencies():
    parent = _load_public(PARENT_NAME, PARENT_SHA256, ("API", "Blocked", "PinnedConnection", "ca_context", "check_operator", "hidden_input", "parse_response", "read_secret_fd"), "_semantic_restore_parent")
    archive = _load_public(ARCHIVE_NAME, ARCHIVE_SHA256, ("ArchiveBlocked", "validate_archive"), "_semantic_restore_archive")
    execution = _load_public(EXECUTION_NAME, EXECUTION_SHA256, ("BoundedRunner", "CommandRunner", "ContainerRuntime", "CustodyError", "HeldBytes", "ProcessError", "cleanup_exact"), "_semantic_restore_execution")
    return parent, archive, execution


def _extract_kv(document, field):
    if not isinstance(document, dict):
        raise Blocked()
    envelope = document.get("data")
    if not isinstance(envelope, dict) or set(envelope) != {"data", "metadata"}:
        raise Blocked()
    data, metadata = envelope["data"], envelope["metadata"]
    value = data.get(field) if isinstance(data, dict) else None
    version = metadata.get("version") if isinstance(metadata, dict) else None
    if not isinstance(value, str) or not 1 <= len(value) <= 4096 or type(version) is not int or version <= 0 or metadata.get("destroyed") is not False or metadata.get("deletion_time") != "":
        raise Blocked()
    return value, version


class LiveCanaries:
    def __init__(self, parent, token, context, connect_ip):
        self.parent, self.token, self.context = parent, token, context
        self.connect_ip = str(ipaddress.ip_address(connect_ip))

    def _get(self, route, field):
        connection = self.parent.PinnedConnection("openbao.hy.home.arpa", 443, connect_ip=self.connect_ip, context=self.context, timeout=20)
        timer = threading.Timer(20, connection.abort)
        timer.daemon = True
        timer.start()
        try:
            connection.request("GET", "/v1/" + route, body=None, headers={"X-Vault-Token": self.token, "Accept": "application/json"})
            response = connection.getresponse()
            headers = response.getheaders()
            if response.status != 200 or any(name.lower() == "location" for name, _ in headers):
                raise Blocked()
            raw = response.read(MAX_JSON + 1)
            try:
                document = self.parent.parse_response(raw)
            except self.parent.Blocked:
                raise Blocked() from None
            return _extract_kv(document, field)
        except Blocked:
            raise
        except (OSError, ssl.SSLError, http.client.HTTPException, ValueError):
            raise Blocked() from None
        finally:
            timer.cancel()
            connection.close()

    def read_all(self):
        return tuple(self._get(*canary) for canary in CANARIES)


class QuiescenceLease:
    KEYS = frozenset({"schema_version", "lease_id", "started_at_utc", "expires_at_utc", "released_at_utc", "snapshot_sha256"})

    def __init__(self, descriptor, lease_id, snapshot_sha256, lease_sha256):
        info = os.fstat(descriptor)
        if descriptor < 3 or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid not in {0, os.getuid()} or stat.S_IMODE(info.st_mode) != 0o600 or not 1 <= info.st_size <= 8192 or os.lseek(descriptor, 0, os.SEEK_CUR) != 0 or not re.fullmatch(r"[a-f0-9]{32}", lease_id) or not HEX64.fullmatch(snapshot_sha256) or not HEX64.fullmatch(lease_sha256):
            raise Blocked()
        self.fd, self.signature = descriptor, _signature(info)
        self.raw = os.pread(descriptor, info.st_size, 0)
        self.lease_id, self.snapshot_sha256 = lease_id, snapshot_sha256
        if not hmac.compare_digest(hashlib.sha256(self.raw).hexdigest(), lease_sha256):
            raise Blocked()

    def recheck(self, saved_at, now=None):
        info = os.fstat(self.fd)
        raw = os.pread(self.fd, info.st_size, 0)
        if _signature(info) != self.signature or raw != self.raw:
            raise Blocked()
        value = _json(raw, maximum=8192)
        if not isinstance(value, dict) or set(value) != self.KEYS:
            raise Blocked()
        try:
            start = datetime.datetime.fromisoformat(value["started_at_utc"])
            expiry = datetime.datetime.fromisoformat(value["expires_at_utc"])
            saved = datetime.datetime.fromisoformat(saved_at)
            moment = datetime.datetime.now(datetime.UTC).timestamp() if now is None else now
            valid_time = all(item.tzinfo is not None for item in (start, saved, expiry)) and start <= saved and saved.timestamp() <= moment < expiry.timestamp()
        except (TypeError, ValueError):
            raise Blocked() from None
        if value["schema_version"] != 1 or value["lease_id"] != self.lease_id or value["snapshot_sha256"] != self.snapshot_sha256 or value["released_at_utc"] is not None or not valid_time:
            raise Blocked()


class Admission:
    def __init__(self, contract, contract_held, snapshot_fd, snapshot_info, receipt, archive, lease):
        self.contract, self.snapshot_fd, self.snapshot_info = (contract, snapshot_fd, snapshot_info)
        self.contract_held, self.receipt, self.archive, self.lease = contract_held, receipt, archive, lease
        self._validate_snapshot()
        self._target_absent()

    def _validate_snapshot(self):
        try:
            validation = self.archive.validate_archive(self.snapshot_fd)
        except self.archive.ArchiveBlocked:
            raise Blocked() from None
        expected = self.contract["snapshot"]
        metadata = validation["metadata"]
        if _signature(os.fstat(self.snapshot_fd)) != _signature(self.snapshot_info) or validation["sha256"] != expected["sha256"] or validation["size"] != expected["size"] or (self.snapshot_info.st_dev, self.snapshot_info.st_ino) != (expected["dev"], expected["ino"]) or metadata["Index"] != expected["raft_index"] or metadata["Term"] != expected["raft_term"]:
            raise Blocked()
        self.contract_held.revalidate()
        self.receipt.revalidate()
        try:
            receipt = self.receipt.json()
        except Exception:
            raise Blocked() from None
        saved = receipt.get("saved_at_utc")
        if receipt.get("http_status") != 200 or not isinstance(saved, str) or receipt.get("sha256") != expected["sha256"] or receipt.get("size") != expected["size"] or receipt.get("dev") != expected["dev"] or receipt.get("ino") != expected["ino"] or receipt.get("cluster_id") != CLUSTER or receipt.get("version") != OLD_VERSION:
            raise Blocked()
        self.saved_at = saved

    def _target_absent(self):
        parent = _open_directory(TARGET.parent)
        try:
            info = os.fstat(parent)
            if (info.st_dev, info.st_ino, info.st_uid, info.st_gid) != PARENT_IDENTITY:
                raise Blocked()
            os.stat(TARGET.name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return
        finally:
            os.close(parent)
        raise Blocked()

    def pre_read(self):
        self._validate_snapshot()
        self.lease.recheck(self.saved_at)
        self._target_absent()

    def post_read(self):
        self._validate_snapshot()
        self.lease.recheck(self.saved_at)
        self._target_absent()


def orchestrate(admission, reader, effects):
    if hasattr(effects, "preflight"):
        effects.preflight()
    admission.pre_read()
    reference = reader.read_all()
    admission.post_read()
    return effects.perform(reference)


def container_security(limits):
    return ["--pull=never", "--log-driver=none", "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--read-only", *limits]


def _write_all(descriptor, raw):
    while raw:
        count = os.write(descriptor, raw)
        if count <= 0:
            raise OSError()
        raw = raw[count:]


class AttemptLedger:
    def __init__(self, contract_digest):
        parent = _open_directory(TARGET.parent)
        descriptor = None
        try:
            info = os.fstat(parent)
            if (info.st_dev, info.st_ino, info.st_uid, info.st_gid) != PARENT_IDENTITY:
                raise Blocked()
            descriptor = os.open(LEDGER, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=parent)
            self.fd = descriptor
            os.fchmod(self.fd, 0o600)
            self.parent = parent
            self.write("admitted", contract_digest)
        except BaseException:
            if descriptor is not None:
                os.close(descriptor)
            os.close(parent)
            raise

    def write(self, state, contract_digest, **public):
        document = {"schema_version": 1, "attempt": ATTEMPT, "state": state, "contract_sha256": contract_digest, **public}
        raw = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        os.lseek(self.fd, 0, os.SEEK_SET)
        os.ftruncate(self.fd, 0)
        _write_all(self.fd, raw)
        os.fsync(self.fd)
        os.fsync(self.parent)

    def close(self):
        os.close(self.fd)
        os.close(self.parent)


def success_receipt(reference, lease_id, snapshot_sha256, raft_index, raft_term):
    # Equality is public; values, hashes, lengths and response metadata are not.
    return {"canaries_equal": len(reference) == 2, "lease_id": lease_id, "snapshot_sha256": snapshot_sha256, "raft_index": raft_index, "raft_term": raft_term}


class RecoveryEffects:
    def __init__(self, options, contract, admission, secrets, contract_digest, execution):
        self.options, self.contract, self.admission = options, contract, admission
        self.home_token, self.root_token, self.shares = secrets
        self.contract_digest = contract_digest
        self.execution = execution
        self.runner = execution.CommandRunner(time.monotonic() + 900, Indeterminate)
        self.runtime = execution.ContainerRuntime(self.runner, ATTEMPT, Indeterminate)
        self.ledger = None
        self.held_artifacts = []

    def _hold(self, path, digest, *, private=False):
        try:
            held = self.execution.HeldBytes.open(path, digest, maximum=1024 * 1024, private=private)
        except self.execution.CustodyError:
            raise Blocked() from None
        self.held_artifacts.append(held)
        return held

    def _held_json(self, path, digest):
        try:
            return self._hold(path, digest).json()
        except self.execution.CustodyError:
            raise Blocked() from None

    def preflight(self):
        for image, expected in ((OLD_IMAGE, OLD_IMAGE), (self.contract["candidate"]["reference"], self.contract["candidate"]["image_id"])):
            result = self.runtime.docker("image", "inspect", "--platform=linux/amd64", "--format", "{{.Id}}", image)
            if result.stdout.strip().decode() != expected:
                raise Blocked()
        for name in (ATTEMPT + "-old", ATTEMPT + "-candidate", ATTEMPT + "-agent", ATTEMPT + "-watcher"):
            if self.runtime.docker("inspect", "--type=container", name, allow_failure=True).returncode == 0:
                raise Blocked()
        if self.runner.run(["findmnt", "-n", "-o", "FSTYPE", "--target", "/dev/shm"]).stdout.strip() != b"tmpfs":
            raise Blocked()
        renderer = self.contract["renderer"]
        helper = Path(renderer["helper"])
        if not helper.is_absolute() or helper.is_symlink():
            raise Blocked()
        receipt = self._held_json(helper.parent / "source-receipt.json", renderer["helper_receipt_sha256"])
        self.held_artifacts[-1].install = ("helper/source-receipt.json", 0o400)
        helper_names = {"issue-renderer-secret-id.sh", "renderer-issuance.py", "renderer-request.sh"}
        if not isinstance(receipt, dict) or set(receipt) != {"source_revision", "sha256"} or receipt["source_revision"] != renderer["revision"] or not isinstance(receipt["sha256"], dict) or set(receipt["sha256"]) != helper_names:
            raise Blocked()
        for name, mode in (("issue-renderer-secret-id.sh", 0o500), ("renderer-issuance.py", 0o400), ("renderer-request.sh", 0o400)):
            if stat.S_IMODE(self._hold(helper.parent / name, receipt["sha256"][name]).info.st_mode) != mode:
                raise Blocked()
            self.held_artifacts[-1].install = ("helper/" + name, mode)
        self._verify_bundle(Path(renderer["bundle"]), renderer["bundle_receipt_sha256"])

    def _verify_bundle(self, bundle, digest):
        required = {"scripts/start-agent.sh", "scripts/health-agent.sh", "config/agent.hcl", "config/templates/keycloak_admin_password.ctmpl", "config/templates/grafana_admin_password.ctmpl", "config/templates/keycloak_admin_password_version.ctmpl", "config/templates/grafana_admin_password_version.ctmpl"}
        receipt = self._held_json(bundle / "source-receipt.json", digest)
        if not isinstance(receipt, dict) or set(receipt) != {"source_revision", "sha256"} or receipt["source_revision"] != self.contract["renderer"]["revision"] or set(receipt["sha256"]) != required:
            raise Blocked()
        for name, expected in receipt["sha256"].items():
            self._hold(bundle / name, expected)
            self.held_artifacts[-1].install = ("bundle/" + name, 0o400)

    def _materialize_artifacts(self, directory):
        trusted = directory / "trusted"
        trusted.mkdir(mode=0o700)
        try:
            for held in self.held_artifacts:
                held.revalidate()
                if hasattr(held, "install"):
                    held.materialize(trusted, *held.install)
        except self.execution.CustodyError:
            raise Blocked() from None
        self.materialized_helper = trusted / "helper/issue-renderer-secret-id.sh"
        self.materialized_bundle = trusted / "bundle"

    def _tmp(self):
        directory = Path(tempfile.mkdtemp(prefix=ATTEMPT + "-", dir="/dev/shm"))
        directory.chmod(0o700)
        if directory.lstat().st_uid != os.getuid() or stat.S_IMODE(directory.lstat().st_mode) != 0o700:
            raise Indeterminate()
        return directory

    def _copy_snapshot(self, directory):
        target = directory / "raft.snap"
        fd = os.open(target, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o440)
        try:
            offset = 0
            while offset < self.admission.snapshot_info.st_size:
                raw = os.pread(self.admission.snapshot_fd, min(65536, self.admission.snapshot_info.st_size - offset), offset)
                if not raw:
                    raise Indeterminate()
                _write_all(fd, raw)
                offset += len(raw)
            os.fchmod(fd, 0o440)
            os.fsync(fd)
            if _signature(os.fstat(self.admission.snapshot_fd)) != _signature(self.admission.snapshot_info):
                raise Indeterminate()
            if _digest_fd(fd, offset) != self.contract["snapshot"]["sha256"] or os.fstat(fd).st_nlink != 1:
                raise Indeterminate()
        finally:
            os.close(fd)

    def _prepare_target(self):
        os.mkdir(TARGET.name, 0o700, dir_fd=self.ledger.parent)
        name = ATTEMPT + "-chown"
        args = ["create", "--name", name, "--label", "hy-home.attempt=" + ATTEMPT, "--network=none", *container_security(SMALL_LIMITS), "--user", "0:0", "--cap-add", "CHOWN", "--mount", f"type=bind,src={TARGET},dst=/restore-target", "--entrypoint", "/bin/chown", OLD_IMAGE, "100:1000", "/restore-target"]
        identity = self.runtime.remember("container", self.runtime.docker(*args))
        self.runtime.docker("start", "--attach", identity)
        if self.runtime.docker("inspect", "--format", "{{.State.ExitCode}} {{.State.OOMKilled}}", identity).stdout.strip() != b"0 false":
            raise Indeterminate()
        info = TARGET.lstat()
        if (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode), info.st_dev) != (100, 1000, 0o700, PARENT_IDENTITY[0]):
            raise Indeterminate()

    def _watcher(self):
        name = ATTEMPT + "-watcher"
        script = 'while :; do m=$(find /target -xdev -mindepth 1 -exec stat -c \'%s %b %F\' \'{}\' \';\' | awk \'$3!="regular"&&$3!="directory"{exit 3} NR>64{exit 4}{a+=$1;b+=$2*512} END{if(NR<=64)print NR,a,b}\'); set -- $m; [ "$#" = 3 ] && [ "$2" -le 1073741824 ] && [ "$3" -le 1073741824 ]; sleep 1; done'
        result = self.runtime.docker("create", "--name", name, "--label", "hy-home.attempt=" + ATTEMPT, "--network=none", *container_security(SMALL_LIMITS), "--user", "100:1000", "--mount", f"type=bind,src={TARGET},dst=/target,readonly", "--entrypoint", "/bin/sh", OLD_IMAGE, "-ec", script)
        identity = self.runtime.remember("container", result)
        self.runtime.watcher = identity
        self.runtime.docker("start", identity)
        self.runner.engine.probe = self.runtime.watcher_probe

    def _watcher_ok(self):
        self.runtime.watcher_probe()

    def _server(self, name, image, directory, network):
        config = {"ui": False, "disable_mlock": True, "storage": {"raft": {"path": "/openbao/data", "node_id": "p01-restore"}}, "listener": [{"tcp": {"address": "0.0.0.0:8200", "cluster_address": "0.0.0.0:8201", "tls_disable": False, "tls_min_version": "tls12", "tls_cert_file": "/openbao/tls/server.pem", "tls_key_file": "/openbao/tls/server-key.pem"}}], "api_addr": "https://openbao:8200", "cluster_addr": "https://openbao:8201", "audit": [{"type": "file", "path": "p01-file", "options": {"file_path": "/openbao/audit/audit.json", "mode": "0600", "log_raw": "false", "hmac_accessor": "true"}}]}
        args = ["create", "--name", name, "--label", "hy-home.attempt=" + ATTEMPT, "--network", network, *container_security(SERVER_LIMITS), "--user", "100:1000", "--env", "BAO_ADDR=https://127.0.0.1:8200", "--env", "BAO_CACERT=/openbao/tls/ca.pem", "--env", "BAO_TLS_SERVER_NAME=openbao", "--env", "BAO_TOKEN_PATH=/openbao/private/token", "--env", "BAO_LOCAL_CONFIG=" + json.dumps(config, separators=(",", ":")), "--mount", f"type=bind,src={TARGET},dst=/openbao/data", "--mount", f"type=bind,src={directory / 'tls'},dst=/openbao/tls,readonly", "--mount", f"type=bind,src={directory / 'raft.snap'},dst=/restore/raft.snap,readonly", "--tmpfs", "/openbao/private:rw,noexec,nosuid,nodev,size=1m,mode=0700,uid=100,gid=1000", "--tmpfs", "/openbao/audit:rw,noexec,nosuid,nodev,size=16m,mode=0700,uid=100,gid=1000", "--tmpfs", "/openbao/config:rw,noexec,nosuid,nodev,size=1m,mode=0700,uid=100,gid=1000", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=40m,mode=0700,uid=100,gid=1000", image, "server"]
        if network != "none":
            args[args.index("--network") + 2 : args.index("--network") + 2] = ["--network-alias", "openbao"]
        identity = self.runtime.remember("container", self.runtime.docker(*args))
        self.runtime.docker("start", identity)
        return identity

    def _json_exec(self, server, *command, input=None, allow_failure=False):
        result = self.runtime.exec(server, "bao", *command, input=input, allow_failure=allow_failure)
        return result, (_json(result.stdout) if result.returncode == 0 else None)

    def _wait_status(self, server, initialized, sealed):
        for _ in range(40):
            result = self.runtime.exec(server, "bao", "status", "-format=json", allow_failure=True)
            try:
                value = _json(result.stdout)
                if value.get("initialized") is initialized and value.get("sealed") is sealed:
                    return value
            except Blocked:
                pass
            time.sleep(0.25)
        raise Indeterminate()

    def _unseal(self, server, share):
        self._json_exec(server, "write", "-format=json", "sys/unseal", "key=-", input=share.encode())

    def _status(self, server, version):
        _result, value = self._json_exec(server, "status", "-format=json")
        if value.get("sealed") is not False or value.get("cluster_id") != CLUSTER or value.get("version") != version or value.get("storage_type") != "raft":
            raise Indeterminate()

    def _canaries(self, server):
        values = []
        for route, field in CANARIES:
            _result, value = self._json_exec(server, "read", "-format=json", route)
            values.append(_extract_kv(value, field))
        return tuple(values)

    def _init_restore(self, old, directory):
        self._wait_status(old, False, True)
        _result, initialized = self._json_exec(old, "operator", "init", "-format=json", "-key-shares=3", "-key-threshold=2")
        root = initialized.get("root_token")
        shares = initialized.get("unseal_keys_b64")
        if not isinstance(root, str) or not isinstance(shares, list) or len(shares) != 3 or len(set(shares)) != 3:
            raise Indeterminate()
        self.runtime.login(old, root)
        self.runtime.restore(old)
        self._wait_status(old, True, True)
        # Shamir cannot reject a share below the threshold, so the restored keyring is
        # proven foreign only when a threshold of throwaway shares fails to combine.
        _result, first = self._json_exec(old, "write", "-format=json", "sys/unseal", "key=-", input=shares[0].encode())
        first = first.get("data", first) if isinstance(first, dict) else {}
        if first.get("sealed") is not True or first.get("progress") != 1:
            raise Indeterminate()
        denied = self.runtime.exec(old, "bao", "write", "-format=json", "sys/unseal", "key=-", input=shares[1].encode(), allow_failure=True)
        if denied.returncode == 0 or b"invalid key" not in denied.stderr:
            raise Indeterminate()
        self.runtime.exec(old, "bao", "operator", "unseal", "-reset")
        for share in self.shares:
            self._unseal(old, share)
        self.runtime.login(old, self.root_token)
        self._status(old, OLD_VERSION)

    def _create_tokens(self, server):
        tokens = []
        try:
            for role in ("renderer-issuer", "renderer-cleanup"):
                _result, value = self._json_exec(server, "write", "-format=json", "auth/token/create/" + role, "-", input=b"{}")
                token = value.get("auth", {}).get("client_token")
                if not isinstance(token, str) or not 1 <= len(token) <= 1024:
                    raise Indeterminate()
                tokens.append(token)
        except BaseException:
            self._revoke_tokens(server, tokens)
            raise
        return tuple(tokens)

    def _revoke_tokens(self, server, tokens):
        failed = False
        for token in tokens:
            try:
                self._json_exec(server, "write", "-format=json", "auth/token/revoke", "-", input=json.dumps({"token": token}, separators=(",", ":")).encode())
            except BaseException:
                failed = True
        if failed:
            raise Indeterminate()

    def _agent(self, server, directory, reference):
        bundle = self.materialized_bundle
        auth, out, journal = (directory / name for name in ("agent", "out", "journal"))
        for path in (auth, out):
            path.mkdir(mode=0o770)
        journal.mkdir(mode=0o700)
        _result, role = self._json_exec(server, "read", "-format=json", "auth/approle/role/hy-home-renderer/role-id")
        role_id = role.get("data", {}).get("role_id")
        if not isinstance(role_id, str):
            raise Indeterminate()
        role_file = auth / "role_id"
        role_fd = os.open(role_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            _write_all(role_fd, role_id.encode())
            os.fsync(role_fd)
        finally:
            os.close(role_fd)
        prep = ATTEMPT + "-agent-chown"
        result = self.runtime.docker("create", "--name", prep, "--label", "hy-home.attempt=" + ATTEMPT, "--network=none", *container_security(SMALL_LIMITS), "--user", "0:0", "--cap-add", "CHOWN", "--mount", f"type=bind,src={auth},dst=/agent", "--mount", f"type=bind,src={out},dst=/out", "--mount", f"type=bind,src={bundle},dst=/bundle", "--entrypoint", "/bin/chown", OLD_IMAGE, "-R", "100:1000", "/agent", "/out", "/bundle")
        prep_id = self.runtime.remember("container", result)
        self.runtime.docker("start", "--attach", prep_id)
        if self.runtime.docker("inspect", "--format", "{{.State.ExitCode}} {{.State.OOMKilled}}", prep_id).stdout.strip() != b"0 false":
            raise Indeterminate()
        result = self.runtime.docker("volume", "create", "--label", "hy-home.attempt=" + ATTEMPT, "--opt", "type=none", "--opt", "o=bind", "--opt", "device=" + str(auth))
        volume_id = self.runtime.remember("volume", result)
        agent = ATTEMPT + "-agent"
        image = self.contract["candidate"]["reference"]
        result = self.runtime.docker("create", "--name", agent, "--label", "hy-home.attempt=" + ATTEMPT, "--network", self.runtime.networks[-1], *container_security(SERVER_LIMITS), "--user", "100:1000", "--env", "BAO_ADDR=https://openbao:8200", "--env", "VAULT_ADDR=https://openbao:8200", "--env", "BAO_CACERT=/openbao/tls/ca.pem", "--env", "VAULT_CACERT=/openbao/tls/ca.pem", "--mount", f"type=bind,src={bundle / 'scripts'},dst=/openbao/scripts,readonly", "--mount", f"type=bind,src={bundle / 'config'},dst=/openbao/config,readonly", "--mount", f"type=bind,src={directory / 'tls' / 'ca.pem'},dst=/openbao/tls/ca.pem,readonly", "--mount", f"type=volume,src={volume_id},dst=/openbao/agent", "--mount", f"type=bind,src={out},dst=/openbao/out", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777", "--entrypoint", "/bin/sh", image, "/openbao/scripts/start-agent.sh")
        agent_id = self.runtime.remember("container", result)
        issuer, cleanup = self._create_tokens(server)
        helper = self.materialized_helper
        try:
            result = self.runner.run([str(helper), server, volume_id, image, agent_id, str(journal), self.contract["renderer"]["revision"]], input=(issuer + "\n" + cleanup + "\n").encode())
            if result.returncode:
                raise Indeterminate()
            rendered = []
            for value_path, version_path in (("/openbao/out/auth/keycloak_admin_password.txt", "/openbao/out/auth/keycloak_admin_password.version"), ("/openbao/out/observability/grafana_admin_password.txt", "/openbao/out/observability/grafana_admin_password.version")):
                value = self.runtime.exec(agent_id, "/bin/cat", value_path).stdout.decode().rstrip("\n")
                raw_version = self.runtime.exec(agent_id, "/bin/cat", version_path).stdout.decode().strip()
                if not raw_version.isdecimal() or not value:
                    raise Indeterminate()
                rendered.append((value, int(raw_version)))
            if tuple(rendered) != reference:
                raise Indeterminate()
        finally:
            self._revoke_tokens(server, (issuer, cleanup))

    def _tls(self, directory):
        tls, issuer = directory / "tls", directory / "issuer"
        tls.mkdir(mode=0o750)
        issuer.mkdir(mode=0o700)
        ca_key, ca, key, csr, cert = (issuer / "ca-key.pem", tls / "ca.pem", tls / "server-key.pem", issuer / "server.csr", tls / "server.pem")
        self.runner.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(ca_key), "-out", str(ca), "-days", "1", "-subj", "/CN=P01 Restore CA"])
        self.runner.run(["openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes", "-keyout", str(key), "-out", str(csr), "-subj", "/CN=openbao"])
        ext = issuer / "server.ext"
        ext.write_text("subjectAltName=DNS:openbao,IP:127.0.0.1\nextendedKeyUsage=serverAuth\n")
        self.runner.run(["openssl", "x509", "-req", "-in", str(csr), "-CA", str(ca), "-CAkey", str(ca_key), "-CAcreateserial", "-out", str(cert), "-days", "1", "-extfile", str(ext)])
        ca_key.chmod(0o600)
        ca.chmod(0o644)
        cert.chmod(0o644)
        key.chmod(0o640)

    def perform(self, reference):
        directory = None
        cleaned = False
        try:
            directory = self._tmp()
            self._materialize_artifacts(directory)
            self._copy_snapshot(directory)
            self._tls(directory)
            self.ledger = AttemptLedger(self.contract_digest)
            self.ledger.write("effect-started", self.contract_digest)
            self._prepare_target()
            self._watcher()
            self._watcher_ok()
            old = self._server(ATTEMPT + "-old", OLD_IMAGE, directory, "none")
            self._init_restore(old, directory)
            if self._canaries(old) != reference:
                raise Indeterminate()
            self.runtime.docker("stop", "--time", "10", old)
            self.runtime.docker("rm", old)
            self.runtime.containers.remove(old)
            result = self.runtime.docker("network", "create", "--internal", "--label", "hy-home.attempt=" + ATTEMPT, ATTEMPT + "-net")
            network = self.runtime.remember("network", result)
            candidate = self._server(ATTEMPT + "-candidate", self.contract["candidate"]["reference"], directory, network)
            self._wait_status(candidate, True, True)
            for share in self.shares:
                self._unseal(candidate, share)
            self.runtime.login(candidate, self.root_token)
            self._status(candidate, OWNED_VERSION)
            if self._canaries(candidate) != reference:
                raise Indeterminate()
            self._agent(candidate, directory, reference)
            self.runtime.exec(candidate, "bao", "token", "revoke", "-self")
            denied = self.runtime.exec(candidate, "bao", "read", "-format=json", "auth/token/lookup-self", allow_failure=True)
            if denied.returncode == 0 or b"403" not in denied.stderr:
                raise Indeterminate()
            self._watcher_ok()
            receipt = success_receipt(reference, self.contract["quiescence"]["lease_id"], self.contract["snapshot"]["sha256"], self.contract["snapshot"]["raft_index"], self.contract["snapshot"]["raft_term"])
            self.runtime.cleanup()
            cleaned = True
            shutil.rmtree(directory)
            directory = None
            self.ledger.write("accepted", self.contract_digest, **receipt)
            return receipt
        except BaseException:
            if self.ledger is not None:
                try:
                    self.ledger.write("indeterminate", self.contract_digest)
                except OSError:
                    pass
                raise Indeterminate() from None
            raise Blocked() from None
        finally:
            try:
                if not cleaned:
                    self.runtime.cleanup()
            finally:
                if directory is not None:
                    try:
                        shutil.rmtree(directory)
                    except OSError:
                        pass
                if self.ledger is not None:
                    self.ledger.close()
                for held in self.held_artifacts:
                    held.close()


def _contract(path, digest, execution):
    try:
        held = execution.HeldBytes.open(path, digest)
        value = held.json()
    except execution.CustodyError:
        raise Blocked() from None
    def rejected():
        held.close()
        raise Blocked()
    required = {"schema_version", "attempt", "target", "parent", "snapshot", "quiescence", "candidate", "renderer", "security_receipt_sha256"}
    if not isinstance(value, dict) or set(value) != required or value["schema_version"] != 1 or value["attempt"] != ATTEMPT or value["target"] != str(TARGET):
        rejected()
    if value["parent"] != {"dev": 2064, "ino": 115612004, "uid": 1000, "gid": 1000}:
        rejected()
    snapshot_keys = {"sha256", "receipt_sha256", "dev", "ino", "size", "cluster_id", "version", "raft_index", "raft_term"}
    snapshot = value["snapshot"]
    if not isinstance(snapshot, dict) or set(snapshot) != snapshot_keys or snapshot["cluster_id"] != CLUSTER or snapshot["version"] != OLD_VERSION or not HEX64.fullmatch(snapshot["sha256"]) or not HEX64.fullmatch(snapshot["receipt_sha256"]):
        rejected()
    candidate = value["candidate"]
    if not isinstance(candidate, dict) or set(candidate) != {"reference", "image_id", "version"} or candidate["version"] != OWNED_VERSION or not candidate["reference"].startswith("hy-home/openbao:2.7.1-go1.27.2-net0.60.0-r1@sha256:") or not re.fullmatch(r"sha256:[a-f0-9]{64}", candidate["image_id"]):
        rejected()
    quiescence = value["quiescence"]
    if not isinstance(quiescence, dict) or set(quiescence) != {"lease_id", "lease_sha256"} or not re.fullmatch(r"[a-f0-9]{32}", quiescence["lease_id"]) or not HEX64.fullmatch(quiescence["lease_sha256"]):
        rejected()
    renderer = value["renderer"]
    if not isinstance(renderer, dict) or set(renderer) != {"helper", "bundle", "revision", "helper_receipt_sha256", "bundle_receipt_sha256"} or not Path(renderer["helper"]).is_absolute() or not Path(renderer["bundle"]).is_absolute() or not re.fullmatch(r"[a-f0-9]{40}", renderer["revision"]) or not HEX64.fullmatch(renderer["helper_receipt_sha256"]) or not HEX64.fullmatch(renderer["bundle_receipt_sha256"]):
        rejected()
    return value, held


def _secrets(parent, options):
    fds = (options.home_read_fd, options.root_fd, options.share_1_fd, options.share_2_fd)
    if all(fd is None for fd in fds):
        values = tuple(parent.hidden_input(label) for label in ("HOME operator token", "Restored root token", "Unseal share 1", "Unseal share 2"))
    elif all(type(fd) is int and fd >= 3 for fd in fds):
        identities = [(os.fstat(fd).st_dev, os.fstat(fd).st_ino) for fd in fds]
        if len(set(identities)) != 4:
            raise Blocked()
        try:
            values = tuple(parent.read_secret_fd(fd) for fd in fds)
        except parent.Blocked:
            raise Blocked() from None
    else:
        raise Blocked()
    if len(set(values)) != 4:
        raise Blocked()
    return values[0], values[1], values[2:]


class PrivateParser(argparse.ArgumentParser):
    def error(self, _message):
        raise Blocked()


def main(arguments=None):
    parser = PrivateParser(description=__doc__)
    for name in ("contract", "contract-sha256", "snapshot", "snapshot-receipt", "security-receipt", "ca", "ca-sha256", "connect-ip"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--quiescence-fd", type=int, required=True)
    for name in ("home-read-fd", "root-fd", "share-1-fd", "share-2-fd"):
        parser.add_argument("--" + name, type=int)
    snapshot_fd = security_fd = effects = None
    contract_held = receipt_held = None
    try:
        options = parser.parse_args(arguments)
        parent, archive, execution = load_dependencies()
        contract, contract_held = _contract(options.contract, options.contract_sha256, execution)
        snapshot_fd, snapshot_info = _open_held(options.snapshot, contract["snapshot"]["sha256"], maximum=32 * 1024 * 1024, private=True)
        try:
            receipt_held = execution.HeldBytes.open(options.snapshot_receipt, contract["snapshot"]["receipt_sha256"], private=True)
        except execution.CustodyError:
            raise Blocked() from None
        security_fd, _ = _open_held(options.security_receipt, contract["security_receipt_sha256"], maximum=1024 * 1024)
        os.close(security_fd)
        security_fd = None
        lease = QuiescenceLease(options.quiescence_fd, contract["quiescence"]["lease_id"], contract["snapshot"]["sha256"], contract["quiescence"]["lease_sha256"])
        context = parent.ca_context(options.ca, options.ca_sha256)
        home_token, root_token, shares = _secrets(parent, options)
        try:
            parent.check_operator(parent.API(home_token, context, options.connect_ip, lookup_only=True).request("GET", "auth/token/lookup-self"))
        except parent.Blocked:
            raise Blocked() from None
        admission = Admission(contract, contract_held, snapshot_fd, snapshot_info, receipt_held, archive, lease)
        effects = RecoveryEffects(options, contract, admission, (home_token, root_token, shares), options.contract_sha256, execution)
        orchestrate(admission, LiveCanaries(parent, home_token, context, options.connect_ip), effects)
        print("RESTORE_ACCEPTED", flush=True)
        return 0
    except Indeterminate:
        print("INDETERMINATE: retain target and ledger; do not retry", file=sys.stderr)
        return 2
    except (Blocked, OSError, ValueError, EOFError, KeyboardInterrupt):
        print("BLOCKED: no restore completion claimed", file=sys.stderr)
        return 1
    finally:
        for descriptor in (snapshot_fd, security_fd):
            if descriptor is not None:
                os.close(descriptor)
        for held in (contract_held, receipt_held):
            if held is not None:
                held.close()
        for held in (() if effects is None else effects.held_artifacts):
            held.close()


if __name__ == "__main__":
    sys.exit(main())
