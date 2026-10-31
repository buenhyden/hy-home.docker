---
title: "Hermes 수집 전송 소스"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-31"
---

# Hermes 수집 전송 소스

## Overview

기존 완료 산출물을 보존하는 로컬 발행기와 영속 대기함, 비활성 수집 흐름의
준비 소스입니다. Blog-data `dev` 커밋 `a6d0957ad380f179f73bdd2a60ff23792d53f7ae`의
수집 API 계약과 합성 Fixture를 고정했습니다. 고정 계약은 서버 B의 배포를
뜻하지 않습니다.

| 구분 | 상태 | 확인 범위 |
| --- | --- | --- |
| 소스 | 부분 구현 | 로컬 대기함, 계약 어댑터, 선택적 동일 요청 재전송, 제한된 `dispatch`, Companion Evidence v1 구조 검증, Ed25519 생산자 서명 검증과 공통 신뢰 판정, 비활성 수집 흐름 |
| 생산자 인증 | BLOCKED | 서명 검증기는 합성 키로 검증했지만 추적 키 저장소가 비어 있고 실제 제한 생산자 계정·키가 없음 |
| 계약·흐름 합성 검증 | PASS | 고정 계약·Fixture와 합성 응답, 빈 VM의 입력 선별 |
| 실제 원본 변환·전송 | BLOCKED | 실제 기사 수집 시각의 신뢰할 수 있는 근거와 전송 실행 연결 부재 |
| 격리 n8n Queue 합성 검증 | PASS | 기본 게시 API·정적 Webhook 등록, Worker·외부 JS Runner, 가짜 Gateway 201·합성 영속 수신 |
| 실제 운영 검증 | NOT_RUN | 추적 워크플로·실제 인증·서버 간 통신 및 Gateway 영속 수신 미실행 |

전체 시험과 최신 조사·독립 검토 결과는 `SPEC-0204-TSK-0022`가 소유합니다.

## Scope

기존 구조화 내보내기 작업 `84d3f689378b`와 원래 조사·이메일을 재사용합니다.
수집 대상은 `6eabd835f969`, `25674fbc0bf3`, `8d0925bc571d`의 완료 결과이며,
비공개 인프라 작업 `3c3f81a925e0`는 제외합니다. 다른 저장소의 크롤링을
복제하거나 매니페스트 통지 소비자를 변경하지 않습니다.

별도 검토된 기존 검증기의 정확한 경로와 다이제스트를 호출자가 지정해야 합니다.
누락·변경된 의존성은 거부합니다. 원본·후보·복수 아이디어의 바이트와 해시를
보존하고 같은 실행의 재입력은 중복으로 처리합니다. 내용 충돌은 최초 산출물과
충돌 기록을 남깁니다. 재요약이나 원본 삭제는 수행하지 않습니다.

## Structure

- [workflow.json](workflow.json): 입력 선별, 고정 HTTPS 대상과 영속 수신 응답 확인을 담은 비활성 템플릿입니다.
- [publisher/](publisher/README.md): 제한된 파일 읽기, 로컬 대기함과 전송 상태 처리입니다.
- [tests/](tests/README.md): 합성 시험과 소스 경계 검증입니다.
- [install.py](install.py): 커밋 하나를 root 소유 불변 release로 설치합니다.
- [pyproject.toml](pyproject.toml), [requirements.lock](requirements.lock): 실행 의존성 선언과 hash 고정본입니다.

## Usage

로컬 준비·상태 명령은 발행기 설명, 재현 가능한 시험 명령은 시험 설명을 봅니다.
배포 단위는 제한된 호스트 프로세스이며 설치물은 아래 "보호 설치"를 따릅니다.
운영 계정 생성, 설치, 서비스·예약 실행 등록은 아직 수행하지 않았습니다. `dispatch` 명령은 있으나 추적 키 저장소가 비어 있어
세 작업은 실제 인증 입력이나 네트워크 요청 없이 `blocked`를 반환합니다.

흐름은 `headerAuth` 수신 후 입력을 선별하고 Gateway에 전달한 응답을 확인합니다.
입력 선별은 전체 스키마 검증이 아니며 최종 판단은 Gateway가 담당합니다. 응답의
200·201 상태와 JSON 영속 수신 증거를 확인하기 전에는 성공을 반환하지 않습니다.
대상 `https://gateway.invalid/v1/ingestions`는 예약된 교체 지점이며 인증 참조도
연결되지 않았습니다. 실제 가져오기·Queue 실행·전달은 검증하지 않았습니다.

