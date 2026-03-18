---
layer: core
---

# mkcert Certificate Generation

**Overview (KR):** 로컬 개발 환경에서 HTTPS를 지원하기 위해 `mkcert`를 사용하여 신뢰할 수 있는 로컬 CA 및 도메인 인증서를 생성하는 가이드입니다.

```bash
mkcert hy-home.local hy-home.dev "*.hy-home.local" "*.hy-home.dev" localhost 127.0.0.1 127.0.0.1.nip.io "*.127.0.0.1" "*.127.0.0.1.nip.io" ::1
```
