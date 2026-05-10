---
status: migrated
---
<!-- Target: docs/05.operations/08-ai/local-llm-setup.md -->

# Local Llm Setup Operations

> Migrated from `docs/05.operations/08-ai/local-llm-setup.md` during the 2026-05-10 operations taxonomy consolidation.

## Usage

### Local LLM Setup Usage

How to pull, test, and use language models with the local Ollama engine.

#### 1. Prerequisites

- Docker stack must be running (`ollama` service active).
- GPU acceleration should be verified (`nvidia-smi` working on host).

#### 2. Pulling Models

Execute the following to download a model (e.g., Llama 3):

```bash
docker exec -it ollama ollama pull llama3
```

#### 3. Verification

Verify the model is loaded and responding:

```bash
docker exec -it ollama ollama run llama3 "Hello, how are you?"
```

#### 4. Integration with Open WebUI

Once pulled, the model will automatically appear in the [Open WebUI](https://chat.${DEFAULT_URL}) selection dropdown.

---

#### Overview (KR)

이 문서는 `docs/05.operations/08-ai/local-llm-setup.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

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

#### Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
