---
title: "Reference: GitHub Actions Platform Mechanics"
type: reference/research-pack
layer: references
status: active
owner: "@buenhyden"
artifact_id: RES-0084
parent_ids: []
created: '2026-07-05'
updated: '2026-08-23'
observed_at: '2026-07-05'
reviewed_at: 2026-08-10
---

# Reference: GitHub Actions Platform Mechanics

## Overview

GitHub Actions is the remote execution substrate this repository depends on,
but the pack has so far described only the part of it the repository actually
uses. That leaves the platform's own rules — how tokens are scoped, how trust
crosses a fork boundary, how a cache can become an execution channel, what a
ruleset can and cannot be read from — documented nowhere.

This reference covers the platform mechanics. It deliberately does not
re-inventory the repository's workflows, jobs, or pinned actions; those live in
`automation, pipeline, and workflow` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `automation-pipeline-workflow` leaf) and are
not duplicated here. The one repository-facing section below records which
platform capabilities are _not_ adopted, which is the complement of that
inventory rather than a copy of it.

Every external claim here was retrieved on **2026-08-10**. GitHub Actions
documentation is mutable guidance under continuous revision, and during this
retrieval several documentation paths returned HTTP 404. An independent check
the same day could not reproduce those failures, so they may have been
transient rather than evidence of a completed docs-tree restructure. Either
way, treat every figure as a point-in-time snapshot.

## Purpose

Record how the GitHub Actions platform behaves, independent of how this
repository happens to use it, so that future workflow changes can be reasoned
about against documented platform rules rather than against local habit.

## Repository Role

`.github/workflows/` and `.github/workflow-contract.yml` remain the tracked
implementation and its typed registry.
`docs/00.agent-governance/rules/github-governance.md` remains the active
policy. This Stage 90 document is a platform reference and changes no rule,
workflow, or contract.

## Scope

### In Scope

- `GITHUB_TOKEN` permission model and repository/organization defaults
- OIDC issuance, claim structure, and subject formats
- Reusable workflows versus composite actions
- Untrusted input, script injection, and privileged-trigger hazards
- Supply chain hardening: SHA pinning, attestations, immutable releases
- Execution control: concurrency, matrix, caching
- Environments, rulesets, and the remote-enforcement read-back boundary
- Runner models including Actions Runner Controller
- Third-party workflow static analysis
- Which of the above this repository does not adopt

### Out of Scope

- Re-inventorying tracked workflows, jobs, or action pins
- Changing any workflow, permission, contract, or policy
- Cloud-provider-specific OIDC trust configuration
- Any authenticated read-back of this repository's remote control plane
- Secret values, tokens, private keys, or raw run logs

## Definitions / Facts

- **`GITHUB_TOKEN`** is an installation token minted per workflow run whose
  scopes are governed by the `permissions` key.
- **Verification of remote enforcement** is not possible from workflow files.
  Ruleset and branch-protection state lives server-side.
- **Mutable guidance** means the source page carries no version and may change
  without notice. Nearly every source in this document is mutable guidance.
- **Version-sensitive claim** means a figure tied to an action major version,
  runner image, or documented numeric limit. These drift fastest.

## Permission and Token Model

`permissions` may be set at workflow level, applying to all jobs, or at job
level via `jobs.<job_id>.permissions`, where the job-level value overrides the
workflow-level one.

The rule that makes least privilege practical is that omission means denial:
"If you specify the access for any of these permissions, all of those that are
not specified are set to `none`." Each scope accepts `read`, `write`, or
`none`. That write subsumes read is the conventional reading of the scope
values and is recorded here as an inference; no retrieved page states it as a
sentence.

The current scope list holds **16 scopes**: `actions`, `artifact-metadata`,
`attestations`, `checks`, `code-quality`, `contents`, `deployments`,
`discussions`, `id-token`, `issues`, `packages`, `pages`, `pull-requests`,
`security-events`, `statuses`, `vulnerability-alerts`. This list has grown over
time; older references list twelve or thirteen, so a scope list must not be
copied from memory or from an archived page.

