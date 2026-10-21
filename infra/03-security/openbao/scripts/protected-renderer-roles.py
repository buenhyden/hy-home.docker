"""Apply the renderer policies, token roles and AppRole with root (RUN-0085 W1c).

Root comes only from the W1 custody descriptor. Every target is read before any
write, written once with the reviewed file bytes, then read back and compared.
The custody directory keeps the prior values for rollback and a value-free
receipt. No credential is created, printed or stored, and no write is retried.
`plan` does every read and records the same receipt shape with nothing written.
"""

from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import os
import stat
import sys
import threading
import time
import types
from pathlib import Path

TOKEN_OPERATIONS_SHA256 = (
    "e459ea9bf80ae04eb16464fd11aa005f22bcdb8c961bf97d8485cf4b0f8b58c0"
)
CONFIG = "infra/03-security/openbao/config/"
# (name, source file, sha256); order is the write order.
POLICIES = (
    (
        "renderer",
        "policies/renderer.hcl",
        "6dc424661967d7c50faf881f61ec258478b8a43be7b6cbde2cdbf71cff032cc1",
    ),
    (
        "renderer-issuer",
        "policies/renderer-issuer.hcl",
        "0ab86b526e0506b658184e0be20a9713a737262f921f1019f2f38609c394d3e5",
    ),
    (
        "renderer-cleanup",
        "policies/renderer-cleanup.hcl",
        "a42f0b23de31acbeaf3c88761ebc2ba5a696fbdfcfe6667062ed864e9998a7a5",
    ),
    (
        "hy-home-operator",
        "policies/operator.hcl",
        "e6d00966dda769cfed3af829c4a7606978cd79ee3437b3393fa54ca450b33093",
    ),
)
TOKEN_ROLES = (
    (
        "renderer-issuer",
        "renderer-issuer-token-role.json",
        "4a1052b4e888e5e0c5b025db7f6447f4719264343abc8f67e0c17fc3269e3a0f",
    ),
    (
        "renderer-cleanup",
        "renderer-cleanup-token-role.json",
        "bceb1e97853f173b5011f1af34033d01c07309e582137d0e67f85ae33b9eb17e",
    ),
)
APPROLE = (
    "hy-home-renderer",
    "renderer-role.json",
    "96f74c4b1908dd2edb3f7bbbf794bdd226b0a66f3133c103f64e1b7790218d79",
)
UNITS = {"s": 1, "m": 60, "h": 3600}
# A role update keeps any field it omits, so every other field a role read
# returns (2.6.2 and 2.7.1) is written at its default, except the AppRole's
# `local_secret_ids`, which is fixed when the role is created.
TOKEN_ROLE_DEFAULTS = {
    "allowed_entity_aliases": [],
    "allowed_policies_glob": [],
    "disallowed_policies": [],
    "disallowed_policies_glob": [],
    "path_suffix": "",
    "token_bound_cidrs": [],
    "token_num_uses": 0,
    "token_period": 0,
}
# Token role reads omit these two when empty (observed on 2.6.2 and 2.7.1), so an
# absent key is the cleared state and any leftover value still mismatches.
OMITTED_WHEN_EMPTY = {"token_bound_cidrs": [], "token_num_uses": 0}
APPROLE_DEFAULTS = {
    "secret_id_bound_cidrs": [],
    "token_bound_cidrs": [],
    "token_explicit_max_ttl": 0,
    "token_no_default_policy": False,
    "token_period": 0,
    "token_strictly_bind_ip": False,
    "token_type": "default",
}


def load_token_operations():
    """Compile only bytes matching the pinned hash; that module pins its own base."""
    path = Path(__file__).absolute().with_name("protected-token-operations.py")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or not 1 <= info.st_size <= 1048576
        ):
            raise ValueError()
        raw = os.read(descriptor, 1048577)
    finally:
        os.close(descriptor)
    if hashlib.sha256(raw).hexdigest() != TOKEN_OPERATIONS_SHA256:
        raise ValueError()
    module = types.ModuleType("approved_protected_token_operations")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    if module.BASE is None:
        raise ValueError()
    return module


try:
    OPS = load_token_operations()
    BASE = OPS.BASE
except (OSError, ValueError, AttributeError):
    OPS = BASE = None

Blocked = BASE.Blocked if BASE else ValueError
Indeterminate = BASE.Indeterminate if BASE else ValueError


def seconds(value):
    if isinstance(value, str) and value[:-1].isdigit() and value[-1:] in UNITS:
        return int(value[:-1]) * UNITS[value[-1]]
    return value


def expected_readback(payload, omitted=None):
    omitted = omitted or {}
    return {
        key: None if omitted.get(key, object()) == value else seconds(value)
        for key, value in payload.items()
    }


def targets(repository):
    """Held, hash-checked sources: ((path, document, readback), ...)."""
    config = Path(repository) / CONFIG
    result = []
    for name, source, digest in POLICIES:
        policy = OPS.read_public(config / source, digest).decode("ascii")
        result.append(("sys/policies/acl/" + name, {"policy": policy}, None))
    for name, source, digest in TOKEN_ROLES:
        payload = {
            **TOKEN_ROLE_DEFAULTS,
            **json.loads(OPS.read_public(config / source, digest)),
        }
        result.append(
            (
                "auth/token/roles/" + name,
                payload,
                expected_readback(payload, OMITTED_WHEN_EMPTY),
            )
        )
    name, source, digest = APPROLE
    payload = {
        **APPROLE_DEFAULTS,
        **json.loads(OPS.read_public(config / source, digest)),
    }
    result.append(("auth/approle/role/" + name, payload, expected_readback(payload)))
    return tuple(result)


