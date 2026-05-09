<!-- Target: docs/08.operations/09-tooling/locust.md -->

# Locust Operations Policy

> Locust 기반 성능 테스트 인프라의 운영 안정성 및 거버넌스 지침입니다.

---

## Overview (KR)

이 문서는 로드 테스팅 수행 시 발생할 수 있는 부작용(운영 서비스 영향 등)을 방지하고, 성능 데이터의 신뢰성을 보장하기 위한 운영 정책을 정의합니다.

## Target Audience

- Operator
- Performance Engineer
- SRE

## Policy Goals

- **가용성 보존**: 대규모 테스트 중 Gateway 등 인프라 코어의 무결성 유지.
- **지표 무결성**: InfluxDB에 전송되는 데이터의 일관성 및 정확성 확보.
- **비용 최적화**: 테스트 미수행 시 워커 노드의 유휴 자원 최소화.

## Operational Standards

### 1. 테스트 실행 거버넌스 (Governance)

- **사전 승인**: 초당 5,000 요청 이상의 부하 테스트는 정기 유지보수 윈도우(02:00 ~ 04:00)에 수행하는 것을 권장함.
- **정의된 시나리오**: 모든 테스트는 Git에 관리되는 `locustfile.py`를 통해서만 수행해야 함.

### 2. 리소스 스케일링 정책 (Scaling)

- 테스트 종료 후 즉시 워커 노드를 기본값(`replicas: 2`)으로 축소해야 함.
- CPU/Memory 임계치(`template-infra-med`) 초과 시, 추가 수직 스케일링을 배포 설정에 반영해야 함.

### 3. 데이터 보존 및 보안 (Data & Security)

- **지표 보존**: InfluxDB 내의 부하 테스트 데이터는 90일간 보존하며, 이후 아카이빙함.
- **접근 통제**: 외부 부하 생성(External Load) 시, 반드시 인증 토큰 및 레이트 리밋 설정을 적용하여 무단 접근을 방지함.

## Security Controls

- **Secret Management**: InfluxDB API 토큰은 Docker Secret으로만 주입하며, 환경 변수에 평문 노출을 금지함.
- **Endpoint Protection**: Locust UI는 내부 어드민 망 또는 VPN 환경에서만 노출되도록 Gateway에서 제어함.

## Related Documents

- **Guide**: [Locust Load Testing Guide](../../07.guides/09-tooling/locust.md)
- **Runbook**: [Locust Recovery Runbook](../../09.runbooks/09-tooling/locust.md)

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
