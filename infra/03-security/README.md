---
title: "Security Tier (03-security)"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-12"
---

# Security Tier (03-security)

## Overview

HOME의 canonical 비밀 관리 서비스는 OpenBao와 `openbao-agent`다. Vault와 `vault-agent`는 MIGRATE 대상으로 보존하며 `legacy-vault`를 명시적으로 선택한 이전·복구 작업에 사용한다. 이 구성은 기존 비밀 데이터의 이전 또는 실제 unseal 완료를 주장하지 않는다.

## Audience

Security owner, 인프라 운영자, 서비스 개발자와 자동화 담당자.

## Scope

OpenBao 상시 서비스의 선언, legacy Vault 전환 경계, Agent 출력 계약과 운영 문서 연결을 소유한다. 비밀 원문·키 관리 자료와 자동 자격 증명 회전은 포함하지 않는다.

## Structure

| 경로 | 책임 |
| --- | --- |
| [openbao/](openbao/README.md) | HOME canonical 서버와 Agent |
| [vault/](vault/README.md) | MIGRATE legacy 서버와 Agent |

## How to Work in This Area

1. 새 소비자는 [OpenBao 가이드 — 문서 인덱스](../../docs/README.md) (`GDE-0085`)를 따른다.
2. 기존 Vault 소비자는 [legacy 전환 가이드 — 문서 인덱스](../../docs/README.md) (`GDE-0016`)로 목록화하고 단계적으로 이전한다.
3. 원본 Vault와 OpenBao 데이터 경로를 분리한다. 백업·복원 및 현재 데이터 상태는 별도 검증 전까지 미확인으로 기록한다.
4. seal 상태, Agent 인증 및 소비자 연결을 각각 확인한다. healthcheck 성공만으로 전체 준비 완료를 판단하지 않는다.

## Tech Stack

실행 이미지·profile·마운트의 원본은 [OpenBao Compose](openbao/docker-compose.yml)와 [Vault Compose](vault/docker-compose.yml)다. [Derived Compose image projection](../tech-stack.versions.json)은 선언 drift 검증을 제공한다.

## Configuration

OpenBao는 `core`, `local`, `dev`, `security`, `secrets`에서 선택된다. Vault는 `legacy-vault`에만 포함된다. `${DEFAULT_SECURITY_DIR}/openbao`와 `${DEFAULT_SECURITY_DIR}/vault` 경로를 공유하지 않는다. 외부 UI는 각각 `openbao.${DEFAULT_URL}`, `vault.${DEFAULT_URL}`이다.

## Testing

저장소 루트에서 공개 예시 환경만 사용해 정적 구성과 하드닝을 검사한다.

```bash
docker compose --env-file .env.example --profile core config --services
docker compose --env-file .env.example --profile legacy-vault config --services
bash scripts/hardening/check-all-hardening.sh 03-security
```

## Change Impact

인증·템플릿·endpoint 변경은 소비자의 비밀 공급에 영향을 준다. 원본 데이터 삭제, 저장소 공유, 재초기화 또는 키 회전을 구성 정리와 함께 수행하지 않는다.

## Related Documents

- [OpenBao 정책 — 문서 인덱스](../../docs/README.md) (`POL-0085`), [OpenBao 런북 — 문서 인덱스](../../docs/README.md) (`RUN-0085`).
- [Vault 정책 — 문서 인덱스](../../docs/README.md) (`POL-0016`), [Vault 런북 — 문서 인덱스](../../docs/README.md) (`RUN-0016`).
- [OpenBao migration 제약](https://openbao.org/docs/next/guides/migration/), [Vault status](https://developer.hashicorp.com/vault/docs/commands/status).
- [Infrastructure index](../README.md).
