---
title: "Examples Surface"
version: "1.0.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
created: "2026-09-03"
---

# examples

> 새 서비스를 시작할 때 복사해서 쓰는 검증된 시드(seed) 모음

## Overview

`examples/`는 이 저장소의 컨테이너 관례를 그대로 담은 복사 가능한 시드를 둡니다.
현재 시드는 [`sample-web-service/`](sample-web-service/README.md) 하나이며, 정적 웹
서비스 형태로 Compose 정의, Dockerfile, nginx 설정, `.env.example`, 서비스 문서를
한 벌로 제공합니다.

이 경로는 실행 중인 인프라가 아닙니다. `infra/`가 실제 서비스 정의를 소유하고,
`examples/`는 그 관례를 배우고 복사하기 위한 출발점만 소유합니다.

## Audience

- 새 컨테이너 서비스를 추가하려는 Developers
- 저장소의 컨테이너 하드닝 관례를 확인하려는 Reviewers
- 새 서비스 골격을 생성하는 AI Agents

## Scope

### In Scope

- 복사 가능한 서비스 시드와 각 시드의 README
- 시드가 보여주는 컨테이너·Compose·시크릿 주입 관례

### Out of Scope

- `infra/`의 실제 서비스 정의와 운영 절차
- 시드를 복사한 뒤의 서비스별 설정값
- `docs/` stage 산출물 본문

## Structure

```text
examples/
├── sample-web-service/  # 정적 웹 서비스 시드 (Compose, Dockerfile, nginx, 서비스 문서)
└── README.md            # This file
```

## How to Work in This Area

1. 시드 폴더 전체를 `infra/`의 대상 tier 아래로 복사합니다 → 원본 시드는 그대로 남습니다.
2. 복사본에서 서비스 이름, 이미지, 포트, 네트워크를 대상 서비스에 맞게 바꿉니다 → `docker compose config`가 성공합니다.
3. 시크릿은 값이 아니라 파일로 주입하고 `.env.example`만 추적합니다 → 평문 자격 증명이 커밋되지 않습니다.
4. 새 서비스 문서를 `docs/05.operations/catalog/`의 해당 도메인에 추가합니다 → 운영 절차 소유자가 생깁니다.
5. `bash scripts/validation/validate-docker-compose.sh`를 실행합니다 → 종료 코드 `0`.

시드 자체를 고칠 때는 복사본이 아니라 `examples/` 원본을 고치고, 그 변경이 기존
서비스에 적용되어야 하는지 함께 판단합니다.

## Related Documents

- [Root README](../README.md)
- [Infrastructure surface](../infra/README.md)
- [Sample web service seed](sample-web-service/README.md)
- [Operations catalog](../docs/05.operations/catalog/README.md)
- [README template](../docs/99.templates/templates/common/readme-repository.template.md)
