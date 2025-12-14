param(
    [string]$ServiceName
)
if (-not $ServiceName) {
    Write-Host "Usage: .\new_infra_service.ps1 <ServiceName>"
    exit 2
}

$root = (Get-Location).Path
if (Test-Path .git) { $root = git rev-parse --show-toplevel 2>$null }
$infra = Join-Path $root 'Infra'
$secrets = Join-Path $root 'secrets'
$svcdir = Join-Path $infra $ServiceName

if (Test-Path $svcdir) {
  Write-Host "Service directory exists: $svcdir"
  # ensure include entry present
  $infraCompose = Join-Path $infra 'docker-compose.yml'
  $include = "  - $ServiceName/docker-compose.yml"
  $content = Get-Content $infraCompose -Raw
  if ($content -notmatch [regex]::Escape($include)) {
    $updated = $content -replace '(?m)^(include:\s*\r?\n)', "`$1$include`n"
    Set-Content -Path $infraCompose -Value $updated -Encoding UTF8
    Write-Host "Added include entry to $infraCompose"
  } else {
    Write-Host "Include already present"
  }
  exit 0
}

New-Item -ItemType Directory -Path $svcdir | Out-Null

$composeText = @"
services:
  $ServiceName:
    image: myorg/$ServiceName:latest
    networks:
      - infra_net
    ports:
      - "0"
"@

$composeFile = Join-Path $svcdir 'docker-compose.yml'
$composeText | Out-File -FilePath $composeFile -Encoding UTF8

New-Item -ItemType Directory -Path $secrets -Force | Out-Null
$secretFile = Join-Path $secrets "$ServiceName`_password.txt"
if (-not (Test-Path $secretFile)) { "your_${ServiceName}_password" | Out-File -FilePath $secretFile -Encoding UTF8 }

# Add include entry to Infra/docker-compose.yml if missing
$infraCompose = Join-Path $infra 'docker-compose.yml'
$include = "  - $ServiceName/docker-compose.yml"
$content = Get-Content $infraCompose -Raw
if ($content -notmatch [regex]::Escape($include)) {
    $updated = $content -replace '(?m)^(include:\s*\r?\n)', "`$1$include`n"
    Set-Content -Path $infraCompose -Value $updated -Encoding UTF8
    Write-Host "Added include entry to $infraCompose"
}
else {
    Write-Host "Include already present"
}

Write-Host "Scaffold created at: $svcdir"
Write-Host "Next steps: update volumes/secrets in Infra/docker-compose.yml and Infra/README.md"
