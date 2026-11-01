"""Render the live Traefik routes the way the file provider does, with sample values."""

import re
from pathlib import Path

LIVE = Path(__file__).resolve().parents[5] / "01-gateway/traefik/dynamic"
ENV = re.compile(r'\{\{ env "([A-Z_]+)" \}\}')
# Deliberately unlike any real site, so a value left in a route fails the tests.
SAMPLE = {
    "DEFAULT_URL": "example.test",
    "HOST_LAN_BIND_IP": "10.0.0.13",
    "BLOG_EXPORT_RECEIVER_IP": "10.0.0.22",
}


def rendered(text):
    out = ENV.sub(lambda m: SAMPLE[m[1]], text)
    if "{{" in out:
        raise ValueError("template syntax other than env remains")
    return out
