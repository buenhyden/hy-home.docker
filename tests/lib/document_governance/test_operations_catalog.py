from __future__ import annotations

import contextlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance import operations_catalog
from scripts.lib.document_governance.operations_catalog import (
    REGISTRY_PATH,
    OperationsAuthorityError,
    _run_git_bounded,
    read_bounded_regular,
    validate_active_operations_references,
    validate_compose_profile_vocabulary,
    validate_current_operations,
)

ROOT = pathlib.Path(__file__).resolve().parents[3]


ROLE_DIRECTORIES = ("guides", "policies", "runbooks")
ROLE_KINDS = {"guides": "guide", "policies": "policy", "runbooks": "runbook"}
NUMBERED_DOMAINS = (
    "01-common",
    "02-gateway-and-networking",
    "03-identity-and-access",
    "04-security-and-secrets",
    "05-databases-and-storage",
    "06-messaging-and-cdc",
    "07-observability",
    "08-workflows-and-automation",
    "09-ai-and-search",
    "10-platform-and-backup",
    "11-mail-and-notifications",
    "12-testing-and-quality",
    "13-analytics-and-data-quality",
    "14-design-system",
    "15-labs",
)


def current_role_paths(root: pathlib.Path = ROOT) -> tuple[pathlib.PurePosixPath, ...]:
    return tuple(
        pathlib.PurePosixPath(path.relative_to(root).as_posix())
        for directory in ROLE_DIRECTORIES
        for path in sorted(
            (root / "docs/05.operations" / directory).rglob("[0-9][0-9][0-9][0-9]-*.md")
        )
    )


def finding_codes(root: pathlib.Path = ROOT) -> set[str]:
    return {finding.code for finding in validate_current_operations(root)}


class OperationsCatalogTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.role_paths = current_role_paths()

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        for source in (
            "docs/05.operations",
            "docs/99.templates/templates/operations",
        ):
            shutil.copytree(ROOT / source, root / source)
        for source in ("docs/99.templates/registry.json",):
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / source, target)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "add", "docs/05.operations", "docs/99.templates"],
            cwd=root,
            check=True,
        )
        context = contextlib.ExitStack()
        context.enter_context(directory)
        self.addCleanup(context.close)
        return context, root

    def _track(self, root: pathlib.Path, *paths: pathlib.Path) -> None:
        subprocess.run(
            ["git", "add", "-A", *(str(path) for path in paths)],
            cwd=root,
            check=True,
        )

    def test_registry_owns_the_exact_numbered_role_domains(self) -> None:
        registry = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
        profiles = {row["id"]: row for row in registry["profiles"]}
        readmes = set(profiles["readme"]["additional_paths"])
        for family, role in ROLE_KINDS.items():
            with self.subTest(family=family):
                prefix = f"docs/05.operations/{family}/"
                domains = tuple(
                    pattern.removeprefix(prefix).split("/", 1)[0]
                    for pattern in profiles[role]["additional_path_patterns"]
                )
                self.assertEqual(NUMBERED_DOMAINS, domains)
                self.assertEqual(
                    {
                        f"docs/05.operations/{family}/{domain}/README.md"
                        for domain in NUMBERED_DOMAINS
                    },
                    {
                        path
                        for path in readmes
                        if path.startswith(prefix) and path != f"{prefix}README.md"
                    },
                )

    def test_prefixed_or_nested_role_member_is_rejected(self) -> None:
        for mutation in ("prefixed", "nested"):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    member = root / self.role_paths[0]
                    if mutation == "prefixed":
                        target = member.with_name(f"ops-{member.name}")
                    else:
                        target = member.parent / "00-workspace" / member.name
                        target.parent.mkdir()
                    member.rename(target)
                    self._track(root, member.parent)
                    self.assertIn("role-path-invalid", finding_codes(root))

    def _lab_fixture(
        self, domain: str = "15-labs"
    ) -> tuple[contextlib.ExitStack, pathlib.Path]:
        context, root = self._fixture()
        for family in ROLE_DIRECTORIES:
            family_root = root / "docs/05.operations" / family
            index = family_root / "README.md"
            index_text = index.read_text(encoding="utf-8")
            # 0999 is a synthetic fixture identity, not a copy of a real subject.
            for existing in family_root.rglob("0999-*.md"):
                index_text = "".join(
                    line
                    for line in index_text.splitlines(keepends=True)
                    if f"({existing.name})" not in line
                )
                existing.unlink()
            source = next(path for path in self.role_paths if path.parts[2] == family)
            text = (root / source).read_text(encoding="utf-8")
            old_id = yaml.safe_load(text.split("---\n", 2)[1])["artifact_id"]
            prefix = old_id.split("-", 1)[0]
            folder = family_root / domain
            folder.mkdir(exist_ok=True)
            (folder / "0999-lab-example.md").write_text(
                text.replace(old_id, f"{prefix}-0999", 1), encoding="utf-8"
            )
            domain_index = folder / "README.md"
            domain_text = (
                domain_index.read_text(encoding="utf-8")
                if domain_index.exists()
                else "# 실험 문서\n"
            )
            domain_index.write_text(
                domain_text + "\n[합성 예제](0999-lab-example.md)\n",
                encoding="utf-8",
            )
            domain_link = f"({domain}/README.md)"
            if domain_link not in index_text:
                index.write_text(
                    index_text + f"\n[합성 문서]({domain}/README.md)\n",
                    encoding="utf-8",
                )
        self._track(root, root / "docs/05.operations")
        return context, root

    def test_typed_lab_folders_with_direct_child_indexes_are_accepted(self) -> None:
        context, root = self._lab_fixture()
        with context:
            self.assertEqual(set(), finding_codes(root))

    def test_registered_domain_folders_with_direct_child_indexes_are_accepted(
        self,
    ) -> None:
        for domain in ("01-common", "04-security-and-secrets"):
            with self.subTest(domain=domain):
                context, root = self._lab_fixture(domain)
                with context:
                    self.assertEqual(set(), finding_codes(root))

    def test_unknown_case_variant_and_deeper_domain_folders_are_rejected(self) -> None:
        for domain in ("common", "99-unknown-domain", "15-Labs", "15-labs/nested"):
            with self.subTest(domain=domain):
                context, root = self._lab_fixture()
                with context:
                    folder = root / "docs/05.operations/guides/15-labs"
                    target = folder.parent / domain
                    if domain == "15-labs/nested":
                        target.mkdir()
                        member = folder / "0999-lab-example.md"
                        member.rename(target / member.name)
                    else:
                        folder.rename(target)
                    self._track(root, folder.parent)
                    self.assertIn("role-path-invalid", finding_codes(root))

    def test_lab_index_requires_exact_member_coverage(self) -> None:
        for mutation in ("missing", "duplicate", "stale", "missing-readme"):
            with self.subTest(mutation=mutation):
                context, root = self._lab_fixture()
                with context:
                    index = root / "docs/05.operations/guides/15-labs/README.md"
                    row = "[합성 예제](0999-lab-example.md)\n"
                    if mutation == "missing-readme":
                        index.unlink()
                    else:
                        replacement = {
                            "missing": "",
                            "duplicate": row + row,
                            "stale": "[합성 예제](0098-gone.md)\n",
                        }[mutation]
                        index.write_text(
                            "# 실험 문서\n\n" + replacement, encoding="utf-8"
                        )
                    self._track(root, index.parent)
                    codes = finding_codes(root)
                    self.assertTrue(
                        {"role-index-invalid", "role-index-membership-invalid"} & codes,
                        codes,
                    )

    def test_domain_and_readme_symlinks_and_untracked_members_are_rejected(
        self,
    ) -> None:
        for mutation in (
            "directory-symlink",
            "readme-symlink",
            "untracked",
            "unregistered-readme",
        ):
            with self.subTest(mutation=mutation):
                context, root = self._lab_fixture()
                with context:
                    folder = root / "docs/05.operations/guides/15-labs"
                    if mutation == "directory-symlink":
                        target = root / "outside-domain"
                        folder.rename(target)
                        folder.symlink_to(target, target_is_directory=True)
                        self._track(root, folder.parent)
                    elif mutation == "readme-symlink":
                        index = folder / "README.md"
                        index.unlink()
                        index.symlink_to(folder.parent / "README.md")
                        self._track(root, folder.parent)
                    elif mutation == "unregistered-readme":
                        registry_path = root / REGISTRY_PATH
                        raw = json.loads(registry_path.read_text(encoding="utf-8"))
                        owner = next(p for p in raw["profiles"] if p["id"] == "readme")
                        owner["additional_paths"].remove(
                            "docs/05.operations/guides/15-labs/README.md"
                        )
                        registry_path.write_text(json.dumps(raw), encoding="utf-8")
                    else:
                        subprocess.run(
                            [
                                "git",
                                "rm",
                                "--cached",
                                str(folder / "0999-lab-example.md"),
                            ],
                            cwd=root,
                            check=True,
                            capture_output=True,
                        )
                    self.assertTrue(finding_codes(root))

    def test_role_entry_budget_covers_parent_and_domains_together(self) -> None:
        context, root = self._lab_fixture()
        with context:
            entries = len(list((root / "docs/05.operations/guides").iterdir()))
            with mock.patch.object(operations_catalog, "MAX_ROLE_ENTRIES", entries + 1):
                self.assertIn("role-bounds", finding_codes(root))

    def test_lab_identity_is_unique_across_domains_within_its_family(self) -> None:
        context, root = self._lab_fixture()
        with context:
            member = root / "docs/05.operations/guides/15-labs/0999-lab-example.md"
            duplicate = member.parent / "0999-other.md"
            duplicate.write_text(member.read_text(encoding="utf-8"), encoding="utf-8")
            index = duplicate.parent / "README.md"
            index.write_text(
                index.read_text(encoding="utf-8") + "\n[복제](0999-other.md)\n",
                encoding="utf-8",
            )
            self._track(root, duplicate.parent)
            self.assertIn("role-identity-duplicate", finding_codes(root))

    def test_file_number_must_equal_the_kept_artifact_number(self) -> None:
        context, root = self._fixture()
        with context:
            member = root / self.role_paths[0]
            renumbered = member.with_name("0999" + member.name[4:])
            member.rename(renumbered)
            self._track(root, member.parent)
            self.assertIn("role-identity-invalid", finding_codes(root))

    def test_slug_is_unique_within_one_role_directory(self) -> None:
        context, root = self._fixture()
        with context:
            member = root / self.role_paths[0]
            text = member.read_text(encoding="utf-8")
            artifact = yaml.safe_load(text.split("---\n", 2)[1])["artifact_id"]
            prefix = artifact.split("-", 1)[0]
            copy = member.with_name("0999" + member.name[4:])
            copy.write_text(
                text.replace(
                    f'artifact_id: "{artifact}"', f'artifact_id: "{prefix}-0999"', 1
                ),
                encoding="utf-8",
            )
            self._track(root, copy)
            self.assertIn("role-slug-duplicate", finding_codes(root))

    def test_role_index_lists_every_member_exactly_once(self) -> None:
        for mutation in ("missing", "duplicate", "stale"):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    member = root / self.role_paths[0]
                    index = member.parent / "README.md"
                    text = index.read_text(encoding="utf-8")
                    link = f"({member.name})"
                    lines = text.splitlines(keepends=True)
                    row = next(line for line in lines if link in line)
                    if mutation == "missing":
                        text = text.replace(row, "", 1)
                    elif mutation == "duplicate":
                        text = text.replace(row, row + row, 1)
                    else:
                        text = text.replace(row, row.replace(link, "(0999-gone.md)"), 1)
                    index.write_text(text, encoding="utf-8")
                    self.assertIn("role-index-membership-invalid", finding_codes(root))

    def test_changed_or_duplicate_role_identity_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            first, second = self.role_paths[:2]
            first_text = (root / first).read_text(encoding="utf-8")
            first_id = yaml.safe_load(first_text.split("---\n", 2)[1])["artifact_id"]
            second_path = root / second
            second_id = yaml.safe_load(
                second_path.read_text(encoding="utf-8").split("---\n", 2)[1]
            )["artifact_id"]
            second_path.write_text(
                second_path.read_text(encoding="utf-8").replace(
                    f'artifact_id: "{second_id}"',
                    f'artifact_id: "{first_id}"',
                    1,
                ),
                encoding="utf-8",
            )
            codes = finding_codes(root)
            self.assertTrue(
                {"role-identity-invalid", "role-identity-duplicate"} <= codes
            )

    def test_release_and_parallel_role_roots_are_rejected(self) -> None:
        for retired in ("releases", "catalog"):
            with self.subTest(retired=retired):
                context, root = self._fixture()
                with context:
                    (root / "docs/05.operations" / retired).mkdir(exist_ok=True)
                    self.assertIn("retired-root-present", finding_codes(root))

    def test_release_profile_is_rejected(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / "docs/99.templates/registry.json"
            registry = registry_path.read_text(encoding="utf-8")
            registry_path.write_text(
                registry.replace(
                    '"profiles": [',
                    '"profiles": [{"id":"release","path_pattern":"docs/05.operations/releases/{slug}.md"},',
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn("release-authority-present", finding_codes(root))

    def test_registry_operations_profiles_and_template_roles_are_present(self) -> None:
        mutations = (
            ("id", "guide-copy"),
            ("template_id", "operation/policy"),
        )
        for key, value in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item for item in registry["profiles"] if item["id"] == "guide"
                    )
                    guide[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn(
                        "registry-operations-profile-invalid", finding_codes(root)
                    )

        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["id"] == "guide")
            registry["profiles"].append(dict(guide))
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-profile-duplicate", finding_codes(root))

    def test_registry_lifecycle_and_required_sections_are_consumed(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            living = registry["lifecycles"]["living"]
            living["statuses"].remove("active")
            living["transitions"].pop("active")
            for targets in living["transitions"].values():
                if "active" in targets:
                    targets.remove("active")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-canonical-invalid", finding_codes(root))

        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["id"] == "guide")
            guide["required_sections"].append("New Contract")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("role-sections-invalid", finding_codes(root))

    def test_registry_schema_valid_optional_changes_do_not_require_a_python_mirror(
        self,
    ) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["id"] == "guide")
            guide["optional_frontmatter"].append("generated_by")
            guide["optional_sections"].append("Operator Notes")
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            codes = finding_codes(root)
            self.assertNotIn("registry-operations-profile-invalid", codes)
            self.assertNotIn("registry-operations-lifecycle-invalid", codes)

    def test_registry_operations_profiles_require_a_layer_declaration(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["id"] == "guide")
            guide["required_frontmatter"] = [
                item for item in guide["required_frontmatter"] if item != "layer"
            ]
            guide["optional_frontmatter"] = [
                item for item in guide["optional_frontmatter"] if item != "layer"
            ]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-operations-profile-invalid", finding_codes(root))

    def test_registry_operations_profiles_reject_malformed_optional_frontmatter(
        self,
    ) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            guide = next(item for item in registry["profiles"] if item["id"] == "guide")
            guide["optional_frontmatter"] = [""]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            codes = finding_codes(root)
            self.assertTrue(
                codes
                & {
                    "registry-canonical-invalid",
                    "registry-operations-profile-invalid",
                }
            )

    def test_malformed_registry_returns_findings_without_traceback(self) -> None:
        for mutation in (
            "missing-artifact-pattern",
            "object-frontmatter-member",
            "object-profile-id",
            "object-lifecycle-id",
        ):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item for item in registry["profiles"] if item["id"] == "guide"
                    )
                    if mutation == "missing-artifact-pattern":
                        del guide["artifact_id_pattern"]
                    elif mutation == "object-frontmatter-member":
                        guide["required_frontmatter"] = [{"bad": "shape"}]
                    elif mutation == "object-profile-id":
                        guide["id"] = {"bad": "shape"}
                    else:
                        guide["lifecycle_id"] = {"bad": "shape"}
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    codes = finding_codes(root)
                    self.assertIn("registry-canonical-invalid", codes)

    def test_registry_loader_rejects_excessive_depth_without_traceback(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            cursor = registry
            for _ in range(70):
                child: dict[str, object] = {}
                cursor["too_deep"] = child
                cursor = child
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-invalid", finding_codes(root))

    def test_registry_loader_rejects_symlinked_parent_directory(self) -> None:
        context, root = self._fixture()
        with context:
            registry_root = root / "docs/99.templates"
            external_root = root / "external-templates"
            registry_root.rename(external_root)
            registry_root.symlink_to(external_root, target_is_directory=True)
            self.assertIn("registry-invalid", finding_codes(root))

    def test_registry_route_and_identity_relation_govern_role_leaves(self) -> None:
        mutations = (
            (
                "path_pattern",
                "docs/05.operations/runbooks/{number:4}-{slug}.md",
                "role-path-invalid",
            ),
            ("identity_relation", "package-member", "role-identity-relation-invalid"),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    guide = next(
                        item for item in registry["profiles"] if item["id"] == "guide"
                    )
                    guide[key] = value
                    if key == "path_pattern":
                        guide["additional_path_patterns"] = []
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn(expected, finding_codes(root))

    def test_registry_route_and_identity_relation_govern_incident_leaves(self) -> None:
        mutations = (
            (
                "path_pattern",
                "docs/05.operations/incidents/{year:4}/incident-{number:4}-{slug}.md",
                "incident-path-profile-mismatch",
            ),
            (
                "identity_relation",
                "package-member",
                "incident-identity-relation-invalid",
            ),
        )
        for key, value, expected in mutations:
            with self.subTest(key=key):
                context, root = self._fixture()
                with context:
                    self._write_incident_packet(root)
                    registry_path = root / REGISTRY_PATH
                    registry = json.loads(registry_path.read_text(encoding="utf-8"))
                    incident = next(
                        item
                        for item in registry["profiles"]
                        if item["id"] == "incident"
                    )
                    incident[key] = value
                    registry_path.write_text(json.dumps(registry), encoding="utf-8")
                    self.assertIn(expected, finding_codes(root))

    def test_registry_required_sections_keep_operations_roles_distinct(self) -> None:
        context, root = self._fixture()
        with context:
            registry_path = root / REGISTRY_PATH
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            profiles = {item["id"]: item for item in registry["profiles"]}
            profiles["policy"]["required_sections"] = list(
                profiles["guide"]["required_sections"]
            )
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIn("registry-role-purpose-duplicate", finding_codes(root))

    def test_role_profile_and_registry_grounded_sections_are_required(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(path for path in self.role_paths)
            text = role.read_text(encoding="utf-8")
            role.write_text(
                text.split("---\n", 2)[0]
                + "---\n"
                + text.split("---\n", 2)[1]
                + "---\n# Arbitrary\n",
                encoding="utf-8",
            )
            self.assertIn("role-sections-invalid", finding_codes(root))

    def test_role_type_is_required_even_when_all_other_metadata_is_valid(
        self,
    ) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(path for path in self.role_paths)
            text = role.read_text(encoding="utf-8")
            role_name = ROLE_KINDS[role.parent.parent.name]
            role.write_text(
                text.replace(f'type: "operation/{role_name}"\n', "", 1),
                encoding="utf-8",
            )
            self.assertIn("role-profile-invalid", finding_codes(root))

    def test_role_frontmatter_rejects_duplicate_same_value_type(self) -> None:
        context, root = self._fixture()
        with context:
            role = root / next(path for path in self.role_paths)
            role_name = ROLE_KINDS[role.parent.parent.name]
            text = role.read_text(encoding="utf-8")
            role.write_text(
                text.replace(
                    f'type: "operation/{role_name}"\n',
                    f'type: "operation/{role_name}"\ntype: "operation/{role_name}"\n',
                    1,
                ),
                encoding="utf-8",
            )
            self.assertIn("frontmatter-invalid", finding_codes(root))

    def _write_incident_packet(
        self,
        root: pathlib.Path,
        *,
        year: str = "2026",
        artifact_id: str = "inc-0001",
        status: str = "open",
        occurred_at: str = "2026-08-23T01:00:00Z",
        resolved_at: str = "2026-08-23T02:00:00Z",
        body: str | None = None,
    ) -> pathlib.Path:
        registry = json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))
        profile = next(
            item for item in registry["profiles"] if item["id"] == "incident"
        )
        packet = root / f"docs/05.operations/incidents/{year}/inc-0001-fixture"
        packet.mkdir(parents=True)
        metadata = (
            f"---\ntype: operation/incident\nstatus: {status}\n"
            f"artifact_id: {artifact_id}\nartifact_type: incident\nparent_ids: []\n"
            "created: 2026-08-23\nupdated: 2026-08-23\n"
            f"occurred_at: {occurred_at}\nresolved_at: {resolved_at}\n---\n"
        )
        sections = body or "\n".join(
            f"## {section}\nEvidence." for section in profile["required_sections"]
        )
        path = packet / "incident.md"
        path.write_text(
            metadata + "# Fixture Incident\n\n" + sections + "\n", encoding="utf-8"
        )
        return path

    def test_incident_body_identity_year_and_date_relations_are_validated(self) -> None:
        mutations = (
            ({"body": "Arbitrary body."}, "incident-sections-invalid"),
            ({"year": "2025"}, "incident-year-date-invalid"),
            ({"artifact_id": "inc-0002"}, "incident-identity-invalid"),
            (
                {
                    "occurred_at": "2026-08-23T02:00:00Z",
                    "resolved_at": "2026-08-23T01:00:00Z",
                },
                "incident-date-order-invalid",
            ),
            ({"status": "active"}, "incident-status-invalid"),
        )
        for kwargs, expected in mutations:
            with self.subTest(expected=expected):
                context, root = self._fixture()
                with context:
                    self._write_incident_packet(root, **kwargs)
                    self.assertIn(expected, finding_codes(root))

    def test_closure_dates_use_conditional_presence_and_real_timestamp_schema(self):
        from scripts.lib.document_governance.registry import (
            load_registry,
            validate_frontmatter,
            validate_profile_values,
        )

        profile = load_registry().profiles["incident"]
        for value in (
            None,
            "",
            " ",
            "2026-02-30T01:00:00Z",
            "2026-09-28T01:00:00",
            "2026-09-28T01:00:00+01:99",
            "not-a-date",
        ):
            with self.subTest(value=value):
                values = {"status": "resolved", "resolved_at": value}
                findings = (
                    *validate_profile_values(values, profile),
                    *validate_frontmatter(values),
                )
                self.assertTrue(any(item.path == "resolved_at" for item in findings))
        self.assertEqual(
            operations_catalog._date_time("2026-09-28T10:00:00+09:00"),
            operations_catalog._date_time("2026-09-28T01:00:00Z"),
        )

    def test_resolved_bundle_requires_published_postmortem_and_current_owner(self):
        for state, owner, expected in (
            (None, "", "incident-postmortem-required"),
            ("draft", "GDE-0011", "incident-postmortem-required"),
            ("published", "GDE-9999", "incident-corrective-owner-required"),
            ("published", "inc-2026-0001", "incident-corrective-owner-required"),
            ("published", "GDE-0011", None),
            ("published", "no corrective action: transient fixture", None),
        ):
            with self.subTest(state=state, owner=owner):
                context, root = self._fixture()
                with context:
                    incident = self._write_incident_packet(
                        root, status="resolved", artifact_id="inc-2026-0001"
                    )
                    if state is not None:
                        (incident.parent / "postmortem.md").write_text(
                            "---\ntype: operation/postmortem\n"
                            f"status: {state}\nartifact_id: inc-2026-0001-PM\n"
                            "parent_ids: [inc-2026-0001]\ncreated: 2026-08-23\n"
                            "updated: 2026-08-23\nreviewed_at: 2026-08-23\n---\n"
                            f"## Corrective Actions\n{owner}\n"
                        )
                    self._track(root, incident.parent)
                    codes = finding_codes(root)
                    if expected:
                        self.assertIn(expected, codes)
                    else:
                        self.assertNotIn("incident-postmortem-required", codes)
                        self.assertNotIn("incident-corrective-owner-required", codes)

    def test_nested_corrective_actions_require_one_substantive_owned_section(self):
        cases = (
            (
                "unique-owned",
                "## Overview\n### Corrective Actions\nGDE-0011\n"
                "## Corrective Actions\n",
                False,
            ),
            (
                "missing",
                "## Overview\nIncident summary.\n## Corrective Actions\n",
                True,
            ),
            (
                "ambiguous",
                "## Overview\n### Corrective Actions\nGDE-0011\n"
                "### Corrective Actions\nGDE-0012\n## Corrective Actions\n",
                True,
            ),
            (
                "owner-missing",
                "## Overview\n### Corrective Actions\nFollow up later.\n"
                "## Corrective Actions\n",
                True,
            ),
        )
        for label, body, expects_finding in cases:
            with self.subTest(label=label):
                context, root = self._fixture()
                with context:
                    incident = self._write_incident_packet(
                        root, status="resolved", artifact_id="inc-2026-0001"
                    )
                    (incident.parent / "postmortem.md").write_text(
                        "---\ntype: operation/postmortem\n"
                        "status: published\nartifact_id: inc-2026-0001-PM\n"
                        "parent_ids: [inc-2026-0001]\ncreated: 2026-08-23\n"
                        "updated: 2026-08-23\nreviewed_at: 2026-08-23\n---\n" + body,
                        encoding="utf-8",
                    )
                    self._track(root, incident.parent)
                    codes = finding_codes(root)
                    self.assertEqual(
                        expects_finding,
                        "incident-corrective-owner-required" in codes,
                    )

    def test_incident_year_packet_and_roles_are_exact(self) -> None:
        mutations = (
            "docs/05.operations/incidents/current/inc-0001-bad/incident.md",
            "docs/05.operations/incidents/2026/incident-0001-bad/incident.md",
            "docs/05.operations/incidents/2026/inc-0001-bad/notes.md",
        )
        for relative in mutations:
            with self.subTest(relative=relative):
                context, root = self._fixture()
                with context:
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("invalid", encoding="utf-8")
                    codes = finding_codes(root)
                    self.assertTrue(
                        codes
                        & {
                            "incident-year-invalid",
                            "incident-packet-invalid",
                            "incident-roles-invalid",
                        }
                    )

    def test_incident_year_readme_must_be_a_regular_file(self) -> None:
        relative = "docs/05.operations/incidents/2026/README.md"
        for mutation in ("regular", "directory"):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    path = root / relative
                    if path.exists():
                        path.unlink()
                    if mutation == "regular":
                        path.write_text("# 2026\n", encoding="utf-8")
                        self.assertNotIn("incident-packet-invalid", finding_codes(root))
                    else:
                        path.mkdir()
                        self.assertIn("incident-packet-invalid", finding_codes(root))

    def test_role_symlink_and_nonregular_inputs_are_rejected(self) -> None:
        target = self.role_paths[0]
        for mutation in ("symlink", "directory"):
            with self.subTest(mutation=mutation):
                context, root = self._fixture()
                with context:
                    path = root / target
                    path.unlink()
                    if mutation == "symlink":
                        path.symlink_to(ROOT / target)
                    else:
                        path.mkdir()
                    self.assertIn("role-file-invalid", finding_codes(root))

    def test_untracked_valid_member_is_not_current_membership(self) -> None:
        context, root = self._fixture()
        with context:
            source = (
                root
                / "docs/05.operations/guides/02-gateway-and-networking/0011-nginx.md"
            )
            target = source.with_name("0999-untracked.md")
            target.write_text(
                re.sub(
                    r'^artifact_id: "GDE-[0-9]{4}"$',
                    'artifact_id: "GDE-0999"',
                    source.read_text(encoding="utf-8"),
                    count=1,
                    flags=re.MULTILINE,
                ),
                encoding="utf-8",
            )
            self.assertIn("untracked-operations-path", finding_codes(root))

    def test_structural_indexes_must_be_regular_and_symlink_free(self) -> None:
        for relative, expected in (
            ("docs/05.operations/README.md", "operations-root-index-invalid"),
            ("docs/05.operations/incidents/README.md", "incident-index-invalid"),
            ("docs/05.operations/guides/README.md", "role-index-invalid"),
        ):
            for mutation in ("symlink", "directory", "fifo"):
                with self.subTest(relative=relative, mutation=mutation):
                    context, root = self._fixture()
                    with context:
                        path = root / relative
                        path.unlink()
                        if mutation == "symlink":
                            path.symlink_to(ROOT / relative)
                        elif mutation == "directory":
                            path.mkdir()
                        else:
                            os.mkfifo(path)
                        self.assertIn(expected, finding_codes(root))

    def test_operations_root_and_role_enumeration_are_independently_bounded(
        self,
    ) -> None:
        mutations = (
            ("MAX_OPERATIONS_ROOT_ENTRIES", "operations-root-bounds"),
            ("MAX_ROLE_ENTRIES", "role-bounds"),
        )
        for constant, expected in mutations:
            with (
                self.subTest(constant=constant),
                mock.patch.object(operations_catalog, constant, 1),
            ):
                self.assertIn(expected, finding_codes())

    def test_incident_enumeration_is_bounded(self) -> None:
        context, root = self._fixture()
        with context:
            self._write_incident_packet(root)
            with mock.patch.object(operations_catalog, "MAX_INCIDENT_ENTRIES", 1):
                self.assertIn("incident-bounds", finding_codes(root))


class BoundedRegularReaderTests(unittest.TestCase):
    def test_reader_rejects_service_readme_regular_to_fifo_race_without_blocking(
        self,
    ) -> None:
        source = """
import os
import pathlib
import sys
from unittest import mock

from scripts.lib.document_governance import operations_catalog

root = pathlib.Path(sys.argv[1])
target = root / "infra/service/README.md"
real_stat = os.stat
swapped = False

def racing_stat(path, *args, **kwargs):
    global swapped
    result = real_stat(path, *args, **kwargs)
    if path == "README.md" and kwargs.get("dir_fd") is not None and not swapped:
        swapped = True
        target.unlink()
        os.mkfifo(target)
    return result

with mock.patch.object(operations_catalog.os, "stat", side_effect=racing_stat):
    try:
        operations_catalog.read_bounded_regular(
            root, pathlib.PurePosixPath("infra/service/README.md")
        )
    except operations_catalog.OperationsAuthorityError:
        sys.exit(0)
sys.exit(1)
"""
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "infra/service/README.md"
            target.parent.mkdir(parents=True)
            target.write_text("content\n", encoding="utf-8")
            environment = os.environ.copy()
            python_path = environment.get("PYTHONPATH")
            environment["PYTHONPATH"] = (
                str(ROOT) if not python_path else f"{ROOT}{os.pathsep}{python_path}"
            )
            try:
                result = subprocess.run(
                    [sys.executable, "-c", source, str(root)],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                    timeout=1.0,
                )
            except subprocess.TimeoutExpired:
                self.fail("regular-to-FIFO reader race blocked during open")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reader_rejects_symlink_and_byte_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "real").write_text("content", encoding="utf-8")
            (root / "link").symlink_to(root / "real")
            with self.assertRaisesRegex(OperationsAuthorityError, "symlink"):
                read_bounded_regular(root, pathlib.PurePosixPath("link"))
            with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
                read_bounded_regular(root, pathlib.PurePosixPath("real"), max_bytes=2)

    def test_reader_rejects_an_in_read_identity_race(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "input"
            target.write_text("content", encoding="utf-8")
            real = os.stat(target)
            changed = types.SimpleNamespace(
                st_dev=real.st_dev,
                st_ino=real.st_ino,
                st_size=real.st_size,
                st_mtime_ns=real.st_mtime_ns + 1,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.fstat",
                side_effect=(real, changed),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "during read"):
                    read_bounded_regular(root, pathlib.PurePosixPath("input"))

    def test_reader_clamps_caller_limit_to_hard_maximum(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "input").write_text("content", encoding="utf-8")
            with mock.patch.object(operations_catalog, "MAX_FILE_BYTES", 2):
                with self.assertRaisesRegex(OperationsAuthorityError, "bound"):
                    read_bounded_regular(
                        root,
                        pathlib.PurePosixPath("input"),
                        max_bytes=1_000_000,
                    )


class BoundedDirectoryEnumerationTests(unittest.TestCase):
    def test_directory_path_identity_swap_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "entry").write_text("content", encoding="utf-8")
            before = os.stat(target)
            swapped = types.SimpleNamespace(
                st_mode=before.st_mode,
                st_dev=before.st_dev,
                st_ino=before.st_ino + 1,
                st_mtime_ns=before.st_mtime_ns,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.stat",
                side_effect=(before, swapped),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "changed"):
                    operations_catalog._directory_entries_bounded(
                        root,
                        pathlib.PurePosixPath("target"),
                        max_entries=8,
                    )

    def test_directory_in_enumeration_metadata_race_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "entry").write_text("content", encoding="utf-8")
            before = os.stat(target)
            changed = types.SimpleNamespace(
                st_mode=before.st_mode,
                st_dev=before.st_dev,
                st_ino=before.st_ino,
                st_mtime_ns=before.st_mtime_ns + 1,
            )
            with mock.patch(
                "scripts.lib.document_governance.operations_catalog.os.fstat",
                side_effect=(before, changed),
            ):
                with self.assertRaisesRegex(OperationsAuthorityError, "changed"):
                    operations_catalog._directory_entries_bounded(
                        root,
                        pathlib.PurePosixPath("target"),
                        max_entries=8,
                    )


