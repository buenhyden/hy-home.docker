---
status: active
---
<!-- Target: docs/05.operations/guides/00-workspace/developer-setup.md -->

# Developer Setup Operations

## Usage

### Overview (KR)

이 문서는 `docs/05.operations/guides/00-workspace/developer-setup.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

### Developer Environment Setup Usage

This guide defines the required local environment configuration and permissions for contributing to the `hy-home.docker` ecosystem.

#### 1. Context & Objective

- **Purpose**: To standardize the local development environment across different machines.
- **Goal**: Ensure agents have sufficient but safe permissions to execute build and validation scripts.

#### 2. Recommended Permissions (Claude Code)

To interact effectively with the infrastructure, your `.claude/settings.local.json` should include the following permission patterns:

##### Infrastructure & Validation

- `Bash(scripts/validation/validate-docker-compose.sh:*)`
- `Bash(docker:*)`
- `Bash(docker-compose:*)`

##### Development Tools

- `Bash(npm run:*)`
- `Bash(npx tsc:*)`
- `Bash(python3:*)`

##### File System Access

- `Read(docs/**)`
- `Read(infra/**)`

#### 3. Tool Configuration

##### Shell Environment

All scripts assume a bash-compatible shell. If you are on Windows, use WSL2.

##### Local Settings Pruning

- Avoid absolute paths (e.g., `D:/blog-data/...`) in shared settings.
- Use `$CLAUDE_PROJECT_DIR` for relative referencing in hooks.

#### 4. Operational Procedures

##### Initial Setup

1. Clone the repository.
2. Ensure Docker and Docker Compose (v2.x) are installed.
3. Copy `.env.example` to `.env` and fill only local values required by the
   selected profiles.
4. For local TLS development, install `mkcert` and generate local files
   without printing key material:

   ```bash
   set -euo pipefail
   [ -f .env ] || { echo ".env is required"; exit 1; }
   set -a
   . ./.env
   set +a
   domain="${DEFAULT_URL:-127.0.0.1.nip.io}"
   cert_dir="secrets/certs"
   mkdir -p "$cert_dir"
   mkcert -install
   mkcert -cert-file "$cert_dir/cert.pem" -key-file "$cert_dir/key.pem" "$domain" "*.$domain"
   cp "$(mkcert -CAROOT)/rootCA.pem" "$cert_dir/rootCA.pem"
   chmod 600 "$cert_dir/key.pem"
   chmod 644 "$cert_dir/cert.pem" "$cert_dir/rootCA.pem"
   ```

5. Run `bash scripts/validation/validate-docker-compose.sh` to verify your local setup.

#### 5. Maintenance & Safety

- **Security**: Never add `allow: ["*"]` permissions. Always scope permissions to specific tools or directories.
- **Secrets**: Ensure your local `.env` is never committed; use `secrets/SENSITIVE_ENV_VARS.md.example` as a template.

---

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Operations index](../../README.md)
