# Vault Operations Policy

> Operational and security policies for the Vault authentication and secrets management layer.

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 보안 심장부인 Vault의 운영 정책을 정의한다. Unseal Key의 관리 체계, 토큰 수명(TTL), 그리고 보안 감사(Audit Logging) 절차를 포함하여 시스템의 무결성을 보장한다.

## Policy Type

`security-policy | operational-standard`

## Target Audience

- Security Administrators
- SRE / Platform Engineers
- Compliance Auditors

## Service SLOs

- **Availability**: 99.99% (Raft Cluster 가용성 유지)
- **Data Integrity**: Zero data loss (Raft 스냅샷 및 분산 합의 보장)

## Operational Procedures

### 1. Unseal Key Management
- **Key Division**: 초기화 시 생성된 5개의 Unseal 키는 서로 다른 관리자(또는 독립된 보안 스토리지)에 분산 보관해야 함.
- **Quorum**: Vault 기동 시 최소 3개의 키가 제공되어야 봉인이 해제됨.
- **Rotation**: 정기적인 운영 점검 시 Unseal 키의 상태를 확인하고 필요 시 리키(Rekey) 수행.

### 2. Token & AppRole TTL Policy
- **Root Token**: 초기 부트스트래핑 완료 후 즉시 파기하거나 엄격히 격리함.
- **AppRole**: 애플리케이션용 AppRole의 토큰 TTL은 최대 24시간을 초과할 수 없으며, 자동 갱신(Renewable) 정책을 적용함.
- **User Token**: OIDC를 통해 발급된 유저 토크느은 1시간 단위로 갱신을 요구함.

### 3. Audit Logging Strategy
- **File Audit**: 모든 Vault API 요청은 `/vault/logs/audit.log`에 JSON 형태로 기록됨.
- **Integrity**: 감사 로그는 수정 불가능한 상태로 보관되어야 하며, 외부 SIEM 또는 중앙 로그 시스템으로 즉시 전송됨.

## Security Controls

- **Encryption at Rest**: 모든 데이터는 Raft 스토리지에 암호화되어 저장됨.
- **Network Isolation**: Vault API는 내부망(`infra_net`)에서만 직접 접근이 가능하며, 외부는 Traefik의 Strict TLS를 통해서만 허용됨.

## Related Documents

- **Guide**: `[../../07.guides/03-security/vault.md]`
- **Runbook**: `[../../09.runbooks/03-security/vault.md]`
- **Spec**: `[../../04.specs/03-security/spec.md]`
