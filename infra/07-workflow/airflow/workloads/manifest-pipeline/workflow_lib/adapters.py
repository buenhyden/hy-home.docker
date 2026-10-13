"""Task-time adapters for protected worker files and the dedicated DEV batch.

No imports of optional drivers, credential reads, or connections occur at module
import. Error messages expose stable codes and retain no driver exception chain.
"""

from __future__ import annotations

import json
import os
import re
import stat
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import MappingProxyType
from urllib.parse import urlsplit

from .manifest import MAX_BYTES, ContractError
from .tls import pin_ca

PRIVATE_DIRECTORY = "/run/opsflow"
MAX_CONFIG_BYTES = 16384
S3_TLS_ENDPOINT = "https://seaweedfs-s3:443"
S3_TLS_CONTRACT = "https:seaweedfs-s3:443"
LIBPQ_ENVIRONMENT = frozenset(
    """PGAPPNAME PGCHANNELBINDING PGCLIENTENCODING PGCONNECT_TIMEOUT PGDATABASE
    PGGSSDELEGATION PGGSSENCMODE PGGSSLIB PGHOST PGHOSTADDR PGKRBSRVNAME
    PGLOADBALANCEHOSTS PGMAXPROTOCOLVERSION PGMINPROTOCOLVERSION PGOPTIONS
    PGPASSFILE PGPASSWORD PGPORT PGREQUIREAUTH PGREQUIREPEER PGREQUIRESSL
    PGSERVICE PGSERVICEFILE PGSSLCERT PGSSLCERTMODE PGSSLCOMPRESSION PGSSLCRL
    PGSSLCRLDIR PGSSLKEY PGSSLMAXPROTOCOLVERSION PGSSLMINPROTOCOLVERSION
    PGSSLMODE PGSSLNEGOTIATION PGSSLROOTCERT PGSSLSNI PGSYSCONFDIR
    PGTARGETSESSIONATTRS PGUSER SSL_CERT_DIR SSL_CERT_FILE""".split()
)
PG_FIELDS = frozenset(
    {
        "host",
        "port",
        "dbname",
        "user",
        "password",
        "connect_timeout",
        "statement_timeout_ms",
        "lock_timeout_ms",
        "sslmode",
        "sslrootcert",
    }
)
S3_FIELDS = frozenset(
    {
        "endpoint_url",
        "access_key_id",
        "secret_access_key",
        "bucket",
        "region",
        "addressing_style",
        "ca_bundle",
        "connect_timeout",
        "read_timeout",
        "endpoint_contract",
    }
)
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class DependencyError(RuntimeError):
    """A redacted task-time dependency failure."""


def _integer(value, maximum=120):
    return type(value) is int and 0 < value <= maximum


def _strings(config, fields):
    return all(
        isinstance(config.get(key), str) and config[key].strip() for key in fields
    )


def _ca_path(value):
    return isinstance(value, str) and value == PRIVATE_DIRECTORY + "/ca.pem"


def _pg_config(config):
    if not isinstance(config, Mapping) or set(config) != PG_FIELDS:
        raise ContractError("pg_config")
    if not _strings(config, ("host", "dbname", "user", "password", "sslmode")):
        raise ContractError("pg_config")
    if (
        config["host"] != "dev-pg"
        or type(config["port"]) is not int
        or config["port"] != 5432
        or config["dbname"] != "opsflow_dev"
        or config["user"] != "opsflow_ingest"
    ):
        raise ContractError("pg_target")
    if not (
        _integer(config["connect_timeout"])
        and _integer(config["statement_timeout_ms"], 300000)
        and _integer(config["lock_timeout_ms"], 300000)
    ):
        raise ContractError("pg_timeout")
    if not (
        (config["sslmode"] == "disable" and config["sslrootcert"] is None)
        or (config["sslmode"] == "verify-full" and _ca_path(config["sslrootcert"]))
    ):
        raise ContractError("pg_tls")
    return deepcopy(dict(config))


