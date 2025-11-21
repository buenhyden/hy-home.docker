# MongoDB

**MongoDB**는 유연한 JSON 유사 문서를 사용하는 NoSQL 데이터베이스입니다.
이 구성은 **Replica Set**으로 설정되어 있어 고가용성을 제공합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **mongodb-rep1** | Primary/Secondary 노드 1 | `27017` |
| **mongodb-rep2** | Primary/Secondary 노드 2 | `27018` (Host) |
| **mongo-express** | 웹 기반 관리 UI | `8081` |
| **mongodb-exporter** | Prometheus용 메트릭 Exporter | `9216` |

## 🛠 설정 및 환경 변수

- **Replica Set**: `MyReplicaSet` 이름으로 구성.
- **인증**: `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD` 사용.
- **Mongo Express**: `http://localhost:8081` 접속 (Basic Auth 설정됨).

## 📦 볼륨 마운트

- `replicaset-1-mongo-data-volume`: 노드 1 데이터
- `replicaset-2-mongo-data-volume`: 노드 2 데이터

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **초기화**: Replica Set 초기화 스크립트나 명령어가 필요할 수 있습니다. (자동 설정 여부 확인 필요)
