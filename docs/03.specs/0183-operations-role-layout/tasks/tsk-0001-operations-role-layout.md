---
title: "Operations Role Layout"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0183-TSK-0001"
parent_ids:
- "SPEC-0183"
- "SPEC-0183-PLAN-0001"
created: "2026-09-26"
---

# Operations Role Layout

## Objective

Execute the [Plan](../plan.md) for the [Spec](../spec.md): move Stage 05 from
the domain catalog to the role layout decided by
[ADR-0043](../../../02.architecture/decisions/0043-operations-role-layout.md),
and record every document's disposition here.

## Inputs

- Baseline: branch `main` at `0deb430ea6d1e604eab91f4803241706f31783fe`,
  working tree clean, `main` equal to `origin/main` at session start. The
  pre-survey commit `b8ac86c641352e819ff002304ae9d98dc2001cd3` is an ancestor
  of the baseline (15 commits behind) and was not restored.
- Work branch: `refactor/operations-role-layout`, created locally from the
  baseline.
- Remote identity was read from the local Git configuration only
  (`https://github.com/buenhyden/hy-home.docker.git`); nothing was fetched or
  pushed.
- Stage 05 inventory computed from the tree, not from the request: 242 tracked
  files, of which 225 role documents (77 Guides, 75 Policies, 73 Runbooks),
  13 domain READMEs, the catalog README, the Stage 05 README, the incidents
  README, and one incident.
- Read-only audits delegated during W1: implementation drift for the network,
  OpenBao, and CouchDB subjects; script lifecycle against the manifest and
  workflow contract; and Guide, Policy, and Runbook role boundaries.

## Work Log

- W1: Recorded the baseline, computed the move map from each document's
  `artifact_id`, and checked it before any write: 225 target paths, no target
  collision, no duplicate identifier, no slug collision within a role
  directory, and one number that differs from its subject folder
  (`POL-0052` in `0051-airflow-dag-lifecycle`).
- W2: Added this package and ADR-0043.
- W3: Wrote the role-first regression tests before changing the validator.
  Against the catalog validator they failed as expected: 86 tests, 13
  failures and 56 errors, each on a role-first path or a retired catalog path.
- W4: Moved the 225 role documents with `git mv`, deleted the catalog README
  and the 13 domain READMEs, generated the three role indexes, and changed the
  Registry (`direct` identity, role READMEs, no `operations-domain-readme`),
  the operations validator, the metadata move baseline, and the consumers of
  the old route. The seven `optimization-hardening` subjects took a domain
  prefix; `POL-0052` took its own number.
- W5: Replaced the missing LLM Wiki generator claim in `scripts/README.md` and
  the dated absence note in the incidents README.
- W6: Applied the role-boundary corrections recorded per row in the ledger
  below. The drift audit of the network, OpenBao, and CouchDB subjects found
  no confirmed drift; `NODENAME=couchdb-1.infra_net` and `lab_net.aliases`
  were not changed. Five manifest rows gained consumers that the manifest
  evidence detector proves; three unproven additions were reverted.
- W7: Added MIG-0005 and advanced the `migration` identity space.
- W8: Removed the `subject-member` identity relation, addressed review
  findings, and verified each commit in isolation and the final tree with
  the full gate.
- W9 (owner follow-up): Applied five of the six deferred documentation
  items: POL-0004 links its `.agents` owners, RUN-0004 drops the delegation
  rules, RUN-0061 owns the approved k6 live run, POL-0006 drops its dated audit
  snapshots, and GDE-0079 holds the full twelve-command static check that
  POL-0079 now links. Fourteen documents lost the retired subject-folder
  wording in their Traceability line.
- W10 (owner follow-up): Applied the script decisions the owner delegated.
  `post-tool-validate.sh` and `sync-tech-stack-versions.sh` became check-only
  unless `--write` is given, and their callers (the post-edit hook, Renovate
  and its command allowlist) pass `--write`. Three manifest rows moved to the
  file that governs them, two mutation labels were corrected, the stale
  Registry `generated_outputs` entry was emptied, and the evidence detector
  learned three launcher shapes so their consumers are declared. Each change
  had a failing test first.
- W11 (owner follow-up): Removed the `### Agent Operations (If Applicable)`
  subsection from 18 Runbooks whose items were all N/A or restated their
  Verification checks; RUN-0055 to RUN-0058 keep theirs as real model and
  inference procedures. The first full gate after the rebase failed one
  `test_heading` case that took its generated-body owner from the Registry
  entry W10 emptied; the test now supplies its own owner map.

## Verification Evidence

Baseline gate: `python3 scripts/validation/run-ci-gate.py --profile full` on
the baseline exited 1 with one failure,
`test_repository_contracts_validate_canonical_spec_packages`, which read this
package's untracked `spec.md` written while the gate ran. The same test on a
clean detached worktree of `main` passed (`Ran 1 test`, `OK`). The failure is a
concurrency artifact of this session, not baseline debt; the final full gate
reruns every suite.

Disposition ledger. Paths are relative to `docs/05.operations/`. Consumers
count, at baseline and outside Stage 98, the files naming the document's
subject path and the files naming its identifier. Verification: V1 is the
operations check (path, number, identity, slug, index membership) plus the
link check; V2 is the index membership check and the link check; V3 is the
incident packet check.

