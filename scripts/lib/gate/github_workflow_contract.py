from __future__ import annotations

import argparse
import ast
import dataclasses
import os
import pathlib
import re
import shlex
import stat
import subprocess
import sys
from typing import Final

import yaml

try:
    from scripts.lib.gate.ci_gate_contract import (
        CI_DEPENDENCY_BOOTSTRAP,
        GateContractError,
        GateRegistry,
        expand_gate_ids as _expand_gate_ids,
        load_contract_document,
        parse_gate_registry,
        validate_gate_registry,
    )
except ModuleNotFoundError:  # Direct sibling-script execution.
    from ci_gate_contract import (  # type: ignore[no-redef]
        CI_DEPENDENCY_BOOTSTRAP,
        GateContractError,
        GateRegistry,
        expand_gate_ids as _expand_gate_ids,
        load_contract_document,
        parse_gate_registry,
        validate_gate_registry,
    )

expand_gate_ids = _expand_gate_ids


WORKFLOW_CONTRACT: Final = pathlib.PurePosixPath(".github/workflow-contract.yml")
WORKFLOW_ROOT: Final = pathlib.PurePosixPath(".github/workflows")
MAX_YAML_BYTES: Final = 2 * 1_048_576
MAX_WORKFLOWS: Final = 128
MAX_AGGREGATE_BYTES: Final = 2 * 1_048_576
MAX_SEMANTIC_HELPER_BYTES: Final = 256 * 1_024
MAX_SEMANTIC_HELPER_TOTAL_BYTES: Final = 4 * 1_048_576
MAX_SEMANTIC_HELPER_FILES: Final = 64
MAX_SEMANTIC_HELPER_DEPTH: Final = 8
PUBLIC_GATE_RUNNER: Final = pathlib.PurePosixPath(
    "scripts/validation/run-ci-gate.py"
)


@dataclasses.dataclass(frozen=True, order=True, slots=True)
class WorkflowFinding:
    code: str
    path: str
    message: str


@dataclasses.dataclass(frozen=True, slots=True)
class TriggerContract:
    events: tuple[str, ...]
    branches: tuple[str, ...]
    paths: tuple[str, ...]
    schedules: tuple[str, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class ActionDependency:
    action: str
    sha: str
    runtime: str
    manifest_url: str
    retrieved_at: str
    consumers: tuple[str, ...]
    security_disposition: str


@dataclasses.dataclass(frozen=True, slots=True)
class WorkflowDocument:
    path: str
    text: str
    data: dict[object, object]


@dataclasses.dataclass(frozen=True, slots=True)
class WorkflowJobContract:
    permissions: dict[str, str] | None
    runs_on: str
    timeout_minutes: int


@dataclasses.dataclass(frozen=True, slots=True)
class WorkflowSpec:
    path: str
    name: str
    classification: str
    trigger: TriggerContract
    trigger_document: dict[str, object]
    permissions: dict[str, str]
    concurrency: dict[str, object] | None
    jobs: dict[str, WorkflowJobContract]


@dataclasses.dataclass(frozen=True, slots=True)
class WorkflowContract:
    schema_version: int
    workflows: tuple[WorkflowSpec, ...]
    actions: tuple[ActionDependency, ...]
    gate_registry: GateRegistry


PermissionItems = tuple[tuple[str, str], ...]


@dataclasses.dataclass(frozen=True, slots=True)
class _WorkflowPermissionBaseline:
    top_level: PermissionItems
    jobs: tuple[tuple[str, PermissionItems | None], ...]


_CONTENTS_READ: Final[PermissionItems] = (("contents", "read"),)
_FULL_GATE_PERMISSIONS: Final[PermissionItems] = (
    ("actions", "read"),
    ("contents", "read"),
    ("security-events", "write"),
)
_WORKFLOW_PERMISSION_BASELINES: Final = (
    (
        ".github/workflows/ci-quality.yml",
        _WorkflowPermissionBaseline(
            top_level=_CONTENTS_READ,
            jobs=(
                ("validation-changed", _CONTENTS_READ),
                ("validation-full", _FULL_GATE_PERMISSIONS),
            ),
        ),
    ),
    (
        ".github/workflows/generate-changelog.yml",
        _WorkflowPermissionBaseline(
            top_level=_CONTENTS_READ,
            jobs=(("changelog", None),),
        ),
    ),
    (
        ".github/workflows/greetings.yml",
        _WorkflowPermissionBaseline(
            top_level=(),
            jobs=(
                (
                    "issue-greeting",
                    (("contents", "read"), ("issues", "write")),
                ),
                (
                    "pull-request-greeting",
                    (("contents", "read"), ("issues", "write")),
                ),
            ),
        ),
    ),
    (
        ".github/workflows/pr-labeler.yml",
        _WorkflowPermissionBaseline(
            top_level=(),
            jobs=(
                (
                    "triage",
                    (("contents", "read"), ("pull-requests", "write")),
                ),
            ),
        ),
    ),
    (
        ".github/workflows/stale.yml",
        _WorkflowPermissionBaseline(
            top_level=(),
            jobs=(
                (
                    "stale",
                    (
                        ("contents", "read"),
                        ("issues", "write"),
                        ("pull-requests", "write"),
                    ),
                ),
            ),
        ),
    ),
    (
        ".github/workflows/tech-stack-version-sync.yml",
        _WorkflowPermissionBaseline(
            top_level=_CONTENTS_READ,
            jobs=(("drift-gate", _CONTENTS_READ),),
        ),
    ),
)
_ACTION_REGISTRY_BASELINE: Final = (
    (
        "actions/checkout",
        "3d3c42e5aac5ba805825da76410c181273ba90b1",
    ),
    (
        "actions/first-interaction",
        "1c4688942c71f71d4f5502a26ea67c331730fa4d",
    ),
    (
        "actions/labeler",
        "bf12e9b00b37c5c0ca2b87b79b2daf7891dbda13",
    ),
    (
        "actions/setup-node",
        "820762786026740c76f36085b0efc47a31fe5020",
    ),
    (
        "actions/setup-python",
        "5fda3b95a4ea91299a34e894583c3862153e4b97",
    ),
    (
        "actions/stale",
        "1e223db275d687790206a7acac4d1a11bd6fe629",
    ),
    (
        "astral-sh/setup-uv",
        "11f9893b081a58869d3b5fccaea48c9e9e46f990",
    ),
    (
        "github/codeql-action/upload-sarif",
        "7188fc363630916deb702c7fdcf4e481b751f97a",
    ),
)


class WorkflowContractError(ValueError):
    def __init__(self, code: str, path: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    key_tags: dict[object, str] = {}
    for key_node, value_node in node.value:
        if (
            isinstance(key_node, yaml.nodes.ScalarNode)
            and key_node.value == "on"
        ):
            key: object = "on"
        else:
            key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping key must be a hashable scalar",
                key_node.start_mark,
            ) from error
        if duplicate:
            if (
                key == "on"
                and key_tags.get(key) != key_node.tag
                and {
                    key_tags.get(key),
                    key_node.tag,
                }
                == {
                    "tag:yaml.org,2002:bool",
                    "tag:yaml.org,2002:str",
                }
            ):
                raise WorkflowContractError(
                    "workflow-trigger-key-ambiguous",
                    "<yaml>",
                    "workflow trigger key has ambiguous YAML forms",
                )
            raise WorkflowContractError(
                "yaml-duplicate-key",
                "<yaml>",
                "duplicate YAML mapping key",
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
        key_tags[key] = key_node.tag
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _assert_safe_parent_directories(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
) -> None:
    current = root
    for part in relative.parts[:-1]:
        current /= part
        try:
            metadata = current.lstat()
        except OSError as error:
            raise WorkflowContractError(
                "yaml-read-error",
                relative.as_posix(),
                "required YAML parent directory is unavailable",
            ) from error
        if not stat.S_ISDIR(metadata.st_mode):
            raise WorkflowContractError(
                "yaml-file-unsafe",
                relative.as_posix(),
                "YAML input parent components must be real directories",
            )


def _read_bounded_yaml(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
) -> tuple[str, dict[object, object]]:
    if (
        relative.is_absolute()
        or not relative.parts
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise WorkflowContractError(
            "yaml-file-unsafe",
            relative.as_posix(),
            "YAML input path must be canonical and repository-relative",
        )
    _assert_safe_parent_directories(root, relative)
    path = root.joinpath(*relative.parts)
    try:
        metadata = path.lstat()
    except OSError as error:
        raise WorkflowContractError(
            "yaml-read-error",
            relative.as_posix(),
            "required YAML file is unavailable",
        ) from error
    if not stat.S_ISREG(metadata.st_mode):
        raise WorkflowContractError(
            "yaml-file-unsafe",
            relative.as_posix(),
            "YAML input must be a regular file",
        )
    if metadata.st_size > MAX_YAML_BYTES:
        raise WorkflowContractError(
            "yaml-file-oversize",
            relative.as_posix(),
            "YAML input exceeds the size limit",
        )
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            opened_metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(opened_metadata.st_mode)
                or (metadata.st_dev, metadata.st_ino)
                != (opened_metadata.st_dev, opened_metadata.st_ino)
            ):
                raise WorkflowContractError(
                    "yaml-file-unsafe",
                    relative.as_posix(),
                    "YAML input changed during safe open",
                )
            if opened_metadata.st_size > MAX_YAML_BYTES:
                raise WorkflowContractError(
                    "yaml-file-oversize",
                    relative.as_posix(),
                    "YAML input exceeds the size limit",
                )
            chunks: list[bytes] = []
            remaining = MAX_YAML_BYTES + 1
            while remaining:
                chunk = os.read(descriptor, remaining)
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            payload = b"".join(chunks)
            closed_metadata = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except WorkflowContractError:
        raise
    except OSError as error:
        raise WorkflowContractError(
            "yaml-read-error",
            relative.as_posix(),
            "YAML input could not be read safely",
        ) from error
    if len(payload) > MAX_YAML_BYTES:
        raise WorkflowContractError(
            "yaml-file-oversize",
            relative.as_posix(),
            "YAML input exceeds the size limit",
        )
    try:
        final_metadata = path.lstat()
    except OSError as error:
        raise WorkflowContractError(
            "yaml-file-unsafe",
            relative.as_posix(),
            "YAML input changed while being read",
        ) from error
    if (
        len(payload) != opened_metadata.st_size
        or opened_metadata.st_size != closed_metadata.st_size
        or (metadata.st_dev, metadata.st_ino)
        != (final_metadata.st_dev, final_metadata.st_ino)
        or not stat.S_ISREG(final_metadata.st_mode)
    ):
        raise WorkflowContractError(
            "yaml-file-unsafe",
            relative.as_posix(),
            "YAML input changed while being read",
        )
    try:
        text = payload.decode("utf-8")
        loaded = yaml.load(text, Loader=_UniqueKeyLoader)
    except UnicodeError as error:
        raise WorkflowContractError(
            "yaml-encoding-invalid",
            relative.as_posix(),
            "YAML input must be UTF-8",
        ) from error
    except WorkflowContractError as error:
        raise WorkflowContractError(
            error.code,
            relative.as_posix(),
            error.message,
        ) from error
    except yaml.YAMLError as error:
        raise WorkflowContractError(
            "yaml-syntax-invalid",
            relative.as_posix(),
            "YAML input is invalid",
        ) from error
    if not isinstance(loaded, dict):
        raise WorkflowContractError(
            "yaml-root-invalid",
            relative.as_posix(),
            "YAML root must be a mapping",
        )
    return text, loaded


def _normalize_workflow_trigger_key(
    data: dict[object, object],
    *,
    path: str,
) -> None:
    boolean_on_keys = tuple(
        key
        for key in data
        if type(key) is bool and key is True
    )
    if boolean_on_keys:
        raise WorkflowContractError(
            "workflow-trigger-key-invalid",
            path,
            "workflow trigger key uses an invalid YAML scalar",
        )


def load_workflows(root: pathlib.Path) -> tuple[WorkflowDocument, ...]:
    _assert_safe_parent_directories(
        root,
        WORKFLOW_ROOT / "__workflow_directory_probe__",
    )
    workflow_directory = root.joinpath(*WORKFLOW_ROOT.parts)
    candidates = sorted(
        (
            path
            for pattern in ("*.yml", "*.yaml")
            for path in workflow_directory.glob(pattern)
        ),
        key=lambda path: path.as_posix(),
    )
    if len(candidates) > MAX_WORKFLOWS:
        raise WorkflowContractError(
            "workflow-count-exceeded",
            WORKFLOW_ROOT.as_posix(),
            "tracked workflow count exceeds the limit",
        )
    documents: list[WorkflowDocument] = []
    for path in candidates:
        relative = pathlib.PurePosixPath(path.relative_to(root).as_posix())
        text, data = _read_bounded_yaml(root, relative)
        _normalize_workflow_trigger_key(
            data,
            path=relative.as_posix(),
        )
        documents.append(
            WorkflowDocument(path=relative.as_posix(), text=text, data=data)
        )
    return tuple(documents)


def _expect_mapping(
    value: object,
    *,
    path: str,
    field: str,
) -> dict[object, object]:
    if not isinstance(value, dict):
        raise WorkflowContractError(
            "contract-schema-invalid",
            path,
            f"{field} must be a mapping",
        )
    return value


def _expect_exact_keys(
    value: dict[object, object],
    expected: set[str],
    *,
    path: str,
    field: str,
) -> None:
    if set(value) != expected:
        raise WorkflowContractError(
            "contract-schema-invalid",
            path,
            f"{field} keys do not match the contract schema",
        )


def _string_tuple(value: object, *, path: str, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise WorkflowContractError(
            "contract-schema-invalid",
            path,
            f"{field} must be a non-empty string list",
        )
    return tuple(value)


def _permissions(
    value: object,
    *,
    path: str,
    field: str,
    nullable: bool,
) -> dict[str, str] | None:
    if value is None and nullable:
        return None
    mapping = _expect_mapping(value, path=path, field=field)
    if any(
        not isinstance(key, str)
        or not isinstance(permission, str)
        or permission not in {"read", "write", "none"}
        for key, permission in mapping.items()
    ):
        raise WorkflowContractError(
            "contract-schema-invalid",
            path,
            f"{field} contains an invalid permission",
        )
    return {str(key): str(permission) for key, permission in mapping.items()}


def _trigger_contract(
    value: object,
    *,
    path: str,
) -> tuple[TriggerContract, dict[str, object]]:
    mapping = _expect_mapping(value, path=path, field="triggers")
    if not mapping or any(not isinstance(event, str) for event in mapping):
        raise WorkflowContractError(
            "contract-schema-invalid",
            path,
            "triggers must register named events",
        )
    events: list[str] = []
    branches: list[str] = []
    paths: list[str] = []
    schedules: list[str] = []
    normalized: dict[str, object] = {}
    for event, options in mapping.items():
        assert isinstance(event, str)
        events.append(event)
        normalized[event] = options
        if event == "schedule":
            if not isinstance(options, list):
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    path,
                    "schedule must be a list",
                )
            for record in options:
                cron = record.get("cron") if isinstance(record, dict) else None
                if (
                    not isinstance(record, dict)
                    or set(record) != {"cron"}
                    or not isinstance(cron, str)
                    or not cron
                ):
                    raise WorkflowContractError(
                        "contract-schema-invalid",
                        path,
                        "schedule entries must contain one cron value",
                    )
                schedules.append(cron)
            continue
        if options is None:
            continue
        event_options = _expect_mapping(
            options,
            path=path,
            field=f"triggers.{event}",
        )
        for branch in event_options.get("branches", []):
            if not isinstance(branch, str):
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    path,
                    "trigger branches must be strings",
                )
            branches.append(f"{event}:{branch}")
        for selected_path in event_options.get("paths", []):
            if not isinstance(selected_path, str):
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    path,
                    "trigger paths must be strings",
                )
            paths.append(f"{event}:{selected_path}")
    return (
        TriggerContract(
            events=tuple(events),
            branches=tuple(branches),
            paths=tuple(paths),
            schedules=tuple(schedules),
        ),
        normalized,
    )


