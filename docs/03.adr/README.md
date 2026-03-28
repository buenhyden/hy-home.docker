# 03. ADR (Architecture Decision Records)

> 프로젝트의 중요한 기술적/아키텍처적 의사결정의 배경과 결과를 기록하는 저장소

## Overview

`docs/03.adr/` 경로는 `hy-home.docker` 프로젝트에서 이루어진 주요 기술적 결정 사항들을 관리한다. ADR은 단순한 결과 기록이 아니라, "왜(Why)" 해당 결정을 내렸는지, 어떤 대안(Alternatives)이 있었는지, 그리고 그로 인한 결과(Consequences)가 무엇인지를 투명하게 공개하여 프로젝트의 아키텍처적 무결성을 유지하고 지식 전파를 돕는다.

## Audience

이 README의 주요 독자:

- Architects & Lead Engineers
- New Team Members (Onboarding)
- Documentation Writers
- AI Agents (Historical context and decision constraints)

## Scope

### In Scope

- 아키텍처 결정 기록문 (`####-<name>.md`)
- 결정의 맥락(Context) 및 비즈니스/기술적 배경
- 고려된 대안 및 각 대안의 장단점 분석
- 결정에 따른 긍정적 효과 및 트레이드 오프(Trade-offs)

### Out of Scope

- 제품 요구사항 (-> `01.prd/`)
- 시스템 아키텍처 참조 모델 (-> `02.ard/`)
- 세부 구현 명세서 (-> `04.specs/`)
- 일시적이거나 사소한 코드 수준의 결정

## Structure

```text
03.adr/
├── 0001-traefik-nginx-hybrid.md         # Gateway 하이브리드 구성 결정
├── 0002-keycloak-oauth2-proxy-choice.md # Auth 티어 기술 스택 선택
├── 0003-vault-as-secrets-manager.md     # Security 티어 비밀 정보 관리 결정
├── 0004-postgresql-ha-patroni.md        # Data 티어 HA 솔루션 선택
├── 0005-kafka-vs-rabbitmq-selection.md  # Messaging 티어 기술 스택 선택
├── 0006-lgtm-stack-selection.md         # Observability 기술 스택 선택
├── 0007-airflow-n8n-hybrid-workflow.md  # Workflow 티어 기술 스택 선택
├── 0008-ai-services.md               # AI Tier 서비스 선정
├── 0009-tooling-services.md          # Tooling Tier 서비스 선정
├── 0010-communication-services.md     # Communication Tier 서비스 선정
├── 0011-laboratory-services.md        # Laboratory Tier 서비스 선정
├── 0015-analytics-engine-selection.md # Analytics Tier 서비스 선정
├── 0016-open-webui-implementation.md # Open WebUI 구현 결정
├── 0017-auth-hardening-runtime-and-fail-closed.md # 02-auth 런타임 하드닝/Fail-closed 결정
├── 0018-vault-hardening-and-ha-expansion-strategy.md # 03-security 단계적 하드닝/HA 확장 전략 결정
├── 0019-04-data-hardening-and-ha-expansion-strategy.md # 04-data 단계적 하드닝/확장 전략 결정
├── 0020-messaging-hardening-and-ha-expansion-strategy.md # 05-messaging 단계적 하드닝/확장 전략 결정
├── 0021-observability-hardening-and-ha-expansion-strategy.md # 06-observability 단계적 하드닝/확장 전략 결정
└── README.md                            # This file
```

## How to Work in This Area

1. 중대한 기술적 변경이나 아키텍처 결정이 필요할 때 `docs/99.templates/adr.template.md`를 사용한다.
2. 파일명은 `####-<short-title>.md` 순차 번호 형식을 유지한다. (예: `0001-choice-of-db.md`)
3. 한 문서 당 하나의 결정 사항만 다룬다.
4. 결정 상태(Status: Proposed, Accepted, Deprecated, Superseded)를 명확히 관리한다 (필요 시 YAML Frontmatter 활용).

## Documentation Standards

- 결정을 내린 시점의 상황을 객관적으로 서술한다.
- 트레이드 오프를 숨기지 않고 명확히 기술한다.
- 가능한 경우 결정에 서명한 사람(Owner)과 날짜를 포함한다.

## Related References

- [01.prd (Requirements)](../01.prd/README.md)
- [02.ard (Architecture)](../02.ard/README.md)
- [04.specs (Specifications)](../04.specs/README.md)
- [99.templates (Templates)](../99.templates/README.md)

---
*Maintained by Technical Decision Committee*
