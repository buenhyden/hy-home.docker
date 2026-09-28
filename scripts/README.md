---
title: "Utilities and Automation Scripts"
version: "1.1.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-02-21"
---

# Utilities & Automation Scripts (`scripts/`)

> Repository maintenance, utility scripts, and automation triggers.

## Overview

`scripts/` 디렉터리에는 빌드, 테스트, 환경 구성 등에 필요한 보조 스크립트와 자동화 도구가 있습니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 저장소 검증, 구현 정합성 점검, 계약 점검, 로컬 QA 게이트 오케스트레이션, agent 이벤트 훅 자동화 스크립트
- 계층별 하드닝 점검과 공유 헬퍼 라이브러리
- 로컬 preflight 검증 모드와 안전한 secret 파일 생성 유틸리티
- canonical purpose-folder 경로에 대한 스크립트 인벤토리와 lifecycle 소유권 규칙

### Out of Scope

- 평문 secret 값, 자격 증명, 토큰, 개인 키, 생성된 인증서 내용
- `docs/05.operations/`에 속하는 장문의 운영 절차
- `graphify-out/` 아래의 생성된 Graphify 산출물
- `infra/` 아래의 서비스별 Docker Compose 소스 파일

## Structure

```text
scripts/
├── validation/          # Compose, 저장소, 문서, 템플릿, quickwin, preflight 검증
├── hardening/           # tier 인자를 받는 통합 하드닝 점검
├── hooks/               # provider-neutral 훅 디스패처와 post-tool 검증
├── knowledge/           # Graphify 참고용 유틸리티
├── operations/          # 로컬 운영, 배포 rehearsal, 생성된 evidence 소유
├── security/            # 로컬 supply-chain 검증과 생성된 요약 소유
├── requirements.txt     # 저장소 검증 스크립트에 필요한 Python 모듈
├── requirements-pre-commit.txt # CI 전용 pre-commit 도구의 정확한 pin
├── lib/<domain>/        # import 전용 도메인 모듈; 공개 entrypoint 아님
├── lib/hardening-lib.sh # tier 하드닝 점검의 공유 구현
└── README.md            # 이 문서
```

## Purpose Folder Implementation

canonical script surface는 purpose-folder 경로입니다. docs, CI, hooks, pre-commit
참조가 purpose-folder 경로로 이동한 뒤 루트 레벨 `scripts/*.sh` 중복 파일은
제거했습니다. 승인된 향후 호환성 계획이 명시적으로 요구하지 않는 한 루트 중복
wrapper를 다시 만들지 않습니다.

`scripts/lib/<domain>/`은 import 전용 도메인 동작을 소유하며 공개 entrypoint를
정의하지 않습니다. `scripts/validation/`, `scripts/security/`,
`scripts/operations/` 같은 purpose 폴더가 entrypoint를 소유하고 도메인 로직을
라이브러리 계층에 위임합니다. `tests/lib/<domain>/`은 라이브러리 책임을 그대로
반영하고, `tests/validation/`은 CLI, entrypoint, 실행 컨텍스트 테스트를
유지합니다.

하드닝 표면은 의도적으로 `scripts/hardening/check-all-hardening.sh` 하나로
통합했습니다. tier별 wrapper entrypoint는 2026-05-17 정리에서
제거했으므로 대신 tier 인자를 사용합니다.

각 purpose 폴더의 정확한 스크립트 목록과 경로, 소유권, 테스트 evidence는
[`scripts/manifest.yaml`](manifest.yaml)이 소유합니다. 이 README는 폴더 단위
역할만 설명하며 개별 스크립트 행을 중복 기록하지 않습니다.

## How to Work in This Area

