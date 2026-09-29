---
title: "Agent Contract Hardening Implementation Plan"
version: "1.1.2"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-PLAN-0001"
parent_ids:
- "SPEC-0190"
created: "2026-09-29"
---

# Agent Contract Hardening Implementation Plan

> For agentic workers: use the requested `superpowers:executing-plans` procedure
> from its installed SKILL.md after Plan/execution approval. Execute in this
> session with bounded specialist assistance and independent review; do not
> require a fresh implementer/reviewer pair for every step. Unchecked steps are
> prospective, not execution evidence. Current Task records own actual results.

## Objective

Implement [SPEC-0190](spec.md) through reversible changes to existing owners:
validation helpers, resource boundaries, recovery review, authority/handoff
contracts, native controls and model-free evaluations. Preserve existing public
CLI behavior, roles, provider models, operational data and unrelated work;
W9 changes the evaluation subsystem path under the owner's explicit instruction.

Architecture: extend the existing canonical validator and link scanner, retain
skill-local helpers, and render only registered native projections. Reuse the
current Task as the execution record and migrate the existing four-file
model-free harness from `evals/` to `.agents/evaluations/` in W9. No new orchestration service or memory database.

Technology: Bash, Python standard library and already-declared YAML support,
Markdown/YAML/JSON/TOML contracts, the registered CI dispatcher and Git.
No new package or installation is proposed.

### Global constraints

- Written-spec and Plan/execution approvals were given on 2026-09-29.
  Approved execution includes local logical commits and bounded independent
  review; external/runtime/cost boundaries below remain separate.
- Retain all 14 role IDs, both sets of role projections and the 23 existing
  skills; add only `stateful-recovery-contract-review`. Retention still needs
  a reviewed file-level disposition, not an inventory-count assertion.
- Required missing tools/plugins produce BLOCKED; optional absence produces
  reasoned SKIPPED; successful discovery with no input produces NOT_APPLICABLE.
  FAIL gives exit 1, incomplete evidence gives exit 2, all required PASS gives 0;
  FAIL takes precedence over BLOCKED while both remain reported.
- Static fixtures do not establish native invocation, hosted success, entitlement,
  editor behavior, monetary enforcement or operational recovery.
- No secret values, live environment, raw logs, remote mutations, global state,
  dependency installation, deployment, restore, push, PR or merge. Preserve the
  branch and worktree. Separate approval binds any later observation to its
  exact tool, input, cost, duration, target and cleanup.
- No Stage 99 schema/template change. The previous spec allocation is retained;
  Plan identity is package-derived. No frozen document is rewritten.

### Review focus

| Condition | Expected outcome | Test owner |
| --- | --- | --- |
| Git discovery fails behind process substitution | nonzero; no empty-input success | W4/W5 helper tests |
| Nested resource is replaced after enumeration | reject before target read; bounded work | W3 descriptor/race fixture |
| A fenced or encoded URL hides a stage authority link | deterministic link finding or explicit semantic-review finding | W2 normalization/authority review |
| FAIL and missing required plugin occur together | exit 1 and both check states retained | W4 mixed-result fixture |
| Handoff looks valid but approval was revoked or shared budget consumed | refuse mutation/call; no fallback | W7 model-free refusal cases and W10 native observation |

## Dependencies

Use the existing managed worktree on `codex/agent-contracts`, observed at
`24b3e45c7fba5f11455c2a9b333463dfccfd3398`. Reconcile HEAD and owned paths at
execution time; this observation is not a permanent completion pin. The shared
checkout and SPEC-0189 are owned by other work and remain untouched.

Read REQ-0024, AD-0027, this Spec and Plan, bootstrap/provider instructions and
only each work unit's role/skills before mutation. Plan prose is not a permission
profile. `doc-writer` owns documentation, `qa-engineer` owns validation/tests,
`infra-implementer` owns its helper, `skill-creator` owns skill authoring, and
`hook-developer` owns native adapters. A unit with several surfaces transfers
exclusive file ownership between these contributors; one named primary owner
is accountable for its final diff. Rules/evaluation/security reviewers do not
write the changes they approve.

Execution dependency order is W1 → W2 → W3 → W4 → W5 → W6 → W7 → W8 → W9 → W10.
Read-only reviews can overlap independent authoring. Serial writes avoid index,
registry, generated-output and shared-test conflicts; do not parallelize writers
against `test_agent_governance_ci_routing.py`, the registry or renderer outputs.

All task paths below are prospective, under this package's `tasks/`; create them
only after Plan approval with the registered Task template and package-derived
IDs. No task directory or second progress ledger is needed during planning.
New documents must start in the registered initial state. Before activation,
W1 establishes a local committed predecessor and validates each transition
with the existing focused CLI; the normal local gate checks active content,
not transition history. Human approval alone cannot bypass lifecycle checks.

## Execution Sequence

