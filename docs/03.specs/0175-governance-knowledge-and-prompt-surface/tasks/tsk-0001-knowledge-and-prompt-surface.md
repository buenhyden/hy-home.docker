---
title: "Knowledge and Prompt Surface Execution"
version: "0.14.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-07"
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
- Position, recorded durably rather than by branch name. Work on this package
  happens on a short branch cut from `main` and retired into `main` as soon as
  it is verified, so any branch name written here is dead by the next
  integration. A resuming session reads its position from Git:
  `git rev-parse --abbrev-ref HEAD` for the branch, `git rev-parse HEAD` for the
  commit, and `git log --oneline origin/main..HEAD` for what is not yet on the
  remote. The durable facts are that `dev` and `main` are the integration
  targets, that the
  Commit Ledger below lists every commit this package has produced, and that the
  originating branch `codex/0173-agent-governance-home` was retired at W13.
- Shared branch, historical: SPEC-0173's Plan claimed the originating branch and
  has six open Tasks on it. This package appends its commits rather than cutting a second branch,
  because a branch from the integration baseline would drop SPEC-0173's commits
  and rewriting another package's history is not authorized. Integrating this
  branch integrates both packages.
- Authorization: local investigation, local edits, local commits on this
  branch, integration into the local `dev` and `main` branches, and retirement
  of the work branch and its worktree. Push, pull request, deployment, live
  service action, secret values, global installation, and remote state changes
  remain unauthorized, and naming `dev` as a target does not grant publishing
  it. Pushing to `main` is additionally blocked by a registered hook and is not
  attempted by any other route.
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

### Current branch and worktree re-verification (2026-09-06)

The baseline above is the package's starting point and is preserved as written.
This section records the state as re-measured after five commits, so a reader
resumes from current Git state rather than from the starting snapshot.

| Check | Command | Result |
| --- | --- | --- |
| Branch and HEAD | `git rev-parse HEAD` | `5af741ce0b87fc1a4d157f639fbb5d06589f3e4c` on `codex/0173-agent-governance-home` |
| Worktree | `git status --porcelain` | empty |
| Worktrees | `git worktree list` | one entry at the primary path; no second tree was created |
| Remote main | `git fetch origin` then `git rev-parse origin/main` | `8176cdee732954415bc5462d6d4d43da4e319394`, unchanged by the fetch |
| Remote truth | `git ls-remote origin refs/heads/main` | `8176cdee732954415bc5462d6d4d43da4e319394`, identical to the local ref |
| Merge base | `git merge-base origin/main HEAD` | `8176cdee732954415bc5462d6d4d43da4e319394` |
| Divergence | `git rev-list --left-right --count origin/main...HEAD` | `0 12`; nothing to integrate from main |

Refreshing the merge base is therefore not available: the local `origin/main`
already equals the remote branch, so the fetch moved nothing and the lifecycle
constraint recorded under the W2 correction is not an artifact of a stale ref.

`resolve_base_selection` in `scripts/lib/document_governance/metadata/lifecycle.py`
picks its base from `TEMPLATE_GATE_BASE`, then `GITHUB_BASE_REF`, then
`@{upstream}`, then `origin/main`, then `main`. The current-branch basis the
repository already supports is `@{upstream}`, and it does not resolve here
because this branch has no remote tracking ref. Establishing one requires a
push, which is outside this Task's authorization and is recorded as a blocked
option rather than taken. Setting `TEMPLATE_GATE_BASE` locally would forge the
gate's comparison base and is prohibited, so it is not used either.

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

### W5: Canonical roots admitted (2026-09-06, local-executed)

Extended `ROOT_ENTRIES`, `GOVERNANCE_PROFILES`, and the closed canonical-source
path allowlist; created both category indexes; declared them in
`canonical_sources`; and routed `.agents/README.md`,
`documentation-protocol.md`, and `stage-authoring-matrix.md` to the new
categories.

RED against the state stored at `HEAD`, then GREEN on the working tree:

```text
HEAD (before W5): failures=4
  ROOT_ENTRIES is ('README.md', 'governance', 'roles', 'skills'), expected ('README.md', 'governance', 'knowledge', 'prompts', 'roles', 'skills')
  GOVERNANCE_PROFILES is missing: governance-knowledge, governance-knowledge-index, governance-prompt, governance-prompt-index
  .agents/knowledge does not exist
  .agents/prompts does not exist
working tree (after W5): failures=0
```

Two defects surfaced when the assertion first ran, and both were corrected
rather than worked around.

The new assertion initially required the full member set of each root. W5
creates only the two indexes, so the assertion demanded files that W6 and W7
write. It now requires each root to exist, to be admitted, to contain its index,
and to have every present member declared in `canonical_sources`. The exact
member set ships with the commits that write those members.

`test_registered_inventory_can_be_read_without_other_payloads` pinned the source
count at `98` and failed as `98 != 100` once two sources were registered. The
count expressed no invariant and recorded only how many sources existed when the
test was written. It is replaced by an equality against the registry's declared
`canonical_sources` list, which additionally proves order and absence of
duplicates. The check is stronger, not weaker, and no threshold was lowered.

`python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract`
returns `Ran 39 tests` `OK`.

`check-document-links.py --mode all` then reported four `missing-link-target`
findings, all of them the prompt index linking members that W6 creates. The
recorded guard applies: a link lands in the commit that creates its target. The
index now names those members as literal file names and gains the links in W6.
The re-run reports `documents=704 links=6007 failures=0`.

### Observed flake outside this package (2026-09-06, local-executed)

The first W5 commit attempt was rejected by the changed public profile with one
failure, in a suite this package does not touch:

```text
FAIL: test_timeout_still_cleans (tests.validation.test_postgres_logical_upgrade_rehearsal.PostgresLogicalUpgradeRehearsalTests.test_timeout_still_cleans)
AssertionError: 'reason=timeout' not found in 'status=failed failure_class=readiness reason=source-state-query-failed\ncleanup_status=passed\n'
Ran 235 tests in 27.446s
FAILED (failures=1)
```

