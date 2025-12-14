param()
$tmp = New-Item -ItemType Directory -Path ([IO.Path]::GetTempPath()) -Name ([guid]::NewGuid().ToString()) -Force
Push-Location $tmp.FullName
git init > $null 2>&1
New-Item -ItemType Directory -Path Infra\foo -Force | Out-Null
New-Item -ItemType Directory -Path Infra\bar -Force | Out-Null
Set-Content -Path Infra\foo\a.txt -Value "initial"
git add .; git commit -m "initial" > $null 2>&1

git checkout -b feature
New-Item -ItemType Directory -Path Infra\newsvc -Force | Out-Null
Set-Content -Path Infra\newsvc\b.txt -Value "x"
git add .; git commit -m "feat: add newsvc" > $null 2>&1

$base = 'master'
$changed = git diff --name-only $base...HEAD
# Only match files under Infra/<service>/... so we don't include top-level infra files
$services = $changed | ForEach-Object { if ($_ -match '^Infra/([^/]+)/') { $matches[1] } } | Sort-Object -Unique
if (-not ($services -contains 'newsvc')) { Write-Error "Failed to detect newsvc in changed services: $($services -join ',')"; exit 1 }
if ($services -contains 'docker-compose.yml') { Write-Error "Detected top-level infra file as a service: $($services -join ',')"; exit 1 }

Write-Host "test_detect_changed_services.ps1 PASSED"
Pop-Location
