---
title: "Conftest Usage Guide"
version: "1.0.5"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-27"
layer: "operations"
artifact_id: "GDE-0095"
parent_ids:
- "POL-0095"
implementation_services:
  infra/11-quality/conftest/docker-compose.yml:
  - conftest
created: "2026-09-23"
---

# Conftest Usage Guide

## Overview

Conftest는 `policy-check`로 선택되는 OPTIONAL 일회성 정책 테스트다. 실행
중인 컨테이너가 아니라 인프라 소스에 대해 Open Policy Agent(Rego) 규칙을
평가하므로, 시작 전에 잘못된 선언을 잡아낸다.

## Scope

### Audience and Goal

인프라 소스에 정책 검사를 실행하는 개발자와 운영자를 위한 문서다. 검사 범위와 규칙을 이해하고 실패 신호를 해석하는 것이 목표다.

## Concepts

### Current implementation

- [Conftest Compose](../../../../infra/11-quality/conftest/docker-compose.yml)는
  고정된 `openpolicyagent/conftest` 이미지를 UID 1000, 읽기 전용 루트,
  네트워크 없음, 공개 `infra/`·`labs/` 읽기 전용 mount로 실행한다.
  `secrets/`, `.env`, Docker socket은 마운트하지 않는다.
- 호스트 wrapper는 기존 canonical Git 추적 목록과 POL-0078 overlay 검증을
  사용한다. 무시된 설치 산출물은 읽지 않고, 무시되지 않은 미추적 소스 후보는
  Docker 호출 전에 실패시킨다. 검증된 overlay의 서비스에 원본 base의 profile만
  넣은 정책 입력과 두 NUL 경로 목록·digest를 임시로 준비한다.
- `run.sh`는 준비된 목록의 Compose·Dockerfile을 검사한다. `verify`, `corpus`,
  기본 `all`은 분리된 실행 범위이며 `deny`는 실패, `warn`은 출력만 한다.
  임시 공개 파생 입력은 읽기 전용이며 종료 시 정리된다.

## Usage

### Rules

| Namespace | Deny | Warn |
| --- | --- | --- |
| `compose` | 허용목록(`cadvisor`) 밖의 privileged 서비스; 프로파일 없는 서비스; `:latest` 또는 태그 없는 이미지; 리터럴 값을 가진 password, secret, token, key 변수; 호스트 주소(리터럴 IP, `${VAR:-address}`, `[::1]`, long-syntax `host_ip`) 없이 게시된 호스트 포트, 또는 `0.0.0.0`/`::`에 게시된 호스트 포트 | — |
| `dockerfile` | 태그 없거나 `:latest`인 `FROM`(빌드 스테이지와 `scratch`는 예외); `--checksum` 없이 URL에서 받는 `ADD` | — |

정확한 키·값 판별과 예외는 [Rego 원본](../../../../infra/11-quality/conftest/policy/compose.rego)을
따른다. 일부 비밀 이름 패턴과 `$`로 시작하는 값 등의 휴리스틱이므로 모든 자격 증명을
탐지하거나 모든 보간이 안전하다고 증명하지 않는다. `*_FILE`·`*_CMD`의 예외도
비밀 값 노출 금지 정책을 면제하지 않는다.

### Commands

| Command | Effect |
| --- | --- |
| `bash scripts/validation/check-conftest-policy.sh` | 정책 단위 테스트 후 준비된 버전 관리 소스 corpus 검사 |
| `bash scripts/validation/check-conftest-policy.sh --mode corpus` | 준비된 Compose·Dockerfile corpus 검사만 실행 |
| `bash scripts/validation/check-conftest-policy.sh --mode verify` | 정책 단위 테스트만 실행 |

### Runbook Handoff

job이 실패하면 [runbook](../../runbooks/12-testing-and-quality/0095-conftest.md)을 사용한다.

### 검사 범위와 실패 신호

wrapper는 root include·base 관계를 상속 profile 검증에만 사용한다. Rego에는
Git으로 추적하는 공개 Compose·LAB·Dockerfile 입력이 전달된다. 부분 overlay는
상속 profile만 보충되며 권한·포트·비밀 참조 등 다른 정책 필드는 유지된다.
일반 서비스의 누락 profile은 면제되지 않으며 overlay에 profile을 중복 선언하지 않는다.
include·override를 합친 최종 Compose, inline Dockerfile 및 실행 중 상태는 이
소스 corpus 정책 검사의 범위가 아니다. 준비되지 않은 직접 job `corpus`·기본 실행은
wrapper 필요 오류로 종료하고 raw fallback은 없다. 직접 job `verify`는 별도 가능하다.
별도 의존성·HTTP health·애플리케이션 데이터는 없으며 exit와 단계별 결과가 신호다.
앞 단계가 실패하면 뒤 단계는 실행되지 않으므로 세 요약을 항상 기대하지 않는다.
네트워크 없음·읽기 전용·사용자 제한을 갖춘 선언된 Compose 작업만 사용한다.

### Traceability

- [Policy](../../policies/12-testing-and-quality/0095-conftest.md) (`POL-0095`)
- [Runbook](../../runbooks/12-testing-and-quality/0095-conftest.md) (`RUN-0095`)
- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Troubleshooting

### Common Checks

- CI는 `repository-integrity` suite에서 `leaf.conftest-policy`
  (`scripts/validation/check-conftest-policy.sh`)로 이 job을 실행한다.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`

## Related Documents

- [Conftest package README](../../../../infra/11-quality/conftest/README.md)
- [Conftest documentation](https://www.conftest.dev/)
- [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-language/)
