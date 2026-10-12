"""Focused public SMTP source validation regressions."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.lib.ops import smtp_public_source
from scripts.lib.ops.smtp_contract import (
    CANONICAL,
    CANONICAL_PATH,
    OLD,
    OLD_PATH,
    ContractError,
    grants,
)


def _common(root: Path, *, body=None) -> Path:
    path = root / smtp_public_source.LAB_COMMON_EXTENDS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            body
            or {
                "services": {
                    "template-infra-med": {
                        "init": True,
                        "labels": {"hy-home.managed": "true"},
                    }
                }
            }
        )
    )
    return path


def _entrypoint() -> list[str]:
    return [
        "/bin/sh",
        "-ec",
        """fail() { echo 'SMTP secret input rejected' >&2; exit 1; }
[ "$${GOTRUE_SMTP_PASS+x}" != x ] || fail
[ -n "$${GOTRUE_SMTP_PASS_FILE:-}" ] || fail
[ -f "$$GOTRUE_SMTP_PASS_FILE" ] && [ -r "$$GOTRUE_SMTP_PASS_FILE" ] && [ -s "$$GOTRUE_SMTP_PASS_FILE" ] || fail
GOTRUE_SMTP_PASS="$$(cat "$$GOTRUE_SMTP_PASS_FILE" 2>/dev/null)" || fail
[ -n "$$GOTRUE_SMTP_PASS" ] || fail
export GOTRUE_SMTP_PASS
[ "$$#" -gt 0 ] || fail
exec "$$@"
""",
        "--",
    ]


def _lab(root: Path, *, auth_overrides=None, text=None) -> Path:
    path = root / smtp_public_source.LAB_SUPABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if text is not None:
        path.write_text(text)
        return path
    auth = {
        "profiles": ["supabase"],
        "extends": {
            "file": "../infra/common-optimizations.yml",
            "service": "template-infra-med",
        },
        "image": "supabase/gotrue:v2.197.0",
        "labels": {"hy-home.tier": "lab"},
        "entrypoint": _entrypoint(),
        "command": ["auth"],
        "secrets": [{"source": CANONICAL, "target": OLD}],
        "environment": {"GOTRUE_SMTP_PASS_FILE": "/run/secrets/supabase_smtp_password"},
    }
    if auth_overrides:
        auth.update(auth_overrides)
    path.write_text(
        yaml.safe_dump(
            {
                "name": "hy-home-lab-supabase",
                "secrets": {CANONICAL: {"file": "../" + CANONICAL_PATH}},
                "services": {"auth": auth},
            }
        )
    )
    return path


def _validate(root: Path):
    return smtp_public_source.validate_lab_sources(
        root,
        canonical=CANONICAL,
        canonical_path=CANONICAL_PATH,
        old=OLD,
        old_path=OLD_PATH,
        grants=grants,
        error=ContractError,
    )


class SMTPPublicSourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def test_valid_lab_hashes_include_fixed_common_parent(self):
        lab = _lab(self.root)
        common = _common(self.root)
        hashes, present = _validate(self.root)
        self.assertTrue(present)
        self.assertEqual(
            set(hashes),
            {str(lab.relative_to(self.root)), str(common.relative_to(self.root))},
        )

    def test_duplicate_shadow_target_rejects_auth_grants(self):
        _common(self.root)
        _lab(
            self.root,
            auth_overrides={
                "secrets": [
                    {"source": CANONICAL, "target": OLD},
                    {"source": "other_secret", "target": OLD},
                ]
            },
        )
        with self.assertRaises(ContractError):
            _validate(self.root)

    def test_duplicate_yaml_keys_reject_before_shape_validation(self):
        _common(self.root)
        _lab(self.root, text="name: hy-home-lab-supabase\nname: other\nservices: {}\n")
        with self.assertRaises(ContractError):
            _validate(self.root)

    def test_recursive_yaml_rejects_as_contract_error(self):
        _common(self.root)
        _lab(
            self.root,
            text="name: hy-home-lab-supabase\nsecrets: &loop [*loop]\nservices: {}\n",
        )
        with self.assertRaises(ContractError):
            _validate(self.root)

    def test_oversized_public_source_rejects_before_parse(self):
        _common(self.root)
        path = self.root / smtp_public_source.LAB_SUPABASE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("name: hy-home-lab-supabase\n" + ("# filler\n" * 40000))
        with self.assertRaises(ContractError):
            _validate(self.root)

    def test_committed_lab_with_untracked_common_parent_rejects(self):
        _lab(self.root)
        _common(self.root)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "add", "--", smtp_public_source.LAB_SUPABASE_PATH],
            cwd=self.root,
            check=True,
        )
        with self.assertRaises(ContractError):
            _validate(self.root)


class SMTPRootPublicSourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "infra").mkdir()
        (self.root / "docker-compose.yml").write_text(
            yaml.safe_dump(
                {
                    "include": ["infra/auth.yml"],
                    "secrets": {CANONICAL: {"file": CANONICAL_PATH}},
                }
            )
        )
        (self.root / "infra/auth.yml").write_text(
            yaml.safe_dump(
                {
                    "services": {
                        "auth": {"secrets": [{"source": CANONICAL, "target": OLD}]}
                    }
                }
            )
        )

    def _source_documents(self):
        hashes, documents, _resolved_images = smtp_public_source.source_documents(
            self.root,
            canonical=CANONICAL,
            canonical_path=CANONICAL_PATH,
            old=OLD,
            old_path=OLD_PATH,
            grants=grants,
            error=ContractError,
        )
        return hashes, documents

    def test_root_source_documents_hash_tracked_include_graph(self):
        hashes, documents = self._source_documents()
        self.assertEqual(set(hashes), {"docker-compose.yml", "infra/auth.yml"})
        self.assertEqual(len(documents), 2)

    def test_root_source_documents_reject_untracked_include_in_git_root(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "add", "--", "docker-compose.yml"], cwd=self.root, check=True
        )
        with self.assertRaises(ContractError):
            self._source_documents()

    def test_root_source_documents_reject_private_include_before_read(self):
        private = self.root / "secrets/private.yml"
        private.parent.mkdir()
        private.write_text("not: public\n")
        root = yaml.safe_load((self.root / "docker-compose.yml").read_text())
        root["include"] = ["secrets/private.yml"]
        (self.root / "docker-compose.yml").write_text(yaml.safe_dump(root))
        with self.assertRaises(ContractError):
            self._source_documents()

    def test_root_source_documents_reject_alias_escape_symlink_and_unexpected_include(
        self,
    ):
        cases = ("escape", "symlink", "unexpected_type")
        for case in cases:
            with self.subTest(case=case):
                self.setUp()
                root = yaml.safe_load((self.root / "docker-compose.yml").read_text())
                if case == "escape":
                    root["include"] = ["../escape.yml"]
                elif case == "symlink":
                    include = self.root / "infra/auth.yml"
                    include.unlink()
                    include.symlink_to(self.root / "docker-compose.yml")
                else:
                    root["include"] = [{}]
                (self.root / "docker-compose.yml").write_text(yaml.safe_dump(root))
                with self.assertRaises(ContractError):
                    self._source_documents()

    def test_root_source_documents_include_cycle_hashes_once(self):
        (self.root / "infra/auth.yml").write_text(
            yaml.safe_dump(
                {
                    "include": ["../docker-compose.yml"],
                    "services": {
                        "auth": {"secrets": [{"source": CANONICAL, "target": OLD}]}
                    },
                }
            )
        )
        hashes, documents = self._source_documents()
        self.assertEqual(set(hashes), {"docker-compose.yml", "infra/auth.yml"})
        self.assertEqual(len(documents), 2)


class SMTPRootExtendsSourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "infra").mkdir()
        (self.root / "docker-compose.yml").write_text(
            yaml.safe_dump({"include": ["infra/service.yml"]})
        )
        (self.root / "infra/service.yml").write_text(
            yaml.safe_dump(
                {
                    "services": {
                        "app": {
                            "extends": {
                                "file": "parent.yml",
                                "service": "template-auth",
                            }
                        }
                    }
                }
            )
        )
        (self.root / "infra/parent.yml").write_text(
            yaml.safe_dump({"services": {"template-auth": {"image": "example/app:1"}}})
        )

    def _source_documents(self):
        hashes, documents, _resolved_images = smtp_public_source.source_documents(
            self.root,
            canonical=CANONICAL,
            canonical_path=CANONICAL_PATH,
            old=OLD,
            old_path=OLD_PATH,
            grants=grants,
            error=ContractError,
        )
        return hashes, documents

    def test_root_extends_parent_file_is_hashed(self):
        hashes, documents = self._source_documents()
        self.assertIn("infra/parent.yml", hashes)
        self.assertEqual(3, len(documents))

    def test_root_extends_parent_must_be_tracked_in_git_root(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "add", "--", "docker-compose.yml", "infra/service.yml"],
            cwd=self.root,
            check=True,
        )
        with self.assertRaises(ContractError):
            self._source_documents()

    def test_root_extends_parent_symlink_escape_and_cycle_reject(self):
        cases = ("symlink", "escape", "cycle")
        for case in cases:
            with self.subTest(case=case):
                self.setUp()
                service = yaml.safe_load((self.root / "infra/service.yml").read_text())
                if case == "symlink":
                    parent = self.root / "infra/parent.yml"
                    target = self.root / "infra/parent-real.yml"
                    target.write_text(parent.read_text())
                    parent.unlink()
                    parent.symlink_to(target)
                elif case == "escape":
                    service["services"]["app"]["extends"]["file"] = (
                        "../secrets/private.yml"
                    )
                    private = self.root / "secrets/private.yml"
                    private.parent.mkdir()
                    private.write_text("services: {}\n")
                    (self.root / "infra/service.yml").write_text(
                        yaml.safe_dump(service)
                    )
                else:
                    service["services"]["app"]["extends"] = {"service": "app"}
                    (self.root / "infra/service.yml").write_text(
                        yaml.safe_dump(service)
                    )
                with self.assertRaises(ContractError):
                    self._source_documents()

    def test_unused_parent_auth_alias_does_not_satisfy_selected_root_auth(self):
        parent = self.root / "infra/parent.yml"
        service = yaml.safe_load((self.root / "infra/service.yml").read_text())
        service["services"]["app"]["extends"]["service"] = "template-app"
        (self.root / "infra/service.yml").write_text(yaml.safe_dump(service))
        parent.write_text(
            yaml.safe_dump(
                {
                    "services": {
                        "template-app": {"image": "example/app:1"},
                        "auth": {"secrets": [{"source": CANONICAL, "target": OLD}]},
                    }
                }
            )
        )
        hashes, documents, resolved = smtp_public_source.source_documents(
            self.root,
            canonical=CANONICAL,
            canonical_path=CANONICAL_PATH,
            old=OLD,
            old_path=OLD_PATH,
            grants=grants,
            error=ContractError,
        )
        self.assertIn("infra/parent.yml", hashes)
        self.assertEqual(("example/app:1",), resolved["images"])
        with self.assertRaisesRegex(ContractError, "auth_alias_missing"):
            smtp_public_source.validate_root_documents(
                documents,
                require_auth=True,
                canonical=CANONICAL,
                canonical_path=CANONICAL_PATH,
                old=OLD,
                old_path=OLD_PATH,
                grants=grants,
                unify=lambda document: document,
                error=ContractError,
                selected_auth_alias=False,
            )

    def test_child_image_override_masks_parent_gotrue(self):
        parent = self.root / "infra/parent.yml"
        parent.write_text(
            yaml.safe_dump(
                {"services": {"template-auth": {"image": "supabase/gotrue:v2.197.0"}}}
            )
        )
        service = yaml.safe_load((self.root / "infra/service.yml").read_text())
        service["services"]["app"]["image"] = "example/app:1"
        (self.root / "infra/service.yml").write_text(yaml.safe_dump(service))
        _hashes, documents, resolved = smtp_public_source.source_documents(
            self.root,
            canonical=CANONICAL,
            canonical_path=CANONICAL_PATH,
            old=OLD,
            old_path=OLD_PATH,
            grants=grants,
            error=ContractError,
        )
        self.assertEqual(("example/app:1",), resolved["images"])
        self.assertFalse(
            smtp_public_source.has_root_gotrue_service(documents, resolved)
        )

    def test_docker_hub_qualified_gotrue_images_are_forbidden(self):
        for image in (
            "supabase/gotrue:v2.197.0",
            "docker.io/supabase/gotrue:v2.197.0",
            "index.docker.io/supabase/gotrue:v2.197.0",
            "ghcr.io/supabase/gotrue:v2.197.0",
            "ghcr.io/example/gotrue@sha256:synthetic",
            "${GOTRUE_IMAGE}",
        ):
            with self.subTest(image=image):
                self.assertTrue(
                    smtp_public_source.has_root_gotrue_service([], {"images": (image,)})
                )


if __name__ == "__main__":
    unittest.main()
