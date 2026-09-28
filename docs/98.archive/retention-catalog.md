---
title: "Retention Catalog"
version: "1.1.0"
type: "archive/retention-catalog"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-28"
---

# Retention Catalog

## Overview

This record holds one row per preserved unit in Stage 98. A unit is a Spec
package directory, an Incident bundle directory, or a single document.
`Record` is the unit path under `docs/98.archive/`, and a package or bundle
ends with `/`. `Class` is the disposition directory. `Names` is the value that
class must name. `Source` is the only source Git object this model admits. A
change that moves a unit cannot name its own commit, so it records the base
commit where the source still existed.

Records preserved before this catalog existed keep the withdrawal records their
contract required at the time; they are not loaded here retroactively. The
[Stage 98 README](README.md) routes readers here, and the archive validator
reads this table.

## Retention Catalog

| Record | Class | Names | Source |
| --- | --- | --- | --- |
| `completed/03.specs/0185-agentic-research-refresh/` | completed | RES-0002 | `e9e65f1087a4adc797c112b4b8f19eb9ac1bbb2e:docs/03.specs/0185-agentic-research-refresh` |
| `superseded/02.architecture/decisions/0033-full-spec-package-preservation.md` | superseded | ADR-0035 | `677a6e5135de8af1faa9110f912f2452972abf22:docs/02.architecture/decisions/0033-full-spec-package-preservation.md` |
| `completed/03.specs/0177-archive-disposition-enforcement/` | completed | ADR-0035 | `9e120c6fc22d6ddb0ff33e878341b8fdcfa73bd0:docs/03.specs/0177-archive-disposition-enforcement` |
| `superseded/02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md` | superseded | ADR-0036 | `ea8623eaf04efa5b4f32d538cb3dc0e5235831e0:docs/02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md` |
| `superseded/02.architecture/decisions/0015-analytics-engine-selection.md` | superseded | ADR-0039 | `6179418507afedbcb631dbef07d7ed7cb854f2ab:docs/02.architecture/decisions/0015-analytics-engine-selection.md` |
| `superseded/02.architecture/decisions/0019-data-hardening-and-ha-expansion-strategy.md` | superseded | ADR-0040 | `6179418507afedbcb631dbef07d7ed7cb854f2ab:docs/02.architecture/decisions/0019-data-hardening-and-ha-expansion-strategy.md` |
| `completed/03.specs/0178-archive-occupancy-citation-and-frozen-identity/` | completed | ADR-0036 | `3c5db48cbae8edfccfa1b0a56ad9421e6b1ccafd:docs/03.specs/0178-archive-occupancy-citation-and-frozen-identity` |
| `completed/03.specs/0180-home-dev-convergence/` | completed | AD-0031 | `2a90260a6f9083993b2e61dee20a49e7b8bd858b:docs/03.specs/0180-home-dev-convergence` |
| `completed/03.specs/0181-home-residual-operations/` | completed | AD-0031 | `98efce81b9481fd7f6a01c92b643b3f336679574:docs/03.specs/0181-home-residual-operations` |
| `superseded/90.references/research/0081-roadmap/README.md` | superseded | RES-0002 | `bb43abb5e0894f45d1179a60770d489a0da41e7c:docs/90.references/research/0081-roadmap/README.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/guide.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/guide.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/policy.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/policy.md` |
| `retired/05.operations/catalog/09-tooling/0067-syncthing/runbook.md` | retired | Syncthing was removed from the active service inventory; no successor exists. | `d1e6ded52808b02392c52472d5416518a3b959d6:docs/05.operations/catalog/09-tooling/0067-syncthing/runbook.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/guide.md` | superseded | GDE-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/guide.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/policy.md` | superseded | POL-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/policy.md` |
| `superseded/05.operations/catalog/04-data/0023-minio/runbook.md` | superseded | RUN-0024 | `988059fe898fe739a2eb420f5370eba346568295:docs/05.operations/catalog/04-data/0023-minio/runbook.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/guide.md` | superseded | GDE-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/guide.md` |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/guide.md` | superseded | GDE-0094 | `8e8082c53ed06e328931427f05b0754e82034e2a:docs/05.operations/catalog/04-data/0018-ksqldb/guide.md` |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/policy.md` | superseded | POL-0094 | `8919696e8a65f47ccd830e577d80c781b810cbd3:docs/05.operations/catalog/04-data/0018-ksqldb/policy.md` |
| `superseded/05.operations/catalog/04-data/0018-ksqldb/runbook.md` | superseded | RUN-0094 | `8919696e8a65f47ccd830e577d80c781b810cbd3:docs/05.operations/catalog/04-data/0018-ksqldb/runbook.md` |
| `superseded/05.operations/catalog/04-data/0020-starrocks/guide.md` | superseded | GDE-0094 | `8e8082c53ed06e328931427f05b0754e82034e2a:docs/05.operations/catalog/04-data/0020-starrocks/guide.md` |
| `superseded/05.operations/catalog/04-data/0020-starrocks/policy.md` | superseded | POL-0094 | `8919696e8a65f47ccd830e577d80c781b810cbd3:docs/05.operations/catalog/04-data/0020-starrocks/policy.md` |
| `superseded/05.operations/catalog/04-data/0020-starrocks/runbook.md` | superseded | RUN-0094 | `8919696e8a65f47ccd830e577d80c781b810cbd3:docs/05.operations/catalog/04-data/0020-starrocks/runbook.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/policy.md` | superseded | POL-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/policy.md` |
| `superseded/05.operations/catalog/03-security/0016-vault/runbook.md` | superseded | RUN-0085 | `a797331dce2f4da089f50e8a73eea525b1445955:docs/05.operations/catalog/03-security/0016-vault/runbook.md` |
| `superseded/02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md` | superseded | ADR-0037 | `cb11af64194432d94739c47046ed707010634468:docs/02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md` |
