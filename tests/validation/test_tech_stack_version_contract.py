from __future__ import annotations

import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest

import yaml

from scripts.lib.document_governance.metadata.heading import validate_body_contract
from scripts.lib.document_governance.metadata.profile import Record
from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    parse_gate_registry,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
)
from scripts.validation.ci_gate_runner import (
    ExecutionContext,
    build_public_validation_plan,
)
from tests.lib.gate.subprocess_support import gate_root_pass_fds

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "infra/tech-stack.versions.json"
RENOVATE_CONFIG = ROOT / "renovate.json5"
RENOVATE_GLOBAL_CONFIG = ROOT / "infra/09-tooling/renovate/config/config.js"
DEPENDABOT_CONFIG = ROOT / ".github/dependabot.yml"
HARDENING_CHECKER = ROOT / "scripts/hardening/check-all-hardening.sh"
OAUTH_DOCKERFILE = ROOT / "infra/02-auth/oauth2-proxy/Dockerfile"
OAUTH_DEV_DOCKERFILE = ROOT / "infra/02-auth/oauth2-proxy/dev.Dockerfile"
DOZZLE_COMPOSE = ROOT / "infra/11-laboratory/dozzle/docker-compose.yml"
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
DIRECT_RUNTIME_DOCS = (
    "infra/01-gateway/README.md",
    "infra/02-auth/keycloak/README.md",
    "infra/06-observability/README.md",
    "infra/06-observability/alloy/README.md",
    "infra/06-observability/prometheus/README.md",
    "infra/06-observability/pushgateway/README.md",
    "infra/06-observability/pyroscope/README.md",
    "infra/06-observability/tempo/README.md",
    "infra/08-ai/README.md",
    "infra/11-laboratory/dozzle/README.md",
    "docs/05.operations/catalog/06-observability/0040-alloy/guide.md",
    "docs/05.operations/catalog/06-observability/0045-prometheus/guide.md",
    "docs/05.operations/catalog/06-observability/0040-alloy/policy.md",
    "docs/05.operations/catalog/06-observability/0045-prometheus/policy.md",
    "docs/05.operations/catalog/06-observability/0040-alloy/runbook.md",
)


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