1. **W1: Bind execution authority and the local baseline.** Primary: doc-writer;
   reviewer: rules-engineer. Task: `tsk-0001-execution-baseline.md`.

   **Files:** this package's `spec.md`, `plan.md` and the named Task, plus
   `docs/03.specs/README.md` and `docs/99.templates/registry.json` for the already
   reviewed index/spec-allocation edits. Preserve those exact edits; W1 grants
   no additional Stage 99 change.
   **Interface:** produces the Task approval/ownership envelope consumed by W2–W10,
   including the exact current base, owned paths and validation environment.

   - [x] Confirm Plan approval and the requested in-session execution method;
     read installed executing-plans instructions without installing anything.
   - [x] Record the user approvals and independent Spec/Plan review, inspect
     local/remote-tracking divergence read-only, and preserve the previous
     three-file authoring diff plus this Plan. Do not reset to main.
   - [x] Validate and commit the reviewed initial drafts after execution/commit
     approval. For each subsequent transition run
     `rtk proxy python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD`
     against the real preceding local commit. Commit Spec draft→review and then
     review→approved separately, promoting its version to 1.0.0 at stable approval;
     validate Plan draft→approved against its own committed draft. Do not inject
     a CI context or alter the public runner to manufacture history. Later
     active parents and Task transitions use the same predecessor discipline.
   - [x] Record baseline checks, missing tools and separately authorized fixture
     boundaries. Record the previous changed-profile exit 0 as dated baseline
     evidence, not a substitute for testing subsequent code.
   - [x] Create later Tasks immediately before their unit; activate parents and
     Task only through the admitted lifecycle. Commit reviewed setup as
     `docs(agent): Record approved contract hardening plan`.

2. **W2: Align current document authority and its scanner.** Primary:
   qa-engineer; documentation contributor: doc-writer; reviewer: rules-engineer.
   Task: `tsk-0002-document-authority.md`.

   **Modify:** `.agents/governance/documentation-protocol.md`,
   `.agents/governance/bootstrap.md`, `.agents/governance/stage-authoring-matrix.md`,
   `.agents/README.md`, `scripts/lib/document_governance/links.py`,
   `tests/lib/document_governance/test_links.py`,
   `.agents/skills/provider-model-evaluation/SKILL.md`, `scripts/README.md`,
   `README.md`, `.github/repository-surface.md` (the semantic audit identified
   stale current-authority claims; historical provenance remains intact).
   **Retain public CLI:** `scripts/validation/check-document-links.py`.
   **Interface:** retain `check_entrypoint` and `MODE_HANDLERS` result shapes;
   extend target classification, not the CLI or general document graph protocol.

   - [x] Add table-driven `test_entrypoint_normalizes_stage_link_forms` and
     `test_entrypoint_preserves_navigation_and_non_authoritative_examples`:
     relative/absolute, GitHub blob/raw, percent-encoded, mixed case/separators,
     anchors, reference Markdown, HTML, wiki and fenced clickable forms must
     reject individual-stage links; README navigation and docs-internal links
     remain valid. Assert stable finding codes and no file writes.
   - [x] Run the link unit module (Verification L) and witness the intended RED.
     Add negative controls for literal output-path examples and historical
     provenance so extending normalization cannot delete them indiscriminately.
   - [x] Implement normalization in `links.py` and reconcile the current policy:
     README navigation is allowed; individual stage documents cannot supply
     current outside-docs authority. Keep schema/registry/template exceptions
     explicit by kind, consumer, need and scope; never a stage-wide whitelist.
   - [x] Review authored `.agents/`, `.claude/`, `.codex/`, root shims, `scripts/`,
     `tests/` and `evals/` for semantic authority dependence. Record each finding
     and exact owner in this Task. Plain artifact IDs/provenance are not findings
     merely because they mention a stage. If a real defect needs an unlisted
     write, amend the exact file map before that write; do not perform blanket
     replacement or broaden approval into historical cleanup.
   - [x] Run L then the entrypoint CLI; obtain independent semantic review and
     commit policy, scanner and regressions together as
     `fix(docs): Align agent document authority checks`.

3. **W3: Enforce recursive skill resource boundaries.** Primary: qa-engineer;
   reviewer: security-auditor. Task: `tsk-0003-skill-resource-boundaries.md`.

   **Modify:** `scripts/lib/agent_governance/agent_governance_contract.py`,
   `tests/lib/agent_governance/test_agent_governance_contract.py`,
   `tests/validation/test_provider_surface_renderer.py` (shared fixture resource
   copying only), `.agents/README.md` (doc-writer contribution),
   `scripts/lib/document_governance/links.py` and
   `tests/lib/document_governance/test_links.py` (shared Markdown opener bounds).
   **Interface:** `validate_canonical_agent_home()` retains its caller contract;
   resource traversal reuses `_read_text`'s bounded/no-follow identity checks.
   Add private `_validate_skill_resources(root: pathlib.Path, skill_root:
   pathlib.PurePosixPath) -> None`; return existing Finding records at the public boundary and translate internal
   ContractLoadError consistently with the existing validator.

   - [x] Extend current bundle tests with direct and transitive reference success;
     nested symlink, FIFO, socket/device-mode, replaced inode, traversal, orphan,
     unsupported local reference syntax and executable reference failures.
     Assert no out-of-root read and no resource execution. Use synthetic trees;
     mock device mode without privileged device creation.
   - [x] Run G and witness RED for currently unvisited resource trees.
   - [x] Traverse directories without following links and bound the traversal
     to 4096 entries per skill, 64 directory levels and 16 MiB of reference text
     per skill, retaining the existing per-file text cap. These are validator
     denial limits, not resource-count assertions about the repository.
   - [x] Resolve Markdown links and explicit local tokens beginning `scripts/`,
     `references/`, `assets/`, including relative links from reached references.
     Start reachability at SKILL.md; metadata/openai.yaml are not resources.
     Allow an executable only below scripts and reachable from the procedure.
     Binary assets may be terminal nodes, never text to execute or import.
   - [x] Run L, G, P and the repository contract; verify all current resources still
     pass and over-limit fixtures fail deterministically. Commit as
     `fix(agent): Validate nested skill resource boundaries`.

