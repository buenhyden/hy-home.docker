# HashiCorp Vault Integration Guide

## 1. 개요 (Overview)

**HashiCorp Vault**는 현대적인 인프라 환경에서 **Secrets(비밀값)**, **Encryption(암호화)**, **Identity(신원)** 관리를 중앙집중화하는 업계 표준 솔루션입니다.
`hy-home.docker` 환경에서 Vault를 도입함으로써 단순한 서비스별 `.env` 기반의 관리를 넘어, **동적 시크릿(Dynamic Secrets)**, **데이터 암호화(Encryption-as-a-Service)**, **정교한 접근 제어(ACL)** 를 구현할 수 있습니다.

### 1.1 Profile

Vault is **optional** and runs under the `vault` profile.

```bash
docker compose --profile vault up -d vault
```

---

## 2. 도입 목적 및 분석 (Objectives & Analysis)

현재 `hy-home.docker`는 Docker Secrets와 `.env` 파일을 사용하여 비밀번호를 관리하고 있습니다. Vault 도입 시 다음과 같은 이점을 얻을 수 있습니다.

### 2.1 주요 이점

1. **Centralized Secret Management**: 분산된 `.env` 파일의 비밀값을 한 곳에서 안전하게 관리.
2. **Dynamic Secrets (동적 시크릿)**:
    * PostgreSQL, MongoDB 등 데이터베이스 접근 시 **일회용 자격 증명(TTL 포함)** 을 발급하여 보안성 극대화.
    * 애플리케이션이 DB 패스워드를 몰라도 됨.
3. **Data Encryption (Transit Engine)**:
    * 민감 개인정보(PII)를 DB에 저장하기 전 Vault를 통해 암호화. (Application-level Encryption)
4. **PKI Management**:
    * 내부 서비스 간 mTLS 통신을 위한 인증서 발급 및 갱신 자동화 (Traefik, Kafka 등과 연동).
5. **Audit Logging**: 누가, 언제, 어떤 비밀값에 접근했는지에 대한 완벽한 감사 로그 제공.

### 2.2 적합성 분석

`hy-home.docker`는 마이크로서비스 아키텍처(MSA)를 지향하고 있으며, Spring Boot, Go, Python 등 다양한 언어 스택을 사용합니다. Vault는 이들 언어에 대한 SDK와 통합 라이브러리(Spring Cloud Vault 등)를 훌륭하게 지원하므로 매우 적합합니다.

---

## 3. 아키텍처 설계 (Architecture Design)

### 3.1 배포 모델

* **Storage Backend**: Raft (Integrated Storage) - 별도의 Consul 없이 Vault 자체적으로 고가용성 클러스터링 지원.
* **Network**: `infra_net` (172.19.0.0/16) 내부에서 동작하며, 외부 노출은 Traefik을 통해 제어.
* **URL**: `vault.${DEFAULT_URL}` (예: `vault.127.0.0.1.nip.io`)

### 3.2 연동 흐름 (Workflow)

```mermaid
graph TD
    Client[Client / App] -->|1. Auth (AppRole/K8s)| V[Vault]
    V -->|2. Token Issue| Client
    Client -->|3. Request Secret| V
    V -->|4. Generate Dynamic Creds| DB[PostgreSQL / MongoDB]
    DB -->|5. Return Creds| V
    V -->|6. Return Creds| Client
    Client -->|7. Access DB| DB
```

---

## 4. 상세 구성 가이드 (Configuration Guide)

### 4.1 Docker Compose 정의

`infra/vault/docker-compose.yml` 참조.
`hashicorp/vault` 최신 이미지를 사용하며, `IPC_LOCK` capability를 추가하여 메모리 스왑을 방지합니다.

### 4.2 초기 설정 프로세스 (Initialization)

Vault는 처음 실행 시 **Sealed** 상태로 시작됩니다. 데이터를 읽고 쓰기 위해서는 **Unseal** 과정이 필요합니다.

1. **Initialize**: 초기화 및 키 생성

    ```bash
    docker compose exec vault vault operator init
    ```

    * **출력된 Unseal Key 5개와 Root Token을 반드시 안전한 곳(`infra/.env` 등)에 저장하세요.**
    * 예시:

        ```text
        Unseal Key 1: UZ59...
        Unseal Key 2: +jR3...
        ...
        Initial Root Token: hvs....
        ```

