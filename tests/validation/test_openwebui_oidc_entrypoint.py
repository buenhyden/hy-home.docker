"""Open WebUI native OIDC entrypoint and Compose contract tests."""

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "infra/08-ai/open-webui/docker-compose.yml"
ENTRYPOINT = ROOT / "infra/08-ai/open-webui/docker-entrypoint.sh"


class OpenWebUiOidcComposeTests(unittest.TestCase):
    def test_service_uses_native_oidc_after_verified_cutover(self):
        service = yaml.safe_load(COMPOSE.read_text())["services"]["open-webui"]
        environment = service["environment"]

        self.assertEqual("home-openwebui", environment["OAUTH_CLIENT_ID"])
        self.assertEqual(
            "https://keycloak.${DEFAULT_URL}/realms/hy-home.realm/"
            ".well-known/openid-configuration",
            environment["OPENID_PROVIDER_URL"],
        )
        self.assertEqual(
            "https://chat.${DEFAULT_URL}/oauth/oidc/callback",
            environment["OPENID_REDIRECT_URI"],
        )
        self.assertEqual("S256", environment["OAUTH_CODE_CHALLENGE_METHOD"])
        self.assertEqual("Keycloak", environment["OAUTH_PROVIDER_NAME"])
        self.assertEqual("false", environment["ENABLE_OAUTH_PERSISTENT_CONFIG"])
        self.assertEqual("false", environment["ENABLE_OAUTH_SIGNUP"])
        self.assertEqual("false", environment["ENABLE_LOGIN_FORM"])
        self.assertEqual("false", environment["ENABLE_PASSWORD_AUTH"])
        self.assertEqual("false", environment["OAUTH_MERGE_ACCOUNTS_BY_EMAIL"])
        self.assertEqual("false", environment["ENABLE_OAUTH_ROLE_MANAGEMENT"])
        self.assertEqual("false", environment["ENABLE_OAUTH_GROUP_MANAGEMENT"])
        self.assertEqual("false", environment["ENABLE_OAUTH_GROUP_CREATION"])
        self.assertEqual("true", environment["WEBUI_AUTH_COOKIE_SECURE"])
        self.assertEqual("false", environment["ENABLE_OAUTH_ID_TOKEN_COOKIE"])
        self.assertNotIn("WEBUI_AUTH_TRUSTED_EMAIL_HEADER", environment)
        self.assertNotIn("WEBUI_AUTH_TRUSTED_NAME_HEADER", environment)
        self.assertNotIn("OAUTH_CLIENT_SECRET", environment)

        self.assertEqual(
            ["/usr/local/bin/open-webui-oidc-entrypoint.sh"], service["entrypoint"]
        )
        self.assertIn("openwebui_oidc_client_secret", service["secrets"])
        self.assertIn(
            "./docker-entrypoint.sh:/usr/local/bin/open-webui-oidc-entrypoint.sh:ro",
            service["volumes"],
        )
        self.assertIn(
            "${DEFAULT_CERT_DIR}/rootCA.pem:/etc/ssl/certs/hy-home-rootCA.pem:ro",
            service["volumes"],
        )
        self.assertEqual(
            "gateway-standard-chain@file",
            service["labels"]["traefik.http.routers.open-webui.middlewares"],
        )

    def test_hardening_accepts_native_contract_and_rejects_password_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (
                "scripts/hardening/check-all-hardening.sh",
                "scripts/lib/hardening-lib.sh",
                "infra/08-ai/ollama/docker-compose.yml",
                "infra/08-ai/open-webui/docker-compose.yml",
            ):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((ROOT / name).read_text())
            target = root / "infra/08-ai/open-webui/docker-compose.yml"
            original = target.read_text()
            for enabled in (False, True):
                target.write_text(
                    original.replace(
                        "ENABLE_PASSWORD_AUTH: 'false'",
                        "ENABLE_PASSWORD_AUTH: 'true'"
                        if enabled
                        else "ENABLE_PASSWORD_AUTH: 'false'",
                    )
                )
                environment = {
                    k: v for k, v in os.environ.items() if k != "HYHOME_CI_GATE_ROOT"
                }
                result = subprocess.run(
                    [
                        "bash",
                        str(root / "scripts/hardening/check-all-hardening.sh"),
                        "08-ai",
                    ],
                    cwd=root,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    not enabled, result.returncode == 0, result.stdout + result.stderr
                )


class OpenWebUiOidcEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.secret = self.root / "client-secret"
        self.root_ca = self.root / "root-ca.pem"
        self.public_ca = self.root / "public-ca.pem"
        self.result = self.root / "result.json"
        self.secret.write_text("synthetic-client-secret\n")
        self.root_ca.write_text("SYNTHETIC LOCAL ROOT CA CERTIFICATE\n")
        self.public_ca.write_text("SYNTHETIC PUBLIC TRUST\n")
        self.probe = self.root / "probe.py"
        self.probe.write_text(
            """import json
import os
import stat
import sys
from pathlib import Path

bundle = Path(os.environ["SSL_CERT_FILE"])
Path(sys.argv[1]).write_text(json.dumps({
    "secret": os.environ["OAUTH_CLIENT_SECRET"],
    "ssl": os.environ["SSL_CERT_FILE"],
    "requests": os.environ["REQUESTS_CA_BUNDLE"],
    "bundle": bundle.read_text(),
    "mode": stat.S_IMODE(bundle.stat().st_mode),
}))
"""
        )

    def run_entrypoint(self, **overrides):
        environment = os.environ.copy()
        environment.update(
            {
                "OPENWEBUI_OIDC_CLIENT_SECRET_FILE": str(self.secret),
                "OPENWEBUI_ROOT_CA_FILE": str(self.root_ca),
                "OPENWEBUI_PUBLIC_CA_FILE": str(self.public_ca),
                "TMPDIR": str(self.root),
            }
        )
        environment.update(overrides)
        result = subprocess.run(
            [
                "bash",
                str(ENTRYPOINT),
                sys.executable,
                str(self.probe),
                str(self.result),
            ],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("synthetic-client-secret", result.stdout + result.stderr)
        return result

    def test_loads_secret_and_combines_public_and_local_ca_before_exec(self):
        result = self.run_entrypoint()

        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(self.result.read_text())
        self.assertEqual("synthetic-client-secret", payload["secret"])
        self.assertEqual(payload["ssl"], payload["requests"])
        self.assertEqual(
            "SYNTHETIC PUBLIC TRUST\n\nSYNTHETIC LOCAL ROOT CA CERTIFICATE\n\n",
            payload["bundle"],
        )
        self.assertEqual(0o600, payload["mode"])

    def test_rejects_missing_empty_or_multiline_secret_before_exec(self):
        missing = self.root / "missing-secret"
        empty = self.root / "empty-secret"
        multiline = self.root / "multiline-secret"
        empty.write_bytes(b"")
        multiline.write_text("synthetic-client-secret\n\n")
        for secret in (missing, empty, multiline):
            with self.subTest(secret=secret.name):
                self.result.unlink(missing_ok=True)
                result = self.run_entrypoint(
                    OPENWEBUI_OIDC_CLIENT_SECRET_FILE=str(secret)
                )
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(self.result.exists())

    def test_rejects_missing_or_empty_ca_before_exec(self):
        empty_ca = self.root / "empty-ca.pem"
        empty_ca.write_bytes(b"")
        cases = (
            ("OPENWEBUI_ROOT_CA_FILE", self.root / "missing-root-ca.pem"),
            ("OPENWEBUI_ROOT_CA_FILE", empty_ca),
            ("OPENWEBUI_PUBLIC_CA_FILE", self.root / "missing-public-ca.pem"),
            ("OPENWEBUI_PUBLIC_CA_FILE", empty_ca),
        )
        for variable, ca_path in cases:
            with self.subTest(variable=variable, path=ca_path.name):
                self.result.unlink(missing_ok=True)
                result = self.run_entrypoint(**{variable: str(ca_path)})
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(self.result.exists())

    def test_repeated_start_keeps_one_atomic_ca_bundle(self):
        for _ in range(2):
            result = self.run_entrypoint()
            self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            ["open-webui-ca-bundle.pem"],
            sorted(path.name for path in self.root.glob("open-webui-ca*")),
        )

    def test_script_is_executable_and_not_group_or_world_writable(self):
        mode = stat.S_IMODE(ENTRYPOINT.stat().st_mode)
        self.assertEqual(0, mode & 0o022)
        self.assertTrue(mode & stat.S_IXUSR)


if __name__ == "__main__":
    unittest.main()