Run alone, the same test passes three times out of three. The fixture gives the
rehearsal a five-second total budget with a two-second cleanup reserve
(`IOR_TEST_TOTAL_TIMEOUT`, `IOR_TEST_CLEANUP_RESERVE`), so under the load of the
full suite the readiness query fails before the deadline is detected and the
run is classified `source-state-query-failed` instead of `timeout`. The
assertion depends on wall-clock timing rather than on the behavior it names.

The file is not modified here. `tests/validation/test_postgres_logical_upgrade_rehearsal.py`
belongs to SPEC-0173's test and fixture convergence Task, which is open, and
changing another package's fixture under this acceptance contract would be
unreviewable. The observation is recorded for that owner instead. This package
does not treat a passing retry as evidence that the test is sound.

### Canonical source damaged by the rejected commit run (2026-09-06, local-executed)

After the rejected W5 attempt, `generate-llm-wiki.py --check` reported `FAIL:
local governance requires a valid canonical source inventory`, and
`canonical_source_paths` raised `AGC-YAML-INVALID
path=.agents/governance/providers/registry.yaml`. The file had been reformatted
in both the index and the working tree, 114 insertions against 109 deletions:
sequence items were de-indented under their key and a comment was rewritten, so
`yaml.safe_load` failed with `mapping values are not allowed here` at line 5.
Every pre-commit hook in that run reported `Passed` except the final suite, so
the reformat came from the rejected run's own worktree handling rather than from
a hook that declared a fix.

Recovery kept the canonical bytes rather than accepting the reformat:
`git checkout HEAD -- .agents/governance/providers/registry.yaml` restored the
authored file, the two `canonical_sources` entries were re-applied as a
two-line addition, and `canonical_source_paths` then returned 100 sources.
`git diff HEAD --numstat` was read for every changed file to confirm no other
file carried unexpected churn.

This is why a rejected gate run is followed by a diff review rather than by an
immediate retry: the rejection left a canonical input invalid, and retrying
would have committed the damage.

### W6: Prompt contracts, and first use of one (2026-09-06, local-executed)

Added `handoff.md`, `diff-review.md`, `commit-message.md` and `test-design.md`,
registered all four in `canonical_sources`, restored the index links now that
their targets exist, and asserted the exact prompt member set.

This commit's own message was drafted through
[commit-message](../../../../.agents/prompts/commit-message.md), which is the
first actual use of the new category rather than a claim about it. Following its
Required Inputs, `git diff --staged --stat` and `git status --porcelain` were
read first; the staged set held nine paths and nothing was unstaged. Following
its Output Contract, the draft was checked against the enforced `.cz.toml`
pattern before the expensive gate ran, and every staged path was matched against
the message.

That last step caught a real gap. The first draft accounted for seven of the
nine paths and said nothing about the two regenerated LLM Wiki inventory
outputs, so a bullet naming them and the reason they travel in this commit was
added. The check that produced this finding was initially written against a
hand-declared list of paths, which is circular and proves nothing; the finding
came from reading the message text against the staged set instead. The prompt's
"list any staged path the message does not account for" step is what makes this
a check rather than a formality.

### W7: Knowledge members, verified against their sources (2026-09-06, local-executed)

Added [repository-map](../../../../.agents/knowledge/repository-map.md),
[glossary](../../../../.agents/knowledge/glossary.md) and
[verification-surface-map](../../../../.agents/knowledge/verification-surface-map.md),
registered all three, and asserted the exact knowledge member set.

The category requires each claim to trace to a tracked source, so the routing
table in the verification surface map was checked by loading the contract rather
than by reading it:

```text
['.agents/', '.claude/', '.codex/', 'AGENTS.md', 'CLAUDE.md'] -> ['agent-governance', 'document-contract', 'document-graph', 'document-lifecycle']
['README.md', '_workspace/', 'docs/01.requirements/', 'docs/02.architecture/', 'docs/03.specs/', 'docs/90.references/', 'docs/98.archive/', 'docs/99.templates/'] -> ['document-contract', 'document-graph', 'document-lifecycle']
['docker-compose.yml', 'docs/05.operations/', 'examples/', 'infra/', 'secrets/'] -> ['document-contract', 'document-graph', 'document-lifecycle', 'operations']
['.github/', '.pre-commit-config.yaml', 'evals/', 'projects/', 'scripts/', 'tests/'] -> ['agent-governance', 'document-contract', 'document-graph', 'document-lifecycle', 'operations', 'repository-integrity']
fallback: ['repository-integrity']
```

All five rows match the member's table. One row listed its prefixes in a
different order than the contract does; the member now follows the contract's
order so a later re-verification compares the two directly. No count is asserted
anywhere in these members, so none can go stale against a growing repository.

No hardcoded totals were introduced: the members route and define, and the
numbers that would date them live in the sources they point at.

Writing the members also exposed a defect in the W4 profile. The metadata check
reported `type-inappropriate-key: key is not declared for governance-knowledge:
review_cycle` for all three. The profile had declared `next_review_at`, a key
that appears in no tracked document in this repository, while `review_cycle` is
the key the corpus and two existing Stage 99 profiles already use. The profile
was corrected to the repository's actual key rather than the members being
rewritten to an invented one, and the check returns `violations=0`.

### W8: Language authority repaired, output style reduced (2026-09-06)

`standards.md` routes the conversational-language rule to `output-style.md`,
which did not state it, leaving the Claude adapter as its only owner. The rule
now lives in its canonical owner, the artifact-language rule in
`documentation-protocol.md` describes the corpus as measured instead of
asserting a per-stage mandate, and the adapter is reduced to Claude Code
rendering plus routing.

The `keep-coding-instructions` field was verified against the installed release
before being used, not assumed (`local-parser`). `claude --version` reports
`2.1.263`. Both `keepCodingInstructions` and `keep-coding-instructions` appear
in that executable, and its own help text reads: `If true, the default coding
instructions stay in the system prompt alongside this style.` Whether the value
takes effect is `unverified-runtime`: an output style is read at session start,
so this change is reviewed as text and observed at the next session.

