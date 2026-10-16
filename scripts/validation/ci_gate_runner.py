from __future__ import annotations

import argparse
import collections.abc
import contextlib
import dataclasses
import datetime
import enum
import errno
import hashlib
import json
import os
import pathlib
import re
import select
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Mapping

if __package__ in {None, ""}:
    _BOOTSTRAP_ROOT = pathlib.Path(__file__).resolve().parents[2]
    if str(_BOOTSTRAP_ROOT) not in sys.path:
        sys.path.insert(0, str(_BOOTSTRAP_ROOT))

from scripts.lib.gate import ci_gate_adapters
from scripts.lib.gate.ci_gate_contract import (
    HOSTED_UNIT_GATE_IDS,
    PUBLIC_SUITE_NAMES,
    GateContractError,
    GateRegistry,
    PublicGateContract,
    PublicValidatorRoute,
    expand_public_gate_ids,
    load_contract_document,
    parse_gate_registry,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
    validate_gate_registry,
    validate_public_execution_argv,
)
from scripts.lib.gate.ci_gate_evidence import (
    EvidenceError,
    EvidenceStore,
    capture_controller_toolchain,
    capture_runtime_observation,
)

_GIT_TIMEOUT_SECONDS = 5
_SHEBANGS = {
    b"#!/usr/bin/env bash": "bash",
    b"#!/usr/bin/env python3": "python",
}
_SECRET_ENV_SHAPE = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL|AUTH|API_KEY|PRIVATE_KEY)",
    re.IGNORECASE,
)
_ADMITTED_ENV_KEYS = frozenset(
    # Exactly the keys some gate node declares. The runner reads EVENT_NAME,
    # PR_BASE_SHA, PR_HEAD_SHA, and PUSH_BEFORE_SHA from its controller, so
    # they are not admitted here; a node that needs one is added deliberately.
    {
        "CI",
        "GITHUB_ACTIONS",
        "PR_BASE_SHA",
        "PR_HEAD_SHA",
        "TEMPLATE_GATE_BASE",
    }
)
_TERMINATION_GRACE_SECONDS = 0.25
_MAX_PROC_PID_ENTRIES = 65_536
_MAX_PROC_STAT_BYTES = 4_096
_PROC_ROOT = pathlib.Path("/proc")
_MAX_CHANGED_PATH_BYTES = 1024 * 1024
_MAX_CHANGED_PATHS = 10_000
_FULL_SHA = re.compile(r"[0-9a-f]{40}\Z")
_LOCAL_EXCLUDED_GATE_IDS = frozenset(
    {
        "leaf.dependency-vulnerability-audit",
        "leaf.frontend-build",
        "leaf.frontend-lint",
        "leaf.frontend-quality",
        "leaf.frontend-typecheck",
        "leaf.opsflow-smtp-node-coverage",
        "leaf.opsflow-smtp-npm-audit",
        "leaf.opsflow-smtp-npm-production-audit",
        "leaf.opsflow-smtp-package",
        "leaf.changed-style",
        "leaf.commit-message-contract",
        "leaf.storybook-coverage",
        "leaf.zizmor",
    }
)
_PR_ONLY_GATE_IDS = frozenset({"leaf.changed-style", "leaf.commit-message-contract"})


def _trusted_git_executable(environ: Mapping[str, str]) -> str:
    value = environ.get("TRUSTED_GIT_PATH", "")
    path = pathlib.Path(value)
    try:
        metadata = path.stat()
    except OSError:
        metadata = None
    if (
        not path.is_absolute()
        or ".." in path.parts
        or metadata is None
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_uid != 0
        or metadata.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
        or not os.access(path, os.X_OK)
    ):
        raise GateContractError(
            "ci-gate-execution-context",
            "git",
            "hosted execution requires the pre-install system Git executable",
        )
    return str(path)


@dataclasses.dataclass(frozen=True, slots=True)
class GateInvocation:
    gate_id: str
    entrypoint: pathlib.PurePosixPath
    argv: tuple[str, ...]
    cwd: pathlib.PurePosixPath
    allowed_env_keys: tuple[str, ...]
    timeout_seconds: int


@dataclasses.dataclass(frozen=True, slots=True)
class SelectedPrerequisites:
    node: bool
    docker: bool


@dataclasses.dataclass(frozen=True, slots=True)
class ExecutionEvidenceRequest:
    directory: pathlib.Path
    identity: Mapping[str, object]
    selection_reasons: Mapping[str, str]
    retention_days: int
    toolchain: Mapping[str, object] | None = None
    runtime_observation: Mapping[str, object] | None = None


class _ChildOutcome(int):
    timed_out: bool

    def __new__(cls, value: int, *, timed_out: bool = False) -> _ChildOutcome:
        outcome = int.__new__(cls, value)
        outcome.timed_out = timed_out
        return outcome


class _ExecutionCancelled(BaseException):
    def __init__(self, signum: int) -> None:
        super().__init__(signum)
        self.signum = signum


@contextlib.contextmanager
def _cancellation_handlers() -> collections.abc.Iterator[None]:
    if threading.current_thread() is not threading.main_thread():
        yield
        return
    signums = tuple(
        signum
        for signum in (signal.SIGINT, signal.SIGTERM, getattr(signal, "SIGHUP", None))
        if isinstance(signum, int)
    )
    previous: dict[int, object] = {}

    def cancel(signum: int, _frame: object) -> None:
        raise _ExecutionCancelled(signum)

    try:
        for signum in signums:
            previous[signum] = signal.signal(signum, cancel)
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


GateExecutor = collections.abc.Callable[[GateInvocation], int]


class ExecutionContext(enum.Enum):
    LOCAL = "local"
    PULL_REQUEST = "pull_request"
    PUSH = "push"
    PUSH_INITIAL = "push_initial"
    WORKFLOW_DISPATCH = "workflow_dispatch"


_INTERNAL_ADAPTER_PATH = pathlib.PurePosixPath("scripts/lib/gate/ci_gate_adapters.py")
_PR_STYLE_INVOCATION = (
    pathlib.PurePosixPath("scripts/validation/run-ci-precommit.sh"),
    ("--mode", "pr-merge"),
)
_INTERNAL_CHECK_INVOCATIONS = frozenset(
    (pathlib.PurePosixPath(path), argv)
    for path, argv in (
        ("scripts/operations/provider_surface_renderer.py", ("--check",)),
        ("scripts/operations/sync-tech-stack-versions.sh", ("--check",)),
        ("scripts/validation/check-github-workflow-contract.py", ()),
        ("scripts/validation/check-operations-catalog.py", ()),
        ("scripts/validation/check-script-manifest.py", ()),
        ("scripts/validation/check-storybook-contract.sh", ()),
        ("scripts/validation/validate-docker-compose.sh", ()),
        ("scripts/validation/run-ci-precommit.sh", ("--mode", "pr-merge")),
        ("tests/validation/test_run_ci_precommit.sh", ()),
    )
)


def _is_admitted_internal_invocation(
    invocation: GateInvocation,
    context: ExecutionContext,
    hosted_unit_bindings: tuple[
        tuple[str, pathlib.PurePosixPath, tuple[str, ...]], ...
    ],
) -> bool:
    if invocation.entrypoint == _INTERNAL_ADAPTER_PATH:
        if (
            context is ExecutionContext.PULL_REQUEST
            and invocation.gate_id in HOSTED_UNIT_GATE_IDS
        ):
            return (
                invocation.gate_id,
                invocation.entrypoint,
                invocation.argv,
            ) in hosted_unit_bindings
        return ci_gate_adapters.admits_adapter_invocation(
            invocation.argv, context.value
        )
    identity = (invocation.entrypoint, invocation.argv)
    if identity == _PR_STYLE_INVOCATION:
        return context is ExecutionContext.PULL_REQUEST
    return identity in _INTERNAL_CHECK_INVOCATIONS


def public_suite_names() -> tuple[str, ...]:
    """Return the immutable public suite names."""

    return PUBLIC_SUITE_NAMES


def derive_execution_context(environ: Mapping[str, str]) -> ExecutionContext:
    """Derive a closed execution context without extending the public CLI."""

    github_actions = environ.get("GITHUB_ACTIONS", "")
    github_event_name = environ.get("GITHUB_EVENT_NAME", "")
    controller_event_name = environ.get("EVENT_NAME", "")
    if not github_actions and not github_event_name and not controller_event_name:
        return ExecutionContext.LOCAL
    if (
        github_actions != "true"
        or github_event_name not in {"pull_request", "push", "workflow_dispatch"}
        or (controller_event_name and controller_event_name != github_event_name)
    ):
        raise GateContractError(
            "ci-gate-execution-context",
            "environment",
            "GitHub execution requires an unmodified registered event",
        )
    event_name = github_event_name
    if event_name == "push":
        before = environ.get("PUSH_BEFORE_SHA", "")
        if not _FULL_SHA.fullmatch(before):
            raise GateContractError(
                "ci-gate-execution-context",
                "push",
                "push execution requires PUSH_BEFORE_SHA",
            )
        if before == "0" * 40:
            return ExecutionContext.PUSH_INITIAL
    if event_name == "workflow_dispatch" and environ.get("PUSH_BEFORE_SHA", ""):
        raise GateContractError(
            "ci-gate-execution-context",
            "workflow_dispatch",
            "workflow dispatch must not invent a comparison base",
        )
    return ExecutionContext(event_name)


