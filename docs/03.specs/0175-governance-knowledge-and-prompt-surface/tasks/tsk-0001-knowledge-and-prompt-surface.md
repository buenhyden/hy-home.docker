---
title: "Knowledge and Prompt Surface Execution"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0175-TSK-0001"
parent_ids:
- "SPEC-0175"
- "SPEC-0175-PLAN-0001"
created: "2026-09-06"
---

# Knowledge and Prompt Surface Execution

## Objective

Own every actual command, result, review finding, blocker, and disposition for
SPEC-0175. This Task is the sole execution and handoff authority for the
package; no second progress ledger is created.

## Inputs

- Branch `codex/0173-agent-governance-home`; investigation baseline
  `origin/main` at `8176cdee732954415bc5462d6d4d43da4e319394`; package baseline
  `9ede309a5b1feba91e6f8b973a729716b14c55ab` with a clean worktree.
- Governing owners: REQ-0024, AD-0027, ADR-0034, SPEC-0175, SPEC-0175-PLAN-0001.
- Authorization: local investigation, local edits, and local commits on this
  branch. Push, pull request, merge, deployment, live service action, secret
  values, global installation, and remote state changes are not authorized.
- Evidence classes used throughout, kept non-substitutable: `local-executed`,
  `configured`, `repository-enforced`, `official-source`, `local-parser`,
  `unverified-runtime`, `unverified-entitlement`, `unverified-remote`.

## Work Log

### Baseline verification (2026-09-06)

| Check | Command | Result |
| --- | --- | --- |
| Branch and HEAD | `git rev-parse HEAD` | `9ede309a5b1feba91e6f8b973a729716b14c55ab` on `codex/0173-agent-governance-home` |
| Remote main | `git rev-parse origin/main` | `8176cdee732954415bc5462d6d4d43da4e319394`, equal to the stated investigation baseline |
| Divergence | `git rev-list --left-right --count origin/main...HEAD` | `0 7`; the baseline is an ancestor and is not reset |
| Worktree | `git status --porcelain`, `git stash list` | empty; no other worker's state present |
| Worktrees | `git worktree list` | one entry; the existing feature branch is reused rather than creating a second isolated tree |
| Graph advisory | `graphify-out/GRAPH_REPORT.md` built from `f8a72211` | differs from HEAD, so the graph is advisory only and conclusions are corroborated against tracked sources |

### External observations (2026-09-06)

| Subject | Method | Result | Evidence class |
| --- | --- | --- | --- |
| External agent catalog upstream head | `git ls-remote` on the public repository, read-only, observed 2026-09-06T16:36:25+09:00 | `1454492577d1af4884722837f491fef14b501e21`, advanced from the pinned `ebe9c99acb5c96f9468de368d8bead775387d1a7` recorded in RES-0002-m0003 | official-source |
| `keep-coding-instructions` output-style field | Vendor documentation for output styles | Supported; default `false`; omitting it drops the provider's built-in software-engineering instructions | official-source |
| Same field in the installed CLI | String scan of the installed 2.1.263 executable | `keep-coding-instructions` and `keepCodingInstructions` both present | local-parser |
| Codex custom agent TOML fields | Vendor subagent documentation | `name`, `description`, `developer_instructions` required; `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` optional | official-source |
| Codex `skills.config` binding | Not exercised | Available but not adopted; runtime acceptance unobserved | unverified-runtime |

No clone, install, converter run, credential read, or provider call was
performed for any of the above.

### W1: Decision and durable owners

| Action | Detail |
| --- | --- |
| Created | `docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md` as `proposed` with `AD-0027` as its single Architecture Description parent |
| Amended | `REQ-0024` gains `REQ-0024-FR-0014` and relaxes FR-0003's category enumeration; version `1.1.0` to `1.2.0` |
| Amended | `AD-0027` System Boundaries and Components gain the two categories; version `1.1.0` to `1.2.0` |
| Allocated | Stage 99 identity spaces: `adr` high water 33 to 34; `REQ-0024.FR` issues 14 |
| Indexed | `docs/02.architecture/decisions/README.md` gains ADR-0033 and ADR-0034 rows; the stale hardcoded ADR count is replaced with a routing statement because a count is not a retention criterion |
| Registered | `tests/lib/document_governance/test_taxonomy.py` `ADR_TO_AD` gains `ADR-0034` to `AD-0027` |

