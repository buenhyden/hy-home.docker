---
title: "`SENSITIVE_ENV_VARS.md.example` vs `SENSITIVE_ENV_VARS.md` Comparison"
version: "2.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0010"
parent_ids: []
created: "2026-06-04"
---

# Secret Registry Metadata Comparison

## Usage

`secrets/SENSITIVE_ENV_VARS.md.example`은 공개 ID·env key·파일 경로·용도 계약을
소유한다. 실제 값은 Git에서 제외된 로컬 registry와 secret 파일에 보관한다.
공개 예제에는 placeholder만 허용한다. ID는 안정적으로 유지하며 다른 credential
의미로 재사용하지 않는다.

문서의 줄 수나 전체 ID 수만 같다는 이유로 메타데이터 일치를 판단하지 않는다.
중복 ID, 중복 env mapping, 중복 경로, 경로 이탈, 현재 Compose 선언과 service
grant의 대응 관계를 함께 확인한다. 실제 점검 수치와 결과는 날짜·commit을 붙여
현재 Task에 기록한다.

## Common Checks

저장소 루트에서 값이 출력되지 않는 기존 검사 경로를 사용한다.

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --dry-run
```

승인된 메타데이터 동기화는 `--sync-metadata`로 수행하고 동일 검사로 drift가
사라졌는지 확인한다. 기존 값·생성일·미등록 로컬 행은 보존되며 secret 값 파일은
이 경로에서 읽거나 쓰지 않는다. 오류나 경로 교체가 감지되면 중단하고 원인을
조사한다. 동기화 성공은 서비스 인증이나 credential 회전 성공을 의미하지 않는다.

공개 registry의 파일 경로가 모두 root Compose grant인 것은 아니다. 초기화용,
파생값 또는 보존된 비활성 metadata 항목은 명시적으로 구분한다. 현재 service
소비자가 없는 선언을 제거하더라도 개인 파일과 ID를 임의 삭제하지 않는다.

로컬 registry가 없으면 관찰되지 않음으로 기록한다. 존재하는 경우 Git ignore와
0600 권한을 확인하고 값, 원문 행, 인증 파일이나 token 내용을 증거에 남기지 않는다.
`--check`는 생성 도구의 설치 여부까지 검사하며 `htpasswd` 누락 등은 별도로 보고한다.

## Runbook Handoff

[Secret 관리 안내](../../../../../secrets/README.md)와 해당 서비스 Runbook을 따른다.
실제 credential 변경, 재시작 또는 데이터 복구는 대상과 영향을 명시한 별도 승인
범위에서 수행한다. 줄 수를 맞추기 위해 로컬 값을 덮어쓰거나 삭제하지 않는다.

## Traceability

- Subject peers: none — `00-workspace/0010-sensitive-env-vars-comparison` holds this document alone.

## Related Documents

- [Env Key Comparison](../0003-env-key-comparison/guide.md)
- [Public secret metadata](../../../../../secrets/SENSITIVE_ENV_VARS.md.example)
- [Metadata synchronization owner](../../../../../scripts/operations/gen-secrets.sh)
- [Secret management](../../../../../secrets/README.md)
