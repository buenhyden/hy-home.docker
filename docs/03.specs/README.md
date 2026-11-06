---
title: "명세 패키지"
version: "1.3.8"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
---

# 명세 패키지

## Overview

`docs/03.specs`는 범위가 정해진 변경의 명세와 실행 package를 관리합니다.
package마다 Spec이 관찰 가능한 동작과 acceptance를, Plan이 구현 순서와
위험을, Task가 실제 실행·검증·검토 증거를 소유합니다. 오래 유지할 구조와
운영 의미는 Stage 01·02·05의 현재 문서로 승격합니다.

이 README는 현재 package로 가는 길만 안내합니다. package 안의 Spec, Plan,
Task와 그 상태는 각 package가 소유하므로 여기에 옮겨 적지 않습니다.

## Scope

- 포함: 진행 중인 변경, 검증이 끝나 삭제 승인을 기다리는 package의
  Spec·Plan·Task와 Spec이 직접 소유하는 실행 가능한 contract.
- 제외: 운영 절차, 감사·조사 데이터, 이미 삭제된 package의 본문, 이전 경로의
  복제본과 redirect. 운영·참조 자료는 각 Stage의 현재 owner가 소유합니다.
  삭제된 package의 번호는 Registry `reserved_history`에 남고, 본문은 Git
  history가 기록합니다.

## Structure

package 하나가 직접 하위 디렉터리 하나입니다. 디렉터리 이름은
`<4자리 번호>-<slug>`이며 package 안의 파일 경로와 역할은
[Stage 99 Registry](../99.templates/registry.json)가 소유합니다.
`design.md`, `tests.md`, 단수형 `task.md`는 package 역할이 아닙니다.

### 현재 package

