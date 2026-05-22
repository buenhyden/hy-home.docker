---
status: active
---
<!-- Target: docs/05.operations/policies/standardize-infra-net.md -->

# infra_net IP Management Operations Policy

## Overview (KR)

이 문서는 `hy-home.docker` 시스템의 네트워크 레이어인 `infra_net` 내 IP 할당 및 관리 정책을 정의한다. IP 충돌 방지 및 일관성 유지를 위한 통제 기준을 제공한다.

## Policy Scope

이 정책은 `infra_net` 브릿지 네트워크에 연결된 모든 Docker 컨테이너의 IP 할당 방식을 관할한다.

## Applies To

- **Systems**: `hy-home.docker` 기반 모든 서비스.
- **Agents**: 모든 인프라 관리 에이전트.
- **Environments**: Local (k3d/docker-compose) 및 Production (Future) 개발/운영 환경.

## Controls

- **Required**:
  - 모든 서비스의 `networks` 항목에 `ipv4_address` 속성 필수 부여.
  - 지정된 그룹별 IP 대역(Lake: 140-149, Tooling: 220-249 등) 내 할당.
- **Allowed**:
  - 그룹별 여유 공간 활용한 신규 서비스 추가.
  - 일시적인 테스트 목적의 유동 IP 할당 (단, 수동 고정으로 머지 필수).
- **Disallowed**:
  - 중복된 IP 할당 (Compose 파일 병합 단계에서 검증 필수).
  - 외부망 주소와의 브릿징 설정 수동 수정.

## Exceptions

- **K3d-hyhome Compatibility**: `k3d-hyhome` 네트워크는 마스터 노드 및 외부 게이트웨이 영역과의 호환성을 위해 기존 IP 체계를 예외적으로 유지하거나 별도 할당 방식을 적용할 수 있음.

## Verification

- `docker compose config` 명령을 통한 구문 검증.
- `grep -r "ipv4_address" infra/` 명령을 통한 모든 서비스의 고정 IP 상태 확인.
- `docker network inspect infra_net` 명령을 통한 런타임 IP 할당 비교.

## Review Cadence

- **Monthly**: IP 맵핑 테이블(Sheet/Doc)과 현재 Compose 파일 사이의 실태 점검 및 업데이트.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [Operations index](../README.md)
- [Operations template](../../99.templates/operation.template.md)
