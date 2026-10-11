---
title: "OpenBao Implementation"
version: "0.1.8"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
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

- `config/`: [Agent 설정](config/agent.hcl)과 template 소스를 담은 디렉터리입니다.
- `config/policies/`: 추적되는 ACL 정책입니다. 운영자가 적용하며 컨테이너에 mount하지 않습니다.
  - [renderer](config/policies/renderer.hcl): Agent AppRole이며 렌더링되는 두 KV data와 해당 metadata 경로를 읽습니다.
  - [operator](config/policies/operator.hcl): `hy-home-operator`, OIDC 사용자용 정책입니다. Prometheus API credential 교체와 Kiali Grafana token 재발급을 포함합니다.
  - [prometheus](config/policies/prometheus.hcl): SEC-002 scrape token이며 `sys/metrics`만 읽습니다.
  - [eso-read-platform](config/policies/eso-read-platform.hcl): hy-home.k8s External Secrets용이며 `secret/platform/{argocd,postgres-app,notifications,prometheus-api,grafana-api}`를 읽습니다.
  - [k8s-bootstrap](config/policies/k8s-bootstrap.hcl): 수명이 짧은 클러스터 bootstrap token입니다.
- [docker-compose.yml](docker-compose.yml)
- [소비자 이관 계약](consumer-migration/README.md): 값 없는 wave·receipt schema와
  합성 검증 경로입니다. 실제 pilot·복구·삭제·회전은 별도 수용 증거가 필요합니다.

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)와 그것이 참조하는 build 소스에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 투영이며 배포 매니페스트가 아닙니다.

## Configuration

| Service | Profiles | Networks | `edge_net`, `obs_net`, `secrets_net` | Secret references |
| --- | --- | --- | --- | --- |
| `openbao` | `security, secrets, core, local, dev` | `secrets_net, edge_net, obs_net` | 호스트 게시 없음 | Compose Secret 부여 없음; 구성된 bootstrap 파일 메타데이터를 확인하십시오 |
| `openbao-agent` | `security, secrets, core, local, dev` | `secrets_net` | 호스트 게시 없음 | Compose Secret 부여 없음; 구성된 bootstrap 파일 메타데이터를 확인하십시오 |

Persistence:

- `openbao-data`: `${DEFAULT_SECURITY_DIR}/openbao/data`
- `openbao-audit`: `${DEFAULT_SECURITY_DIR}/openbao/audit`
- `openbao-agent-data`: `${DEFAULT_SECURITY_DIR}/openbao/agent`
- `openbao-agent-out`: `${DEFAULT_SECURITY_DIR}/openbao/out`

환경 키 이름과 기본값은 Compose와 [공개 환경 예시](../../../.env.example)에 선언되어 있습니다. Compose의 마운트 권한과 healthcheck 명령은 구현을 설명할 뿐이며 설정 검사 통과가 runtime 준비 완료를 증명하지는 않습니다. 비공개 환경 값, credential 파일, 원본 렌더링된 설정은 출력하지 마십시오.

### P01 native trust and bootstrap

내부 endpoint는 `https://openbao:${OPENBAO_PORT:-8200}`이며 Agent·metrics·Gatus·Traefik이
같은 port와 검증된 CA를 사용합니다. 외부 custody의 `ca.pem`, `server.pem`,
`server-key.pem`을 `${DEFAULT_SECURITY_DIR}/openbao/tls`에 먼저 준비하며 SAN `DNS:openbao`와 `IP:127.0.0.1`을
요구합니다. 이 source 경로는 실제 인증서 발급/존재를 뜻하지 않습니다.
[start-server](./scripts/start-server.sh), [start-agent](./scripts/start-agent.sh),
[health-agent](./scripts/health-agent.sh), [wrapped reissue](./scripts/issue-renderer-secret-id.sh)가
port/trust·새 인증·제한 fetch/render 경계를 구현합니다.
SEC01 candidate는 server·Agent·snapshot CLI를 2.7.1로 정렬합니다. operator의 직접 SecretID
발급을 제거하고 5분 비갱신 issuer/cleanup role로 분리합니다. host helper는 Agent volume 밖의
영속 journal을 API 호출 전에 기록하며 새 process 기능 readiness와 accessor 정합화 후에만
완료합니다. source checkout은 신뢰 설치 경로가 아니므로
[installer](./scripts/install-renderer-issuer.sh)는 승인 commit의 blob에서 읽고,
`RUN-0085`의 operator-private 설치 절차를 따릅니다. checkout의 installer를 직접 실행하지 않습니다.
격리 시험은 HOME 배포·cold boot·독립 custody 확인과 별개입니다. 실제 consumer 적용은 별도입니다.

