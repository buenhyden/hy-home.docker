# 🎓 Learning & Theory (학습 및 이론 가이드)

## 목적 (Purpose)

이 디렉터리는 `hy-home.docker` 인프라 구축을 통해 얻을 수 있는 이론적 지식과 실무 역량을 구조화하여 제공합니다. 단순한 설치 가이드를 넘어, 각 기술의 컴퓨터 과학(CS), 컴퓨터 공학(CE), 소프트웨어 공학(SE)적 배경을 깊이 있게 탐구합니다.

## 주요 문서 (Highlights)

- **[Self-Learning Roadmap](./roadmap.md)**: 전체 인프라를 이론적으로 매핑한 핵심 로드맵 (v2)
- **[Roadmap v1 (Archive)](./roadmap-v1.md)**: 초기 버전의 로드맵 (기록용)

## 학습 영역 (Learning Domains)

로드맵은 다음 세 가지 계층으로 구성되어 있습니다.

1. **Tier 1: Computer Science (Theory)**: 분산 시스템, 합의 알고리즘, 인덱싱 구조 등 소프트웨어의 논리적 아키텍처.
2. **Tier 2: Computer Engineering (Hardware/OS)**: 리눅스 커널 가상화, 네트워크 IPAM, 하드웨어 추론 가속 등 소프트웨어와 하드웨어의 접점.
3. **Tier 3: Software Engineering (Practice)**: SRE 관측 가능성 패턴, Zero Trust 보안 모델, EDA(Event-Driven Architecture) 등 실무 엔지니어링 패턴.

## 참고 문서 (References)

심층 학습 주제는 이 디렉터리의 로드맵 문서에서 관리합니다.

- 네트워크 이론 (L4/L7, DNS, ACME)
- OS 및 가상화 (Namespace, Cgroup)
- 데이터 관리 (CAP, ACID, WAL)
- 보안 및 신원 (OAuth2, OIDC, Vault)
- AI 인프라 (Vector Search, RAG, CUDA)
- 분산 메시징 (Kafka, EDA)

## Related Documents

- [90.references](../README.md)
- [docs index](../../README.md)

---
*Created by Antigravity Self-Learning Workflow*

---

## Overview

`docs/90.references/learning`는 느리게 변하는 참고 지식과 외부 기준을 관리하는 reference 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- reference facts, glossary, roadmap
- 느리게 변하는 기준 정보
- 관련 stage 문서 링크

### Out of Scope

- 실시간 운영 절차
- incident 사실 기록
- runtime 설정 원문

## Structure

```text
docs/90.references/learning/
├── README.md  # This file
├── roadmap-v1.md  # 문서
└── roadmap.md  # 문서
```

## How to Work in This Area

1. 참고 정보가 active policy나 runbook을 대체하지 않는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
