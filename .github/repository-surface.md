---
title: "GitHub Control Surface"
version: "1.0.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-06"
created: "2026-02-14"
---

# GitHub Control Surface

## Overview

`.github`에는 GitHub이 직접 읽는 추적 대상 정의가 모여 있다. 워크플로, 워크플로가 실행하는
타입 지정 게이트 레지스트리, 코드 소유권, 기여 템플릿, 브랜치 보호 제안이 여기에
속한다. 이 문서는 이 폴더의 진입점으로, 각 정의와 그 정본 거버넌스 소유자, 이를
검증하는 로컬 명령을 안내한다.

이 파일은 일부러 `README.md`가 아니라 `repository-surface.md`로 이름 붙였다.
GitHub은 저장소에 표시할 README를 루트, `.github/`, `docs/` 순서로 찾기 때문에
`.github/README.md`가 있으면 루트 [README](../README.md)와 저장소 랜딩 페이지
자리를 두고 경쟁하게 된다.

## Audience

- 워크플로, 룰셋, 소유권 규칙을 변경하는 유지관리자.
- GitHub 쪽 동작을 편집하기 전에 그 근거를 찾아야 하는 에이전트.
- CI 변경 사항이 선언된 계약과 일치하는지 확인하는 리뷰어.

## Scope

이 서피스는 추적 대상 GitHub 정의와 그 근거로 가는 경로를 소유한다. 정책 자체는
소유하지 않는다.

- 소유: 아래 인벤토리, 그리고 각 정의를 정본 소유자와 검증 명령으로 매핑하는 것.
- 비소유: GitHub 거버넌스 정책은
  [github-governance.md](../.agents/governance/github-governance.md)에 있다.
  게이트 구성은 [workflow-contract.yml](./workflow-contract.yml)에 있다.
  서버 측 브랜치 보호는 GitHub 프로젝트 설정에 있으며, 여기서는 제안만 한다.

## Structure

| Path | Role |
| :--- | :--- |
| `workflows/` | GitHub Actions가 실행하는 워크플로 정의 |
| `workflow-contract.yml` | 작업, 게이트 노드, 공개 스위트의 타입 지정 레지스트리 |
| `rulesets/` | 프로젝트 설정에서 수동으로 적용하는 브랜치 보호 제안 |
| `ISSUE_TEMPLATE/` | 이슈 양식 |
| `PULL_REQUEST_TEMPLATE.md` | 풀 리퀘스트 본문 템플릿 |
| `CODEOWNERS` | 경로별 리뷰 라우팅 |
| `dependabot.yml` | 의존성 업데이트 일정 |
| `labeler.yml` | 풀 리퀘스트 라벨 라우팅 |
| `SECURITY.md` | 취약점 보고 경로 |

## Navigation / Inventory

- [CI 품질 워크플로](./workflows/ci-quality.yml): main push 보안 검사와 성공 후 `main-current` 갱신
- [타입 지정 워크플로 및 게이트 레지스트리](./workflow-contract.yml): 로컬 변경 경로별 검사와 로컬 전체 검사 구성. 일반 문서 변경은 본문 검증을 유지하고 문서 검사기 회귀 테스트만 생략한다. 검사기·게이트·레지스트리 변경과 미등록 경로는 필요한 회귀 테스트를 포함한다.
- [기여자 환영 워크플로](./workflows/greetings.yml)
- [풀 리퀘스트 라벨러 워크플로](./workflows/pr-labeler.yml)
- [스테일 스레드 워크플로](./workflows/stale.yml)
- [릴리스 체인지로그 워크플로](./workflows/generate-changelog.yml)
- [코드 소유권](./CODEOWNERS)
- [풀 리퀘스트 템플릿](./PULL_REQUEST_TEMPLATE.md)
- [라벨 라우팅](./labeler.yml)

## Verification and Quality Gates

이 서피스를 변경하기 전에 저장소 루트에서 다음을 실행한다.

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/check-github-workflow-contract.py
```

- [타입 지정 게이트 CLI](../scripts/validation/run-ci-gate.py)는 프로필이
  선택한 공개 스위트를 실행한다.
- [전용 워크플로 검사기](../scripts/validation/check-github-workflow-contract.py)는
  `workflow-contract.yml`을 추적 대상 워크플로 정의 전체와 대조해 검증한다.
  main 보안 작업 이름, 이벤트 조건과 태그 작업의 종속성도 검사한다.
- [타입 지정 로컬 QA 게이트](../scripts/validation/run-ci-gate.py)에
  `--explain`을 붙이면 선택된 스위트-검증기 매핑을 보여 준다.

## Usage

1. 정본 소유자부터 바꾼다. 동작 자체가 바뀔 때는
   [github-governance.md](../.agents/governance/github-governance.md)를
   편집한다 → 정책이 새 규칙을 명시한다.
2. 작업이나 게이트 노드를 추가, 제거, 재배선할 때는
   [workflow-contract.yml](./workflow-contract.yml)에 변경 사항을 선언한다 →
   계약이 새 형태를 명시한다.
3. 선언에 맞춰 워크플로 정의를 편집한다 → 워크플로와 계약이 필드 단위로 일치한다.
4. `python3 scripts/validation/check-github-workflow-contract.py`를 실행한다 →
   종료 상태 `0`.
5. 새 정의를 위 인벤토리에 추가한다 → 이 문서에서 이 폴더의 추적 대상 파일
   전체로 갈 수 있다.

브랜치 보호 변경은
[rulesets/main-protection.md](./rulesets/main-protection.md)에서 제안하고
유지관리자가 GitHub 프로젝트 설정에서 적용한다. 이 저장소 자체는 이를 적용할 수
없다.

## Related Documents

- [정본 GitHub 거버넌스](../.agents/governance/github-governance.md)
- [로컬 main-protection 제안](./rulesets/main-protection.md)
- [에이전트 거버넌스 개요](../.agents/README.md)
- [현재 정본 에이전트 거버넌스 작업 체크리스트](../.agents/governance/task-checklists.md)
- Canonical home의 과거 결정: ADR-0032 (현재 권한은 위 에이전트 거버넌스가 소유)
- [저장소 README](../README.md)
- [문서 인덱스](../docs/README.md)