1. 스크립트를 추가, 이름 변경, 삭제하기 전에 이 README를 먼저 읽습니다.
2. 새 스크립트는 해당 동작을 소유하는 기존 purpose 폴더 아래에 둡니다.
3. purpose-folder 스크립트에 대한 루트 레벨 `scripts/*.sh` 중복 파일을 추가하지 않습니다.
4. docs, CI, hooks, pre-commit 항목에서는 canonical purpose-folder 경로를 참조합니다.
5. 여섯 개 공개 suite를 검증하려면 `python3 scripts/validation/run-ci-gate.py --profile full`을 사용합니다.
6. secret 관련 예시는 절차만 남기고, 생성된 secret 값을 출력하거나 문서화하지 않습니다.
7. 저장소 검증 스크립트의 Python 모듈 의존성은 `scripts/requirements.txt`에 유지합니다.

## Active Surface Retention Rules

다음 중 하나라도 해당하면 루트 `scripts/` 구현을 유지합니다:

- GitHub Actions, pre-commit, Claude/Codex 훅, 루트 README 파일, 활성 spec, 활성
  운영 문서, 또는 `infra/**/README.md`가 해당 스크립트를 참조하는 경우
- 다른 구현 스크립트가 이를 라이브러리로 source하는 경우
- 로컬 preflight 점검이나 로컬 secret 파일 생성처럼, 수동 작업의 유일한 canonical
  entrypoint인 경우

단순 중복 wrapper, 활성 문서에 이미 반영된 일회성 작업, 또는 승인된 호환성 계획
없이 재도입된 삭제 entrypoint는 제거하거나 반려합니다. 완료된 요구사항,
아키텍처 결정, 실행 evidence, 거버넌스 메모리, 생성된 참고 산출물 아래의 과거
참조는 감사 근거로만 쓰며 그것만으로 스크립트를 유지하지는 않습니다.

## Hardening Tier Arguments

선택한 tier 하나만 검사하려면 `bash scripts/hardening/check-all-hardening.sh <tier>`를
사용합니다. 인자가 없으면 지원되는 모든 tier를 검사합니다.

| Tier          | Accepted arguments                         |
| :------------ | :----------------------------------------- |
| Gateway       | `01-gateway`, `gateway`                    |
| Auth          | `02-auth`, `auth`                          |
| Security      | `03-security`, `security`                  |
| Data          | `04-data`, `data`                          |
| Messaging     | `05-messaging`, `messaging`                |
| Observability | `06-observability`, `observability`, `obs` |
| Workflow      | `07-workflow`, `workflow`                  |
| AI            | `08-ai`, `ai`                              |
| Tooling       | `09-tooling`, `tooling`                    |
| Laboratory    | `11-laboratory`, `laboratory`, `lab`       |

## Script Lifecycle

## Validation ownership

`.github/workflow-contract.yml`은 실행 가능한 구성 레지스트리입니다. 이 파일의
`public_gate.validators` 행마다 공개 suite를 정확히 하나 선언합니다:
`agent-governance`, `document-contract`, `document-graph`, `document-lifecycle`,
`operations`, 또는 `repository-integrity`. 각 행의 `contexts`는 canonical
standalone 호출이 로컬, PR, push, 수동 workflow dispatch 중 어디에서
허용되는지 선언합니다. `scripts/manifest.yaml`은 별도로 스크립트 인벤토리,
lifecycle, consumer, 테스트 evidence를 소유하며, 여기에는 executable suite,
argv, context 필드를 두지 않습니다. 최종 계획 승인은 상속된 호출과 canonical
호출을 모두 검사합니다: 로컬 계획은 CI 전용 하드닝을 생략하며 수동/런타임/
재귀적 validator 재바인딩은 실행 전에 실패합니다. 내부 호출에는 정확한 경로,
argv, 실행 컨텍스트가 필요하며 adapter 경로와 미분류 경로도 예외가
아닙니다. Explain은 같은 완전한 계획을 먼저 검증한 뒤 canonical validator
행을 렌더링합니다. workflow contract는 구성과 실행 정책의 drift를
거부합니다. 세부적인 document-governance 테스트는
`tests/lib/document_governance/` 아래에서 각 모듈을 그대로 반영하고, CLI와
통합 계약은 `tests/validation/`에 남습니다.

