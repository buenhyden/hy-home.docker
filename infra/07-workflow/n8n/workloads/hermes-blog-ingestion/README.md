---
title: "Hermes 수집 전송 소스"
version: "0.3.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-01"
---

# Hermes 수집 전송 소스

## Overview

서버 A의 호스트 프로세스인 Hermes가 n8n Webhook에 직접 보고서를 제출하고, n8n
Worker가 같은 서버 A의 격리된 Blog-data 수집 Gateway에 전달하는 경로의 소스입니다.
파일 기반 로컬 발행기와 영속 대기함은 직접 경로가 운영 검증될 때까지 복구 경로로
보존합니다. Blog-data `dev` 커밋 `a6d0957ad380f179f73bdd2a60ff23792d53f7ae`의
수집 API 계약과 합성 Fixture를 고정했고, Gateway 이미지는 Resource Export가 들어간
Blog-data `dev` `b372de374ec589b1bec2ff8096ae2f7272461248`(attestation/2, schema 4, `resource-export/3+4b681da87f80`)에서 로컬 빌드합니다.
Blog-data `main`은 이미지·배포 기준으로 쓰지 않습니다. 영속 수신 뒤에는 별도 호스트
서명자가 Attestation을 제출하고, Windows B가 HTTPS로 Export를 가져가 ACK합니다.

| 구분 | 상태 | 확인 범위 |
| --- | --- | --- |
| 소스 | 부분 구현 | 로컬 대기함, 계약 어댑터, 선택적 동일 요청 재전송, 제한된 `dispatch`, Companion Evidence v1 구조 검증, Ed25519 생산자 서명 검증과 공통 신뢰 판정, 비활성 수집 흐름 |
| 생산자 인증 | BLOCKED | 서명 검증기는 합성 키로 검증했지만 추적 키 저장소가 비어 있고 실제 제한 생산자 계정·키가 없음 |
| 계약·흐름 합성 검증 | PASS | 고정 계약·Fixture와 합성 응답, 빈 VM의 입력 선별 |
| 실제 원본 변환·전송 | BLOCKED | 실제 기사 수집 시각의 신뢰할 수 있는 근거와 전송 실행 연결 부재 |
| 격리 n8n Queue 합성 검증 | PASS | 기본 게시 API·정적 Webhook 등록, Worker·외부 JS Runner, 가짜 Gateway 201·합성 영속 수신 |
| 직접 경로 일회용 E2E | PASS | 호스트 → Traefik 경로(합성 사본) → n8n(추적 워크플로) → 실제 Gateway 이미지 → SQLite, [시험](tests/README.md) |
| Attestation·Export·ACK 일회용 E2E | PASS | 합성 서명 → `ready` Export → Manifest·파일 해시 → ACK, `held`·위조·범위 거부, 재시작 영속 |
| Schema 4 업그레이드·백업 복원 | PASS | 이전 고정본 저장소의 제자리 업그레이드와 두 백업의 새 볼륨 복원(합성) |
| 항목 단위 Attester | 소스 PASS, 운영 NOT_RUN | `attest-queue`와 원본 확인 합성 시험·일회용 E2E는 통과했지만 `hermes-attester` 계정·키·Token·timer는 아직 만들지 않음 |
| Hermes 플러그인 소스 | PASS(소스), 운영 NOT_RUN | PR #700으로 `hermes-plugin/`에 추적, 설치본 `~/.hermes/plugins/research-report` 네 파일과 SHA-256 일치(2026-11-01). 실제 제출은 미실행 |
| 실제 Windows 수신기 | NOT_RUN | 서버 B의 수신기 Dry Run·ACK 미실행 |
| 서버 A 운영 배치 | 부분 적용(2026-11-01), 새 고정본 NOT_RUN | 실행 중 Gateway `a43d824…`(이미지 ID `sha256:e513b938…`) 기동, Worker 내부망 연결, n8n 자격 증명·흐름 게시, Webhook·Export Traefik 경로 적용. `export` 설정이 없어 Export는 닫힘 |
| 실제 운영 검증 | NOT_RUN | Hermes `RESEARCH_WEBHOOK_URL` 연결, 실제 Cron 제출·`received`, Windows 수신기 미실행 |

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

