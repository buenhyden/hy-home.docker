---
title: Agent Evaluation Harness
version: 1.0.0
type: common/repository-readme
status: active
owner: "@buenhyden"
created: '2026-09-03'
updated: '2026-09-03'
---

# evals

> 이 저장소의 에이전트 평가 하니스가 사는 곳

## Overview

`evals/`는 에이전트 출력 품질을 결정론적으로 채점하는 하니스를 소유합니다.
고정된 픽스처 카탈로그와 합성 회귀 집합을 가지고, 모델 호출 없이 로컬과 CI에서
동일한 점수를 냅니다.

하니스가 검증하는 것은 **저장소 의미론**입니다. 살아 있는 모델이나 제공자 간
품질 비교는 여기서 주장하지 않으며, 그런 평가는 별도 승인 대상입니다.

`scripts/`는 저장소를 검사하는 자동화를, `evals/`는 에이전트 출력을 채점하는
자동화를 소유합니다. 두 경로 모두 `scripts/manifest.yaml`이 등록합니다.

## Audience

- 픽스처나 채점기를 조정하는 `eval-engineer`
- 게이트 실패 원인을 확인하는 QA 소유자
- 평가 근거를 검토하는 Reviewers

## Scope

### In Scope

- 픽스처 카탈로그, 채점기, 임계값, 합성 회귀 집합
- 로컬·CI 공용 실행 진입점

### Out of Scope

- 살아 있는 모델 호출과 제공자 간 비교 점수
- 픽스처의 서술적 근거 문서 — [Stage 90 픽스처 참조](../docs/90.references/data/0064-agent-output-eval-fixtures/README.md)가 소유합니다
- 회귀 테스트 자체 — `tests/validation/test_agent_output_eval_fixtures.py`가 소유합니다

## Structure

| Path | Role |
| :--- | :--- |
| `agent_output_eval.py` | 픽스처 카탈로그, 채점기, 임계값, 회귀 집합 |
| `run-agent-output-eval-fixtures.sh` | 로컬·CI 공용 실행 진입점 |
| `README.md` | This file |

## Tech Stack

표준 라이브러리 Python 3만 사용합니다. 네트워크 호출, 모델 SDK, 서드파티 의존성이
없어야 결정론이 유지됩니다.

## Validation

```bash
bash evals/run-agent-output-eval-fixtures.sh --list
bash evals/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions
```

두 번째 명령은 `fixtures_check=pass`와 `regressions_check=pass`를 출력하고 종료 코드
`0`을 반환합니다. 공개 게이트는 같은 실행을 `leaf.agent-output-eval-fixture-gate`
노드에서 어댑터를 통해 호출합니다.

## How to Work in This Area

1. 픽스처를 추가하거나 임계값을 바꾸기 전에 [Stage 90 픽스처 참조](../docs/90.references/data/0064-agent-output-eval-fixtures/README.md)를 먼저 갱신합니다 → 하니스가 그 문서를 카탈로그 근거로 읽습니다.
2. `agent_output_eval.py`의 `FIXTURES` 항목을 참조 문서와 일치시킵니다 → `--check-fixtures`가 `pass`.
3. 회귀 집합을 함께 갱신합니다 → `--check-regressions`가 `pass`.
4. `scripts/manifest.yaml`의 해당 행을 갱신합니다 → `python3 scripts/validation/check-script-manifest.py`가 종료 코드 `0`.
5. `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다 → 종료 코드 `0`.

새 실행 파일을 이 폴더에 추가하면 매니페스트 행이 반드시 필요합니다.
`check-script-manifest.py`의 `MANIFEST_ROOTS`가 `evals/`와 `scripts/`를 같은
규칙으로 다루므로, 등록하지 않은 파일은 게이트가 막습니다.

## Related Documents

- [Fixture reference](../docs/90.references/data/0064-agent-output-eval-fixtures/README.md)
- [Provider model evaluation skill](../docs/00.agent-governance/skills/provider-model-evaluation.md)
- [Script manifest](../scripts/manifest.yaml)
- [Scripts surface](../scripts/README.md)
- [Test surface](../tests/README.md)
- [Root README](../README.md)
