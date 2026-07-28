from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "infra/tech-stack.versions.json"
HARDENING_CHECKER = ROOT / "scripts/hardening/check-all-hardening.sh"
REPOSITORY_CHECKER = ROOT / "scripts/validation/check-repo-contracts.sh"
DRIFT_COMPONENTS = (
    "Traefik",
    "Keycloak",
    "PostgreSQL",
    "Prometheus",
    "Alloy",
    "Ollama",
)
STALE_IMAGES = {
    "Traefik": "traefik:v3.7.6",
    "Keycloak": "quay.io/keycloak/keycloak:26.6.4-1",
    "Prometheus": "prom/prometheus:v3.13.0",
    "Alloy": "grafana/alloy:v1.17.1",
    "Ollama": "ollama/ollama:0.31.1",
}
IMAGE_LINE_RE = re.compile(r"(?m)^\s*image:\s*['\"]?([^'\"\s#]+)")
DEFAULT_IMAGE_RE = re.compile(r"\$\{[^}:]+:-([^}]+)\}")
LIFECYCLE_TERM_RE = re.compile(r"\b(?:legacy|deprecated)\b", re.IGNORECASE)
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
REGISTERED_LIFECYCLE_CONTEXTS = {
    "infra/06-observability/alloy/README.md": "migration",
    "infra/06-observability/grafana/dashboards/Infrastructure/neo4j.json": (
        "dashboard-label"
    ),
    "infra/06-observability/grafana/dashboards/Observability/loki-metrics.json": (
        "dashboard-label"
    ),
    "scripts/README.md": "historical",
    "scripts/operations/provider_surface_renderer.py": "migration",
    "scripts/security/generate-supply-chain-sample-service-summary.sh": "migration",
    "scripts/security/verify-sample-service-supply-chain.sh": "migration",
    "scripts/validation/agent_governance_contract.py": "migration",
    "scripts/validation/check-document-metadata.py": "migration",
    "scripts/validation/check-repo-contracts.sh": "migration",
    "scripts/validation/target_surface_contract.py": "migration",
    "tests/validation/test_agent_governance_contract.py": "negative-fixture",
    "tests/validation/test_document_corpus_lifecycle.py": "negative-fixture",
    "tests/validation/test_document_metadata.py": "negative-fixture",
    "tests/validation/test_provider_native_surfaces.py": "negative-fixture",
    "tests/validation/test_provider_surface_renderer.py": "negative-fixture",
    "tests/validation/test_sample_service_delivery_rehearsal.py": "negative-fixture",
    "tests/validation/test_target_surface_contracts.py": "negative-fixture",
    "tests/validation/test_tech_stack_version_contract.py": "negative-fixture",
}
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
    "docs/05.operations/guides/06-observability/alloy.md": (
        ("Alloy", "image"),
    ),
    "docs/05.operations/guides/06-observability/prometheus.md": (
        ("Prometheus", "image"),
    ),
    "docs/05.operations/policies/06-observability/alloy.md": (
        ("Alloy", "image"),
    ),
    "docs/05.operations/policies/06-observability/prometheus.md": (
        ("Prometheus", "image"),
    ),
    "docs/05.operations/runbooks/06-observability/alloy.md": (
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
                    images = entries[component]["images"]
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

    def test_hardening_checker_derives_dozzle_image_from_compose(self) -> None:
        text = HARDENING_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("image: amir20/dozzle:v10.6.7", text)
        self.assertNotIn("image: amir20/dozzle:v10.6.11", text)
        self.assertIn(
            'compose_service_image "$dozzle_compose" "dozzle" >/dev/null',
            text,
        )
        self.assertNotIn(
            'check_contains "$dozzle_compose" "image: ${dozzle_image}"',
            text,
        )

    def test_repository_checker_dozzle_diagnostic_uses_compose_version(
        self,
    ) -> None:
        text = REPOSITORY_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn(
            "Dozzle is declared as amir20/dozzle:v10.6.6",
            text,
        )
        self.assertIn(
            "Dozzle is declared as amir20/dozzle:v10.6.11",
            text,
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
                "services:\n"
                "  target:\n"
                "    image: [registry.example.test/team/app:1]\n"
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
                "services:\n"
                "  target:\n"
                "    image: 'registry.example.test/team/app:1\n"
            ),
            "unterminated-double-quote": (
                "services:\n"
                "  target:\n"
                '    image: "registry.example.test/team/app:1\n'
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
                (
                    "services:\n"
                    "  target:\n"
                    "    image: registry.example.test/team/app:1\n"
                ),
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

    def test_lifecycle_terms_have_registered_preserve_contexts(self) -> None:
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
        occurrence_paths = {
            relative.decode()
            for relative in tracked
            if relative
            and b"\0" not in (ROOT / relative.decode()).read_bytes()
            and LIFECYCLE_TERM_RE.search(
                (ROOT / relative.decode()).read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            )
        }

        self.assertEqual(set(REGISTERED_LIFECYCLE_CONTEXTS), occurrence_paths)
        self.assertEqual(
            (),
            lifecycle_classification_findings(REGISTERED_LIFECYCLE_CONTEXTS),
        )

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
