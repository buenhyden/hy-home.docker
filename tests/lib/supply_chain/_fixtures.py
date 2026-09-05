"""Pure builders for supply-chain external contract variants."""

from __future__ import annotations

from typing import Any


SUBJECT_DIGEST = "sha256:" + "c" * 64
ARCHIVE_DIGEST = "sha256:" + "d" * 64
BUILD_CONTEXT_DIGEST = "sha256:" + "e" * 64
SOURCE_REVISION = "0123456789abcdef0123456789abcdef01234567"


def cyclonedx_report(
    *, image_config_digest: str = SUBJECT_DIGEST
) -> dict[str, Any]:
    return {
        "bomFormat": "CycloneDX",
        "components": [],
        "metadata": {
            "component": {
                "name": "examples/sample-web-service",
                "properties": [
                    {
                        "name": "org.hyhome.delivery.image_config_digest",
                        "value": image_config_digest,
                    },
                    {
                        "name": "org.hyhome.delivery.oci_archive_sha256",
                        "value": ARCHIVE_DIGEST,
                    },
                    {
                        "name": "org.hyhome.delivery.rehearsal.role",
                        "value": "candidate",
                    },
                ],
                "type": "container",
            },
            "timestamp": "2026-07-19T00:00:00Z",
            "tools": [{"name": "syft", "version": "v1.48.0"}],
        },
        "specVersion": "1.6",
        "version": 1,
    }


def grype_match(
    *,
    vulnerability_id: str = "CVE-2099-0001",
    severity: str = "High",
    package: str = "openssl-libs",
) -> dict[str, Any]:
    return {
        "artifact": {"name": package},
        "vulnerability": {"id": vulnerability_id, "severity": severity},
    }


def grype_report(
    *,
    matches: list[dict[str, Any]] | None = None,
    exception_id: str | None = None,
    exception: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "matches": list(matches or []),
        "schema_version": 1,
        "subject_digest": SUBJECT_DIGEST,
    }
    if exception_id is not None:
        report["exception_id"] = exception_id
    if exception is not None:
        report["exception"] = dict(exception)
    return report


def provenance_statement(
    *, archive_digest: str = ARCHIVE_DIGEST
) -> dict[str, Any]:
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "predicate": {
            "buildDefinition": {
                "externalParameters": {
                    "build_context_sha256": BUILD_CONTEXT_DIGEST,
                    "role": "candidate",
                    "source_revision": SOURCE_REVISION,
                },
                "resolvedDependencies": [
                    {
                        "digest": {"sha256": "e" * 64},
                        "uri": "git+local://examples/sample-web-service",
                    }
                ],
            },
            "runDetails": {
                "builder": {"id": "hyhome.local.supply-chain-wrapper"}
            },
        },
        "predicateType": "https://slsa.dev/provenance/v1",
        "subject": [
            {
                "digest": {"sha256": archive_digest.removeprefix("sha256:")},
                "name": "examples/sample-web-service",
            }
        ],
    }


def cosign_verification(
    *, verified: bool = True, archive_digest: str = ARCHIVE_DIGEST
) -> dict[str, Any]:
    return {
        "mode": "cosign-sign-blob",
        "oci_archive_sha256": archive_digest,
        "role": "candidate",
        "schema_version": 1,
        "verified": verified,
    }


def scorecard_report(
    *,
    repository: str = "github.com/buenhyden/hy-home.docker",
    ci_enforcement: str = "fixture-policy-only",
) -> dict[str, Any]:
    return {
        "ci_enforcement": ci_enforcement,
        "mode": "read-only-advisory",
        "observation": "read-only",
        "repository": repository,
        "schema_version": 1,
        "score": 7.3,
    }
