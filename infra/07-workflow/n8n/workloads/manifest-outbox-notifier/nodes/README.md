---
title: "제한된 manifest 통지 노드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# 제한된 manifest 통지 노드

## Overview

manifest outbox의 개발 캡처 통지를 위한 credential-aware 노드 소스입니다.
이 폴더에는 공통 이미지·Compose·node 등록을 변경하는 설치기가 없습니다.

## Audience

P05 작성자, SEC01 이미지 담당자, P03 접속 계약 담당자와 검토자입니다.

## Scope

공개 소스와 합성 시험에 한정합니다. 설치 이미지 호환성, workflow import,
실제 DB·SMTP 통지·예약 실행·회전·복구는 `NOT_RUN`입니다.

## Structure

- [OpsflowSmtp](OpsflowSmtp/README.md): 고정 캡처 대상과 닫힌 입력을 가진 노드 패키지.

## Tech Stack

TypeScript, n8n native SMTP credential API와 Nodemailer를 사용합니다.
정확한 build dependency는 노드 패키지의 `package.json`과
`package-lock.json`이 소유하며 [패키지 안내](OpsflowSmtp/README.md)에서 확인합니다.

## Configuration

실행 대상과 이미지 등록은 총괄·P03·SEC01의 통합 계약 이후 확정합니다.
공개 소스에 실제 credential ID·값·DB lease capability를 넣지 않습니다.

## Validation

패키지의 합성 build·transport 시험을 실행합니다. 실제 서비스 접속 증거로
취급하지 않습니다.

## Usage

[노드 패키지 절차](OpsflowSmtp/README.md)를 통해 재현합니다.

## Related Documents

- [workload](../README.md)
- [노드 패키지와 합성 시험 안내](OpsflowSmtp/README.md)
