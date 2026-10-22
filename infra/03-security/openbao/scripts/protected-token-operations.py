"""Two protected operator operations: periodic snapshot issuance and root revocation.

Actual authority comes from authenticated root, never from a custody receipt or
CLI argument. No operation retries a mutation, reads an auth file implicitly,
prints a credential, upgrades OpenBao or downloads/restores a snapshot.
"""

from __future__ import annotations

import hashlib
import hmac
import http.client
import ipaddress
import json
import os
import secrets
import stat
import sys
import threading
import time
import types
from pathlib import Path

MAINTENANCE_SHA256 = "4553286a0c6f4e45f1901942043762bfe6312d22cad281a3c3ffe15eb232429f"
PRIOR_POLICY_SHA256 = "84af105c666312712a0d6809e0a4c037ed66e7157027e94ac1d79c132131a608"
POLICY_SHA256 = "1aa658e05aee76127c7961abd218020fe6a319fd26253c78ecefb3ae99d4b622"
POLICY_FILE = "infra/03-security/openbao/config/policies/backup-snapshot.hcl"
CANONICAL_HOME_ROOT = Path("/home/hyunyoun/data/hy-home.docker")
POLICY = "sys/policies/acl/backup-snapshot"
CREATE = "auth/token/create-orphan"
RENEW = "auth/token/renew-self"
REVOKE = "auth/token/revoke-self"
CAPS = "sys/capabilities"
DENY_SECRET = "secret/data/hy-home/02-auth/keycloak"
CREATE_PAYLOAD = {
    "policies": ["backup-snapshot"],
    "no_default_policy": True,
    "period": "720h",
    "renewable": True,
    "type": "service",
    "num_uses": 0,
    "display_name": "hy-home-backup-snapshot",
}
CAPABILITIES = {
    "sys/storage/raft/snapshot": ["read"],
    "auth/token/lookup-self": ["read"],
    "auth/token/renew-self": ["update"],
    "auth/token/revoke-self": ["update"],
    DENY_SECRET: ["deny"],
}


class BindingBlocked(Exception):
    """No path, inner exception or public/private input is exposed."""


def read_public(path, expected_sha256):
    """Verify held bytes before execution/use; do not reopen through importlib."""
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise BindingBlocked()
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise BindingBlocked()
    directory = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    descriptor = None
    try:
        for component in path.parent.parts[1:]:
            following = os.open(
                component,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=directory,
            )
            os.close(directory)
            directory = following
        descriptor = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory
        )
        before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or not 1 <= before.st_size <= 1048576
        ):
            raise BindingBlocked()
        raw = os.read(descriptor, 1048577)
        after = os.fstat(descriptor)
        if (
            (
                before.st_dev,
                before.st_ino,
                before.st_mtime_ns,
                before.st_ctime_ns,
                before.st_size,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_mtime_ns,
                after.st_ctime_ns,
                after.st_size,
            )
            or len(raw) != before.st_size
            or not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), expected_sha256)
        ):
            raise BindingBlocked()
        return raw
    except OSError:
        raise BindingBlocked() from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory)


def load_maintenance():
    path = Path(__file__).absolute().with_name("protected-maintenance.py")
    raw = read_public(path, MAINTENANCE_SHA256)
    module = types.ModuleType("approved_protected_maintenance")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


try:
    BASE = load_maintenance()
except (BindingBlocked, OSError, ValueError):
    BASE = None

Blocked = BASE.Blocked if BASE else BindingBlocked
Indeterminate = BASE.Indeterminate if BASE else BindingBlocked


class OperationCustody(BASE.Custody if BASE else object):
    def __init__(self, directory, *, w1_directory=None, destination=None):
        if w1_directory is not None:
            distinct_directories(w1_directory, directory, destination)
        super().__init__(directory)

    def reserve(self, name):
        if name not in {
            ".lock",
            "operation-intent.json",
            "issuance-response.json",
            "renewal-response.json",
            "snapshot.token",
            "state.json",
        }:
            raise Blocked()
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        self.open_files = self.open_files | {descriptor}
        os.fchmod(descriptor, 0o600)
        if not BASE.private_file(os.fstat(descriptor)):
            raise Blocked()
        os.fsync(descriptor)
        os.fsync(self.fd)
        return descriptor


