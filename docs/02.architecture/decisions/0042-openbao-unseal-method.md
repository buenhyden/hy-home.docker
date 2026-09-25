---
title: "OpenBao Unseal Method"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "architecture"
artifact_id: "ADR-0042"
parent_ids:
- "AD-0003"
created: "2026-09-25"
---

# ADR-0042: OpenBao Unseal Method

## Context

OpenBao는 [Compose](../../../infra/03-security/openbao/docker-compose.yml)가 고정한 2.6 계열 이미지로, 단일 노드 Raft로 돈다. Compose의 `BAO_LOCAL_CONFIG`에는
`seal` stanza가 없으므로 기본 Shamir seal이다. RUN-0085에 따라 share는 3개, threshold는 2다.
owner 결정(2026-09-22)으로 세 share는 한 파일 `secrets/security/openbao_unseal_keys.txt`
(SEC-003, `0600`, Git 제외, 컨테이너에 마운트하지 않음)에 함께 있다. 이 파일을 읽을 수 있는
사람은 OpenBao를 unseal할 수 있다. 그리고 이 파일은 host Restic 저장소에도 BKP-002로
암호화되어 들어간다.

auto-unseal은 Vault 시절 ADR-0018에서 "이번 단계에서 KMS/HSM auto-unseal 실구현"을
non-goal로 두고 미뤘을 뿐, 결정한 적이 없다.

재부팅이나 OpenBao 재시작 뒤 현재 순서는 다음과 같다.

1. OpenBao가 sealed로 뜬다. healthcheck는 sealed(`bao status` rc 2)도 통과로 보므로
   `openbao-agent`는 곧바로 시작한다.
2. owner가 대화형 터미널에서 `bao operator unseal`로 share 두 개를 넣는다.
3. Agent는 SecretID 파일을 읽은 뒤 지우므로(`remove_secret_id_file_after_reading = true`)
   재시작하면 다시 인증할 수 없다. owner가 OIDC로 로그인해 새 SecretID(10분, 1회용)를
   발급하고 Agent volume에 넣어야 한다(RUN-0085 delivery 절차).
4. hy-home.k8s의 External Secrets는 Kubernetes auth로 OpenBao를 읽으므로 unseal 전까지
   동기화하지 못한다.

**버전 확인** (OpenBao 공식 문서 2.6.x, 2026-09-25 조회):

- 2.6.x 바이너리에 내장된 seal: AliCloud KMS, AWS KMS, Azure Key Vault, GCP Cloud KMS,
  KMIP, OCI KMS, OVHcloud KMS, PKCS#11, Static Key, T Cloud Public KMS, OpenBao Transit.
- v2.6.0부터 내장되지 않은 방식은 외부 KMS plugin으로 설치할 수 있다. v2.7.0부터는 많은
  내장 방식이 standalone 바이너리에서 빠지고 plugin으로만 제공된다. 따라서 2.7로 올리면
  cloud KMS나 PKCS#11 seal은 plugin 등록이 필요할 수 있다.
- PKCS#11은 2.6.x에서도 cgo로 컴파일한 HSM 빌드 또는 openbao-plugins의 plugin이 필요하다.
  공식 이미지가 HSM 빌드인지는 문서에 없다.
- Static Key seal은 32바이트 AES-256-GCM 키를 설정, `env://`, `file://`로 받는다. 문서는
  "이미 신뢰의 근원(예: 다른 서드파티 secrets manager)이 있을 때만" 권한다.
- Transit seal은 transit 서버가 시작과 unseal 시점에 닿아야 하며, 주기적(periodic) orphan
  token을 권한다.

## Decision Drivers

- 재부팅 뒤 owner 없이 서비스가 돌아와야 하는가(현재는 unseal과 SecretID 모두 owner 필요).
- unseal 재료가 host와 같은 곳에 있으면 auto-unseal은 보안 경계가 아니라 편의일 뿐이다.
- 새 외부 의존성(클라우드 계정, 다른 기기)이 복구 경로를 막지 않아야 한다.
- seal 전환은 되돌리기 어렵다. Shamir에서 auto-unseal로 옮기면 share는 unseal key가 아니라
  recovery key가 되어 unseal에는 쓸 수 없다.
- W11 cold start 런북과 Agent SecretID 전달 방식에 주는 영향.

## Options Considered