def _authenticated_execution_environment(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> dict[str, str]:
    """Bind hosted PR inputs to GitHub's merge SHA and raw commit parents."""

    authenticated = dict(environ)
    context = derive_execution_context(authenticated)
    if context is not ExecutionContext.PULL_REQUEST:
        return authenticated

    merge_sha = authenticated.get("GITHUB_SHA", "")
    trusted_values = {
        "event": authenticated.get("TRUSTED_EVENT_NAME", ""),
        "merge": authenticated.get("TRUSTED_MERGE_SHA", ""),
        "base": authenticated.get("TRUSTED_BASE_SHA", ""),
        "head": authenticated.get("TRUSTED_HEAD_SHA", ""),
    }
    if (
        not _FULL_SHA.fullmatch(merge_sha)
        or merge_sha == "0" * 40
        or trusted_values["event"] != "pull_request"
        or trusted_values["merge"] != merge_sha
    ):
        raise GateContractError(
            "ci-gate-execution-context",
            "pull_request",
            "pull-request execution requires the pre-install GitHub merge identity",
        )

    git_environment = {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }
    git_executable = _trusted_git_executable(authenticated)
    try:
        resolved = subprocess.run(
            (git_executable, "rev-parse", "--verify", "HEAD^{commit}"),
            cwd=root,
            env=git_environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=_GIT_TIMEOUT_SECONDS,
            check=False,
        )
        commit = subprocess.run(
            (git_executable, "cat-file", "commit", merge_sha),
            cwd=root,
            env=git_environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=_GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise GateContractError(
            "ci-gate-execution-context",
            "pull_request",
            "pull-request merge topology could not be authenticated",
        ) from None
    resolved_sha = resolved.stdout.decode("ascii", errors="replace").strip()
    if resolved.returncode != 0 or resolved_sha != merge_sha or commit.returncode != 0:
        raise GateContractError(
            "ci-gate-execution-context",
            "pull_request",
            "the checkout does not match the GitHub merge identity",
        )
    try:
        header = commit.stdout.split(b"\n\n", 1)[0]
        parents = tuple(
            line.removeprefix(b"parent ").decode("ascii", errors="strict")
            for line in header.splitlines()
            if line.startswith(b"parent ")
        )
    except UnicodeDecodeError:
        parents = ()
    if (
        len(parents) != 2
        or any(not _FULL_SHA.fullmatch(parent) for parent in parents)
        or trusted_values["base"] != parents[0]
        or trusted_values["head"] != parents[1]
    ):
        raise GateContractError(
            "ci-gate-execution-context",
            "pull_request",
            "the checkout is not the pre-install pull-request merge topology",
        )
    for key, expected in (
        ("PR_BASE_SHA", parents[0]),
        ("PR_HEAD_SHA", parents[1]),
    ):
        supplied = authenticated.get(key, "")
        if supplied and supplied != expected:
            raise GateContractError(
                "ci-gate-execution-context",
                "pull_request",
                "mutable pull-request identity does not match the merge topology",
            )
        authenticated[key] = expected
    authenticated["EVENT_NAME"] = "pull_request"
    return authenticated


@dataclasses.dataclass(slots=True)
class _VerifiedInvocation:
    invocation: GateInvocation
    entrypoint_fd: int
    cwd_fd: int
    interpreter: str
    tracked_object: str = ""
    source_sha256: str = ""
    source_size: int = 0


@dataclasses.dataclass(slots=True)
class _ProcessLifecycle:
    process: subprocess.Popen[bytes] | None = None
    pidfd: int | None = None
    group_finalized: bool = False
    recovery_kill_completed: bool = False
    recovery_readiness_completed: bool = False
    recovery_leader_ready: bool = False
    reap_started: bool = False
    reap_completed: bool = False
    returncode: int | None = None
    pidfd_close_attempted: bool = False
    cleanup_failed: bool = False

    @property
    def pidfd_acquired(self) -> bool:
        return self.pidfd is not None

    def start_process(
        self,
        argv: list[str],
        *,
        cwd: str,
        environment: Mapping[str, str],
        pass_fds: tuple[int, ...],
    ) -> None:
        self.process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=dict(environment),
            pass_fds=pass_fds,
            shell=False,
            start_new_session=True,
        )

    def bound_process(self) -> subprocess.Popen[bytes]:
        if self.process is None:
            raise _runner_cleanup_error()
        return self.process

    def acquire_pidfd(self) -> None:
        if self.process is None:
            raise _runner_cleanup_error()
        self.pidfd = os.pidfd_open(self.process.pid)

    def mark_group_finalized(self) -> None:
        self.group_finalized = True

    def mark_recovery_kill_completed(self) -> None:
        self.recovery_kill_completed = True

    def mark_recovery_readiness_completed(
        self,
        leader_ready: bool,
    ) -> None:
        self.recovery_readiness_completed = True
        self.recovery_leader_ready = leader_ready

    def mark_reap_started(self) -> None:
        self.reap_started = True

    def mark_reap_completed(self, returncode: int) -> None:
        self.reap_completed = True
        self.returncode = returncode

    def mark_pidfd_close_attempted(self) -> None:
        self.pidfd_close_attempted = True

    def mark_cleanup_failed(self) -> None:
        self.cleanup_failed = True


class _GateArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise GateContractError(
            "ci-gate-cli-arguments",
            "arguments",
            "the runner arguments do not match the closed grammar",
        )


def build_public_execution_plan(
    registry: GateRegistry,
    root_gate_ids: tuple[str, ...],
) -> tuple[GateInvocation, ...]:
    """Expand contract-owned public roots and execute each gate node once."""

    node_by_id = {node.gate_id: node for node in registry.nodes}
    if len(node_by_id) != len(registry.nodes):
        raise GateContractError(
            "ci-gate-id-duplicate",
            "gate_nodes",
            "gate identifiers must be unique",
        )
    invocations: list[GateInvocation] = []
    for gate_id in expand_public_gate_ids(registry, root_gate_ids):
        node = node_by_id[gate_id]
        if node.entrypoint is None or node.cwd is None or node.timeout_minutes is None:
            raise GateContractError(
                "ci-gate-execution-node",
                gate_id,
                "the selected executable gate is incomplete",
            )
        invocations.append(
            GateInvocation(
                gate_id=node.gate_id,
                entrypoint=node.entrypoint,
                argv=node.argv,
                cwd=node.cwd,
                allowed_env_keys=node.allowed_env_keys,
                timeout_seconds=node.timeout_minutes * 60,
            )
        )
    return tuple(invocations)


def build_public_validation_plan(
    registry: GateRegistry,
    root_gate_ids: tuple[str, ...],
    public_contract: PublicGateContract,
    selected_suites: tuple[str, ...],
    context: ExecutionContext,
    *,
    profile: str = "changed",
    root: pathlib.Path | None = None,
) -> tuple[GateInvocation, ...]:
    """Join public suite ownership to one canonical invocation per validator."""

    selected = set(selected_suites)
    if len(selected) != len(selected_suites) or not selected.issubset(
        public_contract.suite_names
    ):
        raise GateContractError(
            "ci-gate-public-suites",
            "suites",
            "selected public suites must be unique and registered",
        )
    base_plan = _filter_execution_context(
        build_public_execution_plan(registry, root_gate_ids),
        context,
        public_contract.local_only_gate_ids,
    )
    manifest_context = (
        "push" if context is ExecutionContext.PUSH_INITIAL else context.value
    )
    selected_ownership = tuple(
        item
        for item in public_contract.validators
        if item.suite in selected and manifest_context in item.contexts
    )
    selected_gate_ids = {item.gate_id for item in selected_ownership}
    templates: dict[str, GateInvocation] = {}
    for invocation in base_plan:
        if invocation.gate_id in selected_gate_ids:
            templates.setdefault(invocation.gate_id, invocation)

    def canonical_invocation(
        item: PublicValidatorRoute,
    ) -> GateInvocation:
        template = templates.get(item.gate_id)
        return GateInvocation(
            gate_id=item.gate_id,
            entrypoint=item.entrypoint,
            argv=_context_validator_argv(item, context, profile),
            cwd=(template.cwd if template is not None else pathlib.PurePosixPath(".")),
            allowed_env_keys=(
                ("TEMPLATE_GATE_BASE",)
                if item.entrypoint.name
                in {"check-document-metadata.py", "check-document-corpus-lifecycle.py"}
                and context in {ExecutionContext.PULL_REQUEST, ExecutionContext.PUSH}
                else ()
                if item.entrypoint.name
                in {"check-document-metadata.py", "check-document-corpus-lifecycle.py"}
                else template.allowed_env_keys
                if template is not None
                else ()
            ),
            timeout_seconds=(template.timeout_seconds if template is not None else 300),
        )

    canonical = {
        item.gate_id: canonical_invocation(item) for item in selected_ownership
    }
    plan: list[GateInvocation] = []
    emitted: set[str] = set()
    standalone_validator_gate_ids = {
        item.gate_id for item in public_contract.validators
    }
    for invocation in base_plan:
        gate_id = invocation.gate_id
        if gate_id in standalone_validator_gate_ids:
            if gate_id in canonical and gate_id not in emitted:
                plan.append(canonical[gate_id])
                emitted.add(gate_id)
            continue
        plan.append(invocation)
    for item in selected_ownership:
        if item.gate_id not in emitted:
            plan.append(canonical[item.gate_id])
            emitted.add(item.gate_id)
    result = tuple(plan)
    if context in {
        ExecutionContext.LOCAL,
        ExecutionContext.PUSH_INITIAL,
        ExecutionContext.WORKFLOW_DISPATCH,
    }:
        result = tuple(
            invocation
            for invocation in result
            if invocation.gate_id != "leaf.repo-metadata-base"
        )
    validate_public_execution_parity(
        public_contract, selected_suites, result, context, profile=profile
    )
    invocation_root = (
        pathlib.Path(__file__).resolve().parents[2] if root is None else root
    )
    seen_keys: dict[tuple[pathlib.Path, tuple[str, ...], str, str], str] = {}
    for invocation in result:
        key = canonical_invocation_key(
            invocation_root,
            invocation,
            profile=profile,
            context=context,
        )
        previous = seen_keys.get(key)
        if previous is not None:
            raise GateContractError(
                "ci-gate-invocation-duplicate",
                invocation.gate_id,
                f"canonical invocation duplicates {previous}",
            )
        seen_keys[key] = invocation.gate_id
    return result


def build_local_only_validation_plan(
    plan: tuple[GateInvocation, ...],
    public_contract: PublicGateContract,
    context: ExecutionContext,
) -> tuple[GateInvocation, ...]:
    """Select typed local-only leaves from an already selected public plan."""

    if context is not ExecutionContext.LOCAL:
        raise GateContractError(
            "ci-gate-local-only-context",
            "local-only",
            "local-only gates require the unauthenticated local execution context",
        )
    local_only_gate_ids = set(public_contract.local_only_gate_ids)
    return tuple(
        invocation for invocation in plan if invocation.gate_id in local_only_gate_ids
    )


def canonical_invocation_key(
    root: pathlib.Path,
    invocation: GateInvocation,
    *,
    profile: str,
    context: ExecutionContext,
) -> tuple[pathlib.Path, tuple[str, ...], str, str]:
    """Return the execution identity shared by every public gate context."""

    resolved = (root / invocation.entrypoint).resolve(strict=True)
    return resolved, tuple(invocation.argv), profile, context.value


def selected_prerequisites(
    plan: tuple[GateInvocation, ...],
    changed_paths: tuple[str, ...],
) -> SelectedPrerequisites:
    """Return bounded hosted prerequisites derived from the selected plan."""

    gate_ids = {invocation.gate_id for invocation in plan}
    node = bool(
        {
            "setup.frontend-node-dependencies",
            "setup.storybook-playwright",
            "leaf.frontend-build",
            "leaf.frontend-lint",
            "leaf.frontend-quality",
            "leaf.frontend-typecheck",
            "leaf.storybook-coverage",
            "setup.opsflow-smtp-node-dependencies",
            "leaf.opsflow-smtp-node-coverage",
            "leaf.opsflow-smtp-npm-audit",
            "leaf.opsflow-smtp-npm-production-audit",
            "leaf.opsflow-smtp-package",
            "leaf.compose-baseline-regressions",
            "leaf.repository-integrity-regressions",
        }
        & gate_ids
    )
    docker = bool(
        {
            "leaf.compose-validation",
            "leaf.conftest-policy",
            "leaf.conftest-policy-tests",
        }
        & gate_ids
    ) or any(
        pathlib.PurePosixPath(path).name == "Dockerfile"
        or pathlib.PurePosixPath(path).name.startswith("Dockerfile.")
        for path in changed_paths
    )
    return SelectedPrerequisites(node=node, docker=docker)


def _context_validator_argv(
    item: PublicValidatorRoute,
    context: ExecutionContext,
    profile: str,
) -> tuple[str, ...]:
    if profile not in {"changed", "full"}:
        raise GateContractError(
            "ci-gate-profile-unknown", "profile", "unknown public profile"
        )
    if item.entrypoint.name == "check-document-metadata.py":
        if profile == "full":
            return ("--mode", "check-contracts", "--history-scope", "full")
        if context in {
            ExecutionContext.LOCAL,
            ExecutionContext.PUSH_INITIAL,
            ExecutionContext.WORKFLOW_DISPATCH,
        }:
            return ("--mode", "check-active")
    return item.argv


def validate_public_execution_parity(
    public_contract: PublicGateContract,
    selected_suites: tuple[str, ...],
    plan: tuple[GateInvocation, ...],
    context: ExecutionContext,
    *,
    profile: str = "changed",
) -> None:
    """Fail unless selected validators occur exactly once and others not at all."""

    selected = set(selected_suites)
    ownership_gate_ids = tuple(item.gate_id for item in public_contract.validators)
    for item in public_contract.validators:
        validate_public_execution_argv(item.entrypoint, item.argv)
    if (
        len(selected) != len(selected_suites)
        or not selected.issubset(public_contract.suite_names)
        or len(ownership_gate_ids) != len(set(ownership_gate_ids))
    ):
        raise GateContractError(
            "ci-gate-public-execution-parity",
            "public_gate",
            "validator ownership and selected suites must be unique and registered",
        )
    manifest_context = (
        "push" if context is ExecutionContext.PUSH_INITIAL else context.value
    )
    expected = {
        item.gate_id: item
        for item in public_contract.validators
        if item.suite in selected and manifest_context in item.contexts
    }
    counts: collections.Counter[str] = collections.Counter()
    for invocation in plan:
        if _is_admitted_internal_invocation(
            invocation, context, public_contract.hosted_unit_bindings
        ):
            continue
        if invocation.gate_id not in expected:
            raise GateContractError(
                "ci-gate-public-execution-parity",
                invocation.gate_id,
                "every invocation requires selected validator or exact internal admission",
            )
        ownership = expected[invocation.gate_id]
        expected_argv = _context_validator_argv(ownership, context, profile)
        if (
            invocation.entrypoint != ownership.entrypoint
            or invocation.argv != expected_argv
        ):
            raise GateContractError(
                "ci-gate-public-execution-parity",
                invocation.gate_id,
                "validator arguments must match their canonical context invocation",
            )
        counts[invocation.gate_id] += 1
    if any(counts[gate_id] != 1 for gate_id in expected):
        raise GateContractError(
            "ci-gate-public-execution-parity",
            "public_gate",
            "selected manifest validators must have exactly one executable invocation",
        )


def render_public_validation_plan(
    plan: tuple[GateInvocation, ...],
    public_contract: PublicGateContract,
    selected_suites: tuple[str, ...],
    context: ExecutionContext,
    *,
    profile: str = "changed",
) -> tuple[str, ...]:
    """Explain the validator rows proven by the executable plan itself."""

    validate_public_execution_parity(
        public_contract, selected_suites, plan, context, profile=profile
    )
    manifest_context = (
        "push" if context is ExecutionContext.PUSH_INITIAL else context.value
    )
    suite_by_gate_id = {
        item.gate_id: item.suite
        for item in public_contract.validators
        if item.suite in selected_suites and manifest_context in item.contexts
    }
    return tuple(
        "{}\t{}\t{}\t{}".format(
            suite_by_gate_id[item.gate_id],
            item.entrypoint.as_posix(),
            item.gate_id,
            json.dumps(list(item.argv), separators=(",", ":")),
        )
        for item in plan
        if item.gate_id in suite_by_gate_id
    )


def _filter_execution_context(
    plan: tuple[GateInvocation, ...],
    context: ExecutionContext,
    local_only_gate_ids: tuple[str, ...],
) -> tuple[GateInvocation, ...]:
    if context is ExecutionContext.LOCAL:
        return tuple(
            invocation
            for invocation in plan
            if invocation.gate_id not in _LOCAL_EXCLUDED_GATE_IDS
            and not invocation.gate_id.startswith("setup.")
        )
    excluded = set(local_only_gate_ids)
    if context is not ExecutionContext.PULL_REQUEST:
        excluded.update(_PR_ONLY_GATE_IDS)
        excluded.update(HOSTED_UNIT_GATE_IDS)
    return tuple(
        invocation for invocation in plan if invocation.gate_id not in excluded
    )


def _evidence_error(error: EvidenceError) -> GateContractError:
    return GateContractError(
        "ci-gate-evidence-invalid",
        "execution-evidence",
        str(error),
    )


def _git_path_for_verification(environ: Mapping[str, str], path_value: str) -> str:
    if environ.get("GITHUB_ACTIONS") != "true":
        return path_value
    trusted_git = pathlib.Path(_trusted_git_executable(environ))
    return os.pathsep.join((str(trusted_git.parent), os.defpath))


def _evidence_rows(
    verified: tuple[_VerifiedInvocation, ...],
    request: ExecutionEvidenceRequest,
) -> tuple[dict[str, object], ...]:
    gate_ids = {item.invocation.gate_id for item in verified}
    if set(request.selection_reasons) != gate_ids:
        raise GateContractError(
            "ci-gate-evidence-selection",
            "execution-evidence",
            "evidence selection reasons must match the executable plan exactly",
        )
    return tuple(
        {
            "gate_id": item.invocation.gate_id,
            "argv": [
                item.invocation.entrypoint.as_posix(),
                *item.invocation.argv,
            ],
            "selection_reason": request.selection_reasons[item.invocation.gate_id],
            "environment_keys": sorted(item.invocation.allowed_env_keys),
            "source": {
                "path": item.invocation.entrypoint.as_posix(),
                "sha256": item.source_sha256,
                "git_object": item.tracked_object,
                "size_bytes": item.source_size,
            },
            "tool_image_digest": "NOT_AVAILABLE",
        }
        for item in verified
    )


def _verified_plan(
    root: pathlib.Path,
    plan: tuple[GateInvocation, ...],
    environ: Mapping[str, str],
) -> tuple[int, list[_VerifiedInvocation]]:
    path_value = environ.get("PATH", "")
    if not path_value:
        raise GateContractError(
            "ci-gate-environment",
            "PATH",
            "the controller PATH must be nonempty",
        )
    root_fd = _open_root(_canonical_root(root))
    verified: list[_VerifiedInvocation] = []
    try:
        git_path = _git_path_for_verification(environ, path_value)
        for invocation in plan:
            verified.append(_verify_invocation(root_fd, invocation, git_path))
    except BaseException:
        for item in verified:
            _close(item.entrypoint_fd)
            _close(item.cwd_fd)
        _close(root_fd)
        raise
    return root_fd, verified


def seed_execution_evidence(
    root: pathlib.Path,
    plan: tuple[GateInvocation, ...],
    environ: Mapping[str, str],
    request: ExecutionEvidenceRequest,
) -> str:
    root_fd, verified = _verified_plan(root, plan, environ)
    try:
        rows = _evidence_rows(tuple(verified), request)
        try:
            with EvidenceStore.create(
                request.directory,
                identity=request.identity,
                rows=rows,
                retention_days=request.retention_days,
                toolchain=request.toolchain,
            ) as store:
                return store.plan_sha256
        except EvidenceError as error:
            raise _evidence_error(error) from error
    finally:
        for item in verified:
            _close(item.entrypoint_fd)
            _close(item.cwd_fd)
        _close(root_fd)


def _selection_reasons(
    registry: GateRegistry,
    public_contract: PublicGateContract,
    selected_suites: tuple[str, ...],
    root_gate_ids: tuple[str, ...],
    plan: tuple[GateInvocation, ...],
) -> dict[str, str]:
    suite_by_gate = {
        route.gate_id: route.suite
        for route in public_contract.validators
        if route.suite in selected_suites
    }
    expanded_by_root = {
        root_gate_id: set(expand_public_gate_ids(registry, (root_gate_id,)))
        for root_gate_id in root_gate_ids
    }
    reasons: dict[str, str] = {}
    for invocation in plan:
        suite = suite_by_gate.get(invocation.gate_id)
        if suite is not None:
            reasons[invocation.gate_id] = f"suite:{suite}"
            continue
        owner = next(
            (
                root_gate_id
                for root_gate_id in root_gate_ids
                if invocation.gate_id in expanded_by_root[root_gate_id]
            ),
            None,
        )
        if owner is None:
            raise GateContractError(
                "ci-gate-evidence-selection",
                invocation.gate_id,
                "the executable gate has no selected root or suite owner",
            )
        reasons[invocation.gate_id] = (
            f"root:{owner}" if invocation.gate_id == owner else f"dependency:{owner}"
        )
    return reasons


def _execution_evidence_request(
    environ: Mapping[str, str],
    *,
    root: pathlib.Path,
    profile: str,
    context: ExecutionContext,
    selection_reasons: Mapping[str, str],
    node_selected: bool,
    observe_runtime: bool,
) -> ExecutionEvidenceRequest | None:
    directory = environ.get("CI_GATE_EVIDENCE_DIR", "")
    if not directory:
        return None
    if context not in {ExecutionContext.LOCAL, ExecutionContext.PULL_REQUEST}:
        raise GateContractError(
            "ci-gate-evidence-context",
            "execution-evidence",
            "runner evidence requires a local or authenticated pull-request context",
        )
    toolchain_environment = environ
    if context is ExecutionContext.LOCAL:
        head_sha = _local_clean_head(root)
        identity = {
            "event_name": "local",
            "profile": profile,
            "execution_context": context.value,
            "input_sha": head_sha,
            "base_sha": "NOT_AVAILABLE",
            "head_sha": head_sha,
            "run_id": str(time.time_ns()),
            "run_attempt": "1",
            "job": "local",
        }
        toolchain_environment = _local_toolchain_environment(
            environ, node_selected=node_selected
        )
    else:
        identity = {
            "event_name": environ.get("GITHUB_EVENT_NAME", ""),
            "profile": profile,
            "execution_context": context.value,
            "input_sha": environ.get("GITHUB_SHA", ""),
            "base_sha": environ.get("PR_BASE_SHA", ""),
            "head_sha": environ.get("PR_HEAD_SHA", ""),
            "run_id": environ.get("GITHUB_RUN_ID", ""),
            "run_attempt": environ.get("GITHUB_RUN_ATTEMPT", ""),
            "job": environ.get("GITHUB_JOB", ""),
        }
    return ExecutionEvidenceRequest(
        directory=pathlib.Path(directory),
        identity=identity,
        selection_reasons=dict(selection_reasons),
        retention_days=14,
        toolchain=_controller_toolchain(
            root, toolchain_environment, node_selected=node_selected
        ),
        runtime_observation=(
            _runtime_observation(toolchain_environment, node_selected=node_selected)
            if observe_runtime
            else None
        ),
    )


def _local_clean_head(root: pathlib.Path) -> str:
    git_path = _local_executable("git", os.defpath)
    git_environment = {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }
    try:
        head = subprocess.run(
            (git_path, "rev-parse", "--verify", "HEAD^{commit}"),
            cwd=root,
            env=git_environment,
            capture_output=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
        status = subprocess.run(
            (git_path, "status", "--porcelain=v1", "-z", "--untracked-files=no"),
            cwd=root,
            env=git_environment,
            capture_output=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GateContractError(
            "ci-gate-evidence-context",
            "local-head",
            "local evidence requires an available clean Git HEAD",
        ) from error
    value = head.stdout.decode("ascii", errors="replace").strip()
    if (
        head.returncode != 0
        or status.returncode != 0
        or status.stdout
        or _FULL_SHA.fullmatch(value) is None
    ):
        raise GateContractError(
            "ci-gate-evidence-context",
            "local-head",
            "local evidence requires an available clean Git HEAD",
        )
    return value


def _local_executable(name: str, path_value: str) -> str:
    value = shutil.which(name, path=path_value)
    if value is None:
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            name,
            "local evidence requires the allowlisted executable",
        )
    try:
        path = pathlib.Path(value).resolve(strict=True)
        metadata = path.stat()
    except OSError as error:
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            name,
            "local evidence requires the allowlisted executable",
        ) from error
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & (
        stat.S_IWGRP | stat.S_IWOTH
    ):
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            name,
            "local evidence executable is writable by another principal",
        )
    return str(path)


