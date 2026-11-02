"""Bounded object recovery and exact synthetic storage permissions for P04."""

from __future__ import annotations

import base64
import hashlib
import json
from urllib.parse import urlencode


class RehearsalFailure(AssertionError):
    """Fixed snapshot diagnostic, also usable inside the isolated client."""


MAX_OBJECT_BYTES = 1024 * 1024
MAX_OBJECTS = 16
MAX_SNAPSHOT_BYTES = 2 * 1024 * 1024
BUCKET = "opsflow-dev"
# 4.48 static identities set generatePrincipalArn(name) with default account
# before binding Account. buildPrincipalARN prefers that explicit principal.
# https://github.com/seaweedfs/seaweedfs/blob/4.48/weed/s3api/auth_credentials.go
WORKER_PRINCIPAL = "arn:aws:iam::000000000000:user/synthetic-worker"


def production_environment():
    from tests.validation._opsflow_airflow_native_guards import airflow_environment

    values = dict(row.split("=", 1) for row in airflow_environment())
    modes = {
        "DATABASE__SQL_ALCHEMY_CONN_CMD": "metadata",
        "CELERY__RESULT_BACKEND_CMD": "result",
        "CELERY__BROKER_URL_CMD": "broker",
    }
    return tuple(
        key + "=" + value
        for key, value in {
            **values,
            **{
                "AIRFLOW__" + key: "python3 /opt/airflow/bin/connection_uri.py " + mode
                for key, mode in modes.items()
            },
            "POSTGRES_PORT": "55432",
            "VALKEY_PORT": "6389",
            "AIRFLOW_VALKEY_HOST": "mng-valkey",
            "AIRFLOW_VALKEY_SECRET": "mng_valkey_password",
        }.items()
    )


def s3_configuration(worker_key, worker_secret, admin_key, admin_secret):
    # Exact 4.48 legacy identity path grants; explicit delete deny is below.
    # https://github.com/seaweedfs/seaweedfs/blob/4.48/weed/s3api/auth_credentials.go
    prefixes = ("manifest-input", "manifest-validated", "manifest-quarantine")
    actions = ["Read:" + BUCKET + "/" + prefix + "/*" for prefix in prefixes]
    actions += ["Write:" + BUCKET + "/" + prefix + "/*" for prefix in prefixes[1:]]
    return {
        "identities": [
            {
                "name": "synthetic-worker",
                "account": {"id": "111111111111"},
                "credentials": [{"accessKey": worker_key, "secretKey": worker_secret}],
                "actions": actions,
            },
            {
                "name": "synthetic-administrator",
                "account": {"id": "222222222222"},
                "credentials": [{"accessKey": admin_key, "secretKey": admin_secret}],
                "actions": ["Admin", "Read", "Write", "List", "Tagging"],
            },
        ]
    }


def worker_bucket_policy():
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "WorkerCannotDelete",
                "Effect": "Deny",
                "Principal": {"AWS": WORKER_PRINCIPAL},
                "Action": ["s3:DeleteObject", "s3:DeleteObjectVersion"],
                "Resource": ["arn:aws:s3:::" + BUCKET + "/*"],
            }
        ],
    }


def permission_observations(client, bucket):
    """Report fixed action/status facts, never a service message or payload."""
    _bucket(bucket)

    def read_canary():
        row = client.get_object(Bucket=bucket, Key="manifest-input/permission-canary")
        try:
            matches = row["Body"].read(64) == b"synthetic"
        finally:
            row["Body"].close()
        return {**row, "body_matches": matches}

    attempts = (
        ("allowed_read", 200, read_canary),
        (
            "allowed_write",
            200,
            lambda: client.put_object(
                Bucket=bucket,
                Key="manifest-validated/permission-write",
                Body=b"synthetic",
            ),
        ),
        (
            "foreign_bucket",
            403,
            lambda: client.get_object(Bucket="p04-foreign-bucket", Key="denied"),
        ),
        (
            "foreign_prefix",
            403,
            lambda: client.get_object(Bucket=bucket, Key="foreign-prefix/denied"),
        ),
        (
            "input_write",
            403,
            lambda: client.put_object(
                Bucket=bucket, Key="manifest-input/denied", Body=b"synthetic"
            ),
        ),
        (
            "foreign_write",
            403,
            lambda: client.put_object(
                Bucket=bucket, Key="foreign-prefix/denied", Body=b"synthetic"
            ),
        ),
        (
            "delete",
            403,
            lambda: client.delete_object(
                Bucket=bucket, Key="manifest-validated/permission-canary"
            ),
        ),
        ("list", 403, lambda: client.list_objects_v2(Bucket=bucket)),
    )
    observed = {}
    for name, expected, operation in attempts:
        body_matches = True
        try:
            result = operation()
            status = result.get("ResponseMetadata", {}).get("HTTPStatusCode")
            body_matches = result.get("body_matches", True)
            if "Body" in result:
                result["Body"].close()
        except Exception as error:
            response = getattr(error, "response", {})
            status = (
                response.get("ResponseMetadata", {}).get("HTTPStatusCode")
                if isinstance(response, dict)
                else None
            )
        status = status if type(status) is int and 100 <= status <= 599 else None
        observed[name] = {
            "expected_http": expected,
            "observed_http": status,
            "passed": status == expected and body_matches is True,
        }
    return observed


