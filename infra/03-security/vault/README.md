---
title: "Vault Legacy Migration"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2026-01-15"
---

# Vault Legacy Migration

## Overview

Vault는 **MIGRATE** 대상이며 `legacy-vault` profile에서만 선택된다. HOME canonical 비밀 관리 서비스는 [OpenBao](../openbao/README.md)다. 이 leaf는 기존 데이터와 소비자 전환을 위한 선언을 보존한다. 데이터 이전·복원·unseal·자격 증명 회전은 아직 검증하거나 수행한 것으로 간주하지 않는다.

## Audience

Security owner, 기존 Vault 소비자 담당자와 인프라 운영자.

## Scope

`vault`, `vault-agent`의 legacy 설정, 상태 조회와 전환 문서를 연결한다. 신규 서비스의 Vault bootstrap이나 자동 데이터 migration은 범위 밖이다.

## Structure

- [docker-compose.yml](docker-compose.yml): profile, 저장소, healthcheck, ingress.
- `config/vault.hcl`: 서버 설정.
- `config/vault-agent.hcl`, `config/templates/`: 인증 및 렌더 선언.

## How to Work in This Area

[전환 가이드 — 문서 인덱스](../../../docs/README.md) (`GDE-0016`), [정책 — 문서 인덱스](../../../docs/README.md) (`POL-0016`), [런북 — 문서 인덱스](../../../docs/README.md) (`RUN-0016`)을 따른다. 기존 소비자의 endpoint·인증·템플릿 계약과 데이터 복구 가능성을 먼저 확인한다. 현재 이미지에 대한 OpenBao 저장소 호환성을 추정하지 않는다.

## Tech Stack

현재 pin은 [Vault Compose](docker-compose.yml)와 [derived Compose image projection](../../tech-stack.versions.json)을 참조한다. 대상 서비스의 선언은 [OpenBao Compose](../openbao/docker-compose.yml)다.

## Configuration

`vault-data:/vault/data`, `vault-agent-data:/vault/agent`, `vault-agent-out:/vault/out`은 `${DEFAULT_SECURITY_DIR}/vault` 아래 별도 저장소다. OpenBao 데이터 경로와 공유하지 않는다. Vault healthcheck는 sealed/uninitialized 상태도 허용하므로 인증된 소비자의 사용 가능 여부를 별도로 확인한다.

## Service Readiness

| Field | Evidence |
| --- | --- |
| Services / profile | `vault`, `vault-agent` / `legacy-vault` |
| Runtime authority | [Compose](docker-compose.yml), [root include](../../../docker-compose.yml) |
| Network / route | `infra_net`, 서버의 `k3d-hyhome`; `vault.${DEFAULT_URL}` |
| Data | 기존 Vault 데이터·백업·복원 성공 여부 미검증 |
| Health | 서버 API 생존 상태와 Agent 프로세스 상태; unseal·렌더·소비자 검증 별도 |
| Migration | HOME의 OpenBao 전환 준비, 실제 데이터 이전 완료 아님 |

## Testing

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile legacy-vault config --services
bash scripts/hardening/check-all-hardening.sh 03-security
```

이미 실행 중인 legacy 인스턴스 점검이 허용된 경우 `docker compose --profile legacy-vault exec vault vault status`를 사용한다. 종료 코드 0은 unsealed, 2는 sealed, 1은 오류다.

## Troubleshooting

seal 또는 Agent 장애는 런북으로 인계한다. 비밀 출력 파일이나 토큰을 로그에 복사하지 않으며, 임의 재초기화·SecretID 재발급·볼륨 삭제를 복구 기본값으로 사용하지 않는다.

## Related Documents

- [Security tier](../README.md).
- [Vault status 공식 문서](https://developer.hashicorp.com/vault/docs/commands/status).
- [OpenBao migration 제약](https://openbao.org/docs/next/guides/migration/): development 문서의 지원 조건을 적용 릴리스와 대조한다.
