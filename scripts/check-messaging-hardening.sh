#!/usr/bin/env bash
set -euo pipefail

failures=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "missing file: $file"
    return 1
  fi
  return 0
}

check_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -Fq -- "$pattern" "$file"; then
    fail "$label (file: $file, expected: $pattern)"
  fi
}

check_not_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq -- "$pattern" "$file"; then
    fail "$label (file: $file, forbidden: $pattern)"
  fi
}

kafka_compose="infra/05-messaging/kafka/docker-compose.yml"
kafka_dev_compose="infra/05-messaging/kafka/docker-compose.dev.yml"
rabbitmq_compose="infra/05-messaging/rabbitmq/docker-compose.yml"

spec_file="docs/04.specs/05-messaging/spec.md"
guide_file="docs/07.guides/05-messaging/optimization-hardening.md"
ops_file="docs/08.operations/05-messaging/optimization-hardening.md"
runbook_file="docs/09.runbooks/05-messaging/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-05-messaging-optimization-hardening.md"
ard_file="docs/02.ard/0020-messaging-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md"

check_file "$kafka_compose" || true
check_file "$kafka_dev_compose" || true
check_file "$rabbitmq_compose" || true
check_file "$spec_file" || true
check_file "$guide_file" || true
check_file "$ops_file" || true
check_file "$runbook_file" || true
check_file "$plan_file" || true
check_file "$task_file" || true
check_file "$prd_file" || true
check_file "$ard_file" || true
check_file "$adr_file" || true

if [[ "$failures" -eq 0 ]]; then
  # Kafka compose hardening checks.
  check_contains "$kafka_compose" "provectuslabs/kafka-ui:v0.7.2" "kafka ui image pin missing (prod)"
  check_not_contains "$kafka_compose" "kafka-ui:main" "floating kafka ui tag remains (prod)"
  check_contains "$kafka_compose" "traefik.http.routers.schema-registry.middlewares: gateway-standard-chain@file" "schema-registry gateway chain missing"
  check_contains "$kafka_compose" "traefik.http.routers.kafka-connect.middlewares: gateway-standard-chain@file" "kafka-connect gateway chain missing"
  check_contains "$kafka_compose" "traefik.http.routers.kafka-rest.middlewares: gateway-standard-chain@file" "kafka-rest gateway chain missing"
  check_contains "$kafka_compose" "traefik.http.routers.kafka-ui.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "kafka-ui middleware chain mismatch"
  check_contains "$kafka_compose" "networks:" "kafka compose networks block missing"
  check_contains "$kafka_compose" "infra_net:" "kafka compose infra_net declaration missing"
  check_contains "$kafka_compose" "external: true" "kafka compose infra_net external contract missing"

  # Kafka dev compose hardening checks.
  check_contains "$kafka_dev_compose" "provectuslabs/kafka-ui:v0.7.2" "kafka ui image pin missing (dev)"
  check_not_contains "$kafka_dev_compose" "kafka-ui:main" "floating kafka ui tag remains (dev)"
  check_not_contains "$kafka_dev_compose" "./infra/05-messaging/kafka/jmx-exporter" "kafka dev jmx volume path still uses repo-root-prefixed path"
  check_not_contains "$kafka_dev_compose" "./infra/05-messaging/kafbat-ui/dynamic_config.yaml" "kafka dev kafbat dynamic config path still uses repo-root-prefixed path"
  check_contains "$kafka_dev_compose" "traefik.http.routers.schema-registry-dev.middlewares: gateway-standard-chain@file" "schema-registry-dev gateway chain missing"
  check_contains "$kafka_dev_compose" "traefik.http.routers.kafka-connect-dev.middlewares: gateway-standard-chain@file" "kafka-connect-dev gateway chain missing"
  check_contains "$kafka_dev_compose" "traefik.http.routers.kafbat-ui-dev.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "kafbat-ui-dev middleware chain mismatch"
  check_contains "$kafka_dev_compose" "networks:" "kafka dev compose networks block missing"
  check_contains "$kafka_dev_compose" "infra_net:" "kafka dev compose infra_net declaration missing"
  check_contains "$kafka_dev_compose" "external: true" "kafka dev compose infra_net external contract missing"

  # RabbitMQ compose hardening checks.
  check_contains "$rabbitmq_compose" "- 'messaging-option'" "rabbitmq optional profile contract missing"
  check_contains "$rabbitmq_compose" "traefik.http.routers.rabbitmq.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "rabbitmq middleware chain mismatch"
  check_contains "$rabbitmq_compose" "networks:" "rabbitmq compose networks block missing"
  check_contains "$rabbitmq_compose" "infra_net:" "rabbitmq compose infra_net declaration missing"
  check_contains "$rabbitmq_compose" "external: true" "rabbitmq compose infra_net external contract missing"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-05-messaging-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0020-messaging-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/05-messaging/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/05-messaging/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/05-messaging/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Messaging hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 05-messaging hardening baseline enforced"
