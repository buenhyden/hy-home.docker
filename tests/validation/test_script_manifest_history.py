from tests.validation._script_manifest_support import *


class ScriptManifestHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ledger_text = (
            LEDGER.read_text(encoding="utf-8")
            .split("```yaml\n", 1)[1]
            .split("```", 1)[0]
        )
        cls.ledger_rows = yaml.safe_load(ledger_text)["records"]
        cls.ledger_by_path = {row["legacy_path"]: row for row in cls.ledger_rows}
    def test_ledger_has_one_complete_sorted_row_for_every_migration_document(
        self,
    ) -> None:
        rows = self.ledger_rows
        expected = set(
            subprocess.run(
                [
                    "git",
                    "ls-tree",
                    "-r",
                    "--name-only",
                    BASELINE,
                    "--",
                    *MIGRATION_ROOTS,
                ],
                cwd=ROOT,
                text=True,
                check=True,
                capture_output=True,
            ).stdout.splitlines()
        )
        declared = [row["legacy_path"] for row in rows]
        self.assertEqual(declared, sorted(declared))
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(expected, set(declared))
        required = {
            "legacy_path",
            "stable_path",
            "artifact_id",
            "action",
            "replacement",
            "source_commit",
            "reason",
        }
        destructive = {"merge", "delete"}
        for row in rows:
            with self.subTest(path=row["legacy_path"]):
                self.assertEqual(required, set(row))
                self.assertIn(
                    row["action"],
                    {"archive", "delete", "merge", "move", "retain", "rewrite"},
                )
                self.assertEqual(
                    BASELINE,
                    row["source_commit"],
                )
                self.assertTrue(row["reason"])
                if row["action"] == "delete":
                    self.assertIsNone(row["stable_path"])
                else:
                    self.assertIsInstance(row["stable_path"], str)
                    self.assertTrue(row["stable_path"])
                if row["action"] in destructive:
                    self.assertIsInstance(row["replacement"], str)
                    self.assertTrue(row["replacement"])
                elif row["action"] != "archive":
                    self.assertIsNone(row["replacement"])

    def test_ledger_targets_match_stable_typed_taxonomy(self) -> None:
        for row in self.ledger_rows:
            with self.subTest(path=row["legacy_path"]):
                target = row["stable_path"]
                replacement = row["replacement"]
                if target is not None:
                    self.assertIsNotNone(stable_target_type(target), target)
                    parts = PurePosixPath(target).parts
                    self.assertNotIn("docs/04.execution", target)
                    self.assertNotIn("README.md/", target)
                    self.assertFalse(
                        any(re.fullmatch(r"[0-9]{4}", part) for part in parts)
                    )
                    self.assertFalse(
                        any(
                            re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-", part)
                            for part in parts
                        )
                    )
                    self.assertFalse(
                        target.startswith(
                            (
                                "docs/05.operations/guides/",
                                "docs/05.operations/policies/",
                                "docs/05.operations/runbooks/",
                            )
                        )
                    )
                if replacement is not None:
                    self.assertNotEqual(row["legacy_path"], replacement)
                    if row["action"] == "archive":
                        self.assertNotEqual(target, replacement)
                    self.assertIsNotNone(stable_target_type(replacement), replacement)

                if target and "/changes/chg-" in target:
                    match = re.fullmatch(
                        r"docs/98\.archive/changes/chg-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    if role == "plan":
                        self.assertEqual(f"plan-{identity}", row["artifact_id"])
                    else:
                        self.assertRegex(
                            str(row["artifact_id"]), rf"^task-{identity}-[0-9]{{2}}$"
                        )

    def test_ledger_artifact_ids_match_target_profile_identities(self) -> None:
        direct_profiles = {
            "prd": (r".*/prd-([0-9]{4})-[^/]+\.md", "prd"),
            "ad": (r".*/ad-([0-9]{4})-[^/]+\.md", "ad"),
            "adr": (r".*/adr-([0-9]{4})-[^/]+\.md", "adr"),
            "spec": (r".*/spec-([0-9]{4})-[^/]+/spec\.md", "spec"),
            "event": (r".*/inc-([0-9]{4})-[^/]+/incident\.md", "inc"),
            "release": (r".*/rel-([0-9]{4})-[^/]+/release\.md", "rel"),
            "reference": (
                r".*/ref-([0-9]{4})-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)",
                "ref",
            ),
            "migration": (r".*/mig-([0-9]{4})-[^/]+\.md", "mig"),
        }
        for row in self.ledger_rows:
            target = row["stable_path"]
            if target is None:
                continue
            target_type = stable_target_type(target)
            artifact_id = row["artifact_id"]
            with self.subTest(path=row["legacy_path"], target=target):
                if target_type == "readme":
                    self.assertIsNone(artifact_id)
                    continue
                self.assertIsInstance(artifact_id, str)
                if target_type in direct_profiles:
                    pattern, prefix = direct_profiles[target_type]
                    match = re.fullmatch(pattern, target)
                    self.assertIsNotNone(match)
                    self.assertEqual(f"{prefix}-{match.group(1)}", artifact_id)
                elif target_type in {"plan", "task"}:
                    match = re.fullmatch(
                        r"docs/03\.specs/spec-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    expected = (
                        f"plan-{identity}" if role == "plan" else f"task-{identity}-01"
                    )
                    self.assertEqual(expected, artifact_id)
                elif target_type == "ops-role":
                    match = re.fullmatch(
                        r"docs/05\.operations/[^/]+/ops-([0-9]{4})-[^/]+/(guide|policy|runbook)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    self.assertEqual(f"{role}-{identity}", artifact_id)
                elif target_type == "change":
                    match = re.fullmatch(
                        r"docs/98\.archive/changes/chg-([0-9]{4})-[^/]+/(plan|task)\.md",
                        target,
                    )
                    self.assertIsNotNone(match)
                    identity, role = match.groups()
                    if role == "plan":
                        self.assertEqual(f"plan-{identity}", artifact_id)
                    else:
                        self.assertRegex(artifact_id, rf"^task-{identity}-[0-9]{{2}}$")
                    target_path = ROOT / target
                    if target_path.is_file():
                        target_metadata = frontmatter(
                            target_path.read_text(encoding="utf-8")
                        )
                        self.assertEqual(
                            target_metadata.get("artifact_id"), artifact_id
                        )
                elif target_type == "tombstone":
                    filename = PurePosixPath(target).stem
                    self.assertTrue(
                        filename.startswith(f"{artifact_id}-")
                        or filename == artifact_id
                    )

    def test_tombstones_are_terminal_and_only_name_active_replacements(self) -> None:
        for row in self.ledger_rows:
            if row["action"] != "archive":
                continue
            with self.subTest(path=row["legacy_path"]):
                metadata = frontmatter(git_text(row["legacy_path"]))
                self.assertIn(
                    metadata.get("status"), {"completed", "superseded", "archived"}
                )
                self.assertTrue(
                    str(row["stable_path"]).startswith("docs/98.archive/tombstones/")
                )
                replacement = row["replacement"]
                if replacement is not None:
                    self.assertFalse(str(replacement).startswith("docs/98.archive/"))

    def test_link_form_tombstone_replacements_are_parsed(self) -> None:
        for legacy_path, expected in LINK_FORM_BASELINE_DECLARATIONS.items():
            with self.subTest(path=legacy_path):
                self.assertEqual(
                    expected,
                    tuple(
                        declared_tombstone_replacements(
                            git_text(legacy_path), legacy_path
                        )
                    ),
                )
        self.assertEqual(
            ["docs/05.operations/example.md"],
            repository_docs_targets(
                "[local](../05.operations/example.md#procedure) "
                "[external](https://example.com/docs/ignored.md)",
                "docs/98.archive/tombstone.md",
            ),
        )

    def test_baseline_tombstone_replacements_are_preserved_as_stable_targets(
        self,
    ) -> None:
        index_replacements: dict[str, list[str]] = {}
        index_path = "docs/98.archive/README.md"
        for line in git_text(index_path).splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 4:
                continue
            archived_paths = repository_docs_targets(cells[1], index_path)
            replacements = repository_docs_targets(cells[3], index_path)
            if (
                len(archived_paths) == 1
                and archived_paths[0].startswith("docs/98.archive/05.operations/")
                and replacements
            ):
                index_replacements[archived_paths[0]] = replacements

        checked: set[str] = set()
        self.assertEqual(9, len(index_replacements))
        for legacy_path in sorted(index_replacements):
            self.assertIn(legacy_path, self.ledger_by_path)
            row = self.ledger_by_path[legacy_path]
            declarations = declared_tombstone_replacements(
                git_text(legacy_path), legacy_path
            )
            checked.add(legacy_path)
            with self.subTest(path=legacy_path):
                self.assertEqual("archive", row["action"])
                self.assertTrue(declarations)
                self.assertEqual(len(declarations), len(set(declarations)))
                self.assertEqual(declarations, index_replacements.get(legacy_path))
                translated: list[str] = []
                for declaration in declarations:
                    self.assertIn(declaration, self.ledger_by_path)
                    target = self.ledger_by_path[declaration]["stable_path"]
                    self.assertIsInstance(target, str)
                    canonical_target = canonical_current_path(str(target))
                    self.assertFalse(canonical_target.startswith("docs/98.archive/"))
                    self.assertIsNotNone(
                        stable_target_type(canonical_target), canonical_target
                    )
                    translated.append(canonical_target)

                self.assertEqual([], replacement_preservation_errors(row, translated))
                if legacy_path in KNOWN_TOMBSTONE_REPLACEMENTS:
                    self.assertEqual(
                        KNOWN_TOMBSTONE_REPLACEMENTS[legacy_path],
                        tuple(translated),
                    )

        known_paths = set(KNOWN_TOMBSTONE_REPLACEMENTS)
        self.assertEqual(known_paths, checked)

    def test_null_link_form_replacement_mutation_is_rejected(self) -> None:
        legacy_path = (
            "docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md"
        )
        declarations = declared_tombstone_replacements(
            git_text(legacy_path), legacy_path
        )
        translated = [
            str(self.ledger_by_path[declaration]["stable_path"])
            for declaration in declarations
        ]
        mutated = dict(self.ledger_by_path[legacy_path])
        mutated["replacement"] = None
        self.assertIn(
            "replacement-null",
            replacement_preservation_errors(mutated, translated),
        )

    def test_completed_linked_plan_task_pairs_share_typed_change_packet(self) -> None:
        plans_by_id: dict[str, str] = {}
        plans_by_slug: dict[str, str] = {}
        for path in self.ledger_by_path:
            if not path.startswith("docs/04.execution/plans/") or path.endswith(
                "README.md"
            ):
                continue
            metadata = frontmatter(git_text(path))
            if isinstance(metadata.get("artifact_id"), str):
                plans_by_id[str(metadata["artifact_id"])] = path
            slug = PurePosixPath(path).stem.removesuffix("-plan")
            plans_by_slug[slug] = path

        pairs: set[tuple[str, str]] = set()
        for task_path in self.ledger_by_path:
            if not task_path.startswith(
                "docs/04.execution/tasks/"
            ) or task_path.endswith("README.md"):
                continue
            body = git_text(task_path)
            metadata = frontmatter(body)
            if metadata.get("status") != "completed":
                continue
            paired = False
            for parent in metadata.get("parent_ids") or []:
                if str(parent) in plans_by_id:
                    pairs.add((plans_by_id[str(parent)], task_path))
                    paired = True
                    break
            task_slug = PurePosixPath(task_path).stem.removesuffix("-tasks")
            if not paired and task_slug in plans_by_slug:
                pairs.add((plans_by_slug[task_slug], task_path))

        self.assertGreater(len(pairs), 80)
        for plan_path, task_path in sorted(pairs):
            with self.subTest(plan=plan_path, task=task_path):
                plan = self.ledger_by_path[plan_path]
                task = self.ledger_by_path[task_path]
                self.assertEqual(
                    PurePosixPath(plan["stable_path"]).parent,
                    PurePosixPath(task["stable_path"]).parent,
                )
                plan_match = re.fullmatch(r"plan-([0-9]{4})", str(plan["artifact_id"]))
                task_match = re.fullmatch(
                    r"task-([0-9]{4})-[0-9]{2}", str(task["artifact_id"])
                )
                self.assertIsNotNone(plan_match)
                self.assertIsNotNone(task_match)
                self.assertEqual(plan_match.group(1), task_match.group(1))

    def test_duplicate_targets_have_exactly_one_non_merge_owner(self) -> None:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in self.ledger_rows:
            if row["stable_path"] is not None:
                grouped[str(row["stable_path"])].append(row)
        duplicates = {target: rows for target, rows in grouped.items() if len(rows) > 1}
        self.assertTrue(duplicates)
        for target, rows in duplicates.items():
            with self.subTest(target=target):
                owners = [row for row in rows if row["action"] != "merge"]
                self.assertEqual(1, len(owners))
                self.assertTrue(
                    all(
                        row["action"] == "merge" for row in rows if row is not owners[0]
                    )
                )

    def test_current_archived_capabilities_are_restored_to_stage03(self) -> None:
        for identity, slug in (
            (123, "agentic-engineering-audit-remediation"),
            (131, "document-corpus-lifecycle-migration-foundation"),
            (132, "agent-governance-harness-convergence"),
            (133, "target-surface-contract-convergence"),
        ):
            path = f"docs/98.archive/03.specs/{identity}-{slug}/spec.md"
            row = self.ledger_by_path[path]
            self.assertEqual("move", row["action"])
            self.assertEqual(f"spec-{identity:04d}", row["artifact_id"])
            self.assertEqual(
                f"docs/03.specs/spec-{identity:04d}-{slug}/spec.md",
                row["stable_path"],
            )
            self.assertIsNone(row["replacement"])
            self.assertIn("current", row["reason"])
