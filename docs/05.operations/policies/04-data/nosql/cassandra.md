---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/nosql/cassandra.md -->

# Cassandra Operations Policy

## Overview (KR)

이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 Cassandra 단일 노드와 `cassandra-exporter` 운영 기준을 정의한다. 기준은 현재 tracked compose의 `cassandra:5.0.8`, `bitnami/cassandra-exporter:2.3.11`, `infra_net`, Docker Secret, `${DEFAULT_DATA_DIR}/cassandra/node1` 볼륨 구성이다.

## Policy Scope

- `infra/04-data/nosql/cassandra/docker-compose.yml`
- `cassandra-node1` service and `cassandra-exporter` service
- `cassandra-node1-volume`, `cassandra-exporter-volume`
- `cassandra_password` Docker Secret and `CASSANDRA_USERNAME` identity variable
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Cassandra documentation must identify the current implementation as a single-node optional include, not as an active multi-node high-availability cluster.
- **Required**: Credential handling must reference `/run/secrets/cassandra_password`; plaintext password variables or copied secret values are disallowed in docs, examples, and evidence.
- **Required**: Volume descriptions must match `${DEFAULT_DATA_DIR}/cassandra/node1` mounted to `/bitnami/cassandra`.
- **Required**: Monitoring references must distinguish the `obs`-profile `cassandra-exporter` from the database node.
- **Allowed**: Local status checks, `nodetool status`, compose rendering, and read-only CQL queries for verification.
- **Allowed**: Documentation-only corrections that keep service names, image tags, profiles, and links aligned with compose.
- **Disallowed**: Unverified multi-node repair, quorum, snapshot restore, or zero-downtime rotation procedures presented as current implementation.
- **Disallowed**: Runtime data mutation, volume replacement, credential rotation, or backup restore from this policy document alone.

## Exceptions

N/A - no currently approved exceptions.

## Verification

- Compare this policy with [Cassandra guide](../../../guides/04-data/nosql/cassandra.md), [Cassandra runbook](../../../runbooks/04-data/nosql/cassandra.md), and [infra README](../../../../../infra/04-data/nosql/cassandra/README.md) after compose changes.
- Run `docker compose -f docker-compose.yml -f infra/04-data/nosql/cassandra/docker-compose.yml --profile data config` before approving service-name, volume, profile, or secret documentation updates.
- Run `bash scripts/validation/check-repo-contracts.sh` and `bash scripts/validation/check-doc-implementation-alignment.sh` after policy or linked operations document updates.

## Review Cadence

- Review on Cassandra compose image/profile/secret/volume changes.
- Review during the Stage 05 operations documentation audit cadence.

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/04-data/nosql/cassandra.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/cassandra.md)
- [Infra README](../../../../../infra/04-data/nosql/cassandra/README.md)
