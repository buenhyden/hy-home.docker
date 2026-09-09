---
title: "Data Packages"
version: "1.1.0"
type: "reference/category-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "references"
created: "2026-07-02"
---

# Data Packages

## Overview

Repository inventories, generated navigation outputs, structured datasets, glossaries, and stable reference facts.

The Stage 90 authority boundary and package lifecycle rules are defined by the [References index](../README.md) and Stage 99 Registry.

The current tree defines the package set: a package exists because its README is
present and satisfies its Stage 99 profile. It is retired by deleting it in the
same change that migrates its needed meaning to a canonical owner, updates every
inbound consumer, removes its row above, and records a Tombstone. A retired
`DATA-` number is never reissued.

Most packages here are generated. A generated package is refreshed by its
registered generator and its freshness check, never edited by hand, and it is
not retired while that generator still writes it.

DATA-0071 was retired on 2026-09-09: it was a dated public observation of
remote CI that two later authenticated protection read-backs superseded. Its
preserved body is under `docs/98.archive/retired/`, recorded by `tomb-DATA-0071`.

DATA-0067 stays. Its rows name paths the canonical-home migration removed, which
reads like dead residue, but the lifecycle gate resolves the Migration record's
`DATA-0067` row and compares this package's payload against its recovery blob
byte for byte. The package is that comparison's anchor, and the consumer that
needs it is a frozen archive body no change may rewrite.

## Packages

| Stable ID | Package | Status |
| :--- | :--- | :--- |
| [DATA-0059](./0059-compose-profile-service-coverage/README.md) | Reference: Docker Compose Profile Service Coverage | active |
| [DATA-0060](./0060-image-version-interpretation/README.md) | Reference: Docker Image and Version Interpretation | active |
| [DATA-0061](./0061-tech-stack-version-provenance/README.md) | Reference: Tech-Stack Version Provenance | active |
| [DATA-0064](./0064-agent-output-eval-fixtures/README.md) | Reference: Agent Output Eval Fixtures | active |
| [DATA-0065](./0065-audit-implementation-matrix/README.md) | Reference: Audit Implementation Matrix | active |
| [DATA-0066](./0066-foundation-summary/README.md) | Document Corpus Migration Summary | active |
| [DATA-0067](./0067-foundation/README.md) | Foundation | active |
| [DATA-0072](./0072-provider-hook-parity-matrix/README.md) | Provider Hook Parity Matrix | active |
| [DATA-0076](./0076-llm-wiki-stage-category-coverage/README.md) | LLM Wiki Stage Category Coverage | active |
| [DATA-0078](./0078-security-automation-readiness/README.md) | Reference: Security Automation Readiness | active |
| [DATA-0079](./0079-supply-chain-sample-service/README.md) | Reference: Sample-service Local Supply-chain Verification | active |
| [DATA-0082](./0082-llm-wiki-index/README.md) | LLM Wiki Generated Index | active |
| [DATA-0083](./0083-repository-map/README.md) | Reference: LLM Wiki Repository Map | active |

## Authoring

Create packages only under `data/####-<slug>/` and use the matching Stage 99 template. Preserve observation dates, citations, provenance, and active-owner Traceability.

## Related Documents

- [References index](../README.md)
- [Stage 99 Registry](../../99.templates/registry.json)
