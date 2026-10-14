#!/usr/bin/env python3
"""Immutable small-input custody and bounded process execution for P01 restore."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import selectors
import stat
import subprocess
import time
from collections import namedtuple
from pathlib import Path

HEX64 = re.compile(r"[a-f0-9]{64}")
SAFE_PART = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


class CustodyError(Exception):
    """An immutable-input custody condition failed."""


class ProcessError(Exception):
    """A process result cannot be accepted."""


def _signature(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_mode,
        info.st_uid,
        info.st_gid,
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _write_all(descriptor, raw):
    offset = 0
    while offset < len(raw):
        count = os.write(descriptor, raw[offset:])
        if count <= 0:
            raise CustodyError()
        offset += count


def strict_json(raw, maximum=65536):
    if not isinstance(raw, bytes) or not 1 <= len(raw) <= maximum:
        raise CustodyError()

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise CustodyError()
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique)
    except (UnicodeError, ValueError, TypeError, RecursionError):
        raise CustodyError() from None
    pending, count = [(value, 0)], 0
    while pending:
        node, depth = pending.pop()
        count += 1
        if count > 2048 or depth > 16:
            raise CustodyError()
        if isinstance(node, dict):
            pending.extend((item, depth + 1) for item in node.values())
        elif isinstance(node, list):
            pending.extend((item, depth + 1) for item in node)
    return value


class HeldBytes:
    def __init__(self, path, descriptor, info, digest, raw):
        self.path, self.fd, self.info, self.digest, self.raw = (
            Path(path),
            descriptor,
            info,
            digest,
            raw,
        )
        self.signature = _signature(info)

    @classmethod
    def open(cls, path, digest, *, maximum=65536, private=False):
        path = Path(path)
        if (
            not path.is_absolute()
            or not HEX64.fullmatch(digest)
            or not 1 <= maximum <= 1024 * 1024
        ):
            raise CustodyError()
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            before = os.fstat(descriptor)
            modes = {0o600} if private else {0o400, 0o440, 0o500, 0o600, 0o640, 0o644}
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_nlink != 1
                or before.st_uid not in {0, os.getuid()}
                or stat.S_IMODE(before.st_mode) not in modes
                or not 1 <= before.st_size <= maximum
            ):
                raise CustodyError()
            raw = os.pread(descriptor, before.st_size, 0)
            after = os.fstat(descriptor)
            current = os.lstat(path)
            if (
                len(raw) != before.st_size
                or _signature(before) != _signature(after)
                or _signature(after) != _signature(current)
                or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), digest)
            ):
                raise CustodyError()
            return cls(path, descriptor, after, digest, raw)
        except BaseException:
            os.close(descriptor)
            raise

    def json(self, maximum=65536):
        return strict_json(self.raw, maximum)

    def revalidate(self):
        try:
            info = os.fstat(self.fd)
            current = os.lstat(self.path)
            raw = os.pread(self.fd, info.st_size, 0)
        except (OSError, TypeError):
            raise CustodyError() from None
        if (
            _signature(info) != self.signature
            or _signature(current) != self.signature
            or len(raw) != self.info.st_size
            or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), self.digest)
        ):
            raise CustodyError()

    def materialize(self, root, relative, mode):
        root, relative = Path(root), Path(relative)
        if (
            relative.is_absolute()
            or not relative.parts
            or any(not SAFE_PART.fullmatch(part) for part in relative.parts)
            or mode not in {0o400, 0o500}
        ):
            raise CustodyError()
        parent = root
        for part in relative.parts[:-1]:
            parent /= part
            try:
                parent.mkdir(mode=0o700)
            except FileExistsError:
                info = parent.lstat()
                if (
                    not stat.S_ISDIR(info.st_mode)
                    or stat.S_IMODE(info.st_mode) != 0o700
                    or info.st_uid != os.getuid()
                ):
                    raise CustodyError() from None
        target = root / relative
        descriptor = os.open(
            target,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            mode,
        )
        try:
            _write_all(descriptor, self.raw)
            os.fchmod(descriptor, mode)
            os.fsync(descriptor)
            info = os.fstat(descriptor)
            if info.st_nlink != 1 or info.st_size != len(self.raw):
                raise CustodyError()
        finally:
            os.close(descriptor)
        return target

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


Result = namedtuple("Result", "returncode stdout stderr")


class BoundedRunner:
    def __init__(self, deadline, *, output_limit=65536, input_limit=8192, probe=None):
        if output_limit < 1 or input_limit < 1:
            raise ProcessError()
        self.deadline, self.output_limit, self.input_limit, self.probe = (
            deadline,
            output_limit,
            input_limit,
            probe,
        )
        self.last_pid = None

    def _stop(self, process):
        if process.poll() is None:
            process.kill()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    def run(self, argv, *, input=None, allow_failure=False):
        if (
            not isinstance(argv, (list, tuple))
            or not argv
            or any(not isinstance(item, str) or not item for item in argv)
            or (
                input is not None
                and (not isinstance(input, bytes) or len(input) > self.input_limit)
            )
        ):
            raise ProcessError()
        if time.monotonic() >= self.deadline:
            raise ProcessError()
        process = None
        selector = selectors.DefaultSelector()
        chunks = {"stdout": bytearray(), "stderr": bytearray()}
        try:
            process = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={"PATH": "/usr/bin:/bin"},
                close_fds=True,
            )
            self.last_pid = process.pid
            if input is not None:
                process.stdin.write(input)
                process.stdin.close()
            for name, stream in (
                ("stdout", process.stdout),
                ("stderr", process.stderr),
            ):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            while selector.get_map() or process.poll() is None:
                if self.probe is not None:
                    self.probe()
                remaining = self.deadline - time.monotonic()
                if remaining <= 0:
                    raise ProcessError()
                for key, _mask in selector.select(min(0.05, remaining)):
                    raw = os.read(key.fileobj.fileno(), 65536)
                    if not raw:
                        selector.unregister(key.fileobj)
                    else:
                        if len(chunks[key.data]) + len(raw) > self.output_limit:
                            raise ProcessError()
                        chunks[key.data].extend(raw)
            returncode = process.wait(timeout=1)
            result = Result(
                returncode, bytes(chunks["stdout"]), bytes(chunks["stderr"])
            )
            if returncode and not allow_failure:
                raise ProcessError()
            return result
        except BaseException:
            if process is not None:
                self._stop(process)
            raise ProcessError() from None
        finally:
            selector.close()
            if process is not None:
                for stream in (process.stdout, process.stderr):
                    if stream is not None:
                        stream.close()


def cleanup_exact(containers, volumes, networks, *, seconds=60):
    failed = False
    commands = [
        ["docker", "rm", "--force", item] for item in reversed(tuple(containers))
    ]
    commands += [["docker", "volume", "rm", item] for item in reversed(tuple(volumes))]
    commands += [
        ["docker", "network", "rm", item] for item in reversed(tuple(networks))
    ]
    slice_seconds = seconds / max(1, len(commands))
    for command in commands:
        try:
            runner = BoundedRunner(time.monotonic() + slice_seconds, output_limit=8192)
            failed |= runner.run(command, allow_failure=True).returncode != 0
        except ProcessError:
            failed = True
    return failed


class CommandRunner:
    def __init__(self, deadline, failure=ProcessError):
        self.failure = failure
        self.engine = BoundedRunner(deadline)

    def run(self, argv, *, input=None, allow_failure=False):
        try:
            return self.engine.run(argv, input=input, allow_failure=allow_failure)
        except ProcessError:
            raise self.failure() from None


class ContainerRuntime:
    def __init__(self, runner, owner, failure=ProcessError):
        self.runner, self.owner, self.failure = runner, owner, failure
        self.containers, self.networks, self.volumes = [], [], []
        self.watcher = None

    def remember(self, kind, result):
        try:
            value = result.stdout.strip().decode("ascii", "strict")
        except (AttributeError, UnicodeError):
            raise self.failure() from None
        if kind not in {"container", "network", "volume"} or not re.fullmatch(
            r"[a-f0-9]{64}", value
        ):
            raise self.failure()
        getattr(self, kind + "s").append(value)
        return value

    def docker(self, *args, input=None, allow_failure=False):
        return self.runner.run(
            ["docker", *args], input=input, allow_failure=allow_failure
        )

    def exec(self, identity, *args, input=None, allow_failure=False, user=None):
        prefix = ["exec", "-i"] + ([] if user is None else ["--user", user])
        return self.docker(
            *prefix, identity, *args, input=input, allow_failure=allow_failure
        )

    def login(self, identity, token):
        self.exec(identity, "bao", "login", "-no-print", input=(token + "\n").encode())
        check = self.exec(
            identity, "/usr/bin/stat", "-c", "%u %g %a %h %F", "/openbao/private/token"
        )
        if check.stdout.strip() != b"100 1000 600 1 regular file":
            raise self.failure()

    def restore(self, identity):
        self.exec(
            identity,
            "bao",
            "operator",
            "raft",
            "snapshot",
            "restore",
            "-force",
            "/restore/raft.snap",
            user="0:0",
        )

    def watcher_probe(self):
        if self.watcher is None:
            return
        try:
            result = BoundedRunner(time.monotonic() + 5, output_limit=8192).run(
                [
                    "docker",
                    "inspect",
                    "--format",
                    "{{.State.Running}} {{.State.OOMKilled}}",
                    self.watcher,
                ]
            )
        except ProcessError:
            raise self.failure() from None
        if result.stdout.strip() != b"true false":
            raise self.failure()

    def cleanup(self):
        self.runner.engine.probe = None
        failed = cleanup_exact(self.containers, self.volumes, self.networks)
        self.containers, self.volumes, self.networks = [], [], []
        if failed:
            raise self.failure()
