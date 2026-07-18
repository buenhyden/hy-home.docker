from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/validation/check-document-metadata.py"
PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
SERVICE_EXAMPLE = ROOT / "examples/sample-web-service/service.md"
TARGET_MANIFEST = (
    ROOT
    / "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml"
)
TARGET_ROOTS = (".github", "archive", "examples", "infra", "projects", "scripts", "secrets", "tests")

spec = importlib.util.spec_from_file_location("target_surface_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def tracked_paths(*pathspecs: str) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *pathspecs],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return [pathlib.Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


class SampleServiceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)
        cls.text = SERVICE_EXAMPLE.read_text(encoding="utf-8")

    def test_sample_service_uses_canonical_metadata_in_canonical_order(self) -> None:
        self.assertEqual(
            {
                "status": "active",
                "artifact_id": "spec:sample-web-service",
                "artifact_type": "spec",
                "parent_ids": ["spec:133-target-surface-contract-convergence"],
            },
            metadata.parse_frontmatter(SERVICE_EXAMPLE),
        )
        frontmatter = self.text.split("---", 2)[1]
        keys = [
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if line and not line.startswith(" ")
        ]
        self.assertEqual(
            self.profiles["common"]["frontmatter_order"][:4],
            keys,
        )

    def test_sample_service_sections_follow_the_registered_service_role(self) -> None:
        role = self.profiles["template_roles"]["service"]
        headings = [line for line in self.text.splitlines() if line.startswith("## ")]
        self.assertEqual(role["required_headings"], headings)
        self.assertNotIn("## Template Usage", headings)

    def test_sample_service_contains_no_template_instruction_or_placeholder(self) -> None:
        for forbidden in (
            "<artifact-id>",
            "<parent-artifact-id>",
            "{{",
            "}}",
            "When authoring a real service",
            "copy the template",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.text)

    def test_migrated_typed_example_manifest_target_matches_document(self) -> None:
        document = metadata._safe_load_unique(  # noqa: SLF001
            TARGET_MANIFEST.read_text(encoding="utf-8")
        )
        row = next(
            entry
            for entry in document["entries"]
            if entry["source_path"] == "examples/sample-web-service/service.md"
        )
        frontmatter = metadata.parse_frontmatter(SERVICE_EXAMPLE)

        self.assertEqual("typed-example", row["surface_class"])
        self.assertEqual("migrate", row["disposition"])
        self.assertEqual(
            {
                "artifact_id": frontmatter["artifact_id"],
                "artifact_type_after": frontmatter["artifact_type"],
                "parent_ids": frontmatter["parent_ids"],
            },
            {
                "artifact_id": row["artifact_id"],
                "artifact_type_after": row["artifact_type_after"],
                "parent_ids": row["parent_ids"],
            },
        )


class TargetReadmeProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_all_75_target_readmes_match_exactly_one_profile(self) -> None:
        readmes = [
            path
            for path in tracked_paths(*TARGET_ROOTS)
            if path.name == "README.md"
        ]
        self.assertEqual(75, len(readmes))
        for path in readmes:
            with self.subTest(path=path.as_posix()):
                self.assertEqual(
                    1,
                    len(metadata.matching_readme_profiles(path, self.profiles)),
                )

    def test_native_markdown_and_typed_example_do_not_inherit_readme_profiles(self) -> None:
        native_or_typed_paths = (
            pathlib.Path(".github/PULL_REQUEST_TEMPLATE.md"),
            pathlib.Path(".github/SECURITY.md"),
            pathlib.Path("examples/sample-web-service/service.md"),
        )
        for path in native_or_typed_paths:
            with self.subTest(path=path.as_posix()):
                self.assertEqual(
                    [], metadata.matching_readme_profiles(path, self.profiles)
                )


class StorybookPhantomContractTests(unittest.TestCase):
    def test_active_surfaces_have_no_storybook_mcp_phantom_reference(self) -> None:
        active_paths = (
            ROOT / ".prettierignore",
            ROOT / "projects/storybook/README.md",
            ROOT / "projects/storybook/nextjs/README.md",
            ROOT / "scripts/knowledge/report-graphify-health.sh",
            ROOT / "scripts/hooks/agent-event-hook.sh",
        )
        for path in active_paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn(
                    "projects/storybook/mcp", path.read_text(encoding="utf-8")
                )

    def test_storybook_has_no_tracked_gitlink(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", "projects/storybook"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertFalse(
            any(line.startswith("160000 ") for line in result.stdout.splitlines())
        )

    def test_historical_spec_and_plan_evidence_remains_allowed(self) -> None:
        historical_owners = (
            ROOT / "docs/03.specs/133-target-surface-contract-convergence/spec.md",
            ROOT / "docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md",
        )
        for path in historical_owners:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn(
                    "projects/storybook/mcp", path.read_text(encoding="utf-8")
                )