Three shorthand forms exist. `read-all` grants read everywhere, `write-all`
grants write everywhere, and `permissions: {}` disables all permissions.

At repository and organization level the default is either **permissive** —
read and write for all permissions — or **restricted**, which is read access
for `contents` and `packages` only. New personal-account repositories default
to restricted; organization repositories inherit the organization setting. A
separate toggle governs whether Actions may create and approve pull requests,
defaulted off for personal repositories.

Across a fork boundary the model tightens. A `pull_request` event from a fork
yields a read-only token, and the documentation states that you can add and
remove read permissions for forked repositories "but typically you can't grant
write access" unless an administrator enables sending write tokens to
workflows from pull requests.

**Boundary worth stating.** The widely used idiom of declaring
`permissions: {}` at workflow level and granting narrowly per job is a sound
reading of the documented primitives, but it is a community-hardened
convention rather than a sentence GitHub publishes. GitHub Security Lab
separately warns that `permissions: {}` alone "can unexpectedly pave the way
for cache poisoning attacks," so the idiom must not be presented as sufficient
on its own.

## OIDC and Keyless Authentication

`id-token: write` is the enabling permission: "The job or workflow must grant
the `id-token: write` permission to allow GitHub's OIDC provider to create a
JSON Web Token (JWT)." The issuer is
`https://token.actions.githubusercontent.com`, with discovery at that host's
`/.well-known/openid-configuration`.

The token carries the standard `aud`, `iss`, `sub`, `exp`, `iat`, `jti`, and
`nbf` claims plus a large GitHub-specific set including `actor`, `environment`,
`event_name`, `job_workflow_ref`, `job_workflow_sha`, `ref`, `repository`,
`repository_id`, `repository_owner`, `repository_visibility`, `run_id`,
`run_attempt`, `runner_environment`, `workflow_ref`, and `repo_property_*`.

Subject formats determine what a cloud trust policy can pin to:

| Context      | `sub` format                                             |
| ------------ | -------------------------------------------------------- |
| Branch       | `repo:ORG/REPO:ref:refs/heads/BRANCH`                    |
| Tag          | `repo:ORG/REPO:ref:refs/tags/TAG`                        |
| Pull request | `repo:ORG/REPO:pull_request`                             |
| Environment  | `repo:ORG/REPO:environment:NAME`                         |
| Immutable    | `repo:OWNER@OWNER-ID/REPO@REPO-ID:ref:refs/heads/BRANCH` |

Subject customization is done through the REST API with `include_claim_keys`,
replacing the default predefined format.

The security property is lifetime. Once the cloud provider validates the
claims it "provides a short-lived cloud access token that is available only
for the duration of the job," and the OIDC token itself is "valid for a single
job, and then automatically expires." This removes the need to store a
long-lived credential as a repository secret at all.

Cloud-provider-side trust configuration was not retrieved and is not asserted
here.

## Reusable Workflows and Composite Actions

Reusable workflows live in `.github/workflows/` and declare `on:
workflow_call:` with typed `inputs` (`boolean`, `number`, `string`),
`outputs`, and `secrets`. Step outputs must first be promoted to job outputs
before a reusable workflow can expose them.

`secrets: inherit` passes all caller secrets implicitly within the same
organization or enterprise. Environment secrets are the exception and cannot
be passed, because `on.workflow_call` does not support the `environment`
keyword.

Two constraints bound the composition graph. Depth is capped: "You can connect
a maximum of ten levels of workflows — that is, the top-level caller workflow
and up to nine levels of reusable workflows," and loops are rejected.
Permission flow is monotonic downward: "Permissions can only be maintained or
reduced — not elevated — throughout the chain."

A comparison against composite actions, condensed from GitHub's own comparison
table. This is a selection, not a reproduction: GitHub's table carries nine
data rows, four of which are omitted here, and the Runner row below is drawn
from the adjacent "Specifying runners" prose rather than from the table
itself.

