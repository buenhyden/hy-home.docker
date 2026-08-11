import os
import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "docs/98.archive/migrations/mig-0001-sdlc-taxonomy-convergence.md"
MIGRATED_DOMAINS = (
    "00-workspace",
    "01-gateway",
    "02-auth",
    "03-security",
)

# Frozen Task 6A boundary: each tuple is (domain, exact ledger subject path,
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

    def test_each_readme_merge_preserves_its_historical_subject_navigation(self):
        scoped_prefix = "docs/05.operations/"
        merge_rows = [
            row
            for row in ledger_records()
            if row["action"] == "merge"
            and re.fullmatch(
                r"docs/05\.operations/(policies|runbooks)/(00-workspace|01-gateway|02-auth|03-security)/README\.md",
                str(row["legacy_path"]),
            )
        ]
        self.assertEqual(8, len(merge_rows))
        stable_paths = {
            str(row["legacy_path"]): str(row["stable_path"])
            for row in ledger_records()
            if str(row["legacy_path"]).startswith(scoped_prefix)
        }
        link_pattern = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)")

        def linked_operations_paths(source: str, body: str) -> set[str]:
            paths: set[str] = set()
            for destination in link_pattern.findall(body):
                resolved = resolve_repo_path(ROOT / source, destination)
                if resolved is None:
                    continue
                canonical = stable_paths.get(str(resolved.relative_to(ROOT)), str(resolved.relative_to(ROOT)))
                if re.fullmatch(r"docs/05\.operations/(00-workspace|01-gateway|02-auth|03-security)/ops-[^/]+/(guide|policy|runbook)\.md", canonical):
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
            source_paths = linked_operations_paths(source, result.stdout)
            target_paths = linked_operations_paths(target, (ROOT / target).read_text())
            with self.subTest(source=source):
                self.assertTrue(source_paths)
                self.assertTrue(source_paths.issubset(target_paths))


if __name__ == "__main__":
    unittest.main()