def _s3_config(config):
    if not isinstance(config, Mapping) or set(config) != S3_FIELDS:
        raise ContractError("s3_config")
    strings = S3_FIELDS - {"ca_bundle", "connect_timeout", "read_timeout"}
    if not _strings(config, strings) or config["bucket"] != "opsflow-dev":
        raise ContractError("s3_config")
    if config["addressing_style"] != "path" or not re.fullmatch(
        r"[a-z0-9-]{1,63}", config["region"]
    ):
        raise ContractError("s3_config")
    if not _integer(config["connect_timeout"]) or not _integer(config["read_timeout"]):
        raise ContractError("s3_timeout")
    endpoint = urlsplit(config["endpoint_url"])
    port = endpoint.port  # Invalid numeric ports are handled by the redacted caller.
    if (
        endpoint.username
        or endpoint.password
        or endpoint.query
        or endpoint.fragment
        or endpoint.path not in ("", "/")
        or not endpoint.hostname
    ):
        raise ContractError("s3_endpoint")
    internal = (
        config["endpoint_url"] == "http://seaweedfs-s3:8333"
        and config["endpoint_contract"] == "seaweedfs-s3-internal-v1"
        and config["ca_bundle"] is None
    )
    secure = (
        config["endpoint_url"] == S3_TLS_ENDPOINT
        and endpoint.scheme == "https"
        and endpoint.hostname == "seaweedfs-s3"
        and port == 443
        and config["endpoint_contract"] == S3_TLS_CONTRACT
        and _ca_path(config["ca_bundle"])
    )
    if not (internal or secure):
        raise ContractError("s3_endpoint")
    return deepcopy(dict(config))


def _validated(config, schema):
    result = None
    error = None
    try:
        if schema == "pg":
            result = _pg_config(config)
        elif schema == "s3":
            result = _s3_config(config)
        else:
            raise ContractError("private_schema")
    except Exception:
        error = "private_config_rejected"
    if error:
        raise ContractError(error)
    return result


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _absolute_parts(path):
    if not isinstance(path, str) or not path.startswith("/") or "\x00" in path:
        raise ValueError("private_path")
    parts = path.split("/")[1:]
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError("private_path")
    return parts