Corpus re-measured at this commit, counting files containing any Hangul
(`local-executed`):

```text
docs/01.requirements       korean=  18 / total=  18
docs/02.architecture       korean=  56 / total=  57
docs/03.specs              korean=   1 / total=  12
docs/05.operations         korean= 196 / total= 209
docs/90.references         korean=   2 / total=  59
docs/99.templates          korean=   0 / total=  38
.agents                    korean=   0 / total=  83
```

Stage 01, 02 and 05 are Korean; Stage 03, 90 and 99 are English; `.agents` holds
83 files and none contains Hangul, so the English-only constraint still holds
after nine files were added to it. The promoted statement describes this rather
than mandating a stage-to-language mapping the corpus would contradict.

### W9: Selector alignment and the intake decision owner (2026-09-06, local-executed)

The workflow contract routes `_workspace/` and `evals/`, but neither
`.pre-commit-config.yaml` public-gate selector admitted them, so a change
confined to either needed suites and ran none locally.

RED, by running the new assertion's own logic against the config stored at
`HEAD`, and GREEN on the working tree:

```text
HEAD (before W9): routed but not admitted = ['_workspace/', 'evals/']
assertion would fail at HEAD: True
after W9, routed but not admitted: none
```

Both selectors were widened rather than the contract narrowed, because the safe
asymmetry runs the gate more often and the unsafe one runs it not at all. The
relation is now owned by
`test_precommit_selector_admits_every_contract_changed_prefix` in
`tests/lib/gate/test_github_workflow_contract.py`, so a future divergence fails
instead of passing quietly.
`python3 -m unittest tests.lib.gate.test_github_workflow_contract` returns
`Ran 51 tests` `OK (skipped=11)`.

The first attempt was rejected by `ruff format`. The formatter runs over each
changed file rather than each changed hunk, so adding a method brought two
pre-existing expressions in the same module into its scope and it rewrote them,
five lines becoming two. The added method itself was already conformant. The
reformat is carried rather than reverted, because the hook is the repository's
own formatting authority and a file it rejects cannot be committed; the two
lines are named here so a reviewer knows they are the formatter's work and not
an unrequested edit.

