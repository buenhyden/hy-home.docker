---
title: "README Navigation and Language Contract Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0184-PLAN-0001"
parent_ids:
- "SPEC-0184"
created: "2026-09-27"
---

# README Navigation and Language Contract Plan

## Objective

Implement [SPEC-0184](spec.md). The Registry declares each profile's prose
language. Two link modes, `navigation` and `language`, enforce the README
contract over the whole corpus. The body contract enforces declared language on
changed non-README documents. The Retention Catalog, the Stage 03 index, and
the template catalog stop forcing descendant enumeration. Every active README
is then rewritten to satisfy the contract before the two modes are switched on
in the gate.

## Dependencies

- Approved SPEC-0184. ADR-0044 stays `proposed` until the owner accepts it.
  That acceptance is not a precondition of this Plan.
- Baseline `f30b168e2` plus commit `4b2f2ca9e` (draft Spec and ADR).
- Tests run with `python3 -m unittest`. Link and metadata checks run through
  `scripts/validation/check-document-links.py` and
  `scripts/validation/check-document-metadata.py`. The gate runs through
  `scripts/validation/run-ci-gate.py`; read its `--explain` output before
  running any profile.
- The `humanize-korean` skill for every Korean README rewrite.

## Execution Sequence

Each work unit is one logical commit unless it says otherwise. A work unit
that changes validator behavior starts with a regression test that is observed
failing. The two new link modes stay unregistered in `MODE_HANDLERS` (inactive)
until W13, so each intermediate commit keeps the existing gates green.

