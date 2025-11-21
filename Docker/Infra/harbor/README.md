# Harbor

**Harbor**는 오픈 소스 클라우드 네이티브 레지스트리로, 컨테이너 이미지와 헬름 차트를 저장, 서명 및 스캔합니다.
이 구성은 외부 데이터베이스(PostgreSQL)와 Redis(Valkey)를 사용하는 분산형 아키텍처로 설정되어 있습니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **harbor-portal** | 웹 UI 프론트엔드 | `80` (설정에 따라 다름) |
| **harbor-core** | API 및 코어 로직 | - |
| **harbor-registry** | Docker 이미지 저장소 | `5000` |
| **harbor-jobservice** | 비동기 작업 처리 (복제, 스캔 등) | - |
| **harbor-registryctl** | 레지스트리 제어 | - |

## 🛠 설정 및 환경 변수

- **의존성**: PostgreSQL (메타데이터), Redis/Valkey (캐시 및 작업 큐).
- **스토리지**: 로컬 파일 시스템 (`/storage`) 사용. (S3 등으로 변경 가능)
- **보안**: `HARBOR_ADMIN_PASSWORD`로 관리자 비밀번호 설정.

## 📦 볼륨 마운트

- `harbor-registry-data-volume`: 이미지 데이터 (`/storage`)
- `harbor-core-data-volume`: 코어 데이터
- 각 서비스별 설정 및 로그 볼륨

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **인증서**: 프로덕션 환경에서는 HTTPS(TLS) 설정이 필수적입니다.
- **데이터베이스**: `Docker/Infra/postgresql` 및 `Docker/Infra/valkey`가 먼저 실행되어 있어야 합니다.
