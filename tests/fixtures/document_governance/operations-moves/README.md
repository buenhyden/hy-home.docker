---
title: "Operations move synthetic fixtures"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# 운영 문서 경로 매핑 합성 입력

## Overview

P08 준비 단계에서 정확한 source 경로·artifact ID·target 경로의 결합과 거부 조건을
검증합니다. 실제 문서 전수 분류나 이동 결과의 증거가 아닙니다.

## Audience

P08 문서 계약 구현자와 코드·보안 검토 담당자입니다.

## Scope

허용된 LAB 문서 목적지는 `docs/05.operations/guides/labs/`,
`docs/05.operations/policies/labs/`, `docs/05.operations/runbooks/labs/`입니다.
저장소 루트 `labs/`와 LAB 런타임·비밀값·데이터는 시험의 이동 대상에서 제외합니다.
학습 앱·Wiki 앱 구현·서비스 실행은 포함하지 않습니다.

## Structure

- `reviewed-map.json`: 합성 Guide·Runbook의 같은 번호와 서로 다른 LAB 결정을
  담습니다. 이미 정리된 Policy와 미분류 Guide를 포함합니다.
- 경계 거부 입력은 전용 단위시험이 소유합니다. 합성 번호는 실문서 판정 규칙이 아닙니다.

## Tech Stack

기존 frontmatter·taxonomy API와 Python unittest를 재사용합니다.

## Configuration

호출자가 현재 Registry profile과 허용 domain을 제공합니다. nested target은
제안 경로이며 현행 Registry 수용과 구분합니다. helper는 파일·프로세스·승인
시스템에 접근하지 않습니다.

## Validation

```sh
python3 -m unittest tests.lib.document_governance.test_operations_moves -v
```

## Usage

[순수 helper](../../../../scripts/lib/document_governance/operations_moves.py)에 이미
읽은 공개 문서와 검토된 정확한 path/ID 결정을 전달합니다. 미분류·기존 domain
충돌은 `REVIEW_REQUIRED`이며 숫자로 domain을 추정하지 않습니다. 반환되는 README
folder tuple은 필요한 작성 위치이며 실제 README 생성·metadata 수용을 의미하지 않습니다.

## Related Documents

- [합성 입력 family](../README.md)
- [운영 문서](../../../../docs/05.operations/README.md)
- [문서 진입점](../../../../docs/README.md): owning Task는 `SPEC-0204-TSK-0015`입니다.
