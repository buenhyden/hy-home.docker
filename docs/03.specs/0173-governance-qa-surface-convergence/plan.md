---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.4.2"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0173-PLAN-0001"
parent_ids:
- "SPEC-0173"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Implementation Plan

## Objective

Relocate reviewed common authority to a real repository-owned `.agents/` home,
remove the former governance directory, and preserve native adapters, operational
safety, document contracts and frozen execution evidence. This plan replaces the
prospective integration/empty-root plan preserved at baseline `e5685b42c`.
Completed Tasks and their evidence are not reopened or re-executed.

The latest user request authorizes local source, consumer, generator, test and
policy changes, a local work branch, and normal scoped approval for protected
writes. The subsequent user instruction authorizes local commits and safe
follow-up verification. Push, merge, PR, deployment, secret access, global
settings and installation remain outside scope. The requested target supersedes earlier
`.agents` removal/empty-container direction. No additional permission follows
from a role, skill, external reference or historical Task.

## Dependencies

- Baseline: local main `e5685b42c92039618ae86cca8736b6a425630221`, initially clean.
- Work branch: `codex/0173-agent-governance-home`, created from that exact HEAD.
- REQ-0024/0026, AD-0027/0030 and ADR-0029/0031 remain the existing owners.
  Introduce the next registered ADR only for the changed authority-location
  decision; preserve ADR-0029's decision body during legal supersession.
- Task 0006 owns the per-source disposition, compatibility table, review and
  actual execution results. This Plan owns prospective steps only.
- Existing scripts remain executable owners. Stage 99 remains the document
  machine-contract owner. Provider Registry remains translation data, not policy.
- All 77 original common files were read and classified before movement. All
  23 skills have explicit preconditions, inputs, procedure, outputs and failures;
  ordinary policy/checklist/SDLC Markdown remains outside native skill discovery.

### Chosen architecture and alternatives

| Choice | Authority and loading | Safety / maintenance / navigation | Decision |
| --- | --- | --- | --- |
| Reviewed canonical relocation | One `.agents` source, native skill discovery, native provider adapters | Requires coordinated path/profile/loader transition; no duplicated bodies | Adopt within the user's requested direction after independent review |
| Keep current Stage 00 sources | Existing direct reads and current checks remain | Does not meet requested canonical home or native skill route | Reject for this request |
| Copy or link entire trees | Multiple policy roots or provider format aliasing | Ambiguous ownership, regeneration cycles and unsafe link boundaries | Reject |

```text
.agents/
  README.md
  governance/
    <existing policy>.md
    sdlc.md
    hooks/<existing hook policy>.md
    providers/README.md
    providers/registry.yaml
  roles/<existing role>.md
  skills/<existing skill>/SKILL.md
  skills/<existing skill>/agents/openai.yaml
.claude/
  provider.md
  README.md                  # generated pointer
  agents/<role>.md           # generated native roles
  skills/<skill>/SKILL.md     # generated thin adapters
  settings.json, hooks/, output-styles/  # existing native mechanics
.codex/
  provider.md
  README.md                  # generated pointer
  agents/<role>.toml         # generated native roles
  hooks.json                 # existing native mechanics
```

Optional rules, knowledge, prompts, workflows, evaluations, scripts and memory
directories are not introduced without a distinct consumer. Normative workflow
is `.agents/governance/workflows.md`; native JavaScript workflows are not adopted.
All 14 role IDs, 23 skill IDs, model/effort/permission mappings and hook registration
values stay unchanged. No `.codex/config.toml` is created solely for symmetry.

### Load graph and contracts

`AGENTS.md` explicitly instructs reading governance/bootstrap, `.codex/provider.md`
and selected policy/role/skill plus the current Task. `CLAUDE.md` uses verified
relative imports for the common bootstrap and `.claude/provider.md`; it does not
import Codex instructions. The two native README outputs point to authored
provider sources and never feed the renderer.

