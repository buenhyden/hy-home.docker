---
title: "Repository Support Staging"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-09-27"
---

# _workspace/repo-support

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Purpose

##### Audience

- Repository Maintainers

##### Outcome

###### Project Role
<!-- core-payload-level:4 -->

`_workspace/repo-support`는 비밀이 아닌 저장소 지원 산출물을 잠시 두는
공간이며 Git이 무시합니다. agent 작업, migration, dry-run, 분석에서 생기는
짧은 수명의 지원 파일을 둡니다. 진단 산출물은 같은 `_workspace`의
`diagnostics/`가 소유하며, 두 위치의 용도와 보존 경계는 상위 README를
따릅니다.

이 디렉터리는 활성 문서 stage, archive, 운영 폴더, 런타임 설정, 장기 증거
보관소가 아닙니다.

###### Boundaries
<!-- core-payload-level:4 -->

작업 중 만들 수 있는 산출물:

- 생성된 분석 요약
- ID, 경로, 계획된 작업 단위의 dry-run 미리보기
- migration ledger
- subagent 인계 파일
- 임시 비교표
- raw log나 비밀이 담긴 출력이 없는 검증 메모

만들거나 남기지 않는 산출물:

- 진단 덤프, 로컬 로그, raw log
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

#### Getting Started

##### Prerequisites

없음: 이 디렉터리에는 설치할 도구나 별도 권한이 없으며, 산출물을 쓰는 스크립트의 사전 요건은 각 스크립트가 정합니다.

##### First Use

작업을 마치기 전에 오래 남길 비밀 아닌 결과를 정본 owner로 옮깁니다.

- 구현 증거는 현재 `docs/03.specs/` package의 Task로 옮깁니다.
- 안정적인 참조 맥락은 `docs/90.references/`로 옮깁니다.
- 오래 유지할 거버넌스 규칙은 `.agents/governance/`의 해당 정책 owner로
  옮깁니다.
- 작업별 맥락은 현재 Task에 남깁니다. 세션을 넘어 남길 에이전트 기억은
  `_workspace`가 아니라 공유 memory 저장소에 둡니다. 그 위치와 규칙은
  [환경 제약](../../.agents/governance/environment-constraints.md#5-shared-agent-memory)이
  소유합니다.

사용자가 비밀 아닌 산출물의 승격을 명시적으로 승인하지 않는 한, 원본
임시 산출물은 무시된 상태로 둡니다.

#### Repository Map

##### Current Paths

| Path | Purpose |
| --- | --- |
| [analysis/README.md](analysis/README.md) | 분석 요약 |
| [previews/README.md](previews/README.md) | dry-run 미리보기 |

###### Directories
<!-- core-payload-level:4 -->

`README.md`만 추적됩니다. 작업별 하위 디렉터리는 무시되는 임시 공간이므로
이 README가 목록을 관리하지 않습니다.

다음 스크립트가 `task-*/` 아래에 결과를 씁니다.

| 스크립트 | 결과 |
| --- | --- |
| `scripts/security/seed-grype-db-cache.sh` | Grype DB seed |
| `scripts/security/verify-sample-service-supply-chain.sh` | 공급망 검증 기록 |
| `scripts/operations/rehearse-sample-service-delivery.sh` | 배포 리허설 입력과 기록 |
| `scripts/lib/ops/compose-core-readiness.sh` | readiness 기록 |

###### Canonical Entry Points
<!-- core-payload-level:4 -->

작업 결과를 승격할 정본 owner는 `docs/03.specs/`의 Task, `docs/90.references/`, `.agents/governance/`의 해당 정책이며, 상위 계약은 [workspace README](../README.md)가 소유합니다.

##### Owners

이 문서의 유지 책임은 frontmatter의 `owner`인 `@buenhyden`에게 있습니다.

#### Support

##### Help

이 문서는 별도의 문의·이슈 보고 경로를 기록하지 않습니다.

##### Related Documentation

- [workspace README](../README.md)

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
