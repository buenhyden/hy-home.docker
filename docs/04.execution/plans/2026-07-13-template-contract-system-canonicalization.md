---
status: active
artifact_id: plan:2026-07-13-template-contract-system-canonicalization
artifact_type: plan
parent_ids:
  - spec:130-template-contract-system-canonicalization
---

<!-- Target: docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md -->

# Template Contract System Canonicalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a single registry-driven template contract system whose
copyable forms, support governance, validators, and directly affected
consumers are consistent and independently reviewable.

**Architecture:** Replace the flat typed-template mapping with one exact
template-role registry that owns source paths, target matchers, target
profiles, and body envelopes. Keep human semantics in Stage 99 support,
copyable forms in Stage 99 templates, and executable interpretation in the
existing Python checker and repository contract gate. Apply the result to the
fully typed baseline and direct fallout while routing the remaining corpus to
preservation-oriented migration waves.

**Tech Stack:** YAML 1.2-compatible metadata, Python 3.12, PyYAML,
`unittest`, Bash, Markdown/CommonMark with GitHub Flavored Markdown
conventions, OpenAPI YAML, GraphQL SDL, Protocol Buffers, repository
generators, Graphify, and Git.

## Global Constraints

- Spec 130 is the sole design authority for this implementation.
- Keep `docs/99.templates/support/document-metadata-profiles.yaml` as the
  only machine-readable document and template registry.
- Preserve the common lifecycle values `draft`, `active`, `completed`,
  `superseded`, and `archived`.
- Preserve the canonical frontmatter presentation order: `status`,
  `artifact_id`, `artifact_type`, `parent_ids`, `supersedes`,
  `reviewed_at`, `review_cycle`, `generated_by`, `archived_from`,
  `archived_on`, `archive_reason`, and `current_replacement`.
- Do not introduce `type`, `document_type`, `template_type`, `owner`,
  `updated`, or `links` as substitute metadata.
- Treat `parent_ids` as a direct-parent set with deterministic serialization,
  not semantic priority.
- Templates own copyable forms only. Support owns role, selection, lifecycle,
  path, migration, review, approval, replacement, and archive rules.
- A target document must replace all frontmatter and body tokens with
  topic-specific content supported by repository or external evidence.
- Use `{{token_name}}` for Markdown body tokens and `__TOKEN_NAME__` for
  machine-readable template tokens.
- Keep one canonical README template, one Audit template, and one Task
  template. Delete the duplicate Harness Task and Stage 00 Memory mirror.
- Keep Spec child documents on `artifact_type: spec` and derive their focused
  roles from exact target paths.
- Allow Incident roots; require Postmortem to parent an Incident; require
  Release to parent a real Spec, Plan, or Task.
- Do not invent review dates, parent IDs, approvals, incidents, postmortems,
  releases, test evidence, or runtime truth.
- Do not bulk-rewrite 510 untyped Stage 01-05 leaves or 229 README files.
- Preserve completed and superseded evidence bodies.
- Do not change Docker Compose, infrastructure runtime, secrets, deployment,
  remote GitHub state, or user-global provider configuration.
- Use TDD for registry, checker, repository-gate, and template-instantiation
  behavior. Use `apply_patch` for authored changes and canonical generators
  for generated outputs.
- Execute the seven tasks serially. Every task gets a fresh implementation
  agent, a separate specification reviewer, and a separate quality reviewer.
- Resolve all Critical and Important review findings before committing the
  task. Record Minor findings and their disposition in the Task evidence.
- Make at least one logical Conventional Commit per task. Keep review fixes in
  separate logical commits when they change behavior or contract meaning.
- Never run `pre-commit run --all-files` directly. Use
  `scripts/validation/run-agent-precommit-all-files.sh` only for the final
  clean-worktree gate.
- After Python, Bash, or generator changes, run `graphify update .` when the
  CLI is available. Treat its report as advisory and corroborate it with
  tracked source and stage documents.

---

## Overview

This plan implements Spec 130 as seven dependency-ordered deliverables. Task 1
establishes the registry and human contract boundaries. Tasks 2 through 5
normalize the Common, Governance, SDLC, Execution, and Operations forms. Task 6
turns the registry into the executable validation source and removes duplicate
shell-owned template semantics. Task 7 performs preservation-oriented direct
consumer migration, regenerates evidence, and records the follow-up waves.

The current 17-document typed baseline predates Spec 130. This Plan, its Task,
and Spec 130 are additional direct consumers and must be validated by the same
changed/new boundary.

## Context

The current registry has strong typed frontmatter and README classification,
but its `template_sources` mapping describes only typed Markdown leaves. It
does not assign exact roles to README, Memory, or Progress forms, does not own
body-section contracts, and cannot deterministically reject two templates that
compete for one target.

Twenty-one of 23 copyable Markdown forms contain non-copyable Rules blocks.
The common README form contains 435 lines of mixed form, snippets, and
governance. Audit reuses the Reference template despite having a distinct
profile. Generic Task and Harness Task target the same path family and artifact
type. The Runbook repeats rollback content, several document roles repeat
summary or verification purposes, and the Stage 00 Memory mirror creates a
second template owner.

The metadata inventory contains 900 records after Spec 130. The 2,025 advisory
findings remain historical migration evidence. This plan must not convert that
advisory baseline into an unbounded body rewrite.

## Goals & In-Scope

- Replace `template_sources` with one validated `template_roles` registry for
  all 23 copyable Markdown forms.
- Define exact source path, artifact profile, target path matchers, required,
  conditional, and forbidden headings for each role.
- Add a single Markdown token syntax and a single machine-template token
  syntax.
- Reconcile all Stage 99 support contracts and external-source rationale.
- Normalize Common, Governance, SDLC, Execution, Operations, and
  machine-readable forms without copying support rules into them.
- Add Audit, remove Harness Task, and remove the Stage 00 Memory mirror.
- Enforce role ambiguity, body envelopes, README headings, forbidden template
  instructions, unresolved tokens, and machine-template example drift.
- Remove the current Target-comment requirement atomically with changed/new
  validator behavior and direct planning-document migration.
- Preserve the 17-document typed baseline unless a concrete contract or link
  requires an edit.
- Regenerate metadata and LLM Wiki evidence through canonical generators.
- Record reproducible entry and exit conditions for migration Waves A through
  E without executing those broad waves in this branch.

## Non-Goals & Out-of-Scope

- No mass migration of active PRD, ARD, ADR, Spec, Plan, Guide, Policy, or
  Runbook corpora.
- No restyling of completed Plans and Tasks.
- No synthetic Incident, Postmortem, Release, review, or verification record.
- No profile-independent README frontmatter normalization.
- No parallel metadata registry, JSON Schema copy, template path alias, or
  compatibility mirror.
