# 🛡️ Security & Identity Guide

인프라의 진입점 보안과 인증 체계에 대한 가이드입니다.

## 1. Edge Router (Traefik)

모든 서비스의 트래픽을 제어하는 리버스 프록시입니다.

- **Dynamic Discovery**: Docker 라벨을 통해 새로운 서비스를 자동으로 인식합니다.
- **SSL**: Let's Encrypt 또는 로컬 인증서를 통해 HTTPS를 제공합니다.
- **Dashboard**: `http://traefik.${DEFAULT_URL}/dashboard/`

## 2. Identity & Access Management (Keycloak)

엔터프라이즈급 SSO(Single Sign-On) 솔루션입니다.

- **Realm**: `Master` 또는 서비스 전용 Realm을 생성하여 사용자를 관리합니다.
- **Client 연동**: Grafana, n8n 등 내부 서비스가 Keycloak을 통해 로그인하도록 설정되어 있습니다.
- **OAuth2/OIDC**: 업계 표준 프로토콜을 지원합니다.

## 3. Secret Management (HashiCorp Vault)

API 키, DB 계정 등 민감한 정보를 암호화하여 저장하고 동적으로 발급합니다.

- **UI**: `http://vault.${DEFAULT_URL}`
- **Unsealing**: 초기 기동 시 5개의 Key 중 3개가 필요합니다 (수동 절차 필요).

## 4. OAuth2 Proxy

자체 인증 기능이 없는 레거시 서비스들을 Keycloak과 연동하여 보안 레이어를 입힙니다.

- **Forward Auth**: Traefik과 결합하여 인증되지 않은 사용자의 접근을 원천 차단합니다.