| Dimension   | Reusable workflow                    | Composite action                        | Source         |
| ----------- | ------------------------------------ | --------------------------------------- | -------------- |
| Unit        | Jobs                                 | Steps run as a single caller step       | Official table |
| Logging     | Every job and step logged separately | Only the calling step appears           | Official table |
| Secrets     | Can use secrets                      | Cannot use secrets                      | Official table |
| Marketplace | Cannot publish                       | Can publish                             | Official table |
| Nesting     | 10 levels                            | Up to 10 composite actions per workflow | Official table |
| Runner      | Can select a different machine       | Runs on the caller's machine            | Adjacent prose |

A composite action runs inside the caller's job and therefore has no
`permissions:` key of its own. That follows from the "single step within the
caller workflow" framing, but no retrieved page states it directly, so it is
recorded here as an inference rather than a quotation.

## Untrusted Input and Privileged Triggers

The mechanism is substitution order. Security Lab states it plainly: "The
expressions inside of `${{ }}` are evaluated and substituted with the
resulting values before the shell script is run which may make it vulnerable
to shell command injection."

The official mitigation is an intermediate environment variable, not
escaping: "For inline scripts, the preferred approach to handling untrusted
input is to set the value of the expression to an intermediate environment
variable." The documented alternative is "a JavaScript action that processes
the context value as an argument."

Attacker-controlled context fields include `github.event.issue.title` and
`.body`, `github.event.pull_request.title`, `.body`, `.head.ref`, and
`.head.label`, `github.event.comment.body`, `github.event.review.body`,
`github.event.commits.*.message`, `github.event.head_commit.message`, and
`github.head_ref`.

`pull_request_target` is the trigger that turns injection into compromise. It
"runs in the context of the default branch of the base repository, rather than
in the context of the merge commit," which means secrets and a write-scoped
token are present. GitHub's warning is explicit: "Running untrusted code on the
`pull_request_target` trigger may lead to security vulnerabilities. These
vulnerabilities include cache poisoning and granting unintended access to write
privileges or secrets."

GitHub now publishes a dedicated reference for this trigger whose governing
rule is: "You must ensure the checked-out code is only ever inspected as data
and never executed before using a `pull_request_target` event." It names three
pwn-request patterns — checking out `github.event.pull_request.head.sha` and
building it, spoofing the checkout repository to the fork, and fetching PR code
outside `actions/checkout` then executing it — and notes the class is not
unique to this trigger: "Any event that runs with secrets can introduce a pwn
request if it checks out or downloads and executes untrusted code."

`workflow_run` is the parallel hazard. Security Lab notes it "may grant write
permissions and access to secrets even if the triggering workflow doesn't have
such privileges," with artifact poisoning as the companion pattern.

The platform has begun closing this by default. `actions/checkout` "refuses to
check out fork pull request code by default when the workflow is triggered by
`pull_request_target` or `workflow_run`," and opting out requires
`allow-unsafe-pr-checkout: true` — a flag GitHub says "is intentionally named to
be easy to spot in code review and static analysis."

The safer default is **not** confined to v7. It shipped in v7.0.0 on 2026-06-18
and was then backported as a breaking change to v6.1.0, v5.1.0, v4.4.0, v3.7.0,
and v2.8.0, all published 2026-07-20. Pinning to an older major therefore no
longer exempts a workflow from the change. This matters here: the repository
pins `actions/checkout` by commit SHA with no version comment, so the effective
major is not readable from the workflow file.

## Supply Chain Hardening

The canonical sentence on pinning: "Pinning an action to a full-length commit
SHA is currently the only way to use an action as an immutable release." The
stated rationale is that defeating it "would need to generate a SHA-1 collision
for a valid Git object payload." Tag pinning is acceptable "only if you trust
the creator," because tags can be moved or deleted if the upstream repository
is compromised.

