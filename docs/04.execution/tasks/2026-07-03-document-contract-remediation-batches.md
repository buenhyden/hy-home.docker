---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md -->

# Task: Document Contract Remediation Batches

## Overview

This task records execution evidence for the document-contract remediation
batches that follow the completed workspace document contract audit pack. The
first work unit creates this evidence file, confirms the current
`WDC-GAP-*` baseline, and preserves protected boundaries before any target
corpus remediation begins.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Execute one remediation batch at a time.
- Do not apply target corpus fixes without the matching batch approval.
- Keep provider, workflow, validator, secret-handling, infra, and target-stage
  edits in separate logical commits.
- Treat Stage 00 governance and Stage 99 template contracts as the source of
  truth; provider files are adapters, not owners.
- Do not inspect secret values, credentials, tokens, certificates, private
  keys, raw logs, shell history, or `.env` values.
- Keep existing infra image/version drift out of documentation batches unless
  an infra-specific task is approved.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` | Approved remediation batch plan and user continuation | Execution evidence | File absent | Task evidence records baseline and future batch status | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/04.execution/tasks/README.md` | Task-stage routing contract | Task index | Remediation batch task not listed | Active task linked in structure and related documents | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `projects/README.md`; `projects/storybook/README.md`; `projects/storybook/nextjs/README.md` | PLN-WDC-RM-003 and user continuation for the next approved batch | Project README profile and template-link cleanup | Project READMEs used `Related References`, removed flat README template links, and `projects/README.md` still named obsolete operations-stage paths. | Project READMEs use `Related Documents`, canonical common README template links, and current Stage 03/04/05 taxonomy wording. | `git revert` the T-003 README batch commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `secrets/README.md` | PLN-WDC-RM-003 secret README approval with redaction boundary | Secret README profile and template-link cleanup | Secret README used `Related References`, duplicated the operations README link, and linked a removed flat README template path. | Secret README uses `Related Documents`, one operations README link, and the canonical common README template link. | `git revert` the T-003 README batch commit | Read only `secrets/README.md`; do not inspect secret value files, credentials, tokens, private keys, certificates, raw logs, shell history, or `.env` values |
