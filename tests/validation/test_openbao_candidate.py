"""Exact candidate synthetic native security regression; no HOME evidence."""

import json
import os
import time
import unittest
from unittest.mock import patch

from . import test_openbao_rehearsal as openbao_rehearsal
from ._openbao_rehearsal_fixture import SOURCE, Client, OwnedFixture, RehearsalFailure

MANIFEST = "sha256:a36ea8c27f0dcff5757664ad080425f96d3b6b2f33db3e76c4e2d3112fb17005"
INVALID_CREDENTIAL = "invalid-synthetic-token"
REFERENCE = "openbao/openbao:2.7.1@" + MANIFEST


class ExpiryRegression(unittest.TestCase):
    def test_expiry_contract_rejects_unused_id(self):
        class DenyingClient:
            def api(self, method, path, payload=None):
                if method == "GET":
                    return 200, {"data": {"role_id": "synthetic-role"}}
                if path.endswith("/secret-id"):
                    return 200, {
                        "data": {
                            "secret_id": "synthetic-id",
                            "secret_id_accessor": "synthetic-accessor",
                        }
                    }
                if path == "auth/approle/login":
                    return 403, {}
                return 204, {}

        with patch("tests.validation.test_openbao_rehearsal.time.sleep"):
            openbao_rehearsal.OpenBaoRehearsalTests().expired_secret_id(DenyingClient())


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_CANDIDATE") == "1",
    "isolated candidate opt-in required",
)
class CandidateNative(unittest.TestCase):
    def test_tls_expiry_audit_and_snapshot(self):
        fixture = OwnedFixture(
            image=MANIFEST, version="2.7.1", image_reference=REFERENCE
        )
        try:
            fixture.prepare()
            server, client = fixture.server("candidate", active=True)
            shares = client.initialize()
            case = openbao_rehearsal.OpenBaoRehearsalTests()
            case.configure(client)
            case.expired_secret_id(client)
            self.verify_short_roles(case, client)
            self.assertGreaterEqual(
                client.api(
                    "GET",
                    "secret/data/auth/keycloak_admin_password",
                    token=INVALID_CREDENTIAL,
                )[0],
                400,
            )
            with self.assertRaises(RehearsalFailure):
                Client(client.target, fixture.wrong_ca).api("GET", "sys/health")
            snapshot = case.snapshot(client, fixture, server)
            _restored, restore = fixture.server("restore")
            foreign = restore.initialize()
            status, _ = restore.api(
                "POST", "sys/storage/raft/snapshot-force", snapshot, binary=True
            )
            self.assertIn(status, (200, 204))
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                if restore.api("GET", "sys/seal-status")[1].get("sealed"):
                    break
                time.sleep(0.25)
            for share in foreign[:2]:
                restore.api("POST", "sys/unseal", {"key": share})
            self.assertTrue(restore.api("GET", "sys/seal-status")[1].get("sealed"))
            restore.api("POST", "sys/unseal", {"reset": True})
            restore.token = client.token
            restore.unseal(shares)
            restore.wait_open()
            case.audit_failure(fixture, server, client)
        finally:
            fixture.cleanup()

    def verify_short_roles(self, case, client):
        for name in ("operator", "renderer-cleanup"):
            case.policy(client, name, SOURCE / "config/policies" / (name + ".hcl"))
        for name in ("renderer-issuer", "renderer-cleanup"):
            case.put(
                client,
                "auth/token/roles/" + name,
                json.loads(
                    (SOURCE / "config" / (name + "-token-role.json")).read_text()
                ),
            )
        status, operator = client.api(
            "POST",
            "auth/token/create",
            {
                "policies": ["operator"],
                "ttl": "5m",
                "renewable": False,
                "no_default_policy": True,
            },
        )
        self.assertEqual(status, 200)
        token = operator["auth"]["client_token"]
        self.assertEqual(
            client.api(
                "POST", "auth/approle/role/hy-home-renderer/secret-id", {}, token=token
            )[0],
            403,
        )
        for name in ("renderer-issuer", "renderer-cleanup"):
            status, issued = client.api(
                "POST",
                "auth/token/create/" + name,
                {
                    "policies": name,
                    "ttl": "5m",
                    "explicit_max_ttl": "5m",
                    "renewable": False,
                    "no_default_policy": True,
                },
                token=token,
            )
            self.assertEqual(status, 200)
            auth = issued["auth"]
            self.assertEqual(auth["policies"], [name])
            self.assertFalse(auth["renewable"])
            self.assertLessEqual(auth["lease_duration"], 300)
            limited = auth["client_token"]
            self.assertEqual(
                client.api(
                    "GET", "secret/data/hy-home/02-auth/keycloak", token=limited
                )[0],
                403,
            )
            self.assertEqual(
                client.api(
                    "POST",
                    "auth/approle/role/other/secret-id-accessor/destroy",
                    {"secret_id_accessor": "synthetic-other"},
                    token=limited,
                )[0],
                403,
            )
            self.assertGreaterEqual(
                client.api(
                    "POST",
                    "auth/token/create/" + name,
                    {"policies": ["root"]},
                    token=token,
                )[0],
                400,
            )
            self.assertGreaterEqual(
                client.api("POST", "auth/token/renew-self", {}, token=limited)[0], 400
            )
