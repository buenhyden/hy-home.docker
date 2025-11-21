# MinIO

**MinIO**는 고성능 S3 호환 객체 스토리지입니다.
클라우드 네이티브 애플리케이션을 위한 데이터 저장소로 사용됩니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **minio** | Object Storage 서버 | `9000` (API), `9001` (Console) |

## 🛠 설정 및 환경 변수

- **콘솔 접속**: `http://localhost:9001`
- **인증**: Docker Secret(`minio_root_user`, `minio_root_password`)을 통해 관리자 계정 설정.

## 📦 볼륨 마운트

- `minio-data`: 데이터 저장소 (`/data`)

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **Secret**: `/run/secrets/` 경로의 파일을 통해 비밀번호를 관리합니다.
