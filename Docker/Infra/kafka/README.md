# Apache Kafka (KRaft Mode)

**Apache Kafka**는 고성능 분산 이벤트 스트리밍 플랫폼입니다.
이 구성은 **Zookeeper를 제거한 KRaft(Kafka Raft Metadata) 모드**로 3개의 브로커 클러스터를 구성합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **kafka-1, 2, 3** | Kafka 브로커 및 컨트롤러 (KRaft) | `9092` (Client), `9093` (Controller) |
| **schema-registry** | Avro 등 스키마 관리 | `8081` |
| **kafka-connect** | 데이터 통합 (Source/Sink Connectors) | `8083` |
| **kafka-rest-proxy** | HTTP REST API로 Kafka 접근 | `8082` |
| **kafka-ui** | 웹 기반 관리 UI (Provectus) | `8080` |
| **kafka-exporter** | Prometheus용 메트릭 Exporter | `9308` |

## 🛠 설정 및 환경 변수

- **KRaft**: `KAFKA_PROCESS_ROLES="broker,controller"`, `KAFKA_CONTROLLER_QUORUM_VOTERS` 설정으로 3노드 쿼럼 구성.
- **네트워크**: `infra_net` (172.19.0.0/16) 내에서 고정 IP 사용 (`172.19.0.11` ~ `172.19.0.18`).
- **복제**: 기본 Replication Factor 3, Min ISR 2 설정으로 고가용성 확보.

## 📦 볼륨 마운트

- `kafka-1-data`, `kafka-2-data`, `kafka-3-data`: 각 브로커의 데이터 저장소
- `kafka-connect-data`: 커넥터 플러그인 및 상태 저장

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **리소스**: 3개의 브로커와 부가 서비스들이 실행되므로 충분한 메모리(4GB 이상 권장)가 필요합니다.
- **초기화**: 첫 실행 시 클러스터 ID(`CLUSTER_ID`)를 기반으로 포맷팅됩니다.
