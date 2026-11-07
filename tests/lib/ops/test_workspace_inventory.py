"""Boundary and recovery behavior of the public workspace inventory."""

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops._workspace_render import render_inventory
from scripts.lib.ops.workspace_inventory import (
    InventoryError,
    atomic_write,
    compare,
    scan,
    validate,
)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, path, content="public\n"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def scan(self, *paths, **kwargs):
        return scan(self.root, public_paths=paths, **kwargs)

    def test_non_git_requires_explicit_public_inputs_and_keeps_private_metadata(self):
        self.put("source.py")
        self.put(".env", "DO_NOT_READ_OR_HASH\n")
        public, private = self.scan("source.py")
        self.assertFalse(public["workspace"]["git"])
        self.assertEqual([r["path"] for r in public["files"]], ["source.py"])
        self.assertEqual(private["files"][0]["path"], ".env")
        self.assertNotIn("DO_NOT_READ", json.dumps((public, private)))
        self.assertNotIn("sha256", private["files"][0])
        self.assertEqual(public["coverage"]["body_review"]["numerator"], 0)
        validate(public)

    def test_git_tracks_dirty_sources_nested_roots_and_names_with_spaces(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.put("a name.py", "before\n")
        subprocess.run(["git", "-C", str(self.root), "add", "a name.py"], check=True)
        self.put("a name.py", "changed\n")
        nested = self.root / "nested"
        nested.mkdir()
        subprocess.run(["git", "init", "-q", str(nested)], check=True)
        public, private = self.scan()
        self.assertTrue(public["workspace"]["git"])
        self.assertEqual(
            public["files"][0]["sha256"], hashlib.sha256(b"changed\n").hexdigest()
        )
        self.assertNotIn("nested", [r["path"] for r in public["roots"]])
        self.assertIn("nested", [r["path"] for r in private["roots"]])
        self.assertTrue(public["workspace"]["dirty_paths"])

    def test_public_selection_cannot_grant_secret_or_external_access(self):
        self.put(".env", "PRIVATE")
        self.put("secrets/token", "PRIVATE")
        for name in (".env", "secrets/token", "../escape", "/absolute"):
            with self.subTest(name=name), self.assertRaises(InventoryError):
                self.scan(name)

    def test_nested_git_secret_is_metadata_only_even_when_tracked(self):
        nested = self.root / "child"
        nested.mkdir()
        subprocess.run(["git", "init", "-q", str(nested)], check=True)
        self.put("child/secrets/token", "PRIVATE_SENTINEL")
        subprocess.run(["git", "-C", str(nested), "add", "secrets/token"], check=True)
        with patch(
            "scripts.lib.ops.workspace_inventory._read_public",
            side_effect=AssertionError("must not open"),
        ):
            public, private = self.scan()
        self.assertEqual(public["files"], [])
        self.assertEqual(private["files"][0]["path"], "child/secrets/token")
        self.assertNotIn("sha256", private["files"][0])

    def test_never_follows_file_or_directory_links(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        (self.root / "linked.py").symlink_to(outside / "missing")
        (self.root / "linked-dir").symlink_to(outside, target_is_directory=True)
        public, private = self.scan("linked.py")
        self.assertEqual(public["files"][0]["state"], "SYMLINK_NOT_FOLLOWED")
        self.assertNotIn("sha256", public["files"][0])
        self.assertIn("linked-dir", [r["path"] for r in private["files"]])

    def test_review_requires_identity_time_hash_and_explicit_scope(self):
        self.put("a.py")
        first, _ = self.scan("a.py")
        row = first["files"][0]
        record = {
            "path": "a.py",
            "sha256": row["sha256"],
            "reviewer": "qa-engineer",
            "observed_at": "2026-11-01T01:00:00Z",
            "scope": "complete source body",
            "complete": True,
        }
        reviewed, _ = self.scan("a.py", reviews=[record])
        self.assertEqual(reviewed["coverage"]["body_review"]["numerator"], 1)
        self.put("a.py", "new\n")
        stale, _ = self.scan("a.py", reviews=[record])
        self.assertEqual(stale["files"][0]["review"]["state"], "STALE")
        for field in ("scope", "reviewer", "observed_at", "sha256"):
            with self.subTest(field=field), self.assertRaises(InventoryError):
                self.scan(
                    "a.py", reviews=[{k: v for k, v in record.items() if k != field}]
                )

    def test_compare_invalidates_only_changed_reviewed_input(self):
        self.put("a.py")
        self.put("stable.py")
        self.put("removed.py")
        before, _ = self.scan("a.py", "stable.py", "removed.py")
        self.put("a.py", "changed\n")
        self.put("new.py")
        (self.root / "removed.py").unlink()
        after, _ = self.scan("a.py", "stable.py", "new.py")
        diff = compare(before, after)
        self.assertEqual(diff["added"], ["new.py"])
        self.assertEqual(diff["removed"], ["removed.py"])
        self.assertEqual(diff["changed"], ["a.py"])
        self.assertEqual(diff["invalidated_reviews"], ["a.py", "removed.py"])

    def test_generated_output_is_not_self_hashed(self):
        self.put("out.yaml", "previous output\n")
        doc, _ = self.scan("out.yaml", excluded_outputs=["out.yaml"])
        self.assertEqual(doc["files"][0]["state"], "GENERATED_OUTPUT")
        self.assertNotIn("sha256", doc["files"][0])

    def test_read_error_is_visible_without_input_or_exception_values(self):
        self.put("a.py")
        with patch(
            "scripts.lib.ops.workspace_inventory._read_public",
            side_effect=PermissionError("SENSITIVE"),
        ):
            doc, _ = self.scan("a.py")
        self.assertEqual(doc["files"][0]["state"], "UNREADABLE")
        self.assertNotIn("SENSITIVE", json.dumps(doc))

    def test_validator_rejects_false_coverage_duplicate_paths_and_review_claims(self):
        self.put("a.py")
        doc, _ = self.scan("a.py")
        for mutate in (
            lambda d: d["files"].append(d["files"][0]),
            lambda d: d["coverage"]["body_review"].update(numerator=1),
            lambda d: d["files"][0]["review"].update(state="REVIEWED"),
            lambda d: d.update(
                ownership=[
                    {"path": "a.py", "writer": "a"},
                    {"path": "a.py", "writer": "b"},
                ]
            ),
        ):
            candidate = json.loads(json.dumps(doc))
            mutate(candidate)
            with self.assertRaises(InventoryError):
                validate(candidate)

    def test_validator_rejects_tier_rows_that_do_not_resolve_to_current_payload(self):
        self.put("a.py")
        doc, _ = self.scan("a.py")
        digest = doc["files"][0]["sha256"]
        doc["services"] = [{"id": "a.py::svc", "service": "svc"}]
        doc["compose"] = {"root_services": ["svc"]}
        doc["coverage_tiers"] = [
            {
                "id": "TIER01",
                "service_ids": ["a.py::svc"],
                "root_service_names": ["svc"],
                "declared_service_rows": 1,
                "source_files": [{"path": "a.py", "sha256": digest}],
            }
        ]
        self.assertTrue(validate(doc))
        tier = lambda d: d["coverage_tiers"][0]  # noqa: E731
        for mutate in (
            lambda d: tier(d).update(service_ids=["moved.yml::svc"]),
            lambda d: tier(d).update(root_service_names=["gone"]),
            lambda d: tier(d).update(declared_service_rows=2),
            lambda d: tier(d)["source_files"][0].update(path="moved.yml"),
            lambda d: tier(d)["source_files"][0].update(sha256="0" * 64),
        ):
            candidate = json.loads(json.dumps(doc))
            mutate(candidate)
            with self.assertRaises(InventoryError):
                validate(candidate)

    def test_atomic_failure_preserves_original_and_cleans_own_temporary_file(self):
        target = self.put("out.yaml", "original")
        with patch(
            "scripts.lib.ops.workspace_inventory.os.replace",
            side_effect=OSError("failure"),
        ):
            with self.assertRaises(InventoryError):
                atomic_write(self.root, "out.yaml", {"safe": True})
        self.assertEqual(target.read_text(), "original")
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["out.yaml"])

    def test_atomic_output_rejects_symlink_and_secret_destinations(self):
        self.put("real")
        (self.root / "link").symlink_to(self.root / "real")
        for target in ("link", ".env", "../outside", "secrets/value"):
            with self.subTest(target=target), self.assertRaises(InventoryError):
                atomic_write(self.root, target, {"safe": True})

    def test_cancellation_does_not_replace_existing_output(self):
        self.put("a.py")
        self.put("out.yaml", "original")
        with patch(
            "scripts.lib.ops.workspace_inventory._read_public",
            side_effect=KeyboardInterrupt,
        ):
            with self.assertRaises(KeyboardInterrupt):
                self.scan("a.py")
        self.assertEqual((self.root / "out.yaml").read_text(), "original")

    def render_fixture(self):
        self.put(
            "docker-compose.yml",
            "services:\n  app:\n    image: alpine:3\n    profiles: [dev]\n",
        )
        self.put(".env.example", "PUBLIC=synthetic\n")
        return self.scan("docker-compose.yml", ".env.example")[0]

    def test_render_is_confined_to_copy_and_scrubs_private_environment(self):
        doc = self.render_fixture()
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            copy = kwargs["cwd"]
            self.assertNotEqual(copy, self.root)
            self.assertFalse((copy / ".env").exists())
            self.assertEqual(set(kwargs["env"]), {"PATH", "DOCKER_CONFIG"})
            self.assertEqual(
                command[-4:-1],
                ["--no-env-resolution", "--no-path-resolution", "--format"]
                if command[-1] == "json"
                else ["--no-path-resolution", "--format", "json"],
            )
            self.assertNotIn("up", command)
            self.assertNotIn("MUST_NOT_APPEAR", json.dumps(kwargs["env"]))
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        result = render_inventory(self.root, doc, run=run)
        self.assertEqual(
            result["coverage"]["render"], {"numerator": 3, "denominator": 3}
        )
        self.assertEqual(len(calls), 3)
        self.assertEqual(doc["coverage"]["render"]["numerator"], 0)

    def test_render_timeout_failure_invalid_model_and_budget_are_separate(self):
        doc = self.render_fixture()
        for runner, expected in (
            (
                lambda *a, **k: subprocess.CompletedProcess(a, 1, b"", b"PRIVATE"),
                "FAIL",
            ),
            (lambda *a, **k: subprocess.CompletedProcess(a, 0, b"not-json"), "ERROR"),
            (
                lambda *a, **k: subprocess.CompletedProcess(a, 0, b'{"services":{}}'),
                "FAIL",
            ),
        ):
            result = render_inventory(self.root, doc, run=runner)
            self.assertTrue(
                all(c["result"] == expected for c in result["compose"]["render_cases"])
            )
            self.assertNotIn("PRIVATE", json.dumps(result))
        limited = render_inventory(self.root, doc, budget_seconds=0)
        self.assertTrue(
            all(c["result"] == "NOT_RUN" for c in limited["compose"]["render_cases"])
        )

    def test_render_rejects_source_changes_and_never_opens_private_inputs(self):
        doc = self.render_fixture()
        self.put("docker-compose.yml", "services: {}\n")
        with self.assertRaises(InventoryError):
            render_inventory(self.root, doc)

    def test_render_replaces_include_environment_and_secret_file_references(self):
        self.put(
            "docker-compose.yml",
            "include:\n  - path: infra/child.yml\n    env_file: /never/read/private.env\nservices:\n  app:\n    image: alpine:3\n    label_file: /never/read/labels\nsecrets:\n  token:\n    file: /never/read/token\n",
        )
        self.put("infra/child.yml", "services:\n  child:\n    image: alpine:3\n")
        doc = self.scan("docker-compose.yml", "infra/child.yml")[0]

        def run(command, **kwargs):
            copied_text = (kwargs["cwd"] / "docker-compose.yml").read_text()
            self.assertNotIn("/never/read", copied_text)
            self.assertIn(".p01-empty-input", copied_text)
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        result = render_inventory(self.root, doc, run=run)
        self.assertGreater(result["coverage"]["render"]["numerator"], 0)
        self.assertEqual(len(result["compose"]["synthetic_file_inputs"]), 3)

    def test_root_member_overlay_uses_root_context(self):
        self.put("docker-compose.yml", "include: [infra/compose.yml]\n")
        self.put("infra/compose.yml", "services: {app: {image: 'alpine:3'}}\n")
        overlay = "infra/compose.override.yml"
        self.put(
            overlay,
            "x-hyhome-overlay: {version: 1, base: infra/compose.yml}\nservices: {app: {read_only: true}}\n",
        )
        doc = self.scan("docker-compose.yml", "infra/compose.yml", overlay)[0]

        def run(command, **kwargs):
            files = [command[i + 1] for i, arg in enumerate(command) if arg == "-f"]
            self.assertEqual(files, ["docker-compose.yml", overlay])
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        result = render_inventory(
            self.root,
            doc,
            run=run,
            only_cases=[("infra/compose.yml", "overlay:" + overlay)],
        )
        self.assertEqual(
            result["compose"]["render_cases"][0]["files"],
            ["docker-compose.yml", overlay],
        )
        for files in (["docker-compose.yml"], [overlay, "docker-compose.yml"]):
            with (
                self.subTest(files=files),
                patch("subprocess.run") as runner,
                self.assertRaises(InventoryError),
            ):
                render_inventory(
                    self.root,
                    doc,
                    case_inputs=[
                        {
                            "source": "infra/compose.yml",
                            "selection": "overlay:" + overlay,
                            "files": files,
                        }
                    ],
                )
            runner.assert_not_called()

    def test_explicit_typed_inputs_are_synthetic_and_case_local(self):
        self.put(
            "compose.yml",
            "services: {app: {image: '${FIXTURE_IMAGE:?}', volumes: ['${FIXTURE_DIR:?}:/data']}}\n",
        )
        doc = self.scan("compose.yml")[0]
        inputs = [
            {
                "source": "compose.yml",
                "selection": "all-profiles",
                "variables": {"FIXTURE_IMAGE": "image", "FIXTURE_DIR": "directory"},
            }
        ]

        def run(command, **kwargs):
            self.assertEqual(
                kwargs["env"]["FIXTURE_IMAGE"], "example.invalid/p01/fixture:synthetic"
            )
            self.assertTrue(
                Path(kwargs["env"]["FIXTURE_DIR"]).is_relative_to(kwargs["cwd"])
            )
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        result = render_inventory(self.root, doc, run=run, case_inputs=inputs)
        self.assertEqual(
            result["compose"]["synthetic_interpolation_inputs"],
            [{**inputs[0], "files": ["compose.yml"]}],
        )
        self.assertNotIn("example.invalid", json.dumps(result))
        for invalid in (
            [{**inputs[0], "variables": {"DOCKER_HOST": "text"}}],
            [{**inputs[0], "variables": {"UNDECLARED": "text"}}],
            [{**inputs[0], "variables": {"FIXTURE_IMAGE": "actual-secret-value"}}],
            [{**inputs[0], "files": ["../outside.yml"]}],
            [{**inputs[0], "selection": "unknown"}],
            inputs + inputs,
        ):
            with self.subTest(invalid=invalid), self.assertRaises(InventoryError):
                render_inventory(self.root, doc, run=run, case_inputs=invalid)

        self.put("compose-other.yml", "services: {other: {image: 'alpine:3'}}\n")
        multiple = self.scan("compose.yml", "compose-other.yml")[0]
        with patch("subprocess.run") as runner, self.assertRaises(InventoryError):
            render_inventory(
                self.root,
                multiple,
                case_inputs=[
                    {
                        "source": "compose.yml",
                        "selection": "all-profiles",
                        "variables": {"UNDECLARED": "text"},
                    }
                ],
            )
        runner.assert_not_called()

    def test_render_failure_categories_never_copy_diagnostic_values(self):
        doc = self.render_fixture()
        for stderr, reason in (
            (
                b"error while interpolating services.app.image: required variable PRIVATE is missing a value",
                "missing-required-interpolation",
            ),
            (
                b"service app refers to undefined network PRIVATE: invalid compose project",
                "undefined-network",
            ),
            (
                b"service app has neither an image nor a build context specified: invalid compose project PRIVATE",
                "missing-service-definition",
            ),
            (b"UNKNOWN PRIVATE", "configuration-not-rendered"),
        ):
            result = render_inventory(
                self.root,
                doc,
                run=lambda *a, diagnostic=stderr, **k: subprocess.CompletedProcess(
                    a, 1, b"", diagnostic
                ),
            )
            self.assertTrue(
                all(r["reason"] == reason for r in result["compose"]["render_cases"])
            )
            self.assertNotIn("PRIVATE", json.dumps(result))

    def test_render_rejects_transitive_external_include_before_any_invocation(self):
        self.put("docker-compose.yml", "include: [infra/child.yml]\n")
        self.put("infra/child.yml", "include: [/outside/private.yml]\n")
        doc = self.scan("docker-compose.yml", "infra/child.yml")[0]
        with patch("subprocess.run", side_effect=AssertionError("must not invoke")):
            result = render_inventory(self.root, doc)
        self.assertTrue(
            all(r["result"] == "NOT_RUN" for r in result["compose"]["render_cases"])
        )

    def test_validator_requires_observation_provenance_and_disjoint_writer_scopes(self):
        self.put("a.py")
        doc = self.scan("a.py")[0]
        for observations, ownership in (
            ([{"level": "runtime", "result": "PASS"}], []),
            (
                [],
                [
                    {"path": "a.py", "writer": "a"},
                    {"path": "a.py", "section": "part", "writer": "b"},
                ],
            ),
        ):
            with self.assertRaises(InventoryError):
                validate({**doc, "observations": observations, "ownership": ownership})

    def test_binary_is_classified_without_opening_content(self):
        self.put("tests/fixture.png", "synthetic binary")
        with patch(
            "scripts.lib.ops.workspace_inventory._read_public",
            side_effect=AssertionError("must not open"),
        ):
            doc = self.scan("tests/fixture.png")[0]
        self.assertEqual(doc["files"][0]["state"], "BINARY_NOT_OPENED")

    def test_merged_include_paths_cannot_load_a_host_project_directory(self):
        self.put(
            "docker-compose.yml",
            "x-defaults: &d\n  path: infra/child.yml\n  project_directory: /host/private\ninclude:\n  - <<: *d\n",
        )
        self.put("infra/child.yml", "services: {app: {image: 'alpine:3'}}\n")
        doc = self.scan("docker-compose.yml", "infra/child.yml")[0]
        with patch("subprocess.run", side_effect=AssertionError("must not invoke")):
            result = render_inventory(self.root, doc)
        self.assertTrue(
            all(r["result"] == "NOT_RUN" for r in result["compose"]["render_cases"])
        )

    def test_render_preserves_service_merge_precedence_without_literal_merge_keys(self):
        import yaml

        self.put(
            "docker-compose.yml",
            "x-base: &base {image: 'alpine:1', restart: always}\nservices:\n  app:\n    <<: *base\n    image: alpine:3\n",
        )
        doc = self.scan("docker-compose.yml")[0]

        def run(command, **kwargs):
            text = (kwargs["cwd"] / "docker-compose.yml").read_text()
            self.assertNotIn("!!merge", text)
            model = yaml.safe_load(text)
            self.assertEqual(
                model["services"]["app"], {"image": "alpine:3", "restart": "always"}
            )
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        result = render_inventory(self.root, doc, run=run)
        self.assertEqual(result["coverage"]["render"]["numerator"], 2)

    def test_render_can_resume_only_named_remaining_cases(self):
        doc = self.render_fixture()
        result = render_inventory(
            self.root,
            doc,
            only_cases=[("docker-compose.yml", "profile:dev")],
            run=lambda *a, **k: subprocess.CompletedProcess(
                a, 0, b'{"services":{"app":{}}}'
            ),
        )
        self.assertEqual(
            result["coverage"]["render"], {"numerator": 1, "denominator": 1}
        )
        with self.assertRaises(InventoryError):
            render_inventory(
                self.root, doc, only_cases=[("docker-compose.yml", "unknown")]
            )

    def test_same_length_symlink_retarget_is_a_change(self):
        target = self.root / "link.py"
        target.symlink_to("one")
        before = self.scan("link.py")[0]
        target.unlink()
        target.symlink_to("two")
        after = self.scan("link.py")[0]
        self.assertEqual(compare(before, after)["changed"], ["link.py"])

    def test_changed_compose_between_collection_passes_is_rejected(self):
        from scripts.lib.ops._workspace_services import inspect_services

        self.put("docker-compose.yml", "services: {app: {image: 'alpine:1'}}\n")

        def inspect(root, paths):
            self.put("docker-compose.yml", "services: {app: {image: 'alpine:2'}}\n")
            return inspect_services(root, paths)

        with patch(
            "scripts.lib.ops._workspace_services.inspect_services", side_effect=inspect
        ):
            with self.assertRaises(InventoryError):
                self.scan("docker-compose.yml")

    def test_unrelated_unsafe_project_does_not_block_valid_root_render(self):
        self.put("docker-compose.yml", "services: {app: {image: 'alpine:3'}}\n")
        self.put("compose-other.yml", "include: [/outside/private.yml]\n")
        doc = self.scan("docker-compose.yml", "compose-other.yml")[0]

        def run(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, b'{"services":{"app":{}}}')

        rendered = render_inventory(self.root, doc, run=run)
        rows = rendered["compose"]["render_cases"]
        self.assertTrue(
            all(
                r["result"] == "PASS"
                for r in rows
                if r["source"] == "docker-compose.yml"
            )
        )
        self.assertTrue(
            all(
                r["result"] == "NOT_RUN"
                for r in rows
                if r["source"] == "compose-other.yml"
            )
        )


if __name__ == "__main__":
    unittest.main()