4. **W4: Make infrastructure static validation fail closed.** Primary:
   infra-implementer; test contributor: qa-engineer; reviewer: iac-reviewer.
   Task: `tsk-0004-infra-static-validation.md`.

   **Modify:** `.agents/skills/infra-validate/scripts/static-checks.sh`,
   `.agents/skills/infra-validate/SKILL.md`,
   `tests/validation/test_agent_governance_ci_routing.py`.
   **Retain:** public `scripts/validation/validate-docker-compose.sh` interface.
   **Interface:** helper accepts only no arguments, `--help` or `-h`; unknown
   flags/operands return 2 before configuration reads. Its per-check records
   include check ID, state, safe category and child exit; the final summary
   counts each state and follows the Spec's 0/1/2 precedence.

   - [x] Add `InfraAndStyleSkillHelperTests` cases with a temporary Git repository
     and fake command PATH: missing required binaries/plugin, Git failure,
     child failure plus BLOCKED, timeout, no eligible shell input, cwd at root/
     subdirectory/skill directory and a root containing spaces. Assert exit and
     each state; synthetic secret sentinels must never appear in diagnostics.
   - [x] Add `test_static_checks_do_not_touch_real_checkout`: pre-existing .env,
     ignored data and outside symlinks are unread and unchanged; every attempted
     Docker subcommand is captured, with daemon operations forbidden.
     Run H to observe RED without touching real environments or services.
   - [x] Resolve root from the script; capture Git discovery status directly.
     Define the required set once: Git/Bash, Docker+Compose, yamllint, and
     shellcheck for eligible tracked infrastructure scripts. Any additional
     command needed by the implementation is itself an explicit prerequisite.
     Apply a 60-second child bound and a 4-KiB diagnostic budget per check;
     emit bounded categories rather than raw stderr/Compose output.
   - [x] Isolate Compose into a task-owned repository-local temporary copy of
     reviewed tracked inputs. Copy current regular tracked source files, including
     reviewed worktree edits, with no-follow reads; never copy .git, real .env,
     ignored data or credential bodies. Use public
     `.env.example` only as a reviewed synthetic-key source, overwrite values
     with explicit fixture values, and keep every generated secret/config/env
     file reference inside the copy. Validate include/extends/env_file/config/
     secret-file paths before invoking Compose; unresolved interpolation,
     external/absolute paths or an unprovable graph yields BLOCKED before
     rendering. The copy gets its own temporary Git root for the retained
     validator. Do not source an environment file, run a secret generator or
     contact a daemon. Cleanup removes only paths created by this invocation.
   - [x] Run H, Bash syntax, available lint and isolated real-CLI structural
     acceptance. Fake binaries prove aggregation, not Compose correctness.
     If safe isolation or a required tool is unavailable, record BLOCKED and
     continue independent units; never change the required set to get exit 0.
     Commit as `fix(infra): Fail closed in static skill validation`.

5. **W5: Make style classification independent of cwd.** Primary: qa-engineer;
   reviewer: code-reviewer. Task: `tsk-0005-style-classification.md`.

   **Modify:** `.agents/skills/style-validation/scripts/classify-changed-files.sh`,
   `.agents/skills/style-validation/SKILL.md`,
   `tests/validation/test_agent_governance_ci_routing.py`.
   **Interface:** preserve existing output buckets and the closed forms: no
   arguments (staged index), `--base <ref>` (ref...HEAD), `--help` or `-h`; root
   discovery and marker reads use the same root, and malformed args/Git/read
   failure are nonzero instead of silently classifying authored content.

   - [x] Add `test_classification_uses_root_for_generated_markers` and
     `test_classification_rejects_discovery_and_marker_read_failures` in the
     helper test class. Assert identical buckets across the W4 cwd matrix.
   - [x] Run H for RED; fix root-relative Git and file reads, capturing discovery
     errors rather than masking them in process substitution.
   - [x] Run H and Bash syntax/lint; compare retained category outputs and
     commit as `fix(qa): Resolve style classification from repository root`.

