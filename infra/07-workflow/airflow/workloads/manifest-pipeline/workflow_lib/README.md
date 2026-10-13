---
title: "Manifest Pipeline Library"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
---

# Manifest Pipeline Library

## Overview

엄격한 합성 manifest parser와 task 실행 시 사용하는 전용 I/O adapter를 둡니다.

## Scope

원본 bytes 기반 ID, 불변 records, 허용 source/date/path, 보호 설정 파일과
S3 readback·PG 게시를 소유합니다. 다른 DB·객체·자격 증명은 접근 대상이 아닙니다.

## Structure

- [manifest.py](manifest.py): parser·ID·partition·게시 순서.
- [adapters.py](adapters.py): 보호 JSON·S3·parameterized PostgreSQL.
- [tls.py](tls.py): 보호된 CA 검증과 쓰기 금지한 메모리 사본의 수명 관리.

## Usage

드라이버는 task 실행 때만 import합니다. 실제 endpoint와 권한 검증을 합성
double의 PASS로 대신하지 않습니다. 설정 예시는 실행 가능한 credential이 아닙니다.

## Related Documents

- [배치](../README.md)
- [예시](../fixtures/README.md)
