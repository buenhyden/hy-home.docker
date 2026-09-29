---
title: "Agent Contract Hardening Specification"
version: "1.0.0"
type: "sdlc/spec"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-09-29"
---

# Agent Contract Hardening Specification

## Overview

Make the existing agent operating contracts reliable at their actual consumers:
required checks cannot disappear into successful summaries; skill resources
cannot bypass repository boundaries; current instructions do not depend on
individual historical stage documents; and recovery readiness has an independent,
read-only review procedure. Reuse the canonical roles, provider projections,
knowledge, prompts, workflow dispatcher and model-free evaluation subsystem.

The owner approved the incremental design, option A, on 2026-09-29 after its
research/design review. That approval authorizes this written specification and
its allocation/index edits only. After independent review, the owner approved
this written specification on 2026-09-29 and authorized Plan authoring. Its
frontmatter is transitioning through the registered local predecessor states;
that machine state does not broaden the recorded human approval. The owner
approved the Plan and local execution on 2026-09-29, including reviewed logical
commits, while preserving the separate external/runtime boundaries. No acceptance criterion is reported as implemented here.

The incoming execution request normalized its repeated item 37 into R37 agents,
R38 workflows and R39 commands. This specification preserves all R01–R39 and the
T01–T33 acceptance scenarios as local request identifiers, not new Requirement
artifact IDs. The Acceptance Contract below defines their observable outcomes
without requiring the original attachments or a temporary report to execute it.

## Boundaries and Inputs

### Baseline and authorship boundary

The authored baseline is local main at
`24b3e45c7fba5f11455c2a9b333463dfccfd3398`, in a separate worktree on
`codex/agent-contracts`. Read current position from Git on every resumption;
this hash identifies an observation, not a permanent completion condition.
SPEC-0189 is allocated by concurrent work and is not reused, copied or changed.
This package allocates SPEC-0190. Preserve other worktrees and their dirty state.

The approved design reuses REQ-0024 and AD-0027. Their current navigation-only
knowledge wording and document-authority boundaries must be reconciled in the
later approved implementation where this specification extends them. A frozen
ADR or completed package is evidence, never implementation authorization.

Research examined all 14 canonical roles, 23 SKILL bodies and eight existing
skill-owned resources, with the registry, renderer, relevant validators, hooks,
workflow contract and evaluations. Tracked-path inventory was broader than body
review. No claim of a full service/runbook audit or native provider observation
follows from that inventory. Previously observed static results include role/
skill contract parsing, zero projection drift, model-free evaluations and hook
fixtures. They are baseline evidence, not acceptance of the changes below.

### Included implementation surfaces

The eventual Plan maps acceptance to exact files before any implementation:

- `.agents/governance/`: current approval/workflow, document-authority, output,
  Git tracking, verification and provider contracts; existing owners remain.
- `.agents/roles/`: bounded responsibility and skill-routing changes below.
- `.agents/skills/`: two existing helpers and their procedures, conditional
  recovery routing, and the new recovery-contract review skill and resources.
- `.agents/knowledge/` and `.agents/prompts/`: verified facts, invalidation and
  provider-neutral handoff contracts, without a new progress ledger.
- `.claude/settings.json`, authored provider adapters and existing hook code:
  narrower read/scratch grants and explicit missing-linter reporting; generated
  role/skill projections are changed only by the registered renderer.
- `scripts/lib/agent_governance/agent_governance_contract.py`,
  `scripts/lib/document_governance/links.py`, relevant hook and gate libraries,
  registered command entrypoints, `scripts/manifest.yaml`, existing tests and
  `.github/workflow-contract.yml`: contracts and their actual consumers.
- `evals/`: current model-free evaluator, catalog and runner; update obsolete
  criteria and add recovery review cases without moving the subsystem.
- Governing Stage 01/02 owners and necessary current Stage 05 descriptions,
  and their indexes: only descriptions needed for these approved contracts.
  Stage 99 changes are limited to this draft’s spec identity allocation; existing
  skill profiles suffice. Any later schema/template change needs an identified
  missing field and separate scope approval. No general document reorganization
  or retroactive rewriting of frozen records.

