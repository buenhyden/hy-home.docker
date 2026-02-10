<#
.SYNOPSIS
    Creates a new implementation plan from the canonical template.
.DESCRIPTION
    Creates: specs/<slug>/plan.md
    Fills: front matter (goal/date/owner/stack) and H1 title.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Feature,

    [Parameter(Mandatory = $true)]
    [string]$Slug,

    [string]$Owner = "",

    [ValidateSet("node", "python")]
    [string]$Stack = "node",

    [switch]$Force
)

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$templatePath = Join-Path $repoRoot "templates\\plans\\plan.template.md"
if (-not (Test-Path $templatePath)) {
    throw "Plan template not found: $templatePath"
}

if ([string]::IsNullOrWhiteSpace($Owner)) {
    $Owner = $env:USERNAME
}
if ([string]::IsNullOrWhiteSpace($Owner)) {
    $Owner = "unknown"
}

$outDir = Join-Path $repoRoot ("specs\\" + $Slug)
$outPath = Join-Path $outDir "plan.md"
if ((Test-Path $outPath) -and (-not $Force)) {
    throw "Plan already exists: $outPath (use -Force to overwrite)"
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$date = (Get-Date).ToString("yyyy-MM-dd")
$goal = "Implement $Feature"

$content = Get-Content $templatePath -Raw
$content = $content.Replace('goal: "[TBD: one sentence outcome]"', "goal: `"$goal`"")
$content = $content.Replace('date_created: "YYYY-MM-DD"', "date_created: `"$date`"")
$content = $content.Replace('last_updated: "YYYY-MM-DD"', "last_updated: `"$date`"")
$content = $content.Replace('owner: "[TBD: name]"', "owner: `"$Owner`"")
$content = ($content -replace '^stack: ".*" # node\|python$', "stack: `"$Stack`" # node|python")
$content = $content.Replace("# [Feature/Component] Implementation Plan", "# $Feature Implementation Plan")

Set-Content -Path $outPath -Value $content -Encoding utf8
Write-Host "✅ Created Plan: $outPath"
