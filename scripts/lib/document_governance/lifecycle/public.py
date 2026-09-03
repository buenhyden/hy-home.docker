"""Current public Spec Package lifecycle validation."""

from __future__ import annotations

import pathlib

from scripts.lib.document_governance.spec_packages import (
    SpecPackageError,
    load_spec_packages,
    validate_repository_spec_package_lifecycle,
)
from scripts.lib.document_governance.lifecycle.contract import (
    Finding,
    _finding,
    metadata,
)


def _spec_package_lifecycle_findings(
    root: pathlib.Path,
    profiles: dict[str, object],
    base_ref: str | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    stage03 = root / "docs/03.specs"
    # This check used to return clean unless a Stage 98 Migration file was
    # present, so archived evidence gated a current control and its removal
    # would have silently passed every Spec Package. Current Stage 03 validation
    # derives from the current tree and the Registry alone.
    registry = profiles.get("_registry")
    if not isinstance(registry, metadata.DocumentRegistry):
        return findings
    try:
        packages = (
            load_spec_packages(stage03, registry=registry)
            if stage03.exists() or stage03.is_symlink()
            else ()
        )
        lifecycle_findings = validate_repository_spec_package_lifecycle(
            root,
            packages,
            base_ref=base_ref,
        )
    except SpecPackageError as error:
        findings.append(
            _finding(
                "docs/03.specs",
                "spec-package-invalid",
                str(error),
            )
        )
    else:
        findings.extend(
            _finding(finding.path, finding.code, finding.message)
            for finding in lifecycle_findings
        )
    return findings
