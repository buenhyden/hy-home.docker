---
title: "Approval Boundaries"
version: "2.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Approval Boundaries

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Approval is bound to a named surface, operation, evidence route, and recovery.
It never expands through delegation or provider handoff.

###### Authority
<!-- core-payload-level:4 -->

This policy is the canonical owner of approval of protected operations and surfaces under [bootstrap precedence](../../../.agents/governance/bootstrap.md#authority-and-precedence).

##### Applies To

Actors, owned surfaces, protected operations, and their current trusted authorization sources.

###### Exclusions
<!-- core-payload-level:4 -->

None: this document states no exclusion.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| APPROVAL-BOUNDARIES-R1 | Always | Required: treat an authorization from the current trusted user, operator or native provider channel as valid only for its stated actor, operation, subject, revision or scope, and recovery boundary | none | none |
| APPROVAL-BOUNDARIES-R2 | Authorization record in a Task, schema, CLI argument or hook | Forbidden: treating it as an authenticator or as authorizing itself | none | none |
| APPROVAL-BOUNDARIES-R3 | Missing, mismatched, expired, revoked or Historical approval | Forbidden: granting a current operation from it | none | none |
| APPROVAL-BOUNDARIES-R4 | Hooks and provider fields | Forbidden: lowering a native sandbox or creating authorization through them | none | none |
| APPROVAL-BOUNDARIES-R5 | Protected operation | Required: the controller resolves the latest actual user message or native permission origin, confirms actor, operation, target/path, revision or scope, recovery and withdrawal, then compares the result with the Task's structural record | none | none |
| APPROVAL-BOUNDARIES-R6 | Trusted origin absent or insufficient | Required: mark only the dependent operation `BLOCKED` | none | none |
| APPROVAL-BOUNDARIES-R7 | Trusted origin absent or insufficient | Required: continue independent safe work | none | none |
| APPROVAL-BOUNDARIES-R8 | Unsupported protected operation | Allowed: an operator performs it directly through its trusted channel | none | none |
| APPROVAL-BOUNDARIES-R9 | Approved local authoring | Allowed: edit documentation, redacted examples, synthetic inputs and metadata without executing the depicted commands | none | none |
| APPROVAL-BOUNDARIES-R10 | Reading a secret value | Required: apply its own approval rule | none | none |
| APPROVAL-BOUNDARIES-R11 | Sensitive target, live mutation, remote write outside the request's branch and pull request, credential operation or destructive recovery | Required: wait for its exact target under this policy | none | none |
| APPROVAL-BOUNDARIES-R12 | Secret-specific execution evidence and redaction boundary | Required: take them from `environment-constraints.md#22-approved-secrets-work-protocol` | none | none |
| APPROVAL-BOUNDARIES-R13 | Always | Forbidden: printing, recording, summarizing, quoting or committing secret values, credentials, private keys, tokens, raw auth/log payloads or shell history | none | none |
| APPROVAL-BOUNDARIES-R14 | Sanitized operational evidence | Allowed: recording value-free identifiers, paths, counts, status and command outcome | none | none |
| APPROVAL-BOUNDARIES-R15 | Reading or processing a secret value | Required: separate explicit approval for a concrete target, operation, redaction boundary, validation and recovery | manual | none |
| APPROVAL-BOUNDARIES-R16 | Auth files, raw logs or shell history | Forbidden: reading them without the same concrete authorization | none | none |
| APPROVAL-BOUNDARIES-R17 | Auth files, raw logs or shell history | Forbidden: treating their presence in a document, fixture or task as that authorization | none | none |
| APPROVAL-BOUNDARIES-R18 | Current explicit request | Allowed: the work it names through its purpose, target, impact and recovery, including source, tests, documents, governance and enforcer changes, logical commits, the branch push, its pull request and the requested merge after required checks pass | none | none |
| APPROVAL-BOUNDARIES-R19 | Approval already given inside the request scope | Forbidden: asking again for that approval | none | none |
| APPROVAL-BOUNDARIES-R20 | Operation whose exact target the request does not name (runtime restart, rollout or deployment, remote mutation outside the request's branch and pull request, credential issue/rotation/revocation, data or volume deletion, public endpoint, anything billed) | Required: wait for that target, not for a second approval | none | none |
| APPROVAL-BOUNDARIES-R21 | The user names the target | Required: run the operation | none | none |
| APPROVAL-BOUNDARIES-R22 | Meaning shared by the four workspace repositories | Required: treat the owner `@buenhyden` as its one joint decision maker | none | none |
| APPROVAL-BOUNDARIES-R23 | Shared contract | Required: activate it only by the owner's explicit approval naming the contract, its revision and the repositories it applies to | manual | none |
| APPROVAL-BOUNDARIES-R24 | Shared contract adoption | Required: each repository records its own adoption in its own Task | none | adoption record in that repository's Task |
| APPROVAL-BOUNDARIES-R25 | Adoption by another repository | Forbidden: deciding or recording it | none | none |
| APPROVAL-BOUNDARIES-R26 | Shared contract revision | Required: treat it as draft until approval, approved after it, and adopted only once this repository's producers and consumers implement it on `main` and are verified | none | none |
| APPROVAL-BOUNDARIES-R27 | Partial adoption | Required: call it partial | none | none |
| APPROVAL-BOUNDARIES-R28 | Adoption record | Required: name contract id and version, single authoring owner, approver and date, scope, exceptions, effective date, migration, rollback and the revision each consumer reads | none | adoption record |
| APPROVAL-BOUNDARIES-R29 | Role permissions | Required: take them from canonical role frontmatter | none | none |
| APPROVAL-BOUNDARIES-R30 | Provider/model and permission translations | Required: take them from `.agents/governance/providers/registry.yaml` | none | none |
| APPROVAL-BOUNDARIES-R31 | Lifecycle, retry and stop behavior | Required: take it from `workflows.md` | none | none |
| APPROVAL-BOUNDARIES-R32 | Always | Forbidden: provider facts overriding agent governance policy | none | none |
| APPROVAL-BOUNDARIES-R33 | Untracked or ignored scratch state | Forbidden: treating it as evidence | none | none |
| APPROVAL-BOUNDARIES-R34 | Always | Required: preserve other workers' dirty state | none | none |
| APPROVAL-BOUNDARIES-R35 | Ownership cannot be proven | Required: stop | none | none |
| APPROVAL-BOUNDARIES-R36 | Configured hook or provider surface | Forbidden: treating it as proof of adoption; it proves tracked configuration only | none | none |
| APPROVAL-BOUNDARIES-R37 | Cost, token and time limits | Forbidden: treating them as safety authorization | none | none |
| APPROVAL-BOUNDARIES-R38 | Cost, token and time limit preflight | Required: follow `agentic.md`, its owner | none | none |
| APPROVAL-BOUNDARIES-R39 | Explicit policy-maintenance request | Allowed: matching reversible policy text edits within the writer's permission profile | none | none |
| APPROVAL-BOUNDARIES-R40 | Explicit policy-maintenance request | Forbidden: treating it as authorizing a protected operation the edited policy describes | none | none |
| APPROVAL-BOUNDARIES-R41 | Scratch deletion | Forbidden: inferring deletion safety from parent ignore probes | none | none |
| APPROVAL-BOUNDARIES-R42 | Scratch ownership | Required: bind it to the controller that created the path | none | none |
| APPROVAL-BOUNDARIES-R43 | Scratch handling | Required: separate inspection from deletion | none | none |
| APPROVAL-BOUNDARIES-R44 | Deleting ignored or untracked scratch | Required: delete only after review of its exact owner, path and disposition | manual | none |
| APPROVAL-BOUNDARIES-R45 | Scratch ownership cannot be proven | Required: stop | none | none |
| APPROVAL-BOUNDARIES-R46 | Reviewer worktrees | Required: isolate them from implementation worktrees | none | none |
| APPROVAL-BOUNDARIES-R47 | Always | Required: preserve every task-owned or user-owned dirty path | none | none |
| APPROVAL-BOUNDARIES-R48 | Digest mismatch | Required: stop | none | none |
| APPROVAL-BOUNDARIES-R49 | Staged paths | Required: reconcile them against the approved ledger | none | none |
| APPROVAL-BOUNDARIES-R50 | Unstaged review-fix round | Forbidden: mutating the index | none | none |
| APPROVAL-BOUNDARIES-R51 | After a concurrency incident | Required: rerun all affected gates before reporting completion | none | none |
| APPROVAL-BOUNDARIES-R52 | Approved documentation | Allowed: `doc-writer` edits it | none | none |
| APPROVAL-BOUNDARIES-R53 | Roles other than `doc-writer` | Forbidden: editing documentation unless their Task explicitly includes a documentation update | none | none |
| APPROVAL-BOUNDARIES-R54 | Role whose canonical `permission_profile` is `read-only` | Required: remain read-only even when routing or reviewing writable work | none | none |
| APPROVAL-BOUNDARIES-R55 | Policy change | Required: `rules-engineer` review | manual | none |

###### Authorization Source and Records
<!-- core-payload-level:4 -->

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
[Environment constraints](../../../.agents/governance/environment-constraints.md#22-approved-secrets-work-protocol).

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
  retry, and stop behavior comes from [workflows.md](../../../.agents/governance/workflows.md). Provider
  facts cannot override agent governance policy.
- Untracked or ignored scratch state is not evidence. Preserve other workers'
  dirty state and stop if ownership cannot be proven.
- A configured hook or provider surface proves tracked configuration only, not
  adoption.
- Cost, token, and time limits are execution guardrails, not safety
  authorization; their preflight owner is [Agentic policy](../../../.agents/governance/agentic.md).
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

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

A current trusted user or native provider authorization permits only its stated operation and scope. The Authorization Source and Records rules above determine that boundary.

###### Approval and Review
<!-- core-payload-level:4 -->

Policy changes require rules-engineer review (Documentation Write Permission); a shared contract needs the owner approval in Core Rules.

#### Enforcement

##### Mechanisms

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

##### Limits

No rule here names an automated check; the rules that require an approval or a review rest on that approval or review.

- Authorization source and records (R1-R12): no check is named.
- Secrets, request scope and exact-target waits (R13-R14, R16-R21): no check is named.
- Shared contracts (R22, R24-R28): no check is named.
- Sources, evidence and cost boundaries (R29-R40): no check is named.
- Shared-worktree safeguards (R41-R43, R45-R51): no check is named.
- Documentation write permission (R52-R54): no check is named.
- Secrets, request scope and exact-target waits (R15): rests on the separate explicit approval the rule requires.
- Shared contracts (R23): rests on the owner's explicit approval.
- Shared-worktree safeguards (R44): rests on the review of owner, path and disposition the rule requires.
- Documentation write permission (R55): rests on `rules-engineer` review.
- Enforcement gap: repository tools do not automatically verify the account identity behind a user message or native permission origin, and the repository does not claim to authenticate an operator's direct act or to relax the native sandbox.
- Rules stated under Enforcement (Mechanisms) are outside this table.

#### Ownership

##### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

##### Review Triggers

Changes land in place with Task evidence; related documents:

- [GitHub governance](../03.process/github-governance.md)
- [Environment constraints](../../../.agents/governance/environment-constraints.md)
- [Agentic policy](../../../.agents/governance/agentic.md)
- [Provider registry](../../../.agents/governance/providers/registry.yaml)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
