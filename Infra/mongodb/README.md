# MongoDB Replica Set

## 개요

이 디렉토리는 레플리카 셋(Replica Set)으로 구성된 MongoDB 클러스터를 위한 Docker Compose 구성을 포함합니다. 2개의 데이터 노드와 1개의 아비터(Arbiter) 노드로 구성되며, 자동 키 생성 및 초기화 기능을 포함합니다.

## 서비스

- **mongodb-rep1, mongodb-rep2**: 데이터 저장 노드.
- **mongodb-arbiter**: 투표권만 가진 아비터 노드 (데이터 저장 안 함).
- **mongo-key-generator**: 레플리카 셋 인증용 KeyFile 생성 및 권한 설정 (일회성).
- **mongo-init**: 레플리카 셋 자동 초기화 (일회성).
- **mongo-express**: MongoDB 웹 관리 인터페이스.
- **mongodb-exporter**: Prometheus 메트릭 Exporter.

## 필수 조건

- Docker 및 Docker Compose 설치.
- `Docker/Infra` 루트 디렉토리에 `.env` 파일.

## 설정

이 서비스는 다음 환경 변수(`.env`에 정의됨)를 사용합니다:

- `MONGODB_ROOT_USERNAME`, `MONGODB_ROOT_PASSWORD`: 루트 관리자 자격 증명.
- `MONGO_EXPRESS_PORT`: Mongo Express 포트.
- `MONGO_EXPORTER_PORT`: Exporter 포트.

## 사용법

서비스 시작:

```bash
docker-compose up -d
```

*참고: 윈도우 환경에서의 권한 문제를 해결하기 위해 `mongo-key` 도커 볼륨을 사용하여 KeyFile을 관리합니다.*

## 접속

- **Mongo Express**: `https://mongo-express.${DEFAULT_URL}` (Traefik 사용)

## 볼륨

- `mongodb*-data`: 각 데이터 노드의 영구 저장소.
- `mongo-key`: 레플리카 셋 인증 키 저장소 (자동 생성됨).
