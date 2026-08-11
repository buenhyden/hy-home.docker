import os
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"
TARGET_SURFACE_MANIFEST = (
    ROOT
    / "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml"
)
TARGET_SURFACE_SUMMARY = TARGET_SURFACE_MANIFEST.with_name(
    "target-surface-convergence-summary.md"
)
MIGRATED_DOMAINS = (
    "00-workspace",
    "01-gateway",
    "02-auth",
    "03-security",
    "04-data",
    "05-messaging",
    "06-observability",
    "07-workflow",
    "08-ai",
    "09-tooling",
)

# Frozen Task 6A/6B/6C boundary: each tuple is (domain, exact ledger subject path,
# shared ops identity, existing role set).  A subject is intentionally absent
# from a role when mig-0001 has no row for that role.
EXPECTED_SUBJECTS = (
    ("00-workspace", "common-optimizations-template-exceptions", "0001", {"policy"}),
    ("00-workspace", "developer-setup", "0002", {"guide"}),
    ("00-workspace", "env-key-comparison", "0003", {"guide"}),
    ("00-workspace", "harness-agent-first-engineering", "0004", {"guide", "policy"}),
    ("00-workspace", "harness-agent-first-engineering-validation", "0005", {"runbook"}),
    ("00-workspace", "infra-service-optimization-catalog", "0006", {"policy"}),
    ("00-workspace", "llm-wiki-maintenance", "0007", {"guide", "policy", "runbook"}),
    ("00-workspace", "new-service-onboarding", "0008", {"guide"}),
    ("00-workspace", "release-management", "0009", {"runbook"}),
    ("00-workspace", "sensitive-env-vars-comparison", "0010", {"guide"}),
    ("01-gateway", "nginx", "0011", {"guide", "policy", "runbook"}),
    ("01-gateway", "setup", "0012", {"guide"}),
    ("01-gateway", "traefik", "0013", {"guide", "policy", "runbook"}),
    ("02-auth", "keycloak", "0014", {"guide", "policy", "runbook"}),
    ("02-auth", "oauth2-proxy", "0015", {"guide", "policy", "runbook"}),
    ("03-security", "vault", "0016", {"guide", "policy", "runbook"}),
    ("04-data", "analytics-influxdb", "0017", {"guide", "policy", "runbook"}),
    ("04-data", "analytics-ksqldb", "0018", {"guide", "policy", "runbook"}),
    ("04-data", "analytics-opensearch", "0019", {"guide", "policy", "runbook"}),
    ("04-data", "analytics-warehouses", "0020", {"guide", "policy", "runbook"}),
    ("04-data", "backup-backup-policy", "0021", {"policy"}),
    ("04-data", "cache-and-kv-valkey-cluster", "0022", {"guide", "policy", "runbook"}),
    ("04-data", "lake-and-object-minio", "0023", {"guide", "policy", "runbook"}),
    ("04-data", "lake-and-object-seaweedfs", "0024", {"guide", "policy", "runbook"}),
    ("04-data", "nosql-cassandra", "0025", {"guide", "policy", "runbook"}),
    ("04-data", "nosql-couchdb", "0026", {"guide", "policy", "runbook"}),
    ("04-data", "nosql-mongodb", "0027", {"guide", "policy", "runbook"}),
    ("04-data", "operational-mng-db", "0028", {"guide", "policy", "runbook"}),
    ("04-data", "operational-supabase", "0029", {"guide", "policy", "runbook"}),
    ("04-data", "optimization-optimization-hardening", "0030", {"guide", "policy", "runbook"}),
    ("04-data", "relational-postgresql-cluster", "0031", {"guide", "policy", "runbook"}),
    (
        "04-data",
        "relational-postgresql-logical-upgrade-restore-rehearsal",
        "0032",
        {"runbook"},
    ),
    ("04-data", "specialized-neo4j", "0033", {"guide", "policy", "runbook"}),
    ("04-data", "specialized-qdrant", "0034", {"guide", "policy", "runbook"}),
    ("04-data", "storage-storage-exhaustion", "0035", {"runbook"}),
    ("05-messaging", "kafka", "0036", {"guide", "policy", "runbook"}),
    ("05-messaging", "optimization-hardening", "0037", {"guide", "policy", "runbook"}),
    ("05-messaging", "rabbitmq", "0038", {"guide", "policy", "runbook"}),
    ("06-observability", "alertmanager", "0039", {"guide", "policy", "runbook"}),
    ("06-observability", "alloy", "0040", {"guide", "policy", "runbook"}),
    ("06-observability", "grafana", "0041", {"guide", "policy", "runbook"}),
    ("06-observability", "lgtm-stack", "0042", {"guide"}),
    ("06-observability", "loki", "0043", {"guide", "policy", "runbook"}),
    ("06-observability", "optimization-hardening", "0044", {"guide", "policy", "runbook"}),
    ("06-observability", "prometheus", "0045", {"guide", "policy", "runbook"}),
    ("06-observability", "pushgateway", "0046", {"guide", "policy", "runbook"}),
    ("06-observability", "pyroscope", "0047", {"guide", "policy", "runbook"}),
    ("06-observability", "retention", "0048", {"policy"}),
    ("06-observability", "tempo", "0049", {"guide", "policy", "runbook"}),
    ("07-workflow", "airflow", "0050", {"guide", "policy", "runbook"}),
    ("07-workflow", "airflow-dag-basics", "0051", {"guide"}),
    ("07-workflow", "dag-deployment", "0052", {"policy"}),
    ("07-workflow", "n8n", "0053", {"guide", "policy", "runbook"}),
    ("07-workflow", "optimization-hardening", "0054", {"guide", "policy", "runbook"}),
    ("08-ai", "gpu-recovery", "0055", {"runbook"}),
    ("08-ai", "ollama", "0056", {"guide", "policy", "runbook"}),
    ("08-ai", "open-webui", "0057", {"guide", "policy", "runbook"}),
    ("08-ai", "optimization-hardening", "0058", {"guide", "policy", "runbook"}),
    ("08-ai", "rag-workflow", "0059", {"guide"}),
    ("09-tooling", "iac-deployment-policy", "0060", {"policy"}),
    ("09-tooling", "k6", "0061", {"guide", "policy", "runbook"}),
    ("09-tooling", "locust", "0062", {"guide", "policy", "runbook"}),
    ("09-tooling", "optimization-hardening", "0063", {"guide", "policy", "runbook"}),
    ("09-tooling", "performance-testing", "0064", {"guide", "policy", "runbook"}),
    ("09-tooling", "registry", "0065", {"guide", "policy", "runbook"}),
    ("09-tooling", "sonarqube", "0066", {"guide", "policy", "runbook"}),
    ("09-tooling", "syncthing", "0067", {"guide", "policy", "runbook"}),
    ("09-tooling", "terraform", "0068", {"guide", "policy", "runbook"}),
    ("09-tooling", "terrakube", "0069", {"guide", "policy", "runbook"}),
)


