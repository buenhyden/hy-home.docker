---
title: "Communication Tier (10-communication)"
version: "1.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# Communication Tier (10-communication)

## Purpose

### Service Role

이 tier에는 현재 root Compose가 include하는 패키지가 없다. 운영 메일 서버
Stalwart와 설정 helper는 SPEC-0262에서 독립 [Stalwart LAB](../../labs/stalwart/docker-compose.yml)으로
옮겼다. 개발용 SMTP 캡처 Mailpit은 [11 Quality](../11-quality/README.md)에서
`dev`, `local`, `mail-dev` profile로 관리하며 `mail_net`을 계속 사용한다.

#### Audience

애플리케이션 개발자, 메일 서비스 운영자와 인프라 담당자.

#### Scope

ADR-0062 capability tier 이름과 메일 경계 안내만 유지한다. 메일 내용, 비밀 원문,
도메인 공급자 설정 변경은 범위 밖이다.

#### Structure

| 대상 | 위치 | 운영 소유자 |
| --- | --- | --- |
| Stalwart LAB | [labs/stalwart/docker-compose.yml](../../labs/stalwart/docker-compose.yml), [설정 자산](../../labs/stalwart/README.md) | `GDE-0070`, `POL-0070`, `RUN-0070` (`docs/05.operations/*/15-labs/`) |
| Mailpit | [11 Quality](../11-quality/mailpit/README.md) | `GDE-0084`, `POL-0084`, `RUN-0084` |

### Supported Environment

없음: 이 tier에는 root Compose가 include하는 패키지가 없어 지원 런타임이 없다. 메일 서버는 독립 Stalwart LAB이, 개발용 SMTP 캡처는 Mailpit이 맡는다.

## Interfaces

### Inputs and Outputs

없음: 이 tier는 입출력을 제공하지 않는다. HOME 컨테이너의 SMTP는 Mailpit 캡처로만 전달되고 Stalwart LAB은 HOME network에 연결되지 않는다.

### Security Boundary

메일 내용과 비밀 원문은 이 tier의 범위 밖이다. Stalwart LAB은 HOME network에 연결되지 않으며 Opsflow notifier는 `stalwart` 호스트를 거부하고 Mailpit으로만 보낸다.

## Development

### Local Workflow

1. HOME 컨테이너의 SMTP는 Mailpit 캡처를 사용한다. Opsflow notifier도 `stalwart`
   호스트를 거부하고 Mailpit으로만 보낸다.
2. Stalwart LAB은 HOME network에 연결되지 않으므로 HOME 컨테이너가 제출할 수 없다.
   외부 송수신은 DNS·평판을 포함한 새 요구사항이 필요하다.

### Checks

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile mail-dev config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

정적 통과는 실제 메일 배달·수신 또는 데이터 복원 성공의 증거가 아니다.

## Operations

### Runbook Links

- [LAB source](../../labs/README.md)
- [Infrastructure index](../README.md)

### Observability and Recovery

없음: 이 tier에는 실행 서비스가 없다. 메일 관련 운영은 [Stalwart LAB README](../../labs/stalwart/README.md)와 [Mailpit Runbook](../../docs/05.operations/runbooks/11-mail-and-notifications/0084-mailpit.md)를 따른다.
