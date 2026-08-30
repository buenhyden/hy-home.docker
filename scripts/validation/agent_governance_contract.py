#!/usr/bin/env python3
"""Validate canonical Stage 00 sources and their two-provider projections."""

from __future__ import annotations

import fnmatch
import json
import os
import pathlib
import re
import stat
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

import yaml


GOVERNANCE = pathlib.PurePosixPath("docs/00.agent-governance")
REGISTRY = GOVERNANCE / "providers/registry.yaml"
SUPPORTED_PROVIDERS = ("claude", "codex")
ROOT_ENTRIES = ("README.md", "policies", "providers", "roles", "sdlc.md", "skills")
PROVIDER_ENTRIES = ("README.md", "claude.md", "codex.md", "registry.yaml")
GOVERNANCE_PROFILES = {
    "governance-hook-policy",
    "governance-policy",
    "governance-provider",
    "governance-provider-index",
    "governance-role",
    "governance-sdlc",
    "governance-skill",
}
EXPECTED_GENERATED_ROOTS = (
    ".agents/agents",
    ".agents/rules",
    ".agents/skills",
    ".agents/workflows",
    ".claude/agents",
    ".claude/skills",
    ".codex/agents",
)
REGISTRY_KEYS = {
    "schema_version",
    "providers",
    "compatibility",
    "canonical_sources",
    "work_profiles",
    "models",
    "model_catalog_policy",
    "permissions",
    "workflow_states",
    "semantic_events",
    "hook_contracts",
    "harness_layers",
    "harness_loops",
    "evidence_fields",
    "prohibited_evidence",
    "agent_output_eval",
    "generated_roots",
}
HARNESS_LOOPS = {
    "approved-all-files-gate",
    "bounded-implementation",
    "context-bootstrap",
    "independent-review",
}
EXPECTED_HOOK_COMMANDS = {
    "claude": {
        "SessionStart": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"',
        "PreToolUse": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/docker-compose-pre.sh"',
        "PostToolUse": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-validate.sh"',
        "Stop": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/stop.sh"',
        "SessionEnd": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh"',
        "PreCompact": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-compact.sh"',
        "UserPromptSubmit": 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/user-prompt-submit.sh"',
    },
    "codex": {
        event: (
            'HY_HOME_HOOK_PROVIDER=codex bash '
            '"${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/'
            f'agent-event-hook.sh" {event}'
        )
        for event in (
            "SessionStart",
            "PreToolUse",
            "PostToolUse",
            "Stop",
            "PreCompact",
            "UserPromptSubmit",
        )
    },
}
EXPECTED_HARNESS_LAYERS = (
    ("canonical-contract", "rules-engineer", "canonical-authority", "design-plan"),
    ("role-skill-routing", "workflow-supervisor", "registered-routing", "discover"),
    ("permission-boundary", "rules-engineer", "explicit-authority", "approval"),
    ("provider-model-policy", "eval-engineer", "native-schema-compatibility", "design-plan"),
    ("semantic-events", "hook-developer", "native-event-honesty", "implement"),
    ("controlled-validation", "qa-engineer", "deterministic-checks", "implement"),
    ("tracked-ci", "ci-cd-engineer", "least-privilege-workflow", "implement"),
    ("sanitized-evidence", "eval-engineer", "value-free-evidence", "evidence"),
)
EXPECTED_HARNESS_LOOP_VALUES = {
    "context-bootstrap": (
        "workflow-supervisor", "rules-engineer", "read-only", ("discover",), 1,
        "bootstrap-contract-pass", "escalate",
    ),
    "bounded-implementation": (
        "qa-engineer", "code-reviewer", "workspace-write", ("implement", "validate"), 2,
        "focused-checks-pass", "narrow-then-escalate",
    ),
    "independent-review": (
        "code-reviewer", "eval-engineer", "read-only", ("independent-review", "evidence"), 2,
        "critical-and-important-zero", "escalate",
    ),
    "approved-all-files-gate": (
        "qa-engineer", "code-reviewer", "workspace-write", ("validate", "evidence"), 1,
        "controlled-wrapper-pass", "record-and-stop",
    ),
}
MAX_TEXT_BYTES = 4 * 1024 * 1024
_RETIRED_PROVIDER = "ge" + "mini"
_RETIRED_EXPERIMENT = "anti" + "gravity"
_RETIRED_HANDOFF = "project" + r"[- .]?" + "memory"
_RETIRED_CURRENT = "memory" + "/current"
UNSUPPORTED_TOKEN = re.compile(
    rf"(?i)(?:\b{_RETIRED_PROVIDER}\b|\b{_RETIRED_EXPERIMENT}\b|"
    rf"{_RETIRED_HANDOFF}|{_RETIRED_CURRENT}|"
    r"docs/00\.agent-governance/(?:rules|scopes|agents|contracts)(?:/|\b)|"
    r"subagent-protocol\.md|harness-implementation-map\.md|"
    r"memory\.template\.md|progress\.template\.md)"
)
RETIRED_PROVIDER_DIRECTORY = "." + _RETIRED_PROVIDER
RETIRED_PROVIDER_SHIM = _RETIRED_PROVIDER.upper() + ".md"
GENERATED_AUTHORITY = re.compile(
    r"(?i)(?:policy source of truth|owns? policy|normative authority)"
)
HISTORICAL_QUOTE_MARKER = "> Historical evidence (not current authority; source: Git history):"
HISTORICAL_TABLE_MARKER = "<!-- Historical evidence table (not current authority; source: Git history). -->"


class ContractLoadError(ValueError):
    """Raised when a Stage 00 source cannot be loaded safely."""


