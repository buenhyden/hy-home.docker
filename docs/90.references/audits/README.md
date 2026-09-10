---
title: "Audit Packages"
version: "2.0.0"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-10"
layer: "references"
created: "2026-07-02"
---

# Audit Packages

## Overview

Point-in-time gap, implementation, and conformance assessments. Audit packages
are evidence, not approval gates.

The Stage 90 authority boundary and package lifecycle rules are defined by the
[References index](../README.md) and Stage 99 Registry.

SPEC-0158 retires this category. The current tree defines the Stage 90 package
set: a package exists because its README is present and satisfies its Stage 99
profile, and it is retired by removing it in the same change that migrates its
needed meaning to a canonical owner, updates every inbound consumer, and
removes its row below. No archive ledger decides membership, so retiring a
package is no longer a Stage 99 amendment.

Stage 99 identity is still consumed once. A retired package's `AUD-` number is
never reissued, because `identity-history-regression` forbids it.

A cross-stage audit belongs in a Task under its governing Spec, where `task` is
a `package-member` profile and so allocates no global identity.

## Packages

This category holds no packages, which completes the retirement SPEC-0158
declared.

Fourteen packages were retired on 2026-09-10. Each was held live by a registered
consumer rather than by a reader: the criterion contract that mapped its
filename, the semantic-freshness checker that asserted its rows, the matrix
generator that read the pack directory, and the metadata profile's path
allow-list. All four were removed in the same change. Each preserved body is
under `docs/98.archive/retired/90.references/audits/`, recorded by tombstones
`tomb-AUD-0019` through `tomb-AUD-0032`.

## Dated Historical Snapshots

The superseded audit snapshot
retains its observation date in metadata; current package paths remain
date-free.

AUD-0097 was retired on 2026-09-09. Three of its four defects were fixed in the
tree while four operations guides still linked it as the owner of an open
finding; the one defect that remained moved to the guide of the subject that
owns it. The preserved body is under `docs/98.archive/retired/`, and
`tomb-AUD-0097` records the disposition.

## Supersession Ledgers

Migration 0003
records historical path recovery.

## Authoring

Create packages only under `audits/####-<slug>/` and use the matching Stage 99
template. Preserve observation dates, citations, provenance, and active-owner
Traceability.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
