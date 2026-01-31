# Setup Guide

이 문서는 로컬 환경에서 인프라를 준비하는 기준을 정리합니다.

## 핵심 파일

- 환경 변수: `.env.example` → `.env`
- 시크릿: `secrets/*.txt`
- 인프라 정의: `infra/*/*/docker-compose.yml`

## 참고

- 전체 기동 절차는 루트 `README.md`의 Quick Start를 기준으로 합니다.
- 서비스별 추가 설정은 각 `infra/<번호-카테고리>/<서비스명>/README.md`를 참고합니다.
