#!/usr/bin/env python3
"""Opt-in, owned synthetic OpenBao 2.6.2 rehearsal; never a HOME receipt.

Run only after reviewing the isolated boundary:
    HYHOME_OPENBAO_REHEARSAL=1 python3 -m unittest \
        tests.validation.test_openbao_rehearsal -v

Requires the exact cached image; never pulls. Secret values stay in memory or
invocation-owned mode-0600 files. Subprocess output, HTTP payloads and audit
content are captured privately and never become assertion messages.
"""

import hashlib
import json
import os
import re
import secrets
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

if __package__:
    from ._openbao_rehearsal_clients import OpenBaoClientCases
    from ._openbao_rehearsal_fixture import (
        ROOT,
        SOURCE,
        Client,
        OwnedFixture,
        RehearsalFailure,
        captured,
    )
else:
    from _openbao_rehearsal_clients import OpenBaoClientCases
    from _openbao_rehearsal_fixture import (
        ROOT,
        SOURCE,
        Client,
        OwnedFixture,
        RehearsalFailure,
        captured,
    )


class OpenBaoCleanupTests(unittest.TestCase):
    def test_failed_cleanup_still_attempts_every_owned_resource(self):
        for failure in (
            "helper-exit",
            "helper-create",
            "helper-wait",
            "stop",
            "remove",
        ):
            with self.subTest(failure=failure):
                fixture = object.__new__(OwnedFixture)
                fixture.containers = ["p01-owned-server"]
                fixture.volumes = ["p01-owned-volume"]
                fixture.network = "p01-owned-network"
                fixture.network_created = True
                fixture.directory = Path("/tmp/p01-owned-test-directory")
                calls = []

                def docker(*args, failure=failure, calls=calls, **kwargs):
                    calls.append(args)
                    stage = args[0]
                    if (
                        (failure == "helper-wait" and stage == "wait")
                        or (failure == "stop" and stage == "stop")
                        or (failure == "remove" and stage == "rm")
                    ):
                        raise RehearsalFailure("synthetic cleanup failure")
                    return SimpleNamespace(
                        returncode=0,
                        stdout=b"1"
                        if failure == "helper-exit" and stage == "wait"
                        else b"0",
                    )

                def container(*args, failure=failure, fixture=fixture, **kwargs):
                    if failure == "helper-create":
                        raise RehearsalFailure("synthetic helper creation failure")
                    fixture.containers.append("p01-owned-cleanup")
                    return "p01-owned-cleanup"

                with (
                    mock.patch.object(fixture, "docker", side_effect=docker),
                    mock.patch.object(fixture, "container", side_effect=container),
                    mock.patch.object(
                        __import__(OwnedFixture.__module__, fromlist=["shutil"]).shutil,
                        "rmtree",
                    ) as remove_directory,
                ):
                    with self.assertRaises(RehearsalFailure):
                        fixture.cleanup()
                    self.assertIn(("rm", "--force", "p01-owned-server"), calls)
                    self.assertIn(("volume", "rm", "p01-owned-volume"), calls)
                    self.assertIn(("network", "rm", "p01-owned-network"), calls)
                    remove_directory.assert_called_once_with(fixture.directory)


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_REHEARSAL") == "1",
    "isolated native rehearsal requires explicit opt-in",
)
class OpenBaoRehearsalTests(OpenBaoClientCases, unittest.TestCase):
    """Assertions expose only status/booleans, never payloads or credentials."""

    def must(self, condition, message):
        if not condition:
            raise RehearsalFailure(message)

    def put(self, client, path, data):
        self.must(
            client.api("POST", path, data)[0] in (200, 204),
            "synthetic setup write failed",
        )

    def policy(self, client, name, path):
        self.put(client, "sys/policies/acl/" + name, {"policy": path.read_text()})

    def wait_render(self, fixture, name, expected):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            result = fixture.docker(
                "exec",
                name,
                "sh",
                "/openbao/scripts/health-agent.sh",
                allow_failure=True,
            )
            if result.returncode == 0:
                paths = [
                    "/openbao/out/auth/keycloak_admin_password.txt",
                    "/openbao/out/observability/grafana_admin_password.txt",
                ]
                values = [
                    fixture.docker("exec", name, "cat", path).stdout.strip()
                    for path in paths
                ]
                version_paths = [
                    "/openbao/out/auth/keycloak_admin_password.version",
                    "/openbao/out/observability/grafana_admin_password.version",
                ]
                versions = [
                    fixture.docker("exec", name, "cat", path).stdout.strip()
                    for path in version_paths
                ]
                if all(value == expected.encode() for value in values) and versions == [
                    b"1",
                    b"1",
                ]:
                    return
            time.sleep(0.25)
        raise RehearsalFailure(
            "Agent failed functional render/readiness (details withheld)"
        )

    def insecure_render_mode(self, fixture, agent):
        paths = (
            "/openbao/agent/token",
            "/openbao/out/auth/keycloak_admin_password.txt",
            "/openbao/out/observability/grafana_admin_password.txt",
            "/openbao/out/auth/keycloak_admin_password.version",
            "/openbao/out/observability/grafana_admin_password.version",
        )
        for path in paths:
            fixture.docker("exec", agent, "chmod", "644", path)
            self.must(
                fixture.docker(
                    "exec",
                    agent,
                    "sh",
                    "/openbao/scripts/health-agent.sh",
                    allow_failure=True,
                ).returncode
                != 0,
                "Agent readiness accepted insecure render permissions",
            )
            fixture.docker("exec", agent, "chmod", "600", path)
        print(
            "observed Agent insecure token/value/version modes rejected: PASS",
            flush=True,
        )

    def wrapping(self, client, fixture, server, agent):
        status, role = client.api(
            "GET", "auth/approle/role/hy-home-renderer/role-id", token=self.issuer_token
        )
        self.must(status == 200, "renderer RoleID lookup failed")
        fixture.docker(
            "exec",
            "-i",
            server,
            "sh",
            "-ec",
            "umask 077; cat > /openbao/agent/role_id",
            data=role["data"]["role_id"].encode(),
        )
        result = captured(
            [
                "sh",
                str(SOURCE / "scripts/issue-renderer-secret-id.sh"),
                server,
                fixture.auth_volume,
                "openbao/openbao:2.6.2",
                agent,
            ],
            data=(self.issuer_token + "\n").encode(),
            allow_failure=True,
        )
        self.must(
            result.returncode == 0, "native limited-issuer wrapped delivery failed"
        )
        token = (
            fixture.docker("exec", server, "cat", "/openbao/agent/secret_id")
            .stdout.decode()
            .strip()
        )
        status, wrapped = client.api("POST", "sys/wrapping/lookup", {}, token=token)
        self.must(
            status == 200
            and wrapped.get("data", {}).get("creation_path")
            == "auth/approle/role/hy-home-renderer/secret-id",
            "wrapping creation path differs",
        )
        return token

    def input_digest(self):
        paths = [
            SOURCE / "docker-compose.yml",
            SOURCE / "config/agent.hcl",
            SOURCE / "config/renderer-role.json",
            Path(__file__).resolve(),
            ROOT / "tests/validation/_openbao_rehearsal_fixture.py",
            ROOT / "tests/validation/_openbao_rehearsal_clients.py",
            ROOT / "infra/09-platform-ops/restic/bin/hyhome-backup.sh",
            ROOT / "infra/06-observability/prometheus/config/prometheus.yml",
            ROOT / "infra/06-observability/prometheus/scripts/start.sh",
            ROOT / "infra/01-gateway/traefik/dynamic/tls.yaml",
            ROOT / "infra/06-observability/gatus/config/config.yaml",
            ROOT / "infra/06-observability/gatus/docker-entrypoint.sh",
            ROOT
            / "infra/06-observability/prometheus/config/alert_rules/alert_rules.openbao.yml",
            ROOT / "tests/validation/fixtures/openbao-audit-alerts.test.yml",
        ]
        paths += [
            SOURCE / "scripts" / name
            for name in (
                "start-server.sh",
                "start-agent.sh",
                "health-agent.sh",
                "issue-renderer-secret-id.sh",
                "check-tls-material.sh",
            )
        ]
        paths += [
            SOURCE / "config/policies" / (name + ".hcl")
            for name in ("renderer", "renderer-issuer", "prometheus", "backup-snapshot")
        ]
        paths += [
            SOURCE / "config/templates" / name
            for name in (
                "keycloak_admin_password.ctmpl",
                "grafana_admin_password.ctmpl",
                "keycloak_admin_password_version.ctmpl",
                "grafana_admin_password_version.ctmpl",
            )
        ]
        manifest = "".join(
            str(path.relative_to(ROOT))
            + " "
            + hashlib.sha256(path.read_bytes()).hexdigest()
            + "\n"
            for path in sorted(paths)
        )
        return hashlib.sha256(manifest.encode()).hexdigest()

    def test_native_trust_auth_audit_and_recovery(self):
        inputs = self.input_digest()
        print("observed rehearsal input SHA256: " + inputs, flush=True)
        fixture = OwnedFixture()
        try:
            fixture.prepare()
            self.temporal_alerts(fixture)
            server, client = fixture.server("server", active=True)
            self.must(
                client.api("GET", "sys/health")[0] == 501,
                "fresh Raft fixture is not uninitialized",
            )
            for ca, host in (
                (fixture.wrong_ca, "openbao"),
                (fixture.tls / "ca.pem", "wrong.invalid"),
            ):
                invalid = Client(client.target, ca, hostname=host)
                with self.assertRaises(RehearsalFailure):
                    invalid.api("GET", "sys/health")
            print("observed TLS CA/SAN rejection: PASS", flush=True)
            shares = client.initialize()
            print("observed synthetic init/unseal/leader: PASS", flush=True)
            self.must(
                client.api("GET", "sys/health")[0] == 200,
                "initialized fixture is not healthy",
            )
            for path in ("sys/generate-root/attempt", "sys/rekey/init"):
                status = client.api("POST", path, {}, token="")[0]
                self.must(
                    status >= 400,
                    "anonymous recovery endpoint "
                    + path
                    + " returned HTTP "
                    + str(status),
                )
            self.configure(client)
            marker = secrets.token_urlsafe(36)
            for target in ("02-auth/keycloak", "06-observability/grafana"):
                self.put(
                    client,
                    "secret/data/hy-home/" + target,
                    {"data": {"admin_password": marker}},
                )
            self.one_use_secret_id(client)
            self.roles(client, marker)
            self.expired_secret_id(client)
            self.expired_certificate(fixture)
            self.clients(fixture)
            print("observed limited/expired token cases: PASS", flush=True)
            agent = fixture.agent("agent", start=False)
            wrap = self.wrapping(client, fixture, server, agent)
            fixture.docker("start", agent)
            self.wait_render(fixture, agent, marker)
            self.must(
                fixture.docker(
                    "exec",
                    server,
                    "test",
                    "!",
                    "-e",
                    "/openbao/agent/secret_id",
                    allow_failure=True,
                ).returncode
                == 0,
                "wrapped SecretID file was retained",
            )
            self.must(
                client.api("POST", "sys/wrapping/unwrap", {}, token=wrap)[0] >= 400,
                "wrapping token replay was accepted",
            )
            fixture.stop(agent)
            self.must(
                fixture.docker("start", agent, allow_failure=True).returncode == 0,
                "Agent container restart command failed",
            )
            time.sleep(1)
            self.must(
                fixture.docker(
                    "exec",
                    agent,
                    "sh",
                    "/openbao/scripts/health-agent.sh",
                    allow_failure=True,
                ).returncode
                != 0,
                "old sink alone passed readiness after restart without reissue",
            )
            fixture.stop(agent)
            fresh = fixture.agent("cold-agent", start=False)
            self.wrapping(client, fixture, server, fresh)
            fixture.docker("start", fresh)
            self.wait_render(fixture, fresh, marker)
            self.insecure_render_mode(fixture, fresh)
            self.must(
                client.api("GET", "secret/metadata/hy-home/02-auth/keycloak")[1]
                .get("data", {})
                .get("current_version")
                == 1,
                "KV version is not independently observed",
            )
            print("observed Agent start/restart/fresh-process render: PASS", flush=True)
            snapshot = self.snapshot(client, fixture, server)
            print("observed existing snapshot renewal/save: PASS", flush=True)
            self.audit(fixture, server, marker, client.token)
            _restored, restore_client = fixture.server("restore")
            foreign_shares = restore_client.initialize()
            status, _ = restore_client.api(
                "POST", "sys/storage/raft/snapshot-force", snapshot, binary=True
            )
            self.must(status in (200, 204), "empty-environment snapshot restore failed")
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if restore_client.api("GET", "sys/seal-status")[1].get("sealed"):
                    break
                time.sleep(0.25)
            restore_client.token = client.token
            for share in foreign_shares[:2]:
                restore_client.api("POST", "sys/unseal", {"key": share})
            self.must(
                restore_client.api("GET", "sys/seal-status")[1].get("sealed") is True,
                "empty-environment keys incorrectly opened restored barrier",
            )
            restore_client.api("POST", "sys/unseal", {"reset": True})
            restore_client.unseal(shares)
            restore_client.wait_open()
            self.must(
                restore_client.api("GET", "secret/data/hy-home/02-auth/keycloak")[1]
                .get("data", {})
                .get("data", {})
                .get("admin_password")
                == marker,
                "restored KV does not match synthetic original",
            )
            print("observed empty Raft restore/original shares: PASS", flush=True)
            self.put(restore_client, "auth/token/revoke-self", {})
            self.must(
                restore_client.api("GET", "secret/data/hy-home/02-auth/keycloak")[0]
                == 403,
                "recovery root token remained valid after explicit revocation",
            )
            self.put(client, "sys/seal", {})
            self.must(
                client.api("GET", "sys/health")[0] == 503,
                "sealed fixture incorrectly reports healthy",
            )
            self.must(
                fixture.docker(
                    "exec",
                    fresh,
                    "sh",
                    "/openbao/scripts/health-agent.sh",
                    allow_failure=True,
                ).returncode
                != 0,
                "Agent readiness accepted a sealed endpoint",
            )
            client.unseal(shares)
            client.wait_open()
            self.audit_failure(fixture, server, client)
            self.must(
                self.input_digest() == inputs,
                "rehearsal source input changed during execution",
            )
        finally:
            fixture.cleanup()

    def one_use_secret_id(self, client):
        path = "auth/approle/role/hy-home-renderer"
        role_id = client.api("GET", path + "/role-id")[1]["data"]["role_id"]
        secret_id = client.api("POST", path + "/secret-id", {})[1]["data"]["secret_id"]
        payload = {"role_id": role_id, "secret_id": secret_id}
        status, login = client.api("POST", "auth/approle/login", payload)
        self.must(status == 200, "synthetic single-use renderer SecretID login failed")
        self.must(
            client.api("POST", "auth/approle/login", payload)[0] >= 400,
            "used renderer SecretID replay authenticated",
        )
        self.put(client, "auth/token/revoke", {"token": login["auth"]["client_token"]})

    def expired_secret_id(self, client):
        role = {
            **json.loads((SOURCE / "config/renderer-role.json").read_text()),
            "secret_id_ttl": "1s",
            "token_ttl": "30s",
            "token_max_ttl": "30s",
        }
        path = "auth/approle/role/p01-expiry"
        self.put(client, path, role)
        status, role_id = client.api("GET", path + "/role-id")
        self.must(status == 200, "expiry fixture RoleID unavailable")
        ids = [client.api("POST", path + "/secret-id", {})[1]["data"] for _ in range(2)]
        time.sleep(2)
        payload = {
            "role_id": role_id["data"]["role_id"],
            "secret_id": ids[0]["secret_id"],
        }
        status, accepted = client.api("POST", "auth/approle/login", payload)
        self.must(
            status == 200,
            "expected exact-2.6.2 upstream SecretID expiry behavior changed",
        )
        print(
            "KNOWN_UPSTREAM_RESIDUAL/P06_BLOCK: expired unused SecretID accepted by 2.6.2",
            flush=True,
        )
        self.put(
            client, "auth/token/revoke", {"token": accepted["auth"]["client_token"]}
        )
        self.put(
            client,
            path + "/secret-id-accessor/destroy",
            {"secret_id_accessor": ids[1]["secret_id_accessor"]},
        )
        self.must(
            client.api(
                "POST",
                "auth/approle/login",
                {
                    "role_id": role_id["data"]["role_id"],
                    "secret_id": ids[1]["secret_id"],
                },
            )[0]
            >= 400,
            "explicit destroyed SecretID still authenticated",
        )

    def configure(self, client):
        self.put(
            client, "sys/mounts/secret", {"type": "kv", "options": {"version": "2"}}
        )
        self.put(client, "sys/auth/approle", {"type": "approle"})
        for name in ("renderer", "renderer-issuer", "prometheus", "backup-snapshot"):
            self.policy(client, name, SOURCE / "config/policies" / (name + ".hcl"))
        self.put(
            client,
            "auth/approle/role/hy-home-renderer",
            json.loads((SOURCE / "config/renderer-role.json").read_text()),
        )
        status, issued = client.api(
            "POST",
            "auth/token/create",
            {
                "policies": ["renderer-issuer"],
                "ttl": "5m",
                "no_default_policy": True,
            },
        )
        self.must(status == 200, "dedicated issuer token creation failed")
        self.issuer_token = issued["auth"]["client_token"]
        for headers in ({}, {"X-Vault-Wrap-TTL": "120s"}):
            self.must(
                client.api(
                    "POST",
                    "auth/approle/role/hy-home-renderer/secret-id",
                    {},
                    token=self.issuer_token,
                    headers=headers,
                )[0]
                == 403,
                "limited issuer bypassed exact response-wrapping TTL",
            )
        self.must(
            client.api(
                "GET", "secret/data/hy-home/02-auth/keycloak", token=self.issuer_token
            )[0]
            == 403,
            "dedicated issuer token fetched a consumer secret",
        )

    def roles(self, client, marker):
        status, issued = client.api(
            "POST",
            "auth/token/create",
            {
                "policies": ["prometheus"],
                "ttl": "5m",
                "no_default_policy": True,
            },
        )
        self.must(status == 200, "metrics-only token issuance failed")
        token = issued["auth"]["client_token"]
        self.metrics_token = token
        metrics_status, metrics_body = client.api(
            "GET", "sys/metrics?format=prometheus", token=token, binary=True
        )
        self.must(metrics_status == 200, "metrics-only fetch failed")
        types = re.findall(
            r"^# TYPE (vault_audit_log_(?:request|response)_failure) (counter|gauge)$",
            metrics_body.decode(),
            re.M,
        )
        self.must(
            len(types) == 2 and all(kind == "counter" for _, kind in types),
            "audit failure metrics are not the observed two counters",
        )
        print(
            "observed audit failure metric types: "
            + ", ".join(name + "=" + kind for name, kind in types),
            flush=True,
        )
        names = set()
        for line in metrics_body.decode().splitlines():
            name = line.split("{", 1)[0].split(" ", 1)[0]
            if re.fullmatch(r"[a-zA-Z_:][a-zA-Z0-9_:]*", name) and "audit" in name:
                names.add(name)
        print("observed audit metric names: " + ", ".join(sorted(names)), flush=True)
        self.must(
            client.api("GET", "secret/data/hy-home/02-auth/keycloak", token=token)[0]
            == 403,
            "metrics token fetched a renderer secret",
        )
        self.must(
            client.api(
                "POST",
                "secret/data/hy-home/02-auth/keycloak",
                {"data": {"admin_password": marker}},
                token=token,
            )[0]
            == 403,
            "metrics token performed a secret write",
        )
        status, short = client.api(
            "POST", "auth/token/create", {"policies": ["renderer"], "ttl": "1s"}
        )
        self.must(status == 200, "short-lived synthetic token issuance failed")
        time.sleep(2)
        self.must(
            client.api(
                "GET",
                "secret/data/hy-home/02-auth/keycloak",
                token=short["auth"]["client_token"],
            )[0]
            == 403,
            "expired token fetched a secret",
        )

    def snapshot(self, client, fixture, server):
        status, issued = client.api(
            "POST",
            "auth/token/create",
            {
                "policies": ["backup-snapshot"],
                "period": "60s",
                "renewable": True,
            },
        )
        self.must(status == 200, "restricted periodic snapshot token issuance failed")
        token = issued["auth"]["client_token"]
        self.must(
            client.api("GET", "secret/data/hy-home/02-auth/keycloak", token=token)[0]
            == 403,
            "snapshot token fetched a renderer secret",
        )
        source = (
            ROOT / "infra/09-platform-ops/restic/bin/hyhome-backup.sh"
        ).read_text()
        snippet = re.search(r"'(BAO_TOKEN=\".*?cat /tmp/hyhome\.snap)'", source, re.S)
        self.must(snippet is not None, "existing backup renewal/save snippet missing")
        result = fixture.docker(
            "exec",
            "-i",
            server,
            "sh",
            "-ec",
            snippet.group(1),
            data=(token + "\n").encode(),
            allow_failure=True,
        )
        self.must(
            result.returncode == 0 and len(result.stdout) > 100,
            "existing restricted renewal/snapshot snippet failed",
        )
        return result.stdout

    def audit(self, fixture, server, marker, root_token):
        raw = fixture.docker("exec", server, "cat", "/openbao/audit/audit.json").stdout
        self.must(bool(raw) and b"hmac-sha256:" in raw, "audit HMAC evidence absent")
        self.must(
            marker.encode() not in raw and root_token.encode() not in raw,
            "audit includes a raw synthetic secret/token (output withheld)",
        )
        for line in raw.splitlines():
            try:
                json.loads(line)
            except ValueError:
                raise RehearsalFailure("audit output is not JSON lines") from None

    def audit_failure(self, fixture, server, client):
        fixture.docker(
            "exec",
            server,
            "sh",
            "-c",
            "dd if=/dev/zero of=/openbao/audit/owned-capacity-fill bs=4096 count=1024",
            allow_failure=True,
        )
        status = 0
        # Exhaust remaining bytes in the already allocated final audit-file page.
        # Stop at the first denial; a failed request is never retried or bypassed.
        for _ in range(16):
            status, _ = client.api("GET", "secret/data/hy-home/02-auth/keycloak")
            if status >= 500:
                break
        self.must(
            status >= 500, "all required audit devices failed without request denial"
        )
        self.must(
            client.api("GET", "sys/health")[0] == 200,
            "non-audited health distinction was not observed",
        )
        for path in ("sys/generate-root/attempt", "sys/rekey/init"):
            self.must(
                client.api("POST", path, {}, token="")[0] >= 400,
                "audit failure reopened unauthenticated recovery endpoints",
            )
        print(
            "observed full audit denial with health200: HTTP " + str(status), flush=True
        )
        # No audit-disable, retry bypass or successful post-failure request follows.


if __name__ == "__main__":
    unittest.main()
