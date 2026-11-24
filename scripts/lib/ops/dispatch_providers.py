"""Claude and Codex worker adapters for the existing work dispatcher.

A plan unit names `provider: {name, model, prompt, max_budget_usd}` instead of
a command. The adapter turns it into the installed CLI's own non-interactive
argv, never a guessed option, and into a sandbox profile: the dispatcher's
bubblewrap boundary keeps the read-only root and the writable worktree, and
the profile adds only what the provider needs to run, the network for its
API, its binary and its credential file read-only, and a private HOME. The
provider's final JSON gives the session, cost and error that the dispatcher
records. The cgroup scope still owns every process the worker starts.

The credential file is inside the sandbox because the CLI must read it, so
the worker's file tools are denied the private HOME and a result whose patch
or log holds any credential value is rejected. Claude gets no network-capable
tool; only its CLI process uses the shared network. Codex gives the model a
shell, which with the host network and its credentials could reach loopback
services and the token, so it is refused until an egress-limited network
namespace exists.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

MAX_BUDGET_USD = 5.0
WORKER_HOME = "/tmp/home"
# Read-only host files a provider needs for DNS and TLS.
NETWORK_FILES = (
    "/etc/hosts",
    "/etc/nsswitch.conf",
    "/etc/passwd",
    "/etc/group",
    "/etc/ssl",
    "/etc/ca-certificates",
)
CLAUDE_TOOLS = "Read,Edit,Write,Glob,Grep"
MIN_SECRET_CHARS = 16


class ProviderError(ValueError):
    """A provider unit the adapter cannot run as asked."""


def _binary(name: str) -> Path:
    path = Path.home() / ".local" / "bin" / name
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise ProviderError(f"{name} is not installed at {path}") from error


def validate(spec: object) -> dict:
    """The provider spec of a unit, checked before anything starts."""
    if not isinstance(spec, dict) or set(spec) - {
        "name",
        "model",
        "prompt",
        "max_budget_usd",
    }:
        raise ProviderError("provider needs name, model, prompt and max_budget_usd")
    name, model, prompt = spec.get("name"), spec.get("model"), spec.get("prompt")
    budget = spec.get("max_budget_usd")
    if name not in ADAPTERS:
        raise ProviderError(f"provider must be one of {sorted(ADAPTERS)}")
    if name in REFUSED:
        raise ProviderError(f"{name}: {REFUSED[name]}")
    if not all(
        isinstance(v, str) and v.strip() and "\0" not in v for v in (model, prompt)
    ):
        raise ProviderError("provider model and prompt must be non-empty text")
    if (
        type(budget) not in (int, float)
        or not math.isfinite(budget)
        or not 0 < budget <= MAX_BUDGET_USD
    ):
        raise ProviderError(
            f"max_budget_usd must be above 0 and at most {MAX_BUDGET_USD}"
        )
    return spec


def _claude(spec: dict) -> tuple[list[str], dict]:
    binary = _binary("claude")
    argv = [
        str(binary),
        "--print",
        "--output-format",
        "json",
        "--safe-mode",
        "--restricted",
        "--permission-mode",
        "acceptEdits",
        "--tools",
        CLAUDE_TOOLS,
        "--allowedTools",
        CLAUDE_TOOLS,
        "--settings",
        json.dumps(
            {
                "permissions": {
                    "deny": [
                        f"{tool}(/{WORKER_HOME}/**)" for tool in CLAUDE_TOOLS.split(",")
                    ]
                }
            }
        ),
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--setting-sources",
        "",
        "--disable-slash-commands",
        "--no-session-persistence",
        "--max-budget-usd",
        str(spec["max_budget_usd"]),
        "--model",
        spec["model"],
        spec["prompt"],
    ]
    credential = Path.home() / ".claude" / ".credentials.json"
    return argv, {
        "binds": [
            (str(binary), str(binary)),
            (str(credential), f"{WORKER_HOME}/.claude/.credentials.json"),
        ],
        "env": {"HOME": WORKER_HOME},
    }


def _codex(spec: dict) -> tuple[list[str], dict]:
    binary = _binary("codex")
    # The dispatcher's bubblewrap and cgroup scope are the external sandbox;
    # Codex's own sandbox cannot nest inside it.
    argv = [
        str(binary),
        "exec",
        "--json",
        "--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox",
        "-m",
        spec["model"],
        spec["prompt"],
    ]
    credential = Path.home() / ".codex" / "auth.json"
    return argv, {
        "binds": [
            (str(binary), str(binary)),
            (str(credential), f"{WORKER_HOME}/.codex/auth.json"),
        ],
        "env": {"HOME": WORKER_HOME, "CODEX_HOME": f"{WORKER_HOME}/.codex"},
    }


ADAPTERS = {"claude": _claude, "codex": _codex}
REFUSED = {
    "codex": "its shell would share the host network with its credentials;"
    " it needs an egress-limited network namespace first"
}


def _secrets(value) -> set[str]:
    if isinstance(value, dict):
        return set().union(*(_secrets(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(_secrets(item) for item in value), set())
    return (
        {value} if isinstance(value, str) and len(value) >= MIN_SECRET_CHARS else set()
    )


def leaks(profile: dict, data: bytes) -> bool:
    """True when a credential value bound into the worker appears in data.

    Values are compared in memory only and never printed or stored.
    """
    for source, target in profile["binds"]:
        if not target.startswith(WORKER_HOME + "/"):
            continue
        try:
            values = _secrets(json.loads(Path(source).read_text()))
        except (OSError, ValueError):
            continue
        if any(value.encode() in data for value in values):
            return True
    return False


def launch(spec: dict) -> tuple[list[str], dict]:
    """The argv and sandbox profile for a validated provider spec."""
    argv, profile = ADAPTERS[validate(spec)["name"]](spec)
    resolver = os.path.realpath("/etc/resolv.conf")
    profile["binds"] += [(path, path) for path in NETWORK_FILES if Path(path).exists()]
    if Path(resolver).exists():
        profile["binds"].append((resolver, "/etc/resolv.conf"))
        if resolver.startswith("/run/"):
            # A stub resolver file sits under /run, which the sandbox replaces.
            profile["binds"].append((resolver, resolver))
    profile["share_net"] = True
    return argv, profile


def result(name: str, output: str) -> dict:
    """Session, cost and error from the provider's final JSON, or a failure."""
    found = None
    for line in reversed(output.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                found = json.loads(line)
            except ValueError:
                continue
            if name == "claude" or found.get("type") in (
                "turn.completed",
                "turn.failed",
                "error",
            ):
                break
    if not isinstance(found, dict):
        return {"name": name, "is_error": True, "reason": "no final JSON result"}
    if name == "claude":
        return {
            "name": name,
            "is_error": bool(found.get("is_error"))
            or found.get("subtype") != "success",
            "session_id": found.get("session_id"),
            "cost_usd": found.get("total_cost_usd"),
            "num_turns": found.get("num_turns"),
            "duration_ms": found.get("duration_ms"),
        }
    return {
        "name": name,
        "is_error": found.get("type") != "turn.completed",
        "usage": found.get("usage"),
    }
