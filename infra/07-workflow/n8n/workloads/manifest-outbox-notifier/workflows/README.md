---
title: "비활성 통지 workflow"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# 비활성 통지 workflow

## Overview

[manifest-outbox-mailpit.json](manifest-outbox-mailpit.json)은 생성기가 소유하는 공개 초안입니다.

## Scope

`active:false`와 credential placeholder를 유지합니다. 실제 import·manual·예약 실행은 NOT_RUN입니다.

## Structure

Manual 또는 단일 1분 polling → claim → 입력 검사 → 제한된 SMTP → 수락 확인 → ack입니다.
불확실·오류·stale lease는 retry 결과 확인 또는 고정 오류 경로로 처리합니다.
빈 claim은 downstream item을 만들지 않습니다. ack 실패는 이전 SMTP node에서 재개하지 않습니다.

## Usage

[생성기](../tools/README.md)의 명시적 CLI로 갱신하고 `--check`로 byte parity를 검사합니다.
선택 이미지의 native node schema·loader·credential binding은 선행 계약 이후 검증합니다.
성공·오류·수동·진행 데이터 저장을 끄며, output·pinData에 원문 driver 오류나 credential을 넣지 않습니다.

## Related Documents

- [워크로드](../README.md)
- [제한된 SMTP node](../nodes/README.md)