def _local_executable_identity(path: str, *version_argv: str) -> tuple[str, str]:
    try:
        payload = pathlib.Path(path).read_bytes()
        result = subprocess.run(
            (path, *version_argv),
            env={"LANG": "C", "LC_ALL": "C", "PATH": os.defpath},
            capture_output=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            pathlib.Path(path).name,
            "local executable identity is unavailable",
        ) from error
    version = (result.stdout + result.stderr).decode("utf-8", errors="replace").strip()
    if result.returncode != 0 or not version or len(version) > 128:
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            pathlib.Path(path).name,
            "local executable version is unavailable",
        )
    return version, hashlib.sha256(payload).hexdigest()


def _local_toolchain_environment(
    environ: Mapping[str, str], *, node_selected: bool
) -> dict[str, str]:
    path_value = environ.get("PATH", os.defpath)
    paths = {
        "git": _local_executable("git", os.defpath),
        "python": str(pathlib.Path(sys.executable).resolve(strict=True)),
        "uv": _local_executable("uv", path_value),
    }
    if node_selected:
        paths["node"] = _local_executable("node", path_value)
    captured: dict[str, str] = {
        "TRUSTED_IMAGE_OS": f"LOCAL-{os.uname().sysname}",
        "TRUSTED_IMAGE_VERSION": os.uname().release,
        "TRUSTED_RUNNER_ARCH": os.uname().machine,
    }
    for name, path in paths.items():
        version, digest = _local_executable_identity(path, "--version")
        prefix = f"TRUSTED_{name.upper()}"
        captured[f"{prefix}_PATH"] = path
        captured[f"{prefix}_VERSION"] = version
        captured[f"{prefix}_SHA256"] = digest
    return captured


