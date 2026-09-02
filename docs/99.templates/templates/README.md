---
title: Template Catalog
type: common/readme
layer: templates
owner: "@buenhyden"
---

# Template Catalog

## Overview

This directory contains copyable sources registered by
[`../registry.json`](../registry.json). Contract explanations live only in the
[Stage 99 README](../README.md).

## Audience

- Documentation Writers
- Repository Maintainers
- AI Agents

## Scope

| Category | Directory | Registered roles |
| :--- | :--- | :--- |
| Governance | `governance/` | Contract, Control, Rule, Provider, Role, Skill |
| Runtime | `runtime/` | Claude agent projection, Codex agent projection |
| Requirements | `requirements/` | Requirement Package |
| Architecture | `architecture/` | Architecture Description, Architecture Decision |
| Specs | `specs/` | Spec, Plan, Task, and `contracts/` Data Model, OpenAPI, GraphQL, Proto |
| Operations | `operations/` | Guide, Policy, Runbook, Incident, Postmortem |
| References | `references/` | Research, Audit, Data — one pack form and one reference form each |
| Archive | `archive/` | Migration, Tombstone |
| Common | `common/` | Stage, domain, and package README forms |

## Structure

The category directories mirror the current documentation responsibilities.
Replaced sources are recoverable through Git history.

## How to Work in This Area

Resolve a template role in `registry.json`, copy its `source`, and follow the
Stage 99 README. Do not select a template by scanning legacy directories.

## Related Documents

- [Stage 99 authority](../README.md)
- [Registry](../registry.json)