def load_workflow_contract(root: pathlib.Path) -> WorkflowContract:
    try:
        raw = load_contract_document(root)
        gate_registry = parse_gate_registry(
            raw,
            WORKFLOW_CONTRACT.as_posix(),
        )
    except GateContractError as error:
        raise WorkflowContractError(
            error.code,
            error.path,
            error.message,
        ) from None
    workflow_mapping = _expect_mapping(
        raw["workflows"],
        path=WORKFLOW_CONTRACT.as_posix(),
        field="workflows",
    )
    workflows: list[WorkflowSpec] = []
    for workflow_path, raw_spec in workflow_mapping.items():
        workflow_relative = (
            pathlib.PurePosixPath(workflow_path)
            if isinstance(workflow_path, str)
            else None
        )
        if (
            workflow_relative is None
            or workflow_relative.is_absolute()
            or workflow_relative.as_posix() != workflow_path
            or workflow_relative.parent != WORKFLOW_ROOT
            or workflow_relative.suffix not in {".yml", ".yaml"}
        ):
            raise WorkflowContractError(
                "contract-workflow-path-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "workflow paths must be canonical repository-relative YAML paths",
            )
        spec = _expect_mapping(raw_spec, path=workflow_path, field="workflow")
        _expect_exact_keys(
            spec,
            {
                "name",
                "classification",
                "triggers",
                "permissions",
                "concurrency",
                "jobs",
            },
            path=workflow_path,
            field="workflow",
        )
        name = spec["name"]
        classification = spec["classification"]
        if not isinstance(name, str) or not name:
            raise WorkflowContractError(
                "contract-schema-invalid",
                workflow_path,
                "workflow name must be a non-empty string",
            )
        if classification not in {"required-quality", "non-gating"}:
            raise WorkflowContractError(
                "contract-schema-invalid",
                workflow_path,
                "workflow classification is invalid",
            )
        trigger, trigger_document = _trigger_contract(
            spec["triggers"],
            path=workflow_path,
        )
        permissions = _permissions(
            spec["permissions"],
            path=workflow_path,
            field="permissions",
            nullable=False,
        )
        assert permissions is not None
        raw_concurrency = spec["concurrency"]
        concurrency: dict[str, object] | None
        if raw_concurrency is None:
            concurrency = None
        else:
            concurrency_mapping = _expect_mapping(
                raw_concurrency,
                path=workflow_path,
                field="concurrency",
            )
            _expect_exact_keys(
                concurrency_mapping,
                {"group", "cancel-in-progress"},
                path=workflow_path,
                field="concurrency",
            )
            if (
                not isinstance(concurrency_mapping["group"], str)
                or not isinstance(concurrency_mapping["cancel-in-progress"], bool)
            ):
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    workflow_path,
                    "concurrency values are invalid",
                )
            concurrency = {
                "group": concurrency_mapping["group"],
                "cancel-in-progress": concurrency_mapping["cancel-in-progress"],
            }
        raw_jobs = _expect_mapping(
            spec["jobs"],
            path=workflow_path,
            field="jobs",
        )
        jobs: dict[str, WorkflowJobContract] = {}
        for job_id, raw_job in raw_jobs.items():
            if not isinstance(job_id, str) or not re.fullmatch(
                r"[A-Za-z0-9_-]+",
                job_id,
            ):
                raise WorkflowContractError(
                    "contract-job-id-invalid",
                    workflow_path,
                    "job IDs must use the GitHub identifier grammar",
                )
            job = _expect_mapping(
                raw_job,
                path=workflow_path,
                field=f"jobs.{job_id}",
            )
            _expect_exact_keys(
                job,
                {"permissions", "runs_on", "timeout_minutes"},
                path=workflow_path,
                field=f"jobs.{job_id}",
            )
            runs_on = job["runs_on"]
            timeout = job["timeout_minutes"]
            if not isinstance(runs_on, str) or not runs_on:
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    workflow_path,
                    "job runs_on must be a non-empty string",
                )
            if (
                not isinstance(timeout, int)
                or isinstance(timeout, bool)
                or not 1 <= timeout <= 30
            ):
                raise WorkflowContractError(
                    "contract-schema-invalid",
                    workflow_path,
                    "job timeout_minutes must be a bounded integer",
                )
            jobs[job_id] = WorkflowJobContract(
                permissions=_permissions(
                    job["permissions"],
                    path=workflow_path,
                    field=f"jobs.{job_id}.permissions",
                    nullable=True,
                ),
                runs_on=runs_on,
                timeout_minutes=timeout,
            )
        workflows.append(
            WorkflowSpec(
                path=workflow_path,
                name=name,
                classification=classification,
                trigger=trigger,
                trigger_document=trigger_document,
                permissions=permissions,
                concurrency=concurrency,
                jobs=jobs,
            )
        )
    if tuple(spec.path for spec in workflows) != tuple(
        sorted(spec.path for spec in workflows)
    ):
        raise WorkflowContractError(
            "contract-order-invalid",
            WORKFLOW_CONTRACT.as_posix(),
            "workflow records must be path-sorted",
        )

    raw_actions = raw["actions"]
    if not isinstance(raw_actions, dict):
        raise WorkflowContractError(
            "contract-schema-invalid",
            WORKFLOW_CONTRACT.as_posix(),
            "actions must be an object",
        )
    actions: list[ActionDependency] = []
    action_names: set[str] = set()
    action_keys = {
        "sha",
        "runtime",
        "manifest_url",
        "retrieved_at",
        "consumers",
        "security_disposition",
    }
    for action_name, record in raw_actions.items():
        if not isinstance(action_name, str) or not action_name:
            raise WorkflowContractError(
                "contract-schema-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "Action registry keys must be non-empty strings",
            )
        mapping = _expect_mapping(
            record,
            path=WORKFLOW_CONTRACT.as_posix(),
            field="actions entry",
        )
        _expect_exact_keys(
            mapping,
            action_keys,
            path=WORKFLOW_CONTRACT.as_posix(),
            field="actions entry",
        )
        scalar_fields = (
            "sha",
            "runtime",
            "manifest_url",
            "retrieved_at",
            "security_disposition",
        )
        if any(
            not isinstance(mapping[field], str) or not mapping[field]
            for field in scalar_fields
        ):
            raise WorkflowContractError(
                "contract-schema-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "action fields must be non-empty strings",
            )
        if action_name in action_names:
            raise WorkflowContractError(
                "contract-action-duplicate",
                WORKFLOW_CONTRACT.as_posix(),
                "Action registry identities must be unique",
            )
        action_names.add(action_name)
        actions.append(
            ActionDependency(
                action=action_name,
                sha=mapping["sha"],
                runtime=mapping["runtime"],
                manifest_url=mapping["manifest_url"],
                retrieved_at=mapping["retrieved_at"],
                consumers=_string_tuple(
                    mapping["consumers"],
                    path=WORKFLOW_CONTRACT.as_posix(),
                    field="action consumers",
                ),
                security_disposition=mapping["security_disposition"],
            )
        )
    if tuple(action.action for action in actions) != tuple(
        sorted(action.action for action in actions)
    ):
        raise WorkflowContractError(
            "contract-order-invalid",
            WORKFLOW_CONTRACT.as_posix(),
            "Action records must be action-sorted",
        )
    required_workflows = [
        workflow
        for workflow in workflows
        if workflow.classification == "required-quality"
    ]
    if len(required_workflows) != 1 or len(required_workflows[0].jobs) != 2:
        raise WorkflowContractError(
            "contract-required-quality-invalid",
            WORKFLOW_CONTRACT.as_posix(),
            "exactly one required-quality workflow with two public-profile jobs is required",
        )
    return WorkflowContract(
        schema_version=2,
        workflows=tuple(workflows),
        actions=tuple(actions),
        gate_registry=gate_registry,
    )


