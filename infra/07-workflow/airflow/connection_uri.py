"""Render supported Airflow _CMD URIs without credential argv or error output.

Airflow 3.3 supports _CMD for metadata, result_backend and broker_url:
https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html
SQLAlchemy requires password-component URL escaping; quote (not quote_plus)
also preserves literal plus for Kombu's Redis URL parser:
https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
"""

from __future__ import annotations

import os
import stat
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import quote

MAX_SECRET_BYTES = 4096
SECRETS_DIRECTORY = Path("/run/secrets")
ERROR = "Airflow connection: invalid input"
BROKERS = frozenset(
    {
        ("mng-valkey", "mng_valkey_password"),
        ("airflow-valkey", "airflow_valkey_password"),
    }
)


class ConnectionError(ValueError):
    """A value-free contract or protected-file failure."""


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_uid,
        value.st_gid,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _directory(path: Path) -> int:
    if not path.is_absolute() or ".." in path.parts:
        raise ConnectionError(ERROR)
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[1:]:
            next_descriptor = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
            details = os.fstat(descriptor)
            if details.st_mode & 0o022 and not (
                details.st_mode & stat.S_ISVTX and details.st_uid in {0, os.geteuid()}
            ):
                raise ConnectionError(ERROR)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _admit(details: os.stat_result) -> None:
    mode = stat.S_IMODE(details.st_mode)
    groups = {*os.getgroups(), os.getegid()}
    owner = details.st_uid in {0, os.geteuid()}
    shared = bool(mode & 0o040) and details.st_gid in groups
    if (
        not stat.S_ISREG(details.st_mode)
        or details.st_nlink != 1
        or mode not in {0o400, 0o600, 0o440, 0o640}
        or not (owner or shared)
        or not 0 < details.st_size <= MAX_SECRET_BYTES
    ):
        raise ConnectionError(ERROR)


def _read_secret(directory: Path, name: str, *, broker: bool) -> str:
    parent = _directory(directory)
    try:
        descriptor = os.open(
            name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent
        )
        try:
            initial = os.fstat(descriptor)
            _admit(initial)
            raw = b""
            while len(raw) <= MAX_SECRET_BYTES:
                chunk = os.read(descriptor, MAX_SECRET_BYTES + 1 - len(raw))
                if not chunk:
                    break
                raw += chunk
            if (
                len(raw) != initial.st_size
                or _identity(os.fstat(descriptor)) != _identity(initial)
                or _identity(os.stat(name, dir_fd=parent, follow_symlinks=False))
                != _identity(initial)
                or not os.path.samestat(
                    os.fstat(parent), os.stat(directory, follow_symlinks=False)
                )
            ):
                raise ConnectionError(ERROR)
        finally:
            os.close(descriptor)
    finally:
        os.close(parent)
    # One terminal LF is file framing. Other spaces and DB CR/TAB are data.
    value = (raw[:-1] if raw.endswith(b"\n") else raw).decode("utf-8")
    if not value or "\n" in value or "\0" in value:
        raise ConnectionError(ERROR)
    if broker and any(
        ord(character) < 32 or ord(character) == 127 for character in value
    ):
        raise ConnectionError(ERROR)
    return value


def _port(environment: Mapping[str, str], name: str, default: str) -> int:
    value = environment.get(name, default)
    if (
        not isinstance(value, str)
        or not 1 <= len(value) <= 5
        or not value.isascii()
        or not value.isdecimal()
        or not 1 <= int(value) <= 65535
    ):
        raise ConnectionError(ERROR)
    return int(value)


def render(
    mode: str,
    environment: Mapping[str, str],
    *,
    secrets_dir: Path = SECRETS_DIRECTORY,
) -> str:
    """Return one URI only to the trusted Airflow _CMD consumer.

    The Python-only directory argument permits synthetic tests. The CLI has
    no arbitrary file/endpoint override. No input mapping is modified.
    """
    try:
        if not isinstance(environment, Mapping):
            raise ConnectionError(ERROR)
        if mode in {"metadata", "result"}:
            port = _port(environment, "POSTGRES_PORT", "5432")
            password = _read_secret(secrets_dir, "airflow_db_password", broker=False)
            scheme = (
                "postgresql+psycopg2"
                if mode == "metadata"
                else "db+postgresql+psycopg2"
            )
            return (
                f"{scheme}://airflow:{quote(password, safe='')}@mng-pg:{port}/airflow"
            )
        if mode != "broker":
            raise ConnectionError(ERROR)
        host = environment.get("AIRFLOW_VALKEY_HOST", "mng-valkey")
        secret = environment.get("AIRFLOW_VALKEY_SECRET", "mng_valkey_password")
        if (host, secret) not in BROKERS:
            raise ConnectionError(ERROR)
        port = _port(environment, "VALKEY_PORT", "6379")
        password = _read_secret(secrets_dir, secret, broker=True)
        return f"redis://:{quote(password, safe='')}@{host}:{port}/0"
    except (OSError, UnicodeError, ValueError, TypeError):
        pass
    # Raise outside the handler so even the suppressed exception context cannot
    # retain a UnicodeDecodeError containing the original credential bytes.
    raise ConnectionError(ERROR)


def _discard_failed_stdout(output) -> None:
    """Prevent CPython's shutdown flush from retrying a failed real pipe.

    Leave injected/test streams alone. Only the failed process stdout file
    descriptor is redirected; no credential is written to a fallback output.
    https://docs.python.org/3.13/library/signal.html#note-on-sigpipe
    """
    if output is not sys.stdout:
        return
    try:
        descriptor = os.open(os.devnull, os.O_WRONLY | os.O_CLOEXEC)
        try:
            os.dup2(descriptor, output.fileno())
        finally:
            os.close(descriptor)
    except OSError:
        pass


def main(
    argv: Sequence[str] | None = None,
    *,
    environment: Mapping[str, str] | None = None,
    secrets_dir: Path = SECRETS_DIRECTORY,
    stdout=None,
    stderr=None,
) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    try:
        if len(arguments) != 1:
            raise ConnectionError(ERROR)
        value = render(
            arguments[0],
            os.environ if environment is None else environment,
            secrets_dir=secrets_dir,
        )
        output.write(value)
        output.flush()
        return 0
    except (ConnectionError, OSError, KeyboardInterrupt) as failure:
        if isinstance(failure, OSError):
            _discard_failed_stdout(output)
        try:
            errors.write(ERROR + "\n")
        except OSError:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
