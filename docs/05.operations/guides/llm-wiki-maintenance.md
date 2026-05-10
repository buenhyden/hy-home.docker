---
status: active
---

# LLM Wiki Maintenance Operations

## Overview (KR)

이 문서는 `hy-home.docker`의 repo-local LLM Wiki를 갱신하고 검증하는 운영 가이드다. LLM Wiki는 source contents를 합치는 문서가 아니라, LLM 에이전트가 안전하게 canonical path를 찾도록 돕는 index layer다.

## Policy Scope

이 가이드는 루트 `llms.txt`, `docs/90.references/llm-wiki/`, `scripts/generate-llm-wiki-index.sh`, `wiki-curator` 역할의 운영 절차를 다룬다.

## Applies To

- **Systems**: `hy-home.docker` documentation and agent-governance surfaces
- **Agents**: `wiki-curator`, `doc-writer`, `workflow-supervisor`
- **Environments**: local repository worktree and CI validation

## Usage

- Root entrypoints, agent governance docs, operations docs, script inventory, infrastructure indexes, or LLM Wiki files changed.
- A validator reports stale LLM Wiki output.
- An AI agent needs a safe repo-local path index before broader repository exploration.

## Controls

- **Required**:
  - Keep `llms.txt` as a thin entrypoint.
  - Keep `repository-map.md` curated and source-backed.
  - Regenerate `docs/90.references/llm-wiki/index.md` with `bash scripts/generate-llm-wiki-index.sh`.
  - Verify freshness with `bash scripts/generate-llm-wiki-index.sh --check`.
- **Allowed**:
  - Link to tracked source paths, README files, governance docs, operations docs, scripts, and infrastructure indexes.
  - Use Graphify output as advisory navigation context when corroborated with tracked source files.
- **Disallowed**:
  - Public website or public wiki deployment.
  - `llms-full.txt` or full-content export.
  - External model calls or network publishing.
  - Secret contents, credentials, private keys, tokens, shell history, raw logs, `volumes/`, dependency trees, generated/minified artifacts, or `graphify-out/` as evidence.

## Procedure

1. Review the changed paths and decide whether they affect LLM-facing navigation.
2. Run the generator.

   ```bash
   bash scripts/generate-llm-wiki-index.sh
   ```

3. Confirm the generated index is fresh.

   ```bash
   bash scripts/generate-llm-wiki-index.sh --check
   ```

4. Run repository contracts after LLM Wiki changes.

   ```bash
   bash scripts/check-repo-contracts.sh
   bash scripts/check-doc-traceability.sh
   ```

5. If Graphify output is needed for navigation, report its advisory health instead of treating it as source truth.

   ```bash
   bash scripts/report-graphify-health.sh
   ```

## Exceptions

- Do not add a new LLM Wiki source category when the same navigation need is already covered by `repository-map.md` or the generated index.
- Do not add runtime hooks for LLM Wiki refresh unless a later task establishes a concrete failure mode that the existing post-tool validation cannot catch.
- Escalate to the user before including any path that may expose private values or user-specific runtime data.

## Verification

- `bash scripts/generate-llm-wiki-index.sh --check` passes.
- `bash scripts/check-repo-contracts.sh` passes.
- `bash scripts/check-doc-traceability.sh` passes.
- LLM Wiki files contain no absolute filesystem links, filesystem URI links, public-site scope drift, or Graphify-as-authority wording.

## Review Cadence

- Review after changes to root entrypoints, `docs/00.agent-governance/`, `docs/05.operations/`, `docs/90.references/llm-wiki/`, `infra/README.md`, `scripts/README.md`, or `secrets/README.md`.
- Review during repository contract failures that mention LLM Wiki freshness or boundary wording.

## AI Agent Policy Section

- **Model / Prompt Change Process**: `wiki-curator` uses `model: sonnet` and imports `docs/00.agent-governance/scopes/docs.md`.
- **Eval / Guardrail Threshold**: stale index, unsafe path inclusion, or forbidden wording is a blocking validation failure.
- **Log / Trace Retention**: record final verification evidence in `docs/00.agent-governance/memory/progress.md`; do not paste raw secret-adjacent logs.
- **Safety Incident Thresholds**: suspected secret exposure or public-scope drift requires immediate stop and user escalation.

## Related Documents

- **Spec**: [../../03.specs/llm-wiki-agent-first-completion/spec.md](../../03.specs/llm-wiki-agent-first-completion/spec.md)
- **Plan**: [../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md)
- **Task**: [../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md)
- **LLM Wiki References**: [../../90.references/llm-wiki/README.md](../../90.references/llm-wiki/README.md)
- **Generator**: [../../../scripts/generate-llm-wiki-index.sh](../../../scripts/generate-llm-wiki-index.sh)
