# Security Operations Policy (03-security)

> Vault Secret Governance & Audit Standards (03-security)

## Overview

이 문서는 `hy-home.docker` 보안Tier(03-security)의 운영 원칙과 통제 기준을 정의한다. Vault를 통한 시크릿 관리의 안전성을 보장하기 위한 규칙을 포함한다.

## Policy Goals

- **Integrity**: 시크릿 데이터의 무결성 보장.
- **Confidentiality**: 접근 권한이 없는 자의 시크릿 접근 차단.
- **Auditability**: 모든 시크릿 접근 및 관리 행위의 추적성 확보.

## Operational Standards

### 1. Unseal Key 관리 정책

- **분산 보관**: 5개의 Unseal Key 조각 중 3개 이상이 있어야 해제가 가능하므로, 각 키 조각은 서로 다른 신뢰할 수 있는 관리자가 분산 보관해야 한다.
- **저장 금지**: 키 조각을 절대 git 저장소, 클라우드 메모장, 또는 일반 평문 파일로 저장하지 않는다.
- **긴급 대응**: 키 조각 보유자의 부재 시를 대비하여 비상 오프라인 보관 절차를 수립한다.

### 2. 접근 제어 (Access Control)

- **Root Token**: 초기화 후 Root Token은 관리자 계정 생성 및 정책 설정 시에만 일시적으로 사용하며, 작업 직후 폐기 또는 안전하게 봉인한다.
- **Least Privilege**: 모든 서비스와 사용자는 최소 권한 원칙에 기반한 Vault Policy를 부여받아야 한다.
- **Authentication**: `AppRole`(서비스용) 및 `Userpass` 또는 `OIDC`(사람용) 인증 방식을 우선 사용한다.

### 3. 감사 및 모니터링

- **Audit Log**: Vault의 Audit Log 기능을 활성화하여 모든 API 요청을 기록한다.
- **Alerting**: Vault 봉인(Sealed) 상태로 남겨진 경우 및 지속적인 인증 실패 시 즉시 알림을 발생시킨다.

## Verification

- [ ] 정기적인 Unseal Key 점검 (Key Ceremony).
- [ ] 미사용 Token 및 권한의 주기적인 정리(Revocation).
- [ ] Raft 스냅샷 백업의 무결성 정기 확인.

## Related Documents

- **ARD**: `[../02.ard/03.security.md]`
- **Runbook**: `[../09.runbooks/03-security/README.md]`
