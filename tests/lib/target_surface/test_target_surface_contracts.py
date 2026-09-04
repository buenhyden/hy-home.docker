from __future__ import annotations

import contextlib
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml

from scripts.lib.document_governance.registry import classify_path, load_registry


ROOT = pathlib.Path(__file__).resolve().parents[3]
CHECKER = ROOT / "scripts/validation/check-document-metadata.py"
LIFECYCLE_CHECKER = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"
SERVICE_EXAMPLE = ROOT / "examples/sample-web-service/service.md"
TARGET_MANIFEST = (
    ROOT / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
)
TARGET_SUMMARY = (
    ROOT / "docs/90.references/data/0068-target-surface-convergence-summary/README.md"
)
CURRENT_DELTA_MANIFEST = (
    ROOT / "docs/90.references/data/0073-target-surface-delta-manifest/data.yaml"
)
TARGET_VALIDATOR = ROOT / "scripts/lib/target_surface/target_surface_contract.py"
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
REGISTERED_ENTRYPOINT_README_PROFILES = frozenset(
    {"repository-readme", "package-readme"}
)
OVERVIEW_HEADING_READMES = (
    "infra/01-gateway/nginx/README.md",
    "infra/01-gateway/traefik/README.md",
    "infra/02-auth/keycloak/README.md",
    "infra/04-data/analytics/README.md",
    "infra/04-data/analytics/influxdb/README.md",
    "infra/04-data/analytics/ksql/README.md",
    "infra/04-data/analytics/opensearch/README.md",
    "infra/04-data/analytics/warehouses/README.md",
    "infra/05-messaging/rabbitmq/README.md",
    "infra/07-workflow/n8n/README.md",
    "infra/09-tooling/README.md",
)
SHARED_AGENT_POLICY_READMES = (
    "infra/01-gateway/nginx/README.md",
    "infra/01-gateway/traefik/README.md",
    "infra/02-auth/README.md",
    "infra/02-auth/keycloak/README.md",
    "infra/02-auth/oauth2-proxy/README.md",
    "infra/03-security/README.md",
    "infra/03-security/vault/README.md",
    "infra/04-data/analytics/README.md",
    "infra/04-data/analytics/influxdb/README.md",
    "infra/04-data/analytics/ksql/README.md",
    "infra/04-data/analytics/opensearch/README.md",
    "infra/04-data/analytics/warehouses/README.md",
    "infra/05-messaging/README.md",
    "infra/05-messaging/kafka/README.md",
    "infra/06-observability/README.md",
    "infra/06-observability/alertmanager/README.md",
    "infra/06-observability/alloy/README.md",
    "infra/06-observability/prometheus/README.md",
    "infra/06-observability/pushgateway/README.md",
    "infra/06-observability/pyroscope/README.md",
    "infra/06-observability/tempo/README.md",
    "infra/07-workflow/README.md",
    "infra/07-workflow/airflow/README.md",
    "infra/07-workflow/n8n/README.md",
    "infra/08-ai/README.md",
    "infra/README.md",
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
    "docs/01.requirements/0005-data-analytics.md",
    "docs/02.architecture/descriptions/0012-data-analytics-architecture.md",
    "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
    "docs/05.operations/catalog/04-data/README.md",
    "docs/05.operations/catalog/04-data/0017-influxdb/guide.md",
    "docs/05.operations/catalog/04-data/0017-influxdb/policy.md",
    "docs/05.operations/catalog/04-data/0017-influxdb/runbook.md",
)
INFLUX_V2_PATH = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
OPENSEARCH_DUPLICATE_PATH = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt.example"
)
OPENSEARCH_RETAINED_PATH = (
    "infra/04-data/analytics/opensearch/opensearch/config/userdict_ko.txt"
)
SEAWEEDFS_DUPLICATE_PATH = (
    "infra/04-data/lake-and-object/seaweedfs/config/security.toml"
)
SEAWEEDFS_RETAINED_PATH = (
    "infra/04-data/lake-and-object/seaweedfs/config/security.toml.example"
)

