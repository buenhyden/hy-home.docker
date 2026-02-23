import re
import os

files = [
    "infra/02-auth/keycloak/docker-compose.yml",
    "infra/02-auth/oauth2-proxy/docker-compose.yml",
    "infra/04-data/mng-db/docker-compose.yml",
    "infra/04-data/minio/docker-compose.yml",
    "infra/04-data/qdrant/docker-compose.yml",
    "infra/04-data/valkey-cluster/docker-compose.yml",
    "infra/04-data/opensearch/docker-compose.yml",
    "infra/05-messaging/kafka/docker-compose.yml"
]

ANCHOR_TEXT = """
x-restart: &default-restart
  restart: unless-stopped
"""

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r') as f:
        content = f.read()

    # Insert x-restart anchor if not present
    if "x-restart: &default-restart" not in content:
        content = re.sub(
            r"(x-logging: &default-logging\n  driver: 'json-file'\n  options:\n    max-size: '5m'\n    max-file: '2'\n)",
            r"\1" + ANCHOR_TEXT,
            content
        )

    # Replace restart: unless-stopped
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Allow preceding spaces and trailing spaces only
        if re.match(r'^(\s+)restart: unless-stopped(\s*)$', line):
            if not "x-restart: &default-restart" in "\n".join(lines[max(0, i-2):i+1]):
                lines[i] = line.replace('restart: unless-stopped', '<<: *default-restart')

    content = '\n'.join(lines)
    with open(filepath, 'w') as f:
        f.write(content)

print("Applied default-restart replacing.")
