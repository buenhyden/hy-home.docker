---
title: "08-AI Optimization Hardening Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0058"
parent_ids:
- "AD-0008"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# 08-AI Optimization Hardening Operations Policy

## Purpose and Scope

### Objective

이 문서는 `08-ai` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, Ollama GPU 보호, Open WebUI LAB 경계, 모델 승격/접근 통제/로그 보존 정책을 통제한다.

#### Authority

- Declared parent: [AI Infrastructure Architecture Description](../../../02.architecture/01.descriptions/0008-ai-architecture.md) (`AD-0008`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

### Applies To

- `infra/08-ai/ollama/docker-compose.yml`
- `labs/open-webui/docker-compose.yml`(독립 LAB, 같은 `08-ai` 검사)
- `scripts/hardening/check-all-hardening.sh 08-ai`

- **Systems**: Ollama, Ollama Exporter, Open WebUI
- **Environments**: 로컬·개발·검증 및 운영 환경에 준하는 환경

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0058-R1 | 항상 | 필수: Ollama public route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 유지한다 | none | none |
| POL-0058-R2 | 항상 | 필수: Open WebUI는 gateway route 없는 독립 LAB이며 `LAB_HOST_BIND_IP`에만 게시한다 | none | none |
| POL-0058-R3 | 항상 | 필수: Open WebUI는 native Keycloak OIDC를 유지한다 | none | none |
| POL-0058-R4 | 항상 | 필수: Ollama는 `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 유지한다 | none | none |
| POL-0058-R5 | 항상 | 필수: Open WebUI는 `template-stateful-med`를 사용한다 | none | none |
| POL-0058-R6 | 항상 | 필수: `ollama-exporter`는 `ollama` health 기반 의존성과 metrics healthcheck를 유지한다 | none | none |
| POL-0058-R7 | AI 변경 | 필수: `check-all-hardening.sh 08-ai` 및 CI `infrastructure-hardening`을 통과한다 | `check-all-hardening.sh 08-ai` / CI `infrastructure-hardening` | 정적 검사와 hardening 검사 결과 |
| POL-0058-R8 | 모델 승격 | 필수: 실험/검증/운영 단계와 승인 기록을 포함한다 | 수동 | 승인 기록 |
| POL-0058-R9 | 항상 | 필수: Open WebUI 모델 접근 권한을 역할/환경 단위로 분리한다 | none | none |
| POL-0058-R10 | 항상 | 필수: 대화 로그의 보존 기간/마스킹 기준을 명시한다 | 수동 | none |
| POL-0058-R11 | 항상 | 필수: 비식별화 정책을 준수한다 | 수동 | none |
| POL-0058-R12 | 항상 | 필수: optimization-hardening 문서(PRD~Procedure) 링크를 유지한다 | none | none |
| POL-0058-R13 | 운영 지표 기반 | 허용: Ollama 상한값의 점진적 튜닝 | none | none |
| POL-0058-R14 | 항상 | 허용: 모델 승격 기준 강화(품질/안전/eval 항목 추가) | none | none |
| POL-0058-R15 | 항상 | 허용: 로그 보존/마스킹 정책의 보수적 강화 | none | none |
| POL-0058-R16 | 항상 | 금지: 무승인 SSO/middleware 완화 | 수동 | none |
| POL-0058-R17 | 항상 | 금지: 모델 승격 절차 생략 배포 | 수동 | 승인 기록 |
| POL-0058-R18 | 항상 | 금지: 민감 대화 로그 무마스킹 저장 | 수동 | none |
| POL-0058-R19 | Ollama 카탈로그 확장 | 필수: 모델 캐시/스토리지 정책을 문서화하고 운영 증적을 확보한다 | none | none |
| POL-0058-R20 | GPU concurrency/queue 상한 변경 | 필수: 근거 지표를 첨부한다 | none | none |
| POL-0058-R21 | 모델 승격(실험 -> 운영) | 필수: 체크리스트를 완료한다 | none | none |
| POL-0058-R22 | Open WebUI 카탈로그 확장 | 필수: native OIDC 유지, gateway route 부재와 우회 금지를 확인한다 | none | none |
| POL-0058-R23 | Open WebUI 카탈로그 확장 | 필수: 모델 접근 권한 분리 정책(역할/환경)을 문서화한다 | none | none |
| POL-0058-R24 | Open WebUI 카탈로그 확장 | 필수: 대화 로그 보존 기간/마스킹 규칙/파기 절차를 문서화한다 | none | none |
| POL-0058-R25 | 별도 통제·구현 변경과 검증 전 | 금지: 자동 chat retention과 모델 접근 분리의 준수 주장 | none | none |
| POL-0058-R26 | 항상 | 금지: 근거를 채우려고 비공개 대화를 로그에 남김 | none | none |
| POL-0058-R27 | ComfyUI 영속성과 Crawl4AI 격리 | 필수: 각 Runbook의 통제를 따른다 | none | none |

- **Required**:
  - Ollama public route는
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 유지한다.
    Open WebUI는 gateway route 없는 독립 LAB이며 `LAB_HOST_BIND_IP`에만 게시하고 native
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

#### Catalog Expansion Approval Gates

- **Ollama 승인 조건**:
  - 모델 캐시/스토리지 정책 문서화 및 운영 증적 확보
  - GPU concurrency/queue 상한 변경 시 근거 지표 첨부
  - 모델 승격(실험 -> 운영) 체크리스트 완료
- **Open WebUI 승인 조건**:
  - native OIDC 유지, gateway route 부재와 우회 금지 확인
  - 모델 접근 권한 분리 정책(역할/환경) 문서화
  - 대화 로그 보존 기간/마스킹 규칙/파기 절차 문서화

#### Control evidence boundary

AI hardening은 일부 소스 문자열만 검사하며 GPU 여유, 사용자별 모델 권한, chat 보존·삭제, password 거부와 추론 성공을 증명하지 않는다. 모델 승격, 역할·환경별 접근 분리, 대화 masking/retention 요구는 유지한다. 소스에는 자동 chat retention과 완성된 모델 접근 분리를 입증할 설정이 부족하다. @buenhyden의 별도 통제·구현 변경과 검증 전에는 준수를 주장하지 않는다. 근거를 채우려고 비공개 대화를 로그에 남기지 않는다. ComfyUI 영속성과 Crawl4AI 격리는 각 Runbook의 통제를 따른다.

### Exceptions

#### Exception Conditions

- 장애 대응으로 일시 완화가 필요할 경우 승인 기록과 종료 시점이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

#### Approval and Review

- 월 1회 정기 검토
- AI 이미지/모델 정책/인증 정책 변경 시 수시 검토

예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다.

## Enforcement

### Mechanisms

점검 명령은 [가이드의 Common Checks](../../01.guides/09.ai-and-search/0058-ai-optimization-hardening.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Limits

hardening 검사는 일부 소스 문자열만 확인하며 정책이 직접 아래 한계를 밝힌다.

- 인증과 노출(POL-0058): R1-R3에는 정책이 지정한 검사가 없다.
- 구성 상한(POL-0058): R4-R6에는 정책이 지정한 검사가 없다.
- 모델 승격과 접근(POL-0058): R8은 수동 검토나 승인에 의존한다; R9에는 정책이 지정한 검사가 없다.
- 대화 로그(POL-0058): R10-R11은 수동 검토나 승인에 의존한다.
- 문서 링크(POL-0058): R12에는 정책이 지정한 검사가 없다.
- 허용 사항(POL-0058): R13-R15에는 정책이 지정한 검사가 없다.
- 금지 사항(POL-0058): R16-R18은 수동 검토나 승인에 의존한다.
- 카탈로그 확장 승인(POL-0058): R19-R24에는 정책이 지정한 검사가 없다.
- 준수 주장(POL-0058): R25-R27에는 정책이 지정한 검사가 없다.
- GPU 여유, 사용자별 모델 권한, chat 보존·삭제, password 거부, 추론 성공은 hardening 검사로 증명되지 않는다.
- 소스에 자동 chat retention과 완성된 모델 접근 분리를 입증할 설정이 부족하여 @buenhyden의 별도 통제·구현 변경과 검증 전에는 준수를 주장하지 않는다.
- Mechanisms는 가이드 Common Checks에 위임되어 있고 표에 검사가 명시된 규칙 외에는 규칙별 검사가 지정되지 않는다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/09.ai-and-search/0058-ai-optimization-hardening.md) (`GDE-0058`), [Runbook](../../03.runbooks/09.ai-and-search/0058-ai-optimization-hardening.md) (`RUN-0058`)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/09.ai-and-search/0058-ai-optimization-hardening.md)
- [Recovery runbook](../../03.runbooks/09.ai-and-search/0058-ai-optimization-hardening.md)
