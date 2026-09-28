"""Exact preservation checks use each Git surface's own catalog and payload."""

import dataclasses
import pathlib
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance.registry import load_registry


class ArchiveSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.origin = "docs/03.specs/0001-example"
        self.record = "completed/03.specs/0001-example/"
        self.archive = "docs/98.archive/" + self.record
        self.catalog = "docs/98.archive/retention-catalog.md"
        self.write(self.origin + "/spec.md", b"---\nstatus: completed\n---\nBody.\n")
        self.git("add", ".")
        self.git("commit", "-qm", "source")
        self.source = self.git("rev-parse", "HEAD").strip()
        raw = load_registry()
        self.registry = dataclasses.replace(
            raw,
            common={
                **raw.common,
                "archive_retention": {
                    **raw.common["archive_retention"],
                    "legacy_capture_revision": self.source,
                    "legacy_transition_units": (),
                },
            },
        )
        self.base = self.source
        self.write(
            self.catalog,
            (
                "## Retention Catalog\n\n"
                "| Record | Class | Names | Source |\n| --- | --- | --- | --- |\n"
                f"| `{self.record}` | completed | no durable contract | `{self.source}:{self.origin}` |\n"
            ).encode(),
        )
        self.write(
            self.archive + "spec.md", (self.root / self.origin / "spec.md").read_bytes()
        )

    def git(self, *args):
        result = subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True
        )
        return result.stdout.decode()

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def findings(self):
        from scripts.lib.document_governance.archive_snapshots import (
            validate_archive_snapshots,
        )

        return validate_archive_snapshots(self.root, self.base, self.registry)

    def test_exact_worktree_capture_passes_before_staging(self):
        self.assertEqual((), self.findings())

    def test_body_newline_mode_and_member_changes_fail(self):
        path = self.root / self.archive / "spec.md"
        original = path.read_bytes()
        for body in (
            original.replace(b"completed", b"cancelled"),
            original.replace(b"\n", b"\r\n"),
        ):
            with self.subTest(body=body):
                path.write_bytes(body)
                self.assertTrue(
                    any(
                        item.code == "archive-exact-bytes-differ"
                        for item in self.findings()
                    )
                )
        path.write_bytes(original)
        path.chmod(0o755)
        self.assertTrue(
            any(item.code == "archive-exact-mode-differs" for item in self.findings())
        )
        path.chmod(0o644)
        self.write(self.archive + "extra.md", b"extra")
        self.assertTrue(
            any(item.code == "archive-exact-members-differ" for item in self.findings())
        )

    def test_index_deletion_is_not_hidden_by_worktree(self):
        self.git("add", ".")
        self.git("update-index", "--force-remove", self.archive + "spec.md")
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-exact-members-differ"
                for item in self.findings()
            )
        )

    def test_index_mode_is_not_hidden_by_worktree(self):
        self.git("add", ".")
        self.git("update-index", "--chmod=+x", self.archive + "spec.md")
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-exact-mode-differs"
                for item in self.findings()
            )
        )

    def test_committed_capture_remains_strict_when_already_in_base(self):
        self.git("add", ".")
        self.git("commit", "-qm", "capture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.assertEqual((), self.findings())
        self.write(self.archive + "spec.md", b"changed\n")
        self.git("add", ".")
        self.git("commit", "-qm", "tamper")
        self.assertTrue(
            any(
                item.detail == "HEAD" and item.code == "archive-exact-bytes-differ"
                for item in self.findings()
            )
        )

    def test_supported_crlf_checkout_is_not_canonical_tampering(self):
        self.write(".gitattributes", b"docs/98.archive/** text eol=crlf\n")
        path = self.root / self.archive / "spec.md"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.git("add", ".")
        self.assertEqual((), self.findings())

    def test_filter_is_reported_without_execution(self):
        self.write(".gitattributes", b"docs/98.archive/** filter=hostile\n")
        self.git("config", "filter.hostile.smudge", "touch FILTER_EXECUTED")
        self.assertTrue(
            any(item.code == "archive-checkout-unsupported" for item in self.findings())
        )
        self.assertFalse((self.root / "FILTER_EXECUTED").exists())

    def test_symlink_payload_fails_closed(self):
        path = self.root / self.archive / "spec.md"
        path.unlink()
        path.symlink_to(self.root / self.origin / "spec.md")
        self.assertTrue(
            any(item.code == "archive-exact-unsafe" for item in self.findings())
        )

    def test_invalid_source_type_path_and_abbreviated_revision_fail(self):
        catalog = self.root / self.catalog
        original = catalog.read_text()
        blob = self.git(
            "rev-parse", self.source + ":" + self.origin + "/spec.md"
        ).strip()
        for source in (
            self.source[:12] + ":" + self.origin,
            blob + ":" + self.origin,
            self.source + ":docs/03.specs/0002-wrong",
        ):
            with self.subTest(source=source):
                catalog.write_text(
                    original.replace(self.source + ":" + self.origin, source)
                )
                self.assertTrue(self.findings())

    def test_index_bytes_are_not_hidden_by_worktree(self):
        self.git("add", ".")
        path = self.root / self.archive / "spec.md"
        original = path.read_bytes()
        path.write_bytes(b"tampered\n")
        self.git("add", self.archive + "spec.md")
        path.write_bytes(original)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-exact-bytes-differ"
                for item in self.findings()
            )
        )

    def test_index_catalog_removal_cannot_hide_committed_capture(self):
        self.git("add", ".")
        self.git("commit", "-qm", "capture")
        self.git("update-index", "--force-remove", self.catalog)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-capture-row-missing"
                for item in self.findings()
            )
        )

    def test_legacy_capture_freezes_cutover_bytes(self):
        # Legacy capture metadata may differ from source under its older contract.
        self.write(self.archive + "spec.md", b"legacy transformed body\n")
        self.git("add", ".")
        self.git("commit", "-qm", "legacy capture")
        revision = self.git("rev-parse", "HEAD").strip()
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_capture_revision": revision,
                },
            },
        )
        self.assertEqual((), self.findings())
        self.git("update-index", "--chmod=+x", self.archive + "spec.md")
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-exact-mode-differs"
                for item in self.findings()
            )
        )
        self.git("commit", "-qm", "legacy mode tamper")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.assertTrue(
            any(
                item.detail == "HEAD" and item.code == "archive-exact-mode-differs"
                for item in self.findings()
            )
        )

    def test_orphan_source_commit_is_not_recovery_authority(self):
        tree = self.git("rev-parse", "HEAD^{tree}").strip()
        orphan = self.git(
            "commit-tree", tree, "-p", self.source, "-m", "unpublished"
        ).strip()
        path = self.root / self.catalog
        path.write_text(path.read_text().replace(self.source + ":", orphan + ":"))
        self.assertTrue(
            any(
                item.code == "catalog-source-commit-orphaned"
                for item in self.findings()
            )
        )

    def test_adopted_generation_cannot_be_relabelled(self):
        import json

        contract = dict(self.registry.common["archive_retention"])
        self.write(
            "docs/99.templates/registry.json",
            json.dumps(
                {
                    "common": {
                        "archive_disposition_model": "adopted",
                        "archive_retention": {
                            "legacy_capture_revision": contract[
                                "legacy_capture_revision"
                            ],
                            "legacy_transition_units": [],
                        },
                    }
                }
            ).encode(),
        )
        self.git("add", ".")
        self.git("commit", "-qm", "adopt generation")
        for field, value in (
            ("legacy_capture_revision", self.git("rev-parse", "HEAD").strip()),
            ("legacy_transition_units", (self.record,)),
        ):
            with self.subTest(field=field):
                self.registry = dataclasses.replace(
                    self.registry,
                    common={
                        **self.registry.common,
                        "archive_retention": {**contract, field: value},
                    },
                )
                self.assertTrue(
                    any(
                        item.code == "archive-generation-changed"
                        for item in self.findings()
                    )
                )

    def test_committed_transition_has_no_permanent_integrity_exemption(self):
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_transition_units": (self.record,),
                },
            },
        )
        self.git("add", ".")
        self.git("commit", "-qm", "bootstrap capture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.assertEqual((), self.findings())
        path = self.root / self.archive / "spec.md"
        path.write_bytes(b"tampered bootstrap\n")
        self.git("add", self.archive + "spec.md")
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "archive-exact-bytes-differ"
                for item in self.findings()
            )
        )
        self.git("commit", "-qm", "tamper bootstrap")
        self.assertTrue(
            any(
                item.detail == "HEAD" and item.code == "archive-exact-bytes-differ"
                for item in self.findings()
            )
        )

    def test_transition_units_must_be_canonical(self):
        for unit in ("completed/../escape", "completed/03.specs/0001-example/spec.md"):
            with self.subTest(unit=unit):
                self.registry = dataclasses.replace(
                    self.registry,
                    common={
                        **self.registry.common,
                        "archive_retention": {
                            **self.registry.common["archive_retention"],
                            "legacy_transition_units": (unit,),
                        },
                    },
                )
                self.assertTrue(
                    any(
                        item.code == "archive-generation-unavailable"
                        for item in self.findings()
                    )
                )

    def test_unauthorized_index_assessment_is_not_hidden_by_worktree(self):
        self.git("add", ".")
        self.git("commit", "-qm", "capture")
        path = self.root / self.catalog
        original = path.read_text()
        path.write_text(
            original + "\n## Current Assessments\n\n"
            "| Record | Assessment | Availability | Current Owner | Decision | Reason | Assessed At | Hold |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| `{self.record}` | invalidated | retained | none | `{self.source}:{self.origin}/spec.md` | unsafe | 2026-09-28 | none |\n"
        )
        self.git("add", self.catalog)
        path.write_text(original)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "assessment-approval-invalid"
                for item in self.findings()
            )
        )

    def test_index_assessment_removal_is_not_hidden_by_restored_worktree(self):
        task = "docs/03.specs/0002-review/tasks/tsk-0001-review.md"
        self.write(
            task,
            (
                "---\ntype: sdlc/task\nstatus: in-progress\nowner: '@owner'\n"
                "artifact_id: SPEC-0002-TSK-0001\narchive_authorizations:\n"
                f"  - unit: {self.record}\n    action: assess\n"
                "    approved_by: '@owner'\n    approved_at: '2026-09-28'\n"
                "    evidence: '#approval-assess'\n    status: approved\n---\n"
                f"## Approval assess\n\n> @owner approved assess for {self.record} on 2026-09-28.\n"
            ).encode(),
        )
        self.git("add", ".")
        self.git("commit", "-qm", "capture and approval")
        approval = self.git("rev-parse", "HEAD").strip()
        path = self.root / self.catalog
        capture = path.read_text()
        assessed = capture + (
            "\n## Current Assessments\n\n"
            "| Record | Assessment | Availability | Current Owner | Decision | Reason | Assessed At | Hold |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| `{self.record}` | usable | retained | none | `{approval}:{task}` | reviewed | 2026-09-28 | none |\n"
        )
        path.write_text(assessed)
        self.git("add", ".")
        self.git("commit", "-qm", "assess")
        self.assertEqual((), self.findings())
        path.write_text(capture)
        self.git("add", self.catalog)
        path.write_text(assessed)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "assessment-row-removed"
                for item in self.findings()
            )
        )

    def test_staged_generation_change_or_removal_is_not_hidden(self):
        import json

        path = "docs/99.templates/registry.json"
        contract = {
            "legacy_capture_revision": self.source,
            "legacy_transition_units": [],
        }
        document = {
            "common": {
                "archive_disposition_model": "adopted",
                "archive_retention": contract,
            }
        }
        original = json.dumps(document).encode()
        self.write(path, original)
        self.git("add", ".")
        self.git("commit", "-qm", "adopt generation")
        for changed in (
            {
                "common": {
                    "archive_disposition_model": "adopted",
                    "archive_retention": {
                        **contract,
                        "legacy_transition_units": [self.record],
                    },
                }
            },
            {
                "common": {
                    "archive_disposition_model": "transition",
                    "archive_retention": contract,
                }
            },
            {"common": {"archive_retention": contract}},
            {"common": {}},
            None,
        ):
            with self.subTest(changed=changed):
                self.git("reset", "--quiet", "HEAD", "--", path)
                if changed is None:
                    self.git("update-index", "--force-remove", path)
                else:
                    self.write(path, json.dumps(changed).encode())
                    self.git("add", path)
                self.write(path, original)
                self.assertTrue(
                    any(
                        item.code == "archive-generation-changed"
                        for item in self.findings()
                    )
                )

    def test_initial_transition_accepts_supported_crlf_checkout(self):
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_transition_units": (self.record,),
                },
            },
        )
        self.write(".gitattributes", b"docs/98.archive/** text eol=crlf\n")
        path = self.root / self.archive / "spec.md"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.git("add", ".")
        self.assertEqual((), self.findings())

    def test_index_capture_envelope_change_is_not_hidden(self):
        self.git("add", ".")
        self.git("commit", "-qm", "capture")
        path = self.root / self.catalog
        original = path.read_text()
        path.write_text(original.replace("no durable contract", "SPEC-0001"))
        self.git("add", self.catalog)
        path.write_text(original)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "capture-row-changed"
                for item in self.findings()
            )
        )

    def test_duplicate_index_registry_keys_fail_closed(self):
        import json

        path = "docs/99.templates/registry.json"
        original = json.dumps(
            {
                "common": {
                    "archive_disposition_model": "adopted",
                    "archive_retention": {
                        "legacy_capture_revision": self.source,
                        "legacy_transition_units": [],
                    },
                }
            }
        ).encode()
        self.write(path, original)
        self.git("add", ".")
        self.git("commit", "-qm", "adopt generation")
        self.write(path, b'{"common": {},' + original[1:])
        self.git("add", path)
        self.write(path, original)
        self.assertTrue(
            any(
                item.code == "archive-generation-unavailable"
                for item in self.findings()
            )
        )

    def test_partial_initial_adoption_requires_staged_generation(self):
        import json

        path = "docs/99.templates/registry.json"
        raw = json.loads(
            (pathlib.Path(__file__).resolve().parents[3] / path).read_text()
        )
        raw["common"]["archive_retention"]["legacy_capture_revision"] = self.source
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_transition_units": tuple(
                        raw["common"]["archive_retention"]["legacy_transition_units"]
                    ),
                },
            },
        )
        self.write(path, json.dumps(raw).encode())
        self.assertEqual(
            (), self.findings()
        )  # The old index is unchanged and remains coherent.
        self.git("add", "docs/98.archive")
        self.assertTrue(
            any(item.code == "archive-generation-changed" for item in self.findings())
        )

    def test_new_index_capture_names_are_validated_on_its_own_surface(self):
        path = self.root / self.catalog
        original = path.read_text()
        path.write_text(original.replace("no durable contract", "nonsense"))
        self.git("add", "docs/98.archive")
        path.write_text(original)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "catalog-names-invalid"
                for item in self.findings()
            )
        )

    def test_index_capture_owner_path_must_exist_in_index(self):
        owner = "docs/01.requirements/0002-owner.md"
        self.write(owner, b"---\nstatus: active\n---\nOwner\n")
        path = self.root / self.catalog
        path.write_text(path.read_text().replace("no durable contract", f"`{owner}`"))
        self.git("add", "docs/98.archive")
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "catalog-names-invalid"
                for item in self.findings()
            )
        )
        self.git("add", owner)
        self.assertEqual((), self.findings())

    def test_orphan_cutover_cannot_classify_capture_generation(self):
        tree = self.git("rev-parse", "HEAD^{tree}").strip()
        orphan = self.git(
            "commit-tree", tree, "-p", self.source, "-m", "orphan cutover"
        ).strip()
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_capture_revision": orphan,
                },
            },
        )
        self.assertTrue(
            any(
                item.code == "archive-generation-unavailable"
                for item in self.findings()
            )
        )

    def test_index_names_owner_uses_index_registry_classification(self):
        self._assert_index_names_registry("completed")

    def test_resolved_index_names_owner_uses_index_registry_classification(self):
        self._assert_index_names_registry("resolved")

    def _assert_index_names_registry(self, disposition):
        import json

        if disposition == "resolved":
            original_record = self.record
            original_archive = self.root / self.archive
            self.record = self.record.replace("completed/", "resolved/", 1)
            self.archive = "docs/98.archive/" + self.record
            target = self.root / self.archive
            target.parent.mkdir(parents=True, exist_ok=True)
            original_archive.rename(target)
            catalog = self.root / self.catalog
            catalog.write_text(
                catalog.read_text()
                .replace(original_record, self.record)
                .replace("| completed |", "| resolved |")
            )
        owner = "docs/01.requirements/0002-owner.md"
        self.write(owner, b"---\nstatus: active\n---\nOwner\n")
        catalog = self.root / self.catalog
        names = (
            f"`{owner}`" if disposition == "completed" else f"inc-2026-0001 `{owner}`"
        )
        catalog.write_text(catalog.read_text().replace("no durable contract", names))
        registry_path = "docs/99.templates/registry.json"
        source_registry = pathlib.Path(__file__).resolve().parents[3] / registry_path
        raw = json.loads(source_registry.read_text())
        raw["common"]["archive_retention"]["legacy_capture_revision"] = self.source
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_transition_units": tuple(
                        raw["common"]["archive_retention"]["legacy_transition_units"]
                    ),
                },
            },
        )
        original = json.dumps(raw).encode()
        self.write(registry_path, original)
        self.git("add", ".")
        self.git("commit", "-qm", "capture with owner and Registry")
        self.assertEqual((), self.findings())
        for profile in raw["profiles"]:
            if profile["id"] == "requirements-package":
                profile["path_pattern"] = (
                    "docs/01.requirements/alternate/{number:4}-{slug}.md"
                )
        self.write(registry_path, json.dumps(raw).encode())
        self.git("add", registry_path)
        self.write(registry_path, original)
        self.assertTrue(
            any(
                item.detail == "index" and item.code == "catalog-names-invalid"
                for item in self.findings()
            )
        )

    def test_pre_extraction_cutover_reads_legacy_catalog_from_archive_readme(self):
        catalog = self.root / self.catalog
        capture_table = catalog.read_bytes()
        catalog.unlink()
        self.write("docs/98.archive/README.md", capture_table)
        self.write(self.archive + "spec.md", b"legacy transformed body\n")
        self.git("add", ".")
        self.git("commit", "-qm", "legacy capture catalog in README")
        cutover = self.git("rev-parse", "HEAD").strip()
        self.registry = dataclasses.replace(
            self.registry,
            common={
                **self.registry.common,
                "archive_retention": {
                    **self.registry.common["archive_retention"],
                    "legacy_capture_revision": cutover,
                },
            },
        )
        self.write(self.catalog, capture_table)
        self.write("docs/98.archive/README.md", b"# Archive index\n")
        self.git("add", ".")
        self.git("commit", "-qm", "extract capture catalog")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.assertEqual((), self.findings())
        from scripts.lib.document_governance.archive_snapshots import is_legacy_capture

        self.assertTrue(is_legacy_capture(self.root, self.record, self.registry))