def _controller_toolchain(
    root: pathlib.Path,
    environ: Mapping[str, str],
    *,
    node_selected: bool,
) -> dict[str, object]:
    try:
        return capture_controller_toolchain(root, environ, node_selected=node_selected)
    except EvidenceError as error:
        raise GateContractError(
            "ci-gate-evidence-toolchain",
            "controller-toolchain",
            str(error),
        ) from error


def _runtime_observation(
    environ: Mapping[str, str],
    *,
    node_selected: bool,
) -> dict[str, object]:
    try:
        return capture_runtime_observation(environ, node_selected=node_selected)
    except EvidenceError as error:
        raise GateContractError(
            "ci-gate-evidence-toolchain", "runtime-observation", str(error)
        ) from error


def execute_execution_plan(
    root: pathlib.Path,
    plan: tuple[GateInvocation, ...],
    environ: Mapping[str, str],
    executor: GateExecutor | None = None,
    *,
    evidence: ExecutionEvidenceRequest | None = None,
) -> int:
    canonical_root = _canonical_root(root)
    path_value = environ.get("PATH", "")
    if not path_value:
        raise GateContractError(
            "ci-gate-environment",
            "PATH",
            "the controller PATH must be nonempty",
        )
    home = pathlib.Path(tempfile.mkdtemp(prefix="ci-gate-home-", dir="/tmp"))
    try:
        if executor is not None:
            for invocation in plan:
                result = executor(invocation)
                if result != 0:
                    return result
            return 0
        if not pathlib.Path("/proc/self/fd").is_dir():
            raise GateContractError(
                "ci-gate-procfd-unavailable",
                "/proc/self/fd",
                "descriptor execution is unavailable",
            )
        root_fd, verified = _verified_plan(canonical_root, plan, environ)
        store: EvidenceStore | None = None
        try:
            descriptor_root = f"/proc/self/fd/{root_fd}"
            python_bootstrap = _create_python_bootstrap(
                home,
                descriptor_root,
            )
            if evidence is not None:
                rows = _evidence_rows(tuple(verified), evidence)
                try:
                    store = EvidenceStore.open(
                        evidence.directory,
                        identity=evidence.identity,
                        rows=rows,
                        retention_days=evidence.retention_days,
                        toolchain=evidence.toolchain,
                    )
                    store.initialize_result(
                        runtime_observation=evidence.runtime_observation
                    )
                except EvidenceError as error:
                    raise _evidence_error(error) from error
            for item in verified:
                child_environment = _child_environment(
                    root_fd,
                    home,
                    item.invocation,
                    item.interpreter,
                    environ,
                    python_bootstrap=python_bootstrap,
                )
                started_at = datetime.datetime.now(datetime.UTC)
                started_monotonic = time.monotonic()
                if store is not None:
                    try:
                        store.mark_started(
                            item.invocation.gate_id,
                            started_at_utc=_utc_timestamp(started_at),
                        )
                    except EvidenceError as error:
                        raise _evidence_error(error) from error
                try:
                    with _cancellation_handlers():
                        result = _run_verified_child(
                            root_fd,
                            item,
                            child_environment,
                        )
                except BaseException as error:
                    if store is not None:
                        ended_at = datetime.datetime.now(datetime.UTC)
                        try:
                            store.mark_terminal(
                                item.invocation.gate_id,
                                status="ERROR",
                                exit_code=1,
                                ended_at_utc=_utc_timestamp(ended_at),
                                duration_ms=max(
                                    0,
                                    round(
                                        (time.monotonic() - started_monotonic) * 1000
                                    ),
                                ),
                                reason=(
                                    "CANCELLED"
                                    if isinstance(
                                        error,
                                        (
                                            KeyboardInterrupt,
                                            SystemExit,
                                            _ExecutionCancelled,
                                        ),
                                    )
                                    else "CONTROLLER_ERROR"
                                ),
                            )
                            store.finalize(blocked_reason="blocked_by_prior")
                        except EvidenceError:
                            pass
                    if isinstance(error, _ExecutionCancelled):
                        return 128 + error.signum
                    raise
                if store is not None:
                    ended_at = datetime.datetime.now(datetime.UTC)
                    timed_out = bool(getattr(result, "timed_out", False))
                    status = "PASS" if result == 0 else "ERROR" if timed_out else "FAIL"
                    reason = (
                        None
                        if result == 0
                        else "TIMEOUT"
                        if timed_out
                        else "NONZERO_EXIT"
                    )
                    try:
                        store.mark_terminal(
                            item.invocation.gate_id,
                            status=status,
                            exit_code=int(result),
                            ended_at_utc=_utc_timestamp(ended_at),
                            duration_ms=max(
                                0,
                                round((time.monotonic() - started_monotonic) * 1000),
                            ),
                            reason=reason,
                        )
                    except EvidenceError as error:
                        if result != 0:
                            return int(result)
                        raise _evidence_error(error) from error
                if result != 0:
                    if store is not None:
                        try:
                            store.finalize(blocked_reason="blocked_by_prior")
                        except EvidenceError:
                            return int(result)
                    return int(result)
            if store is not None:
                try:
                    store.finalize(blocked_reason="blocked_by_prior")
                except EvidenceError as error:
                    raise _evidence_error(error) from error
            return 0
        finally:
            if store is not None:
                store.close()
            for item in verified:
                _close(item.entrypoint_fd)
                _close(item.cwd_fd)
            _close(root_fd)
    finally:
        _remove_home(home)


