---
title: "OpenTofu Implementation"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# OpenTofu

## Overview

운영자가 트리거하는 인프라 CLI입니다. 인라인 Dockerfile이 도구 이미지의
소스이며 워크스페이스와 자격 증명 마운트는 실제 원격 변경 능력을 부여합니다.
이 마운트 자체가 변경 승인을 뜻하지 않으므로 plan/apply의 대상과 권한을 별도로
검토해야 합니다.

Lifecycle: **DEV job**. 루트 Compose가 이 정의를 include하며 명시적 프로필이
활성화를 제어합니다.

## Audience

구현, 설정, 검증을 검토하는 운영자와 개발자.

## Scope

로컬 서비스 정의와 구현 탐색. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/0082-opentofu.md`, `docs/05.operations/policies/0082-opentofu.md`, `docs/05.operations/runbooks/0082-opentofu.md`(ID: `GDE-0082`, `POL-0082`, `RUN-0082`)가 담당합니다.

## Structure

- [docker-compose.yml](docker-compose.yml)

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)와 그 참조 빌드 소스에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

## Configuration

| Service | Profiles | Networks | Host ports | Secret references |
| --- | --- | --- | --- | --- |
| `opentofu` | `iac` | project default; 프로젝트 내 서비스(예: `seaweedfs-s3`)를 대상으로 하는 상태 백엔드에 대한 직접 연결은 현재 선언으로 제공되지 않음; 네트워크 변경은 별도 검토·승인 대상 | 호스트 게시 없음 | Compose Secret 부여 없음; 설정된 부트스트랩 파일 메타데이터를 확인합니다 |

Persistence:

Compose의 서비스 바인드 마운트를 참고합니다. 최상위 명명된 볼륨은 선언되어 있지 않습니다.

환경 변수 키 이름과 기본값은 Compose와 [공개 환경 변수 예시](../../../.env.example)에 선언되어 있습니다. Compose의 마운트 권한과 헬스체크 명령은 구현을 설명할 뿐이며, 설정 검사를 통과했다고 해서 런타임 준비 상태가 증명되는 것은 아닙니다. 비공개 환경 변수 값, 자격 증명 파일, 원본 렌더링된 설정은 출력하지 않습니다.

## Validation

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 사용합니다. 대상별 런타임 확인과 승인 후 복구는 소유 운영 Runbook을 사용합니다. 마운트 누락, 예상치 못한 노출, 초기화 실패 시에는 중지합니다.

## Usage

Compose, 빌드 소스, 공개 환경 변수 키, 시크릿 참조를 일관되게 유지합니다. 게이트웨이 인증, 영속화, 리소스 예산, 버전 예외를 변경하기 전에 검토합니다. 여기에 명령을 중복 기록하지 말고 기존 운영 주제(operations subject)를 업데이트합니다.

### SEC01 후보와 상태 호환성

실제 빌드 소스의 태그와 OCI index digest, 로컬 이미지 태그는
[Compose](docker-compose.yml)의 인라인 Dockerfile과 이미지 선언이 소유한다.
자격 증명 마운트·workspace·entrypoint·프로필과 원격 변경 권한은 기존 계약을 따른다.

[공식 릴리스](https://github.com/opentofu/opentofu/releases)는
WinRM provisioner 제거와 `base64gzip`의 바이트 결과 변경, ephemeral
resource plan JSON과 apply 시 output 재평가 수정을 명시한다.
실제 workspace의 소비 여부는 확인하지 않았으며 원격 plan/apply·state 변환·
credential 읽기는 `NOT_RUN`이다.

운영 반영 전 지정된 빈 합성 workspace에서 provider 다운로드·원격 backend 없이
CLI 및 계획 차이를 검증하고, 정확한 state·lockfile·provider 버전 백업과 기존
1.12.6에서의 읽기/복원 조건을 SPEC-0204-TSK-0009에 기록한다. <!-- runtime-version-exception: migration — 이전 state 해석과 복원 시험의 정확한 기준 버전 -->
새 버전 apply 이후
이미지만 되돌리면 복구된다고 간주하지 않는다.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [Public secret contract](../../../secrets/README.md)
