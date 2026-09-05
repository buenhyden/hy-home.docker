import datetime as dt
import importlib.util
import re
import subprocess
import sys

import scripts.lib.document_governance as document_governance
import yaml

from tests.validation._script_manifest_support import *

MANIFEST = ROOT / "scripts/manifest.yaml"
MANIFEST_CHECKER = ROOT / "scripts/validation/check-script-manifest.py"


def load_manifest_checker():
    spec = importlib.util.spec_from_file_location(
        "check_script_manifest", MANIFEST_CHECKER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {MANIFEST_CHECKER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ScriptManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Read the roots from the checker rather than restating "scripts": the
        # manifest governs every root in MANIFEST_ROOTS, and a second literal
        # here would let coverage and the contract drift apart.
        roots = load_manifest_checker().MANIFEST_ROOTS
        cls.tracked = tracked_paths(*(root.rstrip("/") for root in roots))
        cls.repository_paths = tracked_paths(":(top)")
        cls.manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.rows = cls.manifest["files"]
        cls.rows_by_path = {row["path"]: row for row in cls.rows}
    def test_every_tracked_script_has_one_manifest_record(self) -> None:
        declared = [row["path"] for row in self.rows]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(self.tracked, set(declared))

    def test_production_scripts_do_not_reference_tests_tree(self) -> None:
        violations: list[str] = []
        for path in sorted((ROOT / "scripts").rglob("*")):
            if path.is_file() and path.suffix in {".py", ".sh"}:
                text = path.read_text(encoding="utf-8")
                if "tests/fixtures/" in text or 'ROOT / "tests"' in text:
                    violations.append(path.relative_to(ROOT).as_posix())

        self.assertEqual([], violations)

    def test_stage90_generators_declare_exact_destinations_and_explicit_write_mode(
        self,
    ) -> None:
        for script, output in (
            (
                "scripts/operations/generate-compose-profile-service-coverage.sh",
                "docs/90.references/data/0059-compose-profile-service-coverage/README.md",
            ),
            (
                "scripts/operations/generate-tech-stack-version-provenance.sh",
                "docs/90.references/data/0061-tech-stack-version-provenance/README.md",
            ),
            (
                "scripts/validation/generate-audit-implementation-matrix.sh",
                "docs/90.references/data/0065-audit-implementation-matrix/README.md",
            ),
            (
                "scripts/validation/generate-security-automation-readiness.sh",
                "docs/90.references/data/0078-security-automation-readiness/README.md",
            ),
            (
                "scripts/security/generate-supply-chain-sample-service-summary.sh",
                "docs/90.references/data/0079-supply-chain-sample-service/README.md",
            ),
        ):
            with self.subTest(script=script):
                row = self.rows_by_path[script]
                self.assertEqual([output], row["outputs"])
                self.assertEqual(["bash", script, "--check"], row["check_command"])
                result = subprocess.run(
                    ["bash", script, "--help"],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("--write", result.stdout)

    def test_compose_profile_generator_emits_canonical_published_metadata(
        self,
    ) -> None:
        script = "scripts/operations/generate-compose-profile-service-coverage.sh"
        result = subprocess.run(
            ["bash", script, "--dry-run"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        metadata = yaml.safe_load(result.stdout.split("---", 2)[1])
        expected_fields = (
            "title",
            "version",
            "type",
            "status",
            "owner",
            "updated",
            "layer",
            "artifact_id",
            "parent_ids",
            "created",
            "observed_at",
            "generated_by",
        )
        stable_fields = {
            "title": "Reference: Docker Compose Profile Service Coverage",
            "type": "reference/data-pack",
            "status": "published",
            "owner": "@buenhyden",
            "layer": "references",
            "artifact_id": "DATA-0059",
            "parent_ids": [],
            "generated_by": script,
        }
        semver = re.compile(
            r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
        )
        iso_date = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")

        def assert_valid_envelope(candidate: dict[str, object]) -> None:
            self.assertEqual(expected_fields, tuple(candidate))
            self.assertEqual(
                stable_fields,
                {field: candidate.get(field) for field in stable_fields},
            )
            version = candidate.get("version")
            self.assertIsInstance(version, str)
            self.assertIsNotNone(semver.fullmatch(version))
            for field in ("created", "updated", "observed_at"):
                value = candidate.get(field)
                self.assertIsInstance(value, str)
                self.assertIsNotNone(iso_date.fullmatch(value))
                try:
                    dt.date.fromisoformat(value)
                except ValueError as error:
                    self.fail(f"{field} must be a valid ISO date: {error}")

        assert_valid_envelope(metadata)

        next_publication = dict(metadata)
        next_publication.update(
            version="2.1.0",
            updated="2027-01-02",
            observed_at="2027-01-01",
        )
        assert_valid_envelope(next_publication)

        for field, value in (
            ("status", "active"),
            ("version", 2),
            ("version", "01.0.0"),
            ("updated", dt.date(2027, 1, 2)),
            ("observed_at", "2027-13-40"),
        ):
            with self.subTest(field=field, value=value):
                invalid = dict(metadata)
                invalid[field] = value
                with self.assertRaises(AssertionError):
                    assert_valid_envelope(invalid)

    def test_stage90_generators_require_write_and_touch_only_declared_output(
        self,
    ) -> None:
        scripts = (
            "scripts/operations/generate-compose-profile-service-coverage.sh",
            "scripts/operations/generate-tech-stack-version-provenance.sh",
            "scripts/validation/generate-audit-implementation-matrix.sh",
            "scripts/validation/generate-security-automation-readiness.sh",
            "scripts/security/generate-supply-chain-sample-service-summary.sh",
            "scripts/validation/report-provider-hook-parity.sh",
        )
        for script in scripts:
            with (
                self.subTest(script=script),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                inputs = {script}
                fixture_sources: dict[str, Path] = {}
                fixture_texts: dict[str, str] = {}
                if "tech-stack" in script:
                    (root / "infra").mkdir()
                    (root / "infra/tech-stack.versions.json").write_text(
                        json.dumps(
                            {
                                "entries": [
                                    {
                                        "component": "fixture",
                                        "images": ["fixture:1"],
                                        "compose_files": [
                                            "infra/docker-compose.fixture.yml"
                                        ],
                                    }
                                ]
                            }
                        )
                    )
                    (root / "infra/image-tag-policy.exceptions.json").write_text("{}")
                    (root / "infra/docker-compose.fixture.yml").write_text(
                        "services:\n  fixture:\n    image: fixture:1\n"
                    )
                elif "audit-implementation" in script:
                    inputs.update(
                        {
                            "scripts/validation/audit_criterion_contract.py",
                            "scripts/validation/check-agentic-audit-semantic-freshness.py",
                            "scripts/validation/agentic-audit-semantic-contract.json",
                        }
                    )
                    semantic = json.loads(
                        (
                            ROOT
                            / "scripts/validation/agentic-audit-semantic-contract.json"
                        ).read_text()
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "docs/90.references/audits").rglob("*.md")
                    )
                    # The superseded snapshot the freshness checker reads is
                    # preserved outside the live audit tree, so the producer
                    # fixture takes its location from the checker itself.
                    from tests.validation.test_agentic_audit_semantic_freshness import (
                        module as freshness_module,
                    )

                    inputs.add(freshness_module.SUPERSEDED_2026_07_07_README.as_posix())
                    inputs.update(
                        path
                        for assertion in semantic["assertions"]
                        for path in assertion["required_evidence_paths"]
                    )
                elif "supply-chain" in script:
                    inputs.update(
                        {
                            "scripts/validation/check-supply-chain-policy.py",
                            "scripts/lib/supply_chain/grype_db_seed.py",
                            "examples/sample-web-service/Dockerfile",
                        }
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "infra").glob("supply-chain*.json")
                    )
                    inputs.update(
                        path.relative_to(ROOT).as_posix()
                        for path in (ROOT / "examples/operations/supply-chain").rglob("*")
                        if path.is_file()
                    )
                elif "hook-parity" in script:
                    from tests.validation.test_provider_hook_parity import copy_fixture

                    copy_fixture(root)
                self.assertLess(
                    len(inputs), 180, "fixture must remain a bounded producer input set"
                )
                for relative in sorted(inputs):
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if relative in fixture_texts:
                        target.write_text(fixture_texts[relative], encoding="utf-8")
                    else:
                        source = fixture_sources.get(relative, ROOT / relative)
                        self.assertTrue(source.is_file(), relative)
                        shutil.copy2(source, target)
                output = self.rows_by_path[script]["outputs"][0]
                target = root / output
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("stale output\n", encoding="utf-8")
                subprocess.run(
                    ["git", "init", "-q"], cwd=root, check=True, capture_output=True
                )
                subprocess.run(
                    ["git", "add", "."], cwd=root, check=True, capture_output=True
                )
                environment = {
                    **os.environ,
                    "PYTHONPATH": str(ROOT),
                    "PYTHONDONTWRITEBYTECODE": "1",
                }
                environment.pop("HYHOME_CI_GATE_ROOT", None)
                command = ["bash", str(root / script)]
                extra = ["--root", str(root)] if "hook-parity" in script else []

                def snapshot():
                    return {
                        path.relative_to(root).as_posix(): path.read_bytes()
                        for path in root.rglob("*")
                        if path.is_file() and ".git" not in path.relative_to(root).parts
                    }

                before = snapshot()
                for mode in ([], ["--check"]):
                    result = subprocess.run(
                        [*command, *mode, *extra],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    self.assertNotEqual(0, result.returncode, script)
                    if "compose-profile-service-coverage" in script:
                        self.assertIn(
                            f"Run: bash {script} --write", result.stderr
                        )
                    self.assertEqual(before, snapshot(), script)
                result = subprocess.run(
                    [*command, "--write", *extra],
                    cwd=root,
                    env=environment,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                after = snapshot()
                self.assertEqual(
                    {output},
                    {
                        path
                        for path in before.keys() | after.keys()
                        if before.get(path) != after.get(path)
                    },
                )
                for mode in ([], ["--check"]):
                    result = subprocess.run(
                        [*command, *mode, *extra],
                        cwd=root,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    self.assertEqual(
                        0, result.returncode, result.stdout + result.stderr
                    )
                    self.assertEqual(after, snapshot())

    def test_task12_retires_only_the_proven_successor_scripts(self) -> None:
        self.assertTrue(TASK12_RETIRED_SCRIPTS.isdisjoint(self.tracked))
        self.assertTrue(TASK12_RETIRED_SCRIPTS.isdisjoint(self.rows_by_path))
        self.assertIn(
            "scripts/operations/rehearse-sample-service-delivery.sh",
            self.tracked,
        )

    def test_records_are_sorted_and_use_the_complete_schema(self) -> None:
        paths = [row["path"] for row in self.rows]
        self.assertEqual(paths, sorted(paths))
        for row in self.rows:
            expected_fields = REQUIRED_FIELDS
            if (
                row["kind"] in {"generator", "validator"}
                and row["mutation"] == "check-write"
                and row["disposition"] == "retain"
                and ("check_command" in row or "outputs" in row)
            ):
                expected_fields = REQUIRED_FIELDS | {"check_command", "outputs"}
            self.assertEqual(expected_fields, set(row))
            self.assertIn(row["kind"], KINDS)
            self.assertIn(row["lifecycle"], LIFECYCLES)
            self.assertIn(row["mutation"], MUTATIONS)
            self.assertIn(row["disposition"], DISPOSITIONS)
            self.assertIsInstance(row["authority"], str)
            self.assertTrue(row["authority"])
            self.assertNotEqual(row["authority"], "sdlc-taxonomy-convergence")
            self.assertIn(row["authority"], self.repository_paths)

    def test_consumer_successor_and_test_references_are_evidenced(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                self.assertIsInstance(row["consumers"], list)
                self.assertEqual(row["consumers"], sorted(set(row["consumers"])))
                self.assertIsInstance(row["tests"], list)
                self.assertEqual(row["tests"], sorted(set(row["tests"])))
                for reference in [*row["consumers"], *row["tests"]]:
                    self.assertIn(reference, self.repository_paths)
                    self.assertTrue((ROOT / reference).is_file())
                    self.assertFalse(reference.startswith(FORBIDDEN_EVIDENCE_PREFIXES))
                    self.assertTrue(
                        reference_proves_use(reference, row["path"]),
                        f"{reference} does not invoke/import {row['path']}",
                    )
                successor = row["successor"]
                if row["disposition"] == "retain":
                    self.assertIsNone(successor)
                else:
                    self.assertIsInstance(successor, str)
                    self.assertIn(successor, self.repository_paths)
                if row["disposition"] == "retain" and row["kind"] != "library":
                    self.assertTrue(row["consumers"])
                if row["disposition"] == "retain" and row["kind"] not in {
                    "contract",
                    "dependency-manifest",
                }:
                    self.assertTrue(row["tests"])

    def test_nonretained_successor_is_distinct(self) -> None:
        for row in self.rows:
            if row["disposition"] != "retain":
                with self.subTest(path=row["path"]):
                    self.assertNotEqual(row["path"], row.get("successor"))

    def test_document_governance_package_marker_is_registered(self) -> None:
        marker = "scripts/lib/document_governance/__init__.py"
        self.assertEqual("retain", self.rows_by_path[marker]["disposition"])
        self.assertIn("document-governance", document_governance.__doc__ or "")

    def test_retained_public_entrypoint_has_current_consumer(self) -> None:
        for row in self.rows:
            if (
                row["kind"] in {"validator", "runner", "operations"}
                and row["disposition"] == "retain"
            ):
                with self.subTest(path=row["path"]):
                    self.assertTrue(row["consumers"])
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(is_runbook_authority(row["authority"]))
                    self.assertTrue(row["tests"])
                if (
                    row["kind"] in {"generator", "validator"}
                    and row["mutation"] == "check-write"
                    and row["disposition"] == "retain"
                    and "check_command" in row
                ):
                    self.assertIn("--check", row["check_command"])
                    self.assertNotIn("--write", row["check_command"])
                    self.assertTrue(row["outputs"])

    def test_manifest_inventory_is_not_a_consumer_of_other_scripts(self) -> None:
        offenders = [
            row["path"]
            for row in self.rows
            if row["path"] != "scripts/manifest.yaml"
            and "scripts/manifest.yaml" in row["consumers"]
        ]
        self.assertEqual([], offenders)

    def test_taxonomy_library_declares_exact_real_consumers_and_tests(self) -> None:
        row = self.rows_by_path["scripts/lib/document_governance/taxonomy.py"]
        self.assertEqual("retain", row["disposition"])
        self.assertEqual(
            [
                "scripts/lib/document_governance/metadata/lifecycle.py",
                "scripts/lib/document_governance/metadata/profile.py",
            ],
            row["consumers"],
        )
        self.assertEqual(
            ["tests/lib/document_governance/test_taxonomy.py"],
            row["tests"],
        )

    def test_python_import_evidence_recognizes_package_member_imports(self) -> None:
        adapter = "scripts/validation/check-document-metadata.py"
        self.assertTrue(
            _python_imports_target(
                adapter,
                "scripts/lib/document_governance/metadata_contract.py",
            )
        )
        self.assertTrue(
            _python_imports_target(
                adapter,
                "scripts/lib/document_governance/metadata_validator.py",
            )
        )

    def test_mutation_classes_follow_observed_script_behavior(self) -> None:
        for row in self.rows:
            with self.subTest(path=row["path"]):
                expected = MUTATION_OVERRIDES.get(row["path"], "none")
                self.assertEqual(expected, row["mutation"])
                if (
                    row["kind"] in {"generator", "validator"}
                    and row["mutation"] == "check-write"
                    and row["disposition"] == "retain"
                    and "check_command" in row
                ):
                    self.assertEqual(row["path"], row["check_command"][1])

    def test_plan_mandatory_dispositions_and_high_risk_operations(self) -> None:
        for path, disposition in MANDATORY_DISPOSITIONS.items():
            with self.subTest(path=path):
                self.assertEqual(disposition, self.rows_by_path[path]["disposition"])

        for path in (
            "scripts/operations/gen-secrets.sh",
            "scripts/security/seed-grype-db-cache.sh",
        ):
            with self.subTest(path=path):
                row = self.rows_by_path[path]
                if row["disposition"] == "retain":
                    self.assertTrue(row["consumers"])
                    self.assertTrue(row["tests"])
                    self.assertTrue(is_runbook_authority(row["authority"]))

    def test_postgres_logical_upgrade_uses_the_mirrored_ops_test(self) -> None:
        postgres = self.rows_by_path[
            "scripts/operations/rehearse-postgres-logical-upgrade.sh"
        ]
        self.assertEqual("retain", postgres["disposition"])
        self.assertEqual(
            "docs/05.operations/catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md",
            postgres["authority"],
        )
        self.assertEqual(
            [".github/workflow-contract.yml", postgres["authority"]],
            postgres["consumers"],
        )
        self.assertEqual(
            ["tests/validation/test_postgres_logical_upgrade_rehearsal.py"],
            postgres["tests"],
        )

    def test_authority_is_specific_and_runtime_retention_is_runbook_bound(self) -> None:
        unrelated = {
            "docs/05.operations/runbooks/03-security/vault.md",
            "docs/05.operations/catalog/04-data/0031-postgresql-cluster/runbook.md",
        }
        for row in self.rows:
            with self.subTest(path=row["path"]):
                authority = row["authority"]
                self.assertFalse(
                    authority.startswith("docs/03.specs/"),
                    "script authority must be a current policy, architecture, "
                    "operations, registry, or workflow owner",
                )
                authority_text = (ROOT / authority).read_text(encoding="utf-8")
                basename = PurePosixPath(row["path"]).name
                if (
                    authority in unrelated
                    and basename not in authority_text
                    and row["path"] not in authority_text
                ):
                    self.fail(
                        f"blanket authority {authority} does not govern {row['path']}"
                    )
                if row["mutation"] == "runtime" and row["disposition"] == "retain":
                    self.assertTrue(is_runbook_authority(authority))
                    self.assertTrue(
                        basename in authority_text or row["path"] in authority_text,
                        f"runtime Runbook does not name {row['path']}",
                    )
                elif row["mutation"] == "runtime" and not is_runbook_authority(
                    authority
                ):
                    self.assertNotEqual("retain", row["disposition"])
                    self.assertEqual(row["path"], row["successor"])

    def test_operations_implementation_and_gate_use_the_registry_authority(
        self,
    ) -> None:
        for path in OPERATIONS_MANIFEST_PATHS:
            with self.subTest(path=path):
                row = self.rows_by_path[path]
                self.assertEqual("docs/99.templates/registry.json", row["authority"])
                self.assertNotIn("current_authorities", row)
                self.assertNotIn("semantic_witnesses", row)

    def test_runbook_authority_accepts_only_canonical_catalog_leaf_shape(self) -> None:
        self.assertTrue(
            is_runbook_authority(
                "docs/05.operations/catalog/04-data/"
                "0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md"
            )
        )
        rejected = (
            "docs/05.operations/04-data/ops-0032-example/runbook.md",
            "docs/05.operations/runbooks/04-data/example.md",
            "docs/05.operations/catalog/4-data/ops-0032-example/runbook.md",
            "docs/05.operations/catalog/04-data/ops-032-example/runbook.md",
            "docs/05.operations/catalog/04-data/ops-0032-example/guide.md",
            "docs/05.operations/catalog/04-data/nested/ops-0032-example/runbook.md",
        )
        for path in rejected:
            with self.subTest(path=path):
                self.assertFalse(is_runbook_authority(path))

    def test_scripts_readme_preserves_invocation_warnings(self) -> None:
        text = (ROOT / "scripts/README.md").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", text)
        self.assertIn("Do not invoke a `mutation: runtime` row", compact)
        self.assertIn("Do not invoke a default-write generator without", compact)
        self.assertIn("semantic invocation/import evidence", compact)

    def test_evals_readme_states_its_manifest_registration_rule(self) -> None:
        text = (ROOT / "evals/README.md").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", text)
        # `evals/` is a manifest root, so an unregistered executable added here
        # must fail the gate exactly as it would under `scripts/`.
        self.assertIn("MANIFEST_ROOTS", compact)
        self.assertIn("scripts/manifest.yaml", compact)
        self.assertIn("check-script-manifest.py", compact)

    def test_semantic_helpers_reject_inventory_only_evidence(self) -> None:
        taxonomy = "scripts/lib/document_governance/taxonomy.py"
        self.assertFalse(reference_proves_use("scripts/manifest.yaml", taxonomy))
        self.assertFalse(reference_proves_use(".github/CODEOWNERS", taxonomy))

class ScriptManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_manifest_checker()
        self.tracked = {
            ".github/workflow-contract.yml",
            "docs/authority.md",
            "docs/consumer.md",
            "docs/output.md",
            "scripts/example.py",
            "tests/validation/test_example.py",
        }

    def row(self, **updates: object) -> dict[str, object]:
        row: dict[str, object] = {
            "path": "scripts/example.py",
            "kind": "validator",
            "authority": "docs/authority.md",
            "lifecycle": "active",
            "mutation": "none",
            "consumers": ["docs/consumer.md"],
            "disposition": "retain",
            "successor": None,
            "tests": ["tests/validation/test_example.py"],
        }
        return {**row, **updates}

    def codes(
        self, row: dict[str, object], tracked: set[str] | None = None
    ) -> set[str]:
        document = {"schema_version": 1, "files": [row]}
        return {
            finding.code
            for finding in self.checker.validate_manifest_document(
                document, self.tracked if tracked is None else tracked
            )
        }

    def test_manifest_rejects_unreferenced_executable(self) -> None:
        findings = self.checker.validate_manifest_document(
            {
                "schema_version": 1,
                "files": [
                    {
                        "path": "scripts/example.sh",
                        "kind": "validator",
                        "authority": "docs/authority.md",
                        "lifecycle": "active",
                        "mutation": "none",
                        "consumers": [],
                        "disposition": "retain",
                        "successor": None,
                        "tests": ["tests/validation/test_example.py"],
                    }
                ],
            },
            {
                "scripts/example.sh",
                "docs/authority.md",
                "tests/validation/test_example.py",
            },
        )
        self.assertIn("consumer-missing", {finding.code for finding in findings})

    def test_manifest_rejects_missing_and_invalid_authority(self) -> None:
        self.assertIn(
            "fields-missing",
            self.codes(
                {key: value for key, value in self.row().items() if key != "authority"}
            ),
        )
        self.assertIn("authority-invalid", self.codes(self.row(authority="")))
        self.assertIn(
            "authority-untracked", self.codes(self.row(authority="docs/unknown.md"))
        )

    def test_manifest_rejects_retired_operations_authority_fields(self) -> None:
        for field in ("current_authorities", "semantic_witnesses"):
            with self.subTest(field=field):
                self.assertIn(
                    "fields-unknown",
                    self.codes(self.row(**{field: ["docs/authority.md"]})),
                )

    def test_manifest_rejects_invalid_disposition_and_successor_contract(self) -> None:
        self.assertIn(
            "disposition-invalid", self.codes(self.row(disposition="deprecated"))
        )
        self.assertIn(
            "successor-invalid", self.codes(self.row(successor="scripts/next.py"))
        )
        self.assertIn(
            "successor-missing",
            self.codes(self.row(disposition="merge", successor=None)),
        )
        self.assertIn(
            "successor-untracked",
            self.codes(self.row(disposition="merge", successor="scripts/next.py")),
        )
        self.assertIn(
            "successor-self",
            self.codes(self.row(disposition="rewrite", successor="scripts/example.py")),
        )

    def test_manifest_rejects_missing_behavioral_tests_and_invalid_mutation(
        self,
    ) -> None:
        self.assertIn("tests-missing", self.codes(self.row(tests=[])))
        self.assertIn(
            "mutation-invalid", self.codes(self.row(mutation="default-write"))
        )

    def test_manifest_rejects_retired_placeholder_test_roots(self) -> None:
        for root in ("docs", "qa", "setup"):
            test_path = f"tests/{root}/test_example.py"
            with self.subTest(root=root):
                self.assertIn(
                    "tests-location-invalid",
                    self.codes(
                        self.row(tests=[test_path]),
                        self.tracked | {test_path},
                    ),
                )

    def test_manifest_requires_retained_library_tests_and_document_governance_mirrors(
        self,
    ) -> None:
        library = self.row(
            path="scripts/lib/document_governance/example.py",
            kind="library",
            consumers=[],
            tests=[],
        )
        tracked = self.tracked | {"scripts/lib/document_governance/example.py"}
        self.assertIn("tests-missing", self.codes(library, tracked))

        library["tests"] = ["tests/validation/test_example.py"]
        self.assertIn("tests-mirror-missing", self.codes(library, tracked))

    def test_manifest_rejects_invalid_generated_check_command(self) -> None:
        generator = self.row(
            kind="generator",
            mutation="check-write",
            authority=".github/workflow-contract.yml",
        )
        self.assertIn("generated-check-invalid", self.codes(generator))
        adversarial = (
            ["python3", "scripts/example.py", "--write"],
            ["bash", "scripts/example.py", "--check"],
            ["sh", "-c", "python3 scripts/example.py --check"],
            ["python3", "-c", "pass", "scripts/example.py", "--check"],
            ["python3", "-m", "scripts.example", "--check"],
            ["python3", "scripts/example.py", "--check", "extra"],
            [
                "python3",
                "scripts/validation/check-script-manifest.py",
                "scripts/example.py",
                "--check",
            ],
        )
        for command in adversarial:
            with self.subTest(command=command):
                self.assertIn(
                    "generated-check-invalid",
                    self.codes(
                        self.row(
                            kind="generator",
                            mutation="check-write",
                            authority=".github/workflow-contract.yml",
                            check_command=command,
                            outputs=["docs/output.md"],
                        )
                    ),
                )
        self.assertNotIn(
            "generated-check-invalid",
            self.codes(
                self.row(
                    kind="generator",
                    mutation="check-write",
                    authority=".github/workflow-contract.yml",
                    check_command=["python3", "scripts/example.py", "--check"],
                    outputs=["docs/output.md"],
                )
            ),
        )
        self.assertIn(
            "generated-output-untracked",
            self.codes(
                self.row(
                    kind="generator",
                    mutation="check-write",
                    authority=".github/workflow-contract.yml",
                    check_command=["python3", "scripts/example.py", "--check"],
                    outputs=["docs/unknown-output.md"],
                )
            ),
        )

    def test_manifest_rejects_executable_composition_fields(self) -> None:
        values = {
            "public_suites": ["repository-integrity"],
            "execution_argv": ["--check"],
            "execution_contexts": ["local"],
        }
        for field, value in values.items():
            with self.subTest(field=field):
                self.assertIn("fields-unknown", self.codes(self.row(**{field: value})))

    def test_manifest_rejects_unknown_fields_and_untracked_paths(self) -> None:
        self.assertIn("fields-unknown", self.codes(self.row(legacy=True)))
        self.assertIn(
            "path-untracked",
            self.codes(self.row(path="scripts/unknown.py")),
        )
        self.assertIn(
            "consumers-untracked",
            self.codes(self.row(consumers=["docs/unknown.md"])),
        )
        self.assertIn(
            "tests-untracked",
            self.codes(self.row(tests=["tests/unknown.py"])),
        )

    def test_manifest_rejects_tests_outside_approved_roots(self) -> None:
        tracked = {*self.tracked, "docs/test_example.py"}
        self.assertIn(
            "tests-location-invalid",
            self.codes(self.row(tests=["docs/test_example.py"]), tracked),
        )

    def test_retained_runtime_rejects_unrelated_spec_authority(self) -> None:
        self.assertIn(
            "runtime-authority-invalid",
            self.codes(
                self.row(
                    kind="operations",
                    mutation="runtime",
                    authority="docs/authority.md",
                )
            ),
        )

    def _generator_repo(
        self, root: Path, script: str, script_path: str = "scripts/example.py"
    ) -> Path:
        for relative in ("scripts", "docs", "tests"):
            (root / relative).mkdir(parents=True, exist_ok=True)
        (root / script_path).parent.mkdir(parents=True, exist_ok=True)
        (root / script_path).write_text(script, encoding="utf-8")
        (root / ".github").mkdir(parents=True, exist_ok=True)
        (root / ".github/workflow-contract.yml").write_text(
            f'entrypoint: "{script_path}"\n', encoding="utf-8"
        )
        (root / "docs/authority.md").write_text("authority\n", encoding="utf-8")
        (root / "docs/consumer.md").write_text(
            f"`{script_path}`\n`scripts/manifest.yaml`\n", encoding="utf-8"
        )
        (root / "docs/output.md").write_text("before\n", encoding="utf-8")
        (root / "tests/validation").mkdir(parents=True, exist_ok=True)
        (root / "tests/validation/test_example.py").write_text(
            f"import subprocess\nsubprocess.run(['python3', '{script_path}', '--check'], check=False)\n",
            encoding="utf-8",
        )
        generator = self.row(
            path=script_path,
            kind="generator",
            mutation="check-write",
            authority=".github/workflow-contract.yml",
            check_command=["python3", script_path, "--check"],
            outputs=["docs/output.md"],
        )
        manifest = {
            "schema_version": 1,
            "files": [
                generator,
                {
                    "path": "scripts/manifest.yaml",
                    "kind": "contract",
                    "authority": "docs/authority.md",
                    "lifecycle": "active",
                    "mutation": "none",
                    "consumers": ["docs/consumer.md"],
                    "disposition": "retain",
                    "successor": None,
                    "tests": [],
                },
            ],
        }
        manifest["files"].sort(key=lambda row: row["path"])
        manifest_path = root / "scripts/manifest.yaml"
        manifest_path.write_text(
            yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
        )
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Task Test",
                "-c",
                "user.email=task@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            cwd=root,
            check=True,
        )
        return manifest_path

    def test_generated_checks_fail_closed_on_stale_missing_and_mutating_commands(
        self,
    ) -> None:
        valid_script = "import argparse\nargparse.ArgumentParser().add_argument('--check', action='store_true')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script_path = "scripts/validation/check-supply-chain-policy.py"
            manifest_path = self._generator_repo(root, valid_script, script_path)
            self.assertEqual([], self.checker.check_generated(root, manifest_path))

            (root / script_path).write_text("raise SystemExit(9)\n", encoding="utf-8")
            self.assertIn(
                "generated-check-failed",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )
            producer = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            next(row for row in producer["files"] if row["path"] == script_path).update(
                kind="validator",
            )
            manifest_path.write_text(
                yaml.safe_dump(producer, sort_keys=False), encoding="utf-8"
            )
            self.assertIn(
                "generated-check-failed",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

            (root / script_path).write_text(
                "from pathlib import Path\nPath('docs/output.md').write_text('mutated\\n')\n",
                encoding="utf-8",
            )
            self.assertIn(
                "generated-check-mutated",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

            for surface in ("docs", "tests", "infra"):
                with self.subTest(ignored_surface=surface):
                    subprocess.run(
                        ["git", "restore", "docs/output.md"], cwd=root, check=True
                    )
                    marker = f"{surface}/.ignored-mutation"
                    (root / surface).mkdir(parents=True, exist_ok=True)
                    (root / script_path).write_text(
                        f"from pathlib import Path\nPath('{marker}').write_text('mutated\\n')\n",
                        encoding="utf-8",
                    )
                    (root / ".gitignore").write_text(f"{marker}\n", encoding="utf-8")
                    self.assertIn(
                        "generated-check-mutated",
                        {
                            finding.code
                            for finding in self.checker.check_generated(
                                root, manifest_path
                            )
                        },
                    )
                    (root / marker).unlink()

            subprocess.run(["git", "restore", "docs/output.md"], cwd=root, check=True)
            document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            missing = deepcopy(document)
            next(row for row in missing["files"] if row["path"] == script_path)[
                "check_command"
            ] = [
                "missing-task9-generator-command",
                script_path,
                "--check",
            ]
            manifest_path.write_text(
                yaml.safe_dump(missing, sort_keys=False), encoding="utf-8"
            )
            self.assertIn(
                "generated-check-invalid",
                {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                },
            )

    def test_semantic_evidence_rejects_prose_comments_and_non_test_paths(self) -> None:
        valid_script = "import argparse\nargparse.ArgumentParser().add_argument('--check', action='store_true')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            (root / "docs/consumer.md").write_text(
                "This prose merely mentions scripts/example.py.\n", encoding="utf-8"
            )
            (root / "tests/validation/test_example.py").write_text(
                "# subprocess.run(['python3', 'scripts/example.py', '--check'])\n",
                encoding="utf-8",
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("consumers-unproven", codes)
            self.assertIn("tests-unproven", codes)
            (root / "tests/validation/test_example.py").write_text(
                '"""Prose only: scripts/example.py."""\n', encoding="utf-8"
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("tests-unproven", codes)
            (root / "tests/validation/test_example.py").write_text(
                "TARGET = 'scripts/example.py'\nprint('unrelated')\n",
                encoding="utf-8",
            )
            codes = {
                finding.code
                for finding in self.checker.check_manifest(root, manifest_path)
            }
            self.assertIn("tests-unproven", codes)

    def test_yaml_semantic_evidence_accepts_exact_entry_only(self) -> None:
        target = "scripts/example.py"
        exact = "entry: python3 scripts/example.py --check\n"
        comment = "# entry: python3 scripts/example.py --check\n"
        collision = "entry: python3 scripts/example.py-extra --check\n"

        self.assertTrue(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", exact, target, is_test=False
            )
        )
        self.assertFalse(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", comment, target, is_test=False
            )
        )
        self.assertFalse(
            self.checker._reference_proves_use(
                ".pre-commit-config.yaml", collision, target, is_test=False
            )
        )

    def test_yaml_semantic_evidence_cycle_is_an_explicit_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            consumer = root / ".pre-commit-config.yaml"
            consumer.write_text("entry: &loop\n  - *loop\n", encoding="utf-8")
            document = {
                "files": [
                    {
                        "path": "scripts/example.py",
                        "consumers": [".pre-commit-config.yaml"],
                        "tests": [],
                    }
                ]
            }
            codes = {
                finding.code
                for finding in self.checker._semantic_findings(root, document)
            }
        self.assertIn("consumers-invalid", codes)

    def test_python_semantic_evidence_accepts_target_linked_uses(self) -> None:
        positives = (
            "import scripts.example\n",
            "import subprocess\nsubprocess.run(['python3', 'scripts/example.py', '--check'])\n",
            "from scripts import example\nexample.validate_manifest_document({}, set())\n",
            "import importlib.util\nfrom pathlib import Path\n"
            "TARGET = Path('scripts/example.py')\n"
            "importlib.util.spec_from_file_location('scripts.example', TARGET)\n",
        )
        for source in positives:
            with self.subTest(source=source):
                self.assertTrue(
                    self.checker._python_proves_use(source, "scripts/example.py")
                )

    def test_python_semantic_evidence_rejects_unrelated_calls_and_collisions(
        self,
    ) -> None:
        negatives = (
            "from unrelated import example\n",
            "TARGET = 'scripts/example.py'\nlen(TARGET)\n",
            "len('scripts/example.py')\n",
            "import logging\nTARGET = 'scripts/example.py'\nlogging.info(TARGET)\n",
            "import logging\nlogging.info('scripts/example.py')\n",
            "from pathlib import Path\nTARGET = Path('scripts/example.py')\nTARGET.unrelated()\n",
            "import subprocess\nsubprocess.run(['python3', 'other/scripts/example.py'])\n",
            "import scripts.example_extra\n",
        )
        for source in negatives:
            with self.subTest(source=source):
                self.assertFalse(
                    self.checker._python_proves_use(source, "scripts/example.py")
                )

    def test_python_semantic_evidence_rejects_ambiguous_path_reassignment(self) -> None:
        source = (
            "import subprocess\n"
            "TARGET = 'scripts/example.py'\n"
            "TARGET = 'scripts/other.py'\n"
            "subprocess.run(['python3', TARGET])\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_rejects_sibling_function_scope_join(self) -> None:
        source = (
            "from pathlib import Path\n"
            "def one():\n"
            "    BASE = Path('scripts')\n"
            "def two():\n"
            "    from example import helper\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_rejects_sibling_class_scope_join(self) -> None:
        source = (
            "from pathlib import Path\n"
            "class One:\n"
            "    BASE = Path('scripts')\n"
            "class Two:\n"
            "    from example import helper\n"
        )
        self.assertFalse(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_python_semantic_evidence_allows_explicit_module_path_visibility(
        self,
    ) -> None:
        source = (
            "from pathlib import Path\n"
            "BASE = Path('scripts')\n"
            "def use():\n"
            "    from example import helper\n"
        )
        self.assertTrue(self.checker._python_proves_use(source, "scripts/example.py"))

    def test_declared_paths_reject_symlinks_before_execution(self) -> None:
        valid_script = "raise SystemExit('must not execute')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            outside = root.parent / f"{root.name}-outside.py"
            outside.write_text(valid_script, encoding="utf-8")
            (root / "scripts/example.py").unlink()
            (root / "scripts/example.py").symlink_to(outside)
            try:
                codes = {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                }
                self.assertIn("declared-path-invalid", codes)
                self.assertNotIn("generated-check-failed", codes)
            finally:
                outside.unlink(missing_ok=True)

    def test_declared_output_symlink_outside_repo_is_never_followed(self) -> None:
        valid_script = "raise SystemExit('must not execute')\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = self._generator_repo(root, valid_script)
            outside = root.parent / f"{root.name}-outside-output.md"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "docs/output.md").unlink()
            (root / "docs/output.md").symlink_to(outside)
            try:
                codes = {
                    finding.code
                    for finding in self.checker.check_generated(root, manifest_path)
                }
                self.assertIn("declared-path-invalid", codes)
                self.assertEqual("outside\n", outside.read_text(encoding="utf-8"))
                self.assertNotIn("generated-check-failed", codes)
            finally:
                outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
