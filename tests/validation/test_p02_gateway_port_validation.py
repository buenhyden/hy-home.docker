"""P02 gateway consumer validation for configurable provider listeners."""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NGINX_VALIDATOR = ROOT / "infra/01-gateway/nginx/scripts/validate-upstream-ports.sh"
TRAEFIK_MIDDLEWARE = ROOT / "infra/01-gateway/traefik/dynamic/middleware.yml"


class NginxUpstreamPortValidationTests(unittest.TestCase):
    def test_compose_wires_validator_before_official_entrypoint(self) -> None:
        compose = yaml.safe_load(
            (ROOT / "infra/01-gateway/nginx/docker-compose.yml").read_text(
                encoding="utf-8"
            )
        )
        service = compose["services"]["nginx"]
        self.assertEqual(
            ["/bin/sh", "/usr/local/libexec/nginx/validate-upstream-ports.sh"],
            service["entrypoint"],
        )
        mount = next(
            item
            for item in service["volumes"]
            if not isinstance(item, dict) and "validate-upstream-ports.sh" in item
        )
        self.assertTrue(mount.endswith(":ro"))

    def test_malformed_upstream_port_is_rejected_before_entrypoint(self) -> None:
        malformed = ("", "0", "65536", "12x", "4180;id", "4180\n8080")
        for variable in ("OAUTH2_PROXY_PORT", "KEYCLOAK_PORT"):
            for value in malformed:
                with self.subTest(variable=variable, value=value):
                    environment = os.environ.copy()
                    environment.update(
                        {"OAUTH2_PROXY_PORT": "4180", "KEYCLOAK_PORT": "8080"}
                    )
                    environment[variable] = value
                    result = subprocess.run(
                        ["sh", str(NGINX_VALIDATOR)],
                        cwd=ROOT,
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=5,
                    )
                    self.assertEqual(64, result.returncode)
                    self.assertEqual("", result.stdout)
                    self.assertIn("invalid upstream port", result.stderr)


class TraefikUpstreamPortTemplateTests(unittest.TestCase):
    def test_template_uses_anchored_bounded_port_for_both_proxy_urls(self) -> None:
        source = TRAEFIK_MIDDLEWARE.read_text(encoding="utf-8")
        expression = (
            '{{- $p := env "OAUTH2_PROXY_PORT" -}}{{- if regexMatch '
            '"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|'
            '65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$" '
            '$p -}}{{ $p }}{{- else -}}{{ fail "invalid OAUTH2_PROXY_PORT" }}'
            "{{- end -}}"
        )
        self.assertEqual(2, source.count(expression))
        self.assertNotIn('oauth2-proxy:{{ env "OAUTH2_PROXY_PORT" }}', source)
        self.assertNotIn("oauth2-proxy:4180", source)


if __name__ == "__main__":
    unittest.main()
