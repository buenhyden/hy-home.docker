"""Synthetic declaration inventory never reads operational input values."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.ops._workspace_services import inspect_services


class WorkspaceServicesTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, path, body):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)
        return path

    def test_root_closure_and_separate_project_have_distinct_membership(self):
        paths = [
            self.write("docker-compose.yml", "include: [infra/compose.yml]\n"),
            self.write("infra/compose.yml", "services:\n  db: {image: 'db:1'}\n"),
            self.write("other/compose.yml", "services:\n  db: {image: 'db:2'}\n"),
        ]
        result = inspect_services(self.root, paths)
        self.assertEqual(len(result["services"]), 2)
        self.assertEqual(result["root_services"], ["db"])
        members = {row["source"]: row["root_member"] for row in result["services"]}
        self.assertEqual(
            members, {"infra/compose.yml": True, "other/compose.yml": False}
        )
        self.assertEqual(result["render_cases"], [])

    def test_metadata_projection_does_not_disclose_operational_values(self):
        path = self.write(
            "compose.yml",
            """services:
  api:
    image: ${IMAGE:-PRIVATE_IMAGE_MARKER}
    environment: {TOKEN: PRIVATE_ENV_MARKER}
    env_file: PRIVATE_ENV_FILE_MARKER
    command: PRIVATE_COMMAND_MARKER
    profiles: [dev]
    networks: [local]
    ports: ['127.0.0.1:8080:80']
    secrets: [{source: api-token, target: private-target}]
    volumes: ['${PRIVATE_MOUNT_MARKER}:/run/data', 'data:/data']
    depends_on: {db: {condition: service_healthy}}
    healthcheck: {test: PRIVATE_HEALTH_MARKER}
  db: {image: 'db:1'}
