from __future__ import annotations

import contextlib
import dataclasses
import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest
from types import MappingProxyType
from unittest import mock

from scripts.lib.document_governance import identity_history
from scripts.lib.document_governance.identity_history import (
    IDENTITY_PREFIX_SPACES,
    IdentityHistoryError,
    IssuedIdentities,
    allocate_identity,
    collect_issued_identities,
    cutover_findings,
    rehearse_allocation,
    reserve_number,
    validate_identity_history,
)
from scripts.lib.document_governance.metadata.profile import (
    build_registry_profiles,
    infer_artifact_type,
)
from scripts.lib.document_governance.registry import (
    DEFAULT_REGISTRY,
    load_registry,
    validate_registry,
)

LEGACY_REQUIREMENT = pathlib.PurePosixPath("docs/01.requirements/prd-0042-preserved.md")


# The two real-lineage transition tests scan every merge between the approved
# baseline and HEAD, so against a moving HEAD their Git output and time grow
# with each merged PR until the scan bound fails them. They run on a detached
# checkout of this fixed commit (#141) instead: 23 MiB and about 20 s against
# the 64 MiB and 45 s bounds, constant from now on. The production check scans
# only the PR's own merges and is unaffected.
PINNED_LINEAGE_COMMIT = "4c6d211129615eab372d720ebd209b6c27618c86"


@contextlib.contextmanager
def pinned_lineage_root():
    repo = pathlib.Path(__file__).resolve().parents[3]
    with tempfile.TemporaryDirectory() as directory:
        checkout = pathlib.Path(directory) / "lineage"
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "worktree",
                "add",
                "--detach",
                "-q",
                str(checkout),
                PINNED_LINEAGE_COMMIT,
            ],
            check=True,
        )
        try:
            yield checkout
        finally:
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "worktree",
                    "remove",
                    "--force",
                    str(checkout),
                ],
                check=True,
            )


