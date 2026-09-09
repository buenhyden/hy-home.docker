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

import yaml

from scripts.lib.document_governance.frontmatter import safe_load_unique

# One bootstrap step per job: the workflow contract admits exactly one
# dependency install before the gate program, and `pre-commit` is now a
# gate leaf rather than a job of its own, so both requirement files install
# together here.
CI_DEPENDENCY_BOOTSTRAP = (
    "python3 -m pip install -r scripts/requirements.txt"
    " -r scripts/requirements-pre-commit.txt"
)
_CONTRACT_PATH = pathlib.PurePosixPath(".github/workflow-contract.yml")
_MAX_CONTRACT_BYTES = 1024 * 1024
_MAX_JSON_DEPTH = 256
_MAX_GATE_NODES = 2048
_MAX_GATE_EDGES = 8192
_GIT_TIMEOUT_SECONDS = 5
MAX_MANIFEST_BYTES = 1_048_576
MAX_MANIFEST_DEPTH = 64
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
_MAX_EXECUTION_ARGV = 8
_MAX_ARGUMENT_LENGTH = 64
_LONG_OPTION = re.compile(r"^--[a-z][a-z0-9-]*$")
_ARGUMENT_VALUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_REJECTED_OPTIONS = frozenset({"--help"})
_COMPLETE_CAPABILITY_ARGV = {
    "check-agent-governance-contract.py": (
        "--mode",
        "repository",
        "--section",
        "all",
    ),
    "check-document-links.py": ("--mode", "all"),
    "check-document-metadata.py": ("--mode", "check-changed"),
    "check-supply-chain-policy.py": ("--check",),
    "rehearse-postgres-logical-upgrade.sh": ("--check-config-only",),
    "report-provider-hook-parity.sh": ("--check",),
}
_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "workflows",
        "gate_nodes",
        "public_gate",
        "actions",
    }
)
_OPTIONAL_CHANGED_ROOT_GATE_IDS = (
    "ci.frontend-quality",
    "ci.storybook-coverage",
)
_LOCAL_AGGREGATE_CHILDREN = {
    "local.document-corpus-lifecycle": (
        "leaf.local-document-corpus-lifecycle-tests",
        "leaf.local-document-metadata-tests",
        "leaf.local-hook-rule-tests",
        "leaf.local-document-corpus-lifecycle",
        "leaf.document-lifecycle-regressions",
        "leaf.document-governance-library-regressions",
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
        "leaf.supply-chain-fixture-policy",
        "leaf.supply-chain-deterministic-policy",
        "leaf.supply-chain-summary-freshness",
    ),
    "local.compose-validation": (
        "leaf.compose-validation",
        "leaf.postgres-logical-upgrade-config",
    ),
    "local.infrastructure-hardening": ("leaf.infrastructure-hardening",),
    "local.template-security-baseline": (
        "leaf.template-security-baseline",
        # Added 2026-08-29. Carries the failing-case suite for both Compose
        # baseline gates into the local profiles.
        "leaf.compose-baseline-regressions",
    ),
    "local.quickwin-baseline": ("leaf.quickwin-baseline",),
}
_REQUIRED_ACTIVE_AGGREGATE_CHILDREN = {
    "ci.agent-output-eval-fixture-gate": (
        "leaf.agent-output-eval-fixture-regressions",
        "leaf.agent-output-eval-fixture-gate",
    ),
    "ci.dependency-vulnerability-audit": ("leaf.dependency-vulnerability-audit",),
    "ci.docs-traceability": ("leaf.docs-traceability",),
    "ci.frontend-quality": (
        "setup.frontend-node-dependencies",
        "leaf.frontend-lint",
        "leaf.frontend-typecheck",
        "leaf.frontend-build",
        "leaf.frontend-quality",
    ),
    "ci.git-flow-contract": ("leaf.git-flow-contract",),
    "ci.storybook-coverage": (
        "setup.frontend-node-dependencies",
        "setup.storybook-playwright",
        "leaf.storybook-coverage",
    ),
    "ci.zizmor": ("leaf.zizmor",),
}
_SETUP_PREREQUISITES = {
    "setup.storybook-playwright": ("setup.frontend-node-dependencies",),
    "leaf.frontend-lint": ("setup.frontend-node-dependencies",),
    "leaf.frontend-typecheck": ("setup.frontend-node-dependencies",),
    "leaf.frontend-build": ("setup.frontend-node-dependencies",),
    "leaf.frontend-quality": ("setup.frontend-node-dependencies",),
    "leaf.storybook-coverage": (
        "setup.frontend-node-dependencies",
        "setup.storybook-playwright",
    ),
}
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_ENV_KEY = re.compile(r"[A-Z_][A-Z0-9_]*\Z")
_ADMITTED_ENV_KEYS = frozenset(
    # Exactly the keys some gate node declares. The runner reads EVENT_NAME,
    # PR_BASE_SHA, and PUSH_BEFORE_SHA from its own controller environment, so
    # they are not admitted here; a node that needs one is added deliberately.
    {
        "CI",
        "GITHUB_ACTIONS",
        "HEAD_REF",
        "PR_TITLE",
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


class ManifestContractError(ValueError):
    """Raised when the bounded script-manifest input cannot be trusted."""


def load_manifest_document(path: pathlib.Path) -> object:
    """Read the manifest through one bounded, no-follow YAML boundary."""

    def snapshot(value: os.stat_result) -> tuple[int, ...]:
        return (
            value.st_dev,
            value.st_ino,
            value.st_mode,
            value.st_size,
            value.st_mtime_ns,
            value.st_ctime_ns,
        )

    def ancestor_snapshot(value: os.stat_result) -> tuple[int, ...]:
        return (value.st_dev, value.st_ino, value.st_mode)

    descriptors: list[int] = []
    try:
        absolute = path.absolute()
        if ".." in absolute.parts:
            raise ValueError("parent traversal is forbidden")
        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        parent = os.open(os.path.sep, directory_flags)
        descriptors.append(parent)
        ancestors: list[tuple[int, str, int, os.stat_result]] = []
        for name in absolute.parts[1:-1]:
            child = os.open(name, directory_flags, dir_fd=parent)
            descriptors.append(child)
            ancestors.append((parent, name, child, os.fstat(child)))
            parent = child
        before = os.stat(absolute.name, dir_fd=parent, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_MANIFEST_BYTES:
            raise ValueError("expected a bounded regular file")
        descriptor = os.open(
            absolute.name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
            dir_fd=parent,
        )
        descriptors.append(descriptor)
        if snapshot(os.fstat(descriptor)) != snapshot(before):
            raise ValueError("file changed before read")
        raw = bytearray()
        while len(raw) <= MAX_MANIFEST_BYTES:
            chunk = os.read(
                descriptor,
                min(65_536, MAX_MANIFEST_BYTES + 1 - len(raw)),
            )
            if not chunk:
                break
            raw.extend(chunk)
        if len(raw) != before.st_size or len(raw) > MAX_MANIFEST_BYTES:
            raise ValueError("file changed or exceeded its byte limit")
        if snapshot(os.fstat(descriptor)) != snapshot(before) or snapshot(
            os.stat(absolute.name, dir_fd=parent, follow_symlinks=False)
        ) != snapshot(before):
            raise ValueError("file changed during read")
        for ancestor, name, child, expected in ancestors:
            if ancestor_snapshot(os.fstat(child)) != ancestor_snapshot(
                expected
            ) or ancestor_snapshot(
                os.stat(name, dir_fd=ancestor, follow_symlinks=False)
            ) != ancestor_snapshot(expected):
                raise ValueError("ancestor changed during read")
        source = raw.decode("utf-8")
        depth = 0
        for event in yaml.parse(source):
            if isinstance(event, yaml.events.AliasEvent) or getattr(
                event, "anchor", None
            ):
                raise ValueError("YAML aliases and anchors are forbidden")
            if isinstance(
                event,
                (yaml.events.MappingStartEvent, yaml.events.SequenceStartEvent),
            ):
                depth += 1
                if depth > MAX_MANIFEST_DEPTH:
                    raise ValueError("YAML depth limit exceeded")
            elif isinstance(
                event,
                (yaml.events.MappingEndEvent, yaml.events.SequenceEndEvent),
            ):
                depth -= 1
        return safe_load_unique(source)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, RecursionError) as error:
        raise ManifestContractError(f"manifest input is invalid: {error}") from error
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def validate_public_execution_argv(
    path: pathlib.PurePosixPath, argv: tuple[str, ...]
) -> None:
    """Admit bounded public-validator arguments and complete modal capability."""

    if len(argv) > _MAX_EXECUTION_ARGV:
        raise GateContractError(
            "ci-gate-validator-arguments",
            path.as_posix(),
            f"execution arguments must not exceed {_MAX_EXECUTION_ARGV} tokens",
        )
    seen: set[str] = set()
    expects_value = False
    for token in argv:
        if not token or len(token) > _MAX_ARGUMENT_LENGTH:
            raise GateContractError(
                "ci-gate-validator-arguments",
                path.as_posix(),
                "execution argument has an unbounded length",
            )
        if token.startswith("--"):
            if not _LONG_OPTION.match(token) or token in _REJECTED_OPTIONS:
                raise GateContractError(
                    "ci-gate-validator-arguments",
                    path.as_posix(),
                    f"{token!r} is not an admitted long option",
                )
            if token in seen:
                raise GateContractError(
                    "ci-gate-validator-arguments",
                    path.as_posix(),
                    f"{token!r} is repeated",
                )
            seen.add(token)
            expects_value = True
            continue
        if token.startswith("-"):
            raise GateContractError(
                "ci-gate-validator-arguments",
                path.as_posix(),
                "short options are not admitted",
            )
        if not expects_value or not _ARGUMENT_VALUE.match(token):
            raise GateContractError(
                "ci-gate-validator-arguments",
                path.as_posix(),
                f"{token!r} is not a safe long-option value",
            )
        expects_value = False

    complete = _COMPLETE_CAPABILITY_ARGV.get(path.name)
    if complete is not None and argv != complete:
        raise GateContractError(
            "ci-gate-validator-arguments",
            path.as_posix(),
            "execution arguments must preserve the complete validation capability",
        )


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
    opaque: bool
    children: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class GateRegistry:
    nodes: tuple[GateNode, ...]
    public_roots: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class PublicSuiteRoute:
    name: str
    root_gate_ids: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class PublicValidatorRoute:
    suite: str
    gate_id: str
    entrypoint: pathlib.PurePosixPath
    argv: tuple[str, ...]
    contexts: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class ChangedSuiteRule:
    prefixes: tuple[str, ...]
    suites: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class ChangedRootRule:
    prefixes: tuple[str, ...]
    root_gate_ids: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class PublicGateContract:
    profile_names: tuple[str, ...]
    suites: tuple[PublicSuiteRoute, ...]
    validators: tuple[PublicValidatorRoute, ...]
    changed_rules: tuple[ChangedSuiteRule, ...]
    changed_root_rules: tuple[ChangedRootRule, ...]
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
    _require_fields(
        document,
        _TOP_LEVEL_FIELDS,
        {"schema_version", "gate_nodes"},
        "ci-gate-document-fields",
        path,
    )
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
    public = parse_public_gate_contract(document)
    public_roots = public_root_gate_ids(
        public,
        public.suite_names,
    )
    return GateRegistry(nodes, public_roots)


def parse_public_gate_contract(
    document: Mapping[str, object],
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
                "validators",
                "changed_path_rules",
                "changed_root_rules",
                "changed_fallback_suites",
            }
        ),
        frozenset(
            {
                "profiles",
                "suite_roots",
                "validators",
                "changed_path_rules",
                "changed_root_rules",
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
    if not isinstance(raw_roots, Mapping) or tuple(raw_roots) != PUBLIC_SUITE_NAMES:
        raise GateContractError(
            "ci-gate-public-suites",
            "public_gate/suite_roots",
            "public suite roots must match the exact canonical suite order",
        )
    node_ids = {
        record.get("gate_id")
        for record in document.get("gate_nodes", ())
        if isinstance(record, Mapping)
    }
    routes: list[PublicSuiteRoute] = []
    assigned_roots: set[str] = set()
    for name in PUBLIC_SUITE_NAMES:
        roots = _strings(
            raw_roots[name],
            "ci-gate-public-suite-roots",
            f"public_gate/suite_roots/{name}",
        )
        if (
            not roots
            or len(roots) != len(set(roots))
            or any(root not in node_ids or root in assigned_roots for root in roots)
        ):
            raise GateContractError(
                "ci-gate-public-suite-roots",
                f"public_gate/suite_roots/{name}",
                "public suite roots must be nonempty, unique, and registered",
            )
        assigned_roots.update(roots)
        routes.append(PublicSuiteRoute(name, roots))

    raw_validators = _require_records(
        raw["validators"],
        "ci-gate-public-validators",
        "public_gate/validators",
    )
    validators: list[PublicValidatorRoute] = []
    seen_gate_ids: set[str] = set()
    seen_entrypoints: set[pathlib.PurePosixPath] = set()
    for index, record in enumerate(raw_validators):
        validator_path = f"public_gate/validators[{index}]"
        fields = frozenset({"suite", "gate_id", "entrypoint", "argv", "contexts"})
        _require_fields(
            record,
            fields,
            set(fields),
            "ci-gate-public-validators",
            validator_path,
        )
        suite = _string(record["suite"], "ci-gate-public-validators", validator_path)
        gate_id = _string(
            record["gate_id"], "ci-gate-public-validators", validator_path
        )
        entrypoint = _relative_path(
            record["entrypoint"],
            "ci-gate-public-validators",
            validator_path,
        )
        argv = _strings(
            record["argv"],
            "ci-gate-public-validators",
            validator_path,
            unique=False,
        )
        contexts = _strings(
            record["contexts"],
            "ci-gate-public-validators",
            validator_path,
        )
        expected_contexts = tuple(
            name for name in EXECUTION_CONTEXT_NAMES if name in contexts
        )
        if (
            suite not in PUBLIC_SUITE_NAMES
            or not contexts
            or contexts != expected_contexts
            or gate_id in seen_gate_ids
            or entrypoint in seen_entrypoints
        ):
            raise GateContractError(
                "ci-gate-public-validators",
                validator_path,
                "public validators require one suite, gate, entrypoint, and canonical contexts",
            )
        validate_public_execution_argv(entrypoint, argv)
        seen_gate_ids.add(gate_id)
        seen_entrypoints.add(entrypoint)
        validators.append(
            PublicValidatorRoute(suite, gate_id, entrypoint, argv, contexts)
        )

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
            name for name in PUBLIC_SUITE_NAMES if name in suites
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

    raw_root_rules = _require_records(
        raw["changed_root_rules"],
        "ci-gate-changed-root-rules",
        "public_gate/changed_root_rules",
    )
    root_rules: list[ChangedRootRule] = []
    seen_root_prefixes: set[str] = set()
    covered_optional_roots: set[str] = set()
    for index, record in enumerate(raw_root_rules):
        rule_path = f"public_gate/changed_root_rules[{index}]"
        fields = frozenset({"prefixes", "root_gate_ids"})
        _require_fields(
            record,
            fields,
            fields,
            "ci-gate-changed-root-rules",
            rule_path,
        )
        prefixes = _strings(
            record["prefixes"],
            "ci-gate-changed-root-rules",
            f"{rule_path}/prefixes",
        )
        root_gate_ids = _strings(
            record["root_gate_ids"],
            "ci-gate-changed-root-rules",
            f"{rule_path}/root_gate_ids",
        )
        expected_root_order = tuple(
            gate_id
            for gate_id in _OPTIONAL_CHANGED_ROOT_GATE_IDS
            if gate_id in root_gate_ids
        )
        if (
            not prefixes
            or not root_gate_ids
            or seen_root_prefixes.intersection(prefixes)
            or root_gate_ids != expected_root_order
            or any(not _valid_changed_prefix(prefix) for prefix in prefixes)
            or any(
                not any(
                    _matches_changed_prefix(prefix.removesuffix("/"), known)
                    for known in seen_prefixes
                )
                for prefix in prefixes
            )
        ):
            raise GateContractError(
                "ci-gate-changed-root-rules",
                rule_path,
                "changed root rules require known prefixes and bounded optional roots",
            )
        seen_root_prefixes.update(prefixes)
        covered_optional_roots.update(root_gate_ids)
        root_rules.append(ChangedRootRule(prefixes, root_gate_ids))
    if covered_optional_roots != set(_OPTIONAL_CHANGED_ROOT_GATE_IDS):
        raise GateContractError(
            "ci-gate-changed-root-rules",
            "public_gate/changed_root_rules",
            "every optional changed root requires an explicit path rule",
        )

    fallback = _strings(
        raw["changed_fallback_suites"],
        "ci-gate-changed-fallback",
        "public_gate/changed_fallback_suites",
    )
    expected_fallback_order = tuple(
        name for name in PUBLIC_SUITE_NAMES if name in fallback
    )
    if not fallback or fallback != expected_fallback_order:
        raise GateContractError(
            "ci-gate-changed-fallback",
            "public_gate/changed_fallback_suites",
            "changed fallback suites must be a nonempty canonical subset",
        )
    return PublicGateContract(
        profiles,
        tuple(routes),
        tuple(validators),
        tuple(rules),
        tuple(root_rules),
        fallback,
    )


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
    *,
    changed_paths: tuple[str, ...] | None = None,
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
    roots = tuple(
        gate_id
        for route in contract.suites
        if route.name in selected
        for gate_id in route.root_gate_ids
    )
    if changed_paths is None:
        return roots
    if any(not _valid_changed_path(path) for path in changed_paths):
        raise GateContractError(
            "ci-gate-changed-path",
            "changed_paths",
            "changed paths must be canonical repository-relative paths",
        )
    if any(
        not any(
            _matches_changed_prefix(path, prefix)
            for rule in contract.changed_rules
            for prefix in rule.prefixes
        )
        for path in changed_paths
    ):
        return roots
    selected_optional_roots = {
        gate_id
        for rule in contract.changed_root_rules
        if any(
            _matches_changed_prefix(path, prefix)
            for path in changed_paths
            for prefix in rule.prefixes
        )
        for gate_id in rule.root_gate_ids
    }
    return tuple(
        gate_id
        for gate_id in roots
        if gate_id not in _OPTIONAL_CHANGED_ROOT_GATE_IDS
        or gate_id in selected_optional_roots
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

    node_by_id = {node.gate_id: node for node in registry.nodes}
    if len(node_by_id) != len(registry.nodes):
        finding(
            "ci-gate-id-duplicate",
            "gate_nodes",
            "gate identifiers must be unique",
        )
        return tuple(findings)
    roots = registry.public_roots
    missing_active_roots = (set(_REQUIRED_ACTIVE_AGGREGATE_CHILDREN) - set(roots)) | (
        set(_REQUIRED_ACTIVE_AGGREGATE_CHILDREN) - set(node_by_id)
    )
    if missing_active_roots:
        finding(
            "ci-gate-active-aggregate-root",
            "public_gate",
            "every active CI aggregate must remain a registered public root",
        )
        return tuple(findings)
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

    aggregate_violation = _active_aggregate_child_violation(node_by_id)
    if aggregate_violation is not None:
        aggregate, child = aggregate_violation
        finding(
            "ci-gate-active-aggregate-child",
            f"gate_nodes/{aggregate}",
            f"{aggregate} must retain required child {child}",
        )
        return tuple(findings)

    setup_violation = _setup_prerequisite_violation(node_by_id, roots)
    if setup_violation is not None:
        root_gate_id, prerequisite, consumer = setup_violation
        finding(
            "ci-gate-setup-prerequisite",
            f"gate_nodes/{root_gate_id}",
            f"{prerequisite} must precede {consumer} on every public route",
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
        return tuple(findings)

    for gate_id, expected_children in _LOCAL_AGGREGATE_CHILDREN.items():
        if node_by_id[gate_id].children != expected_children:
            finding(
                "ci-gate-local-aggregate-children",
                f"gate_nodes/{gate_id}",
                "local aggregates must retain their exact ordered children",
            )
            return tuple(findings)

    tracked_files: dict[pathlib.PurePosixPath, bool] = {}
    canonical_directories: dict[pathlib.PurePosixPath, bool] = {}
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


def expand_public_gate_ids(
    registry: GateRegistry,
    root_gate_ids: tuple[str, ...],
) -> tuple[str, ...]:
    if (
        not root_gate_ids
        or len(root_gate_ids) != len(set(root_gate_ids))
        or any(gate_id not in registry.public_roots for gate_id in root_gate_ids)
    ):
        raise GateContractError(
            "ci-gate-public-roots",
            "public_gate",
            "selected roots must be unique registered public roots",
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
        child not in node_by_id for node in registry.nodes for child in node.children
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
    aggregate_violation = _active_aggregate_child_violation(node_by_id)
    if aggregate_violation is not None:
        aggregate, child = aggregate_violation
        raise GateContractError(
            "ci-gate-active-aggregate-child",
            f"gate_nodes/{aggregate}",
            f"{aggregate} must retain required child {child}",
        )
    setup_violation = _setup_prerequisite_violation(node_by_id, root_gate_ids)
    if setup_violation is not None:
        root_gate_id, prerequisite, consumer = setup_violation
        raise GateContractError(
            "ci-gate-setup-prerequisite",
            f"gate_nodes/{root_gate_id}",
            f"{prerequisite} must precede {consumer} on every public route",
        )
    return _expanded_ids(node_by_id, root_gate_ids)


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


def _relative_path(
    value: object, code: str, path: str, *, dot: bool = False
) -> pathlib.PurePosixPath:
    source = _string(value, code, path)
    candidate = pathlib.PurePosixPath(source)
    if (
        candidate.is_absolute()
        or ".." in candidate.parts
        or (source == "." and not dot)
        or candidate.as_posix() != source
    ):
        raise GateContractError(
            code, path, "the field must be a canonical repository path"
        )
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
        raise GateContractError(
            "ci-gate-kind", path, "the gate kind is invalid"
        ) from None
    common = {"gate_id", "kind", "opaque"}
    if kind is GateKind.AGGREGATE:
        _require_fields(
            record,
            frozenset(common | {"children"}),
            common | {"children"},
            "ci-gate-kind-fields",
            path,
        )
        children = _strings(record["children"], "ci-gate-children", path)
        if not children or record["opaque"] is not False:
            raise GateContractError(
                "ci-gate-kind-fields", path, "aggregate fields are invalid"
            )
        return GateNode(
            gate_id,
            kind,
            None,
            None,
            (),
            None,
            (),
            None,
            False,
            children,
        )
    execution = common | {
        "entrypoint",
        "argv",
        "cwd",
        "allowed_env_keys",
        "timeout_minutes",
    }
    required = execution | ({"suite_key"} if kind is GateKind.LEAF else set())
    _require_fields(record, frozenset(required), required, "ci-gate-kind-fields", path)
    opaque = record["opaque"]
    if opaque is not (kind is GateKind.LEAF):
        raise GateContractError(
            "ci-gate-kind-fields", path, "executable gate fields are invalid"
        )
    timeout = record["timeout_minutes"]
    if (
        not isinstance(timeout, int)
        or isinstance(timeout, bool)
        or not 1 <= timeout <= 60
    ):
        raise GateContractError("ci-gate-timeout", path, "the timeout is invalid")
    env_keys = _strings(record["allowed_env_keys"], "ci-gate-env", path)
    if any(
        not _ENV_KEY.fullmatch(key)
        or _SECRET_ENV_SHAPE.search(key)
        or key not in _ADMITTED_ENV_KEYS
        for key in env_keys
    ):
        raise GateContractError(
            "ci-gate-env", path, "an environment key is not admitted"
        )
    suite_key = (
        _string(record["suite_key"], "ci-gate-suite-key", path)
        if kind is GateKind.LEAF
        else None
    )
    if suite_key is not None and gate_id != f"leaf.{suite_key}":
        raise GateContractError(
            "ci-gate-suite-id", path, "leaf identity must match its suite key"
        )
    return GateNode(
        gate_id,
        kind,
        suite_key,
        _relative_path(record["entrypoint"], "ci-gate-entrypoint", path),
        _strings(record["argv"], "ci-gate-argv", path, unique=False),
        _relative_path(record["cwd"], "ci-gate-cwd", path, dot=True),
        env_keys,
        timeout,
        opaque,
        (),
    )


def _expanded_all_ids(
    node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]
) -> tuple[str, ...]:
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


def _expanded_ids(
    node_by_id: Mapping[str, GateNode], roots: tuple[str, ...]
) -> tuple[str, ...]:
    return tuple(
        gate_id
        for gate_id in _expanded_all_ids(node_by_id, roots)
        if node_by_id[gate_id].kind is not GateKind.AGGREGATE
    )


def _setup_prerequisite_violation(
    node_by_id: Mapping[str, GateNode],
    roots: tuple[str, ...],
) -> tuple[str, str, str] | None:
    for root_gate_id in roots:
        ordered = _expanded_ids(node_by_id, (root_gate_id,))
        positions = {gate_id: index for index, gate_id in enumerate(ordered)}
        for consumer, prerequisites in _SETUP_PREREQUISITES.items():
            consumer_index = positions.get(consumer)
            if consumer_index is None:
                continue
            for prerequisite in prerequisites:
                prerequisite_index = positions.get(prerequisite)
                if prerequisite_index is None or prerequisite_index >= consumer_index:
                    return root_gate_id, prerequisite, consumer
    return None


def _active_aggregate_child_violation(
    node_by_id: Mapping[str, GateNode],
) -> tuple[str, str] | None:
    for aggregate, required_children in _REQUIRED_ACTIVE_AGGREGATE_CHILDREN.items():
        node = node_by_id.get(aggregate)
        if node is None:
            continue
        if node.kind is not GateKind.AGGREGATE:
            return aggregate, required_children[0]
        for child in required_children:
            if child not in node.children:
                return aggregate, child
    return None


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
        return (
            not candidate.is_symlink()
            and candidate.is_dir()
            and candidate.resolve() == candidate
        )
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
