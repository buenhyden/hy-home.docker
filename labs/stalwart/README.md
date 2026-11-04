---
title: "Stalwart Mail Server"
version: "2.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-04"
created: "2025-12-03"
---

# Stalwart Mail Server

## Overview

Stalwart는 독립 Compose project인 [Stalwart LAB](../stalwart.yml)(`mail-server`
profile)의 메일 서버 실험입니다. root Compose에 포함되지 않고 HOME network에 연결되지
않으며 Traefik route도 없습니다. 어떤 HOME 컨테이너도 이 서버로 메일을 보내지 않으며
HOME 메일 캡처는 Mailpit(subject `0084-mailpit`)이 담당합니다. 외부 relay는 없고
SMTP/IMAP listener는 `lab_stalwart_net` 안에서만 도달하며, 관리 UI·JMAP(8080)만
`${LAB_HOST_BIND_IP}:${LAB_STALWART_HOST_PORT:-18093}`에 게시됩니다. 자체 완결 LAB이라
HOME endpoint 입력이 없습니다. 운영 subject는 `0070-mail`입니다.

## Audience

메일 운영자, DNS/TLS 담당자와 인프라 엔지니어.

## Scope

Stalwart의 SMTP/IMAP/JMAP, 관리 UI, 비밀 참조와 데이터 저장 선언을 설명한다. 개발 SMTP 트랩과 DNS 공급자 변경 절차는 포함하지 않는다.

## Structure

```text
stalwart/
├── README.md
└── config/              # datastore config, plan.ndjson, start/apply scripts, CLI Dockerfile
```

서비스 정의(`stalwart`, `stalwart-config`)는 [labs/stalwart.yml](../stalwart.yml)이 소유한다.

## Usage

Guide `GDE-0070`(`docs/05.operations/guides/15-labs/0070-mail.md`), Policy `POL-0070`,
Runbook `RUN-0070`을 따른다. 명령은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/stalwart.yml --profile mail-server` 접두사로
실행한다. `config`는 render만 하며, 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down stalwart`의 lease 규칙
([LAB 안내](../README.md#usage))을 따른다. 시작 전 DNS, TLS, 인증, 데이터 복구 증거를 확보한다.

## Configuration

| Setting | Source / behavior |
| --- | --- |
| Profile | `mail-server` / `labs/stalwart.yml` |
| Image | [Compose](../stalwart.yml); [derived Compose image projection](../../infra/tech-stack.versions.json) |
| Data | `${LAB_DATA_DIR}/stalwart/data` → `/var/lib/stalwart` (첫 기동 전 빈 디렉터리로 존재해야 하며 이미지 사용자 UID 2000 소유가 복사됨; 실제 경로의 소유권·권한은 별도 확인) |
| Configuration | `config/plan.ndjson`을 `stalwart-config`가 적용; listener 변경은 다음 재시작부터. 메일 도메인은 `LAB_STALWART_DEFAULT_URL` |
| Secret | `${LAB_SECRET_DIR}/stalwart/password.txt`의 LAB 전용 `lab_stalwart_password` → `/run/secrets/stalwart_password` → recovery admin; Compose에 credential 없음. 한 줄, `:` 없는 값이어야 함(`user:password`로 조합). HOME 값 복사는 별도 승인 |
| Network | `lab_stalwart_net`(`hy-home-lab-stalwart`); HOME network 없음 |
| Host ports | `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_STALWART_HOST_PORT:-18093}` → 8080(관리 UI·JMAP)만. SMTP 25·submission 587·IMAPS 993은 게시하지 않음 |
| Relay | 없음 (`allowRelaying = false`); 설정 도메인 밖 수신자는 SMTP `550`(`Relay not allowed`) |
| UI | Traefik route·SSO 없음; LAB bind 주소의 8080 게시 포트로만 접근 |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |

## Service Readiness

서비스와 healthcheck는 [Compose](../stalwart.yml)에 선언되어 있다. `/healthz/live` healthcheck는 배달·TLS·인증 검증을 대신하지 않는다. 실제 메일함 데이터, 백업 및 복원 성공 여부는 별도 운영 증거가 필요하다. 개발 테스트는 Mailpit 가이드(`GDE-0084`)를 따른다.

서버 패치의 Compose 이미지와 config builder의 서버 `FROM`은 같은 tag/index로
변경합니다. CLI는 독립 공급자 버전과 soak 조건을 따르며, 이번 서버 후보 준비에서
기존 CLI pin·listener·인증·relay 선언은 유지합니다. 소스와 공개 artifact
식별 대조는 실제 config job, SMTP/JMAP 배달, mailstore·backup·복원 인수가 아닙니다.
운영 상태가 바뀐 뒤에는 소스 revert나 이전 tag만으로 데이터를 되돌리지 않습니다.

## Validation

저장소 루트에서 render-only로 검사한다. 공개 예시 입력으로 렌더링하며, 실제 실행은 승인된 `labs/.env`를 쓴다.

```bash
docker compose --env-file labs/.env.example -f labs/stalwart.yml --profile mail-server config --quiet
docker compose --env-file labs/.env.example -f labs/stalwart.yml --profile mail-server config --services
python3 -m unittest tests.validation.test_lab_isolation
```

정적 검사 결과는 배달·복구 성공을 뜻하지 않는다. 런타임 리허설은 활성 lease와 별도 실행 승인이 있을 때만 수행한다.

## Troubleshooting

활성 lease 안에서 `... ps stalwart`로 상태를 확인한다. 관리 UI와 메일 프로토콜 오류를 분리하고 개인 메일·비밀을 제거한 증거만 런북에 기록한다. 데이터 삭제나 검증되지 않은 downgrade를 일반 복구로 실행하지 않는다.

## Related Documents

- [LAB 탐색](../README.md)
- [문서 인덱스](../../docs/README.md)
- [Stalwart 공식 Docker 설치 문서](https://stalw.art/docs/install/platform/docker/).
