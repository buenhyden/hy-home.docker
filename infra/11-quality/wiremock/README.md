---
title: "WireMock HTTP 모의 서비스"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-09-23"
---

<!-- [ID:11-quality:wiremock] -->
# WireMock HTTP 모의 서비스

## Overview

WireMock은 개발·계약 검사에서 외부 HTTP 의존성을 합성 응답으로 대체한다.
기능 모드는 제한된 요청 저널을 사용하고, 부하 모드는 요청 저널을 비활성화한다.
load override가 같은 **wiremock** 서비스의 port·command·healthcheck를 교체하므로
한 Compose model에는 한 모드만 존재한다.

## Audience

- 합성 HTTP fixture를 작성하는 개발자
- 기능·부하 검사를 설계하는 품질 담당자
- 노출 경계와 실행 상태를 확인하는 운영자

## Scope

### In Scope

- **wiremock** 기능 모드의 최대 1,000개 요청 저널과 실행 전 저널 초기화
- load override를 적용한 **wiremock**의 **--no-request-journal** 및 HTTP admin 거부 실행
- 추적된 **mappings/**, **__files/**의 읽기 전용 제공
- 기능 모드의 loopback 전용 호스트 포트

### Out of Scope

- 실제 upstream record-and-playback
- WireMock admin API 인증과 공용 gateway route
- Pact Broker가 소유하는 consumer 계약 판정

## Structure

~~~text
wiremock/
├── __files/           # mapping이 참조하는 추적 body file
├── mappings/          # 추적 stub mapping
├── docker-compose.yml # root에 포함되는 기능 모드
├── wiremock.load.yml # 같은 서비스를 교체하는 부하 모드 override
└── README.md
~~~

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Runtime | WireMock standalone 이미지 | 실제 tag는 [Compose](docker-compose.yml)가 소유 |
| Function mode | **wiremock**, **api-mock** | bounded request journal |
| Load mode | **wiremock**, **api-mock** + load override | override가 request journal과 host port를 제거 |
| Storage | 읽기 전용 bind mount | 영속 writable state 없음 |

## Configuration

기능 모드는 **127.0.0.1:${WIREMOCK_HOST_PORT:-18088}**에만 게시한다. 부하
모드는 host port를 reset하고 project-default network의 peer만
**wiremock:8080**으로 접근한다. 기능 모드 admin API에는 인증이 없다. 부하 모드는
**--admin-api-require-https**를 켜고 HTTPS listener를 열지 않아 HTTP admin 요청을
403으로 거부한다. 두 모드 모두 **traefik.enable=false**를 유지한다.

load 모드는 root와 override를 같은 명령에 전달해야 한다. override는 단독으로
실행할 image를 선언하지 않아 별도 project로 우회 실행할 수 없다.

기능 검사 시작 전 **DELETE /__admin/requests**로 요청 저널을 초기화한다. mapping을
변경하려면 추적 파일을 검토하고 컨테이너를 재생성한다. admin API로 만든 in-memory
stub은 재시작 시 사라지며 권위 있는 fixture가 아니다.

공식 WireMock 계약상 **--no-request-journal**은 요청 기록과 이후 verification을
비활성화한다. load 모드의 **GET /__admin/requests**는 결과 조회 경로가 아니며
현재 HTTP admin은 403으로 거부된다. 이를 빈 요청 저널이나 “요청이 없었음”으로
해석하지 않는다. HTTPS listener를 추가하는 변경은 admin 노출을 다시 검토해야 한다.

| Variable | Required | Description |
| --- | ---: | --- |
| **WIREMOCK_HOST_PORT** | No | 기능 모드 loopback 포트; 기본값 18088 |

## Validation

~~~bash
docker compose --env-file .env.example --profile api-mock config --quiet
docker compose --env-file .env.example -f docker-compose.yml \
  -f infra/11-quality/wiremock/wiremock.load.yml \
  --profile api-mock config --quiet
python3 -m unittest tests.validation.test_quality_mock_lab -v
~~~

정적 render는 실제 admin reset, mapping 응답 또는 부하 중 JVM 사용량을 증명하지
않는다. 2026-10-03 격리 합성 검사는 기능 모드에서 stub GET 200, journal count 1,
DELETE reset 뒤 count 0을 확인했다. load 모드는 같은 stub GET 200과
초기 **GET /__admin/requests** HTTP 500을 확인했다. HTTP admin 거부 옵션을
추가한 별도 격리 검사에서는 stub GET 200과 **GET /__admin/health** HTTP 403을
확인했다. 두 결과는 격리 실행 증거이며 HOME 배포나 실제 target 결과가 아니다.

## How to Work in This Area

1. 합성 데이터만 **mappings/**와 **__files/**에 추가한다.
2. 기능 판정은 root Compose, mock 자체 부하 측정은 root와 load override를 함께 사용한다.
3. 기능 실행마다 요청 저널을 초기화하고 민감한 요청 원문을 증거로 남기지 않는다.
4. load 모드에서 journal API 오류를 empty journal로 변환하거나 성공으로 판정하지 않는다.
5. 변경 후 두 모드를 각각 render하고 focused 테스트를 실행한다.

## Related Documents

- [문서 진입점](../../../docs/README.md) (`GDE-0092`, `POL-0092`, `RUN-0092`)
- [품질 tier](../README.md)
- [WireMock standalone options](https://wiremock.org/docs/standalone/java-jar/)
- [WireMock request journal configuration](https://wiremock.org/docs/configuration/#request-journal)
