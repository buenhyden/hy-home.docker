---
title: "Common Document Contract Adoption Task"
version: "0.1.0"
type: "sdlc/task"
status: "blocked"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0209-TSK-0001"
parent_ids:
- "SPEC-0209-PLAN-0001"
created: "2026-10-05"
---

# Common Document Contract Adoption Task

## Objective

Perform the approved common-document contract adoption and retain truthful,
current evidence for each acceptance criterion.

## Inputs and Authorization

- SPEC-0209, its Plan, REQ-0024, REQ-0026, AD-0027, AD-0030, and ADR-0037.
- User-provided contract attachment with SHA-256
  `f19249ad20d9f05e29cd63ac547dbb2984fb7c9b01c79b747cb8545820fca179`.
- Stage 99 generation 4 at source revision `8b85e88fe2dfef54f4cc125ee2687982c86c1942`.

The actual user implementation message authorizes the scoped local migration,
including documentation, Stage 99 Registry, schemas, templates, necessary
checks, and coordinated consumer, test, and generated-projection work. This
writer owns only the documentation, Registry, schema, and template portion;
the assigned QA owner owns scripts, tests, and generated projections. It does
not authorize pushes, PRs, archive disposition, secrets, runtime execution, or
provider calls.

The actual user implementation message is the scoped authorization origin for
local source changes, necessary QA, and authorized local commits. Attachment
digests, Git source objects, metadata structure, and read-only review do not
authenticate that origin or grant approval. Automatic account or native-actor
authentication is unsupported; no approval API or runtime grant is claimed.

## Work Log

### Execution Procedure and Preflight

Root selected one installed Superpowers 6.4.2 execution pipeline: the earlier
explicit reads of `using-superpowers`, `brainstorming`, and
`subagent-driven-development`, plus its Codex reference, informed discovery,
approved planning, delegated implementation, and independent verification.
The skill sources were
`/home/hyunyoun/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/using-superpowers/SKILL.md`,
`/home/hyunyoun/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/brainstorming/SKILL.md`,
and
`/home/hyunyoun/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/subagent-driven-development/SKILL.md`.
Execution adapts that pipeline to this approved Stage 03 package and the
repository's initial attempt plus one narrower correction after failed
verification; it creates no external `docs/plans` or extra progress ledger.

Root's actual tool preflight observed the QA interpreter
`/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python`: Python 3.12.3, PyYAML 6.0.3,
jsonschema 4.26.0, and Commitizen 4.15.1. Ruff 0.16.10 was available at
`/home/hyunyoun/.local/bin/ruff`. The markdownlint-cli2 0.23.3 version check
reported markdownlint 0.41.1; that startup invocation matched zero source files
and proves tool version only. `conftest` and `trivy` were unavailable on root's
PATH; neither was installed and no scan PASS is claimed.

Numeric budgets and hard native enforcement were not provided and remain
UNKNOWN. The user's scope authorizes necessary local checks; remote, live,
paid, and protected external calls remain unauthorized. Actual model names,
entitlement, and native writer-payload transmission were not observed. Root
observed global `core.hooksPath` as `/home/hyunyoun/.codex/git-hooks`; its
contents and execution remain UNOBSERVED and untouched. No future commit-hook
execution is claimed. Raw authentication data, logs, and global memory were not
read.

### Preserved References and Integration Boundary

Earlier root observations bound `main` to
`2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`; it remained unchanged and is
excluded from integration. The P01 follow-up at
`68e0bfd3edb0895235dc628d03d427ca9fd14736` was not imported or merged, and
the prior review worktree `/tmp/hy-home-p01-review-20261004` was preserved.
Completed SPEC-0208 source `8b85e88fe2dfef54f4cc125ee2687982c86c1942` and its
Task body remain preserved as recorded in the focused source receipt. These
were earlier actual baseline observations. Root's subsequent read-only check
again observed HEAD `8b85e88fe2dfef54f4cc125ee2687982c86c1942`, branch
`codex/p02-common-document-contract-adoption`, the same main and P01 references,
an empty index, only this package's three untracked source files, and the
existing prior review worktree. No merge or commit had occurred at that check.

- 2026-10-05: verified the attachment digest and recorded the initial allocation
  as current `208` and next `209`; created this governed package before bulk
  migration.
- 2026-10-05: issued SPEC-0209 with its requested Plan 0001 and Task 0001,
  advancing the existing Spec allocator from high-water/next `208/209` to
  `209/210`. No identity was reissued and no separate child counter was created.
  The scoped `rtk proxy python3 -B -` mutation asserted the prior values and
  validated the updated Registry against its JSON schema (exit 0).
- 2026-10-05: completed the current Stage 99 source inventory and concrete
  consumer mapping below. Numeric budgets and native enforcement remain unknown.
- 2026-10-05: root observed a clean branch baseline, Python 3.12.3 with
  PyYAML 6.0.3 and jsonschema 4.26.0, and available local diagnostic tools.
  Native hook delivery and numeric enforcement were not observed.
- 2026-10-05: Project-Template loaded a clean compared Registry with no
  diagnostics; all 23 matched target types differed from the proposal except
  ADR lifecycle edges. hy-home.k8s rejected `archive/route` at its loader and
  its later-observed Registry and loader were dirty, so that comparison is
  DEFERRED. Blog-data was absent. These are observations, not adoption claims.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0209 | draft | approved | #inputs-and-authorization |
| SPEC-0209 | approved | in-progress | #work-log |
| SPEC-0209-PLAN-0001 | draft | approved | #inputs-and-authorization |
| SPEC-0209-PLAN-0001 | approved | in-progress | #work-log |
| SPEC-0209-TSK-0001 | draft | ready | #work-log |
| SPEC-0209-TSK-0001 | ready | in-progress | #work-log |
| SPEC-0209 | in-progress | blocked | #retry-budget-reconciliation |
| SPEC-0209-PLAN-0001 | in-progress | blocked | #retry-budget-reconciliation |
| SPEC-0209-TSK-0001 | in-progress | blocked | #retry-budget-reconciliation |
| SPEC-0209 | blocked | in-progress | #bounded-resumption-authorization |
| SPEC-0209-PLAN-0001 | blocked | in-progress | #bounded-resumption-authorization |
| SPEC-0209-TSK-0001 | blocked | in-progress | #bounded-resumption-authorization |
| SPEC-0209 | in-progress | blocked | #local-integration-handoff |
| SPEC-0209-PLAN-0001 | in-progress | blocked | #local-integration-handoff |
| SPEC-0209-TSK-0001 | in-progress | blocked | #local-integration-handoff |

### Package Authorization and Source Binding

The approved attachment digest and source revision in Inputs and Authorization
bind this migration to its observed generation-4 source.

### Contract Migration

