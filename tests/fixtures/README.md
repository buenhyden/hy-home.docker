---
title: "Synthetic fixture family"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# 합성 fixture

## Overview

독립 CLI·schema consumer가 공유하는 비밀값 없는 고정 입력입니다.

## Audience

저장소 계약의 구현·검토 담당자입니다.

## Scope

운영 secret·dotenv·인증자료·원문 로그는 보관하지 않습니다.

## Structure

- [port-contract/](port-contract/README.md): P03 네 위치 포트 선언·합성 config 입력.

## Tech Stack

기존 Python unit/contract 검증을 사용합니다.

## Configuration

각 하위 README와 owning Task가 합성 입력의 의미와 허용 경계를 설명합니다.

## Validation

[검증 진입점](../README.md)의 현재 등록된 시험 owner를 사용합니다.

## Usage

각 consumer에 필요한 명명된 합성 입력만 선택합니다.

## Related Documents

- [Test surface](../README.md)
