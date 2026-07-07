---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/ai-agent-catalogs.md -->

# Reference: AI Agent Catalogs and Comparative Persona Analysis

본 문서는 오픈소스 대규모 에이전트 페르소나 라이브러리인 `msitarzewski/agency-agents`와 `hy-home.docker` 워크스페이스의 거버넌스 최우선 로컬 에이전트 체계를 대조 분석하고, 에이전트의 구조적 인스트럭션(Instruction) 템플릿 아키텍처 및 인프라 안전성과 성능 제어를 위해 워크스페이스에 추가 도입이 필요한 신규 전문 에이전트 페르소나들을 제안한 연구 리포트입니다.

---

## 목차 (Table of Contents)

1. [커뮤니티 에이전트와 로컬 에이전트 아키텍처 비교](#1-커뮤니티-에이전트와-로컬-에이전트-아키텍처-비교)
2. [에이전트 인스트럭션 표준화 템플릿 구조](#2-에이전트-인스트럭션-표준화-템플릿-구조)
3. [워크스페이스를 위한 신규 전문 에이전트 3종 제안](#3-워크스페이스를-위한-신규-전문-에이전트-3종-제안)
4. [결론 및 차기 개선 기회 (Gaps)](#4-결론-및-차기-개선-기회-gaps)

---

## 1. 커뮤니티 에이전트와 로컬 에이전트 아키텍처 비교

오픈소스 프로젝트인 [agency-agents](https://github.com/msitarzewski/agency-agents)와 본 워크스페이스(`hy-home.docker`)가 에이전트를 정의하고 운용하는 방식은 설계 사상 면에서 극단적인 대비를 이룹니다.

*   **`msitarzewski/agency-agents` (대규모 역할 분담 모델)**:
    *   *철학*: 16개 부서(Corporate Divisions)와 140개 이상의 세분화된 비즈니스 페르소나를 사전에 배치하여, 복잡한 조직 구조 내에서의 다중 에이전트 협업 및 비즈니스 프로세스 조율을 모방합니다.
    *   *한계*: 실제 로컬 인프라(컨테이너, 네트워크) 및 파일 시스템에 밀접하게 맞물리는 실시간 하드닝(Hardening) 및 정적 검증 기능이 없으며, 추상적 프롬프트 교환에 집중되어 있어 로컬 실행 환경에서의 오동작 위험도가 높습니다.
*   **`hy-home.docker` (격리된 로컬 작업자 모델)**:
    *   *철학*: 15개의 정밀화된 작업자(Workers) 페르소나만을 운용하며, 각 에이전트는 [docs/00.agent-governance/agents/](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/agents/) 하위의 마크다운 지침에 고정 앵커링됩니다.
    *   *특징*: 모든 에이전트가 Docker Compose, Secrets, 쉘 스크립트 실행 환경, 로컬 린터 및 인간의 승인 경계([approval-boundaries.md](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/rules/approval-boundaries.md))의 지배를 받으며, 도구 사용 범위가 물리적으로 격격히 차단된 형태의 안전지향적 모델을 취합니다.

---

## 2. 에이전트 인스트럭션 표준화 템플릿 구조

본 워크스페이스의 에이전트는 무분별한 자유 서술식 프롬프트를 배제하고, 인간과 AI 컴파일러가 동시에 구조 해석할 수 있는 마크다운 템플릿 포맷을 공유합니다.

```text
    ┌─────────────────────────────────────────────────────────────┐
    │ Markdown Instruction Header & Structure                     │
    │                                                             │
    │ 1. @import docs/00.agent-governance/scopes/xxx.md           │
    │    (Explicitly declare bounds to optimize context ingestion)│
    │                                                             │
    │ 2. Role Description (One-line purpose & pattern definition) │
    │                                                             │
    │ 3. Scope & Rules (Covers/Excludes check matrix)             │
    │                                                             │
    │ 4. Skills & Functions (Permitted tools and script mapping)   │
    │                                                             │
    │ 5. Done Criteria (Validation commands & expected evidence)  │
    └─────────────────────────────────────────────────────────────┘
```

1.  **Scope 명시 선언 (`@import`)**: 에이전트 지침 최상단에 바인딩할 주소 영역(`scopes/infra.md` 등)을 선언하여, 파라미터 유출을 막고 불필요한 시스템 도구 로딩을 사전에 Pruning합니다.
2.  **Scope & Rules Matrix**: 해당 에이전트가 "변경할 수 있는 파일 범주(Covers)"와 "절대로 건드릴 수 없는 파일 및 비밀값(Excludes)"을 테이블로 정의해, 런타임 이탈 시 훅이 이를 감지하도록 돕습니다.
3.  **정적 스크립트 바인딩**: 에이전트가 자율 추론 대신 사용할 수 있는 로컬 유효성 검사 스크립트의 경로(`scripts/validation/...`)를 직접 제공하여 실행의 일관성을 높입니다.
4.  **완료 규격 (Done Criteria)**: 작업이 최종 승인(Completed) 상태가 되기 위해 통과해야 하는 CLI 명령어와 필수 작성 파일의 구조를 규정합니다.

---

## 3. 워크스페이스를 위한 신규 전문 에이전트 3종 제안

현재 15종의 워크스페이스 에이전트 군을 보완하고, 향후 인프라 확장 시 발생할 수 있는 보안 구멍, 성능 한계, 그리고 컨텍스트 용량 오버헤드를 제어하기 위한 신규 3대 전문 에이전트 모델을 제안합니다.

### 3.1 컨테이너 성능 최적화 전문가 (Performance Optimizer)
-   **목적 및 역할**: Docker Compose 스택 내 서비스들의 컨테이너 하드웨어 리소스 제한(`cgroups`), 빌드 소요 시간, 파일 처리 런타임 속도를 전면 정밀 진단합니다.
-   **허용 도구 & 스크립트**: `docker stats`, `check-all-hardening.sh`, [infra-implementer](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/agents/agents/infra-implementer.md) 스코프 바인딩.
-   **구체적 임무**: 
    *   임의 컨테이너가 호스트 CPU/Memory를 점유하지 않도록 `deploy.resources.limits` 구문을 정규화 주입.
    *   컨테이너 영속 볼륨(I/O Bottleneck) 마운트 최적화 스펙 작성.

### 3.2 의존성 취약점 감시 전문가 (Dependency Vulnerability Guardian)
-   **목적 및 역할**: 워크스페이스 프로젝트 의존성(npm, Docker images, GitHub Actions) 및 CI 워크플로 정적 보안 스캔 결과를 감시하고 조치안을 산출합니다.
-   **허용 도구 & 스크립트**: `npm audit`, `zizmor`, `trivy` 정적 이미지 분석 로그 파싱, [security-auditor](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/agents/agents/security-auditor.md) 스코프 바인딩.
-   **구체적 임무**:
    *   CI 빌드 로그의 취약점 경고 스캔 후, 영향받는 base image의 버전 변경 제안서 작성.
    *   SHA 해시가 누락된 제3자 GitHub Actions의 핀 조정(Lock-down) 및 CVE 번호와 대처 런북 연결.

### 3.3 프롬프트 및 컨텍스트 압축 전문가 (Prompt/Context Refiner)
-   **목적 & 역할**: 에이전트가 인프라 수정 작업 중 컨텍스트 윈도우 한계에 도달해 잦은 리트라이나 추론 저하를 겪을 때, 히스토리를 정제하고 규칙을 적시 요약(JIT Compression)합니다.
-   **허용 도구 & 스크립트**: `scripts/knowledge/generate-llm-wiki-index.sh`, [caveman](file:///home/hy/.gemini/config/skills/caveman/SKILL.md) 스킬 제어 모듈.
-   **구체적 임무**:
    *   대용량 리서치 리포트 작성 시, 마크다운의 불필요한 서술 구문을 압축 정리하여 토큰 점유율 감소.
    *   에이전트 부트스트랩 시점에 로드할 규칙 파일들의 지시문을 압축된 카탈로그 형태로 적시 축약.

---

## 4. 결론 및 차기 개선 기회 (Gaps)

### 4.1 요약
`msitarzewski/agency-agents`와 같은 대형 에이전트 풀은 시나리오 설계 아이디어를 주는 훌륭한 참조 소스이지만, 실제 호스트 런타임을 변경해야 하는 모듈형 인프라 워크스페이스에서는 Stage 00 거버넌스와 검증기에 단단히 결속된 소수 정예의 격리형 에이전트 모델이 훨씬 안전하고 높은 품질을 약속합니다.

### 4.2 부족한 요소 (Gaps)
1.  **에이전트 인스트럭션 린터 부재**: 에이전트 명세([docs/00.agent-governance/agents/])를 추가할 때, 표준 마크다운 템플릿의 섹션(Covers, Excludes 등) 누락 여부를 정적으로 체크하여 위반 시 빌드를 중단시키는 정형화된 메타 린터 룰이 미비합니다.
2.  **런타임 로깅 격리 결여**: 에이전트가 다른 서브에이전트를 스폰할 때 주고받는 메시지가 상세 로깅되지 않아 취약점 분석 및 감사(Audit)가 곤란합니다. 추후 서브에이전트의 통신 스트림을 `.agent-work/logs/`에 안전하게 미러링하는 트레이싱 모듈 설계가 필요합니다.

---

## Sources

- [msitarzewski/agency-agents Repository](https://github.com/msitarzewski/agency-agents) - 오픈소스 에이전트 페르소나 라이브러리
- [Agent Catalog Overview](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/agents/README.md) - 로컬 에이전트 카탈로그 개요 SSoT
- [Subagent Protocol Specifications](file:///home/hy/projects/hy-home.docker/docs/00.agent-governance/subagent-protocol.md) - 로컬 에이전트 스폰 및 상호 통신 아키텍처

---

## Maintenance

- **소유자**: 워크스페이스 플랫폼 에이전트 거버넌스 아키텍트
- **검토 주기**: 매 반기 1회 혹은 신규 에이전트 역할 추가 승인 시
- **업데이트 트리거**: `docs/00.agent-governance/agents/` 디렉토리 내 구조 규칙 변경 시
