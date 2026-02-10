<#
.SYNOPSIS
    Creates a new ADR from the template with the next sequential number.
.DESCRIPTION
    Creates: docs/adr/NNNN-<slug>.md
    Fills: Title, Date, Authors (optional)
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Title,

    [string]$Authors = "",

    [switch]$Force
)

function Normalize-Slug {
    param([Parameter(Mandatory = $true)][string]$Value)

    $slug = $Value.Trim().ToLowerInvariant()
    $slug = $slug -replace "[^a-z0-9\\s\\-]", ""
    $slug = $slug -replace "\\s+", "-"
    $slug = $slug -replace "-{2,}", "-"
    $slug = $slug.Trim("-")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        throw "Title '$Value' cannot be converted to a valid slug."
    }
    return $slug
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$adrDir = Join-Path $root "docs\\adr"
$templatePath = Join-Path $root "templates\\adr-template.md"

if (-not (Test-Path $templatePath)) {
    throw "ADR template not found: $templatePath"
}

if (-not (Test-Path $adrDir)) {
    New-Item -ItemType Directory -Force -Path $adrDir | Out-Null
}

$existing = Get-ChildItem -Path $adrDir -File -Filter "*.md" | Where-Object {
    $_.Name -match "^(\\d{4})-.*\\.md$"
}

$max = 0
foreach ($file in $existing) {
    $m = [regex]::Match($file.Name, "^(\\d{4})-")
    if ($m.Success) {
        $n = [int]$m.Groups[1].Value
        if ($n -gt $max) { $max = $n }
    }
}

$next = $max + 1
$num = "{0:D4}" -f $next
$slug = Normalize-Slug -Value $Title
$adrPath = Join-Path $adrDir "$num-$slug.md"

if ((Test-Path $adrPath) -and (-not $Force)) {
    throw "ADR already exists: $adrPath (use -Force to overwrite)"
}

$date = (Get-Date).ToString("yyyy-MM-dd")

$content = Get-Content $templatePath -Raw
$content = $content -replace "# \\[Short Title of Decision\\]", "# $Title"
$content = $content -replace "\\* \\*\\*Date\\*\\*: \\[YYYY-MM-DD\\]", "* **Date**: $date"
if (-not [string]::IsNullOrWhiteSpace($Authors)) {
    $content = $content -replace "\\* \\*\\*Authors\\*\\*: \\[Name\\]", "* **Authors**: $Authors"
}

Set-Content -Path $adrPath -Value $content -Encoding utf8
Write-Host "✅ Created ADR: $adrPath"
