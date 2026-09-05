#!/usr/bin/env python3
"""One complete document-corpus lifecycle route with no mode inventory."""

from __future__ import annotations

import argparse
import collections.abc
import pathlib
import sys

import yaml


_BOOTSTRAP_DIRECTORY = str(pathlib.Path(__file__).resolve().parents[2])
if _BOOTSTRAP_DIRECTORY not in sys.path:
    sys.path.insert(0, _BOOTSTRAP_DIRECTORY)


from scripts.lib.document_governance.lifecycle.contract import (
    DEFAULT_CONTRACT,
    DEFAULT_PROFILES,
    HISTORICAL_CONTRACT,
    ROOT,
    SAFETY_FINDING_CODES,
    Finding,
    ManifestEvidence,
    MigrationManifestDocument,
    MigrationManifestRow,
    ProfileError,
    ReviewVerdict,
    _CorpusSafetyError,
    _ensure_metadata_loaded,
    _lexically_safe_path,
    _read_regular_repo_bytes,
    _rooted,
    _sensitive_value_is_present,
    generate_manifest_skeleton,
    load_migration_contract,
    load_migration_manifest,
    metadata,
    render_migration_manifest,
)
from scripts.lib.document_governance.lifecycle.promoted import (
    _historical_promoted_findings,
)
from scripts.lib.document_governance.lifecycle.public import (
    _spec_package_lifecycle_findings,
)
from scripts.lib.document_governance.lifecycle.recovery import run as run_recovery


def _is_safety_finding(finding: Finding) -> bool:
    return finding.code in SAFETY_FINDING_CODES


def _diagnostic_payload_is_sensitive(value: str) -> bool:
    return _sensitive_value_is_present(value)


def _safe_diagnostic_path(value: object) -> str:
    path = value if isinstance(value, str) else "corpus"
    if (
        len(path.encode("utf-8", errors="replace")) > 512
        or not _lexically_safe_path(path)
        or _diagnostic_payload_is_sensitive(path)
    ):
        return "corpus"
    return path


def _print_findings(findings: collections.abc.Sequence[Finding]) -> None:
    ordered = sorted(set(findings))
    for finding in ordered:
        if _diagnostic_payload_is_sensitive(f"{finding.path}\n{finding.message}"):
            raise _CorpusSafetyError(
                _safe_diagnostic_path(finding.path),
                "diagnostic-redaction-unsafe",
            )
    for finding in ordered:
        print(
            f"{finding.code}: {_safe_diagnostic_path(finding.path)}: "
            "validation rule is not satisfied"
        )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument(
        "--registry",
        "--profiles",
        dest="profiles",
        type=pathlib.Path,
        default=DEFAULT_PROFILES,
        help="Stage 99 registry (legacy --profiles remains a transition alias)",
    )
    parser.add_argument("--base-ref")
    return parser


def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    """Validate the complete current document-corpus lifecycle in one route.

    The four retired modes contributed three finding sources. `check-contract`
    was the Spec Package source alone; `check-public` and `check-promoted` were
    that source plus the promoted source; `check-recovery` was the disjoint
    archive-recovery source. This route emits all three, so it is the union of
    what the modes produced and nothing is lost by their removal.
    """

    parser = _parser()
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        _ensure_metadata_loaded()
        profiles_path = _rooted(root, args.profiles).resolve()
        if profiles_path.suffix.lower() != ".json":
            raise ProfileError("Stage 99 registry must be the JSON registry")
        try:
            registry = metadata.load_registry(profiles_path)
        except metadata.RegistryError as error:
            raise ProfileError("Stage 99 registry is invalid") from error
        profiles = metadata.build_registry_profiles(registry)

        findings = _spec_package_lifecycle_findings(root, profiles, args.base_ref)
        findings.extend(_historical_promoted_findings(root))
        _print_findings(findings)
        print(f"document corpus lifecycle: violations={len(findings)}")
        recovery_code = run_recovery(root)
        if any(_is_safety_finding(item) for item in findings):
            return 3
        return 1 if findings or recovery_code else 0
    except _CorpusSafetyError as error:
        print(
            f"{error.code}: {_safe_diagnostic_path(error.path)}: "
            "selected lifecycle path is unsafe",
            file=sys.stderr,
        )
        return 3
    except ProfileError:
        print(
            "configuration-error: repository lifecycle input is invalid",
            file=sys.stderr,
        )
        return 3
    except (OSError, UnicodeError, yaml.YAMLError):
        print("internal-error: lifecycle operation failed safely", file=sys.stderr)
        return 3
    except Exception:
        print("internal-error: lifecycle operation failed safely", file=sys.stderr)
        return 3


if __name__ != "__main__":
    _ensure_metadata_loaded()


if __name__ == "__main__":
    raise SystemExit(main())
