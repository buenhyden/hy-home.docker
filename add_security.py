import re
import os

security_snippet = """    security_opt:
      - no-new-privileges:true
    read_only: true"""

targets = {
    "infra/02-auth/oauth2-proxy/docker-compose.yml": ["container_name: oauth2-proxy"],
    "infra/04-data/mng-db/docker-compose.yml": ["container_name: mng-valkey-exporter", "container_name: mng-pg-exporter"],
    "infra/04-data/opensearch/docker-compose.yml": ["container_name: opensearch-exporter"],
    "infra/05-messaging/kafka/docker-compose.yml": ["container_name: kafka-exporter"]
}

for filepath, container_names in targets.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r') as f:
        lines = f.readlines()

    content = "".join(lines)
    if "no-new-privileges:true" in content:
        print(f"Skipping {filepath}, already has security_opt")
        continue

    out_lines = []
    for line in lines:
        out_lines.append(line)
        for cname in container_names:
            if cname in line and not line.strip().startswith('#'):
                out_lines.append(security_snippet + "\n")

    with open(filepath, 'w') as f:
        f.writelines(out_lines)

print("Applied security options to targeted containers.")
