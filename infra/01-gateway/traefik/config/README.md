---
layer: infra
---

# Traefik Static Configuration

This folder contains the static configuration for Traefik.

- **traefik.yml**: The main configuration file. It defines the entrypoints (80, 443, 8082), the Docker provider, and the file provider for dynamic configurations in `/dynamic/`.

---

## Overview

`infra/01-gateway/traefik/config`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/01-gateway/traefik/config/
├── README.md  # This file
└── traefik.yml  # 구성 파일
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related References

- [infra/README.md](../../../README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../../docs/05.operations/README.md)
