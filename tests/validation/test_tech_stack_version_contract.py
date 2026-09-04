from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile
import unittest

from scripts.lib.gate.ci_gate_contract import load_public_suite_registry
from tests.lib.gate.subprocess_support import gate_root_pass_fds


ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "infra/tech-stack.versions.json"
HARDENING_CHECKER = ROOT / "scripts/hardening/check-all-hardening.sh"
OAUTH_DOCKERFILE = ROOT / "infra/02-auth/oauth2-proxy/Dockerfile"
OAUTH_DEV_DOCKERFILE = ROOT / "infra/02-auth/oauth2-proxy/dev.Dockerfile"
MANIFEST_PATH = ROOT / "scripts/manifest.yaml"
SUPPLY_CHAIN_SUMMARY_GENERATOR = (
    ROOT / "scripts/security/generate-supply-chain-sample-service-summary.sh"
)
DOZZLE_COMPOSE = ROOT / "infra/11-laboratory/dozzle/docker-compose.yml"
DRIFT_COMPONENTS = (
    "Traefik",
    "Keycloak",
    "PostgreSQL",
    "Prometheus",
    "Alloy",
    "Ollama",
)
STALE_IMAGES = {
    "Traefik": "traefik:v3.7.8",
    "Keycloak": "quay.io/keycloak/keycloak:26.7.0-0",
    "Prometheus": "prom/prometheus:v3.13.1",
    "Alloy": "grafana/alloy:v1.18.0",
    "Ollama": "ollama/ollama:0.32.1",
    "Dozzle": "amir20/dozzle:v10.6.11",
}
IMAGE_LINE_RE = re.compile(r"(?m)^\s*image:\s*['\"]?([^'\"\s#]+)")
DEFAULT_IMAGE_RE = re.compile(r"\$\{[^}:]+:-([^}]+)\}")
PRESERVED_LIFECYCLE_CONTEXTS = frozenset(
    {
        "historical",
        "incident",
        "migration",
        "archive",
        "dashboard-label",
        "negative-fixture",
    }
)
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
DIRECT_CURRENT_DOCS = {
    "infra/01-gateway/README.md": (("Traefik", "tag"),),
    "infra/02-auth/keycloak/README.md": (("Keycloak", "image"),),
    "infra/06-observability/README.md": (
        ("Prometheus", "tag"),
        ("Alloy", "tag"),
    ),
    "infra/06-observability/alloy/README.md": (("Alloy", "tag"),),
    "infra/06-observability/prometheus/README.md": (("Prometheus", "tag"),),
    "infra/06-observability/pushgateway/README.md": (("Prometheus", "tag"),),
    "infra/06-observability/pyroscope/README.md": (("Alloy", "tag"),),
    "infra/06-observability/tempo/README.md": (("Alloy", "tag"),),
    "infra/08-ai/README.md": (("Ollama", "image"),),
    "infra/11-laboratory/dozzle/README.md": (("Dozzle", "tag"),),
    "docs/05.operations/catalog/06-observability/0040-alloy/guide.md": (
        ("Alloy", "image"),
    ),
    "docs/05.operations/catalog/06-observability/0045-prometheus/guide.md": (
        ("Prometheus", "image"),
    ),
    "docs/05.operations/catalog/06-observability/0040-alloy/policy.md": (
        ("Alloy", "image"),
    ),
    "docs/05.operations/catalog/06-observability/0045-prometheus/policy.md": (
        ("Prometheus", "image"),
    ),
    "docs/05.operations/catalog/06-observability/0040-alloy/runbook.md": (
        ("Alloy", "image"),
    ),
}


def declared_images(path: pathlib.Path) -> set[str]:
    images: set[str] = set()
    for match in IMAGE_LINE_RE.finditer(path.read_text(encoding="utf-8")):
        raw_image = match.group(1)
        images.add(raw_image)
        default_match = DEFAULT_IMAGE_RE.search(raw_image)
        if default_match:
            images.add(default_match.group(1))
    return images


