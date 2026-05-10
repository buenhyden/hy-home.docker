# Qdrant Operations Policy

> Operations policy for Qdrant vector database within the `04-data/specialized` tier.

## Overview (KR)

이 문서는 Qdrant 벡터 데이터베이스의 운영 정책을 정의한다. 인덱싱 설정, 세그먼트 최적화, 스냅샷 주기 및 API 보안 통제 기준을 규정한다.

## Policy Scope

Qdrant 서비스의 자원 효율성, 데이터 무결성 및 검색 품질 유지 정책을 규정한다.

## Applies To

- **Systems**: Qdrant (Containerized)
- **Agents**: AI Engineers, DevOps Operators
- **Environments**: Production (AI/Data Profile)

## Controls

### 1. Persistence and Snapshots

- **Automatic Snapshots**: 정기적인 스냅샷을 생성하여 `/qdrant/storage/snapshots`에 보관한다.
- **Data Dir**: 호스트의 `${DEFAULT_DATA_DIR}/qdrant/data`와 바인드 마운트를 유지한다.

### 2. Performance Optimization

- **Indexing**: 대규모 데이터 삽입 시 인덱싱 쓰레드 및 세그먼트 설정을 점검하여 성능 저하를 방지한다.
- **Resource Extension**: `template-stateful-med` 준수를 원칙으로 하며, 필요시 수직 확장을 고려한다.

### 3. Security Controls

- **API Access**: `QDRANT_API_KEY`를 통한 인증을 필수로 하며, 외부 노출은 Traefik TLS를 통한다.
- **Privilege**: `v1.17-unprivileged` 이미지를 사용하여 컨테이너 권한을 최소화한다.

## Exceptions

- 초기 대량 마이그레이션(Initial Loading) 기간 동안 텔레메트리 일시 중지 또는 리소스 임시 증설이 허용된다.

## Verification

- `/readyz` 엔드포인트를 통한 주기적 Healthcheck.
- 각 컬렉션의 `status`를 조회하여 인덱싱 완료 여부 확인.

## Review Cadence

- 반기별(Bi-annually) 검색 정확도(Recall/Precision) 및 데이터 정합성 검토.

## Related Documents

- **ARD**: `[../../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)`
- **Procedure**: `[../../07.operations/04-data/specialized/qdrant.md](../../../07.operations/04-data/specialized/qdrant.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/04-data/specialized/qdrant.md` during the 2026-05-10 operations taxonomy consolidation.

### Qdrant Vector Database Usage

> Technical guide for understanding and using Qdrant within the `04-data/specialized` tier.

#### Overview (KR)

이 문서는 Qdrant 벡터 데이터베이스에 대한 기술 가이드다. 고차원 벡터 임베딩의 저장 및 검색(Similarity Search)을 위한 아키텍처와 RAG(Retrieval-Augmented Generation) 워크플로 통합 방법을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- AI/ML Engineers
- Backend Developers
- Operators
- AI Agents

#### Purpose

이 가이드는 Qdrant의 컬렉션 관리, 벡터 검색 최적화 및 gRPC/REST API를 통한 서비스 연동을 돕는다.

#### Prerequisites

- Docker 및 Docker Compose 설치
- `ai` 또는 `data` 프로필 활성화
- 벡터 임베딩(Vector Embeddings)에 대한 기본 이해

#### Step-by-step Instructions

##### 1. Connecting to Qdrant

Qdrant는 REST와 gRPC 프로토콜을 모두 지원한다.

- **REST URL**: `https://qdrant.${DEFAULT_URL}`
- **gRPC URL**: `qdrant-grpc.${DEFAULT_URL}:6334`

##### 2. Collection Management (REST)

컬렉션을 생성하여 벡터 데이터를 격리한다.

```bash
curl -X PUT "https://qdrant.${DEFAULT_URL}/collections/my_collection" \
     -H "Content-Type: application/json" \
     --data '{
        "vectors": { "size": 1536, "distance": "Cosine" }
     }'
```

##### 3. Vector Similarity Search

임베딩을 사용하여 유사한 문서를 검색한다.