- No runtime, deployment, secrets, remote-protection, or provider-global
  mutation.
- No corpus-wide blocking before the later migration waves complete.

## File Responsibility Map

| Surface | Responsibility |
| --- | --- |
| `docs/99.templates/support/document-metadata-profiles.yaml` | Exact machine schema for profiles, README profiles, template roles, target matchers, body envelopes, tokens, and transitions. |
| `scripts/validation/check-document-metadata.py` | Structural registry validation, role matching, Markdown body validation, target checks, and repository contract diagnostics. |
| `tests/validation/test_document_metadata.py` | RED/GREEN unit, fixture, instantiation, ambiguity, body, README, machine-token, and CLI integration tests. |
| `scripts/validation/check-repo-contracts.sh` | Orchestrates the Python contract checker and repository-wide checks without a second template schema. |
| `docs/99.templates/support/*.md` | Human contracts, governance, selection, lifecycle, README behavior, and external rationale. |
| `docs/99.templates/templates/common/` | README, Reference, Audit, and Archive forms. |
| `docs/99.templates/templates/governance/` | Memory and Progress forms only. |
| `docs/99.templates/templates/sdlc/` | PRD, ARD, ADR, Spec, Plan, and Task forms. |
| `docs/99.templates/templates/spec-contracts/` | API, Agent, Data, Service, Test, OpenAPI, GraphQL, and Protobuf focused forms. |
| `docs/99.templates/templates/operations/` | Guide, Policy, Runbook, Incident, Postmortem, and Release forms. |
| `docs/00.agent-governance/rules/documentation-protocol.md` | Agent-facing authoring route and transition duties. |
| `docs/00.agent-governance/rules/stage-authoring-matrix.md` | Stage 01-05 role, path, and template routing. |
| `docs/00.agent-governance/rules/task-checklists.md` | Task evidence and controlled QA duties. |
| `docs/00.agent-governance/memory/README.md` | Memory route after mirror deletion. |
| `docs/00.agent-governance/memory/progress.md` | Durable task progress and final evidence. |
| `docs/03.specs/130-template-contract-system-canonicalization/spec.md` | Approved design and success criteria. |
| `docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md` | Dependency order, exact tasks, validation, and rollback. |
| `docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md` | Approval, work, review, commit, QA, wrapper, and wave evidence. |
| Canonical metadata and LLM Wiki outputs | Generated evidence refreshed only by owner scripts. |

## Work Breakdown

| Task | Deliverable | Primary acceptance |
| --- | --- | --- |
| T-TCS-001 | Registry and Stage 99 support contracts | Twenty-three unique roles load, match deterministically, and have one human owner. |
| T-TCS-002 | Common, README, and Governance forms | Audit exists; README is bounded; Memory mirror and duplicate rules are gone. |
| T-TCS-003 | Stage 01-03 and Spec-child forms | Role-specific forms contain no copied governance and no duplicate-purpose sections. |
| T-TCS-004 | Stage 04 Plan and Task system | One Task form owns generic and harness evidence without competing templates. |
| T-TCS-005 | Stage 05 Operations forms | Guide, Policy, Runbook, Incident, Postmortem, and Release have distinct executable roles. |
| T-TCS-006 | Executable validator and repository gate | Registry-owned role/body/token contracts fail closed for changed/new targets. |
| T-TCS-007 | Direct consumers and migration-wave evidence | Direct chain remains valid, generated evidence is fresh, and Waves A-E are reproducible. |

## Task 1: Registry and Support Contract Canonicalization

**Files:**

- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`
- Modify: `docs/99.templates/support/frontmatter-contract.md`
- Modify: `docs/99.templates/support/sdlc-document-contract.md`
- Modify: `docs/99.templates/support/common-document-contract.md`
- Modify: `docs/99.templates/support/readme-profile-contract.md`
- Modify: `docs/99.templates/support/template-contract.md`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: `docs/99.templates/support/lifecycle-status.md`
- Modify: `docs/99.templates/support/template-governance.md`
- Modify: `docs/99.templates/support/external-source-rationale.md`
- Modify: `docs/99.templates/support/README.md`
- Modify: `scripts/validation/check-document-metadata.py`
- Test: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: `load_profiles()`, `infer_artifact_type()`, README path matching,
  the existing profile schema, and Spec 130 ownership decisions.
- Produces: `template_roles`, `matching_template_roles(path, artifact_type,
  profiles) -> list[str]`, `classify_template_role(path, artifact_type,
  profiles) -> str`, and structurally validated role records for Tasks 2-6.

- [ ] **Step 1: Add failing registry-schema tests**

Add these exact tests to `ProfileSchemaTests`:

```python
def test_template_roles_require_exact_fields_and_unique_sources(self) -> None:
    profiles = metadata.load_profiles(PROFILES)
    roles = profiles["template_roles"]
    self.assertEqual(23, len(roles))
    sources = [role["source"] for role in roles.values()]
    self.assertEqual(len(sources), len(set(sources)))

def test_template_roles_reject_unknown_profiles_and_heading_overlap(self) -> None:
    self.mutate_and_load(
        lambda values: values["template_roles"]["prd"].__setitem__(
            "artifact_profile", "missing-profile"
        )
    )

def test_template_roles_reject_ambiguous_target_matchers(self) -> None:
    def mutate(values):
        values["template_roles"]["audit"]["target_globs"] = list(
            values["template_roles"]["reference"]["target_globs"]
        )
    self.mutate_and_load(mutate)
