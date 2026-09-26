---
title: "`SENSITIVE_ENV_VARS.md.example` vs `SENSITIVE_ENV_VARS.md` Comparison"
version: "3.2.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
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
bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check
bash scripts/operations/gen-secrets.sh --dry-run
```

두 registry의 ID와 env-key 집합은 정확히 같아야 하며 공개 행마다 실제 소비자,
초기화 입력 또는 파생값 생성 경로가 있어야 한다. 비활성 서비스도 지원되는
profile에서 소비하면 유지하지만, 예정·폐기·미사용 항목은 공개/개인 목록에서
함께 제거한다. 제거한 ID는 Git 이력에 남기고 다른 의미로 재사용하지 않는다.

소비자 검토와 보호된 0600 백업 후, 승인된 `--sync-metadata-prune`로 정리하고
같은 check 모드로 drift가 없는지 확인한다. 개인 registry는 공개 registry와
내용·행 순서·날짜·주변 문장까지 같고 Value cell만 다르다(owner 결정 2026-09-24).
동기화는 공개 파일을 기준으로 개인 파일을 다시 만들고 Value cell만 옮긴다. 값
생성도 Value cell만 바꾸며 날짜를 고치지 않는다. 행마다 `secrets/` 아래 경로의
파일이 있고 비어 있지 않아야 한다. 여러 줄 값(SEC-003의 unseal share)은 표 행을
쪼개므로 파일에만 두고 registry Value cell은 placeholder로 남긴다. 이 경로는 개별 secret 값 파일을 생성·회전·삭제하지 않는다. 공개
스키마 밖의 행을 `Private-only rows` 섹션에 남기는 기존 `--sync-metadata`는 이번 정확한 집합 일치의
완료 검사와 다르다. 중복·모호한 입력·경로 교체는 값을 출력하지 않고 거부한다.

로컬 registry가 없으면 관찰되지 않음으로 기록한다. 존재하는 경우 Git ignore와
0600 권한을 확인하고 값, 원문 행, 인증 파일이나 token 내용을 증거에 남기지 않는다.
`--check`는 생성 도구의 설치 여부까지 검사하며 `htpasswd` 누락 등은 별도로 보고한다.

## Runbook Handoff

[Secret 관리 안내](../../../secrets/README.md)와 해당 서비스 Runbook을 따른다.
실제 credential 변경, 재시작 또는 데이터 복구는 대상과 영향을 명시한 별도 승인
범위에서 수행한다. 단순 줄 수가 아니라 소비자 근거와 정확한 키 집합으로
정리하며, 유지 대상의 개인 값을 덮어쓰지 않는다.

## Traceability

- Subject peers: none — no Policy or Runbook shares number `0010`.

## Related Documents

- [Env Key Comparison](0003-env-key-comparison.md)
- [Public secret metadata](../../../secrets/SENSITIVE_ENV_VARS.md.example)
- [Metadata synchronization owner](../../../scripts/operations/gen-secrets.sh)
- [Secret management](../../../secrets/README.md)
