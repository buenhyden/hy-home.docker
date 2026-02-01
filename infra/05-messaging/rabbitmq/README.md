# RabbitMQ (05-messaging/rabbitmq)

## Overview

RabbitMQ는 AMQP(Advanced Message Queuing Protocol)를 지원하는 오픈 소스 메시지 브로커입니다. 이 구성에는 웹 기반 관리 인터페이스(Management UI)가 포함되어 있어 큐, 교환기(Exchanges), 바인딩 등을 쉽게 모니터링하고 관리할 수 있습니다.

## Features

- **Version**: `4.2.3-management-alpine`
- **Management UI**: `15672` 포트를 통해 접근 가능합니다.
- **Static IP**: `172.19.0.21` (on `infra_net`)
- **Healthcheck**: `rabbitmq-diagnostics`를 사용하여 연동 상태를 주기적으로 체크합니다.
- **Resource Limits**: CPU 0.5CORE / Memory 512MB 할당.

## Configuration (.env)

| Variable                        | Default Value | Description           |
| ------------------------------- | ------------- | --------------------- |
| `RABBITMQ_PORT`                 | `5672`        | AMQP 기본 포트        |
| `RABBITMQ_HOST_PORT`            | `5672`        | 호스트 노출 AMQP 포트 |
| `RABBITMQ_MANAGEMENT_PORT`      | `15672`       | 관리 UI 내부 포트     |
| `RABBITMQ_MANAGEMENT_HOST_PORT` | `15672`       | 관리 UI 호스트 포트   |
| `RABBITMQ_DEFAULT_USER`         | `admin`       | 초기 관리자 계정 명   |
| `RABBITMQ_DEFAULT_PASS`         | `<password>`  | 초기 관리자 비밀번호  |
| `DEFAULT_RABBITMQ_DATA_DIR`     | (Path)        | 데이터 영속화 경로    |

## Run

이 서비스는 `rabbitmq` 프로파일로 관리됩니다.

```bash
# 서비스 실행
docker compose --profile rabbitmq up -d

# 서비스 중지
docker compose --profile rabbitmq stop
```

## File Map

| Path                 | Description                  |
| -------------------- | ---------------------------- |
| `docker-compose.yml` | RabbitMQ 서비스 및 볼륨 정의 |
| `README.md`          | 서비스 설명 및 운영 가이드   |

## Notes

- 관리 UI 접속 주소: `http://localhost:15672` (또는 로컬 도메인 설정 시 `http://rabbitmq.${DEFAULT_URL}`)
- 초기 로그인 후 보안을 위해 비밀번호를 변경하는 것을 권장합니다.