class Destination:
    """One fixed canonical target and retained issuance reservation; no overwrite."""

    def __init__(self, home_root, expected_device, expected_inode):
        root = Path(home_root)
        if (
            root != CANONICAL_HOME_ROOT
            or str(root) != str(home_root)
            or type(expected_device) is not int
            or type(expected_inode) is not int
        ):
            raise Blocked()
        self.root_fd = BASE.open_directory(root)
        self.fd = None
        self.path = root / "secrets/backup/openbao"
        self.expected_root = (expected_device, expected_inode)
        self.reserved = False
        self.mutation_started = False
        try:
            root_info = os.fstat(self.root_fd)
            if (
                root_info.st_dev,
                root_info.st_ino,
            ) != self.expected_root or root_info.st_uid != os.getuid():
                raise Blocked()
            self.fd = BASE.open_directory(self.path)
            info = os.fstat(self.fd)
            if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
                raise Blocked()
            for name in ("snapshot_token.txt", ".snapshot_token.txt.issuance-lock"):
                try:
                    os.stat(name, dir_fd=self.fd, follow_symlinks=False)
                except FileNotFoundError:
                    continue
                raise Blocked()
        except BaseException:
            if self.fd is not None:
                os.close(self.fd)
            os.close(self.root_fd)
            raise

    def check_current(self):
        root = BASE.open_directory(CANONICAL_HOME_ROOT)
        try:
            current = os.fstat(root)
            if (
                current.st_dev,
                current.st_ino,
            ) != self.expected_root or current.st_uid != os.getuid():
                raise Blocked()
        finally:
            os.close(root)
        current = BASE.open_directory(self.path)
        try:
            held, named = os.fstat(self.fd), os.fstat(current)
            if (
                (held.st_dev, held.st_ino) != (named.st_dev, named.st_ino)
                or held.st_uid != os.getuid()
                or stat.S_IMODE(held.st_mode) != 0o700
            ):
                raise Blocked()
        finally:
            os.close(current)

    def reserve(self):
        self.check_current()
        descriptor = os.open(
            ".snapshot_token.txt.issuance-lock",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        try:
            os.fchmod(descriptor, 0o600)
            os.fsync(descriptor)
            os.fsync(self.fd)
            self.reserved = True
        finally:
            os.close(descriptor)

    def deliver(self, token):
        if not self.reserved:
            raise Blocked()
        self.check_current()
        name = ".snapshot_token.txt." + secrets.token_hex(16) + ".pending"
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=self.fd,
        )
        try:
            os.fchmod(descriptor, 0o600)
            if not BASE.private_file(os.fstat(descriptor)):
                raise Blocked()
            raw = BASE.validate_secret(token).encode("ascii")
            while raw:
                count = os.write(descriptor, raw)
                if count <= 0:
                    raise Indeterminate()
                raw = raw[count:]
            os.fsync(descriptor)
            os.link(
                name,
                "snapshot_token.txt",
                src_dir_fd=self.fd,
                dst_dir_fd=self.fd,
                follow_symlinks=False,
            )
            os.unlink(name, dir_fd=self.fd)
            final = os.stat("snapshot_token.txt", dir_fd=self.fd, follow_symlinks=False)
            original = os.fstat(descriptor)
            if not BASE.private_file(final) or (final.st_dev, final.st_ino) != (
                original.st_dev,
                original.st_ino,
            ):
                raise Indeterminate()
            os.fsync(self.fd)
            self.check_current()
        finally:
            os.close(descriptor)

    def __enter__(self):
        return self

    def __exit__(self, _kind, error, _traceback):
        failed = False
        for descriptor in (self.fd, self.root_fd):
            try:
                os.close(descriptor)
            except OSError:
                failed = True
        if failed:
            if isinstance(error, Indeterminate):
                return False
            if self.mutation_started:
                raise Indeterminate() from None
            if error is None:
                raise Blocked() from None
        return False


