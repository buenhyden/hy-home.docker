<!-- Target: docs/07.guides/09-tooling/registry.md -->

# Docker Registry Guide

> Private OCI-compliant image distribution service.

---

## Overview (KR)

이 문서는 `hy-home.docker`에서 운영하는 프라이빗 도커 레지스트리(Docker Registry v2)에 대한 가이드다. 내부 이미지를 저장하고 배포하는 절차와 주의사항을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- CI/CD Developers

## Purpose

- 프라이빗 레지스트리를 통한 내부 이미지 배포 자동화 및 보안 강화.
- 외부 레지스트리 의존성 없이 로컬 네트워크 내에서의 빠른 이미지 풀(Pull)/푸시(Push).

## Prerequisites

- Docker Engine 및 Docker Compose 설치.
- `insecure-registries` 설정 (HTTPS 미적용 시).
- `REGISTRY_PORT` (기본 5000) 접근 가능 여부 확인.

## Step-by-step Instructions

### 1. Registry Login (If Auth is Configured)

기본 설정에서는 인증이 비활성화되어 있을 수 있으나, 활성화된 경우 다음 명령어로 로그인한다.

```bash
docker login registry.hy-home.docker:5000
```

### 2. Image Tagging

로컬 이미지를 레지스트리에 푸시하기 위해 적절한 태그를 부여한다.

```bash
docker tag <local-image>:<tag> registry.hy-home.docker:5000/<project>/<image>:<tag>
```

### 3. Image Push

```bash
docker push registry.hy-home.docker:5000/<project>/<image>:<tag>
```

### 4. Image Pull

```bash
docker pull registry.hy-home.docker:5000/<project>/<image>:<tag>
```

## Common Pitfalls

- **Insecure Registry Error**: `http` 프로토콜을 사용하는 경우, Docker 데몬 설정(`/etc/docker/daemon.json`)에 `insecure-registries` 항목으로 추가해야 한다.
- **Disk Space**: 대량의 이미지가 누적되면 호스트 디스크가 가득 찰 수 있다. 가비지 컬렉션(GC)을 주기적으로 실행해야 한다.
- **Service Down**: 레지스트리 컨테이너가 중단되면 CI/CD 파이프라인 전체가 실패하므로 헬스체크 모니터링이 필수적이다.

## Related Documents

- **Spec**: [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md)
- **Operation**: [../08.operations/09-tooling/registry.md](../08.operations/09-tooling/registry.md)
- **Runbook**: [../09.runbooks/09-tooling/registry.md](../09.runbooks/09-tooling/registry.md)
