from __future__ import annotations

import contextlib
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/validation/check-document-metadata.py"
LIFECYCLE_CHECKER = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
SERVICE_EXAMPLE = ROOT / "examples/sample-web-service/service.md"
TARGET_MANIFEST = (
    ROOT
    / "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml"
)
TARGET_SUMMARY = TARGET_MANIFEST.with_name("target-surface-convergence-summary.md")
TARGET_VALIDATOR = ROOT / "scripts/validation/target_surface_contract.py"
TARGET_CLI = ROOT / "scripts/validation/check-target-surface-contract.py"
TARGET_ROOTS = (
    ".github",
    "archive",
    "examples",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
)
EXPECTED_FINDING_CODES = frozenset(
    {
        "target-duplicate-disposition-invalid",
        "target-manifest-coverage-missing",
        "target-manifest-invalid",
        "target-phantom-gitlink-claim",
        "target-phantom-gitlink-present",
        "target-removed-active-claim",
        "target-removed-path-present",
        "target-sample-service-metadata-invalid",
        "target-sample-service-sections-invalid",
        "target-sample-service-template-residue",
    }
)
PHANTOM_CLAIM_PATHS = (
    ".prettierignore",
    "projects/storybook/README.md",
    "projects/storybook/nextjs/README.md",
    "scripts/knowledge/report-graphify-health.sh",
    "scripts/hooks/agent-event-hook.sh",
)
INFLUX_ACTIVE_PATHS = (
    "infra/04-data/analytics/influxdb/README.md",
    "docs/01.requirements/005-data-analytics.md",
    "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
    "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
    "docs/03.specs/005-data-analytics/README.md",
    "docs/03.specs/005-data-analytics/spec.md",
    "docs/05.operations/guides/04-data/analytics/README.md",
    "docs/05.operations/guides/04-data/analytics/influxdb.md",
    "docs/05.operations/policies/04-data/analytics/influxdb.md",
    "docs/05.operations/runbooks/04-data/analytics/influxdb.md",
)
INFLUX_V2_PATH = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
OPENSEARCH_DUPLICATE_PATH = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example"
)
OPENSEARCH_RETAINED_PATH = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt"
)

VALID_SAMPLE_SERVICE = """---
status: active
artifact_id: spec:sample-web-service
artifact_type: spec
parent_ids:
  - spec:133-target-surface-contract-convergence
---

# sample-web-service Service Contract

## Overview

Fixture overview.

## Parent and Scope

Fixture scope.

## Image and Build

Fixture image.

## Security

Fixture security.

## Networking and Storage

Fixture network.

## Secrets

Fixture secret boundary.

## Health and Operations

Fixture health.

## Validation

Fixture validation.

## Related Documents

- Fixture relation.
"""

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
    return [
        pathlib.Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw
    ]


def load_target_validator():
    validator_spec = importlib.util.spec_from_file_location(
        "target_surface_contract", TARGET_VALIDATOR
    )
    if validator_spec is None or validator_spec.loader is None:
        raise RuntimeError(f"unable to load target validator: {TARGET_VALIDATOR}")
    module = importlib.util.module_from_spec(validator_spec)
    sys.modules[validator_spec.name] = module
    validator_spec.loader.exec_module(module)
    return module


