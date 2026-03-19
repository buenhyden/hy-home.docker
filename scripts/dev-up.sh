#!/bin/bash
# scripts/dev-up.sh
# Quickly start the minimal development infrastructure.

BASE_DIR="$(git rev-parse --show-toplevel)"

cd "$BASE_DIR" || exit 1

if [ ! -f .env ]; then
  echo "No .env file found. Copying from .env.example..."
  cp .env.example .env
fi

echo "Starting minimal dev infrastructure..."
docker compose --profile dev up -d --remove-orphans

echo "Minimal dev infrastructure started. Use 'docker compose ps' to check status."
