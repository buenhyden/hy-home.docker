---
title: "Administration and Experimentation Hardening Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0074"
parent_ids:
- "GDE-0074"
created: "2026-05-17"
---

# Administration and Experimentation Hardening Runbook

## Overview

이 런북은 관리·실험 기능 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. direct 노출 복원, allowlist/SSO/gateway 체인 누락, 네트워크 경계 드리프트, CI 게이트 실패를 중심으로 점검/복구한다.

### Purpose

- Laboratory 관리 UI 보안 경계와 운영 안정성 기준을 신속히 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## When to Use

- `infrastructure-hardening` CI가 실패할 때
- dozzle/redisinsight/open-notebook 접근 경계가 비정상일 때
- dashboard direct 접근 경로가 재노출되었을 때
- dozzle socket 권한 드리프트가 발생했을 때

## Procedure

### Checklist

- [ ] 실패 항목(middleware, allowlist, network, direct exposure, socket 권한, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(관리 UI 접근/보안/감사) 평가

### Steps

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
3. 증상별 복구
   - middleware/allowlist 회귀:
     - 각 서비스의 승인된 체인을 복원한다. Dozzle native OIDC 및 Open Notebook의 공유 SSO 제외 예외를 일괄 덮어쓰지 않는다
   - 네트워크 드리프트:
     - root 선언된 network context에 합류하는 service network block 복원
   - dashboard direct 노출:
     - `ports` 제거, `expose`만 유지
   - dozzle 권한 드리프트:
     - `/var/run/docker.sock` 마운트를 `:ro`로 복원
   - open-notebook route/secret 드리프트:
     - route chain을 `gateway-standard-chain + open-notebook-admin-ip + large-body`로 복원
     - `OPEN_NOTEBOOK_PASSWORD_FILE`과 `OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE` secret-file 주입을 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`

### Verification Steps

- [ ] Laboratory compose static validation 통과
- [ ] laboratory hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening` 결과와 정제된 ingress·서비스 로그
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - 각 패키지의 `docker-compose.yml`: `infra/04-data/redisinsight/`, `infra/06-observability/dozzle/`, `infra/08-ai/open-notebook/`, `infra/08-ai/mlflow/`, `infra/12-analytics/jupyterlab/`
  - `scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
  - `.github/workflows/ci-quality.yml`
- [ ] 파일 되돌림이나 runtime 재시작이 필요하면 승인자와 영향 범위를 기록한 뒤 수행
- [ ] 복구 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

### 검토된 하드닝 변경 순서

1. 정적 구성 점검
   - `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
2. Ingress 경계 정렬
   - 서비스별 승인된 인증 방식을 보존한다. Dozzle은 native OIDC, Open Notebook은 앱 비밀번호이며 나머지 gateway 경로는 해당 정책을 따른다.
   - Open Notebook은 upload boundary를 위해 `large-body@file`을 추가한다.
3. 네트워크 경계 표준화
   - 모든 compose에 root 선언된 network context에 합류하는 service network block을 유지한다.
4. 최소권한 적용
   - dashboard `ports` 제거 후 `expose`만 사용한다.
   - dozzle docker socket을 `:ro`로 전환한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `python3 scripts/validation/check-document-links.py --mode traceability`
6. 카탈로그 확장 로드맵 반영
   - dozzle 로그 제한, redisinsight 감사 정책, open-notebook data retention/direct-port review를 tasks/operations에 반영한다.

## Evidence

- 이 런북 실행의 명령 결과·시각과 운영자 또는 agent의 조치를 기록한다.
- 실패 검사·관측 증상·최종 복구 또는 보고 상태를 해당 Task나 사고 근거에 기록한다.

## Rollback or Recovery

- 위의 `Safe Rollback or Recovery Procedure`를 포함하여 이 런북에 정의된 복구·rollback 단계만 사용한다.
- 관측 실패가 절차와 맞지 않으면 변경을 멈추고 근거를 보존한 뒤 `## Escalation`을 따른다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

검증 실패·비밀 노출 의심·파괴적 변경 필요·예상과 다른 결과가 나타나면 중단하고 책임자에게 보고한다. 근거, 시도한 단계와 현재 복구 상태를 함께 남긴다.

### 적용 범위와 검증 한계

이 주제는 Data·Observability·AI·Analytics로 나뉜 관리·실험 기능의 공통 통제를
소유한다. Dozzle·RedisInsight·JupyterLab은 OPTIONAL이며 tier나 프로필은 격리
수단이 아니다. socket `:ro`는 Docker API 호출을 제한하지 않는다. Open Notebook의
secret 파일이 프로세스 환경변수로 전달될 수 있으므로 값이 Compose·로그·근거에
노출되지 않도록 하고, mutable 이미지의 FILE 옵션 지원은 별도로 검증한다.
정적 gate 통과는 직접 peer 접근 차단·인증·복구 성공을 증명하지 않는다. 승인된
예외, 월별 검토와 같은 릴리스 안의 임시 예외 종료·재검증 조건은 유지한다.

## Traceability

- 상위 문서: [Administration and Experimentation Hardening Usage Guide](../guides/0074-laboratory-optimization-hardening.md) (`GDE-0074`)
- 설계 근거: [Administration and Experimentation Architecture Description](../../02.architecture/descriptions/0011-laboratory-architecture.md) (`AD-0011`)
- 동일 주제 문서: [Guide](../guides/0074-laboratory-optimization-hardening.md) (`GDE-0074`), [Policy](../policies/0074-laboratory-optimization-hardening.md) (`POL-0074`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0074-laboratory-optimization-hardening.md)
- [Operations policy](../policies/0074-laboratory-optimization-hardening.md)