This authoring change touches only this draft, the Stage 03 index and the
monotonic spec allocation. Future protected edits remain unapproved until the
written specification and Plan receive their own approvals.

### Exclusions

No service start/restart/stop, rollout, restore, volume deletion, credential
read/rotation, raw log collection, automatic dependency installation, paid
model evaluation, global configuration/cache mutation, remote ticket/comment,
push, PR, merge, branch deletion or worktree archival is authorized. Live
observations require separately scoped approval. Docker CLI presence is not
permission to render the real environment or inspect container environments.

## Behavior Contract

### Validation commands and aggregation

`infra-validate/scripts/static-checks.sh` has a script-relative repository root,
closed argument grammar and help, quoted paths, bounded child execution and a
stable result contract. Root, subdirectory, skill-directory and space-containing
checkout invocations inspect the same authorized fixture inputs. Invalid flags
or operands fail before reading configuration. Git discovery failure is an error,
never an empty-file-set NOT_APPLICABLE result.

The infrastructure validation contract defines the required set once; the
helper does not infer optionality from whether a binary happens to be installed.
Its static baseline requires Git, Bash, the Docker CLI with Compose plugin,
YAML lint and shell lint when tracked infrastructure shell inputs exist. A
check with no eligible inputs is NOT_APPLICABLE only after successful discovery.
Any extra optional check states its explicit applicability and reason.

Per-check states are PASS, FAIL, BLOCKED, SKIPPED, NOT_APPLICABLE and NOT_RUN.
The summary includes check IDs, counts and safe failure metadata. Exit 0 means
all applicable required checks passed; exit 1 means an executed check failed;
exit 2 means invalid invocation or incomplete required evidence. In mixed
failure/incomplete runs exit 1 takes precedence while both states remain visible.
A missing required tool or plugin is BLOCKED and yields exit 2 unless an
executed failure takes exit-1 precedence. An unavailable optional check is
SKIPPED with a reason; successful discovery with no eligible input is
NOT_APPLICABLE. Required checks cannot be downgraded to optional SKIPPED.
Runtime and secret observations remain NOT_RUN, with their authorization reason.

The helper does not run `docker compose config` against a real checkout or call
`validate-docker-compose.sh` there. Reuse the existing validator only in a
repository-confined, secret-free temporary fixture copy whose inputs have been
reviewed. Use tracked source/configuration and explicit synthetic values;
exclude real environment files, credentials, ignored host data and external
symlink targets. Never run a secret generator or reach a Docker daemon to prove
static validity. If isolation or required inputs cannot be established, report
BLOCKED. Temporary ownership and cleanup are explicit, bounded and no-follow;
cleanup never removes pre-existing paths. An abnormal stop cannot corrupt the
source checkout, even if a task-owned temporary directory survives termination.
The existing public Compose validator interface remains intact unless its
shared root cause requires a separately scoped, caller-complete change.

Diagnostics carry check ID, child exit and a bounded error category. Arbitrary
Compose output, environment values and raw logs are not echoed. Synthetic secret
sentinels must remain absent from successful and failing reports. Output filters
preserve child failures. A timeout is reported, not silently retried forever.

`style-validation/scripts/classify-changed-files.sh` resolves generated markers
against the same repository root, not the caller's cwd. Its existing categories
remain stable, malformed invocation fails, and Git/read failures cannot silently
classify a generated file as authored. Both helpers retain skill-local ownership.

### Skill resources and recovery review

The current scripts/references/assets bundle structure remains permitted. The
canonical validator traverses resource trees within an explicit entry/output
bound, reusing its no-follow and identity-checking primitives. It admits regular
files and directories; rejects nested symlinks, FIFOs, sockets/devices, path
escape, races and unapproved executable resources without following or executing
them. Intentional executable scripts are admitted only in the skill's scripts
surface with a real procedure consumer. An executable bit outside that surface
cannot turn a reference or output asset into an implicit command.

