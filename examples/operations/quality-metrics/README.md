---
title: "합성 OTLP 메트릭 전달 인수"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
---

# 합성 OTLP 메트릭 전달 인수

## Overview

기존 Alloy 설정의 bounded transform·delta 변환·batch·label 제한·remote write를
그대로 추출하여 합성 HTTP OTLP 입력부터 Prometheus 조회까지 확인합니다.
HOME root가 include하지 않는 일회성 회귀 시험이며 상주 collector를 추가하지 않습니다.

## Audience

- 공유 관측 계약을 검증하는 QA·운영 담당자

## Scope

delta/cumulative counter와 histogram의 count·sum·bucket, 정확한 delta replay,
project identity 없는 표본 거절, k6 Rate `condition`(zero/nonzero)과 producer instance의 별도 series 유지, 인증 없는 producer의 401 거부, Prometheus 중단 중 queue 재시도, Alloy 재시작 뒤
동일 metric·resource identity의 새 source epoch에서 counter 4 → 6을 검증합니다. 실제 Grafana datasource·프로젝트 계정·HOME 트래픽은
이 fixture의 입력이 아니며 별도 승인과 실제 소비자가 필요합니다.

## Structure

- `docker-compose.yml`: 별도 internal network의 Alloy·Prometheus·Python probe
- `acceptance.py`: 캐시 digest·context·용량·모델 확인, 전달 인수, 정확한 정리
- `executor_stage.py`: 실제 executor·relay controller·path guard를 쓰는 k6 단계와
  HOME canary(`--home`)
- `README.md`: 입력·출력·검증 범위

## Tech Stack

기존 선언과 동일한 Alloy·Prometheus 및 시험용 Python의 실행 시 확인한 SHA256
digest를 사용합니다. 캐시 tag의 정확한 입력은 [controller의 TAGS](acceptance.py)가
소유합니다. 자동 pull은 없습니다. 추출 원본은
[Alloy 설정](../../../infra/06-observability/alloy/config/config.home.alloy)입니다.

## Configuration

`--alloy-image`, `--prom-image`, `--probe-image`는 캐시된 amd64 immutable image입니다.
현재 tag의 image ID와 digest의 image ID가 일치해야 합니다. 승인된 `default` context의
local Unix socket만 사용하며 별도 UUID project/network의 기존 상태가 없어야 합니다.

host port·Compose secret·named volume은 0개입니다. controller가 만든 합성 bearer token 파일만 `/run/secrets/quality_otlp_token`에 읽기 전용으로 bind합니다. `--source <path>`로 다른 Alloy 설정(예: 변경 전 설정)에 같은 인수를 적용할 수 있습니다. `--k6-image`, `--guard-image`(Traefik), `--mock-image`(WireMock) 세 digest를 함께 주면
k6 단계가 실행됩니다. [path guard fixture](../quality-path-guard/README.md)를 target으로
띄우고 `quality_run.py run`과 relay controller로 실제 실행합니다. relay는 이 harness의
internal network를 egress로 써서 harness Alloy의 인증 수신기에 보냅니다. Prometheus에
남은 요청·check·dropped iteration 수가 k6 summary와 같은지, dashboard 질의가 모두 값을
돌려주는지, 시나리오가 위조한 project·instance가 저장되지 않는지 확인합니다. 이어서
iteration을 버리지 않은 run의 dropped 패널 0과 없는 run의 값 없음, 계약을 어긴 relay의
실행 전 거부, SIGTERM 취소 뒤 그 attempt의 runner·relay만 지워지는지, `cleanup --run-id`가
그 run의 잔여물만 지우는지를 차례로 봅니다. 모든 container는 비특권·read-only이며
CPU 합계 1.25, 메모리 제한 합계 832 MiB입니다. controller가 생성한 합성 설정 파일만
읽기 전용으로 bind합니다. 저장과 WAL은 tmpfs이므로 프로세스/컨테이너 종료 뒤 영속
복구를 증명하지 않습니다. 재시작 검사는 동일 identity의 새 source epoch 초기화와 다음 delta의 누적 범위입니다.
재시작 전 값 5의 보존·복구를 주장하지 않습니다.

## Validation

```bash
python3 -m unittest tests.validation.test_quality_observability -q
python3 examples/operations/quality-metrics/acceptance.py \
  --alloy-image '<cached-alloy@sha256:digest>' \
  --prom-image '<cached-prometheus@sha256:digest>' \
  --probe-image '<cached-python@sha256:digest>'
```

전달 결과는 실제 Prometheus public query API의 값으로 판정합니다. 시작 성공이나
HTTP OTLP 수락만으로 전달 성공을 기록하지 않습니다. label allowlist와 필수 project
identity가 실제 조회에서 지켜지는지도 확인합니다. 증거와 종료 코드는 현재 Task가
소유합니다. cache/context/용량이 없으면 실행을 중단하고 검사를 `NOT_RUN`으로 기록합니다.

`executor_stage.py --home`은 HOME canary입니다. 같은 path guard target과 relay
controller를 쓰되 egress는 `quality_otlp_net`, token은 HOME `quality_otlp_token`입니다.
`obs_net`의 일회성 probe가 HOME Prometheus를 조회하고, Grafana API로 provision된 k6
dashboard를 읽어 그 질의를 `/api/ds/query`로 실행합니다. Grafana admin 비밀번호는 probe에
읽기 전용 파일로만 mount하며 출력하지 않습니다.

```bash
python3 examples/operations/quality-metrics/executor_stage.py --home \
  --k6-image '<grafana/k6@sha256:...>' --guard-image '<traefik@sha256:...>' \
  --mock-image '<wiremock/wiremock@sha256:...>' --alloy-image '<grafana/alloy@sha256:...>' \
  --probe-image '<python@sha256:...>'
```

## Usage

원본 pipeline을 변경하거나 HOME 서비스·망·volume을 연결하지 않습니다. cleanup은
정확한 controller project의 `compose down --timeout 10`만 사용하며 `down -v`·prune은
없습니다. 소유 container와 network가 없어진 것을 확인한 후 controller scratch만
삭제합니다. 정리 실패 시 scratch를 보존하고 정확한 잔여 경로를 조사합니다.

## Related Documents

- [Alloy README](../../../infra/06-observability/alloy/README.md)
- [Grafana README](../../../infra/06-observability/grafana/README.md)
- [문서 허브](../../../docs/README.md)
