---
title: "Requirement Pair Conflict Check Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0030"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Requirement Pair Conflict Check Task

## Overview

### Objective

Execute W46: judge every pair of the request's 148 numbered requirements
(CR-01.01 to CR-21.05), 10,878 pairs, for duplication and conflict
(CR-04.04). This Task owns criterion 41 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for the pairwise conflict check that TSK-0026
recorded as not performed, followed by commit, pull request, and merge. The
owner chose this compact record: the Task lists every pair not judged a
different responsibility, with its reason, and any pair it does not list is
a different responsibility. The input is the owner's pasted request at
`main` merged PR #626. The authorization covers this record, this branch,
its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0030 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0030 | ready | in-progress | #objective |
| SPEC-0212-TSK-0030 | in-progress | completed | #evidence |

### Method

1. Two read-only reviewers recorded, for each CR, its tags from one fixed
   vocabulary, its writer, its polarity, and when it applies. That table is
   below and supplies the `writer_owner`, `scope`, `polarity`, and
   `temporal_condition` fields of every pair.
2. Ten read-only reviewers split the pairs by first member, about 1,100 each.
   A script listed each reviewer's pairs from the request order so none could
   be skipped. The reviewer read both full texts of every pair and chose one
   relation. No relation was set by keyword rule.
3. The lead review merged the ten outputs and checked that the 10,878 pairs
   each appear exactly once, with no extra or missing pair.

| Code | Relation in the request's terms | Outcome |
| --- | --- | --- |
| `DIFF` | Different responsibility | Keep |
| `COMP` | Complementary purpose | Keep |
| `COND` | Compatible by condition or scope | Keep; the reason names the condition |
| `DERIV` | Controlled derivation or reference | Keep |
| `SAME` | Same meaning, same owner | Merge or reference in the request |
| `DUPW` | Same duty, two writers | One canonical writer in the request |
| `CONTRA` | Real contradiction | `BLOCKED` until the owner decides |
| `UNVER` | Cannot be judged | Stays open |

### Result

| Relation | Pairs |
| --- | --- |
| `DIFF` | 9,929 |
| `COMP` | 750 |
| `DERIV` | 112 |
| `COND` | 50 |
| `DUPW` | 22 |
| `SAME` | 15 |
| `CONTRA` | 0 |
| `UNVER` | 0 |

No pair is a real contradiction and none is left unjudged, so no execution
is blocked by this check. The 37 `SAME` and `DUPW` pairs are duplication
inside the request text itself: the same duty is written in two CRs. They
are recorded for the owner's next revision of the request. They need no
repository change, because each duty is already met, or recorded as open,
once in TSK-0029. The required cross-area combinations — document versus
Task status, archive versus memory retention, Git and CI versus remote
approval, shared governance versus local adapter, completed work versus new
orders, native agent versus shared memory, SDLC versus SDD, bulk QA removal
versus unique guarantee — were each judged, and none is `CONTRA` or
`UNVER`.

### Limits

- This is a static check of the requirement texts. Whether the current
  implementation conflicts with them is judged per line in TSK-0029, not per
  pair.
- The reviewers were model agents. Judgements near the `COMP` and `DUPW`
  boundary are reviewer choices. Three of them are flagged:
  - CR-05.12 against six CRs is recorded as `COND`; a stricter reading makes
    them `DUPW`.
  - CR-01.07 with CR-05.02 is recorded as `COMP`.
  - CR-06.06 with CR-07.03 is recorded as `COMP`.
- The full per-pair file, including the `DIFF` reasons, stays outside the
  repository by the owner's choice.

### Requirement attributes

| CR | Tags | Writer | Polarity | Temporal |
| --- | --- | --- | --- | --- |
| CR-01.01 | input-trace,evidence-acceptance | Task | must,must-not | always |
| CR-01.02 | input-trace,conflict-ownership,evidence-acceptance | Task | must,must-not,condition | before start |
| CR-01.03 | baseline-git,task-contract,evidence-acceptance | Task | must,must-not,condition | before start |
| CR-01.04 | baseline-git | Task | must,must-not | before start |
| CR-01.05 | baseline-git,evidence-acceptance | Task | must,condition | during change |
| CR-01.06 | evidence-acceptance,baseline-git | Task | must,must-not | always |
| CR-01.07 | input-trace,baseline-git | Task | must,must-not,condition | before start |
| CR-01.08 | external-research,input-trace,reporting-state | Task | must,must-not | during change |
| CR-01.09 | reporting-state,evidence-acceptance | Task | must,must-not,condition | always |
| CR-02.01 | external-research | Task | must,must-not | before start |
| CR-02.02 | external-research,evidence-acceptance | Task | must,must-not | before start |
| CR-02.03 | external-research,approval-security | Task | must,must-not,exception | before start |
| CR-02.04 | external-research | Task | must,must-not | before start |
| CR-02.05 | external-research,evidence-acceptance | Task | must,must-not | before start |
| CR-02.06 | external-research,common-norms-adoption | Task | must,must-not | before start |
| CR-02.07 | external-research,evidence-acceptance | Task | must,must-not | during change |
| CR-02.08 | external-research,approval-security | Task | must,must-not | before start |
| CR-03.01 | common-norms-adoption,conflict-ownership | .agents/governance | must,must-not | always |
| CR-03.02 | common-norms-adoption,approval-security | owner approval | must,must-not | before start |
| CR-03.03 | common-norms-adoption,readme-language-links | .agents/governance | must,may,must-not | always |
| CR-03.04 | common-norms-adoption,approval-security | owner approval | must,may,condition | before start |
| CR-03.05 | common-norms-adoption,evidence-acceptance | owner approval | must,must-not | at completion |
| CR-03.06 | common-norms-adoption,archive | .agents/governance | must,must-not,condition | after merge |
| CR-03.07 | common-norms-adoption,quality-iso | .agents/governance | must,must-not | during change |
| CR-04.01 | conflict-ownership | .agents/governance | must | before start |
| CR-04.02 | conflict-ownership,archive,oneoff-qa-removal | .agents/governance | must,must-not,condition | during change |
| CR-04.03 | conflict-ownership,agent-instructions | .agents/governance | must,must-not,may | during change |
| CR-04.04 | conflict-ownership,evidence-acceptance | .agents/governance | must,must-not,condition | before start |
| CR-04.05 | conflict-ownership,cost-loop-token | .agents/governance | must,must-not | always |
| CR-05.01 | templates | Stage 99 registry/templates | must,must-not | before start |
| CR-05.02 | templates,qa-graph | Stage 99 registry/templates | must | before start |
| CR-05.03 | templates | Stage 99 registry/templates | must,must-not,condition | during change |
| CR-05.04 | doc-lifecycle,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-05.05 | templates | Stage 99 registry/templates | must,must-not | during change |
| CR-05.06 | templates,req-arch-docs | Stage 99 registry/templates | must,must-not | during change |
| CR-05.07 | templates,qa-graph | Stage 99 registry/templates | must,must-not | during change |
| CR-05.08 | templates,req-arch-docs | Stage 99 registry/templates | must,must-not,condition,exception | before start |
| CR-05.09 | templates,archive | Stage 99 registry/templates | must,must-not | during change |
| CR-05.10 | templates | Stage 99 registry/templates | must,must-not,condition | during change |
| CR-05.11 | templates,evidence-acceptance | Stage 99 registry/templates | must,must-not | at completion |
| CR-05.12 | templates,external-research | Stage 99 registry/templates | must,must-not | during change |
| CR-05.13 | doc-lifecycle,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-06.01 | task-contract,req-arch-docs | .agents/governance | must,must-not | always |
| CR-06.02 | task-contract,reporting-state | Task | must,must-not | during change |
| CR-06.03 | task-contract,doc-lifecycle | Task | must,must-not | during change |
| CR-06.04 | evidence-acceptance,task-contract | Task | must,must-not | during change |
| CR-06.05 | task-contract,reporting-state | Task | must,must-not | during change |
| CR-06.06 | evidence-acceptance | owner approval | must,must-not | at completion |
| CR-06.07 | task-contract,external-research,templates | Task | must,must-not | during change |
| CR-06.08 | task-contract,skills-harness | .agents/governance | must,must-not | during change |
| CR-06.09 | task-contract,req-arch-docs,quality-iso | .agents/governance | must,must-not | during change |
| CR-06.10 | task-contract,evidence-acceptance | .agents/governance | must,must-not | during change |
| CR-07.01 | readme-language-links | .agents/governance | must,must-not | always |
| CR-07.02 | readme-language-links | .agents/governance | must,must-not,exception | always |
| CR-07.03 | readme-language-links,agent-instructions | .agents/governance | must,must-not | always |
| CR-07.04 | readme-language-links,templates | .agents/governance | must,must-not,may | always |
| CR-07.05 | readme-language-links | .agents/governance | must | during change |
| CR-07.06 | readme-language-links | .agents/governance | must,must-not | during change |
| CR-07.07 | readme-language-links,external-research,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-08.01 | archive,common-norms-adoption | Stage 98 archive | must | before start |
| CR-08.02 | archive | Stage 98 archive | must,must-not | before start |
| CR-08.03 | archive | Stage 98 archive | must,must-not,condition | on archive |
| CR-08.04 | archive | Stage 98 archive | must,must-not | on archive |
| CR-08.05 | archive,req-arch-docs | Stage 98 archive | must,must-not | on archive |
| CR-08.06 | archive,task-contract | Task | must,must-not | on archive |
| CR-08.07 | archive,doc-lifecycle | Stage 98 archive | must,must-not,condition | on archive |
| CR-09.01 | req-arch-docs | .agents/governance | must,must-not | during change |
| CR-09.02 | req-arch-docs,quality-iso | .agents/governance | must | during change |
| CR-09.03 | req-arch-docs,evidence-acceptance | .agents/governance | must | during change |
| CR-09.04 | req-arch-docs,reporting-state | Task | must,must-not,condition | during change |
| CR-09.05 | req-arch-docs,external-research | .agents/governance | must,must-not | during change |
| CR-09.06 | req-arch-docs,external-research,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-09.07 | req-arch-docs,external-research,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-10.01 | qa-graph,ci-location | CI workflow contract | must,must-not | before start |
| CR-10.02 | qa-graph | CI workflow contract | must | always |
| CR-10.03 | qa-graph | CI workflow contract | must,must-not | always |
| CR-10.04 | qa-graph | CI workflow contract | must,must-not | during change |
| CR-10.05 | qa-graph,ci-location | CI workflow contract | must | always |
| CR-10.06 | qa-graph,cost-loop-token | CI workflow contract | must,must-not | always |
| CR-10.07 | qa-graph,evidence-acceptance | CI workflow contract | must,must-not,condition | at completion |
| CR-10.08 | qa-graph,doc-lifecycle,archive | CI workflow contract | must,must-not | during change |
| CR-11.01 | oneoff-qa-removal,qa-graph | .agents/governance | must,condition | during change |
| CR-11.02 | oneoff-qa-removal,qa-graph,evidence-acceptance | .agents/governance | must,must-not,condition | after task closure |
| CR-11.03 | oneoff-qa-removal,qa-graph | .agents/governance | must,condition | during change |
| CR-11.04 | cost-loop-token,qa-graph | .agents/governance | must,must-not | during change |
| CR-11.05 | oneoff-qa-removal,evidence-acceptance | Task | must,must-not | at completion |
| CR-12.01 | ci-location,conflict-ownership | CI workflow contract | must,must-not | before start |
| CR-12.02 | ci-location,approval-security,baseline-git | CI workflow contract | must,must-not | before start |
| CR-12.03 | ci-location,evidence-acceptance | CI workflow contract | must,must-not | at completion |
| CR-12.04 | approval-security,ci-location | CI workflow contract | must,condition | during change |
| CR-12.05 | ci-location,evidence-acceptance | CI workflow contract | must,must-not,condition | at completion |
| CR-13.01 | git-commit-release,worktree | .agents/governance | must,must-not | during change |
| CR-13.02 | git-commit-release | .agents/governance | must,must-not | during change |
| CR-13.03 | git-commit-release,approval-security | .agents/governance | must,condition | before start |
| CR-13.04 | git-commit-release,qa-graph | .agents/governance | must | during change |
| CR-13.05 | git-commit-release | CI workflow contract | must,must-not | after merge |
| CR-13.06 | git-commit-release,approval-security | CI workflow contract | condition,must | after merge |
| CR-13.07 | git-commit-release,external-research | .agents/governance | must,must-not | before start |
| CR-14.01 | issues-projects | .agents/governance | must,must-not | before start |
| CR-14.02 | issues-projects,reporting-state,task-contract | Task | must,must-not | always |
| CR-14.03 | issues-projects,reporting-state | Task | must,must-not | during change |
| CR-15.01 | agent-instructions,conflict-ownership | .agents/governance | must,must-not | always |
| CR-15.02 | agent-instructions,external-research | .agents/governance | must,must-not | before start |
| CR-15.03 | agent-instructions,skills-harness | Provider Registry | must,must-not | always |
| CR-15.04 | agent-instructions,approval-security | .agents/governance | must,must-not | before start |
| CR-15.05 | agent-instructions,skills-harness | .agents/governance | must,must-not | during change |
| CR-15.06 | agent-instructions,approval-security | .agents/governance | must,must-not,condition | before start |
| CR-15.07 | agent-instructions | .agents/governance | must,must-not,condition | during change |
| CR-15.08 | agent-instructions,approval-security | .agents/governance | must,must-not | before start |
| CR-15.09 | approval-security,agent-instructions | .agents/governance | must,must-not | always |
| CR-15.10 | skills-harness,agent-instructions | .agents/governance | must,condition,must-not | during change |
| CR-15.11 | approval-security,shared-memory,workspace-dirs | .agents/governance | must,must-not | always |
| CR-15.12 | skills-harness,agent-instructions,external-research | .agents/governance | must,must-not | during change |
| CR-15.13 | skills-harness,agent-instructions,approval-security | .agents/governance | must,must-not | during change |
| CR-15.14 | skills-harness,reporting-state,cost-loop-token | .agents/governance | must,must-not | during change |
| CR-16.01 | skills-harness | Task | must,must-not | before start |
| CR-16.02 | skills-harness,reporting-state | Task | must,must-not | during change |
| CR-16.03 | skills-harness,templates | .agents/governance | must | during change |
| CR-16.04 | skills-harness,agent-instructions | .agents/governance | must,must-not | during change |
| CR-17.01 | shared-memory | .agents shared memory store | must,must-not,condition | before start |
| CR-17.02 | shared-memory | .agents shared memory store | must,may | always |
| CR-17.03 | shared-memory | .agents shared memory store | must-not,must | always |
| CR-17.04 | shared-memory | .agents shared memory store | must | always |
| CR-17.05 | shared-memory,cost-loop-token | .agents shared memory store | must,must-not | always |
| CR-17.06 | shared-memory,worktree | .agents shared memory store | must,must-not | during change |
| CR-17.07 | shared-memory,external-research | .agents shared memory store | must,condition | before start |
| CR-17.08 | shared-memory,agent-instructions | .agents shared memory store | must,must-not | always |
| CR-17.09 | shared-memory,external-research | .agents shared memory store | must,must-not | during change |
| CR-17.10 | shared-memory,approval-security | .agents shared memory store | must,must-not | always |
| CR-17.11 | shared-memory,approval-security | .agents shared memory store | must,must-not | during change |
| CR-18.01 | cost-loop-token,task-contract | .agents/governance | must-not,must,exception | before start |
| CR-18.02 | cost-loop-token,reporting-state | .agents/governance | must,must-not | during change |
| CR-18.03 | cost-loop-token | .agents/governance | must,must-not | during change |
| CR-18.04 | cost-loop-token,external-research | .agents/governance | must,must-not | before start |
| CR-18.05 | cost-loop-token | .agents/governance | must,must-not | during change |
| CR-18.06 | cost-loop-token,evidence-acceptance,approval-security | Task | must,condition | at completion |
| CR-19.01 | workspace-dirs,readme-language-links | .agents/governance | must,must-not | during change |
| CR-19.02 | workspace-dirs,approval-security | .agents/governance | must,must-not | during change |
| CR-19.03 | evidence-acceptance,workspace-dirs,approval-security | Task | must,must-not | at completion |
| CR-19.04 | worktree,shared-memory | .agents/governance | must,must-not | during change |
| CR-20.01 | quality-iso,external-research | .agents/governance | must,must-not | before start |
| CR-20.02 | quality-iso,req-arch-docs | Requirements | must,must-not | during change |
| CR-20.03 | quality-iso,templates | Stage 99 registry/templates | must,must-not | during change |
| CR-21.01 | approval-security | .agents/governance | must-not,exception | always |
| CR-21.02 | approval-security,evidence-acceptance | owner approval | must,must-not | at completion |
| CR-21.03 | approval-security,conflict-ownership | .agents/governance | must,must-not | during change |
| CR-21.04 | approval-security | owner approval | must,must-not | always |
| CR-21.05 | approval-security,external-research | .agents/governance | must,must-not | always |

