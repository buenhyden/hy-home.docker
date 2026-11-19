---
title: "Ollama Operations Policy"
version: "2.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0056"
parent_ids:
- "AD-0008"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Ollama Operations Policy

## Purpose and Scope

### Objective

이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다.

#### Authority

- Declared parent: [AI Infrastructure Architecture Description](../../../02.architecture/01.descriptions/0008-ai-architecture.md) (`AD-0008`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

### Applies To

Ollama 추론 엔진 운영 전반:

- 모델 도입/승격/퇴출 기준
- GPU/VRAM 자원 통제
- 추론 계층 변경 승인 및 검증

- **Systems**: `ollama`, `ollama-exporter`. Open WebUI LAB은 승인된 endpoint로만 접근한다.
- **Environments**: 로컬·개발·홈랩과 운영 환경에 준하는 rehearsal

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0056-R1 | 항상 | 필수: 호스트 직접 API 포트는 loopback에만 바인딩한다 | 수동 | none |
| POL-0056-R2 | 컨테이너 소비자 | 필수: 컨테이너 소비자는 서비스 DNS를 사용한다 | none | none |
| POL-0056-R3 | 원격 소비자 | 필수: 원격 소비자는 인증된 gateway 경로를 사용한다 | none | none |
| POL-0056-R4 | 모델 변경 전 | 필수: 승인된 local/dev rehearsal에서 성능 및 안정성 검증을 수행한다 | 수동 | none |
| POL-0056-R5 | 운영 모델 | 필수: 검증된 태그/소스만 사용한다 | 수동 | none |
| POL-0056-R6 | 항상 | 필수: VRAM/메모리 사용량을 exporter 및 대시보드로 상시 관측한다 | 운영 중 VRAM 과점유/응답 지연/모델 로드 실패율 모니터링 | none |
| POL-0056-R7 | `ai` profile로 AI 서비스 기동 | 필수: runtime 승인 후 기동한다 | 수동 | none |
| POL-0056-R8 | 항상 | 허용: 승인된 경량/양자화 모델 배포 | 수동 | none |
| POL-0056-R9 | 항상 | 허용: `keep_alive` 정책 기반 모델 언로드 최적화 | none | none |
| POL-0056-R10 | 항상 | 금지: 인증 없는 Ollama API를 LAN/공용 인터페이스에 직접 게시하는 구성 | none | none |
| POL-0056-R11 | 항상 | 금지: 승인 없는 대형 모델 상시 로드 | 수동 | none |
| POL-0056-R12 | 항상 | 금지: 출처 불명/무검증 모델 운영 반영 | 수동 | none |
| POL-0056-R13 | 운영 시간대 | 금지: 무단 리소스 상향 | 수동 | none |
| POL-0056-R14 | 항상 | 필수: Ollama와 exporter를 HOME으로 유지한다 | none | none |
| POL-0056-R15 | 모델 추가·교체 | 필수: source/digest/model-card·license, 자원 적합성과 대표 품질·안전 근거를 갖춘다 | 수동 | none |
| POL-0056-R16 | blob 재구축 가능 여부 | 필수: 정확한 artifact를 재현할 수 있을 때만 blob을 재구축 가능 자산으로 보고 그렇지 않으면 model volume을 보존한다 | none | none |
| POL-0056-R17 | Upgrade 전 | 필수: image/model digest와 GPU/driver 호환성을 기록하고 복구 가능한 모델 집합을 보존한다 | none | none |
| POL-0056-R18 | Upgrade 수용 | 필수: API/exporter/대표 추론/WebUI 연동을 검증한 뒤 수용한다 | none | none |
| POL-0056-R19 | 항상 | 금지: 한도·예약을 여유 증거로 해석 | none | none |
| POL-0056-R20 | 동시성 확대 | 필수: 공유 GPU에서 CPU/RAM/VRAM·latency·실패를 측정한 근거를 갖춘다 | none | none |
| POL-0056-R21 | 제거 시 | 필수: 모델 보존 결정, 출처 export, client 중지, route 제거와 model volume 삭제 승인을 갖춘다 | 수동 | none |
| POL-0056-R22 | 항상 | 필수: 병렬·loaded-model·queue 설정을 context 크기와 공유 GPU 메모리와 함께 평가한다 | none | none |
| POL-0056-R23 | 모델 삭제·download·driver 변경 | 필수: 기존 승인·출처 및 GPU 복구 경계를 따른다 | 수동 | none |

- **Required**:
  - 호스트 직접 API 포트는 loopback에만 바인딩한다. 컨테이너 소비자는 서비스 DNS를, 원격 소비자는 인증된 gateway 경로를 사용한다.
  - 모델 변경 전 승인된 local/dev rehearsal에서 성능 및 안정성 검증을 수행해야 한다.
  - 운영 모델은 검증된 태그/소스만 사용해야 한다.
  - VRAM/메모리 사용량을 exporter 및 대시보드로 상시 관측해야 한다.
  - `ai` profile 선택으로 AI 서비스를 기동하는 것은 runtime 승인 후 수행해야 한다.
- **Allowed**:
  - 승인된 경량/양자화 모델 배포.
  - `keep_alive` 정책 기반 모델 언로드 최적화.
- **Disallowed**:
  - 인증 없는 Ollama API를 LAN/공용 인터페이스에 직접 게시하는 구성.
  - 승인 없는 대형 모델 상시 로드.
  - 출처 불명/무검증 모델 운영 반영.
  - 운영 시간대 무단 리소스 상향.

#### Lifecycle and data controls

- Ollama와 exporter를 HOME으로 유지한다. 모델 추가·교체에는 source/digest/model-card·license, 자원 적합성과 대표 품질·안전 근거가 필요하다.
- 정확한 artifact를 재현할 수 있을 때만 blob을 재구축 가능 자산으로 본다. 그렇지 않으면 model volume을 보존한다. Prompt·생성 결과는 사용하는 애플리케이션이 소유한다.
- Upgrade 전에 image/model digest와 GPU/driver 호환성을 기록하고 복구 가능한 모델 집합을 보존한다. API/exporter/대표 추론/WebUI 연동을 검증한 뒤 수용한다.
- 한도·예약은 여유 증거가 아니다. 동시성 확대에는 공유 GPU에서 CPU/RAM/VRAM·latency·실패를 측정한 근거가 필요하다.
- 제거에는 모델 보존 결정, 출처 export, client 중지, route 제거와 model volume 삭제 승인이 필요하다.

#### Model and exporter capacity boundary

용량과 exporter 경계의 설명은 [가이드](../../01.guides/09.ai-and-search/0056-ollama.md#model-and-exporter-capacity-boundary)가 소유한다. 이 정책은 병렬·loaded-model·queue 설정을 context 크기와 공유 GPU 메모리와 함께 평가하고, 한도를 실측 여유로 해석하지 않을 것을 요구한다. 모델 삭제·download·driver 변경은 기존 승인·출처 및 [GPU 복구](../../03.runbooks/09.ai-and-search/0055-gpu-recovery.md) 경계를 따른다.

### Exceptions

#### Exception Conditions

- 장애 복구 목적의 단기 예외(예: 임시 모델 fallback)는 온콜 승인 하에 허용.
- 예외 종료 후 기본 정책으로 즉시 복귀하고 기록을 남겨야 한다.

#### Approval and Review

- **Quarterly**: 모델 포트폴리오/자원 정책 검토
- **Per Model Change**: 모델 도입/교체 건별 검토

예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다.

## Enforcement

### Mechanisms

- 배포 전:
  - `bash scripts/hardening/check-all-hardening.sh 08-ai`
  - `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
  - `nvidia-smi` 정상
  - `/api/tags` 응답 정상
  - 대상 모델 추론 smoke test 성공
- 운영 중:
  - VRAM 과점유, 응답 지연, 모델 로드 실패율 모니터링
- 증적:
  - 배포 로그, 모델 태그 기록, hardening/compose 검증 결과, 롤백 결과

통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Limits

이 정책은 배포 전 검사 명령을 명시하지만 어느 규칙을 검증하는지 지정하지 않아 아래 항목은 기계적으로 강제되지 않는다.

- 노출과 접근(POL-0056): R1은 수동 검토나 승인에 의존한다; R2-R3에는 정책이 지정한 검사가 없다.
- 모델 변경 검증(POL-0056): R4-R5은 수동 검토나 승인에 의존한다.
- 승인(POL-0056): R7은 수동 검토나 승인에 의존한다.
- 허용 사항(POL-0056): R8은 수동 검토나 승인에 의존한다; R9에는 정책이 지정한 검사가 없다.
- 금지 사항(POL-0056): R11-R13은 수동 검토나 승인에 의존한다; R10에는 정책이 지정한 검사가 없다.
- 모델 lifecycle(POL-0056): R15, R21은 수동 검토나 승인에 의존한다; R14, R16-R20에는 정책이 지정한 검사가 없다.
- 용량 경계(POL-0056): R23은 수동 검토나 승인에 의존한다; R22에는 정책이 지정한 검사가 없다.
- 배포 전 `check-all-hardening.sh 08-ai`, `validate-docker-compose.sh`, `nvidia-smi`, `/api/tags`, 추론 smoke test는 Mechanisms에 나열될 뿐 규칙별로 지정되지 않는다.
- VRAM/응답 지연/모델 로드 실패율 모니터링은 운영 중 관측이며 통과 기준이 되는 검사 이름이 없다.
- 동시성 확대와 한도 적정성은 측정 근거를 요구하나 이를 검사하는 자동 점검은 지정되어 있지 않다.
- 분기·모델 변경별 검토는 정기 수동 검토이며 자동 점검이 없다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/09.ai-and-search/0056-ollama.md) (`GDE-0056`), [Runbook](../../03.runbooks/09.ai-and-search/0056-ollama.md) (`RUN-0056`)

- [Ollama API authentication](https://docs.ollama.com/api/authentication): local API의 무인증 동작과 cloud API 인증을 구분한다.
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/09.ai-and-search/0056-ollama.md)
- [Recovery runbook](../../03.runbooks/09.ai-and-search/0056-ollama.md)
