"""Repository-wide metadata references, reports, and CLI orchestration."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import pathlib
import posixpath
import re
import stat
import sys
from collections.abc import Mapping, Sequence

from scripts.lib.document_governance.architecture import (
    ArchitectureDocumentError,
    load_architecture_documents,
    load_preserved_architecture_documents,
    validate_supersession_graph,
)
from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
    parse_frontmatter_text as _parse_frontmatter_text,
)
from scripts.lib.document_governance.identity_history import (
    IdentityHistoryError,
    collect_issued_identities,
    validate_identity_history,
)
from scripts.lib.document_governance.registry import (
    _declares_provider_binding,
    document_type,
    DocumentRegistry,
    RegistryError,
    classify_path as classify_registered_path,
    load_registry,
    load_trusted_requirement_allocation_baseline,
    resolve_template_placeholders,
    validate_frontmatter,
)
from scripts.lib.document_governance.requirements import (
    RequirementPackageError,
    load_requirement_packages,
)
from scripts.lib.document_governance.spec_packages import (
    SpecPackageError,
    load_spec_packages,
    resolve_lifecycle_base,
    validate_repository_spec_package_lifecycle,
)
from scripts.lib.document_governance.metadata.heading import (
    _introduced_body_findings,
    _machine_template_findings,
    _native_migration_compaction_witness,
    extract_markdown_headings,
    validate_body_contract,
)
from scripts.lib.document_governance.metadata.identity import (
    _allocation_findings,
    _decode_git_paths,
    _fenced_yaml_string_arrays,
    _reference_delegation_findings,
    _registry_string_arrays,
    _require_git_worktree,
    _run_git,
    _tracked_machine_templates,
    _tracked_repository_markdown,
)
from scripts.lib.document_governance.metadata.lifecycle import (
    _legacy_exception_evidence,
    _link_target_neutral_text,
    _record_from_text,
    _task10_archive_moved_body_baseline,
    _task5_legacy_parent_ids,
    _task5_move_body_sources,
    _task5_moved_body_baseline,
    _text_at_ref,
    collect_records,
    collect_records_at_ref,
    collect_selected_records_at_ref,
    load_transition_overrides,
    resolve_base_selection,
    validate_record,
)
from scripts.lib.document_governance.metadata.profile import (
    DEFAULT_PROFILES,
    EXPECTED_PROFILE_TYPES,
    ROOT,
    TARGET_MARKDOWN_PREFIXES,
    TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES,
    BaseSelection,
    Finding,
    Manifest,
    ProfileError,
    Record,
    TransitionOverride,
    _finding,
    _normalized_target_path,
    _profile_mapping,
    _string_list,
    build_current_manifest,
    build_manifest,
    build_registry_profiles,
    infer_artifact_type,
    registered_generated_owner,
)

_MARKDOWN_LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")


def _index_membership_findings(
    root: pathlib.Path,
    registry: DocumentRegistry,
    records: Sequence[Record],
) -> list[Finding]:
    """Require every registered package to appear in the index that lists it.

    Stage 90 states the rule in prose: a package "is retired by deleting it in
    the same change that ... removes its row below". The stale direction is
    already covered, because a row pointing at a deleted package fails
    `missing-link-target`. The missing direction had no check at all, which is
    how three Spec Package rows went absent past a green gate.
    """

    findings: list[Finding] = []
    for index_path, member_profile in sorted(registry.indexes.items()):
        members = [
            record.path.as_posix()
            for record in records
            if classify_registered_path(record.path.as_posix(), registry)
            == member_profile
        ]
        source = root / index_path
        if not source.is_file():
            # An absent index over an empty tree is the state of a repository
            # that has no such packages yet, not a governance defect. It only
            # becomes one once a package exists with nowhere to be listed.
            if members:
                findings.append(
                    Finding(
                        index_path,
                        "index-missing",
                        f"{len(members)} registered {member_profile} documents have no index",
                    )
                )
            continue
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding(index_path, "index-unreadable", str(error)))
            continue
        index_directory = pathlib.PurePosixPath(index_path).parent
        listed = set()
        for target in _MARKDOWN_LINK_TARGET.findall(text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("/", "http:", "https:", "mailto:")):
                continue
            listed.add(posixpath.normpath((index_directory / target).as_posix()))
        for member in members:
            if member not in listed:
                findings.append(
                    Finding(
                        index_path,
                        "index-member-unlisted",
                        f"registered {member_profile} is absent from its index: {member}",
                    )
                )
    return findings


def _template_catalog_findings(
    root: pathlib.Path, registry: DocumentRegistry
) -> list[Finding]:
    """Require the catalog to link every registered template source.

    The catalog calls itself "the only navigation surface for templates", and
    category directories carry no README, so a role missing from it is a
    template nobody can find by the documented route. Nothing checked that:
    deleting a row passed both the metadata and the link validators.
    """

    catalog = registry.template_catalog
    present = [
        role_id
        for role_id, role in registry.template_roles.items()
        if isinstance(role.get("source"), str) and (root / role["source"]).is_file()
    ]
    source = root / catalog
    if not source.is_file():
        # An absent catalog over a tree that holds no template source is a
        # repository without templates, not a missing navigation surface.
        if present:
            return [
                Finding(
                    catalog,
                    "template-catalog-missing",
                    f"{len(present)} registered template sources have no catalog",
                )
            ]
        return []
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [Finding(catalog, "template-catalog-unreadable", str(error))]
    directory = pathlib.PurePosixPath(catalog).parent
    listed = set()
    for target in _MARKDOWN_LINK_TARGET.findall(text):
        target = target.split("#", 1)[0]
        if not target or target.startswith(("/", "http:", "https:", "mailto:")):
            continue
        listed.add(posixpath.normpath((directory / target).as_posix()))
    findings: list[Finding] = []
    for role_id in sorted(present):
        if registry.template_roles[role_id]["source"] not in listed:
            findings.append(
                Finding(
                    catalog,
                    "template-catalog-unlisted",
                    f"registered role is absent from the catalog: {role_id}",
                )
            )
    return findings


# A README form is named by its registered profile, never by its filename. The
# `common/readme` type predates the `*-readme` naming, so both are listed.
_README_FORM_TYPES = frozenset({"common/readme"})
_README_FORM_TYPE_SUFFIX = "-readme"


def _is_registered_readme_form(path: pathlib.Path, registry: DocumentRegistry) -> bool:
    """Return whether one path carries a registered README form."""

    profile_id = classify_registered_path(path.as_posix(), registry)
    if profile_id is None:
        return False
    declared = registry.profiles.get(profile_id, {}).get("type")
    return isinstance(declared, str) and (
        declared in _README_FORM_TYPES or declared.endswith(_README_FORM_TYPE_SUFFIX)
    )


def validate_repository_contracts(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    base_ref: str | None = None,
    transition_ref: str | None = None,
) -> list[Finding]:
    """Validate tracked repository surfaces backed by the canonical registry.

    `transition_ref` names the committed state the working tree is compared
    against for lifecycle transitions. Without it every record carries no
    predecessor status, so `invalid-transition` cannot fire and the rule is
    declared but unreachable in this route.
    """

    _require_git_worktree(root)
    findings: list[Finding] = []
    tracked_markdown = _tracked_repository_markdown(root)
    registry_native = isinstance(profiles.get("_registry"), DocumentRegistry)

    if registry_native:
        active_registry = profiles.get("_registry")
        assert isinstance(active_registry, DocumentRegistry)
        findings.extend(_reference_delegation_findings(root, profiles))
        # One ls-tree plus batched blob reads, not a `git show` per file.
        previous_records = (
            {
                record.path.as_posix(): record
                for record in collect_records_at_ref(root, profiles, transition_ref)
            }
            if transition_ref is not None
            else None
        )
        records = collect_records(
            root,
            profiles,
            previous_records=previous_records,
            require_git=True,
        )
        manifest = build_current_manifest(root, records)
        findings.extend(_index_membership_findings(root, active_registry, records))
        findings.extend(_template_catalog_findings(root, active_registry))
        for record in records:
            # Gating on `status == "active"` made `invalid-status` unreachable:
            # a document with a status outside its lifecycle is by definition
            # not active, so the check that would catch it never ran. Template
            # sources keep their own route, because a template's placeholders
            # are correct for a template and invalid for an authored document.
            findings.extend(
                finding
                for finding in validate_record(record, profiles, manifest)
                if finding.severity == "error"
            )
        findings.extend(_allocation_findings(root, profiles, records, base_ref))
        requirement_root = root / "docs/01.requirements"
        if requirement_root.exists() or requirement_root.is_symlink():
            try:
                load_requirement_packages(requirement_root, registry=active_registry)
            except RequirementPackageError as error:
                findings.append(
                    Finding(
                        "docs/01.requirements",
                        "requirement-package-invalid",
                        str(error),
                    )
                )
        spec_root = root / "docs/03.specs"
        spec_package_authority = (
            root
            / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
        )
        if spec_package_authority.is_file():
            try:
                spec_packages = (
                    load_spec_packages(spec_root, registry=active_registry)
                    if spec_root.exists() or spec_root.is_symlink()
                    else ()
                )
                spec_lifecycle_findings = validate_repository_spec_package_lifecycle(
                    root,
                    spec_packages,
                    base_ref=base_ref,
                )
            except SpecPackageError as error:
                findings.append(
                    Finding(
                        "docs/03.specs",
                        "spec-package-invalid",
                        str(error),
                    )
                )
            else:
                findings.extend(
                    Finding(finding.path, finding.code, finding.message)
                    for finding in spec_lifecycle_findings
                )

    if (
        any(prefix.startswith("_workspace/") for prefix in TARGET_MARKDOWN_PREFIXES)
        or _normalized_target_path("_workspace/README.md") is not None
    ):
        findings.append(
            Finding(
                "scripts/validation/check-document-metadata.py",
                "workspace-inventory-coupling",
                "_workspace must remain outside docs metadata inventory inference",
            )
        )

    classified_readmes: list[Record] = []
    readme_registry = profiles.get("_registry") if registry_native else None
    for path in tracked_markdown:
        # `.github/repository-surface.md` carries the repository README form
        # under another name: GitHub resolves a repository's displayed README
        # from `.github/` as well as the root, so a README.md there would take
        # the landing page from the root one. Keying this gate on the filename
        # left that document classified but with none of its declared sections
        # checked.
        if path.name != "README.md" and not (
            isinstance(readme_registry, DocumentRegistry)
            and _is_registered_readme_form(path, readme_registry)
        ):
            continue
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(Finding(path.as_posix(), "readme-unreadable", str(error)))
            continue
        if registry_native:
            active_registry = profiles.get("_registry")
            assert isinstance(active_registry, DocumentRegistry)
            readme_profile = classify_registered_path(path.as_posix(), active_registry)
            if readme_profile is None:
                continue
            # Each README profile declares its own required_sections. Checking
            # them all against the `readme` profile's list would have been
            # wrong, so the previous code checked only `readme` documents and
            # skipped the other 131, leaving every other profile's declared
            # sections unenforced.
            _, h2 = extract_markdown_headings(text)
            raw_readme = active_registry.profiles.get(readme_profile, {})
            required_sections = raw_readme.get("required_sections", ())
            if isinstance(required_sections, Sequence) and not isinstance(
                required_sections, (str, bytes)
            ):
                for section in required_sections:
                    heading = f"## {section}"
                    if isinstance(section, str) and heading not in h2:
                        findings.append(
                            Finding(
                                path.as_posix(),
                                "readme-heading-missing",
                                f"Registry README is missing required heading: {heading}",
                            )
                        )
            continue

    template_roles = profiles.get("template_roles", {})
    if not isinstance(template_roles, dict):
        raise ProfileError("template_roles must be a mapping")
    roles_by_source = {
        role["source"]: (name, role)
        for name, role in template_roles.items()
        if isinstance(name, str)
        and isinstance(role, dict)
        and isinstance(role.get("source"), str)
    }
    template_target_types = EXPECTED_PROFILE_TYPES - {
        "generated",
        "governance",
        "readme",
        "template-source",
        "unsupported",
    }
    tracked_templates = (
        []
        if registry_native
        else [
            path
            for path in tracked_markdown
            if path.as_posix().startswith("docs/99.templates/templates/")
            and path.name != "README.md"
            and (root / path).is_file()
        ]
    )
    for path in tracked_templates:
        try:
            text = (root / path).read_text(encoding="utf-8")
            values = _parse_frontmatter_text(text)
        except FrontmatterError as error:
            findings.append(
                Finding(path.as_posix(), "template-source-invalid", str(error))
            )
            continue
        findings.extend(
            validate_body_contract(
                _record_from_text(path, text),
                text,
                profiles,
                changed_boundary=False,
            )
        )
        declares_type = "artifact_type" in values
        declared_type = values.get("type")
        mapped = roles_by_source.get(path.as_posix())
        mapped_type = mapped[1].get("artifact_profile") if mapped else None
        if path.as_posix() in TRANSITIONAL_UNREGISTERED_TEMPLATE_SOURCES:
            continue
        if not declares_type and mapped_type is None:
            continue
        if not declares_type and mapped_type in {"governance", "readme"}:
            continue
        if declared_type is None:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-missing-type",
                    "registered or typed Markdown template requires a non-null artifact_type",
                )
            )
            continue
        if (
            not isinstance(declared_type, str)
            or declared_type not in template_target_types
        ):
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-unknown-type",
                    f"typed Markdown template declares unsupported artifact_type {declared_type!r}",
                )
            )
        if mapped_type is None:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-unmapped",
                    "typed Markdown template is not registered",
                )
            )
        if mapped_type is not None and declared_type != mapped_type:
            findings.append(
                Finding(
                    path.as_posix(),
                    "template-source-type-mismatch",
                    f"registry target {mapped_type!r} differs from declared artifact_type {declared_type!r}",
                )
            )
    if not registry_native:
        for source_path in sorted(roles_by_source):
            if not (root / source_path).is_file():
                findings.append(
                    Finding(
                        source_path,
                        "template-source-missing",
                        "registered Markdown template does not exist",
                    )
                )

    for path in () if registry_native else _tracked_machine_templates(root):
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                Finding(path.as_posix(), "machine-template-unreadable", str(error))
            )
            continue
        findings.extend(
            validate_body_contract(
                Record(path, {}, "unsupported"),
                text,
                profiles,
                changed_boundary=False,
            )
        )

    human_support = (
        []
        if registry_native
        else [
            path
            for path in tracked_markdown
            if path.as_posix().startswith("docs/99.templates/support/")
            and path.suffix == ".md"
        ]
    )
    registry_arrays_by_key: dict[str, list[tuple[tuple[str, ...], list[str]]]] = (
        collections.defaultdict(list)
    )
    for registry_path, members in _registry_string_arrays(profiles):
        if registry_path:
            registry_arrays_by_key[registry_path[-1]].append((registry_path, members))
    for path in human_support:
        try:
            text = (root / path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                Finding(path.as_posix(), "support-contract-unreadable", str(error))
            )
            continue
        duplicated: set[str] = set()
        for candidate_path, candidate_members in _fenced_yaml_string_arrays(text):
            if not candidate_path:
                continue
            for registry_path, registry_members in registry_arrays_by_key.get(
                candidate_path[-1], []
            ):
                if candidate_members == registry_members:
                    duplicated.add(".".join(registry_path))
        if duplicated:
            findings.append(
                Finding(
                    path.as_posix(),
                    "registry-array-duplicated",
                    f"human support document copies canonical registry arrays: {', '.join(sorted(duplicated))}",
                )
            )

    return sorted(set(findings))


def _relation_impact_findings(
    selected_paths: set[str],
    records_by_path: Mapping[str, Record],
    head_records_by_path: Mapping[str, Record],
    base_records_by_path: Mapping[str, Record],
    manifest: Manifest,
    findings_by_path: Mapping[str, Sequence[Finding]],
) -> dict[str, list[Finding]]:
    """Return only relation findings newly caused by selected typed identity removal."""

    removed_ids: set[str] = set()
    for path in sorted(selected_paths):
        for previous in (
            head_records_by_path.get(path),
            base_records_by_path.get(path),
        ):
            artifact_id = previous.metadata.get("artifact_id") if previous else None
            if (
                isinstance(artifact_id, str)
                and artifact_id.strip()
                and artifact_id.strip() not in manifest
            ):
                removed_ids.add(artifact_id.strip())
    if not removed_ids:
        return {}

    expected_messages = {
        "unresolved-parent": {
            f"parent artifact_id is unresolved: {artifact_id}"
            for artifact_id in removed_ids
        },
        "unresolved-supersedes": {
            f"superseded artifact_id is unresolved: {artifact_id}"
            for artifact_id in removed_ids
        },
    }
    impacted: dict[str, list[Finding]] = {}
    for path, findings in sorted(findings_by_path.items()):
        relation_findings = [
            finding
            for finding in findings
            if finding.severity == "error"
            and finding.message in expected_messages.get(finding.code, set())
        ]
        if relation_findings:
            impacted[path] = sorted(relation_findings)
    return impacted


def _escape_cell(value: object) -> str:
    rendered = str(value).replace("|", "\\|").replace("\n", " ")
    return rendered or "—"


def _profile_sets(profile: dict[str, object]) -> tuple[set[str], set[str], set[str]]:
    return (
        set(profile.get("required", [])),
        set(profile.get("optional", [])),
        set(profile.get("forbidden", [])),
    )


def _frontmatter_state(record: Record, findings: Sequence[Finding]) -> str:
    if record.parse_error_code:
        return record.parse_error_code
    if not record.frontmatter_present:
        return "missing-fence"
    if any(finding.severity == "error" for finding in findings):
        return "profile-semantic-error"
    return "allowed-syntax"


def _identity_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    value = record.metadata.get("artifact_id")
    if "artifact_id" in forbidden:
        return "not-applicable"
    if value is None:
        return "missing" if "artifact_id" in required else "not-provided-optional"
    if "invalid-artifact-id" in codes:
        return "invalid"
    if "duplicate-artifact-id" in codes:
        return "duplicate"
    return "valid" if "artifact_id" in required | optional else "type-inappropriate"


def _relation_state(record: Record, profile: dict[str, object], codes: set[str]) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    if "parent_ids" in forbidden:
        parent_state = "not-applicable"
        order_state = "not-applicable"
    elif "parent_ids" not in record.metadata:
        parent_state = (
            "missing" if "parent_ids" in required else "not-provided-optional"
        )
        order_state = "not-provided"
    else:
        relation_errors = sorted(
            codes
            & {
                "invalid-parent-ids",
                "duplicate-parent",
                "missing-parent",
                "self-parent",
                "unresolved-parent",
                "invalid-parent-type",
                "parent-cycle",
            }
        )
        parents = _string_list(record.metadata.get("parent_ids"))
        order_state = "declared-list" if parents is not None else "invalid"
        if relation_errors:
            parent_state = "invalid:" + ",".join(relation_errors)
        elif parents:
            parent_state = f"resolved:{len(parents)}"
        else:
            parent_state = "root-permitted"
    if "supersedes" not in record.metadata:
        return f"parents={parent_state}; order={order_state}; supersedes=not-provided"
    supersession_errors = sorted(
        code for code in codes if "supersed" in code or "supersession" in code
    )
    supersedes_state = (
        "invalid:" + ",".join(supersession_errors)
        if supersession_errors
        else "resolved"
    )
    return f"parents={parent_state}; order={order_state}; supersedes={supersedes_state}"


def _lifecycle_state(
    record: Record, profile: dict[str, object], codes: set[str]
) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    if "status" in forbidden:
        return "not-applicable"
    status = record.metadata.get("status")
    if status is None:
        return "missing" if "status" in required else "not-provided-optional"
    signals = sorted(
        codes
        & {
            "invalid-status",
            "stale-active",
            "replacement-free-supersession",
            "archived-outside-stage-98",
        }
    )
    state = "invalid" if "invalid-status" in signals else "allowed"
    suffix = "; signals=" + ",".join(signals) if signals else ""
    rendered_status = "invalid-value" if "invalid-status" in signals else status
    return f"status={rendered_status}; {state}{suffix}"


def _transition_state(
    record: Record, profile: dict[str, object], codes: set[str]
) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    if record.artifact_type in {
        "readme",
        "generated",
        "template-source",
        "governance",
        "unsupported",
    }:
        return "not-applicable"
    required, optional, forbidden = _profile_sets(profile)
    if "status" in forbidden or "status" not in required | optional:
        return "not-applicable"
    status = record.metadata.get("status")
    if not isinstance(status, str):
        return "not-applicable"
    if record.previous_status is None:
        return "unavailable-no-history"
    if record.previous_status == status:
        return "available-unchanged"
    verdict = "invalid" if "invalid-transition" in codes else "valid"
    return f"available:{record.previous_status}->{status}; {verdict}"


def _freshness_state(
    record: Record, profile: dict[str, object], codes: set[str]
) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    required, optional, forbidden = _profile_sets(profile)
    states: list[str] = []
    invalid_codes = {
        "reviewed_at": "invalid-reviewed-at",
        "next_review_at": "invalid-review-cycle",
    }
    for key in ("reviewed_at", "next_review_at"):
        disposition = (
            "required"
            if key in required
            else "optional"
            if key in optional
            else "forbidden"
        )
        if key in forbidden and key not in record.metadata:
            evidence = "not-applicable"
        elif key not in record.metadata:
            evidence = "missing" if disposition == "required" else "not-provided"
        elif invalid_codes[key] in codes:
            evidence = "invalid"
        else:
            evidence = "present"
        states.append(f"{key}={disposition}:{evidence}")
    return "; ".join(states)


def _exception_context(
    record: Record, codes: set[str], profiles: dict[str, object]
) -> str:
    if record.parse_error:
        return "unavailable-parser-error"
    if record.artifact_type == "readme":
        active_registry = profiles.get("_registry")
        profile_name = (
            classify_registered_path(record.path.as_posix(), active_registry)
            if isinstance(active_registry, DocumentRegistry)
            else None
        )
        if profile_name is None:
            return (
                "README profile=unclassified; consumer=unavailable; role=folder-index"
            )
        return f"README profile={profile_name}; consumer=registry; role=folder-index"
    if record.artifact_type == "generated":
        owner = record.metadata.get("generated_by") or registered_generated_owner(
            record.path,
            profiles,
        )
        rendered = (
            owner
            if isinstance(owner, str) and "invalid-generator" not in codes
            else "invalid-or-missing"
        )
        return f"generated profile; owner={rendered}"
    if record.artifact_type in {
        "template-source",
        "governance",
        "archive",
        "unsupported",
    }:
        return f"{record.artifact_type} profile"
    return "not-applicable"


def render_report(
    records: Sequence[Record],
    profiles: dict[str, object],
    findings_by_path: dict[str, list[Finding]],
) -> str:
    """Render the deterministic exhaustive advisory Markdown inventory."""

    _, profile_map = _profile_mapping(profiles)
    profile_counts = collections.Counter(record.artifact_type for record in records)
    finding_counts = collections.Counter(
        finding.code for findings in findings_by_path.values() for finding in findings
    )
    semantic_count = sum(1 for findings in findings_by_path.values() if findings)
    parse_count = sum(1 for record in records if record.parse_error)
    lines = [
        "---",
        "status: active",
        "generated_by: scripts/validation/check-document-metadata.py",
        "---",
        "",
        "<!-- Target: docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md -->",
        "",
        "# Reference: Frontmatter Semantic Inventory",
        "",
        "## Overview",
        "",
        "This generated advisory reference inventories every tracked target-stage and",
        "governance/template Markdown document except this self-referential output. It records inferred profiles",
        "and metadata findings without printing body content, secret values, or raw logs.",
        "",
        "## Purpose",
        "",
        "Provide the deterministic pre/post-migration comparison for Spec 123 Tasks 7 and 8.",
        "Historical semantic findings remain advisory here; the separate changed/new",
        "checker enforces only its safely selected diff scope.",
        "",
        "## Repository Role",
        "",
        "Stage 00 and Stage 99 own active metadata policy. This Stage 90 snapshot is",
        "generated evidence only; regenerate it with `check-document-metadata.py`.",
        "",
        "## Scope",
        "",
        "### In Scope",
        "",
        "- Tracked Markdown paths, inferred profiles, safe frontmatter parse state, and finding codes",
        "- Identity, parent, lifecycle, freshness, README, generated, governance, template, and archive profiles",
        "",
        "### Out of Scope",
        "",
        "- Automatic document rewrites, corpus-wide blocking, or lifecycle changes",
        "- Filesystem modification times as freshness evidence",
        "- Raw document bodies, logs, credentials, or secret values",
        "",
        "## Definitions / Facts",
        "",
        f"- **Tracked records**: {len(records)}",
        f"- **Records with findings**: {semantic_count}",
        f"- **Frontmatter parser failures**: {parse_count}",
        "- **Enforcement state**: full inventory advisory; changed/new pre-push selection blocking",
        "",
        "## Profile Summary",
        "",
        "| Profile | Records |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{name}` | {count} |" for name, count in sorted(profile_counts.items())
    )
    lines.extend(
        ["", "## Finding Summary", "", "| Finding | Count |", "| --- | ---: |"]
    )
    if finding_counts:
        lines.extend(
            f"| `{code}` | {count} |" for code, count in sorted(finding_counts.items())
        )
    else:
        lines.append("| `none` | 0 |")
    lines.extend(
        [
            "",
            "## Inventory",
            "",
            "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in sorted(records, key=lambda item: item.path.as_posix()):
        findings = findings_by_path.get(record.path.as_posix(), [])
        code_set = {finding.code for finding in findings}
        codes = ", ".join(sorted(code_set)) or "none"
        raw_profile = profile_map.get(record.artifact_type, {})
        disposition = (
            raw_profile.get("disposition", "advisory-only")
            if isinstance(raw_profile, dict)
            else "advisory-only"
        )
        row = [
            f"`{record.path.as_posix()}`",
            f"`{record.artifact_type}`",
            _frontmatter_state(record, findings),
            _identity_state(record, raw_profile, code_set),
            _relation_state(record, raw_profile, code_set),
            _lifecycle_state(record, raw_profile, code_set),
            _transition_state(record, raw_profile, code_set),
            _freshness_state(record, raw_profile, code_set),
            _exception_context(record, code_set, profiles),
            codes,
            disposition,
        ]
        lines.append("| " + " | ".join(_escape_cell(value) for value in row) + " |")
    lines.extend(
        [
            "",
            "## Source Rules",
            "",
            "- Paths come from sorted `git ls-files '*.md'` output filtered to canonical docs stages; non-Git fixtures use sorted recursive discovery.",
            "- YAML is parsed with PyYAML `safe_load` behavior plus duplicate-key rejection.",
            "- Every row states parse, identity, relation, lifecycle, transition-evidence, freshness, and exception semantics; unavailable history is never inferred.",
            "- The report shows only bounded metadata states, safe repository paths, counts, and finding codes.",
            "- Graphify is advisory and is not used as inventory proof.",
            "",
            "## Sources",
            "",
            "- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) - metadata ownership and exception rules",
            "- [Lifecycle status](../../../99.templates/support/lifecycle-status.md) - lifecycle vocabulary and transitions",
            "- [Spec 123](../../../03.specs/123-agentic-engineering-audit-remediation/spec.md) - typed metadata and rollout contract",
            "- [Semantic audit](./frontmatter-template-readme-implementation.md) - pre-remediation criteria and baseline",
            "",
            "## Maintenance",
            "",
            "- **Owner**: Metadata program owner / rules-engineer",
            "- **Review Cadence**: Regenerate when tracked Markdown or metadata profiles change",
            "- **Update Trigger**: Profile, parser, lifecycle, relation, exception, or corpus changes",
            "",
            "## Related Documents",
            "",
            "- [Audit pack README](./README.md)",
            "- [Frontmatter/template/README audit](./frontmatter-template-readme-implementation.md)",
            "- [SDLC and document-contract audit](./sdlc-document-contracts-implementation.md)",
            "",
        ]
    )
    return "\n".join(lines)


def _changed_paths(
    root: pathlib.Path,
    explicit: Sequence[str],
    base: BaseSelection,
) -> set[str]:
    changed: set[str] = set()
    commands = [
        (
            "unstaged Markdown discovery",
            ["diff", "--name-only", "-z", "--diff-filter=ACDMRT", "--", "*.md"],
        ),
        (
            "staged Markdown discovery",
            [
                "diff",
                "--cached",
                "--name-only",
                "-z",
                "--diff-filter=ACDMRT",
                "--",
                "*.md",
            ],
        ),
        (
            "untracked Markdown discovery",
            ["ls-files", "-z", "--others", "--exclude-standard", "--", "*.md"],
        ),
    ]
    if base.merge_base:
        commands.insert(
            0,
            (
                "committed branch Markdown discovery",
                [
                    "diff",
                    "--name-only",
                    "-z",
                    "--diff-filter=ACDMRT",
                    f"{base.merge_base}...HEAD",
                    "--",
                    "*.md",
                ],
            ),
        )
    for operation, command in commands:
        result = _run_git(root, command, operation=operation)
        if result.returncode != 0:
            raise ProfileError(
                f"cannot establish local Git snapshot: {operation} failed"
            )
        changed.update(
            normalized.as_posix()
            for path in _decode_git_paths(result.stdout, operation)
            if (normalized := _normalized_target_path(path.as_posix())) is not None
        )
    if explicit:
        return {
            normalized.as_posix()
            for path in explicit
            if (normalized := _normalized_target_path(path)) is not None
        }
    return changed


def _write_or_check_output(output: pathlib.Path, rendered: str, check: bool) -> bool:
    if check:
        try:
            return output.read_text(encoding="utf-8") == rendered
        except OSError:
            return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("report", "check-changed", "check-active", "check-contracts"),
        default="report",
    )
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument(
        "--registry",
        "--profiles",
        dest="profiles",
        type=pathlib.Path,
        default=DEFAULT_PROFILES,
        help="Stage 99 registry (legacy --profiles remains a transition alias)",
    )
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument(
        "--check", action="store_true", help="compare --output without writing"
    )
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument(
        "--base-ref",
        default=None,
        help="optional Git ref for lifecycle transition comparison",
    )
    parser.add_argument(
        "--history-scope",
        choices=("changed", "full"),
        default="changed",
        help="scan all Git history only for the explicit full document-contract profile",
    )
    parser.add_argument(
        "--transition-override-file",
        type=pathlib.Path,
        help="explicit scoped reverse-transition approval evidence",
    )
    args = parser.parse_args(argv)
    if args.check and args.output is None:
        parser.error("--check requires --output")
    if args.history_scope == "full" and args.mode != "check-contracts":
        parser.error("--history-scope full requires --mode check-contracts")
    root = args.root.resolve()
    base = BaseSelection("not-applicable", None, None)
    registry = None
    try:
        if args.mode == "check-changed":
            _require_git_worktree(root)
            base = resolve_base_selection(root, args.base_ref)
        elif args.mode == "check-contracts":
            _require_git_worktree(root)
            resolve_base_selection(root, args.base_ref)
        if args.profiles.suffix.lower() == ".json":
            trusted_requirement_baseline = None
            canonical_registry_path = root / "docs/99.templates/registry.json"
            try:
                profile_status = args.profiles.lstat()
            except OSError as error:
                raise RegistryError(f"cannot stat registry input: {error}") from error
            if stat.S_ISLNK(profile_status.st_mode) or not stat.S_ISREG(
                profile_status.st_mode
            ):
                raise RegistryError("registry input must be a regular non-symlink file")
            allocation_transition_mode = args.mode in {
                "check-changed",
                "check-contracts",
            } and args.profiles.resolve(
                strict=False
            ) == canonical_registry_path.resolve(strict=False)
            if allocation_transition_mode:
                revision = resolve_lifecycle_base(root, args.base_ref)
                if revision is None:
                    raise ProfileError(
                        "Requirement allocation transition requires a trusted base commit"
                    )
                trusted_requirement_baseline = (
                    load_trusted_requirement_allocation_baseline(revision, root=root)
                )
            registry = load_registry(
                args.profiles,
                trusted_requirement_baseline=trusted_requirement_baseline,
                allow_requirement_allocation_transition=allocation_transition_mode,
            )
            profiles = build_registry_profiles(registry)
            requirement_root = root / "docs/01.requirements"
            if allocation_transition_mode and (
                requirement_root.exists() or requirement_root.is_symlink()
            ):
                load_requirement_packages(
                    requirement_root,
                    registry=registry,
                    trusted_requirement_baseline=trusted_requirement_baseline,
                    allow_requirement_allocation_transition=True,
                )
            architecture_root = root / "docs/02.architecture"
            if architecture_root.exists() or architecture_root.is_symlink():
                architecture_documents = load_architecture_documents(
                    architecture_root,
                    registry=registry,
                )
                # A preserved predecessor still owns its identity, so the graph
                # sees both sides of a completed supersession.
                architecture_documents += load_preserved_architecture_documents(
                    root / "docs/98.archive",
                    registry=registry,
                )
                graph_findings = validate_supersession_graph(architecture_documents)
                if graph_findings:
                    finding = graph_findings[0]
                    raise ArchitectureDocumentError(
                        f"{finding.code}: {finding.path}: {finding.message}"
                    )
        else:
            raise ProfileError("profiles must be the Stage 99 JSON registry")
    except (
        ArchitectureDocumentError,
        ProfileError,
        RegistryError,
        RequirementPackageError,
        SpecPackageError,
    ) as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 2
    if args.mode == "check-contracts" and args.profiles.suffix.lower() == ".json":
        assert registry is not None
        contract_findings: list[Finding] = []
        for role, definition in registry.template_roles.items():
            source = definition.get("source")
            if not isinstance(source, str):
                continue
            template = root / source
            if not template.is_file() or template.is_symlink():
                contract_findings.append(
                    Finding(
                        source,
                        "template-source-missing",
                        f"registered role is unavailable: {role}",
                    )
                )
                continue
            try:
                text = template.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                contract_findings.append(
                    Finding(
                        source,
                        "template-source-unreadable",
                        "registered template is not readable UTF-8",
                    )
                )
                continue
            if template.suffix == ".md":
                profile_ids = definition["profiles"]
                profile_id = profile_ids[0]
                profile = registry.profiles.get(str(profile_id))
                if not isinstance(profile, Mapping):
                    contract_findings.append(
                        Finding(source, "template-profile-mismatch", str(profile_id))
                    )
                    continue
                try:
                    values = _parse_frontmatter_text(text)
                except FrontmatterError:
                    contract_findings.append(
                        Finding(
                            source,
                            "template-frontmatter-invalid",
                            "template frontmatter is not valid YAML",
                        )
                    )
                    continue
                provider_owned = _declares_provider_binding(profile)
                if not provider_owned and values.get("type") != document_type(
                    profile_id
                ):
                    # A provider-owned template declares the runtime's own keys,
                    # so it carries no `type` and no lifecycle status.
                    contract_findings.append(
                        Finding(
                            source,
                            "template-artifact-type-mismatch",
                            f"expected exact artifact_type: {profile_id}",
                        )
                    )
                required = set(profile.get("required_frontmatter", ()))
                optional = set(profile.get("optional_frontmatter", ()))
                for key in sorted(required - set(values)):
                    contract_findings.append(
                        Finding(
                            source,
                            "template-frontmatter-missing",
                            f"required frontmatter key is missing: {key}",
                        )
                    )
                for key in sorted(set(values) - required - optional):
                    contract_findings.append(
                        Finding(
                            source,
                            "template-frontmatter-unregistered",
                            f"frontmatter key is not registered: {key}",
                        )
                    )
                try:
                    schema_values = resolve_template_placeholders(values)
                    schema_findings = validate_frontmatter(
                        schema_values,
                        root
                        / "docs/99.templates/contracts/document-frontmatter.schema.json",
                    )
                except RegistryError:
                    contract_findings.append(
                        Finding(
                            source,
                            "template-frontmatter-schema-unavailable",
                            "frontmatter schema cannot be trusted",
                        )
                    )
                else:
                    contract_findings.extend(
                        Finding(source, finding.code, finding.message)
                        for finding in schema_findings
                    )
                lifecycle_id = profile.get("lifecycle_id")
                if isinstance(lifecycle_id, str) and not provider_owned:
                    status = values.get("status")
                    if status not in registry.lifecycles.get(lifecycle_id, ()):
                        contract_findings.append(
                            Finding(
                                source,
                                "template-status-invalid",
                                f"status is outside lifecycle: {lifecycle_id}",
                            )
                        )
                h1, h2 = extract_markdown_headings(text)
                if len(h1) != 1:
                    contract_findings.append(
                        Finding(
                            source,
                            "template-h1-invalid",
                            "Markdown template must contain exactly one H1",
                        )
                    )
                actual_sections = {heading.removeprefix("## ") for heading in h2}
                required_sections = set(profile.get("required_sections", ()))
                optional_sections = set(profile.get("optional_sections", ()))
                for section in sorted(required_sections - actual_sections):
                    contract_findings.append(
                        Finding(
                            source,
                            "template-section-missing",
                            f"required section is missing: {section}",
                        )
                    )
                for section in sorted(
                    actual_sections - required_sections - optional_sections
                ):
                    contract_findings.append(
                        Finding(
                            source,
                            "template-section-unregistered",
                            f"section is not registered: {section}",
                        )
                    )
                if re.search(
                    r"docs/(?:01\.requirements|02\.architecture|03\.specs|"
                    r"05\.operations|90\.references|98\.archive)/",
                    text,
                ):
                    contract_findings.append(
                        Finding(
                            source,
                            "template-concrete-target",
                            "template embeds a concrete target-stage path",
                        )
                    )
            else:
                contract_findings.extend(
                    _machine_template_findings(
                        Record(pathlib.PurePosixPath(source), {}, "unsupported"),
                        text,
                    )
                )
        try:
            contract_findings.extend(
                validate_repository_contracts(
                    root,
                    profiles,
                    base_ref=args.base_ref,
                    # The full history scope is the only route with a
                    # committed predecessor to compare against, so it is
                    # where the transition rule becomes reachable.
                    transition_ref="HEAD" if args.history_scope == "full" else None,
                )
            )
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        if args.history_scope == "full":
            try:
                issued = collect_issued_identities(root, refs=("--all",))
            except IdentityHistoryError as error:
                print(f"configuration-error: {error}", file=sys.stderr)
                return 2
            contract_findings.extend(
                Finding(finding.path, finding.code, finding.message)
                for finding in validate_identity_history(registry, issued)
            )
        contract_findings = sorted(set(contract_findings))
        for finding in contract_findings:
            print(f"{finding.code}: {finding.path}: {finding.message}")
        print(f"metadata repository contracts: violations={len(contract_findings)}")
        return 1 if contract_findings else 0
    if args.mode == "check-contracts":
        try:
            contract_findings = validate_repository_contracts(root, profiles)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        for finding in contract_findings:
            print(f"{finding.code}: {finding.path}: {finding.message}")
        print(f"metadata repository contracts: violations={len(contract_findings)}")
        return 1 if contract_findings else 0
    transition_overrides: dict[tuple[str, str, str], TransitionOverride] = {}
    changed_selection: set[str] = set()
    if args.mode == "check-changed":
        try:
            if args.transition_override_file:
                transition_overrides = load_transition_overrides(
                    args.transition_override_file.resolve(),
                    root,
                    profiles,
                )
            changed_selection = _changed_paths(root, args.changed_path, base)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        if base.merge_base:
            print(
                f"metadata base: source={base.source} ref={base.ref} merge_base={base.merge_base}",
                file=sys.stderr,
            )
        else:
            print(
                "metadata base: fallback=working-tree-only; committed branch delta unavailable; full corpus not selected",
                file=sys.stderr,
            )
    elif args.transition_override_file:
        print(
            "configuration-error: --transition-override-file requires --mode check-changed",
            file=sys.stderr,
        )
        return 2
    base_records: list[Record] = []
    verified_task10_move_targets: set[str] = set()
    if base.merge_base:
        try:
            base_records = collect_records_at_ref(root, profiles, base.merge_base)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    base_records_by_path = {record.path.as_posix(): record for record in base_records}
    if args.mode == "check-changed" and base.merge_base:
        for path_text in sorted(changed_selection):
            if path_text in base_records_by_path:
                continue
            moved_record, _ = _task10_archive_moved_body_baseline(
                root,
                pathlib.Path(path_text),
                profiles,
                base.merge_base,
            )
            if moved_record is not None:
                base_records_by_path[path_text] = moved_record
                verified_task10_move_targets.add(path_text)
    try:
        records = collect_records(
            root,
            profiles,
            selected_paths=sorted(changed_selection),
            previous_records=base_records_by_path,
            require_git=args.mode == "check-changed",
        )
        manifest = (
            build_current_manifest(root, records)
            if registry is not None
            else build_manifest(records)
        )
    except ProfileError as error:
        print(f"configuration-error: {error}", file=sys.stderr)
        return 2
    native_findings: list[Finding] = []
    if registry is not None:
        try:
            native_findings.extend(_reference_delegation_findings(root, profiles))
            if args.mode == "check-changed":
                native_findings.extend(
                    _allocation_findings(root, profiles, records, args.base_ref)
                )
                stage = root / "docs/03.specs"
                packages = (
                    load_spec_packages(stage, registry=registry)
                    if stage.exists() or stage.is_symlink()
                    else ()
                )
                native_findings.extend(
                    Finding(item.path, item.code, item.message)
                    for item in validate_repository_spec_package_lifecycle(
                        root, packages, base_ref=args.base_ref
                    )
                )
        except (ProfileError, SpecPackageError) as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    base_manifest = build_manifest(base_records)
    base_findings_by_path = {
        path_text: validate_record(record, profiles, base_manifest)
        for path_text, record in base_records_by_path.items()
        if path_text in changed_selection
    }
    findings_by_path = {
        record.path.as_posix(): validate_record(
            record,
            profiles,
            manifest,
            transition_overrides=transition_overrides,
            migration_compaction_witness=(
                _native_migration_compaction_witness(root, record, base.merge_base)
                if args.mode == "check-changed"
                else None
            ),
            enforce_initial_status=args.mode == "check-changed",
        )
        for record in records
    }
    records_by_path = {record.path.as_posix(): record for record in records}
    changed_body_findings: dict[str, list[Finding]] = {}
    link_only_changes: set[str] = set()
    if args.mode == "check-changed":
        task5_move_sources = _task5_move_body_sources(root)
        for path_text in sorted(changed_selection):
            record = records_by_path.get(path_text)
            if record is None:
                continue
            try:
                current_text = (root / record.path).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                changed_body_findings[path_text] = [
                    _finding(
                        record,
                        "body-unreadable",
                        f"cannot read UTF-8 Markdown body: {error}",
                    )
                ]
                continue
            base_record = base_records_by_path.get(path_text)
            base_text = _text_at_ref(root, record.path, base.merge_base)
            if (
                base_text is not None
                and current_text != base_text
                and _link_target_neutral_text(current_text)
                == _link_target_neutral_text(base_text)
            ):
                link_only_changes.add(path_text)
            if base_record is None or base_text is None:
                moved_record, moved_text = _task10_archive_moved_body_baseline(
                    root,
                    record.path,
                    profiles,
                    base.merge_base,
                )
                base_record = moved_record or base_record
                base_text = moved_text or base_text
            if (
                base_text is not None
                and current_text != base_text
                and _link_target_neutral_text(current_text)
                == _link_target_neutral_text(base_text)
            ):
                link_only_changes.add(path_text)
            if base_record is None or base_text is None:
                moved_record, moved_text = _task5_moved_body_baseline(
                    root,
                    record.path,
                    profiles,
                    task5_move_sources,
                )
                base_record = moved_record or base_record
                base_text = moved_text or base_text
            changed_body_findings[path_text] = _introduced_body_findings(
                record,
                current_text,
                base_record,
                base_text,
                profiles,
            )
    relation_impact_findings: dict[str, list[Finding]] = {}
    if args.mode == "check-changed":
        try:
            head_records_by_path = collect_selected_records_at_ref(
                root,
                profiles,
                changed_selection,
                "HEAD",
            )
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        relation_impact_findings = _relation_impact_findings(
            changed_selection,
            records_by_path,
            head_records_by_path,
            base_records_by_path,
            manifest,
            findings_by_path,
        )
    parser_failures = [record for record in records if record.parse_error]
    rendered = render_report(records, profiles, findings_by_path)

    if args.mode == "report":
        if args.output:
            output = args.output if args.output.is_absolute() else root / args.output
            fresh = _write_or_check_output(output, rendered, args.check)
            if args.check and not fresh:
                print(f"metadata inventory is stale: {output}", file=sys.stderr)
                return 1
            action = "fresh" if args.check else "generated"
            print(
                f"metadata inventory {action}: records={len(records)} findings={sum(map(len, findings_by_path.values()))}"
            )
        else:
            sys.stdout.write(rendered)
        return 2 if parser_failures else 0

    directly_selected_paths = (
        changed_selection
        if args.mode == "check-changed"
        else {
            record.path.as_posix()
            for record in records
            if record.metadata.get("status") == "active"
        }
    )
    selected_paths = directly_selected_paths | set(relation_impact_findings)
    task5_legacy_parent_ids = _task5_legacy_parent_ids(root)
    legacy_exception_evidence = {
        path: evidence
        for path in selected_paths
        if path in records_by_path
        and (
            evidence := _legacy_exception_evidence(
                records_by_path[path],
                findings_by_path.get(path, []),
                base_records_by_path.get(path),
                base_findings_by_path.get(path, []),
                changed_body_findings.get(path, []),
                path in link_only_changes,
                task5_legacy_parent_ids,
                path in verified_task10_move_targets,
            )
        )
        is not None
    }
    legacy_exceptions = set(legacy_exception_evidence)
    for path, (current_count, base_count) in sorted(legacy_exception_evidence.items()):
        print(
            f"{path}: legacy metadata exception: base-existing deficits preserved by an approved structural migration; "
            f"current_deficits={current_count} base_deficits={base_count} new_deficits=0",
            file=sys.stderr,
        )
    selected_findings = sorted(
        set(native_findings)
        | {
            finding
            for path in directly_selected_paths - legacy_exceptions
            for finding in findings_by_path.get(path, [])
            if finding.severity == "error"
        }
        | {
            finding
            for path, findings in relation_impact_findings.items()
            if path not in legacy_exceptions
            for finding in findings
        }
        | {
            finding
            for path, findings in changed_body_findings.items()
            if path not in legacy_exceptions
            for finding in findings
            if finding.severity == "error"
        }
    )
    for finding in selected_findings:
        print(f"{finding.path}: {finding.code}: {finding.message}")
    print(
        f"metadata {args.mode}: selected={len(selected_paths)} violations={len(selected_findings)} "
        f"legacy_exceptions={len(legacy_exceptions)} transition_overrides={len(transition_overrides)}"
    )
    return 1 if selected_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
