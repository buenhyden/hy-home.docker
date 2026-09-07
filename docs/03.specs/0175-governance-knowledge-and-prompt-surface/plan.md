---
title: "Governance Knowledge and Prompt Surface Implementation Plan"
version: "0.10.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0175-PLAN-0001"
parent_ids:
- "SPEC-0175"
created: "2026-09-06"
---

# Governance Knowledge and Prompt Surface Implementation Plan

## Objective

Register `.agents/knowledge/` and `.agents/prompts/` as canonical categories,
author their members, use them inside this package's own execution, and close
the five defects SPEC-0175 names. Deliver each work unit as a separately
reviewable logical commit so a reviewer can accept one and reject its neighbor.

Authorization covers local work on `codex/0173-agent-governance-home`, local
commits, integration into the local `main` branch, and retirement of the work
branch and its worktree. It does not cover push, pull request, deployment, live
service action, credential values, global installation, or remote state. A
registered hook blocks pushing to `main`; that block is respected rather than
routed around, so `origin/main` is unchanged by this work.

## Dependencies

- Baseline: `codex/0173-agent-governance-home` at
  `9ede309a5b1feba91e6f8b973a729716b14c55ab`, clean worktree.
- Durable owners: REQ-0024 (amended with REQ-0024-FR-0014), AD-0027 (amended),
  and proposed ADR-0034.
- Concurrent package: SPEC-0173 stays active and unmodified. No file inside
  `docs/03.specs/0173-governance-qa-surface-convergence/` is touched.
- Shared branch: SPEC-0173's Plan claims this work branch and has open Tasks on
  it, and this package's commits sit on top of that package's commits. A branch
  cut from the integration baseline would drop them, and rewriting them is not
  authorized, so the branch is shared deliberately. Integrating it integrates
  both packages; the integration decision and the review therefore cover both.
- Executable owners keep their current responsibilities:
  `.github/workflow-contract.yml` owns executable composition,
  `scripts/manifest.yaml` owns file inventory, `docs/99.templates/registry.json`
  owns document shape, and `scripts/lib/agent_governance/` owns the canonical
  contract.
- Tools verified present locally: `python3` 3.12.3, `pre-commit`, `shfmt`,
  `shellcheck`, `yamllint`, `markdownlint-cli2`, `ruff`, `jq`, `gh`, `graphify`,
  `claude` 2.1.263, `codex` 0.153.4.

### Current interface boundary

Public validation entrypoints are unchanged:

- `python3 scripts/validation/run-ci-gate.py --profile changed`
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
- `python3 scripts/validation/run-ci-gate.py --profile full`

Provider projection remains the separate direct interface
`python3 scripts/operations/provider_surface_renderer.py --check|--write`.
`scripts/validation/run-agent-precommit-all-files.sh` stays NOT_RUN; its owned
execution may install hook environments and invoke container-bound linters.

## Execution Sequence

Each work unit ends with focused verification and one logical commit.

State per unit, so a resuming session reads progress instead of inferring it
from the Commit Ledger. A unit is `done` only when its commit exists and its
evidence is in the Task. The list is numbered because the completion contract
reads its work units from this section by number, not from the unit headings
below.

1. W1: Decision and durable owners — done
2. W2: Package creation — done
3. W3: RED evidence — done, as a method the later units apply
4. W4: Stage 99 registration — done
5. W5: Contract implementation — done
6. W6: Prompt members — done
7. W7: Knowledge members — done
8. W8: Language authority repair — done
9. W9: Gate selector alignment — done
10. W10: External re-observation — done
11. W11: Generated artifact refresh — done for the LLM Wiki; the graph rebuild is BLOCKED by the tool's own refusal
12. W12: Evidence, review, disposition — done
13. W13: Integration and branch retirement — done, and repeated per branch since
14. W14: Entry-path routing — done
15. W15: Remote advance and lifecycle promotion — done; the Spec reached `approved`, ADR-0034 `accepted`, and the walk this unit opened closed at W18
16. W16: Durable position and the remaining walk — done; the position substitution, both document audits, and the walk all completed, the last of them at W18
17. W17: Acceptance contract completeness — done; criterion 16 requires the entry path to name both categories, which no earlier criterion did
18. W18: Lifecycle promotion and `dev` integration — done; the remote reached the package HEAD, so all three transitions landed in one commit, and `dev` receives the work alongside `main`