격리 시험에서는 고정된 `webhookId`를 가진 합성 흐름을 게시해 Webhook을 등록한 뒤,
추적된 흐름의 정확한 경로를 native helper로 확인하고, Worker와 외부 JavaScript
Runner를 거쳐 가짜 Gateway의 `201`·합성 영속 수신을 확인했습니다. 이는 추적된
흐름의 운영 요청이나 서버 B 요청이 아닙니다. 실제 주소, 인증, TLS, 재시도·복구와
영속 수신은 운영 검증 대기입니다.

정확한 대상과 승인 조건이 확정되면 운영자가 암호화된 기본 인증 저장소와
승인된 비밀 관리 경로로 인증을 연결합니다. 저장소와 공개 흐름에는 비밀값이나
실제 인증 식별자를 넣지 않습니다. 실행 데이터 저장 제한은 관리자 접근이나
실행 중 메모리까지 격리한다는 의미가 아닙니다.

### Companion Evidence v1 계약

Hermes 생산자가 후보 하나마다 함께 넘기는 직접 수집 기록입니다. 기존 후보
producer v1.0.0의 필드는 바꾸지 않습니다. 합성 예시는
[후보](./tests/fixtures/companion-candidate-v1.json)와
[증거](./tests/fixtures/companion-evidence-v1.json)이며 검증 구현은
[evidence.py](publisher/evidence.py)입니다.

| 필드 | 규칙 |
| --- | --- |
| `schema_version` | `hermes-companion-evidence/1` |
| `producer` | `name`, `version` 두 문자열만 허용 |
| `job_id`, `run_id` | 대기함 키와 후보 내용이 정확히 일치 |
| `candidate_sha256` | 후보 원문 바이트의 SHA-256 |
| `scheduled_at` | 해당 Cron 실행의 예정 시각, 시간대 포함 |
| `items[]` | 후보 `items`와 같은 수·순서, 한 항목에 한 기록 |
| `items[].index` | 후보 항목 순번(0부터) |
| `items[].source_url` | 후보 항목 `source_url`과 동일, 누락 시 보고서 전체 보류 |
| `items[].fetched_url` | 실제 응답을 받은 최종 HTTPS URL |
| `items[].fetched_at` | 응답 바이트를 받은 실제 시각, 시간대 포함, 밀리초까지 |
| `items[].http_status` | 2xx 정수 |
| `items[].body_sha256` | 전송·콘텐츠 인코딩을 해제한 실제 HTTP 응답 본문 바이트의 SHA-256 |
| `items[].cache` | `{hit:false,key_sha256:null}` 또는 `{hit:true,key_sha256:<64 hex>}` |
| `items[].tool_call_id` | 취득을 수행한 도구 호출 식별자, 1~128자 |
| `items[].status` | `complete`만 허용, 부분 실패·실패·취소는 보고서 전체 보류 |

모든 시각은 `scheduled_at` 이후, 후보 `generated_at` 이전이어야 합니다. 캐시
적중은 캐시 생성 시각이 아니라 원래 직접 수집 시각을 기록하므로 실행 예정
시각보다 이를 수 있습니다. 보고서 `collected_at`은 항목 `fetched_at`의 최댓값이며
추정·대체하지 않습니다. 중복 키·알 수 없는 필드·형식 오류는 모두 거부합니다.

이 검증은 구조와 결속만 확인하며 생산자 인증이 아닙니다. 구조 PASS만으로는
어떤 게이트도 열리지 않습니다.

### 생산자 인증

생산자 신뢰 경계는 분리 서명 하나로 정합니다.

1. 원천 Receipt는 취득 시점에, 최종 Companion은 후보 확정 뒤에 만듭니다. 각
   기록은 임시 파일에 쓰고 fsync한 뒤 rename으로 게시하며, 게시가 끝나기 전의
   응답 바이트나 Receipt는 요약·내보내기·서명에 쓰지 않습니다. 이 순서는 영속화
   전 소비를 막을 뿐 디스크 장애에 대한 보장은 아닙니다.
2. Hermes LLM 도구·내보내기와 다른 제한 생산자 계정이 Ed25519 개인키를 보관합니다.
   이 계정은 자신의 Receipt와 확정 후보를 읽어 Companion v1을 만들고 서명합니다.
3. 서명 파일은 Companion과 같은 이름에 `.sig`를 붙이며, 생산자는 서명 파일을 먼저
   쓰고 Companion을 나중에 게시합니다. 내용은
   `{schema_version:"hermes-companion-signature/1", key_id, algorithm:"ed25519",
   signature}`이고 서명 대상은 `hermes-companion-evidence/1` 뒤에 NUL 한 바이트와
   Companion 원문 바이트를 이은 값입니다.