| Old path | artifact_id | Role | Domain / subject | Status | parent_ids | Consumers (path / ID) | Conflict, duplication, drift | Target path | Disposition | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `catalog/00-workspace/0001-common-optimizations-template-exceptions/policy.md` | `POL-0001` | policy | 00-workspace / 0001-common-optimizations-template-exceptions | active | [] | 4 / 1 | agent-execution rules in a human Policy; now link `.agents/`; invented `Agents` scope line removed | `policies/0001-common-optimizations-template-exceptions.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0002-developer-environment/guide.md` | `GDE-0002` | guide | 00-workspace / 0002-developer-environment | active | [] | 3 / 0 | none found | `guides/0002-developer-environment.md` | move | V1 |
| `catalog/00-workspace/0003-env-key-comparison/guide.md` | `GDE-0003` | guide | 00-workspace / 0003-env-key-comparison | active | [] | 3 / 0 | none found | `guides/0003-env-key-comparison.md` | move | V1 |
| `catalog/00-workspace/0004-harness-agent-first-engineering/guide.md` | `GDE-0004` | guide | 00-workspace / 0004-harness-agent-first-engineering | active | SPEC-0094 | 3 / 2 | none found | `guides/0004-harness-agent-first-engineering.md` | move | V1 |
| `catalog/00-workspace/0004-harness-agent-first-engineering/policy.md` | `POL-0004` | policy | 00-workspace / 0004-harness-agent-first-engineering | active | SPEC-0094 | 3 / 2 | Policy held the RUN-0004 command bundle; now links it | `policies/0004-harness-agent-first-engineering.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md` | `RUN-0004` | runbook | 00-workspace / 0004-harness-agent-first-engineering | active | SPEC-0094 | 2 / 2 | boilerplate N/A recovery line removed | `runbooks/0004-harness-agent-first-engineering.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md` | `POL-0006` | policy | 00-workspace / 0006-infrastructure-optimization-governance | active | [] | 5 / 1 | restated the HOME list POL-0078 owns; now links it; invented `Agents` scope line removed | `policies/0006-infrastructure-optimization-governance.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0008-new-service-onboarding/guide.md` | `GDE-0008` | guide | 00-workspace / 0008-new-service-onboarding | active | RUN-0009 | 3 / 0 | none found | `guides/0008-new-service-onboarding.md` | move | V1 |
| `catalog/00-workspace/0009-release-management/runbook.md` | `RUN-0009` | runbook | 00-workspace / 0009-release-management | active | [] | 8 / 1 | generic Agent Operations filler removed | `runbooks/0009-release-management.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md` | `GDE-0010` | guide | 00-workspace / 0010-sensitive-env-vars-comparison | active | [] | 3 / 0 | none found | `guides/0010-sensitive-env-vars-comparison.md` | move | V1 |
| `catalog/00-workspace/0078-compose-profile-vocabulary/policy.md` | `POL-0078` | policy | 00-workspace / 0078-compose-profile-vocabulary | active | [] | 13 / 12 | invented `Agents` scope line removed | `policies/0078-compose-profile-vocabulary.md` | move, edit (W6) | V1 |
| `catalog/00-workspace/0086-dependency-version-management/guide.md` | `GDE-0086` | guide | 00-workspace / 0086-dependency-version-management | draft | POL-0086 | 1 / 0 | missing from the 00-workspace index table at baseline | `guides/0086-dependency-version-management.md` | move | V1 |
| `catalog/00-workspace/0086-dependency-version-management/policy.md` | `POL-0086` | policy | 00-workspace / 0086-dependency-version-management | draft | AD-0031 | 3 / 6 | missing from the 00-workspace index table at baseline | `policies/0086-dependency-version-management.md` | move | V1 |
| `catalog/00-workspace/0086-dependency-version-management/runbook.md` | `RUN-0086` | runbook | 00-workspace / 0086-dependency-version-management | draft | POL-0086 | 1 / 0 | missing from the 00-workspace index table at baseline | `runbooks/0086-dependency-version-management.md` | move | V1 |
| `catalog/00-workspace/0098-cold-start-and-reboot/runbook.md` | `RUN-0098` | runbook | 00-workspace / 0098-cold-start-and-reboot | draft | SPEC-0182 | 1 / 1 | copied RUN-0021 backup and RUN-0085 SecretID commands; now links them | `runbooks/0098-cold-start-and-reboot.md` | move, edit (W6) | V1 |
| `catalog/01-gateway/0011-nginx/guide.md` | `GDE-0011` | guide | 01-gateway / 0011-nginx | active | POL-0011 | 6 / 2 | none found | `guides/0011-nginx.md` | move | V1 |
| `catalog/01-gateway/0011-nginx/policy.md` | `POL-0011` | policy | 01-gateway / 0011-nginx | active | AD-0001 | 3 / 2 | N/A AI Agent Policy filler removed; its two real controls moved to Controls; invented `Agents` scope line removed | `policies/0011-nginx.md` | move, edit (W6) | V1 |
| `catalog/01-gateway/0011-nginx/runbook.md` | `RUN-0011` | runbook | 01-gateway / 0011-nginx | active | GDE-0011 | 5 / 2 | none found | `runbooks/0011-nginx.md` | move | V1 |
| `catalog/01-gateway/0012-edge-routing-stack/guide.md` | `GDE-0012` | guide | 01-gateway / 0012-edge-routing-stack | active | [] | 2 / 1 | none found | `guides/0012-edge-routing-stack.md` | move | V1 |
| `catalog/01-gateway/0013-traefik/guide.md` | `GDE-0013` | guide | 01-gateway / 0013-traefik | active | POL-0013 | 7 / 2 | none found | `guides/0013-traefik.md` | move | V1 |
| `catalog/01-gateway/0013-traefik/policy.md` | `POL-0013` | policy | 01-gateway / 0013-traefik | active | AD-0001 | 3 / 2 | N/A AI Agent Policy filler removed; its two real controls moved to Controls; invented `Agents` scope line removed | `policies/0013-traefik.md` | move, edit (W6) | V1 |
| `catalog/01-gateway/0013-traefik/runbook.md` | `RUN-0013` | runbook | 01-gateway / 0013-traefik | active | GDE-0013 | 5 / 2 | none found | `runbooks/0013-traefik.md` | move | V1 |
| `catalog/02-auth/0014-keycloak/guide.md` | `GDE-0014` | guide | 02-auth / 0014-keycloak | active | POL-0014 | 7 / 2 | none found | `guides/0014-keycloak.md` | move | V1 |
| `catalog/02-auth/0014-keycloak/policy.md` | `POL-0014` | policy | 02-auth / 0014-keycloak | active | AD-0002 | 3 / 2 | N/A AI Agent Policy filler removed; its two real controls moved to Controls; invented `Agents` scope line removed | `policies/0014-keycloak.md` | move, edit (W6) | V1 |
| `catalog/02-auth/0014-keycloak/runbook.md` | `RUN-0014` | runbook | 02-auth / 0014-keycloak | active | GDE-0014 | 6 / 3 | none found | `runbooks/0014-keycloak.md` | move | V1 |
| `catalog/02-auth/0015-oauth2-proxy/guide.md` | `GDE-0015` | guide | 02-auth / 0015-oauth2-proxy | active | POL-0015 | 6 / 2 | none found | `guides/0015-oauth2-proxy.md` | move | V1 |
| `catalog/02-auth/0015-oauth2-proxy/policy.md` | `POL-0015` | policy | 02-auth / 0015-oauth2-proxy | active | AD-0002 | 2 / 2 | N/A AI Agent Policy filler removed; its two real controls moved to Controls; invented `Agents` scope line removed | `policies/0015-oauth2-proxy.md` | move, edit (W6) | V1 |
| `catalog/02-auth/0015-oauth2-proxy/runbook.md` | `RUN-0015` | runbook | 02-auth / 0015-oauth2-proxy | active | GDE-0015 | 4 / 2 | none found | `runbooks/0015-oauth2-proxy.md` | move | V1 |
| `catalog/02-auth/0079-application-auth-integration/guide.md` | `GDE-0079` | guide | 02-auth / 0079-application-auth-integration | draft | POL-0079 | 8 / 7 | `airflow db migrate` step contradicted the POL-0050 schedule-pause precondition; now links RUN-0050 | `guides/0079-application-auth-integration.md` | move, edit (W6) | V1 |
| `catalog/02-auth/0079-application-auth-integration/policy.md` | `POL-0079` | policy | 02-auth / 0079-application-auth-integration | draft | ADR-0038 | 3 / 3 | none found | `policies/0079-application-auth-integration.md` | move | V1 |
| `catalog/03-security/0085-openbao/guide.md` | `GDE-0085` | guide | 03-security / 0085-openbao | draft | POL-0085 | 7 / 1 | none found | `guides/0085-openbao.md` | move | V1 |
| `catalog/03-security/0085-openbao/policy.md` | `POL-0085` | policy | 03-security / 0085-openbao | draft | AD-0003 | 4 / 3 | none found | `policies/0085-openbao.md` | move | V1 |
| `catalog/03-security/0085-openbao/runbook.md` | `RUN-0085` | runbook | 03-security / 0085-openbao | draft | POL-0085 | 10 / 8 | none found | `runbooks/0085-openbao.md` | move | V1 |
| `catalog/04-data/0017-influxdb/guide.md` | `GDE-0017` | guide | 04-data / 0017-influxdb | active | POL-0017 | 4 / 3 | none found | `guides/0017-influxdb.md` | move | V1 |
| `catalog/04-data/0017-influxdb/policy.md` | `POL-0017` | policy | 04-data / 0017-influxdb | active | AD-0012 | 3 / 3 | none found | `policies/0017-influxdb.md` | move | V1 |
| `catalog/04-data/0017-influxdb/runbook.md` | `RUN-0017` | runbook | 04-data / 0017-influxdb | active | GDE-0017 | 4 / 3 | none found | `runbooks/0017-influxdb.md` | move | V1 |
| `catalog/04-data/0019-opensearch/guide.md` | `GDE-0019` | guide | 04-data / 0019-opensearch | active | POL-0019 | 4 / 3 | none found | `guides/0019-opensearch.md` | move | V1 |
| `catalog/04-data/0019-opensearch/policy.md` | `POL-0019` | policy | 04-data / 0019-opensearch | active | AD-0012 | 3 / 3 | none found | `policies/0019-opensearch.md` | move | V1 |
| `catalog/04-data/0019-opensearch/runbook.md` | `RUN-0019` | runbook | 04-data / 0019-opensearch | active | GDE-0019 | 4 / 3 | none found | `runbooks/0019-opensearch.md` | move | V1 |
| `catalog/04-data/0021-backup-and-restore/guide.md` | `GDE-0021` | guide | 04-data / 0021-backup-and-restore | draft | POL-0021 | 2 / 1 | none found | `guides/0021-backup-and-restore.md` | move | V1 |
| `catalog/04-data/0021-backup-and-restore/policy.md` | `POL-0021` | policy | 04-data / 0021-backup-and-restore | active | AD-0004 | 16 / 19 | none found | `policies/0021-backup-and-restore.md` | move | V1 |
| `catalog/04-data/0021-backup-and-restore/runbook.md` | `RUN-0021` | runbook | 04-data / 0021-backup-and-restore | draft | GDE-0021 | 8 / 19 | none found | `runbooks/0021-backup-and-restore.md` | move | V1 |
| `catalog/04-data/0022-valkey-cluster/guide.md` | `GDE-0022` | guide | 04-data / 0022-valkey-cluster | active | POL-0022 | 3 / 1 | none found | `guides/0022-valkey-cluster.md` | move | V1 |
| `catalog/04-data/0022-valkey-cluster/policy.md` | `POL-0022` | policy | 04-data / 0022-valkey-cluster | active | AD-0004 | 2 / 1 | none found | `policies/0022-valkey-cluster.md` | move | V1 |
| `catalog/04-data/0022-valkey-cluster/runbook.md` | `RUN-0022` | runbook | 04-data / 0022-valkey-cluster | active | GDE-0022 | 5 / 3 | none found | `runbooks/0022-valkey-cluster.md` | move | V1 |
| `catalog/04-data/0024-seaweedfs/guide.md` | `GDE-0024` | guide | 04-data / 0024-seaweedfs | active | POL-0024 | 4 / 2 | none found | `guides/0024-seaweedfs.md` | move | V1 |
| `catalog/04-data/0024-seaweedfs/policy.md` | `POL-0024` | policy | 04-data / 0024-seaweedfs | active | AD-0004 | 4 / 7 | none found | `policies/0024-seaweedfs.md` | move | V1 |
| `catalog/04-data/0024-seaweedfs/runbook.md` | `RUN-0024` | runbook | 04-data / 0024-seaweedfs | active | GDE-0024 | 9 / 15 | none found | `runbooks/0024-seaweedfs.md` | move | V1 |
| `catalog/04-data/0025-cassandra/guide.md` | `GDE-0025` | guide | 04-data / 0025-cassandra | active | POL-0025 | 4 / 3 | Guide copied its Runbook command list; now links it | `guides/0025-cassandra.md` | move, edit (W6) | V1 |
| `catalog/04-data/0025-cassandra/policy.md` | `POL-0025` | policy | 04-data / 0025-cassandra | active | AD-0004 | 4 / 3 | none found | `policies/0025-cassandra.md` | move | V1 |
| `catalog/04-data/0025-cassandra/runbook.md` | `RUN-0025` | runbook | 04-data / 0025-cassandra | active | GDE-0025 | 4 / 3 | generic documentation-revert recovery step removed | `runbooks/0025-cassandra.md` | move, edit (W6) | V1 |
| `catalog/04-data/0026-couchdb/guide.md` | `GDE-0026` | guide | 04-data / 0026-couchdb | active | POL-0026 | 4 / 3 | Guide copied its Runbook command list; now links it | `guides/0026-couchdb.md` | move, edit (W6) | V1 |
| `catalog/04-data/0026-couchdb/policy.md` | `POL-0026` | policy | 04-data / 0026-couchdb | active | AD-0004 | 3 / 3 | none found | `policies/0026-couchdb.md` | move | V1 |
| `catalog/04-data/0026-couchdb/runbook.md` | `RUN-0026` | runbook | 04-data / 0026-couchdb | active | GDE-0026 | 4 / 3 | generic documentation-revert recovery step removed | `runbooks/0026-couchdb.md` | move, edit (W6) | V1 |
| `catalog/04-data/0027-mongodb/guide.md` | `GDE-0027` | guide | 04-data / 0027-mongodb | active | POL-0027 | 4 / 3 | Guide copied its Runbook command list; now links it | `guides/0027-mongodb.md` | move, edit (W6) | V1 |
| `catalog/04-data/0027-mongodb/policy.md` | `POL-0027` | policy | 04-data / 0027-mongodb | active | AD-0004 | 3 / 3 | none found | `policies/0027-mongodb.md` | move | V1 |
| `catalog/04-data/0027-mongodb/runbook.md` | `RUN-0027` | runbook | 04-data / 0027-mongodb | active | GDE-0027 | 4 / 3 | generic documentation-revert recovery step removed | `runbooks/0027-mongodb.md` | move, edit (W6) | V1 |
| `catalog/04-data/0028-management-database/guide.md` | `GDE-0028` | guide | 04-data / 0028-management-database | active | POL-0028 | 4 / 1 | none found | `guides/0028-management-database.md` | move | V1 |
| `catalog/04-data/0028-management-database/policy.md` | `POL-0028` | policy | 04-data / 0028-management-database | active | AD-0004 | 5 / 1 | none found | `policies/0028-management-database.md` | move | V1 |
| `catalog/04-data/0028-management-database/runbook.md` | `RUN-0028` | runbook | 04-data / 0028-management-database | active | GDE-0028 | 10 / 4 | none found | `runbooks/0028-management-database.md` | move | V1 |
| `catalog/04-data/0029-supabase/guide.md` | `GDE-0029` | guide | 04-data / 0029-supabase | active | POL-0029 | 4 / 3 | none found | `guides/0029-supabase.md` | move | V1 |
| `catalog/04-data/0029-supabase/policy.md` | `POL-0029` | policy | 04-data / 0029-supabase | active | AD-0004 | 3 / 3 | invented `Agents` scope line removed | `policies/0029-supabase.md` | move, edit (W6) | V1 |
| `catalog/04-data/0029-supabase/runbook.md` | `RUN-0029` | runbook | 04-data / 0029-supabase | active | GDE-0029 | 4 / 3 | none found | `runbooks/0029-supabase.md` | move | V1 |
| `catalog/04-data/0030-optimization-hardening/guide.md` | `GDE-0030` | guide | 04-data / 0030-optimization-hardening | active | POL-0030 | 2 / 1 | generic slug qualified by domain; Guide copied its Runbook command list; now links it | `guides/0030-data-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/04-data/0030-optimization-hardening/policy.md` | `POL-0030` | policy | 04-data / 0030-optimization-hardening | active | AD-0004 | 4 / 1 | generic slug qualified by domain | `policies/0030-data-optimization-hardening.md` | move | V1 |
| `catalog/04-data/0030-optimization-hardening/runbook.md` | `RUN-0030` | runbook | 04-data / 0030-optimization-hardening | active | GDE-0030 | 2 / 0 | generic slug qualified by domain | `runbooks/0030-data-optimization-hardening.md` | move | V1 |
| `catalog/04-data/0031-postgresql-cluster/guide.md` | `GDE-0031` | guide | 04-data / 0031-postgresql-cluster | active | POL-0031 | 5 / 3 | Guide copied its Runbook command list; now links it | `guides/0031-postgresql-cluster.md` | move, edit (W6) | V1 |
| `catalog/04-data/0031-postgresql-cluster/policy.md` | `POL-0031` | policy | 04-data / 0031-postgresql-cluster | active | AD-0004 | 3 / 3 | none found | `policies/0031-postgresql-cluster.md` | move | V1 |
| `catalog/04-data/0031-postgresql-cluster/runbook.md` | `RUN-0031` | runbook | 04-data / 0031-postgresql-cluster | active | GDE-0031 | 6 / 3 | generic documentation-revert recovery step removed | `runbooks/0031-postgresql-cluster.md` | move, edit (W6) | V1 |
| `catalog/04-data/0032-postgresql-logical-upgrade-restore-rehearsal/runbook.md` | `RUN-0032` | runbook | 04-data / 0032-postgresql-logical-upgrade-restore-rehearsal | active | [] | 6 / 5 | none found | `runbooks/0032-postgresql-logical-upgrade-restore-rehearsal.md` | move | V1 |
| `catalog/04-data/0033-neo4j/guide.md` | `GDE-0033` | guide | 04-data / 0033-neo4j | active | POL-0033 | 4 / 3 | Guide copied its Runbook command list; now links it | `guides/0033-neo4j.md` | move, edit (W6) | V1 |
| `catalog/04-data/0033-neo4j/policy.md` | `POL-0033` | policy | 04-data / 0033-neo4j | active | AD-0004 | 3 / 3 | none found | `policies/0033-neo4j.md` | move | V1 |
| `catalog/04-data/0033-neo4j/runbook.md` | `RUN-0033` | runbook | 04-data / 0033-neo4j | active | GDE-0033 | 4 / 3 | generic documentation-revert recovery step removed | `runbooks/0033-neo4j.md` | move, edit (W6) | V1 |
| `catalog/04-data/0034-qdrant/guide.md` | `GDE-0034` | guide | 04-data / 0034-qdrant | active | POL-0034 | 5 / 3 | Guide copied its Runbook command list; now links it | `guides/0034-qdrant.md` | move, edit (W6) | V1 |
| `catalog/04-data/0034-qdrant/policy.md` | `POL-0034` | policy | 04-data / 0034-qdrant | active | AD-0004 | 3 / 3 | none found | `policies/0034-qdrant.md` | move | V1 |
| `catalog/04-data/0034-qdrant/runbook.md` | `RUN-0034` | runbook | 04-data / 0034-qdrant | active | GDE-0034 | 5 / 4 | generic documentation-revert recovery step removed | `runbooks/0034-qdrant.md` | move, edit (W6) | V1 |
| `catalog/04-data/0035-storage-exhaustion/runbook.md` | `RUN-0035` | runbook | 04-data / 0035-storage-exhaustion | active | [] | 5 / 3 | none found | `runbooks/0035-storage-exhaustion.md` | move | V1 |
| `catalog/04-data/0094-lakehouse/guide.md` | `GDE-0094` | guide | 04-data / 0094-lakehouse | draft | POL-0094 | 7 / 2 | none found | `guides/0094-lakehouse.md` | move | V1 |
| `catalog/04-data/0094-lakehouse/policy.md` | `POL-0094` | policy | 04-data / 0094-lakehouse | draft | AD-0004 | 7 / 4 | none found | `policies/0094-lakehouse.md` | move | V1 |
| `catalog/04-data/0094-lakehouse/runbook.md` | `RUN-0094` | runbook | 04-data / 0094-lakehouse | draft | GDE-0094 | 6 / 4 | none found | `runbooks/0094-lakehouse.md` | move | V1 |
| `catalog/04-data/0097-superset/guide.md` | `GDE-0097` | guide | 04-data / 0097-superset | draft | POL-0097 | 3 / 2 | none found | `guides/0097-superset.md` | move | V1 |
| `catalog/04-data/0097-superset/policy.md` | `POL-0097` | policy | 04-data / 0097-superset | draft | AD-0004 | 3 / 2 | none found | `policies/0097-superset.md` | move | V1 |
| `catalog/04-data/0097-superset/runbook.md` | `RUN-0097` | runbook | 04-data / 0097-superset | draft | GDE-0097 | 4 / 3 | none found | `runbooks/0097-superset.md` | move | V1 |
| `catalog/05-messaging/0036-kafka/guide.md` | `GDE-0036` | guide | 05-messaging / 0036-kafka | active | POL-0036 | 7 / 2 | none found | `guides/0036-kafka.md` | move | V1 |
| `catalog/05-messaging/0036-kafka/policy.md` | `POL-0036` | policy | 05-messaging / 0036-kafka | active | AD-0005 | 3 / 2 | none found | `policies/0036-kafka.md` | move | V1 |
| `catalog/05-messaging/0036-kafka/runbook.md` | `RUN-0036` | runbook | 05-messaging / 0036-kafka | active | GDE-0036 | 5 / 5 | none found | `runbooks/0036-kafka.md` | move | V1 |
| `catalog/05-messaging/0037-optimization-hardening/guide.md` | `GDE-0037` | guide | 05-messaging / 0037-optimization-hardening | active | POL-0037 | 2 / 2 | generic slug qualified by domain; Guide copied its Runbook command list; now links it | `guides/0037-messaging-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/05-messaging/0037-optimization-hardening/policy.md` | `POL-0037` | policy | 05-messaging / 0037-optimization-hardening | active | AD-0005 | 2 / 1 | generic slug qualified by domain | `policies/0037-messaging-optimization-hardening.md` | move | V1 |
| `catalog/05-messaging/0037-optimization-hardening/runbook.md` | `RUN-0037` | runbook | 05-messaging / 0037-optimization-hardening | active | GDE-0037 | 2 / 1 | generic slug qualified by domain | `runbooks/0037-messaging-optimization-hardening.md` | move | V1 |
| `catalog/06-observability/0039-alertmanager/guide.md` | `GDE-0039` | guide | 06-observability / 0039-alertmanager | active | POL-0039 | 5 / 3 | none found | `guides/0039-alertmanager.md` | move | V1 |
| `catalog/06-observability/0039-alertmanager/policy.md` | `POL-0039` | policy | 06-observability / 0039-alertmanager | active | AD-0006 | 3 / 3 | invented `Agents` scope line removed | `policies/0039-alertmanager.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0039-alertmanager/runbook.md` | `RUN-0039` | runbook | 06-observability / 0039-alertmanager | active | GDE-0039 | 4 / 4 | generic Agent Operations filler removed | `runbooks/0039-alertmanager.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0040-alloy/guide.md` | `GDE-0040` | guide | 06-observability / 0040-alloy | active | POL-0040 | 9 / 3 | none found | `guides/0040-alloy.md` | move | V1 |
| `catalog/06-observability/0040-alloy/policy.md` | `POL-0040` | policy | 06-observability / 0040-alloy | active | AD-0006 | 4 / 3 | invented `Agents` scope line removed | `policies/0040-alloy.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0040-alloy/runbook.md` | `RUN-0040` | runbook | 06-observability / 0040-alloy | active | GDE-0040 | 5 / 3 | generic Agent Operations filler removed | `runbooks/0040-alloy.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0041-grafana/guide.md` | `GDE-0041` | guide | 06-observability / 0041-grafana | active | POL-0041 | 8 / 3 | none found | `guides/0041-grafana.md` | move | V1 |
| `catalog/06-observability/0041-grafana/policy.md` | `POL-0041` | policy | 06-observability / 0041-grafana | active | AD-0006 | 3 / 3 | invented `Agents` scope line removed | `policies/0041-grafana.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0041-grafana/runbook.md` | `RUN-0041` | runbook | 06-observability / 0041-grafana | active | GDE-0041 | 4 / 3 | generic Agent Operations filler removed | `runbooks/0041-grafana.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0042-lgtm-stack/guide.md` | `GDE-0042` | guide | 06-observability / 0042-lgtm-stack | active | [] | 2 / 0 | none found | `guides/0042-lgtm-stack.md` | move | V1 |
| `catalog/06-observability/0043-loki/guide.md` | `GDE-0043` | guide | 06-observability / 0043-loki | active | POL-0043 | 6 / 3 | none found | `guides/0043-loki.md` | move | V1 |
| `catalog/06-observability/0043-loki/policy.md` | `POL-0043` | policy | 06-observability / 0043-loki | active | AD-0006 | 4 / 3 | retention values duplicated POL-0048; now link it; invented `Agents` scope line removed | `policies/0043-loki.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0043-loki/runbook.md` | `RUN-0043` | runbook | 06-observability / 0043-loki | active | GDE-0043 | 4 / 3 | generic Agent Operations filler removed | `runbooks/0043-loki.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0044-optimization-hardening/guide.md` | `GDE-0044` | guide | 06-observability / 0044-optimization-hardening | active | POL-0044 | 3 / 2 | generic slug qualified by domain | `guides/0044-observability-optimization-hardening.md` | move | V1 |
| `catalog/06-observability/0044-optimization-hardening/policy.md` | `POL-0044` | policy | 06-observability / 0044-optimization-hardening | active | AD-0006 | 3 / 2 | generic slug qualified by domain; invented `Agents` scope line removed | `policies/0044-observability-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0044-optimization-hardening/runbook.md` | `RUN-0044` | runbook | 06-observability / 0044-optimization-hardening | active | GDE-0044 | 3 / 2 | generic slug qualified by domain | `runbooks/0044-observability-optimization-hardening.md` | move | V1 |
| `catalog/06-observability/0045-prometheus/guide.md` | `GDE-0045` | guide | 06-observability / 0045-prometheus | active | POL-0045 | 8 / 3 | none found | `guides/0045-prometheus.md` | move | V1 |
| `catalog/06-observability/0045-prometheus/policy.md` | `POL-0045` | policy | 06-observability / 0045-prometheus | active | AD-0006 | 7 / 3 | invented `Agents` scope line removed | `policies/0045-prometheus.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0045-prometheus/runbook.md` | `RUN-0045` | runbook | 06-observability / 0045-prometheus | active | GDE-0045 | 5 / 3 | generic Agent Operations filler removed | `runbooks/0045-prometheus.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0046-pushgateway/guide.md` | `GDE-0046` | guide | 06-observability / 0046-pushgateway | active | POL-0046 | 5 / 3 | none found | `guides/0046-pushgateway.md` | move | V1 |
| `catalog/06-observability/0046-pushgateway/policy.md` | `POL-0046` | policy | 06-observability / 0046-pushgateway | active | AD-0006 | 3 / 3 | invented `Agents` scope line removed | `policies/0046-pushgateway.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0046-pushgateway/runbook.md` | `RUN-0046` | runbook | 06-observability / 0046-pushgateway | active | GDE-0046 | 4 / 3 | none found | `runbooks/0046-pushgateway.md` | move | V1 |
| `catalog/06-observability/0047-pyroscope/guide.md` | `GDE-0047` | guide | 06-observability / 0047-pyroscope | active | POL-0047 | 6 / 3 | none found | `guides/0047-pyroscope.md` | move | V1 |
| `catalog/06-observability/0047-pyroscope/policy.md` | `POL-0047` | policy | 06-observability / 0047-pyroscope | active | AD-0006 | 4 / 3 | invented `Agents` scope line removed | `policies/0047-pyroscope.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0047-pyroscope/runbook.md` | `RUN-0047` | runbook | 06-observability / 0047-pyroscope | active | GDE-0047 | 4 / 3 | generic Agent Operations filler removed | `runbooks/0047-pyroscope.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0048-telemetry-retention/policy.md` | `POL-0048` | policy | 06-observability / 0048-telemetry-retention | active | AD-0006 | 5 / 0 | invented `Agents` scope line removed | `policies/0048-telemetry-retention.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0049-tempo/guide.md` | `GDE-0049` | guide | 06-observability / 0049-tempo | active | POL-0049 | 5 / 3 | none found | `guides/0049-tempo.md` | move | V1 |
| `catalog/06-observability/0049-tempo/policy.md` | `POL-0049` | policy | 06-observability / 0049-tempo | active | AD-0006 | 4 / 3 | retention values duplicated POL-0048; now link it; invented `Agents` scope line removed | `policies/0049-tempo.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0049-tempo/runbook.md` | `RUN-0049` | runbook | 06-observability / 0049-tempo | active | GDE-0049 | 5 / 3 | generic Agent Operations filler removed | `runbooks/0049-tempo.md` | move, edit (W6) | V1 |
| `catalog/06-observability/0087-gatus/guide.md` | `GDE-0087` | guide | 06-observability / 0087-gatus | draft | POL-0087 | 2 / 1 | none found | `guides/0087-gatus.md` | move | V1 |
| `catalog/06-observability/0087-gatus/policy.md` | `POL-0087` | policy | 06-observability / 0087-gatus | draft | AD-0031 | 2 / 3 | none found | `policies/0087-gatus.md` | move | V1 |
| `catalog/06-observability/0087-gatus/runbook.md` | `RUN-0087` | runbook | 06-observability / 0087-gatus | draft | POL-0087 | 3 / 1 | none found | `runbooks/0087-gatus.md` | move | V1 |
| `catalog/07-workflow/0050-airflow/guide.md` | `GDE-0050` | guide | 07-workflow / 0050-airflow | active | POL-0050 | 9 / 3 | none found | `guides/0050-airflow.md` | move | V1 |
| `catalog/07-workflow/0050-airflow/policy.md` | `POL-0050` | policy | 07-workflow / 0050-airflow | active | AD-0007 | 4 / 3 | invented `Agents` scope line removed | `policies/0050-airflow.md` | move, edit (W6) | V1 |
| `catalog/07-workflow/0050-airflow/runbook.md` | `RUN-0050` | runbook | 07-workflow / 0050-airflow | active | GDE-0050 | 8 / 6 | generic Agent Operations filler removed | `runbooks/0050-airflow.md` | move, edit (W6) | V1 |
| `catalog/07-workflow/0051-airflow-dag-lifecycle/guide.md` | `GDE-0051` | guide | 07-workflow / 0051-airflow-dag-lifecycle | active | POL-0052 | 2 / 1 | none found | `guides/0051-airflow-dag-lifecycle.md` | move | V1 |
| `catalog/07-workflow/0051-airflow-dag-lifecycle/policy.md` | `POL-0052` | policy | 07-workflow / 0051-airflow-dag-lifecycle | active | AD-0007 | 2 / 1 | artifact number differs from subject 0051 (MIG-0002 merge); ID kept | `policies/0052-airflow-dag-lifecycle.md` | move | V1 |
| `catalog/07-workflow/0053-n8n/guide.md` | `GDE-0053` | guide | 07-workflow / 0053-n8n | active | POL-0053 | 5 / 3 | none found | `guides/0053-n8n.md` | move | V1 |
| `catalog/07-workflow/0053-n8n/policy.md` | `POL-0053` | policy | 07-workflow / 0053-n8n | active | AD-0007 | 4 / 3 | invented `Agents` scope line removed | `policies/0053-n8n.md` | move, edit (W6) | V1 |
| `catalog/07-workflow/0053-n8n/runbook.md` | `RUN-0053` | runbook | 07-workflow / 0053-n8n | active | GDE-0053 | 5 / 5 | generic Agent Operations filler removed | `runbooks/0053-n8n.md` | move, edit (W6) | V1 |
| `catalog/07-workflow/0054-optimization-hardening/guide.md` | `GDE-0054` | guide | 07-workflow / 0054-optimization-hardening | active | POL-0054 | 2 / 2 | generic slug qualified by domain | `guides/0054-workflow-optimization-hardening.md` | move | V1 |
| `catalog/07-workflow/0054-optimization-hardening/policy.md` | `POL-0054` | policy | 07-workflow / 0054-optimization-hardening | active | AD-0007 | 2 / 2 | generic slug qualified by domain; invented `Agents` scope line removed | `policies/0054-workflow-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/07-workflow/0054-optimization-hardening/runbook.md` | `RUN-0054` | runbook | 07-workflow / 0054-optimization-hardening | active | GDE-0054 | 2 / 2 | generic slug qualified by domain | `runbooks/0054-workflow-optimization-hardening.md` | move | V1 |
| `catalog/08-ai/0055-gpu-recovery/runbook.md` | `RUN-0055` | runbook | 08-ai / 0055-gpu-recovery | active | [] | 2 / 0 | none found | `runbooks/0055-gpu-recovery.md` | move | V1 |
| `catalog/08-ai/0056-ollama/guide.md` | `GDE-0056` | guide | 08-ai / 0056-ollama | active | POL-0056 | 6 / 3 | unconditional model pull contradicted the POL-0056 rehearsal control; removed | `guides/0056-ollama.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0056-ollama/policy.md` | `POL-0056` | policy | 08-ai / 0056-ollama | active | AD-0008 | 4 / 3 | invented `Agents` scope line removed | `policies/0056-ollama.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0056-ollama/runbook.md` | `RUN-0056` | runbook | 08-ai / 0056-ollama | active | GDE-0056 | 5 / 5 | model fallback without approval, contrary to RUN-0055 and POL-0056; now requires operator approval; weaker GPU recovery copy now links RUN-0055 | `runbooks/0056-ollama.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0057-open-webui/guide.md` | `GDE-0057` | guide | 08-ai / 0057-open-webui | active | POL-0057 | 6 / 3 | none found | `guides/0057-open-webui.md` | move | V1 |
| `catalog/08-ai/0057-open-webui/policy.md` | `POL-0057` | policy | 08-ai / 0057-open-webui | active | AD-0008 | 4 / 3 | invented `Agents` scope line removed | `policies/0057-open-webui.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0057-open-webui/runbook.md` | `RUN-0057` | runbook | 08-ai / 0057-open-webui | active | GDE-0057 | 6 / 5 | model fallback now requires operator approval; cross-service Ollama restart now links RUN-0056 and RUN-0055 | `runbooks/0057-open-webui.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0058-optimization-hardening/guide.md` | `GDE-0058` | guide | 08-ai / 0058-optimization-hardening | active | POL-0058 | 2 / 2 | generic slug qualified by domain | `guides/0058-ai-optimization-hardening.md` | move | V1 |
| `catalog/08-ai/0058-optimization-hardening/policy.md` | `POL-0058` | policy | 08-ai / 0058-optimization-hardening | active | AD-0008 | 2 / 2 | generic slug qualified by domain; invented `Agents` scope line removed | `policies/0058-ai-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0058-optimization-hardening/runbook.md` | `RUN-0058` | runbook | 08-ai / 0058-optimization-hardening | active | GDE-0058 | 2 / 2 | generic slug qualified by domain; model fallback now requires operator approval | `runbooks/0058-ai-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/08-ai/0059-rag-workflow/guide.md` | `GDE-0059` | guide | 08-ai / 0059-rag-workflow | active | [] | 3 / 0 | none found | `guides/0059-rag-workflow.md` | move | V1 |
| `catalog/08-ai/0081-comfyui/guide.md` | `GDE-0081` | guide | 08-ai / 0081-comfyui | draft | POL-0081 | 2 / 2 | none found | `guides/0081-comfyui.md` | move | V1 |
| `catalog/08-ai/0081-comfyui/policy.md` | `POL-0081` | policy | 08-ai / 0081-comfyui | draft | AD-0008 | 2 / 2 | none found | `policies/0081-comfyui.md` | move | V1 |
| `catalog/08-ai/0081-comfyui/runbook.md` | `RUN-0081` | runbook | 08-ai / 0081-comfyui | draft | GDE-0081 | 2 / 3 | none found | `runbooks/0081-comfyui.md` | move | V1 |
| `catalog/08-ai/0091-crawl4ai/guide.md` | `GDE-0091` | guide | 08-ai / 0091-crawl4ai | active | POL-0091 | 3 / 3 | none found | `guides/0091-crawl4ai.md` | move | V1 |
| `catalog/08-ai/0091-crawl4ai/policy.md` | `POL-0091` | policy | 08-ai / 0091-crawl4ai | active | AD-0008 | 3 / 3 | none found | `policies/0091-crawl4ai.md` | move | V1 |
| `catalog/08-ai/0091-crawl4ai/runbook.md` | `RUN-0091` | runbook | 08-ai / 0091-crawl4ai | active | GDE-0091 | 3 / 3 | none found | `runbooks/0091-crawl4ai.md` | move | V1 |
| `catalog/09-tooling/0060-iac-deployment/policy.md` | `POL-0060` | policy | 09-tooling / 0060-iac-deployment | active | AD-0009 | 1 / 0 | invented `Agents` scope line removed | `policies/0060-iac-deployment.md` | move, edit (W6) | V1 |
| `catalog/09-tooling/0061-k6/guide.md` | `GDE-0061` | guide | 09-tooling / 0061-k6 | active | POL-0061 | 7 / 1 | none found | `guides/0061-k6.md` | move | V1 |
| `catalog/09-tooling/0061-k6/policy.md` | `POL-0061` | policy | 09-tooling / 0061-k6 | active | AD-0009 | 3 / 1 | Policy held Runbook commands; now links the Runbook | `policies/0061-k6.md` | move, edit (W6) | V1 |
| `catalog/09-tooling/0061-k6/runbook.md` | `RUN-0061` | runbook | 09-tooling / 0061-k6 | active | GDE-0061 | 5 / 0 | none found | `runbooks/0061-k6.md` | move | V1 |
| `catalog/09-tooling/0062-locust/guide.md` | `GDE-0062` | guide | 09-tooling / 0062-locust | active | POL-0062 | 5 / 2 | none found | `guides/0062-locust.md` | move | V1 |
| `catalog/09-tooling/0062-locust/policy.md` | `POL-0062` | policy | 09-tooling / 0062-locust | active | AD-0009 | 3 / 2 | none found | `policies/0062-locust.md` | move | V1 |
| `catalog/09-tooling/0062-locust/runbook.md` | `RUN-0062` | runbook | 09-tooling / 0062-locust | active | GDE-0062 | 5 / 2 | none found | `runbooks/0062-locust.md` | move | V1 |
| `catalog/09-tooling/0063-optimization-hardening/guide.md` | `GDE-0063` | guide | 09-tooling / 0063-optimization-hardening | active | POL-0063 | 2 / 2 | generic slug qualified by domain | `guides/0063-tooling-optimization-hardening.md` | move | V1 |
| `catalog/09-tooling/0063-optimization-hardening/policy.md` | `POL-0063` | policy | 09-tooling / 0063-optimization-hardening | active | AD-0009 | 2 / 2 | generic slug qualified by domain; invented `Agents` scope line removed | `policies/0063-tooling-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/09-tooling/0063-optimization-hardening/runbook.md` | `RUN-0063` | runbook | 09-tooling / 0063-optimization-hardening | active | GDE-0063 | 2 / 2 | generic slug qualified by domain | `runbooks/0063-tooling-optimization-hardening.md` | move | V1 |
| `catalog/09-tooling/0064-performance-testing/guide.md` | `GDE-0064` | guide | 09-tooling / 0064-performance-testing | active | POL-0064 | 1 / 2 | none found | `guides/0064-performance-testing.md` | move | V1 |
| `catalog/09-tooling/0064-performance-testing/policy.md` | `POL-0064` | policy | 09-tooling / 0064-performance-testing | active | AD-0009 | 1 / 2 | none found | `policies/0064-performance-testing.md` | move | V1 |
| `catalog/09-tooling/0064-performance-testing/runbook.md` | `RUN-0064` | runbook | 09-tooling / 0064-performance-testing | active | GDE-0064 | 1 / 2 | none found | `runbooks/0064-performance-testing.md` | move | V1 |
| `catalog/09-tooling/0065-registry/guide.md` | `GDE-0065` | guide | 09-tooling / 0065-registry | active | POL-0065 | 4 / 2 | none found | `guides/0065-registry.md` | move | V1 |
| `catalog/09-tooling/0065-registry/policy.md` | `POL-0065` | policy | 09-tooling / 0065-registry | active | AD-0009 | 3 / 2 | none found | `policies/0065-registry.md` | move | V1 |
| `catalog/09-tooling/0065-registry/runbook.md` | `RUN-0065` | runbook | 09-tooling / 0065-registry | active | GDE-0065 | 4 / 2 | none found | `runbooks/0065-registry.md` | move | V1 |
| `catalog/09-tooling/0066-sonarqube/guide.md` | `GDE-0066` | guide | 09-tooling / 0066-sonarqube | active | POL-0066 | 4 / 2 | none found | `guides/0066-sonarqube.md` | move | V1 |
| `catalog/09-tooling/0066-sonarqube/policy.md` | `POL-0066` | policy | 09-tooling / 0066-sonarqube | active | AD-0009 | 3 / 2 | none found | `policies/0066-sonarqube.md` | move | V1 |
| `catalog/09-tooling/0066-sonarqube/runbook.md` | `RUN-0066` | runbook | 09-tooling / 0066-sonarqube | active | GDE-0066 | 4 / 2 | none found | `runbooks/0066-sonarqube.md` | move | V1 |
| `catalog/09-tooling/0068-terraform/guide.md` | `GDE-0068` | guide | 09-tooling / 0068-terraform | active | POL-0068 | 8 / 1 | none found | `guides/0068-terraform.md` | move | V1 |
| `catalog/09-tooling/0068-terraform/policy.md` | `POL-0068` | policy | 09-tooling / 0068-terraform | active | AD-0009 | 1 / 1 | none found | `policies/0068-terraform.md` | move | V1 |
| `catalog/09-tooling/0068-terraform/runbook.md` | `RUN-0068` | runbook | 09-tooling / 0068-terraform | active | GDE-0068 | 1 / 0 | none found | `runbooks/0068-terraform.md` | move | V1 |
| `catalog/09-tooling/0069-terrakube/guide.md` | `GDE-0069` | guide | 09-tooling / 0069-terrakube | active | POL-0069 | 5 / 2 | none found | `guides/0069-terrakube.md` | move | V1 |
| `catalog/09-tooling/0069-terrakube/policy.md` | `POL-0069` | policy | 09-tooling / 0069-terrakube | active | AD-0009 | 3 / 2 | none found | `policies/0069-terrakube.md` | move | V1 |
| `catalog/09-tooling/0069-terrakube/runbook.md` | `RUN-0069` | runbook | 09-tooling / 0069-terrakube | active | GDE-0069 | 5 / 2 | none found | `runbooks/0069-terrakube.md` | move | V1 |
| `catalog/09-tooling/0082-opentofu/guide.md` | `GDE-0082` | guide | 09-tooling / 0082-opentofu | draft | POL-0082 | 9 / 2 | none found | `guides/0082-opentofu.md` | move | V1 |
| `catalog/09-tooling/0082-opentofu/policy.md` | `POL-0082` | policy | 09-tooling / 0082-opentofu | draft | AD-0009 | 2 / 2 | none found | `policies/0082-opentofu.md` | move | V1 |
| `catalog/09-tooling/0082-opentofu/runbook.md` | `RUN-0082` | runbook | 09-tooling / 0082-opentofu | draft | POL-0082 | 6 / 2 | none found | `runbooks/0082-opentofu.md` | move | V1 |
| `catalog/09-tooling/0083-renovate/guide.md` | `GDE-0083` | guide | 09-tooling / 0083-renovate | draft | POL-0083 | 4 / 0 | Guide copied the Runbook live-run sequence; now links it | `guides/0083-renovate.md` | move, edit (W6) | V1 |
| `catalog/09-tooling/0083-renovate/policy.md` | `POL-0083` | policy | 09-tooling / 0083-renovate | draft | AD-0009 | 2 / 2 | Policy held Runbook commands; now links the Runbook | `policies/0083-renovate.md` | move, edit (W6) | V1 |
| `catalog/09-tooling/0083-renovate/runbook.md` | `RUN-0083` | runbook | 09-tooling / 0083-renovate | draft | POL-0083 | 2 / 1 | none found | `runbooks/0083-renovate.md` | move | V1 |
| `catalog/09-tooling/0090-dbt/guide.md` | `GDE-0090` | guide | 09-tooling / 0090-dbt | active | POL-0090 | 3 / 2 | none found | `guides/0090-dbt.md` | move | V1 |
| `catalog/09-tooling/0090-dbt/policy.md` | `POL-0090` | policy | 09-tooling / 0090-dbt | active | AD-0009 | 3 / 2 | none found | `policies/0090-dbt.md` | move | V1 |
| `catalog/09-tooling/0090-dbt/runbook.md` | `RUN-0090` | runbook | 09-tooling / 0090-dbt | active | GDE-0090 | 3 / 2 | none found | `runbooks/0090-dbt.md` | move | V1 |
| `catalog/09-tooling/0092-wiremock/guide.md` | `GDE-0092` | guide | 09-tooling / 0092-wiremock | active | POL-0092 | 4 / 2 | none found | `guides/0092-wiremock.md` | move | V1 |
| `catalog/09-tooling/0092-wiremock/policy.md` | `POL-0092` | policy | 09-tooling / 0092-wiremock | active | AD-0009 | 3 / 2 | none found | `policies/0092-wiremock.md` | move | V1 |
| `catalog/09-tooling/0092-wiremock/runbook.md` | `RUN-0092` | runbook | 09-tooling / 0092-wiremock | active | GDE-0092 | 3 / 2 | none found | `runbooks/0092-wiremock.md` | move | V1 |
| `catalog/09-tooling/0093-pact-broker/guide.md` | `GDE-0093` | guide | 09-tooling / 0093-pact-broker | active | POL-0093 | 3 / 2 | none found | `guides/0093-pact-broker.md` | move | V1 |
| `catalog/09-tooling/0093-pact-broker/policy.md` | `POL-0093` | policy | 09-tooling / 0093-pact-broker | active | AD-0009 | 3 / 2 | none found | `policies/0093-pact-broker.md` | move | V1 |
| `catalog/09-tooling/0093-pact-broker/runbook.md` | `RUN-0093` | runbook | 09-tooling / 0093-pact-broker | active | GDE-0093 | 3 / 2 | none found | `runbooks/0093-pact-broker.md` | move | V1 |
| `catalog/09-tooling/0095-conftest/guide.md` | `GDE-0095` | guide | 09-tooling / 0095-conftest | draft | POL-0095 | 3 / 2 | none found | `guides/0095-conftest.md` | move | V1 |
| `catalog/09-tooling/0095-conftest/policy.md` | `POL-0095` | policy | 09-tooling / 0095-conftest | draft | AD-0009 | 3 / 5 | none found | `policies/0095-conftest.md` | move | V1 |
| `catalog/09-tooling/0095-conftest/runbook.md` | `RUN-0095` | runbook | 09-tooling / 0095-conftest | draft | GDE-0095 | 3 / 2 | none found | `runbooks/0095-conftest.md` | move | V1 |
| `catalog/10-communication/0070-mail/guide.md` | `GDE-0070` | guide | 10-communication / 0070-mail | active | POL-0070 | 4 / 4 | none found | `guides/0070-mail.md` | move | V1 |
| `catalog/10-communication/0070-mail/policy.md` | `POL-0070` | policy | 10-communication / 0070-mail | active | AD-0010 | 2 / 4 | none found | `policies/0070-mail.md` | move | V1 |
| `catalog/10-communication/0070-mail/runbook.md` | `RUN-0070` | runbook | 10-communication / 0070-mail | active | GDE-0070 | 3 / 4 | none found | `runbooks/0070-mail.md` | move | V1 |
| `catalog/10-communication/0084-mailpit/guide.md` | `GDE-0084` | guide | 10-communication / 0084-mailpit | draft | POL-0084 | 3 / 4 | none found | `guides/0084-mailpit.md` | move | V1 |
| `catalog/10-communication/0084-mailpit/policy.md` | `POL-0084` | policy | 10-communication / 0084-mailpit | draft | AD-0010 | 2 / 3 | none found | `policies/0084-mailpit.md` | move | V1 |
| `catalog/10-communication/0084-mailpit/runbook.md` | `RUN-0084` | runbook | 10-communication / 0084-mailpit | draft | POL-0084 | 2 / 3 | none found | `runbooks/0084-mailpit.md` | move | V1 |
| `catalog/11-laboratory/0072-dozzle/guide.md` | `GDE-0072` | guide | 11-laboratory / 0072-dozzle | active | POL-0072 | 5 / 2 | none found | `guides/0072-dozzle.md` | move | V1 |
| `catalog/11-laboratory/0072-dozzle/policy.md` | `POL-0072` | policy | 11-laboratory / 0072-dozzle | active | AD-0011 | 3 / 2 | none found | `policies/0072-dozzle.md` | move | V1 |
| `catalog/11-laboratory/0072-dozzle/runbook.md` | `RUN-0072` | runbook | 11-laboratory / 0072-dozzle | active | GDE-0072 | 4 / 2 | none found | `runbooks/0072-dozzle.md` | move | V1 |
| `catalog/11-laboratory/0073-open-notebook/guide.md` | `GDE-0073` | guide | 11-laboratory / 0073-open-notebook | active | POL-0073 | 5 / 2 | none found | `guides/0073-open-notebook.md` | move | V1 |
| `catalog/11-laboratory/0073-open-notebook/policy.md` | `POL-0073` | policy | 11-laboratory / 0073-open-notebook | active | AD-0011 | 3 / 3 | none found | `policies/0073-open-notebook.md` | move | V1 |
| `catalog/11-laboratory/0073-open-notebook/runbook.md` | `RUN-0073` | runbook | 11-laboratory / 0073-open-notebook | active | GDE-0073 | 3 / 2 | none found | `runbooks/0073-open-notebook.md` | move | V1 |
| `catalog/11-laboratory/0074-optimization-hardening/guide.md` | `GDE-0074` | guide | 11-laboratory / 0074-optimization-hardening | active | POL-0074 | 2 / 2 | generic slug qualified by domain | `guides/0074-laboratory-optimization-hardening.md` | move | V1 |
| `catalog/11-laboratory/0074-optimization-hardening/policy.md` | `POL-0074` | policy | 11-laboratory / 0074-optimization-hardening | active | AD-0011 | 2 / 2 | generic slug qualified by domain; invented `Agents` scope line removed | `policies/0074-laboratory-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/11-laboratory/0074-optimization-hardening/runbook.md` | `RUN-0074` | runbook | 11-laboratory / 0074-optimization-hardening | active | GDE-0074 | 2 / 2 | generic slug qualified by domain; boilerplate N/A recovery line removed; generic Agent Operations filler removed | `runbooks/0074-laboratory-optimization-hardening.md` | move, edit (W6) | V1 |
| `catalog/11-laboratory/0076-redisinsight/guide.md` | `GDE-0076` | guide | 11-laboratory / 0076-redisinsight | active | POL-0076 | 5 / 2 | none found | `guides/0076-redisinsight.md` | move | V1 |
| `catalog/11-laboratory/0076-redisinsight/policy.md` | `POL-0076` | policy | 11-laboratory / 0076-redisinsight | active | AD-0011 | 3 / 2 | none found | `policies/0076-redisinsight.md` | move | V1 |
| `catalog/11-laboratory/0076-redisinsight/runbook.md` | `RUN-0076` | runbook | 11-laboratory / 0076-redisinsight | active | GDE-0076 | 4 / 2 | none found | `runbooks/0076-redisinsight.md` | move | V1 |
| `catalog/11-laboratory/0080-surrealdb/guide.md` | `GDE-0080` | guide | 11-laboratory / 0080-surrealdb | draft | POL-0080 | 4 / 1 | none found | `guides/0080-surrealdb.md` | move | V1 |
| `catalog/11-laboratory/0080-surrealdb/policy.md` | `POL-0080` | policy | 11-laboratory / 0080-surrealdb | draft | AD-0011 | 3 / 2 | none found | `policies/0080-surrealdb.md` | move | V1 |
| `catalog/11-laboratory/0080-surrealdb/runbook.md` | `RUN-0080` | runbook | 11-laboratory / 0080-surrealdb | draft | POL-0080 | 3 / 0 | none found | `runbooks/0080-surrealdb.md` | move | V1 |
| `catalog/11-laboratory/0088-mlflow/guide.md` | `GDE-0088` | guide | 11-laboratory / 0088-mlflow | active | POL-0088 | 4 / 3 | none found | `guides/0088-mlflow.md` | move | V1 |
| `catalog/11-laboratory/0088-mlflow/policy.md` | `POL-0088` | policy | 11-laboratory / 0088-mlflow | active | AD-0011 | 3 / 3 | none found | `policies/0088-mlflow.md` | move | V1 |
| `catalog/11-laboratory/0088-mlflow/runbook.md` | `RUN-0088` | runbook | 11-laboratory / 0088-mlflow | active | GDE-0088 | 4 / 5 | none found | `runbooks/0088-mlflow.md` | move | V1 |
| `catalog/11-laboratory/0089-jupyterlab/guide.md` | `GDE-0089` | guide | 11-laboratory / 0089-jupyterlab | active | POL-0089 | 3 / 3 | none found | `guides/0089-jupyterlab.md` | move | V1 |
| `catalog/11-laboratory/0089-jupyterlab/policy.md` | `POL-0089` | policy | 11-laboratory / 0089-jupyterlab | active | AD-0011 | 3 / 2 | none found | `policies/0089-jupyterlab.md` | move | V1 |
| `catalog/11-laboratory/0089-jupyterlab/runbook.md` | `RUN-0089` | runbook | 11-laboratory / 0089-jupyterlab | active | GDE-0089 | 3 / 5 | none found | `runbooks/0089-jupyterlab.md` | move | V1 |
| `catalog/12-infra-net/0077-ip-address-management/guide.md` | `GDE-0077` | guide | 12-infra-net / 0077-ip-address-management | active | POL-0077 | 2 / 4 | none found | `guides/0077-ip-address-management.md` | move | V1 |
| `catalog/12-infra-net/0077-ip-address-management/policy.md` | `POL-0077` | policy | 12-infra-net / 0077-ip-address-management | active | AD-0026 | 2 / 2 | invented `Agents` scope line removed | `policies/0077-ip-address-management.md` | move, edit (W6) | V1 |
| `catalog/12-infra-net/0077-ip-address-management/runbook.md` | `RUN-0077` | runbook | 12-infra-net / 0077-ip-address-management | active | GDE-0077 | 2 / 2 | generic Agent Operations filler removed | `runbooks/0077-ip-address-management.md` | move, edit (W6) | V1 |
| `catalog/12-infra-net/0096-k8s-integration/guide.md` | `GDE-0096` | guide | 12-infra-net / 0096-k8s-integration | draft | POL-0096 | 1 / 2 | none found | `guides/0096-k8s-integration.md` | move | V1 |
| `catalog/12-infra-net/0096-k8s-integration/policy.md` | `POL-0096` | policy | 12-infra-net / 0096-k8s-integration | draft | AD-0026 | 1 / 2 | none found | `policies/0096-k8s-integration.md` | move | V1 |
| `catalog/12-infra-net/0096-k8s-integration/runbook.md` | `RUN-0096` | runbook | 12-infra-net / 0096-k8s-integration | draft | GDE-0096 | 5 / 3 | none found | `runbooks/0096-k8s-integration.md` | move | V1 |
| `catalog/00-workspace/README.md` | — | domain index | 00-workspace | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/01-gateway/README.md` | — | domain index | 01-gateway | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/02-auth/README.md` | — | domain index | 02-auth | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/03-security/README.md` | — | domain index | 03-security | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/04-data/README.md` | — | domain index | 04-data | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/05-messaging/README.md` | — | domain index | 05-messaging | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/06-observability/README.md` | — | domain index | 06-observability | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/07-workflow/README.md` | — | domain index | 07-workflow | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/08-ai/README.md` | — | domain index | 08-ai | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/09-tooling/README.md` | — | domain index | 09-tooling | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/10-communication/README.md` | — | domain index | 10-communication | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/11-laboratory/README.md` | — | domain index | 11-laboratory | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/12-infra-net/README.md` | — | domain index | 12-infra-net | active | — | index | parallel navigation removed by ADR-0043 | role indexes | merge, then delete | V2 |
| `catalog/README.md` | — | catalog index | — | active | — | index | parallel navigation removed by ADR-0043 | `README.md` | merge, then delete | V2 |
| `README.md` | — | Stage 05 index | — | active | — | stage router | routed to the catalog | `README.md` | edit | V2 |
| `incidents/README.md` | — | incident index | — | active | — | index | dated 2026-05-28 absence note while inc-2026-0002 exists | `incidents/README.md` | edit | V2 |
| `incidents/2026/inc-0002-airflow-keycloak-native-auth/incident.md` | `inc-2026-0002` | incident | 07-workflow / Airflow | mitigated | RUN-0050 | RUN-0050 link rewrite only | no postmortem; resolution not evidenced | unchanged | keep | V3 |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W4 | met: Registry tests pass in the full gate; no `operations-domain-readme` or `subject-member` remains outside rejection tests | Stage 99 Registry |
| 2 | W4 | met: 225 moves, identifiers unchanged; catalog tree and 14 READMEs deleted | Stage 05 role directories |
| 3 | W4 | met: the operations check reports no index membership finding for the three indexes | Stage 05 README and role indexes |
| 4 | W3, W4 | met: RED 69 of 86 on the catalog validator; `check-operations-catalog.py` PASS | `scripts/lib/document_governance/operations_catalog.py` |
| 5 | W4, W6 | met: `check-document-links.py --mode all` PASS; remaining mentions classified in Rulings | Stage 05 and active consumers |
| 6 | W5 | met: commits `372bbcf62` and `6ea2d9bc6` | `scripts/README.md`, incidents README |
| 7 | W7 | met: commit `6f4efaedd` | MIG-0005 |
| 8 | W8 | met with a recorded exception; see Gate Results | this Task |

