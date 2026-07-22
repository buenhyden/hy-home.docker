#!/usr/bin/env python3
"""Validate the deterministic, redacted local supply-chain fixture contract."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import tarfile
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/supply-chain"
TOOL_REGISTRY_PATH = ROOT / "infra/supply-chain.tool-images.json"
POLICY_PATH = ROOT / "infra/supply-chain.sample-service-policy.json"
EXCEPTIONS_PATH = ROOT / "infra/supply-chain.vulnerability-exceptions.json"
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SCORECARD_REPOSITORY = "github.com/buenhyden/hy-home.docker"
TOOL_PINS = {
    "syft": (
        "anchore/syft:v1.48.0",
        "sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c",
        "v1.48.0",
    ),
    "grype": (
        "anchore/grype:v0.116.0",
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821",
        "v0.116.0",
    ),
    "cosign": (
        "gcr.io/projectsigstore/cosign:v3.0.6",
        "sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00",
        "v3.0.6",
    ),
    "scorecard": (
        "ghcr.io/ossf/scorecard:v5.5.0",
        "sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795",
        "v5.5.0",
    ),
}


def load_json(path: pathlib.Path | str) -> Any:
    with pathlib.Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_date(value: Any) -> bool:
    if not _is_text(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _exception_errors(exception: Any) -> list[str]:
    if not isinstance(exception, dict):
        return ["exception-row-invalid"]
    required = (
        "id",
        "subject_digest",
        "package",
        "vulnerability_id",
        "severity",
        "owner_role",
        "reason",
        "expires_on",
        "compensating_control",
        "approval_reference",
    )
    errors = ["exception-field-missing" for key in required if not _is_text(exception.get(key))]
    if not SHA256_RE.fullmatch(str(exception.get("subject_digest", ""))):
        errors.append("exception-subject-digest-invalid")
    if not _is_text(exception.get("owner_role")):
        errors.append("exception-owner-invalid")
    if not _is_text(exception.get("approval_reference")):
        errors.append("exception-approval-invalid")
    if not _valid_date(exception.get("expires_on")):
        errors.append("exception-expiry-invalid")
    elif dt.date.fromisoformat(exception["expires_on"]) < dt.date.today():
        errors.append("exception-expired")
    return sorted(set(errors))


def validate_tool_registry(registry: Any) -> list[str]:
    if not isinstance(registry, dict):
        return ["tool-registry-invalid"]
    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("tool-schema-version-invalid")
    for field in ("policy_id", "effective_date", "owner_role"):
        if not _is_text(registry.get(field)):
            errors.append(f"tool-registry-{field}-invalid")
    if not _valid_date(registry.get("effective_date")):
        errors.append("tool-registry-effective-date-invalid")
    tools = registry.get("tools")
    if not isinstance(tools, list) or len(tools) != len(TOOL_PINS):
        return sorted(set(errors + ["tool-registry-tool-set-invalid"]))
    by_name = {row.get("name"): row for row in tools if isinstance(row, dict)}
    if set(by_name) != set(TOOL_PINS):
        errors.append("tool-registry-tool-set-invalid")
    for name, expected in TOOL_PINS.items():
        row = by_name.get(name)
        if not isinstance(row, dict):
            continue
        image, digest, version = expected
        if row.get("image") != image:
            errors.append("tool-image-pin-invalid")
        if row.get("digest") != digest or not SHA256_RE.fullmatch(str(row.get("digest", ""))):
            errors.append("tool-digest-invalid")
        if row.get("expected_version") != version:
            errors.append("tool-version-invalid")
        for field in ("command_contract", "network_mode"):
            if not _is_text(row.get(field)):
                errors.append(f"tool-{field}-invalid")
    return sorted(set(errors))


def validate_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["policy-invalid"]
    errors: list[str] = []
    if policy.get("schema_version") != 1:
        errors.append("policy-schema-version-invalid")
    if policy.get("policy_id") != "sample-service-local-v1":
        errors.append("policy-id-invalid")
    subject = policy.get("subject")
    if not isinstance(subject, dict) or subject.get("service") != "examples/sample-web-service":
        errors.append("policy-subject-service-invalid")
    elif subject.get("roles") != ["baseline", "candidate"]:
        errors.append("policy-subject-roles-invalid")
    if policy.get("sbom") != {"format": "cyclonedx-json"}:
        errors.append("policy-sbom-invalid")
    vulnerability = policy.get("vulnerability")
    if not isinstance(vulnerability, dict):
        errors.append("policy-vulnerability-invalid")
    else:
        if vulnerability.get("blocking_severities") != ["critical"]:
            errors.append("policy-blocking-severities-invalid")
        if vulnerability.get("review_severities") != ["high"]:
            errors.append("policy-review-severities-invalid")
        if vulnerability.get("exception_registry") != "infra/supply-chain.vulnerability-exceptions.json":
            errors.append("policy-exception-registry-invalid")
    if policy.get("provenance") != {"predicate_type": "https://slsa.dev/provenance/v1"}:
        errors.append("policy-provenance-invalid")
    if policy.get("signature") != {"mode": "cosign-sign-blob", "key_lifetime": "process"}:
        errors.append("policy-signature-invalid")
    if policy.get("scorecard") != {"mode": "read-only-advisory"}:
        errors.append("policy-scorecard-invalid")
    if policy.get("ci_enforcement") != "fixture-policy-only":
        errors.append("policy-ci-enforcement-invalid")
    return sorted(set(errors))


def validate_exceptions(
    registry: Any, policy: Any, expected_subject_digest: str | None = None
) -> list[str]:
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        return ["exception-registry-invalid"]
    if validate_policy(policy):
        return ["exception-policy-invalid"]
    rows = registry.get("exceptions")
    if not isinstance(rows, list):
        return ["exception-rows-invalid"]
    errors: list[str] = []
    ids: set[str] = set()
    for row in rows:
        errors.extend(_exception_errors(row))
        if isinstance(row, dict):
            identifier = row.get("id")
            if identifier in ids:
                errors.append("exception-id-duplicate")
            if isinstance(identifier, str):
                ids.add(identifier)
    if expected_subject_digest is not None and not SHA256_RE.fullmatch(expected_subject_digest):
        errors.append("exception-expected-subject-invalid")
    return sorted(set(errors))


def validate_subject_tuples(subjects: Any) -> list[str]:
    if not isinstance(subjects, list) or len(subjects) != 2:
        return ["subject-tuples-cardinality-invalid"]
    errors: list[str] = []
    roles: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    revisions: set[str] = set()
    for subject in subjects:
        if not isinstance(subject, dict):
            errors.append("subject-tuple-invalid")
            continue
        role = subject.get("role")
        image = subject.get("image_config_digest")
        archive = subject.get("oci_archive_sha256")
        revision = subject.get("source_revision")
        if role not in {"baseline", "candidate"}:
            errors.append("subject-role-invalid")
        else:
            roles.add(role)
        if not SHA256_RE.fullmatch(str(image)):
            errors.append("subject-image-config-digest-invalid")
        if not SHA256_RE.fullmatch(str(archive)):
            errors.append("subject-oci-archive-digest-invalid")
        if not SHA1_RE.fullmatch(str(revision)):
            errors.append("subject-source-revision-invalid")
        else:
            revisions.add(revision)
        pairs.add((str(image), str(archive)))
    if roles != {"baseline", "candidate"}:
        errors.append("subject-roles-invalid")
    if len(pairs) != 2:
        errors.append("subject-tuples-not-distinct")
    if len(revisions) != 1:
        errors.append("subject-source-revision-mismatch")
    return sorted(set(errors))


def _properties(component: Any) -> dict[str, Any]:
    if not isinstance(component, dict):
        return {}
    rows = component.get("properties")
    if not isinstance(rows, list):
        return {}
    return {
        row.get("name"): row.get("value")
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("name"), str)
    }


def inspect_oci_archive_config_digest(archive_path: pathlib.Path | str) -> str:
    """Return the config digest cryptographically bound by an OCI archive index."""

    def read_member(archive: tarfile.TarFile, name: str, reason: str) -> bytes:
        try:
            member = archive.getmember(name)
        except KeyError as exc:
            raise ValueError(reason) from exc
        handle = archive.extractfile(member)
        if handle is None:
            raise ValueError(reason)
        return handle.read()

    def require_digest(value: Any, reason: str) -> str:
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            raise ValueError(reason)
        return value

    def parse_json(content: bytes, reason: str) -> dict[str, Any]:
        try:
            value = json.loads(content)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(reason) from exc
        if not isinstance(value, dict):
            raise ValueError(reason)
        return value

    try:
        archive = tarfile.open(archive_path, "r:*")
    except (OSError, tarfile.TarError) as exc:
        raise ValueError("oci-archive-invalid") from exc
    with archive:
        index = parse_json(read_member(archive, "index.json", "oci-index-missing"), "oci-index-invalid")
        manifests = index.get("manifests")
        if not isinstance(manifests, list) or len(manifests) != 1 or not isinstance(manifests[0], dict):
            raise ValueError("oci-index-manifest-cardinality-invalid")
        manifest_digest = require_digest(manifests[0].get("digest"), "oci-index-manifest-digest-invalid")
        manifest_blob = read_member(
            archive,
            f"blobs/sha256/{manifest_digest.removeprefix('sha256:')}",
            "oci-manifest-blob-missing",
        )
        if hashlib.sha256(manifest_blob).hexdigest() != manifest_digest.removeprefix("sha256:"):
            raise ValueError("oci-manifest-blob-digest-mismatch")
        manifest = parse_json(manifest_blob, "oci-manifest-invalid")
        config = manifest.get("config")
        if not isinstance(config, dict):
            raise ValueError("oci-manifest-config-invalid")
        config_digest = require_digest(config.get("digest"), "oci-config-digest-invalid")
        config_blob = read_member(
            archive,
            f"blobs/sha256/{config_digest.removeprefix('sha256:')}",
            "oci-config-blob-missing",
        )
        if hashlib.sha256(config_blob).hexdigest() != config_digest.removeprefix("sha256:"):
            raise ValueError("oci-config-blob-digest-mismatch")
    return config_digest


def validate_sbom_subject(sbom: Any, subject: Any) -> list[str]:
    if not isinstance(sbom, dict) or not isinstance(subject, dict):
        return ["sbom-subject-invalid"]
    errors: list[str] = []
    if sbom.get("bomFormat") != "CycloneDX" or not _is_text(sbom.get("specVersion")):
        errors.append("sbom-format-invalid")
    component = (sbom.get("metadata") or {}).get("component") if isinstance(sbom.get("metadata"), dict) else None
    if not isinstance(component, dict) or component.get("name") != "examples/sample-web-service":
        errors.append("sbom-component-invalid")
        return errors
    properties = _properties(component)
    if properties.get("org.hyhome.delivery.image_config_digest") != subject.get("image_config_digest"):
        errors.append("sbom-image-config-subject-mismatch")
    if properties.get("org.hyhome.delivery.oci_archive_sha256") != subject.get("oci_archive_sha256"):
        errors.append("sbom-oci-archive-subject-mismatch")
    if properties.get("org.hyhome.delivery.rehearsal.role") != subject.get("role"):
        errors.append("sbom-role-subject-mismatch")
    return sorted(set(errors))


def _find_exception(
    fixture: dict[str, Any], registry: dict[str, Any], match: dict[str, str], subject_digest: str
) -> tuple[dict[str, Any] | None, str | None]:
    embedded = fixture.get("exception")
    if isinstance(embedded, dict):
        if (
            embedded.get("subject_digest") == subject_digest
            and embedded.get("package") == match["package"]
            and embedded.get("vulnerability_id") == match["vulnerability_id"]
            and str(embedded.get("severity", "")).lower() == match["severity"]
        ):
            return embedded, embedded.get("id") if isinstance(embedded.get("id"), str) else None
        return None, None
    requested_id = fixture.get("exception_id")
    if not isinstance(requested_id, str) or not requested_id:
        return None, None
    rows = registry.get("exceptions") if isinstance(registry.get("exceptions"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if requested_id and row.get("id") != requested_id:
            continue
        if (
            row.get("subject_digest") == subject_digest
            and row.get("package") == match["package"]
            and row.get("vulnerability_id") == match["vulnerability_id"]
            and str(row.get("severity", "")).lower() == match["severity"]
        ):
            return row, row.get("id") if isinstance(row.get("id"), str) else None
    return None, None


def evaluate_grype_fixture(
    fixture: Any, policy: Any, registry: Any, subject: Any
) -> dict[str, str | None]:
    if not isinstance(fixture, dict) or not isinstance(policy, dict) or not isinstance(registry, dict) or not isinstance(subject, dict):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-fixture-invalid"}
    if fixture.get("schema_version") != 1 or fixture.get("subject_digest") != subject.get("image_config_digest"):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-subject-mismatch"}
    matches = fixture.get("matches")
    if not isinstance(matches, list):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-matches-invalid"}
    if not matches:
        return {"verdict": "accepted", "exception_id": None, "reason": "clean"}
    vulnerability = policy.get("vulnerability", {})
    blocking = set(vulnerability.get("blocking_severities", []))
    review = set(vulnerability.get("review_severities", []))
    approved_exception_ids: list[str] = []
    has_outside_policy_match = False
    for match in matches:
        if not isinstance(match, dict):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-match-invalid"}
        artifact = match.get("artifact")
        finding = match.get("vulnerability")
        if not isinstance(artifact, dict) or not isinstance(finding, dict):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-match-invalid"}
        if any(key in finding for key in ("description", "urls", "locations", "relatedVulnerabilities")):
            return {"verdict": "rejected", "exception_id": None, "reason": "raw-finding-leakage"}
        severity = str(finding.get("severity", "")).lower()
        finding_key = {
            "package": str(artifact.get("name", "")),
            "vulnerability_id": str(finding.get("id", "")),
            "severity": severity,
        }
        if not all(finding_key.values()):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-finding-invalid"}
        exception, exception_id = _find_exception(
            fixture, registry, finding_key, str(subject.get("image_config_digest", ""))
        )
        if exception is not None:
            exception_errors = _exception_errors(exception)
            if "exception-expired" in exception_errors:
                return {"verdict": "rejected", "exception_id": exception_id, "reason": "exception-expired"}
            if exception_errors:
                return {"verdict": "rejected", "exception_id": exception_id, "reason": exception_errors[0]}
            if severity in blocking or severity in review:
                if exception_id is None:
                    return {"verdict": "rejected", "exception_id": None, "reason": "exception-id-invalid"}
                approved_exception_ids.append(exception_id)
            continue
        if severity in blocking:
            return {"verdict": "rejected", "exception_id": None, "reason": "blocking-finding-without-exception"}
        if severity in review:
            return {"verdict": "rejected", "exception_id": None, "reason": "review-finding-without-exception"}
        has_outside_policy_match = True
    if approved_exception_ids:
        unique_ids = sorted(set(approved_exception_ids))
        return {
            "verdict": "accepted",
            "exception_id": unique_ids[0] if len(unique_ids) == 1 else None,
            "reason": "all-policy-findings-exception-approved",
        }
    return {"verdict": "accepted", "exception_id": None, "reason": "outside-policy" if has_outside_policy_match else "clean"}


def validate_provenance_subject(provenance: Any, subject: Any) -> list[str]:
    if not isinstance(provenance, dict) or not isinstance(subject, dict):
        return ["provenance-invalid"]
    errors: list[str] = []
    if provenance.get("_type") != "https://in-toto.io/Statement/v1":
        errors.append("provenance-statement-type-invalid")
    if provenance.get("predicateType") != "https://slsa.dev/provenance/v1":
        errors.append("provenance-predicate-type-invalid")
    subjects = provenance.get("subject")
    expected_sha = str(subject.get("oci_archive_sha256", "")).removeprefix("sha256:")
    if not isinstance(subjects, list) or not any(
        isinstance(item, dict)
        and item.get("name") == "examples/sample-web-service"
        and isinstance(item.get("digest"), dict)
        and item["digest"].get("sha256") == expected_sha
        for item in subjects
    ):
        errors.append("provenance-archive-subject-mismatch")
    predicate = provenance.get("predicate")
    if not isinstance(predicate, dict):
        return sorted(set(errors + ["provenance-predicate-invalid"]))
    build_definition = predicate.get("buildDefinition")
    run_details = predicate.get("runDetails")
    if not isinstance(build_definition, dict) or not isinstance(run_details, dict):
        return sorted(set(errors + ["provenance-build-definition-invalid"]))
    params = build_definition.get("externalParameters")
    dependencies = build_definition.get("resolvedDependencies")
    builder = run_details.get("builder")
    if not isinstance(params, dict) or params.get("role") != subject.get("role"):
        errors.append("provenance-role-invalid")
    if not isinstance(params, dict) or params.get("source_revision") != subject.get("source_revision"):
        errors.append("provenance-source-revision-mismatch")
    if not isinstance(dependencies, list) or not dependencies:
        errors.append("provenance-materials-invalid")
    if not isinstance(builder, dict) or not _is_text(builder.get("id")):
        errors.append("provenance-builder-invalid")
    return sorted(set(errors))


def validate_signature_fixture(fixture: Any, subject: Any) -> list[str]:
    if not isinstance(fixture, dict) or not isinstance(subject, dict):
        return ["signature-fixture-invalid"]
    errors: list[str] = []
    if fixture.get("schema_version") != 1 or fixture.get("mode") != "cosign-sign-blob":
        errors.append("signature-fixture-invalid")
    if fixture.get("role") != subject.get("role"):
        errors.append("signature-role-mismatch")
    if fixture.get("oci_archive_sha256") != subject.get("oci_archive_sha256"):
        errors.append("signature-subject-mismatch")
    if fixture.get("verified") is not True:
        errors.append("signature-verification-rejected")
    return sorted(set(errors))


def validate_scorecard_advisory(scorecard: Any) -> list[str]:
    if not isinstance(scorecard, dict):
        return ["scorecard-fixture-invalid"]
    errors: list[str] = []
    if scorecard.get("schema_version") != 1:
        errors.append("scorecard-schema-version-invalid")
    if scorecard.get("mode") != "read-only-advisory" or scorecard.get("observation") != "read-only":
        errors.append("scorecard-advisory-mode-invalid")
    if scorecard.get("ci_enforcement") != "fixture-policy-only":
        errors.append("scorecard-blocking-forbidden")
    if scorecard.get("repository") != SCORECARD_REPOSITORY:
        errors.append("scorecard-repository-invalid")
    return sorted(set(errors))


def _fixture_subject() -> dict[str, str]:
    return {
        "role": "candidate",
        "source_revision": "0123456789abcdef0123456789abcdef01234567",
        "image_config_digest": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "oci_archive_sha256": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    }


def check() -> list[str]:
    registry = load_json(TOOL_REGISTRY_PATH)
    policy = load_json(POLICY_PATH)
    exceptions = load_json(EXCEPTIONS_PATH)
    subject = _fixture_subject()
    errors = [*validate_tool_registry(registry), *validate_policy(policy)]
    errors.extend(validate_exceptions(exceptions, policy, subject["image_config_digest"]))
    errors.extend(
        validate_subject_tuples(
            [
                {
                    **subject,
                    "role": "baseline",
                    "image_config_digest": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "oci_archive_sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                },
                subject,
            ]
        )
    )
    errors.extend(validate_sbom_subject(load_json(FIXTURES / "sample-service-sbom.valid.cdx.json"), subject))
    if not validate_sbom_subject(load_json(FIXTURES / "sample-service-sbom.subject-mismatch.cdx.json"), subject):
        errors.append("negative-sbom-fixture-not-rejected")
    for name, expected in (
        ("grype.clean.json", "accepted"),
        ("grype.high-without-exception.json", "rejected"),
        ("grype.high-with-valid-exception.json", "accepted"),
        ("grype.expired-exception.json", "rejected"),
        ("grype.valid-exception-then-critical.json", "rejected"),
    ):
        result = evaluate_grype_fixture(load_json(FIXTURES / name), policy, exceptions, subject)
        if result["verdict"] != expected:
            errors.append("grype-fixture-verdict-invalid")
    errors.extend(validate_provenance_subject(load_json(FIXTURES / "provenance.valid.intoto.json"), subject))
    if not validate_provenance_subject(load_json(FIXTURES / "provenance.subject-mismatch.intoto.json"), subject):
        errors.append("negative-provenance-fixture-not-rejected")
    errors.extend(validate_signature_fixture(load_json(FIXTURES / "cosign.verify.valid.json"), subject))
    for name in ("cosign.verify.tampered.json", "cosign.verify.wrong-subject.json"):
        if not validate_signature_fixture(load_json(FIXTURES / name), subject):
            errors.append("negative-signature-fixture-not-rejected")
    errors.extend(validate_scorecard_advisory(load_json(FIXTURES / "scorecard.advisory.json")))
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate policy and deterministic fixtures")
    parser.add_argument(
        "--oci-archive-config-digest",
        metavar="ARCHIVE",
        help="print the SHA-256 config digest cryptographically bound by an OCI archive",
    )
    args = parser.parse_args(argv)
    if args.oci_archive_config_digest:
        try:
            print(inspect_oci_archive_config_digest(args.oci_archive_config_digest))
        except ValueError as exc:
            print(f"oci_archive_config_digest=fail reason={exc}", file=sys.stderr)
            return 1
        return 0
    if not args.check:
        parser.print_usage(sys.stderr)
        return 2
    try:
        errors = check()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"supply_chain_policy=fail reason={exc.__class__.__name__}", file=sys.stderr)
        return 1
    if errors:
        print(f"supply_chain_policy=fail errors={','.join(errors)}", file=sys.stderr)
        return 1
    print("supply_chain_policy=pass fixtures=13")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