Two findings surfaced during W1 verification and were corrected rather than
worked around:

1. `check-agent-governance-contract.py` reported `AGC-UNSUPPORTED-TOKEN` on the
   new ADR because its Context section spelled the retired shared progress
   ledger's path. The guard is correct; the prose was rewritten to describe the
   retired surface without naming its path. The pattern was not weakened.
2. `test_stage_02_adr_filename_metadata_and_parent_agree_exactly` failed because
   the new ADR declared a Requirement parent. Every tracked ADR uses an
   Architecture Description parent and the decisions index states that rule, so
   the ADR's `parent_ids` was corrected to `AD-0027` and the enumerated
   `ADR_TO_AD` contract was extended. The Requirement remains linked from the
   ADR's Traceability section.

A forward link from ADR-0034 to `spec.md` was deliberately withheld from this
unit because the target does not exist until W2; `check-document-links.py
--mode all` reported `missing-link-target` when it was present, which is the
guard behaving correctly.

### W1 gate rejection and correction (2026-09-06)

The first `git commit` attempt was rejected by the pre-commit public gate:

```text
FAIL: stale generated LLM Wiki output: docs/90.references/data/0082-llm-wiki-index/README.md
FAIL: stale generated LLM Wiki output: docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md
```

The standalone `run-ci-gate.py --profile changed` had reported both outputs
fresh eight minutes earlier, at 17:08:20, against the same file contents. The
difference is staging: `scripts/knowledge/generate-llm-wiki.py:287` builds its
inventory with `git ls-files --cached`, so the new ADR was invisible to the
generator while it was untracked and entered the inventory only at `git add`
(index mtime 17:11:28). A freshness check on an unstaged tree is a false green.

Correction: regenerate with `--write`, verify `--check` passes against the
staged tree, and carry both regenerated outputs in the same commit as the
document that changed them. That matches commit `150b15614`, which added
ADR-0033 and carried the regenerated index in the same logical unit. The
generated bodies were not hand-edited. The regenerated diff is exactly the new
document's arrival: safe tracked paths 1018 to 1019, `docs/02.architecture` 56
to 57, active stage docs 83 to 84, Markdown reference 568 to 569, plus one
index row.

This operational fact is carried into the canonical verification surface map
when W7 creates it, so the next session does not rediscover it.

### W2 plan correction (2026-09-06, local-executed)

The Plan's original W2 split the package into four commits so the Spec could
walk `draft` to `active` inside this branch. That walk is not reachable. Setting
the Spec to `review` and the Task to `ready` and running the changed-mode
metadata check returned:

```text
metadata base: source=local:origin/main ref=origin/main merge_base=8176cdee732954415bc5462d6d4d43da4e319394
docs/03.specs/0175-governance-knowledge-and-prompt-surface/spec.md: invalid-initial-status: new spec documents must start at draft
docs/03.specs/0175-governance-knowledge-and-prompt-surface/tasks/tsk-0001-knowledge-and-prompt-surface.md: invalid-initial-status: new task documents must start at draft
metadata check-changed: selected=19 violations=2 legacy_exceptions=0 transition_overrides=0
```

`previous_status` is read from the merge base, not from the previous commit, so
splitting the transitions across commits changes nothing. `git show
8176cdee:docs/03.specs/0173-governance-qa-surface-convergence/spec.md` returns
`status: "active"`, which is why the comparison package is exempt: it predates
the merge base. `scripts/lib/gate/ci_gate_contract.py` invokes the check with
`("--mode", "check-changed")` only, so `--transition-override-file` is
unreachable from the gate.

The transitions were reverted with `git checkout HEAD -- docs/03.specs/`, the
working tree returned to clean, and W2b through W2d were removed from the Plan.
The package remains at `draft` for this branch. Every later work unit in this
Task therefore executes under a `draft` package, and this entry is the recorded
reason.

### W4: Stage 99 registration (2026-09-06, local-executed)

Registered four profiles, two template roles, four `living` transitions, two
copyable template sources, and the two catalog rows. `registry.json` round-trips
byte-identically under `json.dumps(data, indent=2, ensure_ascii=False) + "\n"`
before and after, so the edit is a minimal diff rather than a reformat.

RED before GREEN, without a commit that carries a failing test: the assertion's
own logic was run against the registry as stored at `HEAD` and against the
working tree.