### Gate Results

Each commit was checked in a scratch worktree staged against the baseline
(`reset --soft 0deb430ea`), as a pull request would be: metadata
`--mode check-changed` with `TEMPLATE_GATE_BASE` set to the baseline, the
operations check, `check-document-links.py --mode all`, and
`run-ci-gate.py --profile changed`.

| Commit | Metadata selected / exit | Operations | Links | Changed gate |
| --- | --- | --- | --- | --- |
| `572616b48` | 6 / 0 | 0 | 0 | 1: identity high-water only |
| `887a19f76` | 6 / 0 | 0 | 0 | 1: identity high-water only |
| `0a2e9cf16` | 344 / 0 | 0 | 0 | 1: identity high-water only |
| `9591a6e03` | 345 / 0 | 0 | 0 | 1: identity high-water only |
| `b6b038d04` | 345 / 0 | 0 | 0 | 1: identity high-water only |
| `8ade3f32f` | 345 / 0 | 0 | 0 | 1: identity high-water only |
| `d01b7f441` | 345 / 0 | 0 | 0 | 1: identity high-water only |
| `3c97d57ae` | 346 / 0 | 0 | 0 | 1: two executable-mode tests only; 0 after scratch `chmod g-w` |
| `1a89f8af4` | 347 / 0 | 0 | 0 | 0 |
| `464b3c509` | 347 / 0 | 0 | 0 | 0 |

