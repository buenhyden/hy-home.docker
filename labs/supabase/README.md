---
title: "Supabase LAB Source"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
created: "2025-11-12"
---

# Supabase LAB Source

## Overview

이 폴더는 독립 LAB Compose 진입점인 [supabase.yml](../supabase.yml)의 공개 입력
계약을 설명합니다. GoTrue를 포함한 13개 Supabase 서비스는 root Compose include에서
분리되며, `scripts/operations/lab.py`가 검토된 예산·경로·lease 안에서 실행을
조정하는 유일한 runtime 진입점입니다. 이번 이동은 source 경로만 바꾸며 실행 중인
container, 비밀값, 데이터 디렉터리 또는 복구 상태를 변경하지 않습니다.

## Structure

```text
labs/
├── .env                 # LAB controller가 소비하는 단일 실제 public 환경 파일(추적 제외)
├── supabase.yml         # 독립 Compose 프로젝트
└── supabase/
    ├── .env.example     # labs/.env에 옮길 public key 안내
    └── README.md        # 이 문서
```

## Scope

| 항목 | 계약 |
| --- | --- |
| Project | `hy-home-lab-supabase` |
| Profile | 13개 서비스 모두 exact `supabase` |
| Services | `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor` |
| Network | project-local `supabase_net`, 실제 이름 `hy-home-lab-supabase-core` |
| Data root | `${LAB_DATA_DIR}/supabase`; HOME `DEFAULT_DATA_DIR`와 같거나 겹치면 controller가 거부해야 함 |
| Secrets group | `${LAB_SECRETS_GID:-1000}` |
| Published ports | loopback 전용 Kong 2개, Analytics 1개, PostgreSQL/Supavisor 2개 |
| Common controls | `../infra/common-optimizations.yml` |

`db-config`는 `${LAB_DATA_DIR}/supabase/db/config`에 bind-backed된 local volume입니다.
Storage, Imgproxy, Functions와 PostgreSQL data는 격리된 LAB 경로의 기존 writable
state 계약을 유지합니다. DB 초기화 SQL 7개와 Kong, Vector, Supavisor 설정은
read-only bind이며, 누락된 입력을 Docker가 directory로 만들지 않도록
`create_host_path: false`를 사용합니다.

Vector의 Docker socket bind는 read-only여도 Docker API 권한 경계가 아닙니다.
소스 이동으로 이 위험이 해소되거나 runtime readiness가 입증되지는 않습니다.

## Usage

1. [.env.example](.env.example)의 필요한 public key를 단일 `labs/.env`에 둡니다.
2. LAB controller의 경로·예산·lease preflight를 통과합니다.
3. 정확한 host와 복구 경계가 승인된 뒤 `lab.py`로만 선택된 LAB을 실행합니다.

별도 `labs/supabase/.env`를 만들지 않으며 실제 `.env`, secret 값, private 로그를
이 폴더에 기록하지 않습니다.

## Tech Stack

정확한 엔진 버전은 [supabase.yml](../supabase.yml)이 소유합니다.

| Service | Technology | Role |
| :--- | :--- | :--- |
| **db** | PostgreSQL(pgvector) | 핵심 엔진 |
| **auth** | GoTrue | JWT 인증과 관리 |
| **rest** | PostgREST | 자동화된 REST API |
| **studio** | Supabase Studio | 통합 대시보드 |
| **kong** | Kong Gateway | API 게이트웨이 |

## Configuration

### Public Environment Variables

다섯 host port, dashboard username, Docker socket 위치와 공통 LAB
데이터·그룹·예산 key만 공개 환경 입력입니다. 인증자료는 Docker Secret 파일로만
참조하며 `.env.example`에 secret placeholder를 두지 않습니다.

### SMTP 단일 원본

공용 SMTP와 Auth는 COMM-002의 `secrets/communication/smtp/smtp_password.txt`를
함께 사용합니다. Auth는 `source: smtp_password`, `target: supabase_smtp_password`
별칭으로 기존 container 경로를 유지합니다. COMM-003은 값 없는 퇴역 alias입니다.
SMTP username, host, account와 Alertmanager 소비는 그대로 유지합니다.

GoTrue의 `_FILE` 입력은 native 기능이 아니라 Auth의 좁은 wrapper가 처리합니다.
wrapper는 빈/누락/읽기 실패 파일과 직접 `GOTRUE_SMTP_PASS`의 동시 입력을 거부하고,
원래 이미지 user로 값을 읽어 실행 프로세스에 전달한 뒤 원래 `auth` 명령을 exec합니다.
Compose/이미지 inspect에 실제 비밀번호를 넣지 않지만 실행 프로세스 환경에는 남으므로
호스트·Docker 관리자와 프로세스 환경 접근 권한은 계속 보호해야 합니다.
DB URL 및 DB/JWT 입력 결함은 별도이며 SMTP alias나 격리 시험은 전체 stack readiness가 아닙니다.

중복 호스트 파일의 실제 삭제는 SMTP01 참조 전환 완료 후 CLN01과 총괄 통합 순서를
따릅니다. source/runtime/job/backup-restore/external 의존 및 제한된 boolean 비교를
통과해야 하며, 불명확한 소비자는 삭제를 중단합니다. 실제 HOME activation은 별도
운영 증거가 필요합니다. 절차와 복구는
`docs/05.operations/runbooks/0029-supabase.md`의 `RUN-0029`에서 확인합니다.

## Validation

공개 합성 입력으로 Compose 전체 모델을 렌더하고 이전 13-service graph, container
name, profile, dependency, image와 wrapper를 비교합니다. 이동 경로, LAB data root,
local network, 11개 secret source와 read-only input guard만 승인된 차이입니다.
실제 image pull, service start, HOME 배포와 데이터 복구는 수행하지 않습니다.

## Troubleshooting

- read-only config/SQL input의 존재·symlink·HOME overlap을 preflight에서 확인합니다.
- `${LAB_DATA_DIR}`가 HOME data root와 같거나 겹치면 실행을 중단합니다.
- 기존 `supabase-*` container name이 존재하면 exact runtime lease 없이 시작하지 않습니다.
- PostgreSQL, Storage object와 설정의 빈-target 복구가 없으면 readiness를 주장하지 않습니다.

## Related Documents

- Guide: `docs/05.operations/guides/0029-supabase.md` (`GDE-0029`)
- Policy: `docs/05.operations/policies/0029-supabase.md` (`POL-0029`)
- Runbook: `docs/05.operations/runbooks/0029-supabase.md` (`RUN-0029`)

런타임 고정 값은 Compose 선언이 소유하며
[derived Compose 이미지 투영](../../infra/tech-stack.versions.json)은 drift를 검증합니다.
