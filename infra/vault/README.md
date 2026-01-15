# HashiCorp Vault Integration Guide

## 1. 개요 (Overview)

**HashiCorp Vault**는 현대적인 인프라 환경에서 **Secrets(비밀값)**, **Encryption(암호화)**, **Identity(신원)** 관리를 중앙집중화하는 업계 표준 솔루션입니다.
`hy-home.docker` 환경에서 Vault를 도입함으로써 단순한 환경 변수(`<service>/.env`) 기반의 관리를 넘어, **동적 시크릿(Dynamic Secrets)**, **데이터 암호화(Encryption-as-a-Service)**, **정교한 접근 제어(ACL)** 를 구현할 수 있습니다.

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

### 4.1 Docker Compose 정의 (권장)

`infra/vault/docker-compose.yml` (예시)

```yaml
services:
  vault:
    image: hashicorp/vault:1.15
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      VAULT_ADDR: 'http://0.0.0.0:8200'
      VAULT_API_ADDR: 'http://0.0.0.0:8200'
    cap_add:
      - IPC_LOCK
    volumes:
      - vault-data:/vault/file
      - ./config:/vault/config
    command: server
    networks:
      infra_net:
        ipv4_address: 172.19.0.xx
```

### 4.2 초기 설정 프로세스 (Initialization)

1. **Initialize**: `vault operator init` (Unseal Key 5개, Root Token 1개 생성)
2. **Unseal**: `vault operator unseal <KEY>` (최소 3개 키 입력 필요)
3. **Login**: `vault login <ROOT_TOKEN>`

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
      kv:
        enabled: true
      database:
        enabled: true
        role: postgres-readonly
```

### 5.2 Go / Python / Node.js

공식 Vault 클라이언트 라이브러리를 사용하여 API 호출.

---

## 6. 운영 및 보안 고려사항

### 6.1 보안 (Security)

* **Production Hardening**: 프로덕션 환경에서는 반드시 **TLS**를 적용해야 합니다.
* **Unseal Strategy**: 서버 재시작 시마다 수동 Unseal이 필요하므로, AWS KMS나 GCP KMS를 이용한 **Auto Unseal** 구성을 고려하거나, 자동화 스크립트를 주의해서 관리해야 합니다.
* **Access Control**: Root Token은 초기 설정 외에는 사용하지 말고, 용도별 Policy가 적용된 Token이나 AppRole을 사용해야 합니다.

### 6.2 백업 (Backup)

* Raft Storage의 스냅샷 기능을 이용하여 주기적으로 데이터를 백업해야 합니다.

    ```bash
    vault operator raft snapshot save /vault/data/backup.snap
    ```

---

## 7. Vault CLI & Docker 연동 가이드

Vault를 Docker 컨테이너로 실행할 때 CLI를 사용하는 방법에는 크게 두 가지가 있습니다.

### 7.1 Docker 컨테이너 내부 실행 (권장)

별도의 로컬 설치 없이, 실행 중인 Vault 컨테이너 내부의 CLI를 직접 사용하는 방법입니다. 호스트 환경에 영향을 주지 않아 가장 깔끔합니다.

**기본 구문:**

```bash
docker compose exec vault vault <command>
```

**주요 명령어 예시:**

1. **상태 확인**:

    ```bash
    docker compose exec vault vault status
    ```

2. **로그인**:
    (컨테이너 내부는 이미 `VAULT_ADDR=http://127.0.0.1:8200`으로 설정되어 있음)

    ```bash
    docker compose exec vault vault login
    # Token 입력 프롬프트가 뜨면 입력
    ```

3. **시크릿 쓰기 (KV Engine)**:

    ```bash
    docker compose exec vault vault kv put secret/my-app/config apiKey="1234-abcd" dbPass="s3cr3t"
    ```

4. **시크릿 읽기**:

    ```bash
    docker compose exec vault vault kv get secret/my-app/config
    ```

### 7.2 로컬 호스트(PC)에서 실행

로컬 PC(Windows/Mac)에 Vault 바이너리를 설치하고, Docker로 실행 중인 Vault 서버에 원격 접속하는 방법입니다.

1. **Vault CLI 설치**:
    * Windows (Scoop): `scoop install vault`
    * MacOS (Brew): `brew install vault`

2. **환경 변수 설정**:
    로컬 CLI가 Docker 컨테이너의 포트(8200)를 바라보도록 설정합니다.

    * **PowerShell (Windows)**:

        ```powershell
        $env:VAULT_ADDR="http://127.0.0.1:8200"
        ```

    * **Bash/Zsh (Mac/Linux)**:

        ```bash
        export VAULT_ADDR='http://127.0.0.1:8200'
        ```

3. **명령어 실행**:
    이제 `docker compose exec` 없이 바로 `vault` 명령어를 사용할 수 있습니다.

    ```bash
    vault status
    vault login
    ```

### 7.3 문제 해결 (Troubleshooting)

* **http vs https**: 현재 개발 환경 예시는 `http`를 사용합니다. CLI 접속 시 `Error checking seal status: Get "https://..."` 에러가 발생하면 `VAULT_ADDR`에 `http://` 스키마가 명시되었는지 확인하세요.
* **Connection Refused**: `docker compose ps`로 `vault` 컨테이너가 정상 실행(Up) 중인지, 포트 8200이 바인딩되어 있는지 확인해야 합니다.