class DeprecatedRuntimeContractTests(unittest.TestCase):
    def test_influxdb_v2_compose_is_removed(self) -> None:
        self.assertFalse(
            (
                ROOT
                / "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
            ).exists()
        )

    def test_v2_only_example_and_metadata_keys_are_removed(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        metadata_example = (
            ROOT / "secrets/SENSITIVE_ENV_VARS.md.example"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "INFLUXDB_ORG",
            "INFLUXDB_BUCKET",
            "INFLUXDB_USERNAME",
        ):
            with self.subTest(path=".env.example", forbidden=forbidden):
                self.assertNotIn(forbidden, env_example)
        self.assertIn("INFLUXDB_DB_NAME", env_example)
        self.assertNotIn("INFLUXDB_USERNAME", metadata_example)
        self.assertIn("influxdb_api_token", metadata_example)

    def test_locust_image_has_no_influxdb_v2_client(self) -> None:
        dockerfile = (ROOT / "infra/09-tooling/locust/Dockerfile").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("influxdb-client", dockerfile)

    def test_k6_and_locust_have_no_unused_influxdb_wiring(self) -> None:
        compose_paths = (
            ROOT / "infra/09-tooling/k6/docker-compose.yml",
            ROOT / "infra/09-tooling/locust/docker-compose.yml",
        )
        for path in compose_paths:
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "LOCUST_INFLUXDB_",
                "influxdb_api_token",
                "depends_on:\n      influxdb:",
            ):
                with self.subTest(
                    path=path.relative_to(ROOT).as_posix(), forbidden=forbidden
                ):
                    self.assertNotIn(forbidden, text)

    def test_influxdb_leaf_does_not_claim_unprovisioned_token_wiring(self) -> None:
        leaf_compose = (
            ROOT / "infra/04-data/analytics/influxdb/docker-compose.yml"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "influxdb_password",
            "influxdb_api_token",
            "--admin-token-file",
            "INFLUXDB3_ADMIN_TOKEN_FILE",
        ):
            with self.subTest(owner="leaf-compose", forbidden=forbidden):
                self.assertNotIn(forbidden, leaf_compose)

        current_docs = (
            ROOT / "infra/04-data/analytics/influxdb/README.md",
            ROOT / "docs/03.specs/005-data-analytics/spec.md",
            ROOT / "docs/05.operations/guides/04-data/analytics/influxdb.md",
            ROOT / "docs/05.operations/policies/04-data/analytics/influxdb.md",
            ROOT / "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
        )
        corpus = "\n".join(path.read_text(encoding="utf-8") for path in current_docs)
        for forbidden in (
            "Compose mounts `influxdb_api_token`",
            "Docker Secret `influxdb_api_token`을 사용한다",
            "Authorization: Bearer token from the influxdb_api_token secret",
            "docker exec influxdb test -r /run/secrets/influxdb_api_token",
            "source Compose declares `influxdb_api_token`",
        ):
            with self.subTest(owner="current-docs", forbidden=forbidden):
                self.assertNotIn(forbidden, corpus)
        for required in (
            "root declarations and metadata are not leaf server wiring",
            "separate runtime approval",
            "source-only validation cannot prove authorization",
            "https://docs.influxdata.com/influxdb3/core/admin/tokens/",
        ):
            with self.subTest(owner="current-docs", required=required):
                self.assertIn(required, corpus)

    def test_active_docs_describe_only_influxdb_3_contract(self) -> None:
        active_paths = (
            ROOT / "infra/04-data/analytics/influxdb/README.md",
            ROOT / "docs/01.requirements/005-data-analytics.md",
            ROOT / "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
            ROOT / "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
            ROOT / "docs/03.specs/005-data-analytics/README.md",
            ROOT / "docs/03.specs/005-data-analytics/spec.md",
            ROOT / "docs/05.operations/guides/04-data/analytics/README.md",
            ROOT / "docs/05.operations/guides/04-data/analytics/influxdb.md",
            ROOT / "docs/05.operations/policies/04-data/analytics/influxdb.md",
            ROOT / "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
        )
        for path in active_paths:
            text = path.read_text(encoding="utf-8")
            for forbidden in (
                "InfluxDB 2",
                "docker-compose.v2.yml",
                "legacy Flux",
                "8086",
            ):
                with self.subTest(
                    path=path.relative_to(ROOT).as_posix(), forbidden=forbidden
                ):
                    self.assertNotIn(forbidden, text)

        canonical_docs = (
            ROOT / "infra/04-data/analytics/influxdb/README.md",
            ROOT / "docs/03.specs/005-data-analytics/spec.md",
            ROOT / "docs/05.operations/guides/04-data/analytics/influxdb.md",
        )
        for path in canonical_docs:
            text = path.read_text(encoding="utf-8")
            for required in (
                "InfluxDB 3",
                "8181",
                "/api/v3/write_lp",
                "INFLUXDB_DB_NAME",
            ):
                with self.subTest(
                    path=path.relative_to(ROOT).as_posix(), required=required
                ):
                    self.assertIn(required, text)

    def test_historical_and_negative_influxdb_v2_evidence_remains_allowed(self) -> None:
        historical_owners = (
            ROOT / "docs/03.specs/133-target-surface-contract-convergence/spec.md",
            ROOT / "docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md",
        )
        for path in historical_owners:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("InfluxDB 2", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
