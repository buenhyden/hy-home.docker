---
title: "독립 통지 합성 fixture"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# 독립 통지 합성 fixture

## Overview

[cases.json](cases.json)은 공개 합성 claim·수락/ack 유실·retry/stale lease 기대 결과입니다.

## Scope

UUID·run ID·주소는 합성이며 운영 token이나 credential이 아닙니다. DB/SMTP/native 수용 증거를 포함하지 않습니다.

## Structure

닫힌 claim, 상태별 기대 결과, 개인정보 누출 검사 marker와 아직 필요한 native 실패·복구 사례를 둡니다.

## Usage

전용 Python 상태 시험과 제한된 SMTP node 시험에서 사용합니다. malformed·다중 claim·header injection·
수락 목록·timeout·취소와 원문 오류 누출도 각각 부정 사례로 검사합니다.
lease 만료·동시 claim·attempt cap/dead·공식 requeue는 실제 P04 계약 이후 native 시험에서 검증합니다.

## Related Documents

- [워크로드](../README.md)
- [초안 계약](../outbox-contract.json)