### W1: Decision and durable owners

Record the canonical-category decision and amend the durable owners.
Create ADR-0034 with `AD-0027` as its single Architecture Description parent,
add `REQ-0024-FR-0014`, extend AD-0027's System Boundaries and Components,
allocate `ADR-0034` and `REQ-0024-FR-0014` in the Stage 99 identity spaces, and
register `ADR-0034` in the decisions index and in the test file's ADR-to-AD map.

W1 wrote no forward link to SPEC-0175, because link validation fails on a target
that does not exist yet; the link landed in W2 with the package it points at.

Verify: `check-document-metadata.py`, `check-document-links.py --mode all`,
`check-document-corpus-lifecycle.py`,
`check-agent-governance-contract.py --mode repository`, the taxonomy test
module, `git diff --check`, and the changed public profile.

### W2: Package creation

`check-document-metadata.py --mode check-changed` runs in the public gate with
`enforce_initial_status` on, and a document's previous status is read from the
merge base with `origin/main`. That merge base is fixed at
`8176cdee732954415bc5462d6d4d43da4e319394` for this branch, so every member of a
package created here stays new for as long as the branch lives and can never
record an observed transition, no matter how the commits are split. SPEC-0173
reaches `active` only because it already existed at that merge base.
`--transition-override-file` would carry named approval evidence, but
`scripts/lib/gate/ci_gate_contract.py` does not pass the flag, so the gate never
reads an override.

This work unit is therefore one commit.

- **W2a**: create `docs/03.specs/0175-governance-knowledge-and-prompt-surface/`
  with `spec.md`, `plan.md`, and
  `tasks/tsk-0001-knowledge-and-prompt-surface.md`, each at its initial status
  (`draft`). Allocate `SPEC-0175` in the Stage 99 spec identity space, add the
  package row to the Stage 03 index, and add ADR-0034's implementation link now
  that its target exists.

The package was created at `draft` and stayed there while its own commits were
the only ones between it and the merge base. That condition ended once the
package reached `origin/main`; W15 and W16 record the transitions taken since,
and the rule that governs them is stated there rather than here. What this unit
still owns is the reason it did not simply write `active` in frontmatter: a
status is a claim about Git history, and asserting one the history does not show
is the failure the rule exists to prevent.

Verify per commit: metadata in `check-changed` mode, links, corpus lifecycle,
`git diff --check`.

### W3: RED evidence before each implementation

Three assertions describe the target state:

- the canonical root inventory equals
  `("README.md", "governance", "knowledge", "prompts", "roles", "skills")`;
- the Stage 99 registry contains the four new profile ids, each mapped to the
  `living` lifecycle with a `template_roles` entry;
- the pre-commit public-gate `files` selector admits a representative path for
  every prefix in the workflow contract's `changed_path_rules`.

Write each assertion and run its logic against the state stored at `HEAD` and
against the working tree, recording both outputs verbatim in the Task before the
change it guards is committed. Comparing the two is what makes the failure real:
an assertion that has only ever passed proves nothing about what it catches.

The RED state is not committed. This repository's pre-commit stage runs the
changed public profile, which runs these suites, so a commit carrying failing
tests is rejected by the gate. Bypassing that gate is prohibited by
`hookify.block-git-no-verify.md` and by the standing authorization. The Task's
`Work Log` therefore owns the RED evidence, which is the ledger's declared
purpose.

Each assertion then ships in the commit that satisfies it, so every commit is
independently reviewable and independently green: the profile assertion with W4,
the root-inventory assertion with W5, and the selector assertion with W9.

### W4: Stage 99 registration

Add the `governance-knowledge`, `governance-knowledge-index`,
`governance-prompt`, and `governance-prompt-index` profiles, their
`template_roles` and `transitions` entries, the two copyable templates under
`docs/99.templates/templates/governance/`, and the template catalog rows.
`scripts/manifest.yaml` owns only `scripts/` and `evals/`, so a template needs
no entry there.

