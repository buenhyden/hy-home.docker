---
title: "OpenBao Implementation"
version: "0.1.3"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
---

# OpenBao

## Overview

secret 제어 평면은 Raft storage와 AppRole Agent를 사용합니다. bootstrap 의존성이며 sealed 컨테이너의 healthcheck 통과가 secret 전달 준비 완료를 의미하지는 않습니다.

Lifecycle: **HOME**. 루트 Compose가 이 정의를 include하며, 명시적 profile이 활성화를 제어합니다.

## Audience

구현, 설정, 검증을 검토하는 Operator와 Developer.

## Scope

로컬 서비스 정의와 구현 내비게이션을 다룹니다. 운영 통제와 복구는 `GDE-0085`, `POL-0085`, `RUN-0085`(OpenBao 운영 가이드/정책/런북) 소관이며 [문서 인덱스](../../../docs/README.md)를 통해 접근합니다.

## Structure

- `config/`: [Agent 설정](config/agent.hcl)과 template 소스를 담은 디렉터리입니다. ACL 정책과 template 원본 파일 목록은 `config/`의 내용을 확인하십시오.
- [docker-compose.yml](docker-compose.yml)

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)와 그것이 참조하는 build 소스에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 투영이며 배포 매니페스트가 아닙니다.

## Configuration

| Service | Profiles | Networks | `edge_net`, `obs_net`, `secrets_net` | Secret references |
| --- | --- | --- | --- | --- |
| `openbao` | `security, secrets, core, local, dev` | `secrets_net, edge_net, obs_net` | 호스트 게시 없음 | Compose Secret 부여 없음; 구성된 bootstrap 파일 메타데이터를 확인하십시오 |
| `openbao-agent` | `security, secrets, core, local, dev` | `secrets_net` | 호스트 게시 없음 | Compose Secret 부여 없음; 구성된 bootstrap 파일 메타데이터를 확인하십시오 |

Persistence:

- `openbao-data`: `${DEFAULT_SECURITY_DIR}/openbao/data`
- `openbao-agent-data`: `${DEFAULT_SECURITY_DIR}/openbao/agent`
- `openbao-agent-out`: `${DEFAULT_SECURITY_DIR}/openbao/out`

환경 키 이름과 기본값은 Compose와 [공개 환경 예시](../../../.env.example)에 선언되어 있습니다. Compose의 마운트 권한과 healthcheck 명령은 구현을 설명할 뿐이며 설정 검사 통과가 runtime 준비 완료를 증명하지는 않습니다. 비공개 환경 값, credential 파일, 원본 렌더링된 설정은 출력하지 마십시오.

## Validation

저장소 루트에서 문서화된 profile을 선택해 `scripts/validation/validate-docker-compose.sh`를 사용하십시오. 대상 runtime 확인과 승인 후 복구는 소유 운영 Runbook을 사용하십시오. 누락된 마운트, 예기치 않은 노출, 초기화 실패 시 중단하십시오.

## How to Work in This Area

Compose, build 소스, 공개 환경 키, secret 참조를 일관되게 유지하십시오. 변경 전에 gateway 인증, 지속성, 리소스 예산, 버전 예외를 검토하십시오. 여기에 명령을 중복 작성하지 말고 기존 운영 subject를 갱신하십시오.

## Related Documents

- [인프라 인덱스](../../../infra/README.md)
- [문서 인덱스](../../../docs/README.md)
- [공개 secret 계약](../../../secrets/README.md)