def _write_text(root: pathlib.Path, relative: str, text: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _manifest_row(path: str) -> dict[str, object]:
    surface_class = "configuration"
    if path.endswith("README.md"):
        surface_class = "readme"
    elif path == "examples/sample-web-service/service.md":
        surface_class = "typed-example"
    elif path.endswith(".sh"):
        surface_class = "executable-script"
    elif path.endswith("docker-compose.v2.yml"):
        surface_class = "runtime"
    elif path == OPENSEARCH_RETAINED_PATH:
        surface_class = "unsupported-static"

    row: dict[str, object] = {
        "source_path": path,
        "target_path": path,
        "surface_class": surface_class,
        "disposition": "preserve",
        "review_verdict": {"specification": "pending", "quality": "pending"},
    }
    if path == "examples/sample-web-service/service.md":
        row["disposition"] = "migrate"
    if path in {INFLUX_V2_PATH, OPENSEARCH_DUPLICATE_PATH}:
        row.update(
            {
                "target_path": None,
                "disposition": "delete",
                "review_verdict": {"specification": "pass", "quality": "pass"},
            }
        )
    return row


@contextlib.contextmanager
def target_contract_fixture():
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Target Contract Test"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "target@example.invalid"],
            cwd=root,
            check=True,
        )

        files: dict[str, str] = {
            ".prettierignore": "# governed ignore paths\n",
            "examples/sample-web-service/service.md": VALID_SAMPLE_SERVICE,
            INFLUX_V2_PATH: "services: {}\n",
            OPENSEARCH_DUPLICATE_PATH: "",
            OPENSEARCH_RETAINED_PATH: "",
        }
        files.update(
            {path: "Current target surface.\n" for path in PHANTOM_CLAIM_PATHS[1:]}
        )
        files.update(
            {path: "InfluxDB 3 current contract.\n" for path in INFLUX_ACTIVE_PATHS}
        )
        for relative, text in files.items():
            _write_text(root, relative, text)

        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "fixture baseline"], cwd=root, check=True
        )
        baseline = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        (root / INFLUX_V2_PATH).unlink()
        (root / OPENSEARCH_DUPLICATE_PATH).unlink()

        manifest = root / TARGET_MANIFEST.relative_to(ROOT)
        manifest.parent.mkdir(parents=True, exist_ok=True)
        document = {
            "schema_version": 2,
            "wave": "target-surface-convergence",
            "baseline_commit": baseline,
            "generated_by": "check-document-corpus-lifecycle.py",
            "enforcement": "advisory",
            "entries": [_manifest_row(path) for path in sorted(files)],
        }
        manifest.write_text(
            yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        yield root, manifest, baseline


def _mutate_manifest(manifest: pathlib.Path, mutation) -> None:
    document = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    mutation(document)
    manifest.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


class TargetSurfaceValidatorPublicContractTests(unittest.TestCase):
    def test_validator_exposes_every_stable_target_finding_code(self) -> None:
        validator = load_target_validator()
        self.assertEqual(EXPECTED_FINDING_CODES, validator.FINDING_CODES)
        finding = validator.Finding("code", "safe/path", "message")
        with self.assertRaises((AttributeError, TypeError)):
            finding.code = "changed"

    def test_thin_cli_accepts_the_current_repository_without_diagnostics(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TARGET_CLI)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)