| Lifecycle                   | Scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI / quality gate           | `python3 scripts/validation/run-ci-gate.py --profile changed`, `python3 scripts/validation/run-ci-gate.py --profile full` |
| Advisory evidence           | `scripts/validation/check-document-metadata.py --mode report`, `evals/run-agent-output-eval-fixtures.sh`, `scripts/knowledge/report-graphify-health.sh` |
| Runtime hook                | `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/post-tool-validate.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tier hardening              | `scripts/hardening/check-all-hardening.sh <tier>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Manual operations           | `scripts/validation/validate-docker-compose.sh --preflight`, `scripts/operations/check-compose-core-readiness.sh --preflight`, `scripts/operations/rehearse-postgres-logical-upgrade.sh --check-config-only`, `scripts/security/seed-grype-db-cache.sh --preflight`, `scripts/security/seed-grype-db-cache.sh --seed`, `scripts/security/verify-sample-service-supply-chain.sh --preflight`, `scripts/security/verify-sample-service-supply-chain.sh --fixture-only`, `scripts/security/verify-sample-service-supply-chain.sh --advisory`, `scripts/operations/gen-secrets.sh`, `scripts/operations/rehearse-sample-service-delivery.sh preflight`, `scripts/operations/rehearse-sample-service-delivery.sh rehearse`, `scripts/operations/rehearse-sample-service-delivery.sh cleanup` |
| Agent QA/CI environment     | `source scripts/operations/use-qa-ci-tools.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Internal library            | `scripts/lib/hardening-lib.sh`, `scripts/lib/ops/compose-core-readiness.sh` |

`scripts/operations/gen-secrets.sh`는 수동 운영 entrypoint입니다. 인자 없이
실행하는 기본 모드는 로컬 secret registry와 secret 파일을 읽거나 쓸 수
있습니다. 기본 모드를 실행하기 전에 준비 상태 점검에는 `--check`를, ID/경로만
보여주는 미리보기에는 `--dry-run`을 사용합니다.

`scripts/security/seed-grype-db-cache.sh`는
[supply-chain 정책 검사기](validation/check-supply-chain-policy.py)가
관장합니다. 승인된 pinned-Grype 데이터베이스 네트워크 경계는 명시적인
`--seed` 모드에서만 사용할 수 있고 `--preflight`는 네트워크를 사용하지
않습니다. consumer인 `verify-sample-service-supply-chain.sh --advisory`는
데이터베이스를 갱신하거나 내려받지 않습니다. 게시된 불변 seed를 재검증한 뒤
private offline scan 캐시로 복사합니다.

`scripts/hooks/post-tool-validate.sh`는 훅 payload consumer입니다. JSON
payload가 없거나 변경된 경로가 없으면 validator를 실행하지 않고 성공으로
종료합니다. 기본값은 non-mutating이며 diff, syntax, lint, repo 점검은 쓰기
없이 실행됩니다. `--write`를 주면 whitespace normalizer가 활성화되며
`agent-event-hook.sh`의 런타임 post-edit 훅이 이 옵션을 전달합니다.
`POST_TOOL_VALIDATE_CHECK_ONLY=1`은 `--write`가 있어도 check-only 모드를
강제합니다. whitespace normalizer가 이 훅의 유일한 mutation이며,
`.pre-commit-config.yaml`에 등록된 mutator 경계를 읽으므로 고정된(frozen)
archive payload는 바이트 그대로 유지됩니다. 이 훅은 호출자가 준비한 도구 탐색
순서를 그대로 유지하며 `scripts/operations/use-qa-ci-tools.sh`를 자동으로
source하지 않습니다. 선택적 QA/CI 도구를 다른 방법으로 사용할 수 없을 때는 이
헬퍼를 명시적으로 source합니다. 반복 source해도 기존 PATH 순서는 유지되고
사용 가능한 디렉터리만 한 번씩 추가됩니다.

`scripts/validation/run-ci-gate.py`는 의존성 없는 typed-gate CLI입니다.
`.github/workflow-contract.yml`을 읽어 닫힌 `changed` 또는 `full` 공개
profile을 선택하고, `--explain`은 실행 없이 유지합니다. Explain과 실제 실행은
동일한 context-filtered, exact-once canonical 계획을 사용합니다. `--explain`은
standalone validator 계획을 출력하며 parity 테스트는 이 계획이 같은 profile에서
실행되는 validator와 일치하는지 확인합니다. profile은 등록된 regression leaf도
실행하지만 explain은 이를 나열하지 않으므로, explain 출력은 validator
계획으로만 읽고 실행의 전체 내용이나 비용으로 읽지 않습니다. PR과 초기 push가
아닌 push의 base는 검증되어 `TEMPLATE_GATE_BASE`로 전달되며, 로컬·초기
push·workflow dispatch는 비교 base를 임의로 만들지 않고 명시적인
active-corpus metadata 모드를 사용합니다.

`scripts/validation/check-document-metadata.py`는 Stage 99 typed profile
계약과 중복 키를 거부하는 PyYAML safe loading을 사용합니다. `--mode report`는
항상 정렬된 대상 문서 인벤토리를 렌더링하고 의미적 gap은 advisory로
처리하며, parser/설정 오류는 계속 error로 남습니다. canonical snapshot을
생성하려면 `--output <path>`를 사용하고, 최신성 확인에는 `--check`를
추가합니다. `--mode check-contracts` 저장소 게이트는 로드된 레지스트리를
재사용합니다. 이 게이트를 통과하려면 README 소유권이 정확해야 하고 복사 가능
Markdown 템플릿 매핑이 완전하고 타입이 일관되어야 합니다. 전체 레지스트리 배열은
단일 기계 소유권 아래 있어야 하며 docs 인벤토리 추론에서는 `_workspace`를
제외해야 합니다. `check-changed`는 안전하게 선택된 diff에 대한
pre-push 차단 모드이고, `check-active`는 base 없이 동작하는 active-corpus
점검입니다. base를 정할 때는 명시적 참조, CI, 안전한 로컬 참조를 우선하며 그
다음에는 전체 corpus를 선택하지 않고 working-tree 전용 fallback을
보고합니다. base가 존재하는 좁은 legacy 예외는 새 문서나 부분적인 typed
마이그레이션에는 적용할 수 없습니다. 역방향 전환에는 범위를 지정한 별도 evidence
manifest가 필요하며 기본 훅은 이를 제공하지 않습니다. legacy 예외는 base
레코드를 base manifest와 대조 검증합니다. 허용하는 것은 merge base에 이미 존재하는
안정적인 현재 deficit identity뿐입니다. 템플릿 placeholder 점검은 조합된 scalar와
list 안의 등록된 angle-bracket 토큰을 재귀적으로 탐지하며, 날짜 형태의 ID
텍스트를 전역 placeholder로 취급하지 않습니다. 집중 suite는
`python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py' -v`로
실행합니다. 변경 경로 검토에는 tracked, staged, unstaged-new, renamed, 명시적으로
존재하는 Markdown 경로가 들어가며 삭제는 파싱할 수 없는 선택 경로로
처리합니다. 이 report는 Task 4 인벤토리의 모든 필드마다 결정론적 semantic
상태를 노출합니다. YAML/설정 결함은 raw traceback이나 안전하지 않은 metadata
값을 드러내지 않고 정규화합니다.

