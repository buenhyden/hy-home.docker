from __future__ import annotations

import dataclasses
import enum
import errno
import json
import os
import pathlib
import re
import stat
import subprocess
from collections.abc import Mapping

from scripts.lib.document_governance import suite_registry


_CONTRACT_PATH = pathlib.PurePosixPath(".github/workflow-contract.yml")
_MAX_CONTRACT_BYTES = 1024 * 1024
_MAX_JSON_DEPTH = 256
_MAX_GATE_NODES = 2048
_MAX_GATE_EDGES = 8192
_GIT_TIMEOUT_SECONDS = 5
_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "workflows",
        "gate_nodes",
        "job_roots",
        "profile_roots",
        "public_gate",
        "actions",
    }
)
_NODE_PROFILES = (
    "ci",
    "local-script-backed",
    "local-harness",
    "local-all-profiles",
)
_INTERNAL_CI_ROOTS = {
    "docs-traceability": "ci.docs-traceability",
    "docs-implementation-alignment": "ci.docs-implementation-alignment",
    "repo-contracts": "ci.repo-contracts",
    "agent-output-eval-fixture-gate": "ci.agent-output-eval-fixture-gate",
    "supply-chain-fixture-policy": "ci.supply-chain-fixture-policy",
    "dependency-vulnerability-audit": "ci.dependency-vulnerability-audit",
    "git-flow-contract": "ci.git-flow-contract",
    "compose-validation": "ci.compose-validation",
    "compose-all-profiles-validation": "ci.compose-all-profiles-validation",
    "infrastructure-hardening": "ci.infrastructure-hardening",
    "template-security-baseline": "ci.template-security-baseline",
    "quickwin-baseline": "ci.quickwin-baseline",
    "pre-commit": "ci.pre-commit",
    "frontend-quality": "ci.frontend-quality",
    "storybook-coverage": "ci.storybook-coverage",
    "zizmor": "ci.zizmor",
}


def load_public_suite_registry(
    manifest_path: pathlib.Path = pathlib.Path("scripts/manifest.yaml"),
) -> suite_registry.SuiteRegistry:
    """Expose the immutable validator-suite registry to gate contracts."""

    return suite_registry.load(manifest_path)