class TokenAPI:
    """Fixed endpoints, fixed payloads and separate issue/revoke/backup identities."""

    def __init__(self, token, context, connect_ip, mode, policy=None):
        if mode not in {"issue", "revoke", "backup", "operator"}:
            raise Blocked()
        self.token = BASE.validate_secret(token)
        self.context = context
        self.connect_ip = str(ipaddress.ip_address(connect_ip))
        self.mode = mode
        self.policy = policy
        if mode == "issue" and (
            not isinstance(policy, str)
            or hashlib.sha256(policy.encode()).hexdigest() != POLICY_SHA256
        ):
            raise Blocked()

    def for_backup(self, token):
        return TokenAPI(token, self.context, self.connect_ip, "backup")

    def _check(self, method, path, document, deny):
        allowed = {
            "issue": {
                ("GET", BASE.LOOKUP),
                ("GET", BASE.SEAL),
                ("GET", POLICY),
                ("POST", POLICY),
                ("POST", CREATE),
                ("POST", CAPS),
            },
            "revoke": {("GET", BASE.LOOKUP), ("GET", BASE.SEAL), ("POST", REVOKE)},
            "backup": {("GET", BASE.LOOKUP), ("GET", DENY_SECRET), ("POST", RENEW)},
            "operator": {("GET", BASE.LOOKUP)},
        }
        if (method, path) not in allowed[self.mode]:
            raise Blocked()
        if deny and not (
            method == "GET"
            and (path == DENY_SECRET or (self.mode == "revoke" and path == BASE.LOOKUP))
        ):
            raise Blocked()
        expected = None
        if method == "POST":
            expected = {
                CREATE: CREATE_PAYLOAD,
                POLICY: {"policy": self.policy},
                RENEW: {},
                REVOKE: {},
            }.get(path)
            if path == CAPS:
                if (
                    not isinstance(document, dict)
                    or set(document) != {"token", "paths"}
                    or document["paths"] != list(CAPABILITIES)
                ):
                    raise Blocked()
                BASE.validate_secret(document["token"])
                return
        if document != expected:
            raise Blocked()

    def request(self, method, path, document=None, *, deny=False):
        self._check(method, path, document, deny)
        connection = BASE.PinnedConnection(
            BASE.HOST,
            443,
            connect_ip=self.connect_ip,
            context=self.context,
            timeout=BASE.REQUEST_SECONDS,
        )
        timer = threading.Timer(BASE.REQUEST_SECONDS, connection.abort)
        timer.daemon = True
        deadline = time.monotonic() + BASE.REQUEST_SECONDS
        timer.start()
        try:
            connection.request(
                method,
                "/v1/" + path,
                body=json.dumps(document) if document is not None else None,
                headers={
                    "X-Vault-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            if deny:
                if response.status != 403:
                    raise Blocked()
                return True  # No ordinary-secret/auth error body is consumed.
            if method == "GET" and path == POLICY and response.status == 404:
                return None
            if response.status not in (
                {200, 204} if method == "POST" and path in {POLICY, REVOKE} else {200}
            ):
                raise Blocked()
            raw = response.read(BASE.LIMIT + 1)
            if time.monotonic() >= deadline:
                raise Indeterminate()
            return None if response.status == 204 else BASE.parse_response(raw)
        except (OSError, http.client.HTTPException, ValueError):
            raise Indeterminate() from None
        except Blocked:
            if method == "POST":
                raise Indeterminate() from None
            raise
        finally:
            timer.cancel()
            connection.close()


def check_auth(response):
    auth = document(response).get("auth", {})
    if (
        not isinstance(auth, dict)
        or auth.get("policies") != ["backup-snapshot"]
        or auth.get("token_policies", ["backup-snapshot"]) != ["backup-snapshot"]
    ):
        raise Blocked()
    if (
        auth.get("orphan") is not True
        or auth.get("renewable") is not True
        or auth.get("entity_id") != ""
        or auth.get("token_type") != "service"
    ):
        raise Blocked()
    if type(auth.get("lease_duration")) is not int or auth["lease_duration"] != 2592000:
        raise Blocked()
    return BASE.validate_secret(auth.get("client_token"))


def check_backup(response):
    data = document(response).get("data", {})
    if (
        not isinstance(data, dict)
        or data.get("policies") != ["backup-snapshot"]
        or data.get("path") != CREATE
        or data.get("entity_id") != ""
        or data.get("type") != "service"
    ):
        raise Blocked()
    if (
        data.get("orphan") is not True
        or data.get("renewable") is not True
        or data.get("namespace_path", "") != ""
    ):
        raise Blocked()
    for key, value in (
        ("period", 2592000),
        ("creation_ttl", 2592000),
        ("explicit_max_ttl", 0),
        ("num_uses", 0),
    ):
        if type(data.get(key)) is not int or data[key] != value:
            raise Blocked()
    if type(data.get("ttl")) is not int or not 1 <= data["ttl"] <= 2592000:
        raise Blocked()
    BASE.validate_secret(data.get("id"))


def document(value):
    if not isinstance(value, dict):
        raise Blocked()
    return value


def policy_value(value):
    data = document(value).get("data")
    if not isinstance(data, dict) or not isinstance(data.get("policy"), str):
        raise Blocked()
    return data["policy"]


def recovery_operator(value):
    value = document(value)
    BASE.check_operator(value)
    data = value["data"]
    if (
        data.get("type") != "service"
        or data["ttl"] < 600
        or data["renewable"] is not True
    ):
        raise Blocked()


def distinct_directories(w1_directory, operation_directory, destination=None):
    identities = frozenset()
    for path in (w1_directory, operation_directory):
        descriptor = BASE.open_directory(path)
        try:
            info = os.fstat(descriptor)
            if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
                raise Blocked()
            identity = (info.st_dev, info.st_ino)
            if identity in identities:
                raise Blocked()
            identities = identities | {identity}
        finally:
            os.close(descriptor)
    if destination is not None:
        destination.check_current()
        info = os.fstat(destination.fd)
        if (info.st_dev, info.st_ino) in identities:
            raise Blocked()


def issue_snapshot(api, custody, destination, cluster, policy):
    BASE.check_root(document(api.request("GET", BASE.LOOKUP)))
    BASE.check_seal(document(api.request("GET", BASE.SEAL)), cluster)
    old = api.request("GET", POLICY)
    if old is not None:
        previous = policy_value(old)
        if hashlib.sha256(previous.encode()).hexdigest() not in {
            PRIOR_POLICY_SHA256,
            hashlib.sha256(policy.encode()).hexdigest(),
        }:
            raise Blocked()
    destination.reserve()
    intent = custody.reserve("operation-intent.json")
    custody.write(
        intent,
        {
            "operation": "issue-snapshot-token",
            "policy_sha256": hashlib.sha256(policy.encode()).hexdigest(),
            "maintenance_sha256": MAINTENANCE_SHA256,
            "target": "secrets/backup/openbao/snapshot_token.txt",
        },
    )
    issuance = custody.reserve("issuance-response.json")
    custody.mutation_started = destination.mutation_started = True
    try:
        api.request("POST", POLICY, {"policy": policy})
        readback = api.request("GET", POLICY)
        if policy_value(readback) != policy:
            raise Indeterminate()
        response = api.request("POST", CREATE, CREATE_PAYLOAD)
        custody.write(issuance, response)  # Durable before interpreting any credential.
        token = check_auth(response)
        proof = api.request("POST", CAPS, {"token": token, "paths": list(CAPABILITIES)})
        if document(proof).get("data") != CAPABILITIES:
            raise Indeterminate()
        backup_api = api.for_backup(token)
        check_backup(backup_api.request("GET", BASE.LOOKUP))
        backup_api.request("GET", DENY_SECRET, deny=True)
        renewal = custody.reserve("renewal-response.json")
        renewed = backup_api.request("POST", RENEW, {})
        custody.write(renewal, renewed)
        if check_auth(renewed) != token:
            raise Indeterminate()
        check_backup(backup_api.request("GET", BASE.LOOKUP))
        candidate = custody.reserve("snapshot.token")
        custody.write(candidate, token)
        destination.deliver(token)
        state = custody.reserve("state.json")
        custody.write(
            state, {"state": "SNAPSHOT_TOKEN_DELIVERED", "snapshot_saved": False}
        )
        return "SNAPSHOT_TOKEN_DELIVERED"
    except BaseException:
        raise Indeterminate() from None


def revoke_root(api, custody, cluster, operator=None):
    if (
        operator is None
        or not isinstance(operator.token, str)
        or operator.token == api.token
    ):
        raise Blocked()
    BASE.check_root(document(api.request("GET", BASE.LOOKUP)))
    BASE.check_seal(document(api.request("GET", BASE.SEAL)), cluster)
    intent = custody.reserve("operation-intent.json")
    custody.write(
        intent, {"operation": "revoke-root", "maintenance_sha256": MAINTENANCE_SHA256}
    )
    # Check after potentially unbounded filesystem I/O; only three bounded
    # network calls follow before the final positive control.
    recovery_operator(operator.request("GET", BASE.LOOKUP))
    custody.mutation_started = True
    try:
        api.request("POST", REVOKE, {})
        api.request("GET", BASE.LOOKUP, deny=True)
        recovery_operator(operator.request("GET", BASE.LOOKUP))
        result = "ROOT_REVOKED_OPERATOR_HEALTHY"
        state = custody.reserve("state.json")
        custody.write(
            state, {"state": result, "operator_checked": operator is not None}
        )
        return result
    except BaseException:
        raise Indeterminate() from None


def root_input(descriptor, w1_directory):
    directory = BASE.open_directory(w1_directory)
    state_fd = None
    try:
        info = os.fstat(directory)
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
            raise Blocked()
        named = os.stat("root.token", dir_fd=directory, follow_symlinks=False)
        offered = os.fstat(descriptor)
        if not BASE.private_file(named) or (named.st_dev, named.st_ino) != (
            offered.st_dev,
            offered.st_ino,
        ):
            raise Blocked()
        state_fd = os.open(
            "state.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory
        )
        state_info = os.fstat(state_fd)
        if not BASE.private_file(state_info) or not 1 <= state_info.st_size <= 4096:
            raise Blocked()
        state = BASE.parse_response(os.read(state_fd, 4097))
        if state != {"state": "DELIVERED", "operator_healthy": True}:
            raise Blocked()
        return BASE.read_secret_fd(descriptor)
    finally:
        if state_fd is not None:
            os.close(state_fd)
        os.close(directory)


def main(arguments=None):
    if BASE is None:
        print(
            "BLOCKED: approved maintenance source binding unavailable", file=sys.stderr
        )
        return 1
    parser = BASE.PrivateArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("issue-snapshot-token", "revoke-root"))
    for name in (
        "ca",
        "ca-sha256",
        "connect-ip",
        "expected-cluster-id",
        "custody-directory",
        "w1-custody-directory",
    ):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--root-fd", required=True, type=int)
    parser.add_argument("--operator-fd", type=int)
    parser.add_argument("--home-root")
    parser.add_argument("--expected-home-device", type=int)
    parser.add_argument("--expected-home-inode", type=int)
    parser.add_argument("--policy-sha256")
    try:
        options = parser.parse_args(arguments)
        if options.root_fd < 3 or not BASE.UUID.fullmatch(options.expected_cluster_id):
            raise Blocked()
        ipaddress.ip_address(options.connect_ip)
        if (
            options.operation == "issue-snapshot-token"
            and options.operator_fd is not None
        ):
            raise Blocked()
        if options.operation == "revoke-root":
            if options.operator_fd is None or options.operator_fd < 3:
                raise Blocked()
            root_info, operator_info = (
                os.fstat(options.root_fd),
                os.fstat(options.operator_fd),
            )
            if not BASE.private_file(root_info) or not BASE.private_file(operator_info):
                raise Blocked()
            if (root_info.st_dev, root_info.st_ino) == (
                operator_info.st_dev,
                operator_info.st_ino,
            ):
                raise Blocked()
        context = BASE.ca_context(options.ca, options.ca_sha256)
        if options.operation == "issue-snapshot-token":
            if (
                options.home_root is None
                or options.policy_sha256 is None
                or options.expected_home_device is None
                or options.expected_home_inode is None
            ):
                raise Blocked()
            if options.policy_sha256 != POLICY_SHA256:
                raise Blocked()
            policy = read_public(
                Path(__file__).absolute().parents[4] / POLICY_FILE,
                options.policy_sha256,
            ).decode("ascii")
            with (
                Destination(
                    options.home_root,
                    options.expected_home_device,
                    options.expected_home_inode,
                ) as destination,
                OperationCustody(
                    options.custody_directory,
                    w1_directory=options.w1_custody_directory,
                    destination=destination,
                ) as custody,
            ):
                token = root_input(options.root_fd, options.w1_custody_directory)
                api = TokenAPI(token, context, options.connect_ip, "issue", policy)
                result = issue_snapshot(
                    api, custody, destination, options.expected_cluster_id, policy
                )
        else:
            if (
                options.home_root is not None
                or options.policy_sha256 is not None
                or options.expected_home_device is not None
                or options.expected_home_inode is not None
            ):
                raise Blocked()
            with OperationCustody(
                options.custody_directory, w1_directory=options.w1_custody_directory
            ) as custody:
                token = root_input(options.root_fd, options.w1_custody_directory)
                operator = None
                if options.operator_fd is not None:
                    if options.operator_fd < 3:
                        raise Blocked()
                    operator_token = BASE.read_secret_fd(options.operator_fd)
                    if operator_token == token:
                        raise Blocked()
                    operator = TokenAPI(
                        operator_token, context, options.connect_ip, "operator"
                    )
                result = revoke_root(
                    TokenAPI(token, context, options.connect_ip, "revoke"),
                    custody,
                    options.expected_cluster_id,
                    operator,
                )
        try:
            print(result, flush=True)
        except OSError:
            raise Indeterminate() from None
        return 0
    except Indeterminate:
        print(
            "INDETERMINATE: preserve protected custody; never repeat token mutation",
            file=sys.stderr,
        )
        return 2
    except (Blocked, BindingBlocked, OSError, ValueError, EOFError, KeyboardInterrupt):
        print(
            "BLOCKED: no completion claimed; preserve protected custody",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
