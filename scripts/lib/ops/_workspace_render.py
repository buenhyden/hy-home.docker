"""Isolated Compose configuration renders with synthetic private-file inputs."""

import hashlib
import json
import os
import posixpath
import re
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path

import yaml


def _prepare_sources(copied, sources):
    """Confine all file-loading Compose inputs before invoking Compose.

    Private env/config/secret *contents* are replaced by one synthetic empty
    input. Include/extends topology is retained only for copied public paths.
    Bind mount declarations do not cause file reads during `config`.
    """
    from scripts.lib.ops.workspace_inventory import InventoryError

    allowed = {row["path"] for row in sources}
    synthetic = copied / ".p01-empty-input"
    synthetic.write_text("", encoding="utf-8")
    substitutions = []
    blocked = []

    def confined(source, raw, directory=False):
        if (
            not isinstance(raw, str)
            or not raw
            or "$" in raw
            or "://" in raw
            or raw.startswith(("/", "~"))
            or "\\" in raw
        ):
            raise InventoryError("Unsafe render reference.")
        normalized = posixpath.normpath(posixpath.join(posixpath.dirname(source), raw))
        if normalized == ".." or normalized.startswith("../"):
            raise InventoryError("External render reference.")
        if not directory and normalized not in allowed:
            raise InventoryError("Uncopied render source.")
        return str(copied / normalized)

    def merge_entries(node, depth=0):
        if depth > 64 or not isinstance(node, yaml.MappingNode):
            raise InventoryError("Invalid recursive YAML merge.")
        entries = {}
        for key, value in node.value:
            if key.value == "<<":
                members = (
                    value.value if isinstance(value, yaml.SequenceNode) else [value]
                )
                for member in reversed(members):
                    for inherited_key, inherited_value in merge_entries(
                        member, depth + 1
                    ):
                        entries[inherited_key.value] = (inherited_key, inherited_value)
        for key, value in node.value:
            if key.value != "<<":
                entries[key.value] = (key, value)
        return list(entries.values())

    def transform(node, source, parent="", depth=0):
        if depth > 64:
            raise InventoryError("Recursive render structure refused.")
        if isinstance(node, yaml.SequenceNode):
            return yaml.SequenceNode(
                node.tag,
                [transform(item, source, parent, depth + 1) for item in node.value],
            )
        if not isinstance(node, yaml.MappingNode):
            return node
        if parent in {"include", "extends"} and any(
            key.value == "<<" for key, _ in node.value
        ):
            raise InventoryError("Merged render references require explicit paths.")
        pairs = []
        for key_node, value in merge_entries(node):
            key = key_node.value
            if key in {"env_file", "label_file"} or (
                key == "file" and parent != "extends"
            ):
                value = yaml.ScalarNode("tag:yaml.org,2002:str", str(synthetic))
                substitutions.append({"source": source, "field": key})
            elif parent == "include" and key == "project_directory":
                value = yaml.ScalarNode(
                    value.tag, confined(source, value.value, directory=True)
                )
            elif (parent == "extends" and key == "file") or (
                parent == "include" and key == "path"
            ):
                values = [
                    yaml.ScalarNode(item.tag, confined(source, item.value))
                    for item in (
                        value.value if isinstance(value, yaml.SequenceNode) else [value]
                    )
                ]
                value = (
                    yaml.SequenceNode(value.tag, values)
                    if isinstance(value, yaml.SequenceNode)
                    else values[0]
                )
            elif key == "include":
                if not isinstance(value, yaml.SequenceNode):
                    raise InventoryError("Invalid render include.")
                entries = []
                for item in value.value:
                    if isinstance(item, yaml.ScalarNode):
                        entries.append(
                            yaml.ScalarNode(item.tag, confined(source, item.value))
                        )
                    else:
                        entries.append(transform(item, source, "include", depth + 1))
                value = yaml.SequenceNode(value.tag, entries)
            else:
                value = transform(value, source, str(key), depth + 1)
            pairs.append((key_node, value))
        return yaml.MappingNode(node.tag, pairs)

    for source in sorted(allowed):
        # YAML nodes retain !reset, !override and merge tags; constructors are
        # never executed and private input content is never loaded.
        try:
            doc = yaml.compose((copied / source).read_bytes())
            transformed = transform(doc, source)
            (copied / source).write_text(yaml.serialize(transformed), encoding="utf-8")
        except (InventoryError, OSError, ValueError, yaml.YAMLError):
            blocked.append(source)
    return substitutions, blocked


def _closure(files, compose):
    pending, result = list(files), set()
    while pending:
        source = pending.pop()
        if source not in result:
            result.add(source)
            pending.extend(
                r["target"]
                for r in compose["relations"]
                if r["source"] == source and r.get("target") and r["kind"] != "overlay"
            )
    return result


