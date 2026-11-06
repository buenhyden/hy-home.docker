---
title: "Architecture Decision Records"
version: "1.7.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
---

# Architecture Decision Records

## Overview

`docs/02.architecture/decisions`는 중요한 아키텍처 선택의 맥락과 동인,
고려한 대안, 선택, 근거, 결과, 확인 방법과 supersession을 보존한다.
ADR은 구현 명세나 운영 절차가 아니다.

## Scope

이 디렉터리는 현재 유효한 ADR을 보유한다. 각 ADR은 하나의 material
choice를 소유하고 실제 Architecture Description을 parent로 연결한다.
개수는 유지 기준이 아니므로 아래 Current Inventory와 실제 파일 목록이
권위이다.

## Structure

```text
docs/02.architecture/decisions/
├── 0001-traefik-nginx-hybrid.md
├── 0002-keycloak-oauth2-proxy-choice.md
├── ...
├── 0028-local-isolated-readiness-evidence.md
├── 0032-canonical-agent-governance-home.md
├── 0034-canonical-knowledge-and-prompt-surfaces.md
├── 0037-package-disposition-wait-and-task-cancellation.md
├── 0038-selective-native-oidc-for-native-auth-apps.md
├── 0042-openbao-unseal-method.md
├── 0044-readme-navigation-and-document-language.md
├── 0046-capability-tiers-and-quality-boundary.md
├── 0047-dev-timescale-influx-retirement-and-load-tools.md
├── 0048-authority-parents-and-criterion-acceptance.md
├── 0049-shared-agent-memory-store.md
├── 0050-openbao-as-secrets-manager.md
├── 0051-summarize-and-delete-retirement.md
├── 0052-kafka-only-messaging-broker.md
├── 0053-observability-storage-on-seaweedfs.md
├── 0054-mailpit-home-stalwart-lab.md
├── 0055-segmented-per-flow-networks.md
├── 0056-offsite-backup-target-and-size-cap.md
├── 0057-operations-role-and-domain-folders.md
├── 0058-home-tiers-versus-labs.md
├── 0059-native-oidc-open-webui-and-airflow.md
├── 0060-hermes-report-source-contract.md
└── README.md
```

### Current Inventory

- `ADR-0001`부터 `ADR-0028`: 기본 tier와 service selection, hardening, HA, network,
  readiness evidence decisions. 위 Structure의 파일 목록이 현재 남은 번호이다.
- 삭제된 번호 `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0009`~`ADR-0016`,
  `ADR-0018`~`ADR-0020`, `ADR-0022`~`ADR-0027`, `ADR-0029`~`ADR-0031`, `ADR-0033`,
  `ADR-0035`, `ADR-0036`, `ADR-0039`~`ADR-0041`, `ADR-0043`, `ADR-0045`는
  Registry `reserved_history`에 있다. 계보: ADR-0050이 ADR-0003과 ADR-0018을,
  ADR-0032가 ADR-0029를, ADR-0037이 ADR-0036을 대체했다. 2026-11-06 소유자 결정으로
  ADR-0052가 ADR-0005·ADR-0020을, ADR-0053이 ADR-0006을, ADR-0054가 ADR-0010을,
  ADR-0055가 ADR-0026을, ADR-0056이 ADR-0041을, ADR-0057이 ADR-0043을,
  ADR-0058이 ADR-0009·ADR-0024·ADR-0025·ADR-0039·ADR-0040·ADR-0045(앞서
  ADR-0039·ADR-0040이 대체한 ADR-0015·ADR-0019 포함)을, ADR-0059가 ADR-0016·ADR-0022·
  ADR-0023을 대체했다. 본문은 버전 이력에 있다. ADR-0046은 완료된 Task가 링크하므로 유지하며, LAB 배치는
  ADR-0058이 정한다.
- [`ADR-0028`](./0028-local-isolated-readiness-evidence.md):
  local-isolated readiness evidence 전략을 채택한 accepted decision.
- [`ADR-0032`](./0032-canonical-agent-governance-home.md):
  공통 정본의 `.agents` 이전과 native 로딩 경계를 채택한 accepted decision.
- [`ADR-0034`](./0034-canonical-knowledge-and-prompt-surfaces.md):
  `.agents/knowledge/`와 `.agents/prompts/`를 canonical category로 도입하는
  accepted decision.
- [`ADR-0037`](./0037-package-disposition-wait-and-task-cancellation.md):
  모든 구성원이 terminal인 완료 package의 처분 대기와, 구조화된 취소 근거를 가진
  cancelled Task, 현재 재평가·history-only 이용 가능성·새 포착의 정확 동일성을
  채택한 accepted decision. ADR-0036을 대체하며 SPEC-0179(삭제됨, 버전 이력)가 구현·검증했다.
  처분 대기를 다룬 결정 1(마지막 문장 제외)과 결정 2·3의 완료 receipt 조항은 ADR-0048이
  대체하고, 취소 기록·terminal Plan·terminality 규칙은 그대로 유지된다.
  결정 4~10과 결정 1의 마지막 문장은 ADR-0051이 대체한다.
- [`ADR-0038`](./0038-selective-native-oidc-for-native-auth-apps.md):
  Keycloak을 중앙 IdP로 유지하면서 Gateway ForwardAuth와 application-native
  OIDC를 서비스별로 선택하고 Airflow/Kafbat UI의 이중 인증을 금지하는
  accepted decision.
- [`ADR-0042`](./0042-openbao-unseal-method.md):
  auto-unseal을 연기하고 수동 Shamir unseal을 유지하는 accepted decision.
  owner와 재검토 trigger를 담는다(SPEC-0182 W10).
