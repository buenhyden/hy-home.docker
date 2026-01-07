# OpenSearch

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 대규모 데이터 검색 및 로그 분석을 위한 분산 검색 엔진입니다. Elasticsearch의 오픈소스 포크로 시작되었으며, 강력한 전문 검색(Full-text Search), 데이터 분석, 보안 모니터링 기능을 제공합니다.

## 2. 주요 기능 (Key Features)
- **High-Performance Search**: 역인덱스(Inverted Index) 기반의 빠른 텍스트 검색 및 집계.
- **Log Analytics**: 로그 데이터를 실시간으로 수집, 저장, 분석하여 시각화.
- **Security**: RBAC(Role-Based Access Control), TLS 암호화 등 엔터프라이즈급 보안 기능 내장.
- **Visualizations**: OpenSearch Dashboards를 통해 데이터를 차트와 그래프로 시각화.

## 3. 기술 스택 (Tech Stack)
- **Engine**: OpenSearch 3.3.2
- **UI**: OpenSearch Dashboards 3.3.0
- **Monitoring**: Prometheus Elasticsearch Exporter v1.7.0

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 클러스터 구성
- **Node 1 (`opensearch-node1`)**: 현재 단일 노드로 동작하며 Cluster Manager, Data, Ingest 역할을 모두 수행합니다.
- **Scalability**: 설정상 3개 노드(`node2`, `node3`)까지 확장 가능하도록 준비되어 있으나, 리소스 절약을 위해 주석 처리되어 있습니다.

### 데이터 흐름
1.  **Client/App** -> **Traefik (HTTPS)** -> **OpenSearch API (9200)**
2.  **User** -> **Traefik (HTTPS)** -> **Dashboards (5601)** -> **OpenSearch API**

## 5. 시작 가이드 (Getting Started)
**사전 요구사항**:
- 호스트 시스템의 `vm.max_map_count` 설정이 최소 `262144` 이상이어야 합니다.
  ```bash
  # Linux/WSL2
  sysctl -w vm.max_map_count=262144
  ```

**실행 방법**:
```bash
docker compose up -d
```

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 OpenSearch Dashboards
- **접속**: `https://opensearch-dashboard.${DEFAULT_URL}`
- **로그인**: `admin` / `${OPENSEARCH_INITIAL_ADMIN_PASSWORD}` (기본값 확인 필요).
- **기능**: 인덱스 패턴 생성, Discover(로그 탐색), Visualize(차트 생성), Dashboard(모음) 등.

### 6.2 API 활용
- **인덱스 확인**:
  ```bash
  curl -k -u admin:<password> https://opensearch.${DEFAULT_URL}/_cat/indices?v
  ```
- **상태 확인**:
  ```bash
  curl -k -u admin:<password> https://opensearch.${DEFAULT_URL}/_cluster/health?pretty
  ```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `OPENSEARCH_INITIAL_ADMIN_PASSWORD`: 초기 관리자 비밀번호 (반드시 복잡하게 설정).
- `OPENSEARCH_JAVA_OPTS`: JVM 힙 메모리 크기 (기본 `-Xms1g -Xmx1g`).
- `discovery.type`: `single-node` (단일 노드 실행 시).

### 네트워크 포트 (Ports)
- **API**: 9200 (외부 노출됨).
- **Performance Analyzer**: 9600.
- **Dashboards**: 5601.

### 볼륨 마운트 (Volumes)
- `opensearch-data1`: `/usr/share/opensearch/data` (데이터 영속화).
- `./certs`: TLS 인증서 경로.

## 8. 통합 및 API 가이드 (Integration Guide)
**Fluent Bit / Logstash 연동**:
- **Output Plugin**: `opensearch`
- **Host**: `opensearch.${DEFAULT_URL}`
- **Port**: `443`
- **TLS**: `On` (인증서 검증 `Off` 또는 CA 등록 필요).
- **HTTP User/Password**: `admin` 계정 사용.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- 노드 상태: `GET /` (Welcome 메시지).
- 클러스터 상태: `GET /_cluster/health`.

**Monitoring**:
- `opensearch-exporter` 컨테이너가 9114 포트에서 Prometheus 메트릭을 제공합니다 (`/metrics`).

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**스냅샷(Snapshot)**:
- 운영 환경에서는 주기적으로 인덱스 스냅샷을 생성하여 S3 등 외부 저장소에 백업해야 합니다.
- `opensearch-data` 볼륨 백업도 가능하지만, 서비스 중단 없이 백업하려면 스냅샷 API를 권장합니다.

## 11. 보안 및 강화 (Security Hardening)
- **TLS Encryption**: 노드 간 통신 및 클라이언트 통신 모두 HTTPS가 강제됩니다.
- **Admin Password**: 초기 설정 후 즉시 비밀번호를 변경하십시오.
- **Anonymous Access**: 비활성화되어 있습니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Exited with code 78**: `vm.max_map_count` 부족 오류. 호스트 설정을 확인하세요.
- **Connection Refused (Dashboards)**: OpenSearch 노드가 완전히 부팅될 때까지(약 1~2분 소요) 대시보드 접속이 안 될 수 있습니다.

---
**공식 문서**: [https://opensearch.org/docs/latest/](https://opensearch.org/docs/latest/)
