---
title: "Ollama Operations Policy"
version: "2.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0056"
parent_ids:
- "AD-0008"
created: "2026-05-17"
---

# Ollama Operations Policy

## Overview

이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다.

## Scope

Ollama 추론 엔진 운영 전반:

- 모델 도입/승격/퇴출 기준
- GPU/VRAM 자원 통제
- 추론 계층 변경 승인 및 검증

- **Systems**: `ollama`, `ollama-exporter`, `open-webui`
- **Environments**: 로컬·개발·홈랩과 운영 환경에 준하는 rehearsal

## Rules

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

### Lifecycle and data controls

- Ollama와 exporter를 HOME으로 유지한다. 모델 추가·교체에는 source/digest/model-card·license, 자원 적합성과 대표 품질·안전 근거가 필요하다.
- 정확한 artifact를 재현할 수 있을 때만 blob을 재구축 가능 자산으로 본다. 그렇지 않으면 model volume을 보존한다. Prompt·생성 결과는 사용하는 애플리케이션이 소유한다.
- Upgrade 전에 image/model digest와 GPU/driver 호환성을 기록하고 복구 가능한 모델 집합을 보존한다. API/exporter/대표 추론/WebUI 연동을 검증한 뒤 수용한다.
- 한도·예약은 여유 증거가 아니다. 동시성 확대에는 공유 GPU에서 CPU/RAM/VRAM·latency·실패를 측정한 근거가 필요하다.
- 제거에는 모델 보존 결정, 출처 export, client 중지, route 제거와 model volume 삭제 승인이 필요하다.

### Model and exporter capacity boundary

용량과 exporter 경계의 설명은 [가이드](../guides/0056-ollama.md#model-and-exporter-capacity-boundary)가 소유한다. 이 정책은 병렬·loaded-model·queue 설정을 context 크기와 공유 GPU 메모리와 함께 평가하고, 한도를 실측 여유로 해석하지 않을 것을 요구한다. 모델 삭제·download·driver 변경은 기존 승인·출처 및 [GPU 복구](../runbooks/0055-gpu-recovery.md) 경계를 따른다.

## Exceptions

- 장애 복구 목적의 단기 예외(예: 임시 모델 fallback)는 온콜 승인 하에 허용.
- 예외 종료 후 기본 정책으로 즉시 복귀하고 기록을 남겨야 한다.

### Verification

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

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- **Quarterly**: 모델 포트폴리오/자원 정책 검토
- **Per Model Change**: 모델 도입/교체 건별 검토

### Traceability

- Declared parent: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0056-ollama.md) (`GDE-0056`), [Runbook](../runbooks/0056-ollama.md) (`RUN-0056`)

## Related Documents

- [Ollama API authentication](https://docs.ollama.com/api/authentication): local API의 무인증 동작과 cloud API 인증을 구분한다.

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0056-ollama.md)
- [Recovery runbook](../runbooks/0056-ollama.md)
