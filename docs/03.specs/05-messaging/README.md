# 05-messaging Specifications

> 메시지 브로커 및 스트리밍 서비스 기술 사양

## Overview

`docs/03.specs/05-messaging`는 Kafka 및 RabbitMQ 기반 메시징 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- 토픽 구조, 파티셔닝, 소비자 그룹, 브로커 설정 사양
- 메시지 보존 정책 및 인증 경계

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/05-messaging/` 담당)

## Structure

```text
05-messaging/
├── spec.md      # Messaging services technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/05-messaging/README.md](../../../infra/05-messaging/README.md)
- [docs/05.operations/guides/05-messaging/](../../05.operations/guides/05-messaging/)
