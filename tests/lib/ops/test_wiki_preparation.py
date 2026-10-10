"""P09 pure helper semantic boundaries; only synthetic inputs."""

import copy
import json
import unittest
from unittest.mock import patch

from scripts.lib.ops.wiki_preparation import PreparationError, validate_preparation
from tests.validation.test_wiki_preparation_contracts import (
    package_inputs,
    trusted_policy,
)


class PreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas, cls.fixtures, cls.payload = package_inputs()
        cls.policy = trusted_policy()

    def validate(self, kind, doc, **options):
        arguments = {
            "synthetic_bytes": {"example-candidate": self.payload}
            if kind == "blog-data-handoff"
            else self.payload,
            "policy": copy.deepcopy(self.policy),
            "prior_receipts": {},
            "prior_states": {},
        }
        arguments.update(options)
        return validate_preparation(kind, doc, self.schemas, **arguments)

    def assert_reject(self, kind, mutate, **options):
        doc = copy.deepcopy(self.fixtures[kind])
        mutate(doc)
        with self.assertRaises(PreparationError) as caught:
            self.validate(kind, doc, **options)
        self.assertNotIn("example-project", str(caught.exception))

    def test_unknown_contract_and_nonparsed_input_rejected(self):
        for kind, doc in [
            ("unknown", {"project_id": "example-project"}),
            ("consumer-manifest", "raw"),
        ]:
            with self.assertRaises(PreparationError):
                validate_preparation(
                    kind,
                    doc,
                    self.schemas,
                    policy=copy.deepcopy(self.policy),
                    prior_receipts={},
                    prior_states={},
                )

    def test_consumer_boundaries(self):
        cases = [
            lambda d: d.update(namespace="other-project"),
            lambda d: d["identity"].update(audience=""),
            lambda d: d.update(permissions=["admin"]),
            lambda d: d["sources"][0].update(ref="main"),
            lambda d: d["sources"][0].update(paths=["../secret"]),
            lambda d: d.update(disabled_by_design=["wiki-runtime"]),
            lambda d: d["registration"]["approval"].update(state="approved"),
            lambda d: d.update(valkey_commands=["*"]),
            lambda d: d["qdrant_rbac"].update(roles=["admin"]),
            lambda d: d["qdrant_rbac"].update(roles=["*"]),
            lambda d: d["registration"]["valkey"].update(acl_prefix="other-project"),
            lambda d: d["registration"]["db"].update(runtime_role="postgres"),
            lambda d: d["registration"]["search"].update(collection="other-project"),
            lambda d: d["registration"]["s3"].update(bucket="other-project"),
            lambda d: d["registration"]["s3"].update(prefix="example-projectx/"),
            lambda d: d["registration"]["oidc"].update(client_id="other-project"),
            lambda d: d["identity"].update(audience="other-project"),
            lambda d: d["registration"]["telemetry"].update(
                **{"service.name": "other-project"}
            ),
            lambda d: d["registration"].update(allowed_networks=["other-project-net"]),
        ]
        for case in cases:
            self.assert_reject("consumer-manifest", case)
        self.assert_reject("consumer-manifest", lambda d: None, policy={})

    def test_policy_binds_consumer_artifact_and_job_authority(self):
        consumer_cases = [
            lambda d: d["registration"]["endpoints"]["same_daemon"]["db"].update(
                scheme="http", host="other-project-db"
            ),
            lambda d: d["registration"].update(
                infra_ref="b" * 40,
                template_ref="b" * 40,
                project_ref="b" * 40,
            ),
            lambda d: d.update(retention_days=31),
            lambda d: d["backup"].update(rpo_seconds=7200),
            lambda d: d.update(
                permissions=["read", "append-candidate", "project-migrate"]
            ),
            lambda d: d["registration"]["db"].update(
                runtime_role="example_project_other"
            ),
            lambda d: d["registration"].update(
                allowed_networks=["example-project-extra"]
            ),
            lambda d: d["registration"]["quota"].update(cpu_milli=501),
            lambda d: d["registration"]["backup_restore"].update(
                backup_owner="project"
            ),
        ]
        for mutate in consumer_cases:
            with self.subTest(contract="consumer-manifest", mutate=mutate):
                self.assert_reject("consumer-manifest", mutate)

        with self.subTest(contract="source-artifact"):
            self.assert_reject(
                "source-artifact",
                lambda d: d["acl"].update(readers=["example-project-other"]),
            )

        def rename_job_dedup(document):
            document["dedup_key"] = "b" * 64
            document["outbox"]["dedup_key"] = "b" * 64

        with self.subTest(contract="job-outbox-handoff"):
            self.assert_reject("job-outbox-handoff", rename_job_dedup)

    def test_artifact_hash_acl_revocation_and_provenance(self):
        cases = [
            lambda d: d.update(sha256="b" * 64),
            lambda d: d.update(path="other.md"),
            lambda d: d["provenance"].update(source_revision="b" * 40),
            lambda d: d["acl"].update(project_id="other-project"),
            lambda d: d["acl"].update(readers=["other-project-reader"]),
            lambda d: d.update(enforcement=["search"]),
            lambda d: d.update(effective_at="2026-10-11T00:00:00Z"),
            lambda d: d.update(
                events=[
                    {
                        "id": "delete-event",
                        "kind": "delete",
                        "sequence": 1,
                        "generation": 2,
                    }
                ]
            ),
            lambda d: d.update(
                events=[
                    {
                        "id": "delete-event",
                        "kind": "delete",
                        "sequence": 2,
                        "generation": 1,
                    },
                    {
                        "id": "revoke-event",
                        "kind": "revoke",
                        "sequence": 1,
                        "generation": 1,
                    },
                ]
            ),
            lambda d: d.update(
                events=[
                    {
                        "id": "delete-event",
                        "kind": "delete",
                        "sequence": 1,
                        "generation": 1,
                    },
                    {
                        "id": "delete-event",
                        "kind": "revoke",
                        "sequence": 2,
                        "generation": 1,
                    },
                ]
            ),
        ]
        for case in cases:
            self.assert_reject("source-artifact", case)
        self.assert_reject("source-artifact", lambda d: None, synthetic_bytes=None)
        self.assert_reject(
            "source-artifact", lambda d: None, synthetic_bytes=b"changed"
        )
        self.assert_reject(
            "source-artifact", lambda d: d.update(retrieved_at="not-a-date")
        )

    def test_trusted_policy_rejects_coherent_project_renames(self):
        artifact = copy.deepcopy(self.fixtures["source-artifact"])
        artifact.update(project_id="other-project", path="Literature/other.md")
        artifact["source"]["paths"] = ["Literature/other.md"]
        artifact["acl"].update(
            project_id="other-project", readers=["other-project-reader"]
        )

        renamed = {
            "source-artifact": artifact,
            "job-outbox-handoff": {
                **copy.deepcopy(self.fixtures["job-outbox-handoff"]),
                "project_id": "other-project",
            },
            "blog-data-handoff": {
                **copy.deepcopy(self.fixtures["blog-data-handoff"]),
                "project_id": "other-project",
            },
        }
        for kind, document in renamed.items():
            with self.subTest(kind=kind):
                with self.assertRaises(PreparationError):
                    self.validate(kind, document)

    def test_trusted_policy_rejects_authority_expansion(self):
        policy_cases = [
            ("consumer-manifest", lambda p: p.update(project_id="other-project")),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(refs=["main"]),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(
                    refs="development"
                ),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(
                    revisions="x" + ("a" * 40) + "y"
                ),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(
                    paths="prefixLiterature/synthetic.mdsuffix"
                ),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(refs=["dev", 1]),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(
                    refs=["dev", *[f"extra-{index}" for index in range(128)]]
                ),
            ),
            (
                "consumer-manifest",
                lambda p: p["sources"]["buenhyden/blog-data"].update(
                    paths=["Literaturex/synthetic.md"]
                ),
            ),
            (
                "consumer-manifest",
                lambda p: p["resources"].update(s3_bucket="other-project"),
            ),
            ("consumer-manifest", lambda p: p.update(valkey_commands=["*"])),
            (
                "consumer-manifest",
                lambda p: p["qdrant_rbac"].update(roles=["admin"]),
            ),
            (
                "blog-data-handoff",
                lambda p: p["blog"].update(candidate_ids=["other-candidate"]),
            ),
            ("consumer-manifest", lambda p: p.update(classification="")),
        ]
        for kind, mutate in policy_cases:
            with self.subTest(kind=kind, mutate=mutate):
                policy = copy.deepcopy(self.policy)
                mutate(policy)
                with self.assertRaises(PreparationError):
                    self.validate(kind, self.fixtures[kind], policy=policy)

        artifact = copy.deepcopy(self.fixtures["source-artifact"])
        artifact.update(path="Literaturex/synthetic.md")
        artifact["source"]["paths"] = ["Literaturex/synthetic.md"]
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", artifact)

    def test_job_state_retry_generation_and_delete_priority(self):
        cases = [
            lambda d: d["transitions"][0].update(to="succeeded"),
            lambda d: d.update(state="failed"),
            lambda d: d.update(attempt=4),
            lambda d: d["outbox"].update(dedup_key="b" * 64),
            lambda d: d["stores"].update(qdrant="failed"),
            lambda d: d.update(published_generation=2),
            lambda d: d.update(deletion_watermark=2),
            lambda d: d.update(generation_watermark=2),
            lambda d: d.update(transitions=[], state="pending"),
        ]
        for case in cases:
            self.assert_reject("job-outbox-handoff", case)
        pending = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        pending.update(
            transitions=[], state="pending", published_generation=None, attempt=0
        )
        pending["outbox"]["acknowledged"] = False
        self.assertTrue(
            self.validate("job-outbox-handoff", pending)["synthetic_contract_valid"]
        )
        deletion_ahead_of_outbox = copy.deepcopy(pending)
        deletion_ahead_of_outbox["deletion_watermark"] = 999
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", deletion_ahead_of_outbox)
        recovery = copy.deepcopy(pending)
        recovery.update(
            transitions=[
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "partial"},
                {"from": "partial", "to": "running"},
                {"from": "running", "to": "succeeded"},
            ],
            state="succeeded",
            published_generation=1,
            attempt=2,
        )
        self.assertTrue(
            self.validate("job-outbox-handoff", recovery)["synthetic_contract_valid"]
        )

    def test_job_dead_letter_matches_retry_exhaustion(self):
        exhausted = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        exhausted.update(
            transitions=[
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
            ],
            state="failed",
            attempt=3,
            published_generation=None,
            dead_letter={
                "disposition": "quarantined",
                "reason": "retry-exhausted",
                "replay_requires_approval": True,
            },
        )
        exhausted["outbox"]["acknowledged"] = False
        self.assertTrue(
            self.validate("job-outbox-handoff", exhausted)["synthetic_contract_valid"]
        )

        not_quarantined = copy.deepcopy(exhausted)
        not_quarantined["dead_letter"].update(disposition="none", reason=None)
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", not_quarantined)

        premature = copy.deepcopy(exhausted)
        premature.update(
            transitions=[
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
            ],
            attempt=1,
        )
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", premature)

        exhausted_pending = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        exhausted_pending.update(
            transitions=[
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
            ],
            state="pending",
            attempt=1,
            max_attempts=1,
            published_generation=None,
        )
        exhausted_pending["outbox"]["acknowledged"] = False
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", exhausted_pending)

    def test_revocation_delete_priority_and_public_dead_state_rejection(self):
        artifact = copy.deepcopy(self.fixtures["source-artifact"])
        artifact.update(
            events=[
                {
                    "id": "delete-event",
                    "kind": "delete",
                    "sequence": 1,
                    "generation": 1,
                },
                {
                    "id": "revoke-event",
                    "kind": "revoke",
                    "sequence": 2,
                    "generation": 1,
                },
            ],
            access_state="deleted",
            evaluated_sequence=2,
            tombstone=True,
            surface_watermarks={
                surface: 2 for surface in artifact["surface_watermarks"]
            },
        )
        self.assertTrue(
            self.validate("source-artifact", artifact)["synthetic_contract_valid"]
        )
        artifact["access_state"] = "revoked"
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", artifact)
        artifact.update(access_state="deleted", evaluated_sequence=1)
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", artifact)
        artifact.update(
            events=[
                {"id": "revoke-event", "kind": "revoke", "sequence": 1, "generation": 1}
            ],
            access_state="revoked",
            evaluated_sequence=1,
            tombstone=False,
            surface_watermarks={
                surface: 1 for surface in artifact["surface_watermarks"]
            },
        )
        self.assertTrue(
            self.validate("source-artifact", artifact)["synthetic_contract_valid"]
        )
        job = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        job.update(
            transitions=[
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "pending"},
                {"from": "pending", "to": "running"},
                {"from": "running", "to": "failed"},
                {"from": "failed", "to": "dead"},
            ],
            state="dead",
            published_generation=None,
            attempt=3,
        )
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", job)
        job = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        job.update(generation=2, published_generation=2)
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", job)

    def test_blog_exact_selected_writes_hashes_and_receipts(self):
        cases = [
            lambda d: d.update(selected=["other-candidate"]),
            lambda d: d["candidates"].append(
                {**d["candidates"][0], "sha256": "b" * 64}
            ),
            lambda d: d["approval"].update(selected=["other-candidate"]),
            lambda d: d["receipt"].update(base_sha="b" * 40),
            lambda d: d["write_set"].append({**d["write_set"][0], "sha256": "b" * 64}),
            lambda d: d.update(
                selected=["example-candidate", "other-candidate"],
                candidates=[
                    *d["candidates"],
                    {**d["candidates"][0], "id": "other-candidate"},
                ],
            ),
            lambda d: d["write_set"][0].update(path="Permanent/synthetic.md"),
            lambda d: d["write_set"][0].update(sha256="b" * 64),
            lambda d: d["receipt"].update(write_set_sha256="b" * 64),
            lambda d: d["receipt"].update(idempotency_key="b" * 64),
        ]
        for case in cases:
            self.assert_reject("blog-data-handoff", case)
        self.assert_reject("blog-data-handoff", lambda d: None, synthetic_bytes=None)
        self.assert_reject("blog-data-handoff", lambda d: None, synthetic_bytes={})
        self.assert_reject(
            "blog-data-handoff",
            lambda d: None,
            synthetic_bytes={"example-candidate": b"changed"},
        )

    def test_all_blog_candidates_stay_in_safe_literature_paths(self):
        for candidate_id, path in (
            ("permanent-candidate", "Permanent/synthetic.md"),
            ("maps-candidate", "Maps/synthetic.md"),
            ("encoded-candidate", "Literature/%2e%2e/synthetic.md"),
        ):
            with self.subTest(path=path):
                self.assert_reject(
                    "blog-data-handoff",
                    lambda d, candidate_id=candidate_id, path=path: d[
                        "candidates"
                    ].append(
                        {
                            "id": candidate_id,
                            "path": path,
                            "sha256": "b" * 64,
                            "kind": "literature-candidate",
                        }
                    ),
                )

    def test_canonical_paths_surface_watermarks_and_retry_history(self):
        for path in (
            "Literature//synthetic.md",
            "Literature/synthetic.md/",
            "Literature/./synthetic.md",
            "Literature/../synthetic.md",
            "Literature/%2e%2e/synthetic.md",
        ):
            self.assert_reject(
                "consumer-manifest",
                lambda d, path=path: d["sources"][0].update(paths=[path]),
            )
            self.assert_reject(
                "source-artifact", lambda d, path=path: d.update(path=path)
            )
            self.assert_reject(
                "blog-data-handoff",
                lambda d, path=path: d["write_set"][0].update(path=path),
            )
        artifact = copy.deepcopy(self.fixtures["source-artifact"])
        artifact.update(
            events=[
                {"id": "delete-event", "kind": "delete", "sequence": 1, "generation": 1}
            ],
            access_state="deleted",
            evaluated_sequence=1,
            tombstone=True,
            surface_watermarks={
                surface: 1 for surface in artifact["surface_watermarks"]
            },
        )
        artifact["generation"] = 2
        self.assertTrue(
            self.validate("source-artifact", artifact)["synthetic_contract_valid"]
        )
        for surface in artifact["surface_watermarks"]:
            altered = copy.deepcopy(artifact)
            altered["surface_watermarks"][surface] = 0
            with self.assertRaises(PreparationError):
                self.validate("source-artifact", altered)
        artifact["tombstone"] = False
        with self.assertRaises(PreparationError):
            self.validate("source-artifact", artifact)
        job = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        job["transitions"] = [
            {"from": "pending", "to": "running"},
            {"from": "running", "to": "failed"},
            {"from": "failed", "to": "pending"},
        ] * 4 + [
            {"from": "pending", "to": "running"},
            {"from": "running", "to": "succeeded"},
        ]
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", job)
        job = copy.deepcopy(self.fixtures["job-outbox-handoff"])
        job["backfill"] = True
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", job)
        job["backfill_of"] = job["job_id"]
        with self.assertRaises(PreparationError):
            self.validate("job-outbox-handoff", job)
        job["backfill_of"] = "older-dead-job"
        self.assertTrue(
            self.validate("job-outbox-handoff", job)["synthetic_contract_valid"]
        )

    def test_reordered_two_write_set_has_same_receipt(self):
        import hashlib

        document = copy.deepcopy(self.fixtures["blog-data-handoff"])
        candidate = {
            **document["candidates"][0],
            "id": "second-candidate",
            "path": "Literature/second.md",
        }
        document["candidates"].append(candidate)
        document["selected"].append(candidate["id"])
        document["approval"]["selected"].append(candidate["id"])
        document["allowed_paths"].append(candidate["path"])
        document["write_set"].append(
            {
                "candidate_id": candidate["id"],
                "path": candidate["path"],
                "sha256": candidate["sha256"],
            }
        )
        canonical = sorted(
            document["write_set"],
            key=lambda write: (write["path"], write["candidate_id"], write["sha256"]),
        )

        def digest(value):
            return hashlib.sha256(
                json.dumps(
                    value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
                ).encode()
            ).hexdigest()

        document["receipt"]["write_set_sha256"] = digest(canonical)
        document["receipt"]["idempotency_key"] = digest(
            {
                "project_id": "example-project",
                "repository": "buenhyden/blog-data",
                "base_sha": "a" * 40,
                "write_set": canonical,
            }
        )
        policy = copy.deepcopy(self.policy)
        policy["blog"].update(
            candidate_ids=["example-candidate", "second-candidate"],
            allowed_paths=["Literature/synthetic.md", "Literature/second.md"],
            write_set=[
                {
                    "candidate_id": "example-candidate",
                    "path": "Literature/synthetic.md",
                    "sha256": (
                        "ec32b2d2486e1016b4ffca72a25f7c1e"
                        "5540894ed5f1d3fadaa0b46ec04cc26a"
                    ),
                },
                {
                    "candidate_id": "second-candidate",
                    "path": "Literature/second.md",
                    "sha256": (
                        "ec32b2d2486e1016b4ffca72a25f7c1e"
                        "5540894ed5f1d3fadaa0b46ec04cc26a"
                    ),
                },
            ],
        )
        payloads = {"example-candidate": self.payload, "second-candidate": self.payload}
        receipt = self.validate(
            "blog-data-handoff",
            document,
            synthetic_bytes=payloads,
            policy=policy,
        )
        document["write_set"].reverse()
        self.assertEqual(
            receipt,
            self.validate(
                "blog-data-handoff",
                document,
                synthetic_bytes=payloads,
                policy=policy,
            ),
        )
        document["write_set"][1]["path"] = document["write_set"][0]["path"]
        with self.assertRaises(PreparationError):
            self.validate(
                "blog-data-handoff",
                document,
                synthetic_bytes=payloads,
                policy=policy,
            )

    def test_idempotency_replay_and_prior_key_conflict(self):
        for kind, document in self.fixtures.items():
            with self.subTest(kind=kind):
                receipt = self.validate(kind, document)
                replay = self.validate(
                    kind,
                    document,
                    prior_receipts=receipt["receipt_entries"],
                    prior_states=(
                        {receipt["admission_idempotency_key"]: receipt["state_record"]}
                        if receipt["state_record"] is not None
                        else {}
                    ),
                )
                self.assertEqual(receipt, replay)
                with self.assertRaises(PreparationError):
                    self.validate(
                        kind,
                        document,
                        prior_receipts={receipt["idempotency_key"]: "b" * 64},
                    )

    def test_idempotency_keys_are_scoped_by_contract(self):
        source_receipt = self.validate(
            "source-artifact", self.fixtures["source-artifact"]
        )
        job_receipt = self.validate(
            "job-outbox-handoff",
            self.fixtures["job-outbox-handoff"],
            prior_receipts={
                source_receipt["idempotency_key"]: source_receipt["request_sha256"]
            },
        )
        self.assertNotEqual(
            source_receipt["idempotency_key"], job_receipt["idempotency_key"]
        )
        self.assertEqual(
            self.fixtures["source-artifact"]["idempotency_key"],
            source_receipt["raw_idempotency_key"],
        )
        self.assertEqual(
            self.fixtures["job-outbox-handoff"]["dedup_key"],
            job_receipt["raw_idempotency_key"],
        )

    def test_set_like_permutations_keep_request_identity(self):
        document = copy.deepcopy(self.fixtures["consumer-manifest"])
        receipt = self.validate("consumer-manifest", document)
        for field in (
            "permissions",
            "valkey_commands",
            "metric_labels",
            "disabled_by_design",
        ):
            document[field].reverse()
        self.assertEqual(
            receipt["request_sha256"],
            self.validate("consumer-manifest", document)["request_sha256"],
        )

    def test_external_ref_is_never_retrieved(self):
        schemas = copy.deepcopy(self.schemas)
        schemas["source-artifact"] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "https://untrusted.example/schema",
        }
        with patch(
            "urllib.request.urlopen", side_effect=AssertionError("network forbidden")
        ):
            with self.assertRaises(PreparationError):
                validate_preparation(
                    "source-artifact",
                    self.fixtures["source-artifact"],
                    schemas,
                    policy=copy.deepcopy(self.policy),
                    prior_receipts={},
                    prior_states={},
                )
        schemas["source-artifact"] = {"type": "undefined"}
        with self.assertRaises(PreparationError):
            validate_preparation(
                "source-artifact",
                self.fixtures["source-artifact"],
                schemas,
                policy=copy.deepcopy(self.policy),
                prior_receipts={},
                prior_states={},
            )

    def test_calls_are_immutable_and_pure(self):
        before = json.dumps(self.fixtures, sort_keys=True)
        policy_before = json.dumps(self.policy, sort_keys=True)
        targets = [
            "builtins.open",
            "pathlib.Path.open",
            "pathlib.Path.read_text",
            "pathlib.Path.read_bytes",
            "pathlib.Path.write_text",
            "pathlib.Path.write_bytes",
            "os.getenv",
            "subprocess.run",
            "subprocess.Popen",
            "socket.socket",
            "urllib.request.urlopen",
        ]
        from contextlib import ExitStack

        with ExitStack() as stack:
            stack.enter_context(
                patch.object(
                    type(__import__("os").environ),
                    "__getitem__",
                    side_effect=AssertionError("environment forbidden"),
                )
            )
            for name in targets:
                stack.enter_context(
                    patch(name, side_effect=AssertionError("I/O forbidden"))
                )
            for kind, document in self.fixtures.items():
                receipt = self.validate(kind, document)
                self.assertFalse(receipt["deployed"])
                self.assertFalse(receipt["external_facts_verified"])
        self.assertEqual(before, json.dumps(self.fixtures, sort_keys=True))
        self.assertEqual(policy_before, json.dumps(self.policy, sort_keys=True))
