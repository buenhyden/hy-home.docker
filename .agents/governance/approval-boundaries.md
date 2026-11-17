---
title: "Approval Boundaries"
version: "1.6.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Approval Boundaries

## Purpose and Scope

### Objective

Approval is bound to a named surface, operation, evidence route, and recovery.
It never expands through delegation or provider handoff.

#### Authority

This policy is the canonical owner of approval of protected operations and surfaces under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Actors, owned surfaces, protected operations, and their current trusted authorization sources.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| APPROVAL-BOUNDARIES-R1 | Always | Required: treat an authorization as valid only for its stated actor/operation/subject/revision or scope/recovery from the current trusted channel | none | none |
| APPROVAL-BOUNDARIES-R2 | Always | Forbidden: treating a Task/schema/CLI/hook authorization record as an authenticator or as self-authorizing | none | Task authorization record (structural evidence only) |
| APPROVAL-BOUNDARIES-R3 | Always | Forbidden: granting a current operation from missing/mismatched/expired/revoked/Historical approval | none | none |
| APPROVAL-BOUNDARIES-R4 | Always | Forbidden: using hooks or provider fields to lower a native sandbox or create authorization | none | none |
| APPROVAL-BOUNDARIES-R5 | A protected operation | Required: controller resolves the latest user message or native permission origin, confirms actor/operation/target/scope/recovery/withdrawal, then compares with the Task record | none | none |
| APPROVAL-BOUNDARIES-R6 | Trusted origin absent or insufficient | Required: mark only the dependent operation `BLOCKED` and continue independent safe work | none | none |
| APPROVAL-BOUNDARIES-R7 | An unsupported protected operation | Allowed: operator performs it directly through its trusted channel | none | none |
| APPROVAL-BOUNDARIES-R8 | Approved local authoring | Allowed: edit documentation/redacted examples/synthetic inputs/metadata without executing the depicted commands | none | none |
| APPROVAL-BOUNDARIES-R9 | Reading a secret value | Required: reading keeps its own approval rule | none | none |
| APPROVAL-BOUNDARIES-R10 | Sensitive target/live mutation/remote write outside branch and PR/credential operation/destructive recovery | Required: wait for the exact target under this policy | none | none |
| APPROVAL-BOUNDARIES-R11 | Always | Forbidden: printing/recording/summarizing/quoting/committing secret values/credentials/private keys/tokens/raw auth or log payloads/shell history | none | none |
| APPROVAL-BOUNDARIES-R12 | Always | Allowed: sanitized operational evidence of value-free identifiers/paths/counts/status/command outcome | none | none |
| APPROVAL-BOUNDARIES-R13 | Reading or processing a secret value | Required: separate explicit approval for a concrete target/operation/redaction boundary/validation/recovery | none | none |
| APPROVAL-BOUNDARIES-R14 | Auth files/raw logs/shell history | Forbidden: reading them without concrete authorization (their presence in a document/fixture/task is not one) | none | none |
| APPROVAL-BOUNDARIES-R15 | A current explicit request | Allowed: the request authorizes the work it names through purpose/target/impact/recovery (source/tests/docs/governance/enforcer changes/commits/branch push/PR/requested merge after checks pass) | none | none |
| APPROVAL-BOUNDARIES-R16 | Approval already given inside the request scope | Forbidden: asking again for that approval | none | none |
| APPROVAL-BOUNDARIES-R17 | Operation whose exact target the request does not name (restart/rollout/deployment/outside-PR remote mutation/credential change/data or volume deletion/public endpoint/billed) | Required: wait for that target | none | none |
| APPROVAL-BOUNDARIES-R18 | The user names the target | Required: run the operation | none | none |
| APPROVAL-BOUNDARIES-R19 | A meaning shared by the four workspace repositories | Required: owner `@buenhyden` is the one decision maker; a shared contract becomes active only by explicit owner approval naming contract/revision/repositories | manual | none |
| APPROVAL-BOUNDARIES-R20 | Adoption of a shared contract | Required: each repository records its own adoption in its own Task | none | Adoption record in the repository Task |
| APPROVAL-BOUNDARIES-R21 | Adoption of a shared contract | Forbidden: deciding or recording adoption for another repository | none | none |
| APPROVAL-BOUNDARIES-R22 | Shared contract revision | Required: treat as draft until approval/approved after it/adopted only once producers and consumers implement it on `main` and are verified; call partial adoption partial | none | none |
| APPROVAL-BOUNDARIES-R23 | Recording adoption | Required: adoption record names contract id/version/single authoring owner/approver/date/scope/exceptions/effective date/migration/rollback/consumer revision | none | Adoption record |
| APPROVAL-BOUNDARIES-R24 | Always | Required: take role permissions from canonical role frontmatter, provider/model/permission translations from `.agents/governance/providers/registry.yaml`, lifecycle/retry/stop from `workflows.md` | none | none |
| APPROVAL-BOUNDARIES-R25 | Always | Forbidden: letting provider facts override agent governance policy | none | none |
| APPROVAL-BOUNDARIES-R26 | Always | Forbidden: treating untracked or ignored scratch state as evidence | none | none |
| APPROVAL-BOUNDARIES-R27 | Always | Required: preserve other workers' dirty state and stop if ownership cannot be proven | none | none |
| APPROVAL-BOUNDARIES-R28 | Always | Forbidden: treating a configured hook or provider surface as proof of adoption | none | none |
| APPROVAL-BOUNDARIES-R29 | Always | Forbidden: treating cost/token/time limits as safety authorization | none | none |
| APPROVAL-BOUNDARIES-R30 | An explicit policy-maintenance request | Allowed: matching reversible policy text edits within the writer's permission profile | none | none |
| APPROVAL-BOUNDARIES-R31 | An explicit policy-maintenance request | Forbidden: treating it as authorizing a protected operation the edited policy describes | none | none |
| APPROVAL-BOUNDARIES-R32 | Deletion of scratch or ignored paths | Forbidden: inferring deletion safety from parent ignore probes | none | none |
| APPROVAL-BOUNDARIES-R33 | Scratch ownership | Required: bind ownership to the controller that created the path and separate inspection from deletion | none | none |
| APPROVAL-BOUNDARIES-R34 | Deleting ignored or untracked scratch | Required: delete only after review of exact owner/path/disposition and stop when ownership cannot be proven | manual | none |
| APPROVAL-BOUNDARIES-R35 | Reviewer and implementation worktrees | Required: isolate reviewer worktrees from implementation worktrees and preserve every task-owned or user-owned dirty path | none | none |
| APPROVAL-BOUNDARIES-R36 | Digest mismatch or staged paths | Required: stop on digest mismatch and reconcile staged paths against the approved ledger | none | none |
| APPROVAL-BOUNDARIES-R37 | Unstaged review-fix round | Forbidden: mutating the index | none | none |
| APPROVAL-BOUNDARIES-R38 | After a concurrency incident | Required: rerun all affected gates before reporting completion | none | none |
| APPROVAL-BOUNDARIES-R39 | Approved documentation | Allowed: `doc-writer` edits approved documentation | none | none |
| APPROVAL-BOUNDARIES-R40 | Role other than `doc-writer` | Forbidden: editing documentation unless the Task explicitly includes a documentation update | none | none |
| APPROVAL-BOUNDARIES-R41 | Role with canonical `permission_profile` `read-only` | Required: stay read-only even when routing or reviewing writable work | none | none |
| APPROVAL-BOUNDARIES-R42 | A policy change | Required: `rules-engineer` review | manual | none |