Artifact attestations reach **SLSA v1.0 Build Level 2** by default: "Artifact
attestations by itself provides SLSA v1.0 Build Level 2." Level 3 is reachable
through isolation — "Reusable workflows can provide isolation between the build
process and the calling workflow, to meet SLSA v1.0 Build Level 3." Trust roots
differ by visibility: public repositories use the Sigstore Public Good Instance
with a publicly readable immutable transparency log, while for private
repositories GitHub's own Sigstore instance is used and "it does not have a
transparency log and only federates with GitHub Actions." Attestation requires `id-token: write`, `attestations: write`, and
`contents: read`, plus `packages: write` for container images and
`artifact-metadata: write` when `push-to-registry: true`.

**Version-sensitive finding.** `actions/attest-build-provenance` is at v4.2.2,
published 2026-08-06, and its own release note redirects new work elsewhere:
"As of version 4, `actions/attest-build-provenance` is simply a wrapper on top
of `actions/attest`." and "Existing applications may continue to use the
`attest-build-provenance` action, but new implementations should use
`actions/attest` instead." Most third-party guidance still names
`attest-build-provenance` as the action to adopt. Verified directly against the
GitHub REST release endpoint rather than a rendered page.

Immutable releases are generally available. When enabled, "Once an immutable
release is published, its associated Git tag is locked to a specific commit,
cannot be changed, and cannot be deleted while the release exists," and
publishing generates an attestation containing tag, commit SHA, and assets.
Two properties matter operationally: immutability "will only apply to future
releases," and repository-resurrection protection means tags associated with
immutable releases cannot be reused even after deleting and recreating a
repository of the same name.

Dependabot supports the `github-actions` ecosystem with `directory: "/"`
monitoring `.github/workflows`, and keeps both action references and reusable
workflow references current. Whether Dependabot rewrites SHA pins together with
their trailing version comments was not confirmed and is not asserted.

Repository-level allowlisting offers four policies: allow all; local only
(`./` and `$/` references); verified creators; or selected actions with
wildcard and exclusion syntax.

## Execution Control

Concurrency admits one job or workflow per group at a time. Group names are
case-insensitive, and queue processing is **FIFO by wait time, not dispatch
time**. A newer `queue` key accepts `single` (default) or `max`; under `max` up
to 100 runs may be pending in a group, and the combination of `queue: max` with
`cancel-in-progress: true` is rejected as a validation error.

Matrix `include` entries are processed sequentially, later entries can overwrite
earlier ones, entries matching an existing combination add variables to those
jobs, and non-matching entries become separate jobs. `exclude` is applied
afterwards. `max-parallel` caps simultaneous matrix jobs; no upper bound on the
setting itself is documented.

Caching resolves an exact key first, then partial matches, then `restore-keys`
in order, and among multiple partial matches "the most recent cache is
restored." Isolation runs along the branch graph: runs may restore from the
current branch or the default branch, and PR workflows may reach base-branch
caches including in forks, but "Workflow runs cannot restore caches created for
child branches or sibling branches."

Cache is an execution channel, not just an optimization. GitHub's own framing:
"Cache contents are not signed or verified, and any workflow run that can read
a cache may extract its contents. Extracted caches may modify files that are
subsequently executed in a workflow run, leading to malicious code execution."
The documented mitigations are to keep sensitive data out of caches, restrict
cache writes to trusted actors, and "In low-trust workflows, switch to a
restore-only cache operation such as `actions/cache/restore`."

**Recent platform change.** Since 2026-06-26 GitHub issues read-only cache
tokens for untrusted triggers — `pull_request_target`, `issue_comment`, and
fork-PR `workflow_run` cascades scoped to the default-branch SHA — while
`push`, `schedule`, `workflow_dispatch`, `repository_dispatch`, `delete`,
`registry_package`, and `page_build` retain read-write, as do triggers whose
scope is not the default branch, `pull_request` and `release` among them. The
seven named triggers are therefore not an exhaustive read-write list.
Behavior on a blocked
save is a warning, not a failure: "`actions/cache` logs a warning in the run and
the job continues without saving." Any cache-poisoning guidance written before
this date is partially superseded.

## Environments, Rulesets, and Remote Enforcement

Environments gate a job before it runs or reads environment secrets. Required
reviewers allow "up to 6 people or teams," and "Only one of the required
reviewers needs to approve the job for it to proceed." A wait timer delays in
minutes, and branch/tag deployment policies restrict which refs may deploy.
Deleting an environment automatically fails any job waiting on its protection
rules.