A resource graph rooted in SKILL.md proves direct and transitive reachability.
Relative Markdown references and explicit local script/asset paths are supported;
unknown dependency syntax fails with a precise finding rather than executing an
import. A small explicit index is allowed only for a real unresolvable dependency;
no blanket manifest or direct listing of every transitive file is required.
Metadata and provider adapters are classified separately from procedure resources.
Current valid resources remain accepted. Shared CI/tests invoking a helper do
not, by themselves, change that helper's domain ownership.

Add `stateful-recovery-contract-review`, owned by read-only `iac-reviewer`, with
SKILL.md, agents/openai.yaml, references/recovery-contract.md and assets/verdict.md.
It reviews an explicitly supplied, sanitized recovery contract; it does not
perform a restore. Its verdict covers state/volume inventory, backup or provable
rebuild disposition, consistency, retention, capacity, encryption/key custody,
dependency/restore order, version compatibility, isolated target, RPO/RTO as
objectives versus observations, application acceptance, failure/stop conditions,
and responsible implementer/reviewer/human approver. Missing or contradictory
inputs produce BLOCKED with missing fields. A volume existing is not a backup;
a runbook or static test is not evidence of successful recovery.

Do not invent a machine recovery manifest or validator solely for this skill.
Connect its actual consumers through iac-reviewer, infra-cross-validate,
incident-response, ops-runbook-agent and the infrastructure workflow. Preserve
their distinct implementation, cross-check, incident and documentation roles.
Add model-free recovery fixtures including direct, paraphrased, ambiguous and
out-of-scope requests. Compare approved criteria with the no-skill baseline;
static rubric success is distinct from observed native trigger/performance.

### Roles, native configuration and workflow

Keep the 14 canonical role IDs. Clarify iac-reviewer's recovery review,
hook-developer's approved provider-registry/native implementation responsibility,
incident-responder's recovery-review handoff and workflow-supervisor's approval/
resume routing. Independent policy/model/security reviewers remain read-only;
no writer acquires authority to approve its own protected change.

Keep both providers' 14 role projections and existing explicit invocation
mechanisms. Register the new skill, regenerate native projections and prove
source preservation and a second unchanged generation. Unknown/retired role IDs,
orphan adapters, accidental tool expansion and unregistered delegation fail.
No new agents/commands/workflows/memory root is introduced. Model identifiers,
reasoning selections and needs_revalidation remain unchanged absent a separate
reviewed model decision and actual entitlement/runtime evidence.

Remove broad automatic grants for Docker resolved configuration, logs and full
inspect output. Preserve safe metadata-only commands where their current consumer
is justified. Remove unproven broad scratch write grants; if native scratch
support is required, validate the exact current root's ownership and no-follow
boundary before adopting a verified narrow permission form. A lexical prefix is
not ownership. Shell and indirect tool paths remain part of the threat model.

Keep Git hooks, provider hooks, editor actions and CI events distinct. Missing
optional PostTool linters produce visible SKIPPED evidence; the registered final
required gate still owns success. Existing normalization, malformed-payload
denial, timeout, retry and Stop behavior retain their tests. Do not execute a
mutating post-edit hook on another worker's checkout as a validation experiment.
Output style cannot hide failure, non-execution or required approval.

The common workflow distinguishes design approval, written-spec approval and
written-plan/execution approval. Infrastructure changes then follow static
validation and independent review before separately approved runtime action.
Incident evidence routes to corrective work; partial failure resumes only after
scope/source/ownership reconciliation. Existing bounded retries remain bounded.
The five GitHub workflows and their required/non-gating identities remain; no
second auto-review/test-generation/deployment pipeline is created.

### Document authority, knowledge, handoff and budget

Outside docs, README navigation and directory purpose remain allowed, while
links to individual stage documents and current authority dependence on such
documents are rejected. Normalize relative/absolute paths, GitHub blob/raw URLs,
percent encoding, case/separators, anchors, reference links, HTML and wiki forms.
Code fences are not a blanket authority exception. Output-path examples,
non-authoritative historical provenance and test negative controls are classified
by their actual use, not indiscriminately deleted.

