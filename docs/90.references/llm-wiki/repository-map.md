---
status: active
---

# Reference: LLM Wiki Repository Map

## Overview (KR)

이 문서는 `hy-home.docker`를 읽는 LLM 에이전트가 먼저 확인해야 할 canonical tracked source files를 정리한 reference다. 저장소의 문서, 거버넌스, 인프라, script, secret-handling 경계를 빠르게 찾도록 돕는다.

## Purpose

LLM 에이전트가 runtime truth와 reference context를 혼동하지 않도록 repo-local 탐색 순서를 제공한다. 루트 [`llms.txt`](../../../llms.txt)는 이 문서를 가리키는 thin entrypoint이며, 이 문서는 active policy나 runtime 설정 원문을 대체하지 않는다.

## Repository Role

이 reference는 LLM Wiki의 curated repository map이다. 추적 파일을 기준으로 탐색 경로를 제공하며, 정책 판단은 `docs/00.agent-governance/`, 운영 판단은 `docs/05.operations/`, 최신 runtime truth는 `infra/`, `scripts/`, registry JSON 파일, Docker Compose 파일에서 확인한다.

Graphify 산출물은 navigation aid일 뿐이다. `graphify-out/`이 존재하더라도 authoritative source로 사용하지 않고, `bash scripts/report-graphify-health.sh` 결과가 `status=advisory`이면 모든 구조 판단을 canonical tracked source files로 재확인한다.

## Scope

### In Scope

- LLM 에이전트가 먼저 읽을 tracked source files 목록
- docs taxonomy, agent governance, infrastructure, scripts, secret-handling 진입점
- `secrets/`, `volumes/`, `graphify-out/` 경계
- repo-local LLM Wiki 산출물의 유지 규칙

### Out of Scope

- public wiki site, deployed wiki, full-content bundle, `llms-full.txt`
- Graphify publication wiring or regeneration policy
- Docker Compose runtime 변경
- 외부 모델 호출, 네트워크 게시, deployment workflow
- secret values, credentials, private keys, tokens, shell history, raw logs

## Definitions / Facts

- **LLM Wiki**: 루트 `llms.txt`와 `docs/90.references/llm-wiki/`로 구성된 repo-local 탐색 reference다.
- **Generated tracked repo-local index**: `scripts/generate-llm-wiki-index.sh`가 갱신하는 path-only index다.
- **Tracked source files**: Git이 추적하는 README, governance docs, operations docs, Compose files, scripts, registry JSON 파일을 뜻한다.
- **Runtime truth**: 현재 실행 설정과 검증 기준을 직접 정의하는 `infra/`, `scripts/`, registry JSON 파일, Docker Compose 파일, `docs/00.agent-governance/` 문서를 뜻한다.
- **Advisory graph context**: `graphify-out/` 산출물처럼 탐색 힌트로만 사용할 수 있고 canonical evidence로 승격하지 않는 보조 자료를 뜻한다.

## Repository Map

| Need | Canonical Source | Notes |
| --- | --- | --- |
| 저장소 개요 | [README.md](../../../README.md) | human-facing root hub |
| Agent 실행 규칙 | [AGENTS.md](../../../AGENTS.md) | provider-neutral entry shim |
| 문서 taxonomy | [docs/README.md](../../README.md) | active stage routing |
| Agent governance | [docs/00.agent-governance/README.md](../../00.agent-governance/README.md) | repo-local governance SSOT |
| Infrastructure layout | [infra/README.md](../../../infra/README.md) | Compose tier and service map |
| Script inventory | [scripts/README.md](../../../scripts/README.md) | validator and automation map |
| Secret handling | [secrets/README.md](../../../secrets/README.md) | path and policy context only |
| Docker reference context | [docs/90.references/docker/README.md](../docker/README.md) | stable Docker interpretation rules |
| LLM entrypoint | [llms.txt](../../../llms.txt) | thin machine-readable entrypoint |
| LLM generated index | [index.md](./index.md) | generated tracked repo-local path index |
| LLM maintenance guide | [docs/05.operations/guides/llm-wiki-maintenance.md](../../05.operations/guides/llm-wiki-maintenance.md) | refresh and validation procedure |

## Source Rules

- Prefer tracked source files over generated artifacts.
- Use repo-relative links for local files.
- Do not quote or summarize secret values, credentials, private keys, tokens, shell history, or raw logs.
- Treat `secrets/` paths as policy context only unless the user explicitly asks for a task that requires more.
- Exclude `volumes/`, dependency trees, generated/minified artifacts, and `graphify-out/` from authoritative evidence.
- Re-run repository validators after changing this reference or the root LLM entrypoint.

## Sources

- [README.md](../../../README.md) - repository purpose, map, verification entrypoints
- [AGENTS.md](../../../AGENTS.md) - agent bootstrap, Graphify boundary, verification contract
- [docs/README.md](../../README.md) - docs taxonomy, template mapping, contract validation
- [docs/90.references/README.md](../README.md) - reference stage role and lifecycle
- [scripts/check-repo-contracts.sh](../../../scripts/check-repo-contracts.sh) - repository contract validation
- [scripts/report-graphify-health.sh](../../../scripts/report-graphify-health.sh) - advisory Graphify health reporting

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when root README, docs taxonomy, agent governance, script inventory, or secret-handling docs change
- **Update Trigger**: Update when canonical entrypoints move, new tracked-source evidence boundaries are added, or LLM Wiki contract validation changes

## Related Documents

- [LLM Wiki references](./README.md)
- [LLM Wiki generated index](./index.md)
- [LLM Wiki maintenance guide](../../05.operations/guides/llm-wiki-maintenance.md)
- [LLM entrypoint](../../../llms.txt)
- [90.references](../README.md)
- [docs index](../../README.md)
- [agent governance hub](../../00.agent-governance/README.md)
