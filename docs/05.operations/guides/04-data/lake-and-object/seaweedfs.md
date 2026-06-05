---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md -->

# SeaweedFS Usage Guide

> Use this guide to understand and verify the current SeaweedFS data-profile stack.

---

## Usage

### Overview

SeaweedFS는 `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`에 선언된 distributed file/object storage stack이다. 현재 구현은 `data` profile에서 `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`를 실행하며, all services use `infra_net` and image `chrislusf/seaweedfs:4.31`.

### Usage Type

`system-guide | operational-reference`

### Target Audience

- Operator
- Developer
- SRE
- AI Agent

### Purpose

이 가이드는 SeaweedFS의 현재 service set, exposed internal ports, Traefik routes, mount behavior, 일반 확인 절차를 설명한다. 검증되지 않은 metadata restore나 reshard 절차를 usage guide에 섞지 않도록 한다.

### Prerequisites

- Repository checkout at the project root.
- Docker Compose access on the local or approved infrastructure host.
- Approved runtime volumes for `seaweedfs-master-data` and `seaweedfs-volume-data`.
- Host/runtime approval for `seaweedfs-mount`, which runs privileged with `SYS_ADMIN`.

### Step-by-step Instructions

1. 현재 compose service set을 확인한다.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config --services
   ```

   Expected services: `seaweedfs-master`, `seaweedfs-volume`, `seaweedfs-filer`, `seaweedfs-s3`, `seaweedfs-mount`.

2. 접근 경로를 확인한다.

   - Master UI: `https://seaweedfs.${DEFAULT_URL}` through Traefik
   - Filer/CDN route: `https://cdn.${DEFAULT_URL}` through Traefik
   - S3 route: `https://s3.${DEFAULT_URL}` through Traefik
   - Internal ports: master `9333/19333`, volume `8085/18085`, filer `8888/18888`, S3 `8333`

3. 일반 상태를 확인한다.

   ```bash
   docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data ps seaweedfs-master seaweedfs-volume seaweedfs-filer seaweedfs-s3 seaweedfs-mount
   ```

4. Mount service boundary를 확인한다.

   `seaweedfs-mount` uses the SeaweedFS mount command with `privileged: true` and `SYS_ADMIN`. Treat mount behavior as host-impacting and follow the runbook before restarting it.

### Common Pitfalls

- Referring to old SeaweedFS image versions. The current compose image is `chrislusf/seaweedfs:4.31`.
- Assuming `security.toml` is mounted into the current compose. It exists in the directory but is not mounted by the current service definitions.
- Treating `seaweedfs-mount` as a normal read-only service. It has elevated host-facing privileges.
- Running unverified master metadata restore or reshard commands from documentation without owner approval.

## Common Checks

- `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data config`
- `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml --profile data ps`
- Search paired guide/policy/runbook and infra README for stale image versions, single-container log commands, unmounted config claims, or destructive recovery commands.
- Expected result: compose renders, documented services match the compose file, and mount privilege is explicitly acknowledged.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../../runbooks/04-data/lake-and-object/seaweedfs.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/lake-and-object/seaweedfs.md)
- [Recovery runbook](../../../runbooks/04-data/lake-and-object/seaweedfs.md)
- [Infrastructure service README](../../../../../infra/04-data/lake-and-object/seaweedfs/README.md)