1. **W1: Language field and judge.** This unit is executed directly.
   - Schema: add `"language": {"enum": ["ko", "en"]}` to
     `docs/99.templates/contracts/document-profile.schema.json`
     `$defs/profile.properties`.
   - Registry: declare `language` on every prose profile.
     - `ko`: `readme`, `documentation-readme`, `repository-readme`,
       `package-readme`, `reference-category-readme`, `research`, `audit`,
       `data`, `governance-provider-index`, `governance-knowledge-index`,
       `governance-prompt-index`, `guide`, `policy`, `runbook`, `incident`,
       `postmortem`.
     - `en`: `requirements-package`, `architecture-description`, `adr`,
       `spec`, `data-model-contract`, `plan`, `task`, `research-member`,
       `audit-member`, and every non-index `governance-*` profile.
     - No field: machine contracts, templates, runtime projections, the
       `generated`, `unsupported`, archive, migration, and tombstone profiles,
       and `runtime-governance-readme`.
   - Registry: register `tests/lib/README.md`, `tests/validation/README.md`,
     and `_workspace/repo-support/README.md` under `repository-readme`
     `additional_paths`.
   - New module `scripts/lib/document_governance/language.py`:

     ```python
     """Judge whether a document's prose matches its declared language."""

     import re

     LANGUAGES = ("ko", "en")
     # ponytail: character-ratio heuristic; it cannot see meaning, only script.
     KO_MIN_RATIO = 0.20
     EN_MAX_RATIO = 0.02
     MIN_LETTERS = 40

     _FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
     _FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.S | re.M)
     _COMMENT = re.compile(r"<!--.*?-->", re.S)
     _HEADING = re.compile(r"^#{1,6} [^\n]*$", re.M)
     _INLINE_CODE = re.compile(r"`[^`\n]*`")
     _LINK_TARGET = re.compile(r"\]\([^)]*\)")
     _URL = re.compile(r"https?://\S+")
     _TOKEN = re.compile(r"\b[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]*|\b[A-Z]{2,}-\d+\b")
     _HANGUL = re.compile(r"[가-힣]")
     _LATIN = re.compile(r"[A-Za-z]")


     def prose(text: str) -> str:
         """Remove structure tokens that keep their form in every language."""

         for pattern in (_FRONTMATTER, _FENCE, _COMMENT, _HEADING,
                         _INLINE_CODE, _LINK_TARGET, _URL, _TOKEN):
             text = pattern.sub(" ", text)
         return text


     def hangul_ratio(text: str) -> float | None:
         """Return Hangul / (Hangul + Latin) over prose, or None when too short."""

         body = prose(text)
         hangul = len(_HANGUL.findall(body))
         latin = len(_LATIN.findall(body))
         if hangul + latin < MIN_LETTERS:
             return None
         return hangul / (hangul + latin)


     def language_mismatch(text: str, declared: str) -> str | None:
         """Return a reason when prose does not read as the declared language."""

         ratio = hangul_ratio(text)
         if ratio is None:
             return None
         if declared == "ko" and ratio < KO_MIN_RATIO:
             return f"declared ko, Hangul ratio {ratio:.2f} < {KO_MIN_RATIO}"
         if declared == "en" and ratio > EN_MAX_RATIO:
             return f"declared en, Hangul ratio {ratio:.2f} > {EN_MAX_RATIO}"
         return None
     ```

   - Calibrate the thresholds by printing `hangul_ratio` for every active
     README and non-README document. Keep the constants when every document
     that a reviewer reads as Korean clears 0.20 and every document read as
     English stays under 0.02. Otherwise adjust them, and record the
     distribution and the chosen values in the Task.
   - Tests in the new `tests/lib/document_governance/test_language.py`:
     - Korean prose with English headings, paths, identifiers, and a code
       fence passes as `ko`.
     - English prose fails as `ko` and passes as `en`.
     - Korean prose fails as `en`.
     - Text under `MIN_LETTERS` returns `None`.
     - A table whose cells hold only identifiers is ignored.
   - Tests in `test_registry.py`: the schema rejects `language: "fr"`; every
     README-named profile path declares `ko`; the three new README paths
     classify to exactly one profile.
2. **W2: Navigation mode (inactive).** This unit is executed directly.
   - In `scripts/lib/document_governance/links.py`, add `check_navigation(graph)`
     beside `check_entrypoint`. Do not register it in `MODE_HANDLERS` yet.
     - Children come from `git ls-files -z` under the README's directory. The
       result is read once per graph, and names `README.md` and `.gitkeep`
       are ignored.
     - A folder router is a README whose directory has at least one child
       directory and no child file.
     - Destinations are `graph.links` from the README, plus reference-style
       definitions (`^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)`) and HTML `href`
       values parsed from its unfenced lines. They are normalized with
       `_normalized_target`.
     - `navigation-descendant-link`: in a router, a target inside the
       README's directory whose relative path has two or more parts, unless
       it is exactly `<child>/README.md`.
     - `navigation-descendant-tree`: in a router, a fenced tree line using
       `├──`, `└──`, `|--` or `` `-- `` at nesting depth 2 or more that names a
       file (no trailing `/`, not `README.md`, no `<` placeholder).
     - `navigation-label-mismatch`: in any README, a label whose stripped text
       ends in `/` while the target is neither a tracked directory nor a
       `README.md`.
   - Tests in `test_links.py`. Build fixtures in a git-initialized temp root
     through the existing `track_repository`.
     - Failures:
       - A router linking `a/spec.md`.
       - A router linking `a/tasks/tsk-0001-x.md`.
       - A router linking `a/b/` two levels down.
       - A reference-style definition to `a/plan.md`.
       - An HTML `href="a/plan.md"`.
       - A tree naming `│   └── spec.md`.
       - A label `[a/](a/spec.md)`.
     - Passes:
       - A router linking `a/` and `a/README.md`.
       - A collection README (it has a direct file) linking its own
         `x.md`.
       - A router citing `../other/y.md`.
       - A directory holding only `.gitkeep`.
       - A router whose tree names `a/` and `a/README.md`.