Native SKILL frontmatter uses `name`, `description`, and `metadata` containing
existing governance identity, owner, version, lifecycle and scope fields. Preserve
all meaningful source fields through the native-profile contract. Codex's
`agents/openai.yaml` sets `policy.allow_implicit_invocation: false`; Claude thin
adapters set `disable-model-invocation: true`. No tool grants, dependency installer,
server, memory or global skill copy is added. Explicit invocation metadata does
not replace approval gates. Codex reads canonical `.agents/skills`; the Registry
must distinguish canonical discovery from generated native skill output.

## Execution Sequence

1. W1: Record suitability, exact baseline, all source dispositions and successor decision.
2. W2: Replace canonical-home, skill-envelope and provider-rendering contracts with regressions.
3. W3: Move document profiles, discovery, link resolution and knowledge indexing to the new home.
4. W4: Cut over hook, evaluation, CI and root bootstrap consumers without widening execution.
5. W5: Apply reviewed source moves, regenerate native/index outputs and remove the old home.
6. W6: Verify final static behavior, preservation, runtime evidence limits and independent review.

### W1: Reviewed authority decision

- [ ] Record the latest user authorization and local baseline in Task 0006;
  preserve every earlier dated record and replace only obsolete current receipt
  claims and prospective directions.
- [ ] Record every original source, purpose, destination, consumers, dependencies,
  preserved contracts, approval effect and validation in that Task's migration
  table. Missing or duplicate source/destination is a failure.
- [ ] Compare official sources against Codex 0.140.0 and Claude Code 2.1.261.
  Record syntax, discovery, invocation and enforcement as separate evidence.
- [ ] Review proposed ADR-0032 without supersession metadata. On adoption under
  the explicit user relocation request and actual independent review, transition
  it to accepted, replace its proposal wording with the adopted decision and
  actual review basis, and add supersedes ADR-0029. Transition ADR-0029 accepted to
  superseded with reciprocal superseded_by ADR-0032, changing only lifecycle
  metadata before its first preservation. Move those pre-preservation bytes to
  Stage 98 superseded/02.architecture/decisions in the same reviewed change.
  Preserve its decision body and all already-frozen records; no fabricated
  terminal commit, signature, Tombstone or historical approval. Update live
  Spec/Requirement/AD/Registry/index links to the effective successor.
- [ ] Obtain separate read-only rules/code review of this exact design before
  source/code implementation. Address findings within the requested scope.

### W2: Canonical and provider contracts

Owned sources: `scripts/lib/agent_governance/agent_governance_contract.py`,
`provider_surface_renderer.py`, provider Registry, and existing provider/core tests.

- [ ] Constrain native fixture copies to exact tracked configuration inputs,
  excluding local settings/memory. Read new canonical sources and authored native
  provider documents from exact registered expected paths with bounded no-follow
  reads, including task-owned untracked files; staging is not a prerequisite.
- [ ] RED: valid populated canonical home currently fails; missing root, unknown
  entry, symlink/FIFO, wrong skill name/metadata, implicit invocation and canonical
  output injection must fail after migration.
- [ ] Replace the empty-container contract with bounded no-follow canonical
  inventory validation. Unknown source files are preserved and reported; never
  quarantine or remove canonical inputs.
- [ ] Load nested native skills and metadata; derive role procedure links from
  loaded source paths. Validate exact role/skill inventory and native control files.
- [ ] Restrict output roots to existing native surfaces. Reject source/output
  cycles and foreign adapter inputs. Thin Claude adapters link to canonical bodies.
- [ ] Retain source-link rebasing, query/fragment handling, read/output bounds,
  atomic writes, descriptor identities, quarantine races and unknown-file guards.
- [ ] GREEN: run the three existing provider/core modules after fixture hardening;
  test two writes in isolated fixtures plus canonical source-byte preservation.

### W3: Document and knowledge consumers