def _expected_permissions():
    return {
        "allowed_read": 200,
        "allowed_write": 200,
        "foreign_bucket": 403,
        "foreign_prefix": 403,
        "input_write": 403,
        "foreign_write": 403,
        "delete": 403,
        "list": 403,
    }


def permissions_passed(observed):
    expected = _expected_permissions()
    return (
        isinstance(observed, dict)
        and set(observed) == set(expected)
        and all(
            isinstance(row, dict)
            and set(row) == {"expected_http", "observed_http", "passed"}
            and type(row["expected_http"]) is int
            and row["expected_http"] == expected[name]
            and type(row["observed_http"]) is int
            and row["observed_http"] == expected[name]
            and row["passed"] is True
            for name, row in observed.items()
        )
    )


def parse_permission_observations(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise RehearsalFailure("duplicate permission observation rejected")
            result[key] = value
        return result

    if not isinstance(raw, str) or len(raw.encode()) > 8192:
        raise RehearsalFailure("permission observation bound rejected")
    observed = json.loads(raw, object_pairs_hook=unique)
    expected = _expected_permissions()
    if not isinstance(observed, dict) or set(observed) != set(expected):
        raise RehearsalFailure("permission observation schema rejected")
    for name, row in observed.items():
        if (
            not isinstance(row, dict)
            or set(row) != {"expected_http", "observed_http", "passed"}
            or type(row["expected_http"]) is not int
            or row["expected_http"] != expected[name]
            or not (
                row["observed_http"] is None
                or (
                    type(row["observed_http"]) is int
                    and 100 <= row["observed_http"] <= 599
                )
            )
            or type(row["passed"]) is not bool
            or (row["passed"] is True and row["observed_http"] != expected[name])
        ):
            raise RehearsalFailure("permission observation schema rejected")
    return observed


def _bucket(bucket):
    if bucket != BUCKET:
        raise RehearsalFailure("object snapshot bucket rejected")


def _metadata(value):
    if (
        not isinstance(value, dict)
        or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()
        )
        or sum(len(k.encode()) + len(v.encode()) for k, v in value.items()) > 2048
    ):
        raise RehearsalFailure("object snapshot metadata rejected")
    return dict(value)


def _tags(value):
    if not isinstance(value, list) or len(value) > 10:
        raise RehearsalFailure("object snapshot tags rejected")
    pairs = []
    for row in value:
        if (
            not isinstance(row, dict)
            or set(row) != {"Key", "Value"}
            or any(not isinstance(v, str) for v in row.values())
            or not 1 <= len(row["Key"]) <= 128
            or len(row["Value"]) > 256
        ):
            raise RehearsalFailure("object snapshot tags rejected")
        pairs.append((row["Key"], row["Value"]))
    if len({key for key, _ in pairs}) != len(pairs):
        raise RehearsalFailure("object snapshot tags rejected")
    return [{"Key": key, "Value": value} for key, value in sorted(pairs)]


def _key(key):
    if (
        not isinstance(key, str)
        or not key.startswith(
            ("manifest-input/", "manifest-validated/", "manifest-quarantine/")
        )
        or len(key.encode()) > 1024
        or any(part in ("", ".", "..") for part in key.split("/"))
    ):
        raise RehearsalFailure("object snapshot key rejected")


