---
title: "OpenTofu Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0082"
parent_ids:
- "POL-0082"
implementation_services:
  infra/09-tooling/opentofu/docker-compose.yml:
  - opentofu
created: "2026-09-19"
---

# OpenTofu Guide

## Usage

### Purpose and runtime boundary

OpenTofu는 요청 시 실행하는 DEV IaC CLI 작업이다. `iac` profile에만 속하며
HOME과 일반 `tooling`에서는 제외된다. root project는 inline Dockerfile로 로컬
이미지를 빌드하고 `./workspace`를 `/workspace`에 read-write로 마운트하며,
운영자의 AWS와 Azure credential 디렉터리를 read-only로 마운트한다. read-only
credential 마운트라도 원격 API 권한을 부여한다.

이 작업에는 daemon healthcheck가 없고 `restart: "no"`이다. `template-job-low`가
resource/security 기준선을 정의한다. 선언된 network는 provider/backend 네트워크
접근을 허용한다. 이 leaf에는 Docker secret이나 공개된 port가 없다.

### State and command semantics

- 선택된 workspace 설정이 state를 `/workspace`의 로컬 파일로 둘지 원격
  backend로 둘지 결정한다. Compose 파일은 backend를 선택하지 않는다.
- `tofu plan`은 provider API와 state를 읽지만 관리 대상 리소스를 변경하지
  않는다. 그래도 state를 refresh하고 plan 출력에 민감한 값을 노출할 수 있다.
- `tofu apply`, `destroy`, `import`, `state push`, `force-unlock`, 그리고
  state 변경 작업은 원격/파괴적 행위이므로 정확한 별도 승인이 필요하다.
- Backend는 저장소를 제공하고 locking도 제공할 수 있다. locking을
  비활성화하지 않는다. `force-unlock`은 writer가 남아 있지 않다고 증명한
  후, 운영자 자신이 남긴 lock에만 사용한다.

### Normal use

1. repository root에서 작업하며 `infra/09-tooling/opentofu/workspace` 아래의
   정확한 디렉터리, backend, workspace 이름, account, 예상 리소스를 식별한다.
2. `docker compose --profile iac config --quiet`를 실행하고
   `docker compose --profile iac config --services`로 예상한 IaC service만
   있는지 확인한다.
3. 권한 없이 하는 smoke check는
   `docker compose --profile iac run --rm opentofu version`이다.
4. read-only provider/backend 권한으로 정확한 workspace에 대해 initialization,
   formatting, validation, 검토된 plan을 실행한다. plan과 state 파일은 Git
   밖의 보호된 경로에 보관하고 그 내용을 evidence에 붙여넣지 않는다.
5. 저장된 plan을 적용할지는 따로 결정한다. plan digest, 리소스 수,
   승인, exit status, apply 후 점검을 secret 없이 기록한다.

### Backup and upgrade

upgrade나 state 작업 전에 backend를 확인한다. 로컬 state의 경우 모든 writer를
멈추고 state와 backup 파일을 mode-0600으로 복사한다. 원격 backend의 경우
atomic/versioned backup 기능이나 `tofu state pull`을 보호된 파일로 사용하며,
그 출력을 터미널이나 채팅으로 보내지 않는다. 신뢰하기 전에 분리된/테스트용
backend로 격리된 restore를 검증한다. 중간의 모든 OpenTofu upgrade 노트를
검토하고 apply하지 않고 저장된 plan workflow를 테스트한다. 이 문서를 변경하면서
plan, state backup, restore, provider 호출은 실행하지 않았다.

## Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac run --rm opentofu version`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

state 복구, lock 진단, plan/apply 분리, upgrade에는
[runbook](../runbooks/0082-opentofu.md)을 사용한다.

## Traceability

- [Policy](../policies/0082-opentofu.md) (`POL-0082`)
- [Runbook](../runbooks/0082-opentofu.md) (`RUN-0082`)
- [OpenTofu Compose](../../../infra/09-tooling/opentofu/docker-compose.yml)

## Related Documents

- [OpenTofu provisioning workflow](https://opentofu.org/docs/cli/run/)
- [State storage and locking](https://opentofu.org/docs/language/state/backends/)
- [State locking](https://opentofu.org/docs/language/state/locking/)
- [Upgrade guide](https://opentofu.org/docs/intro/upgrading/)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Operations index](../README.md)