- [workflow.json](workflow.json): 인증 수신, 입력 선별, 내부 Gateway 전달과 영속 수신 응답 확인을 담은 비활성 흐름입니다.
- [hermes-webhook.yml](../../../../01-gateway/traefik/dynamic/hermes-webhook.yml): Hermes Webhook 정확한 경로 하나만 SSO 없이 허용하는 Traefik 경로입니다. 2026-11-01 운영 디렉터리에 적용했습니다.
- [blog-export.yml](../../../../01-gateway/traefik/dynamic/blog-export.yml): Windows B의 Export 조회·ACK와 서버 A 호스트의 Attestation 세 요청 형태만 허용하는 Traefik 경로입니다. 2026-11-01 운영 디렉터리에 적용했습니다.
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
Webhook 경로는 `hermes-blog-ingestion`, 대상은 내부 격리망의
`http://blog-ingestion:8787/v1/ingestions`로 고정했습니다. 이전 경로
`hermes-blog-ingestion-contract-hold`와 `gateway.invalid`는 실수로 쓰이지 않게 막는
예약값이었고, 지금은 비활성 상태와 연결되지 않은 인증 참조가 같은 역할을 합니다.
운영 n8n에 가져오기·게시하는 일은 승인된 절차로만 수행합니다.

격리 시험에서는 고정된 `webhookId`를 가진 합성 흐름을 게시해 Webhook을 등록한 뒤,
추적된 흐름의 정확한 경로를 native helper로 확인하고, Worker와 외부 JavaScript
Runner를 거쳐 가짜 Gateway의 `201`·합성 영속 수신을 확인했습니다. 이는 추적된
흐름의 운영 요청이나 운영 Gateway 요청이 아닙니다. 실제 주소, 인증, TLS, 재시도·복구와
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

### 직접 제출 경로와 시간 제한

Hermes 플러그인 `submit_research_report`(Hermes 소유)와 복구용 Publisher
`dispatch`는 같은 Webhook에 제출합니다. 두 구간의 인증은 서로 다르며, A 호스트의
요청 성공을 Worker나 Gateway의 성공으로 대신하지 않습니다.

```text
Hermes(호스트) ─HTTPS─▶ Traefik 정확한 경로 ─▶ n8n ─Queue─▶ n8n-worker
   ─HTTP(n8n_blog_ingest_net)─▶ blog-ingestion ─▶ SQLite(로컬 디스크)
```

- 진입: 기존 `n8n` 라우터와 SSO는 그대로 둡니다. [운영 경로](../../../../01-gateway/traefik/dynamic/hermes-webhook.yml)는
  `Host` + 정확한 `Path(/webhook/hermes-blog-ingestion)` + `POST`만 일치시키고,
  출발지 `192.168.0.13/32`, 본문 1 MiB, 분당 6회로 제한합니다. 운영 Traefik 접근
  기록에서 호스트 프로세스가 `192.168.0.13:443`으로 보낸 요청은 `192.168.0.13`으로
  보였고 LAN 클라이언트는 자기 주소를 유지합니다. 이 값은 A의 모든 호스트 프로세스를
  뜻하며, `edge_net` 컨테이너는 n8n 컨테이너에 직접 닿을 수 있으므로 실제 인증
  경계는 출발지 제한이 아니라 n8n `headerAuth`입니다. 같은
  경로의 GET, 다른 Webhook 경로, n8n 화면은 SSO 라우터로, LAN 출발지는 403으로
  남습니다. `/webhook/*` 전체를 열지 않습니다. 운영 `dynamic/` 반영은 승인 단위입니다.
- 인증 분리: Hermes→n8n은 Webhook `headerAuth`(헤더 `X-Hermes-Ingest-Token`),
  n8n→Gateway는 `Authorization: Bearer`의 수집 전용 Token입니다. 둘은 별도 n8n
  자격 증명이며 Gateway 설정에는 SHA-256 다이제스트만 둡니다. Windows 조회·ACK는
  `export_read`·`export_ack`, 서명자는 `attest`, 운영자 Review는 `review` 범위로 각각 따로 발급합니다.