Deterministic path/entrypoint findings are separate from human semantic review:
a plain path, artifact ID or old approval cannot substitute for a current rule.
The current rule is stated once in governance or its current fact owner. Machine
schema/registry/template access has a narrowly justified exception naming kind,
consumer, necessity and scope; no wildcard exemption admits individual documents.
Docs-internal traceability and investigation reads remain valid. R23 does not
ban reading the Spec/Task while executing approved work.

Use knowledge for verified durable/domain facts, the current Task for short-term
execution, and prompts/handoff.md for a derived transfer view. Retain one owner
per fact and no transcript/global cache. Reuse existing fields/sections to state
owner, scope, source, observed_at, validity, invalidation, review and sensitivity.
Promotion requires source verification; deletion/correction invalidates derived
summaries. Refresh living knowledge when its named source changes; do not rewrite
a dated historical result as a current success.

The receiver validates repository/worktree, HEAD and relevant file digests,
current approval scope, exclusive write ownership, partial results and remaining
retry/budget boundaries before mutation. A stale or revoked handoff stops writes
and returns to the current Task. This is a resumption check, not a new permanent
SHA-pinning completion gate. No provider session database is shared.

Before Task-initiated paid or metered provider calls during approved execution,
the Task states API/subscription context,
request/token/time/concurrency/retry bounds, observation source and available
hard enforcement. Missing account limits remain unknown, not invented universal
RPM/TPM. Refuse unapproved model fallback or spending. Where a provider supplies
retry guidance, use bounded backoff/jitter and maximum elapsed time. Model-free
fixtures cover exhausted budgets, shared-budget contention and bounded failure;
they do not establish that a native provider enforces a monetary cap. If no
supported enforcement route exists, keep that acceptance BLOCKED rather than
adding an imaginary configuration key or a new unrequested inference gateway.

GitHub Issues remain intake/coordination and branch linkage; Task owns approvals
and execution evidence. Projects is the preferred future coordination option;
Linear is an alternative with additional integration ownership. Neither is an
adopted authority or a synchronization job without separate approval. A stale
issue closure is not a Task lifecycle transition. No speculative editor command
ID or keybinding is introduced; actual editor/version/action evidence is required.

## Technical Approach

### File dispositions and consumer transition

Role paths are `.agents/roles/<id>.md`; each maps to the existing Claude Markdown
and Codex TOML role paths. Modify only iac-reviewer, hook-developer,
incident-responder and workflow-supervisor responsibilities described above.
Retain infra-implementer, security-auditor, qa-engineer, drift-detector,
ci-cd-engineer, doc-writer, rules-engineer, skill-creator, eval-engineer and
code-reviewer, including their independent review and approval boundaries.

Skill paths are `.agents/skills/<id>/SKILL.md`. Every row retains its stable ID
and current owner; the new skill is the only addition.

| Skill | Disposition | Consumer/outcome preserved |
| --- | --- | --- |
| adr-writing | retain | doc-writer; durable decision writing |
| change-review-execution | retain | code-reviewer; review execution/verdict |
| ci-cd-patterns | retain | ci-cd-engineer; CI implementation patterns |
| code-review-dimensions | retain | code-reviewer; severity and review axes |
| compose-stack-agent | retain | infra-implementer; approved Compose changes |
| container-threat-modeling | retain | security-auditor; system threat model |
| deployment-pipeline-design | retain | ci-cd-engineer; release/promotion design |
| docker-compose-patterns | retain | infra-implementer; topology selection |
| e2e-testing | retain | qa-engineer; public-interface acceptance |
| execution-plan-agent | retain | workflow-supervisor; approved Spec to Plan |
| incident-response | route recovery review | incident-responder; approved incident response |
| infra-cross-validate | route recovery review | iac-reviewer; general IaC cross-check |
| infra-validate | modify helper and contract | infra-implementer; scoped validation |
| knowledge-map-agent | retain | doc-writer; current ownership routing |
| ops-runbook-agent | route recovery review | doc-writer; operator procedure writing |
| policy-gate-agent | retain bundle | rules-engineer; gate verdict |
| provider-model-evaluation | retain bundle | eval-engineer; model disposition |
| requirements-to-design-agent | retain | rules-engineer; requirement mapping |
| security-audit | retain bundle | security-auditor; change-scope audit |
| style-validation | modify helper and contract | qa-engineer; file classification |
| task-breakdown-agent | retain | workflow-supervisor; reversible units |
| test-authoring | retain | qa-engineer; RED/GREEN regression |
| workspace-audit-revalidation | retain | eval-engineer; dated evidence revalidation |
| stateful-recovery-contract-review | add | iac-reviewer and named routing consumers |