| 옵션 | 무인 재부팅 | 키 위치 | 새 의존성 | W11 영향 |
| --- | --- | --- | --- | --- |
| (a) 수동 Shamir 유지 | 아니오 | host 파일 SEC-003 (현행) | 없음 | unseal 단계를 owner가 수행 |
| (b) 다른 OpenBao/Vault의 transit | 예 (transit 서버가 살아 있으면) | 다른 기기의 transit key | 둘째 서버와 네트워크 | transit 서버를 먼저 띄우는 순서 |
| (c) cloud KMS (AWS/GCP/Azure 등) | 예 (인터넷과 KMS가 되면) | 클라우드 KMS | 클라우드 계정, egress | 인터넷 없이는 시작 불가 |
| (d) Static Key 또는 PKCS#11 (같은 host) | 예 | host 파일 또는 SoftHSM | 없음(Static) 또는 HSM 빌드/plugin | unseal 단계가 사라짐 |
| (e) 연기 (owner와 trigger 기록) | 아니오 | 현행 | 없음 | (a)와 같음 |

### (a) 수동 Shamir unseal 유지 (현행)

- **Good**: 변경이 없다. seal key가 컨테이너 설정이나 환경에 없다. 외부 의존성이 없다.
- **Bad**: 재부팅과 OpenBao 재시작마다 owner가 필요하다. 세 share가 한 파일에 있으므로
  분리 보관의 이점은 이미 없다.
- **Agent SecretID**: 변화 없음. 재부팅마다 owner가 SecretID도 전달한다.

### (b) 둘째 OpenBao/Vault의 transit auto-unseal

- **방법**: 다른 인스턴스에 transit engine과 key를 두고, 이 서버의 `seal "transit"`에 주소,
  key 이름, periodic orphan token을 준다.
- **어디서 돌리나**: 같은 host에서 돌리면 목적이 없다. transit 서버 자체가 unseal돼야 하고,
  host를 가진 공격자는 둘 다 가진다. 다른 기기(NAS, 다른 PC, 소형 VPS)에 두어야 한다.
  hy-home.k8s는 같은 host의 컨테이너이므로 해당하지 않는다.
- **Good**: 클라우드 계정 없이 무인 재부팅. 키가 이 host 밖에 있다.
- **Bad**: 둘째 서버도 자기 unseal 문제를 가진다(보통 수동 Shamir). 그 서버가 꺼져 있으면
  이 서버는 시작하지 못한다. token 관리, TLS, 네트워크 경로가 새로 생긴다.
- **Agent SecretID**: 변화 없음.

### (c) cloud KMS auto-unseal

- **방법**: 현재 2.6 계열에 내장된 `awskms`, `gcpckms`, `azurekeyvault` 등. 자격 증명은 환경 변수나
  파일로 준다(문서는 설정 파일보다 환경 변수를 강하게 권함).
- **Good**: 키가 host 밖(KMS)에 있고 KMS 감사 로그가 남는다. 비용은 key 하나와 적은 호출이라
  월 약 $1 수준(정가 기준 추정). host 도난 시 KMS 접근을 끊으면 데이터를 열 수 없다.
- **Bad**: 인터넷이나 KMS가 안 되면 OpenBao가 시작하지 못한다(home lab 회선 장애 = 비밀 저장소
  장애). KMS 접근 키가 host에 있으므로 host가 살아 있는 동안에는 host 탈취자도 unseal할 수
  있다. v2.7.0 이후 plugin 등록으로 바뀔 수 있다. 새 클라우드 자격 증명(새 SEC 행)과
  OpenBao 컨테이너의 egress가 필요하다.
- **Agent SecretID**: 변화 없음.

### (d) Static Key 또는 PKCS#11 seal (같은 host)

- **방법**: `seal "static"`에 32바이트 키를 `file://`로 주고, 그 파일을 Docker Secret으로
  마운트한다. PKCS#11은 SoftHSM 같은 소프트웨어 토큰에 key를 두지만 HSM 빌드나 plugin이 필요하다.
- **보안 trade-off**: 키가 같은 host에 있으므로 host나 OpenBao 컨테이너를 가진 사람은 unseal할 수
  있다. 현재도 SEC-003 한 파일로 같은 일이 가능하므로 **host 탈취에 대한 보호는 크게 달라지지
  않는다**. 달라지는 점은 두 가지다. 키가 컨테이너에 마운트되어 컨테이너 탈출 없이도 노출될 수
  있고, Raft snapshot과 키가 같은 백업에 함께 있으면 snapshot만 가져간 사람도 열 수 있다.
  SoftHSM은 key 파일이 디스크에 있으므로 Static Key보다 나을 것이 없다. 공식 문서는
  Static Key를 기존 신뢰 근원이 있을 때만 권한다.
- **Good**: 외부 의존성 없이 무인 재부팅.
- **Bad**: seal 보호가 사실상 파일 권한으로 줄어든다. seal 전환(`-migrate`)과 recovery key
  체계 전환이 필요하다.
- **Agent SecretID**: 변화 없음.

