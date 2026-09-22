---
title: "Vault Legacy Migration Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "superseded"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0016"
parent_ids:
- "GDE-0016"
superseded_by: "RUN-0085"
created: "2026-05-17"
---

# Vault Legacy Migration Runbook

## Overview

`legacy-vault`로 남겨 둔 Vault와 Agent의 상태를 확인하고 OpenBao 전환 중단·복구를 판단하는 절차다. 실제 데이터 이전 및 복원은 검증되지 않았다.

## When to Use

legacy 소비자의 인증 실패, Vault seal 상태, Agent 렌더 중단 또는 OpenBao 전환 점검 실패 시 사용한다.

## Procedure

1. 저장소 루트에서 정적 경계를 확인한다.

   ```bash
   docker compose --env-file .env.example --profile legacy-vault config --services
   bash scripts/hardening/check-all-hardening.sh 03-security
   ```

2. 운영 점검이 허용된 기존 실행 인스턴스만 조회한다.

   ```bash
   docker compose --profile legacy-vault ps vault vault-agent
   docker compose --profile legacy-vault exec vault vault status
   ```

3. status 종료 코드 2는 sealed이며 장애 원인과 키 관리자를 확인한다. 실제 threshold를 확인하지 않은 고정 횟수 unseal, 재초기화, key 재발급을 실행하지 않는다.
4. 소비자 주소, 정책 참조, Agent 템플릿과 출력 경로를 공개 선언과 비교한다. 원시 token, SecretID 또는 렌더 출력 파일을 열어 증거로 수집하지 않는다.
5. 마이그레이션 작업 중이면 후속 소비자 전환을 멈추고 원본 Vault 상태, 대상 OpenBao 상태, 마지막 성공 검증을 구분한다.
6. [OpenBao 런북](../0085-openbao/runbook.md)에서 대상 서비스 검증을 수행할 운영자에게 인계한다.

## Evidence

선택 profile, 서비스 상태, seal 여부, 종료 코드, 최근 공개 구성 변경, 실패한 소비자와 담당자를 기록한다. 로그 검토가 필요하면 운영자가 제한된 범위에서 비밀을 제거한 요약만 공유한다. 데이터 백업·복원 증거가 없으면 미검증으로 표시한다.

## Rollback or Recovery

승인된 운영자 token으로 Vault Raft snapshot을 보호된 경로에 생성하고 checksum,
cluster identity, image declaration, seal configuration을 기록한다. restore는 network
egress와 소비자 접근이 차단된 새 data path에서만 수행하고, 같은 threshold 절차로
unseal한 뒤 mount/policy/secret metadata와 대표 비밀의 존재를 값 노출 없이 확인한다.
그 후에야 consumer 전환 판단을 한다. 소비자 endpoint 변경을 되돌리는 것은 기존
Vault가 계속 사용 가능하고 새 쓰기의 처리 방침이 확인된 경우에만 수행한다.
OpenBao 데이터를 Vault 경로에 복사하거나 동일 볼륨으로 재시작하지 않는다.
검증된 데이터 역이전 절차는 없으며 legacy 저장소와 키 자료는 삭제하지 않는다.
이 snapshot restore rehearsal은 2026-09-20 문서 교정 중 실행되지 않았다.

## Escalation

seal 해제, 자격 증명 발급·회전, 데이터 복원·삭제 또는 호환성 불명이 남으면 Security owner에게 인계한다. 상태와 마지막 성공 지점, 소비자 영향, 필요한 결정을 포함한다.

## Traceability

- Declared parent: [03-Security Vault Usage Guide](guide.md) (`GDE-0016`)
- Governing authority: [Security Tier Architecture Description](../../../../02.architecture/descriptions/0003-security-architecture.md) (`AD-0003`)
- Subject peers: [Guide](guide.md) (`GDE-0016`), [Policy](policy.md) (`POL-0016`)

## Related Documents

- [Vault Compose](../../../../../infra/03-security/vault/docker-compose.yml), [OpenBao Compose](../../../../../infra/03-security/openbao/docker-compose.yml): runtime 선언 원본.
- [Curated version projection](../../../../../infra/tech-stack.versions.json): 선언 drift 확인.
- [OpenBao 운영 가이드](../0085-openbao/guide.md), [정책](policy.md), [가이드](guide.md), [런북](runbook.md).
- [Vault status 공식 문서](https://developer.hashicorp.com/vault/docs/commands/status).
- [OpenBao 공식 마이그레이션 제약](https://openbao.org/docs/next/guides/migration/): development 문서이므로 적용할 릴리스의 지원 범위를 별도로 확인한다.
