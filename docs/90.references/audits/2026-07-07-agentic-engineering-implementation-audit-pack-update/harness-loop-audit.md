---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md -->

# Reference: Harness and Loop Engineering Audit

## Overview

본 감사는 `hy-home.docker` 워크스페이스 내 하네스 엔지니어링과 루프 엔지니어링 체계의 구체적인 구현 수준을 검증하고, 각 프로바이더(Claude, Codex, Gemini)별 런타임 통제 방안 및 공통 환경 규칙의 실효성을 평가합니다.

## Purpose

에이전트의 로컬 실행 환경(Harness)과 자가 수정 순환(Loop)을 정밀하게 제어하여 발생할 수 있는 오동작과 정책 이탈을 방지합니다.

## Repository Role

본 문서는 하네스 및 루프 엔지니어링에 관한 오딧 참조 자료이며, 런타임 스크립트 코드나 어댑터 설정을 변경하지 않습니다.

---

## 1. 하네스 엔지니어링 (Harness Engineering) 감사

### A. 구현 현황
- **하네스 라우팅 맵**: `harness-implementation-map.md`를 통해 루트 쉼(`AGENTS.md` 등), 도커 컴포즈 런타임, 자격증명 격리, 검증 스크립트, 프로바이더 훅이 일목요연하게 맵핑 및 작동 중입니다.
- **계약 검증기**: `check-repo-contracts.sh`가 루트 쉼과 스테이지 문서 템플릿 준수 여부(프론트매터, 파일 네이밍 규약 등)를 엄격히 강제하고 있습니다.
- **포스트 검증기**: `post-tool-validate.sh`가 파일 수정 후 동작하여 원치 않는 공백 제거, 불필요한 줄바꿈 등을 자동으로 수정 및 통제합니다.

### B. 격차 및 부족한 요소 (Gaps)
- **샌드박스 보안 통제 편차**: Claude Code와 Codex는 툴 수준에서 OS 명령어 차단 및 파일 경로 쓰기 제한 등을 지원하지만, Gemini는 런타임 샌드박스 경계가 쉘 수준의 사용자 승인 확인 창에 그치며, 에이전트가 예외적으로 `sudo` 권한을 요청하거나 시스템 민감 영역에 손을 댈 위험에 노출되어 있습니다.
- **수동 스냅샷 생성 의존성**: `graphify update` 도구가 자동화 파이프라인의 일부가 아니기 때문에, 작업 후 수동으로 갱신하지 않으면 지식 그래프 정보가 stale 상태로 유지되어 다음 에이전트의 지식 탐색 효율을 떨어뜨릴 수 있습니다.

---

## 2. 루프 엔지니어링 (Loop Engineering) 감사

### A. 구현 현황
- **협업 피드백 루프**: `implementation_plan.md`를 먼저 사용자에게 제시하여 서명(Proceed)을 받은 뒤 작업을 시작하며, 최종 결과를 `walkthrough.md`와 `progress.md`에 등재하는 프로세스가 루프화되어 정착되어 있습니다.
- **로컬 피드백 루프**: 린터와 컴포즈 검증 스크립트가 리턴하는 오류 문구를 어댑터가 즉각 읽어 들여 스스로 코드를 재수정하는 자가 치유(Self-healing) 루프가 활성화되어 있습니다.

### B. 격차 및 부족한 요소 (Gaps)
- **시맨틱 에이전트 평가(Eval) 루프 부재**: 린터와 구문 검증은 자동 실행되지만, 에이전트가 수행한 작업이 Stage 01(요구사항) 및 Stage 03(스펙)의 비즈니스적 의도에 완벽히 부합하는지를 확인하는 시맨틱 검증이 여전히 수동 영역에 남아 있습니다. 로컬에 데모용 advisory runner(`run-agent-output-eval-fixtures.sh`)만 배치되어 있을 뿐, CI의 필수 게이트로 편입되지 못했습니다.

---

## 3. Claude, Codex, Gemini 개별 현황 및 공통 환경 체계

### A. 프로바이더별 특징과 격차

1. **Claude Code**:
   - 현황: `.claude/settings.json` 및 `.claude/agents/`로 구성. 로컬 `agent-event-hook.sh`와의 바인딩이 매우 긴밀하며, ReAct 및 subagent 호출 능력이 뛰어납니다.
   - 부족한 요소: 대량의 파일 수정 작업 시 컨테이너 볼륨과 연동되어 잦은 승인 팝업이 발생하여 병목을 유발합니다.
2. **Codex**:
   - 현황: `.codex/hooks.json` 및 TOML 기반 에이전트 설정 운용. 로컬 실행 제약 및 샌드박싱 제어 능력이 기계적으로 정교합니다.
   - 부족한 요소: Codex 어댑터의 템플릿 유효성 검증기가 저장소의 최신 markdown stage-gate 규약을 감지하지 못하는 오차가 간헐적으로 발생합니다.
3. **Gemini**:
   - 현황: `.agents/` 디렉토리를 참조하며, Antigravity 2.0 IDE 통합의 일환으로 규칙에 따른 지침 실행을 지원합니다.
   - 부족한 요소: 네이티브 훅 및 subagent 호출 구조를 갖춘 공식 CLI 툴링이 부재하여, 타 프로바이더에 비해 자동 검증 루프가 수동적입니다.

### B. 공통 환경 구축 현황 및 보완 사항
- **구축 현황**: `rules/provider-capability-matrix.md`를 기점으로 공통의 모델 위상 및 에이전트 역할 바인딩이 되어 있으며, 15개 에이전트의 지침 파일이 동기화되어 사용됩니다.
- **보완 사항**: 프로바이더에 종속되지 않고 파일 수정 직후 강제적으로 `post-tool-validate.sh` 및 `check-repo-contracts.sh`를 실행시키는 **공통 실행 쉘 래퍼 (Universal Exec Wrapper)**를 만들어, 모든 프로바이더에서 동등한 하네스 강도를 확보해야 합니다.

## Related Documents

- [README.md](./README.md)
- [implementation-overview.md](./implementation-overview.md)
- [sdlc-qa-security-audit.md](./sdlc-qa-security-audit.md)
- [agent-catalog-audit.md](./agent-catalog-audit.md)
- [../../research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md](../../research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md)