VALID_SAMPLE_SERVICE = """---
status: draft
artifact_id: spec:sample-web-service
artifact_type: spec
parent_ids:
  - spec:126-security-supply-chain-remediation
  - spec:127-deployment-release-engineering-remediation
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
    if path in {
        INFLUX_V2_PATH,
        OPENSEARCH_DUPLICATE_PATH,
        SEAWEEDFS_DUPLICATE_PATH,
    }:
        row.update(
            {
                "target_path": None,
                "disposition": "delete",
                "review_verdict": {"specification": "pass", "quality": "pass"},
            }
        )
    return row


@contextlib.contextmanager
def target_contract_fixture(*, seaweedfs_scaffold_text: str = ""):
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
            SEAWEEDFS_DUPLICATE_PATH: "",
            SEAWEEDFS_RETAINED_PATH: seaweedfs_scaffold_text,
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
        (root / SEAWEEDFS_DUPLICATE_PATH).unlink()

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

    def test_seaweedfs_pending_review_is_not_a_reviewed_duplicate(self) -> None:
        def mutation(document: dict[str, object]) -> None:
            row = next(
                entry
                for entry in document["entries"]
                if entry["source_path"] == SEAWEEDFS_DUPLICATE_PATH
            )
            row["review_verdict"] = {
                "specification": "pending",
                "quality": "pending",
            }

        with target_contract_fixture() as (root, manifest, _baseline):
            _mutate_manifest(manifest, mutation)
            self._assert_code(
                "target-duplicate-disposition-invalid",
                root,
                manifest,
                path=SEAWEEDFS_DUPLICATE_PATH,
            )

    def test_seaweedfs_baseline_blob_mismatch_is_value_safe(self) -> None:
        sentinel = "seaweedfs-blob-secret-sentinel"
        with target_contract_fixture(seaweedfs_scaffold_text=sentinel) as (
            root,
            manifest,
            _baseline,
        ):
            findings = self._assert_code(
                "target-duplicate-disposition-invalid",
                root,
                manifest,
                path=SEAWEEDFS_DUPLICATE_PATH,
            )
        self.assertNotIn(sentinel, repr(findings))

    def test_clean_fixture_has_no_findings(self) -> None:
        with target_contract_fixture() as (root, manifest, _baseline):
            self.assertEqual((), self._findings(root, manifest))


class SampleServiceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SERVICE_EXAMPLE.read_text(encoding="utf-8")

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

    def test_predecessor_records_history_and_successor_owns_current_disposition(
        self,
    ) -> None:
        predecessor = metadata._safe_load_unique(  # noqa: SLF001
            TARGET_MANIFEST.read_text(encoding="utf-8")
        )
        predecessor_row = next(
            entry
            for entry in predecessor["entries"]
            if entry["source_path"] == "examples/sample-web-service/service.md"
        )
        successor = metadata._safe_load_unique(  # noqa: SLF001
            CURRENT_DELTA_MANIFEST.read_text(encoding="utf-8")
        )
        successor_row = next(
            entry
            for entry in successor["entries"]
            if entry["path"] == "examples/sample-web-service/service.md"
        )

        self.assertEqual(
            {
                "surface_class": "typed-example",
                "disposition": "migrate",
                "status_after": "active",
                "parent_ids": ["spec:133-target-surface-contract-convergence"],
            },
            {
                key: predecessor_row[key]
                for key in (
                    "surface_class",
                    "disposition",
                    "status_after",
                    "parent_ids",
                )
            },
        )
        self.assertEqual(
            {
                "surface_class": "typed-example",
                "profile": "service",
                "disposition": "update",
                "canonical_owner": "examples/sample-web-service/service.md",
            },
            {
                key: successor_row[key]
                for key in (
                    "surface_class",
                    "profile",
                    "disposition",
                    "canonical_owner",
                )
            },
        )


class TargetReadmeProfileTests(unittest.TestCase):
    def test_target_runtime_readmes_stay_outside_the_document_registry(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--", *TARGET_ROOTS],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        registry = load_registry(REGISTRY)
        readmes = [
            path for path in result.stdout.splitlines() if path.endswith("/README.md")
        ]
        self.assertTrue(readmes)
        for path in readmes:
            with self.subTest(path=path):
                profile = classify_path(path, registry)
                # Repository entrypoint READMEs carry a registered Stage 99 form
                # so their authoring contract has one owner. Every other target
                # README stays governed by the target surface manifest alone.
                if profile in REGISTERED_ENTRYPOINT_README_PROFILES:
                    continue
                self.assertIsNone(profile)

    def test_native_markdown_and_typed_example_stay_outside_the_document_registry(
        self,
    ) -> None:
        registry = load_registry(REGISTRY)
        native_or_typed_paths = (
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/SECURITY.md",
            "examples/sample-web-service/service.md",
        )
        for path in native_or_typed_paths:
            with self.subTest(path=path):
                self.assertIsNone(classify_path(path, registry))

    def test_confirmed_localized_overview_headings_use_exact_profile_id(
        self,
    ) -> None:
        self.assertEqual(11, len(OVERVIEW_HEADING_READMES))
        for relative in OVERVIEW_HEADING_READMES:
            with self.subTest(path=relative):
                headings = {
                    line.strip()
                    for line in (ROOT / relative)
                    .read_text(encoding="utf-8")
                    .splitlines()
                    if line.startswith("## ")
                }
                self.assertIn("## Overview", headings)
                self.assertNotIn("## Overview (KR)", headings)

    def test_confirmed_shared_agent_policy_headings_are_removed(self) -> None:
        self.assertEqual(26, len(SHARED_AGENT_POLICY_READMES))
        forbidden = {
            "## AI Agent Guidance",
            "## AI Agent Operation Policy",
        }
        for relative in SHARED_AGENT_POLICY_READMES:
            with self.subTest(path=relative):
                headings = {
                    line.strip()
                    for line in (ROOT / relative)
                    .read_text(encoding="utf-8")
                    .splitlines()
                    if line.startswith("## ")
                }
                self.assertTrue(
                    headings.isdisjoint(forbidden),
                    f"{relative} retains generic shared Agent policy headings",
                )

    def test_shared_policy_consumers_route_once_to_both_stage00_owners(
        self,
    ) -> None:
        canonical_targets = (
            "docs/00.agent-governance/policies/agentic.md",
            "docs/00.agent-governance/policies/documentation-protocol.md",
        )
        for relative in SHARED_AGENT_POLICY_READMES:
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                local_section = text.split("## How to Work in This Area\n", 1)[1]
                local_section = local_section.split("\n## ", 1)[0]
                for target in canonical_targets:
                    self.assertEqual(1, text.count(target))
                    self.assertIn(target, local_section)

    def test_data_tier_readme_is_one_folder_index_with_one_operations_link(
        self,
    ) -> None:
        text = (ROOT / "infra/04-data/README.md").read_text(encoding="utf-8")

        self.assertNotIn("## 1. Context & Objective", text)
        self.assertNotIn("## 5. Maintenance & Safety", text)
        self.assertEqual(
            1,
            text.count(
                "[docs/05.operations/README.md](../../docs/05.operations/README.md)"
            ),
        )

    def test_secret_inventory_registers_surrealdb_path_only(self) -> None:
        lines = (ROOT / "secrets/README.md").read_text(encoding="utf-8").splitlines()

        self.assertEqual(
            ["- `secrets/db/surreal_db/`"],
            [line for line in lines if "secrets/db/surreal_db/" in line],
        )

    def test_service_local_constraints_survive_in_allowed_working_section(
        self,
    ) -> None:
        witnesses = {
            "infra/01-gateway/traefik/README.md": (
                "Do not modify `traefik.yml` entrypoints"
            ),
            "infra/02-auth/keycloak/README.md": "`9000/health/ready`",
            "infra/05-messaging/kafka/README.md": "`UnderReplicatedPartitions`",
            "infra/06-observability/alloy/README.md": "`discovery.docker`",
            "infra/07-workflow/n8n/README.md": "`EXECUTIONS_MODE: queue`",
        }
        for relative, witness in witnesses.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                section = text.split("## How to Work in This Area\n", 1)[1]
                section = section.split("\n## ", 1)[0]
                self.assertIn(witness, section)

    def test_policy_consumers_do_not_keep_copied_template_workflow(
        self,
    ) -> None:
        copied = (
            "상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.",
            "새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.",
            "변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.",
        )
        for relative in SHARED_AGENT_POLICY_READMES:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for sentence in copied:
                with self.subTest(path=relative, sentence=sentence):
                    self.assertNotIn(sentence, text)


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


class DeprecatedRuntimeContractTests(unittest.TestCase):
    def test_seaweedfs_unmounted_duplicate_is_removed_but_scaffold_remains(
        self,
    ) -> None:
        duplicate = ROOT / SEAWEEDFS_DUPLICATE_PATH
        retained = ROOT / SEAWEEDFS_RETAINED_PATH

        self.assertFalse(duplicate.exists())
        self.assertTrue(retained.is_file())

        compose = (
            ROOT / "infra/04-data/lake-and-object/seaweedfs/docker-compose.yml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("security.toml", compose)

    def test_seaweedfs_direct_docs_keep_only_the_unmounted_example_claim(self) -> None:
        paths = (
            "infra/04-data/lake-and-object/seaweedfs/README.md",
            "docs/05.operations/catalog/04-data/0024-seaweedfs/guide.md",
            "docs/05.operations/catalog/04-data/0024-seaweedfs/policy.md",
        )
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("config/security.toml.example", text)
                self.assertNotIn("config/security.toml`", text)
                self.assertIn("separate approved runtime", text)
                self.assertIn("chrislusf/seaweedfs:4.38", text)
                self.assertNotIn("chrislusf/seaweedfs:4.31", text)

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

        self.assertEqual(b"", (ROOT / retained).read_bytes())

        compose_paths = (
            ROOT / "infra/04-data/analytics/opensearch/docker-compose.yml",
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

        influxdb_path = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
        seaweedfs_path = SEAWEEDFS_DUPLICATE_PATH
        self.assertEqual(483, len(manifest["entries"]))
        self.assertEqual(
            [influxdb_path, source_path, seaweedfs_path],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["disposition"] == "delete"
            ],
        )
        self.assertEqual(
            10,
            sum(entry["disposition"] == "migrate" for entry in manifest["entries"]),
        )
        self.assertEqual(
            470,
            sum(entry["disposition"] == "preserve" for entry in manifest["entries"]),
        )
        self.assertEqual(
            483,
            sum(
                entry["review_verdict"] == {"specification": "pass", "quality": "pass"}
                for entry in manifest["entries"]
            ),
        )
        self.assertEqual(
            0,
            sum(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in manifest["entries"]
            ),
        )

        summary = TARGET_SUMMARY.read_text(encoding="utf-8")
        for expected in (
            f"| {influxdb_path} |  | delete | pass | pass |",
            f"| {source_path} |  | delete | pass | pass |",
            f"| {seaweedfs_path} |  | delete | pass | pass |",
        ):
            with self.subTest(summary=expected):
                self.assertIn(expected, summary)

    def test_reviewed_seaweedfs_row_has_zero_manifest_findings(self) -> None:
        # Current claims are owned by the retained validator; immutable historical
        # payload parity is independently checked by the public lifecycle gate.
        self.assertEqual((), load_target_validator().validate(ROOT))

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
        seaweedfs_path = SEAWEEDFS_DUPLICATE_PATH
        self.assertEqual(483, len(manifest["entries"]))
        self.assertEqual(
            [
                source_path,
                "infra/04-data/analytics/opensearch/opensearch/config/"
                "userdict_ko.txt.example",
                seaweedfs_path,
            ],
            [
                entry["source_path"]
                for entry in manifest["entries"]
                if entry["disposition"] == "delete"
            ],
        )
        self.assertEqual(
            483,
            sum(
                entry["review_verdict"] == {"specification": "pass", "quality": "pass"}
                for entry in manifest["entries"]
            ),
        )
        self.assertEqual(
            0,
            sum(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in manifest["entries"]
            ),
        )
        summary = TARGET_SUMMARY.read_text(encoding="utf-8")
        self.assertIn(
            f"| {source_path} |  | delete | pass | pass |",
            summary,
        )

    def test_seaweedfs_duplicate_manifest_row_records_exact_delete_evidence(
        self,
    ) -> None:
        manifest = yaml.safe_load(TARGET_MANIFEST.read_text(encoding="utf-8"))
        row = next(
            entry
            for entry in manifest["entries"]
            if entry["source_path"] == SEAWEEDFS_DUPLICATE_PATH
        )

        self.assertEqual(
            {
                "source_path": SEAWEEDFS_DUPLICATE_PATH,
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
                        "git diff --name-status 6c3cbc2e417cba6ca466c28efd8a5c4c408a397c..f50fdd2670404f9ad32bdf9a6aa1e0ffb5ff6d0f -- infra/04-data/lake-and-object/seaweedfs/config/security.toml",
                        "git log --format=%H 6c3cbc2e417cba6ca466c28efd8a5c4c408a397c..f50fdd2670404f9ad32bdf9a6aa1e0ffb5ff6d0f -- infra/04-data/lake-and-object/seaweedfs/config/security.toml",
                        "git rev-parse 6c3cbc2e417cba6ca466c28efd8a5c4c408a397c:infra/04-data/lake-and-object/seaweedfs/config/security.toml 6c3cbc2e417cba6ca466c28efd8a5c4c408a397c:infra/04-data/lake-and-object/seaweedfs/config/security.toml.example f50fdd2670404f9ad32bdf9a6aa1e0ffb5ff6d0f:infra/04-data/lake-and-object/seaweedfs/config/security.toml.example",
                    ],
                    "sources": [
                        SEAWEEDFS_DUPLICATE_PATH,
                        SEAWEEDFS_RETAINED_PATH,
                    ],
                    "repository_paths": [
                        "docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md",
                        "docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md",
                        "infra/04-data/lake-and-object/seaweedfs/README.md",
                        SEAWEEDFS_DUPLICATE_PATH,
                        SEAWEEDFS_RETAINED_PATH,
                    ],
                    "consumer_scan": [
                        "git grep -lz --fixed-strings -- security.toml -- infra/04-data/lake-and-object/seaweedfs docs/05.operations"
                    ],
                    "rollback": [
                        "git revert --no-commit f50fdd2670404f9ad32bdf9a6aa1e0ffb5ff6d0f"
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
            3,
            sum(entry["disposition"] == "delete" for entry in manifest["entries"]),
        )
        self.assertEqual(
            10,
            sum(entry["disposition"] == "migrate" for entry in manifest["entries"]),
        )
        self.assertEqual(
            470,
            sum(entry["disposition"] == "preserve" for entry in manifest["entries"]),
        )
        self.assertEqual(
            483,
            sum(
                entry["review_verdict"] == {"specification": "pass", "quality": "pass"}
                for entry in manifest["entries"]
            ),
        )
        self.assertEqual(
            0,
            sum(
                entry["review_verdict"]
                == {"specification": "pending", "quality": "pending"}
                for entry in manifest["entries"]
            ),
        )
        summary = TARGET_SUMMARY.read_text(encoding="utf-8")
        for expected in (
            "- Entries: 483",
            "- `delete`: 3",
            "- `migrate`: 10",
            "- `preserve`: 470",
            f"| {SEAWEEDFS_DUPLICATE_PATH} |  | delete | pass | pass |",
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
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/guide.md",
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/policy.md",
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/runbook.md",
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
            ROOT / "docs/01.requirements/0005-data-analytics.md",
            ROOT
            / "docs/02.architecture/descriptions/0012-data-analytics-architecture.md",
            ROOT / "docs/02.architecture/decisions/0015-analytics-engine-selection.md",
            ROOT / "docs/05.operations/catalog/04-data/README.md",
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/guide.md",
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/policy.md",
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/runbook.md",
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
            ROOT / "docs/05.operations/catalog/04-data/0017-influxdb/guide.md",
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


if __name__ == "__main__":
    unittest.main()
