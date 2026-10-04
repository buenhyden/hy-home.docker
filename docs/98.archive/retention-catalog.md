---
title: "Retention Catalog"
version: "1.1.16"
type: "archive/retention-catalog"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
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
| `completed/03.specs/0194-agent-contract-integration/` | completed | POL-0004 / agent contract governance | `814ac20e4da848e37475757ce1707ceece546ae5:docs/03.specs/0194-agent-contract-integration` |
| `completed/03.specs/0197-infra-tier-layout/` | completed | ADR-0045 / ADR-0046 / infrastructure layout | `814ac20e4da848e37475757ce1707ceece546ae5:docs/03.specs/0197-infra-tier-layout` |
| `completed/03.specs/0198-operations-documentation-system/` | completed | GDE-0099 / RUN-0099 / service role documents | `814ac20e4da848e37475757ce1707ceece546ae5:docs/03.specs/0198-operations-documentation-system` |
| `completed/03.specs/0199-ci-delivery-gate-optimization/` | completed | POL-0004 / workflow contract | `814ac20e4da848e37475757ce1707ceece546ae5:docs/03.specs/0199-ci-delivery-gate-optimization` |
| `completed/03.specs/0200-path-aware-pr-regressions/` | completed | POL-0004 / workflow contract | `814ac20e4da848e37475757ce1707ceece546ae5:docs/03.specs/0200-path-aware-pr-regressions` |
| `completed/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | completed | AD-0004 / AD-0031 / POL-0021 / RUN-0021 | `ce001be7af93aebe6430f586b56a5c443fa9f386:docs/03.specs/0201-home-infrastructure-diagnosis-and-work-design` |
| `completed/03.specs/0202-development-data-and-lab-isolation/` | completed | AD-0004 / AD-0031 / POL-0021 / RUN-0021 | `ce001be7af93aebe6430f586b56a5c443fa9f386:docs/03.specs/0202-development-data-and-lab-isolation` |
| `completed/03.specs/0203-quality-results-and-isolated-load-testing/` | completed | POL-0064 / GDE-0064 / RUN-0064 | `686b71773b8a7cf7be27673b9e81a71fce3f1b26:docs/03.specs/0203-quality-results-and-isolated-load-testing` |
| `completed/03.specs/0205-storybook-dependency-refresh/` | completed | AD-0031 / existing Storybook npm and quality owners | `9f89d0a241a41cfd278217683043d98a0cccc97a:docs/03.specs/0205-storybook-dependency-refresh` |
| `superseded/03.specs/0190-agent-contract-hardening/` | superseded | SPEC-0194 | `c86f55518b8a9a156e10e38fbd52d1a883063d6a:docs/03.specs/0190-agent-contract-hardening` |
| `completed/03.specs/0196-ollama-0-35-decision-model/` | completed | GDE-0056 / RUN-0056 | `0cf685435c9fd1c0c6801937b180b60e04ed32ab:docs/03.specs/0196-ollama-0-35-decision-model` |
| `completed/03.specs/0192-backup-and-host-alerting/` | completed | RUN-0021 | `dbb2413c8166e3d7cd1d9c4bd9e4680e0e03ea20:docs/03.specs/0192-backup-and-host-alerting` |
| `completed/03.specs/0191-backup-valkey-export-timeout/` | completed | RUN-0021 | `ba0b3462e7806d793ae4b32be3c6d819ebe756db:docs/03.specs/0191-backup-valkey-export-timeout` |
| `completed/03.specs/0183-operations-role-layout/` | completed | ADR-0043 | `cce796818043f6663441470d1f3c6604bfb5193a:docs/03.specs/0183-operations-role-layout` |
| `completed/03.specs/0179-package-disposition-wait-and-task-cancellation/` | completed | ADR-0037 | `a451616821ff460750f39517b08495dd69d5c16c:docs/03.specs/0179-package-disposition-wait-and-task-cancellation` |
| `completed/03.specs/0190-home-classification-remaining/` | completed | POL-0078 | `315bd7997c4a591afeb568867f846f1988034ab5:docs/03.specs/0190-home-classification-remaining` |
| `completed/03.specs/0189-home-classification-and-valkey-key/` | completed | POL-0078 | `c4f6e829543ff9f20a51c755118fa97b9dd012b0:docs/03.specs/0189-home-classification-and-valkey-key` |
| `completed/03.specs/0188-compose-host-port-exposure/` | completed | POL-0096 | `24b3e45c7fba5f11455c2a9b333463dfccfd3398:docs/03.specs/0188-compose-host-port-exposure` |
| `completed/03.specs/0187-document-language-migration/` | completed | ADR-0044 | `9143ad8a3f93b63b3b07991901d803a18a36060b:docs/03.specs/0187-document-language-migration` |
| `completed/03.specs/0186-document-governance-dead-code-removal/` | completed | no durable contract | `a406430b2da388b13c863698d438cfd44c3151c9:docs/03.specs/0186-document-governance-dead-code-removal` |
| `completed/03.specs/0184-readme-navigation-and-language-contract/` | completed | ADR-0044 | `ac15a6f84f61c666b90926418bc697da6e0687af:docs/03.specs/0184-readme-navigation-and-language-contract` |
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
| `retired/03.specs/0195-agent-native-observations/` | retired | Owner withdrew the unnecessary SPEC-0195 native-observation follow-up; no successor exists. | `a31453d671153c5985bf08051cbe4b87bca5e6a5:docs/03.specs/0195-agent-native-observations` |
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
| `superseded/03.specs/0201-home-infrastructure-diagnosis-and-work-design/` | superseded | SPEC-0204 | `79b42b604b99bcc6712887d29e36f8244ec0f9eb:docs/03.specs/0201-home-infrastructure-diagnosis-and-work-design` |
| `superseded/03.specs/0202-development-data-and-lab-isolation/` | superseded | SPEC-0204 | `79b42b604b99bcc6712887d29e36f8244ec0f9eb:docs/03.specs/0202-development-data-and-lab-isolation` |
| `superseded/03.specs/0203-quality-results-and-isolated-load-testing/` | superseded | SPEC-0204 | `79b42b604b99bcc6712887d29e36f8244ec0f9eb:docs/03.specs/0203-quality-results-and-isolated-load-testing` |
| `superseded/03.specs/0205-storybook-dependency-refresh/` | superseded | SPEC-0204 | `79b42b604b99bcc6712887d29e36f8244ec0f9eb:docs/03.specs/0205-storybook-dependency-refresh` |
| `completed/03.specs/0193-observability-dashboards-signals-and-alerting/` | completed | GDE-0041 / GDE-0044 / RUN-0050 / observability source | `275d708ab797e0c86a30508351666482ebc04907:docs/03.specs/0193-observability-dashboards-signals-and-alerting` |
| `completed/03.specs/0206-shared-storybook-and-docs-mcp/` | completed | GDE-0101 / POL-0101 / RUN-0101 / shared Storybook source | `275d708ab797e0c86a30508351666482ebc04907:docs/03.specs/0206-shared-storybook-and-docs-mcp` |