The one failure before `3c97d57ae` is
`test_registry_high_water_is_not_below_repository_history`
(`identity_spaces.migration high_water=4 observed=5`). The test scans
`--all` refs, so it sees MIG-0005 from the later commit on the same branch.
It is an isolation artifact of checking an older commit while a newer ref
exists, not a defect in that commit, and it cannot occur on the branch tip.
From `3c97d57ae` on the test passes. At `3c97d57ae` the changed gate first
selected the two executable-mode tests described below and failed them for
the same scratch-worktree reason; with `chmod g-w` applied in the scratch
worktree only, both modules passed at that commit (`Ran 19 tests`, `OK`).

Full gate: `run-ci-gate.py --profile full` on `464b3c509` exited 1 on its
first run with two executable-mode tests
(`infra/06-observability/gatus/docker-entrypoint.sh`,
`infra/08-ai/open-webui/docker-entrypoint.sh`): the scratch worktree was
checked out under umask 002, making both group-writable, while the branch
diff for both files is empty and the main checkout holds them without group
write. After `chmod g-w` in the scratch worktree only, the rerun exited 0:
16 suites, 1500 tests, 23 skipped, 23 min 26 s. Static and local results
only; no remote CI ran and nothing was pushed.

## Review Evidence

A read-only review of the branch diff found active surfaces that still named
the retired catalog (`git-workflow`, `github-governance`, the stage authoring
matrix, the repository map, the `ops-runbook-agent` skill, and
`examples/README.md`); dead catalog code in `metadata/profile.py` and the
unused `_has_symlink_component` in `operations_catalog.py`; sibling binding
that depended on set iteration order; a missing sibling reported at an
invented file path; and a move baseline that accepted a reused identifier
under any slug. Commit `819938777` corrects each one, restricts the baseline
to the kept or domain-prefixed slug, and adds Registry tests for it.
The review is an agent review, not an owner approval.

