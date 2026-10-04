---
title: "Policy Convergence and Safe Authoring"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0207-TSK-0001"
parent_ids:
- "SPEC-0207"
- "SPEC-0207-PLAN-0001"
created: "2026-10-04"
---

# Policy Convergence and Safe Authoring

## Objective

Complete W1–W3: converge P01 policy ownership and document the evidence without
manufacturing authorization, execution, review, or hosted results.

## Inputs

- Approval source: the latest actual current user request delivered through the
  controller's native conversation channel on 2026-10-04. It authorizes
  reversible local P01 policy/documentation edits, the archive-record
  helper/direct-consumer/focused-test clarification, and one local logical
  commit. The native channel does not automatically expose account-identity
  verification; its authority is not fabricated from Task fields.
- Authorization procedure: resolve that latest origin, confirm actor, exact
  operation, target/path, revision or scope, recovery, and withdrawal state,
  then compare the result with this Task's structural record. An absent,
  mismatched, or revoked source blocks only its dependent protected operation;
  independent safe documentation work continues. An operator can directly
  perform an unsupported protected action through its trusted channel; repository
  tools do not authenticate it or relax the native sandbox.
- Excluded: secret, live, remote, provider/model, global-config, or sandbox
  operations; remote push, PR, merge, and hosted execution remain unapproved.
- Before source: `830ab0583f65e1252badb6be34b79c92bcb3c293`; current HEAD,
  index, and dirty paths were re-observed before mutation.
- Requirements and architecture: REQ-0024, AD-0027, ADR-0032.
- Stage 99 allocation: the original `spec` identity-space owner recorded
  `high_water: 206` and `next_number: 207`. This Task allocates SPEC-0207
  atomically as `high_water: 207`, `next_number: 208`; no historical identity
  is reused and no archive shape changes.

## Work Log

### W1 source and consumer matrix

| Concern | Current owner | Actual consumer or route | Disposition |
| --- | --- | --- | --- |
| Protected-operation authorization | `approval-boundaries.md` | `environment-constraints.md`, `workflows.md`, `agentic.md` | Converge here; records are not authentication. |
| Secret and runtime execution evidence | `environment-constraints.md` §§2.1–2.2 | Task evidence for concrete operations | Retain protocol; route authorization to approval owner. |
| Lifecycle approval and review | `workflows.md` | role routing and Task evidence | Keep review read-only; prevent repeated approval for unchanged current scope. |
| Budget and unsupported native controls | `agentic.md` | delegation/resumption envelope | Keep separate from safety denial; preflight required checks. |
| Change verification matrix | `quality-standards.md` | local/hosted gate selection | Reference current authorization owner; no duplicate budget policy needed. |
| Provider/native facts | `providers/registry.yaml`, `.codex/provider.md` | generated adapters and hooks | Consumer only; native sandbox unchanged. |
| Archive approval record match | `scripts/lib/document_governance/archive_assessments.py` | `_assessment_change` → `validate_archive_assessments` → `archive.validate_retention` | Hook developer relabels it as read-only structural validation; no authenticator exists. |
| Archive history-only payload check | `scripts/lib/document_governance/archive_snapshots.py` | `_archive_payload_findings` calls the archive record matcher for assessment consistency | Structural integrity consumer only; a passing check never entitles removal. |

### W1 full authorization-to-executor route