config-owned HMAC audit는 `openbao-audit`에 기록합니다. 한 backend가 실패하면 audited
요청이 차단될 수 있어 외부 rotation/용량/알림이 필요합니다. HOME custody·cold boot·
실제 복구는 운영 Runbook `RUN-0085`([운영 문서 인덱스](../../../docs/05.operations/README.md))을 따르며
P06 확대 전제입니다. 임시 고정 버전 시험은 HOME 완료 증거가 아닙니다.

### P01 versioned issuance journal compatibility

새 발급은 journal 문서에 `schema_version: 2`와 `issuance_id`를 기록합니다.
`issuance_id`는 기존 `nonce`와 같은 값인 호환 별칭이며, accessor metadata에는
`issuance_schema: "2"`, `issuance_id`, 기존 `sec01_nonce`를 함께 기록합니다. 둘의 값은
반드시 같아야 합니다. 과거 v1 journal과 anchor는 version 필드 없이 기존 정확한 형태로
읽을 때 byte를 보존하고, 상태 또는 generation을 갱신할 때도 legacy 형태로 저장합니다.

journal과 활성 anchor는 version·identity가 정확히 일치해야 하며, 실제 accessor metadata는
해당 journal version에서 유도한 전체 metadata와 정확히 일치해야 합니다. v1/v2 혼합,
별칭 불일치, 중복 accessor는 어떤 accessor도 폐기하기 전에 차단합니다. completion witness는
중단된 정리의 복구를 허용하는 별도 기록입니다. 이전 발급을 정합화한 같은 실행은 새 ID를
발급하지 않습니다. 이는 source 계약이며, 실제 HOME 대상·custody·복구 입력은 아직 확정되지
않았습니다.

### P02 공개 secret catalog

[secret-catalog.json](secret-catalog.json)과 [schema](secret-catalog.schema.json)는 값 없는
공개 분류·보존·미결정 mapping을 소유합니다. 각 항목의 원본 기록 날짜와 실행 증거를
구분하며, 계획된 mount·field·UID/GID·mode는 미확정입니다. ACL·delivery·reload·restart·
rotation의 `BLOCKED_P01`은 실제 권한이나 전달 완료가 아닙니다.

[catalog CLI](../../../scripts/operations/secret-catalog.py)는 catalog, schema, 기존 공개
secret 표, support matrix 네 추적 입력을 검사합니다. `render`는 승인된
`.agent-work/p02-views` 안에 공개 예시·값 없는 local view·JSON summary·README 네 파일만
씁니다. 해당 staging 파일은 credential 원본이나 운영 파일로 사용하지 않습니다.
실제 명령과 중단 조건은 기존 `RUN-0085`가 소유하며 운영 문서 인덱스를 통해 접근합니다.

canonical `COMM-002`와 source-retired alias `COMM-003`의 재생성을 거부합니다.
alias는 별도 credential 또는 KV 대상을 만들지 않으며 실제 파일 폐기는 SMTP01 소관입니다.
공개 catalog와 합성 검사 통과는 HOME 인증·소비·이관·rotation·복구를 증명하지 않습니다.

## Validation

저장소 루트에서 문서화된 profile을 선택해 `scripts/validation/validate-docker-compose.sh`를 사용하십시오. 대상 runtime 확인과 승인 후 복구는 소유 운영 Runbook을 사용하십시오. 누락된 마운트, 예기치 않은 노출, 초기화 실패 시 중단하십시오.

## Usage

Compose, build 소스, 공개 환경 키, secret 참조를 일관되게 유지하십시오. 변경 전에 gateway 인증, 지속성, 리소스 예산, 버전 예외를 검토하십시오. 여기에 명령을 중복 작성하지 말고 기존 운영 subject를 갱신하십시오.

## Related Documents

- [인프라 인덱스](../../../infra/README.md)
- [문서 인덱스](../../../docs/README.md)
- [공개 secret 계약](../../../secrets/README.md)