class RoleCustody(BASE.Custody if BASE else object):
    def reserve(self, name):
        if name not in {
            ".lock",
            "operation-intent.json",
            "prior-state.json",
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


class RoleAPI:
    """Root identity; only the fixed target paths and their reviewed bodies."""

    def __init__(self, token, context, connect_ip, documents, *, write=True):
        self.token = BASE.validate_secret(token)
        self.context = context
        self.connect_ip = str(ipaddress.ip_address(connect_ip))
        self.documents = dict(documents)
        self.write = write

    def _check(self, method, path, document):
        if method == "GET" and (
            path in {BASE.LOOKUP, BASE.SEAL} or path in self.documents
        ):
            if document is not None:
                raise Blocked()
            return
        if (
            method == "POST"
            and self.write
            and path in self.documents
            and document == self.documents[path]
        ):
            return
        raise Blocked()

    def request(self, method, path, document=None):
        self._check(method, path, document)
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
                # Send the held reviewed body, not the caller's equal-comparing one.
                body=json.dumps(self.documents[path]) if method == "POST" else None,
                headers={
                    "X-Vault-Token": self.token,
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            if method == "GET" and path in self.documents and response.status == 404:
                return None
            if response.status not in ({200, 204} if method == "POST" else {200}):
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


def current(api, path, readback):
    """Comparable current value: policy text, or the reviewed keys of a role."""
    value = api.request("GET", path)
    if value is None:
        return None
    data = OPS.document(value).get("data")
    if not isinstance(data, dict):
        raise Blocked()
    if readback is None:
        return OPS.policy_value(value)
    return {key: data.get(key) for key in readback}


def wanted(document, readback):
    return document["policy"] if readback is None else readback


def digest(value):
    if value is None:
        return None
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def apply_roles(api, custody, cluster, plan, *, write=True):
    BASE.check_root(OPS.document(api.request("GET", BASE.LOOKUP)))
    BASE.check_seal(OPS.document(api.request("GET", BASE.SEAL)), cluster)
    prior = {path: current(api, path, readback) for path, _document, readback in plan}
    # The deployed Agent holds this AppRole's RoleID; creating a new role would
    # orphan it, so the role must already exist.
    if prior["auth/approle/role/" + APPROLE[0]] is None:
        raise Blocked()
    if not write:
        saved = custody.reserve("prior-state.json")
        custody.write(saved, prior)
        preview = [
            {
                "path": path,
                "prior_sha256": digest(prior[path]),
                "applied_sha256": digest(wanted(document, readback)),
                "changed": prior[path] != wanted(document, readback),
            }
            for path, document, readback in plan
        ]
        state = custody.reserve("state.json")
        custody.write(state, {"state": "RENDERER_ROLES_PLANNED", "targets": preview})
        return "RENDERER_ROLES_PLANNED"
    intent = custody.reserve("operation-intent.json")
    custody.write(
        intent,
        {
            "operation": "apply-renderer-roles",
            "token_operations_sha256": TOKEN_OPERATIONS_SHA256,
            "targets": [path for path, _document, _readback in plan],
        },
    )
    saved = custody.reserve("prior-state.json")
    custody.write(saved, prior)  # Durable rollback input before any write.
    custody.mutation_started = True
    try:
        receipt = []
        for path, document, readback in plan:
            api.request("POST", path, document)
            after = current(api, path, readback)
            if after != wanted(document, readback):
                raise Indeterminate()
            receipt.append(
                {
                    "path": path,
                    "prior_sha256": digest(prior[path]),
                    "applied_sha256": digest(after),
                    "changed": prior[path] != after,
                }
            )
        state = custody.reserve("state.json")
        custody.write(state, {"state": "RENDERER_ROLES_APPLIED", "targets": receipt})
        return "RENDERER_ROLES_APPLIED"
    except BaseException:
        raise Indeterminate() from None


def main(arguments=None):
    if BASE is None:
        print("BLOCKED: approved token operations binding unavailable", file=sys.stderr)
        return 1
    parser = BASE.PrivateArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("plan", "apply"))
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
    try:
        options = parser.parse_args(arguments)
        if options.root_fd < 3 or not BASE.UUID.fullmatch(options.expected_cluster_id):
            raise Blocked()
        ipaddress.ip_address(options.connect_ip)
        context = BASE.ca_context(options.ca, options.ca_sha256)
        plan = targets(Path(__file__).absolute().parents[4])
        OPS.distinct_directories(
            options.w1_custody_directory, options.custody_directory
        )
        with RoleCustody(options.custody_directory) as custody:
            token = OPS.root_input(options.root_fd, options.w1_custody_directory)
            api = RoleAPI(
                token,
                context,
                options.connect_ip,
                ((path, document) for path, document, _readback in plan),
                write=options.operation == "apply",
            )
            result = apply_roles(
                api,
                custody,
                options.expected_cluster_id,
                plan,
                write=options.operation == "apply",
            )
        try:
            print(result, flush=True)
        except OSError:
            raise Indeterminate() from None
        return 0
    except Indeterminate:
        print(
            "INDETERMINATE: preserve protected custody; never repeat a role write",
            file=sys.stderr,
        )
        return 2
    except (
        Blocked,
        OPS.BindingBlocked,
        OSError,
        ValueError,
        EOFError,
        KeyboardInterrupt,
    ):
        print(
            "BLOCKED: no completion claimed; preserve protected custody",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