4. Publisher는 공개키만 담은 추적 파일 [producer-keys.json](publisher/producer-keys.json)을
   읽습니다. 항목은 `key_id`, `algorithm`, `public_key`(원시 32바이트 base64),
   허용 `jobs`, `not_before`, `not_after`, 선택 `revoked_at`입니다. 폐기는 소급하여
   이미 대기함에 있는 기록도 다시 막습니다. 같은 `key_id`가 둘이면 거부합니다.
5. [trust.py](publisher/trust.py)의 판정 하나를 `dispatch`, 전송 처리기,
   요청 결속, 재전송 경계가 함께 쓰며 HTTP 전송기는 그 결과 표지를 확인합니다.
   서명·키·구조 중 하나라도 실패하면 모든 경계가 `blocked`입니다.

같은 계정의 서명 없는 JSON, `trusted=true` 같은 표지, 강제 실행 옵션은 없습니다.
추적 키 저장소는 비어 있으므로 실제 키를 검토해 추가하기 전까지 운영 기본값은
`blocked`입니다. 키 추가·회전·폐기 절차는 RUN-0053을 따릅니다.

서명 계약의 정본은 [trust.py](publisher/trust.py)의 `DOMAIN`, envelope 필드,
저장소 검증입니다. Hermes 생산자에게 전달하는 조건은 다음과 같습니다.

- `key_id`는 `[a-z0-9][a-z0-9._-]{0,63}`, `jobs`는 정확한 작업 ID 목록,
  `not_before`·`not_after`·`revoked_at`은 시간대가 있는 ISO 8601이며
  `not_before < not_after`입니다. 같은 공개키를 두 `key_id`로 등록할 수 없습니다.
- 공개키 지문은 원시 32바이트 공개키의 SHA-256 16진수입니다. 등록 PR에는 이
  지문과, 개인키가 생산자 계정 밖으로 나간 적 없다는 보호 생성·보관 증거를
  함께 둡니다. 운영자가 생산자 계정에서 따로 받은 지문과 일치해야 등록합니다.
- 개인키는 Publisher, 이 저장소, 시험 기록으로 가져오지 않습니다. 시험의 합성키는
  추적 저장소에 넣지 않습니다.

### 보호 설치

운영 전제는 코드가 확인합니다. `python3 -I`로 격리 실행해야 하며, 인터프리터,
venv 설정, 존재하는 모든 import 경로, 적재된 모듈 원본 파일(서명 검증과 인증
자식 프로세스가 쓰는 `ssl`·`http.client` 포함),
Publisher 모듈 전체와 키 저장소의 모든 상위 경로가 root 소유이고 group·other
쓰기 권한이 없으며 실행 계정이 쓸 수 없어야 합니다. 실행 계정이 아닌 다른 일반
계정(예: Hermes 생산자) 소유도 거부합니다. root로 실행하면 항상 막힙니다.
이 검사는 봉인된 설치 위의 탐지선입니다. 바이트코드 캐시, `.pth`, 검사 전에 실행된
코드는 root 소유 release가 보호합니다.

설치물은 사용자 작업 사본이나 편집 가능 설치가 아닙니다. 운영자가 검토된 커밋을
`git archive --format=tar <commit> -- infra/07-workflow/n8n/workloads/hermes-blog-ingestion`
으로 만들고 root가 `python3 -I install.py --archive <tar>`로 설치합니다. clone,
tar, 설치기는 root 전용이어야 하며 설치기는 root 전용이 아닌 tar와 prefix 상위
경로를 거부합니다. 설치기는 pax 머리글의 커밋 ID로
`/opt/hermes-publisher/releases/<commit>`을 만들고, 명시된 Publisher 모듈 목록과
키 저장소·`requirements.lock`만 꺼내며(생산자 쪽 모듈은 설치하지 않음), lock을
`--require-hashes --only-binary :all:`로 새 venv에 설치하고 pip를 제거합니다. 같은
커밋을 다시 설치하지 않으며 되돌리기는 실행기를 이전 release로 바꾸는 것입니다.
실행 계정 검증은 `<release>/venv/bin/python -I -m publisher.cli verify-install`이
`{"keys": N, "runtime": "protected"}`를 내는지로 확인합니다.

Gateway 수신 인증 파일도 그 전용 계정만 읽을 수 있어야 하며, Hermes
계정이 읽을 수 있으면 Webhook을 직접 호출해 생산자 인증을 우회할 수 있습니다.
Companion 디렉터리는 생산자 계정만 쓸 수 있어야 합니다.
먼저 고정된 증거·서명이 이기므로 다른 계정이 먼저 쓰면 그 실행은 영구히 막힙니다.
키 만료는 사용 시점에 확인하므로 미전송 기록은 `not_after` 전에 비워야 합니다.
이 변경 전에 서명 없이 저장된 증거는 서명을 덧붙이거나 덮어쓸 수 없어 계속
막히며, 복구는 새 실행으로 다시 만드는 것입니다.

