param([string] $Outfit = 'classic', [string] $CodexHome, [string] $Python)
$ErrorActionPreference = 'Stop'
if (!$Python) {
    foreach ($candidate in @('python', 'python3')) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) {
            & $candidate -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
            if ($LASTEXITCODE -eq 0) { $Python = $candidate; break }
        }
    }
}
if (!$Python) { throw 'Python 3.10+ is required for the verified installer. See INSTALL.md for manual installation.' }
$arguments = @((Join-Path $PSScriptRoot 'petctl.py'), 'install', '--outfit', $Outfit)
if ($CodexHome) { $arguments += @('--codex-home', $CodexHome) }
& $Python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Local package verified. Reopen Codex and select GPT-chan; use doctor if the artwork is unchanged.'
