---
status: active
artifact_id: spec-0135
artifact_type: spec
parent_ids:
  - spec-0133
  - spec-0134
created: 2026-07-28
updated: 2026-08-11
---
# Target Surface Delta Convergence Specification

**Date:** 2026-07-28 (Asia/Seoul)

**Status:** Active

**Design revision:** 2026-07-29 (Asia/Seoul)

## Overview

This specification defines a successor delta-convergence wave for every
tracked file below `.github/`, `archive/`, `examples/`, `infra/`, `projects/`,
`scripts/`, `secrets/`, and `tests/`. It preserves the completed Spec 133
baseline and classifies only the later delta while revalidating the entire
current target surface for omissions. It also incorporates the directly
affected Stage 00, Stage 04, Stage 90, and Stage 99 owners required to keep
documentation, contracts, validators, generated evidence, CI, and QA
internally consistent.

Spec 133 remains immutable historical evidence. Its completed manifest,
summary, reviews, and verification records are not reopened or rewritten.
This wave uses the Spec 133 closure as its comparison point and the local
`main` commit at worktree creation as its implementation baseline. A new delta
manifest records the disposition of files changed since closure; whole-surface
validators ensure that an unchanged but newly nonconforming file cannot evade
review.

The design is consumer-aware. Native GitHub, Compose, YAML, JSON, TOML, code,
test, shell, and configuration files keep their native schemas. README files
use the exact path-selected README profile and remain frontmatter-free by
default. Typed Markdown uses only metadata consumed by its registered type.
Root `archive/**` and `docs/98.archive/**` continue to use distinct content and
SDLC archive contracts. Secret-related work is limited to identifiers,
redacted inventory, reference topology, and value-free validation.

The local GitHub quality contract defines 16 required job IDs, while the
authenticated read-only remote observation on 2026-07-28 found 12 required
contexts on `main`. The remote default branch was behind the local baseline,
and recent remote CI runs failed. This wave records that drift and improves
tracked definitions, but it neither mutates remote GitHub settings nor claims
that local validation proves remote enforcement.

The CI ownership design is structural rather than interpretive. A typed gate
registry and declarative directed acyclic graph (DAG) define the only admitted
first-party CI entry points, their exact argument vectors, and their required
job roots. Workflows and local QA project from that same graph. The contract
does not attempt to infer arbitrary shell or leaf-program semantics; it proves
registered gate identity, ownership, reachability, and exact invocation.

Implementation uses six logical tasks, a fresh implementation agent and
independent reviewers for each task, logical commits, and a final whole-branch
review. Live service mutation, deployment, remote workflow dispatch, push,
merge, and branch-protection changes remain outside the approved boundary.

## Boundaries and Inputs

### Approved Scope

- Preserve Spec 133 as a completed, immutable predecessor.
- Pin the Spec 133 closure and the new local implementation baseline as
  separate provenance points.
- Classify the post-Spec-133 target delta as `preserve`, `update`, `migrate`,
  or `delete`, with exactly one disposition per path.
- Revalidate every current tracked target path against its native consumer,
  document profile, duplication, deprecation, link, and secret-safety
  contracts.
- Normalize confirmed README heading, local-purpose, inventory, routing, and
  duplicated shared-policy drift without replacing topic-specific content with
  template filler.
- Resolve typed-example ambiguity without presenting an example fixture as an
  active SDLC chain artifact.
- Preserve the split between root content archives and Stage 98 SDLC archives.
- Remove verified obsolete or deprecated active paths only after current
  consumer, replacement, provenance, rollback, and review evidence exists.
- Improve tracked GitHub workflows, trigger contracts, action dependency
  evidence, CI ownership, local QA routing, and regression coverage.
- Keep the 16 required quality job IDs stable while removing duplicate
  expensive execution beneath those job boundaries.
- Replace the mutable transitive dependency in the current pre-commit Action
  path with a repository-owned CI entry point and pinned tool version.
- Reconcile the canonical audit pack, generated evidence, and dated remote
  GitHub observation with the implementation.
- Use isolated-worktree, Subagent-Driven implementation with logical commits
  and independent review.

### Direct-Impact Exception

The primary target list authorizes changes outside those roots only when a
target mutation would otherwise leave the repository false, broken, or
unverifiable. The allowed direct-impact set is limited to:

- Stage 00 GitHub, QA, workflow, approval, and agent execution governance;
- Stage 04 Plan, Task ledger, and sanitized evidence for this wave;
- the canonical 2026-07-05 audit pack and its registered generated evidence;
- Stage 99 document metadata, README, archive, template, and lifecycle owners;
- root QA configuration that directly routes a target path;
- validators, generators, and focused tests that consume an approved target;
- current project memory needed to hand off or close this wave.