### 생산자 계약 버전과 이관

항목 필드 집합이 바뀌면 `schema_version`을 올립니다. Publisher는 고정 검증기의
필드 집합만 받으며 같은 1.0.0이라도 필드가 다른 후보를 호환으로 보지 않습니다.
변경 전 1.0.0 후보는 원본·후보 파일 그대로 보존하고 대기함에 넣지 않습니다.
필요하면 Hermes가 원본에서 새 버전으로 다시 내보내며, 대기함에 없던 실행이므로
기존 기록과 충돌하지 않습니다. Hermes의 저장 전 검증기는 main 검증기
`957d047c…`와 같은 판정을 내야 합니다.

### 진입 경로와 시간 제한

Publisher(서버 A 호스트 Python)는 A의 n8n Webhook으로, n8n Worker(Node)는 B의
Gateway로 각각 따로 연결합니다. 두 구간의 인증서 신뢰와 Token 범위는 다르며 A
호스트의 성공을 Worker 성공으로 대신하지 않습니다.

- A 진입: 기존 `n8n` 라우터의 SSO는 유지합니다. 실제 경로가 확정되면 정확한
  Webhook 경로·POST·A 내부 출발지만 허용하는 별도 라우터를 추가하고 n8n
  `headerAuth`로 인증합니다. `/webhook/*` 전체를 열지 않습니다. 이 라우터는
  아직 추가하지 않았습니다.
- B 진입: Worker는 `https://blog-ingest.hy.home.arpa/v1/ingestions`에 POST만
  보냅니다. Token은 수집 전용이며 A에는 GET·조회 권한을 두지 않습니다. 응답이
  유실되면 Publisher가 `--allow-replay`로 같은 요청 바이트와 멱등 키를 명시적으로
  다시 POST해 대조합니다. 조회용 MCP는 별도 경로·Token의 후속 작업입니다.
- 이름 해석: 이 이름은 Worker 컨테이너 안에서 `192.168.0.22`로 해석되어야
  합니다. 호스트 `/etc/hosts`는 컨테이너에 자동 전달되지 않으므로 내부 DNS 기록
  또는 Worker의 `extra_hosts`가 필요하며, 둘 다 Compose·DNS 변경 승인 대상이라
  적용하지 않았습니다. Worker가 B의 CA를 신뢰하는지도 Worker 안에서 따로
  확인합니다.
- B(Windows 11 + WSL2 NAT): Windows 쪽 443 수신, WSL 전달, 방화벽의 출발지
  `192.168.0.13` 제한이 정본이며 Gateway는 WSL loopback 8787을 유지합니다. 기존
  Windows Vault는 이전하지 않습니다.
- 시간 제한: Gateway 요청 20초 < 흐름 `executionTimeout` 30초(Worker가 실행을
  시작한 뒤부터) < Publisher 시도 45초(Queue 대기 포함 전체)입니다. Traefik v3
  기본 `readTimeout` 60초는 요청 본문을 읽는 시간만 제한하고 상류 응답 대기
  제한은 설정되어 있지 않으므로, Publisher 45초가 한 시도의 바깥 한계입니다.
  Queue 대기가 15초 여유를 넘기면 `uncertain`으로 남기고 같은 요청으로
  대조합니다. 흐름에는 재시도와 예약 실행을 두지 않습니다.
- `uncertain`, 영구 거부(401·403·409 등), 재시도 소진은 성공이 아니며
  `dispatch` 종료 코드 1입니다. 출력의 `reasons`는 거부 이유 코드별 개수만 담고
  원문·Token·키를 담지 않습니다.

### Blog-data Gateway 계약 비교

고정본은 Blog-data `dev` `a6d0957`의 1.0.0, 비교 대상은 2026-10-31 `dev`
`1a4cd60`의 1.1.0입니다.

| 파일·범위 | 비교 결과 | Publisher 영향 |
| --- | --- | --- |
| `ingestion-v1.schema.json` | 바이트 동일 | 없음 |
| `synthetic-report.json` | 바이트 동일 | 없음 |
| `POST /v1/ingestions` 요청·200·201·오류 응답 | 정의 동일 | 없음, 고정 개정 유지 |
| `receipt`, `error`, `summary`, `capture` 정의 | 동일 | 없음 |
| `candidates` 정의 | 항목에 `matching`, `review_count`, `latest_review` 추가 | 후속 조회 도구만 해당 |
| `review`, `reviewReceipt`, `reviews`, `/v1/candidates/{id}/reviews` | 추가 | 후속 조회 도구만 해당 |