```

Add `TemplateRoleInferenceTests` with this table-driven positive fixture:

```python
class TemplateRoleInferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_registered_targets_have_one_exact_role(self) -> None:
        cases = {
            "docs/01.requirements/901-fixture.md": ("prd", "prd"),
            "docs/02.architecture/requirements/0901-fixture.md": ("ard", "ard"),
            "docs/02.architecture/decisions/0901-fixture.md": ("adr", "adr"),
            "docs/03.specs/901-fixture/spec.md": ("spec", "spec"),
            "docs/03.specs/901-fixture/api-spec.md": ("spec", "api-spec"),
            "docs/03.specs/901-fixture/agent-design.md": ("spec", "agent-design"),
            "docs/03.specs/901-fixture/data-model.md": ("spec", "data-model"),
            "docs/03.specs/901-fixture/service.md": ("spec", "service"),
            "docs/03.specs/901-fixture/tests.md": ("spec", "tests"),
            "docs/04.execution/plans/2026-07-13-fixture.md": ("plan", "plan"),
            "docs/04.execution/tasks/2026-07-13-fixture.md": ("task", "task"),
            "docs/05.operations/guides/00-workspace/fixture.md": ("guide", "guide"),
            "docs/05.operations/policies/00-workspace/fixture.md": ("policy", "policy"),
            "docs/05.operations/runbooks/00-workspace/fixture.md": ("runbook", "runbook"),
            "docs/05.operations/incidents/2026/INC-901-fixture/INC-901-fixture.md": ("incident", "incident"),
            "docs/05.operations/incidents/2026/INC-901-fixture/postmortem.md": ("postmortem", "postmortem"),
            "docs/05.operations/releases/2026-07-13-fixture.md": ("release", "release"),
            "docs/90.references/research/fixture.md": ("reference", "reference"),
            "docs/90.references/audits/fixture.md": ("audit", "audit"),
            "docs/98.archive/03.specs/fixture.md": ("archive", "archive"),
            "README.md": ("readme", "readme"),
            "docs/00.agent-governance/memory/fixture.md": ("governance", "memory"),
            "docs/00.agent-governance/memory/progress.md": ("governance", "progress"),
        }
        for path_text, (profile, expected_role) in cases.items():
            with self.subTest(path=path_text):
                self.assertEqual(
                    expected_role,
                    metadata.classify_template_role(
                        pathlib.Path(path_text), profile, self.profiles
                    ),
                )
```

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.TemplateRoleInferenceTests -v
```

Expected: FAIL because `template_roles` and both role-matching functions do not
exist.

- [ ] **Step 3: Replace the flat template mapping with 23 exact roles**

Remove `template_sources` and add `template_roles`. Every role contains exactly
`source`, `artifact_profile`, `target_globs`, `required_headings`,
`conditional_headings`, and `forbidden_headings`.

Use these exact role/source/profile assignments:

| Role | Source | Profile |
| --- | --- | --- |
| prd | `templates/sdlc/prd.template.md` | prd |
| ard | `templates/sdlc/ard.template.md` | ard |
| adr | `templates/sdlc/adr.template.md` | adr |
| spec | `templates/sdlc/spec.template.md` | spec |
| plan | `templates/sdlc/plan.template.md` | plan |
| task | `templates/sdlc/task.template.md` | task |
| guide | `templates/operations/guide.template.md` | guide |
| policy | `templates/operations/policy.template.md` | policy |
| runbook | `templates/operations/runbook.template.md` | runbook |
| incident | `templates/operations/incident.template.md` | incident |
| postmortem | `templates/operations/postmortem.template.md` | postmortem |
| release | `templates/operations/release.template.md` | release |
| reference | `templates/common/reference.template.md` | reference |
| audit | `templates/common/audit.template.md` | audit |
| archive | `templates/common/archive.template.md` | archive |
| readme | `templates/common/readme.template.md` | readme |
| memory | `templates/governance/memory.template.md` | governance |
| progress | `templates/governance/progress.template.md` | governance |
| agent-design | `templates/spec-contracts/agent-design.template.md` | spec |
| api-spec | `templates/spec-contracts/api-spec.template.md` | spec |
| data-model | `templates/spec-contracts/data-model.template.md` | spec |
| service | `templates/spec-contracts/service.template.md` | spec |
| tests | `templates/spec-contracts/tests.template.md` | spec |

Paths in the registry are repository-root paths beginning with
`docs/99.templates/`. Target globs must distinguish parent Spec and each exact
Spec-child filename. README matching delegates to the existing 17 README
profiles. Audit matching excludes README and the generated metadata inventory
through existing profile inference and `inventory_excludes`.

- [ ] **Step 4: Implement structural role validation and matching**

Add:

```python
TEMPLATE_ROLE_KEYS = frozenset({
    "source",
    "artifact_profile",
    "target_globs",
    "required_headings",
    "conditional_headings",
    "forbidden_headings",
})

def matching_template_roles(
    path: pathlib.Path,
    artifact_type: str,
    profiles: dict[str, object],
) -> list[str]:
    """Return sorted template roles matching one target path and profile."""

def classify_template_role(
    path: pathlib.Path,
    artifact_type: str,
    profiles: dict[str, object],
) -> str:
    """Return one role or raise ProfileError for zero or ambiguous matches."""
```

Validate exact role keys, known profiles, safe repository source paths,
non-empty non-overlapping heading lists, safe target globs, unique source
paths, and source-file existence in repository-contract mode. Return sorted
matches so diagnostics are deterministic.

Replace `_validate_template_source()` lookup of `template_sources` with the
source path from the classified role. Typed forms validate target-profile keys
and registered frontmatter tokens. README validates source draft only. Memory
and Progress validate exactly `layer: agentic` plus `status: draft`. Archive
retains source draft while its rendered target validates as archived.

- [ ] **Step 5: Reconcile the human support owners**

Rewrite the support documents so:

- Frontmatter owns interpretation, not duplicated key tables.
- SDLC Contract owns PRD through Release roles and iterative feedback.
- Common Contract owns Reference, Audit, Archive, README-adjacent common,
  governance, generated, repo-support, and native surfaces.
- README Contract owns the 17 profiles and heading envelope behavior.
- Template Contract owns form-only source and instantiated-target rules.
- Selection owns exact purpose, path, and source routing.
- Lifecycle owns the unchanged status vocabulary.
- Governance owns change, review, approval, destructive replacement,
  preservation, migration, and logical commits.
- External rationale records the official sources and 2026-07-13 verification
  date without claiming that local type names are international standards.

Keep `README.md` as a catalog and remove any duplicated normative prose.

- [ ] **Step 6: Run GREEN and contract checks**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.TemplateRoleInferenceTests -v
python3 scripts/validation/check-document-metadata.py --mode check-contracts
bash scripts/validation/check-repo-contracts.sh
```

Expected: all focused tests pass; metadata repository contracts report zero
violations; repository contracts exit 0.

- [ ] **Step 7: Record review evidence and commit**

After Spec PASS and Quality APPROVED:

```bash
git add docs/99.templates/support scripts/validation/check-document-metadata.py tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "feat(metadata): define canonical template roles"
```

## Task 2: Common, README, and Governance Forms

**Files:**

- Modify: `docs/99.templates/templates/common/readme.template.md`
- Modify: `docs/99.templates/templates/common/reference.template.md`
- Create: `docs/99.templates/templates/common/audit.template.md`
- Modify: `docs/99.templates/templates/common/archive.template.md`
- Modify: `docs/99.templates/templates/common/README.md`
- Modify: `docs/99.templates/templates/governance/memory.template.md`
- Modify: `docs/99.templates/templates/governance/progress.template.md`
- Modify: `docs/99.templates/templates/governance/README.md`
- Modify: `docs/99.templates/templates/README.md`
- Delete: `docs/00.agent-governance/memory/template.md`
- Modify: `docs/00.agent-governance/memory/README.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Test: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: Task 1 `template_roles`, README profiles, form-only contract, and
  governance metadata decision.