- Gateway: `blog-ingestion` 프로필, 이미지 `hy-home/blog-ingestion:<Blog-data 커밋>`,
  pull 금지, 읽기 전용 루트, UID 10001, 권한 제거, 공개 포트 없음입니다.
  `n8n_blog_ingest_net`(내부·격리 게이트웨이, `10.250.20.0/24`)에는 `n8n-worker`와
  Gateway만 있어 호스트와 다른 컨테이너가 닿지 못합니다. 같은 망의 평문 HTTP는 이
  격리를 전제로 합니다. capture 설정이 없어 A에서는 Vault 쓰기가 꺼져 있습니다.
- 신뢰: 직접 경로에서 생산자를 증명하는 것은 Webhook Token뿐입니다. Publisher의
  Ed25519 Companion 검증을 대신하지 않으므로 직접 제출분은 Gateway의 `received`와
  Review 대기까지만 갑니다. Publisher도 같은 Webhook·Gateway 자격 증명을 쓰므로
  Gateway는 서명 검증을 거친 Publisher 제출과 직접 제출을 구별하지 못합니다. 따라서
  직접 경로가 켜지면 Publisher의 Ed25519 보장은 Gateway에서 효력이 없고, Webhook
  Token이 LLM 에이전트인 Hermes 프로세스 안에서 읽히며, Token 회전이 두 경로를 함께
  멈춥니다. 서명 결속을 직접 경로에 싣는 계약, 또는 Publisher 전용 경로·자격 증명은
  Blog-data·Hermes와 버전을 맞춰 먼저 정해야 하며 아직 없습니다.
- 시간 제한: Gateway 요청 20초 < 흐름 `executionTimeout` 30초(Worker가 실행을
  시작한 뒤부터) < 제출자 시도 45초(Queue 대기 포함)입니다. Traefik v3 기본
  `readTimeout` 60초는 요청 본문 읽기만 제한하고 상류 응답 대기 제한은 없습니다.
- 재시도: 제출자(플러그인 또는 Publisher)만 소유합니다. 네트워크 오류·시간 초과와
  429·500(Gateway 미도달 시 n8n 응답)·502·503·504는 같은 바이트와 멱등 키로 제한
  재시도합니다. 저장 뒤 재전송은 200 중복이 되므로 안전합니다. 400·401·403·409·413·
  422는 다시 보내지 않습니다. 404는 흐름이 게시되지 않은 상태이며 Publisher는 이를
  영구 거부로 처리하므로, 흐름 게시를 해제하기 전에 Publisher 실행기를 먼저 멈춥니다. 흐름에는 재시도와 예약 실행을 두지 않습니다. `uncertain`, 영구
  거부, 재시도 소진은 성공이 아니며 `dispatch` 종료 코드 1입니다.

### 상태 대응과 관측

새 상태 체계를 만들지 않고 기존 정본에 대응합니다. A의 Gateway 수신은 Windows
저장 완료로 승격하지 않습니다.

| 요청 상태 | 기존 정본 | 확인 위치 |
| --- | --- | --- |
| `produced` | Hermes Cron 실행 결과 | Hermes `~/.hermes/cron/output`(Hermes 소유) |
| `queued` | Publisher `awaiting_contract`·`pending` | `publisher.cli status` |
| `ingested` | Gateway 영수증 `persisted:true`, `status:"received"`(201·200) | n8n 응답, Gateway `/v1/ingestions/{id}` |
| `export_prepared` | Attestation 뒤 Gateway Export `ready` | `GET /v1/exports?state=ready`(`export_read`) |
| `delivered_acknowledged` | Gateway Export `acknowledged`(ACK 201·200) | `GET /v1/exports/{id}`의 `ack_id`·`updated_at` |
| `retryable` | Publisher `pending`(다음 시도 예약)·`uncertain` | `publisher.cli status` |
| `quarantined` | Publisher `blocked`(신뢰 실패), 서명자 `rejected`·건너뜀, Gateway 격리 판정, Export `held`(`hold_reason`) | `status`, `attest-queue` 출력, Gateway Review, `GET /v1/exports?state=held` |
| `conflict` | Publisher `conflict`, Gateway 409 `IDEMPOTENCY_CONFLICT`, Export `conflict`(ACK 409) | `status`, n8n 응답, `GET /v1/exports?state=conflict` |