| Stage | Source fact and route | Result |
| --- | --- | --- |
| Policy | Baseline `830ab0583f65e1252badb6be34b79c92bcb3c293`: `approval-boundaries.md` Core Rules contained the blanket value-read prohibition; `environment-constraints.md` §2.2 contained the concrete secret-operation protocol; `workflows.md` Change Lifecycle owned approval/review order; `agentic.md` owned token/time/concurrency and unsupported-native-control reporting. | Current P01 policy routes authorization to approval boundaries, preserves §2.2 execution evidence, separates review, and keeps budget from overriding safety. |
| Role | `.agents/roles/doc-writer.md` declares `permission_profile: workspace-write`; `.agents/roles/rules-engineer.md`, `code-reviewer.md`, and `workflow-supervisor.md` declare `read-only`; `.agents/roles/hook-developer.md` owns the archive helper change. | `doc-writer` owns these policy/docs writes. Reviewers remain read-only and their review is not authorization. |
| Skill | The writer read `.agents/skills/adr-writing/SKILL.md`, `.agents/skills/knowledge-map-agent/SKILL.md`, and `.agents/skills/ops-runbook-agent/SKILL.md`. No ADR or executable runbook is required, so neither is invoked to create an artifact. `hook-developer` has no `skill_ids`; no canonical execution-plan skill is claimed as invoked. The independent reviewers used `.agents/skills/policy-gate-agent/SKILL.md` (`rules-engineer`) and `.agents/skills/change-review-execution/SKILL.md` (`code-reviewer`). External `using-superpowers`, `brainstorming`, and subagent-driven-development availability was confirmed at plugin version `6.4.2` in `.codex-plugin/plugin.json`; it supplies no additional repository authority or progress ledger. | Role/skill selection did not expand mutation authority. |
| Provider and projection | `providers/registry.yaml:211` maps permission profiles and `:226` maps Codex hook contracts. `.codex/provider.md`, `.codex/hooks.json`, and verified projections `.codex/agents/doc-writer.toml`, `rules-engineer.toml`, `code-reviewer.toml`, `workflow-supervisor.toml`, and `hook-developer.toml` map canonical roles to native mechanics. | Provider surfaces are consumers. They do not authenticate current authority or lower the native sandbox. |
| Hook and dispatcher | `.codex/hooks.json` sends `PreToolUse` to `scripts/hooks/agent-event-hook.sh`; its lines 224–228 provide a `command` only for Bash and pass edit targets separately to `hook_rules.evaluate`. `scripts/lib/hooks/tool_payload.py` supplies the separately normalized edit targets. | A documentation edit containing a protected example is authoring content. Actual Bash is a distinct native tool operation evaluated by the hook path. |
| Executor | The native execution path used `functions.exec` → `tools.exec_command` or `apply_patch`; the repository's Bash/edit adapters are tested separately. Native provider hook delivery and runtime acceptance remain unverified. | No native permission limit was reduced or claimed observed. |
| Archive record consumers | `_assessment_change` calls `_approval_record_matches` at `archive_assessments.py:593`; direct callers also occur in `validate_assessment_snapshot` at `:626` and historical validation at `:698` and `:757`. `archive_snapshots.py:_archive_payload_findings` calls it at `:331`. `archive.validate_retention` calls `validate_retention_catalog`, then assessment and snapshot validation. | Every route validates historical record structure only. No route authenticates the actor, enforces revocation, or entitles removal. |

### W1 same-action rule comparison

| Pinned source fact | Requested action | Allow or deny | Approval owner | Completion evidence |
| --- | --- | --- | --- | --- |
| Pre-P01 `approval-boundaries.md` Core Rules prohibited all secret-value reads; `environment-constraints.md` §2.2 allowed metadata inspection and required concrete secret-operation evidence | Write redacted secret examples or synthetic dangerous-command inputs | Allow as local authoring; do not read values or execute the example | Current trusted user scope for local docs; approval boundaries for protected execution | Diff, metadata/link checks, Task receipt; no value output |
| `documentation-protocol.md` current assessment and Git-history-only availability section formerly treated a pinned original Task approval as sufficient through later lifecycle changes | Preserve completed original archive disposition; attempt a pending/new removal | Preserve the historical record; deny the new removal without current source | Approval boundaries operator procedure; record compared separately | Original regular historical Task blob plus current operator scope/recovery check; archive validator is structural only |
| `workflows.md` Change Lifecycle approval step and routine-review paragraph | Continue unchanged P01 local scope after review | Allow without repeated human approval; deny scope expansion | Current explicit user request, bounded by approval boundaries | Task scope/receipt and independent review; review is not authorization |
| `scripts/hooks/agent-event-hook.sh:224-228` sends only Bash `command` to hook rule evaluation; edit targets are passed separately | Edit documentation containing a dangerous command; execute that command | Allow the edit under doc-writer scope; separately evaluate actual Bash execution | Approval boundaries; provider sandbox remains native | Exact tool input and hook result; no claim that text authoring executed a command |
| `archive_assessments.py:_approval_record_matches` lines 377-448 validates a regular historical Task blob, owner quote, action, date, and evidence heading | Validate an archive authorization record; authorize actual removal | Allow structural validation; deny entitlement inference | Current trusted operator route for removal | Focused missing/mismatched record fixtures; no automatic actor authentication or revocation enforcement claim |
| `archive.py:validate_retention` calls catalog/assessment/snapshot validation; `archive_snapshots.py:_archive_payload_findings` consumes the matcher | Run archive integrity validation | Allow read-only validation; deny mutation entitlement | No authorization is created by the validation | Exit/result is integrity evidence only; actual destructive action stays `NOT_RUN` |