| ID | Package | 목적 |
| --- | --- | --- |
| SPEC-0204 | [서비스 연동·보안·운영](./0204-service-integration-security-and-operations/) | 공통 서비스 호환성·외부 연결·백업 경계의 승인용 계약 |
| SPEC-0212 | [요청 기준선·정합화](./0212-request-baseline-and-reconciliation/) | 2026-10-07 요청의 기준선, 서비스 키 인벤토리, 충돌 지도, 후속 package 순서 |
| SPEC-0218 | [공통 control·예외](./0218-common-controls-and-exceptions/) | root·LAB 모든 서비스의 최종 control을 정확한 예외와 대조, secret group·capability·PID 예산 정리 |
| SPEC-0226 | [AI 런타임 고정 검증](./0226-ai-runtime-pin-verification/) | Ollama·Open WebUI digest 고정, 모델 load·대기열 한도, 세션 key·모델 catalog 백업과 격리 복원·기능 검증 |
| SPEC-0244 | [Native memory 통제 검증](./0244-native-memory-controlled-verification/) | Claude native memory effective-state와 hook delivery를 설정·메뉴·영수증별로 분리해 통제 검증 |
| SPEC-0245 | [Observability CA 실행](./0245-observability-ca-execution/) | Prometheus·Gatus의 백업·격리 복원 검증 후 순차 CA 재생성과 rollback 경계 |
| SPEC-0248 | [Archive·migration 검사 폐기](./0248-archive-and-migration-check-retirement/) | Stage 98 기록과 migration ledger를 검증하던 gate를 삭제하고 현재 검사가 쓰는 읽기 전용 loader와 legacy 허용만 남겨 목록으로 관리 |
| SPEC-0249 | [Stage 98 archive 삭제](./0249-stage98-archive-deletion/) | Stage 98 기록을 01·02 문서에 요약하고 삭제하며, 폐기 번호를 Registry `reserved_history`로 옮기고 archive를 읽던 검사를 제거 |
| SPEC-0250 | [완료 Spec package 삭제](./0250-finished-spec-package-deletion/) | 모든 문서가 terminal인 Spec package를 삭제하고 번호를 Registry `reserved_history`에 예약하며, 현재 문서의 링크를 일반 텍스트로 바꿈 |
| SPEC-0251 | [README와 AGENTS.md 분리](./0251-readme-and-agents-guide-split/) | README는 사람, 폴더 AGENTS.md는 AI agent를 대상으로 나누고, AGENTS.md를 둘 폴더의 규칙과 9개 폴더 guide를 정합니다 |
| SPEC-0253 | [QA·CI legacy 정리](./0253-qa-ci-legacy-cleanup/) | 빈 frozen archive payload 경계와 삭제된 Task를 가리키던 CI gate evidence owner를 정리하고, 일회성 script·test를 점검합니다 |
| SPEC-0254 | [Agent guide 후속 정리](./0254-agent-guide-follow-ups/) | infra README의 개별 stage 링크를 정리하고, 폴더 guide 변경이 agent-governance suite를 고르게 하며, guide type을 `common/agent-guide`로 바꾸고 guide를 사용 상태로 전환합니다 |
| SPEC-0255 | [구현 정합성 수정](./0255-implementation-alignment-fixes/) | 감사에서 확인된 문서와 구현의 차이 중 열린 branch 밖의 항목을 고칩니다: AD-0026 network, 삭제된 Spec을 현재 소유자로 가리키는 문구, 운영 문서의 secret 이름과 database 목록 |
| SPEC-0256 | [Legacy 문서 상태 금지](./0256-legacy-document-status-ban/) | Stage 01~03 lifecycle에서 legacy 상태와 lineage key를 없애고, ADR-0011을 요약·삭제하며, archive scaffolding을 정리함 |
| SPEC-0257 | [구현 정합성 수정 2차](./0257-implementation-alignment-batch2/) | infra README의 운영 문서 경로, Grafana 링크, Registry의 깨진 예외 항목, 누락된 secret 이름을 바로잡습니다. |
| SPEC-0259 | [구현 정합성 수정 3차](./0259-implementation-alignment-batch3/) | 삭제된 Spec 경로를 라벨로 쓰는 Stage 02 링크, OpenBao audit 서술, 구현과 일치하는 Stage 05 문서의 승격을 다룹니다 |
| SPEC-0261 | [REQ-0027 승인](./0261-req-0027-approval/) | REQ-0027 요구사항 승인과, 구현과 일치하는 AD-0031, AD-0032, Stage 05 문서의 승격을 다룹니다 |
| SPEC-0260 | [SPEC-0209·0231 삭제](./0260-spec-0209-0231-retirement/) | generation 5·6 migration proof를 generation 6 revision에서 읽게 하고, proof를 지녔던 두 package를 삭제해 번호를 Registry `reserved_history`에 예약함 |
| SPEC-0262 | [분석 서비스 LAB 이전](./0262-analytics-labs-migration/) | Lakehouse, dbt, Superset, JupyterLab, SonarQube, Stalwart를 root Compose에서 독립 LAB entrypoint로 옮기고, 참조와 Stage 05 문서를 `15-labs`로 정리함 |
| SPEC-0263 | [LAB 이전 계약](./0263-lab-promotion-contract/) | LAB의 표준 구조, 이전 명세, LAB secret 복사본, infra·운영 문서 이동 규칙, 이전 전 자원 공존 점검과 세 가지 이전 절차를 정함 |
| SPEC-0264 | [폴더 guide 전달](./0264-folder-guide-delivery/) | Codex와 Claude가 읽지 못하는 폴더 AGENTS.md를 Claude는 생성된 폴더 `CLAUDE.md` import shim으로, Codex는 공유 hook으로 받게 함 |
| SPEC-0265 | [Hermes 보고서 원문 계약](./0265-hermes-report-source-capture/) | Hermes가 Gateway로 보내는 `source_text`를 확정된 전체 일일 보고서 원문으로 바꾸고, 이메일·Telegram·Gateway가 같은 저장 바이트에서 나오게 하며, schema 5 전환과 backfill 제외를 운영 작업으로 분리함 |

