#!/usr/bin/env python3
"""Validate the live public-gate surface without branch/SHA snapshots."""

from __future__ import annotations

import argparse
import collections
import pathlib
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Final

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.gate import ci_gate_contract  # noqa: E402
from scripts.validation import ci_gate_runner  # noqa: E402


PUBLIC_SUITES: Final = (
    "agent-governance",
    "document-contract",
    "document-graph",
    "document-lifecycle",
    "operations",
    "repository-integrity",
)
PUBLIC_PROFILES: Final = ("changed", "full")
RETIRED_PATHS: Final = (
    "scripts/hooks/patch-graphify-post-commit.sh",
    "scripts/knowledge/generate-llm-wiki-coverage.sh",
    "scripts/knowledge/generate-llm-wiki-index.sh",
    "scripts/validation/check-repo-contracts.sh",
    "scripts/validation/recommend-gap-routing.sh",
    "scripts/validation/recommend-qa-gates.sh",
)
TASK4_REMOVED_PATHS: Final = (
    "docs/00.agent-governance/providers/agents-md.md",
    "docs/00.agent-governance/contracts/agent-governance-artifacts.yaml",
)
PROFILE_SURFACES: Final = (
    ".github/workflows/ci-quality.yml",
    ".pre-commit-config.yaml",
    "scripts/validation/run-local-qa-gates.sh",
    "scripts/hooks/agent-event-hook.sh",
    "scripts/hooks/post-tool-validate.sh",
    ".claude/settings.json",
    ".codex/hooks.json",
)
RUNNER: Final = "python3 scripts/validation/run-ci-gate.py"
CHANGED_COMMAND: Final = f"{RUNNER} --profile changed"
FULL_COMMAND: Final = f"{RUNNER} --profile full"
MAX_SURFACE_BYTES: Final = 2 * 1_048_576
_PROFILE_ARGUMENT_RE: Final = re.compile(r"run-ci-gate\.py\s+--profile\s+([a-z-]+)")


@dataclass(frozen=True, order=True, slots=True)
class DeltaFinding:
    code: str
    path: str
    message: str


def _finding(code: str, path: str, message: str) -> DeltaFinding:
    return DeltaFinding(code, path, message)