### W2 file disposition

| File | Disposition | Result |
| --- | --- | --- |
| `.agents/governance/approval-boundaries.md` | modify canonical authorization owner | PASS: scoped review and fresh changed gate |
| `.agents/governance/environment-constraints.md` | modify routing; retain runtime/secret protocol | PASS: scoped review and fresh changed gate |
| `.agents/governance/workflows.md` | modify approval/review and Historical boundary | PASS: scoped review and fresh changed gate |
| `.agents/governance/agentic.md` | modify budget preflight and unknown native control boundary | PASS: scoped review and fresh changed gate |
| `.agents/governance/documentation-protocol.md` | distinguish frozen disposition record from current removal authorization | PASS: scoped review and fresh changed gate |
| `.agents/governance/task-checklists.md` | require current operator route and fixture integrity cases for archival action | PASS: scoped review and fresh changed gate |
| `docs/99.templates/contracts/document-frontmatter.schema.json` | add historical-record-only description without changing shape | PASS: scoped review and fresh changed gate |
| `docs/99.templates/registry.json` | allocate SPEC-0207 in the existing `spec` identity space | PASS: fresh metadata and changed gate |
| `docs/03.specs/0207-common-authorization-and-safe-authoring/**` | add active package and evidence | PASS: fresh metadata and changed gate |
| `docs/03.specs/README.md` | add navigation link | PASS: fresh metadata, links, and changed gate |
| `scripts/lib/document_governance/archive_assessments.py` | hook-developer-owned structural helper rename/docstring | PASS: focused Ruff check/format check reported clean; one reviewer-found indentation regression was corrected in one scoped retry |
| `scripts/lib/document_governance/archive_snapshots.py` and focused archive-record test | hook-developer-owned sole consumer/test clarification | PASS: focused Ruff/dispatcher checks plus fresh document-library (`629` OK) and hook/payload (`52` OK) leaves |

## Verification Evidence

- Source discovery and policy-to-consumer routing: PASS as recorded above.
- Branch preflight: branch `codex/p01-common-authorization` was created from
  `830ab0583f65e1252badb6be34b79c92bcb3c293`; user approval is local branch
  only. `provider_surface_renderer.py --check`: PASS (`providers=2`, `drift=0`)
  before policy-only source updates. Graphify report and CLI: NOT_RUN (unavailable).
  Core hooksPath was observed as `/home/hyunyoun/.codex/git-hooks`; it was not
  read or changed. A clean `/tmp` QA virtual environment was provisioned with
  `uv` and `scripts/requirements.txt`; prior `ensurepip` and existing-directory
  `uv` attempts failed without host changes.
