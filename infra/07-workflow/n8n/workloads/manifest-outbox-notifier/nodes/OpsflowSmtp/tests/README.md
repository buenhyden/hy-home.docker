---
title: "SMTP 노드 합성 회귀시험"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# SMTP 노드 합성 회귀시험

## Overview

닫힌 claim·credential 경계, 개인정보 제거, SMTP 불확실성과 socket 수명을
합성 fixture로 검증합니다.

## Audience

P05 작성자와 code/security 검토자입니다.

## Scope

시험은 DNS·net connection·listener·실제 credential·DB를 사용하지 않습니다.
native 이미지·workflow import·DB·SMTP·예약·회전·복구는 `NOT_RUN`입니다.

## Structure

- [transport.test.cjs](transport.test.cjs): input/privacy/acceptance/deadline 계약.
- [adapter.test.cjs](adapter.test.cjs): 소유 socket의 연결 실패·취소·종료 경계.
- [protocol.test.cjs](protocol.test.cjs): 실제 Nodemailer와 메모리 Duplex SMTP byte.
- [node.test.cjs](node.test.cjs): 실제 workflow API 타입·오류와 합성 execution context.

## Tech Stack

Node 내장 test/assert/mock timers와 정확히 locked library를 사용합니다.
별도 테스트 서비스나 인증 자료가 필요하지 않습니다.

## Configuration

합성 UUID capability와 공개 source/count/run fixture만 사용합니다.
소켓과 SMTP 응답은 메모리에서 생성하며 fixture bytes는 실제 수신 기록이 아닙니다.

## Validation

부모 패키지에서 `npm run test:coverage`를 실행합니다. compiler build와 모든
시험이 성공하고 compiled source coverage gate가 통과해야 합니다.

## Usage

accepted·unknown/rejected·응답 손실·취소를 재현합니다. lease/ack/retry의 실제
DB 동시성·복구 시험은 P04 계약 인계 이후 별도 native fixture에 연결합니다.

## Related Documents

- [노드 패키지](../README.md)
- [노드 탐색](../../README.md)
