---
title: "Locust 합성 요청 계측 인수"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
---

# Locust 합성 요청 계측 인수

## Overview

기존 Locust LAB Compose를 격리 overlay로 재생하여 실제 **HttpUser.requests** client의
worker request-event·timeout과 master CSV를 대조합니다. OTel SDK나 상주 mock을
추가하지 않습니다. 실제 LAB 환경 파일과 HOME 서비스는 이 시험의 입력이 아닙니다.

## Audience

- Locust Python client의 요청 계측 계약을 검증하는 품질·운영 담당자

## Scope

master 1개·worker 1개·기존 WireMock 이미지로 만든 합성 HTTP 의존성만 실행합니다.
사용자 1명, 생성률 1명/초, headless 4초, stop timeout 1초입니다. 정상 GET과 의도한
read timeout의 counter·누적 histogram count/sum/bucket을 검증합니다. 실제 API 부하,
OTel exporter 전달과 perf_db import는 이 시험이 증명하지 않습니다.

## Structure

- `compose.override.yml`: 기존 LAB 정의를 비밀·포트·named volume 없는 internal network로 제한
- `locustfile.py`: 합성 scenario와 requests client request-event 수집
- `acceptance.py`: digest·context·자원 확인, 결과 대조, 정확한 정리
- `lifecycle.py`: `lab.py` 감독 아래의 완료·종료 코드 전달·상한·취소·master 비정상
  종료·worker 탈락과 CSV 상태·정리 확인
- `README.md`: 입출력·검증·한계

## Tech Stack

[현재 Locust 이미지 원본](../../../infra/11-quality/locust/Dockerfile)의 2.46.6 및 기존
WireMock 이미지의 실행 시 확인한 linux/amd64 digest를 사용합니다. 구성 원본은
[labs/locust.yml](../../../labs/locust.yml)입니다. 공식
[request-event](https://docs.locust.io/en/stable/extending-locust.html)와
[requests client timeout](https://docs.locust.io/en/stable/api.html#locust.clients.HttpSession.request)
계약을 따릅니다. SDK 자동 계측 지원을 가정하지 않습니다.

## Configuration

`--locust-image`와 `--mock-image`는 승인된 immutable digest입니다. controller는
기본 Docker context의 local Unix socket과 캐시된 amd64 이미지만 사용합니다.
Docker는 신뢰할 수 있는 root 소유 절대 실행 경로만 허용하며 빈 scratch HOME와
DOCKER_CONFIG, 고정 PATH로 사용자 credential·plugin 설정을 소비하지 않습니다.
별도 UUID project·internal network, CPU 합계 1.5, 메모리 제한 합계 1024 MiB,
port·secret·named volume 0개입니다. controller의 합성 scenario/mapping만 읽기
전용으로 bind하며 결과는 새 scratch directory에 기록합니다.

request-event 입력 중 method·승인된 `health`/`timeout` group·응답시간(ms)·HTTP 상태와
ReadTimeout 여부만 사용합니다. URL·query·context·header·body·exception 문자열은
읽거나 저장하지 않습니다. counter 단위는 requests, histogram 단위는 ms이며
25/50/100/250/1000ms 누적 bucket과 infinity를 보존합니다. 잘못된 입력은 invalid
count로 기록하고 전체 인수를 실패 처리합니다. container가 작성한 JSON/CSV는
NOFOLLOW·NONBLOCK regular-file 검사, 64 KiB 상한, 읽기 전후 inode/mtime/ctime
대조와 정확한 schema로 검사합니다. 중복 JSON key·미승인 열·민감 field도 거절합니다.
실패 진단에는 원본 container log와 Docker stderr를 출력하지 않습니다. 실제 프로젝트 client/scenario는
외부 프로젝트가 소유하며 해당 client별 이벤트·timeout 지원을 별도로 검증합니다.

## Validation

```bash
python3 -m unittest tests.validation.test_locust_telemetry tests.validation.test_quality_mock_lab -q
python3 examples/operations/locust-telemetry/acceptance.py \
  --locust-image '<approved-locust@sha256:digest>' \
  --mock-image '<approved-wiremock@sha256:digest>'
```

합성 read timeout 때문에 Locust master의 예상 종료 코드는 1입니다. controller는
이 코드를 무조건 성공으로 취급하지 않으며, 정상 200과 실제 ReadTimeout 모두 존재하고
worker event count/failure 수가 master CSV와 같으며 누적 histogram이 유효할 때만
exit 0입니다. client timeout은 50ms이며 backend 지연은 250ms입니다. CSV는 aggregate이며
request별 원본 또는 OTel 전달 완료의 증거가 아닙니다.

## Usage

합성 값이 담긴 빈 환경 파일을 명시하여 저장소 `.env`와 `labs/.env`를 읽지 않습니다.
기존 root include를 수정하지 않으며 추가 host mount와 외부 network를 허용하지 않습니다.
정리는 controller project의 `compose down --timeout 10`만 사용합니다. `down -v`·prune은
없으며 정리가 성공한 뒤 controller scratch만 제거합니다. 정리 실패 시 scratch는
보존하고 잔여 자원을 조사합니다. digest·client·image 등 초기 preflight 실패도
controller scratch를 정리하며, 실제 Docker 정리가 실패한 경우에만 보존합니다.

## Related Documents

- [Locust LAB 계약](../../../labs/locust.md)
- [품질 문서](../../../infra/11-quality/locust/README.md)
- [문서 허브](../../../docs/README.md)
