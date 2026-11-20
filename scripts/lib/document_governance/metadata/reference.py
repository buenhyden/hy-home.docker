"""Repository-wide metadata references, reports, and CLI orchestration."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import hashlib
import pathlib
import posixpath
import re
import stat
import sys
from collections.abc import Mapping, Sequence
from datetime import date
from types import MappingProxyType

from scripts.lib.document_governance.architecture import (
    ArchitectureDocumentError,
    load_architecture_documents,
)
from scripts.lib.document_governance.frontmatter import (
    FrontmatterError,
)
from scripts.lib.document_governance.frontmatter import (
    parse_frontmatter_text as _parse_frontmatter_text,
)
from scripts.lib.document_governance.identity_history import (
    IdentityHistoryError,
    collect_issued_identities,
    validate_identity_history,
)
from scripts.lib.document_governance.links import document_controls_changed
from scripts.lib.document_governance.metadata.heading import (
    _common_document_view,
    _introduced_body_findings,
    _machine_template_findings,
    _runtime_version_findings,
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
    _governance_moved_body_baseline,
    _numbered_folder_moved_baseline,
    _operations_moved_body_baseline,
    _record_from_text,
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
    registered_generated_owner,
)
from scripts.lib.document_governance.metadata.version import (
    product_version_findings,
    version_change_findings,
)
from scripts.lib.document_governance.operations_catalog import (
    OperationsAuthorityError,
    read_bounded_regular,
)
from scripts.lib.document_governance.registry import (
    DEFAULT_FRONTMATTER_SCHEMA,
    DocumentRegistry,
    FrontmatterValidator,
    RegistryError,
    _declares_provider_binding,
    document_type,
    load_registry,
    load_registry_at_revision,
    load_registry_document_at_revision,
    load_trusted_requirement_allocation_baseline,
    normalize_profile_frontmatter,
    resolve_template_placeholders,
)
from scripts.lib.document_governance.registry import (
    classify_path as classify_registered_path,
)
from scripts.lib.document_governance.requirements import (
    RequirementPackageError,
    load_requirement_packages,
)
from scripts.lib.document_governance.spec_packages import (
    MAX_SPEC_FILE_BYTES,
    HistoricalSpecSnapshotContext,
    SpecPackageError,
    _bounded_git,
    load_spec_packages,
    resolve_lifecycle_base,
    validate_repository_spec_package_lifecycle_details,
)

_MARKDOWN_LINK_TARGET = re.compile(r"\]\(([^)\s]+)\)")


@dataclasses.dataclass(frozen=True)
class _GenerationBindings:
    """Exact unchanged state recovered from an approved generation source."""

    revision: str | None = None
    unchanged_statuses: Mapping[str, str] = dataclasses.field(
        default_factory=lambda: MappingProxyType({})
    )
    frozen_terminal_tasks: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "unchanged_statuses",
            MappingProxyType(dict(self.unchanged_statuses)),
        )
        object.__setattr__(
            self, "frozen_terminal_tasks", frozenset(self.frozen_terminal_tasks)
        )


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
            # A package is listed by its directory as well as by its member
            # file, so a folder router need not reach inside the package.
            package = posixpath.dirname(member)
            if member not in listed and package not in listed:
                findings.append(
                    Finding(
                        index_path,
                        "index-member-unlisted",
                        f"registered {member_profile} is absent from its index: {member}",
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


def _registered_generation_normalization(
    profile: Mapping[str, object] | None,
    source_status: object,
    current_status: object,
    registered: frozenset[tuple[object, object, object]],
) -> bool:
    if not isinstance(profile, Mapping):
        return False
    lifecycle_id = profile.get("lifecycle_id")
    return (lifecycle_id, source_status, current_status) in registered and (
        lifecycle_id != "navigation" or profile.get("identity_relation") == "none"
    )


def _source_blob_matches_worktree(
    root: pathlib.Path,
    path: pathlib.Path,
    revision: str | None,
    *,
    source_blob: bytes | None = None,
) -> bool:
    """Return whether a generation blob exactly matches current file bytes."""

    if revision is None:
        return False
    try:
        if source_blob is not None:
            return len(
                source_blob
            ) <= MAX_SPEC_FILE_BYTES and source_blob == read_bounded_regular(
                root,
                pathlib.PurePosixPath(path.as_posix()),
                max_bytes=MAX_SPEC_FILE_BYTES,
            )
        listing = _bounded_git(
            root,
            "ls-tree",
            "-z",
            revision,
            "--",
            path.as_posix(),
            byte_limit=512,
        )
        rows = tuple(row for row in listing.split(b"\0") if row)
        if len(rows) != 1:
            return False
        metadata, raw_path = rows[0].split(b"\t", 1)
        mode, object_type, raw_object_id = metadata.split(b" ", 2)
        if (
            mode not in {b"100644", b"100755"}
            or object_type != b"blob"
            or raw_path.decode("utf-8") != path.as_posix()
        ):
            return False
        object_id = raw_object_id.decode("ascii")
        size_text = (
            _bounded_git(
                root,
                "cat-file",
                "-s",
                object_id,
                byte_limit=64,
            )
            .decode("ascii")
            .strip()
        )
        if not size_text.isdigit():
            return False
        source_size = int(size_text)
        if source_size > MAX_SPEC_FILE_BYTES:
            return False
        current = read_bounded_regular(
            root,
            pathlib.PurePosixPath(path.as_posix()),
            max_bytes=MAX_SPEC_FILE_BYTES,
        )
        if len(current) != source_size:
            return False
        source = _bounded_git(
            root,
            "cat-file",
            "blob",
            object_id,
            byte_limit=MAX_SPEC_FILE_BYTES,
        )
    except (
        OSError,
        OperationsAuthorityError,
        SpecPackageError,
        UnicodeError,
        ValueError,
    ):
        return False
    return len(source) == source_size and source == current


def _generation_task_body_baseline(
    root: pathlib.Path,
    record: Record,
    current_text: str,
    profiles: dict[str, object],
    bindings: _GenerationBindings,
) -> tuple[Record | None, str | None]:
    """Return an exact terminal Task blob from the validated generation source."""

    path = record.path.as_posix()
    if bindings.revision is None or path not in bindings.frozen_terminal_tasks:
        return None, None
    if not _source_blob_matches_worktree(root, record.path, bindings.revision):
        return None, None
    source_text = _text_at_ref(root, record.path, bindings.revision)
    if source_text is None or source_text != current_text:
        return None, None
    return (
        _record_from_text(
            record.path,
            source_text,
            previous_status=bindings.unchanged_statuses.get(path),
            profiles=profiles,
        ),
        source_text,
    )


def _role_design_findings(
    root: pathlib.Path, profiles: Mapping[str, object]
) -> list[Finding]:
    """Check the pinned role design core and every template role's binding."""

    from scripts.lib.document_governance.template_definition import (
        role_design_contract_findings,
    )

    registry = profiles["_registry"]
    assert isinstance(registry, DocumentRegistry)
    return _common_core_findings(root, registry) + [
        Finding(location, code, message)
        for code, location, message in role_design_contract_findings(
            registry, root=root
        )
    ]


