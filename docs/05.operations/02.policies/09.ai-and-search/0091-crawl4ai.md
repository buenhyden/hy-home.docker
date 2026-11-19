---
title: "Crawl4AI Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0091"
parent_ids:
- "AD-0008"
created: "2026-09-21"
next_review_at: "2027-05-13"
---

# Crawl4AI Operations Policy

## Purpose and Scope

### Objective

Crawl4AI는 SSRF가 가능한 서비스다. 검토된 consumer가 필요로 할 때까지 격리하고
인증을 적용한 채 사용하지 않는 상태로 유지한다.

#### Authority

- [AI architecture](../../../02.architecture/01.descriptions/0008-ai-architecture.md)

- [Crawl4AI Compose source](../../../../infra/08-ai/crawl4ai/docker-compose.yml)

### Applies To

활성화, 네트워크 배치, 인증, consumer, provider key, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0091-R1 | 항상 | 필수: `crawl4ai` profile로만 선택한다 | none | none |
| POL-0091-R2 | 항상 | 금지: `ai`, `notebook`, HOME에 추가 | none | none |
| POL-0091-R3 | 항상 | 필수: internal인 `crawl4ai_net`과 `crawl4ai_egress_net`에만 연결한다 | none | none |
| POL-0091-R4 | 항상 | 필수: 밖으로 나가는 경로는 `crawl4ai-egress` 하나로 둔다 | `tests.validation.test_crawl4ai_egress` / 격리 리허설 `HYHOME_CRAWL4AI_REHEARSAL=1` | none |
| POL-0091-R5 | 항상 | 필수: gateway는 전역 라우팅되는 IPv4의 80·443만 허용한다 | `tests.validation.test_crawl4ai_egress` / 격리 리허설 `HYHOME_CRAWL4AI_REHEARSAL=1` | none |
| POL-0091-R6 | 항상 | 필수: gateway는 IPv6를 모두 거절한다 | none | none |
| POL-0091-R7 | 항상 | 필수: 확인한 주소로만 연결한다 | `tests.validation.test_crawl4ai_egress` / 격리 리허설 `HYHOME_CRAWL4AI_REHEARSAL=1` | none |
| POL-0091-R8 | 항상 | 금지: 공유 서비스 네트워크 연결 | none | none |
| POL-0091-R9 | 항상 | 금지: public route 추가 | none | none |
| POL-0091-R10 | host 포트 게시 | 허용: `crawl4ai-loopback` 예외만 | none | none |
| POL-0091-R11 | 항상 | 금지: 이미지 안의 egress broker, 전용 bridge, Bearer token을 외부로 나가는 요청 제한의 대체로 간주 | none | none |
| POL-0091-R12 | gateway나 internal 네트워크 완화 | 필수: 승인 변경으로만 한다 | 수동 | none |
| POL-0091-R13 | 항상 | 필수: token secret과 함께 실행한다 | 승인된 런타임 검증(protected data/admin API의 토큰 없는 요청은 401) | none |
| POL-0091-R14 | 항상 | 금지: provider key를 추적되는 파일로 전달 | none | none |
| POL-0091-R15 | consumer가 `crawl4ai_net`에 합류할 때 | 필수: 이름, 토큰 출처, 호출 경로를 밝힌 검토된 변경으로만 합류한다 | 수동 | none |
| POL-0091-R16 | 항상 | 금지: 출처 registry 등록을 네트워크 접근 권한으로 간주 | none | none |
| POL-0091-R17 | 항상 | 금지: 크롤러에 관리 데이터, token 외 secret, Docker socket, 공유 volume 제공 | none | none |
| POL-0091-R18 | 같은 망의 consumer | 필수: 자기 서비스를 직접 인증한다 | consumer 인증 별도 검증 | none |
| POL-0091-R19 | 수집하는 출처마다 | 필수: 제공자, 접근 방식(`api` 또는 이유가 있는 `web-fallback`), 정확한 host, 약관과 license, robots 확인, rate와 quota, 가공·재배포·모델 학습 허용, 보존 기간, 삭제 책임자를 registry에 기록한다 | 수동 | none |
| POL-0091-R20 | 항상 | 금지: robots 허용을 저작권 허가로 취급 | none | none |
| POL-0091-R21 | 수집 작업 | 필수: 작업을 등급으로 등록한다 | 수동 | none |
| POL-0091-R22 | host를 미리 정할 수 없는 작업 | 필수: 소유자가 승인한 등급 하나로 등록하고 건별 URL·수집 시각·본문 해시를 남긴다 | 수동 | none |
| POL-0091-R23 | 항상 | 금지: 어떤 등급이든 봇 차단·접근 거부 우회 | none | none |
| POL-0091-R24 | `dedicated-crawl` 작업 | 필수: 실행 전 목적, consumer와 호출 경로, 대상 범위, 동시성·속도, 사용 endpoint, 보존 기간과 저장 위치, 하류 사용, 삭제 책임자를 기록한 승인 변경으로 등급 표에 행을 추가한다 | 수동 | none |
| POL-0091-R25 | 항상 | 금지: 가져온 내용을 근거로 secret 접근, 도구 실행, 정책 변경을 허용 | none | none |