Rulesets differ from classic branch protection in three ways that matter for
evidence. They aggregate — "Multiple rulesets can apply at the same time" and
on conflict "the most restrictive version of the rule" applies. They are
visible — "anyone with read access to a repository can view the active
rulesets," unlike admin-only branch protection. And they extend beyond branches
to tag rulesets and push rulesets, the latter applying "across all pushes
without branch targeting" and restricting file paths, extensions, and sizes
across entire fork networks.

Required status checks support a strict mode where "The topic branch **must**
be up to date with the base branch before merging," and a specific GitHub App
may be designated as the expected status source.

**The read-back boundary.** Ruleset state has no workflow-file representation.
It is readable through the UI by anyone with read access, and programmatically
through authenticated REST endpoints — `GET /repos/{owner}/{repo}/rules/branches/{branch}`,
`GET /repos/{owner}/{repo}/rulesets` (with `includes_parents` defaulting to
true), and the per-ruleset and history endpoints. `bypass_actors` is returned
only to a caller with write access to the ruleset. This is why tracked workflow
YAML can never establish that a check is required, and why the pack's
separation of tracked intent from remote enforcement is a platform property
rather than a local caution.

## Runner Models

The governing warning is unambiguous: "Self-hosted runners should almost never
be used for public repositories on GitHub, because any user can open pull
requests against the repository and compromise the environment." GitHub-hosted
runners execute in "ephemeral and clean isolated virtual machines"; self-hosted
runners "do not have guarantees around running in ephemeral clean virtual
machines." Runner groups default to private-repository access only.

Actions Runner Controller is a Kubernetes operator that "orchestrates and
scales self-hosted runners for GitHub Actions" using CRDs, controller managers,
and listener pods over autoscaling runner scale sets, with ephemeral runner
instances. Constraints include a 45-character runner name limit, custom images
placing binaries in `/home/runner/` and launching `/home/runner/run.sh`, and
Kubernetes mode requiring container hooks in `/home/runner/k8s`. If no runner
accepts a job within 24 hours, Actions unassigns it.

Standard GitHub-hosted runners are free and unlimited on public repositories.
Larger runners bill per active minute, are not eligible for included minutes on
private repositories, and require a card on file plus a nonzero spending limit.

## Third-Party Workflow Static Analysis

Neither tool below is GitHub-official. Both are independently versioned, carry
no GitHub support commitment, and are themselves supply-chain dependencies that
should be SHA-pinned like any other action.

**zizmor** is security-focused. At **v1.29.0**, published 2026-08-01, it
implements **40 audit rules** covering the hazards described earlier in this
document: `template-injection` for the substitution-order problem,
`cache-poisoning` for the unsigned-cache channel, `dangerous-triggers` for
`pull_request_target`, `excessive-permissions` for the token model,
`unpinned-uses` and `impostor-commit` for pinning, `secrets-inherit` and
`overprovisioned-secrets` for reusable-workflow secret flow, and
`self-hosted-runner` for the public-repository runner warning.

That count is version-pinned deliberately. `https://docs.zizmor.sh/audits/`
currently renders 41 audits because it tracks unreleased main; the extra entry,
`self-repository`, does not exist at the v1.29.0 tag. Counting the audit
sources at the tag gives 41 `.rs` files under `crates/zizmor/src/audit/`, one of
which is `mod.rs`, so 40. This is the same rendered-page-versus-release trap the
Application Notes warn about for action versions, and it caught this document
once.

zizmor sorts findings by three personas: `regular` (default, core security findings),
`pedantic` (adds quality-focused audits with limited security impact), and
`auditor` (the most comprehensive, flagging findings that include probable
false positives, so the highest noise tolerance). The personas are sensitivity
thresholds that decide which findings are emitted, not a grouping applied to a
fixed finding set.

