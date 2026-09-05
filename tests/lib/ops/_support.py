"""Shared constants for Compose readiness library and wrapper tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LIBRARY = ROOT / "scripts/lib/ops/compose-core-readiness.sh"
RUNNER = ROOT / "scripts/operations/check-compose-core-readiness.sh"
OVERRIDE = (
    ROOT
    / "examples/operations/compose-core-readiness/compose.core-runtime.override.yml"
)
EXPECTED_SERVICES = {
    "keycloak",
    "oauth2-proxy",
    "traefik",
    "vault",
    "vault-agent",
}
EXPECTED_PORTS = {"18000", "18443", "18082", "18083", "18200"}
EXPECTED_IMAGES = {
    "keycloak": (
        "quay.io/keycloak/keycloak@"
        "sha256:0aae0de7fca85525f727d3354df17896092de8bb26ae4c12d89c77e5df8cbce4"
    ),
    "oauth2-proxy": (
        "quay.io/oauth2-proxy/oauth2-proxy@"
        "sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561"
    ),
    "traefik": (
        "traefik@"
        "sha256:21a3d83696379bac6434bb32e1dde0aff0e84ef2abd053ed3db87d3f45e749b2"
    ),
    "vault": (
        "hashicorp/vault@"
        "sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54"
    ),
    "vault-agent": (
        "hashicorp/vault@"
        "sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54"
    ),
}
EXPECTED_CONFIG_DIGESTS = {
    "quay.io/keycloak/keycloak": (
        "sha256:1361d6e492058a69d979ab735cfc19e73e5f1e0a707e8fa5cfb610c00bc3cff2"
    ),
    "quay.io/oauth2-proxy/oauth2-proxy": (
        "sha256:cf3a5d50849b1799260d6aca62367c333b33472f208cbbdaab243a831b1a622f"
    ),
    "traefik": (
        "sha256:7982c57cc89de38c6ca9e3f17caa0569890d2043f6f5271c78ad75a2cff50f32"
    ),
    "hashicorp/vault": (
        "sha256:1747a4ab1e1bea8938269b23827165c5d80eecbdb5c115fd58e6380569537c84"
    ),
}
