# Laboratory Dashboard Operations Policy

> This document defines the operations policy, security controls, and governance for the laboratory dashboard (Homer).

---

## Overview (KR)

이 문서는 `11-laboratory` 티어의 서비스 대시보드(Homer)에 대한 운영 정책을 정의한다. 대시보드의 공개 범위, 신규 서비스 추가 프로세스, 보안 통제 기준을 규정하여 인프라 가시성과 안전성을 동시에 확보한다.

## Policy Scope

- Homer 대시보드 서비스 가용성.
- 대시보드 노출 서비스 선정 기준 및 관리 프로세스.
- 대시보드 접근 제어 및 보안 가드레일.

## Applies To

- **Systems**: Homer (Laboratory Dashboard)
- **Agents**: AI-Ops Agents (대시보드 업데이트 수행 시)
- **Environments**: Production-Management Area

## Controls

- **Required**:
  - 모든 대시보드 접근은 Traefik `sso-auth` 미들웨어를 통해 인증되어야 한다.
  - `config.yml` 변경 전 반드시 로컬에서 구문 검증(`yq` 등)을 거쳐야 한다.
  - 대시보드에 신규 관리 도구 추가 시 해당 도구의 인증 설정 여부를 선제적으로 확인해야 한다.
- **Allowed**:
  - 실험적 서비스의 일시적 등록 (단, 'Lab' 태그 부착 필수).
  - 테마 및 레이아웃의 자유로운 변경 (UI Guidelines 준수 범위 내).
- **Disallowed**:
  - 인증이 없는 데이터베이스 유틸리티나 민감 정보가 포함된 UI를 대시보드에 직접 노출하는 행위.
  - 공개 망(Internet)으로의 정적 배포 (인프라 전용 대시보드 용도 제한).

## Exceptions

- 초기 설정 및 긴급 복구 단계에서의 일시적 비인증 접근은 30분 이내로 제한하며, 작업 완료 후 반드시 인증을 활성화한다.

## Verification

- `yq eval . config/config.yml` 명령을 통한 설정 파일 무결성 확인.
- Traefik 라우터 설정에서 `sso-auth` 적용 여부 교차 검증.

## Review Cadence

- Quarterly (매 분기 대시보드 링크 유효성 및 보안 정책 리뷰).

## Related Documents

- **ARD**: `[../../02.ard/03-security.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/dashboard.md]`
- **Implementation**: `[../../../infra/11-laboratory/dashboard/README.md]`