수신 경로는 호환되므로 고정 개정·Fixture와 기존 대기함의 계약·본문·목적지를
바꾸지 않습니다. 후속 조회 도구가 새 응답을 쓰게 될 때 별도 승인으로 조회용
계약 참조를 추가합니다. 현재 조회 API에는 전문 검색 매개변수가 없고
`date`, `kind`, `status`, `review_status`, `limit`, `after` 필터만 있습니다.

## Configuration

추후 컨테이너 방식은 기존 네트워크·추가 구성 검토 후 `n8n_net` 재사용을
우선합니다. 관측된 해당 네트워크는 외부 네트워크이며 내부 전용 설정이 아니므로
접근 격리를 보장한다고 해석하지 않습니다. 승인된 내보내기·보고서·아이디어만
읽기 전용으로, 전용 대기함만 쓰기 가능하게 연결하고 비관리자 계정·읽기 전용
루트·권한 제거·추가 권한 금지를 적용하는 설계입니다. 홈 전체·브라우저·비밀
디렉터리·도커 소켓이나 새 공개 포트는 필요하지 않습니다. 현재 구성 변경은 없습니다.

## Verification

합성 전송기는 실제 연결 없이 중단·재시도·응답 유실과 대조 상태를 확인합니다.
전송 중 중단은 미확정으로 복구하고, 일치하는 영속 저장 증거 없이 배달 완료로
바꾸지 않습니다. 인증·인증서·시간 초과의 합성 분류는 실제 통신 시험과 구분합니다.

`dispatch` 출력은 결과별 개수와 거부 이유 코드별 개수를 담습니다. 이를 기존
관측 체계에 연결하는 일과 가장 오래된 대기 시간 지표는 설계만 있습니다. 보고서 식별자·제목·본문·비밀값을
지표 표지로 사용하지 않습니다. 알림 기준은 운영 주기 확인과 승인 후 정합니다.
조회 전용 후속 도구는 안정적인 HTTP 전송 후 별도 설계로 진행합니다.

서명되지 않았거나 승인 키가 아닌 증거는 검증 자료일 뿐 전송 권한이 아닙니다.
승인 키로 서명된 Companion이 모든 항목의 실제 수집 시각을 결속하기 전에는
발행기 전송이나 재전송을 시작할 수 없습니다.

## Hermes host → n8n 직접 전송과 Windows Blog-data 인계 (2026-10-31)

> **현황:** 이 절은 최신 요구사항에 대한 아키텍처 결정 후보·실행 프롬프트다. 서버 A/B 실연결, 새로운 Hermes 플러그인, n8n 활성화, Windows 게시, 실제 Secret 사용과 E2E 검증은 모두 **NOT_RUN**. 기존 Publisher, Gateway v1 및 테스트의 완료·차단 증거는 그대로 유지한다.

### 실운영 토폴로지와 비교 근거

- **A = Ubuntu 192.168.0.13:** Hermes Agent는 **Docker 밖의 호스트 프로세스**. n8n·Valkey·Traefik·OpenBao 및 다른 hy-home 서비스는 Docker. Hermes가 같은 서버에 있다는 사실은 n8n container network에 자동 접속한다는 뜻이 아니다.
- **B = Windows 192.168.0.22:** 실제 Blog-data Git checkout과 Obsidian Vault가 있다. Obsidian은 열려 있지 않아도 노트 파일이 생성되어야 한다. Windows에 새 프로그램/WSL/Docker/수신 서비스 설치 및 Vault 이전을 하지 않는다.
- **최우선 직접 전송:** Hermes Cron의 결과 → Hermes 사용자 Plugin의 제한된 `submit_research_report` 도구 → **host-to-n8n HTTP POST**(기존 인증 Webhook, 개별 허용 경로) → 기존 n8n Gateway 전달 → 서버 A에 **Blog-data 소유 Gateway v1/SQLite** → Resource Export 준비 → B의 Windows 내장 PowerShell/Task Scheduler HTTPS Pull → 로컬 Vault 게시 및 A ACK.
- **복구 경로:** 기존 file-based no-agent exporter `84d3f689378b` / Publisher `stage`와 SQLite Outbox는 직행 전환을 검증할 때까지 유지한다. 직접 경로에도 durable Outbox가 필요하면 **현재 Publisher Outbox API를 재사용**하고 stdin/구조화 인메모리 입력을 추가한다. SQLite 저장은 데이터 전송용 파일 투입·폴링과 다르다. Cron 중복 등록이나 평행 Outbox/DB는 만들지 않는다.
- **Hermes 공식 기능:** Hermes Plugin은 `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)`를 지원한다. 일반 `hooks.outbound`는 agent lifecycle **best-effort fire-and-forget** 이벤트, 응답 무시·실패 시 drop 가능이므로 **뉴스 본문 및 영속 receipt 전달의 정본으로 금지**한다. Hermes의 inbound webhook은 반대 방향이다.
- **A→B 선택:** HTTPS **B Pull**은 A에 Vault 쓰기 권한을 주지 않고 Windows의 기존 NTFS에 게시한다. Windows 내장 스케줄러만 사용한다. `A→B SMB` 직접 쓰기도 비교: B 측 작업이 없지만 A에 Resource 경로 쓰기 권한이 필요하고 CIFS/SMB rename-no-replace/fsync 및 경로 공격을 실제 테스트해야 하므로 기본 경로에서 배제한다. GitHub PR로 뉴스/아이디어를 운반하지 않는다.

