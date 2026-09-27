---
title: "Workspace Staging Surface"
version: "1.3.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-03-05"
---

# Workspace Staging Surface

## Overview

`_workspace`는 저장소 로컬 staging 공간입니다. 여기 두는 산출물은 저장소 작업이
진행되는 동안 생성되고 단명하며 secret이 아닙니다. agent, 스크립트, migration이
임시 파일을 문서 stage, 런타임 설정, 영속적인 evidence 폴더 여기저기에 흩뜨리지 않고
선언된 한 곳에 두도록 이 공간을 마련했습니다.

이곳에는 authority가 하나도 없습니다. task가 끝난 뒤에도 남아야 하는 결과는
canonical owner로 요약해 옮기고, staging 사본은 폐기합니다.

## Audience

- task 도중 작업 파일이 필요한 agent와 스크립트
- evidence로 요약되기 전에 task가 만든 산출물을 검토하는 maintainer
- agent scratch 출력이 저장소에 도달하지 않았는지 감사하는 사람

## Scope

- 소유 대상: 아래 두 개의 tracked 계약 문서, 그리고 스크립트가 쓰는
  ignore 대상 `repo-support/` staging 트리
- 비소유 대상: 영속적인 evidence(co-located Stage 03 Task에 속함), operator
  절차(`docs/05.operations/`에 속함), 그리고 secret 값(항상 `secrets/`에
  속하며 이곳에는 절대 두지 않음)

## Structure

| Path | Tracked | Role |
| :--- | :--- | :--- |
| `README.md` | yes | 이 계약 문서 |
| `repo-support/README.md` | yes | staging 트리 계약 |
| `repo-support/**` | no | task 도중 기록되는 ignore 대상 런타임 산출물 |

여기에 쓰는 스크립트는 `repo-support/` 아래 하위 디렉터리 이름을
각자 정해 씁니다. 예를 들어 `scripts/security/verify-sample-service-supply-chain.sh`와
`scripts/operations/rehearse-postgres-logical-upgrade.sh`가 있습니다.

## Allowed Surface

런타임 산출물은 `repo-support/` 아래에 두며 기본적으로 ignore됩니다. 생성된
분석 요약, dry-run 미리보기, migration ledger, secret이나 raw 로그를 담지 않는
subagent 인계 파일이 그 예입니다.

## Prohibited Surface

다음 중 어느 것도 `_workspace` 아래에 두지 않습니다:

- 진단 덤프
- 로컬 로그나 raw 로그
- 인증 파일
- 토큰
- 자격 증명
- private key
- shell history
- secret 값
- 토큰이 포함된 명령 출력
- secret 파일 전체 본문

## Tracking Contract

루트 `.gitignore`는 `_workspace/` 아래 모든 것을 ignore하고, Structure에 명시된
두 개의 tracked 계약 문서만 다시 포함합니다. Git은 제외된 디렉터리 안으로
내려가지 않으므로, `repo-support/`는 다시 포함되고 그 내용물은 다시 제외된
뒤에야 `repo-support/README.md`가 복원됩니다. 바깥쪽 패턴을 이 사다리 구조를
다시 쓰지 않고 바꾸면 두 번째 문서가 조용히 빠집니다. 이 문장을 믿지 말고
규칙을 직접 검증합니다:

```bash
# doc-paths: illustrative
git check-ignore -v --no-index _workspace/repo-support/README.md
git check-ignore -v _workspace/repo-support/scratch.json
git ls-files _workspace/
```

`--no-index`를 붙여야 이 검사가 성립합니다. 이 옵션이 없으면 git이 먼저 index를
참고해 tracked 파일을 ignore된 것으로 답하기를 거부하므로 빠진 negation이
보이지 않습니다. 문서는 여전히 tracked 상태로 남고 그 문서의 ignore 여부를 묻는
질문에는 문서를 다시 포함시킨 규칙이 사라졌는데도 모두 "아니오"라는 답이 나옵니다.

exit status 대신 규칙을 읽어 판정합니다. `-v`는 매칭된 패턴이 제외하든 다시
포함하든 exit 0을 반환하므로 출력된 규칙으로만 둘을 구분할 수 있습니다: 정상적인
사다리는 negation `!/_workspace/repo-support/README.md`로 답하고 깨진
사다리는 바깥쪽 `/_workspace/*`로 답합니다. 두 번째 명령은 scratch 경로를
제외하는 규칙의 이름을 정확히 대야 하고, 세 번째 명령은 정확히 두 개의
tracked README 파일만 나열해야 합니다. 세 번째 tracked 경로가 나오면 산출물이
staging 계약을 벗어난 것입니다.

[tests/lib/test_surface_ownership.py](../tests/lib/test_surface_ownership.py)의
`test_workspace_contract_documents_stay_reachable`가 `-q`로 같은 질문을
던집니다. 이 테스트는 모든 게이트에서 실행되며 exit status로 둘을 실제로 구분합니다.
이제 이 계약은 누군가 명령을 직접 입력해 기억하는 데 의존하지 않습니다.

## How to Work in This Area

1. 산출물을 `_workspace/repo-support/<task-slug>/` 아래에 씁니다 → 경로가
   ignore 대상이므로 `git status`가 깨끗하게 유지됩니다.
2. secret이 아닌 결과를 co-located Stage 03 Task로 요약합니다 → 영속적인
   claim은 evidence와 함께 있어야지 staging에 남으면 안 됩니다.
3. 완료 전에 `git ls-files _workspace/`를 실행합니다 → 출력은 정확히 두 개의
   tracked 계약 문서여야 합니다.
4. 산출물을 그대로 두거나 삭제합니다 → 둘 다 괜찮습니다. 이곳에는
   복구해야 할 authority가 하나도 없습니다.

## Related Documents

- [Staging tree contract](./repo-support/README.md)
- [Subagent protocol](../.agents/governance/agentic.md)
- [Environment constraints](../.agents/governance/environment-constraints.md)
- [Task checklists](../.agents/governance/task-checklists.md)
- [Repository README](../README.md)
