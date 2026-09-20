---
title: "Vault Legacy Migration Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0016"
parent_ids:
- "AD-0003"
created: "2026-05-17"
---

# Vault Legacy Migration Policy

## Overview

Vault는 MIGRATE 대상의 기존 비밀 저장소다. HOME의 canonical 비밀 관리 서비스는 OpenBao이며, 이 정책은 legacy 유지 기간의 데이터 보존과 전환 경계를 정의한다.

## Policy Scope

- `infra/03-security/vault/docker-compose.yml`의 `vault`, `vault-agent` 및 기존 소비자.
- `legacy-vault`를 명시적으로 선택한 이전·복구 작업.
- 새 OpenBao 구축은 [POL-0085](../0085-openbao/policy.md)가 소유한다.

## Controls

- Vault를 HOME `core`/`security` 상시 서비스로 다시 추가하지 않는다.
- 기존 저장소와 OpenBao 저장소를 분리한다. 현재 데이터·백업·복원 상태가 확인되지 않았으므로 공유 볼륨, 덮어쓰기, 삭제를 전환 기본 절차에 포함하지 않는다.
- 전환 전에 소비자 목록, 적용 버전의 upstream 호환성, 백업 복원 증거, key custody, 정책 및 인증 매핑, 되돌릴 시점을 기록한다.
- AppRole/token/unseal key와 렌더된 비밀을 공개 문서·로그·증거에 복사하지 않는다. 자격 증명 재발급·회전은 별도 운영 변경으로 다룬다.
- healthy는 API 과정의 생존 신호이며 unsealed·인증·소비자 연결 성공을 대신하지 않는다.
- 전환 완료는 소비자별 검증과 복구 가능한 상태를 확인한 후 선언한다. 이 문서 변경만으로 완료 처리하지 않는다.

## Exceptions

기존 소비자의 복구 또는 승인된 마이그레이션에 한해 `legacy-vault`를 사용한다. 기간·소유자·종료 기준을 작업 기록에 남긴다. 새 서비스의 legacy 의존성 추가는 허용하지 않는다.

## Verification

```bash
docker compose --env-file .env.example --profile legacy-vault config --services
docker compose --env-file .env.example --profile core config --services
bash scripts/hardening/check-all-hardening.sh 03-security
```

정적 검증과 실제 Vault 데이터·unseal·OpenBao 소비자 검증을 별도 증거로 기록한다.

### Backup and Migration Controls

- Preserve authenticated Raft snapshots and unseal/recovery shares under separate
  custodians. A healthy API is not backup evidence.
- Rehearse restore on isolated storage before migration or upgrade. Never run
  `operator init` over existing data or attach Vault and OpenBao to one data path.
- Keep the legacy source read-only or quiesced until every migrated consumer and
  rollback boundary is accepted. New writes after a cutover require a specific
  reconciliation plan; blind reverse copy is prohibited.

## Review Cadence

매월 및 소비자 전환, 저장소·인증 설정 변경 시 검토한다.

## Traceability

- Declared parent: [Security Tier Architecture Description](../../../../02.architecture/descriptions/0003-security-architecture.md) (`AD-0003`)
- Subject peers: [Guide](guide.md) (`GDE-0016`), [Runbook](runbook.md) (`RUN-0016`)

## Related Documents

- [Vault Compose](../../../../../infra/03-security/vault/docker-compose.yml), [OpenBao Compose](../../../../../infra/03-security/openbao/docker-compose.yml): runtime 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [OpenBao 운영 가이드](../0085-openbao/guide.md), [정책](policy.md), [가이드](guide.md), [런북](runbook.md).
- [Vault status 공식 문서](https://developer.hashicorp.com/vault/docs/commands/status).
- [OpenBao 공식 마이그레이션 제약](https://openbao.org/docs/next/guides/migration/): development 문서이므로 적용할 릴리스의 지원 범위를 별도로 확인한다.
