---
title: 문서 Lifecycle 거버넌스 아키텍처
version: 1.0.0
type: sdlc/architecture-description
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: AD-0030
parent_ids:
  - REQ-0026
created: 2026-09-01
updated: 2026-09-01
---

# 문서 Lifecycle 거버넌스 아키텍처

## Context and Stakeholders

Stage 00은 거버넌스 문서가 언제 유지되고 언제 은퇴하는지를 규정합니다. 이
description은 그 규정을 관측하고 강제하는 구조를 기록합니다. 즉 어떤 구성
요소가 어떤 authority를 어떤 순서로 읽고, 각 구성 요소가 무엇을 판단할 수
있는지를 기록합니다. 소비자는 거버넌스 문서를 변경하는 관리자와 완료 전에 그
변경을 검증하는 agent입니다.

## System Boundaries

경계 안: profile, lifecycle, identity space를 정의하는 Stage 99 registry,
은퇴를 기록하는 Stage 98 archive, 문서를 담는 현재 stage tree, 그리고
`scripts/lib/document_governance/` library와 등록된 validator들.

경계 밖: 은퇴한 내용을 보관하는 Git object storage — 추적되는 복제본이 아니라
recovery commit으로 도달합니다. 그리고 비교 base를 선택하지만 보존 결과를
판단하지는 않는 CI orchestration.

## Components

- `scripts/lib/document_governance/registry.py`는 Stage 99의 profile,
  lifecycle, identity space를 적재합니다. 합법적인 status 값과 식별자 관계에
  대한 유일한 기계 authority입니다.
- `scripts/lib/document_governance/spec_packages.py`는 현재 tree와 비교 base의
  bounded Git snapshot에서 Stage 03 package를 적재하고 제거의 합법성을
  판단합니다.
- `scripts/lib/document_governance/archive.py`는 Stage 98을 적재하고, 은퇴가
  기록되었음을 증명하는 Tombstone record를 노출합니다.
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

`validate_spec_package_lifecycle`은 `_recorded_retirements`가 Stage 98
Tombstone에서 읽은 retired-path 집합을 받습니다. 대응하는 Tombstone이 없는
package 전체 제거는 `package-retirement-unrecorded`를 산출합니다. archive
record는 어떤 문서가 존재하는지를 판단하지 않으며, 오직 제거가 기록되었는지만
판단합니다.

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
- 분리 가능: 보존 규칙은 Spec Package 없이 Stage 00에서 읽을 수 있고, 강제
  방식은 Task 없이 이 description에서 읽을 수 있습니다.

## Risks

- 두 번째 강제 경로가 실행되지 않습니다. `validate_body_contract`의
  `changed_boundary` 분기는 template role의 heading 계약과 변경 target의 잔여
  literal/token 검사를 담당하지만, production 호출부인
  `scripts/lib/document_governance/metadata/reference.py`의 두 지점이 모두
  `False`를 전달합니다. Registry section 계약이 이제 모든 profile에 직접
  강제되므로 heading 검사는 중복이지만, `template-instruction-in-target`과
  `template-body-token-in-target`은 다른 어떤 check도 대신하지 않습니다.
- 잔여 marker 계약이 세 곳에서 서로 다릅니다. `TARGET_TEMPLATE_LITERALS`는
  `<!-- Target:`을 변경 target에 남아서는 안 되는 잔여물로 선언하고, 현재 어떤
  template도 이를 생성하지 않으며, `docs/99.templates` 아래 template source는
  이를 담지 않도록 test로 강제됩니다. 그런데 추적 중인 문서 184개가 이를
  담고 있고 `scripts/validation/check-document-metadata.py`는 자신의 생성
  출력에 계속 기록합니다. 증거가 양방향을 가리키므로 marker를 제거할지
  계약에서 내릴지는 아직 결정되지 않았습니다.
- 9개 도메인이 살아 있는 Stage 02 Description을 둘씩 가집니다. base
  description과 `*-optimization-hardening` description이 관계 선언 없이
  공존하며 어느 쪽도 다른 쪽의 상위 집합이 아닙니다. REQ-0026-FR-0005는
  capability마다 Stage 02 owner 하나를 요구하므로 이는 알려진 위반입니다.
  hardening 서술의 조항 다수가 다른 문서에 없어 단순 은퇴로는 해소되지
  않으며, 두 서술의 병합 또는 명시적 계층 선언이 필요합니다.

## Traceability

- [REQ-0026 문서 보존 및 은퇴](../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0031 보존 기록으로서의 아카이브](../decisions/0031-preserved-archive-record.md)
- [문서 보존 및 은퇴 정책](../../00.agent-governance/policies/documentation-protocol.md)

## Related Documents

- [ADR-0029 Workspace governance authority](../decisions/0029-workspace-governance-authority.md)
