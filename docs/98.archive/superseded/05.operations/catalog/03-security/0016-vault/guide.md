---
title: "Vault Legacy Migration Guide"
version: "1.0.1"
type: "operation/guide"
status: "superseded"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0016"
parent_ids:
- "POL-0016"
implementation_services:
  infra/03-security/vault/docker-compose.yml:
  - vault
  - vault-agent
superseded_by: "GDE-0085"
created: "2026-05-10"
---

# Vault Legacy Migration Guide

## Usage

### Implementation Sources

- [infra/03-security/vault/docker-compose.yml](../../../../../infra/03-security/vault/docker-compose.yml)

### Overview

Vault와 `vault-agent`는 **MIGRATE** 대상이며 `legacy-vault` profile에서만 선택된다. HOME의 상시 비밀 관리 기준은 OpenBao와 `openbao-agent`다. 이 문서는 기존 Vault 의존성을 조사하고 전환 준비를 관리한다. 구성 변경은 실제 데이터 이전, 초기화, unseal 또는 자격 증명 교체 완료를 의미하지 않는다.

### Prerequisites

저장소 루트에서 실행한다. 운영자는 기존 Vault 소비자, 보존 데이터, 키 관리 책임자와 복구 가능성을 먼저 확인한다. 데이터 존재·백업·복원 성공 여부는 아직 검증되지 않았다.

### Step-by-step Instructions

1. 공개 선언을 검사하고 선택된 서비스를 확인한다.

   ```bash
   docker compose --env-file .env.example --profile legacy-vault config --services
   docker compose --env-file .env.example --profile core config --services
   bash scripts/hardening/check-all-hardening.sh 03-security
   ```

2. Vault 주소와 Agent 출력에 의존하는 소비자를 목록화한다. 비밀 값 대신 서비스명, 경로 계약, 담당자, 전환 순서만 기록한다.
3. 이미 실행 중인 legacy 인스턴스에 대한 운영 점검이 허용된 경우 다음 상태 조회를 사용한다.

   ```bash
   docker compose --profile legacy-vault ps vault vault-agent
   docker compose --profile legacy-vault exec vault vault status
   ```

   `vault status` 종료 코드 0은 unsealed, 2는 sealed, 1은 오류다. Compose healthcheck는 sealed/uninitialized 응답도 허용하므로 healthy를 비밀 제공 가능 상태로 해석하지 않는다.
4. 기존 데이터와 대상 OpenBao 저장소를 분리한 채, 호환성·백업 복원·인증 방식·정책·Agent 템플릿의 전환 계획을 검토한다. 공식 migration 문서는 제한된 Vault CE 조합만 검증하므로 현재 선언 이미지에 대한 저장소 호환성을 추정하지 않는다.
5. 새 소비자와 초기 구축은 [OpenBao 가이드](../0085-openbao/guide.md)를 따른다. legacy Vault의 AppRole bootstrap, 토큰 발급 또는 강제 재초기화를 반복하지 않는다.

## Common Checks

- Vault 서비스 선택 profile은 `legacy-vault`이고 OpenBao는 `core` 및 `security`에 포함되는지 확인한다.
- `${DEFAULT_SECURITY_DIR}/vault/{data,agent,out}`과 OpenBao 저장소가 공유되지 않는지 선언을 검토한다.
- 상태 점검 결과, 실제 데이터 검증 여부와 정적 검증 결과를 구분한다.

## Runbook Handoff

전환 중 seal, 인증, 렌더링 또는 소비자 오류가 발생하면 [런북](runbook.md)의 중단·복구 판단을 따른다.

### Legacy Data Protection

Vault integrated-storage state and its unseal/recovery material are separate
recovery authorities. An operator-authenticated Raft snapshot protects the data;
the threshold key custodians protect the ability to unseal. Keep both outside the
container and never place either in Git or task evidence. Before migration or
image change, capture a protected snapshot and rehearse restore into isolated
storage with the same seal configuration and supported image. This repository has
not proven an online Vault-to-OpenBao data conversion.

## Traceability

- Declared parent: [03-Security Vault Operations Policy](policy.md) (`POL-0016`)
- Governing authority: [Security Tier Architecture Description](../../../../02.architecture/descriptions/0003-security-architecture.md) (`AD-0003`)
- Subject peers: [Policy](policy.md) (`POL-0016`), [Runbook](runbook.md) (`RUN-0016`)

## Related Documents

- [Vault Compose](../../../../../infra/03-security/vault/docker-compose.yml), [OpenBao Compose](../../../../../infra/03-security/openbao/docker-compose.yml): runtime 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [OpenBao 운영 가이드](../0085-openbao/guide.md), [정책](policy.md), [가이드](guide.md), [런북](runbook.md).
- [Vault status 공식 문서](https://developer.hashicorp.com/vault/docs/commands/status).
- [OpenBao 공식 마이그레이션 제약](https://openbao.org/docs/next/guides/migration/): development 문서이므로 적용할 릴리스의 지원 범위를 별도로 확인한다.
