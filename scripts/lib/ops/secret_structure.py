"""Value-free, explicit read-only comparison of fixed secret metadata inputs."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from contextlib import ExitStack
from pathlib import Path

MAX_BYTES = 2 * 1024 * 1024
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC
ASSIGNMENT = re.compile(
    r"^([ \t]*(?:export[ \t]+)?([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*)(.*)$"
)
IDENTIFIER = re.compile(r"[A-Z][A-Z0-9_-]*-[0-9]+\Z")
SEPARATOR = re.compile(r":?-{3,}:?\Z")


class UnsafeInput(Exception):
    """A closed error without private content."""


class ClosedParser(argparse.ArgumentParser):
    """Never reflect untrusted arguments in diagnostics."""

    def error(self, message):
        self.exit(2, '{"result": "BLOCKED"}\n')


def _identity(info):
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


def _directory_identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid)


class HeldInputs:
    """Hold every ancestor and input until the final post-read identity check."""

    def __init__(self, root):
        self.stack = ExitStack()
        self.checks = []
        root = Path(root)
        if not root.is_absolute() or any(part in (".", "..") for part in root.parts):
            raise UnsafeInput()
        try:
            self.root = self._open_absolute(root)
            info = os.fstat(self.root)
            if info.st_uid != os.geteuid() or info.st_mode & stat.S_IWOTH:
                raise UnsafeInput()
        except BaseException:
            self.stack.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.stack.__exit__(*args)

    def _open_absolute(self, path):
        fd = os.open("/", DIRECTORY_FLAGS)
        self.stack.callback(os.close, fd)
        for component in path.parts[1:]:
            fd = self._child_directory(fd, component, owned=False)
        return fd

    def _child_directory(self, parent, name, *, owned):
        fd = os.open(name, DIRECTORY_FLAGS, dir_fd=parent)
        self.stack.callback(os.close, fd)
        info = os.fstat(fd)
        if owned and (info.st_uid != os.geteuid() or info.st_mode & stat.S_IWOTH):
            raise UnsafeInput()
        expected = _directory_identity(info)
        self.checks.append(
            lambda p=parent, n=name, f=fd, e=expected: _check_directory(p, n, f, e)
        )
        return fd

    def _parent(self, relative, *, optional):
        parent = self.root
        parts = relative.split("/")
        for name in parts[:-1]:
            try:
                parent = self._child_directory(parent, name, owned=True)
            except FileNotFoundError:
                if not optional:
                    raise
                self.checks.append(lambda p=parent, n=name: _check_absent(p, n))
                return None, parts[-1]
        return parent, parts[-1]

    def open(self, relative, *, private, smtp=False, optional=False, read=True):
        parent, name = self._parent(relative, optional=optional)
        if parent is None:
            return None
        try:
            fd = os.open(name, FILE_FLAGS, dir_fd=parent)
        except FileNotFoundError:
            if not optional:
                raise
            self.checks.append(lambda p=parent, n=name: _check_absent(p, n))
            return None
        self.stack.callback(os.close, fd)
        info = os.fstat(fd)
        mode = stat.S_IMODE(info.st_mode)
        valid_mode = mode in ((0o600, 0o640) if smtp else (0o600,))
        valid_group = mode != 0o640 or info.st_gid in {os.getegid(), *os.getgroups()}
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or info.st_uid != os.geteuid()
            or info.st_size > MAX_BYTES
            or (private and (not valid_mode or not valid_group))
            or (not private and mode & 0o022)
        ):
            raise UnsafeInput()
        expected = _identity(info)
        self.checks.append(
            lambda p=parent, n=name, f=fd, e=expected: _check_file(p, n, f, e)
        )
        if not read:
            return b""
        chunks = []
        total = 0
        while total <= MAX_BYTES:
            part = os.read(fd, min(65536, MAX_BYTES + 1 - total))
            if not part:
                break
            chunks.append(part)
            total += len(part)
        if total > MAX_BYTES:
            raise UnsafeInput()
        _check_file(parent, name, fd, expected)
        return b"".join(chunks)

    def verify(self):
        for check in self.checks:
            check()


def _check_directory(parent, name, fd, expected):
    if (
        _directory_identity(os.fstat(fd)) != expected
        or _directory_identity(os.stat(name, dir_fd=parent, follow_symlinks=False))
        != expected
    ):
        raise UnsafeInput()


def _check_file(parent, name, fd, expected):
    if (
        _identity(os.fstat(fd)) != expected
        or _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)) != expected
    ):
        raise UnsafeInput()


def _check_absent(parent, name):
    try:
        os.stat(name, dir_fd=parent, follow_symlinks=False)
    except FileNotFoundError:
        return
    raise UnsafeInput()


def _decode(data):
    text = data.decode("utf-8")
    if "\r" in text.replace("\r\n", "") or any(
        character in text for character in "\x00\v\f\x85\u2028\u2029"
    ):
        raise UnsafeInput()
    return text


def _comment(value):
    """Keep only inline-comment structure; reject ambiguous quoting."""
    if value.startswith(('"', "'")):
        quote = value[0]
        escaped = False
        for index, char in enumerate(value[1:], 1):
            if quote == '"' and char == "\\" and not escaped:
                escaped = True
                continue
            if char == quote and not escaped:
                tail = value[index + 1 :]
                if tail and not tail.isspace() and not re.fullmatch(r"[ \t]+#.*", tail):
                    raise UnsafeInput()
                return tail if "#" in tail else ""
            escaped = False
        raise UnsafeInput()
    if (len(value) - len(value.rstrip("\\"))) % 2:
        raise UnsafeInput()
    for index, char in enumerate(value):
        if char == "#" and index and value[index - 1] in " \t":
            start = index - 1
            while start and value[start - 1] in " \t":
                start -= 1
            return value[start:]
    return ""


def env_structure(data):
    text = _decode(data)
    seen = set()
    result = []
    for line in text.splitlines(keepends=True):
        ending = (
            "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        )
        body = line[: -len(ending)] if ending else line
        if not body.strip() or body.lstrip().startswith("#"):
            result.append(line)
            continue
        match = ASSIGNMENT.fullmatch(body)
        if match is None or match.group(2) in seen:
            raise UnsafeInput()
        seen.add(match.group(2))
        value = match.group(3)
        prefix = match.group(1)
        if value.startswith("#") and prefix[-1].isspace():
            start = len(prefix.rstrip(" \t"))
            comment = prefix[start:] + value
            prefix = prefix[:start]
        else:
            comment = _comment(value)
        result.append(prefix + "<VALUE>" + comment + ending)
    if not seen:
        raise UnsafeInput()
    return "".join(result)


def _cell(value):
    return value.strip().strip("*`").strip()


def registry_structure(data):
    text = _decode(data)
    seen = set()
    aliases = set()
    result = []
    for line in text.splitlines(keepends=True):
        if not line.lstrip().startswith("|"):
            result.append(line)
            continue
        cells = line.split("|")
        if len(cells) == 4:
            alias = (_cell(cells[1]), _cell(cells[2]))
            # Header, separator, or a retired ID mapped to its canonical ID.
            if alias not in {
                ("Retired ID", "Canonical ID"),
                ("---", "---"),
            } and not all(IDENTIFIER.fullmatch(part) for part in alias):
                raise UnsafeInput()
            if alias in aliases:
                raise UnsafeInput()
            aliases.add(alias)
        elif len(cells) == 10:
            identifier = _cell(cells[1])
            if identifier != "ID" and not SEPARATOR.fullmatch(identifier):
                if not IDENTIFIER.fullmatch(identifier) or identifier in seen:
                    raise UnsafeInput()
                seen.add(identifier)
                cells[4] = "<VALUE>"
                line = "|".join(cells)
        else:
            raise UnsafeInput()
        result.append(line)
    if not seen:
        raise UnsafeInput()
    return "".join(result)


def _public_kind(line, kind):
    if kind == "env":
        if line.lstrip().startswith("#"):
            return "PUBLIC_COMMENT"
        if ASSIGNMENT.fullmatch(line.rstrip("\r\n")):
            return "PUBLIC_ASSIGNMENT"
        return "PUBLIC_LAYOUT"
    if line.lstrip().startswith("|"):
        cells = line.split("|")
        if len(cells) == 10 and IDENTIFIER.fullmatch(_cell(cells[1])):
            return "PUBLIC_ROW"
        return "PUBLIC_TABLE"
    return "PUBLIC_TEXT"


def _first_difference(public, private, kind):
    """Return one public reference; never return private text, positions or counts."""
    public_lines = public.splitlines(keepends=True)
    private_lines = private.splitlines(keepends=True)
    for index, public_line in enumerate(public_lines):
        if index >= len(private_lines):
            return {"reason": "PUBLIC_MISSING", "public_line": index + 1}
        if public_line != private_lines[index]:
            return {"reason": _public_kind(public_line, kind), "public_line": index + 1}
    if len(private_lines) > len(public_lines):
        return {"reason": "PRIVATE_EXTRA"}
    raise UnsafeInput()


def compare(root):
    with HeldInputs(root) as inputs:
        public_env = inputs.open(".env.example", private=False)
        private_env = inputs.open(".env", private=True)
        public_registry = inputs.open(
            "secrets/SENSITIVE_ENV_VARS.md.example", private=False
        )
        private_registry = inputs.open("secrets/SENSITIVE_ENV_VARS.md", private=True)
        env_public = env_structure(public_env)
        env_private = env_structure(private_env)
        registry_public = registry_structure(public_registry)
        registry_private = registry_structure(private_registry)
        env_equal = env_public == env_private
        registry_equal = registry_public == registry_private
        details = {}
        if not env_equal:
            details["env"] = _first_difference(env_public, env_private, "env")
        if not registry_equal:
            details["registry"] = _first_difference(
                registry_public, registry_private, "registry"
            )
        inputs.verify()
    if env_equal and registry_equal:
        return 0, {"result": "MATCH", "env": "MATCH", "registry": "MATCH"}
    return 1, {
        "result": "DRIFT",
        "env": "MATCH" if env_equal else "DRIFT",
        "registry": "MATCH" if registry_equal else "DRIFT",
        "details": details,
    }


def smtp_equality(root):
    with HeldInputs(root) as inputs:
        inputs.open(
            "secrets/communication/smtp/smtp_password.txt",
            private=True,
            smtp=True,
            read=False,
        )
        old = inputs.open(
            "secrets/communication/supabase/supabase_smtp_password.txt",
            private=True,
            smtp=True,
            optional=True,
        )
        canonical = (
            None
            if old is None
            else inputs.open(
                "secrets/communication/smtp/smtp_password.txt", private=True, smtp=True
            )
        )
        inputs.verify()
    if old is None:
        return 2, {"result": "OLD_ABSENT", "comparison_performed": False}
    if not old or not canonical:
        raise UnsafeInput()
    if old != canonical:
        return 1, {"result": "DIFFERENT", "comparison_performed": True}
    return 0, {"result": "EQUAL", "comparison_performed": True}


def main(argv=None):
    parser = ClosedParser(description=__doc__)
    parser.add_argument("--root", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "smtp-equality"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--read-private", required=True, action="store_true")
    args = parser.parse_args(argv)
    try:
        code, result = (
            compare(args.root) if args.command == "check" else smtp_equality(args.root)
        )
    except (UnsafeInput, OSError, UnicodeError, ValueError, OverflowError):
        code, result = 2, {"result": "BLOCKED"}
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