Retain the five workflow files under `.github/workflows/`: ci-quality,
pr-labeler, greetings, stale and generate-changelog. Keep the first as the
required quality flow and the others as their current non-gating consumers.
The workflow contract owns new regression membership, arguments, cwd and timeout;
the CI YAML does not receive duplicated child command lists.

| Command/surface | Disposition and transition |
| --- | --- |
| infra-validate/scripts/static-checks.sh | modify; retain canonical skill caller; add focused fixture test to an existing leaf |
| style-validation/scripts/classify-changed-files.sh | modify; preserve categories; add cwd/error regressions |
| scripts/validation/validate-docker-compose.sh | retain public interface; remove unsafe real-checkout use from static helper |
| scripts/validation/run-ci-gate.py and ci_gate_runner.py | retain public dispatcher; existing contract selects regression leaves |
| scripts/operations/provider_surface_renderer.py | retain source-first renderer; consume registered new skill/role links |
| check-agent-governance-contract.py and its library | extend resource validation without duplicate wrapper |
| check-document-links.py and links.py | align deterministic R23 checks; semantic review remains independent |
| provider hook dispatcher/payload/post-tool validators | preserve existing routing; narrow scratch grants and report missing lint |
| run-agent-precommit-all-files.sh / run-ci-precommit.sh | retain approved local-final-QA / hosted-only boundaries |
| .pre-commit-config.yaml and commit-msg configuration | retain staged-file and message behavior; no installation implied |
| other manifest operations/validation commands | retain unless a caller-proven shared root cause requires a scoped Plan amendment |

No deletion target is manufactured from file counts. Any newly discovered
merge/removal needs replacement consumer, preserved unique behavior, negative
regression and recovery evidence in the Plan before it is performed.

### Evaluation location and evidence

Keep the four-file root evals subsystem: README.md, agent_output_eval.py,
fixture-catalog.md and run-agent-output-eval-fixtures.sh. It already has manifest,
CI, tests, ownership and knowledge consumers. Moving all four to .agents would
change the closed root/registry/manifest/path contracts without correcting a
behavioral defect; splitting data and runner would introduce cross-root coupling.
Neither alternative is selected. Remove the retired LLM Wiki freshness criterion
from current evaluation, correct the generic runner's authority/maintenance owner,
and add AOE-RECOVERY-001 cases in the existing harness.

Pin rubric versions before scoring. Preserve normal/error/boundary cases and
compare equivalent cases before/after changes. Stored/model-free outputs cannot
prove native skill invocation, cost savings, model access or a restored service.
Test prompt injection in evaluation data without treating data as instructions.

### Implementation and recovery constraints

The later Plan binds exact paths, safe tests, dependencies, logical commits,
reviewers and rollback per acceptance criterion. Behavior changes start with a
failing fixture, then the minimal implementation and affected gates. Policy,
validator and regression changes for one invariant stay together. Registered
projections are regenerated and verified twice; authored bytes are preserved.
Revert logical source commits to recover configuration, then regenerate their
outputs. This does not authorize operational recovery. Stop for conflicting file
ownership, unexpected secret/runtime contact or an unexecutable approved plan.

## Interfaces and Data

The CLI state/exit contract above is the externally observable helper interface.
Existing public changed/full/--explain entrypoints remain unchanged. New recovery
review takes sanitized contract facts and emits a bounded verdict with evidence,
missing inputs, responsible owners and separate static/native/operational status;
it accepts no credential payload or implicit execution instruction.

