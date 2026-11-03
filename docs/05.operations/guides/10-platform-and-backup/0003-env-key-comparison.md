---
title: "`.env.example` vs `.env` Key Comparison"
version: "3.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "operations"
artifact_id: "GDE-0003"
created: "2026-06-04"
---

# `.env.example` vs `.env` Key Comparison

## Overview

이 가이드는 공개 `.env.example`과 로컬 `.env`의 키 집합을 비교하는 기준과 방법을 설명한다.

## Scope

### Audience and Goal

대상 독자는 환경변수를 추가·폐기하거나 키 정합성을 점검하는 운영자와 agent다.

목표는 두 파일의 값 이외 구조를 비교하고, 모든 공개 키에 실제 소비자가 있음을 확인하는 것이다.

## Concepts

공개 `.env.example`은 현재 환경변수 계약을 소유하고, 로컬 `.env`는 운영자 값을
보존한다. 키 추가·폐기 시 Compose, Dockerfile, 스크립트의 직접·간접 소비자를
확인한다. 전체 구조 검사는 값 영역만 제외하고 키·순서·구분·주석을 대조한다.
공개 키의 실제 소비자는 실행 중인 컨테이너뿐 아니라 지원되는 profile과 운영
스크립트까지 검토하며, 구조 일치 결과만으로 소비를 수용하지 않는다. 기존
`--sync-metadata-prune-check`의 키 집합 검사는 이 전체 구조 검사와 별도다.

키 수와 실제 비교 결과는 날짜·commit과 함께 현재 Task에 기록한다. 이 가이드는
과거 감사 숫자를 현재 상태로 유지하지 않는다. 값, 원문 환경, 확장된 private
Compose 모델은 증거에 포함하지 않는다.

## Usage

### Runbook Handoff

값 생성·회전·런타임 재시작은 이 키 비교의 범위가 아니다. [Secret 관리 안내](../../../../secrets/README.md)와 해당 서비스 Runbook에서 대상, 승인, 백업 및 복구 절차를 확인한다.

### Traceability

- 같은 번호 `0003`의 Policy/Runbook은 없다.

## Troubleshooting

### Common Checks

저장소 루트에서 기존 메타데이터 도구를 사용한다.

```bash
bash scripts/operations/gen-secrets.sh --dry-run
# private metadata 읽기가 승인된 경우에만 다음 비교를 실행한다.
bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check
```

합성 누출 시험과 독립 보안 검토가 통과한 뒤, private 읽기 범위가 허용된 현재
작업에서 값 제외 전체 구조만 확인한다. 이 명령은 값을 process 안에서 읽지만
파일을 바꾸지 않으며, 값·값 해시·길이·원문을 출력하거나 저장하지 않는다.
일반 CI는 실제 private 파일을 읽지 않고 합성 입력으로만 검사한다.

```bash
python3 scripts/operations/secret-structure.py --root "$PWD" check --read-private
```

고정 결과 `MATCH`는 exit 0, `DRIFT`는 exit 1, 누락·권한·링크·형식·동시 변경
등의 `BLOCKED`는 exit 2다. `DRIFT`의 첫 위치는 공개 예제 기준 행과 고정 사유만
나타내며 private 행 번호나 정확한 원인을 뜻하지 않는다. 차이 원문을 출력하지
않으므로 운영자가 보호된 경로에서 원인을 확인한다. 사설 파일이 없거나 읽을 수 없으면 공개 예제를
대체 입력으로 사용하지 않는다.

`--dry-run`은 공개 schema와 파일 존재 메타데이터를 사용한다. 반면 metadata
check는 private registry와 `.env` 값을 프로세스 내부에서 읽고 출력하지 않는
검사이므로 해당 접근 승인이 필요하다. 종료 코드 `0`은 drift 없음, `1`은 drift,
`2`는 unsafe/ambiguous 입력이다. 쓰기 없음과 개인 값 읽기 없음은 다르다.

두 번째 명령은 유지할 값을 출력하지 않고 공개/개인 키 집합의 정확한 일치를 검사한다.
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

## Related Documents

- [Public environment schema](../../../../.env.example)
- [Metadata synchronization owner](../../../../scripts/operations/gen-secrets.sh)
- [Secrets Key Comparison](../04-security-and-secrets/0010-sensitive-env-vars-comparison.md)
- [Secret management](../../../../secrets/README.md)