def capture_objects(client, bucket):
    _bucket(bucket)
    listed = client.list_objects_v2(Bucket=bucket, MaxKeys=MAX_OBJECTS + 1)
    rows = listed.get("Contents", [])
    if (
        listed.get("IsTruncated")
        or not isinstance(rows, list)
        or len(rows) > MAX_OBJECTS
    ):
        raise RehearsalFailure("object snapshot listing rejected")
    snapshot = {}
    for listed_row in rows:
        key = listed_row["Key"]
        _key(key)
        if key in snapshot:
            raise RehearsalFailure("object snapshot duplicate rejected")
        row = client.get_object(Bucket=bucket, Key=key)
        body = row["Body"]
        try:
            raw = body.read(MAX_OBJECT_BYTES + 1)
        finally:
            body.close()
        if len(raw) > MAX_OBJECT_BYTES or row["ContentLength"] != len(raw):
            raise RehearsalFailure("object snapshot size rejected")
        content_type = row.get("ContentType")
        if not isinstance(content_type, str) or not 1 <= len(content_type) <= 256:
            raise RehearsalFailure("object snapshot content type rejected")
        snapshot[key] = {
            "body": base64.b64encode(raw).decode(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size": len(raw),
            "content_type": content_type,
            "metadata": _metadata(row.get("Metadata", {})),
            "tags": _tags(client.get_object_tagging(Bucket=bucket, Key=key)["TagSet"]),
        }
        _snapshot_bound(snapshot)
    return snapshot


def _snapshot_bound(snapshot):
    if len(json.dumps(snapshot).encode()) > MAX_SNAPSHOT_BYTES:
        raise RehearsalFailure("aggregate object snapshot size rejected")


def _restore_rows(snapshot):
    if not isinstance(snapshot, dict) or len(snapshot) > MAX_OBJECTS:
        raise RehearsalFailure("object snapshot shape rejected")
    prepared = []
    encoded_total = 0
    for key, row in snapshot.items():
        _key(key)
        if not isinstance(row, dict) or set(row) != {
            "body",
            "sha256",
            "size",
            "content_type",
            "metadata",
            "tags",
        }:
            raise RehearsalFailure("object snapshot fields rejected")
        if not isinstance(row["body"], str) or len(row["body"]) > 4 * (
            (MAX_OBJECT_BYTES + 2) // 3
        ):
            raise RehearsalFailure("object snapshot encoded size rejected")
        encoded_total += len(row["body"])
        if encoded_total > MAX_SNAPSHOT_BYTES:
            raise RehearsalFailure("aggregate object snapshot size rejected")
        try:
            raw = base64.b64decode(row["body"], validate=True)
        except (ValueError, TypeError):
            raise RehearsalFailure("object snapshot body rejected") from None
        if (
            len(raw) > MAX_OBJECT_BYTES
            or type(row["size"]) is not int
            or len(raw) != row["size"]
            or hashlib.sha256(raw).hexdigest() != row["sha256"]
            or not isinstance(row["content_type"], str)
            or not 1 <= len(row["content_type"]) <= 256
        ):
            raise RehearsalFailure("object snapshot integrity rejected")
        prepared.append(
            (
                key,
                raw,
                row["content_type"],
                _metadata(row["metadata"]),
                _tags(row["tags"]),
            )
        )
    _snapshot_bound(snapshot)
    return prepared


def restore_stdin(client, bucket, stream):
    payload = stream.read(MAX_SNAPSHOT_BYTES + 1)
    if len(payload.encode()) > MAX_SNAPSHOT_BYTES:
        raise RehearsalFailure("aggregate object snapshot size rejected")
    restore_objects(client, bucket, json.loads(payload))


def validate_snapshot(snapshot):
    """Apply restore's exact pure admission before any owned source teardown."""
    _restore_rows(snapshot)


def restore_snapshot(owned, snapshot):
    from tests.validation._opsflow_airflow_native_fixture import S3_CLIENT

    _restore_rows(snapshot)
    command = S3_CLIENT + (
        "sys.path.insert(0,'/opt/airflow/dags'); import p04_native_data as d; "
        "d.restore_stdin(s,b,sys.stdin)"
    )
    owned.execute("storage-admin", "python", "-c", command, input_=json.dumps(snapshot))


def restore_objects(client, bucket, snapshot):
    _bucket(bucket)
    # Validate the entire input before the first write, then use fresh-only keys.
    prepared = _restore_rows(snapshot)
    for key, raw, content_type, metadata, tags in prepared:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=raw,
            ContentType=content_type,
            Metadata=metadata,
            Tagging=urlencode([(row["Key"], row["Value"]) for row in tags]),
            IfNoneMatch="*",
        )
    if capture_objects(client, bucket) != snapshot:
        raise RehearsalFailure("restored object metadata changed")
