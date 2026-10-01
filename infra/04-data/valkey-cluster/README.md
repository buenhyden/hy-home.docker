---
title: "Valkey Distributed Cluster"
version: "1.0.3"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-20"
---

# Valkey Cluster

## Overview

이 패키지는 저장소의 6노드 Valkey cluster를 정의합니다.

## Audience

Valkey LAB 배포의 operator와 maintainer를 대상으로 합니다.

## Scope

Source: [`docker-compose.yml`](docker-compose.yml). Profile: `valkey-cluster`.
Services: `valkey-node-0`부터 `valkey-node-5`까지, one-shot `valkey-cluster-init`,
`valkey-cluster-exporter`. Initializer가 `lab_net`에 3개 primary와 3개 replica를
생성합니다.

## Structure

각 노드는 `valkey0-data`부터 `valkey5-data`까지를 소유합니다. 이들은 각각
`${DEFAULT_DATA_DIR}/valkey/data-0`부터 `data-5`까지로 뒷받침됩니다. Client 포트 6379-6384와
cluster-bus 포트 16379-16384가 게시/노출됩니다. Startup, init, exporter는
`service_valkey_password`를 읽습니다.
[`config/valkey.conf`](config/valkey.conf),
[`scripts/valkey-start.sh`](./scripts/valkey-start.sh),
[`scripts/valkey-cluster-init.sh`](./scripts/valkey-cluster-init.sh)가 설정을
소유합니다. 모든 노드에는 인증된 `PING` 헬스 체크가, exporter에는 HTTP
헬스 체크가 있습니다. init은 one-shot 완료 job입니다. `nodes.conf`는 노드
로컬 identity입니다.

## How to Work in This Area

저장소 루트에서:

```bash
docker compose --env-file .env.example --profile valkey-cluster config --quiet
docker compose --env-file .env.example --profile valkey-cluster config --services
```

이것은 동일 호스트 LAB이며 HOME `mng-valkey`를 대체하지 않습니다. 선택하려면
named cluster-aware client가 필요합니다. TLS가 선언되지 않았으므로 게시된
포트를 의도된 신뢰 경계로 제한하십시오.

백업과 복구는 모든 primary, 완전한 AOF set/manifest, RDB checkpoint, slot
소유권을 조율해야 합니다. fresh identity를 가진 격리된 호환 cluster에서
복구하고 실행 중인 `nodes.conf`를 재사용하지 마십시오.

## Related Documents

[문서 진입점](../../../docs/README.md)에서 Stage 05 subject
`docs/05.operations/guides/0022-valkey-cluster.md`와 POL-0021을 찾으십시오.

공식 소스: [persistence](https://valkey.io/topics/persistence/),
[cluster operations](https://valkey.io/topics/cluster-tutorial/),
[license](https://github.com/valkey-io/valkey/blob/unstable/COPYING).
