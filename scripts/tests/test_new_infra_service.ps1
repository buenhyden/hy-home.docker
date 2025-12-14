param()
$tmp = New-Item -ItemType Directory -Path ([IO.Path]::GetTempPath()) -Name ([guid]::NewGuid().ToString()) -Force
Write-Host "Using temp root: $($tmp.FullName)"
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'Infra') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'scripts') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'secrets') | Out-Null

$composeLines = @(
    'networks:',
    '  infra_net:',
    '    name: infra_net',
    'include:',
    '  - kafka/docker-compose.yml'
)
$composeLines | Out-File -FilePath (Join-Path $tmp.FullName 'Infra\docker-compose.yml') -Encoding UTF8

$repo = (Get-Location).Path
Copy-Item -Path (Join-Path $repo 'scripts\new_infra_service.ps1') -Destination (Join-Path $tmp.FullName 'scripts')
Push-Location $tmp.FullName
git init > $null 2>&1

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\new_infra_service.ps1 mytestsvc

if (-not (Test-Path "Infra\mytestsvc")) { Write-Error "Infra\mytestsvc not created"; exit 1 }
if (-not (Test-Path "secrets\mytestsvc_password.txt")) { Write-Error "Secret file not created"; exit 1 }
$content = Get-Content -Path Infra\docker-compose.yml -Raw
if ($content -notmatch "mytestsvc/docker-compose.yml") { Write-Error "Include line not added"; exit 1 }

Write-Host "test_new_infra_service.ps1 PASSED"
Pop-Location
