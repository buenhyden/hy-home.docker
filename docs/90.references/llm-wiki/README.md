# LLM Wiki References

> LLM 에이전트가 `hy-home.docker`를 안전하게 탐색하기 위한 repo-local reference index

## Overview

`docs/90.references/llm-wiki`는 LLM 에이전트가 이 저장소를 읽을 때 사용할 수 있는 안정적인 탐색 기준을 관리합니다. 이 폴더는 루트 [`llms.txt`](../../../llms.txt)의 본문 reference 역할을 하며, active stage 문서와 runtime 파일의 위치를 중복 없이 연결합니다.

이 폴더는 배포 가능한 wiki site나 자동 생성 Graphify 산출물이 아닙니다. 최신 runtime truth는 `infra/`, `scripts/`, registry JSON 파일, Docker Compose 파일, 그리고 `docs/00.agent-governance/`에서 유지합니다.

## Category Role

`docs/90.references/llm-wiki`는 tracked source files 기반의 LLM 탐색 지도입니다. 사람과 AI Agent가 같은 canonical 경로를 보도록 돕지만, 정책, 실행 계획, 운영 절차, incident 기록, runtime 설정 원문을 대체하지 않습니다.

Graphify 산출물은 corpus health가 clean일 때도 navigation aid로만 사용합니다. 현재처럼 `graphify-out/`에 runtime volume이나 gitlink/submodule 오염이 포함되면 advisory evidence로 낮추고, 모든 판단은 추적 파일과 canonical docs로 재확인합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- LLM 에이전트용 repo-local entrypoint 설명
- canonical README, governance, infra, scripts, secrets 문서의 탐색 순서
- tracked source files 기반 evidence boundary
- `secrets/`, `volumes/`, `graphify-out/` 사용 경계

### Out of Scope

- public documentation site 또는 wiki deployment
- `llms-full.txt` 생성
- Graphify publication wiring
- 외부 모델 호출, 네트워크 게시, runtime hook 추가
- secret values, credentials, private keys, tokens, shell history, raw logs

## Structure

```text
llm-wiki/
├── README.md          # This file
└── repository-map.md  # Curated LLM navigation map for canonical tracked files
```

## Current References

- [repository-map.md](./repository-map.md) - LLM 에이전트가 먼저 읽어야 할 canonical tracked source map

## How to Work in This Area

1. 루트 [`llms.txt`](../../../llms.txt)를 thin entrypoint로 유지하고, 상세 탐색 기준은 이 폴더에 둡니다.
2. 새 reference를 추가할 때는 [reference.template.md](../../99.templates/reference.template.md)의 필수 섹션을 따릅니다.
3. active policy, runbook, task evidence, runtime truth를 복제하지 말고 해당 canonical 문서로 연결합니다.
4. secret 값, credential, token, private key, shell history, raw log를 쓰지 않습니다.
5. 변경 후 `bash scripts/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [LLM entrypoint](../../../llms.txt)
- [90.references](../README.md)
- [docs index](../../README.md)
- [agent governance hub](../../00.agent-governance/README.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