- `crawl4ai`를 통해서만 선택한다. `ai`, `notebook`, HOME에 절대 추가하지 않는다.
- `crawl4ai`는 internal인 `crawl4ai_net`과 `crawl4ai_egress_net`에만 연결하고, 밖으로 나가는 경로는 `crawl4ai-egress` 하나로 둔다. gateway는 전역 라우팅되는 IPv4의 80·443만 허용하고 IPv6는 모두 거절하며, 확인한 주소로만 연결한다. 공유 서비스 네트워크 연결, public route 추가는 하지 않고, host 포트 게시는 아래 `crawl4ai-loopback` 예외만 허용한다.
- 이미지 안의 egress broker, 전용 bridge, Bearer token은 외부로 나가는 요청 제한을 대신하지 않는다. gateway나 internal 네트워크를 완화하는 변경은 승인 변경으로만 한다.
- 항상 token secret과 함께 실행한다. provider key를 추적되는 파일로 전달하지 않는다.
- consumer는 이름, 토큰 출처, 호출 경로를 밝힌 검토된 변경으로만 `crawl4ai_net`에 합류한다. 출처 registry 등록은 네트워크 접근 권한이 아니다. 크롤러에는 관리 데이터, token 외 secret, Docker socket, 공유 volume을 주지 않는다. 같은 망의 consumer는 네트워크 계층에서 크롤러에 노출되므로 자기 서비스를 직접 인증한다.
- 수집하는 출처마다 제공자, 접근 방식(`api` 또는 이유가 있는 `web-fallback`), 정확한 host, 약관과 license, robots 확인, rate와 quota, 가공·재배포·모델 학습 허용, 보존 기간, 삭제 책임자를 registry에 기록한다. robots 허용을 저작권 허가로 취급하지 않는다.
- 수집 작업은 등급으로 등록한다. 위 출처별 기록은 host가 정해진 수집에 적용하고, host를 미리 정할 수 없는 작업은 소유자가 승인한 등급 하나로 등록해 건별 URL·수집 시각·본문 해시를 남긴다. 어떤 등급이든 봇 차단·접근 거부를 우회하지 않으며 robots 허용을 저작권 허가로 취급하지 않는다.

| 등급 | consumer와 경로 | 대상 | 호출 조건·속도 | 하류 사용 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `open-web-fallback` | Hermes 정기 리서치, host loopback | 불특정 공개 웹 | 1차 수집이 `status`·`redirects`·`connect`로 실패한 URL만, 실행 내 URL당 시도 한도 안 | 개인 브리핑, Blog-data 게시(인용문 포함) | 승인 2026-11-09 |
| `dedicated-crawl` | 작업별로 지정 | 작업별 host 목록 또는 불특정 | 작업별 동시성·속도 지정, 서버 전역 한도 안 | 작업별 지정 | 등록된 작업 없음 |