- [`ADR-0044`](./0044-readme-navigation-and-document-language.md):
  README navigation과 문서 언어를 워크스페이스 전체에서 하나의 강제 계약으로
  통합하는 accepted decision(SPEC-0184).
- [`ADR-0046`](./0046-capability-tiers-and-quality-boundary.md):
  Quality 신설과 관리·연구 패키지의 기능별 tier 재배치를 정한 accepted decision(SPEC-0197). LAB 배치는 ADR-0058이 정한다.
- [`ADR-0047`](./0047-dev-timescale-influx-retirement-and-load-tools.md):
  DEV TimescaleDB 결과 저장, InfluxDB 퇴역, k6 기본·Locust LAB 선택을 정한 accepted decision(SPEC-0212, SPEC-0213).
- [`ADR-0048`](./0048-authority-parents-and-criterion-acceptance.md):
  Spec·Plan은 승인 권한만, Task는 실행 상태를, criterion마다 하나의 수용 판정을
  두고 보관 검토 준비를 읽을 때 계산하는 accepted decision. ADR-0037 결정 1(마지막
  문장 제외)과 결정 2·3의 완료 receipt 조항을 대체하며 SPEC-0231과 SPEC-0233이 구현·검증했고
  두 Spec은 삭제되었다.
- [`ADR-0049`](./0049-shared-agent-memory-store.md):
  Claude와 Codex가 main checkout의 SQLite 저장소 하나를 함께 쓰고 native
  memory를 끄는 accepted decision. CLI만 쓰고 rollback journal과 논리 한도를
  쓴다. ADR-0032의 memory·`.codex/config.toml` 금지를 이 두 항목에 한해 좁히며
  SPEC-0236(삭제됨, 버전 이력)이 구현·검증했다.
- [`ADR-0050`](./0050-openbao-as-secrets-manager.md):
  OpenBao와 `openbao-agent`를 secrets manager로 채택하며 ADR-0003, ADR-0018을 supersede한 accepted decision.
- [`ADR-0051`](./0051-summarize-and-delete-retirement.md):
  은퇴 문서를 01·02 문서에 요약한 뒤 삭제하고 Git 이력을 기록으로 삼으며, 폐기 번호를
  Registry `reserved_history`에 두는 accepted decision. 소유자가 2026-11-03에 채택을 결정했고
  SPEC-0249 병합 직후 accepted가 되었다. ADR-0037 결정 4~10과 결정 1의
  마지막 문장을 대체한다.
- [`ADR-0052`](./0052-kafka-only-messaging-broker.md):
  KRaft 모드 Kafka를 유일한 messaging broker로 두고 RabbitMQ를 철회하는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0053`](./0053-observability-storage-on-seaweedfs.md):
  LGTM stack과 Alloy를 유지하고 Loki·Tempo object store를 SeaweedFS S3로 두는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0054`](./0054-mailpit-home-stalwart-lab.md):
  HOME SMTP trap은 Mailpit, Stalwart는 미승격 LAB으로 두는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0055`](./0055-segmented-per-flow-networks.md):
  `10.250.0.0/16` 안의 흐름별 `/24` 분리 network와 필요한 곳에만 고정 IP를 두는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0056`](./0056-offsite-backup-target-and-size-cap.md):
  Cloudflare R2 offsite 사본과 10 GB 상한 아래 9 GB upload 거부를 정한 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0057`](./0057-operations-role-and-domain-folders.md):
  Stage 05 문서를 `<role>/<NN-domain>/####-<slug>.md`에 두고 domain 폴더마다 README를 두는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0058`](./0058-home-tiers-versus-labs.md):
  root include를 HOME tier 구성원으로, `labs/`를 LAB으로 나누고 tier별 소유·하드닝 gate를 정한 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0059`](./0059-native-oidc-open-webui-and-airflow.md):
  Open WebUI와 Airflow UI를 ForwardAuth 없이 native OIDC로 두고 workflow·AI 하드닝을 잇는 accepted decision. 소유자가 2026-11-06에 채택했다.
- [`ADR-0060`](./0060-hermes-report-source-contract.md):
  Hermes `source_text`를 확정된 전체 일일 보고서 원문으로 두고 receipt 집합은 비공개 감사 기록으로 보존하는 proposed decision.

## Usage

### Audience

- System Architects
- Developers
- Reviewers

### Authoring Flow

1. 상위 [Architecture Description](../descriptions/README.md)을 확인한다.
2. 기존 ADR이 같은 선택을 이미 소유하는지 확인한다.
3. 새 ADR은 [`decision.template.md`](../../99.templates/templates/architecture/decision.template.md)를 사용한다.
4. 선택, alternatives, rationale와 consequences를 보존한다.
5. 이전 결정을 대체하면 새 ADR의 Traceability에 대체한 내용을 요약하고, 이전
   ADR은 삭제한 뒤 번호를 Registry `reserved_history`에 둔다. `supersedes`,
   `superseded_by` metadata와 `deprecated`·`superseded` 상태는 쓰지 않는다.

### Documentation Standards

- `<4-digit-id>-<slug>.md`, `artifact_id: ADR-<4-digit-id>`,
  `type: sdlc/architecture-decision`을 일치시킨다.
- `parent_ids`는 실제 Architecture Description만 포함한다.
- 구현 계약과 검증 기준은 관련 Spec, 운영 절차는 Stage 05에 둔다.
- 결정 확인 근거가 없는 runtime 상태는 주장하지 않는다.

## Related Documents

- [에이전트 작업 규칙](../AGENTS.md)
- [Architecture](../README.md)
- [Architecture Descriptions](../descriptions/README.md)
- [Product Requirements](../../01.requirements/README.md)
- [Specifications](../../03.specs/README.md)
- [Operations](../../05.operations/README.md)
- [ADR Template](../../99.templates/templates/architecture/decision.template.md)