_INTERNAL_ROOT_SUITES = {
    "docs-traceability": ("docs-traceability",),
    "docs-implementation-alignment": (
        "docs-implementation-alignment",
        "docs-qa-gate-recommendations",
    ),
    "repo-contracts": (
        "repo-metadata-base",
        "repo-document-metadata",
        "ci-gate-contract-regressions",
        "ci-gate-runner-regressions",
        "ci-gate-adapter-regressions",
        "workflow-contract-regressions",
        "repo-contracts-control-plane-regressions",
        "ci-precommit-regressions",
        "workflow-contract",
        "operations-catalog-manifest",
        "repo-contracts",
    ),
    "agent-output-eval-fixture-gate": (
        "agent-output-eval-fixture-regressions",
        "agent-output-eval-fixture-gate",
    ),
    "supply-chain-fixture-policy": (
        "supply-chain-fixture-policy",
        "supply-chain-deterministic-policy",
        "supply-chain-summary-freshness",
    ),
    "dependency-vulnerability-audit": ("dependency-vulnerability-audit",),
    "git-flow-contract": ("git-flow-contract",),
    "compose-validation": ("compose-validation",),
    "compose-all-profiles-validation": ("compose-all-profiles-validation",),
    "infrastructure-hardening": ("infrastructure-hardening",),
    "template-security-baseline": ("template-security-baseline",),
    "quickwin-baseline": ("quickwin-baseline",),
    "pre-commit": ("pre-commit",),
    "frontend-quality": (
        "frontend-lint",
        "frontend-typecheck",
        "frontend-build",
        "frontend-quality",
    ),
    "storybook-coverage": ("storybook-coverage",),
    "zizmor": ("zizmor",),
}
_INTERNAL_ROOT_CHILDREN = {
    "ci.docs-traceability": ("leaf.docs-traceability",),
    "ci.docs-implementation-alignment": (
        "leaf.docs-implementation-alignment",
        "leaf.docs-qa-gate-recommendations",
    ),
    "ci.repo-contracts": (
        "leaf.repo-metadata-base",
        "setup.repo-python-dependencies",
        "leaf.repo-document-metadata",
        "leaf.ci-gate-contract-regressions",
        "leaf.ci-gate-runner-regressions",
        "leaf.ci-gate-adapter-regressions",
        "leaf.workflow-contract-regressions",
        "leaf.repo-contracts-control-plane-regressions",
        "leaf.ci-precommit-regressions",
        "leaf.workflow-contract",
        "leaf.operations-catalog-manifest",
        "leaf.repo-contracts",
    ),
    "ci.agent-output-eval-fixture-gate": (
        "leaf.agent-output-eval-fixture-regressions",
        "leaf.agent-output-eval-fixture-gate",
    ),
    "ci.supply-chain-fixture-policy": (
        "leaf.supply-chain-fixture-policy",
        "leaf.supply-chain-deterministic-policy",
        "leaf.supply-chain-summary-freshness",
    ),
    "ci.dependency-vulnerability-audit": (
        "leaf.dependency-vulnerability-audit",
    ),
    "ci.git-flow-contract": ("leaf.git-flow-contract",),
    "ci.compose-validation": (
        "setup.compose-env",
        "leaf.compose-validation",
    ),
    "ci.compose-all-profiles-validation": (
        "setup.compose-env",
        "leaf.compose-all-profiles-validation",
    ),
    "ci.infrastructure-hardening": (
        "setup.compose-env",
        "leaf.infrastructure-hardening",
    ),
    "ci.template-security-baseline": (
        "setup.compose-env",
        "leaf.template-security-baseline",
    ),
    "ci.quickwin-baseline": (
        "setup.compose-env",
        "leaf.quickwin-baseline",
    ),
    "ci.pre-commit": (
        "setup.precommit-python-dependencies",
        "leaf.pre-commit",
    ),
    "ci.frontend-quality": (
        "setup.frontend-node-dependencies",
        "leaf.frontend-lint",
        "leaf.frontend-typecheck",
        "leaf.frontend-build",
        "leaf.frontend-quality",
    ),
    "ci.storybook-coverage": (
        "setup.storybook-node-dependencies",
        "setup.storybook-playwright",
        "leaf.storybook-coverage",
    ),
    "ci.zizmor": ("leaf.zizmor",),
}
_REQUIRED_JOB_ROOTS = {
    "validation-changed": "ci.validation-changed",
    "validation-full": "ci.validation-full",
}
_REQUIRED_ROOT_CHILDREN = {
    root_gate_id: tuple(_INTERNAL_CI_ROOTS.values())
    for root_gate_id in _REQUIRED_JOB_ROOTS.values()
}
_ALL_CI_SUITES = tuple(
    suite
    for job_id in _INTERNAL_CI_ROOTS
    for suite in _INTERNAL_ROOT_SUITES[job_id]
)
_REQUIRED_JOB_SUITES = {
    job_id: _ALL_CI_SUITES for job_id in _REQUIRED_JOB_ROOTS
}
_LOCAL_AGGREGATE_CHILDREN = {
    "local.document-corpus-lifecycle": (
        "leaf.local-document-corpus-lifecycle-tests",
        "leaf.local-document-corpus-contract",
        "leaf.local-document-corpus-promoted",
    ),
    "local.target-surface": (
        "leaf.local-target-surface-regressions",
        "leaf.local-target-surface-contract",
        "leaf.local-target-delta-regressions",
        "leaf.local-target-delta-contract",
    ),
    "local.workflow-harness": (
        "leaf.ci-gate-contract-regressions",
        "leaf.ci-gate-runner-regressions",
        "leaf.ci-gate-adapter-regressions",
        "leaf.workflow-contract-regressions",
        "leaf.repo-contracts-control-plane-regressions",
        "leaf.ci-precommit-regressions",
        "leaf.workflow-contract",
    ),
    "local.supply-chain": (
        "leaf.supply-chain-deterministic-policy",
        "leaf.supply-chain-summary-freshness",
    ),
    "local.generated-freshness": (
        "leaf.local-security-readiness-freshness",
        "leaf.local-audit-matrix-freshness",
        "leaf.local-llm-wiki-freshness",
        "leaf.local-script-manifest",
        "leaf.operations-catalog-manifest",
    ),
    "local.compose-validation": ("leaf.compose-validation",),
    "local.compose-all-profiles-validation": (
        "leaf.compose-all-profiles-validation",
    ),
    "local.infrastructure-hardening": ("leaf.infrastructure-hardening",),
    "local.template-security-baseline": (
        "leaf.template-security-baseline",
    ),
    "local.quickwin-baseline": ("leaf.quickwin-baseline",),
}
_LOCAL_FORBIDDEN_GATE_IDS = frozenset(
    {
        "setup.compose-env",
        "setup.repo-python-dependencies",
        "setup.precommit-python-dependencies",
        "setup.frontend-node-dependencies",
        "setup.storybook-node-dependencies",
        "setup.storybook-playwright",
        "leaf.dependency-vulnerability-audit",
        "leaf.pre-commit",
        "leaf.frontend-lint",
        "leaf.frontend-typecheck",
        "leaf.frontend-build",
        "leaf.frontend-quality",
        "leaf.storybook-coverage",
        "leaf.zizmor",
    }
)
_LOCAL_SCRIPT_BACKED_ROOTS = (
    "leaf.local-diff-hygiene",
    "leaf.local-shell-syntax",
    "leaf.local-provider-surface-drift",
    "ci.agent-output-eval-fixture-gate",
    "leaf.local-agent-governance-contract",
    "leaf.local-tech-stack-version-drift",
    "ci.docs-traceability",
    "leaf.docs-implementation-alignment",
    "local.document-corpus-lifecycle",
    "local.target-surface",
    "local.workflow-harness",
    "local.supply-chain",
    "local.compose-validation",
    "local.infrastructure-hardening",
    "local.template-security-baseline",
    "local.quickwin-baseline",
    "local.generated-freshness",
    "leaf.repo-contracts",
)
_LOCAL_HARNESS_ROOTS = tuple(
    gate_id
    for gate_id in _LOCAL_SCRIPT_BACKED_ROOTS
    if gate_id
    not in {
        "leaf.local-tech-stack-version-drift",
        "local.quickwin-baseline",
    }
)
_EXPECTED_PROFILE_ROOTS = {
    "local-script-backed": _LOCAL_SCRIPT_BACKED_ROOTS,
    "local-harness": _LOCAL_HARNESS_ROOTS,
    "local-all-profiles": (
        *_LOCAL_SCRIPT_BACKED_ROOTS,
        "local.compose-all-profiles-validation",
    ),
}
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_ENV_KEY = re.compile(r"[A-Z_][A-Z0-9_]*\Z")
_ADMITTED_ENV_KEYS = frozenset(
    {
        "CI",
        "EVENT_NAME",
        "GITHUB_ACTIONS",
        "GITHUB_STEP_SUMMARY",
        "HEAD_REF",
        "HYHOME_COMPOSE_PROFILES",
        "PR_BASE_SHA",
        "PR_TITLE",
        "PUSH_BEFORE_SHA",
        "SKIP",
        "TEMPLATE_GATE_BASE",
    }
)
_IDENTIFIER = re.compile(r"[a-z0-9]+(?:[.-][a-z0-9]+)*\Z")