def _job_tokens(job: dict[object, object]) -> tuple[str, ...]:
    tokens: list[str] = []
    steps = job.get("steps")
    if not isinstance(steps, list):
        return ()
    for step in steps:
        if not isinstance(step, dict):
            continue
        uses = step.get("uses")
        if isinstance(uses, str):
            tokens.append(f"uses:{uses}")
        run = step.get("run")
        if isinstance(run, str):
            tokens.extend(line.strip() for line in run.splitlines() if line.strip())
    return tuple(tokens)


def _job_programs(job: dict[object, object]) -> tuple[str, ...]:
    programs: list[str] = []
    steps = job.get("steps")
    if not isinstance(steps, list):
        return ()
    for step in steps:
        if not isinstance(step, dict):
            continue
        run = step.get("run")
        if isinstance(run, str):
            programs.append(run)
    return tuple(programs)


_STATIC_GATE_PROGRAM_RE: Final = re.compile(
    r"python3 scripts/validation/run-ci-gate\.py --profile (changed|full)\Z"
)


def _static_gate_profile(program: str) -> str | None:
    match = _STATIC_GATE_PROGRAM_RE.fullmatch(program)
    return match.group(1) if match is not None else None


def _environment_keys(value: object) -> set[str] | None:
    if value is None:
        return set()
    if not isinstance(value, dict) or any(
        not isinstance(key, str) for key in value
    ):
        return None
    return set(value)