| `tests/README.md` | PLN-WDC-RM-003 and user continuation for the next approved batch | Tests README profile cleanup | Tests README used `Related References`. | Tests README uses `Related Documents`. | `git revert` the T-003 README batch commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/05.operations/guides/06-observability/loki.md`; `docs/05.operations/policies/06-observability/01.retention.md`; `docs/05.operations/policies/06-observability/loki.md`; `docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md` | PLN-WDC-RM-004 and user continuation for the next approved batch | Stage 05 operations frontmatter metadata cleanup | Three observability docs used generic `updated` metadata plus path-derived metadata, and the workspace harness policy carried a non-standard policy-state key. | The four active Stage 05 docs now keep lifecycle `status: active` only in frontmatter; path, title, component, runtime, and enforcement context remain represented by target path, headings, and body sections. | `git revert` the T-004 operations metadata commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, or runtime config changes |
| `docs/01.requirements/2026-03-26-01-gateway.md`; `docs/01.requirements/2026-03-26-02-auth.md`; `docs/01.requirements/2026-03-26-06-observability.md`; `docs/01.requirements/2026-03-26-07-workflow.md` | PLN-WDC-RM-004 and user continuation for the next approved batch | PRD AI agent section heading normalization | Four active PRD docs used `## AI Agent Requirements` while the PRD template and 20 peer requirement docs use `## AI Agent Requirements (If Applicable)`. | The four PRD outliers now use the template heading. | `git revert` the T-004 requirements heading commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, runtime config, or requirement-body scope changes |
| `infra/01-gateway/traefik/README.md`; `infra/01-gateway/nginx/README.md` | PLN-WDC-RM-004 and user continuation for the next approved batch | Infra README validation heading normalization | Two gateway README files used `## Validation Commands` in addition to their canonical `## Validation` sections. | The command tables are merged into the existing `## Validation` sections, leaving no `Validation Commands` heading split. | `git revert` the T-004 infra validation heading commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, runtime config, or Compose behavior changes |
| `docs/99.templates/support/frontmatter-contract.md`; `docs/90.references/audits/document-contracts/frontmatter-routing-profile.md`; `docs/90.references/audits/document-contracts/README.md` | PLN-WDC-RM-004 and user continuation for the next approved batch | Frontmatter routing profile decision | WDC-GAP-006 recorded 185 tracked Markdown files without top frontmatter and required profile-specific routing before corpus edits. | The missing set is classified by surface as required, optional, deferred, or declined; no non-README active target-stage leaf document remains unrouted. | `git revert` the T-004 frontmatter routing commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, runtime config, generated report mutation, GitHub-native behavior, or broad corpus rewrite |
| `docs/90.references/audits/document-contracts/ci-qa-parser-graphify-decision.md`; `docs/90.references/audits/document-contracts/README.md` | PLN-WDC-RM-005 and user continuation for the next approved batch | CI/CD, QA, parser, and Graphify decision evidence | WDC-GAP-010 and WDC-GAP-011 required decisions for dependency-audit gates and Graphify enforcement; WDC-GAP-018 needed parser/tooling classification. | Current coverage and no-change decisions are documented: dependency audit hard gates require future Security/QA approval, Graphify remains advisory, and parser matches are tooling follow-up only. | `git revert` the T-005 decision commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, workflow changes, script changes, pre-commit changes, generated Graphify output changes, or Markdown content rewrites |
| `docs/90.references/audits/document-contracts/historical-evidence-preservation.md`; `docs/90.references/audits/document-contracts/README.md` | PLN-WDC-RM-006 and user continuation for the next approved batch | Historical evidence preservation decision | WDC-GAP-012 through WDC-GAP-015 required a decision on whether old baselines, completed docs, archive tombstones, and progress evidence should be rewritten. | The historical rows are preserved as audit and migration evidence; no completed artifacts or archive material were rewritten. | `git revert` the T-006 preservation commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, completed spec/plan/task rewrites, archive tombstone rewrites, or historical progress rewrites |
| Future protected surfaces | Parent plan approval gates | Provider, workflow, validator, secret-handling, infra, and target-stage changes | No remediation applied in T-001 | Future tasks must record per-batch evidence before edits | Revert the specific future batch commit | Redaction boundary must be restated in each future batch before touching protected surfaces |

## Task Table

| Task ID | Description | Type | Parent Plan / Phase | Source Gaps | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create task evidence and confirm current gap-register baseline. | doc | PLN-WDC-RM-001 | All rows | Baseline counts and validation matrix | Codex | Done |
| T-002 | Fix active governance and provider adapter drift. | doc | PLN-WDC-RM-002 | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Provider sync and repo contracts | Codex | Done |
| T-003 | Normalize README profiles by surface. | doc | PLN-WDC-RM-003 | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | README/template drift checks | Codex | Done |
| T-004 | Normalize target-stage frontmatter and section profiles. | doc | PLN-WDC-RM-004 | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Inventory rerun and profile exceptions | Codex | Done |
| T-005 | Decide CI/CD, QA, parser, and Graphify enforcement. | doc/script | PLN-WDC-RM-005 | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Protected-surface checks | Codex | Done |
| T-006 | Preserve or reclassify historical evidence rows. | doc | PLN-WDC-RM-006 | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Historical evidence review | Codex | Done |
| T-007 | Execute infra drift only as a separate infra task if approved. | ops | PLN-WDC-RM-007 | WDC-GAP-020, WDC-GAP-021 | Infra-only validation | Codex | Deferred |
| T-008 | Close batch evidence, update register dispositions, regenerate indexes, and commit. | doc | PLN-WDC-RM-008 | All touched rows | Final validation matrix and commit trail | Codex | Planned |