- Produces: bounded Common and Governance forms, one Audit form, and one
  Stage 99 Memory source for later validator enforcement.

- [ ] **Step 1: Add failing Common and Governance form tests**

Add exact assertions:

```python
def test_copyable_markdown_forms_have_one_h1_and_no_rules_block(self) -> None:
    for role in self.profiles["template_roles"].values():
        source = ROOT / role["source"]
        text = source.read_text(encoding="utf-8")
        self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))
        self.assertNotIn("> Rules:", text)
        self.assertNotIn("<!-- Target:", text)

def test_audit_has_a_distinct_registered_form(self) -> None:
    role = self.profiles["template_roles"]["audit"]
    self.assertEqual("audit", role["artifact_profile"])
    self.assertTrue((ROOT / role["source"]).is_file())

def test_memory_mirror_is_absent_and_stage99_is_referenced(self) -> None:
    self.assertFalse((ROOT / "docs/00.agent-governance/memory/template.md").exists())
    text = (ROOT / "docs/00.agent-governance/memory/README.md").read_text()
    self.assertIn("docs/99.templates/templates/governance/memory.template.md", text)
```

- [ ] **Step 2: Run RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests -v
```

Expected: failures for Rules blocks, missing Audit form, multi-H1 README form,
and the Stage 00 mirror.

- [ ] **Step 3: Replace Common forms with exact envelopes**

Use one H1 and these H2 headings:

| Role | Required H2 headings |
| --- | --- |
| README | Overview; Audience; Scope; Structure; How to Work in This Area; Related Documents |
| Reference | Overview; Purpose; Scope; Facts and Definitions; Sources; Maintenance; Related Documents |
| Audit | Overview; Scope and Criteria; Evidence; Findings; Gap Analysis; Disposition; Related Documents |
| Archive | Overview; Archive Metadata; Current Replacement; Archive Ledger; Related Documents |

Use `{{title}}` and role-specific `{{token_name}}` body tokens. Remove target
paths, Rules blocks, fixed-depth links, lifecycle prose, snippet libraries,
template usage sections, and example commands.

- [ ] **Step 4: Normalize Governance forms and metadata**

Memory and Progress template frontmatter is exactly:

```yaml
---
layer: agentic
status: draft
---
```

Memory H2 headings are Problem, Context, Resolution, Prevention, Evidence, and
Related Documents. Progress H2 headings are Current Work Log, Phase Tracker,
Layer Audit, Open Issues, and Related Documents. Move Usage Contract prose to
support governance.

- [ ] **Step 5: Delete the mirror and repair references**

Delete `docs/00.agent-governance/memory/template.md`. Update Memory README,
the live Progress log, the Progress form, and tracked links so every template
reference targets the Stage 99 Memory form. Run:

```bash
rg -n "docs/00.agent-governance/memory/template.md|memory/template.md" docs .agents .claude .codex AGENTS.md CLAUDE.md GEMINI.md
```

Expected: no active reference to the deleted mirror.

- [ ] **Step 6: Normalize the three affected catalog READMEs**

Make `templates/README.md`, `common/README.md`, and
`governance/README.md` satisfy the template-catalog profile headings:
Overview, Audience, Scope, Structure, How to Work in This Area, and Related
Documents. Keep catalogs as routing surfaces.

- [ ] **Step 7: Run GREEN and commit**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests tests.validation.test_document_metadata.ReadmeProfileTests -v
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

After both reviews:

```bash
git add docs/99.templates/templates/common docs/99.templates/templates/governance docs/99.templates/templates/README.md docs/00.agent-governance/memory tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "docs(templates): canonicalize common and governance forms"
```

## Task 3: Stage 01-03 and Spec-child Forms

**Files:**

- Modify: `docs/99.templates/templates/sdlc/prd.template.md`
- Modify: `docs/99.templates/templates/sdlc/ard.template.md`
- Modify: `docs/99.templates/templates/sdlc/adr.template.md`
- Modify: `docs/99.templates/templates/sdlc/spec.template.md`
- Modify: `docs/99.templates/templates/sdlc/README.md`
- Modify: `docs/99.templates/templates/spec-contracts/agent-design.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/api-spec.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/data-model.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/service.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/tests.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/openapi.template.yaml`
- Modify: `docs/99.templates/templates/spec-contracts/schema.template.graphql`
- Modify: `docs/99.templates/templates/spec-contracts/service.template.proto`
- Modify: `docs/99.templates/templates/spec-contracts/README.md`
- Test: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: Task 1 role envelopes and token syntax.
- Produces: form-only PRD, ARD, ADR, parent Spec, five focused Markdown child
  forms, and three visibly unresolved machine contract forms.

- [ ] **Step 1: Add failing section-envelope and token tests**

Add the local source-envelope tests before the production extractor exists:

```python
class TemplateBodyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_registered_markdown_sources_match_heading_envelopes(self) -> None:
        for name, role in self.profiles["template_roles"].items():
            source = ROOT / role["source"]
            text = source.read_text(encoding="utf-8")
            headings = {line for line in text.splitlines() if line.startswith("## ")}
            self.assertEqual(1, sum(line.startswith("# ") for line in text.splitlines()))
            self.assertTrue(set(role["required_headings"]) <= headings, name)
            self.assertFalse(set(role["forbidden_headings"]) & headings, name)
            self.assertNotIn("> Rules:", text)
            self.assertNotIn("<!-- Target:", text)

    def test_machine_sources_use_explicit_unresolved_tokens(self) -> None:
        for relative_path in (
            "docs/99.templates/templates/spec-contracts/openapi.template.yaml",
            "docs/99.templates/templates/spec-contracts/schema.template.graphql",
            "docs/99.templates/templates/spec-contracts/service.template.proto",
        ):
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            self.assertRegex(text, r"__[A-Z][A-Z0-9_]*__")
            self.assertNotIn("example.com", text)
            self.assertNotIn("Example", text)
```

- [ ] **Step 2: Run RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests -v
```

Expected: failures for current Rules blocks, duplicate-purpose headings, mixed
token styles, and valid-looking machine examples.

- [ ] **Step 3: Normalize the Stage 01-03 forms**

Use these required H2 headings:

| Role | Required H2 headings |
| --- | --- |
| PRD | Overview; Problem and Stakeholders; Requirements; Acceptance and Verification; Scope and Non-goals; Risks and Dependencies; Related Documents |
| ARD | Overview and Context; Stakeholders and Concerns; Boundaries and Constraints; Quality Attributes; Architecture Views; Data and Infrastructure; Decision and Requirement Traceability; Related Documents |
| ADR | Context and Decision Drivers; Considered Options; Decision; Consequences; Confirmation; Related Documents |
| Spec | Overview; Boundaries and Inputs; Contracts; Core Design; Interfaces and Data; Failure Modes and Guardrails; Verification; Related Documents |

Make AI-specific PRD, ARD, and Spec concerns conditional headings rather than
universal required sections. In ARD, merge Overview and Summary. In Spec, merge
Verification and Success Criteria.

- [ ] **Step 4: Normalize focused Spec-child forms**

Use these required concerns:

- Agent Design: role, inputs and outputs, orchestration, tools and permissions,
  prompt policy, context and memory, guardrails, failure handling, evaluation,
  observability, and related documents.
- API Spec: parent, scope, API style, auth, operations, request and response
  schemas, errors, compatibility, non-functional requirements,
  machine-readable contracts, verification, and related documents.
- Data Model: parent, scope, entities, relationships, schema, integrity,
  storage, privacy, migration, and related documents.
- Service: parent, scope, image and build, security, networking and storage,
  secrets, health and operations, validation, and related documents.
- Tests: parent, verification goals, TDD scope, matrix, contract and
  integration tests, non-functional tests, conditional agent evaluations,
  fixtures, execution, evidence, and related documents.

When a child exists, the parent Spec retains summary, ownership, and the link;
it does not duplicate child details.

- [ ] **Step 5: Replace machine examples with explicit tokens**

Use uppercase double-underscore tokens such as `__API_TITLE__`,
`__SERVER_URL__`, `__SERVICE_NAME__`, `__PACKAGE_NAME__`,
`__QUERY_FIELD__`, and `__MESSAGE_NAME__` while preserving valid YAML,
GraphQL, and Protobuf syntax.

- [ ] **Step 6: Normalize both catalog READMEs**

Make `sdlc/README.md` and `spec-contracts/README.md` satisfy the template
catalog heading envelope and link to support selection rather than repeating
target rules.

- [ ] **Step 7: Run GREEN and commit**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.TemplateMetadataTests -v
python3 -c "import yaml; yaml.safe_load(open('docs/99.templates/templates/spec-contracts/openapi.template.yaml'))"
git diff --check
```

After both reviews:

```bash
git add docs/99.templates/templates/sdlc docs/99.templates/templates/spec-contracts tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "docs(templates): canonicalize design and contract forms"
```

## Task 4: Stage 04 Plan and Task System

**Files:**

- Modify: `docs/99.templates/templates/sdlc/plan.template.md`
- Modify: `docs/99.templates/templates/sdlc/task.template.md`
- Delete: `docs/99.templates/templates/governance/harness-task-contract.template.md`
- Modify: `docs/99.templates/templates/governance/README.md`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify: `docs/00.agent-governance/rules/task-checklists.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Test: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: one `task` role from Task 1 and support ownership from Tasks 1-3.
- Produces: one prospective Plan form and one evidentiary Task form that owns
  generic and harness work without a subtype key.

- [ ] **Step 1: Add failing Task uniqueness and evidence tests**

Add:

```python
def test_task_has_one_source_and_no_harness_competitor(self) -> None:
    roles = self.profiles["template_roles"]
    task_sources = [
        role["source"]
        for role in roles.values()
        if role["artifact_profile"] == "task"
    ]
    self.assertEqual(
        ["docs/99.templates/templates/sdlc/task.template.md"],
        task_sources,
    )
    self.assertFalse(
        (
            ROOT
            / "docs/99.templates/templates/governance/harness-task-contract.template.md"
        ).exists()
    )

def test_task_form_contains_protected_surface_and_qa_evidence(self) -> None:
    text = (ROOT / "docs/99.templates/templates/sdlc/task.template.md").read_text()
    for heading in (
        "## Scope and Change Boundaries",
        "## Approval Evidence",
        "## Work Log",
        "## Verification Evidence",
        "## Review Evidence",
        "## Commit Ledger",
    ):
        self.assertIn(heading, text)
```

- [ ] **Step 2: Run RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests tests.validation.test_document_metadata.TemplateBodyContractTests -v
```

Expected: failure because two Task sources exist and the generic Task lacks
the consolidated evidence envelope.

- [ ] **Step 3: Normalize the Plan form**

Use required H2 headings: Overview, Context and Inputs, Goals and Non-goals,
Work Breakdown, Verification Plan, Risks and Rollback, Completion Criteria,
and Related Documents. Keep prospective validation separate from actual
results.

- [ ] **Step 4: Consolidate the Task form**

Use required H2 headings: Overview, Inputs, Goals and Non-goals, Scope and
Change Boundaries, Work Breakdown, Work Log, Verification Evidence, Review
Evidence, Commit Ledger, Deferred and Blocked Items, and Related Documents.

Make Approval Evidence and Controlled Agent Pre-commit Evidence conditional.
Include tokens for allowed and forbidden paths, protected-surface approval,
Compose/security/operations impact, exact commands, expected evidence,
review verdicts, commit identity, and deferral destination. Remove Suggested
Types and Agent-specific Types.

- [ ] **Step 5: Delete the Harness Task form and repair governance**

Delete the duplicate form and every active link to it. Update Task checklist,
documentation protocol, stage matrix, selection, and Governance catalog so one
Task template serves both ordinary and harness work. Preserve controlled QA
wrapper requirements in Stage 00 and Task evidence, not in catalog README
prose.

- [ ] **Step 6: Run GREEN, search references, and commit**

Run:

```bash
rg -n "harness-task-contract.template.md" docs .agents .claude .codex
python3 -m unittest tests.validation.test_document_metadata.TemplateMetadataTests tests.validation.test_document_metadata.TemplateBodyContractTests -v
bash scripts/validation/check-doc-traceability.sh
git diff --check
```

Expected: the reference search returns no active link; tests and traceability
pass.

After both reviews:

```bash
git add docs/99.templates/templates/sdlc docs/99.templates/templates/governance docs/99.templates/support/template-selection.md docs/00.agent-governance/rules tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "docs(execution): consolidate plan and task forms"
```

## Task 5: Stage 05 Operations Forms

**Files:**

- Modify: `docs/99.templates/templates/operations/guide.template.md`
- Modify: `docs/99.templates/templates/operations/policy.template.md`
- Modify: `docs/99.templates/templates/operations/runbook.template.md`
- Modify: `docs/99.templates/templates/operations/incident.template.md`
- Modify: `docs/99.templates/templates/operations/postmortem.template.md`
- Modify: `docs/99.templates/templates/operations/release.template.md`
- Modify: `docs/99.templates/templates/operations/README.md`
- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Test: `tests/validation/test_document_metadata.py`

**Interfaces:**

- Consumes: Task 1 operation roles and unchanged common lifecycle.
- Produces: six non-overlapping Operations forms, Incident root behavior, one
  Runbook recovery section, and Release-event evidence boundaries.

- [ ] **Step 1: Add failing Operations boundary tests**

Add these form and parent assertions:

```python
def test_operations_forms_have_non_overlapping_headings(self) -> None:
    base = ROOT / "docs/99.templates/templates/operations"
    guide = (base / "guide.template.md").read_text()
    policy = (base / "policy.template.md").read_text()
    runbook = (base / "runbook.template.md").read_text()
    for forbidden in ("## Rollback or Recovery", "## Escalation"):
        self.assertNotIn(forbidden, guide)
    self.assertNotIn("## Procedure", policy)
    self.assertEqual(1, runbook.count("## Rollback or Recovery"))

