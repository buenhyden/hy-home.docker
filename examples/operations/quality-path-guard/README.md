---
title: "합성 부하 시험 HTTP 경로 경계"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
---

# 합성 부하 시험 HTTP 경로 경계

## Overview

기존 Traefik을 재사용하는 별도 합성 rehearsal입니다. 승인한 정확한 HTTP 경로만
WireMock에 전달하며 정상 HOME root는 이 Compose를 include하지 않습니다.

## Audience

- 합성 시험을 승인하고 격리·정리 범위를 확인하는 QA 및 운영 담당자

## Scope

- `test` 환경의 `load` mock mode만 제공하며 실제 앱·관리 API를 연결하지 않습니다.
- 외부 API 부하, HOME 기동, 실비밀 발급, Prometheus 연결은 별도 승인 범위입니다.

## Structure

- `docker-compose.yml`: 단발 rehearsal의 Traefik과 기존 WireMock 이미지 정의
- `acceptance.py`: 사전검증, 승인/비승인 path, threshold 실패와 정확한 정리 인수
- `README.md`: 입력·출력과 격리 계약
- [http_guard.py](../../../infra/11-quality/k6/http_guard.py): manifest에서 정확한 라우터 생성·검증
- [container_executor.py](../../../infra/11-quality/k6/container_executor.py): 실행 전 dependency closure 검사

## Tech Stack

이미지는 기존 [Traefik 선언](../../../infra/01-gateway/traefik/docker-compose.yml)과
[WireMock 선언](../../../infra/11-quality/wiremock/docker-compose.yml)의 버전을 재사용합니다.
실행 시 공식 이미지 digest와 architecture를 확인하여 `QUALITY_GUARD_IMAGE`와
`QUALITY_MOCK_IMAGE`에 SHA256 참조를 전달합니다. 새 HTTP mock이나 상주 gateway는 추가하지 않습니다.

## Configuration

`QUALITY_RUN_ID`, `QUALITY_RUNNER_NETWORK`, `QUALITY_BACKEND_NETWORK`,
`QUALITY_RUNNER_SUBNET`, `QUALITY_BACKEND_SUBNET`은 HOME과 다른 승인된 값을 사용합니다.
`QUALITY_GUARD_CONFIG`는 `prepare-guard`가 만든 파일의 절대 경로입니다.
내용은 JSON 표현의 유효한 YAML이며 Traefik file provider는 `/guard/routes.yml` 하나만 읽습니다.
`QUALITY_MOCK_MAPPINGS`는 읽기 전용 합성 stub 디렉터리입니다. secret·영속 volume·host port는 없습니다.

runner 망에는 실행 전 Traefik만, backend 망에는 Traefik과 WireMock만 존재합니다.
k6는 runner 망에만 접속합니다. 임의 origin·다른 경로는 기본 404이며 WireMock에 전달되지 않습니다.
관리자 API·Docker provider·watch는 사용하지 않습니다. 두 서비스는 UID/GID 1000:1000,
읽기 전용 root, cap drop, 제한된 tmpfs·CPU·메모리·PID로 실행됩니다.
시작 성공을 readiness로 간주하지 않으며 실행 전에 응답 및 manifest 검증을 수행합니다.

## Validation

```bash
python3 infra/11-quality/k6/quality_run.py prepare-guard \
  --manifest /approved/synthetic-run.json --output /approved/routes.yml
python3 -m unittest tests.validation.test_k6_results -q
```

합성 runtime 인수는 승인 후 다음처럼 실행합니다. 이미지 참조는 실행 시 확인한
기존 엔진의 digest를 전달하며 자동 pull은 수행하지 않습니다.

```bash
python3 examples/operations/quality-path-guard/acceptance.py \
  --guard-image '<approved-traefik@sha256:digest>' \
  --mock-image '<approved-wiremock@sha256:digest>' \
  --k6-image '<approved-k6@sha256:digest>'
```

controller는 context·이미지·용량·subnet 충돌을 사전 검사하며 승인 path 200,
비승인/admin path 404, 강제 threshold 실패 exit99를 확인합니다. 성공한 정리 뒤에만
해당 임시 디렉터리를 삭제합니다. 정리 실패 시 정확한 잔여 controller 경로를 조사합니다.

별도 fixture 실행 전 Docker context·프로젝트·포트0·망2·볼륨0·자원·이미지와 정확한
정리 대상을 확인합니다. 승인된 rehearsal만 `--env-file`의 합성 입력으로 render한 뒤 실행합니다.
`run`에 `--guard-config`, `--backend-network`, `--backend-container`와
`--wiremock-container`로 **Traefik container 이름**을 전달합니다.
실제 backend container는 두 번째 망에만 있습니다.
변조된 설정, 다른 provider, 게시 포트, 공유 peer는 container 실행 전에 거절합니다.

## Usage

HOME Compose나 운영 secret을 참조하지 않습니다. 종료 시 지정한 rehearsal 프로젝트의
컨테이너·망만 정리하고 생성한 임시 합성 파일만 삭제합니다. `down -v`·prune은 사용하지 않습니다.
원본 앱 target·트래픽·bucket·writer는 승인된 프로젝트 계약이 마련된 뒤 연결합니다.

## Related Documents

- [k6 README](../../../infra/11-quality/k6/README.md)
- [문서 허브](../../../docs/README.md)
- [공식 정확한 Path 라우팅](https://doc.traefik.io/traefik/reference/routing-configuration/http/routing/rules-and-priority/)
- [공식 file provider](https://doc.traefik.io/traefik/reference/install-configuration/providers/others/file/)
