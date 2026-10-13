$ErrorActionPreference = 'Stop'
function Get-Sha256([string] $Path) {
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [BitConverter]::ToString($algorithm.ComputeHash([System.IO.File]::ReadAllBytes($Path)))
    } finally {
        $algorithm.Dispose()
    }
}
$repoDir = Split-Path -Parent $PSScriptRoot
$sourceDir = Join-Path $repoDir 'output/gpt-chan'
$codexDir = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }
$petsDir = Join-Path $codexDir 'pets'
$targetDir = Join-Path $petsDir 'gpt-chan'
foreach ($filename in @('pet.json', 'spritesheet.webp')) {
    $source = Join-Path $sourceDir $filename
    if (!(Test-Path -LiteralPath $source -PathType Leaf) -or (Get-Item -LiteralPath $source).Length -eq 0) {
        throw "Missing source: $filename"
    }
}
New-Item -ItemType Directory -Force -Path $petsDir | Out-Null
if (Test-Path -LiteralPath $targetDir) {
    $backupDir = Join-Path $petsDir ('gpt-chan.backup.' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Copy-Item -LiteralPath $targetDir -Destination (Join-Path $backupDir 'original') -Recurse -Force
    Write-Host "Backup: $backupDir/original"
}
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
foreach ($filename in @('pet.json', 'spritesheet.webp')) {
    $source = Join-Path $sourceDir $filename
    $target = Join-Path $targetDir $filename
    Copy-Item -LiteralPath $source -Destination $target -Force
    if ((Get-Sha256 $source) -ne (Get-Sha256 $target)) {
        throw "Verification failed: $filename"
    }
}
Write-Host "Installed and verified: $targetDir"
Write-Host 'Reopen Codex and select gpt-chan in Settings > Pets.'
