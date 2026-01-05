# Kafka Platform

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 고성능 분산 이벤트 스트리밍 플랫폼입니다. 실시간 데이터 파이프라인 구축 및 스트림 프로세싱을 위해 사용됩니다.

**주요 기능 (Key Features)**:
- **KRaft Mode**: Zookeeper 의존성을 제거하고 자체 쿼럼 컨트롤러 사용.
- **Schema Registry**: AVRO 등 스키마 검증 및 관리.
- **Kafka Connect**: 외부 시스템(DB, S3 등)과 데이터 연동 자동화.
- **Kafka UI**: 클러스터 상태 모니터링 및 토픽 데이터 조회.

**기술 스택 (Tech Stack)**:
- **Broker**: Confluent Kafka 7.7.7 (KRaft)
- **UI**: Provectus Kafka UI

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**시스템 구조도**:
- 3개의 브로커 노드(`kafka-1`, `2`, `3`)가 Controller와 Broker 역할을 겸임.
- REST Proxy와 Connect는 내부 프로토콜(19092)로 브로커와 통신.

## 3. 시작 가이드 (Getting Started)
**실행 방법 (Deployment)**:
```bash
docker compose up -d
```
(브로커 3개가 쿼럼을 형성해야 정상 동작하므로 초기 기동 시 시간이 소요될 수 있습니다.)

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수 (Environment Variables)**:
- `KAFKA_CLUSTER_ID`: 고유 클러스터 식별자.
- `KAFKA_NODE_ID`: 각 브로커의 번호 (1, 2, 3).
- `KAFKA_CONTROLLER_QUORUM_VOTERS`: 투표권이 있는 노드 목록.

**네트워크 포트 (Network Ports)**:
- **External**: 각 노드별 포트 매핑 (브로커 직접 접속 시 필요).
- **Internal**: 19092 (PLAINTEXT), 9093 (CONTROLLER).
- **UI**: `https://kafka-ui.${DEFAULT_URL}`

## 5. 통합 및 API 가이드 (Integration Guide)
**엔드포인트 명세**:
- **Bootstrap Servers**: `kafka-1:19092,kafka-2:19092,kafka-3:19092` (내부)
- **Schema Registry**: `http://schema-registry:8081`

**클라이언트 설정**:
- 내부 서비스에서 접속 시 보안 프로토콜 `PLAINTEXT` 사용.

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인 (Health Check)**:
- `kafka-broker-api-versions` 명령어로 연결 테스트.

**모니터링 (Monitoring)**:
- `kafka-exporter` 사이드카를 통해 Prometheus 메트릭 노출.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- 각 브로커의 `/var/lib/kafka/data` 볼륨이 중요합니다.
- 토픽 단위 DR(Disaster Recovery) 구성을 위해 MirrorMaker 사용 권장.

## 8. 보안 및 강화 (Security Hardening)
- 현재 내부 통신은 `PLAINTEXT`이므로 신뢰할 수 있는 네트워크(`infra_net`) 내에서만 접근해야 합니다.

## 9. 트러블슈팅 (Troubleshooting)
**진단 명령어**:
```bash
# 토픽 리스트 확인
docker exec -it kafka-1 kafka-topics --bootstrap-server localhost:19092 --list
```
