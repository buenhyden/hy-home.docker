"""Current public lifecycle and CLI-shape tests."""

from __future__ import annotations

import contextlib
import dataclasses
import inspect
import io
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.lifecycle import public as public_module
from tests.validation.lifecycle._support import (
    REGISTRY,
    ROOT,
    SCRIPT,
    lifecycle,
    run,
)


class CurrentPublicContractTests(unittest.TestCase):
    def valid_row(self, **overrides: object):
        values: dict[str, object] = {
            "source_path": pathlib.PurePosixPath(
                "docs/03.specs/0001-example/spec.md"
            ),
            "target_path": pathlib.PurePosixPath(
                "docs/03.specs/0001-example/spec.md"
            ),
            "artifact_id": "SPEC-0001",
            "artifact_type": "spec",
            "status_before": "active",
            "status_after": "active",
            "parent_ids": (),
            "disposition": "preserve",
            "canonical_replacement": None,
            "active_consumers": (),
            "partition_plan": None,
            "preservation_class": None,
            "evidence": lifecycle.ManifestEvidence((), (), (), (), ()),
            "review_verdict": lifecycle.ReviewVerdict("pending", "pending"),
        }
        values.update(overrides)
        return lifecycle.MigrationManifestRow(**values)

    def document(self, *, schema_version: int = 1):
        return lifecycle.MigrationManifestDocument(
            schema_version=schema_version,
            wave="fixture",
            baseline_commit="a" * 40,
            generated_by="check-document-corpus-lifecycle.py",
            enforcement="advisory",
            entries=(self.valid_row(),),
        )

    def write_manifest(self, text: str) -> pathlib.Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = pathlib.Path(directory.name) / "manifest.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_cli_defaults_to_the_registry_and_has_no_mode_inventory(self) -> None:
        parser = lifecycle._parser()
        self.assertEqual(REGISTRY.resolve(), parser.parse_args([]).profiles.resolve())
        self.assertFalse(hasattr(parser.parse_args([]), "mode"))
        self.assertFalse(hasattr(lifecycle, "MODES"))

    def test_public_dataclasses_are_frozen_and_tuple_backed(self) -> None:
        row = self.valid_row()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            row.disposition = "delete"  # type: ignore[misc]
        self.assertIsInstance(row.parent_ids, tuple)
        self.assertIsInstance(row.evidence.commands, tuple)

    def test_manifest_skeleton_signature_remains_plan_bound(self) -> None:
        self.assertEqual(
            str(inspect.signature(lifecycle.generate_manifest_skeleton)),
            "(root: 'pathlib.Path', contract: 'dict[str, object]', *, "
            "wave: 'str', baseline_ref: 'str') -> 'MigrationManifestDocument'",
        )

    def test_cli_misuse_fails_before_opening_repository_files(self) -> None:
        result = run(
            sys.executable,
            str(SCRIPT),
            "--mode",
            "check-contract",
            "--wave",
            "forbidden",
            "--profiles",
            "/missing/profiles.yaml",
            "--contract",
            "/missing/contract.yaml",
            cwd=ROOT,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("--wave", result.stderr)
        self.assertNotIn("configuration-error", result.stderr)

    def test_manifest_loader_rejects_unknown_and_missing_keys(self) -> None:
        loaded = yaml.safe_load(
            lifecycle.render_migration_manifest(self.document())
        )
        for mutation in ("unknown-top", "missing-entry"):
            candidate = {**loaded}
            candidate["entries"] = [dict(loaded["entries"][0])]
            if mutation == "unknown-top":
                candidate["unexpected"] = True
            else:
                del candidate["entries"][0]["status_after"]
            with self.subTest(mutation=mutation), self.assertRaises(
                lifecycle.ProfileError
            ):
                lifecycle.load_migration_manifest(
                    self.write_manifest(
                        yaml.safe_dump(candidate, sort_keys=False)
                    )
                )

    def test_manifest_serialization_is_deterministic_and_lf_only(self) -> None:
        rendered = lifecycle.render_migration_manifest(self.document())
        self.assertTrue(rendered.endswith("\n"))
        self.assertNotIn("\r", rendered)
        reloaded = lifecycle.load_migration_manifest(
            self.write_manifest(rendered)
        )
        self.assertEqual(
            rendered,
            lifecycle.render_migration_manifest(reloaded),
        )

    def test_manifest_v2_exposes_surface_transition_fields(self) -> None:
        loaded = yaml.safe_load(
            lifecycle.render_migration_manifest(self.document())
        )
        loaded["schema_version"] = 2
        row = loaded["entries"][0]
        row["artifact_type_before"] = row.pop("artifact_type")
        row["artifact_type_after"] = row["artifact_type_before"]
        row["surface_class"] = "typed-example"
        manifest = lifecycle.load_migration_manifest(
            self.write_manifest(yaml.safe_dump(loaded, sort_keys=False))
        )
        self.assertEqual(2, manifest.schema_version)
        self.assertEqual("spec", manifest.entries[0].artifact_type_before)
        self.assertEqual("spec", manifest.entries[0].artifact_type_after)
        self.assertEqual("typed-example", manifest.entries[0].surface_class)

    def test_default_route_does_not_load_a_legacy_contract(self) -> None:
        with mock.patch.object(
            lifecycle,
            "load_migration_contract",
            side_effect=AssertionError("legacy authority loaded"),
        ), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, lifecycle.main([]))

    def test_default_route_reports_lifecycle_and_archive_recovery(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(0, lifecycle.main([]))
        rendered = output.getvalue()
        self.assertIn("document corpus lifecycle:", rendered)
        self.assertIn("archive recovery:", rendered)