class TargetSurfaceValidatorFindingTests(unittest.TestCase):
    def _findings(
        self, root: pathlib.Path, manifest: pathlib.Path
    ) -> tuple[object, ...]:
        return load_target_validator().validate(root, manifest)

    def _assert_code(
        self,
        expected: str,
        root: pathlib.Path,
        manifest: pathlib.Path,
        *,
        path: str | None = None,
    ) -> tuple[object, ...]:
        findings = self._findings(root, manifest)
        matches = [finding for finding in findings if finding.code == expected]
        self.assertEqual(1, len(matches), findings)
        if path is not None:
            self.assertEqual(path, matches[0].path)
        self.assertEqual(tuple(sorted(findings)), findings)
        return findings

    def test_invalid_manifest_is_value_free(self) -> None:
        sentinel = "manifest-secret-sentinel"
        with target_contract_fixture() as (root, manifest, _baseline):
            manifest.write_text(f"entries: [{{unsafe: {sentinel}}}\n", encoding="utf-8")
            findings = self._assert_code(
                "target-manifest-invalid",
                root,
                manifest,
                path=manifest.relative_to(root).as_posix(),
            )
        self.assertNotIn(sentinel, repr(findings))

    def test_duplicate_manifest_keys_fail_closed_without_values(self) -> None:
        sentinel = "duplicate-manifest-secret-sentinel"
        mutations = (
            (
                "top-level",
                "wave: target-surface-convergence\n",
                "wave: target-surface-convergence\n"
                f"wave: target-surface-convergence # {sentinel}\n",
            ),
            (
                "row-level",
                "- source_path: .prettierignore\n",
                "- source_path: .prettierignore\n"
                f"  source_path: .prettierignore # {sentinel}\n",
            ),
        )
        for label, old, new in mutations:
            with (
                self.subTest(label=label),
                target_contract_fixture() as (
                    root,
                    manifest,
                    _baseline,
                ),
            ):
                text = manifest.read_text(encoding="utf-8")
                self.assertIn(old, text)
                manifest.write_text(text.replace(old, new, 1), encoding="utf-8")
                findings = self._findings(root, manifest)
                self.assertEqual(1, len(findings), findings)
                self.assertEqual("target-manifest-invalid", findings[0].code)
                self.assertEqual(
                    manifest.relative_to(root).as_posix(), findings[0].path
                )
                self.assertNotIn(sentinel, repr(findings))

    def test_manifest_must_cover_every_baseline_target_path(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            _mutate_manifest(
                manifest,
                lambda document: document["entries"].__setitem__(
                    slice(None),
                    [
                        row
                        for row in document["entries"]
                        if row["source_path"] != ".prettierignore"
                    ],
                ),
            )
            self._assert_code(
                "target-manifest-coverage-missing",
                root,
                manifest,
                path=".prettierignore",
            )

    def test_reviewed_removed_path_must_stay_absent(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            _write_text(root, INFLUX_V2_PATH, "services: {}\n")
            self._assert_code(
                "target-removed-path-present",
                root,
                manifest,
                path=INFLUX_V2_PATH,
            )

    def test_removed_active_claim_is_value_free(self) -> None:
        sentinel = "claim-secret-sentinel"
        path = "infra/04-data/analytics/influxdb/README.md"
        with target_contract_fixture() as (root, manifest, _baseline):
            _write_text(root, path, f"InfluxDB 2 {sentinel}\n")
            findings = self._assert_code(
                "target-removed-active-claim", root, manifest, path=path
            )
        self.assertNotIn(sentinel, repr(findings))

    def test_removed_active_claim_patterns_are_bounded_and_case_insensitive(
        self,
    ) -> None:
        path = "infra/04-data/analytics/influxdb/README.md"
        sentinel = "runtime-claim-secret-sentinel"
        removed_claims = (
            "InfluxDB v2",
            "influxdb 2",
            "legacy flux",
            "DOCKER-COMPOSE.V2.YML",
            "8086",
        )
        for claim in removed_claims:
            with (
                self.subTest(claim=claim),
                target_contract_fixture() as (
                    root,
                    manifest,
                    _baseline,
                ),
            ):
                _write_text(root, path, f"{claim} {sentinel}\n")
                findings = self._assert_code(
                    "target-removed-active-claim", root, manifest, path=path
                )
                self.assertNotIn(sentinel, repr(findings))

        safe_controls = (
            "InfluxDB 20",
            "InfluxDB v20",
            "legacy fluxion",
            "docker-compose.v2.yml.bak",
            "18086",
        )
        with target_contract_fixture() as (root, manifest, _baseline):
            _write_text(root, path, "\n".join(safe_controls) + "\n")
            _write_text(root, "archive/historical-influxdb.md", "InfluxDB v2\n")
            self.assertEqual((), self._findings(root, manifest))

    def test_phantom_gitlink_claim_is_value_free(self) -> None:
        sentinel = "phantom-secret-sentinel"
        with target_contract_fixture() as (root, manifest, _baseline):
            _write_text(
                root,
                ".prettierignore",
                f"projects/storybook/mcp {sentinel}\n",
            )
            findings = self._assert_code(
                "target-phantom-gitlink-claim",
                root,
                manifest,
                path=".prettierignore",
            )
        self.assertNotIn(sentinel, repr(findings))

    def test_phantom_gitlink_index_entry_is_rejected(self) -> None:
        with target_contract_fixture() as (root, manifest, baseline):
            subprocess.run(
                [
                    "git",
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    f"160000,{baseline},projects/storybook/mcp",
                ],
                cwd=root,
                check=True,
            )
            self._assert_code(
                "target-phantom-gitlink-present",
                root,
                manifest,
                path="projects/storybook/mcp",
            )

    def test_sample_service_metadata_is_exact(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            service = root / "examples/sample-web-service/service.md"
            service.write_text(
                service.read_text(encoding="utf-8").replace(
                    "spec:sample-web-service", "spec:wrong-service", 1
                ),
                encoding="utf-8",
            )
            self._assert_code(
                "target-sample-service-metadata-invalid",
                root,
                manifest,
                path="examples/sample-web-service/service.md",
            )

    def test_sample_service_sections_are_exact(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            service = root / "examples/sample-web-service/service.md"
            service.write_text(
                service.read_text(encoding="utf-8").replace("## Security\n", ""),
                encoding="utf-8",
            )
            self._assert_code(
                "target-sample-service-sections-invalid",
                root,
                manifest,
                path="examples/sample-web-service/service.md",
            )

    def test_sample_service_rejects_template_residue_without_echo(self) -> None:
        sentinel = "template-secret-sentinel"
        with target_contract_fixture() as (root, manifest, _baseline):
            service = root / "examples/sample-web-service/service.md"
            service.write_text(
                service.read_text(encoding="utf-8") + f"\n{{{{ {sentinel} }}}}\n",
                encoding="utf-8",
            )
            findings = self._assert_code(
                "target-sample-service-template-residue",
                root,
                manifest,
                path="examples/sample-web-service/service.md",
            )
        self.assertNotIn(sentinel, repr(findings))

    def test_reviewed_duplicate_disposition_is_exact(self) -> None:
        def mutation(document: dict[str, object]) -> None:
            row = next(
                entry
                for entry in document["entries"]
                if entry["source_path"] == OPENSEARCH_DUPLICATE_PATH
            )
            row["review_verdict"] = {
                "specification": "pass",
                "quality": "pending",
            }

        with target_contract_fixture() as (root, manifest, _baseline):
            _mutate_manifest(manifest, mutation)
            self._assert_code(
                "target-duplicate-disposition-invalid",
                root,
                manifest,
                path=OPENSEARCH_DUPLICATE_PATH,
            )

    def test_clean_fixture_has_no_findings(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            self.assertEqual((), self._findings(root, manifest))


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

    def test_sample_service_contains_no_template_instruction_or_placeholder(
        self,
    ) -> None:
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
            path for path in tracked_paths(*TARGET_ROOTS) if path.name == "README.md"
        ]
        self.assertEqual(75, len(readmes))
        for path in readmes:
            with self.subTest(path=path.as_posix()):
                self.assertEqual(
                    1,
                    len(metadata.matching_readme_profiles(path, self.profiles)),
                )

    def test_native_markdown_and_typed_example_do_not_inherit_readme_profiles(
        self,
    ) -> None:
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
            ROOT
            / "docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md",
        )
        for path in historical_owners:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn(
                    "projects/storybook/mcp", path.read_text(encoding="utf-8")
                )


class DeprecatedRuntimeContractTests(unittest.TestCase):
    def test_opensearch_duplicate_example_is_removed_but_mounted_file_remains(
        self,
    ) -> None:
        duplicate = pathlib.Path(
            "infra/04-data/analytics/opensearch/opensearch/config/"
            "userdict_ko.txt.example"
        )
        retained = pathlib.Path(
            "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt"
        )
        self.assertFalse((ROOT / duplicate).exists())
        self.assertTrue((ROOT / retained).is_file())

        pre_delete_commit = "bad9a4a0aeb014c9eee398ea039ec0076723cd68"
        empty_blob = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
        for path in (duplicate, retained):
            with self.subTest(blob=path.as_posix()):
                result = subprocess.run(
                    [
                        "git",
                        "rev-parse",
                        f"{pre_delete_commit}:{path.as_posix()}",
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                self.assertEqual(empty_blob, result.stdout.strip())

        result = subprocess.run(
            ["git", "rev-parse", f"HEAD:{retained.as_posix()}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(empty_blob, result.stdout.strip())

        compose_paths = (
            ROOT / "infra/04-data/analytics/opensearch/docker-compose.yml",
            ROOT / "infra/04-data/analytics/opensearch/docker-compose.cluster.yml",
        )
        for path in compose_paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(compose=path.name):
                self.assertIn("userdict_ko.txt:", text)
                self.assertNotIn("userdict_ko.txt.example", text)

    def test_opensearch_duplicate_manifest_row_records_exact_delete_evidence(
        self,
    ) -> None:
        manifest = yaml.safe_load(TARGET_MANIFEST.read_text(encoding="utf-8"))
        source_path = (
            "infra/04-data/analytics/opensearch/opensearch/config/"
            "userdict_ko.txt.example"
        )
        retained_path = (
            "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt"
        )
        row = next(
            entry
            for entry in manifest["entries"]
            if entry["source_path"] == source_path
        )

        self.assertEqual(
            {
                "source_path": source_path,
                "target_path": None,
                "artifact_id": None,
                "artifact_type_before": None,
                "artifact_type_after": None,
                "surface_class": "configuration",
                "status_before": None,
                "status_after": None,
                "parent_ids": [],
                "disposition": "delete",
                "canonical_replacement": None,
                "active_consumers": [],
                "partition_plan": None,
                "preservation_class": "git-history",
                "evidence": {
                    "commands": [
                        "git diff --name-status bad9a4a0aeb014c9eee398ea039ec0076723cd68..190d2296c8ead19f3367157725694755f5d5cbe8 -- infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example",
                        "git log --format=%H bad9a4a0aeb014c9eee398ea039ec0076723cd68..190d2296c8ead19f3367157725694755f5d5cbe8 -- infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example",
                        "git rev-parse bad9a4a0aeb014c9eee398ea039ec0076723cd68:infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example bad9a4a0aeb014c9eee398ea039ec0076723cd68:infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt 190d2296c8ead19f3367157725694755f5d5cbe8:infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt",
                    ],
                    "sources": [retained_path, source_path],
                    "repository_paths": [retained_path, source_path],
                    "consumer_scan": [
                        "git grep -lz --fixed-strings -- userdict_ko.txt.example -- .env.example infra scripts secrets"
                    ],
                    "rollback": [
                        "git revert --no-commit 190d2296c8ead19f3367157725694755f5d5cbe8"
                    ],
                },
                "review_verdict": {
                    "specification": "pass",
                    "quality": "pass",
                },
            },
            row,
        )

        baseline = subprocess.run(
            [
                "git",
                "show",
                "190d2296c8ead19f3367157725694755f5d5cbe8:"
                "docs/90.references/data/governance/document-corpus-lifecycle/"
                "target-surface-convergence.yaml",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        baseline_manifest = yaml.safe_load(baseline.stdout)
        influxdb_path = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
        influxdb_row = next(
            entry
            for entry in manifest["entries"]
            if entry["source_path"] == influxdb_path
        )
        baseline_influxdb_row = next(
            entry
            for entry in baseline_manifest["entries"]
            if entry["source_path"] == influxdb_path
        )

        self.assertEqual(483, len(manifest["entries"]))
        self.assertEqual(
            [influxdb_path, source_path],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["disposition"] == "delete"
            ],
        )
        self.assertEqual(
            7,
            sum(entry["disposition"] == "migrate" for entry in manifest["entries"]),
        )
        self.assertEqual(
            474,
            sum(entry["disposition"] == "preserve" for entry in manifest["entries"]),
        )
        self.assertEqual(baseline_influxdb_row, influxdb_row)
        self.assertEqual(
            {"specification": "pass", "quality": "pass"},
            influxdb_row["review_verdict"],
        )
        other_paths = {source_path, influxdb_path}
        baseline_other_rows = [
            entry
            for entry in baseline_manifest["entries"]
            if entry["source_path"] not in other_paths
        ]
        current_other_rows = [
            entry
            for entry in manifest["entries"]
            if entry["source_path"] not in other_paths
        ]
        self.assertEqual(481, len(current_other_rows))
        self.assertEqual(baseline_other_rows, current_other_rows)
        self.assertTrue(
            all(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in current_other_rows
            )
        )
        self.assertEqual(
            [influxdb_path, source_path],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["review_verdict"]
                == {"specification": "pass", "quality": "pass"}
            ],
        )
        self.assertEqual(
            481,
            sum(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in manifest["entries"]
            ),
        )

        summary = TARGET_SUMMARY.read_text(encoding="utf-8")
        for expected in (
            "- Entries: 483",
            "- `delete`: 2",
            "- `migrate`: 7",
            "- `preserve`: 474",
            f"| {influxdb_path} |  | delete | pass | pass |",
            f"| {source_path} |  | delete | pass | pass |",
        ):
            with self.subTest(summary=expected):
                self.assertIn(expected, summary)

    def test_reviewed_opensearch_row_has_zero_manifest_findings(
        self,
    ) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(LIFECYCLE_CHECKER),
                "--mode",
                "check-manifest",
                "--wave",
                "target-surface-convergence",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)

    def test_influxdb_v2_manifest_row_records_exact_delete_evidence(self) -> None:
        manifest = yaml.safe_load(TARGET_MANIFEST.read_text(encoding="utf-8"))
        source_path = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
        row = next(
            entry
            for entry in manifest["entries"]
            if entry["source_path"] == source_path
        )

        self.assertEqual(
            {
                "source_path": source_path,
                "target_path": None,
                "artifact_id": None,
                "artifact_type_before": None,
                "artifact_type_after": None,
                "surface_class": "runtime",
                "status_before": None,
                "status_after": None,
                "parent_ids": [],
                "disposition": "delete",
                "canonical_replacement": (
                    "infra/04-data/analytics/influxdb/docker-compose.yml"
                ),
                "active_consumers": [],
                "partition_plan": None,
                "preservation_class": "git-history",
                "evidence": {
                    "commands": [
                        "git diff --name-status cd32264dd5fcb7060a50b516682fe8f3aeb74f85..f300b4f88cc6672445ac25a06602adb62381f7c0 -- infra/04-data/analytics/influxdb/docker-compose.v2.yml",
                        "git log --format=%H cd32264dd5fcb7060a50b516682fe8f3aeb74f85..f300b4f88cc6672445ac25a06602adb62381f7c0 -- infra/04-data/analytics/influxdb/docker-compose.v2.yml",
                    ],
                    "sources": [source_path],
                    "repository_paths": [source_path],
                    "consumer_scan": [
                        "git grep -lz --fixed-strings -- docker-compose.v2.yml -- .env.example infra scripts secrets"
                    ],
                    "rollback": [
                        "git revert --no-commit f300b4f88cc6672445ac25a06602adb62381f7c0"
                    ],
                },
                "review_verdict": {
                    "specification": "pass",
                    "quality": "pass",
                },
            },
            row,
        )
        self.assertEqual(483, len(manifest["entries"]))
        self.assertEqual(
            [
                source_path,
                "infra/04-data/analytics/opensearch/opensearch/config/"
                "userdict_ko.txt.example",
            ],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["disposition"] == "delete"
            ],
        )
        self.assertEqual(
            [
                source_path,
                "infra/04-data/analytics/opensearch/opensearch/config/"
                "userdict_ko.txt.example",
            ],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["review_verdict"]
                == {"specification": "pass", "quality": "pass"}
            ],
        )
        self.assertEqual(
            481,
            sum(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in manifest["entries"]
            ),
        )
        summary = TARGET_SUMMARY.read_text(encoding="utf-8")
        for expected in (
            "- Entries: 483",
            "- `delete`: 2",
            "- `migrate`: 7",
            "- `preserve`: 474",
            f"| {source_path} |  | delete | pass | pass |",
        ):
            with self.subTest(summary=expected):
                self.assertIn(expected, summary)

    def test_influxdb_v2_compose_is_removed(self) -> None:
        self.assertFalse(
            (ROOT / "infra/04-data/analytics/influxdb/docker-compose.v2.yml").exists()
        )

    def test_v2_only_example_and_metadata_keys_are_removed(self) -> None:
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        metadata_example = (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_text(
            encoding="utf-8"
        )

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
            ROOT
            / "docs/02.architecture/requirements/0012-data-analytics-architecture.md",
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
            ROOT
            / "docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md",
        )
        for path in historical_owners:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("InfluxDB 2", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
