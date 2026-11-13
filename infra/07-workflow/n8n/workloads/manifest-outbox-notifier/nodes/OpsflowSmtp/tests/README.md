---
title: "SMTP 노드 합성 회귀시험"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# SMTP 노드 합성 회귀시험

## Purpose

### Service Role

닫힌 claim·credential 경계, 개인정보 제거, SMTP 불확실성과 socket 수명을
합성 fixture로 검증합니다.

#### Audience

P05 작성자와 code/security 검토자입니다.

#### Scope

기존 합성 시험과 새 owned loopback STARTTLS 시험을 구분합니다. 후자는 합성 CA·계정과
실제 Nodemailer를 사용하지만 n8n Worker·Mailpit native fixture나 실제 credential·DB를
사용하지 않습니다. 운영·실제 회전·복구 수용은 별도이며 과거 C19/C22를 취소하지 않습니다.

#### Structure

- [transport.test.cjs](transport.test.cjs): input/privacy/acceptance/deadline 계약.
- [adapter.test.cjs](adapter.test.cjs): 소유 socket의 연결 실패·취소·종료 경계.
- [protocol.test.cjs](protocol.test.cjs): 실제 Nodemailer와 메모리 Duplex SMTP byte.
- [starttls.test.cjs](starttls.test.cjs): 소유 loopback의 CA·이름·인증·downgrade·취소·응답 유실과 socket 정리.
- [node.test.cjs](node.test.cjs): 실제 workflow API 타입·오류와 합성 execution context.

### Supported Environment

Node 내장 test/assert/mock timers와 정확히 locked library를 사용합니다.
STARTTLS 시험은 자체 생성 합성 인증서·계정과 소유 loopback listener를 정리합니다.
실제 서비스나 운영 인증 자료는 사용하지 않습니다.

## Interfaces

### Inputs and Outputs

합성 UUID capability와 공개 source/count/run fixture만 사용합니다.
기존 합성 소켓/응답과 STARTTLS의 실제 loopback 소켓은 서로 다른 시험 수준입니다.
양쪽 모두 외부 배달·운영 수신 증거가 아닙니다.

### Security Boundary

시험은 자체 생성한 합성 CA·계정·UUID capability와 소유 loopback listener만 쓰며 실제 credential·DB·운영 인증 자료를 사용하지 않습니다.

## Development

### Local Workflow

accepted·unknown/rejected·응답 손실·취소를 재현합니다. lease/ack/retry의 실제
DB 동시성·복구 시험은 P04 계약 인계 이후 별도 native fixture에 연결합니다.

### Checks

부모 패키지에서 `npm run test:coverage`를 실행합니다. compiler build와 모든
시험이 성공하고 compiled source coverage gate가 통과해야 합니다.

## Operations

### Runbook Links

- [노드 패키지](../README.md)
- [노드 탐색](../../README.md)

### Observability and Recovery

없음: 시험 패키지라 헬스체크·지표가 없습니다. 실패는 `npm run test:coverage` 출력과 coverage gate로 확인하며 복구는 Git 변경을 되돌리는 것입니다. 시험이 연 loopback listener와 socket은 시험이 정리합니다.
