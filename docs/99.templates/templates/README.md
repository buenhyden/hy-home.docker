---
title: Template Catalog
type: common/readme
layer: agentic
owner: "@buenhyden"
---

# Template Catalog

## Overview

This directory contains copyable sources registered by
[`../registry.json`](../registry.json). Contract explanations live only in the
[Stage 99 README](../README.md).

## Scope

| Category | Directory | Registered roles |
| :--- | :--- | :--- |
| Requirements | `requirements/` | Requirement Package |
| Architecture | `architecture/` | Architecture Description, ADR |
| Specs | `specs/` | Spec, Plan, Task, OpenAPI, GraphQL, Proto |
| Operations | `operations/` | Guide, Policy, Runbook, Incident, Postmortem |
| References | `references/` | Research, Audit, Data |
| Archive | `archive/` | Tombstone |
| Governance | `governance/` | Stage 00 authoring guidance |
| Common | `common/` | navigation README |

## Structure

The category directories mirror the current documentation responsibilities.
Replaced sources are recoverable through Git history.

## How to Work in This Area

Resolve a template role in `registry.json`, copy its `source`, and follow the
Stage 99 README. Do not select a template by scanning legacy directories.

## Related Documents

- [Stage 99 authority](../README.md)
- [Registry](../registry.json)
