"""Fail-closed model registration against the pinned Open Notebook API contract."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.lib.ops.notebook_models import (
    ModelPolicy,
    PolicyError,
    apply_policy,
    atomic_write_receipt,
    load_policy,
    plan_policy,
    read_password_file,
    verify_policy,
)

POLICY = {
    "schema_version": 1,
    "target": "owned-isolated",
    "provider": {
        "name": "ollama",
        "credential_name": "P03 Local Ollama",
        "base_url": "http://ollama:11434",
        "modalities": ["language", "embedding"],
    },
    "models": [
        {"name": "gemma4:e2b", "type": "language", "default": "chat"},
        {
            "name": "embeddinggemma-2:740m",
            "type": "embedding",
            "dimensions": 768,
            "default": "embedding",
        },
    ],
}


class FakeClient:
    def __init__(self, credentials=None, models=None, defaults=None):
        self.credentials = list(credentials or [])
        self.models = list(models or [])
        self.defaults = dict(defaults or {})
        self.calls = []
        self.next_credential = 1
        self.next_model = 1

    def get(self, path):
        self.calls.append(("GET", path, None))
        if path == "/api/credentials?provider=ollama":
            return json.loads(json.dumps(self.credentials))
        if path == "/api/models":
            return json.loads(json.dumps(self.models))
        if path == "/api/models/defaults":
            return json.loads(json.dumps(self.defaults))
        raise AssertionError(path)

    def post(self, path, payload):
        self.calls.append(("POST", path, json.loads(json.dumps(payload))))
        if path == "/api/credentials":
            credential = {
                "id": f"credential:{self.next_credential}",
                "name": payload["name"],
                "provider": payload["provider"],
                "modalities": payload["modalities"],
                "base_url": payload["base_url"],
                "has_api_key": False,
                "model_count": 0,
                "created": "synthetic",
                "updated": "synthetic",
            }
            self.next_credential += 1
            self.credentials.append(credential)
            return dict(credential)
        prefix = "/api/credentials/"
        suffix = "/register-models"
        if path.startswith(prefix) and path.endswith(suffix):
            credential_id = path[len(prefix) : -len(suffix)]
            created = 0
            existing = 0
            for desired in payload["models"]:
                key = (desired["name"].casefold(), desired["model_type"].casefold())
                if any(
                    (m["name"].casefold(), m["type"].casefold()) == key
                    for m in self.models
                ):
                    existing += 1
                    continue
                self.models.append(
                    {
                        "id": f"model:{self.next_model}",
                        "name": desired["name"],
                        "provider": desired["provider"],
                        "type": desired["model_type"],
                        "credential": credential_id,
                        "created": "synthetic",
                        "updated": "synthetic",
                    }
                )
                self.next_model += 1
                created += 1
            return {"created": created, "existing": existing}
        raise AssertionError(path)

    def put(self, path, payload):
        self.calls.append(("PUT", path, json.loads(json.dumps(payload))))
        if path != "/api/models/defaults":
            raise AssertionError(path)
        self.defaults = {**self.defaults, **payload}
        return dict(self.defaults)


def exact_credential(credential_id="credential:1"):
    return {
        "id": credential_id,
        "name": "P03 Local Ollama",
        "provider": "ollama",
        "modalities": ["language", "embedding"],
        "base_url": "http://ollama:11434",
        "has_api_key": False,
        "model_count": 2,
        "created": "synthetic",
        "updated": "synthetic",
    }


def exact_models(credential_id="credential:1"):
    return [
        {
            "id": "model:chat",
            "name": "gemma4:e2b",
            "provider": "ollama",
            "type": "language",
            "credential": credential_id,
            "created": "synthetic",
            "updated": "synthetic",
        },
        {
            "id": "model:embedding",
            "name": "embeddinggemma-2:740m",
            "provider": "ollama",
            "type": "embedding",
            "credential": credential_id,
            "created": "synthetic",
            "updated": "synthetic",
        },
    ]


class ModelPolicyTests(unittest.TestCase):
    def test_public_fixture_is_the_reviewed_policy(self):
        fixture = (
            Path(__file__).resolve().parents[3]
            / "tests/fixtures/p03_models/notebook-model-policy.json"
        )

        self.assertEqual(json.loads(fixture.read_text(encoding="utf-8")), POLICY)

    def test_local_policy_selects_only_chat_and_embedding_defaults(self):
        policy = ModelPolicy.from_document(POLICY)

        self.assertEqual(policy.chat.name, "gemma4:e2b")
        self.assertEqual(policy.embedding.name, "embeddinggemma-2:740m")
        self.assertEqual(policy.embedding.dimensions, 768)
        self.assertEqual(policy.provider.base_url, "http://ollama:11434")

    def test_cloud_fallback_extra_models_and_wrong_dimensions_are_rejected(self):
        candidates = []
        for invalid_schema in (True, 1.0):
            invalid = json.loads(json.dumps(POLICY))
            invalid["schema_version"] = invalid_schema
            candidates.append(invalid)
        cloud = json.loads(json.dumps(POLICY))
        cloud["provider"]["base_url"] = "https://ollama.com"
        candidates.append(cloud)
        fallback = {**POLICY, "fallback": "cloud"}
        candidates.append(fallback)
        extra = json.loads(json.dumps(POLICY))
        extra["models"].append(
            {"name": "unexpected", "type": "language", "default": "chat"}
        )
        candidates.append(extra)
        dimension = json.loads(json.dumps(POLICY))
        dimension["models"][1]["dimensions"] = 1024
        candidates.append(dimension)
        for invalid_dimension in (768.0, True, float("nan")):
            candidate = json.loads(json.dumps(POLICY))
            candidate["models"][1]["dimensions"] = invalid_dimension
            candidates.append(candidate)
        wrong_chat = json.loads(json.dumps(POLICY))
        wrong_chat["models"][0]["name"] = "unselected-chat"
        candidates.append(wrong_chat)
        wrong_embedding = json.loads(json.dumps(POLICY))
        wrong_embedding["models"][1]["name"] = "unselected-embedding"
        candidates.append(wrong_embedding)
        for candidate in candidates:
            with self.subTest(candidate=candidate), self.assertRaises(PolicyError):
                ModelPolicy.from_document(candidate)

    def test_nondefault_local_ollama_listener_is_retained(self):
        candidate = json.loads(json.dumps(POLICY))
        candidate["provider"]["base_url"] = "http://ollama:22434"

        policy = ModelPolicy.from_document(candidate)

        self.assertEqual(policy.provider.base_url, "http://ollama:22434")

    def test_provider_credential_name_rejects_control_characters(self):
        for value in ("P03\x00Local", "P03\nLocal", "P03\x7fLocal"):
            candidate = json.loads(json.dumps(POLICY))
            candidate["provider"]["credential_name"] = value
            with self.subTest(value=repr(value)), self.assertRaises(PolicyError):
                ModelPolicy.from_document(candidate)

    def test_policy_loader_has_stable_fingerprint_and_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy_file = root / "policy.json"
            policy_file.write_text(json.dumps(POLICY))
            policy, fingerprint = load_policy(policy_file)
            self.assertEqual(policy.chat.name, "gemma4:e2b")
            self.assertRegex(fingerprint, r"^[0-9a-f]{64}$")
            link = root / "link.json"
            link.symlink_to(policy_file)
            with self.assertRaises(PolicyError):
                load_policy(link)

    def test_policy_loader_rejects_duplicate_json_members(self):
        with tempfile.TemporaryDirectory() as directory:
            policy_file = Path(directory) / "policy.json"
            body = json.dumps(POLICY)
            unique = '"base_url": "http://ollama:11434"'
            duplicate = unique + ', "base_url": "http://ollama:22434"'
            self.assertIn(unique, body)
            policy_file.write_text(body.replace(unique, duplicate))

            with self.assertRaisesRegex(PolicyError, "policy_file_invalid"):
                load_policy(policy_file)

    def test_policy_and_password_reject_symlinked_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            actual = root / "actual"
            actual.mkdir()
            policy_file = actual / "policy.json"
            policy_file.write_text(json.dumps(POLICY))
            password = actual / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            linked = root / "linked"
            linked.symlink_to(actual, target_is_directory=True)

            with self.assertRaisesRegex(PolicyError, "policy_file_refused"):
                load_policy(linked / "policy.json")
            with self.assertRaisesRegex(PolicyError, "password_file_refused"):
                read_password_file(linked / "password")

    def test_policy_and_password_reject_short_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy_file = root / "policy.json"
            policy_file.write_text(json.dumps(POLICY))
            with (
                patch("scripts.lib.ops.notebook_models.os.read", return_value=b"{}"),
                self.assertRaisesRegex(PolicyError, "policy_file_changed"),
            ):
                load_policy(policy_file)

            password = root / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            with (
                patch(
                    "scripts.lib.ops.notebook_models.os.read",
                    return_value=b"synthetic",
                ),
                self.assertRaisesRegex(PolicyError, "password_file_changed"),
            ):
                read_password_file(password)

    def test_password_file_requires_owner_only_regular_single_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            password = root / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            self.assertEqual(read_password_file(password), "synthetic-password")
            password.chmod(0o640)
            with self.assertRaises(PolicyError):
                read_password_file(password)
            password.chmod(0o600)
            password.write_text("first\nsecond\n")
            with self.assertRaises(PolicyError):
                read_password_file(password)
            link = root / "password-link"
            link.symlink_to(password)
            with self.assertRaises(PolicyError):
                read_password_file(link)

    def test_password_file_rejects_change_observed_after_read(self):
        with tempfile.TemporaryDirectory() as directory:
            password = Path(directory) / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            real_fstat = os.fstat
            calls = 0

            def changing_fstat(descriptor):
                nonlocal calls
                calls += 1
                observed = real_fstat(descriptor)
                if calls == 1:
                    return observed
                values = list(observed)
                values[6] += 1
                return os.stat_result(values)

            with (
                patch(
                    "scripts.lib.ops.notebook_models.os.fstat",
                    side_effect=changing_fstat,
                ),
                self.assertRaisesRegex(PolicyError, "password_file_changed"),
            ):
                read_password_file(password)

    def test_password_file_rejects_stable_change_between_lstat_and_open(self):
        with tempfile.TemporaryDirectory() as directory:
            password = Path(directory) / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            descriptor = os.open(password, os.O_RDONLY)
            try:
                observed = os.fstat(descriptor)
            finally:
                os.close(descriptor)
            values = list(observed)
            values[0] |= 0o040
            changed = os.stat_result(values)
            with (
                patch("scripts.lib.ops.notebook_models.os.fstat", return_value=changed),
                self.assertRaisesRegex(PolicyError, "password_file_changed"),
            ):
                read_password_file(password)

    def test_password_file_rejects_ctime_only_change_before_open(self):
        with tempfile.TemporaryDirectory() as directory:
            password = Path(directory) / "password"
            password.write_text("synthetic-password\n")
            password.chmod(0o600)
            observed = password.stat(follow_symlinks=False)
            changed = SimpleNamespace(
                **{
                    name: getattr(observed, name)
                    for name in (
                        "st_dev",
                        "st_ino",
                        "st_uid",
                        "st_gid",
                        "st_nlink",
                        "st_mode",
                        "st_size",
                        "st_mtime_ns",
                    )
                },
                st_ctime_ns=observed.st_ctime_ns + 1,
            )
            self.assertEqual(changed.st_size, observed.st_size)
            self.assertEqual(changed.st_mtime_ns, observed.st_mtime_ns)
            with (
                patch("scripts.lib.ops.notebook_models.os.fstat", return_value=changed),
                self.assertRaisesRegex(PolicyError, "password_file_changed"),
            ):
                read_password_file(password)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.policy = ModelPolicy.from_document(POLICY)

    def test_plan_is_read_only_and_reports_exact_actions(self):
        client = FakeClient(defaults={"default_tools_model": "model:keep"})
        receipt = plan_policy(self.policy, client, "a" * 64)
        self.assertEqual(
            receipt["actions"],
            ["create_credential", "register_models", "set_defaults"],
        )
        self.assertEqual([row[0] for row in client.calls], ["GET", "GET", "GET"])
        self.assertEqual(receipt["result"], "CHANGE_REQUIRED")
        self.assertNotIn("credential:", json.dumps(receipt))
        self.assertEqual(receipt["target_api_contract_version"], "1.15.0")
        self.assertFalse(receipt["api_version_observed"])
        self.assertNotIn("source_api_version", receipt)

    def test_wrong_case_model_tag_is_rejected_before_mutation(self):
        models = exact_models()
        models[0]["name"] = "GEMMA4:E2B"
        client = FakeClient(credentials=[exact_credential()], models=models)

        with self.assertRaisesRegex(PolicyError, "model_conflict"):
            apply_policy(self.policy, client, "f" * 64, owned_isolated=True)

        self.assertTrue(all(call[0] == "GET" for call in client.calls))

    def test_unicode_api_identifier_is_rejected_before_path_construction(self):
        credential = exact_credential("credential:café")
        client = FakeClient(credentials=[credential])

        with self.assertRaisesRegex(PolicyError, "api_shape_invalid"):
            plan_policy(self.policy, client, "e" * 64)

    def test_exact_registration_and_defaults_are_reused(self):
        credential = exact_credential()
        credential["modalities"] = ["embedding", "language"]
        client = FakeClient(
            credentials=[credential],
            models=exact_models(),
            defaults={
                "default_chat_model": "model:chat",
                "default_embedding_model": "model:embedding",
                "default_tools_model": "model:keep",
            },
        )
        receipt = verify_policy(self.policy, client, "b" * 64)
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["actions"], [])
        self.assertEqual(receipt["evidence"]["embedding_dimensions_policy"], 768)

    def test_conflicting_credential_or_model_association_is_rejected(self):
        wrong_credential = exact_credential()
        wrong_credential["base_url"] = "http://other:11434"
        wrong_model = exact_models("credential:other")
        for client in (
            FakeClient(credentials=[wrong_credential]),
            FakeClient(credentials=[exact_credential()], models=wrong_model),
            FakeClient(
                credentials=[exact_credential(), exact_credential("credential:2")]
            ),
        ):
            with self.subTest(calls=client.calls), self.assertRaises(PolicyError):
                plan_policy(self.policy, client, "c" * 64)
            self.assertTrue(all(call[0] == "GET" for call in client.calls))

    def test_apply_creates_exact_links_and_preserves_optional_defaults(self):
        client = FakeClient(
            defaults={
                "default_transformation_model": "model:transform",
                "default_tools_model": "model:tools",
            }
        )
        receipt = apply_policy(self.policy, client, "d" * 64, owned_isolated=True)
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(
            receipt["actions"],
            ["create_credential", "register_models", "set_defaults"],
        )
        self.assertEqual(client.defaults["default_tools_model"], "model:tools")
        mutations = [row for row in client.calls if row[0] != "GET"]
        self.assertEqual([row[0] for row in mutations], ["POST", "POST", "PUT"])
        create_payload = mutations[0][2]
        self.assertNotIn("api_key", create_payload)
        self.assertEqual(
            mutations[2][2].keys(),
            {
                "default_chat_model",
                "default_embedding_model",
            },
        )

    def test_apply_requires_owned_isolated_switch_before_any_mutation(self):
        client = FakeClient()
        with self.assertRaises(PolicyError):
            apply_policy(self.policy, client, "e" * 64, owned_isolated=False)
        self.assertEqual(client.calls, [])

    def test_apply_does_not_treat_registration_count_as_verification(self):
        class BrokenClient(FakeClient):
            def post(self, path, payload):
                if path.endswith("/register-models"):
                    self.calls.append(("POST", path, payload))
                    return {"created": 2, "existing": 0}
                return super().post(path, payload)

        client = BrokenClient()
        with self.assertRaises(PolicyError):
            apply_policy(self.policy, client, "f" * 64, owned_isolated=True)
        self.assertFalse(any(call[0] == "PUT" for call in client.calls))

    def test_apply_rejects_server_that_erases_an_optional_default(self):
        class DestructiveDefaultsClient(FakeClient):
            def put(self, path, payload):
                response = super().put(path, payload)
                self.defaults.pop("default_tools_model", None)
                return response

        client = DestructiveDefaultsClient(
            defaults={"default_tools_model": "model:preserved"}
        )
        with self.assertRaisesRegex(PolicyError, "optional_defaults_changed"):
            apply_policy(self.policy, client, "1" * 64, owned_isolated=True)

    def test_verify_rejects_missing_defaults_without_mutating(self):
        client = FakeClient(credentials=[exact_credential()], models=exact_models())
        with self.assertRaises(PolicyError):
            verify_policy(self.policy, client, "0" * 64)
        self.assertTrue(all(call[0] == "GET" for call in client.calls))

    def test_atomic_receipt_preserves_previous_on_failure_and_refuses_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = root / "receipt.json"
            receipt.write_text("previous")
            with (
                patch(
                    "scripts.lib.ops.notebook_models.os.replace",
                    side_effect=OSError("private detail"),
                ),
                self.assertRaises(PolicyError) as raised,
            ):
                atomic_write_receipt(receipt, {"result": "PASS"})
            self.assertEqual(receipt.read_text(), "previous")
            self.assertNotIn("private detail", str(raised.exception))
            self.assertEqual([item.name for item in root.iterdir()], ["receipt.json"])
            target = root / "target.json"
            target.write_text("target")
            link = root / "link.json"
            link.symlink_to(target)
            with self.assertRaises(PolicyError):
                atomic_write_receipt(link, {"result": "PASS"})

    def test_atomic_receipt_rejects_a_zero_length_write(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "receipt.json"
            with (
                patch("scripts.lib.ops.notebook_models.os.write", return_value=0),
                self.assertRaisesRegex(PolicyError, "receipt_write_failed"),
            ):
                atomic_write_receipt(receipt, {"result": "PASS"})
            self.assertFalse(receipt.exists())

    def test_partial_apply_is_resumable_without_duplicate_credential(self):
        class InterruptedClient(FakeClient):
            interrupted = True

            def post(self, path, payload):
                if path.endswith("/register-models") and self.interrupted:
                    self.interrupted = False
                    raise OSError("synthetic interruption")
                return super().post(path, payload)

        client = InterruptedClient()
        with self.assertRaises(OSError):
            apply_policy(self.policy, client, "2" * 64, owned_isolated=True)
        self.assertEqual(len(client.credentials), 1)

        receipt = apply_policy(self.policy, client, "2" * 64, owned_isolated=True)

        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(len(client.credentials), 1)


if __name__ == "__main__":
    unittest.main()