3. **W3: Language enforcement (inactive link mode, active changed check).**
   This unit is executed directly.
   - In `links.py`, add `check_language(graph)`. It loads the Registry and,
     for every node whose `classify_path` profile declares `language` and
     whose filename is `README.md`, emits `document-language-mismatch` with
     the `language_mismatch` reason. Leave it unregistered until W13.
   - In `metadata/heading.py` `validate_body_contract`, append a
     `document-language-mismatch` finding when the registered profile declares
     `language` and `language_mismatch` returns a reason. Through
     `_introduced_body_findings`, this becomes an introduced-deficit check on
     changed documents. A document already in the wrong language before the
     change is not newly flagged; P2 removes that tolerance.
   - Templates: in every README template under `templates/common/` and every
     `templates/operations/` template, add the English author prompt
     `<!-- Author prompt: Write body prose in Korean; keep headings, paths,
     identifiers, and commands unchanged. -->`. Every other `docs/` template
     says "in English".
   - Tests:
     - `check_language` flags an English `docs/x/README.md` and passes a
       Korean one.
     - It skips a `docs/98.archive/**` record and `.claude/README.md`.
     - `validate_body_contract` flags a new English Guide and a new Korean
       ADR.
     - For every `template_roles` source whose artifact profile declares
       `language`, the template with each `{{TOKEN}}` replaced by sample prose
       in that language passes `language_mismatch`. With the opposite sample,
       it fails. This repository has no document generator, so the filled
       template is the generated-output evidence.
4. **W4: Stage 03 index shape.** This unit is executed directly.
   - `metadata/reference.py` `_index_membership_findings` accepts a member when
     the member path, its package directory, or its package `README.md` is
     linked.
   - Rewrite `docs/03.specs/README.md`:
     - Korean prose.
     - The current packages as `[SPEC-####](./####-slug/)` rows with a
       one-line purpose, and no status, Plan, Task, or completed row.
     - One sentence that routes completed packages to the Stage 98 README.
   - Tests in `metadata/test_reference.py` `IndexMembershipTests`: a
     directory link counts as membership; a missing package still fails.
5. **W5: Template catalog retirement.** This unit is executed directly.
   - Remove `template_catalog` from `registry.json`, from the schema `required`
     list and `properties`, from `DocumentRegistry` and `load_registry` in
     `registry.py`, and from `_template_catalog_findings` and its call in
     `metadata/reference.py`.
   - Replace the catalog tests at `metadata/test_reference.py:625-650` with a
     test that `docs/99.templates/templates/README.md` links no file below its
     category directories.
   - Rewrite that README in Korean as a router: category directories plus
     the Registry `template_roles` as the type-to-template owner.
   - Update `docs/99.templates/README.md` and `stage-authoring-matrix.md` where
     they name the catalog table.
6. **W6: Retention Catalog relocation.** This unit is executed directly.
   - Create `docs/98.archive/retention-catalog.md`:
     - English.
     - Frontmatter copied from the `readme` shape with type
       `archive/retention-catalog`.
     - `## Overview` explaining the columns.
     - `## Retention Catalog` with the 24 rows moved byte for byte.
   - Register profile `archive-retention-catalog`:
     - `path_pattern` is the file, `lifecycle_id` is `living`.
     - `required_sections` are `Overview` and `Retention Catalog`.
     - `language` is `en`.
     - `template_id` is `null` if the schema admits it. Otherwise register an
       `archive/retention-catalog` template role and source.
   - Remove `Retention Catalog` from the `readme` optional sections.
   - `archive.py`:
     - Rename `_ARCHIVE_INDEX` to `_CATALOG_RECORD` with the new path, for
       reading the current file and the base object.
     - Add `retention-catalog.md` to `load_archive` `required_entries`.
   - Update `test_archive.py` fixtures (`:119`, `:1363-1364`, `:1505`,
     `:1570`, `:1765-1766`) to write the new file.
   - Base comparison: run `validate_catalog_identity` against `main`. If the
     24 rows, now unseen at the base path, yield findings, bound the base read
     to the old README path only when the new path is absent at the base.
     Mark that with a `ponytail:` comment naming P3 as its removal owner, and
     record the observation in the Task.
   - Rewrite `docs/98.archive/README.md` in Korean as a router: the class
     directories and a link to `retention-catalog.md`, with no row.
7. **W7: Governance text.** This unit is executed directly and gets a
   `rules-engineer` review.
   - `documentation-protocol.md#authoring-rules` states the three-level
     language priority, the structure-token rule, the heuristic and its
     limits, and the README navigation rule once.
   - The bootstrap hard constraint exempts `README.md` files from the
     English-only rule and routes to the protocol.
   - `standards.md`, `quality-standards.md`, `output-style.md`, and
     `stage-authoring-matrix.md` route to the protocol without restating it.
   - `docs/README.md` loses its language table.
   - `hookify.warn-korean-in-governance.md` excludes `README.md`, and its
     projection is regenerated through the registered renderer.
   - Also update the statement in the Stage 98 README text that the README is
     the only current document there.
