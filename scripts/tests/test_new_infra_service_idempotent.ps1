param()
$tmp = New-Item -ItemType Directory -Path ([IO.Path]::GetTempPath()) -Name ([guid]::NewGuid().ToString()) -Force
Write-Host "Using temp root: $($tmp.FullName)"
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'Infra') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'scripts') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'secrets') | Out-Null

$compose = @(
    'networks:',
    '  infra_net:',
    '    name: infra_net',
    'include:',
    '  - kafka/docker-compose.yml'
)
$compose | Out-File -FilePath (Join-Path $tmp.FullName 'Infra\docker-compose.yml') -Encoding UTF8

Copy-Item -Path "..\..\new_infra_service.ps1" -Destination (Join-Path $tmp.FullName 'scripts')
Push-Location $tmp.FullName
git init > $null 2>&1

Set-ExecutionPolicy Bypass -Scope Process -Force
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\new_infra_service.ps1 mytestsvc
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\new_infra_service.ps1 mytestsvc

$content = Get-Content -Path Infra\docker-compose.yml -Raw
$count = ([regex]::Matches($content, 'mytestsvc/docker-compose.yml')).Count
if ($count -ne 1) { Write-Error "Include line duplicated ($count)"; exit 1 }

Write-Host "test_new_infra_service_idempotent.ps1 PASSED"
Pop-Location
