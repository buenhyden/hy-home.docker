"""Synthetic Wiki preparation contracts, never runtime."""

import ast
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from scripts.lib.ops.wiki_preparation import PreparationError, validate_preparation

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "infra/09-platform-ops/project-registration/wiki-preparation"
KINDS = (
    "consumer-manifest",
    "source-artifact",
    "job-outbox-handoff",
    "blog-data-handoff",
)


def package_inputs():
    schemas = {
        name: json.loads((PACKAGE / "schemas" / f"{name}.schema.json").read_text())
        for name in KINDS
    }
    schemas["urn:hyhome:registration:v1"] = json.loads(
        (PACKAGE.parent / "schema.json").read_text()
    )
    fixtures = {
        name: json.loads((PACKAGE / "fixtures" / f"{name}.valid.json").read_text())
        for name in KINDS
    }
    payload = (PACKAGE / "fixtures/artifact.synthetic.txt").read_bytes()
    return schemas, fixtures, payload


def trusted_policy():
    """Return caller-owned authority without deriving it from candidate fixtures."""
    return {
        "project_id": "example-project",
        "secret_refs": ["example_project_db_password"],
        "sources": {
            "buenhyden/blog-data": {
                "refs": ["dev"],
                "revisions": ["a" * 40],
                "paths": ["Literature/synthetic.md"],
                "versions": [
                    {
                        "parser": "synthetic-1",
                        "chunker": "synthetic-1",
                        "embedding": "disabled",
                    }
                ],
            },
            "buenhyden/Project-Template": {
                "refs": ["dev"],
                "revisions": ["a" * 40],
                "paths": ["README.md"],
            },
            "buenhyden/hy-home.docker": {
                "refs": ["main"],
                "revisions": ["a" * 40],
                "paths": [
                    "infra/09-platform-ops/project-registration/wiki-preparation"
                ],
            },
            "buenhyden/hy-home.k8s": {
                "refs": ["main"],
                "revisions": ["a" * 40],
                "paths": ["README.md"],
            },
        },
        "identity": {
            "issuer": "https://identity.example.test/realms/dev",
            "audience": "example-project",
        },
        "classification": "internal",
        "registration_endpoints": {
            "same_daemon": {
                "db": {
                    "scheme": "postgresql",
                    "host": "dev-pg",
                    "port": 5432,
                    "path": "/example_project_db",
                }
            }
        },
        "registration_refs": {
            "infra_ref": "a" * 40,
            "template_ref": "a" * 40,
            "project_ref": "a" * 40,
        },
        "registration_backup_restore": {
            "backup_owner": "infra",
            "restore_owner": "infra",
        },
        "permissions": ["read", "append-candidate"],
        "valkey_commands": ["GET", "SET"],
        "qdrant_rbac": {
            "collection": "example-project",
            "roles": ["project-reader", "project-writer"],
        },
        "egress": [],
        "metric_labels": ["operation", "result"],
        "max_metric_series": 20,
        "retention_days": 30,
        "backup": {
            "owner": "project",
            "rpo_seconds": 3600,
            "rto_seconds": 7200,
            "restore_drill": "NOT_RUN",
        },
        "quota": {
            "cpu_milli": 500,
            "memory_mib": 512,
            "storage_gib": 2,
            "requests_per_minute": 60,
        },
        "acl_readers": ["example-project-reader"],
        "allowed_networks": ["example-project-net"],
        "resources": {
            "db_prefix": "example_project_",
            "db": {
                "name": "example_project_db",
                "schema": "example_project_app",
                "owner_role": "example_project_owner",
                "migrator_role": "example_project_migrator",
                "runtime_role": "example_project_runtime",
                "reader_role": "example_project_reader",
            },
            "valkey_user_prefix": "example-project-",
            "valkey_prefix": "example-project",
            "s3_bucket": "example-project",
            "s3_prefix": "example-project/",
            "search_collection": "example-project",
            "search_authorization_path": "/projects/example-project",
            "oidc_client_id": "example-project",
            "telemetry_service": "example-project",
            "network_prefix": "example-project-",
        },
        "blog": {
            "repository": "buenhyden/blog-data",
            "base_sha": "a" * 40,
            "candidate_ids": ["example-candidate"],
            "allowed_paths": ["Literature/synthetic.md"],
            "write_set": [
                {
                    "candidate_id": "example-candidate",
                    "path": "Literature/synthetic.md",
                    "sha256": (
                        "ec32b2d2486e1016b4ffca72a25f7c1e"
                        "5540894ed5f1d3fadaa0b46ec04cc26a"
                    ),
                }
            ],
        },
        "job": {
            "job_id": "example-job",
            "dedup_key": (
                "ec32b2d2486e1016b4ffca72a25f7c1e5540894ed5f1d3fadaa0b46ec04cc26a"
            ),
            "event_id": "example-event",
            "max_attempts": 3,
            "timeout_seconds": 300,
        },
    }


