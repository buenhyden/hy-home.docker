"""P02 gateway consumer validation for configurable provider listeners."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRAEFIK_MIDDLEWARE = ROOT / "infra/01-gateway/traefik/dynamic/middleware.yml"


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