Keep native invocation metadata provider-specific. The new skill uses existing
stable function/owner/scope metadata and Codex explicit-invocation metadata;
Claude receives the registered thin projection. The provider registry uses its
existing fields to register the new skill; no new Stage 99 schema field or
template profile is proposed. No new provider model identifier,
account secret, session database or universal cost constant enters source.

Requirement and test IDs below are local traceability labels. The current Task,
once separately authorized, owns commands, exits, exact file/consumer changes,
review dispositions, approval evidence and commits. A temporary inventory or
this specification never becomes a second execution ledger.

## Failure Modes and Guardrails

| Failure | Required behavior |
| --- | --- |
| Required tool/plugin absent, Git failure or timeout | explicit incomplete/failed state and nonzero aggregate; never false N/A |
| Wrong cwd or path containing spaces | same authorized targets and outcomes |
| Static validator needs real environment/host writes | isolate synthetic inputs or BLOCKED; never inspect real values |
| Resource symlink, FIFO, orphan or race | bounded no-follow rejection without target read or execution |
| Diagnostic contains a synthetic secret sentinel | test fails; keep only sanitized bounded metadata |
| Unsupported model/control or budget exhaustion | stop, preserve needs_revalidation and actual limits; no silent fallback |
| Stale handoff, changed digest, revoked approval or two writers | stop mutation, reconcile current Task/ownership |
| Stage path is an output example or historical provenance | classify its use; do not delete indiscriminately |
| Individual stage artifact supplies current runtime authority | move only the needed current rule to its owner and remove dependency |
| Native/editor/hosted/operational evidence unavailable | record BLOCKED/NOT_RUN, never PASS or unjustified N/A |
| New role/command name bypasses inherited restriction | reject unknown membership and require consumer-complete transition |
| Concurrent unrelated work changes | preserve it; use this isolated worktree and exact owned paths |

## Acceptance Contract

Numbers map one-to-one to R01–R39. Test labels name the supplied scenario family;
the observable conditions here are self-contained. A future Task cannot close
an applicable criterion with BLOCKED, NOT_RUN, SKIPPED or static evidence offered
as native/operational evidence. Conditional non-applicability requires a reviewed
reason, not merely an unavailable tool or missing approval.