class _UniqueLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: _UniqueLoader, node: yaml.MappingNode, deep: bool = False):
    pairs = loader.construct_pairs(node, deep=deep)
    result: dict[object, object] = {}
    for key, value in pairs:
        if not isinstance(key, str):
            raise yaml.YAMLError("mapping keys must be strings")
        if key in result:
            raise yaml.YAMLError(f"duplicate key: {key}")
        result[key] = value
    return result


_UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    code: str
    message: str


@dataclass(frozen=True)
class RoleRecord:
    agent_id: str
    scope: str
    tier: str
    work_profile: str
    permission_profile: str
    skill_ids: tuple[str, ...]
    source_path: pathlib.PurePosixPath
    source_text: str


@dataclass(frozen=True)
class SkillRecord:
    skill_id: str
    scope: str
    owner_agent: str
    source_path: pathlib.PurePosixPath
    source_text: str


@dataclass(frozen=True)
class ProviderRecord:
    provider_id: str
    capability_status: str
    adoption_status: str
    runtime_acceptance: str
    adapter_path: pathlib.PurePosixPath
    agent_pattern: str
    skill_pattern: str
    config_path: pathlib.PurePosixPath


@dataclass(frozen=True)
class CompatibilityRecord:
    agent_pattern: str
    skill_pattern: str


@dataclass(frozen=True)
class AgentGovernanceState:
    providers: tuple[str, ...]
    provider_records: tuple[ProviderRecord, ...]
    compatibility: CompatibilityRecord
    root_entries: tuple[str, ...]
    provider_entries: tuple[str, ...]
    roles: tuple[RoleRecord, ...]
    skills: tuple[SkillRecord, ...]
    registry: Mapping[str, object]


@dataclass(frozen=True)
class ContractBundle:
    state: AgentGovernanceState

    @property
    def registry(self) -> Mapping[str, object]:
        return self.state.registry

    @property
    def catalog(self) -> Mapping[str, object]:
        return MappingProxyType(
            {"agents": self.state.roles, "functions": self.state.skills}
        )

    @property
    def providers(self) -> Mapping[str, object]:
        return self.state.registry

    @property
    def artifacts(self) -> Mapping[str, object]:
        return MappingProxyType({})


def _safe_relative(value: str | pathlib.PurePath) -> pathlib.PurePosixPath:
    raw = pathlib.PurePosixPath(str(value).replace("\\", "/"))
    if raw.is_absolute() or not raw.parts or any(part in {"", ".", ".."} for part in raw.parts):
        raise ContractLoadError("AGC-UNSAFE-PATH")
    if any(ord(char) < 32 or ord(char) == 127 for char in raw.as_posix()):
        raise ContractLoadError("AGC-UNSAFE-PATH")
    return raw


