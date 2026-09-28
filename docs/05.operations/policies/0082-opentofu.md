---
title: "OpenTofu Policy"
version: "0.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0082"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# OpenTofu Policy

## Overview

OpenTofu는 명시적인 `iac` job이다. 정적 선택과 검증은 provider 계정을 읽거나
원격 인프라를 변경할 권한을 결코 암시하지 않는다.

## Policy Scope

로컬 이미지 빌드, `/workspace`, 마운트된 클라우드 자격 증명, 백엔드 상태,
lock, plan, provider 작업, 업그레이드, 서비스 폐기.

## Controls

- **Activation:** `iac` 하에서 루트 프로젝트로부터 명명된 `opentofu` job을
  호출한다. HOME이나 일반 tooling 시작에는 절대 포함하지 않는다.
- **Authorization:** 계정, workspace, 백엔드, 예상 리소스, 허용된 명령
  클래스를 식별한다. plan 권한 부여는 apply, destroy, import, 상태 변경,
  또는 force-unlock을 승인하지 않는다.
- **Credentials:** 마운트된 AWS/Azure 디렉터리는 읽기 전용이더라도 민감한
  권한이다. workspace에 자격 증명을 추가하거나 값을 캡처하지 않는다.
- **State and plans:** 상태와 저장된 plan에는 시크릿이 포함될 수 있다. Git,
  stdout 증거, 공유 로그에서 제외한다. 백업은 모드 `0600`과 별도의 보존
  소유자로 보호한다.
- **Locking:** 백엔드 잠금을 보존한다. Force-unlock은 어떤 운영자나 자동화도
  해당 lock을 소유하지 않는다는 증명을 필요로 하며 기록된 lock ID만
  대상으로 한다.
- **Backup/recovery:** 로컬 상태와 원격 상태를 식별하고, 상태 변경/업그레이드
  전에 보호된 스냅샷을 취하며, 격리된 상태에서 복구를 리허설한다.
- **Upgrade:** 중간 노트를 검토하고, provider/백엔드 호환성을 검증하며,
  런타임 소스를 변경하기 전에 적용되지 않은 plan을 비교한다.
- **Removal:** 관리되는 모든 리소스가 후속 시스템을 가질 때까지 workspace,
  백엔드 상태, 자격 증명, 소유권 기록을 보존한다. 컨테이너 제거가 의도적으로
  인프라를 파괴하는 일은 결코 없다.

## Exceptions

별도의 변경 승인, 상태 보호, 또는 lock 소유권을 우회하는 예외는 없다. 범위,
만료, 복구 아티팩트, 종료 조건을 기록한다.

## Verification

정적 Compose 점검은 선택만 증명한다. 런타임 증거는 버전, init/validate,
plan, apply, apply 이후 결과를 구분한다. 실행되지 않은 상태 복구와 업그레이드
리허설은 공백으로 남는다.

## Review Cadence

모든 provider/백엔드/런타임 업그레이드 전, 그리고 자격 증명 마운트, 네트워크
접근, 또는 workspace 소유권이 변경될 때마다 검토한다.

## Traceability

- [가이드](../guides/0082-opentofu.md) (`GDE-0082`)
- [런북](../runbooks/0082-opentofu.md) (`RUN-0082`)
- [Tooling 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [OpenTofu Compose 소스](../../../infra/09-tooling/opentofu/docker-compose.yml)
- [파생 Compose 이미지 projection](../../../infra/tech-stack.versions.json)
- [OpenTofu 상태 저장소](https://opentofu.org/docs/language/state/backends/)
- [OpenTofu state 명령 안전성](https://opentofu.org/docs/cli/commands/state/)
- [운영 인덱스](../README.md)