def _contracts(inputs, cases, compose):
    from scripts.lib.ops.workspace_inventory import _require

    _require(isinstance(inputs, list), "Invalid synthetic input contracts.")
    known = {(c["source"], c["selection"]): c for c in cases}
    allowed = {r["path"] for r in compose["sources"]}
    result = {}
    for item in inputs:
        _require(
            isinstance(item, dict)
            and set(item) <= {"source", "selection", "variables", "files"}
        )
        identity = (item.get("source"), item.get("selection"))
        _require(
            all(isinstance(v, str) for v in identity)
            and identity in known
            and identity not in result
        )
        variables = item.get("variables", {})
        _require(isinstance(variables, dict) and len(variables) <= 128)
        for name, kind in variables.items():
            _require(
                isinstance(name, str)
                and re.fullmatch(r"[A-Z][A-Z0-9_]{0,99}", name) is not None
            )
            _require(
                not name.startswith(("COMPOSE", "DOCKER", "PYTHON", "LD_", "GIT_"))
                and name not in {"PATH", "HOME", "ENV", "BASH_ENV", "SHELLOPTS"}
            )
            _require(
                isinstance(kind, str)
                and kind
                in {"directory", "file", "image", "integer", "port", "subnet", "text"}
            )
        files = item.get("files", known[identity]["files"])
        _require(
            isinstance(files, list)
            and 0 < len(files) <= 8
            and all(isinstance(p, str) and p in allowed for p in files)
        )
        _require(
            len(set(files)) == len(files) and item["source"] in _closure(files, compose)
        )
        overlay = known[identity].get("overlay")
        if overlay:
            _require(
                files[-1] == overlay
                and item["source"] in _closure(files[:-1], compose),
                "Selected overlay and preceding base required.",
            )
        result[identity] = {**item, "variables": variables, "files": files}
    return result


def _synthetic_environment(copied, contract, ordinal):
    result = {}
    for index, (name, kind) in enumerate(sorted(contract["variables"].items())):
        fixture = copied / ".p01-fixtures" / str(ordinal) / name
        if kind in {"directory", "file"}:
            fixture.parent.mkdir(parents=True, exist_ok=True)
            if kind == "directory":
                fixture.mkdir()
            else:
                fixture.write_text("", encoding="utf-8")
            value = str(fixture)
        else:
            value = {
                "image": "example.invalid/p01/fixture:synthetic",
                "integer": "1000",
                "port": "45678",
                "subnet": f"10.254.{index}.0/24",
                "text": "p01-synthetic",
            }[kind]
        result[name] = value
    return result


def _failure_reason(stderr):
    message = (
        stderr.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes)
        else str(stderr or "")
    )
    for tokens, reason in (
        (("required variable", "missing a value"), "missing-required-interpolation"),
        (("undefined network",), "undefined-network"),
        (("undefined volume",), "undefined-volume"),
        (("undefined service",), "undefined-service"),
        (("neither an image nor a build",), "missing-service-definition"),
    ):
        if all(token in message[:16384] for token in tokens):
            return reason
    return "configuration-not-rendered"


