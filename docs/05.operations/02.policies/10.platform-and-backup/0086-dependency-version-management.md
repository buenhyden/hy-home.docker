---
title: "Dependency Version Management Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-27"
layer: "operations"
artifact_id: "POL-0086"
parent_ids:
- "AD-0031"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Dependency Version Management Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

인프라 버전 변경은 하나의 HOME/DEV 호스트에서 검토 가능하고 재현 가능해야 한다. 버전
업데이트가 배포나 데이터 마이그레이션을 승인하지는 않는다.

###### Authority
<!-- core-payload-level:4 -->

- [Home/Dev architecture](../../../02.architecture/01.descriptions/0031-home-development-host.md) (`AD-0031`)

- [Runtime version projection](../../../../infra/tech-stack.versions.json)
- [Repository Renovate policy](../../../../renovate.json5)

##### Applies To

Compose, Dockerfile 및 인라인 빌드 소스, derived registry, Renovate, 현재
구현/운영 문서의 런타임 버전 참조.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0086-R1 | Compose 이미지와 일반 Dockerfile 변경 시 | 필수: Renovate의 활성화된 Docker manager가 갱신하고 소스 pin 변경을 검토한다 | 수동 | none |
| POL-0086-R2 | OpenTofu 인라인 Dockerfile 변경 시 | 필수: Renovate custom manager가 좁게 선언된 소스 패턴으로만 갱신한다 | none | none |
| POL-0086-R3 | GitHub Actions `uses` 참조 변경 시 | 필수: Renovate patch/minor 그룹으로 갱신하고 SHA를 올리는 PR은 같은 PR에서 `.github/workflow-contract.yml`의 승인된 action 기록도 갱신한다 | none | none |
| POL-0086-R4 | CI toolchain `uses-with` 입력 변경 시 | 필수: 수동으로 하나의 PR에서 uv lock과 함께 변경하고 workflow-contract 테스트와 gate 증거로 검토한다 | workflow-contract 테스트 | gate 증거 |
| POL-0086-R5 | Storybook npm 변경 시 | 필수: Renovate `npm`이 `projects/storybook/nextjs`(workspace 포함)만 minor/patch 그룹으로 갱신하고 TypeScript 7 미만을 유지한다 | none | none |
| POL-0086-R6 | Storybook npm major 업데이트 | 필수: Dashboard 승인을 받는다 | none | none |
| POL-0086-R7 | Storybook npm 업데이트 | 금지: automerge | none | none |
| POL-0086-R8 | OpsflowSmtp npm 변경 시 | 필수: Renovate `npm`이 n8n 노드 `package.json` 하나만 갱신하고 `n8n-workflow`는 갱신에서 제외한 채 n8n과 함께 수동 변경한다 | none | none |
| POL-0086-R9 | OpenTofu provider/module 의존성 변경 시 | 필수: operator가 검토하는 workspace owner가 관리한다 | 수동 | none |
| POL-0086-R10 | tooling 패키지에 provider/module manifest가 처음 생길 때 | 필수: 범위가 제한된 manager를 활성화한다 | none | none |
| POL-0086-R11 | 이미지 내부 `infra/**/requirements.txt` 변경 시 | 필수: Renovate `pip_requirements`가 설정된 좁은 경로만 갱신한다 | none | none |
| POL-0086-R12 | `pip_requirements` major 업데이트 | 필수: Dashboard 승인을 받는다 | none | none |
| POL-0086-R13 | `pip_requirements` 업데이트 | 금지: automerge | none | none |
| POL-0086-R14 | pre-commit hook revision 변경 시 | 필수: maintainer 검토로 갱신한다 | 수동 | none |
| POL-0086-R15 | Derived Compose 이미지 registry 변경 시 | 필수: synchronization script가 추적되는 모든 인프라 Compose 저장소를 정확히 한 번씩, 명시적인 local/custom 분류와 파일별 정확한 소스 그룹으로 갱신한다 | synchronization `--check` | none |
| POL-0086-R16 | 설명형 문서 변경 시 | 필수: human/agent 검토와 기존 metadata validator로 검토하고 정당화된 정확 리터럴 예외만 둔다 | 수동 | none |
| POL-0086-R17 | datasource가 릴리스 timestamp를 제공하는 정기 patch/minor 업데이트 | 필수: 설정된 7일 soak window를 따른다 | none | none |
| POL-0086-R18 | timestamp 없는 registry의 업데이트 | 필수: Monday 일정과 필수 수동 검토를 유지한다 | none | none |
| POL-0086-R19 | timestamp 없는 registry의 업데이트 | 금지: 7일 age 주장 | none | none |
| POL-0086-R20 | 보안 경고 | 필수: 일반 대기를 우회하되 명시적 검토를 받는다 | none | none |
| POL-0086-R21 | 보안 경고가 긴급할 때 | 금지: 마이그레이션이나 롤백 증거 생략 | none | none |
| POL-0086-R22 | 항상 | 금지: infra automerge 활성화 | none | none |
| POL-0086-R23 | 항상 | 금지: self-host `allowedCommands` 확대 | none | none |
| POL-0086-R24 | 항상 | 필수: 설정 구문이 저장소/전역 모드를 분리한 공식 strict validator를 통과한다 | 공식 strict validator(저장소/전역 모드) | none |
| POL-0086-R25 | 항상 | 필수: Renovate를 유일한 의존성 버전 updater로 유지한다 | 수동 | none |
| POL-0086-R26 | 항상 | 금지: Dependabot version updates와 `.github/dependabot.yml` 유지 | none | none |
| POL-0086-R27 | 항상 | 필수: Renovate `npm` manager를 Storybook·OpsflowSmtp 두 대상의 `managerFilePatterns`로만 제한하고 `labs/**`는 `ignorePaths`로 계속 제외한다 | none | none |
| POL-0086-R28 | 항상 | 금지: 새 updater나 manager 범위가 같은 파일을 겹쳐 소유하게 만들기 | 수동 | none |
| POL-0086-R29 | 항상 | 금지: GitHub Actions에 updater 역할 부여 | none | none |
| POL-0086-R30 | 항상 | 필수: GitHub 취약점 경고(Dependabot alerts)를 Renovate의 `vulnerabilityAlerts` 입력으로 켜 둔다 | none | none |
| POL-0086-R31 | Renovate의 첫 정상 실행을 확인한 뒤 | 필수: owner가 저장소의 Dependabot 보안 업데이트(automatic security fixes)를 별도 단계로 끈다 | none | none |
| POL-0086-R32 | 항상 | 금지: 다른 문서에서 Renovate 업데이트 규칙을 복제(링크만 한다) | none | none |
| POL-0086-R33 | 컨테이너 manager(`docker-compose`, `dockerfile`, `custom.regex`) | 필수: `pinDigests`로 모든 이미지를 `tag@sha256:<digest>`로 고정한다 | SEC01 ledger(tag-only 대상 거부) | none |
| POL-0086-R34 | digest 추가(`pinDigest`)와 갱신(`digest`) | 필수: 각각 한 PR로 묶는다 | none | none |
| POL-0086-R35 | 항상 | 금지: digest를 임의로 만들거나 다른 registry의 것으로 대체 | none | none |
| POL-0086-R36 | 상태 비저장 tier(01, 02, 03, 07, 08, 09, 11, 13)의 non-major 이미지 업데이트 | 필수: 한 PR로 묶는다 | none | none |
| POL-0086-R37 | 데이터(04)·메시징(05) tier 이미지, `apache/airflow`, `quay.io/keycloak/keycloak`, `n8nio/**` 업데이트 | 필수: 이미지당 PR 하나를 유지한다 | none | none |
| POL-0086-R38 | 관측성 tier와 Storybook npm 업데이트 | 필수: patch/minor 그룹(Storybook은 minor/patch 그룹)으로 처리한다 | none | none |
| POL-0086-R39 | 항상 | 금지: `nvidia/cuda` 13 이상 갱신(12.x 유지) | none | `renovate.json5` 설명 |
| POL-0086-R40 | 항상 | 금지: `surrealdb/surrealdb` 3.x 이상 갱신(v2.x 유지) | none | `renovate.json5` 설명 |
| POL-0086-R41 | 항상 | 금지: TypeScript 7 이상 갱신 | none | `renovate.json5` 설명 |
| POL-0086-R42 | 항상 | 금지: Renovate가 n8n core/runners 이미지와 `n8n-workflow`를 갱신 | none | none |
| POL-0086-R43 | n8n core/runners 이미지와 `n8n-workflow` 변경 시 | 필수: 하나의 수동 호환성 묶음으로 바꾼다 | none | none |
| POL-0086-R44 | 항상 | 필수: `minimumReleaseAge` 7일, `prConcurrentLimit` 5, `prHourlyLimit` 2를 유지한다 | none | none |
| POL-0086-R45 | major 업데이트 | 필수: Dashboard 승인 후에만 제안한다 | none | none |
| POL-0086-R46 | 항상 | 금지: 인프라 이미지·npm·pip automerge | none | none |
| POL-0086-R47 | Dashboard에서 속도 제한으로 대기 중인 항목 | 필수: 필요한 것만 하나씩 체크한다 | none | none |
| POL-0086-R48 | 항상 | 금지: Dashboard에서 "create all" 사용 | none | none |
| POL-0086-R49 | 항상 | 필수: 일정 창을 월요일 00–05시(KST)로 유지한다 | none | none |
| POL-0086-R50 | 항상 | 필수: 커밋 제목의 대소문자를 보존한다(`commitMessageLowerCase: never`) | none | none |
| POL-0086-R51 | PR마다 | 필수: `postUpgradeTasks`로 `sync-tech-stack-versions.sh --write`와 `sync-update-ledger.sh --write`를 실행해 SEC01 ledger를 다시 묶는다 | none | none |
| POL-0086-R52 | ledger 재결합 시 | 필수: 같은 저장소의 전체 `name:tag@sha256` 참조가 바뀐 기존 행만 받아들이고 tag-only 대상, 새 서비스, 제거는 종료 코드 2로 거부한다 | `sync-update-ledger.sh`(종료 코드 2 거부) | none |
| POL-0086-R53 | 항상 | 금지: 받아들인 ledger 행을 서명·scan·호환성 증거로 취급(행은 `BLOCKED`/`UNKNOWN`/`NOT_RUN` 상태) | none | none |
| POL-0086-R54 | 항상 | 금지: ledger와 파생 registry를 손으로 고치는 것을 정상 경로로 사용 | none | none |
| POL-0086-R55 | 거부 사유 해소 후 | 필수: 같은 도구로 다시 쓴다 | none | none |
| POL-0086-R56 | 이미지 변경 머지 후 | 금지: 머지된 이미지 변경을 HOME에 자동 적용 | 수동 | none |
| POL-0086-R57 | 머지된 이미지 변경을 HOME에 적용할 때 | 필수: 적용(recreate)에 별도 승인을 받는다 | 수동 | none |
| POL-0086-R58 | 항상 | 금지: 머지를 적용·검증 증거로 삼기 | 수동 | none |
| POL-0086-R59 | 수동·에이전트 업데이트 라운드 | 필수: R44의 7일 release age와 R45의 major Dashboard 승인을 Renovate 밖의 갱신에도 똑같이 적용한다 | 수동 | 라운드 Task의 출시일·경과일 기록 |
| POL-0086-R60 | 로컬 빌드 이미지 태그가 버전을 담을 때 | 필수: 태그 버전은 Dockerfile에서 같은 이름의 `FROM` 기준 이미지 버전과 같아야 하며, 지난 버전을 가리키는 태그를 두지 않는다. Renovate post-upgrade의 `sync-tech-stack-versions.sh --write`가 태그를 바꾸고 ledger는 이를 미검증 행으로 받는다 | `sync-tech-stack-versions.sh --check`(`local_image_tags`) | none |