`scripts/validation/check-document-corpus-lifecycle.py`는 lifecycle 전용
companion입니다. 등록된 게이트에서 도달할 수 있는 모드는
정확히 네 개입니다: `--mode check-public`, `--mode check-contract`,
`--mode check-promoted`, 그리고 모든 tombstone의 `commit:path`가 정상적인 Git
blob으로 해석되는지 다시 증명하는 `--mode check-recovery`입니다. 그 외의
`--mode` 값은 argparse 오류입니다. parser, contract, Git, path, redaction,
내부 안전성 실패는 여전히 fail-closed로 처리됩니다. 집중 인벤토리는
`python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py' -v`로
실행합니다. 실행 가능한 테스트 인벤토리는 `tests/validation/lifecycle/` 아래
네 개 책임 모듈이며, legacy 통합본이나 redirect는 남아 있지 않습니다.

`scripts/validation/run-agent-precommit-all-files.sh`는
`pre-commit run --all-files`용으로 승인된 유일한 agent entrypoint입니다.
승인된 최종 QA 게이트에서 실행하며 초기 상태가 깨끗한 linked worktree에서 tracked된
`docs/03.specs/####-<slug>/tasks/tsk-####-<slug>.md` 경로 하나와 저장소 상대
경로인 `--allow-prefix` 값 하나 이상을 함께 넘깁니다. all-files를 직접
실행하는 것은 금지됩니다. 이 wrapper는 훅 출력을 임시 파일에 담고 보고하는 것은 명령,
prefix, 훅 exit, 값이 없는 first-failure 결과, 변경 전/후/새로 변경된
Git-visible 경로뿐입니다. 실행이 성공하면 `first_failure=not_applicable`을
보고합니다. 훅 exit이 0이 아니면 튜플을 최대 하나 보고합니다. 이 튜플에는 정확하고
고유하게 등록된 `.pre-commit-config.yaml` 훅 ID와, `exit_0`부터 `exit_255`까지 또는
`files_modified` 중 하나가 담깁니다. metadata가 없거나
잘못되었거나 미등록·중복·모호·과대·바이너리이거나 위조 가능하면
`first_failure=unavailable`을 보고합니다. 훅 이름, 메시지, 소요 시간, 원본
명령 출력, 출력에서 파생된 경로, 설정이나 환경 값, secret은 절대 출력하지
않습니다. 이 wrapper는 task evidence를 쓰지 않습니다. exit `20`은 훅이 새로 관측된 경로 중 모든
prefix 밖에 있는 경로를 변경했다는 뜻입니다. 그 외에는 wrapper가 훅의
exit 상태를 그대로 반환합니다. 훅이 반영한 편집은 별도로 검토하고
기록합니다. 예상치 못한 결과를 숨기기 위해 reset, checkout, clean을 사용하지
않습니다.

