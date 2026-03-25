# AI Resource Operations Policy (08-ai)

> GPU Management, Model Governance & Capacity Planning

## Overview

이 정책은 `hy-home.docker` AI 계층(08-ai)의 하드웨어 리소스 최적화 및 모델 배포 기준을 정의한다.

## GPU Resource Management

- **Reservations**: AI 서비스를 위해 최소 1개의 고성능 NVIDIA GPU와 전용 VRAM을 예약한다.
- **Over-subscription**: 다수의 모델을 동시에 로드할 경우 VRAM 파편화 방지를 위해 사용되지 않는 모델은 `keep_alive=0` 설정을 통해 명시적으로 언로드(Unload)한다.

## Model Governance

### 1. 모델 도입 기준 (Model Adoption)

- **Security**: 출처가 불분명한 모델 파일(GGUF 등)은 시스템 보안을 위해 사용 전 검증을 거쳐야 한다.
- **Efficiency**: 서비스 용도에 맞춰 파라미터 수(7B, 13B, 70B 등)를 선택하고, 가급적 4-bit 이상 양자화된 모델을 사용한다.

### 2. 라이프사이클 관리

- **Model Purge**: 90일 이상 사용되지 않은 모델 파일은 스토리니 확보를 위해 자동 삭제 대상으로 검토한다.
- **Updates**: 보안 취약점 패치나 성능 개선 버전이 출시된 경우 주기적으로 모델 버전을 갱신한다.

## Scalability

- 추론 요청이 폭증할 경우 `01-gateway` (Traefik) 수준에서 속도 제한(Rate Limiting)을 적용하여 시스템 전체의 안정성을 보호한다.
- 필요 시 다중 Ollama 인스턴스를 구성하여 로드밸런싱을 수행한다.

## Related Documents

- [07. Guides](../../docs/07.guides/08-ai/README.md)
- [09. Runbooks](../../docs/09.runbooks/08-ai/README.md)