def _utc_timestamp(value: datetime.datetime) -> str:
    return (
        value.astimezone(datetime.UTC)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def main(argv: list[str] | None = None) -> int:
    parser = _GateArgumentParser(
        description="Execute registered repository CI gates",
        add_help=True,
        exit_on_error=False,
    )
    parser.add_argument("--profile", required=True)
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--requirements", action="store_true")
    parser.add_argument("--local-only", action="store_true")
    try:
        arguments = parser.parse_args(argv)
        root_value = os.environ.get("HYHOME_CI_GATE_ROOT")
        root = (
            pathlib.Path(root_value)
            if root_value
            else pathlib.Path(__file__).resolve().parents[2]
        )
        execution_environment = _authenticated_execution_environment(root, os.environ)
        context = derive_execution_context(execution_environment)
        document = load_contract_document(root)
        registry = parse_gate_registry(
            document,
            ".github/workflow-contract.yml",
        )
        findings = validate_gate_registry(root, registry)
        if findings:
            for finding in findings:
                print(
                    f"FAIL [{finding.code}] {finding.path}: {finding.message}",
                    file=sys.stderr,
                )
            return 1
        public_contract = parse_public_gate_contract(document)
        if arguments.local_only and context is not ExecutionContext.LOCAL:
            raise GateContractError(
                "ci-gate-local-only-context",
                "local-only",
                "local-only gates require the unauthenticated local execution context",
            )
        changed_paths = (
            ()
            if arguments.profile == "full"
            else collect_changed_paths(root, execution_environment)
        )
        selected_suites = select_public_suites(
            public_contract,
            arguments.profile,
            changed_paths,
        )
        selected_root_gate_ids = public_root_gate_ids(
            public_contract,
            selected_suites,
            changed_paths=(changed_paths if arguments.profile == "changed" else None),
        )
        plan = build_public_validation_plan(
            registry,
            selected_root_gate_ids,
            public_contract,
            selected_suites,
            context,
            profile=arguments.profile,
            root=root,
        )
        if arguments.local_only:
            plan = build_local_only_validation_plan(
                plan,
                public_contract,
                context,
            )
        if arguments.explain and arguments.requirements:
            raise argparse.ArgumentError(
                None,
                "--explain and --requirements are mutually exclusive",
            )
        if arguments.explain:
            lines = (
                tuple(
                    f"local-only\t{invocation.gate_id}\t{invocation.entrypoint}"
                    for invocation in plan
                )
                if arguments.local_only
                else render_public_validation_plan(
                    plan,
                    public_contract,
                    selected_suites,
                    context,
                    profile=arguments.profile,
                )
            )
            for line in lines:
                print(line)
            return 0
        if arguments.requirements:
            if context is not ExecutionContext.PULL_REQUEST:
                raise GateContractError(
                    "ci-gate-requirements-context",
                    "requirements",
                    "hosted prerequisites require a pull-request context",
                )
            prerequisites = selected_prerequisites(plan, changed_paths)
            evidence = _execution_evidence_request(
                execution_environment,
                root=root,
                profile=arguments.profile,
                context=context,
                selection_reasons=_selection_reasons(
                    registry,
                    public_contract,
                    selected_suites,
                    selected_root_gate_ids,
                    plan,
                ),
                node_selected=prerequisites.node,
                observe_runtime=False,
            )
            if evidence is not None:
                seed_execution_evidence(root, plan, execution_environment, evidence)
            print(f"node={'true' if prerequisites.node else 'false'}")
            print(f"docker={'true' if prerequisites.docker else 'false'}")
            return 0
        prerequisites = selected_prerequisites(plan, changed_paths)
        evidence = _execution_evidence_request(
            execution_environment,
            root=root,
            profile=arguments.profile,
            context=context,
            selection_reasons=_selection_reasons(
                registry,
                public_contract,
                selected_suites,
                selected_root_gate_ids,
                plan,
            ),
            node_selected=prerequisites.node,
            observe_runtime=True,
        )
        return execute_execution_plan(
            root,
            plan,
            execution_environment,
            evidence=evidence,
        )
    except (GateContractError, argparse.ArgumentError) as error:
        if isinstance(error, GateContractError):
            code = error.code
            path = error.path
            message = error.message
        else:
            code = "ci-gate-cli-arguments"
            path = "arguments"
            message = "the runner arguments do not match the closed grammar"
        print(f"FAIL [{code}] {path}: {message}", file=sys.stderr)
        return 2 if code == "ci-gate-cli-arguments" else 1


def _local_branch_commands(
    root: pathlib.Path,
    git_environment: Mapping[str, str],
    name_status: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    """Committed branch work since origin/main, as CI compares base...head.

    Without an origin/main ref the local plan keeps the working-tree view.
    """

    try:
        result = subprocess.run(
            ("git", "merge-base", "HEAD", "refs/remotes/origin/main"),
            cwd=root,
            env=git_environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=_GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ()
    base = result.stdout.decode("ascii", errors="replace").strip()
    if result.returncode != 0 or not _FULL_SHA.fullmatch(base):
        return ()
    return (("git", "diff", *name_status, base, "HEAD"),)


def collect_changed_paths(
    root: pathlib.Path,
    environ: Mapping[str, str],
) -> tuple[str, ...]:
    """Collect bounded changed paths for local, pull-request, and push callers."""

    git_environment = {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": (
            os.defpath
            if environ.get("GITHUB_ACTIONS") == "true"
            else environ.get("PATH", os.defpath)
        ),
    }
    event = environ.get("EVENT_NAME", "")
    git_executable = (
        _trusted_git_executable(environ)
        if environ.get("GITHUB_ACTIONS") == "true"
        else "git"
    )
    name_status = ("--name-status", "-z", "--find-renames")
    if event == "pull_request":
        base = environ.get("PR_BASE_SHA", "")
        head = environ.get("PR_HEAD_SHA", "")
        if (
            not _FULL_SHA.fullmatch(base)
            or base == "0" * 40
            or not _FULL_SHA.fullmatch(head)
            or head == "0" * 40
            or base == head
        ):
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "the pull-request comparison base is unavailable",
            )
        commands = ((git_executable, "diff", *name_status, f"{base}...{head}"),)
    elif event == "push":
        base = environ.get("PUSH_BEFORE_SHA", "")
        if not _FULL_SHA.fullmatch(base):
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "the push comparison base is unavailable",
            )
        commands = (
            ((git_executable, "ls-tree", "-r", "--name-only", "-z", "HEAD"),)
            if base == "0" * 40
            else ((git_executable, "diff", *name_status, base, "HEAD"),)
        )
    elif event:
        raise GateContractError(
            "ci-gate-changed-paths",
            "git",
            "the hosted comparison context is unavailable",
        )
    else:
        commands = (
            *_local_branch_commands(root, git_environment, name_status),
            ("git", "diff", *name_status),
            ("git", "diff", "--cached", *name_status),
            ("git", "ls-files", "--others", "--exclude-standard", "-z"),
        )
    paths: set[str] = set()
    total_bytes = 0
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=root,
                env=git_environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=_GIT_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "changed paths could not be collected",
            ) from None
        if result.returncode != 0:
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "changed paths could not be collected",
            )
        total_bytes += len(result.stdout)
        if total_bytes > _MAX_CHANGED_PATH_BYTES or (
            result.stdout and not result.stdout.endswith(b"\0")
        ):
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "changed path output exceeds its boundary",
            )
        fields = [item for item in result.stdout.split(b"\0") if item]
        values: list[str] = []
        try:
            if "--name-status" in command:
                index = 0
                while index < len(fields):
                    status = fields[index].decode("ascii", errors="strict")
                    index += 1
                    path_count = 2 if status.startswith(("C", "R")) else 1
                    if not re.fullmatch(r"(?:[ACDMT]|[CR][0-9]+)", status):
                        raise ValueError
                    if index + path_count > len(fields):
                        raise ValueError
                    values.extend(
                        item.decode("utf-8", errors="strict")
                        for item in fields[index : index + path_count]
                    )
                    index += path_count
            else:
                values.extend(item.decode("utf-8", errors="strict") for item in fields)
        except (UnicodeDecodeError, ValueError):
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "changed path output could not be parsed",
            ) from None
        paths.update(values)
        if len(paths) > _MAX_CHANGED_PATHS:
            raise GateContractError(
                "ci-gate-changed-paths",
                "git",
                "changed path count exceeds its boundary",
            )
    return tuple(sorted(paths))


