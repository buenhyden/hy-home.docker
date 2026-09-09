from __future__ import annotations

import argparse
import dataclasses
import os
import pathlib
import re
import stat
import sys
from typing import Final

import yaml

try:
    from scripts.lib.gate.ci_gate_contract import (
        CI_DEPENDENCY_BOOTSTRAP,
        GateContractError,
        GateRegistry,
        load_contract_document,
        parse_gate_registry,
        parse_public_gate_contract,
        public_root_gate_ids,
        select_public_suites,
        validate_gate_registry,
    )
except ModuleNotFoundError:  # Direct sibling-script execution.
    from ci_gate_contract import (  # type: ignore[no-redef]
        CI_DEPENDENCY_BOOTSTRAP,
        GateContractError,
        GateRegistry,
        load_contract_document,
        parse_gate_registry,
        parse_public_gate_contract,
        public_root_gate_ids,
        select_public_suites,
        validate_gate_registry,
    )

WORKFLOW_CONTRACT: Final = pathlib.PurePosixPath(".github/workflow-contract.yml")
WORKFLOW_ROOT: Final = pathlib.PurePosixPath(".github/workflows")
MAX_YAML_BYTES: Final = 2 * 1_048_576
MAX_WORKFLOWS: Final = 128


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
                    (
                        ("contents", "read"),
                        ("issues", "write"),
                        ("pull-requests", "read"),
                    ),
                ),
                (
                    "pull-request-greeting",
                    (
                        ("contents", "read"),
                        ("issues", "read"),
                        ("pull-requests", "write"),
                    ),
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
        "4391f3da665fdf50b6810c1a66712fb9ba21aa93",
    ),
    (
        "astral-sh/setup-uv",
        "20cfd1bf945f4377ade1205e4dbc17946fc9a30d",
    ),
    (
        "github/codeql-action/upload-sarif",
        "cdf488f595d80d6e07e03d4674febd5ab45fa938",
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
        if isinstance(key_node, yaml.nodes.ScalarNode) and key_node.value == "on":
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
            if not stat.S_ISREG(opened_metadata.st_mode) or (
                metadata.st_dev,
                metadata.st_ino,
            ) != (opened_metadata.st_dev, opened_metadata.st_ino):
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
    boolean_on_keys = tuple(key for key in data if type(key) is bool and key is True)
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
            if not isinstance(concurrency_mapping["group"], str) or not isinstance(
                concurrency_mapping["cancel-in-progress"], bool
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
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        return None
    return set(value)


def _workflow_projection_findings(
    path: str,
    raw_workflow: dict[object, object],
    raw_jobs: dict[object, object],
    contract: WorkflowContract,
) -> tuple[WorkflowFinding, ...]:
    findings: list[WorkflowFinding] = []
    if "env" in raw_workflow:
        findings.append(
            _finding(
                "workflow-gate-environment-invalid",
                path,
                "required workflow top-level environment is forbidden",
            )
        )
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
            selected_profile = (
                "bootstrap"
                if program == CI_DEPENDENCY_BOOTSTRAP
                else _static_gate_profile(program)
            )
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


def _finding(code: str, path: str, message: str) -> WorkflowFinding:
    return WorkflowFinding(code=code, path=path, message=message)


def _permission_baseline_findings(
    documents_by_path: dict[str, WorkflowDocument],
    specs_by_path: dict[str, WorkflowSpec],
) -> tuple[WorkflowFinding, ...]:
    findings: list[WorkflowFinding] = []
    baselines_by_path = dict(_WORKFLOW_PERMISSION_BASELINES)
    baseline_paths = set(baselines_by_path)
    if set(documents_by_path) != baseline_paths or set(specs_by_path) != baseline_paths:
        findings.append(
            _finding(
                "workflow-permission-baseline-invalid",
                WORKFLOW_CONTRACT.as_posix(),
                "workflow permission ownership differs from the code baseline",
            )
        )

    for path in sorted(baseline_paths & set(documents_by_path) & set(specs_by_path)):
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
                    if contract_job.permissions is not None or "permissions" in raw_job:
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
    findings.extend(_permission_baseline_findings(documents_by_path, specs_by_path))
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
                _finding(
                    "workflow-name-mismatch",
                    path,
                    "workflow name differs from the contract",
                )
            )
        trigger = data.get("on")
        if not isinstance(trigger, dict):
            findings.append(
                _finding(
                    "workflow-trigger-invalid",
                    path,
                    "workflow triggers must be a mapping",
                )
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
                _finding(
                    "workflow-permission-write-all", path, "write-all is forbidden"
                )
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
                _finding(
                    "action-registry-sha-invalid",
                    registry_path,
                    "Action SHA is invalid",
                )
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
        manifest_path = (
            f"{action_subpath}/action.yml" if action_subpath else "action.yml"
        )
        expected_url = (
            "https://raw.githubusercontent.com/"
            f"{repository_parts[0]}/{repository_parts[1]}/{action.sha}/{manifest_path}"
            if len(repository_parts) >= 2
            else ""
        )
        if (
            action.manifest_url != expected_url
            or action.retrieved_at != "2026-09-02"
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
