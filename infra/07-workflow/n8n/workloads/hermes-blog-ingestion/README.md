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
| 소스 | 부분 구현 | 로컬 대기함, 계약 어댑터, 선택적 동일 요청 재전송, 제한된 `dispatch`, Companion Evidence v1 구조 검증, 비활성 수집 흐름 |
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

## Usage

로컬 준비·상태 명령은 발행기 설명, 재현 가능한 시험 명령은 시험 설명을 봅니다.
배포 단위는 제한된 호스트 프로세스가 우선이며 서비스 설치나 예약 실행은
아직 구성하지 않았습니다. `dispatch` 명령은 있으나 세 작업의 차단 정책이 닫혀
있어 실제 인증 입력이나 네트워크 요청 없이 `blocked`를 반환합니다.

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
| `items[].body_sha256` | 실제 수신 바이트의 SHA-256 |
| `items[].cache` | `{hit:false,key_sha256:null}` 또는 `{hit:true,key_sha256:<64 hex>}` |

모든 시각은 `scheduled_at` 이후, 후보 `generated_at` 이전이어야 합니다. 캐시
적중은 캐시 생성 시각이 아니라 원래 직접 수집 시각을 기록하므로 실행 예정
시각보다 이를 수 있습니다. 보고서 `collected_at`은 항목 `fetched_at`의 최댓값이며
추정·대체하지 않습니다. 중복 키·알 수 없는 필드·형식 오류는 모두 거부합니다.

이 검증은 구조와 결속만 확인합니다. 누가 기록했는지는 증명하지 않으므로 다음
생산자 신뢰 조건이 별도로 승인되기 전에는 `policy.evidence_required`,
Outbox와 재전송 경계의 차단을 열지 않습니다.

1. 직접 수집 경계에서 응답 바이트를 사용하기 전에 기록을 원자적으로 영속화합니다.
   임시 파일·fsync·rename 순서로 수집과 기록 사이의 중단 공백을 없앱니다.
2. 기록을 만든 생산자를 Publisher가 검증할 수 있어야 하고, 같은 계정의 LLM
   도구·내보내기 단계가 위조할 수 없어야 합니다. 서명 방식과 키 보관 위치는
   Hermes 담당 작업이 제안하고 운영자가 승인합니다.
3. 파일명은 기존 `SHA256(job_id + NUL + run_id).json`을 유지하고 `stage
   --evidence-root`로 대기함에 함께 고정합니다.

위 조건과 그 검증 시험이 승인되면 차단 해제는 정책·Outbox·재전송 경계의 한
변경으로 검토합니다. 그 전에는 증거가 있어도 전송하지 않습니다.

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

성공·실패 횟수, 대기·미확정 수, 재시도 수, 가장 오래된 대기 시간을 기존
관측 체계에 연결하는 설계만 있습니다. 보고서 식별자·제목·본문·비밀값을
지표 표지로 사용하지 않습니다. 알림 기준은 운영 주기 확인과 승인 후 정합니다.
조회 전용 후속 도구는 안정적인 HTTP 전송 후 별도 설계로 진행합니다.

직접 수집 시각의 임시 증거와 Outbox 증거 스냅샷은 검증 자료일 뿐 전송 권한이
아닙니다. Hermes 생산자·구조화 후보·Publisher에 통합되어 모든 항목의 실제
수집 시각을 결속하기 전에는 발행기 실행이나 재전송을 시작할 수 없습니다.

## Related Documents

- [워크로드 목록](../README.md)
- [작업 탐색](../../../../../docs/03.specs/README.md): `SPEC-0204-TSK-0022`가 정본입니다.
- [운영 절차 탐색](../../../../../docs/05.operations/runbooks/08-workflows-and-automation/README.md): `RUN-0053`의 소스 검증·복구 범위를 확인합니다.
