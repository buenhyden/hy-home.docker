<!-- [ID:04-data:seaweedfs] -->
# SeaweedFS

> Distributed file/object storage with master, volume, filer, S3, and mount services.

## Overview

SeaweedFS provides a distributed file and object storage surface for `hy-home.docker`. The current compose path is `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`, using image `chrislusf/seaweedfs:4.31` and the `data` profile.

## Audience

이 README의 주요 독자:

- Infrastructure Operators
- Developers using filer or S3 interfaces
- SREs
- AI Agents

## Scope

### In Scope

- SeaweedFS master, volume, filer, S3, and mount services
- Traefik routes for master UI, CDN/filer, and S3 gateway
- Runtime volumes and mount privilege boundary
- Links to canonical guide, policy, and runbook

### Out of Scope

- Secret values, private file contents, or credential material
- Runtime activation of `config/security.toml`; it is present but not mounted by the current compose file
- Unapproved metadata restore, volume deletion, forced unmount, or reshard operations

## Structure

```text
seaweedfs/
├── config/              # Security config files present for future/optional use
├── docker-compose.yml   # Current SeaweedFS data-profile stack
└── README.md            # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | SeaweedFS service leaf in `04-data`; services: `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount` |
| Config files | `docker-compose.yml`, `config/security.toml`, `config/security.toml.example` |
| Config values | profile: `data`; image: `chrislusf/seaweedfs:4.31` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml` |
| Networks | `infra_net`; static IPs `172.19.0.140` through `172.19.0.144` |
| Volumes | `seaweedfs-master-data:/data:rw`, `seaweedfs-volume-data:/data:rw` |
| Ports | Master `9333/19333`, volume `8085/18085`, filer `8888/18888`, S3 `8333`; direct host `ports` not declared |
| Labels | `hy-home.tier`, Traefik route `seaweedfs.${DEFAULT_URL}`, Traefik route `cdn.${DEFAULT_URL}`, Traefik route `s3.${DEFAULT_URL}` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`; not declared for `seaweedfs-mount` |
| Privilege boundary | `seaweedfs-mount` runs `privileged: true` with `SYS_ADMIN` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md), [Policy](../../../../docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Review the linked operations guide, policy, and runbook before changing SeaweedFS configuration.
2. Treat `seaweedfs-mount` changes as host-impacting because of `privileged` and `SYS_ADMIN`.
3. Do not claim `security.toml` authentication is active unless the compose file mounts and uses it.
4. After compose, route, or mount changes, run the validation commands listed below.

## Runtime Surface

| Surface | Current Evidence |
| --- | --- |
| Image | `chrislusf/seaweedfs:4.31` |
| Master route | `https://seaweedfs.${DEFAULT_URL}` |
| Filer/CDN route | `https://cdn.${DEFAULT_URL}` |
| S3 route | `https://s3.${DEFAULT_URL}` |
| Mount target | `/mnt/seaweedfs` inside `seaweedfs-mount` command |
| Volume limit | `-volumeSizeLimitMB=1024` on master |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Validate this service with `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config`.
- Verify status with `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data ps seaweedfs-master seaweedfs-volume seaweedfs-filer seaweedfs-s3 seaweedfs-mount`.

## Troubleshooting

- Start with compose render and service status before changing configuration.
- Check individual service logs; there is no single `seaweedfs` container.
- For mount issues, follow the linked runbook and preserve evidence before restarting `seaweedfs-mount`.
- For metadata or volume corruption, stop changes and escalate rather than restoring, deleting, resharding, or force-unmounting from README guidance.

## Related Documents

- **Guide**: [Technical Guide](../../../../docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md)
- **Policy**: [Operations Policy](../../../../docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md)
- **Runbook**: [Recovery Runbook](../../../../docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md)
- **Spec**: [Data Persistence Spec](../../../../docs/03.specs/04-data/spec.md)

---
Copyright (c) 2026. Licensed under the MIT License.
