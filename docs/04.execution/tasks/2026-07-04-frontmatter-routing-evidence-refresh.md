---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md -->

# Task: Frontmatter Routing Evidence Refresh

## Overview

This task records the follow-up refresh for the document-contract frontmatter
routing profile after the examples scaffold remediation, remote GitHub
reverification, infra tech-stack version refresh, and Graphify refresh commits.
It updates the current missing-frontmatter count and resolves the provider README
routing wording without adding frontmatter to provider, generated, GitHub-native,
root, or archive files.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md)
- **Frontmatter Routing Profile**: [Frontmatter routing profile](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Provider README Evidence**: [Gemini shared runtime README](../../../.agents/README.md), [Codex runtime surface README](../../../.codex/README.md)

## Working Rules

- Preserve the original 185-file inventory as source audit evidence.
- Refresh only current-state routing evidence and gap-register residual wording.
- Do not add frontmatter to README files, generated Graphify reports,
  GitHub-native Markdown, root special-purpose Markdown, or legacy archive
  material as a bulk style fix.
- Do not change provider runtime behavior, generated Graphify output, GitHub
  settings, Compose files, secrets, credentials, tokens, private keys, raw logs,
  shell history, or `.env` values.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md`; `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md` | User continuation for the next document-contract follow-up; routing-profile update trigger | Current frontmatter routing evidence | The routing profile still said 185 current files and kept provider README routing as deferred even though `WDC-GAP-024` classified provider README profiles as no-action. | The routing profile now records 184 current files, examples closed, Graphify generated reports at 4, and provider README routing as optional/no-action. | `git revert` the evidence-refresh commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, provider config changes, generated Graphify output mutation, GitHub setting changes, or broad Markdown corpus rewrites |
| `docs/04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md`; `docs/04.execution/tasks/README.md`; `docs/00.agent-governance/memory/progress.md`; `docs/90.references/llm-wiki/llm-wiki-index.md` | Stage 04 traceability and index freshness requirements | Task evidence, task index, progress memory, and generated knowledge index | No task evidence existed for this refresh. | Task evidence and indexes record the current routing refresh. | `git revert` the evidence-refresh commit | Same redaction boundary as above |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Re-run the current first-line frontmatter scan and classify the remaining missing set. | doc | N/A | PLN-WDC-RM-008 follow-up | Current classifier reports 184 total files and 0 unclassified paths. | Codex | Done |
| T-002 | Refresh routing profile counts and provider README decision wording. | doc | N/A | PLN-WDC-RM-008 follow-up | `frontmatter-routing-profile.md` records provider README optional/no-action and examples closed. | Codex | Done |
| T-003 | Update the gap register, task index, progress log, and LLM Wiki index. | doc | N/A | PLN-WDC-RM-008 follow-up | Register update row and generated index freshness checks. | Codex | Done |
| T-004 | Run documentation and repository contract validation. | doc | N/A | VAL-WDC-RM-001 through VAL-WDC-RM-008 | Verification Summary. | Codex | Done |

## Verification Summary

- **Test Commands**:
  - `zsh -fc 'git ls-files -z "*.md" | while IFS= read -r -d "" f; do first=$(sed -n "1p" "$f"); [[ "$first" == "---" ]] && continue; print -r -- "$f"; done | wc -l'`
  - `zsh -fc 'stage=0; infra=0; workspace=0; provider=0; example=0; github=0; graphify=0; root=0; archive=0; other=0; git ls-files -z "*.md" | while IFS= read -r -d "" f; do first=$(sed -n "1p" "$f"); [[ "$first" == "---" ]] && continue; case "$f" in docs/*) ((stage++));; infra/*) ((infra++));; .agents/README.md) ((provider++));; examples/*) ((example++));; .github/*) ((github++));; graphify-out/*) ((graphify++));; README.md|CHANGELOG.md|RTK.md) ((root++));; archive/*) ((archive++));; projects/*|scripts/*|secrets/*|tests/*) ((workspace++));; *) ((other++)); print -r -- "OTHER $f";; esac; done; print -r -- "stage=$stage"; print -r -- "infra=$infra"; print -r -- "workspace=$workspace"; print -r -- "provider=$provider"; print -r -- "example=$example"; print -r -- "github=$github"; print -r -- "graphify=$graphify"; print -r -- "root=$root"; print -r -- "archive=$archive"; print -r -- "other=$other"; print -r -- "total=$((stage+infra+workspace+provider+example+github+graphify+root+archive+other))"'`
  - `rg -n 'Provider README routing remains deferred|provider/examples deferred|Path classification of the 185 files|all 185 files' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md`
  - `git diff --check`
  - `git diff --cached --check`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - `bash scripts/operations/sync-provider-surfaces.sh --check`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/check-doc-implementation-alignment.sh`
  - `bash -n scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-repo-contracts.sh`
- **Eval Commands**: N/A for documentation-only evidence refresh.
- **Logs / Evidence Location**: This task document and the refreshed source
  `frontmatter-routing-profile.md`.
- **Results**:
  - PASS: current first-line scan reports 184 tracked Markdown files without
    top frontmatter.
  - PASS: classifier reports `stage=100`, `infra=66`, `workspace=6`,
    `provider=1`, `example=0`, `github=3`, `graphify=4`, `root=3`,
    `archive=1`, `other=0`, `total=184`.
  - PASS: stale deferred-provider and old current-count wording has been
    removed from the active routing/register text; original 185-file source
    inventory is preserved as historical audit evidence.
  - PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1132
    paths and the freshness check passed.
  - PASS: documentation and repository contract validation commands completed
    successfully.
- **Manual Checks**: Confirmed the diff does not add frontmatter to the 184
  routed files, mutate `.agents/README.md` or `.codex/README.md`, edit generated
  Graphify reports, change GitHub-native Markdown behavior, inspect secret
  values, change Compose files, or alter runtime behavior.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md)
- **Frontmatter Routing Profile**: [Frontmatter routing profile](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md)
- **Examples Scaffold Remediation Task**: [Examples scaffold contract remediation](./2026-07-04-examples-scaffold-contract-remediation.md)
- **Infra Tech-Stack Version Refresh Task**: [Infra tech-stack version refresh](./2026-07-04-infra-tech-stack-version-refresh.md)
