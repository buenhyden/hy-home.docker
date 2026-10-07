---
title: "Test Surface"
version: "1.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
created: "2026-02-21"
---

# tests

> 저장소 전역 검증과 테스트 자산의 진입점

## Overview

`tests/`는 저장소 전역 테스트와 검증 자산을 두는 공간입니다. 주요 품질
게이트는 `scripts/`와 GitHub Actions에 정의되어 있으며, 이 트리는
`scripts/lib/<domain>/`의 library-unit 소유권과 validation/entrypoint 소유권을
서로 분리합니다.

## Audience

이 README의 주요 독자:

- Developers
- QA Engineers
- Operators
- AI Agents

## Scope

### In Scope

- 저장소 전역 테스트 정책과 테스트 자산 위치 안내
- 여러 서비스나 문서 계약을 함께 검증하는 테스트 진입점
- CI에서 실행되는 검증 스크립트와의 연결

### Out of Scope

- 개별 서비스의 Docker Compose 원문
- `scripts/`가 소유하는 검증 스크립트 구현
- secret 값, credential, token, 인증서 원문
- 하위 프로젝트의 package-local 테스트 설정

## Structure

```text
tests/
├── README.md  # This file
├── lib/<domain>/      # scripts/lib/<domain>/ library-unit 테스트
├── validation/        # validation/entrypoint 및 실행-context 테스트
└── requirements-integration.txt  # opt-in 통합 테스트 전용 의존성 (수동 갱신)
```

고정 입력 디렉터리는 없습니다. 현재 픽스처는 `_fixtures.py` 형태의 builder
모듈이며, 테스트가 필요한 최소 입력만 만들어 씁니다. 독립 consumer가 읽어야
하거나 형식 재현이 복잡해 builder로 감당되지 않는 입력이 생길 때만
`tests/fixtures/`를 만듭니다.

## Usage

1. 새 테스트 자산을 만들기 전에 같은 검증이 이미 `scripts/` 또는 하위 프로젝트 package script에 있는지 확인합니다.
2. repository contract, doc traceability, Compose validation처럼 전역 검증에 가까운 항목은 [`../scripts/README.md`](../scripts/README.md)에 있는 기존 진입점을 우선 사용합니다.
3. `scripts/lib/<domain>/`의 주 책임을 검증하는 테스트는 같은 이름의
   `tests/lib/<domain>/`에 두고, CLI·entrypoint·실행 context 검증은
   `tests/validation/`에 둡니다.
4. 새 unit·implementation fixture 테스트 파일은 workflow contract의 해당 LOCAL suite에 등록합니다. 실제 corpus·브라우저·HTTP 통합 검증은 등록된 hosted owner가 유지합니다. 실행·결과·미실행 범위는 소유 Task에 기록하며 CLI/API·README에 별도 명령 목록이나 결과 원장을 복제하지 않습니다.
5. 테스트가 특정 service 또는 package에만 해당하면 해당 디렉터리 README에 위치와 실행법을 기록합니다.

### 통합 테스트 (opt-in)

`tests/validation/test_mng_pg_init_sql.py`처럼 실제 컨테이너를 띄워야만
증명되는 계약은 opt-in 통합 테스트로 둡니다. CI gate adapter는
`tests.validation`과 `tests.lib` 모듈만 받으므로 별도 디렉터리를 만들지 않고,
모든 테스트 모듈처럼 full profile suite에 등록합니다.
Testcontainers가 컨테이너 수명주기를 소유하며, 대상 이미지 pin은 테스트가
Compose 선언에서 직접 읽으므로 따로 고정하지 않습니다.

기본 discovery에서는 항상 skip합니다. 실행하려면 Docker daemon과 opt-in이
모두 필요합니다.

```bash
pip install -r tests/requirements-integration.txt
HYHOME_INTEGRATION=1 PYTHONPATH=. python3 -m unittest tests.validation.test_mng_pg_init_sql
```

`HYHOME_INTEGRATION`이 `1`이 아니거나 `testcontainers`가 설치되어 있지 않으면
suite는 사유와 함께 skip하므로, daemon이 없는 환경에서도 전체 discovery가
그대로 동작합니다. CI validation profile은 이 의존성을 설치하지 않으므로
등록된 suite에서도 skip으로 보고되고 게이트를 막지 않습니다. `requirements-integration.txt`는
Renovate 범위 밖이고 `scripts/requirements.txt`와 같은 수동 갱신 대상입니다.

전체 테스트 모듈의 도달 가능성과 중복 등록은 LOCAL full 계획이 소유합니다.
모든 hosted context는 unit·구현 fixture·문서 링크 검사를 제외하며, 원격 PR은
현재 입력의 내용·구성 검증을 한 번 수행합니다. 실제 실행하지 않은 opt-in
runtime은 skip/NOT_RUN이며 live 서비스 성공으로 표현하지 않습니다.

일반 개발에서는 canonical runner의 `--profile changed --local-only --explain`으로
선택과 prerequisites를 먼저 확인한 뒤 필요한 unit·링크만 실행합니다. 각 테스트의
현재 호출과 배정은 Script Manifest와 workflow contract가 소유하며, 과거 mode·모듈
수량이나 완료 Spec 상태를 기대값으로 복사하지 않습니다.

`--profile full`은 별도 승인·예산을 기록한 전체 감사입니다. 현재 자동 workflow의
commit→push→PR→main 단계에 full 실행을 덧붙이지 않습니다. 실행 context와 실제
base/history에 따라 선택·문서 mode가 달라지므로, full 모델이나 로컬 PASS를 hosted
PASS로 대체하지 않습니다. 정확한 mode·argv는 canonical `--explain`과 실행 계약을
확인합니다. 전체 discovery는 일상 필수 gate나 추가 완료 조건이 아닙니다.

운영 rehearsal의 재사용 입력은 `examples/operations/`가 소유합니다. 단일 필드 오류
입력은 현재 동작을 검증하는 fixture builder로 만들며 production은 `tests/`를
읽지 않습니다. 과거 사건의 문자열·수량·폐기 파일 부재만을 검사하는 fixture는
현재 보장 이전과 caller 정리 후 폐기합니다.

## Related Documents

- [Root README](../README.md)
- [Scripts README](../scripts/README.md)
- [Documentation protocol](../.agents/governance/documentation-protocol.md)
- [Task checklists](../.agents/governance/task-checklists.md)