관측 경계는 `git status`가 보고하는 Git-visible 저장소 경로 중 ignore되지 않은
경로로 제한됩니다. ignore된 경로와 저장소 밖의 쓰기는 관측되지 않습니다. 이
wrapper는 프로세스나 파일시스템 샌드박스가 아닙니다. Task evidence도 이와
같은 좁은 claim을 사용해야 합니다. task와 기존 allow-prefix 경로 구성
요소는 symlink여서는 안 되며 존재하지 않는 allow-prefix 말단은 새 출력이라면
유효합니다. before/after Git snapshot이 실패하면 빈 경로 집합을
성공으로 처리하지 않고 exit `6`으로 종료합니다.

저장소 로컬 Hookify 검증은 `python3 scripts/validation/run-ci-gate.py --profile changed`로
선택하며 provider 훅은 atomic validator 명령을 복제하지 않습니다.

---

## Utilities & Automation

### Standard Rules

- **Idempotency**: 모든 스크립트는 여러 번 실행해도 상태가 깨지지 않도록 안전해야 합니다.
- **No Secrets**: 스크립트는 자격 증명을 환경 변수에서 가져와야 하며 절대 하드코딩하지 않습니다.
- **Deterministic**: 추가하는 모든 자동화는 `../.agents/governance/`의 저장소 거버넌스를 따라야 합니다.