def test_incident_profile_allows_root_but_event_children_stay_strict(self) -> None:
    incident = self.profiles["profiles"]["incident"]
    postmortem = self.profiles["profiles"]["postmortem"]
    release = self.profiles["profiles"]["release"]
    self.assertTrue(incident["allow_empty_parents"])
    self.assertEqual(["incident"], postmortem["allowed_parent_types"])
    self.assertFalse(postmortem["allow_empty_parents"])
    self.assertEqual(["spec", "plan", "task"], release["allowed_parent_types"])
    self.assertFalse(release["allow_empty_parents"])

def test_release_template_does_not_create_an_event_leaf(self) -> None:
    leaves = [
        path
        for path in (ROOT / "docs/05.operations/releases").glob("*.md")
        if path.name != "README.md"
    ]
    self.assertEqual([], leaves)
```

- [ ] **Step 2: Run RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.MetadataValidationTests -v
```

Expected: failures for duplicate Runbook recovery and Incident root rejection.

- [ ] **Step 3: Normalize Guide, Policy, and Runbook**

Use these required H2 headings:

| Role | Required H2 headings |
| --- | --- |
| Guide | Overview; Audience and Prerequisites; Routine Usage; Common Checks; Runbook Handoff; Related Documents |
| Policy | Overview; Scope; Controls; Exceptions; Verification; Review Cadence; Related Documents |
| Runbook | Overview; Trigger and Preconditions; Procedure; Verification Record; Evidence; Rollback or Recovery; Escalation; Related Documents |

Guide may contain routine task steps but not recovery procedure. Policy owns
what and why controls. Runbook owns executable steps, expected results,
evidence, recovery, and escalation.

- [ ] **Step 4: Normalize Incident, Postmortem, and Release**

Use these required H2 headings:

| Role | Required H2 headings |
| --- | --- |
| Incident | Overview; Incident Metadata; Impact; Timeline and Response; Evidence; Resolution and Handoff; Related Documents |
| Postmortem | Overview; Incident and Impact; Timeline; Root Cause and Contributing Factors; Lessons; Action Items; Prevention and Verification; Feedback Loop; Related Documents |
| Release | Overview; Identity and Scope; Included Changes; Artifacts; Validation Evidence; Approvals; Rollout and Rollback; Outcome and Known Issues; Related Documents |

Keep Incident response state, Postmortem analysis, and Release lifecycle facts
in their bodies. Do not add a second frontmatter state key.

- [ ] **Step 5: Change Incident parent behavior**

Set `profiles.incident.allow_empty_parents` to `true` and retain Runbook as an
allowed parent. Keep Postmortem and Release parent requirements unchanged.
Update tests and human contract wording together.

- [ ] **Step 6: Normalize the Operations catalog and run GREEN**

Make `operations/README.md` satisfy the template-catalog profile and route to
support selection. Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.MetadataValidationTests tests.validation.test_document_metadata.TemplateMetadataTests -v
find docs/05.operations/releases -maxdepth 1 -type f -name "*.md" ! -name README.md
git diff --check
```

Expected: tests pass; the Release leaf search returns no path.

- [ ] **Step 7: Record reviews and commit**

```bash
git add docs/99.templates/templates/operations docs/99.templates/support/document-metadata-profiles.yaml docs/00.agent-governance/rules/stage-authoring-matrix.md tests/validation/test_document_metadata.py docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "docs(operations): canonicalize operations forms"
```

## Task 6: Executable Template and Target Validation

**Files:**

- Modify: `scripts/validation/check-document-metadata.py`
- Modify: `tests/validation/test_document_metadata.py`
- Modify: `scripts/validation/check-repo-contracts.sh`
- Modify: `docs/03.specs/130-template-contract-system-canonicalization/spec.md`
- Modify: `docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md`
- Modify: `docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md`
- Modify only if a RED test proves necessary: `.github/workflows/ci-quality.yml`

**Interfaces:**

- Consumes: Task 1 role registry and Tasks 2-5 normalized forms.
- Produces: `extract_markdown_headings(text) -> tuple[list[str], list[str]]`,
  `validate_body_contract(record, text, profiles, changed_boundary) ->
  list[Finding]`, machine-token validation, and a repository gate that delegates
  exact template semantics to the Python checker.

- [ ] **Step 1: Add failing body, ambiguity, and integration tests**

Add exact tests:

```python
def test_markdown_heading_extraction_ignores_fenced_examples(self) -> None:
    text = "# Title\n\n~~~text\n## Not a heading\n~~~\n## Overview\n"
    h1, h2 = metadata.extract_markdown_headings(text)
    self.assertEqual(["# Title"], h1)
    self.assertEqual(["## Overview"], h2)

def test_changed_target_rejects_template_instruction_and_body_token(self) -> None:
    text = "# Real Title\n\n> Rules:\n\n## Overview\n{{explain_scope}}\n"
    record = metadata.Record(
        pathlib.Path("docs/03.specs/901-fixture/spec.md"),
        {
            "status": "draft",
            "artifact_id": "spec:901-fixture",
            "artifact_type": "spec",
            "parent_ids": ["prd:901-fixture"],
        },
        "spec",
        frontmatter_present=True,
    )
    codes = {
        item.code
        for item in metadata.validate_body_contract(
            record, text, self.profiles, changed_boundary=True
        )
    }
    self.assertIn("template-instruction-in-target", codes)
    self.assertIn("template-body-token-in-target", codes)

