# Valkey Distributed Cluster

> 고성능, 6노드 분산 캐시 클러스터 (Redis 호환 가능)

## Overview

`valkey-cluster`는 `hy-home.docker` 에코시스템을 위한 고처리량, 저지연 캐싱 및 상태 저장소 계층을 제공합니다. 3개의 프라이머리 노드와 3개의 복제본(Replica) 노드로 구성되어 자동 파티셔닝과 고가용성을 보장하도록 설계되었습니다.

## Audience

이 README의 주요 독자:

- 인프라를 배포하고 관리하는 **Operators**
- 클러스터와 연결되는 서비스를 개발하는 **Developers**
- 자동화된 운영 작업을 수행하는 **AI Agents**

## Scope

### In Scope

- 6노드 Valkey 클러스터 구성 및 관리
- Docker Compose 기반 배포 및 헬스체크
- 클러스터 초기화 및 상태 검증 스크립트

### Out of Scope

- 클러스터 외부의 개별 Valkey 인스턴스 (`mng-valkey`)
- 애플리케이션 레벨의 데이터 모델링 설계
- 다중 리전 복제 및 재해 복구 구성

## Structure

```text
valkey-cluster/
├── config/
│   └── valkey.conf          # 공통 Valkey 설정
├── scripts/
│   ├── valkey-start.sh      # 노드 시작 스크립트
│   └── valkey-cluster-init.sh # 클러스터 구성 스크립트
├── docker-compose.yml       # 클러스터 오케스트레이션
└── README.md                # 이 파일
```

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | 클러스터 전체 노드 시작 |
| `docker compose ps` | 노드별 상태 및 헬스체크 확인 |
| `docker compose logs -f` | 실시간 로그 모니터링 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `DEFAULT_DATA_DIR` | Yes | 데이터 저장 기본 경로 |
| `VALKEYn_PORT` | No | 각 노드별 포트 (기본: 6379-6384) |

### Secrets

| Secret | Description |
| :--- | :--- |
| `service_valkey_password` | 클러스터 인증에 사용되는 마스터 패스워드 |

## Testing & Verification

1. **상태 확인**: `docker exec valkey-node-0 valkey-cli -a $PASS cluster info`
2. **노드 확인**: `docker exec valkey-node-0 valkey-cli -a $PASS cluster nodes`
3. **슬롯 확인**: `docker exec valkey-node-0 valkey-cli -a $PASS cluster slots`

## Related References

- **Guide**: [valkey-cluster.md](../../07.guides/04-data/valkey-cluster.md)
- **Operation**: [valkey-cluster.md](../../08.operations/04-data/valkey-cluster.md)
- **Runbook**: [valkey-cluster.md](../../09.runbooks/04-data/valkey-cluster.md)

---
Copyright (c) 2026. Licensed under the MIT License.
