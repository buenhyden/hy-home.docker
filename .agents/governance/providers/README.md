---
title: "Provider Adapters"
version: "1.1.0"
type: "governance/provider-index"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
---

# Provider Adapters

## Overview

Provider adapter는 agent governance policy, role, skill을 runtime syntax로
번역합니다. 공유 동작을 소유하지 않습니다.

## Scope

Claude와 Codex만 지원됩니다. `registry.yaml`은 provider identity, work-profile
model 선택, permission translation, projection path, semantic event, hook
command에 대한 machine authority입니다. workflow, approval, retry, evidence,
stop, document-profile 규칙은 소유하지 않습니다.

## Structure

- [Claude provider](../../../.claude/provider.md) — Claude의 authored loading 방식과 runtime 동작.
- [Codex provider](../../../.codex/provider.md) — Codex의 authored loading 방식과 runtime 동작.
- `registry.yaml` — 형식화된 provider와 projection fact.

## How to Work in This Area

provider-neutral 동작은 agent governance policy, role, skill source에서
변경합니다. provider fact는 `.agents/governance/providers/registry.yaml`에서
변경하고 대응하는 authored native `provider.md`를 갱신합니다. 생성된 native
README는 output일 뿐이며 canonical `.agents/` source는 결코 renderer
output이 아닙니다. 승인된 canonical 변경 후에는 provider renderer를
`--write`로 한 번 실행하고 즉시 `--check`로 실행합니다. 일반 validation과
CI는 `--check`만 사용합니다.
`--write`가 quarantine된 stale projection을 보고하면 멈춥니다: 이 명령은
active provider path에서 제거했지만 재검증된 blob을
`.provider-surface-quarantine/` 아래에 의도적으로 보존했습니다. 보고된
path를 승인된 retirement와 Git recovery boundary에 대해 검증하고 명시적
cleanup 단계에서 그 정확한 quarantine 파일만 제거한 뒤 `--write`와
`--check`를 다시 실행합니다. 대기 중인 cleanup은 실패한 `--check` 상태이며
convergence로 보고해서는 안 됩니다.

## Related Documents

- [Governance hub](../../README.md)
- [Bootstrap policy](../bootstrap.md)
- [Provider capability matrix](../provider-capability-matrix.md)