def _read_surface(root: pathlib.Path, relative: str) -> str:
    path = root / relative
    try:
        metadata = path.lstat()
        if (
            not path.is_file()
            or path.is_symlink()
            or metadata.st_size > MAX_SURFACE_BYTES
        ):
            raise OSError
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def _tracked(root: pathlib.Path, relative: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def _load_models(
    root: pathlib.Path,
) -> tuple[
    ci_gate_contract.GateRegistry,
    ci_gate_contract.PublicGateContract,
]:
    document = ci_gate_contract.load_contract_document(root)
    gates = ci_gate_contract.parse_gate_registry(
        document,
        ".github/workflow-contract.yml",
    )
    gate_findings = ci_gate_contract.validate_gate_registry(root, gates)
    if gate_findings:
        first = gate_findings[0]
        raise ci_gate_contract.GateContractError(
            first.code,
            first.path,
            first.message,
        )
    public = ci_gate_contract.parse_public_gate_contract(document)
    return gates, public


def _suite_ownership_findings(
    root: pathlib.Path,
    gates: ci_gate_contract.GateRegistry,
    public: ci_gate_contract.PublicGateContract,
) -> list[DeltaFinding]:
    findings: list[DeltaFinding] = []
    if public.suite_names != PUBLIC_SUITES:
        findings.append(
            _finding(
                "public-suites-not-exact",
                ".github/workflow-contract.yml",
                "the public suite set and order must be the six canonical suites",
            )
        )
    if public.profile_names != PUBLIC_PROFILES:
        findings.append(
            _finding(
                "public-profiles-not-exact",
                ".github/workflow-contract.yml",
                "public profiles must be exactly changed and full",
            )
        )

    validator_paths = tuple(
        item.entrypoint.as_posix() for item in public.validators
    )
    duplicates = {
        path
        for path, count in collections.Counter(validator_paths).items()
        if count != 1
    }
    for path in sorted(duplicates):
        findings.append(
            _finding(
                "public-validator-duplicate",
                path,
                "an atomic validator must belong to exactly one public suite",
            )
        )
    for validator in public.validators:
        path = validator.entrypoint.as_posix()
        if not (root / path).is_file() or not _tracked(root, path):
            findings.append(
                _finding(
                    "public-validator-untracked",
                    path,
                    "an atomic validator must be a current tracked regular file",
                )
            )

    routed_gate_ids: list[str] = []
    for route in public.suites:
        if not route.root_gate_ids:
            findings.append(
                _finding(
                    "public-suite-empty",
                    route.name,
                    "a public suite must route at least one atomic gate",
                )
            )
            continue
        try:
            plan = ci_gate_runner.build_public_validation_plan(
                gates,
                route.root_gate_ids,
                public,
                (route.name,),
                ci_gate_runner.ExecutionContext.LOCAL,
            )
        except ci_gate_contract.GateContractError as error:
            findings.append(_finding(error.code, error.path, error.message))
            continue
        for invocation in plan:
            routed_gate_ids.append(invocation.gate_id)
            entrypoint = invocation.entrypoint.as_posix()
            if not (root / entrypoint).is_file() or not _tracked(root, entrypoint):
                findings.append(
                    _finding(
                        "public-route-untracked",
                        entrypoint,
                        "a public route must use a current tracked entrypoint",
                    )
                )
    for gate_id, count in sorted(collections.Counter(routed_gate_ids).items()):
        if count != 1:
            findings.append(
                _finding(
                    "public-route-duplicate",
                    gate_id,
                    "an executable gate must route through exactly one public suite",
                )
            )
    return findings


def _changed_impact_findings(
    public: ci_gate_contract.PublicGateContract,
) -> list[DeltaFinding]:
    findings: list[DeltaFinding] = []
    try:
        full = ci_gate_contract.select_public_suites(public, "full", ())
    except ci_gate_contract.GateContractError as error:
        return [_finding(error.code, error.path, error.message)]
    if full != PUBLIC_SUITES:
        findings.append(
            _finding(
                "public-full-incomplete",
                "public_gate/profiles/full",
                "the full profile must select all six public suites",
            )
        )
    for validator in public.validators:
        path = validator.entrypoint.as_posix()
        try:
            selected = ci_gate_contract.select_public_suites(public, "changed", (path,))
        except ci_gate_contract.GateContractError as error:
            findings.append(_finding(error.code, error.path, error.message))
            continue
        if validator.suite not in selected:
            findings.append(
                _finding(
                    "public-changed-impact-missing",
                    path,
                    "a validator change must select its owning public suite",
                )
            )
    return findings


def _workflow_findings(root: pathlib.Path) -> list[DeltaFinding]:
    relative = ".github/workflows/ci-quality.yml"
    source = _read_surface(root, relative)
    if not source:
        return [
            _finding("public-workflow-unreadable", relative, "workflow is unreadable")
        ]
    try:
        document = yaml.safe_load(source)
    except yaml.YAMLError:
        document = None
    jobs = document.get("jobs") if isinstance(document, dict) else None
    expected = {
        "validation-changed": CHANGED_COMMAND,
        "validation-full": FULL_COMMAND,
    }
    if not isinstance(jobs, dict) or tuple(jobs) != tuple(expected):
        return [
            _finding(
                "public-workflow-jobs",
                relative,
                "required quality jobs must be exactly changed and full",
            )
        ]
    findings: list[DeltaFinding] = []
    for job_id, command in expected.items():
        steps = jobs[job_id].get("steps") if isinstance(jobs[job_id], dict) else None
        runs = [
            step.get("run")
            for step in steps or ()
            if isinstance(step, dict) and "run" in step
        ]
        if runs != [ci_gate_contract.CI_DEPENDENCY_BOOTSTRAP, command]:
            findings.append(
                _finding(
                    "public-workflow-route",
                    f"{relative}#{job_id}",
                    "each required job must bootstrap declared dependencies then run only its public profile command",
                )
            )
    return findings


def _precommit_findings(root: pathlib.Path) -> list[DeltaFinding]:
    relative = ".pre-commit-config.yaml"
    source = _read_surface(root, relative)
    try:
        document = yaml.safe_load(source)
    except yaml.YAMLError:
        document = None
    repos = document.get("repos") if isinstance(document, dict) else None
    local = [
        item
        for item in repos or ()
        if isinstance(item, dict) and item.get("repo") == "local"
    ]
    hooks = local[0].get("hooks") if len(local) == 1 else None
    routes = {
        item.get("id"): (item.get("entry"), item.get("stages"))
        for item in hooks or ()
        if isinstance(item, dict)
    }
    expected = {
        "public-validation-changed": (CHANGED_COMMAND, ["pre-commit"]),
        "public-validation-full": (FULL_COMMAND, ["pre-push"]),
    }
    if routes != expected:
        return [
            _finding(
                "public-precommit-route",
                relative,
                "local pre-commit and pre-push hooks must select changed and full",
            )
        ]
    return []


def _surface_findings(
    root: pathlib.Path,
    gates: ci_gate_contract.GateRegistry,
) -> list[DeltaFinding]:
    findings: list[DeltaFinding] = []
    atomic_paths = {
        node.entrypoint.as_posix()
        for node in gates.nodes
        if node.entrypoint is not None
    } - {"scripts/validation/run-ci-gate.py"}
    for relative in PROFILE_SURFACES:
        source = _read_surface(root, relative)
        if not source:
            findings.append(
                _finding(
                    "public-surface-unreadable",
                    relative,
                    "profile surface is unreadable",
                )
            )
            continue
        copied = sorted(path for path in atomic_paths if path in source)
        if copied:
            findings.append(
                _finding(
                    "public-surface-copied-validator",
                    relative,
                    "workflow and hook surfaces must not copy atomic validator commands",
                )
            )
        profiles = tuple(_PROFILE_ARGUMENT_RE.findall(source))
        if any(profile not in PUBLIC_PROFILES for profile in profiles):
            findings.append(
                _finding(
                    "public-surface-profile-unknown",
                    relative,
                    "profile surfaces may select only changed or full",
                )
            )
        if (
            relative
            in {
                "scripts/validation/run-local-qa-gates.sh",
                "scripts/hooks/agent-event-hook.sh",
                "scripts/hooks/post-tool-validate.sh",
            }
            and RUNNER not in source
        ):
            findings.append(
                _finding(
                    "public-surface-route-missing",
                    relative,
                    "local and provider-neutral hooks must delegate to the public runner",
                )
            )
    return findings


def _retirement_findings(root: pathlib.Path) -> list[DeltaFinding]:
    findings: list[DeltaFinding] = []
    active_text = "\n".join(_read_surface(root, path) for path in PROFILE_SURFACES)
    for relative in RETIRED_PATHS:
        if (root / relative).exists():
            findings.append(
                _finding(
                    "retired-path-present",
                    relative,
                    "the successor-backed transition path must be absent",
                )
            )
        if (
            relative in active_text
            or pathlib.PurePosixPath(relative).name in active_text
        ):
            findings.append(
                _finding(
                    "retired-path-consumed",
                    relative,
                    "an active workflow or hook still consumes a retired path",
                )
            )
    for relative in TASK4_REMOVED_PATHS:
        if (root / relative).exists():
            findings.append(
                _finding(
                    "task4-removal-regressed",
                    relative,
                    "a Task 4 retired projection must remain absent",
                )
            )
    return findings


def _infra_link_findings(root: pathlib.Path) -> list[DeltaFinding]:
    findings: list[DeltaFinding] = []
    infra = root / "infra"
    if not infra.is_dir():
        return findings
    runner = "scripts/validation/run-ci-gate.py"
    command = "`python3 scripts/validation/run-ci-gate.py --profile changed`"
    for path in sorted(infra.rglob("*.md")):
        relative = path.relative_to(root).as_posix()
        source = _read_surface(root, relative)
        if "[run-ci-gate.py]" not in source:
            continue
        target = posixpath.relpath(runner, posixpath.dirname(relative))
        expected = f"[run-ci-gate.py]({target}) ({command})"
        for line_number, line in enumerate(source.splitlines(), start=1):
            if "[run-ci-gate.py]" in line and expected not in line:
                findings.append(
                    _finding(
                        "public-infra-runner-link",
                        f"{relative}:{line_number}",
                        "the current infra runner link and command must be exact",
                    )
                )
    return findings


def validate_repository(root: pathlib.Path) -> tuple[DeltaFinding, ...]:
    """Return deterministic findings for the live six-suite gate surface."""

    root = root.resolve()
    try:
        gates, public = _load_models(root)
    except ci_gate_contract.GateContractError as error:
        code = getattr(error, "code", "public-suite-registry")
        path = getattr(error, "path", "scripts/manifest.yaml")
        message = getattr(error, "message", "the public suite registry is invalid")
        return (_finding(code, path, message),)
    findings = [
        *_suite_ownership_findings(root, gates, public),
        *_changed_impact_findings(public),
        *_workflow_findings(root),
        *_precommit_findings(root),
        *_surface_findings(root, gates),
        *_infra_link_findings(root),
        *_retirement_findings(root),
    ]
    return tuple(sorted(set(findings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate live public suite routing and retirement invariants."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=("advisory", "blocking"), default="blocking")
    arguments = parser.parse_args(argv)
    findings = validate_repository(pathlib.Path(arguments.root))
    for finding in findings:
        print(
            f"FAIL [{finding.code}] {finding.path}: {finding.message}",
            file=sys.stderr,
        )
    if findings:
        return 1
    print("PASS: live public suite routing contract is satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
