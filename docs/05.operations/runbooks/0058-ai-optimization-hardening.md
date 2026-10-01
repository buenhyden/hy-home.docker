---
title: "08-AI Optimization Hardening Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0058"
parent_ids:
- "GDE-0058"
created: "2026-05-17"
---

# 08-AI Optimization Hardening Runbook

## Overview

이 런북은 `08-ai` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, Ollama concurrency 설정 누락, Open WebUI stateful 드리프트, exporter health 계약 실패, CI 게이트 실패를 중심으로 점검/복구한다.

### Purpose

- AI 공개 경로 보안과 GPU 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## When to Use

- `infrastructure-hardening` CI가 실패할 때
- Ollama/Open WebUI 경로 접근 정책이 비정상일 때
- Ollama GPU 과부하/OOM 또는 queue 적체가 반복될 때
- exporter metrics 수집이 실패할 때

## Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

## Procedure

### Checklist

- [ ] 실패 항목(middleware, concurrency, template, healthcheck, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(응답 지연, 인증 실패, GPU 사용률 급등) 평가

### Steps

1. 정적 구성 점검
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
   - `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
   - AI service-local compose 파일은 root 선언된 network과 root include context에 의존하므로 단독 `docker compose config` 대상으로 사용하지 않는다.
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
3. 증상별 복구
   - middleware 회귀:
     - Ollama에는
       `gateway-standard-chain@file,sso-errors@file,sso-auth@file`, Open
       WebUI에는 `gateway-standard-chain@file`과 native OIDC contract를
       source대로 재적용
   - Ollama 과부하/queue 적체:
     - `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 보수값으로 복원
   - Open WebUI stateful drift:
     - `template-stateful-med` 재적용
   - exporter metrics 실패:
     - `depends_on` health gating 및 metrics healthcheck 계약 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
   - `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`

### Verification Steps

- [ ] AI compose static validation 통과
- [ ] AI hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening`, Ollama exporter 지표, Open WebUI 상태, gateway 접근 로그
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 08-ai`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: operator approval을 받은 뒤에만 승인된 운영 모델에서 직전 안정 모델로 전환
- **Tool Disable / Revoke**: AI 자동 배포/승격 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-all-hardening.sh 08-ai`
  - `check-template-security-baseline`
  - `python3 scripts/validation/check-document-links.py --mode all`
- **Trace Capture**: CI 로그, exporter 지표, Compose 설정

### Control evidence boundary

AI hardening은 일부 소스 문자열만 검사하며 GPU 여유, 사용자별 모델 권한, chat 보존·삭제, password 거부와 추론 성공을 증명하지 않는다. 모델 승격, 역할·환경별 접근 분리, 대화 masking/retention 요구는 유지한다. 소스에는 자동 chat retention과 완성된 모델 접근 분리를 입증할 설정이 부족하다. @buenhyden의 별도 통제·구현 변경과 검증 전에는 준수를 주장하지 않는다. 근거를 채우려고 비공개 대화를 로그에 남기지 않는다. ComfyUI 영속성과 Crawl4AI 격리는 각 Runbook의 통제를 따른다.

## Evidence

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 위의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 설정 rollback rehearsal은 계획만 있으며 미실행 상태다. 상태 데이터 복구는 `RUN-0056`, `RUN-0057`, `RUN-0081`이 소유한다. 이 최적화 Runbook으로 모델·SQLite·벡터·워크플로 복구를 입증하지 않는다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 `## Escalation`에 따라 보고한다.

## Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

## Traceability

- Declared parent: [08-AI Optimization Hardening Usage Guide](../guides/0058-ai-optimization-hardening.md) (`GDE-0058`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0058-ai-optimization-hardening.md) (`GDE-0058`), [Policy](../policies/0058-ai-optimization-hardening.md) (`POL-0058`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0058-ai-optimization-hardening.md)
- [Operations policy](../policies/0058-ai-optimization-hardening.md)