The same unit returned the external capability-intake decision to
[agentic policy](../../../../.agents/governance/agentic.md#external-capability-intake).
That boundary lost its canonical owner when the former catalog format was
retired, leaving only a Stage 90 research member describing it; evidence
describes, it never decides. `git-workflow.md` now also documents the commit
shape `.cz.toml` enforces, which previously existed only in that configuration
and rejected messages after the expensive gate had already run.

### W10: External re-observation (2026-09-06, official-source)

`git ls-remote https://github.com/msitarzewski/agency-agents.git HEAD
refs/heads/main` at 2026-09-06T23:15:33+09:00 returns
`1454492577d1af4884722837f491fef14b501e21` for both refs. The upstream default
branch has moved off the pinned `ebe9c99acb5c96f9468de368d8bead775387d1a7`, so
the 2026-08-14 statement that it had not moved is now a closed historical
observation.

The new section is added beside the earlier ones, never over them. The member
still carries the `2026-09-05 Revalidation` section, the pinned SHA still
appears eleven times, and `git diff` shows the only removed lines are the three
frontmatter fields the version and date bump replaces:

```text
-version: "1.1.1"
-observed_at: "2026-09-05"
-reviewed_at: "2026-09-05"
```

No clone, checkout, count derivation, converter run, or installer execution was
performed, so every division and agent count in the member stays bound to the
`ebe9c99a` pin and is explicitly not carried forward to the new head. The member
now links to the restored canonical intake owner and states that it supplies
evidence for that decision without owning it.

### W11: Generated artifacts (2026-09-06)

The LLM Wiki outputs were regenerated and staged inside each source commit
rather than in a separate unit, because the generator reads the staged index:
generating before staging leaves the outputs stale, and a separate commit leaves
them stale in between. `generate-llm-wiki.py --check` reports both outputs fresh
at every commit in this package.

`graphify update .` is NOT_RUN as a write. The command was invoked and refused
its own overwrite:

```text
[graphify] WARNING: new graph has 17882 nodes but existing graph.json has 22689.
Refusing to overwrite - you may be missing chunk files from a previous session.
Pass --force to override.
```

`--force` was not passed. The tool is reporting that this run's corpus is
smaller than the stored graph and naming missing chunk files as the likely
cause; forcing would replace a tracked 22689-node artifact with a 17882-node one
on the strength of a run the tool itself distrusts. `git status --porcelain`
after the invocation returns empty, so nothing was written. The graph therefore
stays at its recorded build commit `f8a72211` and remains advisory, exactly as
the baseline section already states, and every conclusion in this Task is
corroborated against tracked sources rather than against the graph.

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

### Acceptance mapping (2026-09-06)

Each criterion is mapped to what was actually observed, with its evidence class.
A criterion whose check did not run is recorded as such, never promoted.

| # | Criterion | Observed | Class |
| --- | --- | --- | --- |
| 1 | Root inventory exact | `ROOT_ENTRIES` is `('README.md', 'governance', 'knowledge', 'prompts', 'roles', 'skills')`; contract check `PASS failures=0` | local-executed |
| 2 | Four profiles registered | all four present, each `transitions` entry `living`, each with a `template_roles` source | local-executed |
| 3 | Templates and catalog | both template files exist; the catalog lists two new rows | local-executed |
| 4 | Knowledge members exact | `README.md`, `glossary.md`, `repository-map.md`, `verification-surface-map.md`; each declares `observed_at` and `review_cycle` and a `Provenance` section | local-executed |
| 5 | Prompt members exact | `README.md`, `commit-message.md`, `diff-review.md`, `handoff.md`, `test-design.md`; each declares the seven registered sections | local-executed |
| 6 | Inventory and drift | nine new `canonical_sources` entries; `provider_surface_renderer --check` `PASS providers=2 drift=0`; `generated_roots` untouched | local-executed |
| 7 | Output style repaired | `keep-coding-instructions: true` present; the conversational-language rule now stated in `output-style.md`; the artifact-language paragraph describes the measured corpus | local-parser, configured |
| 8 | Selector alignment | routed-but-not-admitted was `['_workspace/', 'evals/']` at `HEAD` and is now empty; the relation is owned by a test | local-executed |
| 9 | Intake decision owner | `agentic.md` carries `External Capability Intake`; the Stage 90 member links to it and disclaims ownership | local-executed |
| 10 | External re-observation | the 2026-09-06 head is recorded and the `2026-09-05 Revalidation` section is preserved | official-source |
| 11 | Preserved invariants | 14 roles, 23 skills, 6 public suites, 2 public profiles unchanged | local-executed |
| 12 | Prompts used in this work | `commit-message` drafted the W6 message and caught two unaccounted paths; `diff-review` drove the independent review; `test-design` shaped the three RED-then-GREEN assertions; `repository-map` and `verification-surface-map` were verified against their sources | local-executed |
| 13 | Focused validators and changed profile | each commit in the ledger passed the changed public profile at pre-commit, which is what admitted it; two attempts were rejected and are recorded with their cause; focused validators recorded per unit | local-executed |
| 14 | Evidence classes distinguished | this table plus the per-unit entries; cost is unmeasured, not zero | local-executed |
| 15 | Closing | each branch fast-forwarded into local `main` and retired after a containment proof. This Task performs no push. The remote has advanced more than once from outside it; the entries are read with `git reflog show origin/main --date=iso` and are routed for a ruling rather than counted here | local-executed |
| 16 | Entry path names both categories | `bootstrap.md` names them twice in its load order and once in its English-only constraint; each authored adapter states it reads them directly and expects no projection | local-executed |
| — | ADR-0034 promotion to `accepted` | rejected on the first attempt with `invalid-initial-status: new adr documents must start at proposed`, then admitted once the package reached the merge base; the decision now carries `accepted`, and the two runs together are what show the rule rather than the outcome alone | local-executed |

### W13: Integration and branch retirement (2026-09-06, local-executed)

The final `run-ci-gate.py --profile changed` on the reviewed head returned exit
`0` with no `FAILED` block.

`main` was verified to be an ancestor of the work branch, then fast-forwarded,
so the reviewed commits reach `main` unchanged and no merge commit is
introduced. Containment was proved before anything was deleted, rather than
inferred from the merge's exit code:

```text
commits on branch not in main: 0
commits in main not on branch: 0
tree identical? yes
```

All nine new canonical files are present under `main` at
`5a84eb5fc8673ccdec09ef9c14e358eafd8010e8`. The work branch
`codex/0173-agent-governance-home` was then deleted with `git branch -d`, which
refuses a branch that is not merged, so the delete is itself a second
containment check. No worktree was removed: one primary worktree is in use and
none was created for this work.

At the moment this section was written, `origin/main` remained
`8176cdee732954415bc5462d6d4d43da4e319394` and nothing had been pushed by this
work. That statement was true when recorded and is false now; the correction is
in W15 below rather than by rewriting this paragraph, because a dated
observation is not edited into agreement with a later one.

No push was performed under this Task. A registered hook blocks pushing to
`main`, and that block was respected rather than routed around.

### W14: The entry path did not reach the new categories (2026-09-07, local-executed)

A post-integration gap review found that the two categories existed, were
enforced by the contract, and were indexed, but no entry path routed to them:

```text
grep -c "knowledge\|prompts" .claude/provider.md .codex/provider.md
  .claude/provider.md:0
  .codex/provider.md:0
```

`bootstrap.md` is the sole owner of the canonical load order, and its step 3
resolved "the agent governance policies, canonical role, and skills needed for
the request" only. Its English-only constraint enumerated governance, roles and
skills. An agent following the entry sequence exactly would therefore never
open `.agents/knowledge/` or `.agents/prompts/`, and would not know the new
files were bound by the language rule.

This is the failure the governing request names directly: a category that exists
but is not used is not delivered. The earlier acceptance evidence measured the
files, the registrations and the guards, and none of those checks can observe an
unrouted category, because every one of them starts from the registry rather
than from the reader.

Fixed in the owners rather than in the members. `bootstrap.md` step 3 now states
when to read each category and repeats that neither grants a tool, path,
permission or approval. Its English-only constraint names both. Each authored
provider adapter states that the categories are read directly from the shared
home and that the absence of a projection under `.claude/` or `.codex/` is not a
defect, matching the existing statement about `.codex/skills/`.

Two other deferrals were re-checked rather than carried forward on trust. Editor
workspace-task integration stays deferred and the reason is confirmed: `git
ls-files` matches no `.vscode/`, `.idea/` or `.code-workspace` path, and neither
directory exists on disk, so there is no tracked editor surface to wire and
inventing command identifiers is prohibited. The sweep for count-dependent and
SHA-dependent checks found no further defect of the kind corrected in W5: the
remaining `len(x) == len(set(x))` comparisons are duplicate-detection
invariants, the pinned forty-character commits in the archive and link tests are
recovery bases that must stay reachable, and the `903` row count describes a
frozen completed migration rather than a growing corpus.

### W15: The remote advanced outside this Task (2026-09-07, local-executed)

A handoff rehearsal, run through
[handoff](../../../../.agents/prompts/handoff.md) by a session with no
conversation context, found that this Task's recorded remote state disagrees
with Git. The disagreement is real:

```text
git rev-parse origin/main            2a939c68a5f38e9bcf545b77259796147e24ede6
git ls-remote origin refs/heads/main  2a939c68a5f38e9bcf545b77259796147e24ede6
git reflog show origin/main --date=iso
  2a939c68a @{2026-09-07 05:54:21 +0900}: update by push
  8176cdee7 @{2026-09-06 08:43:38 +0900}: update by push
```

`origin/main` now carries `2a939c68a`, the commit this Task's W13 entry
fast-forwarded local `main` to. The push is timestamped 2026-09-07T05:54:21, after
the last commit written under this Task, and no `git push` was issued by this
Task; no repository or local hook script contains one. Who performed it is not
determinable from the repository, and this entry does not guess. The fact is
recorded; the authorization question is routed rather than answered here.

Three consequences, none of which are assumed:

Acceptance criterion 15 required that nothing be pushed. That condition no
longer holds for the branch, though it still holds for this Task's own actions.
The criterion is restated below to say exactly that, rather than being marked
passed on a fact that has since reversed.

The lifecycle blocker's cause is gone. `resolve_base_selection` reaches
`origin/main` before `main`, and the merge base is now `2a939c68a`, at which
`spec.md` is `draft` and ADR-0034 is `proposed`. A transition is therefore
observable for the first time. This was tested rather than assumed: promoting
ADR-0034 to `accepted` and running the changed-mode metadata check returns
`selected=5 violations=0`, where the same edit previously returned
`invalid-initial-status`.

The W13 paragraph is not rewritten. It was true when recorded, and editing a
dated observation into agreement with a later one is the failure the external
re-observation unit exists to avoid.

### W14 verification, recorded late (2026-09-07, local-executed)

The handoff rehearsal also found that W14 changed three authority surfaces with
only a `grep -c` observation recorded and no validator evidence. Re-run at that
tree:

```text
agent_governance_contract: PASS mode=repository section=all failures=0
provider_surface_renderer: PASS providers=2 drift=0
PASS: document link mode all
archive recovery: ... violations=0
unittest tests.lib.agent_governance.test_agent_governance_contract: OK
```

The changed public profile also admitted the W14 commit at pre-commit, which is
what allowed it to exist. Recording the evidence only after a reviewer asked is
the defect; the commit was gated, but the Task did not say so.

### Lifecycle walk, and its measured rate (2026-09-07, local-executed)

With the merge base carrying the package, the transition rejected at W2 now
passes: the Spec moved `draft` to `review` and the Task `draft` to `ready` with
`violations=0`.

A second transition on the same branch does not pass. Setting the Spec from
`review` to `approved` in the same working tree returns:

```text
docs/03.specs/0175-governance-knowledge-and-prompt-surface/spec.md: invalid-transition: lifecycle transition requires explicit override: draft -> approved
```

`previous_status` comes from the merge base, not from the previous commit, so an
already-advanced working-tree status is invisible to the check. The rate is one
transition per document per branch, not per commit. The W2 entry concluded zero
transitions; the complete rule is zero when the document is absent from the
merge base and one when it is present.

The Plan reaches `approved` in the same commit because its lifecycle defines
`draft` to `approved` as a single step, so that is its first transition. The
Spec's `approved` and `active`, the Plan's `active`, and the Task's
`in-progress` each need their own later branch. No override was requested: the
gate does not pass `--transition-override-file`, and manufacturing one to move
faster would defeat the check rather than satisfy it.

### A branch name in a Task is stale by construction (2026-09-07, local-executed)

The handoff rehearsal reported that the current branch appeared in no tracked
file, so W15 wrote the branch name into `Inputs`. That fix was wrong in kind. The
branch was retired into `main` in the same session, and the Task immediately
pointed at a branch that no longer exists:

```text
grep -n "codex/0175-bootstrap-routing" <task>   two hits
git branch --list "codex/*"                     zero branches
git rev-parse --abbrev-ref HEAD                 main
```

This is the third occurrence of the same class of defect: the independent review
found the Commit Ledger stale, the handoff rehearsal found the branch absent, and
this pass found the branch present but dead. Writing the name a fourth time would
produce the same result, because a short branch that is retired at integration
cannot be described by a value that only changes when someone remembers to edit
it.

The Task now records what does not expire: `main` is the integration target, the
Commit Ledger is the authority for what this package produced, and position is
read from Git with the three commands named in `Inputs`. The handoff prompt's
Required Inputs already asked for branch and HEAD from Git rather than from the
Task; it now says explicitly that a branch name found in a Task is treated as
historical and that Git is the only current source.

The remaining lifecycle transitions were re-measured on a fresh branch and were
unreachable at that time. `resolve_base_selection` selects the merge base with
`origin/main`, so cutting a local branch changes nothing and only the remote
advancing does. That measurement is not restated as a current fact: what the
base holds is read with `git show "$(git merge-base origin/main HEAD)":<path>`,
and where the remote points with `git rev-parse origin/main`.

### W16: The re-test found the substitution was applied to one claim only (2026-09-07, local-executed)

A second handoff rehearsal, run with no conversation context against the
remediated tree, closed one gap and reopened three. Its verdicts are accepted as
given.

Gap 1, the branch name, is closed, and closed correctly: the Task states the
query instead of the value, and the branch name is absent from every tracked
file by design rather than by omission.

Gaps 2, 3 and 4 were still open, and the reason is one sentence: the same
substitution was applied to the branch name and to nothing else. Remote heads,
ahead-and-behind counts, commit lists and merge-base SHAs were still written as
literals, so each went stale on the next push. The Commit Ledger had fallen four
behind, including the commit that rewrote the ledger's own rule and then omitted
its row. Every remaining literal in this Task and in the Spec is now replaced by
the command that answers it, in the file that owns the claim, and `plan.md`
gained the W16 unit and a stated resume condition, which is what Gap 4 asked for.

Gap 3 is closed with evidence rather than with a claim. The previous HEAD changed
`.agents/prompts/handoff.md`, a registered canonical source, with nothing
recorded. Re-run here, each with its exit code:

```text
check-agent-governance-contract.py --mode repository   PASS failures=0        exit 0
provider_surface_renderer.py --check                   PASS providers=2 drift=0 exit 0
check-document-links.py --mode all                     PASS                   exit 0
check-document-corpus-lifecycle.py                     violations=0           exit 0
unittest tests.lib.agent_governance.test_agent_governance_contract   OK
```

The remote advanced a third time, to the commit this session integrated. That
moved the merge base again, which admitted one further transition: the Spec
reaches `approved`. The Plan and Task cannot follow yet, and this was measured
rather than assumed. Setting the Task to `in-progress` returns
`configuration-error: current Task requires active Spec`, and setting the Plan to
`active` returns `configuration-error: active Plan requires active Spec`. The
package integrity rules, not just the merge base, set the order: the Spec must
reach `active` before either.

### Document audit against current state (2026-09-07, local-executed)

A pass over the Spec, Plan and Task for unfinished work and for claims the
repository has since falsified found six items, all corrected in the file that
owns the claim.

Three were statements left in the present tense after the condition they
describe ended: the Plan asserted the package stays at `draft` for the branch's
life, this Task's acceptance mapping said ADR-0034 stays `proposed`, and its
Deferred Items row said no transition is observable. The Spec's status is
`approved` and the decision's is `accepted`, so all three read as false to
anyone checking. Each now states what happened and what still gates the rest,
rather than restating a superseded rule.

One was a stale explanation: the Plan said a forward link to SPEC-0175 is not
written "because its target does not yet exist", long after the target existed.
It now reads as the record of a decision rather than as a current condition.

One open question was closed by measurement instead of being carried: editor
workspace-task integration is not blocked pending a decision, it is empty
pending a surface. No `.vscode/`, `.idea/`, or `.code-workspace` path is tracked
and neither directory exists, so the Spec now states the measurement and the
condition that would reopen it.

The sixth is the one that mattered. The Plan listed sixteen work units and no
completion state, so nothing in any tracked file said which were finished. Two
independent handoff rehearsals reported that a fresh session cannot name the
next step, and this is why: the Commit Ledger records what happened, but only the
Plan can say what remains, and it was not saying. The Execution Sequence now
carries a per-unit state table, with `done` defined as the commit existing and
the evidence being in this Task.

### A commit cannot name its own SHA (2026-09-07, local-executed)

The previous commit tried to pre-fill its own ledger row to stop the row from
being forgotten again, and wrote `this commit` as a placeholder. A commit's SHA
is not known until the commit exists, so the row could not be completed in the
commit it describes, and the placeholder survived into the tree.

The rule that stops the recurrence is not a placeholder but an ordering: a
unit's row is written in the next commit, which is also where its predecessor's
verification evidence lands. That is what happened here, and it is the only
order that produces a true row without a second edit to the same commit.

Writing this entry reproduced the error one line further on: the draft filled in
a SHA for the commit that was about to be made, which is the same invention in a
different place. It was removed before the commit. The ledger row for this
commit lands in the next one, which is what the ordering above requires; the row
above it, `b22fe6fa5`, is exact because that commit exists.

The acceptance contract was re-verified against the current tree at the same
time, from the files rather than from this Task:

```text
1 roots: ('README.md', 'governance', 'knowledge', 'prompts', 'roles', 'skills')
2 profiles registered: True
3 templates present: True
4 knowledge: README.md, glossary.md, repository-map.md, verification-surface-map.md
5 prompts: README.md, commit-message.md, diff-review.md, handoff.md, test-design.md
6 knowledge and prompt entries in canonical_sources: 9
11 roles: 14   skills: 23
```

### Second document audit: the contract did not require the route (2026-09-07, local-executed)

A second pass over the three documents, after the obvious superseded statements
were corrected, found two items that the first pass missed because both are
absences rather than false claims.

The acceptance contract had fifteen criteria and none of them required the two
categories to be reachable. Criteria 1 through 6 require the files, the
registrations, the templates and the inventory; 7 through 10 require the defect
fixes; 11 through 15 require preservation, usage, verification, evidence classes
and closing. W14 corrected a high-severity defect — no entry path named either
category — and nothing in the contract would have caught its regression. That is
the same blind spot the defect itself had: every registration-side check begins
at the registry, so none can see whether a reader ever arrives. Criterion 16 now
states it, appended rather than inserted so the existing numbering is unchanged.

The in-scope list omitted four files this package changed:
`.agents/governance/bootstrap.md`, `.claude/provider.md`, `.codex/provider.md`,
and `.agents/prompts/handoff.md`. The first three are now declared; the fourth
is already covered by `.agents/prompts/**`. An independent reviewer had flagged
the first three as outside the declared scope, and the scope was corrected here
rather than the change being defended as implied.

Criterion 16 measured at this tree:

```text
bootstrap.md names knowledge/ or prompts/          2 occurrences
bootstrap.md English-only constraint covers both   1
.claude/provider.md names both                     1
.codex/provider.md names both                      1
```

### W18: The remote advanced a third time and the walk completed (2026-09-07, local-executed)

`origin/main` moved to the package HEAD while this unit was being investigated.
The first command of the session read `db9901bbe` with five unpublished commits;
a later read of the same ref returned `7827cb1c2` with none:

```text
git reflog show origin/main
  7827cb1c2 refs/remotes/origin/main@{0}: update by push
  db9901bbe refs/remotes/origin/main@{1}: update by push
stat -c %y .git/refs/remotes/origin/main   2026-09-07 07:53:44 +0900
git rev-list --count origin/main..HEAD     0
```

This session ran no push and holds no grant to run one. This is the third such
advance recorded here; as at W15, who performed it is not determinable from the
repository and is not guessed.

The advance made the merge base equal to HEAD, which completed the lifecycle
walk in one commit rather than three branches:

```text
metadata base: source=local:upstream ref=@{upstream} merge_base=7827cb1c2...
metadata check-changed: selected=3 violations=0 legacy_exceptions=0 transition_overrides=0
document corpus lifecycle: violations=0
```

The order the package integrity rules impose was measured, not assumed. Moving
the Plan alone, with the Spec left at `approved`, is rejected:

```text
configuration-error: docs/.../plan.md active Plan requires active Spec
spec-package-invalid: docs/03.specs: validation rule is not satisfied
```

Moving all three together satisfies the same rules, because they constrain the
end state rather than an ordering across commits.

The first commit attempt was rejected, and the rejection found a surface the
focused validators did not cover. Status is written in a fourth place: the
Stage 03 index prose describes each package's Spec, Plan and Task status, and a
registered test compares that prose against the frontmatter.

```text
FAIL: test_current_index_status_matches_each_current_spec
AssertionError: 'active' not found in 'approved package defining the canonical
  .agents/knowledge/ and .agents/prompts/ categories, with an approved Plan and
  ready Task' : SPEC-0175
```

The metadata, corpus-lifecycle, links, contract, renderer and freshness checks
all passed on the same tree, so running them is not equivalent to running the
gate. The index row was corrected and `tests.lib.document_governance.test_spec_packages`
returned `Ran 33 tests OK`. The staged diff was reviewed after the rejection
before retrying, because an earlier rejected run in this package left a
canonical source damaged; this one changed only the four intended files.

The earlier claim that each remaining transition needs its own later branch is
withdrawn. It sat one paragraph away from its own correction, which already
said that cutting a local branch changes nothing and only the remote advancing
does. The operative condition was never the branch. On `main` the base resolved
as `source=local:upstream ref=@{upstream}`; on a freshly cut
`docs/0175-dev-integration`, which has no upstream, it resolved one candidate
later as `source=local:origin/main ref=origin/main`. Both returned
`merge_base=7827cb1c27c8043c11791c3d1c6fbcdeba68fb39`, so the selected source
differs between branches while the base does not.

`--transition-override-file` was re-examined as a possible shortcut and
rejected on two independent grounds. It appears in no gate, hook, or workflow
file, so a local pass obtained with it would not be reproducible by the check
that gates the commit; and its loader documents it as reverse-transition
evidence requiring a named approval, which no one has given. Manufacturing one
would defeat the check rather than satisfy it.

### The `dev` target measured against the policy that does not name it (2026-09-07, local-executed)

The current request names `dev` as the integration target. A local `dev` did not
exist, and an earlier report in this session concluded from `git branch --list`
that no `dev` branch existed at all. That conclusion was wrong: the command
lists local branches only, and `origin/dev` is present.

```text
git rev-parse origin/dev                       cd13457528347437702c9cabb539efc0f11c22d8
git log -1 --format=%ci origin/dev             2026-06-01 09:47:27 +0900
git rev-list --count origin/main..origin/dev   0
git rev-list --count origin/dev..origin/main   1903
git merge-base HEAD origin/dev                 cd13457528347437702c9cabb539efc0f11c22d8
```

`origin/dev` is a strict ancestor of the integration history and carries no
commit of its own, so bringing it forward is a fast-forward and can lose
nothing. It is also undescribed by governance: `git-workflow.md` names `main` as
the only protected baseline, and the git-flow contract's head-branch pattern at
`scripts/lib/gate/ci_gate_adapters.py:740` admits the Conventional Commit
prefixes plus `dependabot` and `codex` but not `dev`, so `dev` can be a merge
target here and never a pull-request head. That gap is recorded in Deferred
Items and routed to the policy owner rather than closed by this package, which
owns no branching policy.

Updating `origin/dev` is a push and was not performed. The local refs are
fast-forwarded and the remote is left where it stands.

### W18 integration: two targets, and a merge that a generated file blocked (2026-09-07, local-executed)

`run-ci-gate.py --profile changed` returned exit 0 on the final path set. The
`ERROR` lines in its log are the expected output of the fail-closed negative
tests, which assert that the wrapper rejects forged `CI` and `GITHUB_ACTIONS`
values; every unittest summary in the same log is `OK` and none reports
`FAILED`.

The first integration attempt did not apply. Checking out `dev` moved the
working tree back 1903 commits, the graph watcher rebuilt against that tree and
modified the tracked files under `graphify-out/`, and `git merge --ff-only`
then refused rather than overwrite them. Nothing was lost: no merge was left in
progress, and the commits stayed reachable from the work branch. The tracked
generated files were restored with `git checkout -- graphify-out/`, and the
remaining untracked paths were confirmed absent from the target commit before
moving.

The retry avoided the working tree entirely. Both targets were proven to be
strict ancestors first, which makes advancing the ref a fast-forward and not a
rewrite, and only then were the refs moved:

```text
git merge-base --is-ancestor dev  b6c0650f3   -> ancestor
git merge-base --is-ancestor main b6c0650f3   -> ancestor
git branch -f dev  b6c0650f3
git branch -f main b6c0650f3
```

Containment was proven in both directions rather than from a merge's exit code,
and by tree identity rather than by commit count alone:

```text
dev   b6c0650f3  ahead=0 behind=0  tree=d9c9a47d73177c6b05752b8051eb9dfebcdc875a
main  b6c0650f3  ahead=0 behind=0  tree=d9c9a47d73177c6b05752b8051eb9dfebcdc875a
```

`docs/0175-dev-integration` was then deleted with `git branch -d`, which refuses
an unmerged branch and so is a second check rather than only a cleanup. One
primary worktree remains and none was created for this work.

The watcher also left an untracked `graphify-out/2026-09-07/` snapshot, which a
`git add -A` staged with the evidence before the staged list was read back.
Reading `git diff --cached --numstat` before every commit is what caught it, and
that is the reason the step exists.

It was unstaged and stays uncommitted, on a measurement rather than on the
separate-unit rule alone. Dated snapshot directories are tracked here, nine of
them, so the path itself is conventional; this one is truncated:

```text
graphify-out/2026-07-10/graph.json   21209 nodes   (last tracked snapshot)
graphify-out/graph.json              22689 nodes   (current top-level snapshot)
graphify-out/2026-09-07/graph.json    2412 nodes   (this byproduct)
```

At roughly a tenth of the corpus it agrees with the tool's own refusal to
overwrite the top-level graph, which named missing chunk files as the likely
cause. Committing it would publish a navigation graph that is missing ninety
percent of the repository while looking like a routine daily snapshot, so the
stop was allowed with this reason recorded instead. Regenerating it belongs to
the graph CLI and to the rebuild already deferred, not to this package.

`origin/dev` and `origin/main` were not touched. Publishing either target is a
push, which no grant covers, so `origin/dev` still points at
`cd13457528347437702c9cabb539efc0f11c22d8` and the local advance is unpublished.
Where each remote ref points is read with `git rev-parse`, not asserted here.

## Review Evidence

### Independent exact-diff review (2026-09-06, local-executed)

Performed at W12 through
[diff-review](../../../../.agents/prompts/diff-review.md) over
`git diff 9ede309a5..HEAD`, 37 files, by a reviewer that did not write the
change. Disposition: **approve with follow-up**. The reviewer re-ran the
repository's own checks rather than accepting the recorded results, reproduced
the selector defect and its fix against the workflow contract's 24 routed
prefixes, and confirmed the language rule is now stated once rather than twice
or not at all.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | medium | The Commit Ledger claimed W5 through W12 were uncommitted while six implementation commits existed, so an integrator reading the Task as the progress authority would misjudge what this shared branch contains | Fixed: the ledger now lists every commit |
| 2 | low | The assertion replacing the pinned source count could not fail, because `agent_governance_contract.py:1222-1225` already rejects a duplicate or a non-round-tripping entry, and the entry recorded here claimed it proved order and uniqueness | Fixed: it now asserts that every canonical category reaches the inventory, which fails if one is dropped; the earlier claim is corrected below |
| 3 | low | The Claude output style restated three canonical rules and strengthened one, requiring failing output "verbatim" where the canonical owner says only "rather than summarizing it", against acceptance criterion 7 | Fixed: the adapter keeps only rendering consequences and states no rule of its own |
| 4 | low | `repository-map.md` scoped the Provider Registry to provider, model, permission and hook facts, omitting `canonical_sources`, which the same category's index tells authors to register in | Fixed: the row now names the inventory and the other registry keys |

Correction to the W5 entry above: replacing the pinned count `98` was right,
because a count is not an invariant and broke on every registration. The claim
that the replacement additionally proved order and absence of duplicates was
wrong; the contract already enforced both before returning, so that assertion
could not fail. The reviewer caught it, and the assertion was rewritten to one
that can.

Not covered by the review: Hosted CI execution, `origin/main` state, provider
runtime acceptance, native discovery of the two new categories, the effect of
`keep-coding-instructions: true`, and `run-ci-gate.py --profile full`.

## Commit Ledger

| Commit | Unit | Subject |
| --- | --- | --- |
| `1befc0ed4` | W1 | `docs(architecture): Adopt knowledge and prompt canonical categories` |
| `ed0e71d24` | W2a | `docs(spec): Define governance knowledge and prompt surface package` |
| `e6b109b94` | W2 correction | `docs(spec): Correct the package lifecycle plan to what the gate allows` |
| `4fe3c8601` | W4 | `feat(governance): Register knowledge and prompt document shapes` |
| `5af741ce0` | Spec alignment | `docs(spec): Align the acceptance contract with the request and the gate` |
| `0d79578b0` | Re-verification | `docs(task): Re-verify the branch and worktree at the current HEAD` |
| `d8a9a143d` | Scope correction | `docs(spec): State the real change surface and the shared branch` |
| `3e1eee51e` | W5 | `feat(governance): Admit knowledge and prompt roots in the agent contract` |
| `73c145f4c` | Authorization | `docs(spec): Record the granted integration and retirement authorization` |
| `ac6c532eb` | W6 | `feat(governance): Add the four reusable prompt contracts` |
| `9d6b7346d` | W7 | `feat(governance): Add the three knowledge members` |
| `d34c0591a` | W8 | `fix(governance): Return language policy to its canonical owner` |
| `9051977aa` | W9 | `fix(qa): Align the local gate selector with the workflow contract` |
| `8de5aed41` | W10 | `docs(reference): Re-observe the external agent catalog upstream head` |
| `2355c9ea9` | W11 | `docs(task): Record the acceptance mapping and the refused graph rebuild` |

| `5a84eb5fc` | W12 | `fix(governance): Act on the independent review's four findings` |
| `2a939c68a` | W13 | `docs(task): Record the integration and branch retirement` |
| `7374c96e5` | W14 | `fix(governance): Route the entry path to the new canonical categories` |
| `e5e87f451` | W15 | `fix(spec): Correct the remote claim and close the handoff rehearsal gaps` |
| `569e14276` | W15 | `docs(spec): Advance the package to review and the Task to ready` |
| `db9901bbe` | W15 | `docs(spec): Approve the Plan and record the provable transition rate` |
| `f39080c7b` | W16 | `fix(spec): Record position from Git instead of a branch that dies` |
| `7cbc71e21` | W16 | `fix(spec): State the query wherever a Git value was written` |
| `b22fe6fa5` | W16 | `docs(spec): Correct superseded claims and give the Plan unit states` |
| `9c3a5f32c` | W16 | `docs(task): Fill the ledger row that a commit cannot write for itself` |
| `7827cb1c2` | W17 | `docs(spec): Require the entry path to name both categories` |
| `4da883e1f` | W18 | `docs(spec): Promote the package to active and retarget integration at dev` |

The ledger is updated in the commit that closes each unit, because a reader
deciding what this package has produced has no other authority for it. One row
is always outstanding and this is not a defect to be fixed by another commit: a
commit cannot contain its own hash, so the last commit's row would need a
further commit, whose row would need another. The last row is therefore recovered
by query rather than written in advance, with
`git log --oneline <last row in this table>..HEAD`. It fell
three commits behind between W12 and W15 even after the independent review named
exactly that defect, so the rule is restated here: a unit is not closed until its
row exists. Which commits have reached the remote is read from
`git log --oneline origin/main..HEAD`, not from this table, because that answer
changes without any edit to this file.

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
| `dev` as an integration target that governance does not describe | `git-workflow.md` names only `main` as the protected baseline and the git-flow head-branch pattern excludes `dev`, so the target the request names has no policy owner. Closing the gap edits a policy this package does not own; it is routed to that owner rather than decided here |
| Retiring or refreshing the stale `origin/dev` and the two remote `codex/**` branches | Every option is a remote reference change, which no grant here covers |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Decision](../../../02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
