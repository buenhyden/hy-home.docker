---
title: "문서 Lifecycle 거버넌스 아키텍처"
version: "1.3.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "architecture"
artifact_id: "AD-0030"
parent_ids:
- "REQ-0026"
created: "2026-09-01"
---

# 문서 Lifecycle 거버넌스 아키텍처

## Context and Stakeholders

`.agents/`는 거버넌스 문서가 언제 유지되고 언제 은퇴하는지를 규정합니다. 이
description은 그 규정을 관측하고 강제하는 구조를 기록합니다. 즉 어떤 구성
요소가 어떤 authority를 어떤 순서로 읽고, 각 구성 요소가 무엇을 판단할 수
있는지를 기록합니다. 소비자는 거버넌스 문서를 변경하는 관리자와 완료 전에 그
변경을 검증하는 agent입니다.

## System Boundaries

경계 안: profile, lifecycle, identity space를 정의하는 Stage 99 registry,
처분 기록과 frozen body를 분리해 보존하는 Stage 98 archive, 문서를 담는 현재
stage tree, 그리고 `scripts/lib/document_governance/` library와 등록된 validator들.

경계 밖: preserved body의 원본 동일성과 복구 경로를 제공하는 Git object
storage, 그리고 비교 base를 선택하지만 보존 결과를 판단하지는 않는 CI
orchestration.

## Components

- `scripts/lib/document_governance/registry.py`는 Stage 99의 profile,
  lifecycle, identity space를 적재합니다. 합법적인 status 값과 식별자 관계에
  대한 유일한 기계 authority입니다.
- `scripts/lib/document_governance/spec_packages.py`는 현재 tree와 비교 base의
  bounded Git snapshot에서 Stage 03 package를 적재하고 제거의 합법성을
  판단합니다.
- `scripts/lib/document_governance/archive.py`는 Stage 98을 적재하고, Tombstone
  disposition과 `completed/`, `superseded/`, `retired/` frozen path를 분리해
  노출하며 recovery blob과 원래 경로의 일치를 검증합니다.
- `scripts/lib/document_governance/references.py`는 현재 tree에서 Stage 90
  package 집합을 도출하고, 보호 대상 package 자신이 담고 있는 보존 선언을
  강제합니다.
- `scripts/validation/check-document-metadata.py`와
  `scripts/validation/check-document-links.py`는 이 판정을 gate profile로
  노출하는 등록된 entrypoint입니다.
- `docs/98.archive/`는 두 종류를 담습니다. `migrations/`와 `tombstones/`는
  결정의 기록이고, `completed/`, `superseded/`, `retired/`는 보존된 본문입니다.
  `docs/98.archive/tombstones/<stage>/`는 철회 기록의 저장 구조입니다.
  namespace는 은퇴한 문서의 stage를 그대로 반영하므로, 어떤 stage에서 은퇴가
  일어났는지는 디렉터리 목록만으로 읽힙니다. namespace의 부재는 "그 stage는
  은퇴할 수 없다"가 아니라 "아직 은퇴한 적이 없다"를 뜻합니다.
- `scripts/lib/document_governance/metadata/heading.py`는 profile이 선언한
  section 계약을 본문에 강제합니다. 선언과 강제가 갈라지면 corpus는 선언을
  참조하지 않고 자기들끼리 수렴하므로, 이 component가 두 값을 하나로
  유지합니다.

## Data Flow

변경은 한 방향으로 검증됩니다. registry를 먼저 읽어 profile과 lifecycle 값을
고정한 뒤에야 문서를 판단합니다. 그다음 현재 tree를 열거하고, 비교 base를
bounded snapshot으로 Git에서 적재합니다. base에 존재하고 현재 tree에 없는
문서는 두 갈래로 분류됩니다. 유지된 package에서 빠진 member는 그 member의 base
status로 판단하고, 통째로 사라진 package는 Stage 98을 근거로 판단합니다.

`validate_spec_package_lifecycle`은 Stage 98에서 분리해 읽은 Tombstone
retired-path와 frozen preserved-path 집합을 받습니다. completed Spec 경로가
preserved-path에 있으면 completion으로 판정하고, 그렇지 않은 package 이탈은
retirement로 판정합니다. 대응하는 Tombstone이 없는 retirement는
`package-retirement-unrecorded`를 산출합니다. Tombstone은 철회를, completed
Spec은 영구 outcome을, 함께 보존된 Plan과 Task 본문은 그 outcome에 이른 실행
맥락을 각각 증명하며 어느 한 기록이 다른 기록을 대신하지 않습니다.

