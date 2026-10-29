---
title: "OpenTofu Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "operations"
artifact_id: "GDE-0082"
parent_ids:
- "POL-0082"
implementation_services:
  infra/09-platform-ops/opentofu/docker-compose.yml:
  - opentofu
created: "2026-09-19"
---

# OpenTofu Guide

## Overview

OpenTofu는 `infra/09-platform-ops/opentofu/`의 `opentofu` service로 요청 시 실행하는 DEV IaC CLI 작업이다.
`iac` profile에서만 선택된다.

## Scope

### Audience and Goal

대상 독자는 IaC plan과 apply를 승인하고 실행하는 운영자다. 목표는 실행 경계, state와 명령의 의미,
일반 사용 순서를 확인하는 것이다. state 복구와 lock 진단은 [OpenTofu Runbook](../../runbooks/10-platform-and-backup/0082-opentofu.md)이 맡는다.

## Concepts

### 실행 경계

OpenTofu는 요청 시 실행하는 DEV IaC CLI 작업이다. `iac` profile에만 속하며
HOME과 일반 `tooling`에서는 제외된다. root project는 inline Dockerfile로 로컬
이미지를 빌드하고 `./workspace`를 `/workspace`에 read-write로 마운트하며,
운영자의 AWS와 Azure credential 디렉터리를 read-only로 마운트한다. read-only
credential 마운트라도 원격 API 권한을 부여한다.

이 작업에는 daemon healthcheck가 없고 `restart: "no"`이다. `template-job-low`가
resource/security 기준선을 정의한다. 선언된 기본 네트워크의 도달 가능성을 별도로 확인한다. private `object_net`의
tfstate endpoint에는 자동으로 연결되지 않으며 네트워크 추가는 별도 검토가 필요하다. 이 leaf에는 Docker secret이나 공개된 port가 없다.

## Usage

### State와 명령 의미

- 선택된 workspace 설정이 state를 `/workspace`의 로컬 파일로 둘지 원격
  backend로 둘지 결정한다. Compose 파일은 backend를 선택하지 않는다.
- `tofu plan`은 provider API와 state를 읽지만 관리 대상 리소스를 변경하지
  않는다. 그래도 state를 refresh하고 plan 출력에 민감한 값을 노출할 수 있다.
- `tofu apply`, `destroy`, `import`, `state push`, `force-unlock`, 그리고
  state 변경 작업은 원격/파괴적 행위이므로 정확한 별도 승인이 필요하다.
- Backend는 저장소를 제공하고 locking도 제공할 수 있다. locking을
  비활성화하지 않는다. `force-unlock`은 writer가 남아 있지 않다고 증명한
  후, 운영자 자신이 남긴 lock에만 사용한다.

### 일반적인 사용

1. repository root에서 작업하며 `infra/09-platform-ops/opentofu/workspace` 아래의
   정확한 디렉터리, backend, workspace 이름, account, 예상 리소스를 식별한다.
2. `docker compose --profile iac config --quiet`를 실행하고
   `docker compose --profile iac config --services`로 예상한 IaC service만
   있는지 확인한다.
3. 버전 조회도 credential·workspace를 마운트한 컨테이너를 만든다. 실행이 승인된
   경우에만 `docker compose --profile iac run --rm --no-deps opentofu version`을
   사용하며 소스만 읽는 정적 검사와 구분한다.
4. read-only provider/backend 권한으로 정확한 workspace에 대해 initialization,
   formatting, validation, 검토된 plan을 실행한다. plan과 state 파일은 Git
   밖의 보호된 경로에 보관하고 그 내용을 evidence에 붙여넣지 않는다.
5. 저장된 plan을 적용할지는 따로 결정한다. plan digest, 리소스 수,
   승인, exit status, apply 후 점검을 secret 없이 기록한다.

### 백업과 업그레이드

실행 순서와 실패·복구 판단은 [런북](../../runbooks/10-platform-and-backup/0082-opentofu.md)의 `상태 보존과 변경 전 검토` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Terraform 이관

기존 Terraform workspace를 옮기기 전에 state와 lock 정보를 보호한다. 독립 Terraform Compose 서비스가 없다는 사실은 Terrakube workspace의 엔진까지 OpenTofu로 고정되었다는 뜻이 아니다. Terrakube executor는 외부 도구·엔진 목록을 참조하므로 이관 대상별 실제 엔진, provider 및 state 호환성을 확인하고, Terraform configuration과 state가 자동으로 호환된다고 가정하지 않는다. 민감한 state와 plan payload는 문서나 로그에 넣지 않는다.

### Runbook Handoff

state 복구, lock 진단, plan/apply 분리, upgrade에는
[runbook](../../runbooks/10-platform-and-backup/0082-opentofu.md)을 사용한다.

### Traceability

- [Policy](../../policies/10-platform-and-backup/0082-opentofu.md) (`POL-0082`)
- [Runbook](../../runbooks/10-platform-and-backup/0082-opentofu.md) (`RUN-0082`)
- [OpenTofu Compose](../../../../infra/09-platform-ops/opentofu/docker-compose.yml)

## Troubleshooting

### Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac run --rm --no-deps opentofu version`
- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`

## Related Documents

- [OpenTofu provisioning workflow](https://opentofu.org/docs/cli/run/)
- [State storage and locking](https://opentofu.org/docs/language/state/backends/)
- [State locking](https://opentofu.org/docs/language/state/locking/)
- [Upgrade guide](https://opentofu.org/docs/intro/upgrading/)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)
- [Operations index](../../README.md)
