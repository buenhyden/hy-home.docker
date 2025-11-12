# hy-home.infra

K8s(Kind): 백엔드/프론트엔드(배포/HPA/네트워크 정책/PSA), NodePort만 노출

Docker(Compose): Traefik(게이트웨이·TLS·카나리 가중 라우팅), Prometheus/Grafana/Loki/Tempo/Alloy(OTLP 수집), MinIO(S3), PostgreSQL, Redis, Kafka(KRaft), Elasticsearch+Kibana