**actionlint** is correctness-focused. At **v1.7.12**, published 2026-03-30,
MIT licensed, it validates workflow syntax, type-checks `${{ }}` expressions,
verifies action inputs and step outputs, checks reusable-workflow input, output
and secret wiring, validates `needs:` graphs, runner labels, glob syntax, and
cron expressions, and shells out to shellcheck and pyflakes to analyse `run:`
blocks. Its security coverage is a sideline rather than its purpose.

The two are complementary rather than alternative: actionlint catches workflows
that will not behave as written, zizmor catches workflows that behave exactly as
written and should not.

This repository runs both, by different routes. zizmor is the `zizmor` job in
`ci-quality.yml`, uploading SARIF; there is no zizmor configuration file, so the
default persona applies. Note the version gap: the figures above are for
v1.29.0, while `ci_gate_adapters.py:1010` pins `zizmor==1.28.0`, so the audit
count in force here is whatever 1.28.0 shipped rather than the 40 above. actionlint runs as a pre-commit hook:
`.pre-commit-config.yaml` pins `rhysd/actionlint` at `rev: v1.7.12` scoped to
`^\.github/workflows/.*\.(yml|yaml)$`, and `run-ci-precommit.sh` — the
entrypoint of `leaf.pre-commit` under the required-quality root
`ci.pre-commit` — executes `pre-commit run --all-files` skipping only
`eslint-nextjs`. Both therefore run on every push and pull request to `main`.

Worth noting against the pinning guidance above: the actionlint hook is pinned
by tag, not by commit SHA. `.pre-commit-config.yaml` is a different mechanism
from `uses:` and GitHub's immutable-release argument does not transfer to it
unchanged, but the mutable-tag exposure is the same in kind.

## Platform Capability Adoption in This Repository

This is the complement of the tracked inventory in
`automation, pipeline, and workflow` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `automation-pipeline-workflow` leaf), which
records what the repository _does_ declare. This table is therefore strictly
negative: it records only capabilities the repository does **not** use. What it
does use is not restated here. Derived at `4122cecf` by scanning
`.github/workflows/`.

| Capability                           | Evidence of non-use                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `pull_request_target`                | No occurrence — the principal injection hazard is absent by construction                          |
| OIDC (`id-token`)                    | No occurrence; no keyless cloud authentication exists                                             |
| Reusable workflows (`workflow_call`) | No occurrence; the 16 quality jobs are declared in full rather than factored                      |
| Composite actions                    | No `action.yml` or `action.yaml` anywhere in the repository                                       |
| Environments                         | No job references an `environment`; the automation leaf records the resulting CD gap              |
| Artifact attestation                 | No `attest` reference despite the pack citing the guidance                                        |
| Matrix strategy                      | No `strategy:`/`matrix:` in any workflow                                                          |
| Custom caching                       | Only `setup-node`'s built-in `cache: 'npm'` at three sites; no `actions/cache` with explicit keys |

Two platform-side observations follow, neither of which the sibling records.

First, the repository already uses the deny-all-then-grant idiom analysed
above. `greetings.yml`, `pr-labeler.yml`, and `stale.yml` each declare
`permissions: {}` at workflow level and grant per job. That is the community
convention this document declines to attribute to GitHub, in live use here.

Second, permission elevation is broader than the sibling's `ci-quality.yml`
scope implies. Across all seven workflows, **five jobs in four workflows** hold
a write scope: `zizmor` (`security-events: write`, `actions: read`),
`issue-greeting` and `pull-request-greeting` (`issues: write`), `triage`
(`pull-requests: write`), and `stale` (`issues: write`,
`pull-requests: write`). The sibling's statement that only `zizmor` elevates is
correct **within `ci-quality.yml`** and must not be generalised to the
repository, which is exactly the error this table previously made.

Exposure to the two highest-severity platform hazards — pwn requests and cache
poisoning — is nonetheless low, because the repository uses neither
`pull_request_target` nor writable custom caches. That is a property held by
construction rather than by mitigation, so it is worth preserving deliberately
rather than assuming it will survive the next workflow change.

## Documented Limits