- Fresh candidate `8960f69a3efc1c29b0835151789676124a711cdba32b32a606333106040fc954`
  changed-gate session `53003` PASS (exit `0`):
  `rtk /tmp/hy-home-p01-qa-uv-u0r02jaa/bin/python scripts/validation/run-ci-gate.py --profile changed`.
  Output: `/tmp/hy-home-p01-changed-gate-final.txt`. Observed leaves: metadata `130` OK
  in `249.514s`; document library `629` OK in `598.674s`; operations `239` OK
  in `81.402s`; provider renderer `providers=2 drift=0`; agent governance
  `0` failures; links `1094` docs / `10919` links / `0` failures / `1` warning;
  lifecycle and archive recovery `0` violations; hook/payload `52` OK in
  `2.664s`; native/provider `59` OK in `44.838s`; governance `53` OK in
  `70.806s`; migration `16` OK in `25.961s`; final leaf `176` tests OK in
  `52.104s`. Conftest isolated validation (`16`/`270`/`69`) passed, as did the
  baseline, CI pre-commit wrapper, and GitHub workflow contract. Expected
  negative-case `ERROR` lines in those tests are not gate failures. The warning is the pre-existing
  `2870` retained historical links without capture-source resolution; it is not
  resolved or attributed to P01.
- Hook-developer focused source check: `ruff check` and `ruff format --check`
  over `archive_assessments.py`, `archive_snapshots.py`, and
  `tests/validation/test_hook_rules.py` reported PASS (exit 0; three files
  already formatted). `python3 -m unittest
  tests.validation.test_hook_rules.DispatcherTests.test_authoring_content_does_not_execute_its_protected_example`
  reported `Ran 1` / `OK` (exit 0). An independent reviewer found one indentation
  regression; its single scoped retry passed
  `ArchiveAssessmentTests.test_pinned_matching_task_approval_passes` (`Ran 1` /
  `OK`, exit 0), one-file Ruff, and `git diff --check`. No RED result was
  recreated or claimed. The initial default-sandbox Ruff attempt failed with
  `bwrap` exit 1 and the QA-venv Ruff lookup returned 127; the succeeding
  existing Ruff binary performed no installation. These are not RED/GREEN
  evidence and do not prove authorization enforcement.
- Positive/negative invariants: `tests/validation/test_hook_rules.py` adds
  `DispatcherTests.test_authoring_content_does_not_execute_its_protected_example`,
  which permits a documentation edit containing the protected example and keeps
  actual Bash on its separate evaluation path. `tests/lib/document_governance/metadata/test_profile.py`
  uses `_registered_section_findings` to accept the free-form
  `Authorization Source and Records` heading and reject a missing
  `Related Documents` heading; `TemplateMetadataTests` reported `14` OK after
  the worker correction. These tests validate routing and document profile
  invariants, not actor authentication or automatic revocation.
- First-run focused hook source evidence remains PASS. The first changed gate did
  not complete archive/full validation after its two failures; the fresh-candidate
  hook/payload leaf and fresh aggregate are PASS as recorded above.
- Gate leaves observed: lifecycle violations `0`, archive recovery violations `0`,
  and combined hook/payload regressions `52` tests `OK` in `3.089s`. The canonical
  Python Commitizen `4.15.1` was installed only in the `/tmp` QA environment;
  commit-message validation succeeded (exit `0`). The Task remains in progress
  only until the actual local implementation commit is recorded.
- First changed-gate execution: FAIL (exit `1`; `130` tests in `245.911s`; two
  failures). `test_current_requirement_packages_satisfy_repository_contracts`
  reported `identity-allocation-not-advanced` because the new SPEC lacked its
  Stage 99 allocation. A separate worker test snapshot had the wrong
  `free_form_sections` contract. This Task adds only the required SPEC identity
  allocation; the hook worker owns the test correction. The fresh changed-gate
  PASS above is the rerun for this corrected candidate; the initial failure
  remains historical evidence and is not presented as a pass.
- Operator handoff: missing, mismatched, or revoked current authorization stops
  the dependent protected operation through the documented manual procedure.
  Fixture checks cover historical-record integrity only; automatic actor
  authentication and revocation enforcement remain unsupported/UNKNOWN.
- Native authorization enforcement, provider entitlement/model operation,
  live/runtime/remote/hosted behavior: NOT_RUN; no authorized execution target.
