---
title: "MinIO Object Storage Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0023"
parent_ids:
- "POL-0023"
implementation_services:
  infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml:
  - 'minio1'
  - 'minio2'
  - 'minio3'
  - 'minio4'
  infra/04-data/lake-and-object/minio/docker-compose.yml:
  - 'minio'
  - 'minio-create-buckets'
created: "2026-05-10"
---

# MinIO Object Storage Usage Guide

## Usage

MinIO is retained as the HOME S3-compatible store because the root bootstrap
creates `loki-bucket`, `tempo-bucket`, `cdn-bucket`, and `doc-intel-assets`, and
current Loki/Tempo configuration names its endpoint. The four-node
`storage-cluster` topology is LAB on one host. SeaweedFS is OPTIONAL and is not an
automatic replacement.

The upstream community repository was archived and made read-only on 2026-04-25;
its README says the community server is no longer maintained and distributed as
source. Preserve the current data while a separate migration evaluation measures
S3/client compatibility. AIStor documentation is not evidence that the retained
community image has the same lifecycle or license terms.

## Current implementation

[`infra/04-data/lake-and-object/minio/docker-compose.yml`](../../../../../infra/04-data/lake-and-object/minio/docker-compose.yml) defines HOME `minio` and one-shot `minio-create-buckets`;
[`docker-compose.cluster.yaml`](../../../../../infra/04-data/lake-and-object/minio/docker-compose.cluster.yaml)
defines only the four LAB members. Profiles `storage`,
`obs`, `logs`, `tracing`, and `nginx` select the single node. The root project also
includes the LAB cluster file; `storage-cluster` selects `minio1` through `minio4`.

The HOME service owns `minio-data` at `${DEFAULT_DATA_DIR}/minio/data-1`. LAB nodes
use separate `data1` through `data4` paths. Root and application identities come
from `minio_root_username`, `minio_root_password`, `minio_app_username`, and
`minio_app_user_password` secrets. `infra_net` carries service traffic; Traefik
routes the API and console through `gateway-standard-chain@file`. Gateway TLS does
not prove service-to-service TLS or storage encryption. The bootstrap grants
public read to `cdn-bucket`; treat that as intentional exposure requiring review.

## Images, configuration and resource controls

The Compose sources are authoritative for the pinned `quay.io/minio/minio` image;
repository Renovate may propose updates and the version projection is derived.
`MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`,
`MINIO_PROMETHEUS_AUTH_TYPE`, and `MINIO_API_ROOT_ACCESS` are the declared service
keys; the bootstrap consumes the root/application secrets through `mc` commands.
HOME MinIO extends `template-stateful-db-med` and its bootstrap
`template-job-low`; both have completion/health controls. S3 clients reach MinIO
through `infra_net` or the gateway, while the bootstrap configures buckets/users
through the internal endpoint.

## Static preflight

From the repository root:

```bash
docker compose --env-file .env.example --profile storage config --quiet
docker compose --env-file .env.example --profile storage config --services
docker compose --env-file .env.example --profile storage-cluster config --quiet
```

Do not render the leaf file alone. Shared secrets, network, labels and templates
are root-owned. Starting services or changing buckets is a separate runtime task.

## Data protection and lifecycle

Use object-aware mirror/replication to a separate encrypted destination. Capture
bucket inventory, versioning/object-lock state, policies and IAM configuration in
addition to objects; never raw-copy active `/data`. [RUN-0023](runbook.md) defines
an isolated restore and application checks for Loki, Tempo and approved object
clients.

Before an image change or replacement, inventory clients and S3 features, export
all objects/configuration, test the candidate with representative workloads, and
prepare cutover and rollback. No migration target is selected by this guide.

## Official references

- [MinIO community repository, status and AGPL license](https://github.com/minio/minio)
- [MinIO client mirror documentation](https://github.com/minio/mc/blob/master/README.md)
- [MinIO bucket replication documentation](https://github.com/minio/minio/blob/master/docs/bucket/replication/README.md)
- [MinIO security checklist](https://docs.min.io/community/minio-object-store/operations/checklists/security.html)

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0023`; governing policy: `POL-0023`.
- Runtime authority: `infra/04-data/lake-and-object/minio/docker-compose.yml`.

## Related Documents

- [Operations policy](policy.md)
- [Health and recovery runbook](runbook.md)
- [Backup policy](../0021-backup-and-restore/policy.md)
