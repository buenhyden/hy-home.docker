---
title: "Conftest Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
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

## Audience and Goal

인프라 소스에 정책 검사를 실행하는 개발자와 운영자를 위한 문서다. 검사 범위와 규칙을 이해하고 실패 신호를 해석하는 것이 목표다.

## Usage

### Current implementation

- [Conftest Compose](../../../infra/11-quality/conftest/docker-compose.yml)는
  고정된 `openpolicyagent/conftest` 이미지를 UID 1000, 읽기 전용 루트,
  네트워크 없음, `infra/`만 읽기 전용으로 마운트해 실행한다. `secrets/`나
  `.env`는 전혀 보지 않는다.
- `run.sh`는 먼저 정책 자체 테스트에 대해 `conftest verify`를 실행한 다음
  `infra/` 아래의 모든 `docker-compose*.yml`과 `Dockerfile*`을 테스트한다.
  `deny`는 job을 실패시키고 `warn`은 출력만 한다.

### Rules

| Namespace | Deny | Warn |
| --- | --- | --- |
| `compose` | 허용목록(`cadvisor`) 밖의 privileged 서비스; 프로파일 없는 서비스; `:latest` 또는 태그 없는 이미지; 리터럴 값을 가진 password, secret, token, key 변수; 호스트 주소(리터럴 IP, `${VAR:-address}`, `[::1]`, long-syntax `host_ip`) 없이 게시된 호스트 포트, 또는 `0.0.0.0`/`::`에 게시된 호스트 포트 | — |
| `dockerfile` | 태그 없거나 `:latest`인 `FROM`(빌드 스테이지와 `scratch`는 예외); `--checksum` 없이 URL에서 받는 `ADD` | — |

정확한 키·값 판별과 예외는 [Rego 원본](../../../infra/11-quality/conftest/policy/compose.rego)을
따른다. 일부 비밀 이름 패턴과 `$`로 시작하는 값 등의 휴리스틱이므로 모든 자격 증명을
탐지하거나 모든 보간이 안전하다고 증명하지 않는다. `*_FILE`·`*_CMD`의 예외도
비밀 값 노출 금지 정책을 면제하지 않는다.

### Commands

| Command | Effect |
| --- | --- |
| `docker compose --profile policy-check run --rm conftest` | 정책을 검증한 다음 run.sh가 선택한 raw Compose 파일과 Dockerfile을 테스트 |

### Common Checks

- CI는 `repository-integrity` suite에서 `leaf.conftest-policy`
  (`scripts/validation/check-conftest-policy.sh`)로 이 job을 실행한다.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`

### Runbook Handoff

job이 실패하면 [runbook](../runbooks/0095-conftest.md)을 사용한다.

### 검사 범위와 실패 신호

실행 script는 `infra/`의 파일을 직접 읽는다. include·override를 합친 최종 Compose,
루트 파일, inline Dockerfile 및 실행 중 상태는 이 파일 탐색 검사의 범위가 아니다.
별도 의존성·HTTP health·애플리케이션 데이터는 없으며 exit와 단계별 결과가 신호다.
앞 단계가 실패하면 뒤 단계는 실행되지 않으므로 세 요약을 항상 기대하지 않는다.
네트워크 없음·읽기 전용·사용자 제한을 갖춘 선언된 Compose 작업만 사용한다.

### Traceability

- [Policy](../policies/0095-conftest.md) (`POL-0095`)
- [Runbook](../runbooks/0095-conftest.md) (`RUN-0095`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Conftest package README](../../../infra/11-quality/conftest/README.md)
- [Conftest documentation](https://www.conftest.dev/)
- [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-language/)