Every figure retrieved 2026-08-10 and version-sensitive. Most come from the
Actions limits reference, but six do not and are cited to their own pages
instead: reusable-workflow nesting and composite-action nesting from the
reuse-workflows and reusable-workflows pages, required reviewers from
manage-environments, rulesets per repository from about-rulesets, and cache
eviction and key length from dependency-caching.

| Limit                              | Value                          |
| ---------------------------------- | ------------------------------ |
| Workflow run time                  | 35 days                        |
| Job execution, GitHub-hosted       | 6 hours                        |
| Job execution, self-hosted         | 5 days                         |
| Job queue time, self-hosted        | 24 hours                       |
| Matrix jobs per workflow run       | 256                            |
| Environment gate approval window   | 30 days                        |
| Re-runs                            | 50                             |
| Concurrency group queue            | 100 runs                       |
| Reusable workflow nesting          | 10 levels (caller plus 9)      |
| Composite action nesting           | 10 per workflow                |
| Required reviewers per environment | 6 people or teams              |
| Rulesets per repository            | 75                             |
| Cache storage per repository       | 10 GB                          |
| Cache eviction                     | Entries unused for 7 days      |
| Cache key maximum length           | 512 characters                 |
| API rate, `GITHUB_TOKEN`           | 1,000 requests/hour/repository |

## Analysis

Three platform properties explain most of the security guidance above.

Trust is assigned by trigger, not by code. The same repository content executes
with a read-only token under `pull_request` and with secrets and write access
under `pull_request_target`. Nothing in the workflow file distinguishes them;
only the event does.

State that crosses runs is an execution channel. Caches and artifacts are
written by one run and consumed by another, are unsigned, and can carry files
that a later run executes. Permission scoping does not close this, which is
precisely Security Lab's point about `permissions: {}`.

Enforcement lives outside the repository. Required checks, reviewers, and
deployment gates are server-side configuration readable only through the UI or
an authenticated API. A green workflow file proves intent and nothing more.

## Application Notes for This Workspace

- Treat every figure in this document as dated. Several documentation paths
  returned 404 during retrieval; a same-day independent check could not
  reproduce them, so re-test before repeating that caveat as a live condition.
- Verify action versions against the REST release endpoint rather than a
  rendered page. A summarizing fetch of the `attest-build-provenance` releases
  page during this research returned a publication year one full year off; the
  API returned the correct value.
- If artifact attestation is ever adopted, use `actions/attest` rather than
  `actions/attest-build-provenance`, per the upstream release note.
- Record the absence of `pull_request_target` and writable caches as a
  deliberate posture, so a future workflow change does not silently introduce
  either.
- Do not describe `permissions: {}` plus per-job grants as GitHub's documented
  recommendation. It is a sound community idiom built on documented primitives.
- Keep citing rulesets as unverifiable from tracked files. That is a platform
  property, not a gap in local evidence.

## Potential Follow-up / Gap

- A scope-by-scope table of `GITHUB_TOKEN` defaults under permissive versus
  restricted could not be retrieved; four candidate URLs either 404ed or no
  longer served the table. Only the two summary sentences are recorded.
- The `GITHUB_TOKEN` lifetime is not stated on the authentication page. No
  duration is asserted here.
- The documented default for `fail-fast` was not found on the matrix page and is
  not asserted.
- Cloud-provider OIDC trust configuration is unverified and would need separate
  retrieval before any adoption work.
- Whether Dependabot rewrites SHA pins with their version comments is
  unverified.
- Ruleset enforcement status `evaluate` was not present in the retrieved
  content and is not asserted, though it exists on some plans.

## Source Rules

- All external sources were retrieved on **2026-08-10** and are mutable
  retrieval-time guidance unless marked otherwise. None carries a visible
  last-updated date except the two `github.blog` changelog entries.
- Action and tool versions were verified against the GitHub REST API, which is
  authoritative, rather than against rendered documentation pages.
- Quoted sentences are reproduced verbatim from the cited page. Claims that
  could not be retrieved are listed under Potential Follow-up / Gap rather than
  paraphrased.