처분된 package의 본문은 Git 이력에서 찾습니다.
package가 removal review 준비 상태인지는 [SDLC](../../.agents/governance/sdlc.md#sequence)
규칙대로 읽을 때 계산하며 표나 frontmatter에 적지 않습니다. 새 lifecycle
상태도, 처분 승인도 아닙니다.

### 역할 계약

| 역할 | 책임 |
| --- | --- |
| Spec | 범위가 정해진 관찰 가능한 동작, 범위, 실패 모드, acceptance 계약 |
| Plan | 승인된 실행 순서, 위험, rollback, 완료 기준 |
| Task | 실제 작업 기록, 명령 결과, 검토, commit, 이연 증거 |
| Contract | Spec이 소유하는 등록된 실행 가능 인터페이스 |

## Usage

### Audience

현재 Spec Package와 Task를 찾는 작성자·검토자·운영자를 대상으로 합니다.

### Authoring Flow

1. 관련 Requirement, Architecture Description, ADR을 먼저 읽습니다.
2. 등록된 Spec template으로 `spec.md`를 만들거나 고칩니다.
3. 승인된 변경에만 Plan과 번호가 붙은 Task를 추가합니다.
4. 실제 작업은 현재 Task에만 기록합니다.
5. acceptance 대응과 승격 기록은 현재 Task에 남기고 Stage 01·02·05의 오래
   유지할 갱신을 연결하거나 갱신이 필요 없는 이유를 적습니다.
6. metadata, lifecycle, 링크, 구현 정합성, 등록된 gate profile을 검증합니다.
7. 승격과 acceptance 검증으로 package가 removal review 준비 상태가 되고 삭제가
   승인되면, 현재 문서가 여전히 기대는 의미를 01·02 owner에 요약한 뒤 package를
   삭제하고 Spec 번호를
   `reserved_history`에 추가합니다. clarify, analyze, 구현, 검증 순서는
   [SDLC](../../.agents/governance/sdlc.md)를 따릅니다.

### Package 수명주기

- 현재 Requirement와 Architecture가 변경 범위를 이미 다루면 그대로
  재사용합니다.
- Spec·Plan·Task의 정확한 상태와 전이는 Registry가 소유합니다.
- 완료 전에 acceptance와 실제 검증 결과를 연결하고 오래 유지할 의미를 현재
  Stage 01·02·05 owner로 승격합니다. 승격 근거는 현재 Task의
  `Evidence` 한 곳에 기록합니다.
- Spec·Plan 상태는 승인 권한만 기록합니다. 실행 상태는 Task가, 수용 판정은
  Task의 `Criterion Acceptance` 표가 소유합니다.
- removal review 준비가 되고 삭제가 승인된 package는 삭제합니다. 준비 상태는
  모든 criterion이 accepted 또는 `not-required`인 상태이며, typed Criterion
  Acceptance 표가 없는 이전 형식은 모든 criterion이 PASS·accepted이고 해결되지
  않은 required non-PASS가 없으면 준비로 봅니다. 완료 package를 지우라는 사용자
  지시가 그 묶음의 승인이며, 삭제하는 Task가 승인과 package별 criterion 상태를
  기록합니다. Spec 번호는
  Registry `reserved_history`에 추가하고, 현재 문서의 링크는 일반 텍스트로
  바꾸며, 본문은 Git history가 기록합니다. 하나라도 terminal이 아닌 Task가
  있으면 package와 그 완료된 Task는 남깁니다. Stage 98로 옮기지 않습니다.
- terminal Task 본문은 package가 남아 있는 동안 고치지 않습니다. 그 본문이
  나중에 삭제된 package를 가리키는 링크는 고치지 않으며, 링크 검사는 번호가
  예약된 package를 향한 그런 링크만 허용합니다.
- lifecycle generation migration proof는 마지막 generation 6 revision에서 읽으므로,
  proof를 지녔던 package도 같은 조건으로 삭제합니다.
  철회와 완료의 처분 기록은
  [문서 보존 정책](../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)을
  따릅니다.

## Related Documents

- [에이전트 작업 규칙](AGENTS.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Operations](../05.operations/README.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Document Registry](../99.templates/registry.json)