def updater_contract_findings(
    renovate: dict[str, object],
    global_config: dict[str, object],
    dependabot: dict[str, object],
    root: pathlib.Path,
) -> tuple[str, ...]:
    findings: list[str] = []
    managers = renovate.get("enabledManagers")
    expected_managers = {
        "docker-compose",
        "dockerfile",
        "github-actions",
        "custom.regex",
        "pip_requirements",
    }
    if not isinstance(managers, list) or set(managers) != expected_managers:
        findings.append("Renovate manager ownership drift")
    pip = renovate.get("pip_requirements")
    if not isinstance(pip, dict) or pip.get("managerFilePatterns") != [
        r"/^infra\/.+\/requirements\.txt$/"
    ]:
        findings.append("pip_requirements ownership must stay limited to infra images")
    if not any(
        isinstance(rule, dict)
        and rule.get("matchManagers") == ["pip_requirements"]
        and rule.get("automerge") is False
        for rule in renovate.get("packageRules") or []
    ):
        findings.append("image-local Python pins must not automerge")
    if isinstance(managers, list) and "npm" in managers:
        findings.append("npm updater ownership overlaps Dependabot")

    custom_managers = renovate.get("customManagers")
    expected_pattern = r"/^infra\/09-tooling\/opentofu\/docker-compose\.yml$/"
    if not isinstance(custom_managers, list) or len(custom_managers) != 1:
        findings.append("custom regex manager count drift")
    else:
        custom = custom_managers[0]
        patterns = custom.get("managerFilePatterns")
        match_strings = custom.get("matchStrings")
        if patterns != [expected_pattern]:
            findings.append("custom regex manager file ownership is broad")
        if (
            not isinstance(match_strings, list)
            or not match_strings
            or any(
                not isinstance(pattern, str)
                or not pattern.startswith(r"FROM\s+")
                or "image" in pattern.lower()
                for pattern in match_strings
            )
        ):
            findings.append("custom regex manager overlaps Compose images")

    infrastructure_managers = {"docker-compose", "dockerfile", "custom.regex"}
    package_rules = renovate.get("packageRules")
    has_no_automerge = any(
        isinstance(rule, dict)
        and set(rule.get("matchManagers", [])) == infrastructure_managers
        and rule.get("automerge") is False
        for rule in package_rules or []
    )
    if not has_no_automerge:
        findings.append("infrastructure automerge must be disabled")
    if renovate.get("minimumReleaseAge") != "7 days":
        findings.append("normal updates must use the seven-day release age")
    if renovate.get("minimumReleaseAgeBehaviour") != "timestamp-optional":
        findings.append("unknown timestamps must use explicit manual review fallback")
    # Owner commit 8d93673b2 replaced the natural-language schedule with the
    # equivalent explicit cron (Monday 00:00-05:59 Asia/Seoul).
    if renovate.get("timezone") != "Asia/Seoul" or renovate.get("schedule") != [
        "* 0-5 * * 1"
    ]:
        findings.append("Renovate schedule drift")
    alerts = renovate.get("vulnerabilityAlerts")
    if (
        not isinstance(alerts, dict)
        or alerts.get("automerge") is not False
        or "minimumReleaseAge" in alerts
        or "schedule" in alerts
    ):
        findings.append("security updates must bypass normal delay without automerge")

    if global_config.get("allowScripts") is not False:
        findings.append("Renovate scripts must remain disabled")
    if global_config.get("allowedCommands") != [
        r"^bash scripts/operations/sync-tech-stack-versions\.sh$"
    ]:
        findings.append("Renovate command allowlist is unsafe")
    if renovate.get("postUpgradeTasks") != {
        "commands": ["bash scripts/operations/sync-tech-stack-versions.sh"],
        "fileFilters": ["infra/tech-stack.versions.json"],
        "executionMode": "branch",
    }:
        findings.append("Renovate version projection task drift")

    updates = dependabot.get("updates")
    if not isinstance(updates, list) or len(updates) != 1:
        findings.append("Dependabot ownership must contain one npm target")
    else:
        update = updates[0]
        directory = update.get("directory")
        if update.get("package-ecosystem") != "npm":
            findings.append("Dependabot must own npm only")
        if update.get("open-pull-requests-limit") != 5:
            findings.append("Dependabot pull-request limit drift")
        if update.get("cooldown") != {"default-days": 7}:
            findings.append("Dependabot cooldown drift")
        if update.get("schedule") != {
            "interval": "weekly",
            "day": "wednesday",
            "time": "05:00",
            "timezone": "Asia/Seoul",
        }:
            findings.append("Dependabot staggered schedule drift")
        if not isinstance(directory, str) or not directory.startswith("/"):
            findings.append("Dependabot directory is invalid")
        else:
            target = root / directory.removeprefix("/")
            for filename in ("package.json", "package-lock.json"):
                if not (target / filename).is_file():
                    findings.append(f"Dependabot target is missing {filename}")
    return tuple(findings)


