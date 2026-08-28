---
status: draft
artifact_id: reference:agentic-engineering-research-draft:llm-wiki-system
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# LLM Wiki System

## Overview

The repository has a thin authored `llms.txt` entry point and a curated
repository map. They are navigation aids, not a provider-loading guarantee or
the canonical truth for every linked document.

## Purpose

Explain the declared LLM Wiki generator boundary, its outputs, and the limits
of its freshness checks without running it.

## Scope

This leaf reports tracked implementation and retained external conventions as
advisory analysis. The declared `--write` and `--check` commands were not run;
no generator, map, index, or `llms.txt` file is changed by D4.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `LWS-001` | `llms.txt` is a thin authored entry point and `ref-0083-repository-map.md` is curated; old operations links are not current truth. | tracked workspace configuration | VERIFIED | `llms.txt`; repository map | Resolve authority from the target's current owner. |
| `LWS-002` | `scripts/knowledge/generate-llm-wiki.py` declares exactly `docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md` and `docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md`, owned by doc-writer and the knowledge-map skill. | tracked workspace configuration | VERIFIED | generator manifest and skill | Generated outputs require their owner/generator. |
| `LWS-003` | Declared `--check` compares rendered bytes/strings, not source freshness, semantic correctness, local destinations, or runtime behavior. | tracked workspace configuration | VERIFIED | generator implementation | A clean check alone is insufficient evidence. |
| `LWS-004` | Retained llms.txt guidance proposes an H1, optional reader summary, file list, and Optional section; retained AGENTS.md guidance concerns scoped Markdown agent instructions. | historical retained source | HISTORICAL VERIFIED | dated LLM Wiki evidence | These are separate navigation/instruction conventions, not provider-loading proof. |

The generator's tracked mechanics use cached Git paths, regular non-symlink
files, safe exclusions (generally `.py` and the `.agents` root), and its own
script as a forced input. Its index excludes itself and coverage excludes both
projections, so counts differ by design. These are implementation facts, not an
execution observation. `--check` compares projected text only, not semantic,
source, link, or runtime proof; `--write` was never run.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `LWS-SRC-001` | `LWS-001` | LLM entry and repository map / workspace | [llms.txt](../../../../llms.txt); [repository map](../../llm-wiki/ref-0083-repository-map.md) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Curated map can contain obsolete links. |
| `LWS-SRC-002` | `LWS-002`, `LWS-003` | LLM Wiki generator and knowledge-map skill / workspace | [generator](../../../../scripts/knowledge/generate-llm-wiki.py); [skill](../../../00.agent-governance/skills/knowledge-map-agent.md) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Commands are declared, not run. |
| `LWS-SRC-003` | `LWS-004` | llmstxt.org and AGENTS.md conventions | [llms.txt convention](https://llmstxt.org/); [AGENTS.md convention](https://agents.md/) | historical retained source | retained 2026-08-08 observation | 2026-08-08 | Structural conventions do not prove provider loading or industry adoption. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Offer a narrow entry point for agent navigation. | Inspect declared entry paths. | No provider-loading claim. |
| architecture | applies | Link to canonical architecture owners. | Resolve the target path. | Map is not authority. |
| common | applies | Exclude unsafe or untracked material. | Inspect generator rules. | Rules are not execution proof. |
| docs | applies | Regenerate only through the declared owner. | Confirm manifest outputs. | Generator was not run. |
| infra | applies | Resolve infrastructure references through their canonical owner. | Check the target path before publishing a map. | No runtime evidence. |
| ops | applies | Treat old operation links as pointers requiring validation. | Resolve current catalog target. | No operation is inferred. |
| qa | applies | Pair byte checks with semantic/link review. | Record separate checks. | `--check` is narrow. |
| security | applies | Retain safe-path exclusions. | Inspect tracked exclusions. | No security testing. |

## Maintenance

Use the declared generator only with its authorized workflow. Preserve the
distinction between a curated map, generated projections, and canonical owners.

## Related Documents

- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [Documentation architecture](./documentation-architecture.md)
- [Workspace baseline](./workspace-baseline.md)