## Baseline Snapshot

| Measure | Command | Result |
| --- | --- | ---: |
| Total `WDC-GAP-*` rows | `rg '^\| WDC-GAP-[0-9]{3} ' docs/90.references/audits/document-contracts/gap-register.md \| wc -l` | 30 |
| `direct-fix` rows | Row count filtered by disposition `direct-fix`. | 0 |
| `batch-fix` rows | Row count filtered by disposition `batch-fix`. | 11 |
| `historical-evidence` rows | Row count filtered by disposition `historical-evidence`. | 4 |
| `out-of-scope-gap` rows | Row count filtered by disposition `out-of-scope-gap`. | 7 |
| `no-action` rows | Row count filtered by disposition `no-action`. | 8 |

## Batch Status

| Batch | Source Rows | Current Status | Boundary |
| --- | --- | --- | --- |
| Governance and provider adapter drift | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Local adapter drift done; remote evidence deferred | WDC-GAP-001 and WDC-GAP-002 were remediated by making Gemini, Claude, and generated Codex adapter text defer to Stage 00 owners. WDC-GAP-022 still requires separate remote GitHub re-verification approval. |
| README profile normalization | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | Approved surfaces done; examples deferred | Projects, secrets, and tests README surfaces were remediated. `secrets/README.md` was handled as metadata-only documentation and no secret value files were inspected. WDC-GAP-017 remains deferred because `examples/**` needs a separate examples/scaffold contract decision. |
| Target-stage frontmatter and section profiles | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Done | WDC-GAP-007 and WDC-GAP-016 were remediated for active Stage 05 operations metadata. WDC-GAP-008 was remediated by aligning active PRD AI-agent section headings with the PRD template. WDC-GAP-009 was remediated by merging gateway README validation command tables into the canonical `## Validation` sections. WDC-GAP-006 was closed by classifying missing-frontmatter surfaces into required, optional, deferred, and declined profiles without a broad corpus rewrite. |
| CI/CD, QA, parser, and Graphify decisions | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Done; protected implementation deferred | Current coverage and decisions are recorded without mutating workflows, scripts, validators, pre-commit config, Graphify output, or Markdown content. Hard dependency-audit gates and Graphify hard gates require separate Security/QA or knowledge-graph approval. |
| Historical evidence preservation or reclassification | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Done | Historical baselines, completed artifacts, archive tombstones, legacy archive material, and progress rows are preserved. Future cleanup requires proof of active-consumption conflict. |
| Infra drift follow-up | WDC-GAP-020, WDC-GAP-021 | Deferred | Requires separate infra task and runtime-change approval if Compose changes. |

## Validation Results

