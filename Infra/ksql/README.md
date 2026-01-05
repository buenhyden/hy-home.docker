# ksqlDB

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: Apache Kafka를 위한 이벤트 스트리밍 데이터베이스입니다. SQL 구문을 사용하여 실시간 스트림 처리를 수행할 수 있습니다.

**주요 기능 (Key Features)**:
- **Stream Processing**: Kafka 토픽 데이터를 테이블처럼 쿼리 및 조인.
- **Push Queries**: 데이터 변경 시 실시간으로 클라이언트에 결과 전송.

**기술 스택 (Tech Stack)**:
- **Image**: `bitnami/ksql:latest`

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
- **Dependency**: Kafka 클러스터에 강하게 의존합니다. `kafka-0` 브로커를 부트스트랩 서버로 참조합니다.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `KSQL_BOOTSTRAP_SERVERS`: Kafka 브로커 주소 (예: `kafka-0:9092`).

**볼륨 마운트**:
- `ksqldb-node-1-data-volume`: 데이터 저장소.

## 5. 통합 및 API 가이드 (Integration Guide)
**클라이언트 접속**:
- ksqlDB CLI 또는 REST API를 통해 쿼리를 제출합니다.

## 6. 가용성 및 관측성 (Availability & Observability)
- 로그(`docker logs ksqldb-node1`)를 통해 연결 상태를 모니터링하십시오.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
- ksqlDB의 상태는 Kafka 토픽(Command Topic)에도 저장되므로, Kafka 데이터가 안전하다면 복구 가능합니다.
- 로컬 볼륨 백업도 권장됩니다.

## 8. 보안 및 강화 (Security Hardening)
- 8088 포트가 기본 HTTP 프로토콜을 사용하므로, 외부 노출 시 보안 설정(Traefik, TLS 등)이 필요합니다.

## 9. 트러블슈팅 (Troubleshooting)
**이슈**: `kafka-0` 호스트를 찾을 수 없음.
**해결**: Kafka 서비스 이름이 `kafka-0`, `kafka-1` 등으로 정확한지, 그리고 동일 네트워크(`infra_net`)에 있는지 확인하십시오.
