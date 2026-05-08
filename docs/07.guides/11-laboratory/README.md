# Laboratory (11-laboratory) Guides

> 실험 및 관리 서비스 계층의 사용, 구성, 하드닝 가이드 인덱스.

## Overview

이 디렉터리는 `11-laboratory` 계층의 관리 UI와 실험 도구를 안전하게 사용하는 방법을 정리한다. 각 가이드는 사람이 직접 따라 할 수 있는 접근/확인 절차를 제공하며, 운영 정책과 장애 대응 절차는 각각 `docs/08.operations/11-laboratory/`와 `docs/09.runbooks/11-laboratory/`에서 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Developers
- Security Reviewers
- AI Agents

## Scope

### In Scope

- `11-laboratory` 계층 서비스별 사용/접근 가이드
- gateway, SSO, allowlist, Docker Secret 관련 사용자 확인 절차
- 서비스 문서와 운영/런북 문서 간 링크

### Out of Scope

- 운영 통제 정책 자체
- 장애 발생 시 즉시 실행할 복구 절차
- Compose 서비스 정의 변경
- secret 값, token, credential 원문

## Structure

```text
11-laboratory/
├── dashboard.md              # Homer dashboard guide
├── dozzle.md                 # Dozzle log viewer guide
├── open-notebook.md          # Open Notebook usage guide
├── optimization-hardening.md # Laboratory hardening guide
├── portainer.md              # Portainer management UI guide
├── redisinsight.md           # RedisInsight guide
└── README.md                 # This file
```

## Guide Index

- [Optimization Hardening Guide](./optimization-hardening.md): gateway+allowlist+SSO 경계, 최소권한, 정책 게이트 적용 절차
- [Open Notebook Guide](./open-notebook.md): Open Notebook 및 SurrealDB 기반 노트북 작업 환경 사용
- [Portainer Guide](./portainer.md): 컨테이너 관리 UI 사용
- [RedisInsight Guide](./redisinsight.md): Redis 데이터 시각화/분석
- [Dozzle Guide](./dozzle.md): Docker 로그 모니터링
- [Dashboard Guide](./dashboard.md): Homer 서비스 대시보드 구성

## Common Pitfalls

- allowlist CIDR 미설정으로 운영자 접근이 차단됨
- dashboard 또는 관리 UI `ports` 재노출로 인증 우회 경로가 생김
- Docker socket 쓰기 권한으로 최소권한 원칙이 깨짐
- 문서 인덱스/링크를 업데이트하지 않아 추적성이 깨짐

## How to Work in This Area

1. 새 laboratory 서비스를 추가할 때는 먼저 `infra/11-laboratory/<service>/docker-compose.yml`과 `docs/04.specs/11-laboratory/spec.md`를 확인한다.
2. 사용자 사용 절차는 `docs/99.templates/guide.template.md`를 기준으로 이 디렉터리에 작성한다.
3. 운영 통제는 `docs/08.operations/11-laboratory/`, 복구 절차는 `docs/09.runbooks/11-laboratory/`에 함께 연결한다.
4. 문서 추가/삭제 후 이 README의 `Structure`와 `Guide Index`를 갱신한다.

## Related References

- **Infra Source**: [../../../infra/11-laboratory/README.md](../../../infra/11-laboratory/README.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Operations Index**: [../../08.operations/11-laboratory/README.md](../../08.operations/11-laboratory/README.md)
- **Runbooks Index**: [../../09.runbooks/11-laboratory/README.md](../../09.runbooks/11-laboratory/README.md)
- **Template**: [../../99.templates/guide.template.md](../../99.templates/guide.template.md)
