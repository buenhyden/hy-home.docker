"""Gatus native OIDC hardening, secret delivery, and Compose contract tests."""

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
GATUS = ROOT / "infra/06-observability/gatus"
COMPOSE = ROOT / "infra/06-observability/docker-compose.yml"
CONFIG = GATUS / "config/config.oidc.yaml"
DOCKERFILE = GATUS / "Dockerfile"
ENTRYPOINT = GATUS / "docker-entrypoint.sh"
PATCH = GATUS / "patches/oidc-hardening.patch"
UPSTREAM_COMMIT = "ed1107b41a30e22047eecfb6dbc3be5e39829d5a"
UPSTREAM_SHA256 = "5638de42703fc6a936b9820920c3e07d1b1e017f1aabea94808155ed9953433a"


class GatusOidcComposeTests(unittest.TestCase):
    def test_service_selects_native_oidc_after_verified_cutover(self):
        service = yaml.safe_load(COMPOSE.read_text())["services"]["gatus"]
        environment = service["environment"]

        self.assertEqual("${DEFAULT_URL}", environment["DEFAULT_URL"])
        self.assertEqual(
            "${GATUS_OIDC_ALLOWED_SUBJECT}",
            environment["GATUS_OIDC_ALLOWED_SUBJECT"],
        )
        self.assertEqual(
            "/run/secrets/gatus_oidc_client_secret",
            environment["GATUS_OIDC_CLIENT_SECRET_FILE"],
        )
        self.assertNotIn("GATUS_OIDC_CLIENT_SECRET", environment)
        self.assertIn("gatus_oidc_client_secret", service["secrets"])
        self.assertIn(
            "${DEFAULT_CERT_DIR}/rootCA.pem:/etc/ssl/certs/hy-home-rootCA.pem:ro",
            service["volumes"],
        )
        self.assertIn(
            "./gatus/config/config.oidc.yaml:/config/config.yaml:ro",
            service["volumes"],
        )
        self.assertEqual(
            "gateway-standard-chain@file",
            service["labels"]["traefik.http.routers.gatus.middlewares"],
        )
        self.assertEqual(
            "Host(`status.${DEFAULT_URL}`) && !PathPrefix(`/metrics`)",
            service["labels"]["traefik.http.routers.gatus.rule"],
        )

    def test_diff_artifacts_keep_context_whitespace_without_skipping_other_hooks(self):
        config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        hooks = [hook for repo in config["repos"] for hook in repo["hooks"]]
        for hook in hooks:
            if hook["id"] == "trailing-whitespace":
                self.assertIn("diff", hook.get("exclude_types", []))
            else:
                self.assertNotIn("diff", hook.get("exclude_types", []))
        self.assertNotIn("diff", config.get("exclude_types", []))

    def test_native_oidc_configuration_is_exact_and_fail_closed(self):
        oidc = yaml.safe_load(CONFIG.read_text())["security"]["oidc"]

        self.assertEqual(
            "https://keycloak.${DEFAULT_URL}/realms/hy-home.realm",
            oidc["issuer-url"],
        )
        self.assertEqual(
            "https://status.${DEFAULT_URL}/authorization-code/callback",
            oidc["redirect-url"],
        )
        self.assertEqual("home-gatus", oidc["client-id"])
        self.assertEqual("${GATUS_OIDC_CLIENT_SECRET}", oidc["client-secret"])
        self.assertEqual(["openid"], oidc["scopes"])
        self.assertEqual(["${GATUS_OIDC_ALLOWED_SUBJECT}"], oidc["allowed-subjects"])
        self.assertEqual("1h", oidc["session-ttl"])


