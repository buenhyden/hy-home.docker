"""Pre-numbering to numbered classification folder routes (SPEC-0212-TSK-0096).

Historical translation only: a snapshot or immutable record written before the
cutover keeps its unnumbered route, and readers map it here. Current documents
never load through the unnumbered names.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

_FOLDERS = {
    ("00.workspace", "02.process"): "03.process",
    ("00.workspace", "03.quality"): "04.quality",
    ("02.architecture", "descriptions"): "01.descriptions",
    ("02.architecture", "decisions"): "02.decisions",
    ("05.operations", "guides"): "01.guides",
    ("05.operations", "policies"): "02.policies",
    ("05.operations", "runbooks"): "03.runbooks",
    ("05.operations", "incidents"): "04.incidents",
    ("90.references", "research"): "01.research",
    ("90.references", "audits"): "02.audits",
    ("90.references", "data"): "03.data",
    ("99.templates", "contracts"): "01.contracts",
    ("99.templates", "templates"): "02.templates",
}
_TEMPLATE_FOLDERS = {
    "architecture": "02.architecture",
    "common": "93.common",
    "governance": "91.agent-governance",
    "operations": "05.operations",
    "references": "90.references",
    "requirements": "01.requirements",
    "runtime": "92.runtime",
    "specs": "03.specs",
}
# Single files that changed owner folder in the same cutover, keyed by their
# pre-cutover path.
_RELOCATED = {
    "docs/00.workspace/02.process/approval-boundaries.md": (
        "docs/00.workspace/04.quality/approval-boundaries.md"
    ),
    ".agents/knowledge/glossary.md": "docs/00.workspace/01.project/glossary.md",
    "docs/99.templates/templates/governance/vocabulary.template.md": (
        "docs/99.templates/02.templates/00.workspace/vocabulary.template.md"
    ),
    "docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md": (
        "docs/00.workspace/02.architecture/01.descriptions/0027-agent-governance-canonical-adapter.md"
    ),
    "docs/02.architecture/descriptions/0030-document-lifecycle-governance.md": (
        "docs/00.workspace/02.architecture/01.descriptions/0030-document-lifecycle-governance.md"
    ),
    "docs/02.architecture/decisions/0032-canonical-agent-governance-home.md": (
        "docs/00.workspace/02.architecture/02.decisions/0032-canonical-agent-governance-home.md"
    ),
    "docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md": (
        "docs/00.workspace/02.architecture/02.decisions/0034-canonical-knowledge-and-prompt-surfaces.md"
    ),
    "docs/02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md": (
        "docs/00.workspace/02.architecture/02.decisions/0037-package-disposition-wait-and-task-cancellation.md"
    ),
    "docs/02.architecture/decisions/0044-readme-navigation-and-document-language.md": (
        "docs/00.workspace/02.architecture/02.decisions/0044-readme-navigation-and-document-language.md"
    ),
    "docs/02.architecture/decisions/0048-authority-parents-and-criterion-acceptance.md": (
        "docs/00.workspace/02.architecture/02.decisions/0048-authority-parents-and-criterion-acceptance.md"
    ),
    "docs/02.architecture/decisions/0049-shared-agent-memory-store.md": (
        "docs/00.workspace/02.architecture/02.decisions/0049-shared-agent-memory-store.md"
    ),
    "docs/02.architecture/decisions/0051-summarize-and-delete-retirement.md": (
        "docs/00.workspace/02.architecture/02.decisions/0051-summarize-and-delete-retirement.md"
    ),
    "docs/02.architecture/decisions/0057-operations-role-and-domain-folders.md": (
        "docs/00.workspace/02.architecture/02.decisions/0057-operations-role-and-domain-folders.md"
    ),
}
_PACKAGE_FOLDERS = {"tasks": "01.tasks", "contracts": "02.contracts"}
_SPEC_PACKAGE = re.compile(r"[0-9]{4}-[a-z0-9][a-z0-9-]*")
_OLD_DOMAIN = re.compile(r"[0-9]{2}-[a-z0-9][a-z0-9-]*")
_NEW_DOMAIN = re.compile(r"[0-9]{2}\.[a-z0-9][a-z0-9-]*")
_ROLE_FAMILIES = frozenset({"guides", "policies", "runbooks"})


def _invert(mapping: dict) -> dict:
    return {value: key for key, value in mapping.items()}


def _translate(path: PurePosixPath, *, forward: bool) -> PurePosixPath:
    parts = list(path.parts)
    if len(parts) < 3 or parts[0] != "docs":
        return path
    stage, folder = parts[1], parts[2]
    package = _PACKAGE_FOLDERS if forward else _invert(_PACKAGE_FOLDERS)
    if stage == "03.specs":
        if len(parts) > 3 and _SPEC_PACKAGE.fullmatch(folder):
            parts[3] = package.get(parts[3], parts[3])
        return PurePosixPath(*parts)
    if forward:
        old_folder = folder
        renamed = _FOLDERS.get((stage, folder))
    else:
        old_folder = next(
            (
                old
                for (st, old), new in _FOLDERS.items()
                if (st, new) == (stage, folder)
            ),
            None,
        )
        renamed = old_folder
    if renamed is None:
        return path
    parts[2] = renamed
    if stage == "05.operations" and old_folder in _ROLE_FAMILIES and len(parts) > 3:
        if (_OLD_DOMAIN if forward else _NEW_DOMAIN).fullmatch(parts[3]):
            old, new = ("-", ".") if forward else (".", "-")
            parts[3] = parts[3].replace(old, new, 1)
    if stage == "99.templates" and old_folder == "templates" and len(parts) > 3:
        templates = _TEMPLATE_FOLDERS if forward else _invert(_TEMPLATE_FOLDERS)
        sub = parts[3]
        parts[3] = templates.get(sub, sub)
        if sub == ("specs" if forward else "03.specs") and len(parts) > 4:
            parts[4] = package.get(parts[4], parts[4])
    return PurePosixPath(*parts)


def numbered_path(path: PurePosixPath) -> PurePosixPath:
    """Map a pre-numbering repository path to its numbered route."""

    path = PurePosixPath(path)
    relocated = _RELOCATED.get(path.as_posix())
    if relocated is not None:
        return PurePosixPath(relocated)
    translated = _translate(path, forward=True)
    for old, new in _RELOCATED.items():
        if _translate(PurePosixPath(old), forward=True) == translated:
            return PurePosixPath(new)
    return translated


def pre_numbered_path(path: PurePosixPath) -> PurePosixPath:
    """Map a numbered repository path to the route a pre-cutover snapshot used."""

    path = PurePosixPath(path)
    for old, new in _RELOCATED.items():
        if new == path.as_posix():
            return PurePosixPath(old)
    return _translate(path, forward=False)