2. **Unseal**: 봉인 해제 (3개의 키 필요)

    ```bash
    docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_1}"
    docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_2}"
    docker compose exec vault vault operator unseal "${VAULT_UNSEAL_KEY_3}"
    ```

3. **Login**: 루트 로그인

    ```bash
    docker compose exec vault vault login "${VAULT_ROOT_TOKEN}"
    ```

### 4.3 권장 엔진 활성화

1. **KV (Key-Value) v2**: 일반적인 API Key, 설정값 저장.

    ```bash
    vault secrets enable -path=secret kv-v2
    ```

2. **Database**: PostgreSQL/MongoDB 동적 계정 연동.

    ```bash
    vault secrets enable database
    ```

3. **PKI**: 내부 인증서 발급.

    ```bash
    vault secrets enable pki
    ```

---

## 5. 애플리케이션 연동 패턴

### 5.1 Spring Boot (Spring Cloud Vault)

`bootstrap.yml` 또는 `application.yml` 설정을 통해 애플리케이션 시작 시점에 Vault에서 설정을 주입받음.

```yaml
spring:
  cloud:
    vault:
      host: vault
      port: 8200
      scheme: http
      authentication: APPROLE
      app-role:
        role-id: ${VAULT_ROLE_ID}
        secret-id: ${VAULT_SECRET_ID}
```

### 5.2 Go / Python / Node.js

공식 Vault 클라이언트 라이브러리를 사용하여 API 호출.

---

## 6. 운영 및 보안 고려사항

### 6.1 보안 (Security)

* **Production Hardening**: 프로덕션 환경에서는 반드시 **TLS**를 적용해야 합니다. (Traefik이 TLS를 처리하더라도 내부 통신 암호화 권장)
* **Auto Unseal**: 현재 구성은 수동 Unseal 방식입니다. 서버 재시작 시마다 수동으로 Unseal 해야 합니다. 프로덕션 레벨에서는 AWS KMS, GCP KMS 등을 이용한 Auto Unseal 구성을 권장합니다.
  * *Local 개발 환경에서는 스크립트를 통해 자동화할 수 있으나, Unseal Key가 노출되지 않도록 주의해야 합니다.*
* **Access Control**: Root Token은 초기 설정 및 비상용으로만 사용하고, 평소에는 정책(Policy)이 적용된 사용자 Token이나 AppRole을 사용하세요.

### 6.2 백업 (Backup)

* Raft Storage의 스냅샷 기능을 이용하여 주기적으로 데이터를 백업해야 합니다.

    ```bash
    vault operator raft snapshot save /vault/file/backup.snap
    ```

---

## 7. Vault CLI & Docker 연동 가이드

### 7.1 Docker 컨테이너 내부 실행 (권장)

```bash
docker compose exec vault vault status
```

주요 명령어:

* `vault status`: 상태 확인 (Sealed 여부 등)
* `vault kv put secret/my-app/config key=value`: 시크릿 저장
* `vault kv get secret/my-app/config`: 시크릿 조회

### 7.2 로컬 호스트(PC)에서 실행

로컬 PC에 Vault CLI가 설치된 경우:

1. 환경 변수 설정 (Windows PowerShell)

    ```powershell
    $env:VAULT_ADDR="http://127.0.0.1:8200"
    ```

2. 명령어 실행

    ```bash
    vault status
    ```

### 7.3 문제 해결 (Troubleshooting)

* **Sealed Status**: 컨테이너 재시작 후 `Vault is sealed` 상태가 됩니다. 4.2절의 Unseal 과정을 다시 수행해야 합니다.
* **Connection Refused**: 포트 8200이 열려있는지, 컨테이너가 정상 실행 중인지 확인하세요.
* **Permission Denied**: 볼륨 마운트 경로(`.config`, `vault-data`)의 권한을 확인하세요.

## 8. File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | Vault service definition (IPC_LOCK, ports, volumes). |
| `config/vault.hcl` | Vault server configuration (storage, listener, telemetry). |
| `config/vault.hcl.example` | Template config. |
| `secrets/certs/` | TLS materials for Vault (optional, shared). |
| `README.md` | Integration and operational guidance. |
