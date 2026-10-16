"""Private failure evidence boundary for the isolated n8n fixture."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from tests.validation._opsflow_evidence_redaction import redact_text
from tests.validation._supabase_smtp_fixture_storage import write_exclusive

FAILURE_OUTPUT_LIMIT = 256 * 1024
RETAINED_FILE_LIMIT = 64 * 1024 * 1024
METADATA_NAME = "failure-metadata.json"
STREAM_NAMES = {"failure-stdout.txt", "failure-stderr.txt"}
FIXTURE_NAMES = {
    "dev-pg.secret",
    "dev-roles.sql",
    "dev.dump",
    "encryption.secret",
    "ingest.secret",
    "metadata-n8n.secret",
    "metadata-pg.secret",
    "metadata.dump",
    "migrator.secret",
    "notifier.secret",
    "owner.secret",
    "reader.secret",
    "runner.secret",
    "valkey-n8n.secret",
    "valkey-server.secret",
}
RETAINED_NAMES = FIXTURE_NAMES | STREAM_NAMES
FILE_KEYS = {
    "name",
    "device",
    "inode",
    "uid",
    "gid",
    "mode",
    "nlink",
    "bytes",
    "mtime_ns",
    "ctime_ns",
    "sha256",
}
DIRECTORY_KEYS = {"name", "device", "inode", "uid", "gid", "mode", "nlink"}
BODY_FETCH_CONSUMERS = {"n8n_api", "mailpit_capture"}
BODY_FETCH_KINDS = {
    "http_status",
    "fetch_unavailable",
    "transport",
    "response_invalid",
    "unknown",
}
BODY_ERROR_NAMES = {
    "none",
    "Error",
    "TypeError",
    "ReferenceError",
    "SyntaxError",
    "AbortError",
    "other",
}
BODY_CODE_SOURCES = {"none", "cause_code", "error_code", "error_name"}
BODY_ERROR_CODES = {
    "none",
    "connection_refused",
    "connection_reset",
    "timeout",
    "dns",
    "other",
}
BODY_FETCH_FAILURE_JS = r"""
const opsflowNames=new Set(['Error','TypeError','ReferenceError','SyntaxError','AbortError']);
const opsflowCleanError={name:'none',code_source:'none',code:'none'};
const opsflowUnknownError={name:'other',code_source:'none',code:'other'};
const opsflowCode=value=>{
 if(value==='ECONNREFUSED')return 'connection_refused';
 if(value==='ECONNRESET'||value==='UND_ERR_SOCKET')return 'connection_reset';
 if(['ETIMEDOUT','TimeoutError','AbortError','UND_ERR_CONNECT_TIMEOUT'].includes(value))return 'timeout';
 if(value==='ENOTFOUND'||value==='EAI_AGAIN')return 'dns';
 return 'other';
};
const opsflowDescribe=error=>{
 const name=opsflowNames.has(error?.name)?error.name:'other';
 if(typeof error?.cause?.code==='string')return {name,code_source:'cause_code',code:opsflowCode(error.cause.code)};
 if(typeof error?.code==='string')return {name,code_source:'error_code',code:opsflowCode(error.code)};
 if(typeof error?.name==='string')return {name,code_source:'error_name',code:opsflowCode(error.name)};
 return {name,code_source:'none',code:'other'};
};
const opsflowFailure=error=>{
 if(Number.isInteger(error?.opsflowStatus)&&error.opsflowStatus>=100&&error.opsflowStatus<=599)return {kind:'http_status',status:error.opsflowStatus,error:opsflowCleanError};
 const described=opsflowDescribe(error);
 if(error?.opsflowFetchUnavailable===true)return {kind:'fetch_unavailable',status:null,error:described};
 if(error?.opsflowResponseInvalid===true)return {kind:'response_invalid',status:null,error:described};
 if(['cause_code','error_code'].includes(described.code_source))return {kind:'transport',status:null,error:described};
 return {kind:'unknown',status:null,error:opsflowUnknownError};
};
const opsflowFetch=(...args)=>{
 if(typeof fetch!=='function'){const error=new ReferenceError();error.opsflowFetchUnavailable=true;throw error;}
 return fetch(...args);
};
const opsflowJson=async response=>{
 try{return await response.json();}catch(error){error.opsflowResponseInvalid=true;throw error;}
};
const opsflowRequireOk=response=>{
 if(!response.ok){const error=new Error();error.opsflowStatus=response.status;throw error;}
};
const opsflowExit=error=>{
 process.stdout.write(JSON.stringify({failure:opsflowFailure(error)}));
 process.exitCode=1;
};
""".strip()


def body_fetch_failure_facts(result, consumer: str) -> dict[str, object]:
    if consumer not in BODY_FETCH_CONSUMERS:
        raise ValueError("body-fetch consumer rejected")
    invalid = {
        "consumer": consumer,
        "kind": "invalid_output",
        "status": None,
        "error": {"name": "other", "code_source": "none", "code": "other"},
    }
    if (
        type(result.returncode) is not int
        or result.returncode == 0
        or not isinstance(result.stdout, str)
        or not isinstance(result.stderr, str)
        or result.stderr
        or not 0 < len(result.stdout) <= 4096
    ):
        return invalid
    try:
        value = _strict_json(result.stdout.encode("utf-8"))
        if set(value) != {"failure"}:
            raise ValueError("body-fetch output shape rejected")
        failure = value["failure"]
        if not isinstance(failure, dict) or set(failure) != {"kind", "status", "error"}:
            raise ValueError("body-fetch failure shape rejected")
        kind, status, error = failure["kind"], failure["status"], failure["error"]
        if (
            kind not in BODY_FETCH_KINDS
            or not isinstance(error, dict)
            or set(error) != {"name", "code_source", "code"}
        ):
            raise ValueError("body-fetch failure values rejected")
        name, source, code = error["name"], error["code_source"], error["code"]
        if (
            name not in BODY_ERROR_NAMES
            or source not in BODY_CODE_SOURCES
            or code not in BODY_ERROR_CODES
            or (name == "none") != (source == "none" and code == "none")
        ):
            raise ValueError("body-fetch error values rejected")
        if kind == "http_status":
            if (
                type(status) is not int
                or not 100 <= status <= 599
                or error != {"name": "none", "code_source": "none", "code": "none"}
            ):
                raise ValueError("body-fetch HTTP status rejected")
        elif status is not None or code == "none":
            raise ValueError("body-fetch non-HTTP relation rejected")
        if kind == "fetch_unavailable" and error != {
            "name": "ReferenceError",
            "code_source": "error_name",
            "code": "other",
        }:
            raise ValueError("body-fetch availability fact rejected")
        if kind == "transport" and source not in {"cause_code", "error_code"}:
            raise ValueError("body-fetch transport relation rejected")
        if kind == "response_invalid" and (
            source != "error_name"
            or (name, code)
            not in {
                ("SyntaxError", "other"),
                ("TypeError", "other"),
                ("AbortError", "timeout"),
            }
        ):
            raise ValueError("body-fetch JSON fact rejected")
        if kind == "unknown" and (name, source, code) != ("other", "none", "other"):
            raise ValueError("body-fetch unknown fact rejected")
    except (UnicodeError, json.JSONDecodeError, TypeError, ValueError):
        return invalid
    return {"consumer": consumer, "kind": kind, "status": status, "error": dict(error)}


@dataclass(frozen=True)
class PrivateFile:
    path: Path
    device: int
    inode: int
    uid: int
    gid: int
    mode: int

    def with_uid(self, uid: int) -> PrivateFile:
        return PrivateFile(self.path, self.device, self.inode, uid, self.gid, self.mode)


def host_identity() -> tuple[int, int]:
    uid, gid = os.geteuid(), os.getegid()
    if type(uid) is not int or type(gid) is not int or uid < 0 or gid < 0:
        raise ValueError("host identity rejected")
    return uid, gid


def finalize_host_boundary(
    cleanup_host, lock_fd: int
) -> tuple[int, list[str], BaseException | None]:
    failures = []
    cancellation: BaseException | None = None
    if cleanup_host is not None:
        try:
            cleanup_host()
        except BaseException as error:
            failures.append("host")
            if not isinstance(error, Exception):
                cancellation = error
    if lock_fd >= 0:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        except BaseException as error:
            failures.append("lock")
            if not isinstance(error, Exception) and cancellation is None:
                cancellation = error
        try:
            os.close(lock_fd)
            lock_fd = -1
        except BaseException as error:
            failures.append("lock")
            if not isinstance(error, Exception) and cancellation is None:
                cancellation = error
    return lock_fd, failures, cancellation


def _read_file(
    path: Path, maximum: int, expected: PrivateFile | None = None
) -> tuple[dict[str, object], bytes]:
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        before = os.fstat(descriptor)
        content = bytearray()
        while len(content) <= maximum:
            chunk = os.read(descriptor, min(65536, maximum + 1 - len(content)))
            if not chunk:
                break
            content.extend(chunk)
        after = os.fstat(descriptor)
        named = path.stat(follow_symlinks=False)
        stable_before = (
            before.st_dev,
            before.st_ino,
            before.st_uid,
            before.st_gid,
            before.st_mode,
            before.st_nlink,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        stable_after = (
            after.st_dev,
            after.st_ino,
            after.st_uid,
            after.st_gid,
            after.st_mode,
            after.st_nlink,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        )
        named_identity = (
            named.st_dev,
            named.st_ino,
            named.st_uid,
            named.st_gid,
            named.st_mode,
            named.st_nlink,
            named.st_size,
            named.st_mtime_ns,
            named.st_ctime_ns,
        )
        expected_identity = (
            None
            if expected is None
            else (
                expected.device,
                expected.inode,
                expected.uid,
                expected.gid,
                expected.mode,
            )
        )
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_size != len(content)
            or before.st_size > maximum
            or stable_before != stable_after
            or stable_after != named_identity
            or (
                expected is not None
                and (
                    before.st_dev,
                    before.st_ino,
                    before.st_uid,
                    before.st_gid,
                    stat.S_IMODE(before.st_mode),
                )
                != expected_identity
            )
        ):
            raise ValueError("retained evidence file metadata rejected")
        summary = {
            "name": path.name,
            "device": after.st_dev,
            "inode": after.st_ino,
            "uid": after.st_uid,
            "gid": after.st_gid,
            "mode": stat.S_IMODE(after.st_mode),
            "nlink": after.st_nlink,
            "bytes": after.st_size,
            "mtime_ns": after.st_mtime_ns,
            "ctime_ns": after.st_ctime_ns,
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        return summary, bytes(content)
    finally:
        os.close(descriptor)


def _directory_summary(directory: Path, name: str) -> dict[str, object]:
    descriptor = os.open(
        directory, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY
    )
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISDIR(metadata.st_mode)
            or metadata.st_uid != os.geteuid()
            or stat.S_IMODE(metadata.st_mode) != 0o700
        ):
            raise ValueError("retained evidence directory metadata rejected")
        return {
            "name": name,
            "device": metadata.st_dev,
            "inode": metadata.st_ino,
            "uid": metadata.st_uid,
            "gid": metadata.st_gid,
            "mode": stat.S_IMODE(metadata.st_mode),
            "nlink": metadata.st_nlink,
        }
    finally:
        os.close(descriptor)


def _config_summary(directory: Path) -> dict[str, object]:
    config = directory / "docker-config"
    summary = _directory_summary(config, "docker-config")
    descriptor = os.open(
        config, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY
    )
    try:
        if os.listdir(descriptor):
            raise ValueError("retained Docker config directory is not empty")
    finally:
        os.close(descriptor)
    return summary


def _bounded_text(
    value: str, source_bytes: int | None = None
) -> tuple[str, dict[str, object]]:
    if not isinstance(value, str):
        raise TypeError("failure output must be text")
    encoded = value.encode("utf-8")
    if source_bytes is None:
        source_bytes = len(encoded)
    if type(source_bytes) is not int or source_bytes < 0:
        raise ValueError("failure output source size rejected")
    truncated = len(encoded) > FAILURE_OUTPUT_LIMIT
    if truncated:
        marker = "\n[... bounded head/tail ...]\n"
        half = (FAILURE_OUTPUT_LIMIT - len(marker.encode("ascii"))) // 2
        text = (
            encoded[:half].decode("utf-8", "ignore")
            + marker
            + encoded[-half:].decode("utf-8", "ignore")
        )
        retention = "head_tail"
    else:
        text = encoded.decode("utf-8", "ignore")
        retention = "full"
    retained = text.encode("utf-8")
    return text, {
        "bytes": len(retained),
        "source_bytes": source_bytes,
        "retention": retention,
        "truncated": truncated,
        "sha256": hashlib.sha256(retained).hexdigest(),
    }


def _strict_json(content: bytes) -> dict[str, object]:
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError("duplicate failure evidence metadata key")
            result[key] = value
        return result

    value = json.loads(content, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError("failure evidence metadata is not an object")
    return value


def _file_map(items: object) -> dict[str, dict[str, object]]:
    if not isinstance(items, list):
        raise ValueError("failure evidence file list rejected")
    result = {}
    for item in items:
        if not isinstance(item, dict) or set(item) != FILE_KEYS:
            raise ValueError("failure evidence file identity rejected")
        name = item.get("name")
        if not isinstance(name, str) or name in result:
            raise ValueError("failure evidence file name rejected")
        result[name] = item
    return result


def retain_failure_output(
    directory: Path,
    files: dict[Path, PrivateFile],
    receipt: dict[str, object],
    result,
) -> None:
    receipt["failure_evidence"] = {"status": "PENDING"}
    existing = {
        path.name: (path, item) for path, item in files.items() if path.exists()
    }
    if set(existing) != FIXTURE_NAMES:
        raise ValueError("retained fixture file set rejected")
    secrets = tuple(
        _read_file(path, RETAINED_FILE_LIMIT, item)[1].decode("utf-8").strip()
        for name, (path, item) in sorted(existing.items())
        if name.endswith(".secret")
    )
    streams = {}
    for stream, value in (("stdout", result.stdout), ("stderr", result.stderr)):
        sanitized = redact_text(value, secrets)
        text, summary = _bounded_text(sanitized, len(value.encode("utf-8")))
        path = write_exclusive(directory, f"failure-{stream}.txt", text, 0o600)
        metadata = path.stat(follow_symlinks=False)
        files[path] = PrivateFile(
            path,
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_uid,
            metadata.st_gid,
            0o600,
        )
        streams[stream] = summary
    retained = {
        path.name: (path, item) for path, item in files.items() if path.exists()
    }
    if set(retained) != RETAINED_NAMES:
        raise ValueError("retained fixture file set rejected")
    retained_files = [
        _read_file(path, RETAINED_FILE_LIMIT, item)[0]
        for _, (path, item) in sorted(retained.items())
    ]
    metadata = {
        "schema_version": 1,
        "role": "main",
        "command_id": "docker_logs_tail_200",
        "exit_code": (
            result.returncode
            if type(result.returncode) is int and -255 <= result.returncode <= 255
            else None
        ),
        "streams": streams,
        "directory": _directory_summary(directory, directory.name),
        "docker_config": _config_summary(directory),
        "retained_files": retained_files,
    }
    path = write_exclusive(
        directory,
        METADATA_NAME,
        json.dumps(metadata, sort_keys=True) + "\n",
        0o600,
    )
    item = path.stat(follow_symlinks=False)
    files[path] = PrivateFile(
        path, item.st_dev, item.st_ino, item.st_uid, item.st_gid, 0o600
    )
    receipt["failure_evidence"] = {
        **metadata,
        "metadata_file": _read_file(path, FAILURE_OUTPUT_LIMIT, files[path])[0],
    }


def verify_failure_evidence(
    directory: Path, evidence: dict[str, object]
) -> tuple[Path, ...]:
    keys = {
        "schema_version",
        "role",
        "command_id",
        "exit_code",
        "streams",
        "directory",
        "docker_config",
        "retained_files",
        "metadata_file",
    }
    if (
        not isinstance(evidence, dict)
        or set(evidence) != keys
        or evidence.get("schema_version") != 1
        or evidence.get("role") != "main"
        or evidence.get("command_id") != "docker_logs_tail_200"
        or not isinstance(evidence.get("directory"), dict)
        or set(evidence["directory"]) != DIRECTORY_KEYS
        or evidence["directory"] != _directory_summary(directory, directory.name)
        or not isinstance(evidence.get("docker_config"), dict)
        or set(evidence["docker_config"]) != DIRECTORY_KEYS
        or evidence["docker_config"] != _config_summary(directory)
    ):
        raise ValueError("failure evidence receipt rejected")
    expected = _file_map(evidence["retained_files"])
    if set(expected) != RETAINED_NAMES:
        raise ValueError("retained fixture file set rejected")
    metadata = evidence["metadata_file"]
    if not isinstance(metadata, dict) or set(metadata) != FILE_KEYS:
        raise ValueError("failure evidence metadata identity rejected")
    if metadata.get("name") != METADATA_NAME:
        raise ValueError("failure evidence metadata name rejected")
    observed = {item.name for item in directory.iterdir()}
    if observed != RETAINED_NAMES | {METADATA_NAME, "docker-config"}:
        raise ValueError("retained attempt directory file set rejected")
    paths = tuple(directory / name for name in sorted(expected))
    for path in paths:
        summary, _ = _read_file(path, RETAINED_FILE_LIMIT)
        if summary != expected[path.name]:
            raise ValueError("failure evidence identity changed")
    metadata_summary, content = _read_file(
        directory / METADATA_NAME, FAILURE_OUTPUT_LIMIT
    )
    if metadata_summary != metadata:
        raise ValueError("failure evidence metadata identity changed")
    if _strict_json(content) != {
        key: value for key, value in evidence.items() if key != "metadata_file"
    }:
        raise ValueError("failure evidence metadata changed")
    return (*paths, directory / METADATA_NAME)


def sanitized_failure_summary(directory: Path, evidence: dict[str, object]) -> str:
    verify_failure_evidence(directory, evidence)
    expected = _file_map(evidence["retained_files"])

    def bound_content(name: str, maximum: int) -> bytes:
        summary, content = _read_file(directory / name, maximum)
        if summary != expected[name]:
            raise ValueError("failure evidence changed before diagnosis")
        return content

    secrets = tuple(
        bound_content(name, RETAINED_FILE_LIMIT).decode("utf-8").strip()
        for name in sorted(FIXTURE_NAMES)
        if name.endswith(".secret")
    )
    lines, fallback = [], []
    for name in sorted(STREAM_NAMES):
        text = bound_content(name, FAILURE_OUTPUT_LIMIT).decode("utf-8", "replace")
        text = redact_text(text, secrets)
        nonempty = [line.strip()[:500] for line in text.splitlines() if line.strip()]
        fallback.extend(nonempty[-5:])
        candidates = [
            line
            for line in nonempty
            if any(
                marker in line.casefold()
                for marker in ("error", "exception", "fatal", "failed", " at ")
            )
        ]
        lines.extend(candidates[-10:])
    selected = lines[-20:] if lines else fallback[-10:]
    summary = "\n".join(selected) + ("\n" if selected else "")
    if redact_text(summary, secrets) != summary:
        raise ValueError("failure evidence redaction incomplete")
    return summary


def _unlink_bound(
    directory_fd: int,
    name: str,
    expected: dict[str, object],
    maximum: int,
) -> None:
    descriptor = os.open(
        name,
        os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
        dir_fd=directory_fd,
    )
    try:
        before = os.fstat(descriptor)
        content = bytearray()
        while len(content) <= maximum:
            chunk = os.read(descriptor, min(65536, maximum + 1 - len(content)))
            if not chunk:
                break
            content.extend(chunk)
        after = os.fstat(descriptor)
        named = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)

        def stable(metadata):
            return (
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_uid,
                metadata.st_gid,
                metadata.st_mode,
                metadata.st_nlink,
                metadata.st_size,
                metadata.st_mtime_ns,
                metadata.st_ctime_ns,
            )

        summary = {
            "name": name,
            "device": after.st_dev,
            "inode": after.st_ino,
            "uid": after.st_uid,
            "gid": after.st_gid,
            "mode": stat.S_IMODE(after.st_mode),
            "nlink": after.st_nlink,
            "bytes": after.st_size,
            "mtime_ns": after.st_mtime_ns,
            "ctime_ns": after.st_ctime_ns,
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_size != len(content)
            or before.st_size > maximum
            or stable(before) != stable(after)
            or stable(after) != stable(named)
            or summary != expected
        ):
            raise ValueError("failure evidence changed before unlink")
        immediate = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if stable(immediate) != stable(after):
            raise ValueError("failure evidence changed before unlink")
        os.unlink(name, dir_fd=directory_fd)
        try:
            os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise ValueError("failure evidence remained after unlink")
    finally:
        os.close(descriptor)


def reconcile_failure_evidence(directory: Path, evidence: dict[str, object]) -> None:
    paths = verify_failure_evidence(directory, evidence)
    expected = _file_map(evidence["retained_files"])
    expected[METADATA_NAME] = evidence["metadata_file"]
    directory_fd = os.open(
        directory, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY
    )
    try:
        bound_directory = os.fstat(directory_fd)
        prior = evidence["directory"]
        if any(
            value != prior[key]
            for key, value in {
                "device": bound_directory.st_dev,
                "inode": bound_directory.st_ino,
                "uid": bound_directory.st_uid,
                "gid": bound_directory.st_gid,
                "mode": stat.S_IMODE(bound_directory.st_mode),
                "nlink": bound_directory.st_nlink,
            }.items()
        ):
            raise ValueError("attempt directory changed before reconciliation")
        for path in paths:
            _unlink_bound(
                directory_fd,
                path.name,
                expected[path.name],
                RETAINED_FILE_LIMIT,
            )
        config_fd = os.open(
            "docker-config",
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
            dir_fd=directory_fd,
        )
        try:
            config = os.fstat(config_fd)
            expected_config = evidence["docker_config"]
            if (
                os.listdir(config_fd)
                or {
                    "name": "docker-config",
                    "device": config.st_dev,
                    "inode": config.st_ino,
                    "uid": config.st_uid,
                    "gid": config.st_gid,
                    "mode": stat.S_IMODE(config.st_mode),
                    "nlink": config.st_nlink,
                }
                != expected_config
            ):
                raise ValueError("Docker config changed before reconciliation")
            named_config = os.stat(
                "docker-config", dir_fd=directory_fd, follow_symlinks=False
            )
            if (named_config.st_dev, named_config.st_ino) != (
                config.st_dev,
                config.st_ino,
            ):
                raise ValueError("Docker config changed before removal")
            os.rmdir("docker-config", dir_fd=directory_fd)
        finally:
            os.close(config_fd)
        current = os.fstat(directory_fd)
        if any(
            value != prior[key]
            for key, value in {
                "device": current.st_dev,
                "inode": current.st_ino,
                "uid": current.st_uid,
                "gid": current.st_gid,
                "mode": stat.S_IMODE(current.st_mode),
            }.items()
        ):
            raise ValueError("attempt directory identity changed before removal")
        if os.listdir(directory_fd):
            raise ValueError("attempt directory is not empty after reconciliation")
        named_directory = directory.stat(follow_symlinks=False)
        if (named_directory.st_dev, named_directory.st_ino) != (
            current.st_dev,
            current.st_ino,
        ):
            raise ValueError("attempt directory changed before removal")
    finally:
        os.close(directory_fd)
    directory.rmdir()
