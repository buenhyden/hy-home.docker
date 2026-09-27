---
title: "sample-web-service"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
---

<!-- Target: examples/sample-web-service/README.md -->

# sample-web-service

> `hy-home.docker`용 복사 가능한 모범 사례 서비스 시드입니다. 새 컨테이너
> 서비스를 시작할 때 이 폴더를 복사한 뒤, 이름, 이미지, 포트, 설정을 대상
> 서비스에 맞게 바꿉니다.

## Overview

최소한의 정적 웹 서비스로 이 저장소의 컨테이너 하드닝과 Compose 관례(pinned image,
non-root 런타임, read-only root filesystem, capability 제거, healthcheck, 리소스 제한,
secret-free 설정)를 보여 줍니다. Compose 정의는
고정된 top-level project 이름과 `container_name`을 의도적으로 생략하므로,
호출자는 `docker compose --project-name`으로 복사본을 격리할 수 있습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operations/SRE Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 복사 가능한 정적 웹 서비스 scaffold 파일
- 컨테이너 하드닝, healthcheck, 리소스 제한, 로그 보존 예시
- `.env.example`을 통한 secret이 아닌 로컬 환경 설정
- 현재 README와 서비스 scaffold 템플릿으로의 링크

### Out of Scope

- 프로덕션 서비스 소유권, SLA, 장애 대응 기록
- TLS 종료, ingress 라우팅, 영속 데이터 서비스
- secret 값, 자격 증명, 토큰, private key, raw 로그, shell history, `.env` 값

## Structure

```text
sample-web-service/
├── .env.example       # secret이 아닌 환경 변수 템플릿; .env로 복사해서 사용
├── Dockerfile         # 멀티스테이지 빌드와 unprivileged nginx 런타임
├── README.md          # 이 scaffold README
├── docker-compose.yml # 하드닝된 서비스 정의
├── nginx.conf         # 8080 포트로 listen하는 nginx 설정
├── service.md         # 채워진 서비스 scaffold 예시
└── site/index.html    # 서비스가 서빙하는 정적 콘텐츠
```

## How to Work in This Area

1. 새 컨테이너 서비스 예시를 시작할 때 이 폴더를 복사합니다.
2. 새 서비스에 맞게 이름, 이미지 태그, 포트, healthcheck, secret이 아닌 환경
   변수 키를 갱신합니다.
3. `service.md`를 등록된 Service metadata와 section 계약에 맞춰 유지합니다.
4. 병렬 로컬 인스턴스가 필요하면 명시적인 project 이름을 선택합니다.
5. 서비스를 사용하기 전에 Compose를 검증합니다.

## Files

| File                 | Role                                                            |
| -------------------- | --------------------------------------------------------------- |
| `Dockerfile`         | 멀티스테이지 빌드; `HEALTHCHECK`가 있는 unprivileged nginx 런타임 |
| `nginx.conf`         | `8080`(non-root 포트)에서 listen                              |
| `site/index.html`    | 서비스가 서빙하는 정적 콘텐츠                                    |
| `docker-compose.yml` | 하드닝된 서비스 정의                                            |
| `.env.example`       | secret이 아닌 환경 변수 템플릿; `.env`로 복사해서 사용           |
| `service.md`         | canonical Service 계약의 sample 전용 인스턴스                   |

## Service Readiness

| Control              | Status | Evidence                                                   |
| -------------------- | ------ | ---------------------------------------------------------- |
| Pinned image tag     | Ready  | 정확한 pin은 `Dockerfile`이 소유 (build/runtime 스테이지 모두 digest-pinned) |
| Non-root runtime     | Ready  | unprivileged image (uid 101), `privileged` 미사용           |
| Read-only rootfs     | Ready  | `read_only: true` + 쓰기 가능한 경로에 `tmpfs`              |
| Dropped capabilities | Ready  | `cap_drop: [ALL]`, `no-new-privileges:true`                |
| Healthcheck          | Ready  | `HEALTHCHECK` + Compose `healthcheck`                      |
| Resource limits      | Ready  | `deploy.resources.limits` (cpu/memory)                     |
| Secret handling      | Ready  | `env_file`만 사용; compose에 평문 secret 없음               |
| Log rotation         | Ready  | `max-size`/`max-file`를 사용하는 `json-file`                |
| Project isolation    | Ready  | 고정된 project나 container identity 없음                   |

## Operations

```bash
cp .env.example .env
docker compose config        # 검증
docker compose up -d --build # 시작
docker compose ps            # 상태 확인
docker compose down          # 중지
```

Spec 127 delivery rehearsal은 별도의 task 소유 project 이름, loopback 포트
`18080`과 `18081`, 불변 로컬 이미지 config digest를 사용합니다. 병합된
runtime topology는 build 경로를 초기화하고 `pull_policy: never`를 사용합니다.
wrapper는 또한 승인된 각 digest에 대해 정확한 로컬 image-object ID를 요구하며
`--pull never --no-build`로 시작합니다. 승인된 verdict fixture는 계약
테스트용일 뿐 실제 project 시작을 승인하지 않습니다. canonical
Spec 126 baseline/candidate 쌍이 존재하고 모든 상위 게이트를 통과할 때까지
runtime 명령은 fail-closed 상태를 유지합니다.

## Validation

- `docker compose config`가 오류 없이 파싱됩니다.
- `start_period` 이후 `docker compose ps`가 `healthy`를 보고합니다.
- `python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal`는
  Docker 리소스를 시작하지 않고 로컬 delivery 계약을 검증합니다.

## Troubleshooting

- 포트가 이미 사용 중: `.env`의 `WEB_HOST_PORT`를 바꿉니다.
- 컨테이너가 재시작됨: read-only root filesystem 아래에서 nginx 권한이나
  tmpfs 경로 오류가 있는지 `docker compose logs web`으로 확인합니다.

## Related Documents

- README template (`docs/99.templates/templates/common/readme-package.template.md`)
- Spec contract template (`docs/99.templates/templates/specs/spec.template.md`)
- New-service onboarding guide (`docs/05.operations/guides/0008-new-service-onboarding.md`)
- Release management runbook (`docs/05.operations/runbooks/0009-release-management.md`)
- [Documentation index](../../docs/README.md)