1. **R01** — The role responsibility matrix covers Compose, networking/gateway, persistent data, access/secret references, observability/backup/recovery, QA/CI, docs and governance, with implementer, independent reviewer and human approval boundaries. (T10,T28).
2. **R02** — All 23 existing skills and the new candidate have a file-level disposition, actual consumer and focused acceptance; no omitted body is counted as reviewed merely from inventory. (T03,T04,T29).
3. **R03** — Current governance owns authority, exceptions and failure handling for the approved scope without conflicting skill/provider policy copies. (T21).
4. **R04** — Hook payload, event, timeout, duplicate/re-entry, malformed input and failure behavior have regressions; missing lint is visible and actual delivery remains separately evidenced. (T12,T13).
5. **R05** — Each native role resolves its canonical role, skills, model/tool/permission mapping and handoff; unknown membership and permission expansion fail, with discovery/configuration distinguished from invocation. (T10,T11,T13,T30).
6. **R06** — Knowledge facts have a current owner, source, observation and invalidation/refresh contract; selected domain loading and source changes are verified. (T25).
7. **R07** — Reusable prompts specify required inputs, outputs, forbidden actions and missing/partial-input behavior; consumers validate the envelope without granting authority. (T26).
8. **R08** — Design, written-spec and written-plan approvals are distinct; failure, bounded retry, stop, resume and completion transitions preserve the approval actually given. (T21,T31).
9. **R09** — Real CLI/skill/Git/CI entrypoints have known arguments, side effects, cwd, timeout and exit semantics; required absence and failed pipelines cannot report success. (T05,T06,T32).
10. **R10** — Common and provider output styles preserve evidence, failures, non-execution and approval boundaries; unsupported native style features are not invented. (T27).
11. **R11** — Every accepted conflict, contradiction, duplication, drift or orphan finding has one disposition, owner and verified consumer transition; harmless historical references are preserved. (T03,T21,T33).
12. **R12** — Needed bundle resources are reachable and scoped; nested unsafe entries and unsupported input fail without implicit execution. Trigger, exception and functional cases are covered. (T01,T02,T04).
13. **R13** — Task-profile model selection separates documented support, entitlement and runtime observation; unsupported values/fallbacks fail and static parsing cannot clear needs_revalidation. (T11,T13,T18).
14. **R14** — Existing knowledge, Task and handoff implement durable/domain/short-term memory, verified promotion, expiry/correction/deletion and derived-summary invalidation without secrets or a second progress store. (T14,T15,T25).
15. **R15** — Both providers consume one canonical source, with provider-specific invocation and native syntax tested separately; generation preserves source and produces zero second-run drift. Maintenance, deployment-skeleton and derived modes include only their needed assets and do not inherit upstream personal state or approval as new-product facts. (T11,T13,T23).
16. **R16** — Root/project/path/provider instruction loading, language and safety precedence are explicit; Markdown links are not silently imported, global state is preserved and native claims cite actual version evidence. (T13,T27).
17. **R17** — Git pre-commit/pre-push/commit-msg ownership and partial staging remain safe, message generation does not imply paid calls, and configured hooks are distinguished from installed/executed hooks. (T16,T32).
18. **R18** — Editor version/action/selection/keybinding observations are separated from CLI evidence; user bindings remain unchanged and absent native observations remain incomplete. (T17).
19. **R19** — API/subscription and observed/estimated usage are separated, approved budgets/retry/time/concurrency bounds are explicit, deterministic exhaustion/429/contention tests pass, and real hard enforcement is evidenced or remains blocked. (T18).
20. **R20** — Existing CI trust/permission/pin/required-check boundaries remain; untrusted PR code or artifacts do not enter a privileged execution path; local fixtures and hosted acceptance remain distinct. (T12,T19,T23,T24).
21. **R21** — Issue/branch/commit/PR coordination links to the current Task without duplicating execution authority; Projects versus Linear choice and external-mutation approval are recorded. (T19).
22. **R22** — Cross-provider handoff refuses stale HEAD/file digest, revoked approval, wrong worktree, overlapping writers and partial-result ambiguity before writes, then resumes from actual Task/commit evidence. (T14,T15,T26).
23. **R23** — Outside-docs individual-stage links and current-authority dependence are removed across the named surfaces; README navigation, narrowly justified machine inputs, docs-internal traceability and legitimate examples remain; normalized negative cases and independent semantic review pass. (T07,T08,T09).
24. **R24** — The selected skills apply primary-source progressive disclosure and direct/paraphrased/non-target, functional and baseline tests; example upstream thresholds are not copied as universal criteria. (T04).
25. **R25** — Legitimate scripts/references/assets pass while path escape, nonregular nodes, orphan content and unintended executable resources are rejected by regression-tested contracts. (T01,T02).
26. **R26** — Skill-only resources remain in their skill with one implementation; generic runtime/library ownership follows actual domain reuse, not a CI wrapper alone. (T03,T29).
27. **R27** — The nonduplicative recovery review skill is authored, registered, routed and tested, alongside the existing helper improvements; a name/folder or recommendation alone does not satisfy this criterion. (T22,T29).
28. **R28** — Normal infrastructure work and recovery/security/validation/provider exceptions have actual responsible roles and preserved independent approval/review. (T10,T28).
29. **R29** — The pinned external agent sources and license have selected adopted/excluded elements; no upstream persona/install script grants tools, remote actions or implicit deployment rights. (T10,T22,T30).
30. **R30** — Governance covers the real workspace domains and their operating boundaries, without turning static work into service or credential access. (T21,T24).
31. **R31** — Common/native contracts remain in their proper owners; registry, schemas, templates and generated consumers agree, and no empty symmetry directories or parallel authorities are introduced. (T07,T11,T13,T23).
32. **R32** — The retain/move/split evaluation decision is tied to actual files and consumers; retained root evaluations lose obsolete criteria, gain recovery coverage and preserve equivalent negative-case detection. (T20).
33. **R33** — Current stale path/version/role/evaluation claims are corrected from their source while dated history is preserved and local versions are not substituted for CI/runtime policy. (T25,T33).
34. **R34** — Documentation, implementation and actual validation agree for changed invariants, including incomplete tool aggregation and cwd behavior; pre-existing/environment failures remain explicit. (T05,T06,T33).
35. **R35** — Each role has an evidenced final disposition, actual responsibility/permission/consumer change or justified retention; four proposed responsibility updates are tested without losing independent review. (T28).
36. **R36** — Each skill has a final disposition; the two helper changes, recovery skill, dedicated resources, catalogs, invocation metadata and evaluations are actually connected and verified. (T29).
37. **R37** — Each retained native agent projection has a final disposition and validated role/model/tool/delegation mapping; renamed/removed/unknown IDs cannot bypass restrictions, and live acceptance is not inferred. (T30).
38. **R38** — Common workflow and five Actions dispositions preserve starts, branches, approvals, failure/resume/terminal conditions and required check production; no remote settings are silently changed. (T31).
39. **R39** — Every changed command and consumer preserves help, grammar, cwd, missing-tool, timeout and exit behavior; obsolete callers are absent or governed by an explicitly approved expiring transition. (T32).