def _read_text(root: pathlib.Path, relative: str | pathlib.PurePath) -> str:
    root = root.absolute()
    safe = _safe_relative(relative)
    current = root
    for part in safe.parts:
        current = current / part
        try:
            metadata = current.lstat()
        except OSError as error:
            raise ContractLoadError(f"AGC-FILE-MISSING path={safe}") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise ContractLoadError(f"AGC-UNSAFE-FILE path={safe}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ContractLoadError(f"AGC-UNSAFE-FILE path={safe}")
    if metadata.st_mode & 0o444 == 0:
        raise ContractLoadError(f"AGC-UNREADABLE-FILE path={safe}")
    try:
        descriptor = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as source:
            opened = os.fstat(source.fileno())
            if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
                raise ContractLoadError(f"AGC-UNSAFE-FILE path={safe}")
            payload = source.read(MAX_TEXT_BYTES + 1)
            after = os.fstat(source.fileno())
            if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise ContractLoadError(f"AGC-UNSAFE-FILE path={safe}")
    except OSError as error:
        raise ContractLoadError(f"AGC-UNREADABLE-FILE path={safe}") from error
    if len(payload) > MAX_TEXT_BYTES:
        raise ContractLoadError(f"AGC-FILE-TOO-LARGE path={safe}")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractLoadError(f"AGC-INVALID-UTF8 path={safe}") from error


def read_repository_text(root: pathlib.Path, relative_path: str) -> str:
    return _read_text(root, relative_path)


def _load_yaml(root: pathlib.Path, relative: str | pathlib.PurePath) -> Mapping[str, object]:
    try:
        value = yaml.load(_read_text(root, relative), Loader=_UniqueLoader)
    except yaml.YAMLError as error:
        raise ContractLoadError(f"AGC-YAML-INVALID path={relative}") from error
    if not isinstance(value, dict):
        raise ContractLoadError(f"AGC-YAML-MAPPING-REQUIRED path={relative}")
    return MappingProxyType(value)


def load_artifact_contract(root: pathlib.Path, path: pathlib.Path) -> Mapping[str, object]:
    """Compatibility loader for explicitly supplied legacy transition fixtures."""
    root = root.absolute()
    try:
        relative = path.absolute().relative_to(root)
    except ValueError as error:
        raise ContractLoadError("AGC-UNSAFE-PATH") from error
    return _load_yaml(root, pathlib.PurePosixPath(relative.as_posix()))


def _frontmatter(text: str, path: pathlib.PurePosixPath) -> Mapping[str, object]:
    if not text.startswith("---\n"):
        raise ContractLoadError(f"AGC-FRONTMATTER-MISSING path={path}")
    boundary = text.find("\n---\n", 4)
    if boundary < 0:
        raise ContractLoadError(f"AGC-FRONTMATTER-INVALID path={path}")
    try:
        value = yaml.load(text[4:boundary], Loader=_UniqueLoader)
    except yaml.YAMLError as error:
        raise ContractLoadError(f"AGC-FRONTMATTER-INVALID path={path}") from error
    if not isinstance(value, dict):
        raise ContractLoadError(f"AGC-FRONTMATTER-INVALID path={path}")
    return MappingProxyType(value)


def _strings(value: object, *, field: str, path: pathlib.PurePosixPath) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ContractLoadError(f"AGC-FIELD-INVALID path={path} field={field}")
    result = tuple(value)
    if len(result) != len(set(result)):
        raise ContractLoadError(f"AGC-FIELD-DUPLICATE path={path} field={field}")
    return result


def _string(values: Mapping[str, object], field: str, path: pathlib.PurePosixPath) -> str:
    value = values.get(field)
    if not isinstance(value, str) or not value:
        raise ContractLoadError(f"AGC-FIELD-INVALID path={path} field={field}")
    return value


def _mapping(value: object, *, field: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ContractLoadError(f"AGC-PROVIDER-REGISTRY-INVALID field={field}")
    return value


def _exact_keys(values: Mapping[str, object], expected: set[str], *, field: str) -> None:
    if set(values) != expected:
        raise ContractLoadError(f"AGC-PROVIDER-REGISTRY-KEYS field={field}")


def _projection_pattern(value: object, *, token: str, field: str) -> str:
    if not isinstance(value, str) or value.count("{" + token + "}") != 1:
        raise ContractLoadError(f"AGC-PROJECTION-PATTERN field={field}")
    probe = value.replace("{" + token + "}", "registered-id")
    _safe_relative(probe)
    return value


def _validate_registry(
    root: pathlib.Path,
    registry: Mapping[str, object],
    registered_roles: frozenset[str],
) -> tuple[tuple[ProviderRecord, ...], CompatibilityRecord]:
    _exact_keys(registry, REGISTRY_KEYS, field="root")
    if registry.get("schema_version") != 1:
        raise ContractLoadError("AGC-PROVIDER-REGISTRY-VERSION")
    raw_providers = registry.get("providers")
    if not isinstance(raw_providers, list) or len(raw_providers) != 2:
        raise ContractLoadError("AGC-PROVIDER-REGISTRY-INVALID field=providers")
    records: list[ProviderRecord] = []
    provider_keys = {
        "provider_id", "capability_status", "adoption_status", "runtime_acceptance",
        "adapter_path", "native_agent_pattern", "native_skill_pattern", "native_config_path",
    }
    expected_provider_values = {
        "claude": {
            "native_agent_pattern": ".claude/agents/{agent_id}.md",
            "native_skill_pattern": ".claude/skills/{skill_id}/SKILL.md",
            "native_config_path": ".claude/settings.json",
        },
        "codex": {
            "native_agent_pattern": ".codex/agents/{agent_id}.toml",
            "native_skill_pattern": ".agents/skills/{skill_id}/SKILL.md",
            "native_config_path": ".codex/hooks.json",
        },
    }
    for index, raw in enumerate(raw_providers):
        values = _mapping(raw, field=f"providers[{index}]")
        _exact_keys(values, provider_keys, field=f"providers[{index}]")
        provider_id = values.get("provider_id")
        if provider_id not in SUPPORTED_PROVIDERS or provider_id != SUPPORTED_PROVIDERS[index]:
            raise ContractLoadError("AGC-PROVIDER-REGISTRY-INVALID field=provider_id")
        if values.get("capability_status") != "supported" or values.get("adoption_status") != "adopted":
            raise ContractLoadError("AGC-PROVIDER-REGISTRY-INVALID field=status")
        if values.get("runtime_acceptance") != "needs_revalidation":
            raise ContractLoadError("AGC-PROVIDER-REGISTRY-INVALID field=runtime_acceptance")
        adapter = _safe_relative(str(values.get("adapter_path", "")))
        expected_adapter = GOVERNANCE / f"providers/{provider_id}.md"
        if adapter != expected_adapter:
            raise ContractLoadError("AGC-PROVIDER-ADAPTER-CROSS-REFERENCE")
        config = _safe_relative(str(values.get("native_config_path", "")))
        expected_values = expected_provider_values[provider_id]
        if any(values.get(key) != value for key, value in expected_values.items()):
            raise ContractLoadError("AGC-PROVIDER-PROJECTION-CROSS-REFERENCE")
        _read_text(root, config)
        records.append(ProviderRecord(
            provider_id=provider_id,
            capability_status="supported",
            adoption_status="adopted",
            runtime_acceptance="needs_revalidation",
            adapter_path=adapter,
            agent_pattern=_projection_pattern(values.get("native_agent_pattern"), token="agent_id", field="native_agent_pattern"),
            skill_pattern=_projection_pattern(values.get("native_skill_pattern"), token="skill_id", field="native_skill_pattern"),
            config_path=config,
        ))
    compatibility_values = _mapping(registry.get("compatibility"), field="compatibility")
    _exact_keys(compatibility_values, {"agent_pattern", "skill_pattern"}, field="compatibility")
    compatibility = CompatibilityRecord(
        agent_pattern=_projection_pattern(compatibility_values.get("agent_pattern"), token="agent_id", field="compatibility.agent_pattern"),
        skill_pattern=_projection_pattern(compatibility_values.get("skill_pattern"), token="skill_id", field="compatibility.skill_pattern"),
    )
    if compatibility != CompatibilityRecord(
        agent_pattern=".agents/agents/{agent_id}.md",
        skill_pattern=".agents/skills/{skill_id}/SKILL.md",
    ):
        raise ContractLoadError("AGC-COMPATIBILITY-PROJECTION-CROSS-REFERENCE")
    canonical = _mapping(registry.get("canonical_sources"), field="canonical_sources")
    _exact_keys(canonical, {"role_pattern", "skill_pattern"}, field="canonical_sources")
    if canonical != {
        "role_pattern": "docs/00.agent-governance/roles/{agent_id}.md",
        "skill_pattern": "docs/00.agent-governance/skills/{skill_id}.md",
    }:
        raise ContractLoadError("AGC-CANONICAL-SOURCE-PATTERN")
    providers = set(SUPPORTED_PROVIDERS)
    permissions = _mapping(registry.get("permissions"), field="permissions")
    if permissions != {
        "read-only": {"claude": "plan", "codex": "read-only"},
        "workspace-write": {"claude": "acceptEdits", "codex": "workspace-write"},
    }:
        raise ContractLoadError("AGC-PERMISSION-PROFILES")
    for name, raw in permissions.items():
        values = _mapping(raw, field=f"permissions.{name}")
        if set(values) != providers or any(not isinstance(item, str) or not item for item in values.values()):
            raise ContractLoadError(f"AGC-PERMISSION-PROVIDER field={name}")
    semantic_events = _mapping(registry.get("semantic_events"), field="semantic_events")
    hook_contracts = _mapping(registry.get("hook_contracts"), field="hook_contracts")
    if set(semantic_events) != providers or set(hook_contracts) != providers:
        raise ContractLoadError("AGC-HOOK-PROVIDERS")
    for provider_id in SUPPORTED_PROVIDERS:
        events = semantic_events.get(provider_id)
        contracts = _mapping(hook_contracts.get(provider_id), field=f"hook_contracts.{provider_id}")
        if (
            not isinstance(events, list)
            or not events
            or any(not isinstance(event, str) or not event for event in events)
            or len(events) != len(set(events))
            or tuple(contracts) != tuple(events)
        ):
            raise ContractLoadError(f"AGC-HOOK-EVENTS field={provider_id}")
        for event, raw_contract in contracts.items():
            contract = _mapping(raw_contract, field=f"hook_contracts.{provider_id}.{event}")
            _exact_keys(contract, {"command", "timeout", "matcher", "executable"}, field=f"hook_contracts.{provider_id}.{event}")
            if (
                not isinstance(contract.get("command"), str)
                or not contract.get("command")
                or not isinstance(contract.get("timeout"), int)
                or isinstance(contract.get("timeout"), bool)
                or not 1 <= contract["timeout"] <= 600
            ):
                raise ContractLoadError(f"AGC-HOOK-BINDING field={provider_id}.{event}")
            if contract.get("command") != EXPECTED_HOOK_COMMANDS[provider_id].get(event):
                raise ContractLoadError(
                    f"AGC-HOOK-COMMAND-TEMPLATE field={provider_id}.{event}"
                )
            if contract.get("matcher") is not None and not isinstance(contract.get("matcher"), str):
                raise ContractLoadError(f"AGC-HOOK-BINDING field={provider_id}.{event}")
            executable = _safe_relative(str(contract.get("executable", "")))
            _read_text(root, executable)
    work_profiles = _mapping(registry.get("work_profiles"), field="work_profiles")
    models = _mapping(registry.get("models"), field="models")
    if not work_profiles or not models:
        raise ContractLoadError("AGC-MODEL-SELECTION")
    selected: set[str] = set()
    for profile_name, raw in work_profiles.items():
        profile = _mapping(raw, field=f"work_profiles.{profile_name}")
        if set(profile) != providers:
            raise ContractLoadError(f"AGC-WORK-PROFILE-PROVIDERS field={profile_name}")
        for provider_id, raw_selection in profile.items():
            selection = _mapping(raw_selection, field=f"work_profiles.{profile_name}.{provider_id}")
            _exact_keys(selection, {"model", "control", "value"}, field=f"work_profiles.{profile_name}.{provider_id}")
            model_id = selection.get("model")
            model = models.get(model_id) if isinstance(model_id, str) else None
            if (
                not isinstance(model, dict)
                or model.get("provider") != provider_id
                or (
                    model.get("control") != "unsupported"
                    and model.get("control") != selection.get("control")
                )
            ):
                raise ContractLoadError(f"AGC-MODEL-SELECTION field={profile_name}.{provider_id}")
            value = selection.get("value")
            if model.get("control") == "unsupported":
                if value is not None or selection.get("control") != "effort":
                    raise ContractLoadError(f"AGC-MODEL-SELECTION field={profile_name}.{provider_id}")
            elif (
                value not in model.get("supported_values", [])
                or selection.get("control") != model.get("control")
            ):
                raise ContractLoadError(f"AGC-MODEL-SELECTION field={profile_name}.{provider_id}")
            selected.add(model_id)
    if selected != set(models):
        raise ContractLoadError("AGC-MODEL-SELECTION")
    for model_id, raw in models.items():
        model = _mapping(raw, field=f"models.{model_id}")
        expected_model_keys = {
            "provider", "lifecycle", "entitlement", "runtime_acceptance",
            "control", "work_profiles", "source_url",
        }
        if model.get("control") != "unsupported":
            expected_model_keys.add("supported_values")
        _exact_keys(model, expected_model_keys, field=f"models.{model_id}")
        if model.get("provider") not in providers:
            raise ContractLoadError(f"AGC-MODEL-PROVIDER field={model_id}")
        if model.get("runtime_acceptance") != "needs_revalidation" or model.get("entitlement") != "needs_revalidation":
            raise ContractLoadError(f"AGC-MODEL-STATUS field={model_id}")
        listed = model.get("work_profiles")
        if not isinstance(listed, list) or set(listed) != {
            name for name, profile in work_profiles.items()
            if isinstance(profile, dict) and isinstance(profile.get(model.get("provider")), dict)
            and profile[model["provider"]].get("model") == model_id
        }:
            raise ContractLoadError(f"AGC-MODEL-WORK-PROFILES field={model_id}")
        if model.get("lifecycle") != "stable" or not isinstance(model.get("source_url"), str):
            raise ContractLoadError(f"AGC-MODEL-STATUS field={model_id}")
        supported_values = model.get("supported_values")
        if model.get("control") == "unsupported":
            if "supported_values" in model:
                raise ContractLoadError(f"AGC-MODEL-CONTROL field={model_id}")
        elif (
            not isinstance(supported_values, list)
            or not supported_values
            or any(not isinstance(item, str) or not item for item in supported_values)
            or len(supported_values) != len(set(supported_values))
        ):
            raise ContractLoadError(f"AGC-MODEL-CONTROL field={model_id}")
    catalog_policy = _mapping(registry.get("model_catalog_policy"), field="model_catalog_policy")
    _exact_keys(
        catalog_policy,
        {"active_rows_only", "unselected_rows", "activation_requires"},
        field="model_catalog_policy",
    )
    if catalog_policy != {
        "active_rows_only": True,
        "unselected_rows": "external-research-not-active-authority",
        "activation_requires": [
            "official-source-revalidation",
            "entitlement-revalidation",
            "runtime-revalidation",
        ],
    }:
        raise ContractLoadError("AGC-MODEL-CATALOG-POLICY")
    workflow_states = registry.get("workflow_states")
    expected_state_ids = (
        "discover", "design/plan", "approval", "implement", "validate",
        "independent-review", "evidence", "handoff",
    )
    state_keys = {
        "state_id", "owner_agent", "required_inputs", "mutation_authority",
        "entry_condition", "exit_gate", "max_attempts", "failure_return",
        "evidence_fields", "handoff_target",
    }
    if not isinstance(workflow_states, list) or len(workflow_states) != len(expected_state_ids):
        raise ContractLoadError("AGC-WORKFLOW-STATES")
    for index, raw_state in enumerate(workflow_states):
        state = _mapping(raw_state, field=f"workflow_states[{index}]")
        _exact_keys(state, state_keys, field=f"workflow_states[{index}]")
        if state.get("state_id") != expected_state_ids[index]:
            raise ContractLoadError("AGC-WORKFLOW-STATES")
        for field in ("owner_agent", "mutation_authority", "entry_condition", "exit_gate", "failure_return", "handoff_target"):
            if not isinstance(state.get(field), str) or not state[field]:
                raise ContractLoadError(f"AGC-WORKFLOW-STATE field={field}")
        if state["owner_agent"] not in registered_roles:
            raise ContractLoadError("AGC-WORKFLOW-STATE field=owner_agent")
        if state["mutation_authority"] not in permissions:
            raise ContractLoadError("AGC-WORKFLOW-STATE field=mutation_authority")
        if state["failure_return"] not in {*expected_state_ids, "stop"}:
            raise ContractLoadError("AGC-WORKFLOW-STATE field=failure_return")
        if state["handoff_target"] not in {*expected_state_ids, "complete"}:
            raise ContractLoadError("AGC-WORKFLOW-STATE field=handoff_target")
        for field in ("required_inputs", "evidence_fields"):
            values = state.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item for item in values):
                raise ContractLoadError(f"AGC-WORKFLOW-STATE field={field}")
        if not isinstance(state.get("max_attempts"), int) or not 1 <= state["max_attempts"] <= 2:
            raise ContractLoadError("AGC-WORKFLOW-STATE field=max_attempts")
    raw_layers = registry.get("harness_layers")
    layer_keys = {"layer_id", "owner_agent", "gate", "failure_return"}
    if not isinstance(raw_layers, list) or len(raw_layers) != len(EXPECTED_HARNESS_LAYERS):
        raise ContractLoadError("AGC-HARNESS-LAYERS")
    actual_layers: list[tuple[str, str, str, str]] = []
    for index, raw_layer in enumerate(raw_layers):
        layer = _mapping(raw_layer, field=f"harness_layers[{index}]")
        _exact_keys(layer, layer_keys, field=f"harness_layers[{index}]")
        values = tuple(layer.get(field) for field in ("layer_id", "owner_agent", "gate", "failure_return"))
        if any(not isinstance(value, str) or not value for value in values):
            raise ContractLoadError(f"AGC-HARNESS-LAYER field={index}")
        if layer["owner_agent"] not in registered_roles:
            raise ContractLoadError(f"AGC-HARNESS-LAYER-ROLE field={index}")
        actual_layers.append(values)
    if tuple(actual_layers) != EXPECTED_HARNESS_LAYERS:
        raise ContractLoadError("AGC-HARNESS-LAYERS")

    loops = _mapping(registry.get("harness_loops"), field="harness_loops")
    if set(loops) != HARNESS_LOOPS:
        raise ContractLoadError("AGC-HARNESS-LOOPS")
    loop_keys = {
        "owner_agent", "reviewer_agent", "permission_profile", "workflow_states",
        "max_attempts", "stop_condition", "on_failure",
    }
    for loop_id, raw_loop in loops.items():
        loop = _mapping(raw_loop, field=f"harness_loops.{loop_id}")
        _exact_keys(loop, loop_keys, field=f"harness_loops.{loop_id}")
        references = loop.get("workflow_states")
        if (
            not isinstance(references, list)
            or not references
            or any(item not in expected_state_ids for item in references)
            or not isinstance(loop.get("max_attempts"), int)
            or not 1 <= loop["max_attempts"] <= 2
            or loop.get("owner_agent") not in registered_roles
            or loop.get("reviewer_agent") not in registered_roles
            or loop.get("permission_profile") not in permissions
            or not isinstance(loop.get("stop_condition"), str)
            or not loop["stop_condition"]
            or not isinstance(loop.get("on_failure"), str)
            or not loop["on_failure"]
        ):
            raise ContractLoadError(f"AGC-HARNESS-LOOP field={loop_id}")
        actual = (
            loop["owner_agent"],
            loop["reviewer_agent"],
            loop["permission_profile"],
            tuple(references),
            loop["max_attempts"],
            loop["stop_condition"],
            loop["on_failure"],
        )
        if actual != EXPECTED_HARNESS_LOOP_VALUES[loop_id]:
            raise ContractLoadError(f"AGC-HARNESS-LOOP-VALUES field={loop_id}")
    generated = registry.get("generated_roots")
    generated_values = tuple(generated) if isinstance(generated, list) else ()
    if generated_values != EXPECTED_GENERATED_ROOTS:
        raise ContractLoadError("AGC-GENERATED-ROOTS")
    return tuple(records), compatibility


def _load_roles(root: pathlib.Path) -> tuple[RoleRecord, ...]:
    directory = root / GOVERNANCE / "roles"
    records: list[RoleRecord] = []
    for file_path in sorted(directory.glob("*.md")):
        relative = pathlib.PurePosixPath(file_path.relative_to(root).as_posix())
        text = _read_text(root, relative)
        values = _frontmatter(text, relative)
        if "agent_id" not in values:
            continue
        if values.get("profile_id") != "governance-role":
            raise ContractLoadError(f"AGC-ROLE-PROFILE path={relative}")
        agent_id = _string(values, "agent_id", relative)
        if file_path.stem != agent_id:
            raise ContractLoadError(f"AGC-ROLE-IDENTITY path={relative}")
        records.append(
            RoleRecord(
                agent_id=agent_id,
                scope=_string(values, "scope", relative),
                tier=_string(values, "tier", relative),
                work_profile=_string(values, "work_profile", relative),
                permission_profile=_string(values, "permission_profile", relative),
                skill_ids=_strings(values.get("skill_ids"), field="skill_ids", path=relative),
                source_path=relative,
                source_text=text,
            )
        )
    return tuple(records)


def _load_skills(root: pathlib.Path) -> tuple[SkillRecord, ...]:
    directory = root / GOVERNANCE / "skills"
    records: list[SkillRecord] = []
    for file_path in sorted(directory.glob("*.md")):
        relative = pathlib.PurePosixPath(file_path.relative_to(root).as_posix())
        text = _read_text(root, relative)
        values = _frontmatter(text, relative)
        skill_id = _string(values, "function_id", relative)
        if file_path.stem != skill_id or values.get("profile_id") != "governance-skill":
            raise ContractLoadError(f"AGC-SKILL-IDENTITY path={relative}")
        records.append(
            SkillRecord(
                skill_id=skill_id,
                scope=_string(values, "scope", relative),
                owner_agent=_string(values, "owner_agent", relative),
                source_path=relative,
                source_text=text,
            )
        )
    return tuple(records)


def load_agent_governance(root: pathlib.Path) -> AgentGovernanceState:
    root = root.absolute()
    roles = _load_roles(root)
    skills = _load_skills(root)
    registry = _load_yaml(root, REGISTRY)
    provider_records, compatibility = _validate_registry(
        root, registry, frozenset(item.agent_id for item in roles)
    )
    provider_ids = tuple(item.provider_id for item in provider_records)
    governance_root = root / GOVERNANCE
    root_entries = tuple(sorted(path.name for path in governance_root.iterdir()))
    provider_entries = tuple(sorted(path.name for path in (governance_root / "providers").iterdir()))
    return AgentGovernanceState(
        providers=provider_ids,
        provider_records=provider_records,
        compatibility=compatibility,
        root_entries=root_entries,
        provider_entries=provider_entries,
        roles=roles,
        skills=skills,
        registry=registry,
    )


def load_contract_bundle(root: pathlib.Path) -> ContractBundle:
    return ContractBundle(load_agent_governance(root))


def _finding(path: str | pathlib.PurePath, code: str, message: str) -> Finding:
    return Finding(str(path), code, message)


def validate_contract_bundle(root: pathlib.Path, bundle: ContractBundle) -> list[Finding]:
    state = bundle.state
    findings: list[Finding] = []
    if state.providers != SUPPORTED_PROVIDERS:
        findings.append(_finding(REGISTRY, "AGC-PROVIDERS", "providers must be claude and codex"))
    if state.root_entries != ROOT_ENTRIES:
        findings.append(_finding(GOVERNANCE, "AGC-ROOT-INVENTORY", "Stage 00 root inventory differs"))
    if state.provider_entries != PROVIDER_ENTRIES:
        findings.append(_finding(GOVERNANCE / "providers", "AGC-PROVIDER-INVENTORY", "provider inventory differs"))
    role_ids = tuple(item.agent_id for item in state.roles)
    skill_ids = tuple(item.skill_id for item in state.skills)
    if len(role_ids) != 14 or len(role_ids) != len(set(role_ids)):
        findings.append(_finding(GOVERNANCE / "roles", "AGC-ROLE-SET", "expected 14 unique roles"))
    if len(skill_ids) != 23 or len(skill_ids) != len(set(skill_ids)):
        findings.append(_finding(GOVERNANCE / "skills", "AGC-SKILL-SET", "expected 23 unique skills"))
    roles = set(role_ids)
    skills = set(skill_ids)
    work_profiles = bundle.registry.get("work_profiles")
    permissions = bundle.registry.get("permissions")
    if not isinstance(work_profiles, dict) or not isinstance(permissions, dict):
        findings.append(_finding(REGISTRY, "AGC-PROVIDER-REGISTRY", "work profiles and permissions are required"))
        return sorted(set(findings))
    models = bundle.registry.get("models")
    loops = bundle.registry.get("harness_loops")
    layers = bundle.registry.get("harness_layers")
    if not isinstance(models, dict) or not models:
        findings.append(_finding(REGISTRY, "AGC-MODEL-CATALOG", "active model catalog is required"))
    if not isinstance(loops, dict) or set(loops) != HARNESS_LOOPS:
        findings.append(_finding(REGISTRY, "AGC-HARNESS-LOOPS", "bounded harness loops differ"))
    if not isinstance(layers, list) or len(layers) != 8:
        findings.append(_finding(REGISTRY, "AGC-HARNESS-LAYERS", "expected eight harness layers"))
    for role in state.roles:
        if role.work_profile not in work_profiles:
            findings.append(_finding(role.source_path, "AGC-WORK-PROFILE", "unknown work profile"))
        if role.permission_profile not in permissions:
            findings.append(_finding(role.source_path, "AGC-PERMISSION", "unknown permission profile"))
        for skill_id in role.skill_ids:
            if skill_id not in skills:
                findings.append(_finding(role.source_path, "AGC-SKILL-REFERENCE", f"unknown skill {skill_id}"))
    for skill in state.skills:
        if skill.owner_agent not in roles:
            findings.append(_finding(skill.source_path, "AGC-ROLE-REFERENCE", "unknown owner role"))
    if isinstance(models, dict):
        selected = {
            item.get("model")
            for profile in work_profiles.values()
            if isinstance(profile, dict)
            for item in profile.values()
            if isinstance(item, dict)
        }
        if selected != set(models):
            findings.append(_finding(REGISTRY, "AGC-MODEL-SELECTION", "model catalog and work profiles differ"))
        for model_id, model in models.items():
            if not isinstance(model, dict) or model.get("runtime_acceptance") != "needs_revalidation" or model.get("entitlement") != "needs_revalidation":
                findings.append(_finding(REGISTRY, "AGC-MODEL-STATUS", f"model status incomplete: {model_id}"))
    try:
        stage99 = json.loads(_read_text(root, "docs/99.templates/registry.json"))
        profiles = {item.get("profile_id") for item in stage99.get("profiles", []) if isinstance(item, dict)}
    except (ContractLoadError, json.JSONDecodeError, AttributeError) as error:
        raise ContractLoadError("AGC-STAGE99-INVALID") from error
    if not GOVERNANCE_PROFILES.issubset(profiles):
        findings.append(_finding("docs/99.templates/registry.json", "AGC-STAGE99-PROFILES", "governance profiles are incomplete"))
    return sorted(set(findings))


def _projection_ids(root: pathlib.Path, directory: str, suffix: str) -> set[str]:
    base = root / directory
    if not base.exists():
        return set()
    if suffix == "SKILL.md":
        return {path.parent.name for path in base.glob("*/SKILL.md")}
    return {path.name.removesuffix(suffix) for path in base.glob(f"*{suffix}")}


ACTIVE_TEXT_EXTENSIONS = {
    ".json", ".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml",
}
ACTIVE_TEXT_ROOTS = (
    "_workspace",
    ".github",
    "docs/00.agent-governance",
    "docs/01.requirements",
    "docs/02.architecture",
    "docs/03.specs",
    "docs/05.operations",
    "docs/99.templates",
    "scripts",
    ".agents",
    ".claude",
    ".codex",
)
ACTIVE_TEXT_FILES = (
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
)


def _active_text_paths(root: pathlib.Path) -> tuple[pathlib.PurePosixPath, ...]:
    paths = {pathlib.PurePosixPath(item) for item in ACTIVE_TEXT_FILES}
    for directory_name in ACTIVE_TEXT_ROOTS:
        directory = root / directory_name
        try:
            root_metadata = directory.lstat()
        except FileNotFoundError:
            continue
        relative_root = pathlib.PurePosixPath(directory_name)
        if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
            paths.add(relative_root)
            continue
        for path in directory.rglob("*"):
            try:
                metadata = path.lstat()
            except OSError:
                paths.add(pathlib.PurePosixPath(path.relative_to(root).as_posix()))
                continue
            if (
                path.suffix.lower() in ACTIVE_TEXT_EXTENSIONS
                or stat.S_ISLNK(metadata.st_mode)
                or not (stat.S_ISREG(metadata.st_mode) or stat.S_ISDIR(metadata.st_mode))
            ):
                paths.add(pathlib.PurePosixPath(path.relative_to(root).as_posix()))
    return tuple(sorted(paths))


def current_markdown_authority(text: str) -> str:
    """Remove only explicitly delimited historical source quotations."""
    lines = text.splitlines()
    current_lines = []
    quoted_history = False
    table_history = False
    for index, line in enumerate(lines):
        if line == HISTORICAL_TABLE_MARKER and index + 2 < len(lines):
            header, separator = lines[index + 1:index + 3]
            if (re.fullmatch(r"\|(?:[^|\n]+\|)+", header)
                    and re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", separator)
                    and len(header.split("|")) == len(separator.split("|"))
                    and all(cell.strip() for cell in header.split("|")[1:-1])):
                table_history = True
                continue
        if table_history and line.startswith("|"):
            continue
        table_history = False
        if line == HISTORICAL_QUOTE_MARKER:
            quoted_history = True
            continue
        if quoted_history and (line == ">" or line.startswith("> ")):
            continue
        quoted_history = False
        current_lines.append(line)
    return "\n".join(current_lines)


def _has_unsupported_active_token(relative: str, text: str) -> bool:
    if relative.startswith("docs/") and relative.endswith(".md"):
        text = current_markdown_authority(text)
    if relative.endswith(".py"):
        # Literal inventories used to prove retired paths absent are data, not
        # provider adoption. No executable statement is removed by this match.
        text = re.sub(r"(?m)^\w*(?:REMOVED|RETIRED)_PATHS(?::[^=\n]+)? = \(\n(?:[ \t]+\"[^\"\n]+\",\n)+\)", "", text)
        return UNSUPPORTED_TOKEN.search(text) is not None
    # A search pattern names evidence, not an adopted provider. Strip only the
    # quoted pattern, retaining adjacent commands and all remaining arguments.
    text = re.sub(r"(?m)^(\s*!?\s*rg -n(?: -i)? )(['\"])[^\n]*?\2", r"\1", text)
    statements = re.split(r"\n\s*\n|\n(?=\s*(?:[-*] |\d+[.] |\|))|(?<=[.!?])\s+(?=[A-Z])|;|\bbut\b", text)
    for statement in statements:
        if UNSUPPORTED_TOKEN.search(statement) is None:
            continue
        normalized = re.sub(r"\s+", " ", statement).strip()
        if re.match(r"Add mutation cases for\b", normalized):
            continue
        positive = re.search(
            rf"(?i)(?:\b(?:use|load|enable|support|adopt|create|restore|retain)\s+(?:the\s+)?`?(?:{UNSUPPORTED_TOKEN.pattern[4:]})|"
            r"\b(?:must|should)\s+(?:remain|become)\s+active|\bcurrent active authority|"
            rf"(?:{UNSUPPORTED_TOKEN.pattern[4:]}).*?\b(?:is|are|remains?|must be|should be)\s+(?:the\s+)?(?:current|active|default|supported|adopted|enabled|required|canonical)\b|"
            r"\b(?:do not|must not|never)\s+(?:remove|retire|delete))", normalized,
        )
        if positive:
            return True
        if re.search(r"(?i)\b(?:remov(?:e[ds]?|ing|al)|retir(?:e[ds]?|ing|ement)|delet(?:e[ds]?|ing|ion)|absent|absence|forbidden|reject|fail)\b", normalized):
            continue
        if re.search(rf"(?i)\bno\s+[^.;]*(?:{UNSUPPORTED_TOKEN.pattern[4:]})|\bdo(?:es)? not exist\b", normalized):
            continue
        if re.match(r"(?i)(?:[-*] )?Move:", normalized) and " to " in normalized:
            if not UNSUPPORTED_TOKEN.search(normalized.split(" to ", 1)[1]):
                continue
        if re.search(r"(?:self[.])?assertFalse\(Path\([^\n]+\)[.]exists\(\)\)", normalized):
            continue
        return True
    return False


def validate_repository(
    root: pathlib.Path, bundle: ContractBundle, section: str = "all"
) -> list[Finding]:
    if section not in {"catalog", "providers", "harness", "all"}:
        raise ValueError(f"unsupported section: {section}")
    root = root.absolute()
    findings: list[Finding] = []
    roles = {item.agent_id for item in bundle.state.roles}
    skills = {item.skill_id for item in bundle.state.skills}
    if section in {"catalog", "providers", "all"}:
        for directory, suffix, expected, code in (
            (".agents/agents", ".md", roles, "AGC-AGENT-PROJECTION"),
            (".claude/agents", ".md", roles, "AGC-AGENT-PROJECTION"),
            (".codex/agents", ".toml", roles, "AGC-AGENT-PROJECTION"),
            (".agents/skills", "SKILL.md", skills, "AGC-ORPHAN-SKILL"),
            (".claude/skills", "SKILL.md", skills, "AGC-SKILL-PROJECTION"),
        ):
            actual = _projection_ids(root, directory, suffix)
            if actual != expected:
                findings.append(_finding(directory, code, f"expected={sorted(expected)} actual={sorted(actual)}"))
    if section in {"providers", "harness", "all"}:
        if (root / RETIRED_PROVIDER_DIRECTORY).exists() or (
            root / RETIRED_PROVIDER_SHIM
        ).exists():
            findings.append(_finding(".", "AGC-UNSUPPORTED-PROVIDER", "unsupported provider surface exists"))
        for relative_path in _active_text_paths(root):
            try:
                text = _read_text(root, relative_path)
            except ContractLoadError as error:
                findings.append(
                    _finding(
                        relative_path,
                        "AGC-ACTIVE-TEXT-UNSAFE",
                        str(error),
                    )
                )
                continue
            relative = relative_path.as_posix()
            if _has_unsupported_active_token(relative, text):
                findings.append(_finding(relative, "AGC-UNSUPPORTED-TOKEN", "retired provider or handoff token"))
            if relative.startswith((".agents/", ".claude/", ".codex/")) and GENERATED_AUTHORITY.search(text):
                findings.append(_finding(relative, "AGC-GENERATED-AUTHORITY", "generated adapter owns policy"))
    return sorted(set(findings))


def render_findings(findings: Sequence[Finding]) -> str:
    return "\n".join(
        f"{item.code}: {item.path}: {item.message}" for item in sorted(findings)
    )


def normalize_repo_relative_path(path: str | pathlib.PurePath) -> str:
    value = str(path).replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return _safe_relative(value).as_posix()


def _expand_braces(pattern: str) -> tuple[str, ...]:
    match = re.search(r"\{(\d+)\.\.(\d+)\}", pattern)
    if match is None:
        return (pattern,)
    start, end = (int(item) for item in match.groups())
    width = max(len(match.group(1)), len(match.group(2)))
    if end < start or end - start > 1024:
        raise ValueError("invalid brace range")
    return tuple(
        pattern[: match.start()] + f"{value:0{width}d}" + pattern[match.end() :]
        for value in range(start, end + 1)
    )


def path_matches_artifact_pattern(path: str, pattern: str) -> bool:
    normalized = normalize_repo_relative_path(path)
    return any(fnmatch.fnmatchcase(normalized, candidate) for candidate in _expand_braces(pattern))