| Surface | Update owner | Authority and review |
| --- | --- | --- |
| Compose 이미지와 일반 Dockerfile | Renovate | 활성화된 Docker manager; 소스 pin 변경 검토됨 |
| OpenTofu 인라인 Dockerfile | Renovate custom manager | 좁게 선언된 소스 패턴, 임의의 regex 범위 없음 |
| GitHub Actions `uses` 참조 | Renovate | patch/minor 그룹; SHA를 올리는 PR은 같은 PR에서 `.github/workflow-contract.yml`의 승인된 action 기록도 갱신(선례 #898) |
| CI toolchain `uses-with` 입력(`python-version`, setup-uv `version`/체크섬, `node-version`) | 수동 | Renovate 비활성; workflow-contract 테스트, gate 증거, uv lock과 함께 고정되므로 하나의 수동 PR로 변경 |
| Storybook npm | Renovate `npm` | `projects/storybook/nextjs`(workspace 포함)만; minor/patch 그룹, TypeScript 7 미만(typescript-eslint가 TypeScript 7을 거부), major Dashboard 승인, automerge 금지 |
| OpsflowSmtp npm | Renovate `npm` | n8n 노드 `package.json` 하나만; `n8n-workflow`는 n8n 이미지가 번들한 버전과 같아야 하므로 갱신 제외하고 n8n과 함께 수동 변경 |
| OpenTofu provider/module 의존성 | operator가 검토하는 workspace owner | tooling 패키지에 현재 추적되는 provider/module manifest가 없음; 그런 manifest가 처음 생길 때 범위가 제한된 manager를 활성화 |
| 이미지 내부 `infra/**/requirements.txt` | Renovate `pip_requirements` | 설정된 좁은 경로만; major Dashboard 승인, automerge 금지 |
| pre-commit hook revision | maintainer 검토 | pre-commit manager가 꺼져 있어 자동 범위 밖; `requirements.txt` pin은 위 `pip_requirements`가 소관 |
| Derived Compose 이미지 registry | synchronization script | 추적되는 모든 인프라 Compose 저장소를 정확히 한 번씩, 명시적인 local/custom 분류와 파일별 정확한 소스 그룹으로 |
| 설명형 문서 | human/agent 검토와 기존 metadata validator | authority 링크; 정당화된 정확 리터럴 예외만 |

datasource가 릴리스 timestamp를 제공할 때, 정기적인 patch/minor 업데이트는 설정된
7일 soak window를 따른다. `timestamp-optional`이 있어 timestamp가 없는 registry에서도 무한정
기다리지 않는다. 그런 업데이트는 Monday 일정과 필수 수동 검토를 유지하며 7일 age를
주장하지 않는다. Major 업데이트는 별도로 다룬다. 보안 경고는
일반 대기를 우회하고 명시적 검토를 받는다. 긴급하더라도 마이그레이션이나 롤백 증거를
건너뛰지 않는다. 이 fast path는 설정된 manager가 실제로 수신하는 취약점 경고에
적용되며, 컨테이너 이미지 CVE 스캐닝이나 설치된 이미지의 취약점 범위를 확립하지 않는다.
infra automerge를 활성화하거나 self-host allowedCommands를 넓히지 않는다. 설정 구문은
저장소/전역 모드를 분리한 공식 strict validator를 통과해야 한다.

Renovate가 유일한 의존성 버전 updater다(#850). Dependabot version updates는 폐지했고
`.github/dependabot.yml`은 존재하지 않는다. Renovate `npm` manager는 위 두 대상의
`managerFilePatterns`로만 제한하며 `labs/**`는 계속 `ignorePaths`로 제외한다. 새
updater나 manager 범위가 같은 파일을 겹쳐 소유하게 만들지 않는다. GitHub Actions는
검증만 하며 updater 역할이 없다. GitHub 취약점 경고(Dependabot alerts)는 Renovate의
`vulnerabilityAlerts` 입력이므로 켜 둔다. 반면 저장소의 Dependabot 보안 업데이트
(automatic security fixes)는 Renovate의 첫 정상 실행을 확인한 뒤 owner가 별도 단계로 끈다.
이 문서는 그 원격 설정을 바꾸지 않으며 승인도 주지 않는다.

###### Renovate 운영 규칙
<!-- core-payload-level:4 -->

이 절이 Renovate의 업데이트 규칙을 소유한다. 값은 `renovate.json5`가 소유하며 이 절은
의도와 한계만 적는다. 다른 문서는 이 절을 링크하고 규칙을 복제하지 않는다.

- **digest pin**: 컨테이너 manager(`docker-compose`, `dockerfile`, `custom.regex`)는
  `pinDigests`를 켜서 모든 이미지를 `tag@sha256:<digest>`로 고정한다. SEC01 ledger는 tag만 있는
  대상을 거부하므로 tag-only pin은 CI로 갱신할 수 없다. digest 추가(`pinDigest`)는 한 PR,
  digest 갱신(`digest`)은 한 PR로 묶는다. digest를 임의로 만들거나 다른 registry의 것으로
  대체하지 않는다.
- **그룹**: 상태 비저장 tier(01, 02, 03, 07, 08, 09, 11, 13)의 non-major 이미지 업데이트는
  한 PR이다. 모든 이미지 업데이트가 공유 SEC01 ledger를 다시 쓰므로 PR을 나누면 머지마다 충돌한다.
  데이터(04)·메시징(05) tier 이미지, `apache/airflow`(constraints bundle),
  `quay.io/keycloak/keycloak`(시작 시 DB schema migration), `n8nio/**`는 이미지당 PR 하나를 유지한다.
  관측성 tier는 patch/minor 그룹, Storybook npm은 minor/patch 그룹이다.
- **보류**: `nvidia/cuda`는 12.x(GTX 1060 Pascal은 CUDA 13 미지원), `surrealdb/surrealdb`는
  v2.x(open-notebook이 v2만 지원하고 3.x는 2.x 데이터를 export 마이그레이션 없이 읽지 못함),
  TypeScript는 7 미만이다. 해제 조건은 `renovate.json5`의 설명이 가진 근거가 바뀔 때다.
  n8n core/runners 이미지와 `n8n-workflow`는 Renovate가 건드리지 않고 하나의 수동 호환성 묶음으로 바꾼다.
- **속도 제한**: `minimumReleaseAge` 7일, `prConcurrentLimit` 5, `prHourlyLimit` 2.
  major 업데이트는 Dashboard 승인 후에만 제안하고 인프라 이미지·npm·pip는 automerge하지 않는다.
  Dashboard에서 속도 제한으로 대기 중인 항목은 필요한 것만 하나씩 체크하고 "create all"을 쓰지 않는다.
- **일정과 커밋**: 일정 창은 월요일 00–05시(KST)다. 커밋 제목의 대소문자는 보존한다
  (`commitMessageLowerCase: never`).
- **ledger 재결합**: PR마다 `postUpgradeTasks`가 `sync-tech-stack-versions.sh --write`와
  `sync-update-ledger.sh --write`를 실행해 SEC01 ledger를 다시 묶는다. 받아들인 행은
  검증되지 않은 상태(`BLOCKED`/`UNKNOWN`/`NOT_RUN`)이며 서명·scan·호환성 증거가 아니다. 같은
  저장소의 전체 `name:tag@sha256` 참조가 바뀐 기존 행만 받아들이고 그 외(tag-only 대상, 새
  서비스, 제거)는 종료 코드 2로 거부한다. ledger와 파생 registry를 손으로 고치는 것은
  정상 경로가 아니며, 거부 사유를 해소한 뒤 같은 도구로 다시 쓴다.
  절차는 [security-updates README](../../../../infra/09-platform-ops/security-updates/README.md)에 있다.
- **적용 분리**: 머지된 이미지 변경은 HOME에 적용되지 않는다. 적용(recreate)은 별도 승인이
  필요하고 CI는 local 빌드 이미지를 빌드하지 않는다. 머지가 적용·검증의 증거가 아니다.

PR 처리 규칙(rebase 방법, 한 번에 하나씩 머지, 수동 close 금지)은 영문 거버넌스인
`github-governance.md` 3절이 소유하고, 실행 순서는 [Runbook](../../03.runbooks/10.platform-and-backup/0086-dependency-version-management.md)이 소유한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

변경 가능한 이미지 예외는 owner, reason, risk, review cadence, exit condition과 함께
`infra/image-tag-policy.exceptions.json`에 둔다. 서술식 예외로는 source-image
검증을 면제할 수 없다. 예외를 제거하기 전에 이미지 호환성을 검토한다. 태그 변경이
GPU나 데이터 형식 호환성의 증거가 되지는 않는다.

###### Approval and Review
<!-- core-payload-level:4 -->

매월, 그리고 manager 범위, 소스 parser, 이미지 예외, major 업데이트가 변경될 때
검토한다.

#### Enforcement

##### Mechanisms

기존 synchronization `--check`가 registry drift gate다. 추가, 제거, 중복 저장소와
소스/분류 drift를 거부한다. write 모드는 derived 항목을 원자적으로 재조정한다. Compose,
수정된 빌드 소스, 문서 계약, 공식 Renovate 설정은 독립적으로 검증한다. registry 출력을
런타임 health나 backup/restore의 증거로 받아들이지 않는다.

변경 가능한 이미지 예외는 `tests/validation/test_compose_baseline_gates.py`의
`ImageTagPolicyTests`가 검사한다. ROOT Compose image와 ROOT Dockerfile의 `FROM` 가운데 digest,
점이 있는 버전, 세 자리 이상 release 번호, commit ID 태그가 없는 참조는 예외 항목이 있어야 한다.
`v2`처럼 major만 있는 태그는 채널로 본다. 어디에도 쓰이지 않는 항목이나 owner·reason·risk·review
cadence·exit condition이 빠진 항목은 실패한다. local build 서비스의 Compose `image` 이름은 제외하고
그 Dockerfile의 `FROM`을 본다.

##### Limits

다음 규칙은 정책이 규칙과 직접 연결된 기계적 강제를 보이지 않거나 사람 검토에 의존한다.

- update owner 표: 수동 검토/승인에 의존: `POL-0086-R1`, `POL-0086-R9`, `POL-0086-R14`, `POL-0086-R16` / 지정된 검사 없음: `POL-0086-R2`, `POL-0086-R3`, `POL-0086-R5`, `POL-0086-R6`, `POL-0086-R7`, `POL-0086-R8`, `POL-0086-R10`, `POL-0086-R11`, `POL-0086-R12`, `POL-0086-R13`
- soak·보안 경고: 지정된 검사 없음: `POL-0086-R17`, `POL-0086-R18`, `POL-0086-R19`, `POL-0086-R20`, `POL-0086-R21`, `POL-0086-R22`, `POL-0086-R23`
- 단일 updater: 수동 검토/승인에 의존: `POL-0086-R25`, `POL-0086-R28` / 지정된 검사 없음: `POL-0086-R26`, `POL-0086-R27`, `POL-0086-R29`, `POL-0086-R30`, `POL-0086-R31`
- 규칙 소유: 지정된 검사 없음: `POL-0086-R32`
- digest pin: 지정된 검사 없음: `POL-0086-R34`, `POL-0086-R35`
- PR 그룹: 지정된 검사 없음: `POL-0086-R36`, `POL-0086-R37`, `POL-0086-R38`
- 보류: 지정된 검사 없음: `POL-0086-R42`, `POL-0086-R43`
- 속도 제한: 지정된 검사 없음: `POL-0086-R47`, `POL-0086-R48`
- ledger: 지정된 검사 없음: `POL-0086-R51`, `POL-0086-R53`, `POL-0086-R54`, `POL-0086-R55`
- 적용 분리: 수동 검토/승인에 의존: `POL-0086-R56`, `POL-0086-R57`, `POL-0086-R58`
- synchronization `--check`는 registry·예외 drift만 거부하며 런타임 health나 backup/restore의 증거가 아니다.
- fast path는 컨테이너 이미지 CVE 스캐닝이나 설치된 이미지의 취약점 범위를 확립하지 않는다.
- POL-0086-R39, POL-0086-R40, POL-0086-R41, POL-0086-R44, POL-0086-R45, POL-0086-R46, POL-0086-R49, POL-0086-R50: 정책이 이 규칙에 묶은 검사를 명시하지 않는다.

#### Ownership

##### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

##### Review Triggers

- [Guide](../../01.guides/10.platform-and-backup/0086-dependency-version-management.md), [Runbook](../../03.runbooks/10.platform-and-backup/0086-dependency-version-management.md)

- [Operations index](../../README.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