_COMMON_DOCUMENT_MAX_BYTES = 256 * 1024


def _common_definition_findings(
    root, registry, template_id, role, core
) -> list[Finding]:
    """Check the real Markdown definition, independently of native output."""
    from scripts.lib.document_governance.common_document import _headings

    source = str(role.get("source", ""))
    try:
        text = read_bounded_regular(
            root, pathlib.PurePosixPath(source), max_bytes=_COMMON_DOCUMENT_MAX_BYTES
        ).decode("utf-8")
    except (OSError, OperationsAuthorityError, UnicodeError) as error:
        return [Finding(source, "document-core-definition-unreadable", str(error))]
    findings: list[Finding] = []
    try:
        metadata = _parse_frontmatter_text(text)
    except FrontmatterError:
        metadata = {}
    output_types = {
        registry.profiles[name].get("type")
        for name in role["profiles"]
        if name in registry.profiles
    }
    descriptor = metadata.get("type") == "common/template-source"
    if (
        pathlib.PurePosixPath(source).suffix != ".md"
        or (not descriptor and metadata.get("type") not in output_types)
        or (descriptor and metadata.get("template_id") != template_id)
        or metadata.get("template_id", template_id) != template_id
    ):
        findings.append(
            Finding(source, "document-core-definition-binding", template_id)
        )
    expected = [
        pair
        for parent, children in core["headings"].items()
        for pair in [(2, parent), *((3, child) for child in children)]
    ]
    headings = _headings(text)
    if (
        core["payload_encoding"]["marker"] not in text
        or sum(level == 1 for _, level, _ in headings) != 1
        or [(level, title) for _, level, title in headings if level in (2, 3)]
        != expected
    ):
        findings.append(
            Finding(source, "document-core-definition-envelope", template_id)
        )
    return findings


def _common_native_findings(root, registry, template_id, role) -> list[Finding]:
    """A native payload is a separate, owned regular source, never its definition."""
    exception = role.get("core_exception", {})
    required = isinstance(exception, Mapping) and exception.get("kind") == "native"
    native = role.get("native_source")
    if native is None and not required:
        return []
    try:
        if (
            not isinstance(native, str)
            or not pathlib.PurePosixPath(native).is_relative_to(
                "docs/99.templates/02.templates"
            )
            or any(
                native == item.get("source")
                for item in registry.template_roles.values()
            )
            or sum(
                native == item.get("native_source")
                for item in registry.template_roles.values()
            )
            != 1
            or classify_registered_path(native, registry)
            not in {None, "template-source", *role["profiles"]}
        ):
            raise ValueError("native payload must be distinct and owned by this role")
        if not read_bounded_regular(
            root, pathlib.PurePosixPath(native), max_bytes=_COMMON_DOCUMENT_MAX_BYTES
        ):
            raise ValueError("native payload is empty")
    except (OSError, OperationsAuthorityError, ValueError) as error:
        return [Finding(template_id, "document-core-native-binding", str(error))]
    return []