def metadata_for(path: Path) -> dict[str, object]:
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(), flags=re.S)
    if match is None:
        raise AssertionError(f"missing frontmatter: {path.relative_to(ROOT)}")
    return yaml.safe_load(match.group(1))


def ledger_records() -> list[dict[str, object]]:
    match = re.search(r"```yaml\n(.*?)\n```", LEDGER.read_text(), flags=re.S)
    if match is None:
        raise AssertionError("migration ledger YAML block is missing")
    return yaml.safe_load(match.group(1))["records"]


def resolve_repo_path(source: Path, destination: str) -> Path | None:
    if destination.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    target = re.split(r"[?#]", destination, maxsplit=1)[0]
    if not target:
        return None
    candidate = (
        ROOT / target.lstrip("/")
        if target.startswith(("/", "docs/"))
        else source.parent / PurePosixPath(target)
    )
    return Path(os.path.normpath(candidate))


class OperationsTaxonomyTests(unittest.TestCase):
    def test_migrated_domains_leave_no_role_root_copy(self):
        for role in ("guides", "policies", "runbooks"):
            for domain in MIGRATED_DOMAINS:
                self.assertFalse((ROOT / "docs/05.operations" / role / domain).exists())

    def test_each_subject_has_only_ledger_declared_roles_at_its_ops_path(self):
        expected_paths: set[Path] = set()
        for domain, subject, identity, roles in EXPECTED_SUBJECTS:
            subject_root = ROOT / "docs/05.operations" / domain / f"ops-{identity}-{subject}"
            for role in roles:
                path = subject_root / f"{role}.md"
                expected_paths.add(path)
                with self.subTest(path=path):
                    self.assertTrue(path.is_file())

        actual_paths = {
            path
            for domain in MIGRATED_DOMAINS
            for path in (ROOT / "docs/05.operations" / domain).glob("ops-*/*.md")
        }
        self.assertEqual(expected_paths, actual_paths)

    def test_subject_metadata_uses_role_identity_and_noninvented_parents(self):
        for domain, subject, identity, roles in EXPECTED_SUBJECTS:
            subject_root = ROOT / "docs/05.operations" / domain / f"ops-{identity}-{subject}"
            for role in roles:
                path = subject_root / f"{role}.md"
                if not path.is_file():
                    continue
                metadata = metadata_for(path)
                with self.subTest(path=path):
                    self.assertEqual(f"{role}-{identity}", metadata["artifact_id"])
                    self.assertEqual(role, metadata["artifact_type"])
                    self.assertEqual([], metadata["parent_ids"])
                    self.assertRegex(str(metadata["created"]), r"^\d{4}-\d{2}-\d{2}$")
                    self.assertRegex(str(metadata["updated"]), r"^\d{4}-\d{2}-\d{2}$")
                    if int(identity) >= 50:
                        self.assertEqual("2026-08-11", str(metadata["updated"]))

    def test_subject_links_resolve_without_legacy_role_roots(self):
        link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)")
        legacy_root = re.compile(r"docs/05\.operations/(guides|policies|runbooks)/")
        violations: list[str] = []
        for domain, subject, identity, roles in EXPECTED_SUBJECTS:
            subject_root = ROOT / "docs/05.operations" / domain / f"ops-{identity}-{subject}"
            for role in roles:
                path = subject_root / f"{role}.md"
                if not path.is_file():
                    continue
                for destination in link_pattern.findall(path.read_text()):
                    resolved = resolve_repo_path(path, destination)
                    if legacy_root.search(destination) or (
                        resolved is not None and not resolved.exists()
                    ):
                        violations.append(f"{path.relative_to(ROOT)}: {destination}")
        self.assertEqual([], violations)

    def test_scoped_active_consumers_do_not_name_deleted_role_roots(self):
        deleted_root = re.compile(
            r"docs/05\.operations/(guides|policies|runbooks)/"
            r"(04-data|05-messaging|06-observability|07-workflow|08-ai|09-tooling)"
            r"(?:/|\b)"
        )
        active_roots = (
            ROOT / "docs/01.requirements",
            ROOT / "docs/02.architecture",
            ROOT / "docs/03.specs",
            ROOT / "infra/07-workflow",
            ROOT / "infra/08-ai",
            ROOT / "infra/09-tooling",
        )
        active_consumers = [
            path
            for active_root in active_roots
            for path in active_root.rglob("*.md")
        ] + [
            ROOT / "infra/04-data/lake-and-object/README.md",
            ROOT / "docs/05.operations/guides/README.md",
            ROOT / "docs/05.operations/policies/README.md",
            ROOT / "docs/05.operations/runbooks/README.md",
            ROOT / "docs/90.references/llm-wiki/llm-wiki-index.md",
        ]
        violations: list[str] = []
        for path in active_consumers:
            for line_number, line in enumerate(path.read_text().splitlines(), 1):
                if deleted_root.search(line):
                    violations.append(
                        f"{path.relative_to(ROOT)}:{line_number}: {line.strip()}"
                    )
        self.assertEqual([], violations)

    def test_each_readme_merge_preserves_relevant_current_navigation(self):
        scoped_prefix = "docs/05.operations/"
        merge_rows = [
            row
            for row in ledger_records()
            if row["action"] == "merge"
            and re.fullmatch(
                r"docs/05\.operations/(guides|policies|runbooks)/"
                r"(00-workspace|01-gateway|02-auth|03-security|04-data|05-messaging|06-observability|07-workflow|08-ai|09-tooling)"
                r"(?:/[^/]+)?/README\.md",
                str(row["legacy_path"]),
            )
        ]
        self.assertEqual(46, len(merge_rows))
        stable_paths = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in ledger_records()
            if str(row["legacy_path"]).startswith(scoped_prefix)
        }
        merge_rows_by_source = {
            str(row["legacy_path"]): row for row in merge_rows
        }
        link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)")

        preserved_navigation_indexes = {
            "docs/05.operations/README.md",
            "docs/05.operations/guides/README.md",
            "docs/05.operations/policies/README.md",
            "docs/05.operations/runbooks/README.md",
            "docs/05.operations/incidents/README.md",
        }

        def linked_current_navigation_paths(
            source: str, body: str, seen: set[str] | None = None
        ) -> set[str]:
            visited = set() if seen is None else seen
            paths: set[str] = set()
            for destination in link_pattern.findall(body):
                resolved = resolve_repo_path(ROOT / source, destination)
                if resolved is None:
                    continue
                resolved_path = str(resolved.relative_to(ROOT))
                child_row = merge_rows_by_source.get(resolved_path)
                if child_row is not None and resolved_path not in visited:
                    result = subprocess.run(
                        [
                            "git",
                            "show",
                            f"{child_row['source_commit']}:{resolved_path}",
                        ],
                        cwd=ROOT,
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                    paths.update(
                        linked_current_navigation_paths(
                            resolved_path,
                            result.stdout,
                            visited | {resolved_path},
                        )
                    )
                canonical = stable_paths.get(resolved_path, resolved_path)
                if re.fullmatch(
                    r"docs/05\.operations/"
                    r"(00-workspace|01-gateway|02-auth|03-security|04-data|05-messaging|06-observability|07-workflow|08-ai|09-tooling)"
                    r"/ops-[^/]+/(guide|policy|runbook)\.md",
                    canonical,
                ) or (
                    re.match(
                        r"docs/05\.operations/"
                        r"(?:(guides|policies|runbooks)/)?"
                        r"(04-data|05-messaging|06-observability|07-workflow|08-ai|09-tooling)/",
                        source,
                    )
                    and canonical in preserved_navigation_indexes
                ):
                    paths.add(canonical)
            return paths

        for row in merge_rows:
            source = str(row["legacy_path"])
            target = str(row["stable_path"])
            source_commit = str(row["source_commit"])
            result = subprocess.run(
                ["git", "show", f"{source_commit}:{source}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            target_body = (ROOT / target).read_text()
            source_paths = linked_current_navigation_paths(source, result.stdout)
            target_paths = linked_current_navigation_paths(target, target_body)
            source_paths.discard(target)
            target_paths.discard(target)
            with self.subTest(source=source):
                self.assertTrue(source_paths)
                self.assertTrue(source_paths.issubset(target_paths))
                if re.match(
                    r"docs/05\.operations/(04-data|05-messaging|06-observability|07-workflow|08-ai|09-tooling)/",
                    target,
                ):
                    archive_links = []
                    for destination in link_pattern.findall(target_body):
                        resolved = resolve_repo_path(ROOT / target, destination)
                        if resolved is not None and resolved.is_relative_to(
                            ROOT / "docs/98.archive"
                        ):
                            archive_links.append(destination)
                    self.assertEqual([], archive_links)

    def test_task6c_immutable_target_surface_summary_rows_match_owner(self):
        source_pattern = re.compile(
            r"docs/05\.operations/(guides|policies|runbooks)/09-tooling/"
            r"(k6|locust|performance-testing)\.md"
        )
        owner = yaml.safe_load(TARGET_SURFACE_MANIFEST.read_text())
        owner_entries = [
            entry
            for entry in owner["entries"]
            if source_pattern.fullmatch(str(entry["source_path"]))
        ]
        self.assertEqual(9, len(owner_entries))

        owner_sources = {str(entry["source_path"]) for entry in owner_entries}
        stable_targets = {
            str(row["stable_path"])
            for row in ledger_records()
            if str(row["legacy_path"]) in owner_sources
        }
        self.assertEqual(9, len(stable_targets))

        summary_rows = {
            tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
            for line in TARGET_SURFACE_SUMMARY.read_text().splitlines()
            if line.startswith("|")
        }
        relevant_rows = {
            row
            for row in summary_rows
            if len(row) == 5
            and (row[0] in owner_sources | stable_targets)
        }
        expected_rows = {
            (
                str(entry["source_path"]),
                str(entry["target_path"] or ""),
                str(entry["disposition"]),
                str(entry["review_verdict"]["specification"]),
                str(entry["review_verdict"]["quality"]),
            )
            for entry in owner_entries
        }
        self.assertEqual(expected_rows, relevant_rows)


if __name__ == "__main__":
    unittest.main()
