---
title: "Manifest Pipeline Synthetic Fixtures"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# Manifest Pipeline Synthetic Fixtures

## Overview

외부 원문·실제 자격 증명이 없는 공개 합성 예시입니다.

## Scope

Manifest hash는 형식 시험용이며 Git/content authenticity를 증명하지 않습니다.
접속 예시의 null credential은 보호된 worker 파일에서만 실제 제공해야 합니다.

## Structure

- [2026-10-10.json](2026-10-10.json): 초기 source/UTC date의 합성 문서 목록.
- [pg-connection.example.json](pg-connection.example.json): ingest 전용 PG 설정 모양.
- [s3-connection.example.json](s3-connection.example.json): 전용 bucket·prefix 설정 모양.

## Usage

합성시험만 수행하며 게시 prefix 업로드는 W38 검토 후의 별도 동작입니다.
Null 값을 실제 비밀로 채운 파일을 Git·argv·env export·출력에 남기지 않습니다.

## Related Documents

- [배치](../README.md)
- [Adapter](../workflow_lib/README.md)