def _canonical_root(root: pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(root)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root is unavailable",
        ) from None
    if (
        not candidate.is_absolute()
        or resolved != candidate
        or candidate.is_symlink()
        or not candidate.is_dir()
    ):
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root must be a canonical directory",
        )
    return candidate


def _open_root(root: pathlib.Path) -> int:
    try:
        return os.open(
            root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
        )
    except OSError as error:
        raise GateContractError(
            "ci-gate-root-invalid",
            ".",
            "the repository root could not be opened",
        ) from error


def _canonical_parts(
    path: pathlib.PurePosixPath,
    *,
    dot: bool,
    code: str,
) -> tuple[str, ...]:
    source = path.as_posix()
    if (
        path.is_absolute()
        or ".." in path.parts
        or source != str(path)
        or (source == "." and not dot)
        or (source != "." and any(part in {"", "."} for part in path.parts))
    ):
        raise GateContractError(
            code,
            source,
            "the repository-relative path is invalid",
        )
    return () if source == "." else path.parts


def _open_directory_at(
    root_fd: int,
    path: pathlib.PurePosixPath,
    *,
    code: str,
) -> int:
    parts = _canonical_parts(path, dot=True, code=code)
    current = os.dup(root_fd)
    try:
        for part in parts:
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
                dir_fd=current,
            )
            _close(current)
            current = next_fd
        return current
    except OSError as error:
        _close(current)
        raise GateContractError(
            code,
            path.as_posix(),
            "the verified directory is invalid",
        ) from error


def _open_entrypoint_at(
    root_fd: int,
    path: pathlib.PurePosixPath,
) -> int:
    parts = _canonical_parts(
        path,
        dot=False,
        code="ci-gate-entrypoint-invalid",
    )
    parent_fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
                dir_fd=parent_fd,
            )
            _close(parent_fd)
            parent_fd = next_fd
        try:
            entrypoint_fd = os.open(
                parts[-1],
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=parent_fd,
            )
        except OSError as error:
            code = (
                "ci-gate-entrypoint-symlink"
                if error.errno in {errno.ELOOP, errno.ENOTDIR}
                else "ci-gate-entrypoint-invalid"
            )
            raise GateContractError(
                code,
                path.as_posix(),
                "the entrypoint path is invalid",
            ) from error
        return entrypoint_fd
    except OSError as error:
        raise GateContractError(
            "ci-gate-entrypoint-symlink",
            path.as_posix(),
            "the entrypoint parent path is invalid",
        ) from error
    finally:
        _close(parent_fd)