### Usage Examples

```bash
# doc-paths: illustrative
# 더미 파일을 만들지 않고 실제 로컬 preflight 점검을 실행합니다
./scripts/validation/validate-docker-compose.sh --preflight

# 여섯 개 공개 suite를 모두 강제합니다
python3 scripts/validation/run-ci-gate.py --profile full

# traceability, 구현 정합성, docs entry point 점검을 한 번에 강제합니다
python3 scripts/validation/check-document-links.py --mode all

# Quick Win baseline을 강제합니다
./scripts/validation/check-quickwin-baseline.sh

# 명시적 compose profile 집합에 대해 Quick Win baseline을 강제합니다
# 선택한 profile 중 하나라도 baseline 위반이 있으면 실패합니다.
HYHOME_COMPOSE_PROFILES="core dev" ./scripts/validation/check-quickwin-baseline.sh

# 템플릿 + 보안 baseline을 강제합니다
./scripts/validation/check-template-security-baseline.sh

# 변경 경로에 대한 공개 suite를 실행합니다
python3 scripts/validation/run-ci-gate.py --profile changed

# 실행 없이 변경 경로 suite-validator 소유권만 설명합니다
python3 scripts/validation/run-ci-gate.py --profile changed --explain


# 승인된 최종 QA 전용; prefix는 task의 검토 범위와 일치해야 합니다
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/03.specs/9999-example-change/tasks/tsk-0001-example.md \
  --allow-prefix docs/ \
  --allow-prefix scripts/

# advisory Graphify corpus 상태를 보고합니다
./scripts/knowledge/report-graphify-health.sh

# canonical agent governance 파생 provider skill projection을 검증하거나 재생성합니다
python3 scripts/operations/provider_surface_renderer.py --check
python3 scripts/operations/provider_surface_renderer.py --write

# provider-neutral PreToolUse 훅 이벤트를 dispatch합니다
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | bash scripts/hooks/agent-event-hook.sh PreToolUse

# 포맷팅 쓰기 없이 provider-neutral post-edit 검증을 실행합니다 (기본값)
printf '{"tool_input":{"file_path":".agents/governance/task-checklists.md"}}' | bash scripts/hooks/post-tool-validate.sh

# post-edit 훅과 동일하게 실행하며 변경된 파일의 whitespace를 정규화합니다
printf '{"tool_input":{"file_path":".agents/governance/task-checklists.md"}}' | bash scripts/hooks/post-tool-validate.sh --write

# 모든 tier 하드닝 baseline을 강제합니다
./scripts/hardening/check-all-hardening.sh

# 선택한 tier 하나만 강제합니다
./scripts/hardening/check-all-hardening.sh 01-gateway

# secret 값을 읽거나 쓰지 않고 secret 생성 준비 상태를 점검합니다
./scripts/operations/gen-secrets.sh --check

# ID/경로만으로 secret 생성 동작을 미리 봅니다
./scripts/operations/gen-secrets.sh --dry-run

# tech-stack 버전 레지스트리가 선언된 compose 태그와 동기화되어 있는지 검증합니다
bash scripts/operations/sync-tech-stack-versions.sh --check

# 쓰지 않고 예정된 tech-stack 레지스트리 태그 갱신을 미리 봅니다
bash scripts/operations/sync-tech-stack-versions.sh --dry-run

# tech-stack 레지스트리를 선언된 compose 태그로 다시 맞춥니다
bash scripts/operations/sync-tech-stack-versions.sh --write



# 기존 PATH 우선순위를 유지한 채 선택적 QA/CI 도구를 명시적으로 추가합니다
source scripts/operations/use-qa-ci-tools.sh

# agent가 사용할 수 있는 QA/CI 툴체인을 확인합니다
./scripts/operations/use-qa-ci-tools.sh

```

---

## Invocation Safety