6. **W6: Add read-only recovery review and role routing.** Primary: skill-creator;
   native contributor: hook-developer; reviewers: iac-reviewer/rules-engineer.
   Task: `tsk-0006-recovery-contract-review.md`.

   **Create:** `.agents/skills/stateful-recovery-contract-review/SKILL.md`,
   `agents/openai.yaml`, `references/recovery-contract.md`, `assets/verdict.md`
   beneath that same skill root.
   **Modify:** `.agents/roles/{iac-reviewer,incident-responder,workflow-supervisor,hook-developer}.md`,
   `.agents/skills/{infra-cross-validate,incident-response,ops-runbook-agent}/SKILL.md`,
   `.agents/governance/providers/registry.yaml`,
   `tests/validation/test_provider_native_surfaces.py`,
   `tests/validation/test_provider_surface_renderer.py`,
   `tests/validation/test_agent_function_routes.py`,
   `scripts/hooks/agent-event-hook.sh` (new explicit prompt route only).
   Braces in this Plan expand only the named finite set, not a wildcard grant.
   **Generated:** `.claude/skills/stateful-recovery-contract-review/SKILL.md`,
   `.claude/agents/{iac-reviewer,incident-responder,workflow-supervisor,hook-developer}.md`,
   `.codex/agents/{iac-reviewer,incident-responder,workflow-supervisor,hook-developer}.toml`,
   plus `.claude/README.md` and `.codex/README.md` only if the renderer changes
   their registered contents. No Codex skill copy is created.

   - [x] Read the selected installed skill-creator procedure, disambiguating it
     from this canonical role. Add missing-skill/invocation/owner/route fixtures
     to the existing provider modules and run P for RED.
   - [x] Author the sanitized input/reference/verdict contract specified by the
     Spec: inventory, backup/rebuild, consistency, retention/capacity/key custody,
     restore order/compatibility/target, RPO/RTO, application acceptance, stop
     conditions and named implementer/reviewer/approver. Missing facts give
     BLOCKED, not a generated restore command. No manifest or executable.
   - [x] Register only SKILL/openai metadata through existing fields; route the
     consumers and four roles while preserving read-only reviewers. Preserve
     all other role/skill dispositions from the Spec, recording reviewed
     retention and domain coverage in this Task.
   - [x] Use renderer `--write`, `--check`, then `--write` and `--check` again.
     Compare generated bytes before/after the second write and canonical bytes
     around both runs. Generated diff after the second write must be empty.
   - [x] Run G/P/H and the repository contract. Do not add an evaluation threshold
     before its fixture exists in W9. Commit as
     `feat(agent): Add stateful recovery contract review`.

7. **W7: Connect workflow, knowledge, handoff and budget contracts.** Primary:
   doc-writer; reviewer: rules-engineer; fixture contributor: qa-engineer.
   Task: `tsk-0007-workflow-and-handoff.md`.

   **Modify:** `.agents/governance/{agentic,workflows,output-style,provider-capability-matrix,git-workflow,github-governance}.md`,
   `.agents/knowledge/{README,repository-map,verification-surface-map}.md`,
   `.agents/prompts/{handoff,diff-review,commit-message,test-design}.md`,
   `docs/01.requirements/0024-agent-governance-standardization.md`,
   `docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md`,
   `evals/agent_output_eval.py`, `evals/fixture-catalog.md`,
   `tests/validation/test_agent_output_eval_fixtures.py`.
   W7 also reconciles REQ-0024 and AD-0027 category/architecture descriptions
   with the selected `.agents/evaluations/` owner; W9 performs the actual cutover.
   **Interface:** current Task owns state; handoff is its derived envelope;
   knowledge contains verified facts with existing Provenance/Refresh Triggers.
   Existing `score_text` and `run_regressions` own model-free judgments.

   - [x] Add deterministic refusal cases for changed HEAD/digest, wrong worktree,
     revoked approval, concurrent writer, partial result, expired knowledge,
     injected evaluation instruction, exhausted budget, bounded 429/backoff
     and competing tasks consuming the same budget. Assert that evidence of
     refusal is required and static-only native success claims fail the rubric.
     Run E for RED; these evaluate recorded outputs, not a new runtime engine.
   - [x] Separate design/spec/plan approvals, static/operational workflow and
     corrective incident routing; preserve one narrower retry/two attempts.
     Express Task-declared request/token/time/concurrency/retry ceilings and
     native enforcement/observation source. No guessed account RPM/TPM, price,
     universal token budget, provider key or unrequested inference gateway.
   - [x] Extend the handoff required inputs and refusal contract; place durable
     verified facts, scope/source/owner/date/sensitivity/invalidation in existing
     knowledge sections. Reconcile REQ/AD navigation-only wording with this
     bounded fact reuse, leaving detailed design/runbooks at their stage owners.
     Keep frozen ADRs untouched; prompts acquire no execution authority.
   - [x] Keep Git hooks, editor actions, CI and issue coordination separate.
     Projects remains the preferred future option, Linear an alternative;
     neither receives a sync job. Preserve failure/NOT_RUN/approval in output
     style. Do not invent an editor action or modify user bindings.
   - [x] Run E, metadata/link checks and independent semantic review. Real budget
     enforcement stays unresolved for W10 until a supported native route is
     observed. Commit as `docs(agent): Define bounded workflow and handoff contracts`.

