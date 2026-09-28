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
        "sha256:82a77884f3af238beab1e7afd63b5f530e1b5c0590bd7aa60b40a40463e29b2c"
    ),
    "oauth2-proxy": (
        "quay.io/oauth2-proxy/oauth2-proxy@"
        "sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561"
    ),
    "traefik": (
        "traefik@"
        "sha256:24841fe2de7304c149343d877d2923b4c8800a38ba015dea9174c23b20e344a0"
    ),
    "vault": (
        "hashicorp/vault@"
        "sha256:47f14a6acb98f48d798a07df7c83f23a6e636e1cf724c5f8ff165cb32667a1e2"
    ),
    "vault-agent": (
        "hashicorp/vault@"
        "sha256:47f14a6acb98f48d798a07df7c83f23a6e636e1cf724c5f8ff165cb32667a1e2"
    ),
}
EXPECTED_CONFIG_DIGESTS = {
    "quay.io/keycloak/keycloak": (
        "sha256:b2f3e1b85071d17a1da8d2cbcc54707853d19c74ae027071789ea1bb12b3ec89"
    ),
    "quay.io/oauth2-proxy/oauth2-proxy": (
        "sha256:cf3a5d50849b1799260d6aca62367c333b33472f208cbbdaab243a831b1a622f"
    ),
    "traefik": (
        "sha256:f9309349d2c1477b15d04728f38882ba2e9a50b7f76729541121a7ee60d53490"
    ),
    "hashicorp/vault": (
        "sha256:7a32cec814d1d2781ed5a2d3631254649039717be8084328e2b4374e147b6a3c"
    ),
}