The index profiles exist because the registry's `{slug}` token renders as
`[a-z0-9][a-z0-9-]*` and cannot match `README.md`.

Verify: the profile-registration assertion turns GREEN; the registry
round-trips byte-identically under
`json.dumps(..., indent=2, ensure_ascii=False)` plus a trailing newline;
metadata, links, corpus lifecycle, and script manifest checks pass.

### W5: Contract implementation

Extend `ROOT_ENTRIES` and `GOVERNANCE_PROFILES` in
`scripts/lib/agent_governance/agent_governance_contract.py`, then create the two
directories with their index READMEs so the pinned inventory is satisfiable.
Update `.agents/README.md` scope, structure, and the sentence that currently
forbids any additional canonical surface. Update the Gap-to-Stage routing table
in `.agents/governance/documentation-protocol.md` and the Document Type Families
table in `.agents/governance/stage-authoring-matrix.md`. Add every new file to
`canonical_sources` in the Provider Registry.

Verify: the root-inventory assertion turns GREEN,
`check-agent-governance-contract.py --mode repository` passes, and
`provider_surface_renderer.py --check` reports zero drift with
`generated_roots` unchanged.

### W6: Prompt members

Author `handoff.md`, `diff-review.md`, `commit-message.md`, and `test-design.md`
under `.agents/prompts/`. Each declares purpose, required inputs, output
contract, prohibitions, failure handling, and applicability, and links the
owning skill instead of restating its procedure.

From this unit onward, use these prompts for the package's own remaining work
and record each use in the Task.

Verify: metadata, links, agent governance contract, renderer check.

### W7: Knowledge members

Author `repository-map.md`, `glossary.md`, and `verification-surface-map.md`
under `.agents/knowledge/`. Each declares an observation date and refresh
trigger, routes to a canonical owner, and states no obligation.

Verify: metadata, links, agent governance contract, renderer check.

### W8: Language authority repair and Claude output style

Repair the authority inversion before reducing the adapter, in this order.

1. State the conversational-language rule in
   `.agents/governance/output-style.md`, which `standards.md` already routes to
   but which does not currently contain it. Add the reporting and procedure
   shape rules the adapter currently owns.
2. Replace the artifact-language paragraph in
   `.agents/governance/documentation-protocol.md` with a measured statement:
   English-only for `.agents/**`, the authored native provider documents, and
   Stage 99 sources; audience language elsewhere as the profile permits. Record
   the observed per-stage practice as an observation, not an obligation. The
   adapter's current claim that Stage 03 and Stage 90 are Korean is contradicted
   by the tracked corpus and is not promoted.
3. Set `keep-coding-instructions: true` in `.claude/output-styles/hy-home.md`
   and reduce it to routes plus genuinely Claude-specific rendering.

The output-style change takes effect at the next provider session. Record that
boundary; do not claim observed runtime behavior.

Verify: agent governance contract, renderer check, metadata, links.

### W9: Gate selector alignment and intake owner

Align the `.pre-commit-config.yaml` public-gate `files` selectors with the
workflow contract's `changed_path_rules` prefixes so the selector assertion
turns GREEN, and record the exact prefixes added. Restore one current canonical owner
for the external capability-intake decision boundary.

Verify: the selector test passes, `check-github-workflow-contract.py` passes,
and the changed public profile still selects the expected suites.

### W10: External re-observation

Add the 2026-09-06 dated observation of the external agent catalog's upstream
head to `RES-0002-m0003`, beside its earlier observations. Preserve every
earlier dated measurement verbatim.

Verify: metadata, links, corpus lifecycle, reference protection tests.

### W11: Generated artifact refresh

Regenerate the LLM Wiki outputs if documents were added, removed, or renamed
under indexed scopes, and refresh `graphify-out/` with `graphify update .`.
Commit each generated result as its own unit, separate from source changes, to
avoid the pre-commit intermediate-stash race the quality standards describe.

Verify: `generate-llm-wiki.py --check` reports fresh outputs.

### W12: Evidence, review, and disposition