def render_inventory(
    root, document, *, run=None, budget_seconds=120, only_cases=None, case_inputs=None
):
    """Render copied public sources only; never contacts Docker's daemon.

    Every case is counted, including fragments, exclusions and time-budget
    residuals. Successful renders prove configuration parsing only.
    """
    from scripts.lib.ops.workspace_inventory import (
        _read_public,
        _require,
        validate,
    )

    run = run or subprocess.run
    validate(document)
    compose = document["compose"]
    root_rows = [r for r in document["services"] if r["root_member"]]
    profiles = sorted({p for r in root_rows for p in r["profiles"]})
    cases = [
        {"source": p, "selection": "all-profiles", "argv": ["--profile", "*"]}
        for p in compose["entrypoints"]
    ]
    cases += [
        {
            "source": r["target"],
            "overlay": r["source"],
            "selection": "overlay:" + r["source"],
            "argv": ["--profile", "*"],
        }
        for r in compose["relations"]
        if r["kind"] == "overlay" and r.get("target")
    ]
    if "docker-compose.yml" in compose["entrypoints"]:
        cases += [
            {
                "source": "docker-compose.yml",
                "selection": "profile:" + p,
                "argv": ["--profile", p],
            }
            for p in profiles
        ]
        cases += [
            {
                "source": "docker-compose.yml",
                "selection": "service:" + name,
                "argv": [],
                "service": name,
            }
            for name in compose["root_services"]
        ]
    root_sources = {r["source"] for r in root_rows}
    cases = [
        {
            **case,
            "files": [
                "docker-compose.yml"
                if case.get("overlay") and case["source"] in root_sources
                else case["source"],
                *([case["overlay"]] if case.get("overlay") else []),
            ],
        }
        for case in cases
    ]
    contracts = _contracts([] if case_inputs is None else case_inputs, cases, compose)
    cases = [
        {
            **case,
            "files": contracts.get((case["source"], case["selection"]), case)["files"],
        }
        for case in cases
    ]
    _require(len(cases) <= 512, "Render case budget exceeded.")
    if only_cases is not None:
        selected = set(only_cases)
        _require(
            all(
                isinstance(item, tuple)
                and len(item) == 2
                and all(isinstance(v, str) for v in item)
                for item in selected
            ),
            "Invalid render selection.",
        )
        cases = [
            case for case in cases if (case["source"], case["selection"]) in selected
        ]
        _require(len(cases) == len(selected), "Unknown render selection.")
    results = []
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="p01-compose-") as temporary:
        copied = Path(temporary)
        for row in document["files"]:
            if "sha256" not in row:
                continue
            raw = _read_public(Path(root), row["path"])
            _require(
                hashlib.sha256(raw).hexdigest() == row["sha256"],
                "Source changed before render.",
            )
            target = copied / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        environment = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "DOCKER_CONFIG": str(copied / ".docker-public-config"),
        }
        (copied / ".docker-public-config").mkdir()
        synthetic = copied / ".p01.env"
        # The public example is the only environment input; inherited service
        # variables, actual .env files and Docker authentication are absent.
        synthetic.write_bytes(
            (copied / ".env.example").read_bytes()
            if (copied / ".env.example").exists()
            else b""
        )
        source_variables = {
            row["path"]: set(
                re.findall(
                    r"(?<!\$)\$\{([A-Z][A-Z0-9_]*)", (copied / row["path"]).read_text()
                )
            )
            for row in compose["sources"]
        }
        for contract in contracts.values():
            declared = set().union(
                *(
                    source_variables.get(source, set())
                    for source in _closure(contract["files"], compose)
                )
            )
            _require(
                set(contract["variables"]) <= declared, "Undeclared synthetic variable."
            )
        substitutions, blocked = _prepare_sources(copied, compose["sources"])
        for ordinal, case in enumerate(cases):
            outcome = {
                "source": case["source"],
                "selection": case["selection"],
                "overlay": case.get("overlay"),
                "environment": "isolated-public-copy",
                "observed_at": datetime.now(UTC).isoformat(),
                "files": case["files"],
            }
            if time.monotonic() - start >= budget_seconds:
                results.append(
                    {**outcome, "result": "NOT_RUN", "reason": "time-budget"}
                )
                continue
            closure = _closure(case["files"], compose)
            if closure.intersection(blocked):
                results.append(
                    {
                        **outcome,
                        "result": "NOT_RUN",
                        "reason": "input-boundary-or-unsupported-yaml",
                    }
                )
                continue
            if any(g.get("source") in closure for g in compose["gaps"]):
                results.append({**outcome, "result": "NOT_RUN", "reason": "source-gap"})
                continue
            command = [
                "docker",
                "compose",
                "--project-name",
                "p01-inventory",
                "--env-file",
                str(synthetic),
                *[arg for source in case["files"] for arg in ("-f", source)],
                *case["argv"],
                "config",
                "--no-env-resolution",
                "--no-path-resolution",
                "--format",
                "json",
            ]
            if case.get("service"):
                command.append(case["service"])
            case_environment = {
                **environment,
                **_synthetic_environment(
                    copied,
                    contracts.get(
                        (case["source"], case["selection"]),
                        {"files": case["files"], "variables": {}},
                    ),
                    ordinal,
                ),
            }
            try:
                response = run(
                    command,
                    cwd=copied,
                    env=case_environment,
                    capture_output=True,
                    check=False,
                    timeout=min(
                        15, max(1, budget_seconds - (time.monotonic() - start))
                    ),
                )
                if response.returncode:
                    results.append(
                        {
                            **outcome,
                            "result": "FAIL",
                            "exit_code": response.returncode,
                            "reason": _failure_reason(response.stderr),
                        }
                    )
                    continue
                model = json.loads(response.stdout)
                count = len(model.get("services", {}))
                results.append(
                    {
                        **outcome,
                        "result": "PASS" if count else "FAIL",
                        "exit_code": 0,
                        "service_count": count,
                    }
                )
            except (OSError, subprocess.TimeoutExpired, ValueError, TypeError):
                results.append(
                    {
                        **outcome,
                        "result": "ERROR",
                        "reason": "tool-unavailable-timeout-or-invalid-model",
                    }
                )
    updated = {
        **document,
        "compose": {
            **compose,
            "render_cases": results,
            "synthetic_file_inputs": substitutions,
            "synthetic_interpolation_inputs": [
                item
                for identity, item in contracts.items()
                if identity in {(c["source"], c["selection"]) for c in cases}
            ],
        },
        "coverage": {
            **document["coverage"],
            "render": {
                "numerator": sum(r["result"] == "PASS" for r in results),
                "denominator": len(results),
            },
        },
    }
    validate(updated)
    return updated