8. **W8: Narrow native grants and expose missing post-edit lint.** Primary:
   hook-developer; reviewers: security-auditor/code-reviewer.
   Task: `tsk-0008-native-hooks.md`.

   **Modify:** `.claude/settings.json`, `.claude/provider.md`, `.codex/provider.md`,
   `.claude/output-styles/hy-home.md`, `scripts/hooks/post-tool-validate.sh`,
   `tests/validation/test_provider_native_payloads.py`,
   `tests/validation/test_agent_governance_ci_routing.py`.
   **Retain:** native event identities, `.codex/hooks.json`,
   the W6 prompt route in `scripts/hooks/agent-event-hook.sh`, and
   `scripts/lib/hooks/tool_payload.py`.
   **Interface:** missing optional PostTool lint emits a stable SKIPPED stderr
   record without making the final required gate optional; actual failures
   retain existing exit propagation.

   - [ ] Add `test_post_tool_reports_missing_linters_for_eligible_files` and
     `test_native_config_excludes_runtime_and_broad_scratch_grants`; assert
     shellcheck/yamllint are named only for eligible inputs, with a reason,
     and retained available-linter failures remain nonzero. Run H/N for RED.
   - [ ] Remove broad Compose config/log and Docker inspect automatic grants;
     preserve only justified metadata commands. Remove broad tmp Write/Edit
     grants; do not substitute guessed native permission syntax.
   - [ ] Emit `SKIPPED shellcheck (missing tool)` and equivalent yamllint records.
     Align authored adapters/style with shared evidence rules without copying
     shared policy or changing models/effort/needs_revalidation.
   - [ ] Run H/N and existing hook payload, malformed-input, timeout, Stop and
     scratch-parser regressions. Config parsing is not native delivery evidence.
     Commit as `fix(agent): Narrow native grants and report skipped lint`.

9. **W9: Migrate model-free evaluation and align its consumers.** Primary:
   qa-engineer; documentation contributor: doc-writer; reviewer: eval-engineer.
   Task: `tsk-0009-evaluation-consumers.md`.

   **Move:** the four files `evals/{README.md,agent_output_eval.py,fixture-catalog.md,run-agent-output-eval-fixtures.sh}`
   to the same basenames under `.agents/evaluations/`.
   **Modify after move:** `.agents/evaluations/{README.md,agent_output_eval.py,fixture-catalog.md,run-agent-output-eval-fixtures.sh}`,
   `.agents/governance/providers/registry.yaml`, `scripts/manifest.yaml`,
   `tests/validation/test_agent_output_eval_fixtures.py`,
   `.agents/knowledge/verification-surface-map.md`,
   `docs/05.operations/{guides,policies,runbooks}/0004-harness-agent-first-engineering.md`.
   **Additional audited consumers (modify):**
   `.agents/README.md`, `.agents/governance/bootstrap.md`,
   `.agents/knowledge/repository-map.md`,
   `.agents/skills/provider-model-evaluation/SKILL.md`,
   `scripts/lib/agent_governance/agent_governance_contract.py`,
   `scripts/lib/document_governance/registry.py`,
   `scripts/lib/document_governance/references.py`,
   `scripts/lib/document_governance/metadata/lifecycle.py`,
   `scripts/lib/gate/ci_gate_adapters.py`,
   `scripts/validation/check-script-manifest.py`,
   `scripts/validation/ci_gate_runner.py`, `scripts/README.md`,
   `.github/workflow-contract.yml`, `.github/CODEOWNERS`, `ruff.toml`,
   `docs/99.templates/registry.json`,
   `tests/lib/agent_governance/test_agent_governance_contract.py`,
   `tests/lib/gate/test_ci_gate_adapters.py`,
   `tests/validation/test_validator_entrypoints.py`,
   `tests/validation/test_script_manifest.py`,
   `tests/validation/test_ci_gate_plan.py`,
   `tests/validation/test_ci_gate_execution_context.py`,
   `tests/lib/document_governance/metadata/test_profile.py`,
   `tests/lib/document_governance/test_registry.py`,
   `tests/validation/lifecycle/test_contract.py`,
   `docs/03.specs/0190-agent-contract-hardening/spec.md`,
   `docs/03.specs/0190-agent-contract-hardening/plan.md`.
   This Spec and Plan update their current path references at cutover; completed
   Tasks and frozen historical evidence keep their observed old paths.
   No `.pre-commit-config.yaml` or provider projection path consumer was found;
   verify these retained consumers without manufacturing a change.
   **Consumer transition:** register exactly the four destination files in the
   existing canonical source list and validator whitelist, not an unrestricted
   subtree. In the existing Stage 99 registry, replace the repository-readme
   additional path and add only `.agents/evaluations/fixture-catalog.md` to
   `common.inventory_excludes`: the catalog remains evaluator-owned data without
   document frontmatter. Existing evaluator/manifest/link/canonical checks still
   govern it; test that a sibling unregistered Markdown file remains rejected.
   No directory exemption, new profile, schema or template. The existing metadata
   historical-baseline helper also maps exactly `.agents/evaluations/README.md`
   to the trusted base's `evals/README.md` blob, preserving type/identity checks,
   prior lifecycle status and introduced-body validation. This is historical
   provenance only, never a live loading alias or an initial-state override.
   Add a regression to the existing registry tests for exact-path continuity,
   mismatched type/unrelated destination rejection and retained body checks;
   run that module plus a changed-metadata CLI check against the pre-move base.
   Reuse the existing helper and its reference integration, without another
   migration engine. Bootstrap includes evaluations in its
   canonical language/category boundary while evaluation data stays input, not
   automatically loaded execution instructions. Update manifest roots, both root-relative
   runtime calculations, active document discovery, gate preflight/dispatch and
   changed-path impact. The evaluation prefix retains all-six-suite impact.
   Preserve executable modes and `tests/fixtures/agent-output-eval/`. Migrate
   actual consumers atomically, without a duplicate root source or permanent
   compatibility wrapper.
   **Retain:** runner arguments/results and the five workflow YAML identities.
   Existing modules remain in registered leaves; do not duplicate gates.
   **Interface:** add AOE-RECOVERY-001 using the existing Fixture/score result
   shapes and registry evaluation-threshold mechanism; change only the owned
   subsystem location and required consumers alongside the approved new cases.

   - [ ] Record equivalent pre-move fixture/regression results; update the closed
     canonical-home and all proven active path consumers, then move all four
     files together. Require the same cases/results after the move, no stale
     active caller, no duplicate source, and preserved input/output boundaries.
   - [ ] Pin the recovery rubric before scoring: required input completeness,
     backup/rebuild justification, dependency order, objective/observation
     separation, human approval and refusal of operational execution. Use the
     same existing threshold convention as comparable safety-sensitive fixtures;
     no lower threshold merely to pass a stored response.
   - [ ] Add direct/paraphrased/ambiguous/out-of-scope cases and explicit negative
     cases for a volume mistaken for backup, missing key custody, runtime
     restore instructions and static output claimed as recovery success.
     Record the no-skill baseline and run E to witness missing coverage.
   - [ ] Add fixture and threshold atomically, update exact fixture/category
     expectations, and remove only the obsolete LLM Wiki freshness criterion
     from AOE-DOC-001 and its catalog. Keep historical observations intact.
   - [ ] Correct the generic evaluator wrapper's manifest authority/maintenance
     owner to the current evaluation contract and Task-approved role; align
     operational guidance with safe fixture validation and current consumers.
     Review maintenance/deployment-skeleton/derived modes (T23): include only
     needed assets, never personal state or inherited approval. No unrequested
     packaging implementation; a nonexistent mode needs explicit disposition.
   - [ ] Run E/ET/G/C/L and the existing manifest, validator-entrypoint, gate
     adapter/plan/execution-context, GitHub workflow-contract and document
     registry tests through the registered sanitized unittest adapter. Run
     manifest/workflow checks and renderer check; compare equivalent old/new
     cases and require preserved negative detection. Run project-only skill
     stocktake with the same scope as research, keeping caches outside global
     state. Commit as `test(agent): Align recovery evaluations and consumers`.

