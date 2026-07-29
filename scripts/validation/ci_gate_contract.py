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


_CONTRACT_PATH = pathlib.PurePosixPath(".github/workflow-contract.yml")
_MAX_CONTRACT_BYTES = 1024 * 1024
_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "workflows",
        "gate_nodes",
        "job_roots",
        "profile_roots",
        "actions",
    }
)
_NODE_PROFILES = (
    "ci",
    "local-script-backed",
    "local-harness",
    "local-all-profiles",
)
_REQUIRED_JOB_ROOTS = {
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
_REQUIRED_JOB_SUITES = {
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


def load_contract_document(root: pathlib.Path) -> dict[str, object]:
    root = pathlib.Path(root)
    if (
        not root.is_absolute()
        or ".." in root.parts
        or pathlib.Path(root.resolve(strict=False)) != root
    ):
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
    try:
        root_descriptor = os.open(root, directory_flags)
        github_descriptor = os.open(
            ".github",
            directory_flags,
            dir_fd=root_descriptor,
        )
        try:
            file_descriptor = os.open(
                "workflow-contract.yml",
                os_flags,
                dir_fd=github_descriptor,
            )
        except OSError as error:
            if error.errno == errno.ELOOP:
                raise GateContractError(
                    "ci-gate-input-symlink",
                    _CONTRACT_PATH.as_posix(),
                    "the contract input must not be a symbolic link",
                ) from None
            raise
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
    finally:
        for descriptor in (
            file_descriptor,
            github_descriptor,
            root_descriptor,
        ):
            if descriptor >= 0:
                os.close(descriptor)

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
    except (json.JSONDecodeError, ValueError):
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
    if document["schema_version"] != 2 or isinstance(document["schema_version"], bool):
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
    nodes = tuple(
        _parse_node(record, f"{path}#gate_nodes[{index}]")
        for index, record in enumerate(raw_nodes)
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


def validate_gate_registry(
    root: pathlib.Path,
    registry: GateRegistry,
) -> tuple[GateFinding, ...]:
    findings: list[GateFinding] = []

    def finding(code: str, path: str, message: str) -> None:
        findings.append(GateFinding(code, path, message))

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
            "the required quality jobs must map to the exact sixteen roots",
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

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(gate_id: str) -> bool:
        if gate_id in visiting:
            return True
        if gate_id in visited:
            return False
        visiting.add(gate_id)
        if any(visit(child) for child in node_by_id[gate_id].children):
            return True
        visiting.remove(gate_id)
        visited.add(gate_id)
        return False

    if any(visit(node.gate_id) for node in registry.nodes):
        finding(
            "ci-gate-cycle",
            "gate_nodes",
            "the gate graph must be acyclic",
        )
        return tuple(findings)

    reachable: set[str] = set()

    def collect(gate_id: str) -> None:
        if gate_id in reachable:
            return
        reachable.add(gate_id)
        for child in node_by_id[gate_id].children:
            collect(child)

    for root_gate_id in roots:
        collect(root_gate_id)
    if reachable != set(node_by_id):
        finding(
            "ci-gate-orphan",
            "gate_nodes",
            "every gate must be reachable from a registered root",
        )
        return tuple(findings)

    leaves = [node for node in registry.nodes if node.kind is GateKind.LEAF]
    suites = [node.suite_key for node in leaves]
    duplicate_suites = {
        suite_key for suite_key in suites if suites.count(suite_key) > 1
    }
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

    for job in registry.job_roots:
        path_counts: dict[str, int] = {}

        def count_paths(gate_id: str) -> None:
            node = node_by_id[gate_id]
            if node.kind is GateKind.LEAF:
                if node.suite_key is not None:
                    path_counts[node.suite_key] = (
                        path_counts.get(node.suite_key, 0) + 1
                    )
                return
            for child in node.children:
                count_paths(child)

        count_paths(job.root_gate_id)
        if any(count > 1 for count in path_counts.values()):
            finding(
                "ci-gate-suite-reachable-duplicate",
                "job_roots",
                "a semantic suite is reachable more than once from a workflow",
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
    ):
        finding(
            "ci-gate-profile-roots",
            "profile_roots",
            "local profile roots must match the exact ordered projections",
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
        if not _tracked_regular_file(root, node.entrypoint):
            finding(
                "ci-gate-entrypoint-invalid",
                f"gate_nodes/{node.gate_id}",
                "entrypoints must be tracked canonical first-party files",
            )
        if not _canonical_directory(root, node.cwd):
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
    node_by_id = {node.gate_id: node for node in registry.nodes}
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
    if any(not _ENV_KEY.fullmatch(key) or _SECRET_ENV_SHAPE.search(key) for key in env_keys):
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
    return ProfileRoot(
        _string(record["profile"], "ci-gate-profile-value", path),
        _strings(record["root_gate_ids"], "ci-gate-profile-value", path),
        _string(record["classification"], "ci-gate-profile-value", path),
    )


def _expanded_all_ids(node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()

    def walk(gate_id: str) -> None:
        if gate_id in seen:
            return
        seen.add(gate_id)
        ordered.append(gate_id)
        for child in node_by_id[gate_id].children:
            walk(child)

    for root in roots:
        walk(root)
    return tuple(ordered)


def _expanded_ids(node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        gate_id
        for gate_id in _expanded_all_ids(node_by_id, roots)
        if node_by_id[gate_id].kind is not GateKind.AGGREGATE
    )


def _tracked_regular_file(root: pathlib.Path, path: pathlib.PurePosixPath) -> bool:
    candidate = root.joinpath(*path.parts)
    try:
        if not _path_without_symlinks(root, path) or not candidate.is_file():
            return False
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", path.as_posix()],
            cwd=root,
            capture_output=True,
            check=False,
        )
        return result.returncode == 0
    except OSError:
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
