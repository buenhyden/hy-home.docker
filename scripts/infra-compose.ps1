param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("up", "down", "restart", "logs", "ps", "pull", "config")]
  [string]$Action,

  [string[]]$Profiles = @(),

  [string[]]$Services = @(),

  [string]$Args = ""
)

$profileArgs = @()
foreach ($p in $Profiles) {
  if ($p -and $p.Trim().Length -gt 0) {
    $profileArgs += "--profile $p"
  }
}

$serviceArgs = @()
foreach ($s in $Services) {
  if ($s -and $s.Trim().Length -gt 0) {
    $serviceArgs += $s
  }
}

$base = "docker compose -f infra/docker-compose.yml"
$cmd = "$base $($profileArgs -join ' ') $Action $Args $($serviceArgs -join ' ')".Trim()

Write-Host $cmd
Invoke-Expression $cmd
