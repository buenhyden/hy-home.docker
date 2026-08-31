#!/usr/bin/env python3
"""Thin CLI dispatch for the four current document-corpus lifecycle modes."""

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
    LEGACY_MIGRATION_PROFILES,
    MODES,
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
    _load_declared_manifests,
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
        if _diagnostic_payload_is_sensitive(
            f"{finding.path}\n{finding.message}"
        ):
            raise _CorpusSafetyError(
                _safe_diagnostic_path(finding.path),
                "diagnostic-redaction-unsafe",
            )
    for finding in ordered:
        print(
            f"{finding.code}: {_safe_diagnostic_path(finding.path)}: "
            "validation rule is not satisfied"
        )


def _validate_cli_shape(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    requirements: dict[str, tuple[set[str], set[str]]] = {
        "check-public": (set(), {"wave", "manifest", "exceptions", "output"}),
        "check-contract": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
        "check-promoted": (set(), {"base_ref", "manifest", "exceptions", "output"}),
        "check-recovery": (set(), {"wave", "base_ref", "manifest", "exceptions", "output"}),
    }
    required, forbidden = requirements[args.mode]
    for name in sorted(required):
        if getattr(args, name) is None:
            parser.error(f"--{name.replace('_', '-')} is required for --mode {args.mode}")
    for name in sorted(forbidden):
        if getattr(args, name) is not None:
            parser.error(f"--{name.replace('_', '-')} is forbidden for --mode {args.mode}")



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
    parser.add_argument("--contract", type=pathlib.Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--mode", default="check-public", choices=MODES)
    parser.add_argument("--wave")
    parser.add_argument("--base-ref")
    parser.add_argument("--manifest", type=pathlib.Path)
    parser.add_argument("--exceptions", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    return parser




def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    _validate_cli_shape(parser, args)
    try:
        root = args.root.resolve()
        if args.mode == "check-recovery":
            return run_recovery(root)

        _ensure_metadata_loaded()
        profiles_path = _rooted(root, args.profiles).resolve()
        if (
            args.contract is None
            and profiles_path.suffix.lower() == ".json"
            and args.mode in {"check-public", "check-contract", "check-promoted"}
        ):
            registry = metadata.load_registry(profiles_path)
            profiles = metadata.build_registry_profiles(registry)
            findings = _spec_package_lifecycle_findings(
                root,
                profiles,
                args.base_ref,
            )
            if args.mode != "check-contract":
                findings.extend(_historical_promoted_findings(root))
            _print_findings(findings)
            print(f"public document lifecycle: violations={len(findings)}")
            return 1 if findings else 0

        contract_path = (
            _rooted(root, args.contract).resolve()
            if args.contract is not None
            else HISTORICAL_CONTRACT
        )
        contract = load_migration_contract(contract_path)
        if profiles_path.suffix.lower() == ".json":
            try:
                registry = metadata.load_registry(profiles_path)
            except metadata.RegistryError as error:
                raise ProfileError("Stage 99 registry is invalid") from error
            profiles = metadata.build_registry_transition_profiles(
                registry,
                metadata.load_profiles(LEGACY_MIGRATION_PROFILES),
            )
        else:
            profiles = metadata.load_profiles(profiles_path)

        if args.mode == "check-contract":
            findings = _spec_package_lifecycle_findings(root, profiles)
            _print_findings(findings)
            print(
                "document corpus lifecycle contract: "
                f"violations={len(findings)}"
            )
            return 3 if any(_is_safety_finding(item) for item in findings) else (
                1 if findings else 0
            )
        if args.mode == "check-public":
            findings = _spec_package_lifecycle_findings(root, profiles)
            _, promoted_findings = _load_declared_manifests(
                root,
                profiles,
                contract,
                promoted_only=True,
                selected_wave=None,
            )
            findings.extend(promoted_findings)
            _print_findings(findings)
            print(f"public document lifecycle: violations={len(findings)}")
            return 3 if any(_is_safety_finding(item) for item in findings) else (
                1 if findings else 0
            )
        if args.mode == "check-promoted":
            _, findings = _load_declared_manifests(
                root,
                profiles,
                contract,
                promoted_only=True,
                selected_wave=args.wave,
            )
            _print_findings(findings)
            print(f"promoted lifecycle manifests: violations={len(findings)}")
            return 3 if any(_is_safety_finding(item) for item in findings) else (
                1 if findings else 0
            )
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
    raise AssertionError(f"unhandled lifecycle mode: {args.mode}")


if __name__ != "__main__":
    _ensure_metadata_loaded()


if __name__ == "__main__":
    raise SystemExit(main())
