---
title: "08-AI Optimization Hardening Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0058"
parent_ids:
- "AD-0008"
created: "2026-05-10"
---

# 08-AI Optimization Hardening Operations Policy

## Overview

이 문서는 `08-ai` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, Ollama GPU 보호, Open WebUI stateful 운영, 모델 승격/접근 통제/로그 보존 정책을 통제한다.

## Scope

- `infra/08-ai/ollama/docker-compose.yml`
- `infra/08-ai/open-webui/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 08-ai`

- **Systems**: Ollama, Ollama Exporter, Open WebUI
- **Environments**: 로컬·개발·검증 및 운영 환경에 준하는 환경

## Rules

- **Required**:
  - Ollama public route는
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 유지한다.
    Open WebUI route는 `gateway-standard-chain@file`만 적용하고 native
    Keycloak OIDC를 유지한다.
  - Ollama는 `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 유지한다.
  - Open WebUI는 `template-stateful-med`를 사용한다.
  - `ollama-exporter`는 `ollama` health 기반 의존성과 metrics healthcheck를 유지한다.
  - AI 변경은 `check-all-hardening.sh 08-ai` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - 모델 승격은 실험/검증/운영 단계와 승인 기록을 포함해야 한다.
  - Open WebUI 모델 접근 권한은 역할/환경 단위로 분리해야 한다.
  - 대화 로그는 보존 기간/마스킹 기준을 명시하고 비식별화 정책을 준수해야 한다.
  - optimization-hardening 문서(PRD~Procedure) 링크를 유지해야 한다.
- **Allowed**:
  - Ollama 상한값의 점진적 튜닝(운영 지표 기반)
  - 모델 승격 기준 강화(품질/안전/eval 항목 추가)
  - 로그 보존/마스킹 정책의 보수적 강화
- **Disallowed**:
  - 무승인 SSO/middleware 완화
  - 모델 승격 절차 생략 배포
  - 민감 대화 로그 무마스킹 저장

### Catalog Expansion Approval Gates

- **Ollama 승인 조건**:
  - 모델 캐시/스토리지 정책 문서화 및 운영 증적 확보
  - GPU concurrency/queue 상한 변경 시 근거 지표 첨부
  - 모델 승격(실험 -> 운영) 체크리스트 완료
- **Open WebUI 승인 조건**:
  - SSO 강제 경로 검증 및 우회 금지 확인
  - 모델 접근 권한 분리 정책(역할/환경) 문서화
  - 대화 로그 보존 기간/마스킹 규칙/파기 절차 문서화

### Control evidence boundary

AI hardening은 일부 소스 문자열만 검사하며 GPU 여유, 사용자별 모델 권한, chat 보존·삭제, password 거부와 추론 성공을 증명하지 않는다. 모델 승격, 역할·환경별 접근 분리, 대화 masking/retention 요구는 유지한다. 소스에는 자동 chat retention과 완성된 모델 접근 분리를 입증할 설정이 부족하다. @buenhyden의 별도 통제·구현 변경과 검증 전에는 준수를 주장하지 않는다. 근거를 채우려고 비공개 대화를 로그에 남기지 않는다. ComfyUI 영속성과 Crawl4AI 격리는 각 Runbook의 통제를 따른다.

## Exceptions

- 장애 대응으로 일시 완화가 필요할 경우 승인 기록과 종료 시점이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

### Verification

점검 명령은 [가이드의 Common Checks](../guides/0058-ai-optimization-hardening.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- 월 1회 정기 검토
- AI 이미지/모델 정책/인증 정책 변경 시 수시 검토

### Traceability

- Declared parent: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0058-ai-optimization-hardening.md) (`GDE-0058`), [Runbook](../runbooks/0058-ai-optimization-hardening.md) (`RUN-0058`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0058-ai-optimization-hardening.md)
- [Recovery runbook](../runbooks/0058-ai-optimization-hardening.md)
