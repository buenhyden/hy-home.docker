---
title: "Performance Testing Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "operations"
artifact_id: "GDE-0064"
parent_ids:
- "POL-0064"
created: "2026-05-10"
---

# 성능 시험 사용 가이드

## Usage

`k6`는 기본 부하 발생기, WireMock은 외부 HTTP 의존성의 모의 서버,
Locust는 독립 LAB에서 사용하는 선택 도구다. 실제 경로는
승인된 앱 시험에서 `k6 → 개발 API → 실제 worker → WireMock`이다. WireMock만 호출한
수치는 애플리케이션 성능으로 분류하지 않는다. k6는 JavaScript 시나리오와
일회성 CI 실행에 맞고, Locust는 Python 사용자 행동 모델과 분산 worker
실습에 맞는다. 두 도구의 HTTP 지원과 운영 형태가 다르므로 시나리오
소유자가 필요한 프로토콜을 선택한다. 실제 이미지와 유지 상태는 각
Dockerfile/Compose 및 공식 프로젝트 자료에서 재확인한다.

| 도구 | 언어·부하 모델 | 프로토콜·CI/현재 배치 | 라이선스·결정 |
| --- | --- | --- | --- |
| [k6](https://github.com/grafana/k6) | JavaScript, 가상 사용자·도착률 | HTTP 중심 시나리오와 일회성 `testing` job; 종료 코드/threshold를 CI에 연결 | AGPL-3.0, 기본 발생기 |
| [Locust](https://github.com/locustio/locust) | Python, 사용자 행동·분산 worker | 주로 HTTP client, 별도 LAB의 headless 집계·CSV | MIT, 선택 실습 도구 |
| [WireMock](https://github.com/wiremock/wiremock) | Java HTTP stub | HTTP 응답·오류·지연 모의; 부하를 만들지 않음 | Apache-2.0, 의존성 모의 |

실제 태그·호환성·유지 상태는 실행 시점 공식 저장소에서 다시 확인한다.
[Timescale용 xk6 출력 확장](https://github.com/grafana-cold-storage/xk6-output-timescaledb)은
2026-06-05 보관되어 기본 의존성에 넣지 않는다.

외부 프로젝트는 Project-Template에서 파생한 작업공간에서 업무 시나리오,
fixture, API 계약, 완료 확인 및 임계값을 소유한다. 이 저장소는 공용 runner,
실행 manifest, 결과 판정·적재 도구, `perf_db` 권한과 대시보드를 소유한다.
외부 앱 전체 경로는 루트 Compose에 include하지 않는다.

### 실행 전 입력

- 대상 소유자와 `@buenhyden`이 정확한 origin/port, 허용 네트워크,
  users/rate/duration, CPU·메모리·디스크, 중단 SLI를 승인한다. 공개 API,
  관리자 endpoint, 실제 사용자 계정은 대상에서 제외한다.
- `project_id`, `run_id`, `attempt`, scenario/fixture revision과 hash,
  image, mock mode, 임계값, 읽기 전용 scenario 경로와 새 결과 경로를 기록한다.
  URL redirect가 승인된 origin 밖으로 나가지 않게 한다.
- 관리 PostgreSQL·관리 secret을 부하 발생기에 전달하지 않는다. 키는
  승인된 참조만 사용하며 원본에 query/token/cookie/PII를 기록하지 않는다.

### 결과와 판정

k6의 check만으로 실패 종료를 보장하지 않으므로 threshold와 종료 코드를
함께 읽는다. HTTP 202는 접수만 뜻한다. 비동기 완료 상태·최종 조회·권한·
저장을 시나리오에서 별도로 확인한다. 예상한 429/503과 실제 실패, 대상
포화와 발생기 포화, dropped iteration과 수집기 drop도 분리한다.

실행별 manifest·원본·summary·exit metadata·checksum이 완결된 뒤
`perf_db`로 적재한다. 동일 checksum 재적재는 멱등 처리하고 같은
`run_id`/`attempt`의 다른 파일은 충돌로 처리한다. 실행 상태, 시험 판정,
증거 완전성, 적재 상태는 서로 다른 필드다. p95/p99 값을 평균해 전체
백분위수를 만들지 않는다. 원본과 보고서는 제한된 객체 범위에 보관하고
DB에는 정규화 결과와 객체 참조를 둔다. 실제 bucket, secret, 보존 기간은
프로젝트별 승인 계약이 정한다.

### 구현 계약과 연결 경계

[k6 runner 계약](../../../infra/11-quality/k6/README.md)은 승인된 exact-path
경계와 native 원본의 크기·파일 신원·단위·태그 검사를 소유한다. v2 실행은
request-level 원본이 없거나 잘리면 증거를 incomplete로 처리하며 적재를 거절한다.
객체 upload/restore는 프로젝트별로 승인된 endpoint·bucket/prefix·quota 계약과
SHA256 대조가 필요하다. 실제 SeaweedFS 호환성·writer 발급은 별도 인수 대상이다.

[Locust LAB](../../../labs/locust.md)은 client별 request-event/timeout 계약을
소유한다. 합성 HttpUser.requests 실행은 counter·ms histogram·master CSV를
대조하며 SDK exporter 전달을 대신 증명하지 않는다. 실행 도구는 신뢰 가능한
Docker 경로와 빈 임시 HOME/config를 사용하고 결과 파일과 정리 범위를 제한한다.

[Grafana 결과 조회 계약](../../../infra/06-observability/grafana/README.md)은
별도 승인 reader의 project/run/attempt 조회와 opt-in datasource를 소유한다.
Alloy의 합성 delta/cumulative·중복·drop/retry·restart 검증은 HOME 반영이나
재시작을 넘는 메트릭 영속성 증거가 아니다. 실제 reader·bucket·부하 대상이
선정되기 전에는 소스 계약만 소비하며 자동 연결·배포하지 않는다.

## Common Checks

- `python3 scripts/validation/run-ci-gate.py --profile changed`는 변경 경로의
  소스·문서 회귀를 검사한다. 통과해도 실행 대상의 준비 상태는 증명하지 않는다.
- root `--profile '*'` 렌더에 Locust가 없고, 독립 `labs/locust.yml`의
  master/worker closure가 별도 프로젝트·네트워크·볼륨을 사용하는지 본다.
- WireMock 기능 모드의 journal·reset과 부하 모드의 journal 비활성화를
  구분한다. 무저널 모드에서 `GET /__admin/requests`의 HTTP 500은 빈 저널의
  증거가 아니며, 호출 횟수 판정에 사용하지 않는다. admin API는 인증이
  없으므로 호스트 공개와 내부 peer 접근을 제한한다.
- 실제 실행은 `RUN-0064`의 대상·자원·정리 사전 점검과 별도 승인을 따른다.

## Runbook Handoff

[RUN-0064](../runbooks/0064-performance-testing.md)는 부하 중단과 대상
회복 판단을 소유한다. 현재 SPEC-0203 소스·합성 검증은 HOME 실행이나
실제 프로젝트의 성능 수치가 아니다. k6, Locust, WireMock의 세부 절차는
각 서비스 런북을 따른다.

## Traceability

- [POL-0064](../policies/0064-performance-testing.md)
- [RUN-0064](../runbooks/0064-performance-testing.md)
- [SPEC-0203](../../98.archive/completed/03.specs/0203-quality-results-and-isolated-load-testing/spec.md)
- [ADR-0046](../../02.architecture/decisions/0046-capability-tiers-and-quality-boundary.md)

## Related Documents

- [k6 Guide](0061-k6.md)
- [Locust Guide](0062-locust.md)
- [WireMock Guide](0092-wiremock.md)
- [Operations index](../README.md)
