# vault.hcl
ui = true

# 현재 컨테이너 런타임에서는 mlock을 비활성화하고 Vault health/raft 상태로 운영 검증
disable_mlock = true

storage "raft" {
  path    = "/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"

  # 현재 구조는 Traefik이 외부 HTTPS를 종료하고,
  # Vault 컨테이너 내부/infra_net에서는 HTTP로 통신
  tls_disable = 1
}

# 다른 컨테이너가 접근 가능한 주소
api_addr = "http://vault:8200"

# raft peer / cluster traffic용 주소
cluster_addr = "https://vault:8201"

telemetry {
  disable_hostname          = true
  prometheus_retention_time = "30s"
}