## Traceability

| Owner/evidence | Relationship |
| --- | --- |
| [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md) | Canonical authority, least privilege, deterministic validation and current-source consistency |
| [AD-0027 Agent Governance Canonical Adapter](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md) | Source/provider architecture reused; approved extensions must reconcile its current wording |
| [Stage 99](../../99.templates/README.md) | Spec shape, identity and lifecycle; this draft is not implementation approval |
| [Canonical governance](../../../.agents/README.md) | Current policy, role, skill, knowledge and prompt owners |
| [Evaluation surface](../../../evals/README.md) | Retained model-free evaluation owner and actual consumer |

External design evidence was read on 2026-09-29. The
[designated GeekNews article](https://news.hada.io/topic?id=26328) was a discovery
route to the [Anthropic skill guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).
The [Agent Skills specification](https://agentskills.io/specification),
[Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) and
[Claude skills documentation](https://code.claude.com/docs/en/skills) inform
resource disclosure and provider-specific invocation tests, not account access.

The agency-agents sources are pinned to
`68f01534ef30805ed3764f2d302ad03fe443707a`:
[DevOps Automator](https://github.com/msitarzewski/agency-agents/blob/68f01534ef30805ed3764f2d302ad03fe443707a/engineering/engineering-devops-automator.md),
[Code Reviewer](https://github.com/msitarzewski/agency-agents/blob/68f01534ef30805ed3764f2d302ad03fe443707a/engineering/engineering-code-reviewer.md),
[Multi-Agent Systems Architect](https://github.com/msitarzewski/agency-agents/blob/68f01534ef30805ed3764f2d302ad03fe443707a/engineering/engineering-multi-agent-systems-architect.md)
and [MIT license](https://github.com/msitarzewski/agency-agents/blob/68f01534ef30805ed3764f2d302ad03fe443707a/LICENSE).
Select observability/recovery review, evidence-based findings and bounded trust/
failure handling. Exclude automatic deployment/secret rotation and unsupported
performance promises. Preserve required notices if later code/text is copied or
substantially adapted. No catalog installation or blanket vendor copy is selected.

## Open Questions

Written-spec review and human approval are complete. Account entitlement/limits,
native discovery/hook trust, installed editor actions and hosted/operational
observations remain unverified. The Plan must state the required separate
observation approval and execution environment for each, not close them as N/A.
A required control that lacks a real enforcement surface remains blocked until
its bounded implementation route or a changed requirement is explicitly approved.

## Operational Impact

This authoring change has no runtime effect. The proposed implementation narrows
automatic native grants and may therefore surface approval prompts that broad
grants previously suppressed; native behavior must be tested, not inferred.
Validation becomes explicit about incomplete evidence and never restores or
starts services to repair a failed check. Preserve the local work branch and
worktree at completion. Publication, integration and operational actions require
separate approval.
