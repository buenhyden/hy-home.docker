<!-- Target: docs/08.operations/08-ai/ollama.md -->

# Ollama Operations Policy

> GPU/VRAM 거버넌스와 모델 도입·승격·운영 통제 정책.

---

## Overview (KR)

이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다.

## Policy Scope

Ollama 추론 엔진 운영 전반:
- 모델 도입/승격/퇴출 기준
- GPU/VRAM 자원 통제
- 추론 계층 변경 승인 및 검증

## Applies To

- **Systems**: `ollama`, `ollama-exporter`, `open-webui`
- **Agents**: 모델 배포/교체 자동화 에이전트, 추론 호출 에이전트
- **Environments**: `prod`, `staging`, `lab`

## Controls

- **Required**:
  - 모델 변경 전 staging에서 성능 및 안정성 검증을 수행해야 한다.
  - 운영 모델은 검증된 태그/소스만 사용해야 한다.
  - VRAM/메모리 사용량을 exporter 및 대시보드로 상시 관측해야 한다.
- **Allowed**:
  - 승인된 경량/양자화 모델 배포.
  - `keep_alive` 정책 기반 모델 언로드 최적화.
- **Disallowed**:
  - 승인 없는 대형 모델 상시 로드.
  - 출처 불명/무검증 모델 운영 반영.
  - 운영 시간대 무단 리소스 상향.

## Exceptions

- 장애 복구 목적의 단기 예외(예: 임시 모델 fallback)는 온콜 승인 하에 허용.
- 예외 종료 후 기본 정책으로 즉시 복귀하고 기록을 남겨야 한다.

## Verification

- 배포 전:
  - `nvidia-smi` 정상
  - `/api/tags` 응답 정상
  - 대상 모델 추론 smoke test 성공
- 운영 중:
  - VRAM 과점유, 응답 지연, 모델 로드 실패율 모니터링
- 증적:
  - 배포 로그, 모델 버전 기록, 롤백 결과

## Review Cadence

- **Quarterly**: 모델 포트폴리오/자원 정책 검토
- **Per Model Change**: 모델 도입/교체 건별 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
  - 모델/기본 프롬프트 변경은 변경 요청 + 검증 기록 + 운영 반영 순으로 진행
- **Eval / Guardrail Threshold**:
  - 배포 게이트: health, 기본 추론 성공, 리소스 임계 초과 없음
- **Log / Trace Retention**:
  - 추론 계층 운영 로그/지표 증적 최소 90일 보관
- **Safety Incident Thresholds**:
  - GPU 자원 고갈로 서비스 불능, 무단 모델 교체, 비인가 추론 엔드포인트 노출은 `Sev1`

## Related Documents

- **PRD**: `[../../01.prd/2026-03-26-08-ai.md]`
- **ARD**: `[../../02.ard/0008-ai-architecture.md]`
- **ADR**: `[../../03.adr/0008-ollama-openwebui-local-ai.md]`
- **Spec**: `[../../04.specs/08-ai/spec.md]`
- **Guide**: `[../../07.guides/08-ai/ollama.md]`
- **Runbook**: `[../../09.runbooks/08-ai/ollama.md]`