def _workflow_projection_findings(
    path: str,
    raw_workflow: dict[object, object],
    raw_jobs: dict[object, object],
    contract: WorkflowContract,
) -> tuple[WorkflowFinding, ...]:
    findings: list[WorkflowFinding] = []
    workflow_defaults = raw_workflow.get("defaults")
    if isinstance(workflow_defaults, dict) and "run" in workflow_defaults:
        findings.append(
            _finding(
                "workflow-gate-execution-context-invalid",
                path,
                "required workflow defaults.run is forbidden",
            )
        )
    expected_jobs: dict[str, tuple[str, str, dict[str, str]]] = {
        "validation-changed": (
            "changed",
            "github.event_name == 'pull_request'",
            {
                "EVENT_NAME": "${{ github.event_name }}",
                "PR_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
                "PR_TITLE": "${{ github.event.pull_request.title }}",
                "HEAD_REF": "${{ github.head_ref }}",
            },
        ),
        "validation-full": (
            "full",
            "github.event_name != 'pull_request'",
            {
                "EVENT_NAME": "${{ github.event_name }}",
                "PUSH_BEFORE_SHA": "${{ github.event.before }}",
                "HYHOME_COMPOSE_PROFILES": (
                    "core data obs workflow ai tooling messaging security "
                    "communication service storage admin iac registry sast "
                    "sync testing graph mng ksql nginx"
                ),
            },
        ),
    }
    checkout = next(
        (action for action in contract.actions if action.action == "actions/checkout"),
        None,
    )
    expected_checkout = (
        {
            "name": "Checkout repository",
            "uses": f"actions/checkout@{checkout.sha}",
            "with": {"persist-credentials": False, "fetch-depth": 0},
        }
        if checkout is not None
        else None
    )
    for raw_job_id, raw_job in raw_jobs.items():
        if not isinstance(raw_job_id, str) or not isinstance(raw_job, dict):
            continue
        expected_job = expected_jobs.get(raw_job_id)
        if expected_job is None:
            continue
        profile, admitted_job_condition, admitted_job_environment = expected_job
        if raw_job.get("if") != admitted_job_condition:
            findings.append(
                _finding(
                    "workflow-gate-execution-context-invalid",
                    path,
                    f"job {raw_job_id} condition is not admitted",
                )
            )
        job_defaults = raw_job.get("defaults")
        if isinstance(job_defaults, dict) and "run" in job_defaults:
            findings.append(
                _finding(
                    "workflow-gate-execution-context-invalid",
                    path,
                    f"job {raw_job_id} defaults.run is forbidden",
                )
            )
        if raw_job.get("env") != admitted_job_environment:
            findings.append(
                _finding(
                    "workflow-gate-environment-invalid",
                    path,
                    f"job {raw_job_id} environment is not admitted",
                )
            )
        steps = raw_job.get("steps")
        if not isinstance(steps, list):
            findings.append(
                _finding(
                    "workflow-gate-projection-invalid",
                    path,
                    f"job {raw_job_id} has no projected steps",
                )
            )
            continue
        if not steps or steps[0] != expected_checkout:
            findings.append(
                _finding(
                    "workflow-gate-checkout-required",
                    path,
                    f"job {raw_job_id} requires the registered checkout first",
                )
            )
        projected: list[str] = []
        for step in steps:
            if not isinstance(step, dict):
                continue
            program = step.get("run")
            if program is None:
                continue
            if not isinstance(program, str):
                findings.append(
                    _finding(
                        "workflow-gate-projection-invalid",
                        path,
                        f"job {raw_job_id} contains a non-string run program",
                    )
                )
                continue
            if (
                step.get("if") is not None
                or "shell" in step
                or "working-directory" in step
                or "env" in step
            ):
                findings.append(
                    _finding(
                        "workflow-gate-execution-context-invalid",
                        path,
                        f"job {raw_job_id} run step context is not admitted",
                    )
                )
            selected_profile = "bootstrap" if program == CI_DEPENDENCY_BOOTSTRAP else _static_gate_profile(program)
            if selected_profile is None:
                findings.append(
                    _finding(
                        "workflow-gate-projection-invalid",
                        path,
                        f"job {raw_job_id} contains a non-static gate program",
                    )
                )
            else:
                projected.append(selected_profile)
        if projected != ["bootstrap", profile]:
            findings.append(
                _finding(
                    "workflow-gate-projection-mismatch",
                    path,
                    f"job {raw_job_id} must bootstrap dependencies then select its public profile exactly once",
                )
            )
    return tuple(findings)


@dataclasses.dataclass(frozen=True, slots=True)
class _ShellSubstitution:
    placeholder: str
    kind: str
    body: str


@dataclasses.dataclass(frozen=True, slots=True)
class _PreparedShellProgram:
    tokens: tuple[str, ...]
    substitutions: tuple[_ShellSubstitution, ...]
    heredoc_substitutions: tuple[_ShellSubstitution, ...]


@dataclasses.dataclass(frozen=True, slots=True)
class _ScriptInvocation:
    path: str
    direct: bool


@dataclasses.dataclass(slots=True)
class _ShellAnalysis:
    command_signatures: set[tuple[str, ...]]
    script_invocations: list[_ScriptInvocation]
    invalid: bool = False


@dataclasses.dataclass(frozen=True, slots=True)
class _VariableBinding:
    literal: str | None
    tainted: bool


@dataclasses.dataclass(slots=True)
class _SemanticResolution:
    command_signatures: set[tuple[str, ...]]
    script_paths: set[str]
    invalid: bool = False
    aggregate_invalid: bool = False


@dataclasses.dataclass(slots=True)
class _TraversalBudget:
    visited: set[str]
    stack: list[str]
    files: int = 0
    total_bytes: int = 0


_SHELL_SEPARATORS: Final = frozenset(
    {";", "\n", "&&", "||", "|", "&", "(", ")"}
)
_SHELL_PUNCTUATION: Final = ";&|<>()\n"
_SCRIPT_PATH_RE: Final = re.compile(
    r"scripts/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.(?:py|sh)"
)
_VARIABLE_RE: Final = re.compile(
    r"\$(?:([A-Za-z_][A-Za-z0-9_]*)|\{([A-Za-z_][A-Za-z0-9_]*)\})"
)
_INDIRECT_VARIABLE_RE: Final = re.compile(
    r"\$\{!([A-Za-z_][A-Za-z0-9_]*)\}"
)
_ASSIGNMENT_RE: Final = re.compile(
    r"([A-Za-z_][A-Za-z0-9_]*)=(.*)",
    re.DOTALL,
)
_APPROVED_OWNER_SUBSTITUTION: Final = (
    "bash",
    "scripts/validation/run-agent-output-eval-fixtures.sh",
    "--check-fixtures",
    "--check-regressions",
)
_DATA_ONLY_COMMANDS: Final = frozenset(
    {
        "-d",
        "-e",
        "-f",
        "-n",
        "-r",
        "-x",
        "[",
        "[[",
        "cat",
        "cd",
        "echo",
        "for",
        "grep",
        "printf",
        "read",
        "rg",
        "rm",
        "test",
    }
)
_GOVERNED_NON_SCRIPT_SIGNATURES: Final = frozenset(
    {
        (
            "python3",
            "-m",
            "unittest",
            "tests.validation.test_agent_governance_ci_routing",
            "-v",
        ),
        (
            "python3",
            "-m",
            "unittest",
            "tests.validation.test_agent_output_eval_fixtures",
            "-v",
        ),
        (
            "python3",
            "-m",
            "unittest",
            "tests.validation.test_compose_core_readiness",
            "tests.lib.ops.test_postgres_logical_upgrade_rehearsal",
            "tests.lib.supply_chain.test_grype_db_seed",
            "tests.validation.test_supply_chain_policy",
            "tests.validation.test_sample_service_delivery_rehearsal",
            "-v",
        ),
        (
            "npm",
            "audit",
            "--audit-level=high",
            "--prefix",
            "projects/storybook/nextjs",
        ),
        ("[[", "$PR_TITLE", "=~", "$title_re", "]]"),
        (
            "npm",
            "run",
            "build-storybook",
            "--prefix",
            "projects/storybook/nextjs",
        ),
        (
            "npm",
            "run",
            "coverage",
            "--prefix",
            "projects/storybook/nextjs",
        ),
        (
            "uvx",
            "--from",
            "zizmor==1.28.0",
            "zizmor",
            ".",
            "--format",
            "sarif",
            ".",
            ">",
            "results.sarif",
        ),
    }
)
_ADMITTED_SHEBANGS: Final = {
    ".sh": frozenset(
        {
            b"#!/bin/bash",
            b"#!/usr/bin/bash",
            b"#!/usr/bin/env bash",
        }
    ),
    ".py": frozenset(
        {
            b"#!/usr/bin/python3",
            b"#!/usr/bin/env python3",
        }
    ),
}