관측은 기존 체계를 씁니다. n8n 지표(`n8n-monitor`)의 흐름별 실행 성공·실패,
Traefik 라우터 지표(`addRoutersLabels`)의 `hermes-blog-ingestion-webhook` 상태 코드
(401·403·413·429·5xx), 컨테이너·디스크 지표, Gateway `/v1/summary`(`read` 범위)의
일자별 보고서 수와 종류·상태·중복별 후보 수, Publisher `status`의 대기 수입니다.
작업별 최종 수신 시각은 summary에 없어 Gateway 조회 API 확장이 필요합니다. Export
상태는 `export_read` 목록 조회로 셉니다. `state`별 `ready`·`held`·`conflict` 수와
가장 오래된 `ready`의 `created_at`이 미수신 시간이고, `acknowledged` 항목의
`updated_at`이 마지막 ACK 시각입니다. 서명 실패는 `attest-queue` 종료 코드와 Traefik
`blog-attestation` 422, 반복 429·5xx는 `blog-export-*` 라우터 지표로 봅니다.
Gateway에는 지표 엔드포인트가 없으므로 Prometheus 수집은 Blog-data와 지표 계약을
정한 뒤 붙입니다(DEFER). 경보 기준은 운영 주기 확인 후 승인으로 정합니다.

### Attestation과 Resource Export

Gateway는 `POST /v1/ingestions/{id}/attestations`의 Ed25519 서명이 저장된 보고서와
맞을 때만 후보마다 Export를 만듭니다. 서명 대상은 `blog-data-attestation/1`, NUL,
`{producer, job_id, run_id, fire_id, source_sha256, content_sha256}` 정규 JSON이며
`content_sha256`은 멱등 키를 뺀 요청 전체의 정규 JSON SHA-256입니다. 이 서명은 Hermes
Companion 서명과 다른 계약·다른 키입니다.

서명자는 `python3 -I -m publisher.cli attest-queue`이며 Hermes·n8n·Publisher와 다른
전용 계정 `hermes-attester`로 실행합니다. Gateway의 `GET /v1/attestation-queue`에서
미서명 보고서를 읽고 `GET /v1/ingestions/{id}/request`의 정규 요청 바이트를 받아
항목마다 원본을 확인한 뒤, 확인된 항목만 `attestation/2`로 서명해 보냅니다.
서명 대상은 요청 `content_sha256`과 확인된 항목, 증거 해시입니다. 개인키는 그 계정
또는 root 소유 PEM으로 기타 권한이 없어야 하며 그룹 읽기는 서명 계정의 기본 그룹일
때만 허용됩니다. 키는 n8n, Webhook 처리기, Publisher 계정, 저장소에 두지 않습니다.
`192.168.0.13/32` 허용은 서버 A의 모든 호스트 프로세스를 통과시키므로 실제 경계는
`attest`+`read` Token입니다. 조회 경로 `blog-attestation-read`는 위 두 GET만 연결합니다.

```bash
python3 -I -m publisher.cli attest-queue \
  --gateway https://blog-export.hy.home.arpa \
  --auth-header-file <private attest header> --signing-key <private PEM> --key-id <key_id> \
  --state-dir <state> --evidence-dir <evidence>
```

출력은 `attested`·`held_items`·`skipped`·`retry`·`rejected` 개수 한 줄이며
`rejected`가 있으면 종료 코드 1입니다. 보고서·항목 본문과 URL, 자격 증명은 출력하지 않습니다.

#### 항목 단위 Attester

