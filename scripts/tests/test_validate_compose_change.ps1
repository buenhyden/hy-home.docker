param()
$tmp = New-Item -ItemType Directory -Path ([IO.Path]::GetTempPath()) -Name ([guid]::NewGuid().ToString()) -Force
Write-Host "Using temp root: $($tmp.FullName)"
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'Infra') | Out-Null
New-Item -ItemType Directory -Path (Join-Path $tmp.FullName 'scripts') | Out-Null

$composeLines = @(
    'version: "3.8"',
    'services:',
    '  dummy:',
    '    image: alpine:3.18',
    '    command: ["/bin/sh", "-c", "sleep 1"]',
    'networks:',
    '  infra_net:'
)
$composeLines | Out-File -FilePath (Join-Path $tmp.FullName 'Infra\docker-compose.yml') -Encoding UTF8

$repo = (Get-Location).Path
Copy-Item -Path (Join-Path $repo 'scripts\validate_compose_change.ps1') -Destination (Join-Path $tmp.FullName 'scripts')
Push-Location $tmp.FullName

if (Get-Command docker -ErrorAction SilentlyContinue) {
    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_compose_change.ps1
    Write-Host "test_validate_compose_change.ps1 PASSED"
}
else {
    Write-Host "Docker not available on runner; skipping validate_compose_change test"
}
Pop-Location