def test_template_catalog_readme_requires_profile_headings(self) -> None:
    record = metadata.Record(
        pathlib.Path("docs/99.templates/templates/README.md"),
        {"layer": "agentic"},
        "readme",
        frontmatter_present=True,
    )
    codes = {
        item.code
        for item in metadata.validate_body_contract(
            record,
            "# Catalog\n\n## Overview\n",
            self.profiles,
            changed_boundary=True,
        )
    }
    self.assertIn("readme-heading-missing", codes)
```

Add these exact cases to the same class: `test_zero_role_match_reports_code`
expects `template-role-missing`; `test_ambiguous_role_match_reports_code`
expects `template-role-ambiguous`; `test_forbidden_heading_reports_code`
expects `body-heading-forbidden`; `test_conditional_heading_may_be_absent`
expects no finding; `test_two_h1_headings_report_code` expects
`body-h1-count`; `test_machine_source_requires_token` expects
`machine-template-token-missing`; `test_machine_source_rejects_example_host`
expects `machine-template-example-value`; and
`test_release_is_in_required_inventory` expects the Release source path.

- [ ] **Step 2: Run RED**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests tests.validation.test_document_metadata.RepositoryContractIntegrationTests -v
```

Expected: failures because heading extraction, body validation, token
validation, and Python-owned integration do not exist.

- [ ] **Step 3: Implement Markdown and machine-template validation**

Add:

```python
MARKDOWN_BODY_TOKEN = re.compile(r"{{[a-z][a-z0-9_]*}}")
MACHINE_TEMPLATE_TOKEN = re.compile(r"__[A-Z][A-Z0-9_]*__")
TARGET_TEMPLATE_LITERALS = ("<!-- Target:", "> Rules:", "## Template Usage")

def extract_markdown_headings(text: str) -> tuple[list[str], list[str]]:
    """Return H1 and H2 headings outside fenced code blocks."""

def validate_body_contract(
    record: Record,
    text: str,
    profiles: dict[str, object],
    changed_boundary: bool,
) -> list[Finding]:
    """Validate role headings, source tokens, and changed-target residue."""
```

Template sources require exactly one H1, every registered required H2, no
forbidden H2, and at least one body token unless the form is intentionally
literal. Target documents reject body tokens and template literals on the
changed/new boundary. Conditional headings remain optional. Machine sources
require explicit uppercase tokens and reject valid-looking Example,
example.com, and bearer-token literals.

- [ ] **Step 4: Make role matching and README headings fail closed**

Use `classify_template_role()` for changed/new typed targets and template
sources. Emit deterministic finding codes for missing and ambiguous roles.
Validate the six changed template catalog README files against their existing
profile headings without broad rewriting other README profiles.

- [ ] **Step 5: Remove duplicate shell-owned template semantics**

In `check-repo-contracts.sh` remove the hard-coded Python
`heading_requirements`, operation forbidden-heading table, and incomplete
required-template list. Keep the shell orchestration, but call:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-contracts
```

and the existing changed/new checker path. This makes the registry and Python
checker the only exact template schema.

- [ ] **Step 6: Atomically remove Target comments from changed direct docs**

Remove the transitional Target comments from Spec 130, this Plan, and the
active Task in the same logical change that removes the old requirement.
Update Spec 130 wording from transitional to implemented without changing its
approved intent.

- [ ] **Step 7: Run the full validation slice**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata -v
python3 scripts/validation/check-document-metadata.py --mode check-contracts
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
git diff --check
```

Expected: all tests and checks pass with zero contract violations.

- [ ] **Step 8: Record reviews and commit**

```bash
git add scripts/validation/check-document-metadata.py tests/validation/test_document_metadata.py scripts/validation/check-repo-contracts.sh docs/03.specs/130-template-contract-system-canonicalization/spec.md docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
git commit -m "test(validation): enforce template role contracts"
```

## Task 7: Direct Consumers, Generated Evidence, and Migration Waves

**Files:**

- Modify with preservation-oriented heading and template-residue migration:
  `docs/03.specs/123-agentic-engineering-audit-remediation/spec.md` through
  `docs/03.specs/129-document-contract-canonicalization/spec.md`
- Modify with preservation-oriented heading and template-residue migration:
  the seven typed Plans dated 2026-07-11 through 2026-07-13
- Modify with preservation-oriented heading and template-residue migration:
  the three typed Tasks dated 2026-07-11 through 2026-07-13
- Modify: `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md` through its generator
- Modify: `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md` through its generator
- Modify: `docs/90.references/llm-wiki/llm-wiki-index.md` through its generator
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md`

**Interfaces:**

- Consumes: all implemented contracts and validators from Tasks 1-6.
- Produces: a clean direct-consumer set, fresh generated evidence, and exact
  entry, validation, and exit rules for Waves A-E.

- [ ] **Step 1: Capture a direct-consumer report**

Run changed and active checks without editing consumers:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref main
python3 scripts/validation/check-document-metadata.py --mode check-active
rg -n "<!-- Target:|> Rules:|{{[a-z][a-z0-9_]*}}" docs/03.specs/123-agentic-engineering-audit-remediation docs/03.specs/124-compose-runtime-readiness-remediation docs/03.specs/125-infrastructure-operations-readiness-remediation docs/03.specs/126-security-supply-chain-remediation docs/03.specs/127-deployment-release-engineering-remediation docs/03.specs/128-agentic-audit-harness-consolidation docs/03.specs/129-document-contract-canonicalization docs/04.execution/plans docs/04.execution/tasks
```

Record each finding as required fallout, advisory historical structure, or
outside-scope wave debt.

- [ ] **Step 2: Apply preservation-oriented direct fallout**

Migrate all 17 baseline typed consumers to the new target contract. Remove
template-only Target comments, rename semantically equivalent required
headings, and remove copied authoring instructions. Preserve dates, commands,
counts, decisions, verdicts, execution results, and draft runtime-remediation
scope. Do not add conditional headings without topic evidence and do not
change the intended runtime work in Specs 124-127.

- [ ] **Step 3: Record exact migration-wave gates**

In the active Task evidence, record:

- Wave A: 89 active design documents; parent graph required before metadata.
- Wave B: 66 Guides, 64 Policies, and 61 Runbooks; review evidence required.
- Wave C: 229 completed and one superseded document; body preservation default.
- Wave D: five Archive tombstones; provenance confirmation required.
- Wave E: six generated documents; generator-only updates.

Each wave requires a new approved Spec and Plan before editing its corpus.

- [ ] **Step 4: Regenerate canonical evidence**