- 원본 가져오기는 SSRF 방어를 거칩니다. https만, 사용자 정보와 홈 영역 이름 금지,
  해석된 주소가 모두 전역 라우팅 가능해야 하며 검증한 IP로만 연결합니다. 크기 2 MiB,
  리다이렉트 5회, 전체 20초로 제한하고 끌 수 있는 스위치는 없습니다.
- 검사는 필수 필드, `source_quotes` 1~3개(정규화 후 20자 이상)가 페이지 본문에 있는지,
  제목·본문의 숫자와 고유명이 원본에 있는지입니다. 하나라도 실패한 항목은 `held`
  (`SOURCE_UNVERIFIED`)이며 승인되지 않은 작업은 항목 전부가 보류됩니다.
- 일시 실패(통신·5xx 등)는 최초 시도 후 6시간까지 다음 실행에서 재시도하고 그 뒤
  미확인으로 확정합니다. 서명한 본문은 전송 전에 저장하므로 응답을 잃어도 같은
  바이트를 다시 보내며 Gateway는 200 중복으로 응답합니다. 격리된 보고서(409
  `REPORT_QUARANTINED`)는 건너뜁니다.
- 증거(항목별 결과·코드·응답 SHA-256·확인 시각)는 보고서마다 `--evidence-dir`에,
  진행 상태는 `--state-dir`에 0600 파일로 둡니다.
- 실행 단위는 `deploy/hermes-attester.service`(oneshot)와 `.timer`입니다. 비밀은
  `/etc/hermes-attester/`에 두며 런타임 Python은 HTMLParser 보완이 반영된 최신 패치
  판본이어야 합니다(RUN-0053 기록).

Windows B와 서버 A 호스트는 `blog-export.hy.home.arpa`의 정확한 경로만 씁니다.
Gateway는 `n8n_blog_ingest_net`(n8n-worker)과 `blog_export_net`(Traefik)에만 연결되고
포트를 공개하지 않습니다. 서버 B 인계 계약은 다음과 같습니다.

| 항목 | 값 |
| --- | --- |
| HTTPS 기준 주소 | `https://blog-export.hy.home.arpa`(서버 A `192.168.0.13:443`, `*.hy.home.arpa` SAN) |
| CA 공개 인증서 | 서버 A의 mkcert 루트 `rootCA.pem` 공개 인증서. 수신기 설정의 CA 파일로 고정하며 지문은 적용 단계에서 운영자가 기록 |
| 출발지 | Export 조회·ACK는 `192.168.0.22/32`, Attestation은 `192.168.0.13/32` |
| 인증 | `export_read`, `export_ack` 각각 별도 Bearer 토큰(Gateway에는 SHA-256만 저장) |
| API·수신기 | Blog-data Resource Export 1.0과 `scripts/ops/receive-hermes-exports.ps1`, 둘 다 `dev` `b372de374ec589b1bec2ff8096ae2f7272461248` |
| 템플릿 버전 | 각 Manifest의 `template_version`(이미지에 포함된 Resource 템플릿·프로필 레지스트리, `resource-export/3+4b681da87f80`) |

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

Gateway는 [n8n Compose](../../docker-compose.yml)의 `blog-ingestion` 서비스입니다.
기존 프로필 선택에는 포함되지 않으며 `--profile blog-ingestion`과 로컬에 빌드된
고정 이미지가 있어야 시작합니다. `n8n-worker`는 기본 구성에서
`n8n_blog_ingest_net`에 붙으므로 다음 Worker 재생성 때 빈 내부망 하나가 추가됩니다.
호스트 경로 `${DEFAULT_WORKFLOW_DIR}/blog-ingestion/data`와 `config.json`은 미리
만들어야 하며 없으면 시작이 실패합니다. Hermes 홈, Vault, Blog-data 체크아웃,
Docker 소켓은 어느 컨테이너에도 연결하지 않습니다.

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

## Related Documents

- [워크로드 목록](../README.md)
- [작업 탐색](../../../../../docs/03.specs/README.md): `SPEC-0204-TSK-0022`가 정본입니다.
- [운영 절차 탐색](../../../../../docs/05.operations/runbooks/08-workflows-and-automation/README.md): `RUN-0053`의 소스 검증·복구 범위를 확인합니다.
