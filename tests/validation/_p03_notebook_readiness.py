"""Read-only Docker/cache census and explicit P03 Notebook native selection."""

from __future__ import annotations

import os
import re
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass

NOTEBOOK_IMAGE = (
    "lfnovo/open_notebook:1.15.0-single@"
    "sha256:63e2f16daa327b64a98bfad622e0d4b7254a6a437cf266b036169ad25bf3b0c3"
)
SURREALDB_IMAGE = (
    "surrealdb/surrealdb:v2.7.0@"
    "sha256:e5d7387e3727bbe2f7cd6d869e48cd34777272258572ead37c9656b25f745723"
)


@dataclass(frozen=True)
class NativeReadiness:
    notebook_cached: bool
    surrealdb_cached: bool
    blocked_reason: str | None = None

    @property
    def ready(self) -> bool:
        return (
            self.notebook_cached
            and self.surrealdb_cached
            and self.blocked_reason is None
        )

    @property
    def result(self) -> str:
        if self.blocked_reason is not None:
            return "BLOCKED"
        return "READY" if self.ready else "NOT_RUN"

    @property
    def blocked(self) -> tuple[str, ...]:
        return (self.blocked_reason,) if self.blocked_reason is not None else ()

    @property
    def missing(self) -> tuple[str, ...]:
        if self.blocked_reason is not None:
            return ()
        names = []
        if not self.notebook_cached:
            names.append("open_notebook_1_15_0")
        if not self.surrealdb_cached:
            names.append("surrealdb_2_7_0")
        return tuple(names)


def inspect_cached_images(
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> NativeReadiness:
    """Verify local engine authority, then inspect exact images without pulling."""

    blocked_reason: str | None = None

    def invoke(command: list[str]) -> subprocess.CompletedProcess | None:
        nonlocal blocked_reason
        try:
            result = run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except PermissionError:
            blocked_reason = "docker_permission"
            return None
        except (OSError, subprocess.TimeoutExpired):
            blocked_reason = "docker_unavailable"
            return None
        if result.returncode:
            blocked_reason = (
                "docker_permission"
                if "permission denied" in (result.stderr or "").casefold()
                else "docker_unavailable"
            )
            return None
        return result

    context = invoke(["docker", "context", "show"])
    if context is None:
        return NativeReadiness(False, False, blocked_reason)
    if context.stdout.strip() != "default":
        return NativeReadiness(False, False, "docker_context_refused")
    engine = invoke(["docker", "info", "--format", "{{.ID}}|{{.ServerVersion}}"])
    if engine is None:
        return NativeReadiness(False, False, blocked_reason)
    if not re.fullmatch(r"[^|\s]+\|[^|\s]+", engine.stdout.strip()):
        return NativeReadiness(False, False, "docker_engine_identity_invalid")

    def cached(image: str) -> bool:
        nonlocal blocked_reason
        try:
            result = run(
                ["docker", "image", "inspect", "--format", "{{.Id}}", image],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except PermissionError:
            blocked_reason = "docker_permission"
            return False
        except (OSError, subprocess.TimeoutExpired):
            blocked_reason = "docker_unavailable"
            return False
        if result.returncode == 0:
            return True
        detail = (result.stderr or "").casefold()
        if "no such image" in detail or "no such object" in detail:
            return False
        blocked_reason = (
            "docker_permission"
            if "permission denied" in detail
            else "docker_unavailable"
        )
        return False

    notebook = cached(NOTEBOOK_IMAGE)
    surrealdb = False if blocked_reason is not None else cached(SURREALDB_IMAGE)
    return NativeReadiness(notebook, surrealdb, blocked_reason)


class NativeSelectionError(ValueError):
    """The native rehearsal was not explicitly and locally selected."""


def native_selection(environ: Mapping[str, str]) -> str:
    if (
        environ.get("P03_NOTEBOOK_NATIVE_REHEARSAL") != "1"
        or environ.get("P03_NOTEBOOK_NATIVE_CONTEXT") != "default"
        or any(
            environ.get(key)
            for key in (
                "DOCKER_HOST",
                "DOCKER_CONTEXT",
                "DOCKER_TLS_VERIFY",
                "DOCKER_CERT_PATH",
                "DOCKER_CONFIG",
            )
        )
    ):
        raise NativeSelectionError("exact local Notebook native selection required")
    return "default"