def schema_is_valid(kind, document, schemas):
    registry = Registry().with_resources(
        [
            (uri, Resource.from_contents(schema))
            for uri, schema in schemas.items()
            if uri.startswith("urn:")
        ]
    )
    return not list(
        Draft202012Validator(schemas[kind], registry=registry).iter_errors(document)
    )


def run_registration_validator(document):
    """Run the unmodified canonical CLI against one synthetic tempfile."""
    with tempfile.TemporaryDirectory(prefix="p09-registration-") as directory:
        candidate = Path(directory) / "registration.json"
        candidate.write_text(json.dumps(document), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validation/check-project-registration.py"),
                str(candidate),
                "--allow-secret-ref",
                "example_project_db_password",
            ],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
        )


class WikiPreparationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas, cls.fixtures, cls.payload = package_inputs()
        cls.policy = trusted_policy()

    def validate(self, kind, document, **options):
        arguments = {
            "synthetic_bytes": {"example-candidate": self.payload}
            if kind == "blog-data-handoff"
            else self.payload,
            "policy": self.policy,
            "prior_receipts": {},
            "prior_states": {},
        }
        arguments.update(options)
        return validate_preparation(kind, document, self.schemas, **arguments)

    @staticmethod
    def history(receipt, previous=None):
        receipts = dict(previous["prior_receipts"]) if previous else {}
        states = dict(previous["prior_states"]) if previous else {}
        receipts.update(receipt["receipt_entries"])
        if receipt["state_record"] is not None:
            states[receipt["admission_idempotency_key"]] = receipt["state_record"]
        return {"prior_receipts": receipts, "prior_states": states}

    def test_fixture_expectations_separate_schema_from_semantics(self):
        expectations = json.loads((PACKAGE / "fixtures/expectations.json").read_text())
        self.assertEqual(8, len(expectations["cases"]))
        for case in expectations["cases"]:
            with self.subTest(fixture=case["fixture"]):
                kind = case["fixture"].split(".", 1)[0]
                document = json.loads(
                    (PACKAGE / "fixtures" / case["fixture"]).read_text()
                )
                schema_result = (
                    "valid"
                    if schema_is_valid(kind, document, self.schemas)
                    else "invalid"
                )
                self.assertEqual(case["schema"], schema_result)
                try:
                    receipt = self.validate(kind, document)
                except PreparationError:
                    semantic_result = "invalid"
                else:
                    semantic_result = "valid"
                    self.assertTrue(receipt["synthetic_contract_valid"])
                    self.assertFalse(receipt["deployed"])
                self.assertEqual(case["semantic"], semantic_result)

    def test_helper_modules_have_a_fixed_pure_import_boundary(self):
        modules = (
            ROOT / "scripts/lib/ops/wiki_preparation.py",
            ROOT / "scripts/lib/ops/wiki_preparation_semantics.py",
        )
        repository_imports = []
        for module in modules:
            tree = ast.parse(module.read_text())
            functions = [
                node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
            ]
            self.assertLess(
                max(node.end_lineno - node.lineno + 1 for node in functions), 50
            )
            for node in ast.walk(tree):
                imported = (
                    [alias.name for alias in node.names]
                    if isinstance(node, ast.Import)
                    else [node.module]
                    if isinstance(node, ast.ImportFrom)
                    else []
                )
                for name in imported:
                    self.assertNotIn(
                        name.split(".")[0],
                        {"os", "pathlib", "socket", "subprocess", "urllib"},
                    )
                    if name.startswith("scripts."):
                        repository_imports.append(name)
        self.assertEqual(
            ["scripts.lib.ops.wiki_preparation_semantics"], repository_imports
        )

    def test_consumer_qdrant_roles_are_order_insensitive_but_exact(self):
        document = copy.deepcopy(self.fixtures["consumer-manifest"])
        document["qdrant_rbac"]["roles"].reverse()
        self.assertTrue(
            self.validate("consumer-manifest", document)["synthetic_contract_valid"]
        )

    def test_unmodified_generic_registration_cli_is_reused(self):
        document = self.fixtures["consumer-manifest"]["registration"]
        accepted = run_registration_validator(document)
        self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)
        rejected = run_registration_validator({**document, "project_id": "other"})
        self.assertEqual(1, rejected.returncode)
        self.assertIn("project-registration: FAIL", rejected.stdout)

    def test_source_state_receipts_allow_immediate_revocation(self):
        initial = copy.deepcopy(self.fixtures["source-artifact"])
        initial_receipt = self.validate("source-artifact", initial)
        initial_prior = self.history(initial_receipt)
        revoked = copy.deepcopy(initial)
        revoked.update(
            events=[
                {
                    "id": "revoke-event",
                    "kind": "revoke",
                    "sequence": 1,
                    "generation": 1,
                }
            ],
            access_state="revoked",
            evaluated_sequence=1,
            surface_watermarks={
                surface: 1 for surface in revoked["surface_watermarks"]
            },
            tombstone=False,
        )
        changed_rights = copy.deepcopy(revoked)
        changed_rights["rights"]["basis"] = "pending-verification"
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", changed_rights, **initial_prior)

        revoked_receipt = self.validate(
            "source-artifact",
            revoked,
            **initial_prior,
        )
        self.assertNotEqual(
            initial_receipt["idempotency_key"], revoked_receipt["idempotency_key"]
        )

        complete_prior = self.history(revoked_receipt, initial_prior)
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", initial, **complete_prior)

        forgot_revocation = copy.deepcopy(initial)
        forgot_revocation["generation"] = 2
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", forgot_revocation, **complete_prior)

    def test_job_state_receipts_allow_legal_progress(self):
        pending = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        pending.update(
            transitions=[], state="pending", attempt=0, published_generation=None
        )
        pending["outbox"]["acknowledged"] = False
        pending_receipt = self.validate("job-outbox-handoff", pending)
        prior = self.history(pending_receipt)
        changed_admission = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        changed_admission.update(backfill=True, backfill_of="previous-job")
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", changed_admission, **prior)

        succeeded_receipt = self.validate(
            "job-outbox-handoff",
            self.fixtures["job-outbox-handoff"],
            **prior,
        )
        self.assertNotEqual(
            pending_receipt["idempotency_key"], succeeded_receipt["idempotency_key"]
        )

        prior = self.history(succeeded_receipt, prior)
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", pending, **prior)

    def test_source_state_receipts_reject_rollback(self):
        allowed = copy.deepcopy(self.fixtures["source-artifact"])
        allowed_receipt = self.validate("source-artifact", allowed)
        allowed_history = self.history(allowed_receipt)
        revoked = copy.deepcopy(allowed)
        revoked.update(
            events=[
                {
                    "id": "revoke-event",
                    "kind": "revoke",
                    "sequence": 1,
                    "generation": 1,
                }
            ],
            access_state="revoked",
            evaluated_sequence=1,
            surface_watermarks={
                surface: 1 for surface in revoked["surface_watermarks"]
            },
            tombstone=False,
        )
        revoked_receipt = self.validate(
            "source-artifact",
            revoked,
            **allowed_history,
        )
        prior = self.history(revoked_receipt, allowed_history)
        with self.subTest(regression="same-generation"):
            with self.assertRaises(PreparationError):
                self.validate("source-artifact", allowed, **prior)

        forgot_revocation = copy.deepcopy(allowed)
        forgot_revocation["generation"] = 2
        with self.subTest(regression="new-generation"):
            with self.assertRaises(PreparationError):
                self.validate("source-artifact", forgot_revocation, **prior)

    def test_source_frontier_is_path_wide_across_content_changes(self):
        revoked = copy.deepcopy(self.fixtures["source-artifact"])
        revoked.update(
            events=[
                {
                    "id": "revoke-event",
                    "kind": "revoke",
                    "sequence": 1,
                    "generation": 1,
                }
            ],
            access_state="revoked",
            evaluated_sequence=1,
            surface_watermarks={
                surface: 1 for surface in revoked["surface_watermarks"]
            },
            tombstone=False,
        )
        receipt = self.validate("source-artifact", revoked)
        prior = self.history(receipt)
        version_two = {
            "parser": "synthetic-2",
            "chunker": "synthetic-2",
            "embedding": "disabled",
        }
        version_policy = copy.deepcopy(self.policy)
        version_policy["sources"]["buenhyden/blog-data"]["versions"].append(version_two)
        same_generation_version = copy.deepcopy(revoked)
        same_generation_version["versions"] = version_two
        with self.subTest(regression="same-generation-version-change"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    same_generation_version,
                    policy=version_policy,
                    **prior,
                )

        alternate_bytes = b"alternate synthetic source artifact\n"
        alternate_sha = hashlib.sha256(alternate_bytes).hexdigest()
        same_generation = copy.deepcopy(revoked)
        same_generation.update(sha256=alternate_sha, idempotency_key=alternate_sha)
        same_generation["provenance"]["artifact_sha256"] = alternate_sha
        with self.subTest(regression="same-generation-content-change"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    same_generation,
                    synthetic_bytes=alternate_bytes,
                    **prior,
                )

        next_generation = copy.deepcopy(same_generation)
        next_generation.update(generation=2, revision="b" * 40)
        next_generation["versions"] = version_two
        next_generation["source"]["revision"] = "b" * 40
        next_generation["provenance"]["source_revision"] = "b" * 40
        policy = version_policy
        policy["sources"]["buenhyden/blog-data"]["revisions"].append("b" * 40)
        forgot_revocation = copy.deepcopy(next_generation)
        forgot_revocation.update(
            events=[],
            access_state="allowed",
            evaluated_sequence=0,
            surface_watermarks={
                surface: 0 for surface in forgot_revocation["surface_watermarks"]
            },
        )
        with self.subTest(regression="new-content-bypasses-prior-revocation"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    forgot_revocation,
                    synthetic_bytes=alternate_bytes,
                    policy=policy,
                    **prior,
                )

        next_receipt = self.validate(
            "source-artifact",
            next_generation,
            synthetic_bytes=alternate_bytes,
            policy=policy,
            **prior,
        )
        prior = self.history(next_receipt, prior)
        allowed = copy.deepcopy(next_generation)
        allowed.update(
            events=[],
            access_state="allowed",
            evaluated_sequence=0,
            surface_watermarks={
                surface: 0 for surface in allowed["surface_watermarks"]
            },
        )
        with self.subTest(regression="new-content-forgets-revocation"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    allowed,
                    synthetic_bytes=alternate_bytes,
                    policy=policy,
                    **prior,
                )

    def test_source_versions_require_an_exact_typed_policy_allowlist(self):
        artifact = copy.deepcopy(self.fixtures["source-artifact"])
        artifact["versions"]["parser"] = "synthetic-2"
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", artifact)

        source_policy = self.policy["sources"]["buenhyden/blog-data"]
        for versions in (
            "synthetic-1",
            [{"parser": "*", "chunker": "synthetic-1", "embedding": "disabled"}],
            [{"parser": "", "chunker": "synthetic-1", "embedding": "disabled"}],
        ):
            with self.subTest(versions=versions):
                policy = copy.deepcopy(self.policy)
                policy["sources"]["buenhyden/blog-data"]["versions"] = versions
                with self.assertRaises(PreparationError):
                    self.validate(
                        "source-artifact",
                        self.fixtures["source-artifact"],
                        policy=policy,
                    )
        self.assertEqual(1, len(source_policy["versions"]))

    def test_job_state_receipts_reject_rollback(self):
        pending = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        pending.update(
            transitions=[], state="pending", attempt=0, published_generation=None
        )
        pending["outbox"]["acknowledged"] = False
        pending_receipt = self.validate("job-outbox-handoff", pending)
        pending_history = self.history(pending_receipt)
        succeeded_receipt = self.validate(
            "job-outbox-handoff",
            self.fixtures["job-outbox-handoff"],
            **pending_history,
        )
        succeeded_history = self.history(succeeded_receipt, pending_history)
        with self.assertRaises(PreparationError):
            self.validate(
                "job-outbox-handoff",
                pending,
                **succeeded_history,
            )

    def test_source_frontier_rejects_surface_watermark_rollback(self):
        revoked = copy.deepcopy(self.fixtures["source-artifact"])
        revoked.update(
            events=[
                {
                    "id": "revoke-event",
                    "kind": "revoke",
                    "sequence": 1,
                    "generation": 1,
                }
            ],
            access_state="revoked",
            evaluated_sequence=1,
            surface_watermarks={
                surface: 2 for surface in revoked["surface_watermarks"]
            },
            tombstone=False,
        )
        with self.subTest(regression="watermark-beyond-evaluated-sequence"):
            with self.assertRaises(PreparationError):
                self.validate("source-artifact", revoked)

        revoked["evaluated_sequence"] = 2
        receipt = self.validate("source-artifact", revoked)
        regressed = copy.deepcopy(revoked)
        regressed.update(
            generation=2,
            surface_watermarks={
                surface: 1 for surface in regressed["surface_watermarks"]
            },
        )
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", regressed, **self.history(receipt))

    def test_job_frontier_rejects_watermark_rollback(self):
        running = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        running.update(
            transitions=[{"from": "pending", "to": "running"}],
            state="running",
            attempt=1,
            published_generation=None,
            deletion_watermark=2,
            generation_watermark=3,
        )
        running["outbox"].update(sequence=3, acknowledged=False)
        receipt = self.validate("job-outbox-handoff", running)
        regressed = copy.deepcopy(running)
        regressed.update(
            transitions=[
                *regressed["transitions"],
                {"from": "running", "to": "partial"},
            ],
            state="partial",
            deletion_watermark=1,
            generation_watermark=2,
        )
        regressed["outbox"]["sequence"] = 4
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", regressed, **self.history(receipt))

    def test_frontier_rejects_malformed_prior_state(self):
        source = self.fixtures["source-artifact"]
        receipt = self.validate("source-artifact", source)
        for malformed in (None, {"revision": {}}):
            with self.subTest(malformed=malformed):
                with self.assertRaises(PreparationError):
                    self.validate(
                        "source-artifact",
                        source,
                        prior_receipts=receipt["receipt_entries"],
                        prior_states={receipt["admission_idempotency_key"]: malformed},
                    )

    def test_frontier_requires_matching_anchor_and_state(self):
        source = self.fixtures["source-artifact"]
        receipt = self.validate("source-artifact", source)
        history = self.history(receipt)
        with self.subTest(missing="state"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    source,
                    prior_receipts=history["prior_receipts"],
                    prior_states={},
                )
        with self.subTest(missing="anchor"):
            with self.assertRaises(PreparationError):
                self.validate(
                    "source-artifact",
                    source,
                    prior_receipts={
                        receipt["idempotency_key"]: receipt["request_sha256"]
                    },
                    prior_states=history["prior_states"],
                )

    def test_terminal_job_frontier_cannot_advance(self):
        succeeded = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        receipt = self.validate("job-outbox-handoff", succeeded)
        advanced = copy.deepcopy(succeeded)
        advanced.update(
            generation=2,
            published_generation=2,
            generation_watermark=2,
        )
        advanced["outbox"]["sequence"] = 2
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", advanced, **self.history(receipt))

    def test_job_retry_and_timeout_limits_cannot_be_expanded(self):
        for field, value in (
            ("max_attempts", 1_000_000_000),
            ("timeout_seconds", 2_147_483_647),
        ):
            document = copy.deepcopy(self.fixtures["job-outbox-handoff"])
            document[field] = value
            with self.subTest(field=field, expansion="document"):
                with self.assertRaises(PreparationError):
                    self.validate("job-outbox-handoff", document)

            policy = copy.deepcopy(self.policy)
            policy["job"][field] = value
            with self.subTest(field=field, expansion="policy"):
                with self.assertRaises(PreparationError):
                    self.validate(
                        "job-outbox-handoff",
                        self.fixtures["job-outbox-handoff"],
                        policy=policy,
                    )
            with self.subTest(field=field, expansion="coherent"):
                with self.assertRaises(PreparationError):
                    self.validate("job-outbox-handoff", document, policy=policy)

    def test_all_package_folders_have_korean_readme(self):
        for directory in [PACKAGE, *[p for p in PACKAGE.rglob("*") if p.is_dir()]]:
            with self.subTest(directory=directory.name):
                readme = directory / "README.md"
                self.assertTrue(readme.is_file())
                text = readme.read_text()
                self.assertTrue(any("\uac00" <= char <= "\ud7a3" for char in text))
