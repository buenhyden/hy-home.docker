<!-- Target: docs/07.operations/09-tooling/registry.md -->

# Docker Registry Operations Policy

> Private OCI-compliant image distribution service governance.

---

## Overview (KR)

이 문서는 `hy-home.docker` 도커 레지스트리 운영 정책을 정의한다. 이미지의 생명주기 관리, 보안 통제 기준, 그리고 저장 용량 최적화 방법을 규정한다.

## Policy Scope

- `infra/09-tooling/registry` 내에서 구동되는 서비스.
- 저장소 내 모든 컨테이너 이미지 및 OCI 아티팩트.

## Applies To

- **Systems**: Internal Docker Registry v2.
- **Agents**: CI/CD Pipelines, Internal Developers.
- **Environments**: Production (On-premise).

## Controls

- **Required**:
  - `REGISTRY_STORAGE_DELETE_ENABLED: "true"` 설정 유지 (GC를 위해 필수).
  - 이미지 푸시 전 태그 컨벤션 준수 (`registry:<port>/<project>/<image>:<tag>`).
- **Allowed**:
  - `insecure-registries`를 통한 내부 망 접근.
- **Disallowed**:
  - 외부 공인 IP를 통한 레지스트리 직접 노출 금지.

## Exceptions

- 대용량 데이터셋(이미지 외) 저장은 MinIO를 우선 활용하며, 레지스트리 저장 허용 시 별도 승인 필요.

## Verification

- `docker-compose.yml` 환경 변수 설정값 정기 점검.
- `${DEFAULT_REGISTRY_DIR}` 디스크 사용량 임계치(90%) 알림 모니터링.

## Review Cadence

- Quarterly

## AI Agent Policy Section (If Applicable)

- **Registry Access**: 에이전트는 프라이빗 레지스트리의 이미지를 풀(Pull)할 수 있으나, 프로덕션 태그(`v*`)에 대한 푸시는 휴먼 게이트 승인이 필요함.

## Related Documents

- **ARD**: [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md)
- **Procedure**: [../07.operations/09-tooling/registry.md](../../07.operations/09-tooling/registry.md)

## Usage

> Migrated from `docs/07.operations/09-tooling/registry.md` during the 2026-05-10 operations taxonomy consolidation.

### Docker Registry Usage

> Private OCI-compliant image distribution service.

---

#### Overview (KR)

이 문서는 `hy-home.docker`에서 운영하는 프라이빗 도커 레지스트리(Docker Registry v2)에 대한 가이드다. 내부 이미지를 저장하고 배포하는 절차와 주의사항을 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- CI/CD Developers

#### Purpose

- 프라이빗 레지스트리를 통한 내부 이미지 배포 자동화 및 보안 강화.
- 외부 레지스트리 의존성 없이 로컬 네트워크 내에서의 빠른 이미지 풀(Pull)/푸시(Push).

#### Prerequisites

- Docker Engine 및 Docker Compose 설치.
- `insecure-registries` 설정 (HTTPS 미적용 시).
- `REGISTRY_PORT` (기본 5000) 접근 가능 여부 확인.

#### Step-by-step Instructions

##### 1. Registry Login (If Auth is Configured)

기본 설정에서는 인증이 비활성화되어 있을 수 있으나, 활성화된 경우 다음 명령어로 로그인한다.

```bash
docker login registry.hy-home.docker:5000
```

##### 2. Image Tagging

로컬 이미지를 레지스트리에 푸시하기 위해 적절한 태그를 부여한다.

```bash
docker tag <local-image>:<tag> registry.hy-home.docker:5000/<project>/<image>:<tag>
```

##### 3. Image Push

```bash
docker push registry.hy-home.docker:5000/<project>/<image>:<tag>
```

##### 4. Image Pull

```bash
docker pull registry.hy-home.docker:5000/<project>/<image>:<tag>
```

#### Common Pitfalls

- **Insecure Registry Error**: `http` 프로토콜을 사용하는 경우, Docker 데몬 설정(`/etc/docker/daemon.json`)에 `insecure-registries` 항목으로 추가해야 한다.
- **Disk Space**: 대량의 이미지가 누적되면 호스트 디스크가 가득 찰 수 있다. 가비지 컬렉션(GC)을 주기적으로 실행해야 한다.
- **Service Down**: 레지스트리 컨테이너가 중단되면 CI/CD 파이프라인 전체가 실패하므로 헬스체크 모니터링이 필수적이다.

#### Related Documents

- **Spec**: [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md)
- **Operation**: [../07.operations/09-tooling/registry.md](../../07.operations/09-tooling/registry.md)
- **Procedure**: [../07.operations/09-tooling/registry.md](../../07.operations/09-tooling/registry.md)

## Procedure

> Migrated from `docs/07.operations/09-tooling/registry.md` during the 2026-05-10 operations taxonomy consolidation.

### Registry Recovery Procedure

Procedure for recovering the local Docker registry in the `09-tooling` tier.

#### Symptoms

- `Error: response from daemon: Get https://registry.hy-home.com/v2/: dial tcp ...`
- Container `registry` is in `restarting` state.

#### Recovery Steps

1. Verify storage mounts: `df -h ${DEFAULT_DATA_DIR}/registry`
2. Restart service: `docker compose restart registry`
3. Verify logs: `docker compose logs -f registry`

#### Related Documents

- [Operations](../../07.operations/09-tooling/registry.md)

---

#### Overview (KR)

이 런북은 `docs/07.operations/09-tooling/registry.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../07.operations/README.md](../../07.operations/README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