class GateKind(enum.StrEnum):
    LEAF = "leaf"
    AGGREGATE = "aggregate"
    SETUP = "setup"


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class GateFinding:
    code: str
    path: str
    message: str


class GateContractError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message


@dataclasses.dataclass(frozen=True, slots=True)
class GateNode:
    gate_id: str
    kind: GateKind
    suite_key: str | None
    entrypoint: pathlib.PurePosixPath | None
    argv: tuple[str, ...]
    cwd: pathlib.PurePosixPath | None
    allowed_env_keys: tuple[str, ...]
    timeout_minutes: int | None
    profiles: tuple[str, ...]
    opaque: bool
    children: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class JobRoot:
    workflow: str
    job_id: str
    root_gate_id: str
    classification: str


@dataclasses.dataclass(frozen=True, slots=True)
class ProfileRoot:
    profile: str
    root_gate_ids: tuple[str, ...]
    classification: str


@dataclasses.dataclass(frozen=True, slots=True)
class GateRegistry:
    nodes: tuple[GateNode, ...]
    job_roots: tuple[JobRoot, ...]
    profile_roots: tuple[ProfileRoot, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class PublicSuiteRoute:
    name: str
    root_gate_ids: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class ChangedSuiteRule:
    prefixes: tuple[str, ...]
    suites: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class PublicGateContract:
    profile_names: tuple[str, ...]
    suites: tuple[PublicSuiteRoute, ...]
    changed_rules: tuple[ChangedSuiteRule, ...]
    changed_fallback_suites: tuple[str, ...]

    @property
    def suite_names(self) -> tuple[str, ...]:
        return tuple(route.name for route in self.suites)


def load_contract_document(root: pathlib.Path) -> dict[str, object]:
    root = pathlib.Path(root)
    try:
        canonical_root = pathlib.Path(root.resolve(strict=False))
    except OSError:
        raise GateContractError(
            "ci-gate-input-unreadable",
            _CONTRACT_PATH.as_posix(),
            "the contract input could not be read",
        ) from None
    if not root.is_absolute() or ".." in root.parts or canonical_root != root:
        raise GateContractError(
            "ci-gate-path-noncanonical",
            _CONTRACT_PATH.as_posix(),
            "the repository root must be an absolute canonical directory",
        )

    directory_flags = os_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
    directory_flags |= os.O_DIRECTORY
    file_descriptor = -1
    github_descriptor = -1
    root_descriptor = -1
    open_stage = "root"
    try:
        root_descriptor = os.open(root, directory_flags)
        open_stage = "parent"
        github_descriptor = os.open(
            ".github",
            directory_flags,
            dir_fd=root_descriptor,
        )
        open_stage = "input"
        file_descriptor = os.open(
            "workflow-contract.yml",
            os_flags,
            dir_fd=github_descriptor,
        )
        metadata = os.fstat(file_descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise GateContractError(
                "ci-gate-input-not-regular",
                _CONTRACT_PATH.as_posix(),
                "the contract input must be a regular file",
            )
        if metadata.st_size > _MAX_CONTRACT_BYTES:
            raise GateContractError(
                "ci-gate-input-oversized",
                _CONTRACT_PATH.as_posix(),
                "the contract input exceeds the size limit",
            )
        chunks: list[bytes] = []
        remaining = _MAX_CONTRACT_BYTES + 1
        open_stage = "read"
        while remaining:
            chunk = os.read(file_descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > _MAX_CONTRACT_BYTES:
            raise GateContractError(
                "ci-gate-input-oversized",
                _CONTRACT_PATH.as_posix(),
                "the contract input exceeds the size limit",
            )
    except FileNotFoundError:
        raise GateContractError(
            "ci-gate-input-missing",
            _CONTRACT_PATH.as_posix(),
            "the contract input is missing",
        ) from None
    except OSError as error:
        if error.errno == errno.ELOOP:
            code = "ci-gate-input-symlink"
            message = "the contract input must not be a symbolic link"
        elif error.errno == errno.ENOTDIR or open_stage == "parent":
            code = "ci-gate-parent-invalid"
            message = "the contract parent must be a real directory"
        else:
            code = "ci-gate-input-unreadable"
            message = "the contract input could not be read"
        raise GateContractError(
            code,
            _CONTRACT_PATH.as_posix(),
            message,
        ) from None
    finally:
        for descriptor in (
            file_descriptor,
            github_descriptor,
            root_descriptor,
        ):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass

    try:
        source = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise GateContractError(
            "ci-gate-input-non-utf8",
            _CONTRACT_PATH.as_posix(),
            "the contract input must be UTF-8",
        ) from None

    class DuplicateKeyError(ValueError):
        pass

    def strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateKeyError
            result[key] = value
        return result

    def reject_constant(_value: str) -> object:
        raise ValueError

    if not _json_depth_within_limit(source):
        raise GateContractError(
            "ci-gate-json-invalid",
            _CONTRACT_PATH.as_posix(),
            "the contract input must be bounded strict JSON",
        )
    try:
        document = json.loads(
            source,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except DuplicateKeyError:
        raise GateContractError(
            "ci-gate-json-duplicate-key",
            _CONTRACT_PATH.as_posix(),
            "the contract input contains a duplicate JSON key",
        ) from None
    except (json.JSONDecodeError, RecursionError, ValueError):
        raise GateContractError(
            "ci-gate-json-invalid",
            _CONTRACT_PATH.as_posix(),
            "the contract input must be strict JSON",
        ) from None
    if not isinstance(document, dict):
        raise GateContractError(
            "ci-gate-document-type",
            _CONTRACT_PATH.as_posix(),
            "the contract document must be an object",
        )
    schema_version = document.get("schema_version")
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version != 2
    ):
        raise GateContractError(
            "ci-gate-schema-version",
            _CONTRACT_PATH.as_posix(),
            "the contract schema version must be 2",
        )
    return document


def parse_gate_registry(
    document: Mapping[str, object],
    path: str,
) -> GateRegistry:
    _require_fields(document, _TOP_LEVEL_FIELDS, {"schema_version", "gate_nodes", "job_roots", "profile_roots"}, "ci-gate-document-fields", path)
    if type(document["schema_version"]) is not int or document["schema_version"] != 2:
        raise GateContractError(
            "ci-gate-schema-version",
            path,
            "the contract schema version must be 2",
        )
    for field in ("workflows", "actions"):
        if field in document and not isinstance(document[field], dict):
            raise GateContractError(
                "ci-gate-document-fields",
                path,
                "registry sections must be JSON objects",
            )
    raw_nodes = _require_records(document["gate_nodes"], "ci-gate-nodes-type", path)
    if len(raw_nodes) > _MAX_GATE_NODES:
        raise GateContractError(
            "ci-gate-node-limit",
            path,
            "the gate registry exceeds the node limit",
        )
    nodes = tuple(
        _parse_node(record, f"{path}#gate_nodes[{index}]")
        for index, record in enumerate(raw_nodes)
    )
    if sum(len(node.children) for node in nodes) > _MAX_GATE_EDGES:
        raise GateContractError(
            "ci-gate-edge-limit",
            path,
            "the gate registry exceeds the edge limit",
        )
    if len({node.gate_id for node in nodes}) != len(nodes):
        raise GateContractError(
            "ci-gate-id-duplicate",
            path,
            "gate identifiers must be unique",
        )
    raw_jobs = _require_records(document["job_roots"], "ci-gate-job-roots-type", path)
    job_roots = tuple(
        _parse_job_root(record, f"{path}#job_roots[{index}]")
        for index, record in enumerate(raw_jobs)
    )
    raw_profiles = _require_records(
        document["profile_roots"],
        "ci-gate-profile-roots-type",
        path,
    )
    profile_roots = tuple(
        _parse_profile_root(record, f"{path}#profile_roots[{index}]")
        for index, record in enumerate(raw_profiles)
    )
    return GateRegistry(nodes, job_roots, profile_roots)


def parse_public_gate_contract(
    document: Mapping[str, object],
    registry: suite_registry.SuiteRegistry,
) -> PublicGateContract:
    """Parse the closed public profile and changed-path selection contract."""

    raw = document.get("public_gate")
    if not isinstance(raw, Mapping):
        raise GateContractError(
            "ci-gate-public-contract",
            "public_gate",
            "the public gate contract must be an object",
        )
    _require_fields(
        raw,
        frozenset(
            {
                "profiles",
                "suite_roots",
                "changed_path_rules",
                "changed_fallback_suites",
            }
        ),
        frozenset(
            {
                "profiles",
                "suite_roots",
                "changed_path_rules",
                "changed_fallback_suites",
            }
        ),
        "ci-gate-public-contract",
        "public_gate",
    )
    profiles = _strings(
        raw["profiles"],
        "ci-gate-public-profiles",
        "public_gate/profiles",
    )
    if profiles != ("changed", "full"):
        raise GateContractError(
            "ci-gate-public-profiles",
            "public_gate/profiles",
            "public profiles must be exactly changed and full",
        )

    raw_roots = raw["suite_roots"]
    if not isinstance(raw_roots, Mapping) or tuple(raw_roots) != registry.public_names:
        raise GateContractError(
            "ci-gate-public-suites",
            "public_gate/suite_roots",
            "public suite roots must match the exact manifest suite order",
        )
    node_ids = {
        record.get("gate_id")
        for record in document.get("gate_nodes", ())
        if isinstance(record, Mapping)
    }
    routes: list[PublicSuiteRoute] = []
    assigned_roots: set[str] = set()
    for name in registry.public_names:
        roots = _strings(
            raw_roots[name],
            "ci-gate-public-suite-roots",
            f"public_gate/suite_roots/{name}",
        )
        if not roots or len(roots) != len(set(roots)) or any(
            root not in node_ids or root in assigned_roots for root in roots
        ):
            raise GateContractError(
                "ci-gate-public-suite-roots",
                f"public_gate/suite_roots/{name}",
                "public suite roots must be nonempty, unique, and registered",
            )
        assigned_roots.update(roots)
        routes.append(PublicSuiteRoute(name, roots))

    raw_rules = _require_records(
        raw["changed_path_rules"],
        "ci-gate-changed-rules",
        "public_gate/changed_path_rules",
    )
    rules: list[ChangedSuiteRule] = []
    seen_prefixes: set[str] = set()
    for index, record in enumerate(raw_rules):
        rule_path = f"public_gate/changed_path_rules[{index}]"
        _require_fields(
            record,
            frozenset({"prefixes", "suites"}),
            frozenset({"prefixes", "suites"}),
            "ci-gate-changed-rules",
            rule_path,
        )
        prefixes = _strings(
            record["prefixes"],
            "ci-gate-changed-rules",
            f"{rule_path}/prefixes",
        )
        suites = _strings(
            record["suites"],
            "ci-gate-changed-rules",
            f"{rule_path}/suites",
        )
        expected_suite_order = tuple(
            name for name in registry.public_names if name in suites
        )
        if (
            not prefixes
            or not suites
            or len(prefixes) != len(set(prefixes))
            or seen_prefixes.intersection(prefixes)
            or suites != expected_suite_order
            or any(not _valid_changed_prefix(prefix) for prefix in prefixes)
        ):
            raise GateContractError(
                "ci-gate-changed-rules",
                rule_path,
                "changed-path rules must use unique canonical prefixes and suites",
            )
        seen_prefixes.update(prefixes)
        rules.append(ChangedSuiteRule(prefixes, suites))

    fallback = _strings(
        raw["changed_fallback_suites"],
        "ci-gate-changed-fallback",
        "public_gate/changed_fallback_suites",
    )
    expected_fallback_order = tuple(
        name for name in registry.public_names if name in fallback
    )
    if not fallback or fallback != expected_fallback_order:
        raise GateContractError(
            "ci-gate-changed-fallback",
            "public_gate/changed_fallback_suites",
            "changed fallback suites must be a nonempty canonical subset",
        )
    return PublicGateContract(profiles, tuple(routes), tuple(rules), fallback)


def select_public_suites(
    contract: PublicGateContract,
    profile: str,
    changed_paths: tuple[str, ...],
) -> tuple[str, ...]:
    """Select public suites without allowing an unknown profile or unsafe path."""

    if profile not in contract.profile_names:
        raise GateContractError(
            "ci-gate-profile-unknown",
            "profile",
            "the selected profile is not registered",
        )
    if profile == "full":
        return contract.suite_names
    if any(not _valid_changed_path(path) for path in changed_paths):
        raise GateContractError(
            "ci-gate-changed-path",
            "changed_paths",
            "changed paths must be canonical repository-relative paths",
        )
    selected = set(contract.changed_fallback_suites)
    for rule in contract.changed_rules:
        if any(
            _matches_changed_prefix(path, prefix)
            for path in changed_paths
            for prefix in rule.prefixes
        ):
            selected.update(rule.suites)
    return tuple(name for name in contract.suite_names if name in selected)


def public_root_gate_ids(
    contract: PublicGateContract,
    selected_suites: tuple[str, ...],
) -> tuple[str, ...]:
    if len(selected_suites) != len(set(selected_suites)) or any(
        name not in contract.suite_names for name in selected_suites
    ):
        raise GateContractError(
            "ci-gate-public-suites",
            "suites",
            "selected public suites must be unique and registered",
        )
    selected = set(selected_suites)
    return tuple(
        gate_id
        for route in contract.suites
        if route.name in selected
        for gate_id in route.root_gate_ids
    )


def _valid_changed_prefix(value: str) -> bool:
    if not value or "\\" in value or any(ord(character) < 32 for character in value):
        return False
    candidate = pathlib.PurePosixPath(value.removesuffix("/"))
    return (
        not candidate.is_absolute()
        and candidate.as_posix() == value.removesuffix("/")
        and all(part not in {"", ".", ".."} for part in candidate.parts)
    )


def _valid_changed_path(value: str) -> bool:
    return _valid_changed_prefix(value) and not value.endswith("/")


def _matches_changed_prefix(path: str, prefix: str) -> bool:
    literal = prefix.removesuffix("/")
    return path == literal or path.startswith(f"{literal}/")


def validate_gate_registry(
    root: pathlib.Path,
    registry: GateRegistry,
) -> tuple[GateFinding, ...]:
    findings: list[GateFinding] = []

    def finding(code: str, path: str, message: str) -> None:
        findings.append(GateFinding(code, path, message))

    if len(registry.nodes) > _MAX_GATE_NODES:
        finding(
            "ci-gate-node-limit",
            "gate_nodes",
            "the gate registry exceeds the node limit",
        )
        return tuple(findings)
    edge_count = sum(len(node.children) for node in registry.nodes)
    if edge_count > _MAX_GATE_EDGES:
        finding(
            "ci-gate-edge-limit",
            "gate_nodes",
            "the gate registry exceeds the edge limit",
        )
        return tuple(findings)

    job_mapping = {
        job.job_id: job.root_gate_id
        for job in registry.job_roots
        if job.workflow == ".github/workflows/ci-quality.yml"
        and job.classification == "required-quality"
    }
    if (
        len(job_mapping) != len(registry.job_roots)
        or job_mapping != _REQUIRED_JOB_ROOTS
    ):
        finding(
            "ci-gate-required-job-roots",
            "job_roots",
            "required quality must map to the exact two workflow jobs",
        )
        return tuple(findings)

    node_by_id = {node.gate_id: node for node in registry.nodes}
    if len(node_by_id) != len(registry.nodes):
        finding(
            "ci-gate-id-duplicate",
            "gate_nodes",
            "gate identifiers must be unique",
        )
        return tuple(findings)
    roots = tuple(job_mapping.values()) + tuple(
        root_gate_id
        for profile_root in registry.profile_roots
        for root_gate_id in profile_root.root_gate_ids
    )
    missing_roots = {gate_id for gate_id in roots if gate_id not in node_by_id}
    missing_children = {
        child
        for node in registry.nodes
        for child in node.children
        if child not in node_by_id
    }
    if missing_roots or missing_children:
        finding(
            "ci-gate-child-missing",
            "gate_nodes",
            "a registered root or child does not exist",
        )
        return tuple(findings)

    if _graph_has_cycle(node_by_id):
        finding(
            "ci-gate-cycle",
            "gate_nodes",
            "the gate graph must be acyclic",
        )
        return tuple(findings)

    reachable = set(_expanded_all_ids(node_by_id, roots))
    if reachable != set(node_by_id):
        finding(
            "ci-gate-orphan",
            "gate_nodes",
            "every gate must be reachable from a registered root",
        )
        return tuple(findings)

    seen_suites: set[str] = set()
    duplicate_suites: set[str] = set()
    for node in registry.nodes:
        if node.kind is GateKind.LEAF and node.suite_key is not None:
            if node.suite_key in seen_suites:
                duplicate_suites.add(node.suite_key)
            seen_suites.add(node.suite_key)
    if duplicate_suites:
        finding(
            "ci-gate-suite-duplicate",
            "gate_nodes",
            "semantic suite keys must be unique",
        )
        finding(
            "ci-gate-suite-owner-duplicate",
            "job_roots",
            "a semantic suite has more than one required owner",
        )
        return tuple(findings)

    topological_ids = _topological_ids(node_by_id)
    for root_gate_id, expected_children in _INTERNAL_ROOT_CHILDREN.items():
        if node_by_id[root_gate_id].children != expected_children:
            finding(
                "ci-gate-internal-root-children",
                f"gate_nodes/{root_gate_id}",
                "internal CI roots must retain their exact ordered children",
            )
            return tuple(findings)
    for job in registry.job_roots:
        path_counts = _bounded_path_counts(
            node_by_id,
            topological_ids,
            job.root_gate_id,
        )
        if any(
            count > 1
            for gate_id, count in path_counts.items()
            if node_by_id[gate_id].kind is GateKind.LEAF
        ):
            finding(
                "ci-gate-suite-reachable-duplicate",
                "job_roots",
                "a semantic suite is reachable more than once from a workflow",
            )
            return tuple(findings)
        if (
            node_by_id[job.root_gate_id].children
            != _REQUIRED_ROOT_CHILDREN[job.root_gate_id]
        ):
            finding(
                "ci-gate-required-root-children",
                f"gate_nodes/{job.root_gate_id}",
                "required roots must retain their exact ordered children",
            )
            return tuple(findings)
        actual_suites = tuple(
            node_by_id[gate_id].suite_key
            for gate_id in _expanded_ids(node_by_id, (job.root_gate_id,))
            if node_by_id[gate_id].kind is GateKind.LEAF
        )
        if actual_suites != _REQUIRED_JOB_SUITES[job.job_id]:
            finding(
                "ci-gate-suite-owner",
                "job_roots",
                "required suites must belong to their exact required root",
            )
            return tuple(findings)

    profile_mapping = {
        profile.profile: profile.root_gate_ids
        for profile in registry.profile_roots
    }
    if (
        len(profile_mapping) != len(registry.profile_roots)
        or profile_mapping != _EXPECTED_PROFILE_ROOTS
        or any(
            profile.classification != "local"
            for profile in registry.profile_roots
        )
    ):
        finding(
            "ci-gate-profile-roots",
            "profile_roots",
            "local profile roots must match the exact ordered projections",
        )
        return tuple(findings)

    for profile in registry.profile_roots:
        local_reachable = set(
            _expanded_all_ids(node_by_id, profile.root_gate_ids)
        )
        if local_reachable & _LOCAL_FORBIDDEN_GATE_IDS:
            finding(
                "ci-gate-local-unsafe",
                f"profile_roots/{profile.profile}",
                "local profiles must exclude CI-only and networked gates",
            )
            return tuple(findings)

    for gate_id, expected_children in _LOCAL_AGGREGATE_CHILDREN.items():
        if node_by_id[gate_id].children != expected_children:
            finding(
                "ci-gate-local-aggregate-children",
                f"gate_nodes/{gate_id}",
                "local aggregates must retain their exact ordered children",
            )
            return tuple(findings)

    computed_profiles: dict[str, list[str]] = {
        gate_id: [] for gate_id in node_by_id
    }
    for profile in _NODE_PROFILES:
        profile_roots = (
            tuple(job_mapping.values())
            if profile == "ci"
            else profile_mapping[profile]
        )
        for gate_id in _expanded_all_ids(node_by_id, profile_roots):
            computed_profiles[gate_id].append(profile)
    tracked_files: dict[pathlib.PurePosixPath, bool] = {}
    canonical_directories: dict[pathlib.PurePosixPath, bool] = {}
    for node in registry.nodes:
        if node.profiles != tuple(computed_profiles[node.gate_id]):
            finding(
                "ci-gate-profile-drift",
                f"gate_nodes/{node.gate_id}",
                "node profiles must equal computed root reachability",
            )

    for node in registry.nodes:
        if node.kind is GateKind.AGGREGATE:
            continue
        if node.entrypoint is None or node.cwd is None:
            continue
        if node.entrypoint not in tracked_files:
            tracked_files[node.entrypoint] = _tracked_regular_file(
                root,
                node.entrypoint,
            )
        if not tracked_files[node.entrypoint]:
            finding(
                "ci-gate-entrypoint-invalid",
                f"gate_nodes/{node.gate_id}",
                "entrypoints must be tracked canonical first-party files",
            )
        if node.cwd not in canonical_directories:
            canonical_directories[node.cwd] = _canonical_directory(
                root,
                node.cwd,
            )
        if not canonical_directories[node.cwd]:
            finding(
                "ci-gate-cwd-invalid",
                f"gate_nodes/{node.gate_id}",
                "working directories must be canonical repository directories",
            )
    return tuple(sorted(set(findings)))


def expand_gate_ids(
    registry: GateRegistry,
    profile: str,
    gate_id: str | None,
    all_roots: bool,
) -> tuple[str, ...]:
    if (gate_id is None) == (not all_roots):
        raise GateContractError(
            "ci-gate-selection",
            "gate",
            "select exactly one gate or all roots",
        )
    if len(registry.nodes) > _MAX_GATE_NODES:
        raise GateContractError(
            "ci-gate-node-limit",
            "gate_nodes",
            "the gate registry exceeds the node limit",
        )
    if sum(len(node.children) for node in registry.nodes) > _MAX_GATE_EDGES:
        raise GateContractError(
            "ci-gate-edge-limit",
            "gate_nodes",
            "the gate registry exceeds the edge limit",
        )
    node_by_id = {node.gate_id: node for node in registry.nodes}
    if len(node_by_id) != len(registry.nodes):
        raise GateContractError(
            "ci-gate-id-duplicate",
            "gate_nodes",
            "gate identifiers must be unique",
        )
    if any(
        child not in node_by_id
        for node in registry.nodes
        for child in node.children
    ):
        raise GateContractError(
            "ci-gate-child-missing",
            "gate_nodes",
            "a registered child does not exist",
        )
    if _graph_has_cycle(node_by_id):
        raise GateContractError(
            "ci-gate-cycle",
            "gate_nodes",
            "the gate graph must be acyclic",
        )
    if profile == "ci":
        roots = tuple(job.root_gate_id for job in registry.job_roots)
    else:
        matches = tuple(
            item for item in registry.profile_roots if item.profile == profile
        )
        if len(matches) != 1:
            raise GateContractError(
                "ci-gate-profile-unknown",
                "profile",
                "the selected profile is not registered",
            )
        roots = matches[0].root_gate_ids
    selected = roots if all_roots else (gate_id,)
    if gate_id is not None:
        admitted = set(_expanded_all_ids(node_by_id, roots))
        if gate_id not in admitted:
            raise GateContractError(
                "ci-gate-selection-unreachable",
                "gate",
                "the selected gate is not reachable from the profile",
            )
    return _expanded_ids(node_by_id, selected)


def _require_fields(
    record: Mapping[str, object],
    allowed: frozenset[str],
    required: set[str],
    code: str,
    path: str,
) -> None:
    if set(record) - allowed or not required.issubset(record):
        raise GateContractError(code, path, "record fields do not match the schema")


def _require_records(value: object, code: str, path: str) -> list[Mapping[str, object]]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise GateContractError(code, path, "the field must be an array of objects")
    return value


def _string(value: object, code: str, path: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise GateContractError(code, path, "the field must be a nonempty string")
    return value


def _strings(
    value: object,
    code: str,
    path: str,
    *,
    unique: bool = True,
) -> tuple[str, ...]:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or "\x00" in item for item in value)
        or (unique and len(value) != len(set(value)))
    ):
        raise GateContractError(code, path, "the field must be a unique string array")
    return tuple(value)


def _relative_path(value: object, code: str, path: str, *, dot: bool = False) -> pathlib.PurePosixPath:
    source = _string(value, code, path)
    candidate = pathlib.PurePosixPath(source)
    if candidate.is_absolute() or ".." in candidate.parts or (source == "." and not dot) or candidate.as_posix() != source:
        raise GateContractError(code, path, "the field must be a canonical repository path")
    return candidate


def _parse_node(record: Mapping[str, object], path: str) -> GateNode:
    gate_id = _string(record.get("gate_id"), "ci-gate-node-value", path)
    if not _IDENTIFIER.fullmatch(gate_id):
        raise GateContractError(
            "ci-gate-node-value",
            path,
            "the gate identifier is invalid",
        )
    try:
        kind = GateKind(record.get("kind"))
    except (TypeError, ValueError):
        raise GateContractError("ci-gate-kind", path, "the gate kind is invalid") from None
    common = {"gate_id", "kind", "profiles", "opaque"}
    if kind is GateKind.AGGREGATE:
        _require_fields(record, frozenset(common | {"children"}), common | {"children"}, "ci-gate-kind-fields", path)
        children = _strings(record["children"], "ci-gate-children", path)
        if not children or record["opaque"] is not False:
            raise GateContractError("ci-gate-kind-fields", path, "aggregate fields are invalid")
        return GateNode(gate_id, kind, None, None, (), None, (), None, _profiles(record["profiles"], path), False, children)
    execution = common | {"entrypoint", "argv", "cwd", "allowed_env_keys", "timeout_minutes"}
    required = execution | ({"suite_key"} if kind is GateKind.LEAF else set())
    _require_fields(record, frozenset(required), required, "ci-gate-kind-fields", path)
    opaque = record["opaque"]
    if opaque is not (kind is GateKind.LEAF):
        raise GateContractError("ci-gate-kind-fields", path, "executable gate fields are invalid")
    timeout = record["timeout_minutes"]
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 60:
        raise GateContractError("ci-gate-timeout", path, "the timeout is invalid")
    env_keys = _strings(record["allowed_env_keys"], "ci-gate-env", path)
    if any(
        not _ENV_KEY.fullmatch(key)
        or _SECRET_ENV_SHAPE.search(key)
        or key not in _ADMITTED_ENV_KEYS
        for key in env_keys
    ):
        raise GateContractError("ci-gate-env", path, "an environment key is not admitted")
    suite_key = _string(record["suite_key"], "ci-gate-suite-key", path) if kind is GateKind.LEAF else None
    if suite_key is not None and gate_id != f"leaf.{suite_key}":
        raise GateContractError("ci-gate-suite-id", path, "leaf identity must match its suite key")
    return GateNode(
        gate_id,
        kind,
        suite_key,
        _relative_path(record["entrypoint"], "ci-gate-entrypoint", path),
        _strings(record["argv"], "ci-gate-argv", path, unique=False),
        _relative_path(record["cwd"], "ci-gate-cwd", path, dot=True),
        env_keys,
        timeout,
        _profiles(record["profiles"], path),
        opaque,
        (),
    )


def _profiles(value: object, path: str) -> tuple[str, ...]:
    profiles = _strings(value, "ci-gate-profiles", path)
    if any(profile not in _NODE_PROFILES for profile in profiles) or profiles != tuple(profile for profile in _NODE_PROFILES if profile in profiles):
        raise GateContractError("ci-gate-profiles", path, "node profiles are invalid")
    return profiles


def _parse_job_root(record: Mapping[str, object], path: str) -> JobRoot:
    fields = frozenset({"workflow", "job_id", "root_gate_id", "classification"})
    _require_fields(record, fields, set(fields), "ci-gate-job-fields", path)
    return JobRoot(
        _string(record["workflow"], "ci-gate-job-value", path),
        _string(record["job_id"], "ci-gate-job-value", path),
        _string(record["root_gate_id"], "ci-gate-job-value", path),
        _string(record["classification"], "ci-gate-job-value", path),
    )


def _parse_profile_root(record: Mapping[str, object], path: str) -> ProfileRoot:
    fields = frozenset({"profile", "root_gate_ids", "classification"})
    _require_fields(record, fields, set(fields), "ci-gate-profile-fields", path)
    profile = _string(record["profile"], "ci-gate-profile-value", path)
    classification = _string(
        record["classification"],
        "ci-gate-profile-value",
        path,
    )
    if profile not in _EXPECTED_PROFILE_ROOTS or classification != "local":
        raise GateContractError(
            "ci-gate-profile-classification",
            path,
            "the local profile classification is invalid",
        )
    return ProfileRoot(
        profile,
        _strings(record["root_gate_ids"], "ci-gate-profile-value", path),
        classification,
    )


def _expanded_all_ids(node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    pending = list(reversed(roots))
    while pending:
        gate_id = pending.pop()
        if gate_id in seen:
            continue
        if gate_id not in node_by_id:
            raise GateContractError(
                "ci-gate-child-missing",
                "gate_nodes",
                "a registered root or child does not exist",
            )
        seen.add(gate_id)
        ordered.append(gate_id)
        pending.extend(reversed(node_by_id[gate_id].children))
    return tuple(ordered)


def _expanded_ids(node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        gate_id
        for gate_id in _expanded_all_ids(node_by_id, roots)
        if node_by_id[gate_id].kind is not GateKind.AGGREGATE
    )


def _graph_has_cycle(node_by_id: Mapping[str, GateNode]) -> bool:
    state: dict[str, int] = {}
    for start in node_by_id:
        if state.get(start, 0) != 0:
            continue
        state[start] = 1
        stack: list[tuple[str, int]] = [(start, 0)]
        while stack:
            gate_id, child_index = stack[-1]
            children = node_by_id[gate_id].children
            if child_index >= len(children):
                state[gate_id] = 2
                stack.pop()
                continue
            child = children[child_index]
            stack[-1] = (gate_id, child_index + 1)
            child_state = state.get(child, 0)
            if child_state == 1:
                return True
            if child_state == 0:
                state[child] = 1
                stack.append((child, 0))
    return False


def _topological_ids(node_by_id: Mapping[str, GateNode]) -> tuple[str, ...]:
    indegree = {gate_id: 0 for gate_id in node_by_id}
    for node in node_by_id.values():
        for child in node.children:
            indegree[child] += 1
    pending = [
        gate_id
        for gate_id in node_by_id
        if indegree[gate_id] == 0
    ]
    ordered: list[str] = []
    index = 0
    while index < len(pending):
        gate_id = pending[index]
        index += 1
        ordered.append(gate_id)
        for child in node_by_id[gate_id].children:
            indegree[child] -= 1
            if indegree[child] == 0:
                pending.append(child)
    return tuple(ordered)


def _bounded_path_counts(
    node_by_id: Mapping[str, GateNode],
    topological_ids: tuple[str, ...],
    root: str,
) -> dict[str, int]:
    counts = {root: 1}
    for gate_id in topological_ids:
        count = counts.get(gate_id, 0)
        if not count:
            continue
        for child in node_by_id[gate_id].children:
            counts[child] = min(2, counts.get(child, 0) + count)
    return counts


def _json_depth_within_limit(source: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for character in source:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > _MAX_JSON_DEPTH:
                return False
        elif character in "]}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not in_string


def _tracked_regular_file(root: pathlib.Path, path: pathlib.PurePosixPath) -> bool:
    candidate = root.joinpath(*path.parts)
    try:
        if not _path_without_symlinks(root, path) or not candidate.is_file():
            return False
        environment = {
            "PATH": os.defpath,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
        }
        result = subprocess.run(
            [
                "git",
                "--literal-pathspecs",
                "ls-files",
                "--error-unmatch",
                "--",
                path.as_posix(),
            ],
            cwd=root,
            capture_output=True,
            check=False,
            env=environment,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _canonical_directory(root: pathlib.Path, path: pathlib.PurePosixPath) -> bool:
    candidate = root if path.as_posix() == "." else root.joinpath(*path.parts)
    try:
        return not candidate.is_symlink() and candidate.is_dir() and candidate.resolve() == candidate
    except OSError:
        return False


def _path_without_symlinks(
    root: pathlib.Path,
    path: pathlib.PurePosixPath,
) -> bool:
    candidate = root
    try:
        for part in path.parts:
            if part == ".":
                continue
            candidate = candidate / part
            if candidate.is_symlink():
                return False
        return True
    except OSError:
        return False