Record actual commands, exit codes, path sets, review findings, and blockers in
the Task. Run the changed public profile on the final path set. Obtain an
independent exact-diff review using the `diff-review` prompt. Transition
ADR-0034 from `proposed` to `accepted` only after the contract, registry, and
suite evidence is recorded.

ADR-0034 stays at `proposed` on this branch. The same rule that pins the Spec
Package at `draft` pins it: the metadata check reads previous status from the
`origin/main` merge base, and the decision is new relative to that base, so
`accepted` is rejected as `invalid-initial-status`. This was attempted and
measured rather than assumed. Its promotion travels with the package's, on the
first branch after integration.

Deferred items are listed with their reason, not silently dropped.

### W13: Integration and branch retirement

Integration is authorized, so the branch closes rather than being preserved.

1. Verify the working tree is clean and the changed public profile passes on the
   final path set.
2. Fast-forward the local `main` branch onto the work branch. A merge commit is
   avoided where the history already allows a fast-forward, so the reviewed
   commits reach `main` unchanged.
3. Prove `main` contains every commit of this package before retiring anything,
   by comparing the two revisions rather than trusting the merge's exit code.
4. Delete the work branch only after that proof, and remove the worktree only if
   one was created for this work. A single primary worktree is in use here, so
   nothing is removed.
5. Leave `origin/main` untouched. Pushing to `main` is blocked by a registered
   hook, so integration stops at the local branch and every statement about the
   remote stays unverified.

The lifecycle constraint is unchanged by this: `resolve_base_selection` reaches
`origin/main` before `main`, so a local merge does not make the package's
`draft` statuses transitionable. Promotion still waits for the remote branch to
advance.

### W14: Entry-path routing

The two categories were registered, enforced and indexed, but no entry path
named them, so an agent following the canonical load order would never open
either. Route `bootstrap.md` step 3 and both authored provider adapters to them,
and add both to the English-only constraint.

Verify: metadata, links, agent governance contract, renderer parity, and the
changed public profile.

### W15: Remote advance and lifecycle promotion

`origin/main` advanced outside this Task's authorization. Record the observation
with its evidence, correct the acceptance criterion that assumed it had not, and
then walk the lifecycle that the advance makes observable: ADR-0034 to
`accepted`, and the Spec, Plan and Task through their own transitions, at most
one per document per commit.

Exactly one transition per document per branch is provable, not one per commit.
`previous_status` is read from the merge base, so a document already advanced in
the working tree is still compared against the status it had at that base.
Advancing the Spec twice on one branch returns
`invalid-transition: lifecycle transition requires explicit override:
draft -> approved`. The remaining transitions belong to the branch taken after
this one is integrated, one per branch. The Plan advances here only because its
lifecycle defines `draft` to `approved` as a single step, so that is its first
transition rather than its second.

Verify: metadata in `check-changed` mode is the gate that proves each
transition; a rejected transition is recorded, never overridden.

### W16: Durable position and the remaining walk

Two rehearsals found the same class of defect: a point-in-time Git value written
into prose is false within hours. Replace each remaining value with the query
that answers it, in the file that owns the claim. Add the ledger rows and the
verification evidence each preceding unit owed, and take whatever lifecycle
transition the current merge base admits.

Resume condition, stated once so a later session does not have to infer it: this
package is complete when the Spec reaches `active`, the Plan `active`, and the
Task `in-progress`, which the package integrity rules allow only in that order
and at one transition per document per branch. Until then the next action is
always the same: integrate, let the remote advance, cut a branch, take the one
transition the base now admits, and record it.

Verify: metadata in `check-changed` mode, links, the agent governance contract,
renderer parity, and the changed public profile.

### W17: Acceptance contract completeness

The contract required the categories to exist, be registered, be enforced and be
indexed, and required nothing about a reader reaching them. Add the criterion
that closes that, and declare the entry-path surfaces the package already
changed. Append rather than insert, so the existing criteria keep their numbers
and the Task's mapping rows stay aligned.

