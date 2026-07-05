---
status: active
---

<!-- Target: docs/90.references/data/knowledge/README.md -->

# Knowledge Reference Data

> generated LLM Wiki coverage and knowledge-index interpretation data

## Overview

`docs/90.references/data/knowledge` stores stable knowledge-index reference data
that helps audit consumers understand repo-local LLM Wiki coverage without
copying the full generated index.

This folder does not replace canonical source files. Runtime and policy truth
remain in tracked governance, infrastructure, script, operations, and template
surfaces.

## Category Role

This category is for generated or stable reference data about repository
knowledge navigation. It complements [LLM Wiki references](../../llm-wiki/README.md)
and keeps coverage snapshots under `data/` rather than mixing them into the
human-facing LLM Wiki index itself.

## Audience

This README is for:

- Documentation Writers
- QA Engineers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- Generated LLM Wiki stage/category coverage snapshots.
- Knowledge-index interpretation and freshness references.
- Read-only coverage counts derived from safe tracked source paths.

### Out of Scope

- Public wiki or website generation.
- Full-content exports.
- Runtime source of truth.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Structure

```text
knowledge/
├── README.md                              # This file
└── llm-wiki-stage-category-coverage.md    # Generated LLM Wiki coverage snapshot
```

## Current References

- [llm-wiki-stage-category-coverage.md](./llm-wiki-stage-category-coverage.md) -
  generated LLM Wiki stage/category coverage snapshot.

## How to Work in This Area

1. Keep generated coverage output deterministic and source-path based.
2. Do not store full document contents or secret-bearing paths here.
3. Run `bash scripts/knowledge/generate-llm-wiki-coverage.sh` after in-scope
   path changes.
4. Run `bash scripts/validation/check-repo-contracts.sh` after changing
   knowledge reference data or LLM Wiki generator scripts.

## Related Documents

- [reference data](../README.md)
- [LLM Wiki references](../../llm-wiki/README.md)
- [LLM Wiki generated index](../../llm-wiki/llm-wiki-index.md)
- [LLM Wiki coverage generator](../../../../scripts/knowledge/generate-llm-wiki-coverage.sh)
- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh)