def _directory_fd(parts, allowed_owners, expected_group, effective_groups):
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for index, name in enumerate(parts):
            child = os.open(
                name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            os.close(fd)
            fd = child
            info = os.fstat(fd)
            mode = stat.S_IMODE(info.st_mode)
            trusted_tmp = (
                index == 0 and name == "tmp" and info.st_uid == 0 and mode == 0o1777
            )
            if info.st_uid not in {0, os.geteuid()} or (
                mode & 0o022 and not trusted_tmp
            ):
                raise ValueError("private_parent")
            if index == len(parts) - 1:
                if info.st_uid not in allowed_owners or mode not in (0o700, 0o750):
                    raise ValueError("private_directory")
                expected_group = (
                    info.st_gid if expected_group is None else expected_group
                )
                if (
                    info.st_gid != expected_group
                    or expected_group not in effective_groups
                ):
                    raise ValueError("private_directory_group")
        return fd, expected_group
    except Exception:
        os.close(fd)
        raise


def _signature(info):
    return (
        info.st_dev,
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
        info.st_mode,
        info.st_uid,
        info.st_gid,
        info.st_nlink,
    )


def _verified_bytes(parent_fd, name, allowed_owners, expected_group):
    secret_fd = os.open(
        name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd
    )
    with os.fdopen(secret_fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_uid not in allowed_owners
            or before.st_gid != expected_group
            or stat.S_IMODE(before.st_mode) not in (0o600, 0o640)
            or before.st_size > MAX_CONFIG_BYTES
        ):
            raise ValueError("private_file")
        raw = stream.read(MAX_CONFIG_BYTES + 1)
        after = os.fstat(stream.fileno())
        if len(raw) > MAX_CONFIG_BYTES or _signature(before) != _signature(after):
            raise ValueError("private_changed")
    return raw, after


def _private_read(path, directory, uid, gid):
    if any(
        value is not None and (type(value) is not int or value < 0)
        for value in (uid, gid)
    ):
        raise ValueError("private_identity")
    parts = _absolute_parts(path)
    directory_parts = _absolute_parts(directory)
    if parts[:-1] != directory_parts or parts[-1] not in ("pg.json", "s3.json"):
        raise ValueError("private_path")
    allowed_owners = {0, os.geteuid()} if uid is None else {0, uid}
    effective_groups = {os.getegid(), *os.getgroups()}
    expected_group = gid
    if expected_group is not None and expected_group not in effective_groups:
        raise ValueError("private_group")
    fd, expected_group = _directory_fd(
        directory_parts, allowed_owners, expected_group, effective_groups
    )
    try:
        parent_identity = os.fstat(fd)
        raw, file_info = _verified_bytes(fd, parts[-1], allowed_owners, expected_group)
        current_fd, _ = _directory_fd(
            directory_parts, allowed_owners, expected_group, effective_groups
        )
        try:
            current_parent = os.fstat(current_fd)
            current_file = os.stat(parts[-1], dir_fd=current_fd, follow_symlinks=False)
            if (parent_identity.st_dev, parent_identity.st_ino) != (
                current_parent.st_dev,
                current_parent.st_ino,
            ) or _signature(file_info) != _signature(current_file):
                raise ValueError("private_path_changed")
        finally:
            os.close(current_fd)
        return json.loads(raw, object_pairs_hook=_unique_object)
    finally:
        os.close(fd)


def read_private_json(
    path,
    *,
    expected_directory=PRIVATE_DIRECTORY,
    expected_uid=None,
    expected_gid=None,
    schema=None,
):
    """Read one exact, identity-checked pg.json/s3.json worker file using fd traversal.

    Callers may bind observed worker IDs explicitly. Defaults accept root or the
    current effective owner; file group must match the protected directory and a
    current authorized effective or supplementary worker group.
    An explicit temporary directory is useful only for isolated synthetic tests.
    """
    result = None
    failed = False
    try:
        schema = schema or PurePosixPath(path).stem
        if schema != PurePosixPath(path).stem:
            raise ValueError("private_schema_path")
        result = _validated(
            _private_read(path, expected_directory, expected_uid, expected_gid), schema
        )
    except Exception:
        failed = True
    if failed:
        raise ContractError("private_file_rejected")
    return result


def _pin_ca(path):
    return pin_ca(path, expected_directory=PRIVATE_DIRECTORY)


def _key(key, prefix):
    if not isinstance(key, str) or not key.startswith(prefix + "/") or len(key) > 512:
        raise ContractError("s3_key")
    parts = key.split("/")
    if any(part in ("", ".", "..") or part.startswith(".") for part in parts):
        raise ContractError("s3_key")
    forbidden = {"secret", "secrets", "password", "passwords", "credentials", "tokens"}
    if any(part.lower() in forbidden for part in parts) or not re.fullmatch(
        r"[A-Za-z0-9_./-]+", key
    ):
        raise ContractError("s3_key")
    return key


def _driver_code(error):
    response = getattr(error, "response", {})
    return (
        str(response.get("Error", {}).get("Code", ""))
        if isinstance(response, dict)
        else ""
    )


def _head(client, bucket, key):
    missing = False
    failed = False
    result = None
    try:
        result = client.head_object(Bucket=bucket, Key=key)
    except Exception as error:
        missing = _driver_code(error) in {"NoSuchKey", "NotFound", "404"}
        failed = not missing
    if failed:
        raise DependencyError("s3_request_failed")
    return None if missing else result


def _task_action(action, code):
    failure = None
    result = None
    try:
        result = action()
    except ContractError:
        failure = ContractError("s3_contract_rejected")
    except Exception:
        failure = DependencyError(code)
    if failure:
        raise failure
    return result


def _require_s3_origin(request, **_):
    try:
        endpoint = urlsplit(request.url)
        valid = (
            endpoint.scheme == "https"
            and endpoint.hostname == "seaweedfs-s3"
            and endpoint.port == 443
            and not endpoint.username
            and not endpoint.password
            and not endpoint.query
            and not endpoint.fragment
        )
    except Exception:
        valid = False
    if not valid:
        raise DependencyError("s3_endpoint_changed")


def _reject_s3_redirect(response=None, **_):
    if not response or not isinstance(response, tuple) or not response:
        return
    raw = response[0]
    status = getattr(raw, "status_code", None)
    headers = getattr(raw, "headers", {})
    location = isinstance(headers, Mapping) and any(
        str(name).lower() == "location" for name in headers
    )
    if (type(status) is int and 300 <= status < 400) or location:
        raise DependencyError("s3_redirect_rejected")


class S3Store:
    """Restricted input reader and conditional verified artifact writer."""

    def __init__(self, config):
        config = _validated(config, "s3")
        ca = _pin_ca(config["ca_bundle"]) if config["ca_bundle"] else None

        def create():
            import boto3
            from botocore.config import Config

            client = boto3.client(
                "s3",
                endpoint_url=config["endpoint_url"],
                region_name=config["region"],
                aws_access_key_id=config["access_key_id"],
                aws_secret_access_key=config["secret_access_key"],
                verify=ca.path if ca else True,
                config=Config(
                    signature_version="s3v4",
                    connect_timeout=config["connect_timeout"],
                    read_timeout=config["read_timeout"],
                    retries={"mode": "standard", "max_attempts": 2},
                    s3={"addressing_style": "path"},
                    proxies={},
                ),
            )
            try:
                if ca:
                    client.meta.events.register_first(
                        "before-send.s3",
                        _require_s3_origin,
                        unique_id="opsflow-exact-s3-origin",
                    )
                    client.meta.events.register_first(
                        "needs-retry.s3",
                        _reject_s3_redirect,
                        unique_id="opsflow-deny-s3-redirect",
                    )
            except Exception:
                client.close()
                raise
            return client

        try:
            self.client = _task_action(create, "s3_dependency_unavailable")
        except Exception:
            if ca:
                ca.close()
            raise
        self._ca = ca
        self._closed = False
        self.bucket = config["bucket"]

    def __enter__(self):
        return self

    def __exit__(self, kind, *_):
        try:
            self.close()
        except DependencyError:
            if kind is None:
                raise
        return False

    def close(self):
        if self._closed:
            return
        self._closed = True
        failed = False
        try:
            self.client.close()
        except Exception:
            failed = True
        finally:
            self.client = None
            if self._ca:
                try:
                    self._ca.close()
                except ContractError:
                    failed = True
                self._ca = None
        if failed:
            raise DependencyError("s3_close_failed")

    def _read(self, key, head):
        if not isinstance(head, dict) or type(head.get("ContentLength")) is not int:
            raise DependencyError("s3_metadata_invalid")
        if head["ContentLength"] < 0 or head["ContentLength"] > MAX_BYTES:
            raise ContractError("input_size")
        etag = head.get("ETag")
        if not isinstance(etag, str) or not etag:
            raise DependencyError("s3_metadata_invalid")
        response = self.client.get_object(Bucket=self.bucket, Key=key, IfMatch=etag)
        stream = response["Body"]
        try:
            raw = stream.read(MAX_BYTES + 1)
        finally:
            stream.close()
        if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
            raise ContractError("input_size")
        if len(raw) != head["ContentLength"] or response.get("ETag") != etag:
            raise DependencyError("s3_read_changed")
        return raw

    def read_input(self, key):
        _key(key, "manifest-input")

        def read():
            head = _head(self.client, self.bucket, key)
            if head is None:
                raise DependencyError("s3_input_missing")
            return self._read(key, head)

        return _task_action(read, "s3_input_failed")

    def _create(self, key, body):
        failed = False
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType="application/json",
                IfNoneMatch="*",
            )
        except Exception as error:
            failed = _driver_code(error) not in {
                "PreconditionFailed",
                "412",
                "ConditionalRequestConflict",
                "409",
            }
        if failed:
            raise DependencyError("s3_output_failed")

    def put_verified(self, key, body):
        _key(key, "manifest-validated")
        if not isinstance(body, bytes) or not body or len(body) > MAX_BYTES:
            raise ContractError("artifact_size")

        def write():
            head = _head(self.client, self.bucket, key)
            if head is None:
                self._create(key, body)
                head = _head(self.client, self.bucket, key)
            if head is None or self._read(key, head) != body:
                raise DependencyError("s3_verify_failed")

        return _task_action(write, "s3_output_failed")


