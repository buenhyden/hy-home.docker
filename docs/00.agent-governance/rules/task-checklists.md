---
layer: agentic
---

# Task Checklists

Unified task execution checklists for all agent work.

## 1. Pre-Task Checklist

- [ ] Confirm active persona, layer, and primary scope.
- [ ] Confirm editable scope for this task.
- [ ] For implementation-agent work, confirm the approved plan exists and every planned edit maps to it.
- [ ] Check whether a requested or obviously applicable skill/workflow strategy
      changes how the task should be performed; map its outputs to canonical
      repository stages before editing.
- [ ] Confirm whether `docs/01` to `docs/99` are in read-only mode.
- [ ] Identify required input documents (PRD, ARD, ADR, Specs, Plans, Tasks).
- [ ] For audit/review/validation gaps, classify the canonical owner with
      `documentation-protocol.md` gap-to-stage routing before editing.
- [ ] Review `docs/00.agent-governance/memory/README.md` and `progress.md`; retrieve relevant memory notes when the task touches governance, docs, runtime, or repeated failures.
- [ ] Identify ambiguity. Ask before state changes if a wrong assumption could
      change scope, policy, security posture, or verification outcome.
- [ ] Treat ambiguity as blocking before planning, implementation, model/config
      changes, or completion claims when the answer cannot be discovered from
      repository evidence.
- [ ] For model, reasoning-effort, provider adapter, hook, or CI/CD config
      changes, confirm the governing Stage 00 policy and validator support
      before editing.
- [ ] For high-risk approved surfaces, bind the approval to concrete evidence
      before editing: policy, runtime, CI, templates, secrets, remote GitHub,
      model policy, and provider adapters require a Stage 04 task record that
      names the target surface, approval source, validation command, rollback or
      recovery path, and redaction boundary.
- [ ] Identify key risks (security, data loss, breaking changes, governance drift).
- [ ] Define verification commands and acceptance criteria before edits.
- [ ] If full-repository pre-commit is planned, confirm that it is the approved
      final QA gate and name the tracked task path plus minimal allowed prefixes.

## 2. In-Task Checklist

- [ ] Keep changes within declared editable scope.
- [ ] Preserve audit/planning/implementation/verification separation when the workflow defines those roles.
- [ ] Keep external strategy outputs in canonical stage paths; do not create
      active non-stage specs, plans, or task logs.
- [ ] Preserve SSoT traceability across affected documentation artifacts.
- [ ] Route each new gap to exactly one canonical owner first; use downstream
      links instead of duplicating rules or evidence across stages.
- [ ] Maintain language policy consistency (English governance, Korean human-facing docs).
- [ ] Keep assumptions explicit and update them when repository evidence disproves them.
- [ ] Validate new/changed links as edits are made.
- [ ] For changed/new target Markdown, run the typed metadata checker with an
      explicit safe base; do not treat the advisory full inventory as a gate.
- [ ] When a document is modified, update the parent folder `README.md` if the change affects the folder's description of that document (title, status, scope, or summary-level content); see DOCS 3 R2 in `rules/documentation-protocol.md`.
- [ ] Remove stale, conflicting, or nonexistent references in editable scope.
- [ ] Record template deviations or explicit N/A rationale in task evidence; do
      not silently normalize historical artifacts outside the approved scope.
- [ ] For approved secret work, record metadata, IDs, paths, or rotation evidence
      only; never paste secret values into docs, logs, commits, PRs, or summaries.
- [ ] For approved remote GitHub work, record the repository, remote surface,
      command class, before/after evidence, and any unverified remote gate.
- [ ] Keep provider adapters aligned with Stage 00 lifecycle terms:
      discovery -> applicability -> provider loading -> canonical artifact ->
      validation evidence.
- [ ] Update `docs/00.agent-governance/memory/progress.md` for material task progress.
- [ ] Never run `pre-commit run` directly. The approved final QA all-files gate
      uses only `scripts/validation/run-agent-precommit-all-files.sh` from an
      initially clean linked worktree; stop on unexpected paths without cleanup.
- [ ] Record out-of-scope issues instead of patching read-only stages.

## 3. Completion Checklist

- [ ] Run relevant repository checks for changed layers.
- [ ] Confirm each implemented change is traceable to the approved plan when an approved-plan gate applies.
- [ ] Validate link integrity for changed root/governance files.
- [ ] Inspect the post-edit diff after hook-managed formatting or style checks.
- [ ] Confirm new documents cannot use the legacy metadata exception and any
      reverse lifecycle transition has explicit scoped Stage 04 override evidence.
- [ ] Confirm no contradictory policy statements were introduced.
- [ ] Confirm any HADS usage follows the mandatory
      `docs/90.references/data/hads/` profile when applicable, or is explicitly
      approved/documented as advisory elsewhere.
- [ ] Confirm completion criteria are satisfied for the affected stage(s).
- [ ] Confirm any attachment gap coverage, template exceptions, or model/config
      uncertainty was either resolved in editable scope or recorded as a human
      approval gate.
- [ ] Confirm approved high-risk surface evidence is recorded in the task
      document, including whether runtime, secrets, remote GitHub, model, or
      provider adapter state was actually changed or only verified.
- [ ] Confirm QA/CI/CD evidence includes local checks, CI-only gates, and
      skipped-check rationale appropriate to the change type.
- [ ] When the controlled pre-commit gate applies, record command, allowed
      prefixes, hook exit, modified paths, unexpected-path review disposition,
      and skipped rationale; the wrapper never writes this evidence itself.
- [ ] Update `docs/00.agent-governance/memory/progress.md` with final status, verification evidence, and memory note links.
- [ ] Create/update out-of-scope or durable finding reports from `docs/99.templates/templates/governance/memory.template.md` when needed.
- [ ] For completed repository-modifying agent work, create logical Conventional Commits or record why commits were intentionally skipped.
- [ ] Summarize what changed, what was verified, and what remains out-of-scope.

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/persona.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