Verify: metadata, links, the agent governance contract, and the changed public
profile; and measure the new criterion from the files rather than asserting it.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| A new category becomes a second authority | Registered required sections plus independent review; a stated obligation routes back to `governance/` | Revert the offending member file |
| Contract and registry half-land | The contract reads the profile set with `issubset`, so the registry leads and the contract follows; each commit carries the assertion it satisfies | Revert W5, then W4; the recorded RED run remains the evidence |
| Registry edit reformats the whole file | Confirm byte-identical JSON round-trip before and after each edit | Revert the registry hunk |
| Prose naming a retired path trips the token guard | Describe the retired surface without spelling its path | Rephrase; never weaken the pattern |
| Forward link to a not-yet-created target | The link lands in the commit that creates its target | Remove the link and re-add it in the correct unit |
| A parallel plan system appears outside Stage 03 | No `docs/superpowers` tree is created; this Spec, Plan, and Task are the only plan authority | Delete the stray tree and restate the content in its registered owner |
| Selector widening runs the gate on more commits | Compare selectors as sets and record the exact added prefixes | Revert W9 |
| Output-style change is claimed as observed runtime | Record it as configured, effective next session | Revert W8 |
| Concurrent edits collide with SPEC-0173 | No file under that package is touched | None required |
| A long gate run is interrupted mid-suite | Run it detached and confirm the process exited before reading the verdict | Re-run on the same path set |

## Verification

The Task owns every actual command, working directory, selected input, exit
code, scope, review finding, and PASS/FAIL/BLOCKED/NOT_RUN/N/A state. This Plan
owns order and resume conditions only and makes no execution claim.

Per work unit, run the focused validators mapped to the changed authority
surface through the
[shared verification matrix](../../../.agents/governance/quality-standards.md#5-change-type-verification-matrix).
Run the changed public profile at W1, W5, W9, and W12 at minimum, and on the
final path set before completion.

These remain outside this Plan and are never inferred from a local result:
Hosted CI, remote branch protection, provider entitlement, native runtime
discovery and invocation, the controlled all-files wrapper, and any cost
measurement. Record each as NOT_RUN or unverified with its missing input.

### W18: Lifecycle promotion and `dev` integration

Two conditions changed at once. `origin/main` advanced to the package HEAD from
outside this Plan, making the merge base equal to HEAD, and the current request
named `dev` as an integration target.

Because the base equals HEAD, every package document sits exactly one lifecycle
edge from its own base status, so the Spec's `approved` to `active`, the Plan's
`approved` to `active`, and the Task's `ready` to `in-progress` are all provable
in a single commit. The package integrity rules are satisfied by the end state
rather than by an ordering across commits: an `active` Plan and an
`in-progress` Task each require an `active` Spec, and all three are active
together. Measure this before committing it, and record the measured base with
the reported `merge_base` rather than assuming which ref was selected.

The earlier conclusion that each transition needs its own later branch is
withdrawn by this measurement. A branch was never the operative condition; the
base is, and `resolve_base_selection` reaches the same base from any local
branch cut off the same remote ref.

Integration then closes the branch:

1. Verify the working tree is clean and the changed public profile passes on the
   final path set.
2. Create a local `dev` from `origin/dev` and fast-forward it onto the work
   branch. `origin/dev` carries no commit that `main` lacks, so this is a
   fast-forward and no merge commit is created.
3. Fast-forward `main` onto the same commit, so the two targets name one
   reviewed history rather than diverging.
4. Prove each target contains every commit of this package before retiring
   anything, by comparing revisions rather than trusting a merge's exit code.
5. Delete the work branch only after that proof.
6. Leave `origin/dev` and `origin/main` untouched. Publishing either is a push,
   which no grant in this package covers, so integration stops at the local
   refs and every statement about the remote stays unverified.

## Rulings

- SPEC-0173 is not modified. Its open retention-owner design dependency stays
  with that package.
- No new policy, role, skill, provider, model row, permission profile, hook
  binding, public suite, or public profile is introduced.
- A knowledge or prompt member never owns execution state, an obligation, or a
  procedure body.
- Generated outputs are regenerated by their registered generator and committed
  as separate logical units; none is hand-edited to pass a check.
- Deferred work is recorded with its blocking input, never marked complete.

## Related Documents

- [Specification](spec.md)
- [Task evidence](tasks/tsk-0001-knowledge-and-prompt-surface.md)
- [Stage 03 index](../README.md)