### 현존 소스 상태 및 차단 조건

1. `workflow.json`은 `active:false`이고 `headerAuth` Webhook과 Gateway relay/200·201 persisted 검사까지 **이미 작성**되어 있다. Webhook 경로는 `hermes-blog-ingestion-contract-hold`이며 현재 Gateway URL은 `https://gateway.invalid/v1/ingestions`이다. 운영 목적지·credential·방화벽·외부 Runner 네이티브 동작은 아직 연결되지 않았다. **새 동등 워크플로를 중복 생성하지 않고 기존 것을 개정한다.**
2. 기존 `publisher/gateway_adapter.py`는 Blog-data v1의 고정 계약을 구현하지만 authoritative `scheduled_at`, `collected_at`의 근거를 자동 생성하지 않는다. 현재 후보의 `collection_evidence` 텍스트는 fetch 증거가 아니다. `hermes-companion-evidence/1` + Ed25519 서명 및 제한 signer/key registry가 미충족이면 `blocked`를 유지한다.
3. **기존 신뢰 정책을 직접 전송 때문에 우회하지 않는다.** 직접 수집의 출처 응답·실제 시간·내용 SHA와 별도 보호 서명 또는 동등하게 검증되는 **정식 새 계약/ADR/테스트**가 있어야 자동 수집·전송 승인 가능하다. 새 신뢰 경계가 정식 승인될 때까지 구조화 webhook에 도착한 자료는 격리/준비만 허용하고 Resource 공개·Capture는 금지한다.
4. 수신 `200/201 persisted:true`는 A Gateway SQLite 수신 성공이지 B 로컬 노트 게시 성공이 아니다. B 완료는 별도 export_id/document SHA를 바인딩한 확인(ACK)으로만 기록한다. n8n 자체 queue/Valkey는 원본 보존 대체가 아니다.

### Hermes Agent에 실제로 전달할 구현 프롬프트 (무엇·어떻게·왜)

**무엇:** Ubuntu **호스트**에서 실행 중인 Hermes Agent에 공식 플러그인 인터페이스로 `submit_research_report` 도구를 추가한다. 이미 등록된 `6eabd835f969`(전략 뉴스), `25674fbc0bf3`(DevOps), `8d0925bc571d`(사업 아이디어) Cron의 스케줄·이메일 결과는 유지하고, 동일 실행의 구조화 결과를 **별도 파일 투입 없이** 기존 n8n 인증 Webhook으로 전달한다. 비공개 `3c3f81a925e0`(인프라 보고)는 범위 제외다.

**어떻게 1 — 현황 확인:** Hermes CLI 버전, `hermes cron list`/`hermes cron runs`/`hermes hooks list`/`hermes tools`와 기존 Job 원본·툴셋·실행 상태를 읽기 전용 확인한다. 실제 명령의 --help/현재 설치 코드에서 명령 지원을 검증한다. Cron job IDs, cadence, 성공 메일 주소, no-agent exporter `84d3f689378b`, Publisher 보호설치를 정확히 기록하고 먼저 **NO_CHANGE / MODIFY / RETIRE**로 분류한다. 기존 `jobs.json`을 직접 패치하지 않고 `cronjob_manage` 또는 현행 CLI로만 Cron을 변경한다.