| Scope | Command | Result |
| --- | --- | --- |
| Gap baseline | Baseline `rg ... \| wc -l` commands listed in `## Baseline Snapshot` | PASS: register still has 30 rows with disposition distribution `0/11/4/7/8`. |
| Task path pre-check | `test -f docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` before creation | PASS: command exited non-zero before creation, confirming the evidence file was new. |
| Target corpus boundary | Manual diff review | PASS: T-001 creates task evidence and task index only; no target corpus remediation is applied. |
| LLM Wiki regeneration | `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1128 paths after the T-006 historical preservation update. |
| Historical evidence source review | Reads of `frontmatter-inventory.md`, `readme-profile-inventory.md`, `section-profile-inventory.md`, and `template-application-gaps.md` | PASS: WDC-GAP-012 through WDC-GAP-015 source rows are audit baselines, completed evidence, archive/tombstone evidence, or old-path migration history. |
| Historical evidence preservation scan | `rg -n -e 'docs/99\.templates/readme\.template' -e 'docs/99\.templates/service\.template' -e 'Related References' -e 'status: completed' -e 'status: archived' docs/03.specs docs/04.execution docs/98.archive archive docs/00.agent-governance/memory/progress.md --glob '*.md'` | PASS: matches are preserved historical or archive evidence; no active-guidance rewrite was applied in T-006. |
| Whitespace | `git diff --check` | PASS: no whitespace errors. |
| LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS: generated LLM Wiki index is fresh. |
| Provider surfaces | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS: `failures=0`. |
| Implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS: `failures=0`. |
| Repo contract syntax | `bash -n scripts/validation/check-repo-contracts.sh` | PASS: shell syntax is valid. |
| Full repo contract | `bash scripts/validation/check-repo-contracts.sh` | Expected FAIL: `failures=2`; no task, plan, reference, provider, LLM Wiki, Stage 99, or document-contract remediation failures. Failures remain confined to known out-of-scope infra drift: the Keycloak hardening image mismatch and `infra/tech-stack.versions.json` expected-image drift. |
| Adapter wording drift | `rg -n 'gemini-3\.1-pro\|gemini-3\.5-flash\|DOCS 3 RULES\|R1\)\|R2\)\|R3\)\|docs/99\.templates/(readme\|service)\.template\|updated:' GEMINI.md .agents/rules/workspace.md .agents/workflows/documentation.md .claude/agents/doc-writer.md .claude/skills/ops-runbook-agent/skill.md .codex/skills/ops-runbook-agent/skill.md` | PASS: no matches in the remediated adapter surfaces. |
| Provider mirror generation | `bash scripts/operations/sync-provider-surfaces.sh --write` | PASS: regenerated generated Codex/Gemini provider surfaces after the Claude ops-runbook skill edit. |
| Provider mirror freshness | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| README approved surfaces | `rg -n 'Related References\|docs/99\.templates/(readme\|service)\.template\|docs/0[7]\.operations\|docs/1[0]' projects/README.md projects/storybook/README.md projects/storybook/nextjs/README.md secrets/README.md tests/README.md` | PASS: no stale section, removed template, or legacy stage-pattern matches in approved T-003 surfaces. |
| README examples boundary | `rg -n 'docs/99\.templates/(readme\|service)\.template\|Related References' projects secrets tests examples` | EXPECTED SCOPED RESIDUAL: matches remain only under `examples/sample-web-service/**`, which is WDC-GAP-017 and remains deferred. |
| Operations metadata cleanup | `rg -n '^updated:\|^component:\|^runtime_state:\|^tier:\|^policy_state:' docs/05.operations` | PASS: no active Stage 05 matches remain for the remediated non-standard metadata keys. |
| Changed target-stage gate | `bash scripts/validation/check-repo-contracts.sh` | Expected FAIL only on known infra drift; changed target-stage documents report `changed_template_docs_total=5`, `normalized_changed_template_docs_total=5`, and `legacy_changed_template_docs_skipped=0`. |
| PRD AI-agent heading split | `rg -n '^## AI Agent Requirements$' docs/01.requirements` | PASS: no bare PRD AI-agent heading remains. |
| PRD canonical AI-agent heading count | `rg -n '^## AI Agent Requirements \(If Applicable\)$' docs/01.requirements \| wc -l` | PASS: 24 canonical PRD AI-agent headings. |
| Infra validation heading split | `rg -n '^## Validation Commands$\|^### Validation Commands$' infra --glob '*.md'` | PASS: no `Validation Commands` headings remain under infra. |
| Gateway validation heading count | `rg -n '^## Validation$' infra/01-gateway/traefik/README.md infra/01-gateway/nginx/README.md` | PASS: the two changed gateway READMEs each retain one canonical `## Validation` section. |
| Missing frontmatter routing | Current tracked Markdown first-line scan plus routing classifier | PASS: 185 files without top frontmatter are routed by surface; 0 non-README active target-stage leaf documents remain unrouted. |
| Local QA responsibility inventory | `bash scripts/validation/run-local-qa-gates.sh --list` | PASS: lists local script-backed gates, CI/local-tooling gates, and remote-only gates; dependency audit is not listed as an active local gate. |
| Dependency audit active-gate search | `rg -n 'npm audit\|pip audit' .github scripts --glob '*.yml' --glob '*.yaml' --glob '*.sh'` | PASS: no active workflow or script-backed `npm audit` / `pip audit` commands found. |
| Graphify advisory status | `bash scripts/knowledge/report-graphify-health.sh` | PASS: command exits 0 and reports `status=advisory` with `surprising_cross_root_inferred_edges=2`, confirming advisory posture. |
| Parser gap reproduction | `rg -n '^# ' .github/PULL_REQUEST_TEMPLATE.md scripts/README.md secrets/README.md` | PASS: matches include real H1 headings plus shell-comment examples, confirming WDC-GAP-018 is parser/tooling follow-up rather than content drift. |

## Remediation Evidence

### T-002 Governance and Provider Adapter Drift

- WDC-GAP-001: updated `.agents/rules/workspace.md` and
  `.agents/workflows/documentation.md` so Gemini/Antigravity native surfaces
  defer model policy, workflow policy, artifact routing, and template rules to
  Stage 00 and Stage 99 owners instead of restating those rules.
- WDC-GAP-002: updated `.claude/agents/doc-writer.md` and
  `.claude/skills/ops-runbook-agent/skill.md` so runtime prompts link to the
  documentation protocol, docs scope, stage authoring matrix, and mapped
  operations templates instead of owning DOCS 3 or operations section profiles.
- Generated Codex mirror: refreshed
  `.codex/skills/ops-runbook-agent/skill.md` from the Claude skill through
  `scripts/operations/sync-provider-surfaces.sh --write`.
- Root shim alignment: updated `GEMINI.md` so model selection points to
  `docs/00.agent-governance/subagent-protocol.md` rather than repeating model
  values.
- WDC-GAP-022: remote branch-protection evidence remains deferred. No `gh api`
  remote verification or remote setting mutation was performed in this batch.

### T-003 README Profile Normalization

- WDC-GAP-003: updated project README surfaces to use `## Related Documents`
  and canonical `docs/99.templates/templates/common/readme.template.md`
  links. `projects/README.md` also no longer repeats obsolete operations-stage
  path literals.
- WDC-GAP-004: updated `secrets/README.md` to use the README profile's
  `## Related Documents` heading, removed a duplicate operations README link,
  and replaced the removed flat README template link. No secret value files
  were opened.
- WDC-GAP-005: updated `tests/README.md` to use `## Related Documents`.
- WDC-GAP-017: examples remain deferred; `examples/sample-web-service/**`
  still contains the removed flat service-template references until an
  examples/scaffold contract decision is approved.
- WDC-GAP-019: the stale operations-stage literal in `projects/README.md` was
  remediated after project README scope approval in this batch.

### T-004 Operations Metadata Profile Cleanup

- WDC-GAP-007: removed generic `updated` metadata from the three active Stage
  05 observability documents identified by the audit report.
- WDC-GAP-016: applied the Stage 05 operations metadata decision for this
  sub-batch: active operations target documents keep lifecycle `status` in
  frontmatter, while path-derived tier/component/title/runtime context belongs
  in the path, headings, and body. This removed `tier`, `component`,
  `runtime_state`, and the remaining workspace policy-state key from active
  Stage 05 frontmatter.
- Remaining T-004 scope after the PRD heading cleanup: WDC-GAP-006 broad
  frontmatter routing and WDC-GAP-009 infra validation heading normalization
  remain separate sub-batches.

### T-004 Requirements Section Heading Cleanup

- WDC-GAP-008: aligned the four active PRD outliers with
  `docs/99.templates/templates/sdlc/prd.template.md` by changing
  `## AI Agent Requirements` to
  `## AI Agent Requirements (If Applicable)`.
- Remaining T-004 scope after the infra validation heading cleanup:
  WDC-GAP-006 broad frontmatter routing.

### T-004 Infra Validation Heading Cleanup

- WDC-GAP-009: merged the Traefik and Nginx gateway README validation command
  tables into their existing `## Validation` sections and removed the
  `Validation Commands` split heading.
- Remaining T-004 scope after this sub-batch: WDC-GAP-006 broad frontmatter
  routing.

### T-004 Frontmatter Routing Profile

- WDC-GAP-006: created
  `docs/90.references/audits/document-contracts/frontmatter-routing-profile.md`
  and updated `docs/99.templates/support/frontmatter-contract.md` to classify
  the 185 current missing-frontmatter files by surface.
- Decision summary: stage folder README indexes, infra README files, and
  workspace utility README files are frontmatter-optional; provider/examples
  surfaces are deferred to provider or examples contracts; GitHub-native
  Markdown, generated Graphify reports, root special-purpose files, and legacy
  archive material are declined for incidental manual frontmatter.
- No broad corpus rewrite was performed, and no runtime, provider config,
  GitHub-native behavior, generated report output, secret material, or Compose
  behavior was changed.

### T-005 CI/CD, QA, Parser, and Graphify Decision

- WDC-GAP-010: documented the current dependency-update and QA coverage and
  decided not to add `npm audit` or `pip audit` hard gates in this documentation
  batch. Future hard gates require Security/QA approval for workflow/script
  changes, thresholds, exceptions, and package-manager scope.
- WDC-GAP-011: kept Graphify advisory. Current `report-graphify-health.sh`
  output is advisory, so Graphify is a navigation aid that must be
  corroborated against tracked source files and canonical docs.
- WDC-GAP-018: classified the heading-scan matches in the PR template, scripts
  README, and secrets README as fenced/comment-like parser evidence, not
  content drift. No content fix was applied.
- No `.github/workflows/**`, `scripts/**`, `.pre-commit-config.yaml`,
  Graphify generated output, or Markdown content surface was changed.

### T-006 Historical Evidence Preservation

- WDC-GAP-012: preserved frontmatter and README inventory baselines because
  they are audit evidence. They should be superseded by a future inventory run,
  not rewritten in place.
- WDC-GAP-013: preserved requirement section-profile baseline evidence because
  the active PRD heading drift was already remediated in T-004.
- WDC-GAP-014: preserved archive tombstones and
  `archive/Windows-Network-IP.md` as migration and historical-structure
  evidence.
- WDC-GAP-015: preserved old template-path mentions inside completed specs,
  plans, tasks, and progress rows as evidence of the earlier template layout.
- No completed Stage 03/04 artifacts, archive tombstones, legacy archive
  material, or historical progress rows were rewritten.

## Verification Summary

- **Test Commands**: Listed in `## Validation Results`.
- **Eval Commands**: N/A for documentation task evidence.
- **Logs / Evidence Location**: This task document and the source
  `gap-register.md`.
- **Manual Checks**: Confirmed T-003 changes stayed limited to approved
  project, secrets, and tests README surfaces, and T-004 operations metadata
  changes stayed limited to approved Stage 05 documentation frontmatter. T-004
  requirements changes stayed limited to section heading normalization in four
  PRD documents. T-004 infra changes stayed limited to README section
  consolidation without runtime, Compose, or script changes. T-004 frontmatter
  routing created a contract/reference decision only and did not add
  frontmatter to the 185 routed files. T-005 created decision evidence only;
  no provider, workflow, validator, script, pre-commit, secret value, generated
  report, GitHub-native, Compose, Markdown content, or runtime surfaces were
  changed. T-006 created preservation evidence only and did not rewrite
  historical documents.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Plan**: [Workspace document contract audit pack plan](../plans/2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Spec**: [Workspace document contract audit pack spec](../../03.specs/workspace-document-contract-audit-pack/spec.md)