class GatusOidcEntrypointTests(unittest.TestCase):
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
    "secret": os.environ["GATUS_OIDC_CLIENT_SECRET"],
    "bundle": bundle.read_text(),
    "mode": stat.S_IMODE(bundle.stat().st_mode),
}))
"""
        )

    def run_entrypoint(self, **overrides):
        environment = os.environ.copy()
        environment.update(
            {
                "GATUS_OIDC_CLIENT_SECRET_FILE": str(self.secret),
                "GATUS_ROOT_CA_FILE": str(self.root_ca),
                "GATUS_PUBLIC_CA_FILE": str(self.public_ca),
                "DEFAULT_URL": "example.test",
                "GATUS_OIDC_ALLOWED_SUBJECT": "synthetic-subject",
                "TMPDIR": str(self.root),
            }
        )
        environment.update(overrides)
        result = subprocess.run(
            ["sh", str(ENTRYPOINT), sys.executable, str(self.probe), str(self.result)],
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
        self.assertEqual(
            "SYNTHETIC PUBLIC TRUST\n\nSYNTHETIC LOCAL ROOT CA CERTIFICATE\n\n",
            payload["bundle"],
        )
        self.assertEqual(0o600, payload["mode"])

    def test_reuses_single_ca_bundle_path_across_container_restarts(self):
        first = self.run_entrypoint()
        second = self.run_entrypoint()

        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(0, second.returncode, second.stderr)
        self.assertEqual(
            [self.root / "gatus-ca-bundle.pem"],
            list(self.root.glob("gatus-ca*")),
        )

    def test_rejects_missing_or_empty_secret_before_exec(self):
        empty = self.root / "empty-secret"
        empty.write_bytes(b"")
        for secret in (self.root / "missing-secret", empty):
            with self.subTest(secret=secret.name):
                self.result.unlink(missing_ok=True)
                result = self.run_entrypoint(GATUS_OIDC_CLIENT_SECRET_FILE=str(secret))
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(self.result.exists())

    def test_rejects_missing_or_empty_ca_before_exec(self):
        empty = self.root / "empty-ca.pem"
        empty.write_bytes(b"")
        cases = (
            ("GATUS_ROOT_CA_FILE", self.root / "missing-root-ca.pem"),
            ("GATUS_ROOT_CA_FILE", empty),
            ("GATUS_PUBLIC_CA_FILE", self.root / "missing-public-ca.pem"),
            ("GATUS_PUBLIC_CA_FILE", empty),
        )
        for variable, path in cases:
            with self.subTest(variable=variable, path=path.name):
                self.result.unlink(missing_ok=True)
                result = self.run_entrypoint(**{variable: str(path)})
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(self.result.exists())

    def test_rejects_missing_identity_configuration_before_exec(self):
        for variable in ("DEFAULT_URL", "GATUS_OIDC_ALLOWED_SUBJECT"):
            with self.subTest(variable=variable):
                self.result.unlink(missing_ok=True)
                result = self.run_entrypoint(**{variable: ""})
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(self.result.exists())

    def test_script_is_not_group_or_world_writable(self):
        self.assertEqual(0, stat.S_IMODE(ENTRYPOINT.stat().st_mode) & 0o022)


class GatusOidcSourceHardeningTests(unittest.TestCase):
    def test_build_pins_verified_upstream_and_runs_security_tests(self):
        dockerfile = DOCKERFILE.read_text()

        self.assertIn(UPSTREAM_COMMIT, dockerfile)
        self.assertIn(UPSTREAM_SHA256, dockerfile)
        self.assertIn("sha256sum -c -", dockerfile)
        self.assertIn("patch --batch --forward --fuzz=0", dockerfile)
        self.assertIn("go mod tidy -diff", dockerfile)
        self.assertIn("go test ./api ./security", dockerfile)

    def test_patch_enforces_cookie_pkce_and_one_time_cookie_contracts(self):
        patch = PATCH.read_text()

        self.assertGreaterEqual(patch.count("Secure:   true"), 4)
        self.assertGreaterEqual(patch.count("HTTPOnly: true"), 3)
        self.assertGreaterEqual(patch.count("HttpOnly: true"), 2)
        self.assertIn("oauth2.S256ChallengeOption", patch)
        self.assertIn("oauth2.VerifierOption", patch)
        self.assertIn("cookieNamePKCEVerifier", patch)
        self.assertIn("clearOIDCCookies", patch)
        self.assertIn("TestOIDCConfig_loginHandlerUsesSecureCookiesAndPKCE", patch)
        self.assertIn("TestOIDCConfig_callbackRejectsMissingPKCEVerifier", patch)
        self.assertIn("TestOIDCConfig_validateOIDCCookie", patch)
        self.assertIn("TestOIDCConfig_isSubjectAllowedUsesExactMatch", patch)
        self.assertIn("if allowedSubject == tokenSubject", patch)

    def test_patch_native_protects_status_data_and_preserves_bootstrap_routes(self):
        patch = PATCH.read_text()
        protected_routes = (
            "/v1/endpoints/:key/health/badge.svg",
            "/v1/endpoints/:key/health/badge.shields",
            "/v1/endpoints/:key/uptimes/:duration",
            "/v1/endpoints/:key/uptimes/:duration/badge.svg",
            "/v1/endpoints/:key/response-times/:duration",
            "/v1/endpoints/:key/response-times/:duration/badge.svg",
            "/v1/endpoints/:key/response-times/:duration/chart.svg",
            "/v1/endpoints/:key/response-times/:duration/history",
        )
        for route in protected_routes:
            with self.subTest(route=route):
                self.assertIn(
                    f'+\tprotectedAPIRouter.Get("{route}"',
                    patch,
                )

        self.assertIn("metrics-remains-public-for-internal-scrape", patch)
        self.assertIn("health-remains-public-for-container-probe", patch)
        self.assertIn("external-result-keeps-bearer-token-boundary", patch)
        self.assertIn("mayExposeAnnouncements := !hasOIDC || isAuthenticated", patch)
        self.assertIn(
            "TestConfigHandler_HidesAnnouncementsBeforeOIDCAuthentication",
            patch,
        )


if __name__ == "__main__":
    unittest.main()