Owned surfaces: Stage 99 Registry/schema/templates, document-governance library,
metadata/link/lifecycle entrypoints, wiki generator and associated registered tests.

- [ ] RED: hidden canonical source discovery and valid relative links are currently
  absent; old live README route and unknown native skill fields expose old contracts.
- [ ] Register each new source exactly once, including the native skill envelope
  and invocation metadata, without weakening common authored or frozen profiles.
- [ ] Admit only the new canonical hidden root and remove old live route ownership.
  Retain historical namespace readers needed for frozen identities and recovery.
- [ ] Scan canonical outbound links and apply current-authority archive boundaries.
  Existing frozen outbound-link handling remains unchanged; no redirect is added.
- [ ] Update LLM Wiki input scopes/category, source templates and exact output owner.
  Preserve secret, symlink, lockfile, private/dotfile and bounded-read exclusions.
- [ ] GREEN: existing document tests plus new hidden discovery, retired-root,
  malformed skill, link escape and wiki scope negative cases; official check modes.

### W4: Hooks, entrypoints and repository routing

Owned surfaces: hook_rules and event hook, evals, parity/report scripts, script
manifest, semantic contract, workflow/labeler/CODEOWNERS and active navigation.

- [ ] RED: missing configured policy directory must fail closed rather than
  silently loading zero rules. Exercise new directory with independent known
  rule count, deny/allow/error/root fixtures. Run the actual dispatcher for both
  providers on missing/invalid policy and Python/evaluator errors; require deny
  JSON or exit 2 so an outer exception handler cannot turn a loader failure into allow.
- [ ] Move policy paths, source contexts, bootstrap strings and skill suggestions
  through the reviewed mapping; preserve events, matchers, budgets and permissions.
- [ ] Keep provider event conversion separate. Do not enable or trust new hooks,
  run a native session with bypass flags, or alter user-local settings.
- [ ] Keep hidden `.agents` changes in existing CI/document/security selection;
  remove old active prefix routing, not tests of retired-root rejection.
- [ ] Rebase current links/imports by resolved source/target paths. Historical
  quotations retain dated meaning and current-owner context; frozen bytes stay exact.
- [ ] GREEN: direct rule/core/eval/routing regressions and fresh changed-plan
  inspection; verify no ignored local file was read by fixture setup.

### W5: Protected cutover and generated outputs

- [ ] Verify every old regular source hash still matches its inventoried baseline
  and every destination is absent before applying the reviewed mapping. Abort on
  drift or local-state collision. This is a single transition, not two authorities.
- [ ] Use normal scoped approval for `.agents`/`.codex` source writes and native
  regeneration. Do not unmount protection or widen trust/sandbox/global settings.
- [ ] Apply content-specific edits, native envelopes and resolved relative links;
  preserve policy meaning and English contract language. Remove original files
  only when their mapped source exists and has been checked.
- [ ] Regenerate via `python3 scripts/operations/provider_surface_renderer.py --write`,
  then `--check`; run a second write and compare native/canonical byte inventories.
- [ ] Regenerate affected LLM outputs via their official `--write` then `--check`;
  do not edit generated output to satisfy a validator.
- [ ] Remove only now-empty original directories with `rmdir`. Verify `lstat`
  absence, current functional references zero, and classify every remaining old
  string as historical evidence, historical grammar or a negative regression.

### W6: Final evidence and review

- [ ] Run `git diff --check`, formal metadata/contracts/links/lifecycle checks,
  provider/wiki drift checks and the focused changed-code regressions.
- [ ] Inspect `run-ci-gate.py --profile changed --explain` on final paths and trace
  indirect operations before actual execution. The baseline selected QuickWin and
  template-security leaves implicitly consume real `.env` through Compose; this
  request does not authorize that. Record BLOCKED/NOT_RUN precisely if still selected.
