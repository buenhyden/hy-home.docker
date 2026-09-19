---
title: "`.env.example` vs `.env` Key Comparison"
version: "2.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0003"
parent_ids: []
created: "2026-06-04"
---

# `.env.example` vs `.env` Key Comparison

## Usage

공개 `.env.example`은 현재 환경변수 계약을 소유하고, 로컬 `.env`는 운영자 값을
보존한다. 키 추가·폐기 시 Compose, Dockerfile, 스크립트의 직접·간접 소비자를
확인한다. 공개 예제에서 폐기한 키를 로컬 파일에서 자동 삭제하지 않는다.
순서나 로컬 전용 키가 남아 있다는 사실만으로 drift라고 판단하지 않는다.

키 수와 실제 비교 결과는 날짜·commit과 함께 현재 Task에 기록한다. 이 가이드는
과거 감사 숫자를 현재 상태로 유지하지 않는다. 값, 원문 환경, 확장된 private
Compose 모델은 증거에 포함하지 않는다.

## Common Checks

저장소 루트에서 기존 메타데이터 도구를 사용한다.

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-check
bash scripts/operations/gen-secrets.sh --dry-run
```

첫 명령은 값과 미등록 로컬 항목을 보존하는 메타데이터 계약을 확인한다.
`--dry-run`은 생성 계획이며 런타임 인증 성공이나 credential 회전의 증거가 아니다.
`--check`는 생성 도구 의존성도 확인하므로 `htpasswd` 등 도구가 없으면 실패한다.

공개 키 중복, 사용되지 않는 키, secret registry의 env mapping 및 파일 경로를
함께 검토한다. 경로를 조합하는 키나 ID 기반 htpasswd username처럼 간접 소비하는
키는 단순 문자열 검색 결과만으로 삭제하지 않는다. 로컬 파일이 없으면 상태를
관찰되지 않음으로 남기고 기존 값이 있다고 가정하지 않는다.

승인된 `--sync-metadata`는 공개 스키마와 메타데이터를 정렬하면서 기존 값과
미등록 항목을 보존한다. 실행 후 `--sync-metadata-check`, Git ignore 여부와 0600
권한을 확인한다. 서비스 추가·제거 또는 공개 스키마 변경 시 다시 점검한다.

## Runbook Handoff

값 생성·회전·런타임 재시작은 이 키 비교의 범위가 아니다. [Secret 관리 안내](../../../../../secrets/README.md)와 해당 서비스 Runbook에서 대상, 승인, 백업 및 복구 절차를 확인한다.

## Traceability

- Subject peers: none — `00-workspace/0003-env-key-comparison` holds this document alone.

## Related Documents

- [Public environment schema](../../../../../.env.example)
- [Metadata synchronization owner](../../../../../scripts/operations/gen-secrets.sh)
- [Secrets Key Comparison](../0010-sensitive-env-vars-comparison/guide.md)
- [Secret management](../../../../../secrets/README.md)