def _common_core_findings(
    root: pathlib.Path, registry: DocumentRegistry
) -> list[Finding]:
    """Validate the actual pinned common core and complete explicit bindings."""
    from scripts.lib.document_governance.common_document import (
        CORE_PATH,
        CommonDocumentError,
        _decode_contract,
    )

    binding = registry.common.get("document_core")
    if not isinstance(binding, Mapping):
        return [Finding("common", "document-core-binding-missing", "document_core")]
    source = binding.get("source_path")
    if source != CORE_PATH:
        return [Finding("common", "document-core-identity", "unexpected common source")]
    try:
        raw = read_bounded_regular(
            root, pathlib.PurePosixPath(source), max_bytes=_COMMON_DOCUMENT_MAX_BYTES
        )
    except (OSError, OperationsAuthorityError) as error:
        return [Finding(source, "document-core-source-unreadable", str(error))]
    if hashlib.sha256(raw).hexdigest() != binding.get("source_sha256"):
        return [
            Finding(
                source, "document-core-source-changed", "sha256 differs from Registry"
            )
        ]
    try:
        core = _decode_contract(raw)
    except (CommonDocumentError, KeyError, TypeError) as error:
        return [Finding(source, "document-core-source-invalid", str(error))]
    if (core.get("contract_id"), core.get("version")) != (
        binding.get("contract_id"),
        binding.get("contract_version"),
    ):
        return [Finding(source, "document-core-identity", "id or version differs")]
    if (
        not core["headings"]
        or not core["payload_profiles"]
        or core["payload_encoding"].get("marker")
        != f"<!-- document-core: {core['contract_id']}/{core['version']} -->"
        or any(
            not isinstance(payload, Mapping)
            or not isinstance(payload.get("required_content"), (tuple, list))
            or not payload["required_content"]
            or any(
                not isinstance(item, str) or not item.strip()
                for item in payload["required_content"]
            )
            or any(
                not isinstance(payload.get(key), str) or not payload[key].strip()
                for key in ("placement", "rule")
            )
            for payload in core["payload_profiles"].values()
        )
    ):
        return [
            Finding(
                source,
                "document-core-source-invalid",
                "incomplete envelope or payload profile",
            )
        ]
    profiles = binding.get("profile_bindings", {})
    expected = {
        name
        for name, profile in registry.profiles.items()
        if profile.get("template_id") is not None
    }
    findings: list[Finding] = []
    if not isinstance(profiles, Mapping) or set(profiles) != expected:
        findings.append(
            Finding(
                source,
                "document-core-profile-binding",
                "output profile coverage differs",
            )
        )
    if not isinstance(profiles, Mapping):
        return findings
    for name, profile in profiles.items():
        if (
            not isinstance(profile, Mapping)
            or profile.get("kind") not in core["payload_profiles"]
        ):
            findings.append(
                Finding(
                    str(name), "document-core-profile-binding", "unknown payload kind"
                )
            )
    for path, override in binding.get("path_bindings", {}).items():
        if (
            classify_registered_path(path, registry) not in expected
            or not isinstance(override, Mapping)
            or ("kind" in override and override["kind"] not in core["payload_profiles"])
        ):
            findings.append(
                Finding(
                    path,
                    "document-core-profile-binding",
                    "unknown path override or payload kind",
                )
            )
    for template_id, role in registry.template_roles.items():
        role_profiles = role["profiles"]
        kinds = {
            profiles[name].get("kind")
            for name in role_profiles
            if isinstance(profiles.get(name), Mapping)
        }
        if len(kinds) != 1 or any(
            name not in expected
            or registry.profiles[name].get("template_id") != template_id
            for name in role_profiles
        ):
            findings.append(
                Finding(
                    template_id,
                    "document-core-profile-binding",
                    "role and output profile bindings differ",
                )
            )
        findings.extend(
            _common_definition_findings(root, registry, template_id, role, core)
        )
        findings.extend(_common_native_findings(root, registry, template_id, role))
    return findings


def _workspace_inventory_findings() -> list[Finding]:
    # Only the Registry-owned _workspace READMEs are metadata targets; the
    # staging tree itself never becomes an inferred inventory root.
    if (
        any(prefix.startswith("_workspace/") for prefix in TARGET_MARKDOWN_PREFIXES)
        or _normalized_target_path("_workspace/diagnostics/notes.md") is not None
    ):
        return [
            Finding(
                "scripts/validation/check-document-metadata.py",
                "workspace-inventory-coupling",
                "_workspace must remain outside docs metadata inventory inference",
            )
        ]
    return []


