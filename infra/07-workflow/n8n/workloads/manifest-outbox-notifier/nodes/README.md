---
title: "제한된 manifest 통지 노드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# 제한된 manifest 통지 노드

## Purpose

### Service Role

manifest outbox의 개발 캡처 통지를 위한 credential-aware 노드 소스입니다.
이 폴더에는 공통 이미지·Compose·node 등록을 변경하는 설치기가 없습니다.

#### Audience

P05 작성자, SEC01 이미지 담당자, P03 접속 계약 담당자와 검토자입니다.

#### Scope

공개 소스와 합성 시험에 한정합니다. 설치 이미지 호환성, workflow import,
실제 DB·SMTP 통지·예약 실행·회전·복구는 `NOT_RUN`입니다.

#### Structure

- [OpsflowSmtp](OpsflowSmtp/README.md): 고정 캡처 대상과 닫힌 입력을 가진 노드 패키지.

### Supported Environment

TypeScript, n8n native SMTP credential API와 Nodemailer를 사용합니다.
정확한 build dependency는 노드 패키지의 `package.json`과
`package-lock.json`이 소유하며 [패키지 안내](OpsflowSmtp/README.md)에서 확인합니다.

## Interfaces

### Inputs and Outputs

실행 대상과 이미지 등록은 총괄·P03·SEC01의 통합 계약 이후 확정합니다.
공개 소스에 실제 credential ID·값·DB lease capability를 넣지 않습니다.

### Security Boundary

공개 소스에 실제 credential ID·값·DB lease capability를 넣지 않습니다. 이 폴더에는 공통 이미지·Compose·node 등록을 바꾸는 설치기가 없어 운영 서비스에 영향을 주지 않으며, 접근 경계의 세부는 [노드 패키지](OpsflowSmtp/README.md)가 소유합니다.

## Development

### Local Workflow

[노드 패키지 절차](OpsflowSmtp/README.md)를 통해 재현합니다.

### Checks

패키지의 합성 build·transport 시험을 실행합니다. 실제 서비스 접속 증거로
취급하지 않습니다.

## Operations

### Runbook Links

- [workload](../README.md)
- [노드 패키지와 합성 시험 안내](OpsflowSmtp/README.md)

### Observability and Recovery

없음: 소스 폴더라 헬스체크·지표가 없고 설치 이미지·workflow import·실제 통지는 `NOT_RUN`입니다. 복구할 런타임 상태가 없으며 Git 변경을 되돌립니다.
