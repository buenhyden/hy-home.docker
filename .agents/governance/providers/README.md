---
title: "Provider Adapters"
version: "1.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Provider Adapters

## Stage Responsibility

### Purpose and Readers

Provider adapter는 agent governance policy, role, skill을 runtime syntax로
번역합니다. 공유 동작을 소유하지 않습니다.

### Inputs and Outputs

Claude와 Codex만 지원됩니다. `registry.yaml`은 provider identity, work-profile
model 선택, permission translation, projection path, semantic event, hook
command에 대한 machine authority입니다. workflow, approval, retry, evidence,
stop, document-profile 규칙은 소유하지 않습니다.

## Contents

### Current Items

| Path | Purpose |
| --- | --- |
| [registry.yaml](registry.yaml) | provider identity와 native 번역 사실 |

- [Claude provider](../../../.claude/provider.md) — Claude의 authored loading 방식과 runtime 동작.
- [Codex provider](../../../.codex/provider.md) — Codex의 authored loading 방식과 runtime 동작.

### Classification

이 폴더의 정본은 `registry.yaml` 하나입니다. provider별 authored 문서(`.claude/provider.md`, `.codex/provider.md`)는 loading과 syntax 차이만 소유하며 공유 정책을 소유하지 않습니다.

## Workflow

### Create and Review

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

### Transition and Exit

이 README는 `navigation` 수명주기의 `active` 상태만 가지며 다른 상태로 전이하지 않습니다. 목록 항목을 추가·이동·삭제할 때 이 문서를 함께 갱신하고, 삭제한 항목의 이력은 Git이 기록합니다.

## Related Documents

### Upstream and Downstream

- [Bootstrap policy](../bootstrap.md)
- [Provider capability matrix](../provider-capability-matrix.md)

### Policy and Templates

- [Governance hub](../../README.md)
- [문서 작성 계약](../documentation-protocol.md#readme-and-agentsmd): README 형식과 언어 규칙의 정본
- 전용 템플릿 없음: Registry의 `governance-provider-index` profile(`docs/99.templates/registry.json`)이 형식을 소유합니다.