def _validate_repository_contracts(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    base_ref: str | None = None,
    transition_ref: str | None = None,
    previous_records: Mapping[str, Record] | None = None,
    current_records: Mapping[str, Record] | None = None,
    frontmatter_validator: FrontmatterValidator | None = None,
    validation_paths: set[str] | None = None,
    transition_overrides: Mapping[tuple[str, str, str], TransitionOverride]
    | None = None,
) -> tuple[
    list[Finding],
    frozenset[tuple[str, str, str]],
    frozenset[tuple[str, str, str]],
    _GenerationBindings,
]:
    """Validate tracked repository surfaces backed by the canonical registry.

    `transition_ref` names the committed state the working tree is compared
    against for lifecycle transitions. Without it every record carries no
    predecessor status, so `invalid-transition` cannot fire and the rule is
    declared but unreachable in this route.
    """

    _require_git_worktree(root)
    findings: list[Finding] = []
    actual_lifecycle_transitions: frozenset[tuple[str, str, str]] = frozenset()
    actual_lifecycle_normalizations: set[tuple[str, str, str]] = set()
    actual_lifecycle_normalization_sources: dict[str, str] = {}
    generation_revision: str | None = None
    unchanged_generation_statuses: dict[str, str] = {}
    frozen_terminal_tasks: set[str] = set()
    tracked_markdown = _tracked_repository_markdown(root)
    registry_native = isinstance(profiles.get("_registry"), DocumentRegistry)

    if registry_native:
        frontmatter_validator = frontmatter_validator or FrontmatterValidator()
        active_registry = profiles.get("_registry")
        assert isinstance(active_registry, DocumentRegistry)
        findings.extend(_reference_delegation_findings(root, profiles))
        # Changed-mode callers already parsed this exact predecessor corpus.
        previous_records = (
            previous_records
            if previous_records is not None
            else (
                {
                    record.path.as_posix(): record
                    for record in collect_records_at_ref(root, profiles, transition_ref)
                }
                if transition_ref is not None
                else None
            )
        )
        records = collect_records(
            root,
            profiles,
            selected_paths=sorted(
                validation_paths
                if validation_paths is not None
                else _changed_paths(root, (), BaseSelection("worktree", None, None))
            ),
            previous_records=previous_records,
            require_git=True,
            current_records=current_records,
        )
        manifest = build_current_manifest(root, records)
        findings.extend(_index_membership_findings(root, active_registry, records))
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
        # Current Stage 03 alone decides whether Spec Package validation runs;
        # no Stage 98 record gates it (SPEC-0248).
        if spec_root.exists() or spec_root.is_symlink():
            try:
                historical_context = HistoricalSpecSnapshotContext()
                spec_packages = load_spec_packages(
                    spec_root,
                    registry=active_registry,
                    _historical_context=historical_context,
                )
                spec_lifecycle = validate_repository_spec_package_lifecycle_details(
                    root,
                    spec_packages,
                    base_ref=base_ref,
                    registry=active_registry,
                    _historical_context=historical_context,
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
                actual_lifecycle_transitions = spec_lifecycle.actual_transitions
                actual_lifecycle_normalizations.update(
                    spec_lifecycle.actual_normalizations
                )
                if spec_lifecycle.generation_source is not None:
                    generation_revision = spec_lifecycle.generation_source
                    migration_contract = active_registry.common.get(
                        "task_lifecycle_events", {}
                    )
                    migration = (
                        migration_contract.get("migration", {})
                        if isinstance(migration_contract, Mapping)
                        else {}
                    )
                    registered_normalizations = frozenset(
                        (
                            item.get("lifecycle_id"),
                            item.get("from_status"),
                            item.get("to_status"),
                        )
                        for item in migration.get("normalizations", ())
                        if isinstance(item, Mapping)
                    )
                    source_registry = load_registry_document_at_revision(
                        spec_lifecycle.generation_source,
                        root=root,
                    )
                    source_registry_contract = load_registry_at_revision(
                        spec_lifecycle.generation_source,
                        root=root,
                    )
                    source_profiles = source_registry.get("profiles")
                    source_lifecycles = source_registry.get("lifecycles")
                    source_profiles_by_id = (
                        {
                            profile.get("id"): profile
                            for profile in source_profiles
                            if isinstance(profile, Mapping)
                        }
                        if isinstance(source_profiles, list)
                        else {}
                    )
                    source_blobs: dict[str, bytes] = {}
                    source_records = collect_selected_records_at_ref(
                        root,
                        profiles,
                        [record.path.as_posix() for record in records],
                        spec_lifecycle.generation_source,
                        raw_blobs=source_blobs,
                    )
                    for record in records:
                        source = source_records.get(record.path.as_posix())
                        if source is None:
                            continue
                        current_profile = active_registry.profiles.get(
                            record.artifact_type
                        )
                        source_status = source.metadata.get("status")
                        current_status = record.metadata.get("status")
                        source_profile = source_profiles_by_id.get(record.artifact_type)
                        source_lifecycle_id = (
                            source_profile.get("lifecycle_id")
                            if isinstance(source_profile, Mapping)
                            else None
                        )
                        source_lifecycle = (
                            source_lifecycles.get(source_lifecycle_id)
                            if isinstance(source_lifecycles, Mapping)
                            and isinstance(source_lifecycle_id, str)
                            else None
                        )
                        current_lifecycle_id = (
                            current_profile.get("lifecycle_id")
                            if isinstance(current_profile, Mapping)
                            else None
                        )
                        current_statuses = active_registry.lifecycles.get(
                            str(current_lifecycle_id), ()
                        )
                        current_identity = record.metadata.get("artifact_id")
                        source_identity = source.metadata.get("artifact_id")
                        identity_is_bound = (
                            source.artifact_type == record.artifact_type
                            and (
                                (
                                    isinstance(current_identity, str)
                                    and source_identity == current_identity
                                )
                                or (
                                    current_identity is None
                                    and source_identity is None
                                    and isinstance(current_profile, Mapping)
                                    and current_profile.get("identity_relation")
                                    == "none"
                                )
                            )
                        )
                        if (
                            identity_is_bound
                            and isinstance(source_status, str)
                            and source_status == current_status
                            and isinstance(source_lifecycle, Mapping)
                            and source_status in source_lifecycle.get("statuses", ())
                            and current_status in current_statuses
                        ):
                            unchanged_generation_statuses[record.path.as_posix()] = (
                                source_status
                            )
                        source_profile_contract = source_registry_contract.profiles.get(
                            record.artifact_type
                        )
                        source_lifecycle_contract = (
                            source_profile_contract.get("lifecycle_id")
                            if isinstance(source_profile_contract, Mapping)
                            else None
                        )
                        if (
                            identity_is_bound
                            and record.artifact_type == "task"
                            and isinstance(source_status, str)
                            and source_status == current_status
                            and source_status
                            in source_registry_contract.lifecycle_terminal_statuses.get(
                                str(source_lifecycle_contract), ()
                            )
                        ):
                            if _source_blob_matches_worktree(
                                root,
                                record.path,
                                spec_lifecycle.generation_source,
                                source_blob=source_blobs.get(record.path.as_posix()),
                            ):
                                frozen_terminal_tasks.add(record.path.as_posix())
                        normalization = (
                            record.path.as_posix(),
                            source_status,
                            current_status,
                        )
                        if normalization in actual_lifecycle_normalizations:
                            actual_lifecycle_normalization_sources[
                                record.path.as_posix()
                            ] = source_status
                        if (
                            source.artifact_type == record.artifact_type
                            and source.metadata.get("artifact_id")
                            == record.metadata.get("artifact_id")
                            and source_status != current_status
                            and isinstance(source_lifecycle, Mapping)
                            and source_status in source_lifecycle.get("statuses", ())
                            and current_status in current_statuses
                            and _registered_generation_normalization(
                                current_profile,
                                source_status,
                                current_status,
                                registered_normalizations,
                            )
                        ):
                            actual_lifecycle_normalization_sources[
                                record.path.as_posix()
                            ] = source_status
                            actual_lifecycle_normalizations.add(normalization)
                findings.extend(
                    Finding(finding.path, finding.code, finding.message)
                    for finding in spec_lifecycle.findings
                )
        for record in records:
            if (
                validation_paths is not None
                and record.path.as_posix() not in validation_paths
            ):
                continue
            # Template sources keep their own route because their placeholders
            # are correct for a template and invalid for an authored document.
            findings.extend(
                finding
                for finding in validate_record(
                    record,
                    profiles,
                    manifest,
                    transition_overrides=transition_overrides,
                    actual_lifecycle_transitions=actual_lifecycle_transitions,
                    actual_lifecycle_normalizations=frozenset(
                        actual_lifecycle_normalizations
                    ),
                    actual_lifecycle_normalization_sources=(
                        actual_lifecycle_normalization_sources
                    ),
                    unchanged_generation_statuses=unchanged_generation_statuses,
                    enforce_initial_status=validation_paths is not None
                    or transition_ref is not None,
                    frontmatter_validator=frontmatter_validator,
                )
                if finding.severity == "error"
            )

    findings.extend(_workspace_inventory_findings())
    if registry_native:
        findings.extend(_role_design_findings(root, profiles))

    readme_registry = profiles.get("_registry") if registry_native else None
    for path in tracked_markdown:
        if validation_paths is not None and path.as_posix() not in validation_paths:
            continue
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
            from scripts.lib.document_governance.common_document import (
                CommonDocumentError,
                payload_text,
            )

            try:
                _, h2 = extract_markdown_headings(payload_text(text))
            except CommonDocumentError as error:
                findings.append(
                    Finding(path.as_posix(), "readme-envelope-invalid", str(error))
                )
                continue
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
            if path.as_posix().startswith("docs/99.templates/02.templates/")
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

    return (
        sorted(set(findings)),
        actual_lifecycle_transitions,
        frozenset(actual_lifecycle_normalizations),
        _GenerationBindings(
            generation_revision,
            MappingProxyType(dict(unchanged_generation_statuses)),
            frozenset(frozen_terminal_tasks),
        ),
    )


def validate_repository_contracts(
    root: pathlib.Path,
    profiles: dict[str, object],
    *,
    base_ref: str | None = None,
    transition_ref: str | None = None,
    frontmatter_validator: FrontmatterValidator | None = None,
) -> list[Finding]:
    """Validate repository contracts while keeping transition details internal."""

    findings, _, _, _ = _validate_repository_contracts(
        root,
        profiles,
        base_ref=base_ref,
        transition_ref=transition_ref,
        frontmatter_validator=frontmatter_validator,
    )
    return findings


def _metadata_validation_paths(
    changed: set[str],
    current: Mapping[str, Record],
    previous: Mapping[str, Record],
) -> set[str]:
    """Keep complete identity indexes while validating only changed consumers."""

    if document_controls_changed(changed):
        return set(current)
    by_id: dict[str, set[str]] = collections.defaultdict(set)
    consumers: dict[str, set[str]] = collections.defaultdict(set)
    for path, record in current.items():
        artifact_id = record.metadata.get("artifact_id")
        if isinstance(artifact_id, str):
            by_id[artifact_id].add(path)
        for field in ("parent_ids", "supersedes"):
            for target in _string_list(record.metadata.get(field)) or ():
                consumers[target].add(path)
    selected = set(changed)
    queue = collections.deque(changed)
    while queue:
        path = queue.popleft()
        identities = {
            value
            for records in (current, previous)
            if (record := records.get(path)) is not None
            and isinstance(value := record.metadata.get("artifact_id"), str)
        }
        for identity in identities:
            for dependent in by_id[identity] | consumers[identity]:
                if dependent not in selected:
                    selected.add(dependent)
                    queue.append(dependent)
    return selected


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
    required, _optional, forbidden = _profile_sets(profile)
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
    required, _optional, forbidden = _profile_sets(profile)
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
    """Render the current advisory inventory with its actual observation date."""

    from scripts.lib.document_governance.common_document import wrap_document

    _, profile_map = _profile_mapping(profiles)
    observed_on = date.today().isoformat()
    profile_counts = collections.Counter(record.artifact_type for record in records)
    finding_counts = collections.Counter(
        finding.code for findings in findings_by_path.values() for finding in findings
    )
    semantic_count = sum(1 for findings in findings_by_path.values() if findings)
    parse_count = sum(1 for record in records if record.parse_error)
    lines = [
        "---",
        'title: "Reference: Frontmatter Semantic Inventory"',
        'version: "2.0.0"',
        'type: "reference/audit-pack"',
        'status: "published"',
        'owner: "@buenhyden"',
        "document_scope:",
        '  subject: "hy-home.docker"',
        '  layer: "reference"',
        f'updated: "{observed_on}"',
        'layer: "references"',
        'artifact_id: "AUD-0023"',
        'created: "2026-07-05"',
        f'observed_at: "{observed_on}"',
        "generated_by: scripts/validation/check-document-metadata.py",
        "---",
        "",
        "# Reference: Frontmatter Semantic Inventory",
        "",
        "## Responsibility",
        "",
        "### Purpose",
        "",
        "이 참고 보고서는 추적 중인 문서와 선별한 새 문서를 조사합니다.",
        "대상은 관리되는 문서 단계와 거버넌스·템플릿의 Markdown이며 자기 자신은 제외합니다.",
        "본문·비밀값·원시 로그를 출력하지 않고 profile과 메타데이터 발견 사항만 기록합니다.",
        "원래 관측은 Spec 123의 Task 7·8을 지원했으며, 이번 재생성은 현재 작업 상태를 측정합니다.",
        "",
        "#### Repository Role",
        "",
        "현행 메타데이터 정책은 `.agents/governance`와 Stage 99가 소유합니다. 이 Stage 90 보고서는",
        "생성된 근거이며 `check-document-metadata.py`로 다시 관측합니다.",
        "",
        "#### In Scope",
        "",
        "- 관리되는 Markdown 경로, 추론한 profile, 안전한 frontmatter 해석 상태와 발견 코드",
        "- 식별자·부모·수명주기·최신성 및 README·생성물·거버넌스·템플릿·보존 profile",
        "",
        "### Excluded Responsibilities",
        "",
        "- 문서 자동 수정, 전체 문서 차단 또는 수명주기 변경은 수행하지 않습니다.",
        "- 파일 수정 시각을 문서 최신성의 근거로 사용하지 않습니다.",
        "- 원시 본문·로그·자격 증명·비밀값은 포함하지 않습니다.",
        "",
        "## Current Contents",
        "",
        "### Paths",
        "",
        "이 생성 보고서는 단일 파일이며 하위 문서를 나열하지 않습니다.",
        "",
        "| Path | Purpose |",
        "| --- | --- |",
        "",
        "### Owners",
        "",
        "- **소유자**: 메타데이터 프로그램 담당자 / rules-engineer",
        "",
        "## Usage",
        "",
        "### Entry Points",
        "",
        "- [Document Registry](../../../99.templates/registry.json) - 메타데이터 소유권과 예외 규칙",
        "- [Template governance](../../../99.templates/README.md) - 수명주기 용어와 전이",
        "- [Semantic audit](../0024-frontmatter-template-readme-implementation/README.md) - 수정 전의 과거 기준과 관측",
        "- [Audit pack README](./README.md)",
        "- [Frontmatter/template/README audit](../0024-frontmatter-template-readme-implementation/README.md)",
        "- [SDLC and document-contract audit](../0029-sdlc-document-contracts-implementation/README.md)",
        "",
        "### Checks",
        "",
        "#### Criteria",
        "",
        "Stage 99 Registry의 profile·식별자·관계·수명주기·최신성 계약을 적용합니다.",
        "과거 발견 사항은 이 보고서에서 참고 근거로 남습니다. 별도의 변경·신규 검사는",
        "안전하게 선택한 차이 범위만 집행합니다.",
        "",
        "#### Evidence",
        "",
        f"- **현재 기록**: {len(records)}",
        f"- **발견 사항이 있는 기록**: {semantic_count}",
        f"- **Frontmatter 해석 실패**: {parse_count}",
        "- **집행 상태**: 전체 목록은 참고용이며 변경·신규 선택 범위는 차단 검사 대상입니다.",
        "",
        "#### Profile Summary",
        "",
        "| Profile | Records |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{name}` | {count} |" for name, count in sorted(profile_counts.items())
    )
    lines.extend(
        [
            "",
            "#### Findings",
            "",
            "##### Finding Summary",
            "",
            "| Finding | Count |",
            "| --- | ---: |",
        ]
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
            "#### Inventory",
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
            "#### Source Rules",
            "",
            "- 경로는 관리 루트로 제한한 Git 추적·변경·신규 Markdown 탐색에서 가져오며 무시된 파일은 제외합니다. Git이 없는 시험 입력은 정렬된 재귀 탐색을 사용합니다.",
            "- YAML은 PyYAML `safe_load` 동작에 중복 키 거부를 추가해 해석합니다.",
            "- 각 행은 해석·식별자·관계·수명주기·전이 근거·최신성·예외 의미를 기록하며 확인할 수 없는 이력은 추정하지 않습니다.",
            "- 보고서는 제한된 메타데이터 상태, 안전한 저장소 경로, 집계와 발견 코드만 표시합니다.",
            "- Graphify는 탐색 참고이며 목록의 증거로 사용하지 않습니다.",
            "",
            "#### Conformance",
            "",
            f"발견 사항이 있는 기록은 {semantic_count}개, 해석 실패는 {parse_count}개입니다. 이 집계는 정적 문서 검사 결과이며 실행이나 provider runtime 적합성을 증명하지 않습니다.",
            "별도의 공식 검사는 선택 범위의 결과를 제공하며, 실제 인수 결정은 해당 권한자가 기록합니다.",
            "",
            "#### Actions",
            "",
            "- **검토 주기**: 추적 Markdown이나 메타데이터 profile이 바뀌면 다시 관측합니다.",
            "- **갱신 조건**: profile·파서·수명주기·관계·예외·문서 집합의 변경",
            "",
        ]
    )
    return wrap_document("\n".join(lines), kind="reference-pack")