#### Authorization Source and Records

The current trusted user, operator, or native provider channel supplies an
authorization only for its stated actor, operation, subject, revision or scope,
and recovery boundary. An authorization record in a Task, schema, CLI argument,
or hook is structural evidence of what was recorded; it is
not an authenticator and cannot authorize itself. Missing, mismatched, expired,
revoked, or Historical approval never grants a current operation. Hooks and
provider fields cannot lower a native sandbox or create authorization.

For a protected operation, the controller resolves the latest actual user
message or native permission origin available to it, confirms the authorized
actor, exact operation, target/path, revision or scope, recovery, and whether it
was withdrawn, then compares that result with the Task's structural record.
Repository tools do not automatically verify the account identity behind that
origin. If the trusted origin is absent or insufficient, mark only the dependent
operation `BLOCKED` and continue independent safe work. An operator may perform
an unsupported protected operation directly through its trusted channel; this
repository does not claim to authenticate that act or to relax the native
sandbox.

Approved local authoring may edit documentation, redacted examples, synthetic
inputs, and metadata without executing the commands depicted. Reading a secret
value keeps its own approval rule. Acting on a sensitive target, a live
mutation, a remote write outside the request's branch and pull request, a
credential operation, or destructive recovery waits for its exact target under
this policy. The secret-specific execution evidence and
redaction boundary are defined by
[Environment constraints](environment-constraints.md#22-approved-secrets-work-protocol).

**Core Rules**

- Never print, record, summarize, quote, or commit secret values, credentials,
  private keys, tokens, raw auth/log payloads, or shell history. Sanitized
  operational evidence may record value-free identifiers, paths, counts, status,
  and command outcome.
- Read or process a secret value only with separate explicit approval for a
  concrete target, operation, redaction boundary, validation, and recovery.
  Do not read auth files, raw logs, or shell history without the same concrete
  authorization; their presence in a document, fixture, or task is not one.
- A current explicit request authorizes the work it names through its
  purpose, target, impact, and recovery: source, tests, documents, governance
  and enforcer changes, logical commits, the branch push, its pull request,
  and the merge it asks for after the required checks pass. Do not ask again
  for approval already given inside that scope.
- An operation whose exact target the request does not name waits for that
  target, not for a second approval: runtime restart, rollout, or deployment;
  a remote mutation outside the request's branch and pull request; issuing,
  rotating, or revoking a credential; deleting data or volumes; opening a
  public endpoint; and anything billed. Once the user names the target, run it.
- A meaning shared by the four workspace repositories (`blog-data`,
  `Project-Template`, `hy-home.docker`, `hy-home.k8s`) has one joint decision
  maker: the owner `@buenhyden`, who owns all four. A shared contract becomes
  active only by that owner's explicit approval naming the contract, its
  revision, and the repositories it applies to. Each repository records its own
  adoption in its own Task; this repository never decides or records adoption
  for another. A revision is draft until that approval, approved after it, and
  adopted only once this repository's producers and consumers implement it on
  `main` and are verified; partial adoption is called partial. The adoption record names
  the contract id and version, the single authoring owner, who approved it and
  when, the scope, exceptions, the effective date, migration, rollback and the
  revision each consumer reads.
- Role permissions come from canonical role frontmatter; provider/model and
  permission translations come from `.agents/governance/providers/registry.yaml`; lifecycle,
  retry, and stop behavior comes from [workflows.md](workflows.md). Provider
  facts cannot override agent governance policy.
- Untracked or ignored scratch state is not evidence. Preserve other workers'
  dirty state and stop if ownership cannot be proven.
- A configured hook or provider surface proves tracked configuration only, not
  adoption.
- Cost, token, and time limits are execution guardrails, not safety
  authorization; their preflight owner is [Agentic policy](agentic.md).
- An explicit policy-maintenance request authorizes matching reversible policy
  text edits within the writer's permission profile. It does not authorize any
  protected operation that the edited policy describes.

**Shared-worktree Safeguards**

- Never infer deletion safety from parent ignore probes. Bind scratch ownership
  to the controller that created the path and separate inspection and deletion.
- Delete ignored or untracked scratch only after review of its exact owner,
  path, and disposition. Stop when that ownership cannot be proven.
- Isolate reviewer worktrees from implementation worktrees and preserve every
  task-owned or user-owned dirty path.
- Stop on digest mismatch, reconcile staged paths against the approved ledger,
  and do not mutate the index during an unstaged review-fix round.
- Rerun all affected gates after a concurrency incident before reporting
  completion.

**Documentation Write Permission**

- `doc-writer` may edit approved documentation.
- All other roles are read-only unless their Task explicitly includes a
  documentation update.
- A role whose canonical `permission_profile` is `read-only` remains read-only
  even when it routes or reviews writable work.
- Policy changes require `rules-engineer` review.

### Exceptions

#### Exception Conditions

A current trusted user or native provider authorization permits only its stated operation and scope. The Authorization Source and Records rules above determine that boundary.

#### Approval and Review

Policy changes require rules-engineer review (Documentation Write Permission); a shared contract needs the owner approval in Core Rules.

## Enforcement

### Mechanisms

**Protected Surfaces**

| Surface | Required evidence | Recovery |
| --- | --- | --- |
| Compose and `infra/**` | scoped Compose validation and Task approval | revert config; no implicit runtime action |
| `secrets/**` and real environment values | path-only redacted evidence | revert mapping; rotate only with approval |
| `.github/workflows/**` | workflow contract and security review | revert logical commit |
| `scripts/**` | focused tests and harness validation | revert logical commit |
| `.claude/**`, `.codex/**` | canonical contract, authored/native distinction, and renderer parity | restore authored/native controls; regenerate only registered outputs |
| `.agents/**` | canonical contract, links, and Task evidence | restore approved authored sources; never treat them as generated cleanup |
| `docs/99.templates/**` | registry/schema validation and Task evidence | revert logical commit |

### Limits

Most rules here rest on controller judgment, owner approval, and review rather than a named check:

- Authorization and records (R1-R10): no check authenticates the origin; repository tools do not verify the account identity behind a user message or native permission origin, and a Task record is structural evidence only.
- Secrets and exact-target waits (R11-R18): no automated check is named.
- Shared contracts (R19-R23): R19 rests on `@buenhyden` approval (manual); each repository records adoption by hand in its own Task (R20-R23).
- Source, evidence, and cost boundaries (R24-R31): no check is named.
- Shared-worktree safeguards (R32-R38): no script is named; R34 rests on review (manual).
- Documentation write permission (R39-R41): role read-only status follows canonical role frontmatter with no check named; R42 depends on `rules-engineer` review (manual).

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [GitHub governance](github-governance.md)
- [Environment constraints](environment-constraints.md)
- [Agentic policy](agentic.md)
- [Provider registry](providers/registry.yaml)