Every direct-impact path must be associated with an approved requirement and
target consumer in the Task ledger. Directory adjacency is not authorization.

### Non-goals

- Reopening, superseding, regenerating, or rewriting the completed Spec 133
  manifest and review evidence.
- Starting, stopping, recreating, probing, or mutating a live Compose service.
- Deploying, promoting, releasing, rolling back, or changing a runtime
  environment.
- Pushing a branch, opening or merging a pull request, dispatching a workflow,
  or changing remote branch protection, rulesets, required checks,
  environments, variables, secrets, or repository settings.
- Reading, rendering, printing, storing, or committing secret values,
  credentials, tokens, private keys, auth files, shell history, or raw
  secret-bearing logs.
- Treating tracked workflow files, local tests, or local desired-state
  documents as proof of remote execution or enforcement.
- Applying one frontmatter schema to all Markdown or adding Markdown
  frontmatter to native machine-readable files.
- Deleting historically correct uses of the words `legacy` or `deprecated`
  when they are research, migration, incident, archive, or negative-fixture
  evidence.
- Adding arbitrary policy prose to README files or copying template prose into
  topic documents.
- Running all-files pre-commit directly. A final all-files run requires a new
  explicit approval and the controlled clean-worktree wrapper.

### Canonical Inputs

- [Spec 133: Target Surface Contract Convergence](../spec-0133-target-surface-contract-convergence/spec.md)
- [Spec 134: Agent Governance Canonical Convergence](../spec-0134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/ref-0019-readme.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Common document contract](../../99.templates/support/common-document-contract.md)
- [SDLC document contract](../../99.templates/support/sdlc-document-contract.md)

### External Source Basis

The rolling source verification was performed on 2026-07-28 KST and the CI
execution sources were revalidated for this design revision on 2026-07-29 KST.
External sources define platform behavior and industry syntax; they do not
define this repository's path taxonomy, lifecycle states, approval authority,
archive dispositions, or evidence vocabulary.