- `dedicated-crawl` 작업은 실행 전에 목적, consumer와 호출 경로, 대상 범위, 동시성·속도, 사용 endpoint, 보존 기간과 저장 위치, 하류 사용, 삭제 책임자를 기록한 승인 변경으로 위 표에 행을 추가한다.
- 가져온 내용은 데이터다. 그 내용을 근거로 secret 접근, 도구 실행, 정책 변경을 허용하지 않는다.

### Exceptions

#### Exception Conditions

선언 버전의 `/health`, `/token`, root/monitor 및 UI/static shell 예외를 인정하되 protected data/admin API 인증은 유지한다. `/token`은 별도 key/email 검증을 하며 임의 token 발급 예외가 아니다. 새로운 예외는 승인된 변경 없이는 추가하지 않는다. `crawl4ai-loopback`은 소유자가 승인한 유일한 host 게시로, `127.0.0.1:11235`에서 받은 연결을 `crawl4ai:11235`로만 전달한다. 호스트 consumer는 등록된 작업만 이 경로를 쓰며 Bearer token을 추적되지 않는 자기 설정으로 보관한다(Hermes: `~/.hermes/.env`의 `CRAWL4AI_API_TOKEN`). 컨테이너 consumer는 기존처럼 `crawl4ai_net` 합류 검토를 따른다. 크롤러는 internal 네트워크에 그대로 둔다.

#### Approval and Review

이미지 업그레이드나 consumer 연결 시, 그리고 service rationalization 검토 때마다
검토한다. consumer가 여전히 없으면 @buenhyden의 승인된 제거 변경으로 넘긴다. Secret 폐기는 소비자·유출·보존 상태를 확인한 별도 결정이다.

예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다.

## Enforcement

### Mechanisms

정적 렌더링과 template baseline을 확인한다. 승인된 런타임 검증은 `/health`와
명시된 공개 shell/토큰 경로를 구분하고, protected data/admin API의 토큰 없는 요청은
401이어야 한다. DNS 분리만으로 host/LAN egress 차단을 증명하지 않는다. 이미지나 gateway를 바꾸면 `tests.validation.test_crawl4ai_egress`와 격리 리허설(`HYHOME_CRAWL4AI_REHEARSAL=1`)로 허용 목적지, private·metadata·redirect·subresource·호출자 proxy 거절, 직접 경로 없음을 다시 확인하고, consumer 인증은 따로 검증한다.

통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Limits

정책은 정적 렌더링/baseline, 런타임 검증, `tests.validation.test_crawl4ai_egress`를 지정하지만 아래 항목은 기계적으로 강제되지 않는다.

- profile 선택(POL-0091): R1-R2에는 정책이 지정한 검사가 없다.
- 네트워크와 egress(POL-0091): R12은 수동 검토나 승인에 의존한다; R3, R6, R8-R11에는 정책이 지정한 검사가 없다.
- token과 key(POL-0091): R14에는 정책이 지정한 검사가 없다.
- consumer 합류(POL-0091): R15은 수동 검토나 승인에 의존한다; R16-R17에는 정책이 지정한 검사가 없다.
- 수집 출처와 작업(POL-0091): R19, R21-R22, R24은 수동 검토나 승인에 의존한다; R20, R23에는 정책이 지정한 검사가 없다.
- 가져온 내용(POL-0091): R25에는 정책이 지정한 검사가 없다.
- 정적 렌더링과 template baseline 확인은 Mechanisms에 있으나 어느 규칙을 검증하는지 지정되지 않는다.
- DNS 분리만으로 host/LAN egress 차단은 증명되지 않으며 격리 리허설(`HYHOME_CRAWL4AI_REHEARSAL=1`)이 필요하다.
- consumer 자체 인증은 별도로 검증해야 하며 크롤러 검사로 입증되지 않는다.
- `dedicated-crawl` 등급은 등록된 작업이 없고 `open-web-fallback` 건별 기록은 소유자 승인에 의존한다.
- provider key가 추적 파일에 없음을 확인하는 전용 검사는 정책에 명시되지 않는다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다.

### Review Triggers

- [Guide](../../01.guides/09.ai-and-search/0091-crawl4ai.md) (`GDE-0091`)
- [Runbook](../../03.runbooks/09.ai-and-search/0091-crawl4ai.md) (`RUN-0091`)