- Staged secret scan: `gitleaks --redact --config .gitleaks.toml` PASS, no
  leaks. Commit-message input `fix(governance): Separate authorization from
  authoring records` passed Python Commitizen `4.15.1` in the `/tmp` QA
  environment only. No commit or normal-hook result exists yet.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: complete source-to-executor matrix, fresh changed gate, and scoped review | [approval boundaries](../../../../.agents/governance/approval-boundaries.md) |
| 2 | W2 | PASS: safe authoring and separately denied sensitive execution are documented and tested | [approval boundaries](../../../../.agents/governance/approval-boundaries.md) |
| 3 | W2 | PASS: structural-record boundary and missing/mismatched fixture invariants pass; automatic revocation remains UNKNOWN | [documentation protocol](../../../../.agents/governance/documentation-protocol.md) |
| 4 | W2 | PASS: read-only review and native-limit boundary pass scoped review and gate | [workflows](../../../../.agents/governance/workflows.md) |
| 5 | W2 | PASS: safety/budget separation passes scoped review and gate | [agentic policy](../../../../.agents/governance/agentic.md) |
| 6 | W3 | PENDING actual local commit receipt; source, QA, and independent review are PASS, and remote finish remains `NOT_RUN` | [this Task](tsk-0001-policy-convergence.md) |
| 7 | W3 | PASS: current-source procedure and fixture boundary pass; automatic revocation remains UNKNOWN | [task checklists](../../../../.agents/governance/task-checklists.md) |

## Review Evidence

- Read-only rules-engineer pre-implementation review: supplied to the writer;
  it confirmed the P01 policy scope and archive-record distinction.
- Frozen source packet `8960f69a3efc1c29b0835151789676124a711cdba32b32a606333106040fc954`:
  `policy_review` returned PASS; independent `final_code_review` approved the
  spec/source conditionally on final QA and approved quality with no findings.
  The later scoped review accepted the registry/test/Skill evidence correction
  with no source findings. Review is evidence, not authorization.
- Superpowers procedure: the root read and applied installed
  `using-superpowers/SKILL.md` and `brainstorming/SKILL.md`, then read
  `subagent-driven-development/SKILL.md` and selected that single execution
  route. The installed version is `6.4.2` at
  `/home/hyunyoun/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/.codex-plugin/plugin.json`.
  The procedure was adapted to the existing Stage 03 package, approved scope,
  canonical roles, budget/retry limits, and this Task ledger. It created no
  external docs, parallel progress ledger, model override, or global install;
  `executing-plans`, skill-creator, skill-stocktake, skill-improver, and Harness
  procedures were not used. The actual delegation was read-only rules-engineer
  policy review, doc-writer policy work, bounded hook-developer code work, and
  independent code review.

## Commit Ledger

No commit exists yet. The reviewed, QA-passing candidate is prepared for one
local logical commit with message `fix(governance): Separate authorization from
authoring records`; after creation, locate the containing commit by this exact
message and its prepared diff rather than rewriting this Task with its own SHA.

## Rulings

- The current trusted user/operator/native channel is the supported authority
  source; no automatic source authenticator is claimed.
- The original completed archive disposition remains a frozen structural record.
  A later lifecycle change does not rewrite it, while any pending or new removal
  still requires a current trusted-operator source. Missing, mismatched, or
  revoked current authorization is rejected by that procedure; automatic
  revocation enforcement is UNKNOWN.
- A redacted or synthetic command in documentation is authoring content, not
  execution. Actual sensitive, live, remote, credential, and destructive
  operations stay separately explicit.
- No provider sandbox, hook, or wrapper bypass is permitted.
- Local rollback is `git revert` of the containing logical commit. Remote
  push/PR/merge, hosted CI, live service observation, archive follow-up, and
  provider/model operations are `NOT_RUN`.

## Deferred Items

- Actual local implementation-commit receipt, then a Task-only execution receipt
  after narrow metadata/link/diff checks; remote PR/push/merge, hosted checks,
  and archive follow-up remain `NOT_RUN`.
