$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Join-Path $HOME "Intellect-Media"
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Bootstrap = Join-Path $ScriptRoot "intellect_media_autonomous_foundation_bootstrap_clean.py"
if (-not (Test-Path $RepoRoot)) { throw "Intellect-Media repository not found at $RepoRoot" }
if (-not (Test-Path $Python)) { throw "Python virtual environment not found at $Python" }
if (-not (Test-Path $Bootstrap)) { throw "Bootstrap Python file not found at $Bootstrap" }
Set-Location $RepoRoot
Write-Host "=== INTELLECT MEDIA AUTONOMOUS DEVELOPMENT SYSTEM ===" -ForegroundColor Cyan
& $Python $Bootstrap
if ($LASTEXITCODE -ne 0) { throw "Autonomous foundation bootstrap failed." }
Write-Host "=== BOOTSTRAP FINISHED ===" -ForegroundColor Green
& git status --short
