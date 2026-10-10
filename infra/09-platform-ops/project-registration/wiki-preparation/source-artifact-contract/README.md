---
title: "원천·artifact·provenance와 권한 철회"
version: "0.1.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 원천·artifact·provenance와 권한 철회

## Overview

Git은 코드·문서 원천이고 blog-data는 사람이 검토한 Literature/Permanent/Maps·초안·출판물의 원본입니다. 준비 패키지는 두 번째 지식 원본을 만들지 않습니다. artifact는 revision·path·hash·retrieved/effective 시각·권리 근거·ACL·parser/chunker/embedding version·generation·idempotency와 provenance를 연결합니다. 합성 bytes의 hash 일치만 검사하며 원천 진위나 라이선스 검증으로 표현하지 않습니다.

삭제 또는 권한 철회는 ordered outbox event로 기록합니다. search·point query·citation·download·cache·이전 generation 접근 모두 즉시 거부한 뒤 물리 정리를 수행해야 합니다. offline fixture는 이 계약 필드와 순서만 검증합니다. 복원 시 삭제 watermark보다 이전의 접근 권한과 내용이 다시 공개되지 않도록 event replay·ACL 재평가·cache 무효화·object 및 vector 정리를 선행합니다. 합성 문서는 access_state·tombstone·evaluated_sequence와 각 surface_watermark를 대조하여 삭제 우선순위와 이전 generation의 미적용 event를 거절합니다. 이는 실제 접근 차단 결과가 아닌 선언된 상태 정합 검사입니다. old generation의 immutable artifact 보관은 열람 권한 복원을 뜻하지 않습니다.

caller policy는 source repository/ref/revision/path allowlist와 typed `versions` allowlist를 제공합니다. `versions`는 최대 128개의 정확한 `{parser, chunker, embedding}` mapping이며, 각 값은 비어 있지 않고 `*` 문자를 포함할 수 없으며 중복 mapping은 허용하지 않습니다. 값은 exact 문자열로만 비교합니다. helper는 artifact 문서와 합성 bytes가 그 범위·선언 hash에 맞고 document `versions`가 그 allowlist의 한 mapping과 정확히 같은지만 검사합니다. Source admission scope는 `H(project_id, contract, repository, ref, path)`이며 raw source idempotency key는 현재 content SHA로 보존하지만 revision, content hash, timestamp와 processing version은 admission digest에 넣지 않습니다. 다음 source 호출은 `{generation, evaluated_sequence}`, per-surface watermark와 prior source `artifact`를 포함한 parsed `prior_states`, complete `prior_receipts`를 제공해야 합니다. state artifact는 `{source_revision, content_sha256, versions}`입니다. 이 artifact는 같은 generation에서 바뀔 수 없고, 갱신된 caller policy 아래 더 높은 generation에서만 바뀔 수 있습니다. revision/history/allowed→revoked/deleted와 terminal frontier는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 유일하게 소유합니다. repository/ref의 이름만으로 immutable revision을 추정하지 않으며, approved revision은 caller가 명시해야 합니다. artifact authenticity, license, source global repository/ref mapping, caller completeness, 실제 store update와 runtime은 NOT_RUN입니다.

helper 결과의 scoped idempotency와 원본 source hash의 관계는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 소유합니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[schema](../schemas/source-artifact.schema.json)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.
