# Portainer Operations Policy

> Docker 관리 도구의 보안 노출 및 운영 정책 정의.

---

## Policy Scope

Portainer 인터페이스의 접근 제어, 데이터 백업, 리소스 관리 가이드라인.

## Applies To

- **Systems**: Portainer (Container Management)
- **Environments**: Infrastructure Management Area

## Controls

- **Access Control**:
  - 반드시 Traefik `sso-auth@file` 미들웨어를 통해 1차 인증을 수행해야 한다.
  - Portainer 내부 RBAC를 활성화하여 불필요한 관리자 권한 부여를 제한한다.
- **Data Persistence**:
  - `portainer_data` 볼륨은 `${DEFAULT_MANAGEMENT_DIR}/portainer`에 매핑되어야 하며, 시스템 백업 대상에 포함되어야 한다.
- **Resource Management**:
  - `sts` (Short Term Support) 이미지를 사용하여 보안 업데이트를 주기적으로 적용한다.

## Disallowed Actions

- Portainer 내부의 `docker.sock`을 외부에 API 형태로 노출하는 행위.
- `admin` 계정의 비밀번호를 평문으로 기록하거나 공유하는 행위.

## Verification

- **Security Scan**: 주기적으로 `docker.sock`에 대한 무단 접근 시도를 로깅하고 분석한다.
- **Connectivity**: `https://portainer.${DEFAULT_URL}` 접속 시 SSO 인증 창이 정상적으로 뜨는지 확인한다.

## Review Cadence

- Semi-annually (6개월 단위 정기 보안 리뷰)

## Related Documents

- **System Guide**: `[../../07.guides/11-laboratory/portainer.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/portainer.md]`

---

## Overview (KR)

이 문서는 `docs/08.operations/11-laboratory/portainer.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