class BoundedGitAndTrackedInputTests(unittest.TestCase):
    def _repo(self) -> tempfile.TemporaryDirectory[str]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.invalid"],
            cwd=root,
            check=True,
        )
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        return directory

    def test_git_helper_drains_stdout_and_stderr_without_deadlock(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            alias = (
                "alias.noisy=!python3 -c 'import sys;"
                'sys.stdout.write("o"*65536);sys.stdout.flush();'
                'sys.stderr.write("e"*65536);sys.stderr.flush()\''
            )
            result = _run_git_bounded(
                root,
                ["-c", alias, "noisy"],
                timeout_seconds=2,
                max_stdout=100_000,
                max_stderr=100_000,
            )
            self.assertEqual(0, result.returncode)
            self.assertEqual(65_536, len(result.stdout))
            self.assertEqual(65_536, len(result.stderr))

    def test_git_helper_enforces_deadline_and_reaps_process_group(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            started = time.monotonic()
            with self.assertRaisesRegex(OperationsAuthorityError, "deadline"):
                _run_git_bounded(
                    root,
                    ["-c", "alias.wait=!sleep 2", "wait"],
                    timeout_seconds=0.05,
                )
            self.assertLess(time.monotonic() - started, 1.0)

    def test_git_helper_enforces_stdout_and_stderr_caps(self) -> None:
        with self._repo() as directory:
            root = pathlib.Path(directory)
            (root / "blob").write_text("x" * 512, encoding="utf-8")
            subprocess.run(["git", "add", "blob"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            with self.assertRaisesRegex(OperationsAuthorityError, "stdout"):
                _run_git_bounded(root, ["show", "HEAD:blob"], max_stdout=32)
            with self.assertRaisesRegex(OperationsAuthorityError, "stderr"):
                _run_git_bounded(root, ["show", "HEAD:missing"], max_stderr=8)

    def test_active_scan_rejects_catalog_routes_and_allows_role_routes(self) -> None:
        cases = (
            ("See docs/05.operations/catalog/00-workspace/0001-a/guide.md.", True),
            ("See docs/05.operations/catalog/README.md.", True),
            ("See docs/05.operations/guides/0001-a.md.", False),
            ("See docs/05.operations/runbooks/0009-release-management.md.", False),
            (
                "See docs/05.operations/guides/01-common/0001-a.md.",
                False,
            ),
            (
                "See docs/05.operations/catalog/00-workspace/0001-a/guide.md. "
                "retired-route-record",
                False,
            ),
        )
        for text, rejected in cases:
            with self.subTest(text=text), self._repo() as directory:
                root = pathlib.Path(directory)
                (root / "active.md").write_text(text + "\n", encoding="utf-8")
                subprocess.run(["git", "add", "active.md"], cwd=root, check=True)
                codes = {
                    finding.code
                    for finding in validate_active_operations_references(root)
                }
                self.assertEqual(
                    rejected, "active-operations-reference-invalid" in codes
                )

    def test_active_scan_allows_deletion_but_rejects_nonregular_tracked_paths(
        self,
    ) -> None:
        mutations = ("broken-symlink", "directory")
        for mutation in mutations:
            with self.subTest(mutation=mutation), self._repo() as directory:
                root = pathlib.Path(directory)
                path = root / "tracked.md"
                path.write_text("tracked", encoding="utf-8")
                subprocess.run(["git", "add", "tracked.md"], cwd=root, check=True)
                subprocess.run(
                    ["git", "commit", "-qm", "fixture"], cwd=root, check=True
                )
                path.unlink()
                if mutation == "broken-symlink":
                    path.symlink_to("missing.md")
                elif mutation == "directory":
                    path.mkdir()
                with self.assertRaises(OperationsAuthorityError):
                    validate_active_operations_references(root)

        with self._repo() as directory:
            root = pathlib.Path(directory)
            path = root / "tracked.md"
            path.write_text("tracked", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.md"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            path.unlink()
            self.assertEqual((), validate_active_operations_references(root))


class ComposeProfileVocabularyTests(unittest.TestCase):
    POLICY = "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md"
    REQUIRED_HOME = (
        "core",
        "mng",
        "ai",
        "workflow",
        "obs-core",
        "obs-host",
        "availability",
        "logs",
        "alerting",
        "storage",
    )

    def _repo(
        self,
        *,
        include: tuple[str, ...] = (
            "infra/a/docker-compose.yml",
            "infra/b/docker-compose.cluster.yaml",
        ),
        services_b: str = "  z:\n    profiles: [beta]\n",
        services_a: str = (
            "  x:\n    profiles: [alpha, dev]\n  y:\n    profiles: [alpha]\n"
        ),
        header: str = "| Profile | Category | Purpose | Selected services | 서비스 |",
        rows: tuple[str, ...] = (
            "| `alpha` | domain | a | `x`, `y` | 2 |",
            "| `dev` | baseline | a | `x` | 1 |",
            "| `beta` | domain | b | `z` | 1 |",
        ),
    ) -> pathlib.Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = pathlib.Path(directory.name)
        home_base_profiles = tuple(
            profile for profile in self.REQUIRED_HOME if profile != "dev"
        )
        required_categories = {
            "core": "baseline",
            "mng": "role",
            "ai": "domain",
            "workflow": "domain",
            "obs-core": "capability",
            "obs-host": "capability",
            "availability": "capability",
            "logs": "capability",
            "alerting": "capability",
            "storage": "role",
        }
        count_cell = " | 1" if "서비스" in header or "Services" in header else ""
        required_rows = tuple(
            f"| `{profile}` | {required_categories[profile]} | HOME fixture | "
            f"`home-base`{count_cell} |"
            for profile in home_base_profiles
        )
        files = {
            "docker-compose.yml": "include:\n"
            + "".join(f"  - {item}\n" for item in include),
            "infra/a/docker-compose.yml": (
                "services:\n"
                + services_a
                + "  home-base:\n    profiles: ["
                + ", ".join(home_base_profiles)
                + "]\n"
            ),
            "infra/b/docker-compose.cluster.yaml": "services:\n" + services_b,
            self.POLICY: "\n".join(
                (
                    header,
                    "| --- | --- | --- | --- | ---: |",
                    *rows,
                    *required_rows,
                    "",
                    "| Named selection | Profiles | Forbidden categories |",
                    "| --- | --- | --- |",
                    "| HOME | "
                    + ", ".join(f"`{profile}`" for profile in self.REQUIRED_HOME)
                    + " | `automation`, `lifecycle`, `topology` |",
                    "",
                    "| 쌍 | 충돌 | 근거 |",
                    "| --- | --- | --- |",
                    "| `alpha` ↔ `beta` | host port 80 | 대체재 |",
                    "",
                )
            ),
        }
        for relative, text in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        return root

    def _findings(self, root: pathlib.Path) -> list[tuple[str, str, str]]:
        return [
            (finding.code, finding.path, finding.message)
            for finding in validate_compose_profile_vocabulary(root)
        ]

    def _set_home_profiles(self, root: pathlib.Path, profiles: tuple[str, ...]) -> None:
        policy = root / self.POLICY
        current = ", ".join(f"`{profile}`" for profile in self.REQUIRED_HOME)
        replacement = ", ".join(f"`{profile}`" for profile in profiles)
        text = policy.read_text(encoding="utf-8")
        self.assertIn(f"| HOME | {current} |", text)
        policy.write_text(
            text.replace(
                f"| HOME | {current} |",
                f"| HOME | {replacement} |",
                1,
            ),
            encoding="utf-8",
        )

    def _add_overlay(
        self,
        root: pathlib.Path,
        model: object,
        *,
        name: str = "infra/a/compose.workflow.override.yml",
    ) -> pathlib.Path:
        overlay = root / name
        overlay.parent.mkdir(parents=True, exist_ok=True)
        overlay.write_text(yaml.safe_dump(model, sort_keys=False), encoding="utf-8")
        subprocess.run(["git", "add", str(overlay)], cwd=root, check=True)
        return overlay

    def _add_overlay_text(
        self,
        root: pathlib.Path,
        text: str,
        *,
        name: str = "infra/a/compose.workflow.override.yml",
    ) -> pathlib.Path:
        overlay = root / name
        overlay.parent.mkdir(parents=True, exist_ok=True)
        overlay.write_text(text, encoding="utf-8")
        subprocess.run(["git", "add", str(overlay)], cwd=root, check=True)
        return overlay

    def test_standalone_lab_profile_is_catalogued_but_excluded_from_root(self) -> None:
        root = self._repo()
        lab = root / "labs/cluster.yml"
        lab.parent.mkdir()
        lab.write_text(
            "name: isolated-lab\nservices:\n  lab-node:\n    profiles: [lab-cluster]\n",
            encoding="utf-8",
        )
        policy = root / self.POLICY
        policy.write_text(
            policy.read_text(encoding="utf-8").replace(
                "| `beta` | domain | b | `z` | 1 |",
                "| `beta` | domain | b | `z` | 1 |\n"
                "| `lab-cluster` | topology | isolated LAB | `lab-node` | 1 |",
                1,
            ),
            encoding="utf-8",
        )
        self.assertEqual([], self._findings(root))
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8") + "  - labs/cluster.yml\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any(
                code == "compose-include-drift" and "labs/cluster.yml" in message
                for code, _, message in self._findings(root)
            )
        )

    def test_semantic_table_has_no_manual_counts(self) -> None:
        root = self._repo(
            header="| Profile | Category | Purpose | Selected services |",
            rows=(
                "| `alpha` | domain | alpha services | `x`, `y` |",
                "| `dev` | baseline | development selection | `x` |",
                "| `beta` | capability | beta services | `z` |",
            ),
        )
        self.assertEqual([], self._findings(root))

    def test_semantic_columns_are_required(self) -> None:
        for row, message in (
            ("| `alpha` | invalid | alpha services | `x`, `y` |", "no valid category"),
            ("| `alpha` | domain | | `x`, `y` |", "no purpose"),
            (
                "| `alpha` | domain,baseline | alpha services | `x`, `y` |",
                "no valid category",
            ),
        ):
            with self.subTest(row=row):
                root = self._repo(
                    header="| Profile | Category | Purpose | Selected services |",
                    rows=(
                        row,
                        "| `dev` | baseline | development | `x` |",
                        "| `beta` | capability | beta services | `z` |",
                    ),
                )
                self.assertTrue(
                    any(message in finding[2] for finding in self._findings(root))
                )

    def _conftest_repo(self) -> pathlib.Path:
        root = self._repo()
        dockerfile = root / "infra/a/Dockerfile"
        dockerfile.write_text("FROM busybox:1.37\n", encoding="utf-8")
        subprocess.run(["git", "add", str(dockerfile)], cwd=root, check=True)
        return root

    def test_conftest_context_inherits_profiles_without_changing_other_fields(self):
        root = self._conftest_repo()
        overlay = self._add_overlay_text(
            root,
            "x-hyhome-overlay: {version: 1, base: infra/a/docker-compose.yml}\n"
            "services:\n  x:\n    secrets: !override [monitor]\n"
            "    privileged: true\n    ports: ['8080:80']\n"
            "    environment: {DB_PASSWORD: literal-fixture}\n",
        )
        before = overlay.read_bytes()
        relative = pathlib.PurePosixPath(overlay.relative_to(root).as_posix())
        context = operations_catalog.conftest_source_context(root)
        original = operations_catalog._compose_mapping(root, relative)
        projected = context["overlay_inputs"][relative]
        self.assertEqual(["alpha", "dev"], projected["services"]["x"]["profiles"])
        restored = {
            **projected,
            "services": {
                name: {
                    key: value for key, value in service.items() if key != "profiles"
                }
                for name, service in projected["services"].items()
            },
        }
        self.assertEqual(dict(original), restored)
        self.assertEqual(before, overlay.read_bytes())
        self.assertIn(relative, context["compose"])
        self.assertIn(relative, context["overlays"])
        self.assertNotIn(relative, context["regular"])
        self.assertEqual(
            (pathlib.PurePosixPath("infra/a/Dockerfile"),), context["dockerfiles"]
        )

    def test_conftest_context_resolves_root_overlay_service_origin(self):
        root = self._conftest_repo()
        overlay = self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {"x": {"networks": {"private": {}}}},
                "networks": {"private": {"internal": True}},
            },
        )
        relative = pathlib.PurePosixPath(overlay.relative_to(root).as_posix())
        context = operations_catalog.conftest_source_context(root)
        self.assertEqual(
            ["alpha", "dev"],
            context["overlay_inputs"][relative]["services"]["x"]["profiles"],
        )

    def test_conftest_context_does_not_read_ignored_install_artifacts(self):
        root = self._conftest_repo()
        (root / ".gitignore").write_text("/infra/cache/\n", encoding="utf-8")
        ignored = root / "infra/cache"
        ignored.mkdir()
        (ignored / "Dockerfile").write_text("FROM alpine:edge\n", encoding="utf-8")
        (ignored / "compose.yml").write_text(
            "x-hyhome-overlay: malformed\n", encoding="utf-8"
        )
        read = operations_catalog.read_bounded_regular

        def checked_read(source_root, relative, **kwargs):
            self.assertFalse(relative.as_posix().startswith("infra/cache/"))
            return read(source_root, relative, **kwargs)

        with mock.patch.object(
            operations_catalog, "read_bounded_regular", checked_read
        ):
            context = operations_catalog.conftest_source_context(root)
        self.assertFalse(any("cache" in path.parts for path in context["compose"]))
        self.assertFalse(any("cache" in path.parts for path in context["dockerfiles"]))

    def test_conftest_context_rejects_nonignored_untracked_candidates(self):
        for relative in (
            "infra/new/Dockerfile",
            "infra/new/compose.yml",
            "labs/new.yml",
        ):
            with self.subTest(path=relative):
                root = self._conftest_repo()
                candidate = root / relative
                candidate.parent.mkdir(parents=True, exist_ok=True)
                candidate.write_text("services: {}\n", encoding="utf-8")
                with self.assertRaises(OperationsAuthorityError):
                    operations_catalog.conftest_source_context(root)

    def test_conftest_context_rejects_invalid_profiles_and_ambiguous_root(self):
        for mutation in ("empty", "string", "non-string", "ambiguous"):
            with self.subTest(mutation=mutation):
                root = self._conftest_repo()
                self._add_overlay(
                    root,
                    {
                        "x-hyhome-overlay": {
                            "version": 1,
                            "base": "docker-compose.yml",
                        },
                        "services": {"x": {"networks": {"private": {}}}},
                        "networks": {"private": {"internal": True}},
                    },
                )
                path = root / "infra/a/docker-compose.yml"
                if mutation == "ambiguous":
                    path = root / "infra/b/docker-compose.cluster.yaml"
                    path.write_text(path.read_text() + "  x: {profiles: [alpha]}\n")
                else:
                    value = {"empty": "[]", "string": "alpha", "non-string": "[1]"}[
                        mutation
                    ]
                    path.write_text(path.read_text().replace("[alpha, dev]", value, 1))
                with self.assertRaises(OperationsAuthorityError):
                    operations_catalog.conftest_source_context(root)

    def test_conftest_context_keeps_ordinary_missing_profile_unpromoted(self):
        root = self._conftest_repo()
        path = root / "infra/a/docker-compose.yml"
        path.write_text(path.read_text() + "  missing: {image: 'busybox:1.37'}\n")
        context = operations_catalog.conftest_source_context(root)
        self.assertIn(
            pathlib.PurePosixPath("infra/a/docker-compose.yml"), context["compose"]
        )
        self.assertFalse(context["overlay_inputs"])
        self.assertNotIn(
            "profiles",
            operations_catalog._compose_mapping(
                root, pathlib.PurePosixPath("infra/a/docker-compose.yml")
            )["services"]["missing"],
        )

    def test_conftest_context_rejects_tracked_symlink_dockerfiles(self):
        root = self._conftest_repo()
        path = root / "infra/a/Dockerfile"
        path.unlink()
        path.symlink_to(root / "docker-compose.yml")
        subprocess.run(["git", "add", str(path)], cwd=root, check=True)
        with self.assertRaises(OperationsAuthorityError):
            operations_catalog.conftest_source_context(root)

    def test_matching_fixture_has_no_findings(self) -> None:
        self.assertEqual([], self._findings(self._repo()))

    def test_typed_overlay_is_not_a_root_include_or_profile_authority(self) -> None:
        root = self._repo()
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {
                    "version": 1,
                    "base": "infra/a/docker-compose.yml",
                },
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
        )

        self.assertEqual([], self._findings(root))

    def test_root_overlay_can_join_root_services_to_new_internal_network(
        self,
    ) -> None:
        root = self._repo()
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {
                    "x": {"networks": {"capture": {}}},
                    "z": {"networks": {"capture": {}}},
                },
                "networks": {"capture": {"internal": True}},
            },
        )

        self.assertEqual([], self._findings(root))

    def test_root_overlay_rejects_compose_replacement_tags(self) -> None:
        tagged_documents = (
            """x-hyhome-overlay:
  version: 1
  base: docker-compose.yml
services: !override
  x:
    networks:
      capture: {}
networks:
  capture:
    internal: true
""",
            """x-hyhome-overlay:
  version: 1
  base: docker-compose.yml
services:
  x: !reset
    networks:
      capture: {}
networks:
  capture:
    internal: true
""",
            """x-hyhome-overlay:
  version: 1
  base: docker-compose.yml
services:
  x:
    networks: !override
      capture: {}
networks:
  capture:
    internal: true
""",
            """x-hyhome-overlay:
  version: 1
  base: docker-compose.yml
services:
  x:
    networks:
      capture: {}
networks: !reset
  capture:
    internal: true
""",
        )
        for index, document in enumerate(tagged_documents):
            with self.subTest(index=index):
                root = self._repo()
                self._add_overlay_text(root, document)

                with self.assertRaises(OperationsAuthorityError) as raised:
                    validate_compose_profile_vocabulary(root)
                self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_compose_tag_lookalikes_and_leaf_overlay_tags_remain_compatible(
        self,
    ) -> None:
        root = self._repo()
        self._add_overlay_text(
            root,
            """# !reset is documentation, not a YAML tag.
x-hyhome-overlay:
  version: 1
  base: docker-compose.yml
x-note: "!override"
services:
  x:
    networks:
      capture: {}
networks:
  capture:
    internal: true
""",
        )
        self.assertEqual([], self._findings(root))

        root = self._repo()
        self._add_overlay_text(
            root,
            """x-hyhome-overlay:
  version: 1
  base: infra/a/docker-compose.yml
services:
  x:
    build: !reset
      context: .
""",
        )
        self.assertEqual([], self._findings(root))

    def test_root_overlay_is_validated_from_an_infra_only_caller_subset(self) -> None:
        root = self._repo()
        overlay = self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {
                    "x": {"networks": {"capture": {}}},
                    "z": {"networks": {"capture": {}}},
                },
                "networks": {"capture": {"internal": True}},
            },
        )
        sources = operations_catalog._compose_sources(
            root,
            (
                pathlib.PurePosixPath("infra/a/docker-compose.yml"),
                pathlib.PurePosixPath("infra/b/docker-compose.cluster.yaml"),
                pathlib.PurePosixPath(overlay.relative_to(root).as_posix()),
            ),
        )

        self.assertEqual(
            (pathlib.PurePosixPath("infra/a/compose.workflow.override.yml"),),
            sources.overlays,
        )

    def test_compose_sources_without_overlays_do_not_require_a_root_model(
        self,
    ) -> None:
        root = self._repo()
        (root / "docker-compose.yml").unlink()

        sources = operations_catalog._compose_sources(
            root,
            (
                pathlib.PurePosixPath("infra/a/docker-compose.yml"),
                pathlib.PurePosixPath("infra/b/docker-compose.cluster.yaml"),
            ),
        )

        self.assertEqual((), sources.overlays)

    def test_root_overlay_network_and_membership_fail_closed(self) -> None:
        annotation = {"version": 1, "base": "docker-compose.yml"}
        invalid_models = (
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": [],
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": {},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": None,
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": {"capture": None},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": {"capture": {"internal": False}},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"capture": {}}}},
                "networks": {"capture": {"internal": 1}},
            },
            *(
                {
                    "x-hyhome-overlay": annotation,
                    "services": {"x": {"networks": {"capture": {}}}},
                    "networks": {"capture": {"internal": True, field: value}},
                }
                for field, value in (
                    ("external", True),
                    ("name", "capture"),
                    ("driver", "bridge"),
                    ("driver_opts", {}),
                    ("ipam", {}),
                    ("attachable", True),
                    ("unknown", True),
                )
            ),
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"image": "example/x:2.0.0"}},
                "networks": {"capture": {"internal": True}},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
            *(
                {
                    "x-hyhome-overlay": annotation,
                    "services": {"x": {"networks": {"capture": {}}, field: value}},
                    "networks": {"capture": {"internal": True}},
                }
                for field, value in (
                    ("privileged", True),
                    ("image", "example/x:2.0.0"),
                    ("build", "."),
                    ("command", ["worker"]),
                    ("entrypoint", ["/entrypoint"]),
                    ("ports", ["10000:10000"]),
                    ("volumes", ["./data:/data"]),
                    ("secrets", ["worker_secret"]),
                    ("depends_on", ["z"]),
                    ("network_mode", "host"),
                )
            ),
            {
                "x-hyhome-overlay": annotation,
                "services": {
                    "x": {"networks": {"capture": {"aliases": ["capture-x"]}}}
                },
                "networks": {"capture": {"internal": True}},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": ["capture"]}},
                "networks": {"capture": {"internal": True}},
            },
            *(
                {
                    "x-hyhome-overlay": annotation,
                    "services": {"x": {"networks": {"capture": {field: value}}}},
                    "networks": {"capture": {"internal": True}},
                }
                for field, value in (
                    ("aliases", ["capture-x"]),
                    ("ipv4_address", "10.0.0.2"),
                    ("priority", 1),
                )
            ),
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"networks": {"undeclared": {}}}},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"new-service": {"networks": {"capture": {}}}},
                "networks": {"capture": {"internal": True}},
            },
            {
                "x-hyhome-overlay": annotation,
                "services": {"x": {"profiles": ["alpha"]}},
            },
            {
                "x-hyhome-overlay": {"version": 1, "base": "compose.yml"},
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
        )
        for index, model in enumerate(invalid_models):
            with self.subTest(index=index):
                root = self._repo()
                self._add_overlay(root, model)
                with self.assertRaises(OperationsAuthorityError) as raised:
                    validate_compose_profile_vocabulary(root)
                self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_root_overlay_cannot_redefine_a_root_network(self) -> None:
        root = self._repo()
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8")
            + "networks:\n  root_net:\n    internal: true\n",
            encoding="utf-8",
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {"x": {"networks": {"root_net": {}}}},
                "networks": {"root_net": {"internal": True}},
            },
        )

        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_root_overlay_cannot_redefine_an_included_leaf_network(self) -> None:
        root = self._repo()
        leaf = root / "infra/a/docker-compose.yml"
        leaf.write_text(
            leaf.read_text(encoding="utf-8") + "networks:\n  leaf_net: {}\n",
            encoding="utf-8",
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {"x": {"networks": {"leaf_net": {}}}},
                "networks": {"leaf_net": {"internal": True}},
            },
        )

        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_root_overlay_cannot_redefine_the_implicit_default_network(self) -> None:
        root = self._repo()
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {"x": {"networks": {"default": {}}}},
                "networks": {"default": {"internal": True}},
            },
        )

        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_each_root_overlay_service_must_join_a_new_internal_network(
        self,
    ) -> None:
        root = self._repo()
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8") + "networks:\n  root_net: {}\n",
            encoding="utf-8",
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {
                    "x": {"networks": {"capture": {}}},
                    "z": {"networks": {"root_net": {}}},
                },
                "networks": {"capture": {"internal": True}},
            },
        )

        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_root_overlay_cannot_target_a_root_direct_service(self) -> None:
        root = self._repo()
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8")
            + "services:\n  root-only:\n    profiles: [alpha]\n",
            encoding="utf-8",
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": "docker-compose.yml"},
                "services": {"root-only": {"networks": {"capture": {}}}},
                "networks": {"capture": {"internal": True}},
            },
        )

        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_root_overlay_base_must_be_tracked_and_non_overlay(self) -> None:
        for mutation in ("untracked", "overlay"):
            with self.subTest(mutation=mutation):
                root = self._repo()
                if mutation == "untracked":
                    subprocess.run(
                        ["git", "rm", "--cached", "docker-compose.yml"],
                        cwd=root,
                        check=True,
                        capture_output=True,
                    )
                else:
                    compose = root / "docker-compose.yml"
                    compose.write_text(
                        compose.read_text(encoding="utf-8")
                        + "x-hyhome-overlay:\n  version: 1\n  base: docker-compose.yml\n",
                        encoding="utf-8",
                    )
                self._add_overlay(
                    root,
                    {
                        "x-hyhome-overlay": {
                            "version": 1,
                            "base": "docker-compose.yml",
                        },
                        "services": {"x": {"image": "example/x:2.0.0"}},
                    },
                )

                with self.assertRaises(OperationsAuthorityError) as raised:
                    validate_compose_profile_vocabulary(root)
                self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_overlay_annotation_version_and_base_fail_closed(self) -> None:
        invalid_annotations = (
            None,
            {"version": True, "base": "infra/a/docker-compose.yml"},
            {"version": 2, "base": "infra/a/docker-compose.yml"},
            {"version": 1},
            {"version": 1, "base": None},
            {"version": 1, "base": ""},
            {
                "version": 1,
                "base": "infra/a/docker-compose.yml",
                "unknown": "field",
            },
            {"version": 1, "base": "/infra/a/docker-compose.yml"},
            {"version": 1, "base": "infra/a/../a/docker-compose.yml"},
            {"version": 1, "base": "infra/a/missing-compose.yml"},
            {"version": 1, "base": "infra/b/docker-compose.cluster.yaml"},
        )
        for annotation in invalid_annotations:
            with self.subTest(annotation=annotation):
                root = self._repo(include=("infra/a/docker-compose.yml",))
                self._add_overlay(
                    root,
                    {
                        "x-hyhome-overlay": annotation,
                        "services": {"x": {"image": "example/x:2.0.0"}},
                    },
                )
                with self.assertRaises(OperationsAuthorityError):
                    validate_compose_profile_vocabulary(root)

    def test_overlay_top_level_and_service_membership_are_closed(self) -> None:
        valid_annotation = {
            "version": 1,
            "base": "infra/a/docker-compose.yml",
        }
        invalid_models = (
            *(
                {
                    "x-hyhome-overlay": valid_annotation,
                    "services": {"x": {"image": "example/x:2.0.0"}},
                    field: {},
                }
                for field in (
                    "include",
                    "name",
                    "networks",
                    "volumes",
                    "secrets",
                    "configs",
                    "profiles",
                )
            ),
            {"x-hyhome-overlay": valid_annotation, "services": {}},
            {"x-hyhome-overlay": valid_annotation, "services": []},
            {
                "x-hyhome-overlay": valid_annotation,
                "services": {"new-service": {"image": "example/new:1.0.0"}},
            },
            {
                "x-hyhome-overlay": valid_annotation,
                "services": {"x": {"profiles": ["alpha"]}},
            },
            {
                "x-hyhome-overlay": valid_annotation,
                "services": {1: {"image": "example/x:2.0.0"}},
            },
            {
                "x-hyhome-overlay": valid_annotation,
                "services": {"": {"image": "example/x:2.0.0"}},
            },
            {"x-hyhome-overlay": valid_annotation, "services": {"x": "invalid"}},
        )
        for index, model in enumerate(invalid_models):
            with self.subTest(index=index):
                root = self._repo()
                self._add_overlay(root, model)
                with self.assertRaises(OperationsAuthorityError) as raised:
                    validate_compose_profile_vocabulary(root)
                self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_overlay_service_runtime_fields_do_not_become_catalog_authority(
        self,
    ) -> None:
        root = self._repo()
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {
                    "version": 1,
                    "base": "infra/a/docker-compose.yml",
                },
                "x-purpose": "isolated merge input",
                "services": {
                    "x": {
                        "image": "example/x:2.0.0",
                        "build": {"context": "."},
                        "pull_policy": "never",
                        "command": ["worker"],
                        "entrypoint": ["/entrypoint"],
                        "user": "1000:0",
                        "ports": ["127.0.0.1:10000:10000"],
                        "secrets": ["worker_secret"],
                        "depends_on": ["y"],
                        "volumes": ["./code:/opt/code:ro"],
                        "networks": ["workflow"],
                    }
                },
            },
        )

        self.assertEqual([], self._findings(root))

    def test_unannotated_override_remains_a_regular_compose_source(self) -> None:
        root = self._repo()
        self._add_overlay(
            root,
            {"services": {"x": {"image": "example/x:2.0.0"}}},
        )
        findings = self._findings(root)
        self.assertTrue(any(code == "compose-include-drift" for code, _, _ in findings))
        self.assertTrue(
            any(code == "compose-service-profile-missing" for code, _, _ in findings)
        )

    def test_root_include_cannot_select_a_typed_overlay(self) -> None:
        root = self._repo(
            include=(
                "infra/a/docker-compose.yml",
                "infra/b/docker-compose.cluster.yaml",
                "infra/a/compose.workflow.override.yml",
            )
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {
                    "version": 1,
                    "base": "infra/a/docker-compose.yml",
                },
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
        )
        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_overlay_base_cannot_be_an_overlay_or_symlink(self) -> None:
        root = self._repo()
        first = "infra/a/compose.first.override.yml"
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {
                    "version": 1,
                    "base": "infra/a/docker-compose.yml",
                },
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
            name=first,
        )
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {"version": 1, "base": first},
                "services": {"x": {"image": "example/x:3.0.0"}},
            },
            name="infra/a/compose.second.override.yml",
        )
        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

        root = self._repo()
        linked_base = root / "infra/link/docker-compose.yml"
        linked_base.parent.mkdir(parents=True)
        linked_base.symlink_to("../a/docker-compose.yml")
        subprocess.run(["git", "add", str(linked_base)], cwd=root, check=True)
        self._add_overlay(
            root,
            {
                "x-hyhome-overlay": {
                    "version": 1,
                    "base": "infra/link/docker-compose.yml",
                },
                "services": {"x": {"image": "example/x:2.0.0"}},
            },
        )
        with self.assertRaises(OperationsAuthorityError) as raised:
            validate_compose_profile_vocabulary(root)
        self.assertEqual("symlink-invalid", raised.exception.code)

    def test_tracked_missing_and_broken_symlink_compose_fail_closed(self) -> None:
        for mutation in ("missing", "broken-symlink"):
            with self.subTest(mutation=mutation):
                root = self._repo()
                overlay = self._add_overlay(
                    root,
                    {
                        "x-hyhome-overlay": {
                            "version": 1,
                            "base": "infra/a/docker-compose.yml",
                        },
                        "services": {"x": {"image": "example/x:2.0.0"}},
                    },
                )
                overlay.unlink()
                if mutation == "broken-symlink":
                    overlay.symlink_to("missing-compose.yml")
                with self.assertRaises(OperationsAuthorityError) as raised:
                    validate_compose_profile_vocabulary(root)
                self.assertIn(
                    raised.exception.code,
                    {"file-unreadable", "symlink-invalid"},
                )

    def test_declared_profile_without_a_row_is_rejected(self) -> None:
        root = self._repo(services_b="  z:\n    profiles: [beta, gamma]\n")
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    self.POLICY,
                    "profile gamma is declared by 1 service(s) and has no row",
                )
            ],
            self._findings(root),
        )

    def test_row_that_no_service_declares_is_rejected(self) -> None:
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `retired` | domain | none | `retired-service` | 3 |",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    f"{self.POLICY}:6",
                    "profile retired has a row and no tracked Compose service declares it",
                )
            ],
            self._findings(root),
        )

    def test_service_count_that_differs_from_compose_is_rejected(self) -> None:
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 3 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    f"{self.POLICY}:3",
                    "profile alpha row counts 3 service(s); Compose declares 2",
                )
            ],
            self._findings(root),
        )

    def test_tracked_compose_file_missing_from_root_include_is_rejected(self) -> None:
        root = self._repo(include=("infra/a/docker-compose.yml",))
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8")
            + "  # - infra/b/docker-compose.cluster.yaml\n",
            encoding="utf-8",
        )
        self.assertEqual(
            [
                (
                    "compose-include-drift",
                    "docker-compose.yml",
                    "infra/b/docker-compose.cluster.yaml is tracked and not included",
                )
            ],
            self._findings(root),
        )

    def test_standard_compose_file_missing_from_root_include_is_rejected(
        self,
    ) -> None:
        root = self._repo()
        standard = root / "infra/c/compose.yaml"
        standard.parent.mkdir()
        standard.write_text("services: {}\n", encoding="utf-8")
        subprocess.run(["git", "add", "infra/c/compose.yaml"], cwd=root, check=True)
        self.assertIn(
            (
                "compose-include-drift",
                "docker-compose.yml",
                "infra/c/compose.yaml is tracked and not included",
            ),
            self._findings(root),
        )

    def test_zero_depth_standard_compose_missing_from_root_include_is_rejected(
        self,
    ) -> None:
        root = self._repo()
        standard = root / "infra/compose.yaml"
        standard.write_text("services: {}\n", encoding="utf-8")
        subprocess.run(["git", "add", "infra/compose.yaml"], cwd=root, check=True)
        self.assertIn(
            (
                "compose-include-drift",
                "docker-compose.yml",
                "infra/compose.yaml is tracked and not included",
            ),
            self._findings(root),
        )

    def test_standard_compose_file_profiles_are_in_vocabulary_scope(self) -> None:
        root = self._repo()
        standard = root / "infra/c/compose.yaml"
        standard.parent.mkdir()
        standard.write_text(
            "services:\n  standard:\n    profiles: [unregistered]\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "infra/c/compose.yaml"], cwd=root, check=True)
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8") + "  - infra/c/compose.yaml\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any(
                finding[0] == "compose-profile-vocabulary-drift"
                and "profile unregistered" in finding[2]
                for finding in self._findings(root)
            )
        )

    def test_zero_depth_standard_compose_profiles_are_in_vocabulary_scope(
        self,
    ) -> None:
        root = self._repo()
        standard = root / "infra/compose.yaml"
        standard.write_text(
            "services:\n  standard:\n    profiles: [unregistered]\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "infra/compose.yaml"], cwd=root, check=True)
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8") + "  - infra/compose.yaml\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any(
                finding[0] == "compose-profile-vocabulary-drift"
                and "profile unregistered" in finding[2]
                for finding in self._findings(root)
            )
        )

    def test_include_entry_that_is_not_a_tracked_compose_file_is_rejected(
        self,
    ) -> None:
        root = self._repo(
            include=(
                "infra/a/docker-compose.yml",
                "infra/b/docker-compose.cluster.yaml",
                "infra/c/docker-compose.yml",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-include-drift",
                    "docker-compose.yml",
                    "infra/c/docker-compose.yml is included and is not a tracked "
                    "Compose file under infra/",
                )
            ],
            self._findings(root),
        )

    def test_unparseable_compose_file_raises_authority_error(self) -> None:
        root = self._repo(services_b="  z: [unclosed\n")
        with self.assertRaisesRegex(OperationsAuthorityError, "cluster.yaml"):
            validate_compose_profile_vocabulary(root)

    def test_duplicate_row_is_rejected_even_when_the_first_row_matches(self) -> None:
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `alpha` | domain | again | `wrong` | 9 |",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    f"{self.POLICY}:6",
                    "profile alpha has more than one row; the first is line 3",
                )
            ],
            self._findings(root),
        )

    def test_row_without_an_integer_count_is_rejected(self) -> None:
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `y` | two |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    f"{self.POLICY}:3",
                    "profile alpha row has no integer service count",
                )
            ],
            self._findings(root),
        )

    def test_non_ascii_digit_count_is_rejected_rather_than_aborting(self) -> None:
        # "²".isdigit() is true and int("²") raises, which aborted the leaf.
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `y` | ² |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
            )
        )
        self.assertEqual(
            [
                (
                    "compose-profile-vocabulary-drift",
                    f"{self.POLICY}:3",
                    "profile alpha row has no integer service count",
                )
            ],
            self._findings(root),
        )

    def test_compose_merge_tags_and_an_empty_file_are_valid_input(self) -> None:
        root = self._repo(services_b="  z:\n    profiles: !reset [beta]\n")
        empty = root / "infra/c/docker-compose.yml"
        empty.parent.mkdir(parents=True)
        empty.write_text("", encoding="utf-8")
        compose = root / "docker-compose.yml"
        compose.write_text(
            compose.read_text(encoding="utf-8") + "  - infra/c/docker-compose.yml\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        self.assertEqual([], self._findings(root))

    def test_mapping_form_and_dot_prefixed_include_entries_are_read(self) -> None:
        root = self._repo()
        (root / "docker-compose.yml").write_text(
            "include:\n"
            "  - ./infra/a/docker-compose.yml\n"
            "  - path: infra/b/docker-compose.cluster.yaml\n",
            encoding="utf-8",
        )
        self.assertEqual([], self._findings(root))

    def test_underscore_profile_name_is_matched_to_its_row(self) -> None:
        root = self._repo(
            services_b="  z:\n    profiles: [beta_two]\n",
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta_two` | domain | b | `z` | 1 |",
            ),
        )
        self.assertEqual([], self._findings(root))

    def test_service_without_profiles_is_rejected(self) -> None:
        root = self._repo(services_b="  z:\n    profiles: [beta]\n  w:\n    image: x\n")
        self.assertEqual(
            [
                (
                    "compose-service-profile-missing",
                    "infra/b/docker-compose.cluster.yaml",
                    "service w declares no profile, so it starts when none is selected",
                )
            ],
            self._findings(root),
        )

    def test_same_count_membership_swap_reports_missing_and_unknown_services(
        self,
    ) -> None:
        root = self._repo(
            rows=(
                "| `alpha` | domain | a | `x`, `z` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
            )
        )
        messages = [message for _, _, message in self._findings(root)]
        self.assertIn(
            "profile alpha Selected services missing from policy: y", messages
        )
        self.assertIn("profile alpha Selected services unknown or extra: z", messages)

    def test_cross_profile_move_reports_both_rows(self) -> None:
        root = self._repo(
            services_a=(
                "  x:\n    profiles: [beta, dev]\n  y:\n    profiles: [alpha]\n"
            ),
            services_b="  z:\n    profiles: [beta]\n",
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
            ),
        )
        messages = [message for _, _, message in self._findings(root)]
        self.assertIn("profile alpha Selected services unknown or extra: x", messages)
        self.assertIn("profile beta Selected services missing from policy: x", messages)

    def test_duplicate_empty_and_malformed_selected_services_are_rejected(self) -> None:
        for selected, message in (
            ("`x`, `x`, `y`", "duplicates service x"),
            ("", "has empty Selected services"),
            ("`x`, y", "has malformed Selected services"),
        ):
            with self.subTest(selected=selected):
                root = self._repo(
                    rows=(
                        f"| `alpha` | domain | a | {selected} | 2 |",
                        "| `dev` | baseline | a | `x` | 1 |",
                        "| `beta` | domain | b | `z` | 1 |",
                    )
                )
                self.assertTrue(
                    any(message in finding[2] for finding in self._findings(root))
                )

    def test_selected_services_column_is_required_by_exact_name(self) -> None:
        for header in (
            "| Profile | Category | Purpose | 서비스 |",
            "| Profile | Category | Purpose | Selected service | 서비스 |",
        ):
            with self.subTest(header=header):
                root = self._repo(header=header)
                self.assertTrue(
                    any(
                        "table has no Selected services column" in finding[2]
                        for finding in self._findings(root)
                    )
                )

    def test_fixed_safety_category_relabels_are_rejected(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n"
                "  tofu:\n    profiles: [iac]\n"
                "  vault:\n    profiles: [legacy-vault]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `iac` | domain | iac | `tofu` | 1 |",
                "| `legacy-vault` | capability | vault | `vault` | 1 |",
            ),
        )
        messages = [message for _, _, message in self._findings(root)]
        self.assertIn(
            "profile iac must use safety category automation, found domain", messages
        )
        self.assertIn(
            "profile legacy-vault must use safety category lifecycle, found capability",
            messages,
        )

    def test_home_rejects_forbidden_profiles_and_dependency_escape(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n"
                "  runner:\n    profiles: [testing]\n"
                "  home-app:\n    profiles: [app]\n"
                "    depends_on: [outside]\n"
                "  outside:\n    profiles: [optional]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `testing` | automation | load | `runner` | 1 |",
                "| `app` | domain | home | `home-app` | 1 |",
                "| `optional` | capability | optional | `outside` | 1 |",
            ),
        )
        self._set_home_profiles(root, (*self.REQUIRED_HOME, "testing", "app"))
        messages = [message for _, _, message in self._findings(root)]
        self.assertTrue(
            any("HOME includes forbidden" in message for message in messages)
        )
        self.assertTrue(
            any("required dependency outside" in message for message in messages)
        )

    def test_home_rejects_topology_profile_and_unsafe_service_overlap(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n"
                "  shared:\n    profiles: [app, testing]\n"
                "  cluster:\n    profiles: [couchdb]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `app` | domain | home | `shared` | 1 |",
                "| `testing` | automation | load | `shared` | 1 |",
                "| `couchdb` | topology | cluster | `cluster` | 1 |",
            ),
        )
        self._set_home_profiles(root, (*self.REQUIRED_HOME, "app", "couchdb"))
        messages = [message for _, _, message in self._findings(root)]
        self.assertTrue(
            any("HOME includes forbidden" in message for message in messages)
        )
        self.assertTrue(
            any("HOME services overlap forbidden" in message for message in messages)
        )

    def test_home_allows_base_service_shared_with_unselected_topology(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n  shared:\n    profiles: [app, couchdb]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `app` | domain | home | `shared` | 1 |",
                "| `couchdb` | topology | cluster | `shared` | 1 |",
            ),
        )
        self._set_home_profiles(root, (*self.REQUIRED_HOME, "app"))
        self.assertEqual([], self._findings(root))

    def test_home_requires_the_current_spec_profile_set(self) -> None:
        cases = (
            (("core",), "ai"),
            (
                tuple(
                    profile for profile in self.REQUIRED_HOME if profile != "storage"
                ),
                "storage",
            ),
        )
        for profiles, missing in cases:
            with self.subTest(profiles=profiles):
                root = self._repo()
                self._set_home_profiles(root, profiles)
                self.assertTrue(
                    any(
                        "HOME is missing required profiles" in finding[2]
                        and missing in finding[2]
                        for finding in self._findings(root)
                    )
                )

    def test_compose_profile_name_home_is_reserved_case_insensitively(self) -> None:
        for reserved in ("home", "HOME", "HoMe"):
            with self.subTest(reserved=reserved):
                root = self._repo(
                    services_b=(
                        "  z:\n    profiles: [beta]\n"
                        f"  reserved:\n    profiles: [{reserved}]\n"
                    ),
                    rows=(
                        "| `alpha` | domain | a | `x`, `y` | 2 |",
                        "| `dev` | baseline | a | `x` | 1 |",
                        "| `beta` | domain | b | `z` | 1 |",
                        f"| `{reserved}` | domain | reserved | `reserved` | 1 |",
                    ),
                )
                self.assertTrue(
                    any(
                        f"profile {reserved} uses reserved HOME name" in finding[2]
                        for finding in self._findings(root)
                    )
                )

    def test_ksql_is_automation_and_cannot_join_home_or_tooling(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n"
                "  ksql-service:\n    profiles: [ksql, tooling]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `ksql` | automation | stream tooling | `ksql-service` | 1 |",
                "| `tooling` | domain | tools | `ksql-service` | 1 |",
            ),
        )
        self._set_home_profiles(root, (*self.REQUIRED_HOME, "ksql"))
        messages = [message for _, _, message in self._findings(root)]
        self.assertTrue(
            any(
                "HOME includes forbidden profiles: ksql" in message
                for message in messages
            )
        )
        self.assertTrue(
            any(
                "tooling overlaps automation/lifecycle profile ksql" in message
                for message in messages
            )
        )

    def test_tooling_is_disjoint_from_automation_profiles(self) -> None:
        root = self._repo(
            services_b=(
                "  z:\n    profiles: [beta]\n"
                "  runner:\n    profiles: [tooling, testing]\n"
            ),
            rows=(
                "| `alpha` | domain | a | `x`, `y` | 2 |",
                "| `dev` | baseline | a | `x` | 1 |",
                "| `beta` | domain | b | `z` | 1 |",
                "| `tooling` | domain | tools | `runner` | 1 |",
                "| `testing` | automation | load | `runner` | 1 |",
            ),
        )
        self.assertTrue(
            any(
                "tooling overlaps automation/lifecycle profile testing: runner"
                in finding[2]
                for finding in self._findings(root)
            )
        )


class ServiceInventoryTests(unittest.TestCase):
    def _repo(self, *, flat: bool = False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        self.compose = "infra/04-data/example/docker-compose.yml"
        domain = "" if flat else "/05-databases-and-storage"
        self.guide = f"docs/05.operations/guides{domain}/0001-example.md"
        self.policy = f"docs/05.operations/policies{domain}/0001-example.md"
        self.runbook = f"docs/05.operations/runbooks{domain}/0001-example.md"
        compose_link = (
            "../../../infra/04-data/example/docker-compose.yml"
            if flat
            else "../../../../infra/04-data/example/docker-compose.yml"
        )
        files = {
            self.compose: """services:
  database:
    profiles: [core]
    image: example/database:1.2.3
    extends: {file: ../../common-optimizations.yml, service: base}
    environment: {DATABASE_PASSWORD_FILE: /run/secrets/db_password}
    secrets: [db_password]
    networks: [infra_net]
    ports: ['127.0.0.1:${DB_PORT:-5432}:5432']
    volumes: ['db-data:/data']
  exporter:
    profiles: [core]
    image: example/exporter:1.0.0
    depends_on: [database]
    networks: [infra_net]
volumes:
  db-data:
    driver_opts: {device: '${DEFAULT_DATA_DIR}/database'}
""",
            "infra/common-optimizations.yml": """services:
  base:
    cpus: '0.50'
    mem_limit: 256m
    security_opt: [no-new-privileges:true]
    cap_drop: [ALL]
""",
            self.guide: """---
type: operation/guide
status: active
implementation_services:
  infra/04-data/example/docker-compose.yml: [database, exporter]
---
"""
            + f"[Compose]({compose_link})\n",
            self.policy: "---\ntype: operation/policy\nstatus: active\n---\n",
            self.runbook: "---\ntype: operation/runbook\nstatus: active\n---\n",
            "renovate.json5": "{}\n",
        }
        for name, value in files.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value)
        self.paths = tuple(pathlib.PurePosixPath(name) for name in files)
        patcher = mock.patch.object(
            operations_catalog, "_tracked_paths", return_value=self.paths
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        rows = []
        for service in ("database", "exporter"):
            rows.append(
                {
                    "Compose path": self.compose,
                    "Service": service,
                    "Runtime classification": "HOME",
                    "Consumer": "Owner-required HOME; runtime activity unverified",
                    "Security": "Policy review; runtime security unverified",
                    "Backup": "Required: database state and configuration; isolated restore unverified",
                    "Disposition": "retain; required HOME dependency",
                }
            )
        self.inventory = root / operations_catalog.SERVICE_INVENTORY_PATH
        self.inventory.parent.mkdir(parents=True, exist_ok=True)
        self._write_rows(rows)
        self.inventory.write_text(operations_catalog.render_service_inventory(root))
        return root

    def test_inventory_bindings_preserve_flat_primary_and_numbered_routes(self):
        for flat in (True, False):
            with self.subTest(flat=flat):
                root = self._repo(flat=flat)
                sources = operations_catalog._inventory_sources(root, self.paths)
                owners, findings = operations_catalog._inventory_bindings(
                    root, self.paths, sources
                )
                self.assertEqual([], findings)
                self.assertEqual(
                    pathlib.PurePosixPath(self.guide),
                    owners[(self.compose, "database")],
                )
                self.assertEqual(
                    pathlib.PurePosixPath(self.guide),
                    owners[(self.compose, "exporter")],
                )

    def _write_rows(self, rows):
        columns = operations_catalog.SERVICE_INVENTORY_COLUMNS
        text = "<!-- current-service-inventory:start -->\n"
        text += "| " + " | ".join(columns) + " |\n"
        text += "| " + " | ".join("---" for _ in columns) + " |\n"
        for row in rows:
            text += (
                "| "
                + " | ".join(row.get(column, "pending") for column in columns)
                + " |\n"
            )
        text += "<!-- current-service-inventory:end -->\n"
        self.inventory.write_text(text)

    def _change(self, column, value, index=0):
        rows = operations_catalog._service_inventory_rows(self.inventory.read_text())
        updated = [
            {**row, column: value} if i == index else row for i, row in enumerate(rows)
        ]
        self._write_rows(updated)

    def _codes(self, root):
        return {
            item.code for item in operations_catalog.validate_service_inventory(root)
        }

    def test_lab_guide_binding_is_valid_without_adding_lab_to_home_inventory(self):
        root = self._repo()
        lab_path = pathlib.PurePosixPath("labs/cluster.yml")
        lab = root / lab_path
        lab.parent.mkdir()
        lab.write_text(
            "name: hy-home-lab-cluster\nservices:\n  lab-node:\n"
            "    profiles: [lab-cluster]\n    image: example/node:1.0.0\n"
        )
        guide = root / self.guide
        guide.write_text(
            guide.read_text().replace(
                "  infra/04-data/example/docker-compose.yml: [database, exporter]",
                "  infra/04-data/example/docker-compose.yml: [database, exporter]\n"
                "  labs/cluster.yml: [lab-node]",
            )
            + "[LAB Compose](../../../../labs/cluster.yml)\n"
        )
        paths = (*self.paths, lab_path)
        with mock.patch.object(
            operations_catalog, "_tracked_paths", return_value=paths
        ):
            sources = operations_catalog._inventory_sources(root, paths)
            owners, findings = operations_catalog._inventory_bindings(
                root, paths, sources
            )
            self.assertEqual([], findings)
            self.assertEqual(
                pathlib.PurePosixPath(self.guide), owners[(str(lab_path), "lab-node")]
            )
            self.assertNotIn((str(lab_path), "lab-node"), sources)
            self.assertNotIn(
                "labs/cluster.yml", operations_catalog.render_service_inventory(root)
            )
            self.assertEqual(set(), self._codes(root))
            guide.write_text(guide.read_text().replace("[lab-node]", "[removed-node]"))
            self.assertIn("service-operations-removed", self._codes(root))

    def test_lab_binding_rejects_malformed_or_overlay_services(self):
        root = self._repo()
        lab_path = pathlib.PurePosixPath("labs/cluster.yml")
        lab = root / lab_path
        lab.parent.mkdir()
        guide = root / self.guide
        guide.write_text(
            guide.read_text().replace(
                "  infra/04-data/example/docker-compose.yml: [database, exporter]",
                "  infra/04-data/example/docker-compose.yml: [database, exporter]\n"
                "  labs/cluster.yml: [lab-node]",
            )
            + "[LAB Compose](../../../../labs/cluster.yml)\n"
        )
        paths = (*self.paths, lab_path)
        for model in (
            {"services": []},
            {"services": {"lab-node": "not-a-service"}},
            {"x-hyhome-overlay": {}, "services": {"lab-node": {}}},
        ):
            with (
                self.subTest(model=model),
                mock.patch.object(
                    operations_catalog, "_tracked_paths", return_value=paths
                ),
            ):
                lab.write_text(yaml.safe_dump(model))
                self.assertIn("service-operations-removed", self._codes(root))

    def test_lab_binding_does_not_follow_source_symlink(self):
        root = self._repo()
        lab_path = pathlib.PurePosixPath("labs/cluster.yml")
        lab = root / lab_path
        lab.parent.mkdir()
        lab.symlink_to(root / self.compose)
        guide = root / self.guide
        guide.write_text(
            guide.read_text().replace(
                "  infra/04-data/example/docker-compose.yml: [database, exporter]",
                "  infra/04-data/example/docker-compose.yml: [database, exporter]\n"
                "  labs/cluster.yml: [database]",
            )
            + "[LAB Compose](../../../../labs/cluster.yml)\n"
        )
        paths = (*self.paths, lab_path)
        with self.assertRaises(operations_catalog.OperationsAuthorityError):
            operations_catalog._inventory_bindings(
                root, paths, operations_catalog._inventory_sources(root, paths)
            )

    def test_bound_lab_source_requires_every_declared_service_owner(self):
        root = self._repo()
        lab_path = pathlib.PurePosixPath("labs/cluster.yml")
        lab = root / lab_path
        lab.parent.mkdir()
        guide = root / self.guide
        guide.write_text(
            guide.read_text().replace(
                "  infra/04-data/example/docker-compose.yml: [database, exporter]",
                "  infra/04-data/example/docker-compose.yml: [database, exporter]\n"
                "  labs/cluster.yml: [lab-node]",
            )
            + "[LAB Compose](../../../labs/cluster.yml)\n"
        )
        paths = (*self.paths, lab_path)
        for extra, expected in (
            ({"profiles": ["lab-cluster"]}, "service-operations-missing"),
            ("not-a-service", "service-operations-removed"),
        ):
            with (
                self.subTest(extra=extra),
                mock.patch.object(
                    operations_catalog, "_tracked_paths", return_value=paths
                ),
            ):
                lab.write_text(
                    yaml.safe_dump(
                        {
                            "services": {
                                "lab-node": {"profiles": ["lab-cluster"]},
                                "undocumented-node": extra,
                            }
                        }
                    )
                )
                self.assertIn(expected, self._codes(root))

    def test_untracked_lab_binding_is_rejected(self):
        root = self._repo()
        lab = root / "labs/cluster.yml"
        lab.parent.mkdir()
        lab.write_text("services: {lab-node: {profiles: [lab-cluster]}}\n")
        guide = root / self.guide
        guide.write_text(
            guide.read_text().replace(
                "  infra/04-data/example/docker-compose.yml: [database, exporter]",
                "  infra/04-data/example/docker-compose.yml: [database, exporter]\n"
                "  labs/cluster.yml: [lab-node]",
            )
            + "[LAB Compose](../../../labs/cluster.yml)\n"
        )
        self.assertIn("service-operations-removed", self._codes(root))

    def test_shared_operations_subject_and_source_projection_are_valid(self):
        root = self._repo()
        self.assertEqual(set(), self._codes(root))
        rows = operations_catalog._service_inventory_rows(self.inventory.read_text())
        database = next(row for row in rows if row["Service"] == "database")
        self.assertIn("DATABASE_PASSWORD_FILE", database["Env"])
        self.assertNotIn("/run/secrets", database["Env"])
        self.assertIn("db_password", database["Secret metadata"])
        self.assertIn("0.50", database["Resources"])
        self.assertIn("256m", database["Resources"])
        self.assertIn("${DEFAULT_DATA_DIR}", database["Persistence"])
        self.assertNotIn(str(root), self.inventory.read_text())
        self.assertNotIn("1.2.3", database["Runtime version authority"])

    def test_current_derived_cells_cannot_drift(self):
        root = self._repo()
        original = self.inventory.read_text()
        for field in (
            "Compose path",
            "Profiles",
            "Dependencies",
            "Network",
            "Ports",
            "Persistence",
            "Env",
            "Secret metadata",
            "Resources",
            "Operations docs",
            "Runtime version authority",
            "Update owner",
        ):
            with self.subTest(field=field):
                self.inventory.write_text(original)
                self._change(field, "wrong")
                self.assertTrue(self._codes(root))

    def test_missing_extra_and_duplicate_service_rows_are_rejected(self):
        root = self._repo()
        rows = operations_catalog._service_inventory_rows(self.inventory.read_text())
        for changed in (
            rows[:-1],
            [*rows, {**rows[0], "Service": "removed"}],
            [*rows, rows[0]],
        ):
            with self.subTest(rows=len(changed)):
                self._write_rows(changed)
                self.assertTrue(self._codes(root))

    def test_every_required_field_is_nonempty(self):
        root = self._repo()
        original = self.inventory.read_text()
        for field in operations_catalog.SERVICE_INVENTORY_COLUMNS:
            with self.subTest(field=field):
                self.inventory.write_text(original)
                self._change(field, "")
                self.assertIn("service-inventory-field", self._codes(root))

    def test_broken_triplet_and_missing_guide_source_are_rejected(self):
        root = self._repo()
        policy = root / self.policy
        original = policy.read_text()
        policy.unlink()
        self.assertIn("service-operations-owner", self._codes(root))
        policy.write_text(original)
        guide = root / self.guide
        guide.write_text(guide.read_text().split("[Compose]")[0])
        self.assertIn("service-guide-source", self._codes(root))

    def test_removed_service_current_guide_and_unowned_addition_are_rejected(self):
        root = self._repo()
        path = root / self.compose
        original = path.read_text()
        path.write_text(original.replace("  exporter:", "  replacement:"))
        codes = self._codes(root)
        self.assertIn("service-operations-removed", codes)
        self.assertIn("service-operations-missing", codes)

    def test_standard_compose_file_service_requires_operations_owner(self):
        root = self._repo()
        standard = pathlib.PurePosixPath("infra/04-data/example/compose.yaml")
        (root / standard).write_text(
            "services:\n"
            "  standard:\n"
            "    profiles: [core]\n"
            "    image: example/standard:1.0.0\n",
            encoding="utf-8",
        )
        with mock.patch.object(
            operations_catalog,
            "_tracked_paths",
            return_value=(*self.paths, standard),
        ):
            self.assertIn("service-operations-missing", self._codes(root))

    def test_typed_overlay_does_not_create_or_overwrite_inventory_rows(self):
        root = self._repo()
        overlay = pathlib.PurePosixPath(
            "infra/04-data/example/compose.workflow.override.yml"
        )
        (root / "docker-compose.yml").write_text(
            f"include:\n  - {self.compose}\n", encoding="utf-8"
        )
        (root / overlay).write_text(
            yaml.safe_dump(
                {
                    "x-hyhome-overlay": {"version": 1, "base": self.compose},
                    "services": {
                        "database": {
                            "image": "example/database:2.0.0",
                            "depends_on": ["exporter"],
                            "networks": ["overlay-only"],
                        }
                    },
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        tracked = (*self.paths, overlay)
        with mock.patch.object(
            operations_catalog, "_tracked_paths", return_value=tracked
        ):
            rendered = operations_catalog.render_service_inventory(root)
            rows = operations_catalog._service_inventory_rows(rendered)
            self.assertEqual({"database", "exporter"}, {row["Service"] for row in rows})
            database = next(row for row in rows if row["Service"] == "database")
            self.assertEqual("none", database["Dependencies"])
            self.assertNotIn("overlay-only", database["Network"])
            self.inventory.write_text(rendered, encoding="utf-8")
            self.assertEqual(set(), self._codes(root))

    def test_inventory_rejects_root_included_overlay(self):
        root = self._repo()
        overlay = pathlib.PurePosixPath(
            "infra/04-data/example/compose.workflow.override.yml"
        )
        (root / "docker-compose.yml").write_text(
            f"include:\n  - {self.compose}\n  - {overlay}\n", encoding="utf-8"
        )
        (root / overlay).write_text(
            yaml.safe_dump(
                {
                    "x-hyhome-overlay": {"version": 1, "base": self.compose},
                    "services": {"database": {"image": "example/database:2.0.0"}},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        with self.assertRaises(OperationsAuthorityError) as raised:
            operations_catalog._inventory_sources(root, (*self.paths, overlay))
        self.assertEqual("compose-overlay-invalid", raised.exception.code)

    def test_guide_binding_cannot_treat_overlay_as_service_authority(self):
        root = self._repo()
        overlay = pathlib.PurePosixPath(
            "infra/04-data/example/compose.workflow.override.yml"
        )
        (root / "docker-compose.yml").write_text(
            f"include:\n  - {self.compose}\n", encoding="utf-8"
        )
        (root / overlay).write_text(
            yaml.safe_dump(
                {
                    "x-hyhome-overlay": {"version": 1, "base": self.compose},
                    "services": {"database": {"image": "example/database:2.0.0"}},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        guide = root / self.guide
        guide.write_text(
            guide.read_text(encoding="utf-8")
            .replace(self.compose, overlay.as_posix())
            .replace(
                "[database, exporter]",
                "[database]",
            ),
            encoding="utf-8",
        )
        with mock.patch.object(
            operations_catalog,
            "_tracked_paths",
            return_value=(*self.paths, overlay),
        ):
            self.assertIn("service-operations-removed", self._codes(root))

    def test_zero_depth_standard_compose_service_requires_operations_owner(self):
        root = self._repo()
        standard = pathlib.PurePosixPath("infra/compose.yaml")
        (root / standard).write_text(
            "services:\n"
            "  standard:\n"
            "    profiles: [core]\n"
            "    image: example/standard:1.0.0\n",
            encoding="utf-8",
        )
        with mock.patch.object(
            operations_catalog,
            "_tracked_paths",
            return_value=(*self.paths, standard),
        ):
            self.assertIn("service-operations-missing", self._codes(root))

    def test_duplicate_service_ownership_is_rejected(self):
        root = self._repo()
        duplicate = (
            "docs/05.operations/guides/05-databases-and-storage/0002-duplicate.md"
        )
        path = root / duplicate
        path.write_text((root / self.guide).read_text())
        with mock.patch.object(
            operations_catalog,
            "_tracked_paths",
            return_value=(*self.paths, pathlib.PurePosixPath(duplicate)),
        ):
            self.assertIn("service-operations-duplicate", self._codes(root))

    def test_resource_template_change_invalidates_projection(self):
        root = self._repo()
        path = root / "infra/common-optimizations.yml"
        path.write_text(path.read_text().replace("256m", "512m"))
        self.assertIn("service-inventory-drift", self._codes(root))

    def test_declared_replicas_are_projected_and_invalidate_inventory(self):
        root = self._repo()
        compose = root / self.compose
        model = yaml.safe_load(compose.read_text())
        model["services"]["database"]["deploy"] = {
            "replicas": 2,
            "resources": {"limits": {"cpus": "0.75"}},
        }
        compose.write_text(yaml.safe_dump(model))
        self.inventory.write_text(operations_catalog.render_service_inventory(root))
        row = next(
            row
            for row in operations_catalog._service_inventory_rows(
                self.inventory.read_text()
            )
            if row["Service"] == "database"
        )
        self.assertIn('"replicas":2', row["Resources"])

        model["services"]["database"]["deploy"]["replicas"] = 3
        compose.write_text(yaml.safe_dump(model))
        self.assertIn("service-inventory-drift", self._codes(root))

    def test_private_environment_and_secret_values_are_never_opened(self):
        root = self._repo()
        (root / ".env").write_text("MUST_NOT_APPEAR=private-value-marker\n")
        self.assertNotIn(
            "private-value-marker", operations_catalog.render_service_inventory(root)
        )
        self.assertEqual(set(), self._codes(root))

    def test_build_authority_supports_inline_string_and_public_default_selector(self):
        root = self._repo()
        compose = root / self.compose
        original = compose.read_text()
        dockerfile = pathlib.PurePosixPath("infra/04-data/example/Dockerfile")
        (root / dockerfile).write_text("FROM example/base:2.3.4\n")
        for build in (
            {"context": ".", "dockerfile_inline": "FROM example/base:2.3.4"},
            ".",
            {"context": ".", "dockerfile": "${BUILD_FILE:-Dockerfile}"},
        ):
            with self.subTest(build=build):
                model = yaml.safe_load(original)
                model["services"]["database"]["build"] = build
                compose.write_text(yaml.safe_dump(model))
                with mock.patch.object(
                    operations_catalog,
                    "_tracked_paths",
                    return_value=(*self.paths, dockerfile),
                ):
                    rendered = operations_catalog.render_service_inventory(root)
                row = next(
                    row
                    for row in operations_catalog._service_inventory_rows(rendered)
                    if row["Service"] == "database"
                )
                self.assertNotIn("2.3.4", row["Runtime version authority"])
                if isinstance(build, dict) and "dockerfile_inline" in build:
                    self.assertIn("inline Dockerfile", row["Runtime version authority"])
                else:
                    self.assertIn(
                        "example/Dockerfile", row["Runtime version authority"]
                    )

    def test_reverse_edges_refresh_without_replacing_authored_consumer_evidence(self):
        root = self._repo()
        self._change("Consumer", "Owner-required HOME; declared reverse edges=exporter")
        compose = root / self.compose
        compose.write_text(
            compose.read_text().replace("depends_on: [database]", "depends_on: []")
        )
        rendered = operations_catalog.render_service_inventory(root)
        row = next(
            row
            for row in operations_catalog._service_inventory_rows(rendered)
            if row["Service"] == "database"
        )
        self.assertEqual(
            "Owner-required HOME; declared reverse edges=none", row["Consumer"]
        )

    def test_guide_source_link_must_be_real_markdown_not_a_code_example(self):
        root = self._repo()
        guide = root / self.guide
        text = guide.read_text()
        prefix, link = text.split("[Compose]", 1)
        guide.write_text(prefix + "```markdown\n[Compose]" + link + "```\n")
        self.assertIn("service-guide-source", self._codes(root))


if __name__ == "__main__":
    unittest.main()