```text
HEAD (before W4): failures=4
  governance-knowledge: profile is not registered
  governance-knowledge-index: profile is not registered
  governance-prompt: profile is not registered
  governance-prompt-index: profile is not registered
working tree (after W4): failures=0
```

The assertion then landed in
`tests/lib/agent_governance/test_agent_governance_contract.py` as
`test_knowledge_and_prompt_profiles_are_registered`.
`python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract`
returns `Ran 38 tests` `OK`.

The `GOVERNANCE_PROFILES` subset assertion is deliberately not here.
`agent_governance_contract.py:973` reads that set with `issubset`, so the
registry may register a profile the contract has not yet admitted, but not the
reverse. That assertion ships in W5, the commit that admits the roots.

## Verification Evidence

### W1 focused checks (2026-09-06, local-executed)

| Command | Exit | State |
| --- | --- | --- |
| `git diff --check` | 0 | PASS |
| `python3 scripts/validation/check-document-metadata.py` | 0 | PASS |
| `python3 scripts/validation/check-document-links.py --mode all` | 0 | PASS, 697 documents, 5966 links, 0 failures |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | 0 | PASS, 0 violations |
| `python3 scripts/validation/check-agent-governance-contract.py --mode repository` | 0 | PASS, 0 failures |
| `python3 scripts/operations/provider_surface_renderer.py --check` | 0 | PASS, 2 providers, 0 drift |
| `python3 -m unittest tests.lib.document_governance.test_taxonomy` | 0 | PASS, 18 tests |

Acceptance mapping is completed before package completion, not per work unit.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3, W5 | NOT_RUN | pending |
| 2 | W4 | NOT_RUN | pending |
| 3 | W4 | NOT_RUN | pending |
| 4 | W7 | NOT_RUN | pending |
| 5 | W6 | NOT_RUN | pending |
| 6 | W5 | NOT_RUN | pending |
| 7 | W8 | NOT_RUN | pending |
| 8 | W3, W9 | NOT_RUN | pending |
| 9 | W9 | NOT_RUN | pending |
| 10 | W10 | NOT_RUN | pending |
| 11 | W12 | NOT_RUN | pending |
| 12 | W6, W7, W12 | NOT_RUN | pending |
| 13 | W12 | NOT_RUN | pending |
| 14 | W12 | NOT_RUN | pending |

## Review Evidence

Independent exact-diff review is performed at W12 using the canonical
`diff-review` prompt once that prompt exists. No review disposition is recorded
before it is actually performed.

## Commit Ledger

| Unit | Type and scope | State |
| --- | --- | --- |
| W1 | `docs(architecture)` | pending |

## Rulings

- SPEC-0173 is not modified by this package.
- A guard that fires is treated as correct until proven otherwise; the change is
  adjusted rather than the guard weakened.
- Static configuration, renderer parity, and local test results never establish
  native runtime discovery, provider entitlement, Hosted CI, or remote state.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED with their missing input
  and are never promoted to a PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| Stage 90 curated repository map consolidation into `knowledge/` | Tracked consumers in the LLM Wiki generator, the reference validator, `llms.txt`, and four documents; needs its own coordinated change and a registered data lifecycle transition |
| Model context, cost, latency, and output-ceiling rows | No authorized API path exists locally; cost is recorded as unmeasured rather than zero |
| Codex `skills.config` native binding | Runtime acceptance unobserved; adoption would need direct observation |
| Editor workspace-task integration | No editor workspace configuration is tracked; inventing command identifiers is prohibited |
| Automated pull-request review expansion | Remote activation and execution cannot be observed under current authorization |
| Fixture reduction | Requires a separate duplication and maintenance-cost comparison; safety negative tests must be preserved |
| REQ-0026, AD-0030, ADR-0031 retention-owner promotion | Owned by SPEC-0173 as its declared open design dependency |
| Role-system import, consolidation, or retirement from the external catalog | Each change moves a permission profile and a handoff contract; this package's acceptance contract preserves 14 role IDs, so the change would be unreviewable here. This package restores the canonical owner of the intake decision instead |
| Spec, Plan, and Task promotion beyond `draft` | The metadata check reads previous status from the fixed `origin/main` merge base, so no transition is observable on this branch; promotion belongs to the first branch after integration |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Decision](../../../02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
