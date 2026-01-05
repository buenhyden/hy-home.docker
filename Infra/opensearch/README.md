# OpenSearch

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: Elasticsearch에서 파생된 분산형 검색 및 분석 엔진입니다. 텍스트 검색, 로그 분석, 보안 모니터링 등에 활용됩니다.

**주요 기능 (Key Features)**:
- **Search Engine**: 강력한 전문 검색 기능.
- **Analytics**: 대시보드(OpenSearch Dashboards)를 통한 데이터 시각화.
- **Security**: 플러그인을 통한 세분화된 보안 제어 (Role, User, SSL).

**기술 스택 (Tech Stack)**:
- **Core**: OpenSearch 3.3.2
- **UI**: OpenSearch Dashboards 3.3.0
- **Exporter**: Prometheus Elasticsearch Exporter

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**구성**:
- **Node 1**: Cluster Manager, Data, Ingest 역할을 모두 수행하는 단일 노드로 구성됨 (설정상 클러스터 확장은 가능하나 현재 노드 2, 3은 비활성화 상태).
- **Communication**: Traefik -> OpenSearch (HTTPS). OpenSearch는 자체 서명 인증서(SSL)를 기본적으로 활성화하고 있습니다.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **주의**: 메모리 설정을 위해 호스트의 `vm.max_map_count`가 262144 이상이어야 합니다.

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `OPENSEARCH_INITIAL_ADMIN_PASSWORD`: 초기 `admin` 계정 비밀번호.
- `OPENSEARCH_JAVA_OPTS`: JVM 힙 크기 설정 (예: `-Xms1g -Xmx1g`).

**네트워크 포트**:
- **API**: 9200 (`https://opensearch.${DEFAULT_URL}`)
- **Dashboard**: 5601 (`https://opensearch-dashboard.${DEFAULT_URL}`)
- **Perf**: 9600 (Performance Analyzer)

## 5. 통합 및 API 가이드 (Integration Guide)
**엔드포인트**:
- Base: `https://opensearch.${DEFAULT_URL}`
- 인증: Basic Auth (`admin` / 설정된 암호) 혹은 Traefik 레벨 인증.

**Dashboards 접속**:
- URL: `https://opensearch-dashboard.${DEFAULT_URL}`

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: `/_cluster/health`
**모니터링**: `opensearch-exporter`가 Prometheus 메트릭을 `9114` 포트로 노출합니다.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- `opensearch-data1` 볼륨에 인덱스 데이터가 저장됩니다.
- 스냅샷 기능을 이용해 S3 또는 로컬 스토리지로 백업을 구성할 수 있습니다.

## 8. 보안 및 강화 (Security Hardening)
- OpenSearch Security Plugin이 활성화되어 있으며, HTTPS 통신을 강제합니다.
- 운영 환경에서는 정식 인증서를 발급받아 교체하는 것을 권장합니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Bootstrap check failed**: `vm.max_map_count` 설정 확인.
- **SSL Handshake Error**: 클라이언트가 자체 서명 인증서를 신뢰하지 않을 때 발생 (`insecure-skip-verify` 옵션 필요).
