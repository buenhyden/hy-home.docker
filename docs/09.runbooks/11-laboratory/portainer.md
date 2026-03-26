# Portainer Runbook

> 관리자 비밀번호 복구 및 서비스 장애 해결 절차.

---

## Overview (KR)

이 런북은 Portainer 관리 계정 접근 불능 사유 발생 시 비밀번호를 초기화하거나, 서비스 시작 불능 상황을 복구하는 절차를 제공한다.

## Procedure or Checklist

### 1. Admin Password Reset

Portainer 내부 DB의 관리자 비밀번호를 수동으로 재설정해야 하는 경우 다음을 수행한다.

1. Portainer 컨테이너 중지:

   ```bash
   docker compose down
   ```

2. 비밀번호 초기화 헬퍼 도구 실행 (데이터 볼륨 사용):

   ```bash
   docker run --rm -v portainer_data:/data portainer/helper-reset-password
   ```

   *참고: 출력되는 임시 비밀번호를 기록한다.*

### 3. Stack Deployment

1. 'Stacks' 메뉴에서 Docker Compose 파일을 직접 업로드하거나 붙여넣어 배포할 수 있다.

### Implementation Snippet

### Service Configuration
 Issues

Portainer가 로컬 Docker 환경에 연결하지 못하는 경우:

1. `docker-compose.yml`의 볼륨 섹션에서 `/var/run/docker.sock` 매핑 여부를 확인한다.
2. 호스트의 socket 권한 확인: `ls -l /var/run/docker.sock`.
3. Portainer 로그 확인: `docker| Storage | `portainer_data` | Persistent volume for config |

### Traefik Integration

데이터베이스 오염으로 인해 실행되지 않는 경우:

1. 백업된 `${DEFAULT_MANAGEMENT_DIR}/portainer` 데이터를 복원한다.
2. 기존 볼륨을 삭제하고 새 데이터를 배치한 뒤 재시작한다.

## Verification Steps

- [ ] `https://portainer.${DEFAULT_URL}` 로그인 후 'Home' 대시보드에 로컬 환경이 'Active' 상태인지 확인.
- [ ] 'Containers' 목록이 정상적으로 업데이트되는지 확인.

## Related Documents

- **Operations**: `[../../08.operations/11-laboratory/portainer.md]`
- **System Guide**: `[../../07.guides/11-laboratory/portainer.md]`
