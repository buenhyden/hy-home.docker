"""Value-free outcome classification for the P03 runner fixture."""

from __future__ import annotations

from tests.validation._opsflow_native_fixture import RehearsalFailure

SAFE_ERROR_CLASSES = frozenset(
    {
        "Error",
        "EvalError",
        "NodeOperationError",
        "ReferenceError",
        "SyntaxError",
        "TaskRunnerProcessError",
        "TimeoutError",
        "TypeError",
    }
)
ERROR_CATEGORY_NEEDLES = (
    (
        "code_generation_blocked",
        ("evalerror", "code generation from strings", "disallow-code-generation"),
    ),
    (
        "module_access_denied",
        # ponytail: "module '" covers the pinned runner's JS "Module 'x' is
        # disallowed" and Python stdlib denial; it would also match a Python
        # "module 'x' has no attribute" error, which import denial precedes.
        (
            "cannot find module",
            "module is not allowed",
            "require is not defined",
            "module '",
            "import of external package",
            "relative imports are disallowed",
        ),
    ),
    # The pinned Python runner removes `open` from builtins by default.
    ("builtin_denied", ("name 'open' is not defined",)),
    (
        "environment_access_denied",
        ("access to environment", "environment variable access", "env access denied"),
    ),
    (
        "filesystem_access_denied",
        ("permission denied", "operation not permitted", "access is not allowed"),
    ),
    (
        "filesystem_not_mounted",
        ("filenotfounderror", "no such file or directory"),
    ),
    ("task_timeout", ("timeouterror", "timed out", "timeout")),
    (
        "broker_unavailable",
        ("task runner", "task broker", "runner unavailable", "no runner"),
    ),
    ("request_error", ("fetch failed", "request failed")),
    ("syntax_error", ("syntaxerror",)),
    ("node_operation_error", ("nodeoperationerror",)),
)


def safe_error_facts(payload: object) -> dict[str, str]:
    """Classify a bounded error chain without returning its payload text."""
    cursor = payload
    values: list[str] = []
    observed_name = False
    error_class = "unknown"
    for _ in range(4):
        if not isinstance(cursor, dict):
            break
        name = cursor.get("name")
        if isinstance(name, str):
            observed_name = True
            if name in SAFE_ERROR_CLASSES and error_class == "unknown":
                error_class = name
        for key in ("name", "message", "description", "stack"):
            value = cursor.get(key)
            if isinstance(value, str):
                values.append(value[:2048])
        cursor = cursor.get("cause")
    if error_class == "unknown" and observed_name:
        error_class = "other"
    if not isinstance(payload, dict):
        category = "absent"
    else:
        sample = " ".join(values).lower()[:8192]
        category = next(
            (
                candidate
                for candidate, needles in ERROR_CATEGORY_NEEDLES
                if any(needle in sample for needle in needles)
            ),
            "unclassified",
        )
    return {"error_class": error_class, "error_category": category}


def safe_terminal_error_facts(
    summary: object, allowed_categories: frozenset[str]
) -> dict[str, str | bool]:
    """Require an attributed, value-free terminal denial result."""
    if not isinstance(summary, dict) or summary.get("status") != "error":
        raise RehearsalFailure("terminal denial status rejected")
    error_class = summary.get("errorClass")
    error_category = summary.get("errorCategory")
    known_categories = {category for category, _ in ERROR_CATEGORY_NEEDLES}
    if (
        not allowed_categories
        or not allowed_categories <= known_categories
        or error_category not in allowed_categories
    ):
        raise RehearsalFailure("terminal denial was not safely attributed")
    return {
        "error_class": str(error_class)
        if error_class in SAFE_ERROR_CLASSES
        else "unknown",
        "error_category": str(error_category),
        "attributed": True,
    }


def indeterminate_error_facts(summary: object) -> dict[str, str | bool]:
    """Return a value-free error summary without accepting it as boundary proof."""
    if not isinstance(summary, dict) or summary.get("status") != "error":
        raise RehearsalFailure("indeterminate error status rejected")
    error_class = summary.get("errorClass")
    error_category = summary.get("errorCategory")
    return {
        "error_class": str(error_class)
        if error_class in SAFE_ERROR_CLASSES
        else "unknown",
        "error_category": str(error_category)
        if error_category in {category for category, _ in ERROR_CATEGORY_NEEDLES}
        else "unclassified",
        "attributed": False,
    }