- `zizmor` and `actionlint` are third-party, independently versioned, and carry
  no GitHub support commitment.
- Repository adoption facts are derived from tracked workflow files at
  `4122cecf`; no remote state was queried and no authenticated read-back was
  performed.
- No source listed here is adopted policy.

## Sources

- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - permissions keys, scope list, concurrency, `queue`
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) - SHA pinning, untrusted input, cache and runner hazards
- [Security hardening guide](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) - intermediate environment variable mitigation, secret handling
- [Automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) - least-privilege posture statement
- [Actions settings for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) - permissive and restricted defaults, action allowlisting
- [OIDC concepts](https://docs.github.com/en/actions/concepts/security/openid-connect) - single-job token lifetime
- [OIDC reference](https://docs.github.com/en/actions/reference/security/oidc) - issuer, claims, subject formats
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) - `workflow_call`, `secrets: inherit`, nesting depth, permission flow
- [Reusable workflows concepts](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusable-workflows) - reusable workflow versus composite action comparison
- [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) - `pull_request_target` context and warning
- [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) - pwn-request patterns and the data-not-code rule
- [Security Lab: untrusted input](https://securitylab.github.com/resources/github-actions-untrusted-input/) - substitution mechanism and attacker-controlled fields
- [Security Lab: new patterns](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/) - `workflow_run`, artifact poisoning, `permissions: {}` caveat
- [actions/checkout](https://github.com/actions/checkout) - default refusal of unsafe fork checkout and the `allow-unsafe-pr-checkout` opt-out
- [Safer pull_request_target defaults for actions/checkout](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/) - the flag naming rationale and the backport to every supported major version
- [Artifact attestations concepts](https://docs.github.com/en/actions/concepts/security/artifact-attestations) - SLSA build levels, Sigstore trust roots
- [Use artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) - required permission set
- [Immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases) - tag locking and resurrection protection
- [Dependabot for actions](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot) - `github-actions` ecosystem configuration
- [Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) - key resolution, branch isolation, poisoning framing
- [Read-only cache for untrusted triggers](https://github.blog/changelog/2026-06-26-read-only-actions-cache-for-untrusted-triggers/) - 2026-06-26 platform behavior change
- [Run job variations](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations) - matrix `include`/`exclude` order, `max-parallel`
- [Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) - reviewers, wait timers, deployment policies
- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) - aggregation, visibility, push rulesets
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) - required status checks and strict mode
- [Repository rules REST API](https://docs.github.com/en/rest/repos/rules) - authenticated read-back endpoints
- [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) - runner classes and public-repository availability
- [Actions Runner Controller](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller) - operator model and constraints
- [Manage runner access](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access) - runner group defaults
- [Actions limits](https://docs.github.com/en/actions/reference/limits) - run, job, queue, matrix, re-run, and API-rate limits; six further limits in the table below it are cited to their own pages
- [zizmor audits](https://docs.zizmor.sh/audits/) - third-party audit rule catalog
- [actionlint](https://github.com/rhysd/actionlint) - third-party workflow linter check classes
- [Tracked workflows](../../../../.github/workflows/ci-quality.yml) - repository adoption evidence entry point
- [Typed workflow contract](../../../../.github/workflow-contract.yml) - registry that factors gate definitions

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when GitHub Actions guidance, action major versions, or tracked workflow adoption changes
- **Update Trigger**: Re-retrieve every cited page and re-query action versions through the REST API; do not carry a version claim forward from a rendered page

## Related Documents

- `research pack index` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `README` leaf)
- `automation, pipeline, and workflow` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `automation-pipeline-workflow` leaf)
- `quality, CI, CD, QA, and formatting` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `quality-ci-formatting` leaf)
- `security governance` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `security-governance` leaf)
- `verification and validation` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `verification-validation` leaf)
- [GitHub governance](../../../00.agent-governance/policies/github-governance.md)

## Question

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Method

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Findings

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Implications

This package preserves its existing research evidence under the Stage 99 `research` contract.

## Traceability

This package preserves its existing research evidence under the Stage 99 `research` contract.
