<!-- Target: docs/08.operations/08-ai-operational-policy.md -->

# 08-ai Operational Policy

## Overview (KR)

이 문서는 `08-ai` 계층 인프라의 운영 정책과 유지보수 가이드라인을 정의한다. GPU 자원 관리, 모델 생애주기, 그리고 보안 준수 사항을 다룬다.

## Resource Management

### 1. GPU Allocation
- Ollama 컨테이너는 단일 GPU 전용 예약을 유지한다. (`deploy.resources.reservations.devices`)
- 다른 컨테이너가 GPU를 점유하여 추론 성능이 저하되지 않도록 모니터링한다.

### 2. VRAM Cleanup
- 오랫동안 사용되지 않는 모델은 Ollama 메모리에서 자동으로 언로드되도록 설정(`OLLAMA_KEEP_ALIVE=5m`)되어 있다.
- 필요 시 `curl http://ollama:11434/api/generate -d '{"model": "name", "keep_alive": 0}'` 명령으로 강제 언로드할 수 있다.

## Model Lifecycle

### 1. Model Selection
- 공식 프로젝트 모델은 `spec.md`에 명시된 표준 모델로 제한한다.
- 신규 모델 도입 시 `docs/03.adr`을 통해 결정 과정을 기록하고 `spec.md`를 갱신해야 한다.

### 2. Updates & Security
- 모델 가중치는 정기적으로 업데이트하지 않으며, 특정 취약점이 보고되거나 성능 개선이 명확할 때만 교체한다.
- 모든 모델 다운로드는 `infra_net` 외부로의 직접 연결이 아닌, 사전 승인된 미러 또는 프록시를 통해 수행될 수 있다.

## Compliance & Security

- **Data Privacy**: 사용자 대화 로그는 외부로 전송되지 않으며, `open-webui` 데이터베이스에만 저장된다.
- **RBAC**: 일반 사용자는 모델 설정 및 시스템 프롬프트를 변경할 수 없으며, 관리자 권한은 시스템 운영팀으로 제한한다.

## Monitoring

- **Metrics**: `ollama-exporter`를 통해 수집된 지표를 Grafana 대시보드에서 상시 모니터링한다.
- **Alerts**: GPU 온도 80도 초과 또는 VRAM 점유율 95% 지속 시 경고를 발생시킨다.

## Related Documents

- **ARD**: [../../02.ard/0008-ai-architecture.md](../../02.ard/0008-ai-architecture.md)
- **Spec**: [../../04.specs/08-ai/spec.md](../../04.specs/08-ai/spec.md)