10. **W10: Validate, obtain independent acceptance and preserve local work.**
    Primary: qa-engineer; report contributor: doc-writer; reviewers:
    code-reviewer, rules-engineer and iac-reviewer for their respective findings.
    Task: `tsk-0010-final-acceptance.md`.

    **Files:** Task evidence and any independently approved fixes in W2–W9's
    owned paths only; no new cleanup/deletion scope.
    **Interface:** produces numbered acceptance receipts and reviewed commit
    evidence, keeping static/native/hosted/operational results separate.

    - [ ] Verify the file-level dispositions for all retained roles, skills,
      native agents, workflows and commands; record actual consumer changes,
      justified retention, no orphan adapters and no copied authority.
    - [ ] Run the final registered changed/full profiles after the safety
      preflight in Verification. Run the controlled all-files wrapper only from
      a clean linked worktree after reviewed logical commits; never run it
      directly on the shared checkout or use hook bypass/environment SKIP.
    - [ ] Obtain a whole-branch independent review and resolve material findings
      within the retry/scope bounds. Rerun affected checks after fixes, not every
      full suite after every unrelated prose edit.
    - [ ] Use the observation matrix below to request only still-needed concrete
      approvals. Unavailable observations remain BLOCKED/NOT_RUN, not PASS.
      Do not claim all 39 criteria complete if any applicable part is unresolved.
    - [ ] Record each receipt's criterion number, W-number, exact command/exit,
      review and durable owner in its Task. Commit evidence as
      `docs(agent): Record contract hardening verification`; preserve worktree
      and branch without publishing, merging or archiving.

## Risk and Rollback

Each unit is one logical commit or an explicitly coupled small group. Stage only
its reviewed exact files; use `git diff --cached --check` and the repository's
Conventional Commit validator. Do not use `git add .`, reset/clean, force push,
no-verify or hidden environment overrides. Check the diff again after hooks.

Rollback is a reviewed inverse change of the failed unit, followed by its
focused tests. Revert dependent units first when their inputs would disappear;
never remove W3 while W6 relies on its resource contract. Regenerate registered
projections from restored canonical source, compare source bytes and second-run
output, and preserve unknown entries for review. File rollback never restores
services or credentials. Preserve failed evidence and baseline defects.

| Risk | Stop/recovery condition |
| --- | --- |
| Initial-state or parent lifecycle conflict | stop activation; use the existing supported predecessor route or seek a scoped lifecycle decision; never waive the gate |
| Unknown real env/include/secret path during isolation | BLOCKED before Compose; retain source bytes; clean only proven owned temporary paths |
| Resource race, huge graph or unknown local dependency syntax | bounded rejection; no target read, import or execution |
| Changed branch/file ownership while working | stop writer, reconcile actual Git state and approval, rerun affected checks |
| New helper behavior blocks existing callers | compare caller/argument fixtures; fix or revert the same logical unit |
| Native grant removal changes prompting | observe separately on a synthetic target; do not restore broad grants merely to silence prompts |
| Missing tools/cache/image or unsupported account limit | record environment/control blocker; no installation, pull or fictional PASS |
| Semantic review needs an unlisted deletion/rename | produce exact amended disposition and obtain required scope approval first |

