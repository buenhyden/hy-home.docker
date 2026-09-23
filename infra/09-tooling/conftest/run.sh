#!/bin/sh
# Verify the policies against their own tests, then test every tracked Compose
# leaf and Dockerfile under infra/. Any deny fails the job; warnings are shown.
set -eu
cd /project
policy=infra/09-tooling/conftest/policy
conftest verify --policy "$policy"
find infra -name 'docker-compose*.yml' -type f | sort | xargs conftest test --policy "$policy" --namespace compose
find infra -name 'Dockerfile*' -type f | sort | xargs conftest test --parser dockerfile --policy "$policy" --namespace dockerfile
