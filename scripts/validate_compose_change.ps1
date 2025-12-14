param(
    [string]$ServiceName = $null,
    [switch]$Up
)

# Validate Infra/docker-compose.yml using docker compose config and optionally up a service
$root = (Get-Location).Path
if (Test-Path .git) { $root = git rev-parse --show-toplevel 2>$null }
$compose = Join-Path $root 'Infra/docker-compose.yml'
if (-not (Test-Path $compose)) { Write-Host "Infra compose not found: $compose"; exit 1 }

Write-Host "Validating: $compose"
docker compose -f $compose config > $null
Write-Host "Compose config is valid"

if ($ServiceName -and $Up) {
    Push-Location (Join-Path $root 'Infra')
    Write-Host "Starting service: $ServiceName (no deps)"
    docker compose up -d --no-deps --force-recreate $ServiceName
    Start-Sleep -Seconds 5
    docker compose -f $compose logs --no-color --tail 200 $ServiceName
    Pop-Location
}

Write-Host "Done."