| Date | Source revision | Evidence |
| --- | --- | --- |
| 2026-10-05 | 8b85e88fe2dfef54f4cc125ee2687982c86c1942 | #package-authorization-and-source-binding: approved attachment SHA-256 and source binding |

- 2026-10-05: migrated active Hookify documents from `governance/hook-policy`
  to `governance/rule`, and the active SDLC document from `governance/sdlc`
  to `governance/workflow`. Registry profile types follow those mappings;
  native fields remain unchanged.

Whole-Stage-99 source inventory and disposition (all current source files):

| Path | Owner and actual consumer | Disposition |
| --- | --- | --- |
| `docs/99.templates/README.md` | Stage 99 documentation integrator → `Current navigation; metadata/heading.py::validate_body_contract` | Adopt common/readme core and direct-child Path/Purpose table. |
| `docs/99.templates/contracts/document-frontmatter.schema.json` | Stage 99 documentation integrator → `registry.py::validate_registry / validate_frontmatter` | Preserve existing typed extensions; adopt common and cancellation value shapes. |
| `docs/99.templates/contracts/document-profile.schema.json` | Stage 99 documentation integrator → `registry.py::validate_registry / validate_frontmatter` | Preserve existing typed extensions; adopt common and cancellation value shapes. |
| `docs/99.templates/registry.json` | Stage 99 documentation integrator → `registry.py::load_registry / validate_registry` | Adopt generation 5 exact profiles, lifecycles, and common table contracts. |
| `docs/99.templates/templates/README.md` | Stage 99 documentation integrator → `Current navigation; metadata/heading.py::validate_body_contract` | Adopt common/readme core and direct-child Path/Purpose table. |
| `docs/99.templates/templates/architecture/decision.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID adr; current type sdlc/architecture-decision` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/architecture/description.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID architecture-description; current type sdlc/architecture-description` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/archive/migration.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID migration; current type archive/route` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/archive/tombstone.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID tombstone; current type archive/route` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-category.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID reference-category-readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-documentation.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID documentation-readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-package.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID package-readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-repository.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID repository-readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-runtime-governance.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID runtime-governance-readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/common/readme-stage.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID readme; current type common/readme` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/contract.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-sdlc; current type governance/workflow` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/control.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-policy; current type governance/policy` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/knowledge.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-knowledge; current type governance/control` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/prompt.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-prompt; current type governance/prompt` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/provider.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-provider; current type governance/provider` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/role.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-role; current type governance/role` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/rule.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-hook-policy; current type governance/rule` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/governance/skill.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID governance-skill; current type governance/skill` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/operations/guide.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID guide; current type operation/guide` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/operations/incident.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID incident; current type operation/incident` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/operations/policy.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID policy; current type operation/policy` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/operations/postmortem.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID postmortem; current type operation/postmortem` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/operations/runbook.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID runbook; current type operation/runbook` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/audit-pack.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID audit; current type reference/audit-pack` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/audit.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID audit-member; current type reference/audit` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/data-pack.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID data; current type reference/data-pack` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/data.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID generated; current type reference/data` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/research-pack.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID research; current type reference/research-pack` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/references/research.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID research-member; current type reference/research` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/requirements/requirement-package.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID requirements-package; current type sdlc/requirement` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/runtime/claude-agent.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; native authoring copy source` | Preserve native projection syntax and consumed fields. |
| `docs/99.templates/templates/runtime/codex-agent.template.toml` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; native authoring copy source` | Preserve native projection syntax and consumed fields. |
| `docs/99.templates/templates/specs/contracts/data-model.template.md` | Stage 99 documentation integrator → `Registry media/profile reader; metadata/heading.py::_validate_template_source` | Retain existing interface or data-model contract shape outside the 28-profile attachment. |
| `docs/99.templates/templates/specs/contracts/openapi.template.yaml` | Stage 99 documentation integrator → `Registry media/profile reader; metadata/heading.py::_validate_template_source` | Retain existing interface or data-model contract shape outside the 28-profile attachment. |
| `docs/99.templates/templates/specs/contracts/schema.template.graphql` | Stage 99 documentation integrator → `Registry media/profile reader; metadata/heading.py::_validate_template_source` | Retain existing interface or data-model contract shape outside the 28-profile attachment. |
| `docs/99.templates/templates/specs/contracts/service.template.proto` | Stage 99 documentation integrator → `Registry media/profile reader; metadata/heading.py::_validate_template_source` | Retain existing interface or data-model contract shape outside the 28-profile attachment. |
| `docs/99.templates/templates/specs/plan.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID plan; current type sdlc/plan` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/specs/spec.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID spec; current type sdlc/spec` | Adopt ordered profile core and exact semantic authoring shape. |
| `docs/99.templates/templates/specs/task.template.md` | Stage 99 documentation integrator → `metadata/heading.py::_validate_template_source; profile ID task; current type sdlc/task` | Adopt ordered profile core and exact semantic authoring shape. |

### Read-only Cross-repository Comparison

This comparison is discovery evidence; it is outside the mandatory local
adoption criterion and grants no foreign edit, network call, or adoption claim.

| Repository | Source and loader | Observation | Result and limit |
| --- | --- | --- | --- |
| Project-Template | `/home/hyunyoun/data/Project-Template`, HEAD `9fc61181a89d3065d3977e791d4b6af26c30c567`; `scripts/lib/registry_loading.py::load_registry(path, repo_root=root)`, Python `-B` | Exit 0, zero diagnostics, 51 profiles, 23 of 28 proposed types matched. All 23 core tuples differed; ADR states and edges matched while its fields and core differed. Registry SHA-256 `d5c05d6a4caeaa3e50b586961f999430ede1f332a57edce046c13edfd831192e`; targeted Registry, loader, and parser were clean after observation. | Observed local loader result only. |
| hy-home.k8s | `/home/hyunyoun/data/hy-home.k8s`, HEAD `7fc8829858bdcdf27e3ab93c23e62cb2a84df751`; `scripts/document_contracts.py::load_registry(root)` | Exit 1: `REGISTRY_AUTHORITY` caused by `LIFECYCLE_NODE_SET` for `archive/route` in `document_authority`. Registry and loader were dirty. Later Registry SHA-256 `6463a73eff2a2082c07a9d4b08f82f281362d650e52f51570666199c4d99743d` is not a prebound digest for that failure. | DEFER; no retry, fix, bypass, or stable-source comparison claim. |
| Blog-data | Known location `/home/hyunyoun/data/blog-data` | Absent at that location. | UNOBSERVED; no machine-global absence claim. |

### Consumer Ownership and Source Disposition

| Owned source | Actual consumer or caller | Disposition |
| --- | --- | --- |
| Stage 99 Registry profiles, lifecycle graph, identity spaces, and template roles | `scripts/lib/document_governance/registry.py::{load_registry,validate_registry,document_type,classify_path,validate_frontmatter,validate_profile_values}` | Adopt exact 28 proposed type contracts within existing profiles; retain registered identities, paths, optional consumed extensions, and scalar successor. |
| Stage 99 frontmatter and profile schemas | Registry validation; `frontmatter.py::{frontmatter_record_from_text,parse_frontmatter_text,safe_load_unique}`; `metadata/lifecycle.py::validate_record` | Type and quote shared scalars, reject duplicate keys, and validate cancellation reason, authorization reference, and criterion dispositions. |
| Registered Markdown templates | `metadata/heading.py::{validate_body_contract,_registered_section_findings,_validate_template_source}`, through Registry `template_roles` | Adopt ordered semantic cores and exact table columns; preserve authoring-language prompts and destination-specific modules. |
| Native interface templates and provider projection templates | Registered media profiles and `metadata/heading.py::_validate_template_source` | Preserve OpenAPI, GraphQL, Protocol Buffer, TOML, and native envelope syntax; QA owns projection rendering and parity from canonical role/skill inputs; these templates remain validated authoring examples. |
| Current Stage 01, 02, 03, 05, and 90 authored Markdown and README navigation | `metadata/reference.py::{_validate_repository_contracts,validate_repository_contracts,main}`, metadata-validator facade, taxonomy `classify_path`, and link checks | Current-document writer adopts profile cores and updates active inbound links. |
| Nonterminal Stage 03 Spec, Plan, and Task | `spec_packages.py::{load_spec_packages,validate_repository_spec_package_lifecycle_details}`; `archive.py::validate_active_stage_occupancy` | Frontmatter-only Task status, six-column Plan, eight-column Evidence; root retains closure ownership. |
| Canonical governance and knowledge; authored provider adapters, roles, skills, and prompts | Bootstrap and authored adapters; provider renderer consumes authored role/skill and Provider Registry inputs, not Stage 99 template files | Documentation integrator owns governance/knowledge; native-document writer owns role/skill/prompt/adapter sources. Metadata adoption proves no native delivery or authorization authentication. |
| Hookify rule sources | `scripts/hooks/hook_rules.py::load_rules`; dispatcher `scripts/hooks/agent-event-hook.sh` | Rule cores adopt `governance/rule`; native event/action/conditions remain unchanged in meaning. The existing consumer needs no type-guard change; preserve its supported single-line native serialization and run focused QA checks. |
| Generated provider projections | Provider renderer writes registered `.claude/agents/*.md`, `.codex/agents/*.toml`, and other registered outputs | QA only; regenerate from canonical sources, then check parity. |
| Frozen Stage 98 bodies, sealed route records, completed Task bodies, original Commit Ledgers, and historical provenance | Archive source-object readers and generation-3/4 compatibility readers | Preserve source bytes and original evidence; generation migration binds exact source revision rather than a historical-path allowlist. |

### Tool Denial and Recovery

After source migration, the repository PreToolUse hook rejected even a read-only
`rtk proxy git diff -- .agents/governance/hooks/hookify.block-git-no-verify.md`:
`Repository hook policy could not be loaded or evaluated; resolve the policy
configuration before retrying.` The user’s native-terminal diagnosis loaded `scripts/hooks/hook_rules.py::load_rules`
and reached its `re.compile` call at line 155. It failed for
`hookify.block-gha-secrets-in-run.md` with `bad escape (end of pattern) at
position 68`. The YAML serializer wrapped a long double-quoted native regex at
its default width, which the native single-line parser could not unfold.
The initially suggested loader path and type-guard cause were unverified and
withdrawn. The supported scoped repair preserves the adopted common six fields
and body, verifies native values against source `8b85e88fe2dfef54f4cc125ee2687982c86c1942`,
and restores original raw native header lines for the existing Hookify sources.
The reported repair and observed local tool resumption are recorded below.
Full native event delivery remains unverified; subsequent local consumer checks
are recorded below. No disabled hook, alternate
wrapper, alias restoration, or repeated denied command was used.

The user reported the scoped repair restored native serialization for 18
Hookify files and `load_rules` loaded 16 rules. Root subsequently observed a
successful ordinary read-only Git-status tool call (exit 0). These observations
establish recovery of local policy loading; they do not establish full native
event delivery, runtime acceptance, or approval authentication. Subsequent
authoring preserves the restored native header lines.

Current `docs/98.archive/README.md` and `retention-catalog.md` are editable
management documents, separate from frozen payloads. This migration changes
their current envelope/core/navigation only; capture and assessment rows and
all frozen bodies and sealed route records remain preserved.

### Focused Source Checks

- 2026-10-05: root independently ran a read-only Python stdin diagnostic with
  `git ls-tree`, `git show`, and `git diff` against source
  `8b85e88fe2dfef54f4cc125ee2687982c86c1942` (exit 0). All seven source-terminal
  completed/cancelled Task Markdown bodies matched current full bytes; their
  combined ordered source SHA-256 was
  `c9d855d2ce8c31513a334b2ec77c26a246a7a43e46571739d2de978b85624918`.
  Stage 98's diff contained only its current `README.md` and
  `retention-catalog.md` management documents; no frozen payload or sealed route
  changed. These observed counts are this source comparison's receipt, not a
  permanent filename/count allowlist or closure claim.
- 2026-10-05: QA traced all generation-5 evidence callers to the canonical
  top-level common sections, columns, and domains. The current Registry retired
  its unused `spec_completion_evidence` and `review_evidence` objects; the
  profile schema rejects them at generation 5 and retains the generation-1–4
  reader contract. QA routes historical receipts through the exact migration
  source Registry. `task_lifecycle_events` remains actively consumed. The
  scoped `rtk proxy python3 -B -` JSON/schema check passed (exit 0).
- 2026-10-05: the same scoped stdin diagnostic validated the exact generation-4
  Registry from `git show 8b85e88fe2dfef54f4cc125ee2687982c86c1942:docs/99.templates/registry.json`
  against the updated profile schema and confirmed that a generation-5 candidate
  carrying the retired `review_evidence` object is rejected (exit 0). A final
  nonempty-core/native-header diagnostic and owned whitespace rerun passed
  (exit 0); no public gate was run by the documentation writer.

- 2026-10-05: `rtk proxy python3 -B -` with an inline read-only diagnostic
  passed (exit 0). Inputs were the approved attachment,
  `docs/99.templates/registry.json`, both existing JSON schemas, registered
  Markdown template sources, and the owned current Markdown listed in the
  source/disposition inventory. The assertions compare required fields/cores,
  exact initial states/status lists/direct edge sets, and Registry jsonschema.
  The diagnostic also compared catalog table lines and raw Hookify native
  header blocks using `git show 8b85e88fe2dfef54f4cc125ee2687982c86c1942:<path>`.
  The scan covered 80 owned document/template records, exact lifecycle initial
  states, status lists, edge sets, required frontmatter and ordered cores.
- 2026-10-05: baseline comparison at the bound source revision confirmed all
  current Retention Catalog table rows and all 18 Hookify native header blocks
  unchanged. The current archive index and catalog envelope/core are editable;
  frozen payloads and sealed records remain outside migration.
- 2026-10-05: `rtk proxy git diff --check -- docs/99.templates
  docs/03.specs/0209-common-document-contract-adoption .agents/governance
  .agents/knowledge .agents/README.md README.md docs/98.archive/README.md
  docs/98.archive/retention-catalog.md` initially reported two trailing blank
  lines. A scoped whitespace correction removed them; the rerun passed (exit 0).
- 2026-10-05: `rtk proxy python3 -B -` with an inline current-link diagnostic
  checked Markdown link anchors in root/shared READMEs, owned governance and
  knowledge, Stage 99, SPEC-0209, and the current archive index/catalog; it
  found zero missing anchors (exit 0).
- 2026-10-05: `rtk proxy python3 -B -` with AST-only source inspection
  confirmed the concrete consumer definitions and imports: Registry itself
  defines `classify_path` and taxonomy imports that facade; metadata lifecycle,
  heading, and reference callers import it. No consumer was executed by this
  symbol inspection (exit 0).

### QA Attempts and Approved Resumption

The initial broad metadata/archive run used this exact invocation against
its pre-correction source:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest -q tests.lib.document_governance.metadata.test_profile tests.lib.document_governance.metadata.test_heading tests.lib.document_governance.metadata.test_lifecycle tests.lib.document_governance.metadata.test_reference tests.lib.document_governance.metadata.test_identity tests.lib.document_governance.test_metadata_validator tests.lib.document_governance.test_archive
```

It executed 222 tests in 393 seconds with 18 FAIL and 2 ERROR. Findings included
generation-5 versus historical heading/receipt handling, stale fixtures, and
seven empty optional template `parent_ids`. The next selected run attempted 15
selectors and reported 8 FAIL and 2 ERROR; source inputs changed during the
run, and both errors were incorrect frozen-test class selectors rather than
executed leaf failures. Its original selector string was not retained after
compaction and is not reconstructed here. Both failed attempts remain failures.

The actual user reply authorized one additional remaining correction and final
checks attempt. That scoped reply is the consent origin for the resumed local
work; no digest, assignment, or native identity authenticates it. QA corrected
existing consumers and fixtures, treating omitted optional template parents as
absent. The seven optional template `parent_ids: []` fields remain omitted.
No broad empty-array exemption or rejected alternative was applied.

Review found cancelled-Task PASS/accepted rows could count toward Spec
completion. This exact command was RED (`SpecPackageError not raised` for
cancelled-only proof), then GREEN (one test OK) after a completed-status filter:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest -v tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_v5_evidence_uses_frontmatter_status_and_exact_eight_columns
```

Requirement parsing crossed a following H2 boundary. Its exact RED command
incorrectly parsed `REQ-0001-FR-9999`:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest -v tests.lib.document_governance.test_requirements.RequirementPackageTests.test_h3_requirement_sections_stop_before_the_following_h2
```

The final suite below verified the corrected boundary, historical H2 handling,
wrong-parent exclusion, and filled current template groups. The template now
uses Functional, Non-functional, and Interface Requirements H3 groups while
preserving its required H2 core, envelope, and placeholder IDs.

The current Spec profile no longer permits `spec` as a structural parent.
The existing shared cancellation successor pattern now admits exact public
Spec, Plan, or Task IDs: `^SPEC-[0-9]{4}(?:-(?:PLAN|TSK)-[0-9]{4})?$`.
Narrow read-only JSON/relation and positive/negative pattern checks passed
(exit 0), retaining allocator `209/210`. Consumers enforce corresponding
family, existence, noncancelled successor, and Task assignment semantics.
Syntax grants no authorization; historical source Registry objects are intact.

### Final Focused QA Results

The first final selection used this exact command:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest -v tests.lib.document_governance.test_requirements.RequirementPackageTests.test_h3_requirement_sections_stop_before_the_following_h2 tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_unreviewed_historical_completion_rows_do_not_become_v5_proof tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_v5_evidence_uses_frontmatter_status_and_exact_eight_columns tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_v5_cancellation_requires_authorization_and_criterion_disposition tests.lib.document_governance.metadata.test_lifecycle.CurrentSpecRelationTests tests.lib.document_governance.metadata.test_heading.CurrentBodyContractTests.test_additional_body_token_is_blocked_without_value_leakage tests.lib.document_governance.metadata.test_heading.CurrentBodyContractTests.test_new_file_body_deficit_is_blocked tests.lib.document_governance.metadata.test_heading.RuntimeVersionBodyTests.test_changed_mode_uses_the_current_profile_body_contract tests.lib.document_governance.metadata.test_profile.CurrentRegistryContractTests.test_current_requirement_packages_satisfy_repository_contracts tests.lib.document_governance.metadata.test_profile.TemplateMetadataTests tests.lib.document_governance.metadata.test_reference.MetadataValidatorCompatibilityTests.test_generated_inventory_has_registered_audit_metadata tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_repository_contracts_validate_canonical_spec_packages tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_registry_contracts_parse_profile_and_section_contracts tests.lib.document_governance.metadata.test_reference.ReadmeSectionProfileTests.test_every_readme_profile_that_declares_sections_is_satisfied tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_stage_03_occupancy_is_judged_per_package tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_every_frozen_migration_is_byte_identical tests.lib.document_governance.test_archive.ArchiveMinimizationTests.test_frozen_migration_is_byte_identical_at_prefixless_path tests.lib.agent_governance.test_agent_governance_contract.AgentGovernanceContractTests.test_read_only_canonical_directory_is_valid tests.validation.test_provider_surface_renderer
```

Result: 76 tests in 224.227 seconds, 74 PASS, one stale fixture expectation FAIL,
and one incorrect selector ERROR. QA reported all executed production, corpus,
and provider cases in that selection passed. The command as a whole remains
failed. The final narrower invocation corrected its selector/fixture scope:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest -v tests.lib.document_governance.test_requirements.RequirementPackageTests.test_h3_requirement_sections_stop_before_the_following_h2 tests.lib.document_governance.test_requirements.RequirementPackageTests.test_current_requirement_template_groups_are_all_parsed tests.lib.document_governance.metadata.test_heading.CurrentBodyContractTests.test_additional_body_token_is_blocked_without_value_leakage tests.lib.document_governance.metadata.test_heading.CurrentBodyContractTests.test_new_file_body_deficit_is_blocked tests.lib.document_governance.metadata.test_heading.RuntimeVersionBodyTests.test_real_active_cli_rejects_runtime_pin_and_accepts_authority_link tests.lib.document_governance.metadata.test_profile.CurrentRegistryContractTests.test_current_requirement_packages_satisfy_repository_contracts tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_repository_contracts_validate_canonical_spec_packages tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_registry_contracts_parse_profile_and_section_contracts
```

Result: eight tests OK in 189.835 seconds. This selected current-source check
does not represent a repeated full 222-test suite or the public changed gate.
Both exact projection commands passed: two providers, zero drift.

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/operations/provider_surface_renderer.py --write
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/operations/provider_surface_renderer.py --check
```

The before/after structured authority digest across 28 role projections stayed
`83465853341a33c5f7176cc94ddd7dee13038312ffc47f1a7c37df284a71d6fa`.
Its scope was Claude tools/model/effort/permissionMode/skills and Codex
model/reasoning/sandbox, excluding content. This proves field preservation and
local parity, not native delivery, entitlement, or approval authentication.

Initial scoped Ruff found four lint findings and eight format files.
Deterministic formatting and import/unused-name corrections produced these
exact final commands:

```sh
/home/hyunyoun/.local/bin/ruff check scripts/lib/agent_governance/agent_governance_contract.py scripts/lib/document_governance/archive.py scripts/lib/document_governance/metadata/heading.py scripts/lib/document_governance/metadata/lifecycle.py scripts/lib/document_governance/metadata/reference.py scripts/lib/document_governance/registry.py scripts/lib/document_governance/requirements.py scripts/lib/document_governance/spec_packages.py tests/lib/document_governance/metadata/test_heading.py tests/lib/document_governance/metadata/test_lifecycle.py tests/lib/document_governance/metadata/test_profile.py tests/lib/document_governance/test_archive.py tests/lib/document_governance/test_registry.py tests/lib/document_governance/test_requirements.py tests/lib/document_governance/test_spec_packages.py
/home/hyunyoun/.local/bin/ruff format --check scripts/lib/agent_governance/agent_governance_contract.py scripts/lib/document_governance/archive.py scripts/lib/document_governance/metadata/heading.py scripts/lib/document_governance/metadata/lifecycle.py scripts/lib/document_governance/metadata/reference.py scripts/lib/document_governance/registry.py scripts/lib/document_governance/requirements.py scripts/lib/document_governance/spec_packages.py tests/lib/document_governance/metadata/test_heading.py tests/lib/document_governance/metadata/test_lifecycle.py tests/lib/document_governance/metadata/test_profile.py tests/lib/document_governance/test_archive.py tests/lib/document_governance/test_registry.py tests/lib/document_governance/test_requirements.py tests/lib/document_governance/test_spec_packages.py
rtk git diff --check -- scripts tests .claude .codex
```

Lint reported all checks passed; format reported 15 files already formatted;
scoped whitespace exited 0. Earlier Registry 114-test, Spec-package 65-test,
Hook-rule 27-test, current-package loading (five packages/ten Tasks), and real
main generation 3 to source generation 4 to current generation 5 chain passes
are historical execution facts before the last corrections. Generation 3 had
no validation findings; exact generation 4 loaded 50 profiles. These earlier
checks are not the latest full implementation PASS. No final gate or staging
was run by QA or the documentation writer.

### First Staged Changed Gate

Root staged the implementation against HEAD
`8b85e88fe2dfef54f4cc125ee2687982c86c1942` and main
`2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`. The exact frozen staged
packet, generated by `git diff --cached --binary --no-ext-diff --no-textconv HEAD`,
had SHA-256
`78ee5f5ce1f0acdb8d6f54f227066ef44bf9ac0803645bf9536b832af42e485f`,
2,577,741 bytes, and 536 paths; its staged tree was
`f45aeddd2df6d81c84d688989f2f9d5a11152208`. Both read-only staged reviews
reported no blocking/Critical/Important findings: code review reported
Specification PASS and Quality PASS, with only the MINOR nested-heading
advisory; policy review reported no BLOCKER/HIGH. These results bind to that
packet and establish review, not QA success or authorization authentication.

The changed-gate `--explain` invocation exited 0. The actual gate command was:

```sh
PATH=/tmp/hy-home-p01-qa-uv-u0r02jaa/bin:$PATH TEMPLATE_GATE_BASE=main rtk proxy /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/validation/run-ci-gate.py --profile changed
```

Session 23797 exited 1 at the link leaf. Preceding suites reported 57, 53,
and 59 tests OK; provider parity passed, and the active-document status scan
checked 479 records with zero violations. The link scan inspected 1,100
documents and 11,006 links, 39 catalog pairs, 65 direct archive citations,
zero removed mentions, and 56 historical observations; it reported three
failures and zero warnings:

- `missing-link-target` in frozen
  `docs/98.archive/migrations/0004-research-package-consolidation.md:61`,
  for `../../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md`.
- `archive-link-contract-invalid` in current
  `docs/98.archive/retention-catalog.md`: cannot resolve Archive assessment/source contract.
- A current `docs/03.specs/README.md` navigation-label finding, subsequently
  corrected by its source owner; this correction has no gate PASS yet.

The current catalog's headings and capture columns match the Registry's
registered archive-retention contract. QA traced the caught exception to
`archive_assessments.py::_table`: the present prose-only Current Assessments
section had zero table lines, which the reader rejected. That failure invalidated
archive context and exposed MIG-0004's historical citation as a current missing
target. Frozen payloads and terminal Task source bytes remain preserved. The
first gate remains FAIL; fresh changed-gate validation is pending.

The user's actual reply, `두 로컬 검사 동작 승인`, explicitly approved the
two proposed local checks: the isolated cached Conftest job with network none,
read-only infrastructure input and cleanup, and Compose configuration reading
the existing `.env` without reporting its values. Neither check was reached
before the link failure. Their approval does not establish execution or PASS.

### Link Consumer Correction Receipt

QA added a focused regression and the shared two-line reader correction:
zero table lines return an empty assessment set, while malformed partial
tables still fail closed. An absent assessment row retains the registered
`unreviewed`/`retained` defaults; it grants no approval and introduces no
source alias or historical path exception. No catalog or frozen-source
mutation was needed. The existing exact-byte sealed-route resolver stayed
unchanged; QA observed MIG-0004 at the bound legacy revision and HEAD.

The exact RED invocation exited 1: one test in 0.279 seconds, ERROR with
`ValueError: archive table shape is invalid` from `_table`:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_archive_assessments.ArchiveAssessmentTests.test_present_empty_assessment_section_has_effective_defaults
```

The exact combined narrow recheck also exited 1: three selectors in 0.580
seconds. The first two passed; the third was a selector ERROR because the
module has no `LinkGovernanceTests` attribute. Its leaf did not execute, and
the combined command is not a PASS. No additional leaf retry was spent.

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_archive_assessments.ArchiveAssessmentTests.test_present_empty_assessment_section_has_effective_defaults tests.lib.document_governance.test_archive_assessments.ArchiveAssessmentTests.test_bad_rows_and_duplicate_assessments_fail_closed tests.lib.document_governance.test_links.LinkGovernanceTests.test_unchanged_sealed_route_uses_its_last_authored_revision
```

The following lint command initially could not execute due to bwrap, then
passed through the supported execution route. Root subsequently found a
format-check issue; one deterministic format correction and its confirmation
reported one file reformatted and one file already formatted, respectively.
QA's scoped diff check passed. No behavior change followed the tests.

```sh
/home/hyunyoun/.local/bin/ruff check scripts/lib/document_governance/archive_assessments.py tests/lib/document_governance/test_archive_assessments.py
/home/hyunyoun/.local/bin/ruff format tests/lib/document_governance/test_archive_assessments.py
/home/hyunyoun/.local/bin/ruff format --check tests/lib/document_governance/test_archive_assessments.py
```

These scoped results do not establish whole-gate success. Root owns the fresh
staged packet, read-only review supplements, and changed gate at the corrected
input; at that receipt the Task remained in progress with closure FAIL/pending.

### Second Staged Changed Gate

Root's corrected staged packet had SHA-256
`f7a37a6bce755532108b15f43adaddd577273de1a367d8e49ec5d055ee8e5af4`,
2,585,275 bytes and 538 paths, with tree
`7a182121c61cdb428b3cb2879f91a7bde62d7c80`. Both narrow read-only review
supplements passed with no blockers/Critical/Important findings; their scope
was the changed packet, not execution success or approval authentication.
The same recorded changed-gate command ran as session 34700 and exited 1.
It reached the document-governance-library leaf, which ran 664 tests in
599.994 seconds and failed with 9 FAIL and 30 ERROR. This was an actual failed
test run, not a timeout. Its 55,951-token output was truncated to head/tail;
the full 39 failing selector details were not retained and are not invented.

Before that failure, suites of 57, 53, and 59 tests and provider parity passed.
The active scan checked 479 records with zero violations. Link validation
checked 1,100 documents, 11,006 links, 39 catalog pairs, 65 direct archive
citations and 56 historical observations: zero failures and one warning.
`historical-links-unrecorded` at the current retention catalog reported 2,870
legacy links without capture source; their historical resolution remains
unverified. Lifecycle suites reported 15 tests/97.026 seconds, 52 tests/2.885
seconds, and 16 tests/24.976 seconds OK. Corpus violations were zero. Archive
recovery reported 5 migrations, 140 tombstones, 348 preserved records, 286
decisions, 374 recovery rows and zero violations. The metadata suite reported
133 tests/397.911 seconds OK. These passed leaves do not turn the gate into
a PASS; remaining changed-metadata/main, Conftest, Compose, supply-chain and
other later leaves were not reached by that failed gate.

Two known Requirement selectors failed because their fixtures omitted the
current Overview/Requirements/Scope/Related Documents core, before the
allocation exceptions they intended to exercise. One bounded Requirement
fixture batch was applied before HOLD; its focused two-test run reported OK
in 0.754 seconds. This result covers only those two tests, not the other 37
unretained failure details. QA subsequently supplied the retained exact command:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.test_requirements.RequirementPackageTests.test_child_declarations_follow_registry_allocation_state tests.lib.document_governance.test_requirements.RequirementPackageTests.test_duplicate_or_reused_child_identity_fails_closed
```

It exited 0, reporting two tests in 0.754 seconds, OK. The research fixture's
old three-section assertions versus the five-section current core are a
candidate correction only, pending fresh authorization.

### Main Comparison Metadata Check

After the failed gate, root separately ran this actual command as session
49280 and held record writes until it exited:

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref main
```

It exited 1 against explicit main merge base
`2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`: 576 selected records, 39
violations, zero legacy exceptions and zero overrides. Reported categories
included current README/catalog draft-to-active transitions; 0182/0204
Spec/Plan active-to-blocked and 0207 active-to-in-progress transitions;
historical 0208 Spec/Plan/Task incorrectly treated as new draft-initial
documents, with its preserved Task's six-column body rejected as missing the
eight-column current shape; and research 0085 review-to-in-review. The
main-comparison requirement is UNSATISFIED. No override, current alias, or
historical Task rewrite was applied to suppress these findings. QA's diagnosis
of the exact generation/source comparison consumer is read-only and pending.

### Bounded Resumption Authorization

On 2026-10-05, the actual user reply `정확한 한 차례 재개 승인` explicitly
approved one bounded resumption of the concrete continuation proposal below.
That manual reply is the authorization origin; this Task, its lifecycle rows,
digests, and structural references do not authenticate an actor or grant
approval. No automatic native account or approval API authentication is claimed.

The approved scope retains the already-applied archive-assessment consumer and
test correction, Spec-index navigation label, and Requirement fixture. QA is
the sole implementation writer for one coherent batch covering the stale
research assertions and actual metadata generation/source-binding corrections
before focused validation, the remaining final changed gate, review, and
authorized local commits. This authorization adds no documentation cleanup,
scope expansion, ledger, historical Task rewrite, or external action. All
664-test failures and 39 main-comparison violations remain recorded; resumption
itself proves no correction or validation PASS. The three actual
blocked-to-in-progress events cite this same-package evidence.

### Authorized Final Preflight

Within the latest user-authorized bounded resumption, QA ran this exact
focused invocation: eight tests OK in 5.899 seconds.

```sh
/tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python -m unittest tests.lib.document_governance.metadata.test_lifecycle.CurrentSpecRelationTests.test_only_an_unchanged_generation_status_replaces_the_older_base tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_generation_normalization_accepts_only_registered_named_edges tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_changed_mode_retains_repository_contract_findings tests.lib.document_governance.metadata.test_reference.RepositoryContractIntegrationTests.test_terminal_task_body_baseline_requires_exact_generation_blob tests.lib.document_governance.test_spec_packages.SpecPackageTests.test_current_repository_spec_packages_cover_spec_directories tests.lib.document_governance.test_requirements.RequirementPackageTests.test_child_declarations_follow_registry_allocation_state tests.lib.document_governance.test_requirements.RequirementPackageTests.test_duplicate_or_reused_child_identity_fails_closed tests.lib.document_governance.test_references.ProtectedResearchDeclarationTests.test_declared_leaves_keep_substantive_research_shape
```

The corrected source binding admits only equal statuses proven by the exact
generation source. The terminal Task baseline was intended to require exact
source blobs, but the later raw-byte review found the newline-normalization
defect recorded below; its byte-exact guard claim is not accepted. Current
lifecycle edges and alias rejection remain enforced; this is not an override.
Research assertions retain substantive declaration checks.

README header verification first used the wrong
`RegistrySectionContractTests` class, producing three loader ERRORs with no
test bodies executed. The corrected selection under
`tests.lib.document_governance.metadata.test_heading.RegisteredSectionContractTests`
ran `test_readme_documents_module_uses_registered_columns`,
`test_readme_documents_module_rejects_other_header_shapes`, and
`test_every_declaring_profile_accepts_its_own_contract`: three tests OK in
1.618 seconds. The shared Documents-header consumer is corrected without
further README content cleanup.

The final real comparison command was:

```sh
PATH=/tmp/hy-home-p01-qa-uv-u0r02jaa/bin:$PATH /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/validation/check-document-metadata.py --mode check-changed --base-ref main
```

It exited 0 at merge base `2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`,
with 576 selected records, zero violations, zero legacy exceptions, and zero
transition overrides. This supersedes the earlier intermediate comparison
results for this corrected input, while preserving their failed-run receipts.
Scoped Ruff lint passed on eight implementation/test files; format initially
found four line-wrap files, then reported all eight already formatted after
the deterministic correction. Scoped diff checking passed. These focused
results do not replace the failed 664-test run or establish a full rerun.
At that preflight receipt the fresh final gate was pending, status was in
progress, and criterion 5/W5 remained FAIL/pending. Its actual later result
and the blocked local-integration handoff follow.

### Latest Changed Gate and Raw-byte Review

The latest frozen packet had SHA-256
`9e6891f2f23203ca60a81c0902e49d7c2b2b4ee634a54cf36fced026f5422931`,
2,619,406 bytes and 540 paths, with tree
`9b8feb73c9c8f59ae9b514c2fcee9c018a26dd08`. Session 43334 ran the same
recorded changed-gate command and exited 1. Its document-governance-library
leaf ran 664 tests in 550.802 seconds with 6 FAIL and 18 ERROR.

All 18 errors came from
`test_taxonomy.StableDocumentTaxonomyTests.test_stage_01_requirement_package_filename_and_metadata_agree_exactly`
with `KeyError: parent_ids`. The six failures were reported in:

- `operations_catalog`: `current_tree_self_authoritative_archive_free`;
  `registry_schema_valid_optional_no_python_mirror`;
  `resolved_bundle_requires_published_postmortem_current_owner`, including
  published/GDE-0011 and published/no-corrective-action fixture subtests.
- `operations_taxonomy`: `operations_checker_executable_one_complete_route`.
- `references`: `declaration_pins_no_count_hash_or_commit`, because the
  Preservation Declaration now contains a historical SHA.

Before that failure, suites of 57, 53, 59, 15, 52, 16, and 137 tests passed.
The active scan checked 479 records with zero violations; link validation
checked 1,100 documents and 11,006 links with zero failures and one warning
for 2,870 uncaptured historical links. Their historical resolution remains
unverified. Corpus and archive-recovery violations were zero. Conftest,
Compose `.env` checks and later leaves were not reached and remain NOT_RUN.
The earlier explicit main CLI's 576 selected/zero-violation result is a
separate successful check at its recorded input, not this gate's result.

The later independent review found an Important raw-byte baseline defect in
`scripts/lib/document_governance/metadata/reference.py` at the reviewed lines
255 and 513: `_text_at_ref` uses `text=True`, while `Path.read_text` also
normalizes universal newlines. A frontmatter-only CRLF change can therefore
compare equal despite a different complete blob. The consumer guard has not
passed raw-byte preservation review. Root's actual source comparison still
observed all seven terminal Task raw-byte bodies preserved, with combined
SHA-256 `c9d855d2ce8c31513a334b2ec77c26a246a7a43e46571739d2de978b85624918`;
that observation is not a claim that the defective guard test passed.

Automatic approval review had rejected an unapplied broad historical-status
substitution because it could mask invalid transitions without demonstrated
exact identity/byte binding and tests. The implemented narrower alternative
requires equal source/current status with proven identity and lifecycle;
different statuses are not substituted. That safer status binding does not
resolve the newly identified raw-byte defect.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Attachment integrity and source binding | 1 | W1 | SHA-256 comparison | Approved attachment; source revision `8b85e88fe2dfef54f4cc125ee2687982c86c1942` | PASS | This Task, Inputs and Authorization | accepted |
| Whole Stage 99 source inventory | 1 | W1 | File, owner, consumer, and disposition review | Registry, schemas, templates, and READMEs listed in Work Log | PASS | This Task, Work Log | accepted |
| Registry and schema syntax | 2 | W2 | JSON parsing and jsonschema Registry validation | Registry and both JSON schemas | PASS | Documentation integrator focused check, 2026-10-05 | accepted |
| Authored whitespace | 2 | W2 | `git diff --check -- docs/99.templates` | Stage 99 tracked edits | PASS | Local focused check, 2026-10-05 | accepted |
| Common contract source migration | 2 | W2 | Exact attachment/profile/lifecycle comparison; jsonschema and ordered-core scan; focused current Registry parsing | Registry, schemas, registered Markdown templates; 80 owned core/template records and final selected checks | PASS | This Task, Focused Source Checks and Final Focused QA Results | pending |
| Current authored-document migration | 3 | W3 | Final selected current metadata/body/package checks and source link diagnostics | Current nonfrozen Markdown; corrected Requirement template | PASS | This Task, Final Focused QA Results | pending |
| Terminal Task and frozen-source preservation | 3 | W3 | Root read-only Python stdin with `git ls-tree`, `git show`, and `git diff` | Exact source revision `8b85e88fe2dfef54f4cc125ee2687982c86c1942`; current source tree | PASS | This Task, Focused Source Checks | pending |
| Consumer and projection compatibility | 4 | W4 | Final selected consumer checks, cancellation RED/GREEN, and projection write/check | Corrected current consumers; historical source readers; two providers and preserved authority fields | PASS | This Task, QA Attempts and Final Focused QA Results | pending |
| Raw-byte terminal Task guard | 4 | W4 | Independent review of source-blob equality | `_text_at_ref` and `Path.read_text` newline normalization in metadata reference consumer | FAIL | This Task, Latest Changed Gate and Raw-byte Review | pending |
| Closure evidence | 5 | W5 | Root staged reviews and latest changed gate; separate explicit main comparison | Latest packet `9e6891f2f23203ca60a81c0902e49d7c2b2b4ee634a54cf36fced026f5422931` | FAIL | This Task, Latest Changed Gate and Raw-byte Review | pending |

## Review and Completion

The Spec, Plan, and Task are blocked at the local-integration handoff.
Prior changed-gate executions failed, including the latest 6 FAIL/18 ERROR
run; the latest explicit main metadata CLI passed at its separately recorded
input. Earlier scoped reviews do not supersede the Important raw-byte finding.
Criteria 4/W4 and 5/W5 remain FAIL/pending, without mandatory acceptance.
Completion requires every assigned criterion/work pair's mandatory
`PASS` evidence and accepted review. Supplemental observations or
not-applicable records cannot satisfy a missing mandatory pair.

### Local Integration Handoff

The user explicitly declined the raw-byte correction with
`현재 결과만 기록하고 추가 수정 중단`. No further implementation repair is
authorized by the record reconciliation. The subsequent actual user message
`강제 병합하고, p01과 p02에 맞는 내용만 정리하여 main만 남긴다`, repeated
with the finishing skill and P01/P02 merge request, authorizes root's local
preservation commits, main integration, and branch/worktree cleanup after
preservation. It does not authorize the declined code fix or convert failed
validation into approval, acceptance, or completed lifecycle status.

This Task records the actual results and three in-progress-to-blocked events
against this same-package handoff. No merge or commit OID is claimed before
root performs and observes it. Frozen source and completed Task bodies stay
preserved; local integration remains root-owned. No additional tests, remote
actions, cleanup expansion, or new ledger are introduced by these records.

### Retry Budget Reconciliation

Policy review confirmed `.agents/governance/workflows.md:62-70` applies the
implementation retry budget to the attempt, not separately to each new gate
leaf. The earlier user-authorized additional correction/check attempt was
already consumed. Root incorrectly treated newly reached leaves as fresh
budgets when directing the already-applied link-consumer and Requirement
fixture corrections. This record discloses that interpretation error and does
not invent additional user consent or authenticate approval from a Task entry.
The three actual in-progress-to-blocked events above reflect outstanding
mandatory checks that awaited fresh authorization. At that blocked receipt,
this proposal authorized no further implementation, check, staging, or commit.
The subsequent actual user reply and its bounded scope are recorded separately
in Bounded Resumption Authorization.

The concrete continuation proposal retains the already-applied
`scripts/lib/document_governance/archive_assessments.py` correction,
`tests/lib/document_governance/test_archive_assessments.py` regression,
current Spec-index navigation label, and current-core Requirement fixture in
`tests/lib/document_governance/test_requirements.py`. It proposes one bounded
correction batch to align only the stale research shape assertions in
`tests/lib/document_governance/test_references.py` with the exact Registry core,
preserving URL validation, substantive content and document-type assertions,
and to correct the actual metadata comparison consumer's generation handling
using exact main-generation and source-8b85 Git object binding with minimal
negative cases. Diagnosis must identify that existing consumer before editing;
no guessed source file or broad compatibility exception is proposed.

After that batch, the proposal permits focused checks and the remaining final
public changed gate within SPEC-0209 W4 and the existing local-source/QA/local-
commit scope. It weakens no gate or schema, rewrites no preserved Task, adds
no cleanup or framework, and grants no live, remote, paid or secret action.
Only the two separately approved local Conftest/Compose checks retain their
existing scope. The fresh actual user reply approved this bounded proposal
through the manual origin recorded above; the written proposal itself remains
neither approval nor authentication evidence.

The independent policy review found no BLOCKER or HIGH canonical-policy,
authority, or generation-5 design conflict. It inspected bootstrap/provider
guidance, applicable rules-engineer procedures, approval boundaries,
documentation protocol, SDLC, authoring matrix, quality and role policy,
Provider Registry, the governing package and attachment, Stage 99 schema and
templates, and actual hook/consumer sources. This limited policy PASS is not
final implementation QA or staged review.

Independent code review identified cancelled-Task false completion coverage,
the H3/H2 requirement boundary, current Spec-parent lineage, historical-Task
early-return and mixed coverage, duplicate criterion-number collapse, assigned
cancellation-disposition gaps, and Spec/Plan cancellation-reference checks.
The initial final-source code review reported no Critical or Important findings
and specification/quality PASS against packet SHA-256
`28965f348da7ff55a578da18526030173c1e82b267e94fbe30cd79b40cc71aab`
(2,563,081 bytes: binary Git diff against HEAD plus sorted content of the three
untracked package files). This source-packet review predates this final receipt
update and is not the staged supplement, final gate, or closure acceptance.
Its remaining redundant nested-heading observations were MINOR advisory only.

Historical coverage binds to exact generation-4 source pairs and intersects
current assignments; it grants no new coverage or fabricated review.
Source SPEC-0207's Spec and Plan were in progress, with only Task 1 completed.
SPEC-0208's observed source PASS/accepted pairs were `1/W1`, `2/W2`, `3/W2`,
`4/W2`, `5/W3`, and `5/W4`; its current Plan was aligned to those actual pairs
without rewriting its completed Task. Missing-review or PARTIAL legacy
0207/0182/0204 evidence remains unaccepted. Nonterminal or blocked packages
need current proof for future closure.

### Bounded Source Cleanup Authorization

Automatic approval review rejected the proposed cleanup of 93 current
architecture, Spec, and reference Markdown paths. Its stated reason was that,
despite an exact manifest and bounded expression, the operation relied mainly
on agent scope claims rather than trusted user confirmation for that specific
cleanup. No files changed and no alternate role, tool, or wrapper was used.
The user subsequently explicitly approved this exact 93-wrapper/49-empty-core
cleanup. That actual user reply is the scoped consent origin; the manifest
digest identifies the proposal and does not authenticate approval. The current
document owner resumed through the normal supported route, within SPEC-0209's
existing local-source, QA, and local-commit scope.

Root's read-only manifest identifies two concrete corrections: remove only
redundant adjacent `## X` / empty `### X` / `### X` wrappers in the 93 matched
paths, and move existing Traceability links into the empty Related Documents
cores where those links are actually found. The 49 observed paths have empty
Related Documents cores; the scan does not establish that every path has an
existing Traceability block. Diagnose each path, move only actual existing
Traceability or related-link blocks, and record a factual absence and reason
where no relation exists. The proposal invents no relationship or artificial
`None` content. Its sorted JSON manifest keys are
`wrapper_paths` and `empty_related_paths`, with SHA-256
`72ba653ceab9d59b594870f2c6e86b5a093d349e2df109ca1415f516599fa768`.
These source-bound counts describe the observed proposal, not permanent
filename/count assertions. The approved current-document cleanup is complete.
Read-only review confirmed zero targeted triples, zero empty Related Documents
cores, and clean source whitespace. It moved 45 actual Traceability blocks
with anchors preserved and used existing Spec/Task relations for four Plans.
The preceding approval-review rejections remain recorded and caused no
mutation. Broader nested identical-heading noise is a MINOR advisory outside
this bounded cleanup; it has not expanded the authorized work.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Stage 99 Registry](../../../99.templates/registry.json)
