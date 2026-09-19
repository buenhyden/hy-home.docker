---
title: "`.env.example` vs `.env` Key Comparison"
version: "3.0.0"
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
확인한다. 운영 기준은 두 파일의 키 집합이 정확히 같고, 모든 키에 실제
소비자가 있는 상태다. 실행 중인 컨테이너뿐 아니라 지원되는 profile과 운영
스크립트의 소비자도 포함한다. 값과 키 순서는 같을 필요가 없다.

키 수와 실제 비교 결과는 날짜·commit과 함께 현재 Task에 기록한다. 이 가이드는
과거 감사 숫자를 현재 상태로 유지하지 않는다. 값, 원문 환경, 확장된 private
Compose 모델은 증거에 포함하지 않는다.

## Common Checks

저장소 루트에서 기존 메타데이터 도구를 사용한다.

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check
bash scripts/operations/gen-secrets.sh --dry-run
```

첫 명령은 유지할 값을 출력하지 않고 공개/개인 키 집합의 정확한 일치를 검사한다.
`--dry-run`은 생성 계획이며 런타임 인증 성공이나 credential 회전의 증거가 아니다.
`--check`는 생성 도구 의존성도 확인하므로 `htpasswd` 등 도구가 없으면 실패한다.

공개 키 중복, 사용되지 않는 키, secret registry의 env mapping 및 파일 경로를
함께 검토한다. 경로를 조합하는 키나 ID 기반 htpasswd username처럼 간접 소비하는
키는 단순 문자열 검색 결과만으로 삭제하지 않는다. 로컬 파일이 없으면 상태를
관찰되지 않음으로 남기고 기존 값이 있다고 가정하지 않는다.

소비자를 먼저 조사해 공개 스키마를 정리한 뒤, 승인된 `--sync-metadata-prune`로
공개 스키마에 없는 개인 키를 제거한다. 실행 전 0700 디렉터리에 0600 백업을
보관한다. 유지하는 assignment와 값은 그대로 보존하며 비밀 파일은 삭제하지
않는다. 실행 후 `--sync-metadata-prune-check`, 키 집합, 값 보존 여부, Git ignore와
0600 권한을 확인한다. 기존 `--sync-metadata`는 미등록 항목 보존 모드이므로
이 엄격한 정리의 완료 검사로 사용하지 않는다.

## Runbook Handoff

값 생성·회전·런타임 재시작은 이 키 비교의 범위가 아니다. [Secret 관리 안내](../../../../../secrets/README.md)와 해당 서비스 Runbook에서 대상, 승인, 백업 및 복구 절차를 확인한다.

## Traceability

- Subject peers: none — `00-workspace/0003-env-key-comparison` holds this document alone.

## Related Documents

- [Public environment schema](../../../../../.env.example)
- [Metadata synchronization owner](../../../../../scripts/operations/gen-secrets.sh)
- [Secrets Key Comparison](../0010-sensitive-env-vars-comparison/guide.md)
- [Secret management](../../../../../secrets/README.md)