class UpdaterOwnershipContractTests(unittest.TestCase):
    @staticmethod
    def load_contracts() -> tuple[
        dict[str, object], dict[str, object], dict[str, object]
    ]:
        renovate = json.loads(RENOVATE_CONFIG.read_text(encoding="utf-8"))
        result = subprocess.run(
            [
                "node",
                "-e",
                ("process.stdout.write(JSON.stringify(require(process.argv[1])))"),
                str(RENOVATE_GLOBAL_CONFIG),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        global_config = json.loads(result.stdout)
        dependabot = yaml.safe_load(DEPENDABOT_CONFIG.read_text(encoding="utf-8"))
        return renovate, global_config, dependabot

    def test_current_updater_ownership_is_non_overlapping_and_fail_closed(
        self,
    ) -> None:
        self.assertEqual(
            (),
            updater_contract_findings(*self.load_contracts(), ROOT),
        )

    def test_npm_overlap_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        overlap = json.loads(json.dumps(renovate))
        overlap["enabledManagers"].append("npm")
        self.assertIn(
            "npm updater ownership overlaps Dependabot",
            updater_contract_findings(overlap, global_config, dependabot, ROOT),
        )

    def test_broad_custom_regex_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        broad = json.loads(json.dumps(renovate))
        broad["customManagers"][0]["managerFilePatterns"] = ["/.*/"]
        self.assertIn(
            "custom regex manager file ownership is broad",
            updater_contract_findings(broad, global_config, dependabot, ROOT),
        )

    def test_unsafe_allowed_commands_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        unsafe_global = {**global_config, "allowedCommands": [".*"]}
        self.assertIn(
            "Renovate command allowlist is unsafe",
            updater_contract_findings(renovate, unsafe_global, dependabot, ROOT),
        )

    def test_enabled_scripts_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        enabled = {**global_config, "allowScripts": True}
        self.assertIn(
            "Renovate scripts must remain disabled",
            updater_contract_findings(renovate, enabled, dependabot, ROOT),
        )

    def test_missing_dependabot_package_json_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = pathlib.Path(temporary_directory) / "projects/storybook/nextjs"
            target.mkdir(parents=True)
            (target / "package-lock.json").write_text("{}\n")
            self.assertEqual(
                ("Dependabot target is missing package.json",),
                updater_contract_findings(
                    renovate,
                    global_config,
                    dependabot,
                    pathlib.Path(temporary_directory),
                ),
            )

    def test_missing_dependabot_package_lock_mutation_is_detected(self) -> None:
        renovate, global_config, dependabot = self.load_contracts()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = pathlib.Path(temporary_directory) / "projects/storybook/nextjs"
            target.mkdir(parents=True)
            (target / "package.json").write_text("{}\n")
            self.assertEqual(
                ("Dependabot target is missing package-lock.json",),
                updater_contract_findings(
                    renovate,
                    global_config,
                    dependabot,
                    pathlib.Path(temporary_directory),
                ),
            )


class TechStackVersionContractTests(unittest.TestCase):
    @staticmethod
    def registry_entries() -> dict[str, dict[str, object]]:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return {entry["component"]: entry for entry in registry["entries"]}

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

    def test_runtime_docs_link_authority_without_duplicating_pins(self) -> None:
        for relative_path in DIRECT_RUNTIME_DOCS:
            with self.subTest(path=relative_path):
                record = Record(pathlib.Path(relative_path), {}, "common/readme")
                findings = validate_body_contract(
                    record,
                    (ROOT / relative_path).read_text(encoding="utf-8"),
                    {"profiles": {}},
                    False,
                )
                self.assertEqual(
                    [],
                    [
                        finding
                        for finding in findings
                        if finding.code.startswith("runtime-version-")
                    ],
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

    def test_public_contract_owns_hardening_version_validation(self) -> None:
        public = parse_public_gate_contract(load_contract_document(ROOT))
        hardening = tuple(
            item
            for item in public.validators
            if item.entrypoint
            == pathlib.PurePosixPath("scripts/hardening/check-all-hardening.sh")
        )
        self.assertEqual(1, len(hardening))
        self.assertEqual("repository-integrity", hardening[0].suite)

    def test_required_drift_check_runs_once_in_each_public_context(self) -> None:
        document = load_contract_document(ROOT)
        public = parse_public_gate_contract(document)
        registry = parse_gate_registry(document, ".github/workflow-contract.yml")
        leaf = next(
            node
            for node in document["gate_nodes"]
            if node["gate_id"] == "leaf.local-tech-stack-version-drift"
        )
        self.assertEqual(
            ("scripts/operations/sync-tech-stack-versions.sh", ["--check"], "."),
            (leaf["entrypoint"], leaf["argv"], leaf["cwd"]),
        )
        for profile, context in (
            ("changed", ExecutionContext.LOCAL),
            ("changed", ExecutionContext.PULL_REQUEST),
            ("full", ExecutionContext.LOCAL),
            ("full", ExecutionContext.PUSH),
            ("full", ExecutionContext.WORKFLOW_DISPATCH),
        ):
            with self.subTest(profile=profile, context=context):
                suites = select_public_suites(public, profile, ())
                plan = build_public_validation_plan(
                    registry,
                    public_root_gate_ids(public, suites),
                    public,
                    suites,
                    context,
                    profile=profile,
                    root=ROOT,
                )
                self.assertEqual(
                    1,
                    sum(invocation.gate_id == leaf["gate_id"] for invocation in plan),
                )

        # Compare executable step commands, not comments or documentation examples.
        for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
            with self.subTest(workflow=path.name):
                workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
                commands = [
                    shlex.split(line, comments=True)
                    for job in workflow["jobs"].values()
                    for step in job["steps"]
                    for line in step.get("run", "").splitlines()
                ]
                self.assertNotIn(["bash", leaf["entrypoint"], *leaf["argv"]], commands)

    def test_the_required_gate_reaches_the_drift_leaf_on_every_pull_request(
        self,
    ) -> None:
        """Every PR reaches the drift leaf, even without a matching path rule."""

        document = load_contract_document(ROOT)
        public = parse_public_gate_contract(document)
        registry = parse_gate_registry(document, ".github/workflow-contract.yml")

        # An empty change set selects the declared fallback, which is the floor
        # every pull request gets before any path rule adds to it.
        suites = select_public_suites(public, "changed", ())
        self.assertIn("repository-integrity", suites)

        plan = build_public_validation_plan(
            registry,
            public_root_gate_ids(public, suites),
            public,
            suites,
            ExecutionContext.PULL_REQUEST,
            profile="changed",
            root=ROOT,
        )
        self.assertIn(
            "leaf.local-tech-stack-version-drift",
            {invocation.gate_id for invocation in plan},
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
                    "services:\n"
                    "  target:\n"
                    f"    image: {expected}\n"
                    f"  {sibling_key}:\n"
                    "    image: registry.example.test/team/other:9\n"
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
                    "services:\n"
                    "  target:\n"
                    "    restart: unless-stopped\n"
                    f"  {sibling_key}:\n"
                    "    image: registry.example.test/team/other:9\n"
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
                    "services:\n"
                    f"  {first_key}:\n"
                    "    image: registry.example.test/team/app:1\n"
                    f"  {second_key}:\n"
                    "    image: registry.example.test/team/app:2\n"
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
                    "services:\n"
                    "  target:\n"
                    "    image: registry.example.test/team/app:1\n"
                    f"  {first_key}:\n"
                    "    image: registry.example.test/team/other:1\n"
                    f"  {second_key}:\n"
                    "    image: registry.example.test/team/other:2\n"
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


class TechStackSynchronizationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.script = self.root / "scripts/operations/sync-tech-stack-versions.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copyfile(
            ROOT / "scripts/operations/sync-tech-stack-versions.sh", self.script
        )
        self.registry = self.root / "infra/tech-stack.versions.json"
        self.registry.parent.mkdir()
        self.compose = self.root / "infra/example/docker-compose.yml"
        self.compose.parent.mkdir()
        self.compose.write_text("services:\n  app:\n    image: example/app:2\n")
        self.write_registry()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "add", "infra/example/docker-compose.yml"],
            cwd=self.root,
            check=True,
        )

    def write_registry(self, image: str = "example/app:1") -> None:
        self.registry.write_text(
            json.dumps(
                {
                    "source_of_truth": (
                        "Git-tracked infra/**/{compose,docker-compose}*.{yml,yaml} "
                        "service image declarations"
                    ),
                    "local_repository_prefixes": ["hy/", "hyhome/", "hy-home/"],
                    "entries": [
                        {
                            "component": "Synthetic",
                            "classification": "external",
                            "repository_classifications": {"example/app": "external"},
                            "images": [image],
                            "compose_files": ["infra/example/docker-compose.yml"],
                            "sources": [
                                {
                                    "compose_file": (
                                        "infra/example/docker-compose.yml"
                                    ),
                                    "images": [image],
                                }
                            ],
                        }
                    ],
                },
                indent=4,
            )
            + "\n"
        )

    def run_sync(
        self,
        *arguments: str,
        extra_env: dict[str, str] | None = None,
        pass_fds: tuple[int, ...] = (),
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(self.script), *arguments],
            cwd=self.root,
            env={
                **{
                    key: value
                    for key, value in os.environ.items()
                    if key != "HYHOME_CI_GATE_ROOT"
                },
                **(extra_env or {}),
            },
            text=True,
            capture_output=True,
            check=False,
            pass_fds=pass_fds,
        )

    def assert_rejected_without_write(self, expected: str) -> None:
        before = self.registry.read_bytes()
        for mode in ((), ("--check",), ("--dry-run",)):
            with self.subTest(mode=mode):
                result = self.run_sync(*mode)
                self.assertNotEqual(0, result.returncode, result.stdout)
                self.assertIn(expected, result.stderr)
                self.assertEqual(before, self.registry.read_bytes())

    def test_missing_compose_file_fails_closed(self) -> None:
        self.compose.unlink()
        self.assert_rejected_without_write("compose")

    def test_missing_source_metadata_fails_closed(self) -> None:
        body = json.loads(self.registry.read_text())
        body.pop("source_of_truth")
        self.registry.write_text(json.dumps(body))
        self.assert_rejected_without_write("source_of_truth")

    def test_new_external_repository_requires_projection_then_write_adds_it(
        self,
    ) -> None:
        added = self.root / "infra/new/docker-compose.yaml"
        added.parent.mkdir()
        added.write_text("services:\n  new:\n    image: registry.test/team/new:3\n")
        subprocess.run(
            ["git", "add", "infra/new/docker-compose.yaml"],
            cwd=self.root,
            check=True,
        )
        before = self.registry.read_bytes()
        check = self.run_sync("--check")
        self.assertEqual(1, check.returncode)
        self.assertIn("out of sync", check.stderr)
        self.assertEqual(before, self.registry.read_bytes())

        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        body = json.loads(self.registry.read_text())
        added_entry = next(
            entry
            for entry in body["entries"]
            if entry["images"] == ["registry.test/team/new:3"]
        )
        self.assertEqual("external", added_entry["classification"])
        self.assertEqual(
            ["infra/new/docker-compose.yaml"], added_entry["compose_files"]
        )
        self.assertEqual(0, self.run_sync("--check").returncode)

    def test_hyphenated_compose_filename_is_in_source_universe(self) -> None:
        baseline = self.run_sync()
        self.assertEqual(0, baseline.returncode, baseline.stderr)
        added = self.root / "infra/example/docker-compose-dev.yml"
        added.write_text("services:\n  new:\n    image: example/new:1\n")
        subprocess.run(
            ["git", "add", "infra/example/docker-compose-dev.yml"],
            cwd=self.root,
            check=True,
        )
        before = self.registry.read_bytes()
        check = self.run_sync("--check")
        self.assertEqual(1, check.returncode)
        self.assertIn("out of sync", check.stderr)
        self.assertEqual(before, self.registry.read_bytes())

        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        body = json.loads(self.registry.read_text())
        added_entry = next(
            entry for entry in body["entries"] if entry["images"] == ["example/new:1"]
        )
        self.assertEqual(
            ["infra/example/docker-compose-dev.yml"],
            added_entry["compose_files"],
        )

    def test_standard_compose_filename_is_in_source_universe(self) -> None:
        baseline = self.run_sync()
        self.assertEqual(0, baseline.returncode, baseline.stderr)
        added = self.root / "infra/example/compose.yaml"
        added.write_text("services:\n  new:\n    image: example/standard:1\n")
        subprocess.run(
            ["git", "add", "infra/example/compose.yaml"],
            cwd=self.root,
            check=True,
        )
        before = self.registry.read_bytes()
        check = self.run_sync("--check")
        self.assertEqual(1, check.returncode)
        self.assertIn("out of sync", check.stderr)
        self.assertEqual(before, self.registry.read_bytes())

        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        body = json.loads(self.registry.read_text())
        added_entry = next(
            entry
            for entry in body["entries"]
            if entry["images"] == ["example/standard:1"]
        )
        self.assertEqual(
            ["infra/example/compose.yaml"],
            added_entry["compose_files"],
        )

    def test_duplicate_repository_ownership_fails_closed(self) -> None:
        body = json.loads(self.registry.read_text())
        duplicate = {**body["entries"][0], "component": "Duplicate"}
        body["entries"].append(duplicate)
        self.registry.write_text(json.dumps(body))
        self.assert_rejected_without_write("duplicate repository ownership")

    def test_removed_repository_requires_projection_then_write_removes_it(
        self,
    ) -> None:
        self.compose.write_text("services: {}\n")
        before = self.registry.read_bytes()
        check = self.run_sync("--check")
        self.assertEqual(1, check.returncode)
        self.assertEqual(before, self.registry.read_bytes())
        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        self.assertEqual([], json.loads(self.registry.read_text())["entries"])
        self.assertEqual(0, self.run_sync("--check").returncode)

    def test_local_custom_repository_is_explicitly_classified(self) -> None:
        self.compose.write_text("services:\n  app:\n    image: hy-home/app:2-local\n")
        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        entry = json.loads(self.registry.read_text())["entries"][0]
        self.assertEqual("local-custom", entry["classification"])
        self.assertEqual(["hy-home/app:2-local"], entry["images"])

    def test_distinct_versions_preserve_exact_source_groups(self) -> None:
        second = self.root / "infra/second/docker-compose.yml"
        second.parent.mkdir()
        second.write_text("services:\n  app:\n    image: example/app:3\n")
        subprocess.run(
            ["git", "add", "infra/second/docker-compose.yml"],
            cwd=self.root,
            check=True,
        )
        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        entry = json.loads(self.registry.read_text())["entries"][0]
        self.assertEqual(["example/app:2", "example/app:3"], entry["images"])
        self.assertEqual(
            [
                {
                    "compose_file": "infra/example/docker-compose.yml",
                    "images": ["example/app:2"],
                },
                {
                    "compose_file": "infra/second/docker-compose.yml",
                    "images": ["example/app:3"],
                },
            ],
            entry["sources"],
        )

    def test_multiple_versions_keep_exact_authored_source_group(self) -> None:
        self.compose.write_text(
            "services:\n  app:\n    image: example/app:1\n"
            "  second:\n    image: example/app:2\n"
        )
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        entry = json.loads(self.registry.read_text())["entries"][0]
        self.assertEqual(["example/app:1", "example/app:2"], entry["images"])
        self.assertEqual(
            [
                {
                    "compose_file": "infra/example/docker-compose.yml",
                    "images": ["example/app:1", "example/app:2"],
                }
            ],
            entry["sources"],
        )
        self.assertEqual(0, self.run_sync("--check").returncode)

    def test_yaml_service_images_exclude_comment_and_extension_decoys(self) -> None:
        self.compose.write_text(
            "x-decoy:\n  image: example/app:9\n"
            "services:\n  app: {image: 'example/app:2'}\n"
        )
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"example/app:2"', self.registry.read_text())

    def test_compose_override_and_reset_tags_have_declared_semantics(self) -> None:
        self.compose.write_text(
            "services:\n  app:\n    image: !override example/app:2\n"
            "  reset:\n    image: !reset example/app:9\n"
            "    ports: !reset []\n"
        )
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"example/app:2"', self.registry.read_text())

    def test_duplicate_yaml_keys_and_unsafe_scalars_are_rejected(self) -> None:
        for text in (
            "services:\n  app:\n    image: example/app:1\n    image: example/app:2\n",
            "services:\n  app:\n    image: [example/app:2]\n",
            "services:\n  app:\n    image: example/app:2 trailing\n",
            "services:\n  app:\n    image: !unknown example/app:2\n",
        ):
            with self.subTest(text=text):
                self.compose.write_text(text)
                self.assert_rejected_without_write("compose")

    def test_digest_changes_keep_repository_identity(self) -> None:
        old_digest, new_digest = "a" * 64, "b" * 64
        for old, new in (
            (
                f"example/app:1@sha256:{old_digest}",
                f"example/app:2@sha256:{new_digest}",
            ),
            (f"example/app@sha256:{old_digest}", f"example/app@sha256:{new_digest}"),
            (
                "registry.test:5000/team/app:1",
                f"registry.test:5000/team/app@sha256:{new_digest}",
            ),
        ):
            with self.subTest(old=old):
                self.write_registry(old)
                self.compose.write_text(f"services:\n  app:\n    image: {new}\n")
                result = self.run_sync()
                self.assertEqual(0, result.returncode, result.stderr)
                images = json.loads(self.registry.read_text())["entries"][0]["images"]
                self.assertEqual([new], images)

    def test_dry_run_and_check_never_write_and_write_preserves_format(self) -> None:
        before = self.registry.read_bytes()
        for mode, code in (("--dry-run", 0), ("--check", 1)):
            with self.subTest(mode=mode):
                result = self.run_sync(mode)
                self.assertEqual(code, result.returncode, result.stderr)
                self.assertEqual(before, self.registry.read_bytes())
        self.registry.chmod(0o640)
        with self.registry.open("rb") as original:
            result = self.run_sync()
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(before, original.read(), "write must replace atomically")
        self.assertEqual(
            before.replace(b"example/app:1", b"example/app:2"),
            self.registry.read_bytes(),
        )
        self.assertEqual(0o640, self.registry.stat().st_mode & 0o777)
        self.assertEqual(0, self.run_sync("--check").returncode)

    def test_dry_run_previews_exact_image_and_source_change(self) -> None:
        before = self.registry.read_bytes()
        result = self.run_sync("--dry-run")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            (
                "change Synthetic "
                "source=infra/example/docker-compose.yml "
                "old=example/app:1 new=example/app:2"
            ),
            result.stdout,
        )
        self.assertEqual(before, self.registry.read_bytes())

    def test_argument_validation_rejects_extra_arguments(self) -> None:
        before = self.registry.read_bytes()
        for arguments in (("--bad",), ("--check", "extra"), ("--dry-run", "--check")):
            with self.subTest(arguments=arguments):
                result = self.run_sync(*arguments)
                self.assertEqual(2, result.returncode)
                self.assertEqual(before, self.registry.read_bytes())

    def test_interpolation_uses_declared_defaults_without_environment(self) -> None:
        self.compose.write_text(
            "services:\n  app:\n    image: ${IMAGE:-example/app:2}\n"
        )
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"example/app:2"', self.registry.read_text())

    def test_write_preserves_registry_line_endings(self) -> None:
        before = self.registry.read_bytes().replace(b"\n", b"\r\n")
        self.registry.write_bytes(before)
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            before.replace(b"example/app:1", b"example/app:2"),
            self.registry.read_bytes(),
        )

    def test_yaml_merge_can_override_an_inherited_image(self) -> None:
        self.compose.write_text(
            "x-default: &base\n  image: example/app:9\n"
            "services:\n  app:\n    <<: *base\n    image: example/app:2\n"
        )
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"example/app:2"', self.registry.read_text())

    def test_root_identity_guard_accepts_only_matching_directory_fd(self) -> None:
        invalid = self.run_sync(
            "--check", extra_env={"HYHOME_CI_GATE_ROOT": str(self.root)}
        )
        self.assertEqual(2, invalid.returncode)
        descriptor = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            accepted = self.run_sync(
                "--dry-run",
                extra_env={"HYHOME_CI_GATE_ROOT": f"/proc/self/fd/{descriptor}"},
                pass_fds=(descriptor,),
            )
            self.assertEqual(0, accepted.returncode, accepted.stderr)
        finally:
            os.close(descriptor)

    def test_atomic_replace_failure_preserves_original_and_cleans_temp(self) -> None:
        hook_dir = self.root / "hooks"
        hook_dir.mkdir()
        (hook_dir / "sitecustomize.py").write_text(
            "import os\n"
            "def fail_replace(*args, **kwargs):\n"
            "    raise OSError('synthetic replace failure')\n"
            "os.replace = fail_replace\n"
        )
        before = self.registry.read_bytes()
        result = self.run_sync(extra_env={"PYTHONPATH": str(hook_dir)})
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(before, self.registry.read_bytes())
        self.assertEqual(
            [], list(self.registry.parent.glob(".tech-stack.versions.json.*"))
        )

    def test_registry_shape_and_nonimage_metadata_fail_closed(self) -> None:
        valid = json.loads(self.registry.read_text())
        for invalid in (
            {**valid, "entries": "invalid"},
            {
                **valid,
                "entries": [
                    {
                        "component": "Synthetic",
                        "images": "example/app:1",
                        "compose_files": ["infra/example/docker-compose.yml"],
                    }
                ],
            },
            {
                **valid,
                "entries": [
                    {
                        "component": "Synthetic",
                        "images": ["example/app:1"],
                        "compose_files": "infra/example/docker-compose.yml",
                    }
                ],
            },
        ):
            with self.subTest(invalid=invalid):
                self.registry.write_text(json.dumps(invalid))
                self.assert_rejected_without_write("registry")
        self.write_registry()
        body = json.loads(self.registry.read_text())
        self.registry.write_text(json.dumps({**body, "description": "example/app:1"}))
        result = self.run_sync()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            "example/app:1",
            json.loads(self.registry.read_text())["description"],
        )

    def test_missing_default_and_path_escape_fail_closed(self) -> None:
        self.compose.write_text("services:\n  app:\n    image: ${IMAGE}\n")
        self.assert_rejected_without_write("compose")
        self.compose.write_text("services:\n  app:\n    image: example/app:2\n")
        body = json.loads(self.registry.read_text())
        entry = {**body["entries"][0], "compose_files": ["../compose.yml"]}
        self.registry.write_text(json.dumps({**body, "entries": [entry]}))
        before = self.registry.read_bytes()
        check = self.run_sync("--check")
        self.assertEqual(1, check.returncode)
        self.assertEqual(before, self.registry.read_bytes())
        write = self.run_sync()
        self.assertEqual(0, write.returncode, write.stderr)
        self.assertEqual(
            ["infra/example/docker-compose.yml"],
            json.loads(self.registry.read_text())["entries"][0]["compose_files"],
        )


if __name__ == "__main__":
    unittest.main()