### (e) 연기 (owner와 trigger 기록)

(a)를 유지하면서 criterion 10에 맞게 owner와 재검토 trigger를 적는다. 후보 trigger:

- 계획하지 않은 재부팅이나 정전으로 OpenBao가 owner 부재 중 sealed 상태로 24시간 넘게 머묾.
- hy-home.k8s나 다른 서비스가 OpenBao를 부팅 직후 필수로 요구하게 됨.
- ADR-0041에서 클라우드 제공자를 고름(같은 계정의 KMS를 검토할 근거가 생김).
- OpenBao 2.7 업그레이드(seal 방식이 plugin으로 바뀌는 시점).

## Decision

**Pending owner decision.** owner가 아래에서 하나를 고른다.

- (a) 수동 Shamir unseal 유지
- (b) 다른 기기의 OpenBao/Vault transit auto-unseal
- (c) cloud KMS auto-unseal (AWS KMS, GCP Cloud KMS, Azure Key Vault 등)
- (d) 같은 host의 Static Key 또는 PKCS#11 seal
- (e) 연기: owner와 trigger 또는 날짜를 적는다

작성자 권고: **(e) 연기, (a) 유지**. owner는 @buenhyden, trigger는 위 목록 가운데 먼저 오는 것.

- auto-unseal만으로는 무인 재부팅이 되지 않는다. Agent는 재시작마다 owner가 발급한 1회용
  SecretID가 필요하므로 owner는 어차피 재부팅 절차에 들어간다.
- 같은 host 키(d)는 보안 이득 없이 키 노출 면만 넓힌다. 다른 기기(b)나 클라우드(c)는 새
  가용성 의존을 만든다. 지금 규모에서 이 비용이 이득보다 크다.
- 무인 재부팅이 실제 요구가 되면 먼저 Agent 인증 방식(SecretID 전달)을 함께 바꾸는 결정이
  필요하다. 그때 (c) 또는 (b)를 이 ADR을 대체하는 새 ADR로 다시 연다.

## Consequences

- **W11 cold start 런북**:
  - (a)/(e): 순서는 OpenBao 시작 → owner unseal(share 2개, 숨김 입력) → OIDC 로그인 →
    SecretID 발급과 Agent 전달 → Agent 인증 확인 → hy-home.k8s External Secrets 동기화 확인.
    unseal과 SecretID 단계에 owner 시간이 기록된다.
  - (b)/(c)/(d): unseal 단계가 자동이 되지만 SecretID 전달 단계는 남는다. (b)는 transit 서버
    선기동, (c)는 인터넷과 KMS 확인이 런북 선행 조건이 된다.
- **Agent SecretID**: 모든 옵션에서 1회용 SecretID 전달은 그대로다. 이를 없애려면 SecretID
  수명·횟수를 늘리거나 다른 auth method를 쓰는 별도 결정이 필요하고, 그것은 이 ADR의 범위가
  아니다.
- **seal 전환 시**: share가 recovery key로 바뀐다. RUN-0085의 generate-root와 break-glass
  절차, SEC-003 설명, POL-0021 OpenBao 행, 새 SEC 행(키 또는 KMS 자격 증명)을 함께 고친다.
  전환 전 보호된 Raft snapshot과 격리 복구 리허설이 필요하다.

## Traceability

- Parent: [AD-0003 Security Architecture](../descriptions/0003-security-architecture.md)
- Earlier deferral: [ADR-0018](0018-vault-hardening-and-ha-expansion-strategy.md)
- Spec: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md) criterion 10 and 11,
  Plan W10/W11,
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- Runbook: [RUN-0085](../../05.operations/catalog/03-security/0085-openbao/runbook.md)
- Runtime sources: [OpenBao Compose](../../../infra/03-security/openbao/docker-compose.yml),
  [Agent configuration](../../../infra/03-security/openbao/config/agent.hcl)

## Follow-up

- owner 결정 뒤 이 ADR을 `accepted`로 올리고 Decision 절을 선택한 옵션으로 다시 적는다.
- W11 런북은 결정 시점에 실제로 쓰는 unseal 방식을 적는다.
- 연기라면 owner와 trigger를 Task 0003의 Deferred Items에 적는다.

### Official references

- [OpenBao seal configuration (2.6.x)](https://openbao.org/docs/2.6.x/configuration/seal/)
- [Static Key seal](https://openbao.org/docs/configuration/seal/static/)
- [Transit seal](https://openbao.org/docs/configuration/seal/transit/)
- [PKCS#11 seal (2.6.x)](https://openbao.org/docs/2.6.x/configuration/seal/pkcs11/)
- [AWS KMS seal](https://openbao.org/docs/configuration/seal/awskms/)
