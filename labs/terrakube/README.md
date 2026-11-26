---
title: "Terrakube"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
created: "2026-11-26"
---

# Terrakube

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> 자체 PostgreSQL·Valkey·로컬 state를 가진 on-demand Terraform/OpenTofu 협업 플랫폼 LAB입니다.

#### Service

##### Purpose

Terrakube는 독립 Compose project인 [Terrakube LAB](docker-compose.yml)(`lab-terrakube` profile)입니다.
ADR-0062 item 9와 2026-11-26 owner 결정(SPEC-0263 TSK-0004)으로 HOME `09-platform-ops`에서 옮겼습니다.
root Compose에 포함되지 않고 HOME network에 연결되지 않으며 Traefik route도 없습니다. API와 UI는
`${LAB_HOST_BIND_IP}`의 `${LAB_TERRAKUBE_API_HOST_PORT:-18096}`, `${LAB_TERRAKUBE_UI_HOST_PORT:-18097}`에만
게시됩니다. HOME의 IaC 실행은 [OpenTofu](../../infra/09-platform-ops/opentofu/README.md)가 맡습니다.

###### Audience
<!-- core-payload-level:4 -->

이 README의 주요 독자:

- Platform Engineers (LAB 실험)
- Operators (LAB lease와 HOME 퇴역)

###### In Scope
<!-- core-payload-level:4 -->

- `terrakube-api`, `terrakube-ui`, `terrakube-executor`와 LAB 전용 `terrakube-pg`, `terrakube-valkey`.
- Terraform state·plan·실행 output을 API와 executor가 함께 쓰는 LAB 로컬 디렉터리(`StorageType: LOCAL`).
- Keycloak native OIDC(LAB 전용 public client `lab-terrakube`)와 HOME root CA binding.

###### Out of Scope
<!-- core-payload-level:4 -->

- HOME mng-pg·mng-valkey·SeaweedFS: 이 LAB은 쓰지 않습니다.
- Docker socket: executor에 마운트하지 않습니다(owner 결정 2026-11-26).
- Keycloak client 등록과 HOME에 남은 런타임 자원 정리(별도 승인 단계).

###### Structure
<!-- core-payload-level:4 -->

```text
labs/terrakube/
├── docker-compose.yml               # 독립 LAB entrypoint
├── bindings/ca-certificates/type    # Paketo CA binding 표식
├── promotion.yaml                   # SPEC-0263 승격 manifest
└── README.md                        # 이 파일
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_TERRAKUBE_API_HOST_PORT:-18096}` -> 8080 API | terrakube-api | UI, Terraform CLI | Keycloak 발급 token을 issuer `https://keycloak.${LAB_TERRAKUBE_DEFAULT_URL}/realms/hy-home.realm`, client `lab-terrakube`로 검증합니다. | 필수 입력이 비면 render가 거부되고 장애 대응은 RUN-0069를 따릅니다. |
| `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_TERRAKUBE_UI_HOST_PORT:-18097}` -> 8080 UI | terrakube-ui | 브라우저 | redirect URI는 loopback UI 주소이며 Keycloak에 같은 값을 등록해야 합니다. | client가 없거나 redirect가 다르면 로그인이 실패합니다. |
| `terrakube-executor:8090` | terrakube-executor | terrakube-api | LAB network 안에서만 쓰며 internal secret으로 인증합니다. | API health 실패 시 executor는 기동하지 않습니다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

| 항목 | 값 |
| --- | --- |
| Profile·project | `lab-terrakube`, `hy-home-lab-terrakube` |
| Network | `lab_terrakube_net`만 사용 |
| Data | `${LAB_DATA_DIR}/terrakube/{pg,valkey,state}` |
| 필수 입력 | `LAB_TERRAKUBE_DEFAULT_URL`, `LAB_TERRAKUBE_CA_FILE` ([.env.example](../.env.example)) |
| Secret | `${LAB_SECRET_DIR}/terrakube/`의 `db_password.txt`(`LAB-038`), `valkey_password.txt`(`LAB-039`), `pat_secret.txt`(`LAB-040`), `internal_secret.txt`(`LAB-041`) |
| Image | [Compose](docker-compose.yml)가 Terrakube·PostgreSQL·Valkey 이미지를 digest로 고정; `labs/**`는 Renovate와 SEC01 ledger 밖 |

고정한 Terrakube 이미지는 `_FILE` 변수를 읽지 않습니다. Spring `configtree` import가 `/run/secrets`의 각 파일을
같은 이름의 설정으로 읽으므로 secret은 설정 이름(`DatasourcePassword`, `TerrakubeRedisPassword`,
`PatSecret`, `InternalSecret`)을 target으로 마운트합니다. API와 executor는 `-Duser.home=/terrakube-home`로
같은 state volume을 씁니다. HOME Compose의 UI 포트 3000과 output 설정 키는 고정한 이미지와 맞지 않아
이 LAB에서 바로잡았습니다(UI nginx는 8080, output은 state plugin이 저장).

###### Security Boundary
<!-- core-payload-level:4 -->

API와 UI는 loopback bind에만 게시하며 gateway route가 없고 HOME network에 연결되지 않습니다. executor에는
Docker socket이 없습니다. Valkey 비밀번호는 명령행이 아닌 stdin으로 `valkey-server`에 전달합니다.

#### Usage

##### Prerequisites

1. owner가 `${LAB_SECRET_DIR}/terrakube/`에 네 secret 파일을 만듭니다.
2. owner가 Keycloak `hy-home.realm`에 public client `lab-terrakube`(redirect `http://localhost:18097/*`, PKCE)를 등록합니다.
3. `${LAB_DATA_DIR}/terrakube/{pg,valkey,state}` 디렉터리를 만듭니다. image 사용자가 state 디렉터리에 쓸 수 있는지는
   첫 승인 기동에서 확인합니다.

##### Selected Start

1. Usage guide(`docs/05.operations/01.guides/15.labs/0069-terrakube.md`)와 LAB 승격 정책을 읽습니다.
2. `python3 scripts/operations/lab.py check terrakube`로 render와 충돌을 검사합니다.
3. 실제 기동은 secret 사본, Keycloak client와 lease가 있을 때만 `lab.py up`으로 합니다.

#### Checks

##### Readiness

`python3 scripts/operations/lab.py check terrakube`로 render와 충돌을 검사하고
`bash scripts/hardening/check-all-hardening.sh 09-platform-ops`로 no-route·bind·no-socket 계약을 확인합니다.
통과는 실제 기동의 증거가 아닙니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [LAB 목록](../README.md)
- Usage guide(`docs/05.operations/01.guides/15.labs/0069-terrakube.md`) (`GDE-0069`)
- Operations policy(`docs/05.operations/02.policies/15.labs/0069-terrakube.md`) (`POL-0069`)
- Runbook(`docs/05.operations/03.runbooks/15.labs/0069-terrakube.md`) (`RUN-0069`)
- ADR-0062(`docs/02.architecture/02.decisions/0062-home-lab-membership.md`)
- [문서 인덱스](../../docs/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

- 필수 입력이 비면 render가 거부됩니다.
- 장애 대응과 HOME 퇴역 순서는 runbook(`docs/05.operations/03.runbooks/15.labs/0069-terrakube.md`)을 따릅니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
