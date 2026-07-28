from __future__ import annotations

import json
import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "infra/tech-stack.versions.json"
HARDENING_CHECKER = ROOT / "scripts/hardening/check-all-hardening.sh"
DRIFT_COMPONENTS = (
    "Traefik",
    "Keycloak",
    "PostgreSQL",
    "Prometheus",
    "Alloy",
    "Ollama",
)
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


class TechStackVersionContractTests(unittest.TestCase):
    @staticmethod
    def registry_entries() -> dict[str, dict[str, object]]:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return {entry["component"]: entry for entry in registry["entries"]}

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
                    self.assertIn(expected, text)

    def test_hardening_checker_has_no_independent_stale_keycloak_literal(self) -> None:
        text = HARDENING_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("quay.io/keycloak/keycloak:26.6.4-1", text)
        self.assertIn("infra/tech-stack.versions.json", text)

    def test_hardening_checker_derives_dozzle_image_from_compose(self) -> None:
        text = HARDENING_CHECKER.read_text(encoding="utf-8")
        self.assertNotIn("image: amir20/dozzle:v10.6.7", text)
        self.assertNotIn("image: amir20/dozzle:v10.6.11", text)
        self.assertIn(
            'dozzle_image="$(compose_service_image "$dozzle_compose" "dozzle")"',
            text,
        )
        self.assertIn(
            'check_contains "$dozzle_compose" "image: ${dozzle_image}"',
            text,
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
