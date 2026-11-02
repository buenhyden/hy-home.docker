"""Effective control ownership and registry boundaries for P09."""

import datetime as dt
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.validation import compose_controls as controls


class P09ComposeControlsTests(unittest.TestCase):
    def test_registry_rejects_duplicate_keys_and_invalid_identity(self):
        registry = json.loads((controls.ROOT / controls.REGISTRY).read_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text('{"schema_version":2,"schema_version":1}')
            with self.assertRaises(ValueError):
                controls.load_registry(path)
            for key, value in (
                ("schema_version", 1),
                ("policy_id", "other"),
                ("controls", {}),
                ("naming_exceptions", {}),
                ("exceptions", [{"scope": 3}]),
            ):
                with self.subTest(key=key):
                    path.write_text(json.dumps({**registry, key: value}))
                    with self.assertRaises(ValueError):
                        controls.load_registry(path)
            path.write_text(json.dumps(registry))
            self.assertEqual(registry, controls.load_registry(path))
            linked = path.parent / "linked.json"
            linked.symlink_to(path)
            with self.assertRaises(ValueError):
                controls.load_registry(linked)

    def test_duplicate_service_ownership_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b = root / "a.yml", root / "b.yml"
            a.write_text("services:\n  same: {}\n")
            b.write_text("services:\n  same: {}\n")
            with patch.object(controls, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "duplicate"):
                    controls._service_files([a, b])

    def test_adoption_requires_actual_extends_not_comment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "infra" / "x" / "docker-compose.yml"
            path.parent.mkdir(parents=True)
            path.write_text("# common-optimizations.yml\nservices:\n  a: {}\n")
            with patch.object(controls, "ROOT", root):
                self.assertTrue(controls.template_findings([path]))
                path.write_text(
                    "services:\n  a:\n    extends:\n      file: ../common-optimizations.yml\n      service: template-low\n"
                )
                self.assertFalse(controls.template_findings([path]))

    def test_overlay_reuses_only_unchanged_base_deviations(self):
        base = {"services": {"a": {"cap_add": ["NET_BIND_SERVICE"]}}}
        overlay = {"services": {"a": {"cap_add": ["NET_BIND_SERVICE"]}}}
        reg = {"controls": {"cap_add": "declared"}}
        self.assertEqual(
            [], controls.overlay_findings(reg, base, overlay, "infra/overlay.yml", ())
        )
        widened = {"services": {"a": {"cap_add": ["NET_BIND_SERVICE", "SYS_ADMIN"]}}}
        findings = controls.overlay_findings(
            reg, base, widened, "infra/overlay.yml", ()
        )
        self.assertEqual(1, len(findings))
        self.assertIn("cap_add", findings[0])
        self.assertIn("infra/overlay.yml", findings[0])
        fixed = {"services": {"a": {"cap_add": []}}}
        self.assertEqual(
            [], controls.overlay_findings(reg, base, fixed, "infra/overlay.yml", ())
        )

    def test_current_registry_round_trip(self):
        loaded = controls.load_registry(controls.ROOT / controls.REGISTRY)
        self.assertTrue(loaded["exceptions"])
        self.assertLessEqual(
            dt.date.fromisoformat(loaded["exceptions"][0]["reviewed"]), dt.date.today()
        )

    def test_public_copy_never_copies_private_env_and_neutralizes_env_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            copied = Path(directory) / "copy"
            (root / "labs").mkdir(parents=True)
            copied.mkdir()
            (root / ".env.example").write_text("PUBLIC=fixture\n")
            (root / "labs/.env.example").write_text("PUBLIC=fixture\n")
            (root / ".env").write_text("PRIVATE-CANARY-NEVER-COPY\n")
            (root / "docker-compose.yml").write_text(
                "services:\n  a:\n    image: fixture\n    env_file: .env\n"
            )
            with patch.object(controls, "ROOT", root):
                controls._copy_public_render_sources(copied, {"docker-compose.yml"})
            self.assertFalse((copied / ".env").exists())
            self.assertNotIn(
                "PRIVATE-CANARY", (copied / "docker-compose.yml").read_text()
            )
            self.assertIn(
                ".p01-empty-input", (copied / "docker-compose.yml").read_text()
            )

    def test_public_copy_rejects_changed_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            copied = Path(directory) / "copy"
            (root / "labs").mkdir(parents=True)
            copied.mkdir()
            for name in (".env.example", "labs/.env.example", "docker-compose.yml"):
                (root / name).write_text("services: {}\n")
            with patch.object(controls, "ROOT", root):
                expected = controls._public_hashes(
                    {".env.example", "labs/.env.example", "docker-compose.yml"}
                )
                (root / "docker-compose.yml").write_text("services: {changed: {}}\n")
                with self.assertRaisesRegex(ValueError, "compose_source_changed"):
                    controls._copy_public_render_sources(
                        copied, {"docker-compose.yml"}, expected=expected
                    )

    def test_duplicate_service_key_within_one_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "a.yml"
            path.write_text("services:\n  same: {}\n  same: {}\n")
            with patch.object(controls, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "duplicate"):
                    controls._service_files([path])

    def test_changed_gpu_reservation_cannot_reuse_base_exception(self):
        base = {"services": {"a": {"gpus": [{"device_ids": ["0"]}]}}}
        changed = {"services": {"a": {"gpus": [{"device_ids": ["1"]}]}}}
        findings = controls.overlay_findings(
            {"controls": {"gpu": "registered"}}, base, changed, "x.yml", ()
        )
        self.assertEqual(1, len(findings))

    def test_unrelated_seccomp_does_not_change_no_new_privileges(self):
        base = {"services": {"a": {"security_opt": ["no-new-privileges:false"]}}}
        overlay = {
            "services": {
                "a": {"security_opt": ["no-new-privileges:false", "seccomp=/profile"]}
            }
        }
        self.assertEqual(
            [],
            controls.overlay_findings(
                {"controls": {"no_new_privileges": "registered"}},
                base,
                overlay,
                "overlay.yml",
                (),
            ),
        )

    def test_daemon_restart_change_does_not_change_absent_healthcheck(self):
        base = {"services": {"a": {"restart": "always"}}}
        overlay = {"services": {"a": {"restart": "unless-stopped"}}}
        self.assertEqual(
            [],
            controls.overlay_findings(
                {"controls": {"healthcheck": "registered"}},
                base,
                overlay,
                "overlay.yml",
                (),
            ),
        )

    def test_nonpositive_and_malformed_resource_limits_are_not_accepted(self):
        invalid = {"cpus": "0", "mem_limit": "0m", "pids_limit": -1}
        found = controls.deviations(invalid, ())
        self.assertTrue({"cpus", "mem_limit", "pids_limit"}.issubset(found))
        invalid = {"cpus": "nan", "mem_limit": "nonsense", "pids_limit": "1.5"}
        found = controls.deviations(invalid, ())
        self.assertTrue({"cpus", "mem_limit", "pids_limit"}.issubset(found))
        valid = {"cpus": "0.5", "mem_limit": "128MiB", "pids_limit": "128"}
        found = controls.deviations(valid, ())
        self.assertTrue({"cpus", "mem_limit", "pids_limit"}.isdisjoint(found))

    def test_exact_secret_root_bind_is_a_reader_but_sibling_is_not(self):
        def bind(source):
            return {"volumes": [{"type": "bind", "source": source}]}

        self.assertTrue(
            controls.needs_secret_group(bind("/repo/secrets"), ("/repo/secrets/",))
        )
        self.assertTrue(
            controls.needs_secret_group(bind("/repo/secrets/key"), ("/repo/secrets/",))
        )
        self.assertFalse(
            controls.needs_secret_group(
                bind("/repo/secrets-other/key"), ("/repo/secrets/",)
            )
        )

    def test_no_new_privileges_does_not_accept_unrelated_substring(self):
        valid = {"security_opt": ["no-new-privileges:true"]}
        invalid = {"security_opt": ["bogus-no-new-privileges:true"]}
        self.assertNotIn("no_new_privileges", controls.deviations(valid, ()))
        self.assertIn("no_new_privileges", controls.deviations(invalid, ()))

    def test_conflicting_or_duplicate_no_new_privileges_fails_closed(self):
        for values in (
            ["no-new-privileges:true", "no-new-privileges:false"],
            ["no-new-privileges:true", "no-new-privileges:true"],
            ["no-new-privileges:true", "no-new-privileges=false"],
        ):
            with self.subTest(values=values):
                self.assertIn(
                    "no_new_privileges",
                    controls.deviations({"security_opt": values}, ()),
                )

    def test_final_source_change_prevents_success(self):
        models = controls.RenderedModels(
            {"root": ({"services": {}}, {}, ())}, {"source.yml": "old"}
        )
        with (
            patch.object(
                controls,
                "_public_hashes",
                side_effect=[
                    {"registry": "same"},
                    {"registry": "same"},
                    {"source.yml": "new"},
                ],
            ),
            patch.object(
                controls,
                "load_registry",
                return_value={"controls": {}, "exceptions": []},
            ),
            patch.object(controls, "render_models", return_value=models),
            patch.object(controls, "template_findings", return_value=[]),
            patch.object(
                controls, "_source_inventory", return_value=([], [], {"source.yml"})
            ),
            patch(
                "scripts.lib.supply_chain.latest_version_gate.expected_from_root",
                return_value=([], {"input_files": []}),
            ),
        ):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(1, controls.main([]))
            self.assertIn("FAIL invalid control inputs", output.getvalue())

    def test_new_lab_or_compose_path_invalidates_snapshot(self):
        with (
            patch.object(
                controls,
                "_source_inventory",
                return_value=([], [], {"source.yml", "labs/new.yml"}),
            ),
            patch.object(controls, "_public_hashes") as hashes,
        ):
            with self.assertRaisesRegex(ValueError, "compose_source_changed"):
                controls._validate_source_snapshot({"source.yml": "old"})
            hashes.assert_not_called()

    def test_untracked_infrastructure_refused_before_render(self):
        with (
            patch(
                "scripts.lib.document_governance.operations_catalog._conftest_untracked_candidates",
                side_effect=ValueError("untracked"),
            ),
            patch.object(controls, "_compose") as compose,
        ):
            with self.assertRaisesRegex(ValueError, "untracked"):
                controls.render_models()
            compose.assert_not_called()


if __name__ == "__main__":
    unittest.main()