**어떻게 2 — Plugin:** Hermes 공식 `~/.hermes/plugins/<name>/{plugin.yaml,__init__.py,schemas.py,tools.py}` 계약과 현재 설치 버전의 `register_tool` API를 확인한다. `submit_research_report`는 `job_id`, `run_id/fire_id`, `report_kind`, `items`, `source_text`, authoritative timestamp/evidence, canonical hash/idempotency key만 허용한다. 서버 대상/인증/임의 파일 경로를 Agent 인자로 허용하지 않는다. 세 작업 allowlist, 크기(1 MiB/100 item), 중복 키, 비밀/PII/내부 경로, HTTPS/TLS/redirect 금지, event identity, JSON schema를 **툴 핸들러에서** 검증한다. Agent의 자연어 프롬프트는 보안 권한의 정본이 아니다.

**어떻게 3 — Provenance:** Hermes 웹 조사에서 직접 취득한 응답은 HTTP final URL, 실제 fetched_at, 2xx 상태, response-body SHA-256, cache/tool-call ID를 제한된 획득 컴포넌트가 기록해야 한다. 모델 생성 문자열로 receipt를 채우지 않는다. 기존 `hermes-companion-evidence/1` 및 제한된 **별도** Ed25519 signer의 서명·키 수명 조건을 만족하거나 새 직접 경로 신뢰 계약을 승인받는다. 미충족·증거 누락·원천 미확인은 reject/quarantine으로 명확히 구분한다. 이미 보호된 Publisher 키와 제한 계정 정책을 낮추지 않는다.

**어떻게 4 — 전송:** 전용 도구는 고정 n8n Webhook endpoint만 사용하며 `headerAuth`/허용된 인증 방식의 비밀은 보호된 **호스트 Secret** 저장소에서 핸들러만 읽는다(도구 인자, Agent 메시지, stderr/stdout, Git, test fixture에 없음). 정상 요청은 job/run/idempotency/source hash 바이트를 고정하고 n8n이 Gateway의 `200/201 persisted:true`를 반환할 때만 `ingestion_received`를 기록한다. 503/타임아웃은 동일 바이트로 bounded retry와 기존 Outbox reconciliation; 401/403/409/422는 재시도 금지·운영자 점검. 응답 분실, unknown 결과, 재실행은 같은 key로 대조하고 원문·메일의 완료와 독립 상태를 유지한다.

**어떻게 5 — Cron prompt 수정:** 기존 뉴스·아이디어 생성 조건과 이메일 전문은 그대로 유지하고, 검증된 `submit_research_report` 호출을 별도 단계로 수행하도록 세 job의 프롬프트만 **최소 변경**한다. 도구 오류·증거 거부·201 미확인 시 외관상 성공 메시지를 쓰지 말고 Cron 실패/partial 상태를 명시한다. 장애로 report가 사라지지 않는지 기존 `~/.hermes/cron/output`(Hermes 기본 실행 결과 저장소)와 durable Outbox를 통해 복구 시험한다. 플러그인 자체는 호스트 설치물이며 Docker 컨테이너나 Windows에 배포하지 않는다.

**어떻게 6 — 검증/완료:** 기존 세 Cron 각각 합성 POST를 실 n8n이 아닌 로컬 fake webhook으로 검증하고, 잘못된 job, signer/key, URL, fabricated timestamp, 부분 수집, PII, 401, 409, timeout, 503, restart, receipt 분실, 동일 key replay, 이메일 성공/저장 실패, 7일 B 오프라인을 포함한다. n8n 실연동, 비밀 설치·회전, Cron 등록/수정은 운영 환경의 별도 승인과 되돌리기 계획 없이는 실행하지 않는다. 실행 전/후 Job ID·설정 diff·테스트 exit·실제 PASS/BLOCKED/NOT_RUN을 보고한다.

**왜:** Hermes→n8n 전달을 불필요한 파일 polling에 의존하지 않고 직접 연결하되, 출처 신뢰·서명·정확한 수신 확인·재처리 가능성을 희생하지 않기 위해서다.

**Skills:** 가능할 때 Superpowers Using Superpowers → Brainstorming → Executing Plans(작업 분할) → Subagent Driven Development(파일 소유 분리) → Finishing A Development Branch(검증/커밋) 순서로 실행하되, 현재 저장소의 승인과 Spec/Task 규칙을 우선한다.

### hy-home.docker에 전달할 구현 프롬프트 (무엇·어떻게·왜)

**무엇:** 기존 `workflow.json`, 제한 Publisher/SQLite Outbox, n8n/Valkey, Traefik, OpenBao 및 모니터링 서비스에 **Hermes 호스트 → n8n 직접 POST**를 추가하고, A에서 Blog-data Gateway v1/Export API를 호스팅하는 운영 경로를 만든다.