Run:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
```

Expected: the Wiki index and coverage report include all tracked paths and the
metadata inventory reports the post-change record and finding counts.

- [ ] **Step 5: Run complete pre-review validation**

Run:

```bash
python3 -m unittest tests.validation.test_document_metadata -v
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
git status --short
```

Expected: all commands exit 0; only approved Task 7 paths are modified.

- [ ] **Step 6: Update Progress and Task evidence**

Record each task commit, review verdict, validation command, generated count,
Graphify status, direct-consumer disposition, and Wave A-E boundary. Do not
record a final wrapper pass before the wrapper is executed.

- [ ] **Step 7: Commit the pre-closure state**

After both Task 7 reviews:

```bash
git add docs/03.specs docs/04.execution docs/90.references docs/00.agent-governance/memory/progress.md
git commit -m "docs(migration): align direct template consumers"
```

## Spec Coverage Matrix

| Spec 130 criterion | Owning plan work |
| --- | --- |
| SC-TCS-001 | Task 1 support ownership and role registry |
| SC-TCS-002 | Tasks 1-5 source roles and form normalization |
| SC-TCS-003 | Tasks 1 and 6 metadata and target enforcement |
| SC-TCS-004 | Tasks 1 and 2 Audit/Reference separation |
| SC-TCS-005 | Task 4 Task/Harness consolidation |
| SC-TCS-006 | Tasks 2 and 6 README source and heading enforcement |
| SC-TCS-007 | Tasks 3-5 duplicate-purpose section consolidation |
| SC-TCS-008 | Tasks 1, 3, 4, 5, and 6 stage traceability |
| SC-TCS-009 | Task 7 preservation-oriented migration of 17 typed consumers |
| SC-TCS-010 | Task 7 Wave A-E gates |
| SC-TCS-011 | Tasks 6 and 7 validation |
| SC-TCS-012 | Controlled final QA |
| SC-TCS-013 | Per-task and whole-branch reviews |
| SC-TCS-014 | Global constraints and whole-branch scope review |

## Verification Plan

### Per-task minimum

- Run the focused RED test before implementation.
- Run the same focused test after implementation and record GREEN.
- Run `git diff --check`.
- Run the smallest repository contract slice affected by the task.
- Obtain separate Spec PASS and Quality APPROVED verdicts.
- Commit only the task's approved paths.

### Pre-closure whole-branch review

After Task 7, dispatch a fresh reviewer with the full Spec, Plan, Task, and
`main...HEAD` diff. The reviewer must check:

- one canonical owner per rule and form;
- registry/source/target agreement;
- no duplicate Task, Audit, README, or Memory purpose;
- no copied support rules in templates;
- no invented metadata or historical evidence rewrite;
- changed/new and active validator behavior;
- Stage 01-05 feedback and traceability;
- no runtime or remote-state mutation.

Resolve all blocking findings and rerun the affected reviews and validation.

### Controlled final QA

From a clean committed worktree, run:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md --allow-prefix docs/ --allow-prefix scripts/validation/ --allow-prefix tests/validation/
```

Record the wrapper command, allowed prefixes, hook exit, snapshot result,
before and after path sets, changed paths, unexpected paths, and disposition.
Never include raw credential-bearing output.

### Lifecycle closure

After the wrapper passes:

1. Record the wrapper result and whole-branch verdict in the active Task.
2. Change Spec 130, this Plan, and the Task from active to completed.
3. Regenerate metadata inventory and LLM Wiki outputs through owner scripts.
4. Run metadata changed-mode, repository contracts, traceability, alignment,
   generator check modes, and `git diff --check`.
5. Commit only lifecycle and generated evidence:

```bash
git add docs/03.specs/130-template-contract-system-canonicalization/spec.md docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md docs/90.references docs/00.agent-governance/memory/progress.md
git commit -m "docs(task): close template contract canonicalization"
```

Do not rerun the all-files wrapper after the evidence-only closure commit;
record the exact clean pre-closure commit observed by the wrapper.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Role globs overlap | Reject overlap structurally and test all 23 positive matches plus ambiguous fixtures. |
| New body gate churns history | Enforce body residue and role contracts on template sources and changed/new targets; keep historical corpus advisory. |
| Target-comment removal creates a red intermediate commit | Change checker semantics and Spec/Plan/Task comments atomically in Task 6. |
| Audit matches README or generated inventory | Resolve README and generated profiles before Audit role matching and retain inventory exclusion. |
| Governance source metadata conflicts with template-source profile | Validate Memory and Progress source metadata through their explicit template roles. |
| Machine tokens break syntax | Parse YAML and use focused GraphQL/Protobuf fixture checks before commit. |
| Policy or Runbook dates are fabricated | Preserve current values and route unreviewed documents to Wave B. |
| Completed evidence is restyled | Task 7 requires a proven branch-caused failure before editing a historical body. |
| Shell and Python retain duplicate schemas | Remove shell-owned headings and inventory after Python integration tests pass. |
| Generated files drift after closure edits | Regenerate before pre-closure commit and use check mode after review fixes. |

## Rollback

- Revert tasks in reverse order from Task 7 to Task 1.
- Restore checker behavior before restoring templates that depend on the old
  mapping.
- Restore deleted Harness or Memory paths only with every reference and
  ownership contract; never leave two active canonical owners.
- Regenerate metadata and Wiki outputs after any registry or path rollback.
- If a target matcher becomes ambiguous, stop changed/new enforcement for the
  affected task by reverting that task commit; do not add an unreviewed
  exception.
- If the controlled wrapper reports unexpected paths, stop, preserve the
  evidence, and inspect those paths before cleanup or closure.

## Completion Criteria

- All 23 Markdown form roles have unique sources and deterministic target
  classification.
- Stage 99 support documents have one canonical concern owner each.
- README, Audit, Task, and Memory duplicate-purpose defects are closed.
- Templates contain only profile-compatible metadata, one H1, registered body
  sections, explicit tokens, and Related Documents.
- PRD through Release role boundaries match Spec 130.
- Incident roots validate; Postmortem and Release parent contracts remain
  strict.
- Repository checks consume the registry instead of hard-coded duplicate
  heading and template tables.
- Changed/new targets reject template instructions and unresolved body tokens.
- The 17-document baseline plus Spec 130, its Plan, and its Task remains valid.
- Generated inventory and LLM Wiki outputs are fresh.
- Waves A-E have exact scope and approval gates without broad migration.
- Every task has implementation, specification, quality, validation, and commit
  evidence.
- Whole-branch review has no unresolved blocking finding.
- Controlled final QA passes with no unexpected paths.
- No runtime, secret, deployment, remote GitHub, or global provider state
  changed.

## Related Documents

- [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Stage 99 template system](../../99.templates/README.md)
- [Metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Template contract](../../99.templates/support/template-contract.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Controlled QA wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
