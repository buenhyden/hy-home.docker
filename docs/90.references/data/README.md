---
title: "Data Packages"
version: "2.0.0"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-10"
layer: "references"
created: "2026-07-02"
---

# Data Packages

## Overview

Repository inventories, generated navigation outputs, structured datasets,
glossaries, and stable reference facts.

The Stage 90 authority boundary and package lifecycle rules are defined by the
[References index](../README.md) and Stage 99 Registry.

The current tree defines the package set: a package exists because its README is
present and satisfies its Stage 99 profile. It is retired by removing it in the
same change that migrates its needed meaning to a canonical owner, updates every
inbound consumer, removes its row below, and records a Tombstone. A retired
`DATA-` number is never reissued.

## Packages

This category holds no packages.

Thirteen packages were retired on 2026-09-10. SPEC-0173 states the rule this
category runs on: Stage 90 data "remains current only while a current consumer
exists." Every consumer that made these packages live — their registered
generators, their freshness gates, and the metadata allow-lists that named their
paths — was removed in the same change, so the packages had no reader left. Each
preserved body is under `docs/98.archive/retired/90.references/data/`, recorded
by a tombstone.

DATA-0067 was the one package whose remaining consumer was not a reader: the
lifecycle gate byte-compares its `data.yaml` against the Migration 0003 recovery
blob. Under the same approval the Migration row was repointed to the preserved
path, and the payload is preserved byte for byte, so the comparison proves the
same equality against the same bytes.

A new package here needs a current consumer named before it is created, not
after.

## Authoring

Create packages only under `data/####-<slug>/` and use the matching Stage 99
template. Preserve observation dates, citations, provenance, and active-owner
Traceability.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