networks: {local: {}}
""",
        )
        result = inspect_services(self.root, [path])
        serialized = json.dumps(result)
        self.assertNotIn("PRIVATE_", serialized)
        api, db = result["services"]
        self.assertIsNone(api["image"])
        self.assertEqual(api["secrets"], ["api-token"])
        self.assertEqual(api["mounts"][0]["source"], None)
        self.assertEqual(api["mounts"][1]["source"], "data")
        self.assertEqual(db["consumers"], ["compose.yml::api"])
        self.assertEqual(api["ports"]["host_publication"]["state"], "declared")
        dns = api["ports"]["internal_dns"]["endpoints"][0]
        self.assertEqual(dns["network_reference"], "local")
        self.assertNotIn("network_key", dns)

    def test_long_include_and_extends_only_read_allowlisted_sources(self):
        paths = [
            self.write(
                "compose.yml",
                "include:\n - path: [child/base.yml]\n   project_directory: child\n   env_file: child/.env\nservices:\n  app:\n    extends: {file: child/common.yml, service: base}\n",
            ),
            self.write("child/base.yml", "services: {db: {image: 'db:1'}}\n"),
            self.write("child/common.yml", "services: {base: {image: 'base:1'}}\n"),
        ]
        self.write("child/.env", "PRIVATE_INPUT_MARKER")
        result = inspect_services(self.root, paths)
        self.assertEqual(len(result["sources"]), 3)
        self.assertEqual(result["relations"][0]["env_file"], ["child/.env"])
        self.assertEqual(result["relations"][1]["kind"], "extends")
        self.assertEqual(result["gaps"], [])
        self.assertNotIn("PRIVATE_INPUT_MARKER", json.dumps(result))

    def test_duplicate_mapping_keys_are_rejected_without_yaml_value_echo(self):
        path = self.write(
            "compose.yml",
            "services:\n  app: {image: PRIVATE_FIRST}\n  app: {image: PRIVATE_SECOND}\n",
        )
        result = inspect_services(self.root, [path])
        self.assertEqual(result["services"], [])
        self.assertEqual(result["gaps"][0]["code"], "duplicate_yaml_key")
        self.assertNotIn("PRIVATE_", json.dumps(result))

    def test_duplicate_root_declarations_remain_visible_and_unresolved(self):
        paths = [
            self.write(
                "docker-compose.yml",
                "include: [infra/compose-a.yml, infra/compose-b.yml]",
            ),
            self.write("infra/compose-a.yml", "services: {db: {}}"),
            self.write("infra/compose-b.yml", "services: {db: {}}"),
        ]
        result = inspect_services(self.root, paths)
        self.assertEqual(len(result["services"]), 2)
        self.assertIn("duplicate_root_service", {gap["code"] for gap in result["gaps"]})

    def test_cycles_missing_refs_and_boundary_escape_are_explicit(self):
        paths = [
            self.write(
                "compose.yml",
                "include: [child/compose.yml, missing.yml, ../PRIVATE_ESCAPE]",
            ),
            self.write("child/compose.yml", "include: [../compose.yml]"),
        ]
        result = inspect_services(self.root, paths)
        codes = {gap["code"] for gap in result["gaps"]}
        self.assertTrue(
            {
                "include_cycle",
                "source_not_allowlisted",
                "unsafe_or_unresolved_reference",
            }
            <= codes
        )
        self.assertNotIn("PRIVATE_ESCAPE", json.dumps(result))

    def test_symlink_and_non_public_path_are_not_read(self):
        outside = Path(self.directory.name).parent / (self.root.name + "-outside")
        outside.write_text("PRIVATE_OUTSIDE_MARKER")
        self.addCleanup(outside.unlink)
        (self.root / "compose.yml").symlink_to(outside)
        result = inspect_services(
            self.root, ["compose.yml", "/PRIVATE_ABSOLUTE", "../escape", ".env"]
        )
        self.assertEqual(result["services"], [])
        self.assertNotIn("PRIVATE_", json.dumps(result))
        self.assertEqual(len(result["gaps"]), 3)

    def test_labs_declaration_and_invalid_yaml_are_separate(self):
        paths = [
            self.write(
                "labs/sample/docker-compose.yml", "services: {lab: {image: 'lab:1'}}"
            ),
            self.write("compose-bad.yaml", "services: [PRIVATE_BAD]"),
            self.write("other/not-compose.yml", "PRIVATE_NOT_A_CANDIDATE"),
        ]
        result = inspect_services(self.root, paths)
        self.assertEqual([row["service"] for row in result["services"]], ["lab"])
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(result["gaps"][0]["code"], "source_unreadable_or_invalid")

    def test_extends_missing_service_and_bad_port_remain_unverified(self):
        path = self.write(
            "compose.yml",
            "services:\n  app:\n    extends: {service: absent}\n    ports: [PRIVATE_INVALID_PORT]\n",
        )
        result = inspect_services(self.root, [path])
        self.assertEqual(
            {gap["code"] for gap in result["gaps"]},
            {"extends_service_missing", "endpoint_projection_unresolved"},
        )
        self.assertIsNone(result["services"][0]["ports"])
        self.assertNotIn("PRIVATE_INVALID_PORT", json.dumps(result))

    def test_failed_root_authority_does_not_drop_declarations(self):
        path = self.write("docker-compose.yml", "services: {app: {}}")
        with patch(
            "scripts.lib.ops._workspace_services.expected_from_root",
            side_effect=ValueError,
        ):
            result = inspect_services(self.root, [path])
        self.assertEqual(result["root_services"], ["app"])
        self.assertEqual(result["gaps"][0]["code"], "root_authority_unresolved")

    def test_digest_image_preserved_and_userinfo_or_defaults_hidden(self):
        digest = "registry:5000/team/image:1@sha256:" + "a" * 64
        path = self.write(
            "compose.yml",
            f"services:\n  pinned: {{image: '{digest}'}}\n  unsafe: {{image: 'user:PRIVATE@registry/image'}}\n",
        )
        result = inspect_services(self.root, [path])
        self.assertEqual(result["services"][0]["image"], digest)
        self.assertIsNone(result["services"][1]["image"])
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_include_self_and_local_extends_cycles_but_not_local_base(self):
        path = self.write(
            "compose.yml",
            "include: [compose.yml]\nservices:\n  app: {extends: {service: base}}\n  base: {image: 'base:1'}\n  loop: {extends: {service: loop}}\n",
        )
        result = inspect_services(self.root, [path])
        self.assertEqual(
            [gap["code"] for gap in result["gaps"]].count("extends_cycle"), 1
        )
        self.assertIn("include_cycle", {gap["code"] for gap in result["gaps"]})

    def test_unrelated_invalid_source_does_not_skip_root_authority(self):
        paths = [
            self.write("docker-compose.yml", "services: {app: {}}"),
            self.write("compose-bad.yml", "services: [broken]"),
        ]
        with patch(
            "scripts.lib.ops._workspace_services.expected_from_root",
            side_effect=ValueError,
        ) as expected:
            result = inspect_services(self.root, paths)
        expected.assert_called_once()
        self.assertIn(
            "root_authority_unresolved", {gap["code"] for gap in result["gaps"]}
        )

    def test_documented_overlay_targets_repository_base_and_is_not_entrypoint(self):
        paths = [
            self.write("docker-compose.yml", "services: {app: {image: 'app:1'}}"),
            self.write(
                "infra/deep/compose.workflow.override.yml",
                "x-hyhome-overlay: {version: 1, base: docker-compose.yml}\nservices: {app: {networks: {internal: {}}}}",
            ),
        ]
        result = inspect_services(self.root, paths)
        self.assertIn(
            {"kind": "overlay", "source": paths[1], "target": "docker-compose.yml"},
            result["relations"],
        )
        self.assertEqual(result["entrypoints"], ["docker-compose.yml"])
        self.assertEqual(result["gaps"], [])

    def test_overlay_rejects_invalid_annotation_and_missing_base(self):
        for annotation, code in [
            ("{version: true, base: docker-compose.yml}", "invalid_overlay_annotation"),
            ("{version: 1, base: ../PRIVATE_OUTSIDE}", "invalid_overlay_annotation"),
            ("{version: 1, base: missing.yml}", "source_not_allowlisted"),
        ]:
            with self.subTest(annotation=annotation):
                path = self.write(
                    "compose.override.yml",
                    f"x-hyhome-overlay: {annotation}\nservices: {{app: {{}}}}",
                )
                result = inspect_services(self.root, [path])
                self.assertIn(code, {gap["code"] for gap in result["gaps"]})
                self.assertNotIn("PRIVATE_OUTSIDE", json.dumps(result))
                self.assertEqual(result["entrypoints"], [])


if __name__ == "__main__":
    unittest.main()
