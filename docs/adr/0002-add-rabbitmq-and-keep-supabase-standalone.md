# 0002 - Add RabbitMQ (Optional) and Keep Supabase Standalone

## Status

Accepted

## Context

- Kafka는 고성능 스트리밍에 적합하지만, 단순 AMQP 큐 기반 워크로드에는 운영 부담이 큽니다.
- RabbitMQ는 관리 UI와 간단한 큐/라우팅 패턴을 제공하여 비동기 작업 처리에 유리합니다.
- Supabase는 다수의 컴포넌트와 포트를 사용하며, 항상 구동하기에는 리소스/운영 부담이 큽니다.

## Decision

- RabbitMQ를 `rabbitmq` 프로파일 기반 **선택 스택**으로 추가하고, 루트 `docker-compose.yml`에서 include한다.
- Supabase는 **Standalone 스택**으로 유지하여 필요할 때만 `infra/04-data/supabase`에서 실행한다.
- RabbitMQ 관련 환경 변수는 `.env`에 추가하고, 문서에 실행/접속 방법을 명시한다.

## Consequences

- AMQP 기반 메시징을 선택적으로 사용할 수 있다.
- 기본 기동 시 RabbitMQ/Supabase가 자동 실행되지 않아 리소스 소비를 줄일 수 있다.
- Supabase는 별도 실행/종료 관리가 필요하며, 운영 절차가 분리된다.

## Alternatives Considered

- **Kafka만 사용**: 단순 큐 처리에는 과도한 운영 비용.
- **Supabase를 기본 include로 편입**: 리소스 사용량 증가와 포트 충돌 리스크.
