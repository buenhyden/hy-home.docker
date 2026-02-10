<#
.SYNOPSIS
    Creates a new PRD (and optional Spec) from templates.
.DESCRIPTION
    Scaffolds:
      - docs/prd/<feature>-prd.md
      - specs/<feature>/spec.md (optional)

    This operationalizes the Business/Product checklist inside the PRD template.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Feature,

    [string]$Owner = "",

    [string]$ParentEpic = "",

    [switch]$WithSpec,

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
        throw "Feature name '$Value' cannot be converted to a valid slug."
    }
    return $slug
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$slug = Normalize-Slug -Value $Feature

$prdTemplatePath = Join-Path $root "templates\\prd-template.md"
$specTemplatePath = Join-Path $root "templates\\spec-template.md"

if (-not (Test-Path $prdTemplatePath)) {
    throw "PRD template not found: $prdTemplatePath"
}

$prdDir = Join-Path $root "docs\\prd"
if (-not (Test-Path $prdDir)) {
    New-Item -ItemType Directory -Force -Path $prdDir | Out-Null
}

$prdPath = Join-Path $prdDir "$slug-prd.md"
if ((Test-Path $prdPath) -and (-not $Force)) {
    throw "PRD already exists: $prdPath (use -Force to overwrite)"
}

$prdContent = Get-Content $prdTemplatePath -Raw
$prdContent = $prdContent -replace "# \\[Feature/Epic Name\\] PRD", "# $Feature PRD"
if (-not [string]::IsNullOrWhiteSpace($Owner)) {
    $prdContent = $prdContent -replace "(?m)^[\\*-]\\s+\\*\\*Owner\\*\\*:\\s+\\[Name\\]\\s*$", "- **Owner**: $Owner"
}
if (-not [string]::IsNullOrWhiteSpace($ParentEpic)) {
    $prdContent = $prdContent -replace "(?m)^[\\*-]\\s+\\*\\*Parent Epic\\*\\*:\\s+\\[Link to Epic PRD\\]\\s*\\(Optional\\)\\s*$", "- **Parent Epic**: $ParentEpic (Optional)"
}

Set-Content -Path $prdPath -Value $prdContent -Encoding utf8
Write-Host "✅ Created PRD: $prdPath"

if ($WithSpec) {
    if (-not (Test-Path $specTemplatePath)) {
        throw "Spec template not found: $specTemplatePath"
    }

    $specDir = Join-Path $root "specs\\$slug"
    if (-not (Test-Path $specDir)) {
        New-Item -ItemType Directory -Force -Path $specDir | Out-Null
    }

    $specPath = Join-Path $specDir "spec.md"
    if ((Test-Path $specPath) -and (-not $Force)) {
        throw "Spec already exists: $specPath (use -Force to overwrite)"
    }

    $specContent = Get-Content $specTemplatePath -Raw
    $specContent = $specContent -replace "# \\[Component Name\\] Technical Specification", "# $Feature Technical Specification"
    $specContent = $specContent -replace "- \\*\\*PRD Reference\\*\\*: \\[Link to PRD\\]", "- **PRD Reference**: docs/prd/$slug-prd.md"

    Set-Content -Path $specPath -Value $specContent -Encoding utf8
    Write-Host "✅ Created Spec: $specPath"
}
