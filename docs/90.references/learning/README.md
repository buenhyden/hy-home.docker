# Learning References

> Docker 기반 홈 인프라를 CS, CE, SE 관점으로 학습하기 위한 stable roadmap reference

## Overview

`docs/90.references/learning`은 `hy-home.docker` 인프라를 학습 대상으로 해석하기 위한 이론적 배경과 로드맵을 관리합니다. 이 폴더는 설치 가이드나 운영 절차가 아니라, 관련 개념을 장기적으로 참조하기 위한 학습 reference입니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- CS/CE/SE 학습 로드맵
- 분산 시스템, 네트워크, 스토리지, 보안, AI 인프라 이론 요약
- repo-local infrastructure와 이론 주제의 연결
- 외부 논문, 표준, 책 링크

### Out of Scope

- 실제 설치 절차
- 서비스 운영 runbook
- incident timeline 또는 postmortem
- 최신 릴리스/가격/뉴스 상태

## Structure

```text
docs/90.references/learning/
├── README.md       # This file
├── roadmap.md      # Current learning roadmap reference
└── roadmap-v1.md   # Archived initial roadmap reference
```

## Current References

- [roadmap.md](./roadmap.md) - current CS/CE/SE learning roadmap
- [roadmap-v1.md](./roadmap-v1.md) - archived initial roadmap

## How to Work in This Area

1. Keep learning references stable and source-backed.
2. Use [reference.template.md](../../99.templates/reference.template.md) for new non-README reference docs.
3. Link repo-local examples to active docs or `infra/` paths with relative links.
4. Preserve archived roadmaps as reference history unless explicitly asked to remove them.
5. Run `bash scripts/check-repo-contracts.sh` after changing learning reference docs.

## Related Documents

- [90.references](../README.md)
- [docs index](../../README.md)
- [reference template](../../99.templates/reference.template.md)