## Commit Ledger

Branch `refactor/operations-role-layout`, first built on `0deb430ea` and then
rebased, with owner approval, onto `origin/main` at `af61cab27` (#281). Rename
detection carried #281's edits to the retired `catalog/` paths of RUN-0021 and
RUN-0088 onto `runbooks/0021-backup-and-restore.md` and
`runbooks/0088-mlflow.md` without conflict. The per-commit Gate Results name
the commits as they were before the rebase.

| Commit | Before rebase | Work unit | Subject |
| --- | --- | --- | --- |
| `7c1666f61` | `572616b48` | W2 | docs(specs): Add SPEC-0183 and ADR-0043 for operations role layout |
| `372bbcf62` | `887a19f76` | W5 | docs(scripts): Drop the missing LLM Wiki generator from the scripts README |
| `ae3d21af7` | `0a2e9cf16` | W3, W4 | refactor(docs): Move Stage 05 operations from catalog to role directories |
| `6ea2d9bc6` | `9591a6e03` | W5 | docs(operations): List the current incident in the incidents README |
| `f2983b9c4` | `b6b038d04` | W6 | docs(operations): Keep each Operations role to the content it owns |
| `9ae25732a` | `8ade3f32f` | W8 | refactor(governance): Remove the subject-member identity relation |
| `db4f9a22b` | `d01b7f441` | W6 | chore(scripts): Declare the proven consumers of five manifest rows |
| `6f4efaedd` | `3c97d57ae` | W7 | docs(archive): Record the operations role layout route as MIG-0005 |
| `819938777` | `1a89f8af4` | W8 | fix(governance): Address the SPEC-0183 review findings |
| `b26460e1e` | `464b3c509` | W6 | docs(task): Record the SPEC-0183 W6 dispositions in the ledger |
| `78c242d82` | `48f4ef93c` | W8 | docs(task): Record the SPEC-0183 verification evidence |
| `7a6d2705c` | `f87ed3de8` | W9 | docs(operations): Route the remaining mixed content to its owning role |
| `85668437d` | `0bc87bd9c` | W10 | chore(scripts): Correct manifest labels, authorities, and generated outputs |
| `bf7b6df7b` | `90cb54611` | W10 | fix(hooks): Make post-tool validation check-only unless --write is given |
| `ba8837376` | `cacd80ce2` | W10 | fix(scripts): Make the tech-stack sync check-only unless --write is given |
| `01cb27f3a` | `179e8212e` | W10 | fix(scripts): Recognize three launcher shapes as manifest consumer evidence |
| `d935608d8` | `e99f06223` | W10 | docs(task): Record the SPEC-0183 W9 and W10 owner follow-ups |
| `157b32887` | — | W10 | docs(task): Record the SPEC-0183 rebase onto #281 in the ledger |
| `286eb2885` | — | W11 | test(governance): Supply the generated-body owner inside the heading test |
| `fea69d8a3` | — | W11 | docs(operations): Drop filler Agent Operations subsections from 18 Runbooks |

## Rulings

- Stage 98 frozen bodies, sealed Tombstones, Migrations MIG-0001 to MIG-0004,
  and the Retention Catalog rows keep the catalog paths they record.
- Stage 90 evidence keeps catalog paths in its dated observations; only its
  link targets follow the move.
- `metadata/reference.py` keeps its write path: it writes only with an
  explicit `--output PATH` and prints to standard output otherwise.
- `metadata_validator.py` is retained: `check-document-metadata.py` and
  `metadata_contract.py` import it, and a registered suite tests it.
- The manifest roots stay `evals/` and `scripts/`. `.claude/hooks` files are
  renderer outputs checked for drift by `provider_surface_renderer.py`, and
  the two `.agents/skills/*/scripts` files are owned by their `SKILL.md`.
- `inc-2026-0002` stays `mitigated`: no resolution evidence exists in the
  repository, so no postmortem is written and no closure is recorded.

## Deferred Items

Each item needs an owner decision, another workspace, or access this session
did not have.

- `GDE-0079` keeps its dated `Result` column. Moving results into the SPEC-0182
  Task 0003 would edit an in-progress SPEC-0182 Task that this package does
  not own.
- The `POL-0006` backlog stays in place because
  `links.py` validates its Operations and Runbook link pairs; moving it needs a
  validator change and an owner for backlogs.
- Renovate reads `renovate.json` before `renovate.json5`, and the contract test
  reads only `renovate.json5`. Both were updated; the duplicate needs an owner.
- After merge, the host checkout must be updated so the mounted Renovate
  `config.js` allowlist accepts `--write`; until then Renovate artifact updates
  fail closed.
- `inc-2026-0002` stays `mitigated`. Resolution needs an authenticated
  request to Pool, DAG, Asset, and HITL; the read-only check found healthy
  containers and provider 0.9.0 but no authenticated access record.
- Host systemd units and the running Prometheus keep the old
  `Documentation=` and `runbook_url` values until the units are reinstalled
  and Prometheus is reloaded. Neither was done; both need approval.
- Other repositories: `hy-home.k8s` at `698745e6` names no catalog route (its
  11 uncommitted files were not read). `hy-home.secrets` could not be read
  (permission denied), so its links are unverified. MIG-0005 is the route
  record for both owners.
