<!-- Target: docs/03.adr/0010-communication-services.md -->

# ADR-0010: 10-communication 계층 주요 서비스 선정 및 구성

## Context

`10-communication` 계층은 시스템의 전자우편 기반 알림 및 메시지 수발신을 담당한다. 개발 단계에서는 실제 사용자에게 메일이 발송되는 사고를 방지해야 하며, 운영 단계에서는 높은 도달율(Deliverability)과 보안성을 갖춘 메일 서버가 필요하다. 이를 위해 경량화된 샌드박스와 현대적인 고성능 메일 서버 솔루션을 선정해야 한다.

## Decision

다음과 같은 서비스 스택을 `10-communication`의 표준 도구로 선정한다.

1. **SMTP Trap (Dev)**: **MailHog**
    * 이유: 설정이 간편하고, 웹 UI를 통해 캡처된 메일을 즉시 확인할 수 있으며, 외부 릴레이 없이 메모리상에서만 동작하여 안전하다.
2. **Mail Server (Prod)**: **Stalwart**
    * 이유: Rust로 작성되어 메모리 효율과 성능이 뛰어나며, JMAP, IMAP, SMTP 등 현대적인 프로토콜을 모두 지원한다. 또한 단일 바이너리로 운영이 가능하여 유지보수가 용이하다.

## Rationale

* **격리 정책**: 개발용 `mailhog`는 1025 포트를, 운영용 `stalwart`는 표준 25/465/587 포트를 사용하여 논리적으로 명확히 분리한다.
* **보안 프로토콜**: 모든 통신에 TLS 1.3을 적용하며, Stalwart는 Keycloak OIDC를 통해 관리 권한을 위임받는다.
* **데이터 신뢰성**: Stalwart의 메일 저장소는 영구 볼륨으로 관리되어 시스템 재시작 후에도 데이터를 유지한다.

## Consequences

* **Positive**:
  * 개발 단계에서의 메일 오발송 리스크가 완전히 제거된다.
  * 표준화된 메일 서버 구성을 통해 SPF/DKIM 등 복잡한 스팸 방지 정책을 일관되게 적용할 수 있다.
* **Negative**:
  * Stalwart의 초기 설정(도메인 인증 등)이 다소 복잡할 수 있다.
  * 메일 서버 운영에 필요한 고정 IP 및 DNS 레코드 관리가 수반된다.

## Status

Accepted (2026-03-26)
