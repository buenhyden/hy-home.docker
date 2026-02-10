<#
.SYNOPSIS
    Validates PRD and Spec markdown documents.
.DESCRIPTION
    Convenience wrapper around:
      - scripts/validate_prd.py
      - scripts/validate_spec.py
#>

param(
    [switch]$Strict,
    [switch]$ChangedOnly
)

$root = Resolve-Path (Join-Path $PSScriptRoot "..")

$python = "python"

$prdArgs = @()
$specArgs = @()
if ($Strict) {
    $prdArgs += "--strict"
    $specArgs += "--strict"
}
if ($ChangedOnly) {
    $prdArgs += "--changed-only"
    $specArgs += "--changed-only"
}
$planArgs = @()
if ($Strict) { $planArgs += "--strict" }
if ($ChangedOnly) { $planArgs += "--changed-only" }
$adrArgs = @()
if ($Strict) { $adrArgs += "--strict" }
if ($ChangedOnly) { $adrArgs += "--changed-only" }
$ardArgs = @()
if ($Strict) { $ardArgs += "--strict" }
if ($ChangedOnly) { $ardArgs += "--changed-only" }

Push-Location $root
try {
    $prdTargets = @()
    $specTargets = @()
    $planTargets = @()
    $adrTargets = @()
    $ardTargets = @()

    if (-not $ChangedOnly) {
        if (Test-Path "docs\\prd") {
            $prdTargets = Get-ChildItem -Path "docs\\prd" -File -Filter "*.md" -Recurse |
                Where-Object { $_.Name -ne "README.md" } |
                ForEach-Object {
                    $rel = (Resolve-Path -Relative $_.FullName)
                    $rel = $rel -replace "^[.][\\\\/]", ""
                    $rel -replace "\\\\", "/"
                }
        }

        if (Test-Path "specs") {
            $specTargets = Get-ChildItem -Path "specs" -File -Filter "*.md" -Recurse |
                Where-Object { $_.Name -notin @("README.md", "plan.md") } |
                ForEach-Object {
                    $rel = (Resolve-Path -Relative $_.FullName)
                    $rel = $rel -replace "^[.][\\\\/]", ""
                    $rel -replace "\\\\", "/"
                }
        }

        if (Test-Path "specs") {
            $planTargets = Get-ChildItem -Path "specs" -File -Filter "plan.md" -Recurse |
                ForEach-Object {
                    $rel = (Resolve-Path -Relative $_.FullName)
                    $rel = $rel -replace "^[.][\\\\/]", ""
                    $rel -replace "\\\\", "/"
                }
        }

        if (Test-Path "docs\\adr") {
            $adrTargets = Get-ChildItem -Path "docs\\adr" -File -Filter "*.md" -Recurse |
                Where-Object { $_.Name -ne "README.md" } |
                ForEach-Object {
                    $rel = (Resolve-Path -Relative $_.FullName)
                    $rel = $rel -replace "^[.][\\\\/]", ""
                    $rel -replace "\\\\", "/"
                }
        }

        if (Test-Path "docs\\ard") {
            $ardTargets = Get-ChildItem -Path "docs\\ard" -File -Filter "*.md" -Recurse |
                Where-Object { $_.Name -ne "README.md" } |
                ForEach-Object {
                    $rel = (Resolve-Path -Relative $_.FullName)
                    $rel = $rel -replace "^[.][\\\\/]", ""
                    $rel -replace "\\\\", "/"
                }
        }
    }

    if ($ChangedOnly -or $prdTargets.Count -gt 0) {
        & $python -B "scripts/validate_prd.py" @prdArgs @prdTargets
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    if ($ChangedOnly -or $specTargets.Count -gt 0) {
        & $python -B "scripts/validate_spec.py" @specArgs @specTargets
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    if ($ChangedOnly -or $planTargets.Count -gt 0) {
        & $python -B "scripts/validate_plan.py" @planArgs @planTargets
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    if ($ChangedOnly -or $adrTargets.Count -gt 0) {
        & $python -B "scripts/validate_adr.py" @adrArgs @adrTargets
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    if ($ChangedOnly -or $ardTargets.Count -gt 0) {
        & $python -B "scripts/validate_ard.py" @ardArgs @ardTargets
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
} finally {
    Pop-Location
}

Write-Host "✅ Docs validation passed."
