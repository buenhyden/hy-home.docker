---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md -->

# Reference: Frontmatter Routing Profile

## Overview

This reference classifies the tracked Markdown files that lack top YAML
frontmatter into surface-specific routing decisions. It closes the profile
decision needed by `WDC-GAP-006` without rewriting the Markdown corpus.

## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route**: [canonical agentic implementation audit](../2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.

## Purpose

The original frontmatter inventory found 185 tracked Markdown files without top
frontmatter. The current first-line scan finds 184 because the example scaffold
follow-up added frontmatter to two files and the latest Graphify refresh added
one generated report. The remaining set mixes active target-stage README
indexes, infra README files, provider adapters, GitHub-native Markdown,
generated reports, root special-purpose files, and legacy archive material. This
document separates those surfaces so future work can add, omit, defer, or
decline frontmatter intentionally by profile.

## Repository Role

This reference supports the Stage 04 document-contract remediation task and the
Stage 99 frontmatter contract. It is not active policy by itself, not a
validator specification, and not approval to rewrite the current missing
frontmatter population.

## Scope

### In Scope

- Current tracked Markdown files that do not start with a top `---` YAML
  frontmatter fence.
- Routing decisions for README indexes, infra README files, workspace utility
  README files, provider/example surfaces, GitHub-native Markdown, generated
  Graphify reports, root special-purpose files, and legacy archive material.
- Evidence commands that list paths and counts without printing secret values.

### Out of Scope

- Adding frontmatter to all currently missing files as a bulk formatting sweep.
- Changing GitHub-native behavior, generated report output, provider runtime
  config, Docker Compose runtime behavior, or secret material.
- Reclassifying examples, Graphify, or remote GitHub evidence beyond the
  explicit decisions below.

## Definitions / Facts

- **Required**: the surface must carry repository frontmatter according to an
  active contract.
- **Optional**: the surface may omit frontmatter because role is already
  derived from path, heading, and profile.
- **Deferred**: a separate surface-specific contract must decide before edits.
- **Declined**: the repository should not add manual frontmatter because the
  surface is native to another platform, generated, historical, or
  special-purpose.

## Method

| Evidence ID | Command or Read | Result Summary | Use |
| --- | --- | --- | --- |
| FMR-001 | `git ls-files '*.md'` plus first-line frontmatter scan | 184 tracked Markdown files currently lack top frontmatter. | Refreshes the WDC-GAP-006 routing population after the examples and Graphify follow-ups. |
| FMR-002 | Path classification of the 184 files | 0 missing non-README active target-stage leaf docs were found. | Confirms no broad target-stage leaf rewrite is required. |
| FMR-003 | Reads of `frontmatter-contract.md`, `template-selection.md`, and repo contract validator rules | README files are folder-index profiles; non-README target-stage docs carry lifecycle `status`. | Binds routing decisions to existing contracts. |
| FMR-004 | Reads of `.agents/README.md`, `.codex/README.md`, and `WDC-GAP-024` | Provider README files remain intentionally thinner than folder README profiles; `.agents/README.md` may omit frontmatter and `.codex/README.md` may keep Codex-specific metadata. | Closes the provider README routing deferral as optional/no-action rather than a target-stage frontmatter gap. |

## Routing Matrix