- [ ] Use full only if current policy/impact requires it and its execution inputs
  are authorized. Prior main full exit 10/Docker socket denial is historical
  baseline evidence, not proof of an absent image or permission for a retry.
- [ ] Verify all existing frozen hashes, monotonic IDs, no local-state changes,
  only approved index/commit changes and native model/permission/event equality.
- [ ] Attempt only supported, non-model local discovery with installed tooling;
  filter results to repository paths. Paid invocation, hook trust and fresh-session
  enforcement remain NOT_RUN without their specific authority and actual evidence.
- [ ] Obtain independent policy/Python review of the exact final diff and record
  each correction and verification. Commit the verified coupled source/consumer
  transition using explicit task-owned paths. Keep the branch/workspace, with no
  push, merge, PR, deployment or cleanup of historical working artifacts.

### Follow-up after local commit

1. Preserve the verified transition as one atomic local commit; disconnected
   folder-only commits would break source, generated output and consumer paths.
2. Recheck the committed tree's contracts and freshness. A clean local `changed`
   profile selects no committed diff, so do not use it as proof of that commit.
   Newly allocated or relocated ordinary documents enter the Wiki through Git's
   tracked inventory. Regenerate and check its outputs after those paths enter
   the index, and recheck the final committed tree; an earlier untracked-input
   checkpoint is not sufficient evidence for the tracked inventory.
3. Review a clean isolated linked worktree for the two Compose baseline checks,
   using tracked non-sensitive examples only and no copied local environment.
   Execute only after inspecting the exact commands and available tools.
4. Keep PostgreSQL image/runtime evidence and normal native discovery separate.
   Do not replace their guarantees with synthetic fixtures, global-state bypass,
   or a broad all-files wrapper that could install tools or start containers.
   If a clean checkout exposes a test-ownership defect, preserve all existing
   behavior cases while restoring the library/CLI responsibility split required
   by this Spec. Update the Manifest, existing gate registration and independent
   ownership checks together; an empty or cache-only directory is not a repair.
5. Record actual follow-up results and remaining boundaries in Task 0006, then
   commit that evidence separately. No remote integration is authorized.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| Source meaning lost | All-source disposition and before/after review | Restore only affected source/consumer slice from e568 baseline after review |
| Skill gains implicit execution | Native explicit-invocation metadata and negative tests | Revert source/control/adapter slice together; no global disable |
| Missing policy becomes zero rules | Fail-closed path errors and direct rule tests | Restore the registered policy path/core pair |
| Canonical files treated as generated | Distinct source/output inventories and race guards | Stop, preserve exact paths and regenerate only reviewed native outputs |
| Frozen record rewritten | Baseline hashes and existing recovery checks | Stop; no in-place frozen correction |
| Protected write unavailable | Scoped normal approval; no protection bypass | Keep original authority until cutover can be completed |
| Aggregate reads operating inputs | Inspect actual selected leaf graph | Record BLOCKED and run safe formal static checks separately |

## Verification

Task 0006 records commands, cwd, exit code, scope and PASS/FAIL/BLOCKED/NOT_RUN/N/A.
A syntax or repository-contract pass is not discovery, invocation, permission
or hook execution. The current session loaded the old bootstrap before migration;
re-reading a new file is not a fresh-session startup test.

## Rulings

- The latest explicit relocation request replaces the old empty `.agents` policy
  and previous integration/cleanup plan, without weakening other approvals.
- No new Spec/Plan/Task identity is needed. A successor ADR is a distinct durable
  decision required by the existing authority contract.
- Archived Tasks remain durable full-body evidence. Git history does not replace
  their preservation and raw-string counts never justify their deletion.
- No optional native feature, plugin, server, model or global configuration is
  enabled by this relocation.

## Related Documents

- [Specification](spec.md)
- [Task 0006 evidence](tasks/tsk-0006-generated-evidence-and-final-verification.md)
- [Stage 03 index](../README.md)
