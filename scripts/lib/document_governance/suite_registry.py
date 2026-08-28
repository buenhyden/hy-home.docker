"""Immutable ownership of public validation suites."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping

import yaml


PUBLIC_SUITE_NAMES = (
    "agent-governance",
    "document-contract",
    "document-graph",
    "document-lifecycle",
    "operations",
    "repository-integrity",
)
EXECUTION_CONTEXT_NAMES = (
    "local",
    "pull_request",
    "push",
    "workflow_dispatch",
)
IMMUTABLE_RETAINED_VALIDATOR_OWNERSHIP = MappingProxyType(
    {
        PurePosixPath("scripts/hardening/check-all-hardening.sh"): "repository-integrity",
        PurePosixPath("scripts/validation/agent_governance_contract.py"): "agent-governance",
        PurePosixPath("scripts/validation/agent_output_eval.py"): "agent-governance",
        PurePosixPath("scripts/validation/agentic-research-gate9-evidence.py"): "document-lifecycle",
        PurePosixPath("scripts/validation/audit_criterion_contract.py"): "repository-integrity",
        PurePosixPath("scripts/validation/carry_owner_contract.py"): "document-contract",
        PurePosixPath("scripts/validation/check-agent-governance-contract.py"): "agent-governance",
        PurePosixPath("scripts/validation/check-agentic-audit-semantic-freshness.py"): "repository-integrity",
        PurePosixPath("scripts/validation/check-doc-implementation-alignment.sh"): "document-graph",
        PurePosixPath("scripts/validation/check-doc-traceability.sh"): "document-graph",
        PurePosixPath("scripts/validation/check-document-corpus-lifecycle.py"): "document-lifecycle",
        PurePosixPath("scripts/validation/check-document-links.py"): "document-graph",
        PurePosixPath("scripts/validation/check-document-metadata.py"): "document-contract",
        PurePosixPath("scripts/validation/check-github-workflow-contract.py"): "repository-integrity",
        PurePosixPath("scripts/validation/check-old-path-gate.py"): "document-lifecycle",
        PurePosixPath("scripts/validation/check-operations-catalog.py"): "operations",
        PurePosixPath("scripts/validation/check-quickwin-baseline.sh"): "repository-integrity",
        PurePosixPath("scripts/validation/check-script-manifest.py"): "repository-integrity",
        PurePosixPath("scripts/validation/check-storybook-contract.sh"): "repository-integrity",
        PurePosixPath("scripts/validation/check-supply-chain-policy.py"): "repository-integrity",
        PurePosixPath("scripts/validation/check-target-surface-contract.py"): "document-contract",
        PurePosixPath("scripts/validation/check-target-surface-delta-contract.py"): "document-contract",
        PurePosixPath("scripts/validation/check-task4-migration.py"): "agent-governance",
        PurePosixPath("scripts/validation/check-template-security-baseline.sh"): "repository-integrity",
        PurePosixPath("scripts/validation/ci_gate_adapters.py"): "repository-integrity",
        PurePosixPath("scripts/validation/ci_gate_contract.py"): "repository-integrity",
        PurePosixPath("scripts/validation/github_workflow_contract.py"): "repository-integrity",
        PurePosixPath("scripts/validation/grype_db_seed.py"): "repository-integrity",
        PurePosixPath("scripts/validation/old_path_gate_contract.py"): "document-lifecycle",
        PurePosixPath("scripts/validation/rehearse-postgres-logical-upgrade.sh"): "operations",
        PurePosixPath("scripts/validation/report-audit-pack-coverage.sh"): "document-lifecycle",
        PurePosixPath("scripts/validation/report-provider-hook-parity.sh"): "agent-governance",
        PurePosixPath("scripts/validation/target_surface_contract.py"): "document-contract",
        PurePosixPath("scripts/validation/target_surface_delta_contract.py"): "document-contract",
        PurePosixPath("scripts/validation/validate-harness.sh"): "agent-governance",
    }
)
NON_STANDALONE_VALIDATOR_PATHS = frozenset(
    PurePosixPath(path)
    for path in (
        "scripts/validation/agent_governance_contract.py",
        "scripts/validation/agentic-research-gate9-evidence.py",
        "scripts/validation/ci_gate_adapters.py",
        "scripts/validation/ci_gate_contract.py",
        "scripts/validation/github_workflow_contract.py",
        "scripts/validation/grype_db_seed.py",
        "scripts/validation/old_path_gate_contract.py",
        "scripts/validation/rehearse-postgres-logical-upgrade.sh",
        "scripts/validation/target_surface_contract.py",
        "scripts/validation/target_surface_delta_contract.py",
        "scripts/validation/validate-harness.sh",
    )
)
_MIRRORED_TEST_ROOT = PurePosixPath("tests/lib/document_governance")


class SuiteRegistryError(ValueError):
    """Raised when manifest suite ownership is incomplete or ambiguous."""


@dataclass(frozen=True, slots=True)
class ValidatorOwnership:
    path: PurePosixPath
    public_suites: tuple[str, ...]
    execution_argv: tuple[str, ...]
    execution_contexts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProductionModule:
    path: PurePosixPath
    tests: tuple[PurePosixPath, ...]

    @property
    def has_mirrored_test(self) -> bool:
        return any(test.is_relative_to(_MIRRORED_TEST_ROOT) for test in self.tests)


@dataclass(frozen=True, slots=True)
class PublicSuite:
    name: str
    validators: tuple[PurePosixPath, ...]


@dataclass(frozen=True, slots=True)
class SuiteRegistry:
    public_names: tuple[str, ...]
    suites: tuple[PublicSuite, ...]
    validators: tuple[ValidatorOwnership, ...]
    production_modules: tuple[ProductionModule, ...]

    @property
    def by_name(self) -> Mapping[str, PublicSuite]:
        return MappingProxyType({suite.name: suite for suite in self.suites})


def load(path: Path = Path("scripts/manifest.yaml")) -> SuiteRegistry:
    """Load a closed, immutable suite mapping from the script manifest."""

    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise SuiteRegistryError("manifest is unreadable") from error
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        raise SuiteRegistryError("manifest files must be a list")

    rows = document["files"]
    validators: list[ValidatorOwnership] = []
    modules: list[ProductionModule] = []
    suites: dict[str, list[PurePosixPath]] = {name: [] for name in PUBLIC_SUITE_NAMES}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise SuiteRegistryError("manifest rows require a path")
        row_path = PurePosixPath(row["path"])
        _paths(row.get("consumers"), row_path, "consumers")
        tests = _paths(row.get("tests"), row_path, "tests")
        if row.get("kind") == "validator":
            public_suites = _suite_names(row.get("public_suites"), row_path)
            execution_argv = _optional_strings(
                row.get("execution_argv", []), row_path, "execution_argv"
            )
            execution_contexts = _execution_contexts(
                row.get("execution_contexts"), row_path
            )
            expected_contexts = (
                ()
                if row_path in NON_STANDALONE_VALIDATOR_PATHS
                else EXECUTION_CONTEXT_NAMES[1:]
                if row_path == PurePosixPath("scripts/hardening/check-all-hardening.sh")
                else EXECUTION_CONTEXT_NAMES
            )
            if execution_contexts != expected_contexts:
                raise SuiteRegistryError(
                    f"{row_path}: execution contexts must match the retained safety policy"
                )
            validators.append(
                ValidatorOwnership(
                    row_path,
                    public_suites,
                    execution_argv,
                    execution_contexts,
                )
            )
            suites[public_suites[0]].append(row_path)
        elif "public_suites" in row:
            raise SuiteRegistryError(f"{row_path}: only validators may declare public_suites")
        if row.get("kind") == "library" and row_path.name != "__init__.py" and row_path.is_relative_to(
            PurePosixPath("scripts/lib/document_governance")
        ):
            modules.append(ProductionModule(row_path, tests))

    for module in modules:
        if not module.has_mirrored_test:
            raise SuiteRegistryError(f"{module.path}: requires a mirrored library test")

    actual_ownership = {
        item.path: item.public_suites[0] for item in validators
    }
    if actual_ownership != IMMUTABLE_RETAINED_VALIDATOR_OWNERSHIP:
        raise SuiteRegistryError(
            "validator ownership must match the immutable Task 11 retained inventory"
        )

    return SuiteRegistry(
        public_names=PUBLIC_SUITE_NAMES,
        suites=tuple(PublicSuite(name, tuple(suites[name])) for name in PUBLIC_SUITE_NAMES),
        validators=tuple(validators),
        production_modules=tuple(modules),
    )


def _paths(value: object, row_path: PurePosixPath, field: str) -> tuple[PurePosixPath, ...]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise SuiteRegistryError(f"{row_path}: {field} must be a string list")
    paths = tuple(PurePosixPath(item) for item in value)
    if len(paths) != len(set(paths)):
        raise SuiteRegistryError(f"{row_path}: {field} must not contain duplicates")
    return paths


def _suite_names(value: object, row_path: PurePosixPath) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], str):
        raise SuiteRegistryError(f"{row_path}: validator must map to exactly one public suite")
    if value[0] not in PUBLIC_SUITE_NAMES:
        raise SuiteRegistryError(f"{row_path}: unknown public suite {value[0]!r}")
    return (value[0],)


def _optional_strings(
    value: object, row_path: PurePosixPath, field: str
) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SuiteRegistryError(f"{row_path}: {field} must be a string list")
    return tuple(value)


def _execution_contexts(value: object, row_path: PurePosixPath) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SuiteRegistryError(f"{row_path}: execution_contexts must be a string list")
    contexts = tuple(value)
    expected_order = tuple(name for name in EXECUTION_CONTEXT_NAMES if name in contexts)
    if contexts != expected_order or len(contexts) != len(set(contexts)):
        raise SuiteRegistryError(
            f"{row_path}: execution_contexts must be unique and canonically ordered"
        )
    return contexts