**어떻게:**
1. `main` 최신 HEAD와 `SPEC-0204-TSK-0022`, `SPEC-0247`/현행 검증기, n8n `workflow.json`, delivery/adapter/transport, 기존 회귀, Blog-data API/fixture의 정확한 커밋을 확인한다. 완료 기능은 `NO_CHANGE`로 표시하고 **재구현하지 않는다**. Hermes가 Docker가 아님을 Compose/Network 문서와 테스트에 반영한다.
2. **기존 Webhook 단일화:** `hermes-blog-ingestion-contract-hold` 기존 워크플로를 소유 Task에서 개정하여 실제 계약 확정 전 `active:false`를 유지한다. Hermes 호스트가 접근하는 **별도 제한된 ingress**(기존 Traefik의 정확한 Webhook path 전용 ACL/TLS)만 추가한다. n8n 관리 UI와 다른 웹훅을 익명 노출하지 않는다. 전면 `sso-auth`를 우회하는 광범위 라우팅도 금지한다. n8n Webhook의 Header Auth/제한 URL/요청 크기·rate limit과 Gateway ingest credential은 서로 다른 Secret이다.
3. **기존 Gateway 재사용:** Blog-data 소유 `scripts/lib/ingestion/**`를 검토된 소스·이미지 digest로 서버 **A의 별도 격리된 Linux 컨테이너**에서 호스팅한다. Blog-data Git/Vault 전체를 컨테이너에 마운트하지 않는다. `.github/docker/ingestion.compose.yaml`은 원래 B 준비 예제이므로 A로 옮기는 계약/Compose는 Blog-data 소유자와 협의하고 신규 저장소를 복제하지 않는다.
4. **동일 계약 유지:** Hermes 플러그인에서 이미 `ingestion-v1.schema.json`을 만족한 report가 들어오면 n8n은 검증→Gateway 전달→receipt 반환만 담당한다. n8n의 계산으로 `scheduled_at`/`collected_at`를 만들어 넣거나 item/source 순서를 바꾸지 않는다. 초과 payload/unknown field/신뢰 위반/민감자료를 거부 또는 명확히 격리한다. 수신 `persisted:true`와 B 게시 ACK는 독립이다.
5. **Resource 전달:** Blog-data 소유 신규 versioned Resource export API에 대해 Traefik B 전용 HTTPS read/ack 접근을 구성한다. Windows B에는 Docker·WSL·별도 프로그램을 설치하지 않는다. 기존 OpenBao/monitoring을 재사용한다. 단순 비동기 n8n 실행 성공을 `stored`로 표시하지 않는다. B 오프라인 동안 A DB와 export 패키지를 보존한다.
6. **검증:** n8n 비활성 fixture/native import, 제한 Webhook auth, host-to-container TCP/TLS/DNS 및 timeout, exact API fixture/duplicate 200/new 201, error 400/401/403/409/422/503, 재전송, Gateway restart, Valkey worker, Secret 미노출, certificate verification, host 방화벽, producer 재시작, 원격 B ack를 계층별 합성 검증한다. `workflow.json`의 날짜 검증은 KST offset 전날 UTC 날짜도 통과하는지 회귀로 점검한다. 기존 상태·보안 게이트를 약화시키지 않는다.
7. **문서/정리:** 기존 Spec/Task/README/RUN-0053, infra inventory, gateway/n8n 운영 문서, test fixture·script에서 Hermes Docker 가정, Linux B, 실제 배포 완료 오인, 파일 exporter 필수 가정, legacy/deprecated API/fixture를 검색한다. 정본·사용처를 확인하여 `UPDATE`/`RETIRE`하고 archive 완료 기록은 삭제/재서술하지 않는다. 코드 수정은 별도 Task와 검증된 PR로 한다.

**왜:** 이미 작성된 n8n→Gateway API·재전송 엔진을 활용하고, Hermes 호스트와 n8n 컨테이너 간 명확한 네트워크·인증 경계를 운영하기 위해서다.

**완료 조건:** Linux 호스트→n8n→A Gateway 201 persisted까지 합성 E2E, 장애 시 재전송, 이중 실행 안전성, Windows A→B 수신/ACK 연계, 템플릿/문서 품질 검사, rollback evidence가 모두 PASS인 경우에만 완료를 주장한다. 실제 운영 비밀·스케줄·포트·서비스 활성화는 별도 준비와 승인 이후에만 한다.

## Related Documents

- [워크로드 목록](../README.md)
- [작업 탐색](../../../../../docs/03.specs/README.md): `SPEC-0204-TSK-0022`가 정본입니다.
- [운영 절차 탐색](../../../../../docs/05.operations/runbooks/08-workflows-and-automation/README.md): `RUN-0053`의 소스 검증·복구 범위를 확인합니다.