def _canonical_script_path(token: str) -> str | None:
    candidate = token[2:] if token.startswith("./") else token
    if _SCRIPT_PATH_RE.fullmatch(candidate) is None:
        return None
    relative = pathlib.PurePosixPath(candidate)
    if (
        relative.as_posix() != candidate
        or not relative.parts
        or relative.parts[0] != "scripts"
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        return None
    return candidate


def _looks_like_repo_script(token: str) -> bool:
    return (
        "scripts/" in token
        and (".sh" in token or ".py" in token)
    )


def _read_repo_script_bytes(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    *,
    maximum: int,
) -> bytes | None:
    if _canonical_script_path(relative.as_posix()) != relative.as_posix():
        return None
    descriptors: list[int] = []
    try:
        directory_flags = (
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptors.append(os.open(root, directory_flags))
        for part in relative.parts[:-1]:
            descriptor = os.open(
                part,
                directory_flags,
                dir_fd=descriptors[-1],
            )
            metadata = os.fstat(descriptor)
            if not stat.S_ISDIR(metadata.st_mode):
                os.close(descriptor)
                return None
            descriptors.append(descriptor)
        file_flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(
            relative.name,
            file_flags,
            dir_fd=descriptors[-1],
        )
        descriptors.append(descriptor)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_size > maximum:
            return None
        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        closed = os.fstat(descriptor)
        if (
            len(payload) != opened.st_size
            or len(payload) > maximum
            or opened.st_size != closed.st_size
            or (opened.st_dev, opened.st_ino)
            != (closed.st_dev, closed.st_ino)
            or not stat.S_ISREG(closed.st_mode)
        ):
            return None
        return payload
    except OSError:
        return None
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _read_public_gate_runner(root: pathlib.Path) -> str | None:
    payload = _read_repo_script_bytes(
        root,
        PUBLIC_GATE_RUNNER,
        maximum=MAX_AGGREGATE_BYTES,
    )
    if payload is None:
        return None
    try:
        return payload.decode("utf-8")
    except UnicodeError:
        return None


def _capture_parenthesized(
    source: str,
    start: int,
) -> tuple[str, int] | None:
    depth = 1
    index = start + 2
    quote: str | None = None
    while index < len(source):
        character = source[index]
        if character == "\\" and quote != "'":
            index += 2
            continue
        if quote == "'":
            if character == "'":
                quote = None
            index += 1
            continue
        if quote == '"':
            if character == '"':
                quote = None
                index += 1
                continue
            if source.startswith("$(", index):
                depth += 1
                index += 2
                continue
            if character == ")":
                depth -= 1
                if depth == 0:
                    return source[start + 2 : index], index + 1
            index += 1
            continue
        if character in {"'", '"'}:
            quote = character
            index += 1
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return source[start + 2 : index], index + 1
        index += 1
    return None


def _capture_backticks(
    source: str,
    start: int,
) -> tuple[str, int] | None:
    index = start + 1
    while index < len(source):
        if source[index] == "\\":
            index += 2
            continue
        if source[index] == "`":
            return source[start + 1 : index], index + 1
        index += 1
    return None


def _mask_shell_substitutions(
    source: str,
) -> tuple[str, tuple[_ShellSubstitution, ...]] | None:
    output: list[str] = []
    substitutions: list[_ShellSubstitution] = []
    quote: str | None = None
    index = 0
    while index < len(source):
        character = source[index]
        if character == "\\" and quote != "'":
            output.append(source[index : index + 2])
            index += 2
            continue
        if quote == "'":
            output.append(character)
            if character == "'":
                quote = None
            index += 1
            continue
        if character == "'" and quote is None:
            quote = "'"
            output.append(character)
            index += 1
            continue
        if character == '"':
            quote = None if quote == '"' else '"'
            output.append(character)
            index += 1
            continue
        kind: str | None = None
        capture: tuple[str, int] | None = None
        if source.startswith("$(", index):
            kind = "command"
            capture = _capture_parenthesized(source, index)
        elif source.startswith("<(", index) or source.startswith(">(", index):
            kind = "process"
            capture = _capture_parenthesized(source, index)
        elif character == "`":
            kind = "backtick"
            capture = _capture_backticks(source, index)
        if kind is None:
            output.append(character)
            index += 1
            continue
        if capture is None:
            return None
        body, next_index = capture
        placeholder = f"__TSDC_SUB_{len(substitutions):04d}__"
        substitutions.append(
            _ShellSubstitution(
                placeholder=placeholder,
                kind=kind,
                body=body,
            )
        )
        output.append(placeholder)
        index = next_index
    return "".join(output), tuple(substitutions)


def _heredoc_declarations(
    line: str,
) -> tuple[tuple[str, bool, bool], ...] | None:
    source = line
    declarations: list[tuple[str, bool, bool]] = []
    quote: str | None = None
    index = 0
    while index < len(source):
        character = source[index]
        if character == "\\" and quote != "'":
            index += 2
            continue
        if quote is not None:
            if character == quote:
                quote = None
            index += 1
            continue
        if character in {"'", '"'}:
            quote = character
            index += 1
            continue
        if character == "#":
            break
        if source.startswith("<<<", index):
            index += 3
            continue
        if not source.startswith("<<", index):
            index += 1
            continue
        index += 2
        strip_tabs = index < len(source) and source[index] == "-"
        if strip_tabs:
            index += 1
        while index < len(source) and source[index] in " \t":
            index += 1
        quoted = False
        if index < len(source) and source[index] in {"'", '"'}:
            quoted = True
            delimiter_quote = source[index]
            end = source.find(delimiter_quote, index + 1)
            if end == -1:
                return None
            delimiter = source[index + 1 : end]
            index = end + 1
        elif index < len(source) and source[index] == "\\":
            quoted = True
            index += 1
            match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", source[index:])
            if match is None:
                return None
            delimiter = match.group(0)
            index += len(delimiter)
        else:
            match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", source[index:])
            if match is None:
                return None
            delimiter = match.group(0)
            index += len(delimiter)
        declarations.append((delimiter, quoted, strip_tabs))
    return tuple(declarations)


def _shell_program_tokens(source: str) -> tuple[str, ...] | None:
    lexer = shlex.shlex(
        source,
        posix=True,
        punctuation_chars=_SHELL_PUNCTUATION,
    )
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = "#"
    try:
        raw_tokens = tuple(lexer)
    except ValueError:
        return None
    tokens: list[str] = []
    punctuation_pattern = re.compile(
        r"&&|\|\||<<-|<<|>>|[;&|<>()\n]"
    )
    for token in raw_tokens:
        if token and all(
            character in _SHELL_PUNCTUATION for character in token
        ):
            pieces = punctuation_pattern.findall(token)
            if "".join(pieces) != token:
                return None
            tokens.extend(pieces)
        else:
            tokens.append(token)
    return tuple(tokens)


def _prepare_shell_program(text: str) -> _PreparedShellProgram | None:
    retained: list[str] = []
    heredocs: list[tuple[str, bool, bool]] = []
    heredoc_substitutions: list[_ShellSubstitution] = []
    for raw_line in text.splitlines():
        if heredocs:
            delimiter, quoted, strip_tabs = heredocs[0]
            candidate = raw_line.lstrip("\t") if strip_tabs else raw_line
            if candidate == delimiter:
                heredocs.pop(0)
            elif not quoted:
                masked_body = _mask_shell_substitutions(raw_line)
                if masked_body is None:
                    return None
                heredoc_substitutions.extend(
                    substitution
                    for substitution in masked_body[1]
                    if substitution.kind in {"command", "backtick"}
                )
            retained.append("\n")
            continue
        declarations = _heredoc_declarations(raw_line)
        if declarations is None:
            return None
        heredocs.extend(declarations)
        retained.append(raw_line)
        retained.append("\n")
    if heredocs:
        return None
    source = "".join(retained)
    source = re.sub(r"\\\r?\n", " ", source)
    masked = _mask_shell_substitutions(source)
    if masked is None:
        return None
    tokens = _shell_program_tokens(masked[0])
    if tokens is None:
        return None
    return _PreparedShellProgram(
        tokens=tokens,
        substitutions=masked[1],
        heredoc_substitutions=tuple(heredoc_substitutions),
    )


def _shell_command_segments(
    tokens: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    segments: list[tuple[str, ...]] = []
    start = 0
    conditional_depth = 0
    for index, token in enumerate(tokens):
        if token == "[[":
            conditional_depth += 1
        elif token == "]]" and conditional_depth:
            conditional_depth -= 1
        if token not in _SHELL_SEPARATORS or conditional_depth:
            continue
        if start < index:
            segments.append(tokens[start:index])
        start = index + 1
    if start < len(tokens):
        segments.append(tokens[start:])
    return tuple(segments)


def _strip_shell_control_tokens(tokens: list[str]) -> list[str]:
    while tokens and tokens[0] in {
        "if",
        "then",
        "elif",
        "while",
        "until",
        "do",
        "else",
        "!",
        "{",
    }:
        tokens.pop(0)
    while tokens and tokens[-1] in {"then", "do", "fi", "done", "}"}:
        tokens.pop()
    return tokens


def _binding_for_value(
    value: str,
    bindings: dict[str, _VariableBinding],
    substitutions: dict[str, _ShellSubstitution],
) -> _VariableBinding:
    if value in substitutions:
        return _VariableBinding(literal=None, tainted=False)
    indirect = _INDIRECT_VARIABLE_RE.fullmatch(value)
    if indirect is not None:
        target = bindings.get(indirect.group(1))
        if target is not None and target.literal in bindings:
            return _VariableBinding(
                literal=None,
                tainted=bindings[target.literal].tainted,
            )
        return _VariableBinding(literal=None, tainted=True)
    variable = _VARIABLE_RE.fullmatch(value)
    if variable is not None:
        binding = bindings.get(variable.group(1) or variable.group(2))
        return binding or _VariableBinding(literal=None, tainted=False)
    if "$" in value or "`" in value:
        return _VariableBinding(
            literal=None,
            tainted=_looks_like_repo_script(value),
        )
    return _VariableBinding(
        literal=value,
        tainted=_looks_like_repo_script(value),
    )


def _resolve_shell_word(
    word: str,
    bindings: dict[str, _VariableBinding],
) -> _VariableBinding:
    indirect = _INDIRECT_VARIABLE_RE.fullmatch(word)
    if indirect is not None:
        pointer = bindings.get(indirect.group(1))
        if pointer is not None and pointer.literal in bindings:
            target = bindings[pointer.literal]
            return _VariableBinding(literal=None, tainted=target.tainted)
        return _VariableBinding(literal=None, tainted=True)
    variable = _VARIABLE_RE.fullmatch(word)
    if variable is not None:
        return bindings.get(
            variable.group(1) or variable.group(2),
            _VariableBinding(literal=None, tainted=False),
        )
    if "$" in word or "`" in word:
        return _VariableBinding(
            literal=None,
            tainted=_looks_like_repo_script(word),
        )
    return _VariableBinding(
        literal=word,
        tainted=_looks_like_repo_script(word),
    )


def _strip_safe_wrappers(
    tokens: list[str],
) -> tuple[list[str], bool]:
    invalid = False
    while tokens:
        if tokens[0] in {"command", "exec"}:
            tokens.pop(0)
            if tokens and tokens[0] == "--":
                tokens.pop(0)
            elif tokens and tokens[0].startswith("-"):
                invalid = True
            continue
        if tokens[0] != "env":
            break
        tokens.pop(0)
        while tokens:
            if tokens[0] == "--":
                tokens.pop(0)
                break
            if tokens[0] in {"-i", "--ignore-environment"}:
                tokens.pop(0)
                continue
            if tokens[0] in {"-u", "--unset"}:
                if len(tokens) < 2:
                    invalid = True
                    break
                del tokens[:2]
                continue
            if tokens[0].startswith("--unset="):
                tokens.pop(0)
                continue
            if _ASSIGNMENT_RE.fullmatch(tokens[0]):
                tokens.pop(0)
                continue
            break
        if tokens and tokens[0].startswith("-"):
            invalid = True
        continue
    return tokens, invalid


def _tokens_reference_repo_script(
    tokens: tuple[str, ...] | list[str],
    bindings: dict[str, _VariableBinding],
) -> bool:
    for token in tokens:
        resolved = _resolve_shell_word(token, bindings)
        if resolved.tainted:
            return True
        if (
            resolved.literal is not None
            and _canonical_script_path(resolved.literal) is not None
        ):
            return True
    return False


def _tokens_contain_script_text(
    tokens: tuple[str, ...] | list[str],
    bindings: dict[str, _VariableBinding],
) -> bool:
    return any(
        (
            (resolved := _resolve_shell_word(token, bindings)).tainted
            or (
                resolved.literal is not None
                and _looks_like_repo_script(resolved.literal)
            )
        )
        for token in tokens
    )


def _analyze_shell_program(
    text: str,
    *,
    allow_owner_substitution: bool,
) -> _ShellAnalysis:
    prepared = _prepare_shell_program(text)
    analysis = _ShellAnalysis(
        command_signatures=set(),
        script_invocations=[],
    )
    if prepared is None:
        analysis.invalid = True
        return analysis
    substitutions = {
        substitution.placeholder: substitution
        for substitution in prepared.substitutions
    }
    bindings: dict[str, _VariableBinding] = {}

    def analyze_substitution(
        substitution: _ShellSubstitution,
    ) -> _ShellAnalysis:
        return _analyze_shell_program(
            substitution.body,
            allow_owner_substitution=False,
        )

    def substitution_is_relevant(nested: _ShellAnalysis) -> bool:
        return bool(
            nested.script_invocations
            or (
                nested.command_signatures
                & _GOVERNED_NON_SCRIPT_SIGNATURES
            )
        )

    if prepared.heredoc_substitutions:
        analysis.invalid = True

    for raw_segment in _shell_command_segments(prepared.tokens):
        segment = _strip_shell_control_tokens(list(raw_segment))
        if not segment:
            continue
        segment_substitutions = [
            substitutions[token]
            for token in segment
            if token in substitutions
        ]
        for token in segment:
            assignment = _ASSIGNMENT_RE.fullmatch(token)
            if assignment is None:
                continue
            value = assignment.group(2)
            if value in substitutions:
                segment_substitutions.append(substitutions[value])
        approved_nested: list[_ShellAnalysis] = []
        for substitution in segment_substitutions:
            nested = analyze_substitution(substitution)
            assignment_only = (
                len(segment) == 1
                and (assignment := _ASSIGNMENT_RE.fullmatch(segment[0]))
                is not None
                and assignment.group(2) == substitution.placeholder
            )
            approved = (
                allow_owner_substitution
                and substitution.kind == "command"
                and assignment_only
                and _APPROVED_OWNER_SUBSTITUTION
                in nested.command_signatures
                and {
                    invocation.path
                    for invocation in nested.script_invocations
                }
                == {_APPROVED_OWNER_SUBSTITUTION[1]}
                and not nested.invalid
            )
            if approved:
                approved_nested.append(nested)
            elif substitution_is_relevant(nested):
                analysis.invalid = True
        for nested in approved_nested:
            analysis.command_signatures.update(nested.command_signatures)
            analysis.script_invocations.extend(nested.script_invocations)

        while segment and (assignment := _ASSIGNMENT_RE.fullmatch(segment[0])):
            name, value = assignment.groups()
            bindings[name] = _binding_for_value(
                value,
                bindings,
                substitutions,
            )
            segment.pop(0)
        if not segment:
            continue
        segment, wrapper_invalid = _strip_safe_wrappers(segment)
        if not segment:
            continue
        segment = _strip_shell_control_tokens(segment)
        if not segment:
            continue
        signature = tuple(segment)
        analysis.command_signatures.add(signature)
        executable_binding = _resolve_shell_word(segment[0], bindings)
        executable = executable_binding.literal
        relevant = _tokens_reference_repo_script(segment, bindings)
        if wrapper_invalid and relevant:
            analysis.invalid = True
            continue
        if executable in _DATA_ONLY_COMMANDS:
            continue
        if executable in {"eval", "source", "."}:
            if (
                _tokens_contain_script_text(segment[1:], bindings)
                or segment_substitutions
            ):
                analysis.invalid = True
            continue
        if executable in {"bash", "sh", "zsh", "python", "python3"}:
            arguments = segment[1:]
            if "-c" in arguments:
                if (
                    _tokens_contain_script_text(arguments, bindings)
                    or segment_substitutions
                ):
                    analysis.invalid = True
                continue
            while arguments and arguments[0] == "--":
                arguments.pop(0)
            if not arguments or (
                executable in {"python", "python3"}
                and arguments[0] == "-m"
            ):
                continue
            script_binding = _resolve_shell_word(arguments[0], bindings)
            if script_binding.literal is None:
                analysis.invalid = True
                continue
            script_path = _canonical_script_path(script_binding.literal)
            if script_path is None:
                if _looks_like_repo_script(script_binding.literal):
                    analysis.invalid = True
                continue
            suffix = pathlib.PurePosixPath(script_path).suffix
            if (
                executable in {"bash", "sh", "zsh"}
                and suffix != ".sh"
            ) or (
                executable in {"python", "python3"}
                and suffix != ".py"
            ):
                analysis.invalid = True
                continue
            analysis.script_invocations.append(
                _ScriptInvocation(path=script_path, direct=False)
            )
            continue
        if executable is None:
            if (
                _VARIABLE_RE.fullmatch(segment[0])
                or _INDIRECT_VARIABLE_RE.fullmatch(segment[0])
                or executable_binding.tainted
                or relevant
            ):
                analysis.invalid = True
            continue
        direct_path = _canonical_script_path(executable)
        if direct_path is not None:
            analysis.script_invocations.append(
                _ScriptInvocation(path=direct_path, direct=True)
            )
            continue
        if _looks_like_repo_script(executable) or relevant:
            analysis.invalid = True
    return analysis


def _python_call_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        owner = _python_call_name(node.value)
        return f"{owner}.{node.attr}" if owner else node.attr
    return None


def _literal_python_command(node: ast.expr) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values: list[str] = []
    for element in node.elts:
        if not (
            isinstance(element, ast.Constant)
            and isinstance(element.value, str)
        ):
            return None
        values.append(element.value)
    return shlex.join(values)


def _analyze_python_helper(text: str) -> _ShellAnalysis:
    analysis = _ShellAnalysis(
        command_signatures=set(),
        script_invocations=[],
    )
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        analysis.invalid = True
        return analysis
    admitted_calls = {
        "os.execl",
        "os.execle",
        "os.execlp",
        "os.execlpe",
        "os.execv",
        "os.execve",
        "os.execvp",
        "os.execvpe",
        "os.system",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
        "subprocess.run",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _python_call_name(node.func) not in admitted_calls or not node.args:
            continue
        command = _literal_python_command(node.args[0])
        if command is None:
            continue
        nested = _analyze_shell_program(
            command,
            allow_owner_substitution=False,
        )
        analysis.command_signatures.update(nested.command_signatures)
        analysis.script_invocations.extend(nested.script_invocations)
        analysis.invalid = analysis.invalid or nested.invalid
    return analysis


def _tracked_executable_mode(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
) -> bool:
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                os.fspath(root),
                "ls-files",
                "--stage",
                "--",
                relative.as_posix(),
            ],
            check=False,
            capture_output=True,
            env={
                **os.environ,
                "GIT_LITERAL_PATHSPECS": "1",
                "LC_ALL": "C",
            },
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if result.returncode != 0 or len(result.stdout) > 4_096:
        return False
    match = re.fullmatch(
        rb"100755 [0-9a-f]{40,64} 0\t([^\x00\r\n]+)\n?",
        result.stdout,
    )
    return (
        match is not None
        and match.group(1).decode("utf-8", errors="ignore")
        == relative.as_posix()
    )


def _direct_script_admitted(
    root: pathlib.Path,
    relative: pathlib.PurePosixPath,
    payload: bytes,
) -> bool:
    if not _tracked_executable_mode(root, relative):
        return False
    try:
        metadata = root.joinpath(*relative.parts).lstat()
    except OSError:
        return False
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_mode & 0o111 == 0
    ):
        return False
    shebang = payload.splitlines()[0] if payload.splitlines() else b""
    return shebang in _ADMITTED_SHEBANGS.get(relative.suffix, frozenset())


def _governed_script_paths() -> frozenset[str]:
    return frozenset()


def _merge_shell_analysis(
    resolution: _SemanticResolution,
    analysis: _ShellAnalysis,
) -> None:
    resolution.command_signatures.update(analysis.command_signatures)
    resolution.script_paths.update(
        invocation.path for invocation in analysis.script_invocations
    )


def _resolve_job_semantics(
    root: pathlib.Path,
    programs: tuple[str, ...],
) -> _SemanticResolution:
    resolution = _SemanticResolution(
        command_signatures=set(),
        script_paths=set(),
    )
    governed = _governed_script_paths()
    budget = _TraversalBudget(visited=set(), stack=[])

    def mark_invalid(*, aggregate: bool) -> None:
        if aggregate:
            resolution.aggregate_invalid = True
        else:
            resolution.invalid = True

    def walk_script(
        invocation: _ScriptInvocation,
        *,
        depth: int,
        aggregate: bool,
    ) -> None:
        relative = pathlib.PurePosixPath(invocation.path)
        if invocation.direct:
            resolution.script_paths.discard(invocation.path)
        maximum = (
            MAX_AGGREGATE_BYTES
            if relative == PUBLIC_GATE_RUNNER
            else MAX_SEMANTIC_HELPER_BYTES
        )
        payload = _read_repo_script_bytes(
            root,
            relative,
            maximum=maximum,
        )
        if payload is None:
            mark_invalid(aggregate=aggregate)
            return
        if invocation.direct and not _direct_script_admitted(
            root,
            relative,
            payload,
        ):
            mark_invalid(aggregate=aggregate)
            return
        if invocation.direct:
            resolution.script_paths.add(invocation.path)
        if (
            invocation.path in governed
            and relative != PUBLIC_GATE_RUNNER
        ):
            return
        if depth > MAX_SEMANTIC_HELPER_DEPTH:
            mark_invalid(aggregate=aggregate)
            return
        if invocation.path in budget.stack:
            mark_invalid(aggregate=aggregate)
            return
        if invocation.path in budget.visited:
            return
        budget.files += 1
        budget.total_bytes += len(payload)
        if (
            budget.files > MAX_SEMANTIC_HELPER_FILES
            or budget.total_bytes > MAX_SEMANTIC_HELPER_TOTAL_BYTES
        ):
            mark_invalid(aggregate=aggregate)
            return
        budget.visited.add(invocation.path)
        budget.stack.append(invocation.path)
        try:
            if relative.suffix == ".py":
                text = payload.decode("utf-8")
                analysis = _analyze_python_helper(text)
                _merge_shell_analysis(resolution, analysis)
                if analysis.invalid:
                    mark_invalid(aggregate=aggregate)
                for child in analysis.script_invocations:
                    if child.path in governed:
                        if child.direct:
                            walk_script(
                                child,
                                depth=depth + 1,
                                aggregate=aggregate,
                            )
                        continue
                    walk_script(
                        child,
                        depth=depth + 1,
                        aggregate=aggregate,
                    )
                return
            text = payload.decode("utf-8")
            analysis = _analyze_shell_program(
                text,
                allow_owner_substitution=False,
            )
            _merge_shell_analysis(resolution, analysis)
            if analysis.invalid:
                mark_invalid(aggregate=aggregate)
            for child in analysis.script_invocations:
                if child.path in governed:
                    if child.direct:
                        walk_script(
                            child,
                            depth=depth + 1,
                            aggregate=aggregate,
                        )
                    continue
                walk_script(
                    child,
                    depth=depth + 1,
                    aggregate=aggregate,
                )
        except UnicodeError:
            mark_invalid(aggregate=aggregate)
        finally:
            budget.stack.pop()

    for program in programs:
        analysis = _analyze_shell_program(
            program,
            allow_owner_substitution=True,
        )
        _merge_shell_analysis(resolution, analysis)
        if analysis.invalid:
            resolution.invalid = True
        for invocation in analysis.script_invocations:
            aggregate = invocation.path == PUBLIC_GATE_RUNNER.as_posix()
            if invocation.direct:
                if aggregate or invocation.path in governed:
                    walk_script(
                        invocation,
                        depth=0,
                        aggregate=aggregate,
                    )
            elif aggregate:
                walk_script(
                    invocation,
                    depth=0,
                    aggregate=aggregate,
                )
    return resolution


def _semantic_command_marker(command: str) -> str:
    repository_script = re.search(
        r"scripts/[A-Za-z0-9_./-]+\.(?:py|sh)",
        command,
    )
    return repository_script.group(0) if repository_script else command


def _semantic_command_signatures(command: str) -> frozenset[tuple[str, ...]]:
    analysis = _analyze_shell_program(
        command,
        allow_owner_substitution=True,
    )
    return frozenset(analysis.command_signatures)


def _finding(code: str, path: str, message: str) -> WorkflowFinding:
    return WorkflowFinding(code=code, path=path, message=message)


def _permission_baseline_findings(
    documents_by_path: dict[str, WorkflowDocument],
    specs_by_path: dict[str, WorkflowSpec],
) -> tuple[WorkflowFinding, ...]:
    findings: list[WorkflowFinding] = []
    baselines_by_path = dict(_WORKFLOW_PERMISSION_BASELINES)
    baseline_paths = set(baselines_by_path)
    if (
        set(documents_by_path) != baseline_paths
        or set(specs_by_path) != baseline_paths
    ):
        findings.append(
            _finding(
                "workflow-permission-baseline-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "workflow permission ownership differs from the code baseline",
            )
        )

    for path in sorted(
        baseline_paths & set(documents_by_path) & set(specs_by_path)
    ):
        baseline = baselines_by_path[path]
        document = documents_by_path[path]
        spec = specs_by_path[path]
        expected_top_level = dict(baseline.top_level)
        baseline_valid = (
            spec.permissions == expected_top_level
            and "permissions" in document.data
            and document.data["permissions"] == expected_top_level
        )

        expected_jobs = dict(baseline.jobs)
        raw_jobs = document.data.get("jobs")
        if (
            set(spec.jobs) != set(expected_jobs)
            or not isinstance(raw_jobs, dict)
            or set(raw_jobs) != set(expected_jobs)
        ):
            baseline_valid = False
        else:
            for job_id, permission_items in expected_jobs.items():
                raw_job = raw_jobs.get(job_id)
                contract_job = spec.jobs.get(job_id)
                if not isinstance(raw_job, dict) or contract_job is None:
                    baseline_valid = False
                    continue
                if permission_items is None:
                    if (
                        contract_job.permissions is not None
                        or "permissions" in raw_job
                    ):
                        baseline_valid = False
                    continue
                expected_permissions = dict(permission_items)
                if (
                    contract_job.permissions != expected_permissions
                    or "permissions" not in raw_job
                    or raw_job["permissions"] != expected_permissions
                ):
                    baseline_valid = False

        if not baseline_valid:
            findings.append(
                _finding(
                    "workflow-permission-baseline-invalid",
                    path,
                    "workflow permissions differ from the code baseline",
                )
            )
    return tuple(findings)


def validate_workflows(
    root: pathlib.Path,
    contract: WorkflowContract,
) -> tuple[WorkflowFinding, ...]:
    findings: list[WorkflowFinding] = [
        _finding(finding.code, finding.path, finding.message)
        for finding in validate_gate_registry(root, contract.gate_registry)
    ]
    try:
        documents = load_workflows(root)
    except WorkflowContractError as error:
        return (_finding(error.code, error.path, error.message),)
    documents_by_path = {document.path: document for document in documents}
    specs_by_path = {spec.path: spec for spec in contract.workflows}
    findings.extend(
        _permission_baseline_findings(documents_by_path, specs_by_path)
    )
    for path in sorted(set(specs_by_path) - set(documents_by_path)):
        findings.append(
            _finding("workflow-missing", path, "registered workflow is missing")
        )
    for path in sorted(set(documents_by_path) - set(specs_by_path)):
        findings.append(
            _finding("workflow-unregistered", path, "tracked workflow is unregistered")
        )

    job_owners: dict[str, str] = {}
    action_consumers: dict[tuple[str, str], set[str]] = {}
    sha_pattern = re.compile(r"[0-9a-f]{40}")
    forbidden_events = {"pull_request_target", "workflow_run", "workflow_call"}
    workflow_names: dict[str, str] = {}
    for document in documents:
        workflow_name = document.data.get("name")
        if isinstance(workflow_name, str):
            normalized_name = " ".join(workflow_name.split()).casefold()
            previous_path = workflow_names.get(normalized_name)
            if previous_path is not None:
                findings.append(
                    _finding(
                        "workflow-name-duplicate",
                        document.path,
                        "workflow name is duplicated",
                    )
                )
            else:
                workflow_names[normalized_name] = document.path
        raw_jobs = document.data.get("jobs")
        if not isinstance(raw_jobs, dict):
            continue
        for job_id in raw_jobs:
            if not isinstance(job_id, str):
                continue
            previous_path = job_owners.get(job_id)
            if previous_path is not None:
                findings.append(
                    _finding(
                        "workflow-job-identity-duplicate",
                        document.path,
                        "job identity is duplicated across workflows",
                    )
                )
            else:
                job_owners[job_id] = document.path
    for path in sorted(set(specs_by_path) & set(documents_by_path)):
        spec = specs_by_path[path]
        document = documents_by_path[path]
        data = document.data
        if data.get("name") != spec.name:
            findings.append(
                _finding("workflow-name-mismatch", path, "workflow name differs from the contract")
            )
        trigger = data.get("on")
        if not isinstance(trigger, dict):
            findings.append(
                _finding("workflow-trigger-invalid", path, "workflow triggers must be a mapping")
            )
            trigger = {}
        for event in sorted(set(trigger) & forbidden_events):
            findings.append(
                _finding(
                    "workflow-trigger-forbidden",
                    path,
                    f"forbidden event is configured: {event}",
                )
            )
        if trigger != spec.trigger_document:
            findings.append(
                _finding(
                    "workflow-trigger-mismatch",
                    path,
                    "events, branches, paths, types, tags, or schedules differ from the contract",
                )
            )
        permissions = data.get("permissions")
        if permissions == "write-all":
            findings.append(
                _finding("workflow-permission-write-all", path, "write-all is forbidden")
            )
        if permissions != spec.permissions:
            findings.append(
                _finding(
                    "workflow-permission-mismatch",
                    path,
                    "top-level permissions differ from the contract",
                )
            )
        if data.get("concurrency") != spec.concurrency:
            findings.append(
                _finding(
                    "workflow-concurrency-mismatch",
                    path,
                    "concurrency differs from the contract",
                )
            )
        raw_jobs = data.get("jobs")
        if not isinstance(raw_jobs, dict):
            findings.append(
                _finding("workflow-jobs-invalid", path, "jobs must be a mapping")
            )
            raw_jobs = {}
        if set(raw_jobs) != set(spec.jobs):
            findings.append(
                _finding(
                    "workflow-job-set-mismatch",
                    path,
                    "job IDs differ from the contract",
                )
            )
        if spec.classification == "required-quality":
            findings.extend(
                _workflow_projection_findings(
                    path,
                    data,
                    raw_jobs,
                    contract,
                )
            )
        for job_id, raw_job in raw_jobs.items():
            if not isinstance(job_id, str) or not isinstance(raw_job, dict):
                findings.append(
                    _finding("workflow-job-invalid", path, "job definition is invalid")
                )
                continue
            expected_job = spec.jobs.get(job_id)
            if expected_job is None:
                continue
            if raw_job.get("permissions") != expected_job.permissions:
                findings.append(
                    _finding(
                        "workflow-job-permission-mismatch",
                        path,
                        f"job {job_id} permissions differ from the contract",
                    )
                )
            if raw_job.get("runs-on") != expected_job.runs_on:
                findings.append(
                    _finding(
                        "workflow-job-runner-mismatch",
                        path,
                        f"job {job_id} runner differs from the contract",
                    )
                )
            if raw_job.get("timeout-minutes") != expected_job.timeout_minutes:
                findings.append(
                    _finding(
                        "workflow-job-timeout-mismatch",
                        path,
                        f"job {job_id} timeout differs from the contract",
                    )
                )
            steps = raw_job.get("steps")
            if not isinstance(steps, list):
                continue
            step_names: set[str] = set()
            for step in steps:
                if not isinstance(step, dict):
                    continue
                step_name = step.get("name")
                if not isinstance(step_name, str) or not step_name.strip():
                    findings.append(
                        _finding(
                            "workflow-step-name-missing",
                            path,
                            f"job {job_id} contains an unnamed step",
                        )
                    )
                elif step_name in step_names:
                    findings.append(
                        _finding(
                            "workflow-step-name-duplicate",
                            path,
                            f"job {job_id} contains a duplicate step name",
                        )
                    )
                else:
                    step_names.add(step_name)
                if step.get("continue-on-error") is not None:
                    findings.append(
                        _finding(
                            "workflow-continue-on-error-forbidden",
                            path,
                            f"job {job_id} weakens failure handling",
                        )
                    )
                run = step.get("run")
                if isinstance(run, str) and "${{" in run:
                    findings.append(
                        _finding(
                            "workflow-run-interpolation-unsafe",
                            path,
                            f"job {job_id} interpolates an Actions expression directly in run",
                        )
                    )
                if (
                    job_id == "zizmor"
                    and isinstance(run, str)
                    and "zizmor" in run
                    and "env" in step
                ):
                    findings.append(
                        _finding(
                            "workflow-zizmor-env-forbidden",
                            path,
                            "zizmor must not receive a credential environment",
                        )
                    )
                if isinstance(run, str) and re.search(
                    r"(?im)(?:\bgit\s+push\b|\bgh\s+(?:api\b[^\n]*"
                    r"(?:--method|-X)\s*(?:POST|PUT|PATCH|DELETE)|"
                    r"pr\s+(?:create|merge)|release\s+create|workflow\s+run)|"
                    r"\bcurl\b[^\n]*(?:-X|--request)\s*"
                    r"(?:POST|PUT|PATCH|DELETE)|\bdocker\s+push\b|"
                    r"\bnpm\s+publish\b)",
                    run,
                ):
                    findings.append(
                        _finding(
                            "workflow-remote-mutation-forbidden",
                            path,
                            f"job {job_id} contains a remote mutation command",
                        )
                    )
                uses = step.get("uses")
                if not isinstance(uses, str):
                    continue
                if uses.startswith("./"):
                    findings.append(
                        _finding(
                            "action-local-reference-forbidden",
                            path,
                            "local Action references are not approved",
                        )
                    )
                    continue
                if "@" not in uses:
                    findings.append(
                        _finding(
                            "action-ref-mutable",
                            path,
                            "direct Action reference is missing a full SHA",
                        )
                    )
                    continue
                action, sha = uses.rsplit("@", 1)
                if action.casefold() == "actions/upload-artifact":
                    findings.append(
                        _finding(
                            "workflow-artifact-upload-forbidden",
                            path,
                            "artifact upload is outside the approved workflow contract",
                        )
                    )
                if sha_pattern.fullmatch(sha) is None:
                    findings.append(
                        _finding(
                            "action-ref-mutable",
                            path,
                            "direct Action reference is not a full SHA",
                        )
                    )
                    continue
                action_consumers.setdefault((action, sha), set()).add(path)

    registry_identities = tuple(
        (action.action, action.sha) for action in contract.actions
    )
    if registry_identities != _ACTION_REGISTRY_BASELINE:
        findings.append(
            _finding(
                "action-registry-baseline-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "Action registry identities differ from the code baseline",
            )
        )
    registry = {(action.action, action.sha): action for action in contract.actions}
    for action in contract.actions:
        registry_path = WORKFLOW_CONTRACT.as_posix()
        if re.fullmatch(r"[0-9a-f]{40}", action.sha) is None:
            findings.append(
                _finding("action-registry-sha-invalid", registry_path, "Action SHA is invalid")
            )
        if action.runtime.casefold() in {"node20", "node16", "node12"}:
            findings.append(
                _finding(
                    "action-runtime-unsupported",
                    registry_path,
                    "Action runtime is retired",
                )
            )
        if action.runtime not in {"node24", "composite"}:
            findings.append(
                _finding(
                    "action-runtime-unapproved",
                    registry_path,
                    "Action runtime evidence is not approved",
                )
            )
        repository_parts = action.action.split("/")
        action_subpath = "/".join(repository_parts[2:])
        manifest_path = f"{action_subpath}/action.yml" if action_subpath else "action.yml"
        expected_url = (
            "https://raw.githubusercontent.com/"
            f"{repository_parts[0]}/{repository_parts[1]}/{action.sha}/{manifest_path}"
            if len(repository_parts) >= 2
            else ""
        )
        if (
            action.manifest_url != expected_url
            or action.retrieved_at != "2026-07-28"
            or action.security_disposition
            not in {"approved-node24", "approved-composite-reviewed"}
        ):
            findings.append(
                _finding(
                    "action-evidence-invalid",
                    registry_path,
                    "Action manifest evidence is incomplete or inconsistent",
                )
            )
        actual_consumers = action_consumers.get((action.action, action.sha), set())
        if actual_consumers != set(action.consumers):
            findings.append(
                _finding(
                    "action-consumer-mismatch",
                    registry_path,
                    "Action consumers differ from the registry",
                )
            )
    for identity in sorted(set(action_consumers) - set(registry)):
        findings.append(
            _finding(
                "action-unregistered",
                WORKFLOW_CONTRACT.as_posix(),
                "direct Action reference is not registered",
            )
        )
    if any(action.action == "pre-commit/action" for action in contract.actions):
        findings.append(
            _finding(
                "action-precommit-composite-forbidden",
                WORKFLOW_CONTRACT.as_posix(),
                "the mutable transitive pre-commit Action path is forbidden",
            )
        )
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate tracked GitHub workflows")
    parser.add_argument("--root", type=pathlib.Path)
    arguments = parser.parse_args(argv)
    root = (
        arguments.root.resolve()
        if arguments.root is not None
        else pathlib.Path(__file__).resolve().parents[3]
    )
    try:
        contract = load_workflow_contract(root)
    except WorkflowContractError as error:
        print(f"FAIL [{error.code}] {error.path}: {error.message}", file=sys.stderr)
        return 1
    findings = validate_workflows(root, contract)
    if findings:
        for finding in findings:
            print(
                f"FAIL [{finding.code}] {finding.path}: {finding.message}",
                file=sys.stderr,
            )
        return 1
    job_count = sum(len(workflow.jobs) for workflow in contract.workflows)
    print(
        "PASS: GitHub workflow contract "
        f"(workflows={len(contract.workflows)}, jobs={job_count}, "
        f"actions={len(contract.actions)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