def _managed_document_change(path: str) -> str | None:
    normalized = _normalized_target_path(path)
    if normalized is not None:
        return normalized.as_posix()
    return path if document_controls_changed((path,)) else None


def _changed_paths(
    root: pathlib.Path,
    explicit: Sequence[str],
    base: BaseSelection,
) -> set[str]:
    changed: set[str] = set()
    commands = [
        (
            "unstaged document/control discovery",
            ["diff", "--name-only", "-z", "--no-renames", "--diff-filter=ACDMRT"],
        ),
        (
            "staged document/control discovery",
            [
                "diff",
                "--cached",
                "--name-only",
                "-z",
                "--no-renames",
                "--diff-filter=ACDMRT",
            ],
        ),
        (
            "untracked document/control discovery",
            ["ls-files", "-z", "--others", "--exclude-standard"],
        ),
    ]
    if base.merge_base:
        commands.insert(
            0,
            (
                "committed branch document/control discovery",
                [
                    "diff",
                    "--name-only",
                    "-z",
                    "--no-renames",
                    "--diff-filter=ACDMRT",
                    f"{base.merge_base}...HEAD",
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
            normalized
            for path in _decode_git_paths(result.stdout, operation)
            if (normalized := _managed_document_change(path.as_posix())) is not None
        )
    if explicit:
        return {
            normalized
            for path in explicit
            if (normalized := _managed_document_change(path)) is not None
        } | {path for path in changed if document_controls_changed((path,))}
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
        dest="profiles",
        type=pathlib.Path,
        default=DEFAULT_PROFILES,
        help="Stage 99 registry",
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
                load_architecture_documents(architecture_root, registry=registry)
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
    profiles = {**profiles, "_runtime_root": root}
    frontmatter_validator = FrontmatterValidator()
    if args.mode == "check-contracts" and args.profiles.suffix.lower() == ".json":
        assert registry is not None
        contract_findings: list[Finding] = []
        template_schema = (
            root / "docs/99.templates/01.contracts/document-frontmatter.schema.json"
        )
        template_validator = (
            frontmatter_validator
            if template_schema == DEFAULT_FRONTMATTER_SCHEMA
            else FrontmatterValidator(template_schema)
        )
        for role, definition in registry.template_roles.items():
            source = definition.get("native_source", definition.get("source"))
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
                    values = normalize_profile_frontmatter(
                        _parse_frontmatter_text(text), profile
                    )
                except (FrontmatterError, RegistryError):
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
                    schema_findings = template_validator(schema_values)
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
                from scripts.lib.document_governance.common_document import payload_text

                h1, h2 = extract_markdown_headings(payload_text(text))
                if len(h1) != 1 and not provider_owned:
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
                    frontmatter_validator=frontmatter_validator,
                )
            )
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
        if args.history_scope == "full":
            try:
                # HEAD-reachable history: another branch's unmerged allocation
                # surfaces as a Registry merge conflict, not as a finding here.
                issued = collect_issued_identities(root, refs=("HEAD",))
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
    elif args.mode in {"report", "check-active"} and (root / ".git").exists():
        try:
            changed_selection = _changed_paths(root, (), base)
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    base_records: list[Record] = []
    base_texts: dict[str, str] = {}
    if base.merge_base:
        try:
            base_records = collect_records_at_ref(
                root,
                profiles,
                base.merge_base,
                texts_by_path=base_texts if args.mode == "check-changed" else None,
            )
        except ProfileError as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    base_records_by_path = {record.path.as_posix(): record for record in base_records}
    governance_move_texts: dict[str, str] = {}
    if args.mode == "check-changed" and base.merge_base:
        for path_text in sorted(changed_selection):
            if path_text in base_records_by_path:
                continue
            operations_record, operations_text = _operations_moved_body_baseline(
                root, pathlib.Path(path_text), profiles, base_records, base.merge_base
            )
            if operations_record is not None and operations_text is not None:
                base_records_by_path[path_text] = operations_record
                governance_move_texts[path_text] = operations_text
                continue
            governance_record, governance_text = _governance_moved_body_baseline(
                root, pathlib.Path(path_text), profiles, base.merge_base
            )
            if governance_record is not None and governance_text is not None:
                base_records_by_path[path_text] = governance_record
                governance_move_texts[path_text] = governance_text
                continue
            numbered_record, numbered_text = _numbered_folder_moved_baseline(
                root, pathlib.Path(path_text), profiles, base.merge_base
            )
            if numbered_record is not None and numbered_text is not None:
                base_records_by_path[path_text] = numbered_record
                governance_move_texts[path_text] = numbered_text
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
    records_by_path = {record.path.as_posix(): record for record in records}
    validation_paths = (
        _metadata_validation_paths(
            changed_selection, records_by_path, base_records_by_path
        )
        if args.mode == "check-changed"
        else set(records_by_path)
    )
    actual_lifecycle_transitions: frozenset[tuple[str, str, str]] = frozenset()
    actual_lifecycle_normalizations: frozenset[tuple[str, str, str]] = frozenset()
    actual_lifecycle_normalization_sources: dict[str, str] = {}
    generation_bindings = _GenerationBindings()
    if registry is not None:
        try:
            if args.mode == "check-changed":
                (
                    contract_findings,
                    actual_lifecycle_transitions,
                    actual_lifecycle_normalizations,
                    generation_bindings,
                ) = _validate_repository_contracts(
                    root,
                    profiles,
                    base_ref=base.merge_base,
                    transition_ref=base.merge_base,
                    previous_records=(
                        base_records_by_path if base.merge_base is not None else None
                    ),
                    current_records=records_by_path,
                    frontmatter_validator=frontmatter_validator,
                    validation_paths=validation_paths,
                    transition_overrides=transition_overrides,
                )
                actual_lifecycle_normalization_sources = {
                    path: source for path, source, _ in actual_lifecycle_normalizations
                }
                native_findings.extend(contract_findings)
            else:
                native_findings.extend(_reference_delegation_findings(root, profiles))
        except (ProfileError, SpecPackageError) as error:
            print(f"configuration-error: {error}", file=sys.stderr)
            return 2
    if args.mode == "check-changed":
        findings_by_path: dict[str, list[Finding]] = collections.defaultdict(list)
        for finding in native_findings:
            findings_by_path[finding.path].append(finding)
    else:
        findings_by_path = {
            record.path.as_posix(): validate_record(
                record,
                profiles,
                manifest,
                transition_overrides=transition_overrides,
                enforce_initial_status=False,
                actual_lifecycle_transitions=actual_lifecycle_transitions,
                actual_lifecycle_normalizations=actual_lifecycle_normalizations,
                actual_lifecycle_normalization_sources=(
                    actual_lifecycle_normalization_sources
                ),
                unchanged_generation_statuses=generation_bindings.unchanged_statuses,
                frontmatter_validator=frontmatter_validator,
            )
            for record in records
        }
    if args.mode != "check-changed":
        # Active/report checks also enforce runtime authority. Changed mode uses
        # the same helper through the existing introduced-body comparison.
        for record in records:
            try:
                text = read_bounded_regular(
                    root,
                    record.path,
                    max_bytes=4 * 1024 * 1024,
                ).decode("utf-8")
            except (OSError, UnicodeError, OperationsAuthorityError):
                continue  # Existing record parsing owns unreadable-file errors.
            path_text = record.path.as_posix()
            findings_by_path[path_text] = [
                *findings_by_path[path_text],
                *_common_document_view(record, text, profiles)[2],
                *_runtime_version_findings(record, text, root),
            ]
    changed_body_findings: dict[str, list[Finding]] = {}
    if args.mode == "check-changed":
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
            base_text = governance_move_texts.get(path_text)
            generation_record, generation_text = _generation_task_body_baseline(
                root,
                record,
                current_text,
                profiles,
                generation_bindings,
            )
            if generation_record is not None and generation_text is not None:
                base_record = generation_record
                base_text = generation_text
            if base_text is None:
                base_text = base_texts.get(path_text)
                if base_text is None:
                    base_text = _text_at_ref(root, record.path, base.merge_base)
            changed_body_findings[path_text] = _introduced_body_findings(
                record,
                current_text,
                base_record,
                base_text,
                profiles,
            )
    version_findings: list[Finding] = []
    if args.mode == "check-changed":
        version_findings = version_change_findings(
            root,
            {
                path: records_by_path[path]
                for path in changed_selection
                if path in records_by_path
            },
            base.merge_base,
            profiles,
            base_texts=base_texts,
        ) + product_version_findings(root, base.merge_base)
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
    if args.mode == "report":
        parser_failures = [record for record in records if record.parse_error]
        rendered = render_report(records, profiles, findings_by_path)
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
        validation_paths
        if args.mode == "check-changed"
        else {
            record.path.as_posix()
            for record in records
            if record.metadata.get("status") in {"active", "approved"}
        }
    )
    selected_paths = directly_selected_paths | set(relation_impact_findings)
    selected_findings = sorted(
        set(native_findings)
        | set(version_findings)
        | {
            finding
            for path in directly_selected_paths
            for finding in findings_by_path.get(path, [])
            if finding.severity == "error"
        }
        | {
            finding
            for path, findings in relation_impact_findings.items()
            for finding in findings
        }
        | {
            finding
            for path, findings in changed_body_findings.items()
            for finding in findings
            if finding.severity == "error"
        }
    )
    for finding in selected_findings:
        print(f"{finding.path}: {finding.code}: {finding.message}")
    print(
        f"metadata {args.mode}: selected={len(selected_paths)} violations={len(selected_findings)} "
        f"transition_overrides={len(transition_overrides)}"
    )
    return 1 if selected_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