완료 순서는 outcome과 current consumer를 먼저 Spec 또는 다른 현재 정본으로
write back한 뒤, Spec·Plan·모든 Task의 terminal 전환과 archive 이동을 한 결과
tree에 적용하는 것입니다. 이 순서 때문에 active Stage 03에는 terminal 중간
상태가 생기지 않습니다.

link validator와 metadata validator는 결과 tree 위에서 독립적으로 실행됩니다.
따라서 은퇴한 경로를 여전히 가리키는 잔존 문서는 lifecycle 술어를 거치지 않고
자기 자신의 기준으로 실패합니다.

## Deployment View

이 library는 `scripts/manifest.yaml`에 등록된 validator가 import하고,
`scripts/validation/run-ci-gate.py`가 `changed`와 `full` profile로 실행합니다.
로컬에서 비교 base는 `HEAD`가 기본값이고, CI에서는 workflow contract가 공급하는
신뢰된 base입니다. 검증 중에 Stage 98이나 stage tree에 쓰는 구성 요소는
없습니다.

## Quality Attributes

- Fail-closed: Stage 98을 읽을 수 없으면 retired-path 집합이 비어 모든 제거가
  기록되지 않은 것으로 판단됩니다. 조용히 허용되지 않습니다.
- 도출되며 고정되지 않음: 멤버십, 허용 파일, 은퇴 합법성은 현재 tree, registry,
  Stage 98에서 나옵니다. 고정 count, digest, expected commit chain은 판정에
  참여하지 않습니다.
- Bounded: base snapshot, 파일 읽기, Git 출력은 byte와 entry 단위로 제한되어
  큰 history가 validator를 고갈시키지 않습니다.
- 분리 가능: 보존 규칙은 Spec Package 없이 `.agents/`에서 읽을 수 있고, 강제
  방식은 Task 없이 이 description에서 읽을 수 있습니다.

## Risks

- 변경 문서의 잔여 template 지침과 token은 `check-changed`의
  `_introduced_body_findings`가 현재 본문과 base 본문을 각각
  `changed_boundary=True`로 비교하여 새로 도입된 위반을 거부합니다.
  `reference.py`의 template source 검사에 있는 두 `False` 호출만으로 이
  production 경로가 비활성이라고 판단할 수 없습니다. 기존 위반은 변경분
  검증과 구분되며, current/base 비교가 기존 marker의 일괄 정비를 증명하지는
  않습니다.
- `TARGET_TEMPLATE_LITERALS`가 선언한 `<!-- Target:` 잔여물 규칙을
  유지합니다. 현재 template source와 metadata report는 이 주석을 생성하지
  않습니다. 활성 운영 문서에 남은 자기 경로 주석은 본문·절차·식별자를
  보존하며 제거했습니다. 정비 결과는 SPEC-0173-TSK-0006의 현재 실행 증거로
  추적하며, 관측한 문서 수를 영구 계약으로 고정하지 않습니다.
- 9개 도메인이 살아 있는 Stage 02 Description을 둘씩 가집니다. base
  description과 `*-optimization-hardening` description이 관계 선언 없이
  공존하며 어느 쪽도 다른 쪽의 상위 집합이 아닙니다. REQ-0026-FR-0005는
  capability마다 Stage 02 owner 하나를 요구하므로 이는 알려진 위반입니다.
  hardening 서술의 조항 다수가 다른 문서에 없어 단순 은퇴로는 해소되지
  않으며, 두 서술의 병합 또는 명시적 계층 선언이 필요합니다.

## Traceability

- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0033 Spec Package 전체 본문 보존](../decisions/0033-full-spec-package-preservation.md)
- [ADR-0031 보존 기록으로서의 아카이브](../../98.archive/superseded/02.architecture/decisions/0031-preserved-archive-record.md) (superseded)
- [문서 보존 및 은퇴 정책](../../../.agents/governance/documentation-protocol.md)

## Related Documents

- [ADR-0032 Canonical agent governance home](../decisions/0032-canonical-agent-governance-home.md)
