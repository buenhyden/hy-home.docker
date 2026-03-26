# Ollama Governance Operations Policy

> GPU Management, Model Adoption & Efficiency Standards

---

## Overview (KR)

이 문서는 `hy-home.docker`의 Ollama 추론 엔진에 대한 운영 정책을 정의한다. 한정된 GPU 리소스(VRAM)의 효율적 활용과 보안이 검증된 모델 도입 기준을 규정한다.

## Policy Scope

Ollama 서비스의 런타임 구성, 모델 파일 관리, 그리고 GPU 자원 할당 정책을 관장한다.

## Applies To

- **Systems**: `ollama`, `ollama-exporter`
- **Agents**: AI 서비스 연동 에이전트
- **Environments**: Production, Lab (GPU 기반 노드)

## Controls

- **Required**:
  - 모든 추론 요청은 `keep_alive` 파라미터를 사용하여 비활성 시 모델을 언로드해야 한다 (기본값 설정 권장).
  - 프로덕션 환경의 모델은 반드시 `4-bit` 이상의 양자화(Quantized) 버전을 사용해야 한다.
- **Allowed**:
  - 검증된 공식 라이브러리(`library/` 네임스페이스)의 모델 풀링.
  - 실험 목적의 커스텀 GGUF 모델 사용 (보안 검토 후).
- **Disallowed**:
  - 8-bit 미만 양자화되지 않은 FP16/FP32 모델의 무단 로드 (VRAM 점유 방지).
  - 인증되지 않은 외부 소스에서의 모델 직접 실행.

## Exceptions

- 70B 이상의 대규모 모델 구동 시 전용 노드 예약이 가능하며, 이 경우 `keep_alive` 정책 예외 적용 가능 (사전 승인 필요).

## Verification

- `ollama-exporter`를 통해 VRAM 사용량을 매시간 점검한다.
- `80%` 이상의 VRAM 점유 상태가 10분 이상 지속될 경우 경고를 발생시킨다.

## Review Cadence

- Quarterly (분기별 모델 사용 현황 및 최신 양자화 기술 적용 검토)

## Related Documents

- **ARD**: `[../02.ard/08-ai/llm-inference.md]` (TBD)
- **Runbook**: `[../09.runbooks/08-ai/ollama.md]`
- **Guide**: `[../07.guides/08-ai/ollama.md]`