def _registry_bytes_with_live_spec(number: int) -> bytes:
    """Registry file bytes with one Spec number treated as still issued."""

    import json

    from scripts.lib.document_governance.registry import DEFAULT_REGISTRY

    raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
    spec = raw["identity_spaces"]["spec"]
    spec["reserved_history"] = [n for n in spec["reserved_history"] if n != number]
    return (json.dumps(raw, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _registry_with_live_spec(number: int):
    """The repository Registry, with one Spec number treated as still issued.

    These fixtures reuse SPEC-0104, which this repository has since retired.
    """

    registry = load_registry()
    spaces = dict(registry.identity_spaces)
    spec = spaces["spec"]
    spaces["spec"] = dataclasses.replace(
        spec,
        reserved_history=tuple(n for n in spec.reserved_history if n != number),
    )
    return dataclasses.replace(registry, identity_spaces=MappingProxyType(spaces))


class IdentityHistoryTests(unittest.TestCase):
    def test_incident_year_does_not_consume_allocation_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            fixtures = (
                ("2026/inc-0002-example/incident.md", "inc-2026-0002"),
                ("2026/inc-0002-example/postmortem.md", "inc-2026-0002-PM"),
            )
            for relative, artifact in fixtures:
                path = root / "docs/05.operations/incidents" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"---\nartifact_id: {artifact}\n---\n")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "incident fixtures")
            issued = collect_issued_identities(root)
            self.assertEqual(frozenset({2}), issued.numbers["incident"])

    def test_current_classifier_rejects_legacy_requirement_path(self) -> None:
        profiles = build_registry_profiles(load_registry())
        self.assertEqual(
            "unsupported",
            infer_artifact_type(pathlib.Path(LEGACY_REQUIREMENT), profiles),
        )

    def test_history_reader_parses_legacy_requirement_children(self) -> None:
        historical, declarations = (
            identity_history.parse_historical_requirement_declarations(
                {
                    "docs/01.requirements/prd-0042-preserved.md": (
                        "## Requirements\n"
                        "### Functional requirements\nPRD-0042-R0001\n"
                        "### Non-functional requirements\nPRD-0042-R0002\n"
                    )
                }
            )
        )
        self.assertTrue(historical)
        self.assertEqual({1}, declarations["REQ-0042.FR"])
        self.assertEqual({2}, declarations["REQ-0042.NFR"])

    def test_current_registry_delegates_old_grammar_to_history_reader(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        original = identity_history.parse_historical_requirement_declarations
        with mock.patch.object(
            identity_history,
            "parse_historical_requirement_declarations",
            wraps=original,
        ) as historical_parser:
            registry_module.load_trusted_requirement_allocation_baseline(":")

        historical_parser.assert_called_once()
        registry_source = pathlib.Path(registry_module.__file__).read_text(
            encoding="utf-8"
        )
        self.assertNotIn("_TRUSTED_LEGACY_REQUIREMENT_SECTION", registry_source)
        self.assertNotIn("_TRUSTED_LEGACY_CHILD_ID", registry_source)

    def test_identity_scan_does_not_read_patch_text(self) -> None:
        """Identity history cost must not grow with every historical diff."""

        source = (
            pathlib.Path(__file__).resolve().parents[3]
            / "scripts/lib/document_governance/identity_history.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn('"-p"', source)
        self.assertNotIn('"--patch"', source)
        self.assertNotIn('"-G"', source)
        self.assertNotIn("_record_history_patch", source)
        self.assertIn("MAX_GIT_OUTPUT_BYTES = 8 * 1024 * 1024", source)
        self.assertNotIn(
            "MAX_GIT_OUTPUT_BYTES = 64 * 1024 * 1024",
            source,
        )

    def test_predecessor_without_a_registry_fails_closed(self) -> None:
        with pinned_lineage_root() as root:
            base = self._git(root, "rev-list", "--max-parents=0", "HEAD").split()[0]
            self.assertEqual(
                "",
                self._git(
                    root, "ls-tree", base, "--", "docs/99.templates/registry.json"
                ),
            )
            with self.assertRaisesRegex(IdentityHistoryError, "lacks a Registry"):
                identity_history.validate_allocation_transition(
                    root,
                    load_registry(),
                    {"docs/03.specs/0008-workflow/spec.md": "SPEC-0008"},
                    base,
                )

    def test_ordinary_allocation_transition_reads_each_blob_once(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q", "-b", "main")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            spec = root / "docs/03.specs/0001-example/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text("---\nartifact_id: SPEC-0001\n---\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "base")
            base = self._git(root, "rev-parse", "HEAD").strip()
            # Two forks carry the same Registry and Spec blobs into one merge
            # after the base, so the merge scan meets each blob more than once.
            self._git(root, "checkout", "-qb", "fork")
            (root / "fork.md").write_text("fork\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "fork")
            self._git(root, "checkout", "-q", "main")
            (root / "main.md").write_text("main\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "main")
            self._git(root, "merge", "-q", "--no-edit", "fork")
            real = identity_history._run_git
            blobs: list[str] = []

            def counting(root_arg, args, **kwargs):
                if tuple(args[:2]) == ("cat-file", "blob"):
                    blobs.append(args[2])
                return real(root_arg, args, **kwargs)

            with mock.patch.object(identity_history, "_run_git", counting):
                identity_history.validate_allocation_transition(
                    root,
                    load_registry(),
                    {"docs/03.specs/0001-example/spec.md": "SPEC-0001"},
                    base,
                )
        self.assertTrue(blobs, "the transition read no blob")
        self.assertEqual(len(blobs), len(set(blobs)))

    def test_removed_identity_must_be_reserved_in_the_same_change(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        registry = load_registry()
        adr = registry.identity_spaces["adr"]
        number = next(
            n for n in range(1, adr.high_water + 1) if n not in adr.reserved_history
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            document = root / f"docs/02.architecture/decisions/{number:04d}-x.md"
            document.parent.mkdir(parents=True)
            document.write_text(f'---\nartifact_id: "ADR-{number:04d}"\n---\n')
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "base")
            base = self._git(root, "rev-parse", "HEAD").strip()

            def codes(candidate):
                return {
                    item.code
                    for item in identity_history.validate_allocation_transition(
                        root, candidate, {}, base
                    )
                }

            self.assertIn("identity-retired-not-reserved", codes(registry))
            spaces = dict(registry.identity_spaces)
            spaces["adr"] = dataclasses.replace(
                adr, reserved_history=(*adr.reserved_history, number)
            )
            reserved = dataclasses.replace(
                registry, identity_spaces=MappingProxyType(spaces)
            )
            self.assertNotIn("identity-retired-not-reserved", codes(reserved))

    def test_retirement_check_spares_moves_and_partial_removal(self) -> None:
        """A moved document or a package that loses one Task retires nothing;
        a removed requirement child must be reserved like a package."""

        from scripts.lib.document_governance import registry as registry_module

        registry = load_registry()
        spaces = registry.identity_spaces

        def live(space):
            return next(
                n
                for n in range(1, space.high_water + 1)
                if n not in space.reserved_history
            )

        adr, spec = live(spaces["adr"]), live(spaces["spec"])
        child_name = next(
            name
            for name in spaces["requirement"].child_spaces
            if name.endswith(".FR")
            and int(name[4:8]) not in spaces["requirement"].reserved_history
            and spaces["requirement"].child_spaces[name].high_water >= 3
            and not {2, 3}
            & set(spaces["requirement"].child_spaces[name].reserved_history)
        )
        package = int(child_name[4:8])
        requirement_path = f"docs/01.requirements/{package:04d}-x.md"
        requirement_id = f"REQ-{package:04d}"
        unissued = spaces["requirement"].child_spaces[child_name].high_water + 5
        # FR-0002 is issued; the unissued mention models a malformed
        # cross-reference whose removal retires nothing.
        child_line = (
            f"{requirement_id}-FR-0001\n{requirement_id}-FR-0002\n"
            f"see {requirement_id}-FR-{unissued:04d}\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            files = {
                "docs/99.templates/registry.json": (
                    registry_module.DEFAULT_REGISTRY.read_text(encoding="utf-8")
                ),
                f"docs/02.architecture/decisions/{adr:04d}-old.md": (
                    f'---\nartifact_id: "ADR-{adr:04d}"\n---\n'
                ),
                f"docs/03.specs/{spec:04d}-x/spec.md": (
                    f'---\nartifact_id: "SPEC-{spec:04d}"\n---\n'
                ),
                f"docs/03.specs/{spec:04d}-x/tasks/tsk-0001-x.md": (
                    f'---\nartifact_id: "SPEC-{spec:04d}-TSK-0001"\n---\n'
                ),
                requirement_path: (
                    f'---\nartifact_id: "{requirement_id}"\n---\n{child_line}'
                ),
                # Not an identified body: its mention never counts as issued.
                "docs/01.requirements/README.md": f"{requirement_id}-FR-0003\n",
            }
            for relative, text in files.items():
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).write_text(text, encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "base")
            base = self._git(root, "rev-parse", "HEAD").strip()
            current = {
                f"docs/02.architecture/decisions/{adr:04d}-new.md": f"ADR-{adr:04d}",
                f"docs/03.specs/{spec:04d}-x/spec.md": f"SPEC-{spec:04d}",
                requirement_path: requirement_id,
            }

            def retired(candidate):
                return {
                    item.path
                    for item in identity_history.validate_allocation_transition(
                        root, candidate, current, base
                    )
                    if item.code == "identity-retired-not-reserved"
                }

            (root / requirement_path).write_text(
                f'---\nartifact_id: "{requirement_id}"\n---\n{requirement_id}-FR-0001\n',
                encoding="utf-8",
            )
            child_path = f"identity_spaces.requirement.child_spaces.{child_name}"
            self.assertEqual({child_path}, retired(registry))

            requirement = spaces["requirement"]
            children = dict(requirement.child_spaces)
            child = children[child_name]
            children[child_name] = dataclasses.replace(
                child, reserved_history=(*child.reserved_history, 2)
            )
            reserved = dict(spaces)
            reserved["requirement"] = dataclasses.replace(
                requirement, child_spaces=MappingProxyType(children)
            )
            self.assertEqual(
                set(),
                retired(
                    dataclasses.replace(
                        registry, identity_spaces=MappingProxyType(reserved)
                    )
                ),
            )

            # Preserving the whole body elsewhere keeps every child issued.
            preserved = f"docs/98.archive/completed/01.requirements/{package:04d}-x.md"
            (root / preserved).parent.mkdir(parents=True)
            (root / preserved).write_text(
                f'---\nartifact_id: "{requirement_id}"\n---\n{child_line}',
                encoding="utf-8",
            )
            del current[requirement_path]
            current[preserved] = requirement_id
            self.assertEqual(set(), retired(registry))

    def test_reserved_history_cannot_drop_a_number(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "registry")
            base = self._git(root, "rev-parse", "HEAD").strip()
            registry = load_registry()

            def codes(candidate):
                return {
                    item.code
                    for item in identity_history.validate_allocation_transition(
                        root, candidate, {}, base
                    )
                }

            self.assertNotIn("identity-reserved-history-dropped", codes(registry))
            spaces = dict(registry.identity_spaces)
            spaces["adr"] = dataclasses.replace(
                spaces["adr"], reserved_history=spaces["adr"].reserved_history[1:]
            )
            dropped = dataclasses.replace(
                registry, identity_spaces=MappingProxyType(spaces)
            )
            self.assertIn("identity-reserved-history-dropped", codes(dropped))

            live_adr = registry.identity_spaces["adr"].reserved_history[0]
            live = {
                item.code
                for item in identity_history.validate_allocation_transition(
                    root,
                    registry,
                    {
                        f"docs/02.architecture/decisions/{live_adr:04d}-x.md": (
                            f"ADR-{live_adr:04d}"
                        )
                    },
                    base,
                )
            }
            self.assertIn("identity-reserved-history-live", live)

    def test_generic_allocation_rejects_retired_reuse_and_requires_atomic_advance(
        self,
    ) -> None:

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(_registry_bytes_with_live_spec(104))
            spec = root / "docs/03.specs/0104-original/spec.md"
            spec.parent.mkdir(parents=True)
            spec.write_text("---\nartifact_id: SPEC-0104\n---\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue identity")
            previous = self._git(root, "rev-parse", "HEAD").strip()
            registry = _registry_with_live_spec(104)
            current = {"docs/03.specs/0104-moved/spec.md": "SPEC-0104"}
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, registry, current, previous
                ),
            )
            spec.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "retire identity")
            retired = self._git(root, "rev-parse", "HEAD").strip()
            findings = identity_history.validate_allocation_transition(
                root, registry, current, retired
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})
            # Derive the unallocated number rather than pin one. A literal here
            # is consumed the moment real work issues that identity, and the
            # test then asserts that a legitimately allocated number is not
            # allocated. `SPEC-0154` was the pin and SPEC-0154 was issued.
            unallocated = registry.identity_spaces["spec"].high_water + 1
            introduced = {
                f"docs/03.specs/{unallocated:04d}-new/spec.md": f"SPEC-{unallocated:04d}"
            }
            findings = identity_history.validate_allocation_transition(
                root, registry, introduced, retired
            )
            self.assertIn(
                "identity-allocation-not-advanced", {item.code for item in findings}
            )
            spaces = dict(registry.identity_spaces)
            spaces["spec"] = dataclasses.replace(
                spaces["spec"], high_water=unallocated, next_number=unallocated + 1
            )
            advanced = dataclasses.replace(
                registry, identity_spaces=MappingProxyType(spaces)
            )
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, advanced, introduced, retired
                ),
            )

    def test_merged_lineage_proves_canonical_identity_issuance_only(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q", "-b", "main")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            registry_path = root / "docs/99.templates/registry.json"
            registry_path.parent.mkdir(parents=True)
            raw_registry = json.loads(registry_module.DEFAULT_REGISTRY.read_text())
            issued = raw_registry["identity_spaces"]["spec"]["high_water"] + 10

            def write_registry(high_water: int) -> None:
                raw_registry["identity_spaces"]["spec"].update(
                    {"high_water": high_water, "next_number": high_water + 1}
                )
                registry_path.write_text(json.dumps(raw_registry), encoding="utf-8")

            write_registry(issued - 1)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "allocation baseline")
            fork = self._git(root, "rev-parse", "HEAD").strip()

            self._git(root, "checkout", "-qb", "issued-lineage")
            canonical = root / f"docs/03.specs/{issued:04d}-fixture/spec.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text(
                f"---\nartifact_id: SPEC-{issued:04d}\n---\n", encoding="utf-8"
            )
            write_registry(issued)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue identity")

            self._git(root, "checkout", "-qb", "conflicting-lineage", fork)
            conflicting = root / f"docs/03.specs/{issued:04d}-other/spec.md"
            conflicting.parent.mkdir(parents=True)
            conflicting.write_text(
                f"---\nartifact_id: SPEC-{issued:04d}\n---\n", encoding="utf-8"
            )
            write_registry(issued)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue conflicting identity")

            self._git(root, "checkout", "-q", "main")
            write_registry(issued + 1)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "reserve later identity")
            base = self._git(root, "rev-parse", "HEAD").strip()
            merge = subprocess.run(
                ["git", "merge", "-qm", "merge issued lineage", "issued-lineage"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, merge.returncode)
            write_registry(issued + 1)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "merge issued lineage")

            registry = load_registry(registry_path)
            current = {canonical.relative_to(root).as_posix(): f"SPEC-{issued:04d}"}
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, registry, current, base
                ),
            )
            preserved = {
                (
                    f"docs/98.archive/completed/03.specs/{issued:04d}-fixture/spec.md"
                ): f"SPEC-{issued:04d}"
            }
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, registry, preserved, base
                ),
            )

            collision = dict(current)
            collision[f"docs/03.specs/{issued:04d}-collision/spec.md"] = (
                f"SPEC-{issued:04d}"
            )
            findings = identity_history.validate_allocation_transition(
                root, registry, collision, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            merge = subprocess.run(
                [
                    "git",
                    "merge",
                    "--no-ff",
                    "-qm",
                    "merge conflicting lineage",
                    "conflicting-lineage",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, merge.returncode)
            conflicting.unlink()
            write_registry(issued + 1)
            self._git(root, "add", "-A")
            self._git(root, "commit", "-qm", "resolve conflicting issuance")
            findings = identity_history.validate_allocation_transition(
                root, registry, current, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            self._git(root, "checkout", "-qb", "post-reservation", base)
            canonical.parent.mkdir(parents=True)
            canonical.write_text(
                f"---\nartifact_id: SPEC-{issued:04d}\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "reuse reserved identity")
            self._git(root, "checkout", "-qb", "laundering-main", base)
            self._git(
                root,
                "merge",
                "--no-ff",
                "-qm",
                "merge post-reservation reuse",
                "post-reservation",
            )
            findings = identity_history.validate_allocation_transition(
                root, registry, current, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            self._git(root, "checkout", "-q", "--detach", base)
            findings = identity_history.validate_allocation_transition(
                root, registry, current, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

    def test_predecessor_archive_identity_is_not_new_issuance(self) -> None:
        from scripts.lib.document_governance import registry as registry_module

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            registry_path = root / "docs/99.templates/registry.json"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_bytes(registry_module.DEFAULT_REGISTRY.read_bytes())
            registry = load_registry(registry_path)
            issued = registry.identity_spaces["spec"].high_water
            preserved = root / (
                f"docs/98.archive/completed/03.specs/{issued:04d}-fixture/spec.md"
            )
            preserved.parent.mkdir(parents=True)
            preserved.write_text(
                f"---\nartifact_id: SPEC-{issued:04d}\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "preserve issued identity")
            base = self._git(root, "rev-parse", "HEAD").strip()
            current = {preserved.relative_to(root).as_posix(): f"SPEC-{issued:04d}"}

            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root, registry, current, base
                ),
            )

    def test_deleted_package_identity_requires_exact_git_recovery(self) -> None:

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            registry_path = root / "docs/99.templates/registry.json"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_bytes(_registry_bytes_with_live_spec(104))
            decision = root / "docs/03.specs/0104-decision/tasks/tsk-0001-recovery.md"
            decision.parent.mkdir(parents=True)
            decision.write_text(
                "---\nartifact_id: SPEC-0104-TSK-0001\n---\n", encoding="utf-8"
            )
            source = (
                root / "docs/90.references/research/0085-workspace/REQUEST-SCOPE.md"
            )
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nartifact_id: RES-0085-SCOPE\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue incomplete package")
            source_commit = self._git(root, "rev-parse", "HEAD").strip()
            source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete incomplete package")
            base = self._git(root, "rev-parse", "HEAD").strip()
            target_path = (
                "docs/90.references/research/0085-workspace/m0001-request-scope.md"
            )
            decision_path = decision.relative_to(root).as_posix()
            current = {
                target_path: "RES-0085-m0001",
                decision_path: "SPEC-0104-TSK-0001",
            }

            findings = identity_history.validate_allocation_transition(
                root, _registry_with_live_spec(104), current, base
            )
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            recovery = {
                target_path: {
                    "source_commit": source_commit,
                    "source_path": source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                    "decision_path": decision_path,
                    "decision_artifact_id": "SPEC-0104-TSK-0001",
                    "disposition": "consolidated",
                }
            }
            decision_evidence = {
                decision_path: [
                    {
                        "source_commit": source_commit,
                        "source_path": source.relative_to(root).as_posix(),
                        "source_artifact_id": "RES-0085-SCOPE",
                        "target_path": target_path,
                        "target_artifact_id": "RES-0085-m0001",
                        "disposition": "consolidated",
                    }
                ]
            }
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root,
                    _registry_with_live_spec(104),
                    current,
                    base,
                    recovery_evidence=recovery,
                    decision_evidence=decision_evidence,
                ),
            )

            target = root / target_path
            target.write_text(
                "---\nartifact_id: RES-0085-m0001\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "introduce recovered package")
            target_base = self._git(root, "rev-parse", "HEAD").strip()
            self.assertEqual(
                (),
                identity_history.validate_allocation_transition(
                    root,
                    _registry_with_live_spec(104),
                    current,
                    target_base,
                    recovery_evidence=recovery,
                    decision_evidence=decision_evidence,
                ),
            )

            # Stage 98 holds no records (SPEC-0249): a Task under any archive
            # disposition is never a decision owner, so recovery fails closed.
            preserved_path = (
                "docs/98.archive/completed/03.specs/0104-decision/tasks/"
                "tsk-0001-recovery.md"
            )
            for disposition, allowed in (
                ("completed", False),
                ("superseded", False),
                ("retired", False),
            ):
                moved = preserved_path.replace("/completed/", f"/{disposition}/")
                with self.subTest(disposition=disposition):
                    findings = identity_history.validate_allocation_transition(
                        root,
                        _registry_with_live_spec(104),
                        {target_path: "RES-0085-m0001", moved: "SPEC-0104-TSK-0001"},
                        base,
                        recovery_evidence={
                            target_path: {
                                **recovery[target_path],
                                "decision_path": moved,
                            }
                        },
                        decision_evidence={moved: decision_evidence[decision_path]},
                    )
                    self.assertEqual(
                        allowed,
                        "identity-recovery-invalid"
                        not in {item.code for item in findings},
                        findings,
                    )

            recovery[target_path]["source_artifact_id"] = "RES-0084-SCOPE"
            findings = identity_history.validate_allocation_transition(
                root,
                _registry_with_live_spec(104),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})
            self.assertIn("identity-reuse-forbidden", {item.code for item in findings})

            recovery[target_path]["source_artifact_id"] = "RES-0085-SCOPE"
            findings = identity_history.validate_allocation_transition(
                root,
                _registry_with_live_spec(104),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence={},
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

            untyped_decision_path = "docs/03.specs/0104-decision/tasks/tsk-0001.md"
            recovery[target_path]["decision_path"] = untyped_decision_path
            current[untyped_decision_path] = "SPEC-0104-TSK-0001"
            decision_evidence[untyped_decision_path] = decision_evidence[decision_path]
            findings = identity_history.validate_allocation_transition(
                root,
                _registry_with_live_spec(104),
                current,
                base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})
            recovery[target_path]["decision_path"] = decision_path
            current.pop(untyped_decision_path)
            decision_evidence.pop(untyped_decision_path)

            canonical_source = (
                root / "docs/90.references/research/0085-workspace/README.md"
            )
            canonical_source.write_text(
                "---\nartifact_id: RES-0085\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue canonical package")
            canonical_commit = self._git(root, "rev-parse", "HEAD").strip()
            canonical_source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete canonical package")
            canonical_base = self._git(root, "rev-parse", "HEAD").strip()
            recovery[target_path].update(
                {
                    "source_commit": canonical_commit,
                    "source_path": canonical_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085",
                }
            )
            decision_evidence[decision_path][0].update(
                {
                    "source_commit": canonical_commit,
                    "source_path": canonical_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085",
                }
            )
            findings = identity_history.validate_allocation_transition(
                root,
                _registry_with_live_spec(104),
                current,
                canonical_base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

            foreign_source = (
                root / "docs/90.references/research/0084-other/REQUEST-SCOPE.md"
            )
            foreign_source.parent.mkdir(parents=True)
            foreign_source.write_text(
                "---\nartifact_id: RES-0085-SCOPE\n---\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "issue foreign legacy member")
            foreign_commit = self._git(root, "rev-parse", "HEAD").strip()
            foreign_source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete foreign legacy member")
            foreign_base = self._git(root, "rev-parse", "HEAD").strip()
            recovery[target_path].update(
                {
                    "source_commit": foreign_commit,
                    "source_path": foreign_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                }
            )
            decision_evidence[decision_path][0].update(
                {
                    "source_commit": foreign_commit,
                    "source_path": foreign_source.relative_to(root).as_posix(),
                    "source_artifact_id": "RES-0085-SCOPE",
                }
            )
            findings = identity_history.validate_allocation_transition(
                root,
                _registry_with_live_spec(104),
                current,
                foreign_base,
                recovery_evidence=recovery,
                decision_evidence=decision_evidence,
            )
            self.assertIn("identity-recovery-invalid", {item.code for item in findings})

    def test_missing_predecessor_registry_is_not_a_generic_bootstrap_exception(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Identity Fixture")
            self._git(root, "config", "user.email", "identity@example.invalid")
            source = root / "docs/99.templates/registry.json"
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps({}), encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "introduce registry")
            source.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete registry")
            previous = self._git(root, "rev-parse", "HEAD").strip()
            with self.assertRaises(IdentityHistoryError):
                identity_history.validate_allocation_transition(
                    root, load_registry(), {}, previous
                )

    def _git(self, root: pathlib.Path, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout

    def test_deleted_lowercase_package_and_child_ids_remain_reserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            requirement = root / "docs/01.requirements/prd-0042-example.md"
            requirement.parent.mkdir(parents=True)
            requirement.write_text(
                "---\nartifact_id: prd-0042\n---\n\n"
                "**PRD-0042-R0043**: old functional requirement\n"
                "**PRD-0042-NFR-0044**: old non-functional requirement\n"
                "**IFR-0042-R0045**: old interface requirement\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add deleted requirement")
            second = root / "docs/01.requirements/req-0043-example.md"
            second.write_text(
                "---\nartifact_id: REQ-0043\n---\n\n"
                "REQ-0043-FR-0043\nREQ-0043-NFR-0044\nREQ-0043-IF-0045\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add second requirement")
            requirement.unlink()
            second.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete requirement")

            issued = collect_issued_identities(root)

        self.assertGreaterEqual(issued.high_water("requirement"), 42)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.FR"), 43)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.NFR"), 44)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0042.IF"), 45)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.FR"), 43)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.NFR"), 44)
        self.assertGreaterEqual(issued.high_water("requirement.REQ-0043.IF"), 45)

    def test_stage90_category_not_legacy_ref_filename_owns_identity_space(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            audit = root / "docs/90.references/audits/ref-0023-fixture.md"
            data = root / "docs/90.references/data/history/ref-0061-fixture.md"
            audit.parent.mkdir(parents=True)
            data.parent.mkdir(parents=True)
            audit.write_text("---\nartifact_id: AUD-0023\n---\n", encoding="utf-8")
            data.write_text("---\nartifact_id: DATA-0061\n---\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add Stage 90 fixtures")

            issued = collect_issued_identities(root)

        self.assertIn(23, issued.numbers["audit"])
        self.assertIn(61, issued.numbers["data"])
        self.assertNotIn(23, issued.numbers.get("research", frozenset()))
        self.assertNotIn(61, issued.numbers.get("research", frozenset()))

    def test_operations_prefixes_record_the_operations_subject_space(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            fixtures = (
                ("guides/01-common/0103-example.md", "GDE-0103"),
                ("policies/01-common/0104-example.md", "POL-0104"),
                ("runbooks/01-common/0105-example.md", "RUN-0105"),
                ("runbooks/01-common/0106-legacy.md", "RUNBOOK-0106"),
            )
            for relative, artifact in fixtures:
                path = root / "docs/05.operations" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"---\nartifact_id: {artifact}\n---\n")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "operations fixtures")

            issued = collect_issued_identities(root)

        self.assertEqual(
            frozenset({103, 104, 105}), issued.numbers["operations-subject"]
        )

    def test_every_numbered_registry_prefix_is_scanned(self) -> None:
        registry = json.loads(
            (
                pathlib.Path(__file__).resolve().parents[3]
                / "docs/99.templates/registry.json"
            ).read_text(encoding="utf-8")
        )
        patterns = set()

        def walk(node: object) -> None:
            if isinstance(node, dict):
                pattern = node.get("artifact_id_pattern")
                if isinstance(pattern, str):
                    patterns.add(pattern)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(registry)
        scanned = {prefix for prefix, _space, _root in IDENTITY_PREFIX_SPACES}
        special = ("REQ-", "inc-", "tomb-")
        for pattern in sorted(patterns):
            prefix = pattern.split("{", 1)[0]
            if prefix.startswith(special) or "{number" not in pattern:
                continue
            with self.subTest(pattern=pattern):
                self.assertIn(prefix.upper(), scanned)

    def test_registry_high_water_is_not_below_observed_history(self) -> None:
        # The real-tree scan is the full-profile metadata gate's job; its
        # result depends on local refs, so this test pins the rule instead.
        registry = load_registry()
        high_water = registry.identity_spaces["spec"].high_water

        def findings(observed: int) -> set[str]:
            issued = IssuedIdentities(MappingProxyType({"spec": frozenset({observed})}))
            return {
                finding.code for finding in validate_identity_history(registry, issued)
            }

        self.assertNotIn("identity-history-regression", findings(high_water))
        self.assertIn("identity-history-regression", findings(high_water + 1))

    def test_history_uses_only_bounded_object_name_scans(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[3]
        commands: list[tuple[str, ...]] = []
        real_run_git = identity_history._run_git

        def recording_run_git(
            repo: pathlib.Path,
            arguments: tuple[str, ...],
            **kwargs: object,
        ) -> str:
            commands.append(arguments)
            return real_run_git(repo, arguments, **kwargs)

        with mock.patch.object(
            identity_history,
            "_run_git",
            side_effect=recording_run_git,
        ):
            collect_issued_identities(root, refs=("HEAD",))

        history_commands = [
            command for command in commands if command[:2] == ("rev-list", "--objects")
        ]
        self.assertEqual(
            [
                ("rev-list", "--objects", "HEAD", "--", pathspec)
                for pathspec in identity_history.GIT_HISTORY_QUERIES
            ],
            history_commands,
        )
        grep_commands = [
            command for command in commands if command[:2] == ("grep", "-h")
        ]
        self.assertTrue(grep_commands)
        self.assertTrue(
            all(
                len(command) <= identity_history._GIT_GREP_BATCH_SIZE + 12
                for command in grep_commands
            )
        )
        self.assertTrue(
            all(
                token not in command
                for command in commands
                for token in ("-p", "--patch", "-G", "-S")
            )
        )

    def test_git_output_cap_terminates_stdout_and_stderr_producers_early(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            executable = root / "git"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import os, pathlib, signal, sys, time\n"
                "marker = pathlib.Path(os.environ['FAKE_GIT_MARKER'])\n"
                "def stop(*_):\n"
                "    marker.write_text('terminated', encoding='utf-8')\n"
                "    raise SystemExit(0)\n"
                "signal.signal(signal.SIGTERM, stop)\n"
                "target = int(os.environ['FAKE_GIT_FD'])\n"
                "chunk = b'x' * 4096\n"
                "while True:\n"
                "    os.write(target, chunk)\n"
                "    time.sleep(0.001)\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)

            for stream_name, descriptor in (("stdout", "1"), ("stderr", "2")):
                with self.subTest(stream=stream_name):
                    marker = root / f"{stream_name}.marker"
                    environment = {
                        "PATH": f"{root}{os.pathsep}{os.environ.get('PATH', '')}",
                        "FAKE_GIT_MARKER": str(marker),
                        "FAKE_GIT_FD": descriptor,
                    }
                    started = time.monotonic()
                    with (
                        mock.patch.dict(os.environ, environment),
                        self.assertRaisesRegex(
                            IdentityHistoryError,
                            "Git identity scan exceeded its output bound",
                        ),
                    ):
                        identity_history._run_git(
                            root,
                            ("adversarial",),
                            max_output_bytes=1024,
                            timeout_seconds=4,
                        )
                    self.assertLess(time.monotonic() - started, 2)
                    self.assertEqual("terminated", marker.read_text(encoding="utf-8"))

    def test_terminate_and_reap_waits_for_killed_child_and_surfaces_reap_failure(
        self,
    ) -> None:
        alive = True
        process = mock.Mock()
        process.poll.side_effect = lambda: None if alive else -9

        def wait(timeout: float | None = None) -> int:
            nonlocal alive
            if timeout is not None:
                raise subprocess.TimeoutExpired("fake-git", timeout)
            alive = False
            return -9

        process.wait.side_effect = wait
        identity_history._terminate_and_reap(process, None)

        self.assertIsNotNone(process.poll())
        process.kill.assert_called_once_with()
        process.wait.assert_called_once_with()

        failed = mock.Mock()
        failed.poll.return_value = None
        failed.wait.side_effect = OSError("wait failed")
        with self.assertRaisesRegex(
            IdentityHistoryError, "failed to reap bounded Git identity scan"
        ):
            identity_history._terminate_and_reap(failed, None)

    def test_history_rejects_an_issued_but_unregistered_package_child_space(
        self,
    ) -> None:
        registry = load_registry()
        requirement = registry.identity_spaces["requirement"]
        children = {
            key: value
            for key, value in requirement.child_spaces.items()
            if key != "REQ-0001.FR"
        }
        broken_requirement = dataclasses.replace(
            requirement, child_spaces=MappingProxyType(children)
        )
        broken_registry = dataclasses.replace(
            registry,
            identity_spaces=MappingProxyType(
                {
                    **registry.identity_spaces,
                    "requirement": broken_requirement,
                }
            ),
        )
        issued = IssuedIdentities(
            MappingProxyType({"requirement.REQ-0001.FR": frozenset({4})})
        )

        self.assertIn(
            "identity-history-space-missing",
            {
                finding.code
                for finding in validate_identity_history(broken_registry, issued)
            },
        )

    def test_rename_into_docs_uses_the_destination_path_for_added_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            source = root / "notes.md"
            source.write_text("artifact_id: note-0001\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add note")
            target = root / "docs/01.requirements/0099-example.md"
            target.parent.mkdir(parents=True)
            source.rename(target)
            target.write_text("artifact_id: REQ-0099\n", encoding="utf-8")
            self._git(root, "add", "-A")
            self._git(root, "commit", "-qm", "promote requirement")
            target.unlink()
            self._git(root, "add", "-u")
            self._git(root, "commit", "-qm", "delete requirement")

            issued = collect_issued_identities(root)

        self.assertGreaterEqual(issued.high_water("requirement"), 99)

    def test_default_scan_ignores_an_unmerged_branch_allocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q", "-b", "main")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            target = root / "docs/01.requirements/0098-example.md"
            target.parent.mkdir(parents=True)
            target.write_text("artifact_id: REQ-0098\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "main requirement")
            self._git(root, "switch", "-qc", "feature")
            other = root / "docs/01.requirements/0099-example.md"
            other.write_text("artifact_id: REQ-0099\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "branch requirement")
            self._git(root, "switch", "-q", "main")

            default = collect_issued_identities(root)
            every_ref = collect_issued_identities(root, refs=("--all",))

        self.assertEqual(98, default.high_water("requirement"))
        self.assertEqual(99, every_ref.high_water("requirement"))

    def test_deleted_worktree_source_is_history_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            source = root / "docs/90.references/research/0099-example/README.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "---\nartifact_id: RES-0099\n---\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add identity source")
            source.unlink()

            issued = collect_issued_identities(root)

        self.assertIn(99, issued.numbers["research"])

    def test_tracked_identity_source_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Registry Test")
            self._git(root, "config", "user.email", "registry@example.invalid")
            target = root / "target.md"
            target.write_text("artifact_id: REQ-0001\n", encoding="utf-8")
            link = root / "docs/01.requirements/0001-example.md"
            link.parent.mkdir(parents=True)
            link.symlink_to(target)
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "add unsafe identity source")

            with self.assertRaises(IdentityHistoryError):
                collect_issued_identities(root)


if __name__ == "__main__":
    unittest.main()


class GitPredicateTests(unittest.TestCase):
    """`git merge-base --is-ancestor` exits 1 to answer `false`, not to fail."""

    def _repo_with_two_unrelated_commits(self, root: pathlib.Path) -> tuple[str, str]:
        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True,
                text=True,
                check=True,
            )

        run("init", "-q")
        run("config", "core.hooksPath", "")
        run("config", "user.name", "Predicate Fixture")
        run("config", "user.email", "predicate@example.invalid")
        (root / "a.txt").write_text("a", encoding="utf-8")
        run("add", ".")
        run("commit", "-qm", "one")
        first = run("rev-parse", "HEAD").stdout.strip()
        run("checkout", "-q", "--orphan", "unrelated")
        (root / "b.txt").write_text("b", encoding="utf-8")
        run("add", ".")
        run("commit", "-qm", "two")
        second = run("rev-parse", "HEAD").stdout.strip()
        return first, second

    def test_false_predicate_is_an_answer_not_a_scan_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first, _ = self._repo_with_two_unrelated_commits(root)
            self.assertFalse(
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", first, "HEAD")
                )
            )

    def test_true_predicate_is_reported_as_true(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            _, second = self._repo_with_two_unrelated_commits(root)
            self.assertTrue(
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", second, "HEAD")
                )
            )

    def test_scan_failure_names_the_command_and_carries_git_stderr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self._repo_with_two_unrelated_commits(root)
            with self.assertRaises(IdentityHistoryError) as caught:
                identity_history.git_predicate(
                    root, ("merge-base", "--is-ancestor", "not-a-commit", "HEAD")
                )
            message = str(caught.exception)
            self.assertIn("merge-base --is-ancestor not-a-commit HEAD", message)
            self.assertNotEqual("bounded Git identity scan failed", message)


class IdentityNamespaceRehearsalTests(unittest.TestCase):
    """D-17/DOC-12: the next numbering namespace is prepared, not executed.

    After W11 the Q-07 cutover starts new Specs at SPEC-0001. These tests
    rehearse that allocator on a copy of the Registry, so no real number is
    issued and no reserved or historical identity is reissued.
    """

    def setUp(self) -> None:
        self.raw = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        self.before = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
        self.namespace = self.raw["identity_namespaces"]["next"]
        self.baseline = self.namespace["id"]

    def codes(self) -> set[str]:
        return {finding.code for finding in validate_registry(self.raw)}

    def rehearse(self, space: str = "spec", **overrides: object):
        arguments = {
            "baseline": self.baseline,
            "expected_next": self.namespace["spaces"][space]["next_number"],
            **overrides,
        }
        return rehearse_allocation(self.namespace, space, **arguments)

    def rehearse_state(self, name: str, space: dict):
        spaces = {**self.namespace["spaces"], name: space}
        return rehearse_allocation(
            {**self.namespace, "spaces": spaces},
            name,
            baseline=self.baseline,
            expected_next=space["next_number"],
        )

    def test_the_prepared_namespace_issues_nothing_and_matches_the_current_spaces(
        self,
    ) -> None:
        self.assertEqual("baseline-1", self.raw["identity_namespaces"]["active"])
        self.assertEqual("prepared", self.namespace["state"])
        self.assertEqual("Q07_AFTER_W11_ONLY", self.namespace["cutover"])
        self.assertEqual(
            self.raw["identity_spaces"].keys(), self.namespace["spaces"].keys()
        )
        for name, space in self.namespace["spaces"].items():
            with self.subTest(space=name):
                current = self.raw["identity_spaces"][name]
                self.assertEqual(
                    (current["prefix"], current["width"], 0, 1, []),
                    (
                        space["prefix"],
                        space["width"],
                        space["high_water"],
                        space["next_number"],
                        space["reserved_history"],
                    ),
                )
        self.assertFalse(
            {code for code in self.codes() if code.startswith("identity-namespace")}
        )

    def test_a_namespace_that_already_issued_a_number_is_rejected(self) -> None:
        self.namespace["spaces"]["spec"].update(high_water=1, next_number=2)
        self.assertIn("identity-namespace-invalid", self.codes())

    def test_a_namespace_that_differs_from_the_current_spaces_is_rejected(
        self,
    ) -> None:
        for mutate in (
            lambda ns: ns["spaces"].pop("spec"),
            lambda ns: ns["spaces"]["spec"].update(prefix="PKG-"),
            lambda ns: ns["spaces"]["spec"].update(width=5),
            lambda ns: ns.update(predecessor="baseline-3"),
            lambda ns: ns.update(id="baseline-1"),
        ):
            with self.subTest(mutate=mutate):
                self.setUp()
                mutate(self.namespace)
                self.assertIn("identity-namespace-invalid", self.codes())

    def test_a_registry_without_the_prepared_namespace_is_rejected(self) -> None:
        del self.raw["identity_namespaces"]
        self.assertTrue({"schema-invalid", "identity-namespace-invalid"} & self.codes())

    def test_the_first_allocation_is_spec_0001_and_the_rehearsal_changes_nothing(
        self,
    ) -> None:
        identity, state = self.rehearse()
        self.assertEqual("SPEC-0001", identity)
        self.assertEqual((1, 2), (state["high_water"], state["next_number"]))
        self.assertEqual(self.before, self.raw)

    def test_every_space_starts_at_one_without_a_gap(self) -> None:
        for name, space in self.namespace["spaces"].items():
            with self.subTest(space=name):
                issued = []
                for _ in range(3):
                    identity, space = self.rehearse_state(name, space)
                    issued.append(identity)
                prefix, width = space["prefix"], space["width"]
                self.assertEqual([f"{prefix}{n:0{width}d}" for n in (1, 2, 3)], issued)

    def test_a_reserved_or_retired_number_is_never_reissued(self) -> None:
        space = self.namespace["spaces"]["spec"]
        issued: list[str] = []
        for _ in range(40):
            identity, space = self.rehearse_state("spec", space)
            issued.append(identity)
            # Retire every third number, as a removed package does.
            if len(issued) % 3 == 0:
                space = reserve_number(space, space["high_water"])
        self.assertEqual(len(issued), len(set(issued)))
        self.assertEqual(list(range(3, 40, 3)), space["reserved_history"])
        self.assertEqual(40, space["high_water"])

    def test_a_number_already_reserved_cannot_be_allocated(self) -> None:
        space = {**self.namespace["spaces"]["spec"], "reserved_history": [1]}
        with self.assertRaises(IdentityHistoryError):
            self.rehearse_state("spec", space)

    def test_a_stale_or_concurrent_request_is_rejected(self) -> None:
        for expected in (0, 2, 99):
            with (
                self.subTest(expected=expected),
                self.assertRaises(IdentityHistoryError),
            ):
                self.rehearse(expected_next=expected)

    def test_the_old_and_new_baselines_are_not_confused(self) -> None:
        for baseline in ("baseline-1", "baseline-3", ""):
            with (
                self.subTest(baseline=baseline),
                self.assertRaises(IdentityHistoryError),
            ):
                self.rehearse(baseline=baseline)

    def test_an_unknown_space_is_rejected(self) -> None:
        with self.assertRaises(IdentityHistoryError):
            rehearse_allocation(
                self.namespace, "nope", baseline=self.baseline, expected_next=1
            )

    def test_a_prepared_namespace_refuses_a_real_allocation(self) -> None:
        with self.assertRaises(IdentityHistoryError):
            allocate_identity(
                self.namespace, "spec", baseline=self.baseline, expected_next=1
            )

    def test_the_cutover_is_refused_once_the_new_namespace_has_issued_a_number(
        self,
    ) -> None:
        self.assertEqual((), cutover_findings(self.raw))
        self.namespace["spaces"]["spec"].update(high_water=1, next_number=2)
        self.assertTrue(cutover_findings(self.raw))
        self.setUp()
        self.raw["identity_namespaces"]["active"] = self.baseline
        self.assertTrue(cutover_findings(self.raw))

    def test_the_closed_baseline_keeps_every_reserved_number(self) -> None:
        # The rehearsal never touches baseline-1, so its reserved history and
        # high-water stay exactly as the Registry records them.
        self.rehearse()
        self.assertEqual(self.before["identity_spaces"], self.raw["identity_spaces"])
