---
title: "Ollama Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0056"
parent_ids:
- "AD-0008"
created: "2026-05-17"
---

# Ollama Operations Policy

## Overview

이 문서는 Ollama 운영 정책을 정의한다. 제한된 GPU 자원에서 안정적으로 추론 서비스를 제공하기 위해 모델 도입 기준, 리소스 사용 한계, 장애 대응 기준을 규정한다.

## Policy Scope

Ollama 추론 엔진 운영 전반:

- 모델 도입/승격/퇴출 기준
- GPU/VRAM 자원 통제
- 추론 계층 변경 승인 및 검증

- **Systems**: `ollama`, `ollama-exporter`, `open-webui`
- **Agents**: 모델 배포/교체 자동화 에이전트, 추론 호출 에이전트
- **Environments**: Local, Dev, Homelab, Production-like rehearsal

## Controls

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

- Ollama and its exporter remain `HOME`. Model additions and replacements require source, digest, model-card/license, resource fit, and representative quality/safety evidence.
- Treat model blobs as rebuildable only when the exact artifact is reproducible; otherwise preserve the model volume as recovery data. User prompts or generated content are outside this service volume and follow their owning application.
- Before upgrade, record image/model digests and GPU/driver compatibility, preserve a recoverable model set, and verify API, exporter, representative inference, and Open WebUI integration before accepting the new version.
- Resource declarations are caps/reservations, not headroom claims. Any concurrency increase requires measured CPU, RAM, VRAM, latency, and failure evidence under the shared-GPU workload.
- Removal requires an approved model-retention decision, provenance export, client shutdown, route removal, and explicit approval before deleting the model volume.

## Exceptions

- 장애 복구 목적의 단기 예외(예: 임시 모델 fallback)는 온콜 승인 하에 허용.
- 예외 종료 후 기본 정책으로 즉시 복귀하고 기록을 남겨야 한다.

## Verification

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

## Review Cadence

- **Quarterly**: 모델 포트폴리오/자원 정책 검토
- **Per Model Change**: 모델 도입/교체 건별 검토

## Traceability

- Declared parent: [AI Infrastructure Architecture Description](../../../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](guide.md) (`GDE-0056`), [Runbook](runbook.md) (`RUN-0056`)

## Related Documents

- [Ollama API authentication](https://docs.ollama.com/api/authentication): local API의 무인증 동작과 cloud API 인증을 구분한다.

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
