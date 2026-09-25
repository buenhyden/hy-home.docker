---
title: "Security Optimization and Hardening Architecture"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "AD-0018"
parent_ids:
- "REQ-0003"
created: "2026-03-28"
---
# Security Optimization and Hardening Architecture

## Context and Stakeholders

이 문서는 `infra/03-security/`에 구현된 OpenBao와 OpenBao Agent 경계를 설명한다.
Maintainer, service owner, operator는 secret 원본, rendered output, health,
복구 절차의 소유권을 명확히 구분해야 한다.

## System Boundaries

- OpenBao는 KV-v2 secret 저장과 조회를 소유한다.
- OpenBao Agent는 AppRole 인증, token sink, service별 template rendering을
  소유한다.
- Gateway는 외부 TLS 종료와 routing을 소유하며 OpenBao 내부 secret lifecycle을
  소유하지 않는다.
- 애플리케이션별 설정 파싱과 외부 KMS/HSM 운영은 이 아키텍처 밖이다.

## Components

현재 HOME 구현은 `infra/03-security/openbao/docker-compose.yml`의 `openbao`와
`openbao-agent`, policy·configuration·template 파일, 지속 volume으로 구성된다.
Traefik이 외부 경계를 제공하고 OpenBao Agent가 최소 범위의 출력만 소비
서비스에 제공한다.

## Data Flow

Secret 원본은 OpenBao KV-v2에 저장된다. OpenBao Agent는 AppRole로 인증하고
`/openbao/agent/token`에 제한된 token state를 유지한 뒤
`/openbao/out/<service>/<key>`로 template output을 렌더링한다. 원본 secret과
rendered output은 서로 다른 접근 경계를 유지한다.

## Deployment View

현재 HOME 배치는 Docker Compose 기반 단일 OpenBao와 OpenBao Agent 구조다.
`scripts/hardening/check-all-hardening.sh 03-security`, Compose validation,
template security baseline이 tracked configuration을 검사한다. Raft 3-node,
auto-unseal, remote audit sink는 현재 구현이 아니며 별도 승인된 Requirement와
ADR 없이는 current topology로 간주하지 않는다.

## Quality Attributes

- **Security**: plaintext secret과 placeholder path를 거부하고 최소 권한을
  유지한다.
- **Reliability**: healthcheck, persistent data, 명시적 복구 절차를 유지한다.
- **Observability**: health와 rendering 결과는 secret value를 노출하지 않고
  확인할 수 있어야 한다.
- **Operability**: configuration, Operations 절차, validation 결과가 같은
  current topology를 설명해야 한다.

## Traceability

- [REQ-0003](../../01.requirements/0003-security.md)
- [ADR-0018](../decisions/0018-vault-hardening-and-ha-expansion-strategy.md)
- [SPEC-0003](0003-security-architecture.md)
- [OpenBao policy](../../05.operations/policies/0085-openbao.md)
- [OpenBao runbook](../../05.operations/runbooks/0085-openbao.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