| Official or primary source | Local design consequence |
| --- | --- |
| [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Register exact workflow events, branch and path filters, permissions, concurrency, and timeouts. Keep required quality checks off path filters because a filtered required workflow can remain pending. |
| [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Require least-privilege tokens, reject dangerous trusted-context checkout, and use full commit SHAs for immutable direct Action references. |
| [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | Keep required job names unique and distinguish tracked desired checks from authenticated remote enforcement. |
| [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) | Reuse workflow structure where it reduces duplication, but do not treat a reusable workflow as a second command-ownership authority. |
| [GitHub Action metadata syntax](https://docs.github.com/en/enterprise-cloud%40latest/actions/reference/workflows-and-actions/metadata-syntax) | Treat composite Actions as executable dependency surfaces; register admitted uses and do not use a composite Action to hide untyped shell execution. |
| [Node 20 deprecation on Actions runners](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/) | Reject Node 20 Action runtime dependencies and record Node 24 compatibility evidence. |
| [GitHub self-hosted runner minimum-version enforcement](https://github.blog/changelog/2026-06-12-github-actions-minimum-version-enforcement-timeline-for-self-hosted-runners/) | Keep runner compatibility a dated observation and do not claim self-hosted readiness without an authenticated inventory. |
| [pre-commit](https://pre-commit.com/) | Treat all-files execution as repository-wide and potentially mutating; keep Agent and CI entry points distinct and pinned. |
| [GitHub YAML frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter) | Use consumer-specific frontmatter rather than a universal metadata set. |
| [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) and [GitHub Flavored Markdown](https://github.github.com/gfm/) | Validate Markdown body structure separately from metadata parsing. |

The exact currently pinned Action manifests were also read from their official
repositories. `actions/checkout`, `actions/setup-python`,
`actions/setup-node`, `actions/first-interaction`, `actions/labeler`,
`actions/stale`, `astral-sh/setup-uv`, and
`github/codeql-action/upload-sarif` declare Node 24 at the pinned commits.
`pre-commit/action` is a composite Action whose pinned manifest invokes
`actions/cache@v4` by a mutable tag. That transitive mutable reference is the
confirmed reason to replace the Action path rather than merely update its
outer SHA.

### Baseline Evidence

| Observation | Result | Interpretation |
| --- | --- | --- |
| Local implementation baseline | `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74` | Worktree and feature branch start from this local `main` commit. |
| Spec 133 closure comparison point | `63039b5b0b20c99a10aae7162627afefcd7a1d8b` | The predecessor evidence remains immutable; later target changes form the delta. |
| Current target inventory | 474 tracked paths: `.github` 16, `archive` 1, `examples` 9, `infra` 275, `projects` 52, `scripts` 53, `secrets` 19, `tests` 49 | Whole-surface validation must cover this current set rather than the older 422-path baseline. |
| Current document inventory | 82 Markdown/MDX files, including 75 README files | README profile checks must remain path-selected and consumer-aware. |
| Post-closure target delta | 102 target paths changed | A successor delta wave is warranted; rewriting the predecessor is not. |
| Existing target checker | Pass at the new baseline | Existing blocking facts are still green but do not cover every newly confirmed drift class. |
| Existing target unit tests | 40 tests pass | New failures must be added as regression cases rather than weakening the prior suite. |
| Canonical audit distribution | 77 Implemented, 60 Partial, 13 Missing, 2 N/A, 9 Needs Revalidation; total 161 | New evidence may update only affected rows and generated totals. |
| Remote default branch | `bffc5aed...`, behind the local baseline | Remote failures cannot be attributed to or cleared by unpushed local changes. |
| Remote `main` required contexts | 12 observed, compared with 16 local desired job IDs | `docs-implementation-alignment`, `agent-output-eval-fixture-gate`, `supply-chain-fixture-policy`, and `dependency-vulnerability-audit` are not remotely required. |
| Recent remote runs | Main run `30325161033` and PR run `30325219960` failed | Job and failing-step metadata are observed; raw-log root causes remain `unverified`. |

The remote branch observation also found strict required checks, one approving
review, CODEOWNERS review, conversation resolution, disabled force-push and
deletion, no repository ruleset, and disabled admin enforcement, linear
history, stale-review dismissal, last-push approval, and required signatures.
These are dated observations only. No remote setting changes are approved by
this specification.

## Contracts

### Requirement and Acceptance Matrix

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| TSDC-001 | Preserve predecessor evidence. | Spec 133 artifacts remain byte-identical; the new wave references immutable closure provenance. |
| TSDC-002 | Classify the delta completely. | Every target path changed since closure has exactly one reviewed disposition and no current target path escapes whole-surface validation. |
| TSDC-003 | Keep native formats native. | Machine-readable, source, test, script, and workflow files receive no Markdown frontmatter and pass their native parser or static checker. |
| TSDC-004 | Normalize README files by profile. | Every target README matches one profile, uses its exact required heading envelope, contains local context, and routes shared rules to their owner. |
| TSDC-005 | Normalize typed documents by consumer. | Every typed target document has only registered ordered keys and sections; example fixtures cannot impersonate an active SDLC chain. |
| TSDC-006 | Preserve archive separation. | Root content tombstones and Stage 98 SDLC tombstones use their distinct profiles, provenance, and snapshot boundaries. |
| TSDC-007 | Protect secret boundaries. | Secret-related checks operate on tracked names, paths, and redacted metadata only; value-bearing output is neither read nor persisted. |
| TSDC-008 | Resolve confirmed duplication. | Duplicate-purpose files, sections, links, and shared-policy copies have one current owner or an explicit preserved rationale. |
| TSDC-009 | Remove active deprecated state safely. | Every active deletion or migration has consumer, replacement, provenance, rollback, test, and review evidence; historical evidence remains intact. |
| TSDC-010 | Type workflow triggers. | Every tracked workflow matches an approved event, branch, path, schedule, permission, timeout, and concurrency contract. |
| TSDC-011 | Preserve CI status identity. | The 16 required job IDs remain unique and synchronized across workflow, validator, governance, and desired-state protection documents. |
| TSDC-012 | Enforce typed CI gate ownership. | Every required semantic check has one registered `suite_key`, one required-job root owner, and at most one reachable execution in a workflow; governed `run` steps use only the exact static gate runner grammar. |
| TSDC-013 | Harden Action dependencies. | Direct Actions are full-SHA pinned, approved runtime evidence is current, Node 20 is rejected, and the mutable transitive pre-commit Action path is removed. |
| TSDC-014 | Keep Agent and CI QA distinct. | CI uses its repository-owned entry point; Agents use only the separately approved controlled wrapper for an all-files run. |
| TSDC-015 | Represent remote state honestly. | Dated remote observations, desired-state differences, and unverified causes are separate from local pass/fail evidence; no mutation occurs. |
| TSDC-016 | Reconcile audits and evidence. | Affected canonical audit rows, generated summaries, cross-links, and Stage 04 evidence match the implemented repository state. |
| TSDC-017 | Close through independent review. | Six logical tasks pass focused validation, independent specification and quality review, and a fresh whole-branch review. |

### Delta and Whole-Surface Contract

The Spec 133 manifest is an immutable predecessor. This wave creates a
separate delta contract with:

- the immutable predecessor closure;
- the new baseline commit;
- the target path;
- the native surface class and document profile where applicable;
- the predecessor relationship;
- exactly one disposition;
- canonical owner and direct consumers;
- confirmed finding or preserve rationale;
- replacement or migration destination where applicable;
- secret-safety classification;
- required validators and tests;
- provenance and rollback for destructive changes;
- specification and quality review verdicts.

The delta contract is not sufficient by itself. A whole-surface validator
recomputes the current tracked path set and verifies profile coverage,
forbidden drift patterns, duplicate ownership, action routing, and declared
exceptions. An omitted delta row is a blocking failure when the path changed
after the predecessor closure. A new current path outside the approved target
set is not silently admitted through this contract.

### Document and Frontmatter Contract

Each file follows its real consumer:

1. Native GitHub, Compose, YAML, JSON, TOML, source, test, and script files use
   native format and comments only.
2. README files match exactly one registry profile. Frontmatter is absent by
   default and is permitted only when the profile identifies a real consumer.
3. Typed Markdown uses one registered artifact type, exact key order,
   required/optional/forbidden key sets, and value domains.
4. Generated files require a registered owner, deterministic generator, and
   check mode.
5. Archive files use the path-selected archive profile.

README headings are exact contract identifiers. Localized content may appear
beneath them, but suffixes such as `Overview (KR)` do not create alternative
heading names. README files own navigation, local inventory, local setup, and
service-specific troubleshooting or secret references. Stage 00 or Stage 99
owns shared agent policy, lifecycle rules, metadata schemas, and validation
algorithms.

The confirmed document convergence set includes:

- removing the obsolete operations-guide preface and repeated links from
  `infra/04-data/README.md` while preserving its folder-index role;
- normalizing the 11 confirmed `Overview (KR)` variants;
- replacing duplicated shared `AI Agent Guidance` or `AI Agent Operation
  Policy` bodies with Stage 00 routing while retaining service-specific
  constraints;
- registering `examples/sample-web-service/service.md` explicitly as a typed
  example fixture rather than an active SDLC chain;
- synchronizing `secrets/README.md` with tracked redacted directory
  identifiers, including the SurrealDB directory, without reading values.

### Archive Contract

Root `archive/**` selects `content-archive`; `docs/98.archive/**` selects
`sdlc-archive`. Both remain semantic archives, but only the SDLC profile admits
parent relations, replacement relations, and the approved conditional
snapshot fields.

Git history is the default preservation route. A full snapshot is admitted
only for an audit, legal, or approved evidence-preserve need after
confidentiality and checksum verification. Active guidance never routes to a
tombstone as current truth. `archive/Windows-Network-IP.md` is already a valid
content tombstone and remains preserved unless new evidence proves a contract
failure.

### Legacy, Deprecated, and Destructive Change Contract

The words `legacy` and `deprecated` are not deletion selectors. A current
implementation is removed only when:

1. the active consumer graph is known;
2. a supported replacement or withdrawal rationale is recorded;
3. cross-links and validators are migrated;
4. Git provenance and rollback are recorded;
5. targeted tests fail before and pass after the change;
6. specification and quality reviewers approve the disposition.

Historical research, incidents, postmortems, migrations, archives, and
negative fixtures retain accurate historical terms. One-time generated files
are deleted only when a deterministic owner replaces them or no current
consumer remains.

### CI Job Ownership Contract

`ci-quality.yml` remains the single tracked required-quality workflow and keeps
the following 16 unique job IDs:

- `docs-traceability`;
- `docs-implementation-alignment`;
- `repo-contracts`;
- `agent-output-eval-fixture-gate`;
- `supply-chain-fixture-policy`;
- `dependency-vulnerability-audit`;
- `git-flow-contract`;
- `compose-validation`;
- `compose-all-profiles-validation`;
- `infrastructure-hardening`;
- `template-security-baseline`;
- `quickwin-baseline`;
- `pre-commit`;
- `frontend-quality`;
- `storybook-coverage`;
- `zizmor`.

`.github/workflow-contract.yml` advances to schema version 2 and remains the
single canonical machine registry. A parallel command registry is forbidden.
The schema retains workflow triggers, permissions, concurrency, job metadata,
and Action dependency facts while replacing free-form `owner_commands` and
string-based expensive-command matching with:

- `gate_nodes`, keyed by a unique stable `gate_id`;
- `job_roots`, mapping each required-quality job to exactly one root `gate_id`;
- `profile_roots`, mapping each local QA profile to ordered root gate IDs;
- the existing workflow and Action registries.

A gate node has exactly one `kind`: `leaf`, `aggregate`, or `setup`.

- A `leaf` identifies one semantic suite with a stable `suite_key`, tracked
  first-party executable `entrypoint`, an exact string-array `argv` containing
  only arguments after that entry point, repository-relative `cwd`, admitted
  environment-key list, timeout, applicability profiles, and explicit
  opaque-leaf classification.
- An `aggregate` has only ordered `children`. It owns no entry point, argument
  vector, environment, or executable shell body.
- A `setup` represents required executable preparation that cannot be
  expressed as an immutable admitted Action. It uses the same typed
  entrypoint, argument, directory, environment, timeout, and profile rules as
  a leaf but has no semantic `suite_key`.

The graph must be acyclic. Every child must exist, every active node must be
reachable from a registered job or local profile root, and nodes forbidden by
their kind are rejected. Each semantic `suite_key` belongs to exactly one leaf.
Every required semantic `suite_key` has exactly one required-job root owner and
is reachable at most once from a workflow. Reachability is deduplicated by gate
identity before execution. Normal Compose validation and all-profile Compose
validation remain separate gate and suite identities because their
applicability and expected coverage differ.

Each of the 16 required job IDs maps to one root gate without merging status
identities. A repository-contract umbrella may verify graph wiring, registry
freshness, and static ownership, but it must not execute a focused suite owned
by another job. An opaque leaf is an explicit assurance boundary: it requires
gate-specific tests and review, cannot be an aggregate owner, and is not
recursively interpreted as arbitrary shell or Python.

The planned repository-owned runner is
`scripts/validation/run-ci-gate.py`. Its admitted interface is:

```text
python3 scripts/validation/run-ci-gate.py --profile <profile> --gate <static-gate-id>
python3 scripts/validation/run-ci-gate.py --profile <profile> --all
python3 scripts/validation/run-ci-gate.py --profile <profile> --list
python3 scripts/validation/run-ci-gate.py --profile <profile> --dry-run (--gate <static-gate-id> | --all)
```

The runner expands the registered DAG deterministically, preserves child
order, deduplicates gate identities, and executes each leaf or setup argument
vector as `[verified_entrypoint, *argv]` with `shell=False` and the registered
timeout. It confines working directories and entry points to tracked
repository-relative regular files, rejects symlinks and identity changes
between validation and execution, and binds execution to the verified file
identity rather than an unchecked path re-resolution. It starts from a minimal
allowlisted environment, clears all ambient `GIT_*` variables, and never
prints secret values. Required Git context is passed as a typed argument or
constructed from separately admitted CI metadata, not inherited through
`GIT_*`. Unknown profiles, unknown gates, malformed arguments, graph drift, or
provenance failures stop before execution.

The required workflow projection admits only:

- an immutable registered `uses:` reference; or
- the exact single-line static runner invocation
  `python3 scripts/validation/run-ci-gate.py --profile ci --gate <gate-id>`.

Executable multiline bodies, dynamic gate IDs, workflow-expression command
construction, variables, heredocs, substitutions, `eval`, `source`, shell
`-c`, direct script/tool execution, and unregistered local Actions are
rejected. Executable setup currently embedded in workflow shell is migrated to
a typed `setup` node or an immutable registered Action; there is no hidden
setup-shell exemption.

CI and local QA consume the same registry and graph. The `ci` profile derives
its roots from `job_roots`; `local-script-backed`, `local-harness`, and
`local-all-profiles` derive theirs from `profile_roots`. Profiles may select
different admitted roots, but they may not redefine a gate's entrypoint or
arguments. `local-all-profiles` consists of the full ordered
`local-script-backed` roots followed by
`local.compose-all-profiles-validation` and is selected only through
`profile_roots`, with neither a second command list nor a direct gate route.
All three local profiles exclude the CI-only `setup.compose-env` node and
preserve an existing ignored `.env` unchanged.
`scripts/validation/check-repo-contracts.sh` remains a wiring and repository
contract checker, not a second gate executor.

GitHub-native automation remains separate because its events and mutation
authority differ from required quality gates. The non-gating catalog includes
`greetings.yml`, `stale.yml`, `pr-labeler.yml`,
`generate-changelog.yml`, `document-corpus-lifecycle.yml`, and
`tech-stack-version-sync.yml`.

### Workflow Trigger Contract

The machine contract records exact allowed triggers per workflow:

- `ci-quality.yml`: `push` to `main`, `pull_request` targeting `main`, and
  `workflow_dispatch`; no path filter;
- `tech-stack-version-sync.yml`: `pull_request` targeting `main`, limited to
  governed Compose and version-registry paths;
- lifecycle, stale, greeting, label, and changelog automation: only their
  explicitly registered event, branch, path, schedule, or manual combinations.

The validator rejects `pull_request_target`, unauthorized `workflow_run`,
unauthorized `workflow_call`, event widening, permission widening, write-all,
missing timeouts, unsafe interpolation, mutable direct Action references, and
duplicate required job IDs. In the required-quality workflow it also rejects
executable steps outside the typed gate projection. Non-gating automation
remains governed by its registered trigger, permission, Action, and
classification contract rather than being counted as a required gate root.

### Action Dependency and Pre-commit Contract

A machine-readable dependency registry records each directly used Action:

- repository and action path;
- exact 40-character commit SHA;
- verified `runs.using` value or `composite`;
- official manifest URL;
- retrieval date;
- approved workflow consumers;
- security disposition.

The validator compares workflow `uses:` entries with the registry and rejects
Node 20. It does not claim to continuously inspect arbitrary remote transitive
dependencies. A composite Action with a mutable nested dependency is removed
or separately mirrored and reviewed; the current pre-commit composite follows
the removal path.

The `pre-commit` CI job installs a pinned pre-commit version and invokes a
repository-owned CI script. It retains the intentional `eslint-nextjs` skip
because frontend lint is owned by `frontend-quality`. The CI script is not an
Agent authorization path. Agents remain prohibited from direct all-files
execution and require a separate final-gate approval for
`scripts/validation/run-agent-precommit-all-files.sh`.

### Local and Remote Evidence Contract

Tracked desired state and authenticated remote observation are separate data
objects. The remote observation records repository, retrieval time, default
branch commit, workflow run IDs, exposed jobs, failing steps, branch protection
fields, ruleset result, and verification limitations. It never stores tokens,
raw logs, secret values, or credential material.

The four locally desired but not remotely required checks remain an explicit
drift list. The observed remote failures remain failures at their remote
commits; local fixes are candidates only until pushed and rerun under separate
approval. Root causes remain `unverified` unless sanitized logs are separately
approved and inspected.

## Core Design

### Dependency-Ordered Tasks

| Task | Implementation boundary | Primary output |
| --- | --- | --- |
| T-TSDC-001 | Delta foundation | Successor manifest, baseline contract, whole-surface omissions check, failing fixtures |
| T-TSDC-002 | Document surface convergence | README, typed example, archive, project, and redacted secret-catalog normalization |
| T-TSDC-003 | Runtime-support and legacy convergence | Verified active-path cleanup across infra, scripts, and tests with provenance and rollback |
| T-TSDC-004 | CI and QA control-plane convergence | Typed gate registry and DAG, exact runner, workflow/local projections, trigger and dependency contracts, CI pre-commit entry point, governance coupling |
| T-TSDC-005 | Audit and remote evidence reconciliation | Updated canonical audit facts, generated summaries, remote drift observation, cross-links |
| T-TSDC-006 | Closure and whole-branch review | Full validation ladder, independent reviews, terminal Task and memory evidence |

Task 1 must land before any destructive or protected-surface change. Tasks 2
and 3 consume its classification and validation interfaces. Task 4 may proceed
after the foundation contract is stable but must account for scripts and tests
owned by Task 3. Task 5 consumes the implementation heads of Tasks 2 through 4.
Task 6 begins only after all prior task reviews are closed.

Task 4 uses a three-wave cutover:

1. introduce the version 2 registry, DAG validator, runner, and failing
   contract fixtures while retaining current workflow execution;
2. convert workflow and local QA routes to typed gates and prove ordered
   one-time parity with a fake executor;
3. remove the dead prior shell/Python semantic interpreter and its obsolete
   tests only after independent parity review.

When schema version 2 becomes canonical, it is the sole ownership authority:
`ExpensiveCommandOwner`, `_EXPENSIVE_COMMAND_BASELINE`, and every active
semantic-ownership claim or hard-coded command table are removed in that same
conversion. The remaining old parser implementation may exist only as
dead/inactive cutover evidence until Wave C deletes it; it is neither a
fallback nor a parallel authority. Failure in any wave leaves Task 4 blocked
without weakening the exact runner grammar.

### Convergence Flow

1. Discover the immutable predecessor and current path set.
2. Classify each delta path and recompute whole-surface coverage.
3. Add a failing regression fixture for each confirmed drift class.
4. Change the smallest canonical owner and its direct consumers.
5. Run focused validation and sanitize evidence.
6. Obtain independent specification and quality review.
7. Commit one logical task.
8. Regenerate registered evidence after implementation truth is stable.
9. Run the final validation ladder and whole-branch review.
10. Record local, remote, skipped, and unverified outcomes separately.

## Interfaces and Data

### Delta Manifest Record

Each record contains:

- `path`;
- `surface_class`;
- `profile`;
- `changed_since`;
- `disposition`;
- `canonical_owner`;
- `direct_consumers`;
- `finding`;
- `replacement`;
- `secret_safety`;
- `validators`;
- `tests`;
- `provenance`;
- `rollback`;
- `spec_verdict`;
- `quality_verdict`.

`replacement` is required for `migrate`, optional for `delete` when withdrawal
is valid, and absent for `preserve`. Destructive dispositions require
provenance, rollback, and both review verdicts. Secret-bearing payload data is
not a permitted field.

### Action Dependency Record

Each record contains:

- `action`;
- `sha`;
- `runtime`;
- `manifest_url`;
- `retrieved_at`;
- `consumers`;
- `security_disposition`.

Records are ordered deterministically by action and path. The validator
requires an exact registry match for every external `uses:` reference and
rejects unused active records.

### Typed Gate Node Record

Each gate node contains:

- `gate_id`;
- `kind`;
- `suite_key` for semantic leaves;
- `entrypoint` and `argv` for executable leaves and setup nodes;
- `cwd`;
- `allowed_env_keys`;
- `timeout_minutes`;
- `profiles`;
- `opaque`;
- ordered `children` for aggregate nodes.

Fields not admitted by the selected `kind` are forbidden rather than ignored.
Argument vectors contain literal strings. The runner performs no shell,
workflow-expression, substitution, or implicit environment expansion; a leaf
program that interprets an argument is covered only by that opaque leaf's
focused tests and review. Registry ordering and `--list` or `--dry-run` output
are deterministic.

### CI Job Root Record

Each job-root record contains:

- `workflow`;
- `job_id`;
- `root_gate_id`;
- `classification`.

The 16 required-quality records must match the preserved job-ID set exactly.
Graph validation computes root ownership and semantic-suite reachability from
these records; a second hard-coded command table is not permitted.

### Local QA Profile Root Record

Each local profile-root record contains:

- `profile`;
- ordered `root_gate_ids`;
- `classification`.

The admitted local profiles are exactly `local-script-backed`,
`local-harness`, and `local-all-profiles`. Their roots may reuse CI gates but
cannot override node fields. `local-all-profiles` is the complete ordered
`local-script-backed` root sequence followed by
`local.compose-all-profiles-validation`; it is selected only through its
`profile_roots` record and has neither a second command list nor a direct gate
route. All three local profiles exclude the CI-only `setup.compose-env` node
and preserve an existing ignored `.env` unchanged. The `ci` profile is derived
from required `job_roots`, so the registry cannot define a conflicting second
CI root list.

### Remote Observation Record

The observation contains value-free fields for:

- repository and retrieval timestamp;
- local and remote commit identities;
- tracked and remote workflow inventory;
- desired and observed required checks;
- branch protection and ruleset observations;
- workflow run and job metadata;
- verification boundary;
- proposed future sync and rollback guidance.

It is evidence, not desired-state authority and not a mutation instruction.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| Rewriting predecessor history | Hash and path assertions reject changes to Spec 133 evidence. |
| Missing a changed path | Git-delta recomputation and whole-surface enumeration fail closed. |
| Blanket frontmatter insertion | Native-surface and README-profile tests reject unconsumed metadata. |
| README becomes a second policy owner | Forbidden-topic and canonical-owner routing checks block duplicated shared rules. |
| Template filler replaces real content | Placeholder and repeated-template scanners fail; review requires topic-specific evidence. |
| Secret value enters output | Value-free fixtures, path-only inventory, redaction checks, and prohibited-payload scans block evidence. |
| Historical evidence is deleted as deprecated | Path class and active-consumer evidence are mandatory before destructive disposition. |
| Required status identity changes accidentally | Four-way coupling check compares workflow, validator, governance, and desired protection document. |
| Workflow trigger widens | Exact event/branch/path contract rejects unregistered trigger changes. |
| Mutable or Node 20 Action enters CI | Dependency registry and full-SHA/runtime tests fail. |
| CI duplicates a semantic suite | DAG reachability requires one required-job owner and at most one workflow execution for each `suite_key`. |
| A workflow bypasses the registry | Exact projection checks reject free-form, multiline, computed, indirect, or unregistered executable steps. |
| Gate graph contains a cycle, missing child, or orphan | Schema and graph validation fail before workflow or local execution. |
| Aggregate node hides executable behavior | Kind-specific forbidden fields and opaque-leaf rules reject executable aggregate nodes. |
| Entrypoint or environment is redirected after validation | Repository confinement, no-follow regular-file checks, verified identity binding, and minimal environment construction fail closed. |
| CI and local QA drift | Both projections resolve gate identities from the same versioned registry and deterministic runner. |
| Local pass is reported as remote enforcement | Evidence schema separates local, desired, observed, and unverified axes. |
| Generated output is hand-edited | Generator-owner and byte-for-byte check mode reject drift. |
| Another agent's work is overwritten | File ownership, isolated worktree, status checks, and scoped commits are mandatory. |
| Final QA mutates unrelated paths | Controlled wrapper requires a new approval, clean linked worktree, minimal allowed prefixes, and recorded evidence. |

No destructive recovery uses `git reset --hard` or reverts unrelated user
work. Corrections are made through scoped edits and new commits. Remote
failures, unavailable tools, and environment limitations remain explicit
instead of being converted into product passes.

## Verification

### Per-Task Evidence

Each task records:

- baseline and implementation commit;
- changed and preserved paths;
- focused test commands and results;
- skipped or unavailable checks with rationale;
- secret-safety boundary;
- implementation-agent handoff;
- specification review;
- quality and security review;
- corrective iterations;
- final logical commit.

### Validation Ladder

1. **Diff hygiene:** `git status --short`, `git diff --check`, scoped diff and
   deleted-consumer review.
2. **Native syntax:** YAML, JSON, TOML, shell, Python, workflow, Compose, and
   Markdown checks selected by changed paths.
3. **Focused regression:** target-surface, metadata, archive, workflow,
   typed-gate schema, DAG ownership, exact projection, runner,
   action-dependency, QA-routing, and script tests for the changed contract.
4. **Repository contracts:** document implementation alignment, cross-links,
   target-surface checker, audit freshness, and repository contract suite.
5. **Conditional domain gates:** Compose, hardening, supply-chain, frontend,
   and coverage checks only when their implementation inputs changed.
6. **Controlled all-files gate:** only after a new explicit approval, through
   the clean-worktree wrapper, with value-free Task evidence.
7. **Whole-branch review:** fresh correctness, security, scope, deletion,
   evidence, and documentation review.

Remote workflow success is not a local validation rung. It remains pending
until a separately approved push or pull request executes the tracked
definitions.

Task 4 focused evidence must include positive and mutation cases for duplicate
IDs, duplicate owners, duplicate suite reachability, cycles, missing children,
orphans, unregistered entrypoints, symlink or provenance failure, dynamic gate
IDs, co-mutated workflow and registry data, free-form shell, direct program
execution, permission drift, Action drift, trigger drift, and required-job
drift. A fake executor must demonstrate the exact ordered leaf set and one-time
execution without invoking real suites. The existing trigger, permission,
concurrency, timeout, Action, CI pre-commit, and 16-job contracts remain
regression gates through cutover.

The resulting assurance is intentionally structural and repository-local. It
does not prove arbitrary equivalence inside an opaque leaf, remote enforcement,
or immunity from a malicious change to the validator and registry in the same
revision. Independent review, immutable provenance, branch protection, and
remote CI remain separate controls.

## Agent Role and IO Contract

Each logical task uses a fresh implementation agent with explicit file
ownership and a reminder that other agents share the repository and must not
have their changes reverted. The implementation agent receives the approved
Spec, Plan task, starting commit, allowed files, non-goals, and required tests.
It returns a scoped diff summary, commands, results, limitations, and proposed
commit.

An independent specification reviewer verifies requirement coverage and scope.
A separate quality reviewer verifies correctness, security, maintainability,
test adequacy, secret safety, and deletion evidence. Review findings return to
the same task implementation loop until resolved. The final whole-branch
reviewer is fresh and did not implement the reviewed task.

Task 4 requires an additional independent cutover review before deleting the
old semantic interpreter. That review compares the preserved 16 job roots,
ordered fake-executor output, local/CI profile projection, negative mutation
coverage, and retained workflow-shape controls. It cannot authorize remote
mutation or expand the approved retry budget.

The root agent owns task sequencing, worktree integrity, cross-task conflict
resolution, logical commits, generated-evidence timing, terminal Task state,
and the distinction between local, remote, skipped, and unverified evidence.

## Related Documents

- [Spec 133: Target Surface Contract Convergence](../spec-0133-target-surface-contract-convergence/spec.md)
- [Spec 134: Agent Governance Canonical Convergence](../spec-0134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/ref-0019-readme.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Workflow contract](../../../.github/workflow-contract.yml)
- [Target surface checker](../../../scripts/validation/check-target-surface-contract.py)
- [Repository contract checker](../../../scripts/validation/check-repo-contracts.sh)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