8. **W8: Repository-surface READMEs.** Dispatched to a subagent.
   - Files: `README.md`, `_workspace/**/README.md`, `evals/README.md`,
     `examples/**/README.md`, `projects/**/README.md`, `scripts/README.md`,
     `secrets/README.md`, `tests/**/README.md`.
9. **W9: `docs/` READMEs.** Dispatched to a subagent.
   - Files: `docs/README.md` and every README under Stages 01, 02, 05, 90,
     and 99, excluding those W4, W5, and W6 already rewrote, and excluding
     `docs/98.archive/**` records.
   - Frozen Stage 98 bodies are never edited.
10. **W10: Governance and provider READMEs.** Dispatched to a subagent.
    - `.agents/**/README.md`.
    - The runtime-governance README template and the route sentence in
      `scripts/operations/provider_surface_renderer.py:298` in Korean. After
      the edit, regenerate `.claude/README.md` and `.codex/README.md` through
      the renderer and prove renderer parity.
11. **W11: `infra/` layers 01 through 05.** Dispatched to a subagent.
12. **W12: `infra/` layers 06 through 11 and remaining infra READMEs.**
    Dispatched to a subagent.

    Brief shared by W8 through W12:
    - Rewrite prose to Korean with a `humanize-korean` pass. Keep required
      headings, paths, identifiers, and commands unchanged.
    - Remove descendant enumeration from folder routers.
    - Replace hand-copied counts, versions, and ports that have no consuming
      purpose with a route to the Compose or config owner.
    - Fix mislabeled links and retired identifiers found by the audit.
    - Record, but do not resolve, contradictions that the canonical source
      does not settle.
    - Do not edit Compose, config, or runtime files.
    - Do not commit. The controller reviews each unit, runs the checks, and
      commits one commit per work unit.
13. **W13: Activation and verification.** This unit is executed directly.
    - Register `navigation` and `language` in `MODE_HANDLERS` and update the
      pinned mode tuple at `test_links.py:1303`.
    - Run `check-document-links.py --mode all`, the metadata, archive,
      lifecycle, and operations validators, the unit suites, and the changed
      and full gate profiles.
    - Record results against baseline in the Task.
14. **W14: Final review.**
    - A fresh reviewer checks the whole branch diff against SPEC-0184.
    - Findings are fixed in follow-up commits.
    - The branch and worktree are kept local; nothing is pushed.

## Risk and Rollback

- The two new modes are inactive until W13, so W1 through W12 can each be
  reverted as one commit without breaking the gate.
- W6 is the only data-bearing move. The row set is compared before and after,
  and reverting the commit restores the README ledger.
- A subagent rewrite that drops meaning is caught by the per-unit review
  against the file's pre-change text. The fix is to revert that file and
  redo it.
- A language false positive on an identifier-heavy README is handled by
  recalibrating the constants in `language.py`, with evidence. It is never
  handled by an allowlist.

## Verification

- W1 through W6 and W13 carry red-then-green unit evidence. Run each suite with
  `python3 -m unittest discover -s tests/lib/document_governance -p 'test_*.py'`
  and with the `metadata/` and `lifecycle/` subdirectories.
- Each work unit runs `check-document-metadata.py --mode check-changed --base-ref main`,
  `check-document-links.py --mode all`, and `git diff --cached --check`.
- W13 runs `run-ci-gate.py --profile changed` and `--profile full`, each
  after its `--explain` output shows no runtime, network, or secret side
  effect. A suite that would have one is recorded as blocked, not run.
- Acceptance criteria 1 through 9 map to W1, W2, W3, W6, W4, W5, W7,
  W8 through W12, and W13, in that order.

## Rulings

- Non-README language is enforced as an introduced deficit until P2, per
  Spec rule 4. It is not an allowlist.
- W8 through W12 use subagent-driven development because their file sets are
  disjoint and follow W1 through W7's stable contract. Every other unit
  changes shared contracts and is executed directly under executing-plans.
- Subagents never run `git commit`; the controller owns the index.
