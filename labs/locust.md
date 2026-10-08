---
title: "Locust 분산 부하 LAB"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
created: "2026-10-03"
---

# Locust 분산 부하 LAB

## Overview

이 문서는 root Compose에서 분리된 Locust master/worker LAB 계약을 설명한다.
독립 project, network, scenario volume과 result volume을 사용하며 HOME 상태나
정상 profile을 공유하지 않는다. 실행은 headless이고 승인된 제한 안에서 종료한다.

## Audience

- Python 기반 분산 부하 실습을 준비하는 품질 담당자
- LAB의 대상·자원·정리 경계를 승인하는 운영자
- root와 LAB 분리를 검토하는 인프라 담당자

## Scope

### In Scope

- master 한 개와 `LAB_LOCUST_EXPECT_WORKERS`개 worker의 독립 LAB closure
- 승인된 scenario의 읽기 전용 mount
- fresh result directory의 CSV summary와 full-history 출력
- worker 수, 사용자 수, 생성률, 실행 시간, 종료 코드 제한. 전체 상한은 worker 대기 상한 + `--run-time` + `--stop-timeout`이며, master가 끝나면 worker는 quit 메시지로 종료한다. pin된 image에는 OpenTelemetry SDK가 없어 `--otel`은 사용하지 않는다(SPEC-0214).

### Out of Scope

- HOME 서비스 기동·재시작과 실제 target traffic
- 외부 프로젝트 scenario 작성과 업무 API fixture의 의미 검증
- request별 raw trace와 장기 결과 적재
- 실행 결과를 **perf_db**에 가져오는 절차
- DB·Kafka 장애 주입처럼 WireMock 범위를 벗어나는 Toxiproxy 검토

## Structure

~~~text
labs/
├── .env.example # LAB 전용 공개 기본값
├── locust.yml   # 독립 Compose entrypoint
└── locust.md
~~~

실행 이미지는 [Locust 패키지](../infra/11-quality/locust/)가 소유한다.

## Tech Stack

| Category | Contract |
| --- | --- |
| Project | **hy-home-lab-locust** |
| Services | **lab-locust-master**, **lab-locust-worker** |
| Profile | **lab-locust** |
| Network | LAB 전용 **lab_locust_net**; HOME network 미참여 |
| Scenario | **LAB_LOCUST_SCENARIO_DIR** → **/mnt/locust/scenario:ro** |
| Results | **LAB_LOCUST_RESULT_DIR** → **/mnt/locust/results:rw**; master만 mount |
| Host exposure | 없음 |

## Configuration

| Variable | Required | Description |
| --- | ---: | --- |
| **LAB_LOCUST_SCENARIO_DIR** | Yes | 검토된 locustfile.py가 있는 read-only source |
| **LAB_LOCUST_RESULT_DIR** | Yes | 비어 있는 실행별 결과 directory |
| **LAB_LOCUST_NETWORK_NAME** | No | LAB 전용 network 이름 |
| **LAB_LOCUST_EXPECT_WORKERS** | No | worker replica 수이자 master가 기다릴 worker 수(한 입력); 기본값 2 |
| **LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT** | No | worker 접속 대기 상한(초); 부족하면 부하 없이 non-zero로 종료; 기본값 60 |
| **LAB_LOCUST_USERS** | No | 최대 동시 사용자 수; 기본값 10 |
| **LAB_LOCUST_SPAWN_RATE** | No | 초당 사용자 생성률; 기본값 1 |
| **LAB_LOCUST_RUN_TIME** | No | bounded 실행 시간; 기본값 30s |
| **LAB_LOCUST_STOP_TIMEOUT** | No | task 종료 대기 초; 기본값 5 |
| **LAB_LOCUST_EXIT_CODE_ON_ERROR** | No | threshold 실패 종료 코드; 기본값 1 |

CSV full history는 시간대별 aggregate이며 request별 raw evidence가 아니다. master의
종료 코드와 CSV 파일이 모두 있어야 실행 결과를 판정할 수 있다. 각 scenario는
client timeout을 명시해야 한다. master readiness는 이미지에 있는 Python으로 TCP 5557을
확인하며 worker는 Python으로 실제 process argv의 `--worker`를 확인한다.
별도 `pgrep` 실행 파일의 설치를 가정하지 않는다. 사용하는 client가 OpenTelemetry를 직접 지원하지
않으면 Locust request event에서 별도 계측하는 계약을 외부 프로젝트가 소유한다.

## Validation

실제 컨테이너를 만들지 않는 정적 render 예시:

~~~bash
LAB_LOCUST_SCENARIO_DIR=/tmp/hyhome-locust-scenario \
LAB_LOCUST_RESULT_DIR=/tmp/hyhome-locust-result \
docker compose --env-file labs/.env.example -f labs/locust.yml \
  --profile lab-locust config --quiet
python3 -m unittest tests.validation.test_quality_mock_lab -v
~~~

정적 render는 scenario 정확성, worker 접속, target 권한, OTel 전달, client timeout,
생성기 포화 또는 결과 완전성을 증명하지 않는다.

[합성 request-event 인수](../examples/operations/locust-telemetry/README.md)는 실제
HttpUser.requests worker의 counter·ms histogram·ReadTimeout과 master CSV를
대조한다. client URL·context·header·body·예외 문자열은 수집하지 않는다.
이 결과는 해당 client/event 경로의 검증이며 OTel SDK exporter 전달, 모든 Python
client와 실제 외부 프로젝트의 timeout 지원까지 검증한 것으로 확대하지 않는다.
같은 디렉터리의 `lifecycle.py`는 `lab.py`의 감독 아래에서 완료·종료 코드 전달·상한·
취소·master 비정상 종료·worker 탈락을 재현한다.

## Usage

1. Docker context, project, target origin, network, volume, CPU/RAM/디스크와 정확한
   정리 대상을 먼저 기록한다.
2. scenario directory를 읽기 전용으로 검토하고 새로운 빈 result directory를
   실행마다 지정한다.
3. target 소유자의 승인 뒤에만 `python3 scripts/operations/lab.py run locust --purpose "<목적>" --lease <기간> --deadline <상한>`으로 실행한다. 제어기가 master 종료를 기다리고, 상한이나 SIGTERM에서 master를 멈춘 뒤 project를 내린다. 결과는 ledger의 `outcome`과 제어기 종료 코드(정상은 master 코드, 상한 124, 취소 130)로 남는다.
4. master 종료 코드, worker 수와 CSV 산출물을 함께 보존한다.
5. 정리는 이 LAB가 소유한 project와 경로만 대상으로 하며 **down -v**와 volume
   prune을 사용하지 않는다.

## Related Documents

- [Locust 실행 이미지](../infra/11-quality/locust/README.md)
- [운영 문서 색인](../docs/05.operations/README.md) — `GDE-0062`, `POL-0062`, `RUN-0062`