### Pairs other than different responsibility

Every pair not listed here is `DIFF`, with the fields from the attribute
table above.

| A | B | Relation | Justification |
| --- | --- | --- | --- |
| CR-01.01 | CR-01.02 | SAME | atom split with one primary_CR per atom and owner distinction stated in both (Task); 01.02 is the defining clause |
| CR-01.01 | CR-01.09 | SAME | unretrieved original/source neither halts nor expands/fills defined duties is stated in both (Task) |
| CR-01.03 | CR-01.09 | SAME | blocked unit stays BLOCKED only for its stage, independent work continues, not counted success; same Task atom |
| CR-02.02 | CR-02.08 | SAME | site citation record (URL/section/date/doc version) stated in both with Task owner; 02.08 adds git ref pinning |
| CR-02.03 | CR-02.06 | SAME | unretrieved source must not be closed as non-applicable; same duty, Task owner, 02.06 field-level |
| CR-03.06 | CR-03.07 | SAME | four-repo adoption counted only when all repos apply same approved revision; partial not complete, same CR-03 owner |
| CR-04.05 | CR-11.02 | SAME | removal of completed-task-only standing checks is one duty stated in 04.05 and 11.02, same governance owner |
| CR-05.06 | CR-05.11 | SAME | both forbid counting a template-only update as doc migration completion; same CR-05 owner |
| CR-06.08 | CR-06.10 | SAME | regenerate only future plan while keeping Task execution records, same owner twice |
| CR-10.01 | CR-10.02 | SAME | duplicate-check criterion (same input/guarantee/consumer) stated in both; merge or reference |
| CR-12.02 | CR-12.04 | SAME | 12.04 detail repeats 12.02 duty to compare protection/ruleset checks, App, bypass, access limits |
| CR-15.09 | CR-15.13 | SAME | instruction declaration does not grant access; verify real permission boundary, written in both |
| CR-15.12 | CR-15.13 | SAME | SRC-AGENT/agency-agents role mapping, native conversion, install.sh ban and tests written in both |
| CR-15.13 | CR-21.05 | SAME | external text never elevates privilege, with isolated prompt-injection negative tests, in both |
| CR-17.09 | CR-17.10 | SAME | wiki vs SQLite authority and decay/forget/auto-improve audit written twice for SRC-MEM |
| CR-01.03 | CR-05.08 | DUPW | no re-run of completed 0001 renumber is written in 01.03 (Task) and 05.08 (Stage99); one writer should own it |
| CR-01.03 | CR-08.03 | DUPW | no re-delete/regenerate of completed archive payload units written in 01.03 (Task) and 08.03 (Stage98) |
| CR-01.03 | CR-13.05 | DUPW | fix existing release producer instead of reinstall is written in 01.03 (Task) and 13.05 (CI contract) |
| CR-01.03 | CR-17.01 | DUPW | KEEP adequate memory DB without reinstall is written in 01.03 (Task) and 17.01 (memory store) |
| CR-01.05 | CR-10.07 | DUPW | narrow result reuse only with proven input equivalence is written in 01.05 (Task) and 10.07 (CI contract) |
| CR-02.08 | CR-21.05 | DUPW | external text commands are review data not execution authority, written in both 02.08 and 21.05 (canonical CR-21) |
| CR-03.03 | CR-07.02 | DUPW | user-set document language not relaxed by repo practice stated in both 03.03 and 07.02 (canonical CR-07.02) |
| CR-03.04 | CR-06.05 | DUPW | no future approvals/commits required before drafting/starting, written in 03.04 and 06.05 |
| CR-03.04 | CR-18.01 | DUPW | research/planning not required to have nonexistent commits/digests/approvals, also in 18.01 |
| CR-03.04 | CR-21.04 | DUPW | approval scopes for drafts/isolated changes vs norm activation and reuse of valid prior approval in both |
| CR-03.06 | CR-10.08 | DUPW | re-verify only changed contracts and consumers after initial four-repo adoption, written in 03.06 and 10.08 |
| CR-03.07 | CR-05.03 | DUPW | Required string/boolean types not batch-converted before reader/validator support proven, in both 03.07 and 05.03 |
| CR-06.04 | CR-17.03 | DUPW | memory-is-not-execution-evidence rule authored by both Evidence and memory owners |
| CR-06.05 | CR-06.08 | DUPW | realign current description after real implementation restated in Spec Kit clause by other writer |
| CR-06.05 | CR-18.01 | DUPW | ban on requiring not-yet-existing commit/digest/approval before start written twice |
| CR-06.06 | CR-08.07 | DUPW | unaccepted obligations transfer-or-stay-blocked rule written by acceptance and archive owners |
| CR-06.07 | CR-06.08 | DUPW | Spec Kit tasks generation must not overwrite completed Task: tested in both by different writers |
| CR-06.07 | CR-06.10 | DUPW | regenerate tasks without erasing finished Task records stated in both |
| CR-06.09 | CR-12.05 | DUPW | no forced deployment for doc-only changes stated by governance and CI owners |
| CR-07.04 | CR-07.07 | DUPW | direct current procedure + link background rule restated by Stage99 writer (07.07) vs governance (07.04) |
| CR-07.04 | CR-08.05 | DUPW | cite accessible historical source when current path deleted: written in governance 07.04 and archive 08.05 |
| CR-13.01 | CR-19.04 | DUPW | preserving uncommitted changes when creating a branch/worktree is authored in both CR-13 and CR-19 |
| CR-01.02 | CR-01.03 | COND | 01.02 bars retroactive closure of past pre-research but orders no rework; 01.03 keeps completed implementation |
| CR-01.03 | CR-01.08 | COND | 01.08 orders implementing differences but allows a KEEP report when nothing differs, matching 01.03 no-change |
| CR-01.03 | CR-05.05 | COND | 05.05 must edit templates where the norm differs; 01.03 KEEPs conforming ones; scoped to real differences |
| CR-01.08 | CR-03.06 | COND | four-repo adoption needs each repo to apply; 01.08 keeps other repos read-only, so adoption goes via handoff |
| CR-01.08 | CR-03.07 | COND | 03.07 routes other-repo changes through approval boundary and handoff, compatible with 01.08 read-only |
| CR-01.09 | CR-02.04 | COND | 01.09 optional-unverified status covers unverifiable shared conversations, not mandatory SRC sources |
| CR-02.07 | CR-08.03 | COND | 02.07 keeps existing preservation; 08.03 deletes payload only with recoverable history |
| CR-04.02 | CR-05.08 | COND | completed work not reimplemented: 05.08 renumbers only areas where the one-off conversion is not already done (KEEP) |
| CR-04.02 | CR-09.01 | COND | 09.01 orders adding area docs but KEEPs adequate ones, so it does not redo completed work |
| CR-05.03 | CR-06.02 | COND | field ownership: 06.02 sets execution-state fields inside Task, 05.03 sets document-family form; distinct scopes |
| CR-05.03 | CR-06.07 | COND | Spec/Plan/Task field lists in 06.07 explicitly defer to local schema keys, i.e. the 05.03 contract |
| CR-05.03 | CR-09.06 | COND | ADR fields in 09.06 are proposals adapted to the approved schema, not a single official frontmatter |
| CR-05.03 | CR-15.12 | COND | agent role form: 05.03 owns the Agent profile form, 15.12 owns role content and native conversion |
| CR-05.04 | CR-05.11 | COND | state axes: 05.11 obligation receipts use section 4 states, 05.04 doc lifecycle uses CR-05.13; kept separate |
| CR-05.04 | CR-06.02 | COND | doc status vs Task status: 06.02 Task owns execution state, 05.04 forbids merging it into doc lifecycle |
| CR-05.04 | CR-08.07 | COND | archive axis: 08.07 transition order is a process not a status field; 05.04 keeps archive separate from status |
| CR-05.04 | CR-09.06 | COND | ADR status: 09.06 accepted/rejected/superseded fits approved schema and CR-05.13 ADR row |
| CR-05.06 | CR-08.03 | COND | 05.06 lists Stage98 docs as template consumers; compatible because payload removal follows CR-08 and old evidence is preserved |
| CR-05.07 | CR-08.03 | COND | 05.07 keeps archive read rules; compatible since removed payload is read only from historical Git sources |
| CR-05.08 | CR-09.06 | COND | Nygard number non-reuse vs one-time 0001 conversion; reconciled by explicit one-time generation and lineage |
| CR-05.09 | CR-17.04 | COND | 05.09 updates current memory references; compatible as memory bodies are preserved and stale sources drop from recall |
| CR-05.11 | CR-06.02 | COND | 05.11 duty statuses use §4 ledger; compatible if recorded in the Task, the sole execution writer |
| CR-05.12 | CR-06.07 | COND | 05.12 maps adopted SDD forms into Stage99 fields only after 06.07 decides Spec/Plan/Task content |
| CR-05.12 | CR-07.07 | COND | 05.12 maps Diataxis form only once 07.07 adopts its local reader-mode fields |
| CR-05.12 | CR-09.06 | COND | ADR field set decided in 09.06; 05.12 only links it into Stage99 profile |
| CR-05.12 | CR-09.07 | COND | arc42 checks decided in 09.07; 05.12 only maps them to the architecture template |
| CR-05.12 | CR-15.12 | COND | agent role form decided in 15.12; 05.12 links it to Stage99 form only if adopted |
| CR-05.12 | CR-17.09 | COND | SRC-MEM memory form adoption decided in 17.09; 05.12 maps it only after adoption |
| CR-06.10 | CR-10.05 | COND | change-class checks: 06.10 sets artifacts/approval scope, 10.05 owns per-stage check matrix |
| CR-07.04 | CR-07.05 | COND | ops docs: 07.04 needs direct current procedure, 07.05 dedupes repeats; compatible since 07.04 bars whole-canon copies |
| CR-08.03 | CR-09.06 | COND | ADR non-reuse/preservation vs archive payload deletion; 09.06 reconciles via historical source and lineage |
| CR-10.01 | CR-10.06 | COND | 10.06 removes duplicates only after trust/input differences checked, as 10.01 requires |
| CR-10.06 | CR-11.01 | COND | check removal limited to purpose-less checks; required guarantees kept in both |
| CR-10.07 | CR-11.04 | COND | narrow result reuse allowed only with 10.07 equivalence proof |
| CR-11.04 | CR-12.03 | COND | result reuse allowed only when provably bound to the candidate; prior commit success never reused |
| CR-11.05 | CR-12.04 | COND | removal limited to caller=0/no-guarantee; purposeful security negative tests of 12.04 are kept |
| CR-12.01 | CR-13.07 | COND | 13.07 evaluation cannot by itself change the target branches 12.01 names |
| CR-12.01 | CR-21.04 | COND | 12.01 proposes needed runner/setting changes; applying remote changes needs 21.04 approval |
| CR-12.03 | CR-18.03 | COND | deterministic receipts reusable only when bound to same candidate; prior commit success excluded |
| CR-12.05 | CR-21.04 | COND | deployment run only with unique guarantee and approval scope; doc-only not forced |
| CR-13.01 | CR-21.04 | COND | commit/PR/merge proceed only within the approved remote push/PR/merge scope |
| CR-13.03 | CR-21.04 | COND | global personal Git config change only under separate approval scope |
| CR-13.04 | CR-15.05 | COND | 15.05 tests native hook events; Git hook propagation owned by 13.04 |
| CR-13.05 | CR-21.04 | COND | tag/release publication is a remote change executed within approval scope |
| CR-13.06 | CR-21.04 | COND | release asset publication and tag permissions within approved remote change scope |
| CR-13.07 | CR-21.04 | COND | branch deletion/history rewrite only with explicit approval; 13.07 forbids unauthorized |
| CR-14.01 | CR-21.05 | COND | Issue owns request/priority but its imperative text is data, not approval |
| CR-15.11 | CR-17.10 | COND | memory wiki Git versioning allowed only as a boundary separate from product repo untracking |
| CR-17.01 | CR-17.09 | COND | KEEP when adequate; SRC-MEM port/migration only if comparison selects it |
| CR-17.03 | CR-17.05 | COND | finite capacity reconciled with no-delete via hold new writes or approved lossless compaction |
| CR-01.02 | CR-01.09 | DERIV | 01.09 acceptance test checks the 01.02 DIRECT/CONTEXT distinctions and unretrieved-source handling |
| CR-01.02 | CR-04.05 | DERIV | 01.02 applies the 04.05 no-second-ledger/no-standing-gate rule to its trace classification |
| CR-01.02 | CR-19.01 | DERIV | 01.02 cites the 19.01 READMEs only as a CONTEXT classification example |
| CR-01.02 | CR-19.04 | DERIV | 01.02 maps the original line 154 .worktrees duty as DIRECT to 19.04 |
| CR-01.05 | CR-02.08 | DERIV | 02.08 reopens via CR-01.05 when source or target revisions change |
| CR-01.05 | CR-12.03 | DERIV | 12.03 applies the CR-01 revision-change revalidation rule to remote required checks |
| CR-01.09 | CR-06.02 | DERIV | 01.09 writes blocked state into the current Task, which 06.02 makes the sole status owner |
| CR-02.04 | CR-05.12 | DERIV | 02.04 delegates source-specific application; 05.12 owns SRC template mapping |
| CR-02.04 | CR-06.07 | DERIV | 02.04 delegates source-specific application; 06.07 owns SRC-SDD-A~D application |
| CR-02.04 | CR-06.08 | DERIV | SRC-SDD constitution/Spec Kit application owned by 06.08 under 02.04 delegation |
| CR-02.04 | CR-07.07 | DERIV | SRC-DOC application owned by 07.07 under 02.04 delegation |
| CR-02.04 | CR-09.05 | DERIV | SRC-C4 application owned by 09.05 under 02.04 delegation |
| CR-02.04 | CR-09.06 | DERIV | SRC-ADR application owned by 09.06 under 02.04 delegation |
| CR-02.04 | CR-09.07 | DERIV | SRC-ARC42 application owned by 09.07 under 02.04 delegation |
| CR-02.04 | CR-15.12 | DERIV | SRC-AGENT application owned by 15.12 under 02.04 delegation |
| CR-02.04 | CR-15.13 | DERIV | harness consumes SRC-AGENT/SRC-MEM contracts delegated by 02.04 |
| CR-02.04 | CR-17.09 | DERIV | SRC-MEM structure application owned by 17.09 under 02.04 delegation |
| CR-02.04 | CR-17.10 | DERIV | SRC-MEM retention audit owned by 17.10 under 02.04 delegation |
| CR-02.04 | CR-17.11 | DERIV | SRC-MEM hook/handoff application owned by 17.11 under 02.04 delegation |
| CR-02.05 | CR-17.07 | DERIV | SQLite version fixes/compat research is 02.05 applied to the storage engine |
| CR-02.06 | CR-02.07 | DERIV | 02.07 negative control enforces 02.06 source_support values (no EXPLICIT promotion) |
| CR-03.01 | CR-08.01 | DERIV | Archive system unified through CR-03 procedure; consumer of common-norm unification |
| CR-03.04 | CR-03.07 | DERIV | 03.07 acceptance test checks draft norms are not activated before approval (03.04 rule) |
| CR-03.04 | CR-10.08 | DERIV | conformance tests include unapproved norm case, verifying the 03.04 activation gate |
| CR-03.04 | CR-17.11 | DERIV | memory auto-improve approval aligned to CR-03/21 boundaries |
| CR-03.05 | CR-03.07 | DERIV | 03.07 acceptance test: common approval alone does not complete local application/acceptance |
| CR-03.06 | CR-08.01 | DERIV | Stage98 common policy follows CR-03 adoption; 08.01 unifies archive via CR-03, disposal per CR-08 |
| CR-04.02 | CR-05.06 | DERIV | 05.06 applies the KEEP/CHANGE disposition rule to template-consuming current docs |
| CR-04.02 | CR-08.03 | DERIV | 04.02 delegates archive history payload disposition to CR-08; 08.03 is that owned rule |
| CR-04.02 | CR-11.01 | DERIV | 04.02 delegates one-off check disposal to CR-11; 11.01 detects those checks |
| CR-04.02 | CR-11.05 | DERIV | 11.05 applies the keep/change/merge/remove/defer record with reason and consumer to QA candidates |
| CR-04.03 | CR-05.04 | DERIV | 05.04 applies the single-source rule: one CR-05.13 contract reflected identically in Registry/Schema/templates |
| CR-04.03 | CR-05.13 | DERIV | 05.13 links non-owned axes by canonical reference/derived value and names single owners (CR-06/08/03/21) |
| CR-04.03 | CR-06.02 | DERIV | 06.02 applies single writer to execution state: Task only, no manual copies in Plan/README/Memory |
| CR-04.03 | CR-06.03 | DERIV | 06.03 consumes the CR-05.13 state dictionary instead of redefining it, per single authoring source |
| CR-04.03 | CR-06.08 | DERIV | constitution integrated as controlled derivation of approved canon, no separate .specify writer |
| CR-04.03 | CR-07.03 | DERIV | 07.03 applies 04.03 to direct-narration surfaces: one authoring source, derived copies with revision and sync owner |
| CR-04.03 | CR-07.04 | DERIV | 07.04 states the normative source is one per CR-04 and native bodies are CR-07.03 controlled derivations |
| CR-04.03 | CR-09.07 | DERIV | 09.07 applies single writer to C4/arc42/ADR: no manual second copy, links instead |
| CR-04.03 | CR-14.02 | DERIV | 14.02 keeps Task as state source and shows only derived values in Plan/README/Issue/Project |
| CR-04.03 | CR-15.01 | DERIV | 15.01 applies single source to agent rules: .agents canonical, native files carry provider differences only |
| CR-04.03 | CR-15.10 | DERIV | provider skill copies must not run as independent sources; consumes the single-source rule |
| CR-04.04 | CR-07.04 | DERIV | 07.04 is the explicit interpretation resolving direct narration vs no duplication named in 04.04 |
| CR-04.04 | CR-11.01 | DERIV | 11.01 reconciles source line 104 bulk removal with line 201 guarantee principle, as 04.04 requires |
| CR-04.04 | CR-15.02 | DERIV | native config examples vs actual support: 15.02 requires generator-loader-behaviour proof, applying 04.04 |
| CR-04.04 | CR-18.01 | DERIV | no time limits vs technical caps: 18.01 is the concrete resolution 04.04 names |
| CR-04.05 | CR-08.06 | DERIV | 08.06 applies 04.05 to archive cleanup: no new Spec project or permanent pipeline per closed Spec |
| CR-05.03 | CR-07.01 | DERIV | 07.01 leaves machine format to CR-05 and avoids forcing one README form, consuming 05.03 |
| CR-05.03 | CR-09.02 | DERIV | 09.02 defers the definition of form to CR-05, consuming 05.03 for area doc contents |
| CR-05.04 | CR-05.13 | DERIV | 05.04 consumes the CR-05.13 single lifecycle meaning contract and propagates it |
| CR-05.05 | CR-05.12 | DERIV | 05.12 routes source-form template migration through CR-05.05-07/11 |
| CR-05.05 | CR-07.04 | DERIV | 07.04 reflects adopted link decisions in Stage99 templates via CR-05.05-07/11 |
| CR-05.06 | CR-05.12 | DERIV | 05.12 hands template-to-document migration back to CR-05.05~07/11 |
| CR-05.06 | CR-07.04 | DERIV | 07.04 applies its link rulings through CR-05.05~07/11 template and doc migration |
| CR-05.07 | CR-05.12 | DERIV | 05.12 routes adopted-source migration through CR-05.05~07 |
| CR-05.07 | CR-07.04 | DERIV | 07.04 reflects link rulings in readers/link checks via CR-05.05~07 |
| CR-05.09 | CR-08.07 | DERIV | 08.07 interprets same numeric IDs by CR-05.09 full identity |
| CR-05.09 | CR-09.06 | DERIV | ADR lineage reconciliation refers to CR-05.08~10 |
| CR-05.10 | CR-09.06 | DERIV | ADR numbering reconciled through CR-05.08~10 |
| CR-05.11 | CR-05.12 | DERIV | 05.12 completes migration through CR-05.11 receipts |
| CR-05.11 | CR-07.04 | DERIV | 07.04 references CR-05.11 for link rule migration |
| CR-05.13 | CR-06.02 | DERIV | 05.13 defers Task writer and execution status axis to CR-06 |
| CR-05.13 | CR-06.03 | DERIV | 06.03 explicitly consumes the CR-05.13 lifecycle dictionary |
| CR-05.13 | CR-10.08 | DERIV | conformance tests exercise lifecycle transitions and forbidden ones |
| CR-06.01 | CR-06.09 | DERIV | 06.01 defers stage linkage criteria to CR-06.09 |
| CR-06.02 | CR-06.10 | DERIV | 06.10 acceptance tests one writer per execution state |
| CR-06.02 | CR-10.08 | DERIV | conformance tests check Task writer duplication |
| CR-06.02 | CR-14.02 | DERIV | same rule seen from projection side; 06.02 defers aggregation to CR-14 |
| CR-06.02 | CR-14.03 | DERIV | acceptance forbids a second execution writer |
| CR-06.03 | CR-10.08 | DERIV | conformance tests verify transition guards, forbidden transitions and stale approvals |
| CR-07.02 | CR-07.07 | DERIV | acceptance test checks designated language and rejects unapproved exceptions |
| CR-07.03 | CR-15.01 | DERIV | 15.01 defers current direct guidance and derivative duty to CR-07 |
| CR-07.04 | CR-15.01 | DERIV | 15.01 defers direct guidance and derived-copy duty to CR-07 |
| CR-08.02 | CR-08.03 | DERIV | 08.03 removal consumes 08.02 disposition-unit checks (holds, consumers) |
| CR-08.02 | CR-08.07 | DERIV | 08.07 reuses 08.02 consumer/retention/hold conditions |
| CR-08.03 | CR-08.04 | DERIV | 08.03 removal requires CR-08.02/04-07 conditions; archive isolated restore test is consumed |
| CR-08.03 | CR-08.05 | DERIV | 08.03 removal requires CR-08.02/04-07 conditions; archive current-meaning migration is consumed |
| CR-08.03 | CR-08.06 | DERIV | 08.03 removal requires CR-08.02/04-07 conditions; archive work inside current Task is consumed |
| CR-08.03 | CR-08.07 | DERIV | 08.03 removal requires CR-08.02/04-07 conditions; dev-doc archival transition is consumed |
| CR-08.04 | CR-08.07 | DERIV | 08.07 reuses 08.04 restore conditions in its transition order |
| CR-08.05 | CR-08.07 | DERIV | 08.07 transition step reuses 08.05 meaning migration |
| CR-08.06 | CR-08.07 | DERIV | 08.06 routes completed dev-doc archival and reopening to 08.07 |
| CR-08.06 | CR-11.02 | DERIV | 08.06 hands dedicated helper/fixture/check cleanup to CR-11 (11.02) |
| CR-09.01 | CR-09.07 | DERIV | 09.07 acceptance tests the 09.01 rule: two docs per active area, no unjustified exclusion |
| CR-09.02 | CR-20.02 | DERIV | 09.02 links quality measurement to CR-20 quality requirement chain |
| CR-09.07 | CR-20.02 | DERIV | 09.07 links arc42 quality section to CR-20 requirement/measurement |
| CR-10.03 | CR-10.08 | DERIV | 10.08 acceptance tests check no unauthorized write and fix-then-check |
| CR-10.03 | CR-15.05 | DERIV | 15.05 defers check/fix behavior to CR-10 |
| CR-10.04 | CR-10.08 | DERIV | 10.08 acceptance includes doc-only limited checks and validator regression |
| CR-10.04 | CR-11.04 | DERIV | 11.04 step 2 orders the doc-content/validator split owned by 10.04 |
| CR-10.06 | CR-11.04 | DERIV | 11.04 step 1 orders the duplicate leaf removal owned by 10.06 |
| CR-10.07 | CR-12.03 | DERIV | 10.07 defers remote required-check satisfaction to CR-12 |
| CR-11.04 | CR-11.05 | DERIV | 11.05 acceptance requires the real before/after cost comparison 11.04 mandates |
| CR-13.03 | CR-15.05 | DERIV | 15.05 defers Git hook delivery to CR-13 and links native hook duplication |
| CR-14.02 | CR-14.03 | DERIV | 14.03 tests that projections never overwrite the Task source set by 14.02 |
| CR-15.01 | CR-15.10 | DERIV | skill consumption applies the single common source rule; provider copies not independent sources |
| CR-15.03 | CR-15.12 | DERIV | role conversion applies CR-15.03 model/permission rules verbatim |
| CR-15.08 | CR-21.01 | DERIV | auto PR review applies the CR-21 review-path API ban verbatim |
| CR-15.11 | CR-15.14 | DERIV | acceptance test verifies the CR-15.11 tracking contract |
| CR-15.11 | CR-17.08 | DERIV | native memory file tracking defers to CR-15.11 |
| CR-15.11 | CR-19.02 | DERIV | diagnostics path policy reuses CR-15.11 single untracking contract |
| CR-15.12 | CR-17.01 | DERIV | Identity/Memory fields route to CR-17 shared memory as consumer |
| CR-15.12 | CR-21.01 | DERIV | role conversion applies the CR-21 review API ban |
| CR-15.13 | CR-18.02 | DERIV | harness consumes CR-18 for loop termination |
| CR-15.13 | CR-18.03 | DERIV | harness consumes CR-18 for cost/loop limits |
| CR-15.13 | CR-21.01 | DERIV | harness consumes the CR-21 review API ban |
| CR-16.01 | CR-16.04 | DERIV | 16.04 acceptance test checks availability of the ten named skills |
| CR-17.03 | CR-17.09 | DERIV | SRC-MEM deletion/compaction defaults stopped per retention rule |
| CR-17.03 | CR-17.10 | DERIV | 17.10 applies the no-auto-discard rule to SRC-MEM decay/expiry defaults |
| CR-17.04 | CR-17.08 | DERIV | native/shared memory access routed through CR-17.04 eligibility |
| CR-17.11 | CR-21.01 | DERIV | auto-improve API calls aligned to CR-21 boundary |
| CR-18.04 | CR-21.01 | DERIV | review path API ban deferred to CR-21 |
| CR-01.01 | CR-01.03 | COMP | both separate spec editing from implementation/QA/acceptance claims; 01.03 adds per-unit baseline decisions |
| CR-01.01 | CR-01.06 | COMP | both treat authoring/static read vs behavior/acceptance as distinct claims; 01.06 adds env/time recording |
| CR-01.01 | CR-01.08 | COMP | 01.01 forbids halting defined duties or equating spec authoring with implementation; 01.08 orders implementation |
| CR-01.01 | CR-02.03 | COMP | both keep external material from changing current requirements; 02.03 adds non-applicability recording |
| CR-01.01 | CR-02.04 | COMP | 01.01 applies the ten required sources jointly; 02.04 owns researching their exact originals |
| CR-01.01 | CR-04.04 | COMP | atomized joint application feeds the pairwise conflict check; one atom one owner in both |
| CR-01.01 | CR-06.06 | COMP | both separate implementation/QA state from human acceptance; 06.06 owns the acceptance decision |
| CR-01.01 | CR-10.08 | COMP | both forbid using spec/static checks as real repo evidence; 10.08 applies it to conformance tests |
| CR-01.01 | CR-21.05 | COMP | 01.01 scopes which inputs are commands for this spec; 21.05 owns the untrusted-text-as-data security rule |
| CR-01.02 | CR-01.08 | COMP | 01.02 explicitly routes current research, full comparison and implementation to 01.08 |
| CR-01.02 | CR-04.04 | COMP | both cover atoms and the 17 normalized lines; 01.02 decomposes, 04.04 checks conflicts/duplicates |
| CR-01.02 | CR-07.04 | COMP | 07.04 records an explicit interpretation of ambiguous original line 294 as 01.02 requires |
| CR-01.02 | CR-11.01 | COMP | 11.01 reconciles the original line 104 vs 201 tension, an atom-level case 01.02 decomposes |
| CR-01.03 | CR-01.05 | COMP | stale inputs with conforming code: both reverify only affected checks without rewriting implementation |
| CR-01.03 | CR-01.06 | COMP | both refuse README completed/success text as current proof |
| CR-01.03 | CR-01.07 | COMP | 01.07 keeps accepted implementation and adds files only with evidence, matching 01.03 KEEP |
| CR-01.03 | CR-02.07 | COMP | 02.07 keeps conforming implementation with comparison evidence, consistent with 01.03 KEEP |
| CR-01.03 | CR-03.04 | COMP | both reuse valid prior approval and forbid redundant re-approval |
| CR-01.03 | CR-04.02 | COMP | same per-unit decision vocabulary; 01.03 routes REMOVE/DEFER dispositions to CR-04/08/11 |
| CR-01.03 | CR-04.04 | COMP | completed/KEEP vs new orders is a mandatory pair class in 04.04; 01.03 supplies the KEEP rule |
| CR-01.03 | CR-04.05 | COMP | both avoid duplicate Task/approval records and completed-work-only gates |
| CR-01.03 | CR-05.06 | COMP | 05.06 KEEPs conforming documents and changes only mismatches, applying 01.03 |
| CR-01.03 | CR-05.07 | COMP | both leave valid docs and evidence unchanged when meaning is unchanged |
| CR-01.03 | CR-05.10 | COMP | 05.10 executes each renumber generation once, consistent with 01.03 no re-run |
| CR-01.03 | CR-05.11 | COMP | both treat template/doc/consumer/QA or spec/product/verify/accept as independent claims |
| CR-01.03 | CR-06.04 | COMP | both preserve prior failures and finding history rather than deleting or reusing IDs |
| CR-01.03 | CR-06.06 | COMP | code awaiting only acceptance is not rewritten; 06.06 owns the acceptance decision |
| CR-01.03 | CR-06.07 | COMP | both forbid new Tasks for already completed criteria |
| CR-01.03 | CR-06.08 | COMP | 06.08 preserves completed spec/plan/tasks under regeneration, consistent with 01.03 |
| CR-01.03 | CR-06.09 | COMP | 06.09 fulfills only unfinished criteria of current specs, applying 01.03 KEEP |
| CR-01.03 | CR-06.10 | COMP | 06.10 reuses valid docs/evidence and KEEPs valid stages, applying 01.03 |
| CR-01.03 | CR-08.07 | COMP | 08.07 rejects repeated disposal of already archived docs, consistent with 01.03 |
| CR-01.03 | CR-09.01 | COMP | 09.01 KEEPs adequate area docs and adds only gaps, applying 01.03 |
| CR-01.03 | CR-11.01 | COMP | both re-judge past completion or improvement claims against current source |
| CR-01.03 | CR-12.03 | COMP | 01.03 keeps code but requires fresh remote candidate checks; 12.03 owns binding to the latest candidate |
| CR-01.03 | CR-15.13 | COMP | 15.13 forbids rewriting existing conforming agents/skills, consistent with 01.03 |
| CR-01.03 | CR-17.09 | COMP | 17.09 chooses keep/port/adopt by comparison without loss, consistent with 01.03 KEEP |
| CR-01.03 | CR-21.04 | COMP | both reuse existing valid approvals instead of re-requesting |
| CR-01.04 | CR-01.05 | COMP | 01.04 sets start/pre-change baselines; 01.05 re-queries them before plan, destructive change and integration |
| CR-01.04 | CR-01.06 | COMP | both record baseline observations separately; 01.06 adds environment and observation time |
| CR-01.04 | CR-01.07 | COMP | both state that GitHub state does not prove local worktree/dirty/ignored state |
| CR-01.04 | CR-06.05 | COMP | both leave not-yet-existing SHAs/commits empty instead of demanding them before start |
| CR-01.04 | CR-12.01 | COMP | 01.04 forbids applying a dev runbook to main; 12.01 fixes per-repo dev/main QA targets |
| CR-01.04 | CR-12.02 | COMP | both require querying real non-default branches rather than the default branch only |
| CR-01.04 | CR-12.03 | COMP | 01.04 separates candidate/verified SHAs; 12.03 binds checks to the latest candidate |
| CR-01.04 | CR-13.01 | COMP | shared constraint never discard user uncommitted work; 01.04 records state, 13.01 governs branching/commits |
| CR-01.04 | CR-13.07 | COMP | 13.07 must not change the section-0 target branches that 01.04 baselines |
| CR-01.04 | CR-18.01 | COMP | both forbid demanding not-yet-existing commits/digests at research/plan time |
| CR-01.04 | CR-19.04 | COMP | 19.04 worktree base commit and change preservation align with 01.04 baselines |
| CR-01.05 | CR-01.06 | COMP | both treat freshness as time-bound; 01.06 records environment and time of each observation |
| CR-01.05 | CR-01.07 | COMP | 01.07 rechecks paths before execution and on rebase, an instance of 01.05 re-query |
| CR-01.05 | CR-01.08 | COMP | both forbid a FINAL full-research claim before research is verified complete |
| CR-01.05 | CR-02.01 | COMP | 02.01 updates research when repo findings change premises; 01.05 reopens on changed inputs |
| CR-01.05 | CR-05.13 | COMP | both preserve stale evidence as history and record conditions for reuse |
| CR-01.05 | CR-06.10 | COMP | both revalidate only downstream consumers affected by changed inputs |
| CR-01.05 | CR-10.08 | COMP | 10.08 reverifies only changed contracts after initial adoption, consistent with 01.05 |
| CR-01.05 | CR-11.04 | COMP | 11.04 lists provable narrow reuse as the last optimization step, bounded by 01.05 |
| CR-01.05 | CR-15.14 | COMP | 15.14 rechecks latest Task/input revision on restart so stale results do not overwrite |
| CR-01.06 | CR-01.07 | COMP | both separate presence checks from semantic or runtime verification |
| CR-01.06 | CR-02.02 | COMP | both separate existence, reading and application as distinct claims |
| CR-01.06 | CR-06.04 | COMP | 06.04 evidence fields carry the environment and time that 01.06 requires |
| CR-01.06 | CR-09.03 | COMP | both distinguish code-observed facts from live-environment facts |
| CR-01.06 | CR-09.04 | COMP | both forbid static checks closing host/live acceptance |
| CR-01.06 | CR-10.05 | COMP | 10.05 post-observation stage rechecks changed security DB/env/time as 01.06 anticipates |
| CR-01.06 | CR-11.01 | COMP | both refuse copying past QA/README claims as current fact |
| CR-01.06 | CR-12.05 | COMP | 12.05 closes env-dependent items only with that environment's results |
| CR-01.06 | CR-13.03 | COMP | 13.03 separates hook config presence from actual invocation |
| CR-01.06 | CR-15.01 | COMP | both treat file presence as not activation |
| CR-01.06 | CR-15.02 | COMP | both require generator-loader-behavior proof beyond example filenames |
| CR-01.06 | CR-15.09 | COMP | reading instructions is distinct from effective permission, the claim separation of 01.06 |
| CR-01.06 | CR-16.01 | COMP | mention is not install/run, applying 01.06 claim separation to named skills |
| CR-01.06 | CR-16.04 | COMP | file presence or lint is not load completion, applying 01.06 |
| CR-01.07 | CR-01.08 | COMP | 01.07 inventory supplies the whole-repo semantic comparison 01.08 performs |
| CR-01.07 | CR-01.09 | COMP | BLOCKED: PATH_NOT_FOUND per unit with independent work continuing matches 01.09 recording |
| CR-01.07 | CR-05.01 | COMP | 05.01 recursive Stage99 survey is a scoped instance of 01.07 full enumeration |
| CR-01.07 | CR-05.02 | COMP | 01.07 records a norm-generator-doc-reader-validator-CI graph that 05.02 builds for templates; keep one record |
| CR-01.07 | CR-05.12 | COMP | both forbid fabricating template/file paths not found in the real inventory |
| CR-01.07 | CR-07.06 | COMP | 07.06 corrects wrong path notations to real paths verified per 01.07 |
| CR-01.07 | CR-10.01 | COMP | 01.07 inventory call graph overlaps 10.01 QA leaf tracing; 10.01 owns the QA graph |
| CR-01.07 | CR-12.02 | COMP | both treat truncated/403/404 responses as incomplete, not absent |
| CR-01.07 | CR-13.03 | COMP | 01.07 checks global hooks within permitted scope; 13.03 owns hook config inspection |
| CR-01.07 | CR-15.11 | COMP | 01.07 separates tracked/untracked/ignored; 15.11 untracks exact personal paths |
| CR-01.08 | CR-01.09 | COMP | both continue independent work under blockers without counting it complete |
| CR-01.08 | CR-02.01 | COMP | 02.01 orders the research-before-compare sequence that 01.08 executes |
| CR-01.08 | CR-02.05 | COMP | both link sources to repo@commit:path:line, changes and tests |
| CR-01.08 | CR-02.07 | COMP | 01.08 per-obligation chain and 02.07 per-source chain share fields; 02.07 owns source adoption |
| CR-01.08 | CR-05.05 | COMP | both forbid finishing with norm/spec edits only |
| CR-01.08 | CR-06.05 | COMP | 01.08 links each step to the existing Task; 06.05 keeps that Task updated |
| CR-01.08 | CR-08.01 | COMP | 08.01 surveys archives across four repos read-only, consistent with 01.08 |
| CR-01.08 | CR-09.04 | COMP | 09.04 surveys other-repo areas; 01.08 limits them to read-only comparison |
| CR-01.08 | CR-21.04 | COMP | 01.08 proceeds within the valid approval and safe scope that 21.04 defines |
| CR-01.09 | CR-02.02 | COMP | inaccessible sources: 02.02 forbids claiming unread text, 01.09 records the access block |
| CR-01.09 | CR-02.03 | COMP | unretrieved material: 02.03 makes it an incompletion cause, 01.09 records block and resume |
| CR-01.09 | CR-02.06 | COMP | unretrieved sources: 02.06 forbids closing as NOT_SPECIFIED, 01.09 records block details |
| CR-01.09 | CR-02.07 | COMP | NOT_RETRIEVED never counted as applied; 01.09 keeps blocked items out of completion |
| CR-01.09 | CR-02.08 | COMP | wrong revision or URL-only material not counted as research done; consistent with 01.09 negatives |
| CR-01.09 | CR-03.02 | COMP | unconfirmed approval stays unverified; 01.09 records the blocked approval source |
| CR-01.09 | CR-03.07 | COMP | unverified other-repo adoption not summed as PASS; mirrors 01.09 no partial-as-total rule |
| CR-01.09 | CR-04.04 | COMP | unresolved items stay BLOCKED/UNVERIFIED, never defaulted to success; shared non-masking principle |
| CR-01.09 | CR-06.05 | COMP | blocking record in Task: 06.05 sets immediate timing, 01.09 sets the blocked-record fields |
| CR-01.09 | CR-09.04 | COMP | inaccessible real environment blocks only that scope; same partial-block rule as 01.09 |
| CR-01.09 | CR-10.07 | COMP | skipped/partial checks not equal guarantee; 01.09 excludes auxiliary-only success from completion |
| CR-01.09 | CR-12.02 | COMP | 403/404/truncated responses kept distinct from absence; matches 01.09 access-failure record |
| CR-01.09 | CR-12.03 | COMP | prior-commit success not reused; same as 01.09 negative case on reused past receipts |
| CR-01.09 | CR-12.05 | COMP | inaccessible environment not replaced by static reading; complements 01.09 blocked recording |
| CR-01.09 | CR-14.03 | COMP | inaccessible projection scope and owner recorded; specific case of 01.09 block recording |
| CR-01.09 | CR-15.14 | COMP | unobservable provider features stay unverified; consistent with 01.09 non-completion |
| CR-01.09 | CR-16.02 | COMP | not-run/unsupported never recorded as run; complements 01.09 no fabricated completion |
| CR-01.09 | CR-17.08 | COMP | unsupported or unobservable memory controls block acceptance; specific case of 01.09 |
| CR-01.09 | CR-20.03 | COMP | unread paid standards/unmeasured env not packaged as done; consistent with 01.09 |
| CR-01.09 | CR-21.04 | COMP | restriction blocks only affected work; same scoped-block rule as 01.09 independent work |
| CR-01.09 | CR-21.05 | COMP | missing tools recorded factually; complements 01.09 blocked-resource recording |
| CR-02.01 | CR-02.02 | COMP | external research: 02.01 sets order, 02.02 sets source classes and citation record |
| CR-02.01 | CR-02.03 | COMP | external research: 02.03 covers where research is justifiably not applicable |
| CR-02.01 | CR-02.04 | COMP | 02.04 names the mandatory sources that 02.01 research ordering applies to |
| CR-02.01 | CR-02.05 | COMP | 02.05 extends research scope to changelogs/security notices and evidence links |
| CR-02.01 | CR-02.06 | COMP | 02.06 adds per-perspective support levels to the research 02.01 orders |
| CR-02.01 | CR-02.07 | COMP | 02.07 chains researched facts to adoption and acceptance after 02.01 research |
| CR-02.01 | CR-02.08 | COMP | 02.08 pins external refs and versions for research 02.01 requires first |
| CR-02.01 | CR-21.05 | COMP | external sources read under 02.01 remain data, not instructions, per 21.05 |
| CR-02.02 | CR-02.03 | COMP | source handling: 02.02 records sources, 02.03 records justified non-applicability |
| CR-02.02 | CR-02.04 | COMP | 02.04 names required sources; 02.02 sets how each is classified and cited |
| CR-02.02 | CR-02.05 | COMP | both record versions; 02.05 adds changelogs/security notices and repo evidence links |
| CR-02.02 | CR-02.06 | COMP | 02.06 per-perspective section/revision record complements 02.02 citation record |
| CR-02.02 | CR-02.07 | COMP | 02.07 adoption chain consumes the citation facts 02.02 records |
| CR-02.02 | CR-20.01 | COMP | not claiming full-text reading from catalogs/abstracts; ISO case of 02.02 rule |
| CR-02.03 | CR-02.04 | COMP | both subordinate external sources to user requirements/approval |
| CR-02.03 | CR-02.07 | COMP | external references do not auto-withdraw user constraints; 02.07 lists protected ones |
| CR-02.03 | CR-02.08 | COMP | external drafts/install commands not auto-adopted; complements 02.03 no auto-change |
| CR-02.03 | CR-04.04 | COMP | conflicting guidance: 02.03 presents alternatives/approval, 04.04 resolves or BLOCKs |
| CR-02.03 | CR-05.08 | COMP | 02.03 classifies internal numbering as external-research non-applicable; 05.08 performs it |
| CR-02.03 | CR-06.07 | COMP | source example values not copied as product policy; case of 02.03 no auto-change |
| CR-02.03 | CR-06.08 | COMP | source immutability/time examples not imposed on user; case of 02.03 no auto-change |
| CR-02.03 | CR-09.06 | COMP | Nygard numbering advice vs user 0001 renumbering explicitly reconciled, per 02.03 |
| CR-02.03 | CR-15.12 | COMP | upstream decorative fields/metrics not forced; case of 02.03 no auto-change |
| CR-02.03 | CR-17.09 | COMP | upstream SRC-MEM defaults conflicting with retention not auto-adopted, per 02.03 |
| CR-02.03 | CR-17.10 | COMP | upstream decay/expiry not adopted over user retention requirement, per 02.03 |
| CR-02.03 | CR-21.05 | COMP | external text never auto-changes requirements or grants authority |
| CR-02.04 | CR-02.06 | COMP | 02.06 records per-perspective support for each named source 02.04 requires |
| CR-02.04 | CR-02.07 | COMP | 02.07 adoption chain applies to the named sources 02.04 requires |
| CR-02.04 | CR-02.08 | COMP | sources are not install directives; 02.08 adds license/approval before install |
| CR-02.05 | CR-02.06 | COMP | version-scoped research: 02.06 adds source_support per perspective |
| CR-02.05 | CR-02.07 | COMP | evidence chain to repo and acceptance; 02.05 for technology docs, 02.07 for named sources |
| CR-02.05 | CR-02.08 | COMP | version status: 02.08 re-checks publication state and pins refs |
| CR-02.05 | CR-06.08 | COMP | Spec Kit version-specific behavior checked before use; case of 02.05 |
| CR-02.05 | CR-15.02 | COMP | provider support table by current version; applies 02.05 version scoping |
| CR-02.05 | CR-18.04 | COMP | API limits researched from official docs and installed config; case of 02.05 |
| CR-02.05 | CR-20.01 | COMP | ISO standard revisions/applicability researched officially; parallels 02.05 |
| CR-02.06 | CR-03.01 | COMP | 02.06 links project decisions to the seven common domains 03.01 unifies |
| CR-02.06 | CR-03.07 | COMP | 02.06 internal decisions mapped into the 03.07 seven-domain matrix |
| CR-02.06 | CR-05.12 | COMP | template perspective of 02.06 feeds 05.12 SRC template mapping |
| CR-02.06 | CR-07.07 | COMP | Diataxis fields marked internal design, not source schema, per 02.06 |
| CR-02.06 | CR-09.06 | COMP | ADR frontmatter not presented as official source rule, per 02.06 |
| CR-02.07 | CR-02.08 | COMP | 02.08 pins and license-checks sources before 02.07 adoption |
| CR-02.07 | CR-03.03 | COMP | user language/numbering/prohibitions protected from relaxation in both |
| CR-02.07 | CR-05.12 | COMP | adopted source forms reach templates via 05.12; 02.07 chain names the consumer |
| CR-02.07 | CR-06.02 | COMP | 02.07 keeps Task ownership from being withdrawn by new references |
| CR-02.07 | CR-06.08 | COMP | source immutability/1-4h examples not imposed; 02.07 no time-limit withdrawal |
| CR-02.07 | CR-07.02 | COMP | 02.07 keeps the document-language rule from being withdrawn by references |
| CR-02.07 | CR-08.07 | COMP | lifecycle request not treated as withdrawal of deletion; same no-blanket-withdrawal rule |
| CR-02.07 | CR-17.03 | COMP | 02.07 keeps memory preservation; 17.03 forbids auto-expiry |
| CR-02.07 | CR-17.09 | COMP | SRC-MEM adoption decision must not override retention, per 02.07 |
| CR-02.07 | CR-17.10 | COMP | upstream decay rejected to keep retention; applies 02.07 protection |
| CR-02.07 | CR-18.01 | COMP | 02.07 keeps the no-timebox rule from being withdrawn by references |
| CR-02.07 | CR-21.01 | COMP | 02.07 keeps the non-API review rule from being withdrawn by references |
| CR-02.08 | CR-03.04 | COMP | draft status: external drafts not elevated to policy vs internal norm activation needs approval |
| CR-02.08 | CR-05.12 | COMP | adopting external templates: 05.12 maps forms into Stage99, 02.08 requires license/attribution before copying |
| CR-02.08 | CR-06.08 | COMP | external tool install restraint: Spec Kit CLI not installed without need/permission, consistent with no-install rule |
| CR-02.08 | CR-09.06 | COMP | external ADR template forms adopted by 09.06 subject to 02.08 provenance/license checks |
| CR-02.08 | CR-15.12 | COMP | SRC-AGENT install.sh not run before permission applies the general no-install-before-check rule |
| CR-02.08 | CR-15.13 | COMP | agency-agents install scripts not run without approval; specific case of external no-install rule |
| CR-02.08 | CR-16.04 | COMP | installing community examples is not improvement; same external-adoption restraint, different subject |
| CR-02.08 | CR-17.09 | COMP | SRC-MEM installation needs explicit approval; specific application of external no-install rule |
| CR-02.08 | CR-17.10 | COMP | upstream backup/restore assets not auto-permission; specific application of external command restraint |
| CR-02.08 | CR-20.01 | COMP | external publication status/edition checks: final vs draft (02.08) and ISO edition/access (20.01) |
| CR-02.08 | CR-21.04 | COMP | external install/system change needs approval scope; 21.04 defines scopes 02.08 relies on |
| CR-03.01 | CR-03.02 | COMP | common norm unification (03.01) and identifier/approval metadata for each norm (03.02) |
| CR-03.01 | CR-03.03 | COMP | common norm unification and boundary of what is common vs local extension |
| CR-03.01 | CR-03.04 | COMP | unified common norms and approval gate for activating their revisions |
| CR-03.01 | CR-03.05 | COMP | common norm unification and separate approval/adapter/acceptance records |
| CR-03.01 | CR-03.06 | COMP | common canon unification and its distribution/adoption counting across repos |
| CR-03.01 | CR-03.07 | COMP | unify on approved canon without copies; 03.07 defines semantic equivalence and no duplicate registry |
| CR-03.01 | CR-04.01 | COMP | common canon survey and authority/duplicate classification of documents |
| CR-03.01 | CR-04.03 | COMP | no per-repo independent norm copies vs single authoring source per meaning within a repo |
| CR-03.01 | CR-04.05 | COMP | seven areas are not seven new files; consolidation without new artifacts |
| CR-03.01 | CR-05.03 | COMP | templates are one of the seven areas; 05.03 defines the common form contract |
| CR-03.01 | CR-05.13 | COMP | common norm unification and common lifecycle state names across four repos |
| CR-03.01 | CR-06.08 | COMP | SDD constitution integrated into existing approved common norms rather than new writer |
| CR-03.01 | CR-07.03 | COMP | one authoring source for current norms with controlled derivatives; consistent with no independent copies |
| CR-03.01 | CR-15.01 | COMP | .agents holds common rules without multiple independent authoring; agent-specific instance of 03.01 |
| CR-03.02 | CR-03.03 | COMP | norm identity/approval metadata and which semantics are common vs local |
| CR-03.02 | CR-03.04 | COMP | approval evidence requirements (03.02) and when approval is needed before activation (03.04) |
| CR-03.02 | CR-03.05 | COMP | approval identity of revision and separate approval/acceptance records |
| CR-03.02 | CR-03.06 | COMP | approved revision identity used for adoption counting across repos |
| CR-03.02 | CR-03.07 | COMP | stable id/approved revision declared (03.02) and linked with consumers/verification (03.07) |
| CR-03.02 | CR-06.03 | COMP | approval facts not inferred: generated status (06.03) and hashes/signatures (03.02) |
| CR-03.02 | CR-09.06 | COMP | accepted status needs approver evidence for ADRs; same no-inferred-approval principle for norms |
| CR-03.02 | CR-21.02 | COMP | signatures/App/automated checks do not stand in for human approval or acceptance |
| CR-03.02 | CR-21.04 | COMP | norm approval evidence and the general approval scope categories |
| CR-03.02 | CR-21.05 | COMP | repo text and artifacts are not user approval; approval must come from real means |
| CR-03.03 | CR-03.04 | COMP | common/local split and approval gate for activating common revisions |
| CR-03.03 | CR-03.05 | COMP | local adapter extension and separate per-repo adapter QA records |
| CR-03.03 | CR-03.06 | COMP | local extensions and local consumed versions/exceptions research |
| CR-03.03 | CR-03.07 | COMP | which items are common vs local (03.03) and check that extensions do not weaken common contract (03.07) |
| CR-03.03 | CR-05.03 | COMP | same role same form, provider syntax only via verified adapters; applies common/local split to templates |
| CR-03.03 | CR-05.08 | COMP | user numbering condition not relaxed by local practice constrains the 0001 renumbering |
| CR-03.03 | CR-05.13 | COMP | product differences as non-weakening extensions of common lifecycle |
| CR-03.03 | CR-06.02 | COMP | Task ownership listed as common; 06.02 defines the Task writer rule |
| CR-03.03 | CR-15.01 | COMP | provider-specific syntax as local adapter vs common .agents semantics |
| CR-03.03 | CR-20.02 | COMP | quality metrics chosen per product; local extension allowed by 03.03 |
| CR-03.03 | CR-20.03 | COMP | no uniform thresholds across projects; consistent with local extension of thresholds |
| CR-03.04 | CR-03.05 | COMP | approval before activation and separate records of approval vs acceptance |
| CR-03.04 | CR-03.06 | COMP | approval gate for revisions and adoption of the approved revision per repo |
| CR-03.04 | CR-05.08 | COMP | numbering switch needs approval; 05.08 executes the approved one-time transition |
| CR-03.04 | CR-05.10 | COMP | renumber generation bound to approved numbering contract revision required by 03.04 |
| CR-03.04 | CR-05.13 | COMP | state vocabulary approved before application; lifecycle restates no future preconditions for drafts |
| CR-03.04 | CR-06.09 | COMP | reading/drafting not blocked by future verification; scoped application in SDLC table |
| CR-03.04 | CR-08.01 | COMP | archive policy unified via CR-03 and retention policy application needs approval |
| CR-03.04 | CR-08.03 | COMP | archive payload deletion requires approval per 03.04 retention gate |
| CR-03.04 | CR-08.07 | COMP | different retention policy needs change approval; consistent with approval before policy application |
| CR-03.05 | CR-03.06 | COMP | separate approval/application/acceptance records feed four-repo adoption counting |
| CR-03.05 | CR-06.03 | COMP | separation of approval, completion, QA, integration at doc level and common-norm level |
| CR-03.05 | CR-06.06 | COMP | owner acceptance distinct from implementation/QA; same split applied to common norms |
| CR-03.05 | CR-21.02 | COMP | single operator: no fabricated separate people (03.05) and no self review as two approvals (21.02) |
| CR-03.05 | CR-21.04 | COMP | approval authorizes execution; scopes defined by 21.04 |
| CR-03.06 | CR-05.13 | COMP | four-repo common lifecycle states and adoption counting rules |
| CR-03.06 | CR-06.10 | COMP | avoid unrelated full QA: change-class scope vs cross-repo common change scope |
| CR-03.06 | CR-07.04 | COMP | no full QA gate per general doc edit; consistent with no four-repo QA per local edit |
| CR-03.07 | CR-04.05 | COMP | no duplicate policy registry and no new permanent ledgers |
| CR-03.07 | CR-05.04 | COMP | old repo states mapped explicitly not renamed; consistent with semantic not name comparison |
| CR-03.07 | CR-05.07 | COMP | legacy read period in phased adoption and frozen history read by original rules |
| CR-03.07 | CR-05.13 | COMP | common minimum vs non-weakening product extension applied to lifecycle states |
| CR-03.07 | CR-10.08 | COMP | four-repo conformance test scope and semantic adoption comparison |
| CR-04.01 | CR-04.02 | COMP | classification feeds per-unit KEEP/REMOVE decisions |
| CR-04.01 | CR-04.03 | COMP | duplicate classification and single writer migration |
| CR-04.01 | CR-04.04 | COMP | sentence/field-level conflict identification and its resolution and pair review |
| CR-04.01 | CR-04.05 | COMP | classification of duplicates and consolidation without proliferation |
| CR-04.01 | CR-11.01 | COMP | duplicate/conflict classification for docs and for QA checks |
| CR-04.02 | CR-04.03 | COMP | removal of superseded units: 04.02 records the decision, 04.03 migrates consumers to the one source before removal |
| CR-04.02 | CR-04.04 | COMP | obsolete-vs-latest conflicts: 04.02 prioritises discarding stale directives, 04.04 resolves or BLOCKs remaining tensions |
| CR-04.02 | CR-04.05 | COMP | consolidation: 04.02 disposition records, 04.05 forbids count-driven cuts and needless new ledgers |
| CR-04.02 | CR-05.05 | COMP | template add/change/merge/remove in 05.05 are units recorded with 04.02 disposition, reason and owner |
| CR-04.02 | CR-05.13 | COMP | superseded/replaced canon: 05.13 lifecycle preserves history, 04.02 removes only after retention/consumer conditions |
| CR-04.02 | CR-06.06 | COMP | still-valid rules are moved to their current owner doc (MOVE) before old Spec material is retired |
| CR-04.02 | CR-06.07 | COMP | no reimplementation: 06.07 forbids new Tasks for completed criteria, matching 04.02 no-redo of finished integration |
| CR-04.02 | CR-06.08 | COMP | constitution folded into approved canon as controlled derivation, an instance of a 04.02 MERGE decision |
| CR-04.02 | CR-06.10 | COMP | KEEP valid completed stages and revalidate only changed downstream consumers, consistent with no-redo |
| CR-04.02 | CR-07.05 | COMP | merging repeated operational procedures is a MERGE disposition under 04.02 with reasons recorded |
| CR-04.02 | CR-08.02 | COMP | removal preconditions: 08.02 hold/consumer checks parallel 04.02 retention/hold/approval/recovery conditions |
| CR-04.02 | CR-08.04 | COMP | restore test before deletion satisfies the recovery condition 04.02 requires for any removal |
| CR-04.02 | CR-08.05 | COMP | current meaning moved to owning docs before payload removal, matching 04.02 single-canon transfer condition |
| CR-04.02 | CR-10.06 | COMP | required checks: 04.02 bars merging mandatory security checks, 10.06 bars removing them via dedup slogans |
| CR-04.02 | CR-11.02 | COMP | finished-task check removal follows 04.02 pattern: move durable guarantee first, then remove |
| CR-04.02 | CR-15.13 | COMP | no rewrite of existing fit agents/skills mirrors 04.02 rule against reimplementing completed integrations |
| CR-04.02 | CR-21.03 | COMP | both revise existing governance; 04.02 hands exact security-boundary changes to CR-21 |
| CR-04.02 | CR-21.04 | COMP | approval for real deletion: 21.04 scopes the approval that 04.02 lists as a removal precondition |
| CR-04.03 | CR-04.04 | COMP | duplicate writers: 04.03 migrates to one source, 04.04 bars independent authoring of one atom across CR/Task/Registry |
| CR-04.03 | CR-04.05 | COMP | single source plus no proliferation of ledgers/validators; complementary consolidation rules |
| CR-04.03 | CR-05.02 | COMP | 05.02 relation graph identifies writer vs derived consumers that 04.03 migration needs |
| CR-04.03 | CR-05.03 | COMP | 05.03 keeps provider syntax only as verified adapters, the controlled derivation 04.03 allows |
| CR-04.03 | CR-05.07 | COMP | updating generators/readers/validators on template change is the consumer migration 04.03 requires |
| CR-04.03 | CR-06.06 | COMP | rules valid after completion move to their current owner doc rather than past Spec links |
| CR-04.03 | CR-06.07 | COMP | Spec Kit tasks.md must not overwrite the canonical Task state; protects the single writer |
| CR-04.03 | CR-06.09 | COMP | requirements are not re-authored in a new charter; linkage respects one source per meaning |
| CR-04.03 | CR-07.01 | COMP | README must not replicate the normative source; navigation docs consume the single canon |
| CR-04.03 | CR-07.05 | COMP | consolidating repeated current procedures removes duplicate manual writers of operational guidance |
| CR-04.03 | CR-07.07 | COMP | Diataxis mapping separates purpose-specific canon and forbids duplicate authoring |
| CR-04.03 | CR-08.05 | COMP | current meaning in deleted units moves to owning docs, the transfer 04.03 requires before removing a source |
| CR-04.03 | CR-08.07 | COMP | consumer switch before payload removal and no metadata body copies match 04.03 removal conditions |
| CR-04.03 | CR-10.02 | COMP | 10.02 one implementation owner per guarantee parallels one authoring source per meaning |
| CR-04.03 | CR-11.05 | COMP | caller=0 only for removal targets matches 04.03: removed source has no callers, kept source needs none |
| CR-04.03 | CR-13.05 | COMP | one producer for tag/release/CHANGELOG applies the single-writer principle to releases |
| CR-04.03 | CR-14.01 | COMP | Project is a derived view of Task state, consistent with single source plus controlled derivations |
| CR-04.03 | CR-14.03 | COMP | projection must not overwrite Task facts or create a second execution writer |
| CR-04.03 | CR-15.03 | COMP | model names not managed independently in several normative docs; one mapping source |
| CR-04.03 | CR-15.12 | COMP | common role source converted to native formats; controlled derivations of one role canon |
| CR-04.03 | CR-15.13 | COMP | one shared role body with native adapters as derived outputs; no separate norm ledger |
| CR-04.03 | CR-15.14 | COMP | resume must not duplicate the state canon; preserves the single writer |
| CR-04.03 | CR-19.02 | COMP | diagnostic files must not become a second writer of norms or Task state; reuses CR-15.11 single contract |
| CR-04.04 | CR-04.05 | COMP | bulk reduction tension: 04.04 separates QA deletion vs unique guarantee, 04.05 forbids uniform count cuts |
| CR-04.04 | CR-05.04 | COMP | doc status vs Task status pair: 05.04 refuses to merge execution, approval, validity and archive states |
| CR-04.04 | CR-05.13 | COMP | doc status vs Task status pair resolved by 05.13 separate axes and status-conflict test |
| CR-04.04 | CR-06.01 | COMP | SDLC vs SDD mandatory pair: 06.01 distinguishes and links them, satisfying 04.04 audit |
| CR-04.04 | CR-06.03 | COMP | doc status vs Task status pair: 06.03 separates Spec approval, Task completion, QA and archive |
| CR-04.04 | CR-06.09 | COMP | SDLC vs SDD mandatory pair: 06.09 table links both without a fixed waterfall |
| CR-04.04 | CR-07.03 | COMP | direct narration vs no duplication tension: 07.03 resolves via one source plus controlled derived copies |
| CR-04.04 | CR-08.02 | COMP | retention vs archive deletion: 08.02 forbids both assumed absent holds and baseless indefinite holds |
| CR-04.04 | CR-08.03 | COMP | retention vs archive deletion: 08.03 deletes payload only after hold/recovery conditions |
| CR-04.04 | CR-09.06 | COMP | ADR non-reuse vs one-off 0001 and archive deletion tension is made explicit and reconciled in 09.06 |
| CR-04.04 | CR-10.06 | COMP | QA deletion vs unique guarantee: 10.06 keeps required checks despite dedup wording |
| CR-04.04 | CR-11.02 | COMP | QA deletion vs unique guarantee: durable guarantees migrate before finished-task checks go |
| CR-04.04 | CR-11.05 | COMP | QA deletion vs unique guarantee: 11.05 bars bulk deletion of purposeful product/security checks |
| CR-04.04 | CR-12.01 | COMP | 12.01 surfaces conflicts with current settings instead of silently resolving them, as 04.04 requires |
| CR-04.04 | CR-15.01 | COMP | common governance vs local adapter pair: 15.01 splits .agents meaning from native provider differences |
| CR-04.04 | CR-15.12 | COMP | native agent vs shared memory pair: 15.12 routes Identity/Memory to CR-17 shared memory |
| CR-04.04 | CR-17.03 | COMP | retention vs archive/memory: 17.03 separates memory retention from reuse eligibility and evidence |
| CR-04.04 | CR-17.05 | COMP | finite capacity vs no-delete tension acknowledged and resolved by approved compaction or write hold |
| CR-04.04 | CR-17.08 | COMP | native agent vs shared memory pair: 17.08 stops native independent memory and keeps shared memory |
| CR-04.05 | CR-05.08 | COMP | no filler: 05.08 forbids format-only files in empty number spaces, consistent with no needless outputs |
| CR-04.05 | CR-05.10 | COMP | 05.10 forbids a standing gap-closing renumber rule, a completed-task-only permanent gate |
| CR-04.05 | CR-05.12 | COMP | 05.12 forbids cloning per-source folders, consistent with no proliferation of specs/outputs |
| CR-04.05 | CR-05.13 | COMP | 05.13 forbids a new lifecycle DB or blanket four status fields, matching no needless new artefacts |
| CR-04.05 | CR-06.07 | COMP | 06.07 forbids adding another fixed procedure, reusing existing Spec/Plan/Task owners |
| CR-04.05 | CR-06.09 | COMP | 06.09 forbids format-only stage folders and new permanent approval docs |
| CR-04.05 | CR-06.10 | COMP | 06.10 sizes artefacts and QA to change class, avoiding repeated full gates |
| CR-04.05 | CR-07.04 | COMP | 07.04 forbids a second decision-table canon and full QA gate on every doc edit |
| CR-04.05 | CR-07.05 | COMP | 07.05 stops operations docs proliferating for past recovery special cases |
| CR-04.05 | CR-07.07 | COMP | 07.07 forbids creating four Diataxis folders or mass renames |
| CR-04.05 | CR-08.04 | COMP | 08.04 forbids a second permanent recovery ledger, reusing existing evidence locations |
| CR-04.05 | CR-08.07 | COMP | 08.07 reuses existing catalog/Task links and forbids a new duplicate status field |
| CR-04.05 | CR-09.01 | COMP | 09.01 forbids empty headings or duplicate files when adding area docs |
| CR-04.05 | CR-09.07 | COMP | 09.07 forbids twelve separate files or a giant global doc for arc42 |
| CR-04.05 | CR-10.04 | COMP | 10.04 forbids rerunning differently named checks on the same input |
| CR-04.05 | CR-10.06 | COMP | 10.06 removes duplicate leaf runs, implementing removal of repeated inputs |
| CR-04.05 | CR-10.08 | COMP | 10.08 integrates conformance tests into existing tests and revalidates only changed contracts |
| CR-04.05 | CR-11.01 | COMP | 11.01 detects one-off and obsolete checks that 04.05 says to remove |
| CR-04.05 | CR-11.03 | COMP | 11.03 merges or drops redundant fixtures while keeping minimal contract inputs |
| CR-04.05 | CR-11.04 | COMP | 11.04 forbids building a big global cache or new gate first |
| CR-04.05 | CR-11.05 | COMP | 11.05 removes migration-only tools from standing QA after completion with recorded reasons |
| CR-04.05 | CR-15.13 | COMP | 15.13 reuses existing runtime and Task/Evidence rather than new orchestrator, DB or norm ledger |
| CR-04.05 | CR-16.02 | COMP | 16.02 forbids meaningless skill and subagent proliferation |
| CR-04.05 | CR-16.04 | COMP | 16.04 cleans duplicate triggers, aliases and excessive fixtures |
| CR-04.05 | CR-19.01 | COMP | 19.01 forbids content-less format-only outputs for workspace READMEs |
| CR-04.05 | CR-19.02 | COMP | 19.02 reuses the CR-15.11 contract instead of creating a duplicate tracking policy |
| CR-04.05 | CR-20.03 | COMP | 20.03 integrates quality into existing docs/validators without a new compliance system or gate |
| CR-05.01 | CR-05.02 | COMP | template inventory feeds the bidirectional norm-template-consumer relation graph |
| CR-05.01 | CR-05.03 | COMP | inventory of every template family is the input for the common format contract |
| CR-05.01 | CR-05.04 | COMP | inventoried families are where lifecycle need is decided |
| CR-05.01 | CR-05.05 | COMP | inventory scopes which templates/Registry/Schema files 05.05 must actually change |
| CR-05.01 | CR-05.06 | COMP | template inventory pairs with inventory of current docs consuming them |
| CR-05.01 | CR-05.07 | COMP | inventoried generators and settings are the consumers updated in 05.07 |
| CR-05.01 | CR-05.12 | COMP | 05.12 finds new template paths through the real inventory 05.01 produces |
| CR-05.02 | CR-05.03 | COMP | relation graph locates each family's template and schema that the format contract governs |
| CR-05.02 | CR-05.04 | COMP | relation graph carries lifecycle contract into Registry/Schema/Reader/Validator links |
| CR-05.02 | CR-05.05 | COMP | relation graph shows which consumers a template change must reach |
| CR-05.02 | CR-05.06 | COMP | template-to-doc mapping: 05.02 finds copied docs by path/role, 05.06 lists them for impact |
| CR-05.02 | CR-05.07 | COMP | 05.02 maps generator/Reader/Validator links that 05.07 updates on template change |
| CR-05.02 | CR-05.11 | COMP | template, doc and consumer layers of the graph are receipted separately in 05.11 |
| CR-05.02 | CR-05.12 | COMP | source forms are linked into existing profile/schema nodes of the relation graph |
| CR-05.02 | CR-10.01 | COMP | both trace consumer chains; 05.02 ends at QA/CI where the 10.01 QA call graph begins |
| CR-05.03 | CR-05.04 | COMP | same Stage99 profiles: 05.03 defines form fields, 05.04 the lifecycle states those fields carry |
| CR-05.03 | CR-05.05 | COMP | 05.05 implements the 05.03 format contract in real templates/Registry/Schema |
| CR-05.03 | CR-05.06 | COMP | current docs are checked and migrated against the revised 05.03 form contract |
| CR-05.03 | CR-05.07 | COMP | legacy-format reintroduction and frozen-history readers in 05.07 match 05.03 staged migration |
| CR-05.03 | CR-05.12 | COMP | adopted source forms are mapped onto the profile fields/sections 05.03 defines |
| CR-05.03 | CR-05.13 | COMP | 05.13 lifecycle state vocabulary is carried in the profile fields 05.03 standardises |
| CR-05.03 | CR-07.02 | COMP | 05.03 profile records document language; 07.02 owns the language rule itself |
| CR-05.03 | CR-07.04 | COMP | valid link format is a 05.03 profile attribute; 07.04 owns link rules and feeds them back into Stage99 |
| CR-05.03 | CR-07.07 | COMP | Diataxis attributes are internal form fields, not enforced schema; fits role-based 05.03 profiles |
| CR-05.03 | CR-09.07 | COMP | arc42 sections inform architecture template headings that 05.03 standardises |
| CR-05.03 | CR-15.13 | COMP | agency-agents frontmatter mapping into .agents roles uses the Agent profile form of 05.03 |
| CR-05.03 | CR-20.03 | COMP | quality requirements are integrated into existing templates whose form 05.03 defines |
| CR-05.04 | CR-05.05 | COMP | 05.05 implements the unified lifecycle in actual templates/Registry/Schema |
| CR-05.04 | CR-05.06 | COMP | current docs are mapped from legacy states to the unified lifecycle in 05.06 migration |
| CR-05.04 | CR-05.07 | COMP | 05.07 updates Reader/Validator consumers that must reflect the 05.04 lifecycle identically |
| CR-05.04 | CR-06.03 | COMP | both consume CR-05.13; 05.04 reflects it in Stage99, 06.03 owns execution-driven transition requests |
| CR-05.04 | CR-07.01 | COMP | both avoid forcing development states onto README navigation docs |
| CR-05.04 | CR-10.08 | COMP | 10.08 conformance tests exercise the lifecycle transitions and guards 05.04 unifies |
| CR-05.04 | CR-14.02 | COMP | derived Task status in README/Project is display only, consistent with no forced dev state on README |
| CR-05.05 | CR-05.06 | COMP | template changes in 05.05 must be followed by migrating consuming docs in 05.06 |
| CR-05.05 | CR-05.07 | COMP | template changes require generator/Reader/Validator/QA updates in 05.07 |
| CR-05.05 | CR-05.11 | COMP | 05.11 receipts the template change separately from doc and consumer changes |
| CR-05.05 | CR-05.13 | COMP | 05.13 says adding state words without changing transition consumers is not done; 05.05 enforces real file changes |
| CR-05.05 | CR-06.07 | COMP | SRC-SDD fields are applied by modifying the existing Spec/Plan/Task templates |
| CR-05.05 | CR-07.07 | COMP | Diataxis checks lead to template edits carried out under 05.05 |
| CR-05.05 | CR-09.06 | COMP | 09.06 applies ADR forms to the common decision template changed under 05.05 |
| CR-05.05 | CR-09.07 | COMP | 09.07 fixes the architecture description template, a 05.05 template change |
| CR-05.05 | CR-10.08 | COMP | both reject extending partial passes: deployed template vs generated doc mismatch not hidden |
| CR-05.05 | CR-20.03 | COMP | quality requirements integration edits existing templates under 05.05 |
| CR-05.06 | CR-05.07 | COMP | template migration: 05.06 inventories applied docs, 05.07 updates generators/readers/validators |
| CR-05.06 | CR-05.13 | COMP | lifecycle contract migration must close template-to-all-applied-docs mapping that 05.06 inventories |
| CR-05.06 | CR-07.07 | COMP | Diataxis template edits must also update current applied docs per 05.06 |
| CR-05.06 | CR-09.06 | COMP | decision template change must carry to all current ADRs |
| CR-05.06 | CR-09.07 | COMP | architecture template and area docs changed together |
| CR-05.06 | CR-10.08 | COMP | conformance tests reject template version vs generated doc mismatch |
| CR-05.07 | CR-05.11 | COMP | consumer updates get their own receipt separate from template change |
| CR-05.07 | CR-05.13 | COMP | lifecycle migration reuses the frozen-history read adapter rule |
| CR-05.07 | CR-08.05 | COMP | both forbid rewriting frozen historical bodies into the new form |
| CR-05.07 | CR-10.04 | COMP | validator/schema changes need positive and negative regression |
| CR-05.07 | CR-10.08 | COMP | integrated conformance tests cover generator output and reader parsing |
| CR-05.08 | CR-05.09 | COMP | renumbering needs the old-to-new identity table |
| CR-05.08 | CR-05.10 | COMP | 05.10 defines the generation that makes 05.08 run once |
| CR-05.08 | CR-05.12 | COMP | 05.12 must not silently change the 0001 conversion |
| CR-05.08 | CR-05.13 | COMP | lifecycle acceptance tests unnecessary renumbering on routine change |
| CR-05.08 | CR-06.10 | COMP | renumbering is one change class needing minimal SDD scope |
| CR-05.08 | CR-07.04 | COMP | renumbering requires relative path and anchor rechecks |
| CR-05.08 | CR-14.03 | COMP | projections must keep references valid after number migration |
| CR-05.09 | CR-05.10 | COMP | generation identity and old-to-new mapping are one conversion record |
| CR-05.09 | CR-07.04 | COMP | historical citations use exact repo/commit/path/ID identity |
| CR-05.09 | CR-14.03 | COMP | projection references updated after number migration |
| CR-05.10 | CR-05.12 | COMP | source adoption must not alter the completed 0001 generation |
| CR-05.10 | CR-05.13 | COMP | lifecycle acceptance includes resume and no repeat renumbering |
| CR-05.11 | CR-05.13 | COMP | ledger PASS/FAIL is §4 status and never replaces doc approved/active |
| CR-05.11 | CR-06.04 | COMP | per-duty receipts are Evidence records |
| CR-05.11 | CR-10.07 | COMP | partial pass is not counted as completion |
| CR-05.12 | CR-05.13 | COMP | both feed the Stage99 registry/contracts, one source mapping, one lifecycle |
| CR-05.12 | CR-09.05 | COMP | C4 guidance mapped into templates; C4 views implemented in area docs |
| CR-05.12 | CR-15.13 | COMP | agency-agents role sections map into the common role form |
| CR-05.12 | CR-17.02 | COMP | memory body guidance vs memory tier field definitions |
| CR-05.13 | CR-06.01 | COMP | document roles and their lifecycle meanings |
| CR-05.13 | CR-06.06 | COMP | human acceptance is a separate axis from document approval |
| CR-05.13 | CR-06.08 | COMP | Plan regeneration must protect decision basis and real execution history |
| CR-05.13 | CR-07.01 | COMP | README lifecycle need judged per role without forced work status |
| CR-05.13 | CR-07.05 | COMP | Guide/Runbook/Incident lifecycle meanings vs ops doc consolidation |
| CR-05.13 | CR-07.07 | COMP | Diataxis docs not forced into dev approval gates |
| CR-05.13 | CR-08.07 | COMP | lifecycle meaning vs archive disposal transition; no archiving on Task completion alone |
| CR-05.13 | CR-09.06 | COMP | ADR proposed/accepted/superseded meaning vs ADR template lineage checks |
| CR-05.13 | CR-21.04 | COMP | 05.13 defers approval authority to CR-03/21 |
| CR-06.01 | CR-06.02 | COMP | Task role in SDD chain and its sole execution writer |
| CR-06.01 | CR-06.07 | COMP | SDD source fields refine the document roles |
| CR-06.01 | CR-06.10 | COMP | document roles scaled per change class |
| CR-06.01 | CR-14.01 | COMP | Issue/Spec/Task/Project role split extends doc roles |
| CR-06.02 | CR-06.03 | COMP | Task owns execution; 06.03 links results to transition requests |
| CR-06.02 | CR-06.05 | COMP | progress and blocking written immediately to the Task |
| CR-06.02 | CR-06.06 | COMP | acceptance judgment recorded in Task, decided by acceptor |
| CR-06.02 | CR-06.07 | COMP | tasks.md generation must not overwrite Task state |
| CR-06.02 | CR-06.08 | COMP | regeneration preserves Task results and history |
| CR-06.02 | CR-15.12 | COMP | agent persona does not acquire Task state writer |
| CR-06.02 | CR-15.13 | COMP | harness records execution in the Task |
| CR-06.02 | CR-15.14 | COMP | stale runs must not overwrite Task completion |
| CR-06.02 | CR-17.01 | COMP | Task/pointer/handoff do not replace memory body and vice versa |
| CR-06.02 | CR-17.11 | COMP | observation/handoff not a new Task writer |
| CR-06.02 | CR-19.02 | COMP | diagnostic files not a second Task writer |
| CR-06.03 | CR-06.04 | COMP | transitions link to evidence; 06.04 defines the evidence record itself |
| CR-06.03 | CR-06.05 | COMP | Task progress updates feed transition requests; neither rewrites past approvals |
| CR-06.03 | CR-06.06 | COMP | 06.03 links transition to acceptance; 06.06 has acceptor decide per item from evidence |
| CR-06.03 | CR-06.07 | COMP | Task implementation_state/owner_acceptance fields carry the transition/acceptance split |
| CR-06.03 | CR-06.08 | COMP | both stop tooling from fabricating or overwriting approval/acceptance facts |
| CR-06.03 | CR-06.09 | COMP | SDD tool output not a substitute for status transitions/approval; same boundary |
| CR-06.03 | CR-06.10 | COMP | cancellation/successor transfer: 06.03 aligns rules, 06.10 tests negative cases |
| CR-06.03 | CR-08.07 | COMP | doc archival kept separate from Task completion; 08.07 bars moves by completed string |
| CR-06.03 | CR-09.06 | COMP | ADR accepted status needs approver evidence; consumes status dictionary, no fabricated acceptance |
| CR-06.03 | CR-15.14 | COMP | stale harness results must not overwrite Task completion/approval/acceptance |
| CR-06.03 | CR-17.11 | COMP | memory observations/handoff cannot become writer of approval/acceptance |
| CR-06.03 | CR-21.02 | COMP | automated checks/status never stand in for human acceptance |
| CR-06.03 | CR-21.04 | COMP | separate approval kinds: Spec approval vs remote integration vs activation |
| CR-06.04 | CR-06.05 | COMP | evidence history kept; realignment never rewrites past evidence |
| CR-06.04 | CR-06.06 | COMP | acceptor reads evidence records defined by 06.04 |
| CR-06.04 | CR-06.07 | COMP | Task verification_evidence field maps onto Evidence record contract |
| CR-06.04 | CR-06.08 | COMP | regeneration must preserve Evidence and failure history defined by 06.04 |
| CR-06.04 | CR-06.09 | COMP | verification row ends in Task Evidence per 06.04 fields |
| CR-06.04 | CR-06.10 | COMP | acceptance test requires per-criterion evidence and failure history |
| CR-06.04 | CR-07.04 | COMP | historical evidence citations need exact repo/commit/path like evidence locations |
| CR-06.04 | CR-08.05 | COMP | current docs cite evidence by version/path; matches evidence location rule |
| CR-06.04 | CR-10.07 | COMP | skipped/cached results not guarantees; evidence must record real execution |
| CR-06.04 | CR-11.02 | COMP | past results of removed checks preserved in existing Evidence |
| CR-06.04 | CR-15.13 | COMP | harness trace uses existing Task/Evidence, no second ledger |
| CR-06.04 | CR-19.03 | COMP | sanitized evidence promotion with source version, no secret copies |
| CR-06.05 | CR-06.06 | COMP | post-completion rules moved to current owner docs after realignment |
| CR-06.05 | CR-06.07 | COMP | drift correction of Spec/Plan/Architecture after implementation |
| CR-06.05 | CR-06.09 | COMP | SDLC linkage relies on docs realigned after implementation |
| CR-06.05 | CR-06.10 | COMP | new investigation facts synced to Spec/Plan/Architecture complements post-impl realignment |
| CR-06.05 | CR-07.03 | COMP | realigned ops/agent docs must give direct current guidance |
| CR-06.05 | CR-08.05 | COMP | neither rewrites frozen past approvals/evidence; current meaning moved forward |
| CR-06.05 | CR-09.03 | COMP | stale technical descriptions updated to match actual changes |
| CR-06.06 | CR-06.07 | COMP | Task owner_acceptance field records acceptor decisions |
| CR-06.06 | CR-06.08 | COMP | checklist reviewer judgment kept distinct from implementation completion |
| CR-06.06 | CR-06.09 | COMP | verification/acceptance-prep row feeds acceptor decision |
| CR-06.06 | CR-06.10 | COMP | acceptance test needs acceptance decisions and successor transfer cases |
| CR-06.06 | CR-07.03 | COMP | both ban past-Spec links replacing current explanation; 06.06 transfer, 07.03 writing |
| CR-06.06 | CR-08.05 | COMP | still-valid meaning moved to current owner docs at completion and at deletion |
| CR-06.06 | CR-21.02 | COMP | automation/QA status never replaces human owner acceptance |
| CR-06.07 | CR-06.09 | COMP | SDD field mapping implements spec/plan/task rows of SDLC table |
| CR-06.08 | CR-06.09 | COMP | external SDD tool output never replaces transitions/approval/Archive |
| CR-06.08 | CR-07.03 | COMP | constitution as controlled derivation of the single common norm source |
| CR-06.08 | CR-15.01 | COMP | constitution folds into common .agents norms, no separate writer |
| CR-06.08 | CR-18.01 | COMP | 1-4 hour examples not deadlines applies general no-timebox rule |
| CR-06.08 | CR-21.04 | COMP | CLI install/force init only within confirmed permission scope |
| CR-06.09 | CR-06.10 | COMP | stage linkage table vs change-class minimal artifacts; both iterative, not waterfall |
| CR-06.09 | CR-08.07 | COMP | termination row defers to CR-08 archival transition and verification |
| CR-06.09 | CR-15.13 | COMP | execution automation owned by CR-15 harness inside SDLC/SDD stages |
| CR-06.10 | CR-08.06 | COMP | archive/renumber change class handled inside current Task with minimal artifacts |
| CR-06.10 | CR-10.04 | COMP | doc-only changes get limited checks matching minimal scope |
| CR-06.10 | CR-10.08 | COMP | after initial adoption only changed contracts and consumers revalidated |
| CR-06.10 | CR-12.05 | COMP | no unnecessary deployment/QA beyond change risk |
| CR-06.10 | CR-14.02 | COMP | single writer per execution state matches Task as status source |
| CR-06.10 | CR-21.04 | COMP | emergency fixes still respect approval scopes |
| CR-07.01 | CR-07.02 | COMP | README classification plus Korean language rule for README |
| CR-07.01 | CR-07.03 | COMP | README role classification vs direct current guidance in README |
| CR-07.01 | CR-07.04 | COMP | README parent/child navigation vs link delegation boundaries |
| CR-07.01 | CR-07.07 | COMP | README role axis vs reader-goal axis kept separate |
| CR-07.01 | CR-19.01 | COMP | workspace READMEs are one README class written to 07.01 roles |
| CR-07.03 | CR-07.04 | COMP | 07.04 refines link boundaries and cites 07.03 for controlled derivation |
| CR-07.03 | CR-07.05 | COMP | single current procedure instead of repeats across ops docs |
| CR-07.03 | CR-07.07 | COMP | current procedures kept direct; background linked to purpose owners |
| CR-07.03 | CR-15.03 | COMP | model names not independently authored in multiple norm docs |
| CR-07.03 | CR-15.10 | COMP | provider skill copies not independent sources; controlled derivation |
| CR-07.03 | CR-15.12 | COMP | native role conversions derived from one common role source |
| CR-07.03 | CR-15.13 | COMP | native adapters as derived from common body with load checks |
| CR-07.04 | CR-07.06 | COMP | doc paths/anchors: link boundary rules plus correction of wrong 98/99 path notation |
| CR-07.04 | CR-08.01 | COMP | current citation eligibility of archive content complements historical-citation link rules |
| CR-07.04 | CR-08.04 | COMP | post-deletion citation/loader checks complement link and historical-source rules |
| CR-07.04 | CR-08.07 | COMP | archival transition switches current references; 07.04 sets the link/historical citation boundary |
| CR-07.04 | CR-09.03 | COMP | Req-Arch-ADR-Spec-Task traceability links match 07.04 Stage01-03 relationship row |
| CR-07.04 | CR-09.07 | COMP | arch docs link C4/ADR instead of copying, consistent with 07.04 no full re-authoring |
| CR-07.04 | CR-10.04 | COMP | doc content checks (links/relations) implement 07.04 negative link tests without full QA gate |
| CR-07.04 | CR-10.08 | COMP | 07.04 link/Reader negative tests fit into existing conformance tests of 10.08 |
| CR-07.04 | CR-19.01 | COMP | workspace READMEs must give direct current content per 07.04 README rule |
| CR-07.04 | CR-19.03 | COMP | evidence citations must be persistently accessible, matching historical citation rule |
| CR-07.05 | CR-07.07 | COMP | Runbook/Guide procedures: consolidation plus reader-mode completeness checks |
| CR-07.05 | CR-08.05 | COMP | still-needed meaning moves into ops docs; 07.05 prevents proliferation of ops docs |
| CR-07.05 | CR-08.07 | COMP | archival keeps valid ops guidance classified; 07.05 consolidates ops doc set |
| CR-07.07 | CR-10.04 | COMP | doc QA: 07.07 adds reader-scenario checks beyond 10.04 profile/link content checks |
| CR-08.01 | CR-08.02 | COMP | archive area: scheme survey and archive logical disposition units |
| CR-08.01 | CR-08.03 | COMP | archive area: unified scheme feeds payload removal |
| CR-08.01 | CR-08.04 | COMP | archive area: scheme survey and archive isolated restore test |
| CR-08.01 | CR-08.05 | COMP | archive area: scheme survey and archive current-meaning migration |
| CR-08.01 | CR-08.06 | COMP | archive area: survey and keeping disposition inside current Task |
| CR-08.01 | CR-08.07 | COMP | archive area: unified scheme used by dev-doc archival transition |
| CR-08.01 | CR-09.06 | COMP | ADR lineage reconciles with CR-08 archive scheme and citation rules |
| CR-08.02 | CR-08.04 | COMP | disposition unit checks and restore test both precede deletion |
| CR-08.02 | CR-08.05 | COMP | disposition units and migration of still-needed meaning |
| CR-08.02 | CR-08.06 | COMP | disposition units processed within current Task |
| CR-08.03 | CR-10.08 | COMP | conformance tests check archive non-regeneration that 08.03 requires |
| CR-08.03 | CR-21.04 | COMP | payload deletion needs approved units; 21.04 separates data-deletion approval and forbids history rewrite |
| CR-08.04 | CR-08.05 | COMP | restore test and meaning migration both before payload removal |
| CR-08.04 | CR-08.06 | COMP | restore checks executed inside current Task |
| CR-08.05 | CR-08.06 | COMP | meaning migration done within current Task |
| CR-08.05 | CR-09.06 | COMP | both forbid rewriting frozen past approvals; ADR lineage preserved |
| CR-08.06 | CR-10.08 | COMP | archive checks integrated into existing tests, no new permanent pipeline |
| CR-08.06 | CR-11.01 | COMP | 08.06 routes one-off archive checks to CR-11 detection |
| CR-08.06 | CR-11.03 | COMP | archive-specific fixture cleanup handed to CR-11 fixture consolidation |
| CR-08.06 | CR-11.05 | COMP | migration-only tools removed after completion per 11.05 records |
| CR-08.07 | CR-09.06 | COMP | reopening history via new version; ADR supersession keeps old decisions intact |
| CR-08.07 | CR-10.08 | COMP | conformance tests cover forbidden transitions and archive regeneration from 08.07 |
| CR-08.07 | CR-14.02 | COMP | document archival not triggered by completed string; Task stays execution status source |
| CR-08.07 | CR-21.04 | COMP | different archive policy needs explicit change approval; 21.04 approval scopes |
| CR-09.01 | CR-09.02 | COMP | area Req/Arch docs: inventory complemented by Req/Arch content fields |
| CR-09.01 | CR-09.03 | COMP | area Req/Arch docs: inventory complemented by area traceability chain |
| CR-09.01 | CR-09.04 | COMP | area Req/Arch docs: inventory complemented by per-project area surveys |
| CR-09.01 | CR-09.05 | COMP | area Req/Arch docs: inventory complemented by C4 architecture views |
| CR-09.01 | CR-09.06 | COMP | area Req/Arch docs: inventory complemented by ADR template and lineage |
| CR-09.02 | CR-09.03 | COMP | area Req/Arch docs: content items vs their trace to code/tests |
| CR-09.02 | CR-09.04 | COMP | area docs: required content vs per-area survey that fills it |
| CR-09.02 | CR-09.05 | COMP | Architecture content: structure/deployment items realised by C4 views |
| CR-09.02 | CR-09.06 | COMP | Architecture alternatives/decisions item links to ADR records |
| CR-09.02 | CR-09.07 | COMP | architecture content list checked against arc42 12 viewpoints |
| CR-09.02 | CR-20.03 | COMP | quality requirements integrated into existing Req/Arch docs/templates |
| CR-09.03 | CR-09.04 | COMP | area trace and per-area survey; both separate code observation from real-env facts |
| CR-09.03 | CR-09.05 | COMP | C4 elements linked to code/Compose/GitOps as part of area trace |
| CR-09.03 | CR-09.06 | COMP | ADR decision log linked into Req/Spec/Arch trace |
| CR-09.03 | CR-09.07 | COMP | both separate intent/design/code/real-env observation in architecture docs |
| CR-09.03 | CR-12.05 | COMP | static observation vs real-env confirmation; doc trace vs CI acceptance scope |
| CR-09.03 | CR-20.02 | COMP | trace chain extended with quality metrics; observed vs proposed separated |
| CR-09.04 | CR-09.05 | COMP | per-area survey of Compose/GitOps feeds C4 deployment links |
| CR-09.04 | CR-09.07 | COMP | active-area survey supplies the two docs arc42 acceptance requires |
| CR-09.04 | CR-12.05 | COMP | same no-static-closure principle; area infra acceptance vs CI env acceptance scopes |
| CR-09.04 | CR-20.02 | COMP | same four areas: survey vs area-specific quality metrics |
| CR-09.04 | CR-21.04 | COMP | both limit blocking to the affected scope only |
| CR-09.05 | CR-09.07 | COMP | arc42 structure/runtime/deployment views link to C4, no duplication |
| CR-09.05 | CR-12.05 | COMP | no PASS without runtime access for relation facts; aligns with env acceptance |
| CR-09.06 | CR-09.07 | COMP | arc42 section 9 decisions links to ADR as canonical decision record |
| CR-09.06 | CR-13.07 | COMP | branch strategy choice/alternatives recorded as a decision |
| CR-09.06 | CR-14.03 | COMP | one-time renumbering: ADR 0001 transition vs references after number migration |
| CR-09.07 | CR-20.03 | COMP | no giant doc or new gate; quality folded into existing templates |
| CR-10.01 | CR-10.04 | COMP | renamed repeat checks on same input; call graph identifies them |
| CR-10.01 | CR-10.05 | COMP | call graph stage leaves feed the per-stage check matrix |
| CR-10.01 | CR-10.07 | COMP | call graph leaf assertions vs result semantics of skipped/cached checks |
| CR-10.01 | CR-11.01 | COMP | 10.01 re-review of obsolete temporary QA vs 11.01 legacy detection |
| CR-10.01 | CR-11.02 | COMP | call graph callers/registrations used when retiring one-off checks |
| CR-10.01 | CR-11.03 | COMP | fixtures traced as graph leaves vs fixture consolidation |
| CR-10.01 | CR-11.04 | COMP | graph-based duplicate leaves and impact selection vs optimization order |
| CR-10.01 | CR-11.05 | COMP | caller counts from call graph back disposition records |
| CR-10.01 | CR-12.03 | COMP | remote approved commit vs local checkout kept distinct in both |
| CR-10.01 | CR-13.03 | COMP | hook registration vs actual invocation; native vs Git hook duplicates |
| CR-10.01 | CR-15.05 | COMP | provider hooks traced in call graph vs native hook registration tests |
| CR-10.02 | CR-10.04 | COMP | check identity by input; no renamed repeat on same input |
| CR-10.02 | CR-10.05 | COMP | independent checks per stage justified by differing input/trust |
| CR-10.02 | CR-10.06 | COMP | duplicate removal relies on input/guarantee identity |
| CR-10.02 | CR-10.07 | COMP | result reuse needs equivalence of the same identity attributes |
| CR-10.02 | CR-11.04 | COMP | identity attributes justify narrow result reuse step |
| CR-10.03 | CR-10.05 | COMP | explicit formatter at edit stage vs check never writing |
| CR-10.03 | CR-13.04 | COMP | hook worktree impact tests vs checks not modifying sources/index |
| CR-10.04 | CR-10.05 | COMP | doc vs validator change classes in the stage matrix |
| CR-10.04 | CR-10.06 | COMP | no renamed repeat runs vs duplicate removal |
| CR-10.04 | CR-12.05 | COMP | doc-only changes get limited checks, no blanket deploy |
| CR-10.05 | CR-10.06 | COMP | stage matrix defines where duplicates are removed |
| CR-10.05 | CR-11.04 | COMP | change-class matrix enables change-impact selection |
| CR-10.05 | CR-12.01 | COMP | stage matrix vs per-repo execution location roles |
| CR-10.05 | CR-12.03 | COMP | PR/main candidate stages vs remote required check binding |
| CR-10.05 | CR-12.05 | COMP | build/deploy stage env checks; doc-only not forced to deploy |
| CR-10.05 | CR-13.02 | COMP | pre-commit stage checks actual message; commit-msg validation |
| CR-10.05 | CR-13.07 | COMP | per-branch QA responsibility vs per-stage matrix |
| CR-10.06 | CR-11.02 | COMP | duplicate removal vs retiring one-off checks after moving guarantees |
| CR-10.06 | CR-11.05 | COMP | removal decisions recorded with guarantee and consumer |
| CR-10.06 | CR-12.03 | COMP | local vs server checks differ in trust; not removed as duplicates |
| CR-10.06 | CR-13.03 | COMP | installed hook plus manual pre-run and native/Git hook duplicates |
| CR-10.06 | CR-13.04 | COMP | duplicate hook execution prevention |
| CR-10.07 | CR-10.08 | COMP | missing/failed required check propagation tested in conformance suite |
| CR-10.07 | CR-12.05 | COMP | skipped/partial not completion; acceptance needs env results |
| CR-10.07 | CR-13.04 | COMP | failure exit code propagation in hooks vs result semantics |
| CR-10.07 | CR-18.02 | COMP | both forbid treating failed/unrun required checks as success |
| CR-10.08 | CR-11.03 | COMP | minimal normal/error inputs vs fixture consolidation keeping min inputs |
| CR-10.08 | CR-11.05 | COMP | initial adoption scope vs removing migration-only tools afterwards |
| CR-10.08 | CR-12.05 | COMP | spec static checks not reused as real repo/host evidence |
| CR-10.08 | CR-14.02 | COMP | Task writer duplication tested vs Task as single status source |
| CR-10.08 | CR-14.03 | COMP | Task writer duplication tested vs no second execution writer |
| CR-11.01 | CR-11.02 | COMP | detect one-off checks vs retire them after moving guarantees |
| CR-11.01 | CR-11.03 | COMP | detect obsolete fixtures vs consolidate fixtures |
| CR-11.01 | CR-11.04 | COMP | detect duplicates/overreach vs optimization order |
| CR-11.01 | CR-11.05 | COMP | detection candidates vs per-candidate disposition records |
| CR-11.02 | CR-11.03 | COMP | closed-task check removal and unneeded fixture disposal are complementary cleanup steps |
| CR-11.02 | CR-11.04 | COMP | duplicate leaf removal in optimization order complements migrating/removing retired checks |
| CR-11.02 | CR-11.05 | COMP | 11.05 records disposition and caller=0 removal for the same cleanup candidates 11.02 migrates |
| CR-11.02 | CR-19.03 | COMP | past check results kept in existing Evidence; 19.03 governs how evidence is promoted |
| CR-11.03 | CR-11.04 | COMP | fixture consolidation feeds the QA optimization order |
| CR-11.03 | CR-11.05 | COMP | fixture dispositions recorded per candidate with consumer analysis |
| CR-11.03 | CR-16.04 | COMP | QA fixture consolidation vs excessive fixture cleanup inside skill bundles |
| CR-11.04 | CR-15.14 | COMP | avoiding needless full QA on harness resume aligns with impact selection |
| CR-11.04 | CR-18.03 | COMP | reusable deterministic receipts and no full build loops align with narrow result reuse |
| CR-11.04 | CR-20.03 | COMP | both forbid adding large new gates; complementary |
| CR-11.05 | CR-16.04 | COMP | QA disposition records vs bundle-level validation and fixture cleanup |
| CR-12.01 | CR-12.02 | COMP | runner role targets checked against inspected runner registration and protection |
| CR-12.01 | CR-12.03 | COMP | runner locations vs binding check results to candidate |
| CR-12.01 | CR-12.04 | COMP | self-hosted runner placement vs its trust isolation |
| CR-12.01 | CR-12.05 | COMP | location roles vs closing acceptance with that environment's results |
| CR-12.02 | CR-12.03 | COMP | protection inspection vs required-check binding to latest candidate |
| CR-12.02 | CR-12.05 | COMP | 403/404 distinct from absence; access failure not replaced by static reading |
| CR-12.02 | CR-13.07 | COMP | 13.07 states protection inspection does not replace strategy evaluation |
| CR-12.03 | CR-12.04 | COMP | candidate result binding vs base tool/candidate input separation |
| CR-12.03 | CR-12.05 | COMP | both separate local success from remote/required results |
| CR-12.03 | CR-15.14 | COMP | both forbid stale results standing in for a new candidate/version |
| CR-12.03 | CR-21.02 | COMP | required checks/Apps do not replace human acceptance |
| CR-12.04 | CR-12.05 | COMP | isolated inputs preferred while env acceptance closes with real env results |
| CR-12.04 | CR-13.06 | COMP | SLSA provenance/artifact lineage vs verifying release source and assets |
| CR-12.04 | CR-15.13 | COMP | malicious PR metadata tests vs harness prompt-injection/privilege-escalation tests |
| CR-12.04 | CR-21.05 | COMP | untrusted PR metadata negative tests vs external text as data, injection tests |
| CR-12.05 | CR-15.14 | COMP | unobservable features stay unverified, not replaced by mocks or static reads |
| CR-13.01 | CR-13.02 | COMP | commit units vs message format |
| CR-13.01 | CR-13.07 | COMP | commit/Spec integration path vs branch strategy evaluation |
| CR-13.01 | CR-15.11 | COMP | no forced reset/stash vs no broad forced removal or history rewrite |
| CR-13.02 | CR-13.03 | COMP | commit-msg format vs hook installation/invocation |
| CR-13.02 | CR-13.04 | COMP | actual commit-msg input checked vs hook stdin/argument propagation tests |
| CR-13.02 | CR-13.05 | COMP | standard messages feed SemVer/changelog production |
| CR-13.02 | CR-21.02 | COMP | no false approval text in generated messages vs no fake independent approval |
| CR-13.03 | CR-13.04 | COMP | hook config/invocation inspection vs isolated propagation tests |
| CR-13.03 | CR-15.04 | COMP | global/local Git config scope vs agent settings scope; personal changes need separate permission |
| CR-13.05 | CR-13.06 | COMP | single release producer vs immutable release publication order |
| CR-13.05 | CR-13.07 | COMP | main release PR changelog vs branch-release relationship evaluation |
| CR-14.01 | CR-14.02 | COMP | ownership split of Issue/Spec/Task/Project vs Task as status source |
| CR-14.01 | CR-14.03 | COMP | projection roles vs sync tests |
| CR-14.01 | CR-15.13 | COMP | both define Task as actual execution state |
| CR-14.02 | CR-15.12 | COMP | persona/memory text gains no Task status writer; consistent single writer |
| CR-14.02 | CR-15.13 | COMP | harness records in existing Task without a second state writer |
| CR-14.02 | CR-15.14 | COMP | resume must not clone a new state source; Task stays source |
| CR-14.02 | CR-17.01 | COMP | Task is execution source; pointers/handoff do not replace it or memory |
| CR-14.02 | CR-17.11 | COMP | observation/handoff never become Task status writers |
| CR-14.02 | CR-19.02 | COMP | diagnostic files are not second Task writers |
| CR-14.03 | CR-15.14 | COMP | stale/derived results must not overwrite Task facts |
| CR-14.03 | CR-18.05 | COMP | projection retry handling should respect retry budget and cancellation policy |
| CR-15.01 | CR-15.02 | COMP | native support table feeds the common/native split; both deny file names as activation proof |
| CR-15.01 | CR-15.03 | COMP | model names kept out of multi-doc authoring, mirroring single common source rule |
| CR-15.01 | CR-15.12 | COMP | common role source with native conversions follows the common/native split |
| CR-15.01 | CR-15.13 | COMP | harness keeps .agents as common meaning and native config as loading |
| CR-15.01 | CR-15.14 | COMP | acceptance test repeats that native file presence is not activation |
| CR-15.01 | CR-16.04 | COMP | both require real loader proof of .agents sources; 16.04 is the broader bundle e2e |
| CR-15.02 | CR-15.04 | COMP | settings files listed in support table vs settings scope/precedence survey |
| CR-15.02 | CR-15.05 | COMP | hooks rows in support table vs hook registration and merge tests |
| CR-15.02 | CR-15.12 | COMP | `agents/*.md` and `*.toml` support rows vs role conversion native load check |
| CR-15.02 | CR-15.14 | COMP | same file to loader to behavior verification chain; support table vs acceptance test |
| CR-15.02 | CR-16.04 | COMP | native path support vs installed loader e2e; example names not proof |
| CR-15.02 | CR-17.08 | COMP | agent-memory files in support table vs identifying and stopping native memory |
| CR-15.04 | CR-15.09 | COMP | settings scope survey vs effective permission composition tests |
| CR-15.04 | CR-15.11 | COMP | personal exceptions not copied to shared settings vs personal files untracked |
| CR-15.05 | CR-15.13 | COMP | hook registration vs harness blocking affected writes when a required hook does not run |
| CR-15.05 | CR-16.04 | COMP | hook registration tests vs e2e check that hooks touch only expected areas |
| CR-15.05 | CR-18.02 | COMP | hook recursion/failure tests vs no Stop-hook infinite restart |
| CR-15.06 | CR-16.04 | COMP | MCP survey vs e2e check of MCP connection boundaries |
| CR-15.06 | CR-18.04 | COMP | both: unused service is grounded N/A and nothing new is added to satisfy the survey |
| CR-15.08 | CR-18.04 | COMP | both survey cost and forbid introducing a new API without need |
| CR-15.08 | CR-21.02 | COMP | auto PR check survey vs verification that review path has no banned calls |
| CR-15.09 | CR-15.14 | COMP | effective-permission composition vs acceptance chain ending in effective permission |
| CR-15.09 | CR-16.04 | COMP | permission composition tests vs e2e permission/sandbox boundary check |
| CR-15.09 | CR-17.08 | COMP | both forbid bypassing unsupported behavior with fake settings or broader permission |
| CR-15.09 | CR-21.03 | COMP | no broader-permission bypass vs minimal policy change without global protection removal |
| CR-15.09 | CR-21.05 | COMP | read instructions grant no permission vs file text is data, not approval |
| CR-15.10 | CR-15.14 | COMP | skill symlink support vs acceptance that symlink count alone is not proof |
| CR-15.10 | CR-16.04 | COMP | skill symlink consumption vs e2e validity of native paths and symlinks |
| CR-15.11 | CR-21.04 | COMP | both forbid forced history rewrite; tracking removal vs approval scope |
| CR-15.12 | CR-16.04 | COMP | role conversion vs bundle e2e; neither counts installing community examples as done |
| CR-15.12 | CR-21.05 | COMP | no upstream install.sh run vs external role files never grant execution |
| CR-15.13 | CR-15.14 | COMP | harness execution chain vs its resume/replay/late-result rules |
| CR-15.13 | CR-16.04 | COMP | harness entrypoint tracing vs installed loader e2e verification |
| CR-15.13 | CR-17.01 | COMP | harness keeps Task as state and memory as reuse context; Task cannot replace memory |
| CR-15.13 | CR-21.04 | COMP | both confine blocking to affected work; failed hook vs missing approval |
| CR-15.14 | CR-16.04 | COMP | acceptance and e2e both reject file presence or symlink count as completion |
| CR-15.14 | CR-17.04 | COMP | restart rechecks memory reuse eligibility defined by CR-17.04 |
| CR-15.14 | CR-18.02 | COMP | auto-resume without infinite loop vs explicit loop termination and resume conditions |
| CR-15.14 | CR-18.03 | COMP | no unnecessary full QA on resume vs no full build loops or restarts |
| CR-15.14 | CR-18.06 | COMP | unobservable features unverified vs mock results kept distinct from operations |
| CR-16.01 | CR-16.02 | COMP | status categories for ten skills vs general rule not to record unrun as run |
| CR-16.02 | CR-16.04 | COMP | no skill/subagent proliferation vs dedupe of triggers and subagents |
| CR-16.02 | CR-21.05 | COMP | record missing tools truthfully in both; skill use vs untrusted input |
| CR-16.03 | CR-16.04 | COMP | SKILL.md content vs bundle-level trigger/output validation |
| CR-17.01 | CR-17.02 | COMP | canonical store vs tier schema it must hold |
| CR-17.01 | CR-17.03 | COMP | KEEP existing store vs retention rule applied to it |
| CR-17.01 | CR-17.04 | COMP | recall eligibility is one of the gaps 17.01 names |
| CR-17.01 | CR-17.05 | COMP | capacity is one of the gaps 17.01 names |
| CR-17.01 | CR-17.06 | COMP | concurrency is one of the gaps 17.01 names |
| CR-17.01 | CR-17.07 | COMP | no pollution of personal DB vs isolated test data first; overlapping test-data clause |
| CR-17.01 | CR-17.08 | COMP | native memory boundary is one of the gaps 17.01 names |
| CR-17.01 | CR-17.11 | COMP | shared store KEEP vs SRC-MEM consumer fixes; handoff not a state writer |
| CR-17.01 | CR-19.04 | COMP | worktrees isolate outputs but use the same physical memory store |
| CR-17.02 | CR-17.03 | COMP | tiers defined vs short/long are usage classes, not deletion deadlines |
| CR-17.02 | CR-17.05 | COMP | tier schema vs per-tier capacity limits |
| CR-17.02 | CR-17.10 | COMP | tier schema vs working/episodic/semantic tier mapping in SRC-MEM audit |
| CR-17.03 | CR-17.04 | COMP | retention vs recall exclusion that keeps body preserved |
| CR-17.03 | CR-17.08 | COMP | no auto-discard vs native memory not deleted without review |
| CR-17.03 | CR-19.03 | COMP | retained memory not evidence vs evidence promotion rules |
| CR-17.03 | CR-19.04 | COMP | retention vs no removal of shared DB at worktree end |
| CR-17.04 | CR-17.09 | COMP | eligibility rule vs stale default recall blocking tests in SRC-MEM |
| CR-17.04 | CR-17.10 | COMP | eligibility vs score decay as search eligibility change, not loss |
| CR-17.04 | CR-17.11 | COMP | eligibility vs revocation and cross-project recall tests |
| CR-17.05 | CR-17.09 | COMP | capacity limits vs SRC-MEM compaction policies |
| CR-17.05 | CR-17.10 | COMP | approved lossless compaction vs SRC-MEM lossy compaction rejection |
| CR-17.05 | CR-17.11 | COMP | capacity saturation in 17.11 acceptance test |
| CR-17.06 | CR-17.07 | COMP | concurrency implementation vs engine write serialization research |
| CR-17.06 | CR-17.09 | COMP | conflicts preserved during SRC-MEM migration |
| CR-17.06 | CR-17.11 | COMP | concurrency vs alternation/concurrent-write acceptance test |
| CR-17.06 | CR-19.04 | COMP | worktree alternation vs single shared memory store |
| CR-17.07 | CR-17.09 | COMP | SQLite research vs SQLite holding real state, not just index |
| CR-17.07 | CR-17.11 | COMP | backup/restore research vs index rebuild and restore tests on isolated input |
| CR-17.08 | CR-17.09 | COMP | native independent memory writes stopped by default in both |
| CR-17.08 | CR-17.11 | COMP | native auto memory blocking vs its isolated tests |
| CR-17.09 | CR-17.11 | COMP | SRC-MEM migration vs hook/handoff scope fixes; claim-once in both |
| CR-17.09 | CR-18.06 | COMP | no paid provider calls without approval in both |
| CR-17.10 | CR-17.11 | COMP | auto-improve defaults audited vs aligned with CR-03/21 |
| CR-17.10 | CR-21.05 | COMP | external tool install not auto-permission vs untrusted input grants nothing |
| CR-18.01 | CR-18.02 | COMP | budget/limit as explicit loop end vs safety caps kept |
| CR-18.01 | CR-18.04 | COMP | billing caps kept vs cost limits researched |
| CR-18.01 | CR-18.05 | COMP | safety timeouts vs retry wait cap and hold |
| CR-18.01 | CR-18.06 | COMP | safety caps vs their negative tests |
| CR-18.02 | CR-18.03 | COMP | loop termination vs no infinite retries or restarts |
| CR-18.02 | CR-18.05 | COMP | loop termination vs retry budget and no infinite retry |
| CR-18.02 | CR-18.06 | COMP | no failure hiding vs acceptance against infinite loops and hidden failures |
| CR-18.03 | CR-18.04 | COMP | token limits researched in both scopes |
| CR-18.03 | CR-18.05 | COMP | no infinite retry in both; context vs retry policy |
| CR-18.04 | CR-18.05 | COMP | provider limits vs retry-after handling |
| CR-18.04 | CR-18.06 | COMP | cost/rate survey vs negative tests |
| CR-18.05 | CR-18.06 | COMP | retry policy vs retry negative tests |
| CR-19.01 | CR-19.02 | COMP | READMEs vs actual outputs routed to those paths |
| CR-19.02 | CR-19.03 | COMP | diagnostic output routing vs evidence promotion from it |
| CR-19.03 | CR-19.04 | COMP | evidence promotion vs moving worktree evidence to owned locations |
| CR-20.01 | CR-20.02 | COMP | ISO research vs quality requirement chain |
| CR-20.01 | CR-20.03 | COMP | ISO research vs integration without compliance claims |
| CR-20.02 | CR-20.03 | COMP | requirement chain vs template integration and non-uniform thresholds |
| CR-21.01 | CR-21.02 | COMP | API ban vs verification of no banned calls |
| CR-21.02 | CR-21.04 | COMP | human acceptance vs approval scope separation |
| CR-21.03 | CR-21.04 | COMP | policy change vs approval scopes; no false approval |
| CR-21.04 | CR-21.05 | COMP | approval scope vs file text never counts as approval |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pair coverage | 41 | W46 | Merge script: each of the 10,878 pairs once, none missing or extra, 4 columns | Ten reviewer outputs | PASS | 10,878 pairs | required | - |
| Attribute coverage | 41 | W46 | Merge script: 148 rows in request order, tags from the fixed vocabulary | Two reviewer outputs | PASS | 148 CRs | required | - |
| Metadata contracts | 41 | W46 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Runtime conflict per pair | 41 | W46 | Pairwise check of implementation against both CRs | - | NOT_RUN | Judged per line in TSK-0029 instead | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 41 | accepted | Pair coverage, Attribute coverage, Metadata contracts | All 10,878 pairs are judged; none contradicts or is unjudged; 37 duplicated duties in the request text are recorded for the owner. | SPEC-0212 TSK-0030 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Request line meaning audit](tsk-0029-request-line-meaning-audit.md)