```bash
curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/points/search" \
     -H "Content-Type: application/json" \
     --data '{
        "vector": [0.1, 0.2, ...],
        "limit": 10
     }'
```

#### Common Pitfalls

- **Payload Size**: 대용량 페이로드 저장 시 메모리 및 디스크 사용량이 급증할 수 있으므로, 필요한 메타데이터만 포함한다.
- **Indexing Latency**: 데이터 대량 삽입 후 Indexing이 완료될 때까지 검색 성능이 저하될 수 있다.

#### Related Documents

- **Spec**: `[infra/04-data/specialized/qdrant/README.md](../../../../infra/04-data/specialized/qdrant/README.md)`
- **Operation**: `[../../07.operations/04-data/specialized/qdrant.md](../../../07.operations/04-data/specialized/qdrant.md)`
- **Procedure**: `[../../07.operations/04-data/specialized/qdrant.md](../../../07.operations/04-data/specialized/qdrant.md)`

## Procedure

> Migrated from `docs/07.operations/04-data/specialized/qdrant.md` during the 2026-05-10 operations taxonomy consolidation.

### Qdrant Recovery Procedure

: Qdrant Vector Database

> Procedure for snapshot management and disaster recovery for Qdrant within the `04-data/specialized` tier.

#### Overview (KR)

이 런북은 Qdrant 데이터베이스의 스냅샷 생성, 복원 및 클러스터 상태 복구 절차를 정의한다. 데이터 손상 또는 유실 시 단계별 조치 지침을 제공한다.

#### Purpose

벡터 컬렉션의 무결성을 유지하고 장애 시 신속한 서비스 복원을 지원한다.

#### Canonical References

- `[../../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)`
- `[../../../07.operations/04-data/specialized/qdrant.md](../../../07.operations/04-data/specialized/qdrant.md)`
- `[infra/04-data/specialized/qdrant/README.md](../../../../infra/04-data/specialized/qdrant/README.md)`

#### When to Use

- 컬렉션 단위의 스냅샷 생성이 필요할 때.
- 특정 시점의 스냅샷으로 데이터를 복원해야 할 때.
- 서비스 응답 지연 또는 `/readyz` 실패 시 조치.

#### Procedure or Checklist

##### 1. Collection Snapshot Execution

실행 중인 상태에서 컬렉션별 스냅샷을 생성한다.

1. 스냅샷 요청:

   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots"
   ```

2. 생성 결과 확인: `/qdrant/storage/snapshots` 디렉토리 내 `.snapshot` 파일 생성 여부 점검.

##### 2. Restoration from Snapshot

1. 컬렉션 삭제 (필요시): `curl -X DELETE "https://qdrant.${DEFAULT_URL}/collections/my_collection"`
2. 스냅샷 복원 요청:

   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots/recover" \
        -H "Content-Type: application/json" \
        --data '{ "location": "file:///qdrant/storage/snapshots/my_collection_snapshot.snapshot" }'
   ```

##### 3. Emergency Health Recovery

1. 로그 확인: `docker compose logs -f qdrant`
2. 데이터 디렉토리 권한 점검: `1000:1000` (Unprivileged user) 소유 확인.
3. 임시 파일 정리: `/tmp` (tmpfs) 용량 확인 및 정리.

#### Verification Steps

- [ ] `curl https://qdrant.${DEFAULT_URL}/readyz` 호출 시 `200 OK` 확인.
- [ ] 컬렉션 인벤토리 확인: `curl https://qdrant.${DEFAULT_URL}/collections`.

#### Observability and Evidence Sources

- **Signals**: Qdrant Telemetry, Traefik Dashboard.
- **Evidence to Capture**: 컬렉션 현황 캡처, 스냅샷 파일 목록.

#### Safe Rollback or Recovery Procedure

- 스냅샷 복원 실패 시, 호스트 레벨의 `${DEFAULT_DATA_DIR}/qdrant/data` 전체 백업 본을 사용하여 볼륨 데이터 전체를 교체한다.

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../../07.operations/README.md)
- [../../10.incidents/README.md](../../../10.incidents/README.md)
