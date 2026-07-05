<!-- README Target: docs/90.references/llm-wiki/README.md -->

# LLM Wiki References

> LLM 에이전트가 `hy-home.docker`를 안전하게 탐색하기 위한 repo-local reference index

## Overview

`docs/90.references/llm-wiki`는 LLM 에이전트가 이 저장소를 읽을 때 사용할 수 있는 안정적인 탐색 기준을 관리합니다. 이 폴더는 루트 [`llms.txt`](../../../llms.txt)의 본문 reference 역할을 하며, active stage 문서와 runtime 파일의 위치를 중복 없이 연결합니다.

이 폴더는 배포 가능한 wiki site나 자동 생성 Graphify 산출물이 아닙니다. `llm-wiki-index.md`는 tracked source path만 나열하는 generated tracked repo-local index이며, 최신 runtime truth는 `infra/`, `scripts/`, registry JSON 파일, Docker Compose 파일, 그리고 `docs/00.agent-governance/`에서 유지합니다.

## Category Role

`docs/90.references/llm-wiki`는 tracked source files 기반의 LLM 탐색 지도입니다. 사람과 AI Agent가 같은 canonical 경로를 보도록 돕지만, 정책, 실행 계획, 운영 절차, incident 기록, runtime 설정 원문을 대체하지 않습니다.

Graphify 산출물은 corpus health가 clean일 때도 navigation aid로만 사용합니다. `graphify-out/` health가 advisory이면 이유가 runtime volume, gitlink/submodule, generated/minified artifact, meaningless god node, cross-root inferred edge 중 무엇이든 advisory evidence로 낮추고, 모든 판단은 추적 파일과 canonical docs로 재확인합니다.

## Language Rule

이 category README는 한국어를 기본으로 작성합니다. Generated `llm-wiki-index.md`, repo-local navigation labels, machine-readable path lists, and LLM-facing map text may use English when that improves provider-neutral parsing. Paths, commands, file names, agent names, and evidence labels must remain unchanged.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- LLM 에이전트용 repo-local entrypoint 설명
- generated tracked repo-local path index
- Stage 90 data coverage snapshot for LLM Wiki source-bucket/category counts
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
├── llm-wiki-index.md  # Generated tracked repo-local path index
└── repository-map.md  # Curated LLM navigation map for canonical tracked files
```

## Current References

- [llm-wiki-index.md](./llm-wiki-index.md) - generator가 갱신하는 repo-local path index
- [repository-map.md](./repository-map.md) - LLM 에이전트가 먼저 읽어야 할 canonical tracked source map
- [../data/knowledge/llm-wiki-stage-category-coverage.md](../data/knowledge/llm-wiki-stage-category-coverage.md) - Stage 90 data snapshot that groups safe tracked LLM Wiki paths by source bucket, category, and role

## How to Work in This Area

1. 루트 [`llms.txt`](../../../llms.txt)를 thin entrypoint로 유지하고, 상세 탐색 기준은 이 폴더에 둡니다.
2. 새 reference를 추가할 때는 [reference.template.md](../../99.templates/templates/common/reference.template.md)의 필수 섹션을 따릅니다.
3. `llm-wiki-index.md`는 `bash scripts/knowledge/generate-llm-wiki-index.sh`로 갱신하고 `--check`로 freshness를 확인합니다.
4. coverage snapshot은 `bash scripts/knowledge/generate-llm-wiki-coverage.sh`로 갱신하고 `--check`로 freshness를 확인합니다.
5. active policy, runbook, task evidence, runtime truth를 복제하지 말고 해당 canonical 문서로 연결합니다.
6. secret 값, credential, token, private key, shell history, raw log를 쓰지 않습니다.
7. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [LLM entrypoint](../../../llms.txt)
- [generated index](./llm-wiki-index.md)
- [generated coverage snapshot](../data/knowledge/llm-wiki-stage-category-coverage.md)
- [maintenance guide](../../05.operations/guides/00-workspace/llm-wiki-maintenance.md)
- [90.references](../README.md)
- [docs index](../../README.md)
- [agent governance hub](../../00.agent-governance/README.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