def _verify_invocation(
    root_fd: int,
    invocation: GateInvocation,
    path_value: str,
) -> _VerifiedInvocation:
    cwd_fd = _open_directory_at(
        root_fd,
        invocation.cwd,
        code="ci-gate-cwd-invalid",
    )
    entrypoint_fd = -1
    try:
        entrypoint_fd = _open_entrypoint_at(root_fd, invocation.entrypoint)
        metadata = os.fstat(entrypoint_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise GateContractError(
                "ci-gate-entrypoint-not-regular",
                invocation.entrypoint.as_posix(),
                "the entrypoint must be a regular file",
            )
        first_line = os.pread(entrypoint_fd, 256, 0).split(b"\n", 1)[0]
        interpreter = _SHEBANGS.get(first_line)
        if interpreter is None:
            raise GateContractError(
                "ci-gate-entrypoint-shebang",
                invocation.entrypoint.as_posix(),
                "the entrypoint shebang is not admitted",
            )
        mode, object_id = _tracked_entrypoint(
            root_fd,
            invocation.entrypoint,
            path_value,
        )
        if mode is None:
            raise GateContractError(
                "ci-gate-entrypoint-untracked",
                invocation.entrypoint.as_posix(),
                "the entrypoint must be tracked",
            )
        if mode != "100755":
            raise GateContractError(
                "ci-gate-entrypoint-mode",
                invocation.entrypoint.as_posix(),
                "the tracked entrypoint mode must be executable",
            )
        if not _descriptor_matches_object(
            root_fd,
            entrypoint_fd,
            object_id,
            path_value,
        ):
            raise GateContractError(
                "ci-gate-entrypoint-identity",
                invocation.entrypoint.as_posix(),
                "the entrypoint identity differs from the tracked object",
            )
        source_sha256 = _descriptor_sha256(entrypoint_fd, metadata.st_size)
        return _VerifiedInvocation(
            invocation,
            entrypoint_fd,
            cwd_fd,
            interpreter,
            object_id,
            source_sha256,
            metadata.st_size,
        )
    except BaseException:
        if entrypoint_fd >= 0:
            _close(entrypoint_fd)
        _close(cwd_fd)
        raise


def _descriptor_sha256(descriptor: int, expected_size: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while offset < expected_size:
        chunk = os.pread(descriptor, min(65536, expected_size - offset), offset)
        if not chunk:
            raise GateContractError(
                "ci-gate-entrypoint-identity",
                "entrypoint",
                "the verified entrypoint changed while it was hashed",
            )
        digest.update(chunk)
        offset += len(chunk)
    metadata = os.fstat(descriptor)
    if metadata.st_size != expected_size or os.pread(descriptor, 1, expected_size):
        raise GateContractError(
            "ci-gate-entrypoint-identity",
            "entrypoint",
            "the verified entrypoint changed while it was hashed",
        )
    return digest.hexdigest()


def _git_environment(path_value: str) -> dict[str, str]:
    return {
        "PATH": path_value,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }


def _tracked_entrypoint(
    root_fd: int,
    path: pathlib.PurePosixPath,
    path_value: str,
) -> tuple[str | None, str]:
    try:
        result = subprocess.run(
            [
                "git",
                "--literal-pathspecs",
                "ls-files",
                "--stage",
                "-z",
                "--error-unmatch",
                "--",
                path.as_posix(),
            ],
            cwd=f"/proc/self/fd/{root_fd}",
            env=_git_environment(path_value),
            pass_fds=(root_fd,),
            capture_output=True,
            check=False,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise GateContractError(
            "ci-gate-entrypoint-provenance",
            path.as_posix(),
            "tracked entrypoint provenance is unavailable",
        ) from None
    if result.returncode != 0 or not result.stdout:
        return None, ""
    records = result.stdout.rstrip(b"\0").split(b"\0")
    if len(records) != 1:
        return None, ""
    try:
        metadata, recorded_path = records[0].split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split(" ")
        decoded_path = recorded_path.decode("utf-8", errors="strict")
    except (UnicodeDecodeError, ValueError):
        return None, ""
    if stage != "0" or decoded_path != path.as_posix():
        return None, ""
    return mode, object_id


def _descriptor_matches_object(
    root_fd: int,
    entrypoint_fd: int,
    expected_object_id: str,
    path_value: str,
) -> bool:
    duplicate = os.dup(entrypoint_fd)
    try:
        os.lseek(duplicate, 0, os.SEEK_SET)
        with os.fdopen(duplicate, "rb", closefd=True) as source:
            duplicate = -1
            result = subprocess.run(
                ["git", "hash-object", "--stdin"],
                cwd=f"/proc/self/fd/{root_fd}",
                env=_git_environment(path_value),
                stdin=source,
                pass_fds=(root_fd,),
                capture_output=True,
                check=False,
                timeout=_GIT_TIMEOUT_SECONDS,
            )
    except (OSError, subprocess.TimeoutExpired):
        return False
    finally:
        if duplicate >= 0:
            _close(duplicate)
    if result.returncode != 0:
        return False
    try:
        actual = result.stdout.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError:
        return False
    return actual == expected_object_id


def _child_environment(
    root: pathlib.Path | int,
    home: pathlib.Path,
    invocation: GateInvocation,
    interpreter: str,
    environ: Mapping[str, str],
    *,
    python_bootstrap: pathlib.Path | None = None,
) -> dict[str, str]:
    for key in invocation.allowed_env_keys:
        if _SECRET_ENV_SHAPE.search(key) or key not in _ADMITTED_ENV_KEYS:
            raise GateContractError(
                "ci-gate-environment",
                invocation.gate_id,
                "the gate environment key is not admitted",
            )
    root_value = f"/proc/self/fd/{root}" if isinstance(root, int) else str(root)
    admitted: dict[str, str] = {
        "PATH": environ["PATH"],
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": str(home),
        "TMPDIR": "/tmp",
        "PYTHONNOUSERSITE": "1",
        "PYTHONSAFEPATH": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "HYHOME_CI_GATE_ROOT": root_value,
    }
    if interpreter == "python":
        if python_bootstrap is None:
            raise GateContractError(
                "ci-gate-python-bootstrap",
                invocation.gate_id,
                "the isolated Python bootstrap is unavailable",
            )
        admitted["PYTHONPATH"] = str(python_bootstrap)
    for key in invocation.allowed_env_keys:
        if key == "TEMPLATE_GATE_BASE":
            base = _metadata_comparison_base(environ)
            if base is None:
                raise GateContractError(
                    "ci-gate-environment",
                    invocation.gate_id,
                    "the metadata comparison base is unavailable",
                )
            admitted[key] = base
        elif key in environ:
            admitted[key] = environ[key]
    return admitted


def _metadata_comparison_base(environ: Mapping[str, str]) -> str | None:
    event_name = environ.get("EVENT_NAME", "")
    if event_name == "pull_request":
        base = environ.get("PR_BASE_SHA", "")
        return base if _FULL_SHA.fullmatch(base) and base != "0" * 40 else None
    if event_name == "push":
        base = environ.get("PUSH_BEFORE_SHA", "")
        return base if _FULL_SHA.fullmatch(base) and base != "0" * 40 else None
    return None


def _create_python_bootstrap(
    home: pathlib.Path,
    _descriptor_root: str,
) -> pathlib.Path:
    directory = home / "python-bootstrap"
    try:
        directory.mkdir(mode=0o700)
        descriptor = os.open(
            directory / "sitecustomize.py",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
        )
        try:
            payload = (
                b"import os, sys\n"
                b"root = os.environ['HYHOME_CI_GATE_ROOT']\n"
                b"sys.path[:0] = [root, root + '/scripts/validation']\n"
            )
            _write_all(descriptor, payload)
            os.fsync(descriptor)
        finally:
            _close(descriptor)
    except OSError:
        raise GateContractError(
            "ci-gate-python-bootstrap",
            "python-bootstrap",
            "the isolated Python bootstrap could not be created",
        ) from None
    return directory


def _run_verified_child(
    root_fd: int,
    item: _VerifiedInvocation,
    environment: Mapping[str, str],
) -> _ChildOutcome:
    argv = [
        f"/proc/self/fd/{item.entrypoint_fd}",
        *item.invocation.argv,
    ]
    lifecycle = _ProcessLifecycle()
    product_error: BaseException | None = None
    timed_out = False
    cleanup_failed = False
    try:
        try:
            lifecycle.start_process(
                argv,
                cwd=f"/proc/self/fd/{item.cwd_fd}",
                environment=environment,
                pass_fds=tuple(
                    sorted(
                        {
                            root_fd,
                            item.cwd_fd,
                            item.entrypoint_fd,
                        }
                    )
                ),
            )
            lifecycle.acquire_pidfd()
            if lifecycle.pidfd is None:
                raise _runner_cleanup_error()
            leader_ready = _pidfd_ready(
                lifecycle.pidfd,
                item.invocation.timeout_seconds,
            )
            timed_out = not leader_ready
            _finalize_process_group(
                lifecycle,
                leader_ready=leader_ready,
            )
            lifecycle.mark_group_finalized()
        except BaseException as error:
            product_error = error
    finally:
        try:
            _finalize_process_lifecycle(lifecycle)
        except BaseException:
            if lifecycle.process is not None:
                lifecycle.mark_cleanup_failed()
        cleanup_failed = lifecycle.cleanup_failed
    result = _resolve_process_result(
        item.invocation.gate_id,
        lifecycle,
        product_error,
        cleanup_failed=cleanup_failed,
        timed_out=timed_out,
    )
    return _ChildOutcome(result, timed_out=timed_out)


def _finalize_process_group(
    lifecycle: _ProcessLifecycle,
    *,
    leader_ready: bool,
) -> None:
    process = lifecycle.bound_process()
    if lifecycle.pidfd is None:
        raise _runner_cleanup_error()
    pidfd = lifecycle.pidfd
    pgid = process.pid
    _signal_process_group(pgid, signal.SIGTERM)
    if not leader_ready:
        leader_ready = _pidfd_ready(
            pidfd,
            _TERMINATION_GRACE_SECONDS,
        )
    members = _same_pgid_members(pgid, process.pid) if leader_ready else ()
    if not leader_ready or members:
        _signal_process_group(pgid, signal.SIGKILL)
        if not leader_ready:
            leader_ready = _pidfd_ready(
                pidfd,
                _TERMINATION_GRACE_SECONDS,
            )
        if not leader_ready:
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader did not become ready",
            )
        if not _wait_for_nonleader_absence(pgid, process.pid):
            raise GateContractError(
                "ci-gate-runner-proc-members",
                "proc",
                "the adapter process group retained members",
            )


def _finalize_process_lifecycle(
    lifecycle: _ProcessLifecycle,
) -> None:
    try:
        try:
            if lifecycle.process is not None:
                if lifecycle.reap_started:
                    lifecycle.mark_cleanup_failed()
                elif not lifecycle.pidfd_acquired or not lifecycle.group_finalized:
                    _signal_process_group(
                        lifecycle.bound_process().pid,
                        signal.SIGKILL,
                    )
                    lifecycle.mark_recovery_kill_completed()
        except BaseException:
            if lifecycle.process is not None:
                lifecycle.mark_cleanup_failed()
    finally:
        try:
            try:
                if (
                    lifecycle.process is not None
                    and lifecycle.pidfd_acquired
                    and not lifecycle.group_finalized
                    and not lifecycle.reap_started
                ):
                    if lifecycle.pidfd is None:
                        raise _runner_cleanup_error()
                    leader_ready = _pidfd_ready(
                        lifecycle.pidfd,
                        _TERMINATION_GRACE_SECONDS,
                    )
                    lifecycle.mark_recovery_readiness_completed(leader_ready)
            except BaseException:
                if lifecycle.process is not None:
                    lifecycle.mark_cleanup_failed()
        finally:
            try:
                try:
                    if lifecycle.process is not None:
                        if lifecycle.reap_started:
                            if not lifecycle.reap_completed:
                                lifecycle.mark_cleanup_failed()
                        elif (
                            not lifecycle.pidfd_acquired
                            or lifecycle.group_finalized
                            or (
                                lifecycle.recovery_readiness_completed
                                and lifecycle.recovery_leader_ready
                            )
                        ):
                            _bounded_reap(lifecycle)
                        else:
                            lifecycle.mark_cleanup_failed()
                except BaseException:
                    if lifecycle.process is not None:
                        lifecycle.mark_cleanup_failed()
            finally:
                try:
                    if (
                        lifecycle.process is not None
                        and lifecycle.pidfd_acquired
                        and not lifecycle.pidfd_close_attempted
                    ):
                        _close_pidfd_once(lifecycle)
                except BaseException:
                    if lifecycle.process is not None:
                        lifecycle.mark_cleanup_failed()


def _resolve_process_result(
    gate_id: str,
    lifecycle: _ProcessLifecycle,
    product_error: BaseException | None,
    *,
    cleanup_failed: bool,
    timed_out: bool,
) -> int:
    if cleanup_failed:
        raise _runner_cleanup_error()
    if product_error is None:
        if not lifecycle.reap_completed or lifecycle.returncode is None:
            raise _runner_cleanup_error()
        return 124 if timed_out else lifecycle.returncode
    if lifecycle.process is None:
        if isinstance(product_error, Exception):
            raise GateContractError(
                "ci-gate-child-exec",
                gate_id,
                "the verified gate could not be executed",
            ) from None
        raise product_error
    if isinstance(product_error, GateContractError):
        raise product_error
    if not lifecycle.pidfd_acquired and isinstance(product_error, OSError):
        raise GateContractError(
            "ci-gate-runner-pidfd-acquisition",
            "pidfd",
            "the adapter leader identity could not be acquired",
        ) from None
    if isinstance(product_error, Exception):
        raise _runner_cleanup_error()
    raise product_error


def _bounded_reap(
    lifecycle: _ProcessLifecycle,
) -> int:
    if lifecycle.reap_started:
        raise _runner_cleanup_error()
    lifecycle.mark_reap_started()
    returncode = int(lifecycle.bound_process().wait(timeout=_TERMINATION_GRACE_SECONDS))
    lifecycle.mark_reap_completed(returncode)
    return returncode


def _close_pidfd_once(lifecycle: _ProcessLifecycle) -> None:
    if (
        not lifecycle.pidfd_acquired
        or lifecycle.pidfd is None
        or lifecycle.pidfd_close_attempted
    ):
        raise _runner_cleanup_error()
    lifecycle.mark_pidfd_close_attempted()
    os.close(lifecycle.pidfd)


def _signal_process_group(pgid: int, signum: int) -> None:
    try:
        os.killpg(pgid, signum)
    except OSError as error:
        if isinstance(error, ProcessLookupError) or error.errno == errno.ESRCH:
            return
        raise GateContractError(
            "ci-gate-runner-signal",
            "process-group",
            "the adapter process group could not be signaled",
        ) from None


def _pidfd_ready(pidfd: int, timeout_seconds: float) -> bool:
    deadline = time.monotonic() + max(0.0, timeout_seconds)
    poller = select.poll()
    try:
        poller.register(pidfd, select.POLLIN)
    except (OSError, ValueError):
        raise GateContractError(
            "ci-gate-runner-pidfd-readiness",
            "pidfd",
            "the adapter leader readiness could not be observed",
        ) from None
    while True:
        try:
            remaining = max(0.0, deadline - time.monotonic())
            timeout_ms = min(
                2_147_483_647,
                max(0, int(remaining * 1000)),
            )
            events = poller.poll(timeout_ms)
        except OSError as error:
            if error.errno == errno.EINTR and time.monotonic() < deadline:
                continue
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader readiness could not be observed",
            ) from None
        if events:
            for descriptor, event in events:
                if descriptor != pidfd or event & (select.POLLERR | select.POLLNVAL):
                    raise GateContractError(
                        "ci-gate-runner-pidfd-readiness",
                        "pidfd",
                        "the adapter leader readiness could not be observed",
                    )
                if event & select.POLLIN:
                    return True
            raise GateContractError(
                "ci-gate-runner-pidfd-readiness",
                "pidfd",
                "the adapter leader readiness could not be observed",
            )
        if time.monotonic() >= deadline:
            return False


def _wait_for_nonleader_absence(
    pgid: int,
    leader_pid: int,
) -> bool:
    deadline = time.monotonic() + _TERMINATION_GRACE_SECONDS
    while True:
        if not _same_pgid_members(pgid, leader_pid):
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.01)