@dataclass(frozen=True, repr=False)
class _ProtectedConfig(Mapping):
    """Read-only driver inputs whose normal representation never exposes values."""

    _values: Mapping

    def __getitem__(self, key):
        return self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return "<protected opsflow configuration>"


class PgPublisher:
    """One restricted publication transaction; construction performs no DB I/O."""

    def __init__(self, config):
        config = _validated(config, "pg")
        self._config = _ProtectedConfig(MappingProxyType(config))

    @property
    def config(self):
        return self._config

    def publish(self, manifest, identifier, digest, artifact):
        if not isinstance(identifier, str) or not DIGEST.fullmatch(identifier):
            raise ContractError("run_id")
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise ContractError("manifest_digest")
        _key(artifact, "manifest-validated")
        failed = False
        result = None
        ca = None
        try:
            if any(name in os.environ for name in LIBPQ_ENVIRONMENT):
                raise ValueError("libpq_environment")
            config = self.config
            ca = _pin_ca(config["sslrootcert"]) if config["sslrootcert"] else None
            import psycopg2
            from psycopg2.extras import Json

            connection = psycopg2.connect(
                **{
                    key: config[key]
                    for key in (
                        "host",
                        "port",
                        "dbname",
                        "user",
                        "password",
                        "connect_timeout",
                        "sslmode",
                    )
                },
                sslrootcert=ca.path if ca else None,
                gssencmode="disable",
                application_name="source_manifest_ingest",
                options=f"-c statement_timeout={config['statement_timeout_ms']} "
                f"-c lock_timeout={config['lock_timeout_ms']}",
            )
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT ops_flow.publish_manifest(%s,%s,%s,%s,%s::jsonb,%s)",
                            (
                                manifest.source,
                                identifier,
                                digest,
                                manifest.captured_at,
                                Json([dict(record) for record in manifest.records]),
                                artifact,
                            ),
                        )
                        row = cursor.fetchone()
                        if not row or row[0] not in (
                            "published",
                            "historical",
                            "replayed",
                        ):
                            raise ValueError("publication_result")
                        result = row[0]
            finally:
                connection.close()
        except Exception:
            failed = True
        finally:
            if ca:
                try:
                    ca.close()
                except ContractError:
                    failed = True
        if failed:
            raise DependencyError("pg_publish_failed")
        return result
