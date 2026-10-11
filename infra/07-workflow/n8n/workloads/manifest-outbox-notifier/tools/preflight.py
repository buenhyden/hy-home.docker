"""Report source binding gaps; this module never authorizes native operations."""

import re


def pending_prerequisites(contract):
    binding = contract.get("binding", {}) if isinstance(contract, dict) else {}
    reviewed = (
        isinstance(contract, dict)
        and contract.get("status") == "reviewed"
        and isinstance(binding, dict)
        and isinstance(binding.get("sql_commit"), str)
        and re.fullmatch(r"[0-9a-f]{40}", binding["sql_commit"]) is not None
        and isinstance(binding.get("sql_sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", binding["sql_sha256"]) is not None
        and type(binding.get("interface_version")) is int
        and binding["interface_version"] > 0
        and isinstance(binding.get("review_receipt"), str)
        and bool(binding["review_receipt"])
    )
    # Even a structurally complete record cannot authenticate itself or prove
    # image/endpoint/role/backup receipts and current operator authorization.
    return (() if reviewed else ("reviewed_p04_sql_binding",)) + (
        "native_receipts_and_exact_targets",
        "current_operator_authorization",
    )