def _same_pgid_members(
    pgid: int,
    leader_pid: int,
    *,
    proc_root: pathlib.Path = _PROC_ROOT,
) -> tuple[int, ...]:
    proc_fd = -1
    product_error: BaseException | None = None
    members: list[int] = []
    try:
        proc_fd = os.open(
            proc_root,
            os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
        )
        try:
            numeric_names: list[str] = []
            with os.scandir(proc_fd) as entries:
                for entry in entries:
                    name = entry.name
                    if (
                        not name
                        or not name.isascii()
                        or any(character < "0" or character > "9" for character in name)
                    ):
                        continue
                    numeric_names.append(name)
                    if len(numeric_names) > _MAX_PROC_PID_ENTRIES:
                        raise _proc_scan_error()
        except OSError:
            raise _proc_scan_error() from None
        numeric_entries: list[tuple[int, str]] = []
        for name in numeric_names:
            if len(name) > 20:
                raise _proc_scan_error()
            try:
                pid = int(name, 10)
            except ValueError:
                raise _proc_scan_error() from None
            numeric_entries.append((pid, name))
        numeric_entries.sort()
        for pid, name in numeric_entries:
            if pid == leader_pid:
                continue
            member_pgid = _read_proc_entry_pgid(proc_fd, name, pid)
            if member_pgid == pgid:
                members.append(pid)
    except GateContractError as error:
        product_error = error
    except OSError:
        product_error = _proc_scan_error()
    except BaseException as error:
        product_error = error
    finally:
        cleanup_failed = False
        if proc_fd >= 0:
            try:
                os.close(proc_fd)
            except BaseException:
                cleanup_failed = True
    if cleanup_failed:
        raise _runner_cleanup_error()
    if product_error is not None:
        raise product_error
    return tuple(members)


def _read_proc_entry_pgid(
    proc_fd: int,
    name: str,
    pid: int,
) -> int | None:
    pid_fd = -1
    stat_fd = -1
    vanished = False
    entry_error: GateContractError | None = None
    product_error: BaseException | None = None
    cleanup_failed = False
    pgrp: int | None = None
    try:
        try:
            pid_fd = os.open(
                name,
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_DIRECTORY,
                dir_fd=proc_fd,
            )
        except OSError as error:
            if error.errno in {errno.ENOENT, errno.ESRCH}:
                vanished = True
            else:
                entry_error = _proc_scan_error()
        if not vanished and entry_error is None:
            try:
                stat_fd = os.open(
                    "stat",
                    os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK,
                    dir_fd=pid_fd,
                )
            except OSError as error:
                if error.errno in {errno.ENOENT, errno.ESRCH}:
                    vanished = True
                else:
                    entry_error = _proc_scan_error()
        if not vanished and entry_error is None:
            try:
                payload = _read_proc_stat(stat_fd)
            except OSError as error:
                if error.errno in {errno.ENOENT, errno.ESRCH}:
                    vanished = True
                else:
                    entry_error = _proc_scan_error()
            else:
                try:
                    pgrp = _parse_proc_stat_pgid(payload, pid)
                except ValueError:
                    entry_error = _proc_scan_error()
    except BaseException as error:
        product_error = error
    finally:
        for descriptor in (stat_fd, pid_fd):
            if descriptor < 0:
                continue
            try:
                os.close(descriptor)
            except BaseException:
                cleanup_failed = True
    if cleanup_failed:
        raise _runner_cleanup_error()
    if product_error is not None:
        raise product_error
    if entry_error is not None:
        raise entry_error
    return None if vanished else pgrp


def _read_proc_stat(descriptor: int) -> bytes:
    payload = bytearray()
    while len(payload) <= _MAX_PROC_STAT_BYTES:
        chunk = os.read(
            descriptor,
            _MAX_PROC_STAT_BYTES + 1 - len(payload),
        )
        if not chunk:
            return bytes(payload)
        payload.extend(chunk)
        if len(payload) > _MAX_PROC_STAT_BYTES:
            raise OSError(errno.EFBIG, "proc stat too large")
    raise OSError(errno.EFBIG, "proc stat too large")


def _parse_proc_stat_pgid(payload: bytes, pid: int) -> int:
    if len(payload) > _MAX_PROC_STAT_BYTES or b"\0" in payload:
        raise ValueError
    line = payload[:-1] if payload.endswith(b"\n") else payload
    if not line or b"\n" in line:
        raise ValueError
    prefix = f"{pid} (".encode("ascii")
    if not line.startswith(prefix):
        raise ValueError
    comm_end = line.rfind(b") ")
    if comm_end < len(prefix):
        raise ValueError
    fields = line[comm_end + 2 :].split()
    if (
        len(fields) < 3
        or len(fields[0]) != 1
        or not fields[1].isdigit()
        or not fields[2].isdigit()
    ):
        raise ValueError
    return int(fields[2], 10)


def _proc_scan_error() -> GateContractError:
    return GateContractError(
        "ci-gate-runner-proc-scan",
        "proc",
        "the process-group membership scan failed",
    )


def _runner_cleanup_error() -> GateContractError:
    return GateContractError(
        "ci-gate-runner-cleanup",
        "process-group",
        "the adapter process group could not be cleaned up",
    )


def _remove_home(home: pathlib.Path) -> None:
    for attempt in range(3):
        try:
            shutil.rmtree(home)
            return
        except OSError:
            if attempt < 2:
                time.sleep(0.05)
    raise GateContractError(
        "ci-gate-home-cleanup",
        "HOME",
        "the isolated gate home could not be removed",
    ) from None


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError(errno.EIO, "short write")
        view = view[written:]


def _close(descriptor: int) -> None:
    if descriptor < 0:
        return
    try:
        os.close(descriptor)
    except OSError:
        pass