check-only validator는 `mutation: none`을 사용합니다. Generator와
synchronizer는 `mutation: check-write`를 사용합니다: 기본 호출은 저장소
상태를 바꾸지 않고 점검하거나 렌더링해야 하며, 저장소를 실제로 갱신하려면
명시적인 `--write`가 필요합니다. 유지되는 check-write generator는 안전한
argv `check_command`와 자신이 소유하는 정확한 tracked `outputs`를 등록합니다.
`mutation: runtime` 스크립트는 Operations entrypoint입니다. 문서 마이그레이션
중에는 실행하지 않으며 명시적으로 호출하려면 먼저 현재 Runbook과 선언된 테스트
evidence가 필요합니다. 두 all-files pre-commit runner는 fixer 훅이 파일을
다시 쓰기 때문에 `check-write`입니다. `run-ci-precommit.sh`는 일회용 GitHub
Actions checkout에서만 실행되고, `run-agent-precommit-all-files.sh`는 격리된
linked worktree에서만 실행됩니다.

전환(transition) 행에는 non-retain disposition, 구분되는 tracked successor,
비어 있지 않은 `removal_condition`이 모두 있어야 합니다. active 행은
`removal_condition`을 생략합니다.

인벤토리나 마이그레이션 evidence로부터 `mutation: runtime` 행을 호출하지
않습니다. 대신 현재 Runbook과 명시적인 operator 경계를 따릅니다. 문서화된
non-mutating check 옵션 없이 default-write generator를 호출하지 않습니다.
안전한 기본값이 없는 행은 재작성이나 병합 대상으로 분류됩니다. Consumer와
테스트로 인정하려면 의미 있는 호출/import evidence가 있어야 합니다: manifest 언급, 생성된
index, archive 기록, 소유권 glob만으로는 소비(consumption)로 인정되지
않습니다.

유지 관리되는 LLM Wiki generator는 없습니다. tracked output과 함께
제거했습니다. 저장소 탐색은 `.agents/knowledge/` 아래의 canonical
knowledge map과 루트 `llms.txt` entry point가 소유하며,
`scripts/knowledge/report-graphify-health.sh`는 쓰기 없이 advisory Graphify
상태만 보고합니다.

## Verification

manifest와 생성된 output 게이트는 다음으로 실행합니다:

```bash
python3 scripts/validation/check-script-manifest.py
python3 scripts/validation/check-script-manifest.py --check-generated
PYTHONPATH=. .venv/bin/python tests/validation/test_script_manifest.py
```

이 게이트는 tracked 경로와 현재 존재하는 non-ignored Task-local 경로에서
커버리지를 도출합니다. 정확한 필드와 어휘 계약을 검증하고 결정론적 순서를
확인하며 선언된 모든 consumer와 테스트 경로는 호출/import evidence를
포함해야 합니다. `--check-generated`는 유지되는 check-write generator 중
`check_command`와 `outputs`를 선언한 것만 실행하며 runtime을 변경하는 행은
절대 호출하지 않습니다. 현재 두 조건을 모두 선언한 행은 없으므로 이 모드는
기본 점검 이상을 추가하지 않습니다.

## Related Documents

- [🤖 Agent Governance](../AGENTS.md)
- ⚙️ Operations Baseline (`docs/05.operations/README.md`)
- 📘 Runbooks (`docs/05.operations/runbooks/README.md`)
- [Public Suite Ownership Manifest](manifest.yaml)
- [Agent Evaluation Harness](../evals/README.md) - 형제 자동화 루트; `evals/README.md`가 이 manifest도 등록하는 eval 표면을 소유합니다
- Workspace Governance Authority (`docs/02.architecture/decisions/0032-canonical-agent-governance-home.md`)
- Document Profile Registry (`docs/99.templates/registry.json`)
- [Documentation index](../docs/README.md)

Note: QuickWin baseline exceptions are sourced from `infra/common-optimizations.exceptions.json`.
