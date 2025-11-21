# SonarQube

**SonarQube**는 코드 품질을 지속적으로 검사하기 위한 오픈 소스 플랫폼입니다.
버그, 코드 스멜, 보안 취약점을 자동으로 감지합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **sonarqube** | 코드 분석 서버 | `9000` |

## 🛠 설정 및 환경 변수

- **이미지**: `sonarqube:lts-community`
- **데이터베이스**: PostgreSQL (`Docker/Infra/postgresql`) 연결.
- **접속**: `http://localhost:9000` (초기 계정: `admin` / `admin`)

## 📦 볼륨 마운트

- `sonarqube-data-volume`: 데이터
- `sonarqube-extensions-volume`: 플러그인
- `sonarqube-logs-volume`: 로그

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **시스템 설정**: Elasticsearch를 내장하고 있어 `vm.max_map_count` 설정(262144 이상)이 필요합니다.
