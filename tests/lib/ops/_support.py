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
        "sha256:7e66a96e4739239070aeaf72e4c5decf0f7f682cfc725b9f7ea2b336eaba38b3"
    ),
    "oauth2-proxy": (
        "quay.io/oauth2-proxy/oauth2-proxy@"
        "sha256:10a1165743a192e1940b4708fb9647027185ce11a681a1c5519b442ff7f1f561"
    ),
    "traefik": (
        "traefik@"
        "sha256:63f61f603052fbcc77597da1dc71ed8c39cf3f3e5a7c92c73bc94d84973997c3"
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
        "sha256:4938c322f47d3736c580fc57bb335d35c784489bc7e6d8fbbd52dbdd1b27e72e"
    ),
    "quay.io/oauth2-proxy/oauth2-proxy": (
        "sha256:cf3a5d50849b1799260d6aca62367c333b33472f208cbbdaab243a831b1a622f"
    ),
    "traefik": (
        "sha256:01cfccdef2fd9144a75922dcc0dc71f6c76bb25244c709a709a4b5fa1a5c9c13"
    ),
    "hashicorp/vault": (
        "sha256:7a32cec814d1d2781ed5a2d3631254649039717be8084328e2b4374e147b6a3c"
    ),
}
