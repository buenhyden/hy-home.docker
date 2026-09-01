#!/usr/bin/env python3
"""Validate the script inventory and optionally check maintained generators."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any, Iterable, Mapping, Sequence

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.lib.document_governance.suite_registry import (  # noqa: E402
    SuiteRegistryError,
    load_manifest_document,
    validate_execution_argv,
)


REQUIRED_FIELDS = frozenset(
    {
        "path",
        "kind",
        "authority",
        "lifecycle",
        "mutation",
        "consumers",
        "disposition",
        "successor",
        "tests",
    }
)
OPTIONAL_FIELDS = frozenset(
    {
        "check_command",
        "outputs",
        "public_suites",
        "execution_argv",
        "execution_contexts",
    }
)
KINDS = frozenset(
    {
        "contract",
        "dependency-manifest",
        "generator",
        "hook",
        "library",
        "operations",
        "runner",
        "validator",
    }
)
LIFECYCLES = frozenset({"active", "transition"})
MUTATIONS = frozenset({"none", "check-write", "runtime"})
DISPOSITIONS = frozenset({"retain", "merge", "delete", "rewrite"})
NON_EXECUTABLE_KINDS = frozenset({"contract", "dependency-manifest", "library"})
FORBIDDEN_EVIDENCE_PREFIXES = (
    "docs/04.execution/",
    "docs/90.references/data/0082-llm-wiki-index/",
    "docs/98.archive/",
    "graphify-out/",
)
SELF_PATH = "scripts/validation/check-script-manifest.py"
REQUIRED_LOCAL_PATHS = frozenset(
    {
        SELF_PATH,
        "scripts/knowledge/generate-llm-wiki.py",
        "tests/validation/test_generate_llm_wiki.py",
    }
)
APPROVED_TEST_PREFIXES = ("tests/lib/", "tests/validation/")
PUBLIC_SUITE_NAMES = frozenset(
    {
        "agent-governance",
        "document-contract",
        "document-graph",
        "document-lifecycle",
        "operations",
        "repository-integrity",
    }
)
RUNBOOK_AUTHORITY = __import__("re").compile(
    r"docs/05\.operations/catalog/[0-9]{2}-[^/]+/[0-9]{4}-[^/]+/runbook\.md"
)
MACHINE_AUTHORITIES = frozenset(
    {
        ".github/workflow-contract.yml",
        "docs/00.agent-governance/providers/registry.yaml",
        "scripts/manifest.yaml",
    }
)
MAX_OBSERVED_PATHS = 50_000
MAX_OBSERVED_BYTES = 512 * 1_048_576
@dataclass(frozen=True, order=True)
class Finding:
    code: str
    path: str
    message: str


def _finding(code: str, path: object, message: str) -> Finding:
    return Finding(code=code, path=str(path or "<manifest>"), message=message)


def _safe_repo_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and value == path.as_posix()


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def _generator_command_error(row: Mapping[str, Any]) -> str | None:
    command = row.get("check_command")
    if not _string_list(command):
        return "retained check-write generator requires a non-empty argv check_command"
    assert isinstance(command, list)
    path = str(row.get("path", ""))
    allowed = [["python3", path, "--check"], [path, "--check"]]
    if path.endswith(".sh"):
        allowed.append(["bash", path, "--check"])
    if command not in allowed:
        return (
            "generator check_command must be exact non-shell argv: "
            "an admitted interpreter, the registered path, and --check"
        )
    outputs = row.get("outputs")
    if not _string_list(outputs):
        return "retained check-write generator requires a non-empty outputs list"
    if len(outputs) != len(set(outputs)) or outputs != sorted(outputs):
        return "generator outputs must be unique and sorted"
    if any(not _safe_repo_path(output) for output in outputs):
        return "generator outputs must be safe repository-relative paths"
    return None


def validate_manifest_document(
    document: object, tracked_paths: Iterable[str]
) -> list[Finding]:
    """Return deterministic fail-closed findings for a parsed manifest."""

    tracked = set(tracked_paths)
    findings: list[Finding] = []
    if not isinstance(document, dict):
        return [_finding("document-invalid", "<manifest>", "document must be a mapping")]
    if document.get("schema_version") != 1:
        findings.append(_finding("schema-version-invalid", "<manifest>", "schema_version must equal 1"))
    if set(document) != {"schema_version", "files"}:
        findings.append(_finding("document-fields-invalid", "<manifest>", "top-level fields must be schema_version and files"))
    rows = document.get("files")
    if not isinstance(rows, list):
        findings.append(_finding("files-invalid", "<manifest>", "files must be a list"))
        return sorted(findings)

    declared: list[str] = []
    tracked_scripts = {path for path in tracked if path == "scripts" or path.startswith("scripts/")}
    for index, raw_row in enumerate(rows):
        if not isinstance(raw_row, dict):
            findings.append(_finding("row-invalid", f"files[{index}]", "row must be a mapping"))
            continue
        row: Mapping[str, Any] = raw_row
        path = row.get("path")
        label = path if isinstance(path, str) and path else f"files[{index}]"
        fields = set(row)
        missing = REQUIRED_FIELDS - fields
        unknown = fields - REQUIRED_FIELDS - OPTIONAL_FIELDS
        if missing:
            findings.append(_finding("fields-missing", label, f"missing fields: {sorted(missing)}"))
        if unknown:
            findings.append(_finding("fields-unknown", label, f"unknown fields: {sorted(unknown)}"))
        if not _safe_repo_path(path) or not str(path).startswith("scripts/"):
            findings.append(_finding("path-invalid", label, "path must be below scripts/"))
            continue
        path = str(path)
        declared.append(path)
        if path not in tracked:
            findings.append(_finding("path-untracked", path, "manifest path is not tracked in the current tree"))

        if row.get("kind") not in KINDS:
            findings.append(_finding("kind-invalid", path, f"invalid kind: {row.get('kind')!r}"))
        public_suites = row.get("public_suites")
        if row.get("kind") == "validator":
            if (
                not isinstance(public_suites, list)
                or len(public_suites) != 1
                or not isinstance(public_suites[0], str)
                or public_suites[0] not in PUBLIC_SUITE_NAMES
            ):
                findings.append(
                    _finding(
                        "public-suite-invalid",
                        path,
                        "every validator requires exactly one canonical public_suites value",
                    )
                )
            execution_argv = row.get("execution_argv", [])
            if not isinstance(execution_argv, list) or not all(
                isinstance(item, str) and item for item in execution_argv
            ):
                findings.append(
                    _finding(
                        "validator-execution-argv-invalid",
                        path,
                        "validator execution_argv must be a string list",
                    )
                )
            execution_contexts = row.get("execution_contexts")
            if isinstance(execution_argv, list) and all(isinstance(item, str) for item in execution_argv):
                try:
                    validate_execution_argv(PurePosixPath(path), tuple(execution_argv))
                except SuiteRegistryError as error:
                    findings.append(_finding("validator-execution-argv-invalid", path, str(error)))
            if (
                not isinstance(execution_contexts, list)
                or execution_contexts
                != [
                    context
                    for context in (
                        "local",
                        "pull_request",
                        "push",
                        "workflow_dispatch",
                    )
                    if context in execution_contexts
                ]
                or len(execution_contexts) != len(set(execution_contexts))
            ):
                findings.append(
                    _finding(
                        "validator-execution-contexts-invalid",
                        path,
                        "validator execution_contexts must be a canonical context list",
                    )
                )
        elif public_suites is not None:
            findings.append(
                _finding(
                    "public-suite-kind-invalid",
                    path,
                    "only validator rows may declare public_suites",
                )
            )
        else:
            if "execution_argv" in row or "execution_contexts" in row:
                findings.append(
                    _finding(
                        "validator-execution-kind-invalid",
                        path,
                        "only validator rows may declare execution fields",
                    )
                )
        authority = row.get("authority")
        if not _safe_repo_path(authority):
            findings.append(_finding("authority-invalid", path, "authority must be a non-empty repository path"))
        elif authority not in tracked:
            findings.append(_finding("authority-untracked", path, f"authority is not tracked: {authority}"))
        if row.get("lifecycle") not in LIFECYCLES:
            findings.append(_finding("lifecycle-invalid", path, f"invalid lifecycle: {row.get('lifecycle')!r}"))
        if row.get("mutation") not in MUTATIONS:
            findings.append(_finding("mutation-invalid", path, f"invalid mutation: {row.get('mutation')!r}"))
        disposition = row.get("disposition")
        if disposition not in DISPOSITIONS:
            findings.append(_finding("disposition-invalid", path, f"invalid disposition: {disposition!r}"))
        if row.get("mutation") == "runtime" and disposition == "retain":
            if not isinstance(authority, str) or RUNBOOK_AUTHORITY.fullmatch(authority) is None:
                findings.append(
                    _finding(
                        "runtime-authority-invalid",
                        path,
                        "retained runtime script requires a domain-first Operations Runbook authority",
                    )
                )

        for field, empty_code in (("consumers", "consumer-missing"), ("tests", "tests-missing")):
            values = row.get(field)
            if not _string_list(values):
                findings.append(_finding(f"{field}-invalid", path, f"{field} must be a list of paths"))
                continue
            assert isinstance(values, list)
            if values != sorted(set(values)):
                findings.append(_finding(f"{field}-unsorted", path, f"{field} must be unique and sorted"))
            is_library = row.get("kind") == "library"
            is_document_governance_library = isinstance(path, str) and path.startswith(
                "scripts/lib/document_governance/"
            ) and not path.endswith("/__init__.py")
            requires_evidence = (
                field == "tests"
                and row.get("kind") not in {"contract", "dependency-manifest"}
            ) or (field == "consumers" and not is_library)
            if disposition == "retain" and requires_evidence and not values:
                findings.append(_finding(empty_code, path, f"retained {row.get('kind')} requires {field}"))
            if disposition == "retain" and is_document_governance_library and field == "tests":
                if not any(value.startswith("tests/lib/document_governance/") for value in values):
                    findings.append(
                        _finding(
                            "tests-mirror-missing",
                            path,
                            "retained document-governance library requires a mirrored library test",
                        )
                    )
            for value in values:
                if value not in tracked:
                    findings.append(_finding(f"{field}-untracked", path, f"{field} path is not tracked: {value}"))
                if value.startswith(FORBIDDEN_EVIDENCE_PREFIXES):
                    findings.append(_finding(f"{field}-historical", path, f"{field} cannot use historical/generated evidence: {value}"))
                if field == "tests" and not (
                    value.startswith(APPROVED_TEST_PREFIXES)
                    and value.endswith((".py", ".sh"))
                ):
                    findings.append(
                        _finding(
                            "tests-location-invalid",
                            path,
                            f"test must be executable evidence below an approved test root: {value}",
                        )
                    )

        successor = row.get("successor")
        if disposition == "retain":
            if successor is not None:
                findings.append(_finding("successor-invalid", path, "retained rows require successor: null"))
        elif not _safe_repo_path(successor):
            findings.append(_finding("successor-missing", path, "non-retained rows require a successor path"))
        elif successor not in tracked:
            findings.append(_finding("successor-untracked", path, f"successor is not tracked: {successor}"))

        maintained_generator = (
            (
                row.get("kind") == "generator"
                or (
                    row.get("kind") == "validator"
                    and ("check_command" in row or "outputs" in row)
                )
            )
            and row.get("mutation") == "check-write"
            and disposition == "retain"
        )
        if maintained_generator:
            if authority not in MACHINE_AUTHORITIES:
                findings.append(
                    _finding(
                        "generated-authority-invalid",
                        path,
                        "retained check-write generator requires canonical machine authority",
                    )
                )
            error = _generator_command_error(row)
            if error:
                findings.append(_finding("generated-check-invalid", path, error))
            outputs = row.get("outputs")
            if isinstance(outputs, list):
                for output in outputs:
                    if isinstance(output, str) and output not in tracked:
                        findings.append(
                            _finding(
                                "generated-output-untracked",
                                path,
                                f"generated output is not tracked: {output}",
                            )
                        )
        elif "check_command" in row or "outputs" in row:
            findings.append(_finding("generated-fields-invalid", path, "generator fields are allowed only on retained check-write producers"))

    duplicates = sorted(path for path, count in __import__("collections").Counter(declared).items() if count > 1)
    for path in duplicates:
        findings.append(_finding("path-duplicate", path, "manifest path appears more than once"))
    if declared != sorted(declared):
        findings.append(_finding("paths-unsorted", "<manifest>", "manifest rows must be sorted by path"))
    for path in sorted(tracked_scripts - set(declared)):
        findings.append(_finding("manifest-record-missing", path, "tracked script has no manifest row"))
    return sorted(set(findings))


def _git_paths(repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z"],
        cwd=repo_root,
        text=False,
        check=True,
        capture_output=True,
    )
    paths = {raw.decode("utf-8", "surrogateescape") for raw in result.stdout.split(b"\0") if raw}
    for relative in REQUIRED_LOCAL_PATHS:
        candidate = repo_root / relative
        if candidate.is_file() and not candidate.is_symlink():
            paths.add(relative)
    return {
        relative
        for relative in paths
        if _safe_repo_path(relative)
        and (repo_root / relative).is_file()
        and not (repo_root / relative).is_symlink()
    }


def _load_manifest(manifest_path: Path) -> object:
    try:
        return load_manifest_document(manifest_path)
    except SuiteRegistryError as exc:
        return {"_load_error": str(exc)}


def _python_proves_use(text: str, target: str) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    scope_nodes = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)
    node_scopes: dict[int, ast.AST] = {}

    def bind_scopes(node: ast.AST, scope: ast.AST) -> None:
        node_scopes[id(node)] = scope
        for child in ast.iter_child_nodes(node):
            bind_scopes(child, child if isinstance(child, scope_nodes) else scope)

    bind_scopes(tree, tree)
    module = target.removesuffix(".py").replace("/", ".")
    parent_module, _, module_leaf = module.rpartition(".")
    subprocess_modules: set[tuple[ast.AST, str]] = set()
    subprocess_calls: set[tuple[ast.AST, str]] = set()
    runpy_modules: set[tuple[ast.AST, str]] = set()
    importlib_modules: set[tuple[ast.AST, str]] = set()
    spec_calls: set[tuple[ast.AST, str]] = set()
    local_imports: list[tuple[ast.AST, ast.ImportFrom]] = []
    for node in ast.walk(tree):
        scope = node_scopes[id(node)]
        if isinstance(node, ast.Import):
            for alias in node.names:
                local_name = alias.asname or alias.name.split(".", 1)[0]
                if alias.name == module:
                    return True
                if alias.name == "subprocess":
                    subprocess_modules.add((scope, local_name))
                elif alias.name == "runpy":
                    runpy_modules.add((scope, local_name))
                elif alias.name in {"importlib", "importlib.util"}:
                    importlib_modules.add((scope, local_name))
        elif isinstance(node, ast.ImportFrom):
            if node.module == module:
                return True
            if node.module == parent_module and any(
                alias.name == module_leaf for alias in node.names
            ):
                return True
            if node.module == "subprocess":
                subprocess_calls.update(
                    (scope, alias.asname or alias.name)
                    for alias in node.names
                    if alias.name in {"Popen", "check_call", "check_output", "run"}
                )
            elif node.module == "runpy":
                subprocess_calls.update(
                    (scope, alias.asname or alias.name)
                    for alias in node.names
                    if alias.name == "run_path"
                )
            elif node.module == "importlib.util":
                spec_calls.update(
                    (scope, alias.asname or alias.name)
                    for alias in node.names
                    if alias.name == "spec_from_file_location"
                )
            else:
                local_imports.append((scope, node))

    assignments: list[tuple[ast.AST, list[ast.AST], ast.AST]] = []
    for node in ast.walk(tree):
        scope = node_scopes[id(node)]
        if isinstance(node, ast.Assign):
            assignments.append((scope, list(node.targets), node.value))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            assignments.append((scope, [node.target], node.value))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            assignments.append((scope, [node.target], node.iter))

    ambiguous_path = object()
    static_paths: dict[tuple[ast.AST, str], str | object] = {
        (node_scopes[id(name)], name.id): ""
        for name in ast.walk(tree)
        if isinstance(name, ast.Name) and name.id in {"ROOT", "REPO_ROOT"}
    }

    def static_path(node: ast.AST) -> str | object | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return PurePosixPath(node.value).as_posix()
        if isinstance(node, ast.Name):
            scope = node_scopes[id(node)]
            local = static_paths.get((scope, node.id))
            if local is not None:
                return local
            return static_paths.get((tree, node.id))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left = static_path(node.left)
            right = static_path(node.right)
            if left is None or right is None:
                return None
            if left is ambiguous_path or right is ambiguous_path:
                return ambiguous_path
            assert isinstance(left, str) and isinstance(right, str)
            return (PurePosixPath(left) / right).as_posix()
        if (
            isinstance(node, ast.Call)
            and len(node.args) == 1
            and not node.keywords
            and (
                isinstance(node.func, ast.Name) and node.func.id in {"Path", "str"}
                or isinstance(node.func, ast.Attribute) and node.func.attr == "Path"
            )
        ):
            return static_path(node.args[0])
        return None

    changed = True
    while changed:
        changed = False
        for scope, assignment_targets, value in assignments:
            resolved = static_path(value)
            if resolved is None:
                continue
            for assignment_target in assignment_targets:
                if not isinstance(assignment_target, ast.Name):
                    continue
                key = (scope, assignment_target.id)
                current = static_paths.get(key)
                if current is None:
                    joined = resolved
                elif current is ambiguous_path or resolved is ambiguous_path:
                    joined = ambiguous_path
                elif current == resolved:
                    joined = current
                else:
                    joined = ambiguous_path
                if current is not joined:
                    static_paths[key] = joined
                    changed = True

    target_parent = PurePosixPath(target).parent.as_posix()
    for import_scope, node in local_imports:
        if node.module != module_leaf:
            continue
        if any(
            value == target_parent
            and (path_scope is import_scope or path_scope is tree)
            for (path_scope, _), value in static_paths.items()
        ):
            return True

    def contains_exact_target(
        node: ast.AST, names: set[tuple[ast.AST, str]]
    ) -> bool:
        return any(
            static_path(child) == target
            or isinstance(child, ast.Name)
            and (
                (node_scopes[id(child)], child.id) in names
                or (tree, child.id) in names
            )
            for child in ast.walk(node)
        )

    def contains_exact_module(node: ast.AST) -> bool:
        return any(static_path(child) == module for child in ast.walk(node))

    target_names: set[tuple[ast.AST, str]] = set()
    changed = True
    while changed:
        changed = False
        for scope, assignment_targets, value in assignments:
            if not contains_exact_target(value, target_names):
                continue
            assigned = {
                (scope, child.id)
                for assignment_target in assignment_targets
                for child in ast.walk(assignment_target)
                if isinstance(child, ast.Name)
                and static_paths.get((scope, child.id)) is not ambiguous_path
            }
            if not assigned.issubset(target_names):
                target_names.update(assigned)
                changed = True

    invocation_names = {"Popen", "check_call", "check_output", "run", "run_path"}

    def attribute_root(node: ast.AST) -> str:
        current = node
        while isinstance(current, ast.Attribute):
            current = current.value
        return current.id if isinstance(current, ast.Name) else ""

    def visible(names: set[tuple[ast.AST, str]], scope: ast.AST, name: str) -> bool:
        return (scope, name) in names or (tree, name) in names

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        scope = node_scopes[id(node)]
        call_name = (
            node.func.id
            if isinstance(node.func, ast.Name)
            else node.func.attr
            if isinstance(node.func, ast.Attribute)
            else ""
        )
        target_argument = any(
            contains_exact_target(argument, target_names)
            for argument in (*node.args, *(keyword.value for keyword in node.keywords))
        )
        root_name = attribute_root(node.func)
        if (
            isinstance(node.func, ast.Attribute)
            and call_name == "import_module"
            and visible(importlib_modules, scope, root_name)
            and any(contains_exact_module(argument) for argument in node.args)
        ):
            return True
        if target_argument and (
            isinstance(node.func, ast.Name)
            and visible(subprocess_calls, scope, node.func.id)
            or isinstance(node.func, ast.Attribute)
            and call_name in invocation_names
            and (
                visible(subprocess_modules, scope, root_name)
                or visible(runpy_modules, scope, root_name)
            )
        ):
            return True
        if len(node.args) >= 2 and contains_exact_target(node.args[1], target_names) and (
            isinstance(node.func, ast.Name)
            and visible(spec_calls, scope, node.func.id)
            or isinstance(node.func, ast.Attribute)
            and call_name == "spec_from_file_location"
            and visible(importlib_modules, scope, root_name)
        ):
            return True
        if (
            isinstance(node.func, ast.Attribute)
            and call_name in {"exists", "is_file", "read_bytes", "read_text"}
            and contains_exact_target(node.func.value, target_names)
        ):
            return True
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "open"
            and node.args
            and contains_exact_target(node.args[0], target_names)
        ):
            return True
    return False


_MACHINE_REFERENCE_KEYS = frozenset(
    {
        "argv",
        "command",
        "commands",
        "entry",
        "entrypoint",
        "implementation",
        "path",
        "required_evidence_paths",
        "run",
        "script",
    }
)


class EvidenceTraversalError(ValueError):
    """Raised when machine evidence is cyclic and cannot be bounded safely."""


def _machine_config_proves_use(
    document: object,
    target: str,
    parent: str = "",
    _active: set[int] | None = None,
) -> bool:
    """Return whether a typed machine field names the exact target path."""

    if isinstance(document, (dict, list)):
        active = set() if _active is None else _active
        identity = id(document)
        if identity in active:
            raise EvidenceTraversalError("cyclic machine evidence")
        active.add(identity)
        try:
            if isinstance(document, dict):
                for key, value in document.items():
                    if _machine_config_proves_use(
                        value, target, str(key), active
                    ):
                        return True
            else:
                for value in document:
                    if _machine_config_proves_use(value, target, parent, active):
                        return True
            return False
        finally:
            active.remove(identity)
    if parent not in _MACHINE_REFERENCE_KEYS or not isinstance(document, str):
        return False
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9_./-]){re.escape(target)}(?![A-Za-z0-9_./-])",
            document,
        )
    )


def _reference_proves_use(reference: str, text: str, target: str, *, is_test: bool) -> bool:
    basename = PurePosixPath(target).name
    if reference.endswith(".py"):
        return _python_proves_use(text, target)
    if reference.endswith(".sh"):
        return any(
            (target in line or basename in line) and not line.lstrip().startswith("#")
            for line in text.splitlines()
        )
    if is_test:
        return False
    if reference.endswith((".yaml", ".yml")):
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError:
            return False
        return _machine_config_proves_use(value, target)
    if reference.endswith(".json"):
        try:
            value = __import__("json").loads(text)
        except ValueError:
            return False
        return _machine_config_proves_use(value, target)
    if reference.endswith(".md"):
        in_fence = False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if (target in line or basename in line) and (
                in_fence
                or any(
                    target in span or basename in span
                    for span in __import__("re").findall(r"`([^`]+)`", line)
                )
                or ("[" in line and "](" in line)
            ):
                return True
    return False


def _semantic_findings(repo_root: Path, document: object) -> list[Finding]:
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        return []
    findings: list[Finding] = []
    for row in document["files"]:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        path = row["path"]
        for field in ("consumers", "tests"):
            values = row.get(field)
            if not isinstance(values, list):
                continue
            for reference in values:
                ref_path = repo_root / str(reference)
                if not ref_path.is_file():
                    continue
                try:
                    text = ref_path.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    findings.append(_finding(f"{field}-unreadable", path, f"cannot read {reference}"))
                    continue
                try:
                    proven = _reference_proves_use(
                        reference, text, path, is_test=field == "tests"
                    )
                except EvidenceTraversalError:
                    findings.append(
                        _finding(
                            f"{field}-invalid",
                            path,
                            f"{reference} contains cyclic machine evidence",
                        )
                    )
                    continue
                if not proven:
                    findings.append(
                        _finding(
                            f"{field}-unproven",
                            path,
                            f"{reference} does not prove invocation/import/API fixture use",
                        )
                    )
    return findings


def _repo_regular_path(repo_root: Path, relative: str) -> bool:
    try:
        root = repo_root.resolve(strict=True)
        candidate = repo_root / relative
        current = root
        for part in PurePosixPath(relative).parts:
            current = current / part
            if current.is_symlink():
                return False
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
        return resolved.is_file() and not resolved.is_symlink()
    except (OSError, RuntimeError, ValueError):
        return False


def _declared_path_findings(repo_root: Path, document: object) -> list[Finding]:
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        return []
    findings: list[Finding] = []
    for row in document["files"]:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        declared = [row["path"]]
        if isinstance(row.get("outputs"), list):
            declared.extend(value for value in row["outputs"] if isinstance(value, str))
        for relative in declared:
            if not _safe_repo_path(relative) or not _repo_regular_path(repo_root, relative):
                findings.append(
                    _finding(
                        "declared-path-invalid",
                        row["path"],
                        f"declared executable/output must be a repository-contained regular non-symlink path: {relative}",
                    )
                )
    return findings


def _authority_findings(repo_root: Path, document: object) -> list[Finding]:
    if not isinstance(document, dict) or not isinstance(document.get("files"), list):
        return []
    findings: list[Finding] = []
    for row in document["files"]:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        if not (row.get("mutation") == "runtime" and row.get("disposition") == "retain"):
            continue
        authority = row.get("authority")
        if not isinstance(authority, str) or not _repo_regular_path(repo_root, authority):
            continue
        text = (repo_root / authority).read_text(encoding="utf-8")
        metadata: object = {}
        if text.startswith("---\n"):
            try:
                metadata = yaml.safe_load(text.split("---\n", 2)[1]) or {}
            except yaml.YAMLError:
                metadata = {}
        if not isinstance(metadata, dict) or metadata.get("status") != "active" or metadata.get("type") != "operations/runbook":
            findings.append(_finding("runtime-authority-inactive", row["path"], f"{authority} is not a current typed Runbook"))
        if not _reference_proves_use(authority, text, row["path"], is_test=False):
            findings.append(_finding("runtime-authority-unproven", row["path"], f"{authority} does not semantically govern the runtime script"))
    return findings


def check_manifest(repo_root: Path, manifest_path: Path) -> list[Finding]:
    """Validate manifest syntax, working-tree coverage, and semantic references."""

    document = _load_manifest(manifest_path)
    if isinstance(document, dict) and "_load_error" in document:
        return [_finding("manifest-unreadable", manifest_path, str(document["_load_error"]))]
    tracked = _git_paths(repo_root)
    return sorted(
        set(
            validate_manifest_document(document, tracked)
            + _semantic_findings(repo_root, document)
            + _declared_path_findings(repo_root, document)
            + _authority_findings(repo_root, document)
        )
    )


def _git_visible_state(repo_root: Path) -> tuple[str, tuple[tuple[str, str], ...]]:
    diff = subprocess.run(
        ["git", "diff", "--binary", "HEAD"],
        cwd=repo_root,
        text=False,
        check=True,
        capture_output=True,
    ).stdout
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=repo_root,
        text=False,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    fingerprints: list[tuple[str, str]] = []
    for raw in sorted(untracked):
        if not raw:
            continue
        relative = raw.decode("utf-8", "surrogateescape")
        path = repo_root / relative
        if path.is_file() and not path.is_symlink():
            fingerprints.append((relative, hashlib.sha256(path.read_bytes()).hexdigest()))
    return hashlib.sha256(diff).hexdigest(), tuple(fingerprints)


def _declared_output_state(repo_root: Path, outputs: Sequence[str]) -> tuple[tuple[str, str], ...]:
    state: list[tuple[str, str]] = []
    for relative in sorted(outputs):
        if not _repo_regular_path(repo_root, relative):
            raise ValueError(f"unsafe declared output: {relative}")
        state.append((relative, hashlib.sha256((repo_root / relative).read_bytes()).hexdigest()))
    return tuple(state)


def _bounded_repository_state(
    repo_root: Path,
) -> tuple[tuple[str, str, int, int, int, str], ...]:
    """Hash the whole in-repo tree without traversing `.git` or symlinks."""

    state: list[tuple[str, str, int, int, int, str]] = []
    observed_bytes = 0
    for directory, names, filenames in os.walk(repo_root, followlinks=False):
        directory_path = Path(directory)
        if directory_path != repo_root:
            relative_directory = directory_path.relative_to(repo_root).as_posix()
            directory_stat = directory_path.lstat()
            state.append(
                (
                    relative_directory,
                    "directory",
                    directory_stat.st_mode,
                    directory_stat.st_size,
                    directory_stat.st_mtime_ns,
                    "",
                )
            )
        kept_names: list[str] = []
        for name in sorted(names):
            path = directory_path / name
            relative = path.relative_to(repo_root).as_posix()
            if relative == ".git":
                continue
            if path.is_symlink():
                stat = path.lstat()
                state.append(
                    (
                        relative,
                        "symlink",
                        stat.st_mode,
                        stat.st_size,
                        stat.st_mtime_ns,
                        os.readlink(path),
                    )
                )
            else:
                kept_names.append(name)
        names[:] = kept_names
        for name in sorted(filenames):
            path = directory_path / name
            relative = path.relative_to(repo_root).as_posix()
            if relative == ".git":
                continue
            stat = path.lstat()
            if path.is_symlink():
                state.append(
                    (
                        relative,
                        "symlink",
                        stat.st_mode,
                        stat.st_size,
                        stat.st_mtime_ns,
                        os.readlink(path),
                    )
                )
            elif path.is_file():
                observed_bytes += stat.st_size
                if observed_bytes > MAX_OBSERVED_BYTES:
                    raise RuntimeError("bounded repository snapshot exceeds safe byte limit")
                digest = hashlib.sha256()
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1_048_576), b""):
                        digest.update(chunk)
                state.append(
                    (
                        relative,
                        "file",
                        stat.st_mode,
                        stat.st_size,
                        stat.st_mtime_ns,
                        digest.hexdigest(),
                    )
                )
        if len(state) > MAX_OBSERVED_PATHS:
            raise RuntimeError("bounded repository snapshot exceeds safe path limit")
    return tuple(sorted(state))


def check_generated(repo_root: Path, manifest_path: Path) -> list[Finding]:
    """Run registered read-only generator checks and reject visible mutation."""

    findings = check_manifest(repo_root, manifest_path)
    if findings:
        return findings
    document = _load_manifest(manifest_path)
    assert isinstance(document, dict)
    for row in document["files"]:
        if not (
            row["kind"] in {"generator", "validator"}
            and row["mutation"] == "check-write"
            and row["disposition"] == "retain"
            and "check_command" in row
            and "outputs" in row
        ):
            continue
        command = row["check_command"]
        outputs = row["outputs"]
        try:
            before = (
                _git_visible_state(repo_root),
                _declared_output_state(repo_root, outputs),
                _bounded_repository_state(repo_root),
            )
        except (OSError, RuntimeError, ValueError) as exc:
            findings.append(_finding("generated-check-boundary", row["path"], str(exc)))
            continue
        try:
            result = subprocess.run(
                command,
                cwd=repo_root,
                text=True,
                check=False,
                capture_output=True,
            )
        except OSError as exc:
            findings.append(_finding("generated-check-missing", row["path"], str(exc)))
            continue
        try:
            after = (
                _git_visible_state(repo_root),
                _declared_output_state(repo_root, outputs),
                _bounded_repository_state(repo_root),
            )
        except (OSError, RuntimeError, ValueError) as exc:
            findings.append(_finding("generated-check-mutated", row["path"], str(exc)))
            continue
        if after != before:
            findings.append(
                _finding(
                    "generated-check-mutated",
                    row["path"],
                    "registered check command changed declared outputs, Git-visible state, or bounded repository surfaces",
                )
            )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            findings.append(_finding("generated-check-failed", row["path"], detail[-1] if detail else f"exit {result.returncode}"))
    return sorted(set(findings))


def _print_findings(findings: Sequence[Finding]) -> int:
    if findings:
        for finding in findings:
            print(f"FAIL [{finding.code}] {finding.path}: {finding.message}", file=sys.stderr)
        print(f"script_manifest_failures={len(findings)}", file=sys.stderr)
        return 1
    print("PASS: script manifest is valid")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("scripts/manifest.yaml"))
    parser.add_argument("--check-generated", action="store_true")
    args = parser.parse_args(argv)
    repo_root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, check=True, capture_output=True).stdout.strip())
    manifest_path = args.manifest if args.manifest.is_absolute() else repo_root / args.manifest
    findings = check_generated(repo_root, manifest_path) if args.check_generated else check_manifest(repo_root, manifest_path)
    return _print_findings(findings)


if __name__ == "__main__":
    raise SystemExit(main())