| Surface Profile | Count | Representative Paths | Decision | Rationale |
| --- | ---: | --- | --- | --- |
| Stage folder README indexes | 100 | `docs/README.md`, `docs/03.specs/001-gateway/README.md`, `docs/05.operations/guides/README.md`, `docs/90.references/data/docker/README.md` | Optional | README role is derived from path and folder-index headings; adding target lifecycle status would blur README and leaf-document profiles. |
| Infra README files | 66 | `infra/README.md`, `infra/01-gateway/traefik/README.md`, `infra/06-observability/grafana/README.md` | Optional | Infra README files are implementation and service indexes, not canonical docs target-stage leaf documents. |
| Workspace README and utility README files | 6 | `projects/README.md`, `projects/storybook/README.md`, `scripts/README.md`, `secrets/README.md`, `tests/README.md` | Optional | The common README template is profile-driven and does not require target frontmatter after copying. |
| Provider README files | 1 | `.agents/README.md` | Optional | `WDC-GAP-024` records provider README profiles as intentionally thinner than folder README profiles; `.agents/README.md` does not need frontmatter unless a provider metadata consumer is introduced. |
| Example scaffold files | 0 | Previously `examples/sample-web-service/README.md`, `examples/sample-web-service/service.md` | Closed | The examples scaffold contract follow-up closed `WDC-GAP-017`; both files now carry lifecycle frontmatter and current nested template links. |
| GitHub-native Markdown | 3 | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`, `.github/rulesets/main-protection.md` | Declined | GitHub-native Markdown and ruleset evidence should not receive repository frontmatter unless a GitHub-specific consumer is approved. |
| Generated Graphify reports | 4 | `graphify-out/GRAPH_REPORT.md`, `graphify-out/2026-06-04/GRAPH_REPORT.md`, `graphify-out/2026-07-04/GRAPH_REPORT.md` | Declined | Generated output should remain generator-owned unless the generator is changed. |
| Root special-purpose files | 3 | `README.md`, `CHANGELOG.md`, `RTK.md` | Declined | These root surfaces have special consumers and should not receive copied target-stage metadata. |
| Legacy archive material outside `docs/98.archive` | 1 | `archive/Windows-Network-IP.md` | Declined | Historical archive material is outside the active stage chain and should not be normalized for style alone. |

## Findings

- `WDC-GAP-006` does not require a broad frontmatter rewrite because the
  missing set contains no non-README active target-stage leaf documents.
- Folder index README files are valid without top YAML frontmatter unless a
  future README contract explicitly adds a metadata consumer.
- Generated, GitHub-native, root special-purpose, and legacy archive files
  should not receive manual repository frontmatter as incidental cleanup.
- Provider README routing is optional/no-action: `.agents/README.md` may omit
  frontmatter, while `.codex/README.md` may keep Codex-specific frontmatter,
  because provider README files are not target-stage leaf documents.
- Example scaffold routing was closed by the `WDC-GAP-017` follow-up without
  changing example runtime files.

## Source Rules

- Prefer the Stage 99 frontmatter contract for required and disallowed keys.
- Treat README files as folder-index or surface-entry documents unless a
  surface-specific contract says otherwise.
- Preserve generated and external-platform-native Markdown unless the owning
  generator or platform integration is changed in an approved task.
- Do not print secret values, `.env` values, raw logs, credentials, tokens,
  certificates, or private keys when reproducing the inventory.

## Sources

- [Frontmatter inventory](./frontmatter-inventory.md) - Supplies the original
  185-file missing-frontmatter baseline.
- [Gap register](./gap-register.md) - Supplies the `WDC-GAP-006` remediation
  requirement and `WDC-GAP-024` provider README no-action classification.
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md) -
  Defines required and disallowed frontmatter roles.
- [Template selection](../../../99.templates/support/template-selection.md) -
  Defines README and target-stage template routing.
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) -
  Defines target-stage frontmatter and README profile boundaries.
- [Repository contract validator](../../../../scripts/validation/check-repo-contracts.sh) -
  Enforces non-README target-stage status and README section profiles.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`.
- **Review Cadence**: Review after README contract changes, provider README
  profile changes, generated-report routing changes, GitHub-native document
  changes, or example scaffold contract decisions.
- **Update Trigger**: Update when the missing-frontmatter inventory count
  changes materially or when a surface-specific contract changes a routing
  decision.

## Related Documents

- [Document contract audit references](./README.md)
- [Frontmatter inventory](./frontmatter-inventory.md)
- [Gap register](./gap-register.md)
- [Frontmatter contract](../../../99.templates/support/frontmatter-contract.md)
- [Template selection](../../../99.templates/support/template-selection.md)