def lifecycle_classification_findings(
    classifications: dict[str, str],
    *,
    active_obsolete_paths: frozenset[str] = frozenset(),
) -> tuple[str, ...]:
    findings: list[str] = []
    for path, context in sorted(classifications.items()):
        if path in active_obsolete_paths:
            findings.append(f"{path}: registered active obsolete implementation")
        elif context not in PRESERVED_LIFECYCLE_CONTEXTS:
            findings.append(f"{path}: unclassified lifecycle context {context}")
    return tuple(findings)


def direct_current_document_version_findings(
    text: str,
    *,
    current: str,
    stale: str,
) -> tuple[str, ...]:
    findings: list[str] = []
    if current not in text:
        findings.append("current version absent")
    if stale in text:
        findings.append("stale version present")
    return tuple(findings)


class TechStackVersionContractTests(unittest.TestCase):
    @staticmethod
    def registry_entries() -> dict[str, dict[str, object]]:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return {entry["component"]: entry for entry in registry["entries"]}

    def test_supply_chain_summary_is_fresh(self) -> None:
        completed = subprocess.run(
            ["bash", str(SUPPLY_CHAIN_SUMMARY_GENERATOR), "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            pass_fds=gate_root_pass_fds(ROOT),
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    @staticmethod
    def run_compose_image_resolver_path(
        compose_path: pathlib.Path,
        service: str = "target",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "bash",
                str(HARDENING_CHECKER),
                "--resolve-compose-service-image",
                str(compose_path),
                service,
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            pass_fds=gate_root_pass_fds(ROOT),
        )

    @classmethod
    def run_compose_image_resolver(
        cls,
        compose_text: str,
        service: str = "target",
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            compose_path = pathlib.Path(temporary_directory) / "compose.yml"
            compose_path.write_text(compose_text, encoding="utf-8")
            return cls.run_compose_image_resolver_path(compose_path, service)

    def test_registry_matches_compose_image_declarations(self) -> None:
        entries = {
            component: entry
            for component, entry in self.registry_entries().items()
            if component in DRIFT_COMPONENTS
        }
        self.assertEqual(set(DRIFT_COMPONENTS), set(entries))

        for component in DRIFT_COMPONENTS:
            with self.subTest(component=component):
                entry = entries[component]
                compose_images: set[str] = set()
                for compose_file in entry["compose_files"]:
                    compose_images.update(declared_images(ROOT / compose_file))

                registry_images = set(entry["images"])
                registry_repositories = {
                    image.rsplit(":", 1)[0] for image in registry_images
                }
                matching_compose_images = {
                    image
                    for image in compose_images
                    if image.rsplit(":", 1)[0] in registry_repositories
                }
                self.assertTrue(
                    registry_images <= compose_images,
                    (
                        f"{component}: registry={sorted(registry_images)} "
                        f"compose={sorted(matching_compose_images)}"
                    ),
                )

    def test_direct_current_docs_use_registry_versions(self) -> None:
        entries = self.registry_entries()
        for relative_path, expectations in DIRECT_CURRENT_DOCS.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            for component, representation in expectations:
                with self.subTest(path=relative_path, component=component):
                    images = (
                        sorted(declared_images(DOZZLE_COMPOSE))
                        if component == "Dozzle"
                        else entries[component]["images"]
                    )
                    self.assertEqual(1, len(images))
                    image = images[0]
                    expected = (
                        image if representation == "image" else image.rsplit(":", 1)[1]
                    )
                    stale_image = STALE_IMAGES[component]
                    stale = (
                        stale_image
                        if representation == "image"
                        else stale_image.rsplit(":", 1)[1]
                    )
                    self.assertEqual(
                        (),
                        direct_current_document_version_findings(
                            text,
                            current=expected,
                            stale=stale,
                        ),
                    )

    def test_direct_current_document_rejects_stale_and_current_versions(
        self,
    ) -> None:
        self.assertEqual(
            ("stale version present",),
            direct_current_document_version_findings(
                "canonical:v2\nstale:v1\n",
                current="canonical:v2",
                stale="stale:v1",
            ),
        )

    def test_hardening_checker_has_no_independent_stale_keycloak_literal(self) -> None:
        text = HARDENING_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("quay.io/keycloak/keycloak:26.6.4-1", text)
        self.assertIn("infra/tech-stack.versions.json", text)
        self.assertIn(
            (
                'keycloak_compose_image="$(compose_service_image '
                '"$keycloak_compose" "keycloak")"'
            ),
            text,
        )
        self.assertIn(
            '[[ "$keycloak_compose_image" != "$keycloak_image" ]]',
            text,
        )
        self.assertNotIn(
            'check_contains "$keycloak_compose" "image: ${keycloak_image}"',
            text,
        )

    def test_oauth2_proxy_production_numeric_identity_contract(self) -> None:
        dockerfile = OAUTH_DOCKERFILE.read_text(encoding="utf-8")
        dev_dockerfile = OAUTH_DEV_DOCKERFILE.read_text(encoding="utf-8")
        checker = HARDENING_CHECKER.read_text(encoding="utf-8")

        for expected in (
            "addgroup -S -g 101 oauth2proxy",
            "adduser -S -D -H -u 100 -s /sbin/nologin -G oauth2proxy oauth2proxy",
            "USER 100:101",
        ):
            self.assertIn(expected, dockerfile)
            self.assertIn(expected, checker)
        self.assertNotIn("USER oauth2proxy:oauth2proxy", dockerfile)
        self.assertIn("USER oauth2proxy:oauth2proxy", dev_dockerfile)
        self.assertIn(
            'check_contains "$oauth_dev_dockerfile" "USER oauth2proxy:oauth2proxy"',
            checker,
        )

    def test_hardening_checker_derives_dozzle_image_from_compose(self) -> None:
        text = HARDENING_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("image: amir20/dozzle:v10.6.7", text)
        self.assertNotIn("image: amir20/dozzle:v10.6.11", text)
        self.assertIn(
            (
                'dozzle_compose_image="$(compose_service_image '
                '"$dozzle_compose" "dozzle")"'
            ),
            text,
        )
        self.assertIn(
            '[[ "$dozzle_compose_image" != "$dozzle_image" ]]',
            text,
        )

    def test_public_operations_suite_owns_hardening_version_validation(
        self,
    ) -> None:
        registry = load_public_suite_registry(MANIFEST_PATH)
        operations = next(
            suite for suite in registry.suites if suite.name == "operations"
        )
        self.assertEqual(
            1,
            operations.validators.count(
                pathlib.PurePosixPath(
                    "scripts/lib/ops/rehearse-postgres-logical-upgrade.sh"
                )
            ),
        )
        repository_integrity = next(
            suite for suite in registry.suites if suite.name == "repository-integrity"
        )
        self.assertEqual(
            1,
            repository_integrity.validators.count(
                pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh")
            ),
        )

    def test_compose_image_resolver_accepts_exact_safe_scalars(self) -> None:
        expected = "registry.example.test/team/app:1.2.3"
        for label, scalar in (
            ("unquoted", expected),
            ("single-quoted", f"'{expected}'"),
            ("double-quoted", f'"{expected}"'),
        ):
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    f"services:\n  target:\n    image: {scalar}\n"
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(f"{expected}\n", result.stdout)
                self.assertEqual("", result.stderr)

    def test_compose_image_resolver_accepts_quoted_service_keys(self) -> None:
        expected = "registry.example.test/team/app:1.2.3"
        for label, service_key in (
            ("single-quoted", "'target'"),
            ("double-quoted", '"target"'),
        ):
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    f"services:\n  {service_key}:\n    image: {expected}\n"
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(f"{expected}\n", result.stdout)
                self.assertEqual("", result.stderr)

    def test_compose_image_resolver_stops_at_quoted_sibling_service(
        self,
    ) -> None:
        expected = "registry.example.test/team/app:1.2.3"
        for label, sibling_key in (
            ("single-quoted", "'other'"),
            ("double-quoted", '"other"'),
        ):
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    (
                        "services:\n"
                        "  target:\n"
                        f"    image: {expected}\n"
                        f"  {sibling_key}:\n"
                        "    image: registry.example.test/team/other:9\n"
                    )
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(f"{expected}\n", result.stdout)
                self.assertEqual("", result.stderr)

    def test_compose_image_resolver_rejects_quoted_sibling_image_theft(
        self,
    ) -> None:
        for label, sibling_key in (
            ("single-quoted", "'other'"),
            ("double-quoted", '"other"'),
        ):
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    (
                        "services:\n"
                        "  target:\n"
                        "    restart: unless-stopped\n"
                        f"  {sibling_key}:\n"
                        "    image: registry.example.test/team/other:9\n"
                    )
                )
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    "FAIL: invalid compose service image contract\n",
                    result.stderr,
                )

    def test_compose_image_resolver_rejects_duplicate_quoted_target_keys(
        self,
    ) -> None:
        duplicate_pairs = (
            ("unquoted-single", "target", "'target'"),
            ("unquoted-double", "target", '"target"'),
            ("single-unquoted", "'target'", "target"),
            ("double-unquoted", '"target"', "target"),
            ("single-double", "'target'", '"target"'),
            ("double-single", '"target"', "'target'"),
        )
        for label, first_key, second_key in duplicate_pairs:
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    (
                        "services:\n"
                        f"  {first_key}:\n"
                        "    image: registry.example.test/team/app:1\n"
                        f"  {second_key}:\n"
                        "    image: registry.example.test/team/app:2\n"
                    )
                )
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    "FAIL: invalid compose service image contract\n",
                    result.stderr,
                )

    def test_compose_image_resolver_rejects_duplicate_sibling_service_names(
        self,
    ) -> None:
        duplicate_pairs = (
            ("unquoted-single", "other", "'other'"),
            ("single-unquoted", "'other'", "other"),
            ("unquoted-double", "other", '"other"'),
            ("double-unquoted", '"other"', "other"),
        )
        for label, first_key, second_key in duplicate_pairs:
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(
                    (
                        "services:\n"
                        "  target:\n"
                        "    image: registry.example.test/team/app:1\n"
                        f"  {first_key}:\n"
                        "    image: registry.example.test/team/other:1\n"
                        f"  {second_key}:\n"
                        "    image: registry.example.test/team/other:2\n"
                    )
                )
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    "FAIL: invalid compose service image contract\n",
                    result.stderr,
                )

    def test_compose_image_resolver_rejects_ambiguous_or_unsafe_yaml(
        self,
    ) -> None:
        payload_marker = "PAYLOAD_SHOULD_NOT_BE_ECHOED"
        invalid_fixtures = {
            "duplicate-top-level-services": (
                "services:\n"
                "  target:\n"
                "    image: registry.example.test/team/app:1\n"
                "services:\n"
                "  other:\n"
                "    image: registry.example.test/team/other:1\n"
            ),
            "duplicate-target-service": (
                "services:\n"
                "  target:\n"
                "    image: registry.example.test/team/app:1\n"
                "  target:\n"
                "    image: registry.example.test/team/app:2\n"
            ),
            "duplicate-image": (
                "services:\n"
                "  target:\n"
                "    image: registry.example.test/team/app:1\n"
                "    image: registry.example.test/team/app:2\n"
            ),
            "missing-image": "services:\n  target:\n    restart: unless-stopped\n",
            "malformed-trailing-token": (
                "services:\n"
                "  target:\n"
                "    image: registry.example.test/team/app:1 trailing\n"
            ),
            "mapping-image": (
                "services:\n"
                "  target:\n"
                "    image: {repository: registry.example.test/team/app, tag: 1}\n"
            ),
            "list-image": (
                "services:\n"
                "  target:\n"
                "    image:\n"
                "      - registry.example.test/team/app:1\n"
            ),
            "explicit-list-image": (
                "services:\n  target:\n    image: [registry.example.test/team/app:1]\n"
            ),
            "non-scalar-image": "services:\n  target:\n    image: null\n",
            "unsafe-image": (
                "services:\n"
                "  target:\n"
                f"    image: registry.example.test/team/app:1;{payload_marker}\n"
            ),
            "unsafe-quoted-image": (
                "services:\n"
                "  target:\n"
                f'    image: "registry.example.test/team/app:1$({payload_marker})"\n'
            ),
            "unterminated-single-quote": (
                "services:\n  target:\n    image: 'registry.example.test/team/app:1\n"
            ),
            "unterminated-double-quote": (
                'services:\n  target:\n    image: "registry.example.test/team/app:1\n'
            ),
        }
        for label, compose_text in invalid_fixtures.items():
            with self.subTest(label=label):
                result = self.run_compose_image_resolver(compose_text)
                self.assertEqual(2, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual(
                    "FAIL: invalid compose service image contract\n",
                    result.stderr,
                )
                self.assertNotIn(
                    payload_marker,
                    result.stdout + result.stderr,
                )

    def test_compose_image_resolver_rejects_unsafe_file_types_and_size(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = pathlib.Path(temporary_directory)
            regular_path = temporary_root / "regular.yml"
            regular_path.write_text(
                ("services:\n  target:\n    image: registry.example.test/team/app:1\n"),
                encoding="utf-8",
            )
            symlink_path = temporary_root / "symlink.yml"
            symlink_path.symlink_to(regular_path)
            directory_path = temporary_root / "directory"
            directory_path.mkdir()
            oversized_path = temporary_root / "oversized.yml"
            oversized_path.write_bytes(b"#" * (1024 * 1024 + 1))

            for label, fixture_path in (
                ("symlink", symlink_path),
                ("directory", directory_path),
                ("oversized", oversized_path),
            ):
                with self.subTest(label=label):
                    result = self.run_compose_image_resolver_path(fixture_path)
                    self.assertEqual(2, result.returncode)
                    self.assertEqual("", result.stdout)
                    self.assertEqual(
                        "FAIL: invalid compose service image contract\n",
                        result.stderr,
                    )

    def test_post_deletion_scan_reads_only_current_files(self) -> None:
        tracked = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                *TARGET_ROOTS,
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
        current_paths = {
            relative.decode()
            for relative in tracked
            if relative and (ROOT / relative.decode()).is_file()
        }
        self.assertTrue(
            {
                "scripts/hooks/patch-graphify-post-commit.sh",
                "scripts/knowledge/generate-llm-wiki-coverage.sh",
                "scripts/knowledge/generate-llm-wiki-index.sh",
                "scripts/validation/check-repo-contracts.sh",
                "scripts/validation/recommend-gap-routing.sh",
                "scripts/validation/recommend-qa-gates.sh",
            }.isdisjoint(current_paths)
        )
        for relative in current_paths:
            (ROOT / relative).read_bytes()

    def test_lifecycle_context_policy_preserves_evidence_categories(self) -> None:
        classifications = {
            f"fixture/{context}.txt": context
            for context in PRESERVED_LIFECYCLE_CONTEXTS
        }
        self.assertEqual((), lifecycle_classification_findings(classifications))

    def test_registered_active_obsolete_implementation_fails_classification(
        self,
    ) -> None:
        path = "infra/example/obsolete-implementation.conf"
        findings = lifecycle_classification_findings(
            {path: "migration"},
            active_obsolete_paths=frozenset({path}),
        )
        self.assertEqual(
            (f"{path}: registered active obsolete implementation",),
            findings,
        )


if __name__ == "__main__":
    unittest.main()