## Verification

### Focused command map

Run from the managed repository root. The following are commands, not claimed
results. For registered unittest modules use the existing sanitized adapter;
`env -i` excludes session-injected control variables, not a failed check.

| ID | Command | Expected result |
| --- | --- | --- |
| L | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.lib.document_governance.test_links -v` | named link regressions pass |
| G | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.lib.agent_governance.test_agent_governance_contract -v` | valid resources pass; unsafe fixtures reject |
| H | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.validation.test_agent_governance_ci_routing -v` | helper and hook-routing regressions pass |
| P | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.validation.test_provider_native_surfaces tests.validation.test_provider_surface_renderer tests.validation.test_agent_function_routes -v` | source preservation, invocation and routing pass |
| N | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.validation.test_hook_rules tests.lib.hooks.test_tool_payload tests.validation.test_provider_native_payloads -v` | malformed/unsafe payloads reject; retained routes pass |
| E | `rtk proxy bash evals/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` | all fixture and regression checks pass |
| ET | `rtk proxy env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 python3 scripts/lib/gate/ci_gate_adapters.py run-unittest tests.validation.test_agent_output_eval_fixtures -v` | evaluator mutation/negative cases pass |
| C | `rtk proxy python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all` | repository contract passes |
| R | `rtk proxy python3 scripts/operations/provider_surface_renderer.py --check` | zero projection drift |
| D | `rtk proxy python3 scripts/validation/run-ci-gate.py --profile changed` | selected registered gates exit 0 |
| F | `rtk proxy python3 scripts/validation/run-ci-gate.py --profile full` | all authorized registered gates exit 0; otherwise explicit blocker |

E uses the listed current path through W8; after W9 cutover use
`.agents/evaluations/run-agent-output-eval-fixtures.sh` with identical arguments.
W9 updates this command table and all active consumers at cutover.
E steps also run ET after implementation. W2 additionally runs
`rtk proxy python3 scripts/validation/check-document-links.py --mode entrypoint`.
W6's writes use `rtk proxy python3 scripts/operations/provider_surface_renderer.py --write`.
No direct unittest path or copied shell wrapper replaces the admitted route.

Before D/F, inspect `--explain`, the selected leaves and their side effects.
The existing profiles can launch a disposable conftest container or render
Compose; they are not daemon-free simply because their name is validation.
Use a reviewed secret-free fixture checkout and already-present tools/images;
if the selected route would access real environment, create host data, pull an
image or require broader approval, record the gate BLOCKED and run its safe
focused checks. Do not weaken selectors or count omitted required leaves as PASS.

The final wrapper is
`rtk proxy bash scripts/validation/run-agent-precommit-all-files.sh --task docs/03.specs/0190-agent-contract-hardening/tasks/tsk-0010-final-acceptance.md`
followed by one `--allow-prefix` for each exact reviewed owned file that hooks may
change. The executor constructs that argument list from the Task's reviewed
file map; no broad directory wildcard. Preconditions: clean linked worktree,
tracked Task, approved all-files scope, installed dependencies and inspected
hook side effects. Do not trigger automatic environment installation if caches
are missing. CI-only `run-ci-precommit.sh` stays hosted-only.

Behavior changes require witnessed RED/GREEN, branch/error/security cases and
existing integration/CLI tests. Measure affected executable coverage with an
already-installed supported coverage route, targeting the requested 80%; do
not infer coverage from passing counts or install a tool to create evidence.
Document-only changes use metadata/link/semantic checks, not artificial tests.

### Acceptance ownership

Every numbered Spec criterion has a primary Task owner below. Cross-unit
receipts cite the other Task's evidence rather than duplicating results.

| Criterion | Primary unit | Supporting units | Required scenario families |
| --- | --- | --- | --- |
| R01 | W6 | none | T10,T28 |
| R02 | W6 | W3/W9 | T03,T04,T22,T29 |
| R03 | W2 | W7 | T21 |
| R04 | W8 | W4/W6/W9/W10 | T12,T13,T24 |
| R05 | W6 | W8/W10 | T10,T11,T13,T30 |
| R06 | W7 | W9 | T25 |
| R07 | W7 | none | T26 |
| R08 | W7 | W2/W9 | T21,T26,T31 |
| R09 | W4 | W5/W7/W8/W10 | T05,T06,T32 |
| R10 | W8 | W7 | T27 |
| R11 | W2 | W3/W4/W5/W6/W7/W9 | T03,T21,T33 |
| R12 | W3 | W4/W5/W6/W7/W8/W9 | T01,T02,T04,T05,T06,T24,T29 |
| R13 | W10 | W6/W7/W8 | T11,T13,T18,T30 |
| R14 | W7 | W9/W10 | T14,T15,T25 |
| R15 | W9 | W6/W8/W10 | T11,T12,T13,T23,T30 |
| R16 | W8 | W6/W7/W10 | T13,T27 |
| R17 | W7 | W4/W5/W8/W10 | T16,T32 |
| R18 | W10 | W4/W5/W8 | T17,T32 |
| R19 | W7 | W4/W10 | T05,T18 |
| R20 | W9 | W4/W7/W8/W10 | T12,T16,T19,T23,T24,T31 |
| R21 | W7 | W9/W10 | T19 |
| R22 | W7 | W10 | T14,T15,T26 |
| R23 | W2 | none | T07,T08,T09 |
| R24 | W6 | W9 | T04 |
| R25 | W3 | none | T01,T02 |
| R26 | W3 | W6/W9 | T01,T02,T03,T29 |
| R27 | W6 | W3/W9 | T04,T22,T29 |
| R28 | W6 | none | T10,T28 |
| R29 | W6 | W8/W9/W10 | T10,T22,T30 |
| R30 | W7 | W2/W4/W8 | T21,T24 |
| R31 | W9 | W2/W6/W8/W10 | T07,T08,T11,T13,T23 |
| R32 | W9 | none | T20 |
| R33 | W9 | W2/W4/W5/W7 | T09,T21,T25,T33 |
| R34 | W4 | W2/W5/W7/W9 | T05,T06,T09,T21,T33 |
| R35 | W6 | none | T28 |
| R36 | W6 | W2/W3/W4/W5/W9 | T29,T33 |
| R37 | W6 | W8/W10 | T30 |
| R38 | W7 | W9 | T31 |
| R39 | W4 | W2/W5/W8/W9/W10 | T32,T33 |

### Separately observed acceptance

| Required evidence | Concrete bounded next observation | Current disposition |
| --- | --- | --- |
| Native discovery/invocation and hook delivery | approved installed Claude/Codex session on one synthetic repository target; record version, role/skill/event, denial and result metadata | NOT_RUN; no extra model call or hook trust change now |
| Model entitlement and supported budget ceiling | identify account kind and documented control without auth-file reads; request an explicit call/time/token/spend cap and synthetic refusal observation | BLOCKED until a real supported control exists; no new inference service |
| Editor command/selection behavior | user-approved installed editor/version on a synthetic document with explicit action ID; preserve bindings | NOT_RUN; CLI parsing cannot substitute |
| Hosted CI/required checks and issue coordination | read approved changed revision's hosted status and relevant settings after publication is separately authorized | NOT_RUN; no push, issue mutation or CI dispatch now |
| Recovery readiness versus recovery success | review sanitized recovery contract locally; actual restore remains a separate operational task | review covered by W6/W9; operational success unclaimed |
| All-files/coverage/tool-dependent checks | inspect installed tools/cache and exact clean-worktree wrapper scope before execution | environment-dependent; absent evidence cannot close acceptance |

## Rulings

- The human approved the written Spec and this Plan for local execution on
  2026-09-29. Initial drafts were committed before lifecycle promotion. Approval
  permits the named implementation; it does not establish acceptance results.
  Local lifecycle commits are executable after Plan approval; an eventual PR
  against a base without the draft still requires separately approved sequential
  integration. This Plan does not promise one-shot mergeability or authorize it.
- User-selected executing-plans/in-session work takes precedence over the
  writing-plans skill's alternative fresh-agent-per-task recommendation. Existing
  independent specialists may review bounded units, followed by whole-branch review.
- The Stage 99 Plan template owns heading shape and location. Skill guidance is
  represented under these registered sections, without a second plans directory.
- No Task template changes, new Stage 99 fields, resource manifest, runtime
  budget engine, model switch, editor integration or remote coordination setup.
- Applicable BLOCKED/NOT_RUN evidence keeps the package open. Local implementation
  may be reported separately, but all-criteria completion cannot be claimed until
  observation requirements pass or the user explicitly changes the requirement.

- W3 independent review reproduced quadratic scanning in the reused Markdown
  opener patterns before the resource graph bound applies. Extend W3 by the
  existing shared parser and its test file before editing them; exclude nested
  opening brackets from two character classes and consume destination spans
  once rather than rescanning overlapping malformed openers; retain the parser interface,
  and add L. Retain a pre-parse 16,384-opening-bracket limit as a separate
  output/allocation bound because the shared parser materializes link records;
  this bound does not substitute for fixing repeated CPU work. No new parser.

- W3 shared parser completion consumes complete link/title spans, masks hidden
  grammar contexts, handles escape parity, and extracts exact HTML attributes
  with the standard library. Comment/frontmatter content is not a procedure
  consumer. These corrections remain within the amended six-file map.

- On 2026-09-29 the owner explicitly changed the evaluation disposition to
  migration into `.agents/evaluations/`. This supersedes root retention. W7
  still edits the existing location before W9; W9 moves the resulting subsystem
  and updates its exact audited consumers. The existing Stage 99 README
  path mapping and exact code-owned catalog inventory exclusion are included;
  no structural schema/template change is needed.
  Other work units and external/runtime
  boundaries remain unchanged. No migration write precedes its completed map.

- Read-only W9 preflight found that changed-metadata selection discards Git
  rename pairs and the base corpus excludes the old root evaluation README.
  Without historical continuity the active moved README fails initial-state
  validation. Add only the existing metadata lifecycle helper and registry
  regression module to W9's exact map before implementation; retain the current
  reference integration and all state/type/body checks. This is necessary for
  the user-authorized migration, not approval to relax lifecycle validation.
