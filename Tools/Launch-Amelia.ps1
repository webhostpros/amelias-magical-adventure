param([string]$UserDir = '', [switch]$Windowed)
$ErrorActionPreference = 'Stop'
$gameExe = Join-Path $PSScriptRoot 'Windows/ameliasadventure1.exe'
$desktopPath = [Environment]::GetFolderPath('Desktop')
$launcherMutex = New-Object Threading.Mutex($false, 'Local\AmeliaDesktopLauncher')
if (-not $launcherMutex.WaitOne(0, $false)) { exit }
$startedAt = Get-Date
$gameArgs = @('-NoSplash')
if ($Windowed) { $gameArgs += @('-windowed','-ResX=1280','-ResY=720') }
if ($UserDir) { $gameArgs += ('-UserDir="' + $UserDir + '"') }
$shotRoots = @(
    (Join-Path $env:LOCALAPPDATA 'ameliasadventure1/Saved/Screenshots/Windows'),
    (Join-Path $env:LOCALAPPDATA 'ameliasadventure1/Saved/Screenshots/WindowsClient'),
    (Join-Path $PSScriptRoot 'Windows/ameliasadventure1/Saved/Screenshots/Windows'),
    $desktopPath
)
if ($UserDir) {
    $shotRoots += (Join-Path $UserDir 'Saved/Screenshots/Windows')
    $shotRoots += (Join-Path $UserDir 'Saved/Screenshots/WindowsClient')
    $shotRoots += (Join-Path $UserDir 'ameliasadventure1/Saved/Screenshots/Windows')
}
Start-Process -FilePath $gameExe -ArgumentList $gameArgs -WindowStyle Hidden
$deadline = (Get-Date).AddSeconds(40)
do {
    foreach ($shotRoot in $shotRoots) {
        foreach ($shotFile in Get-ChildItem -LiteralPath $shotRoot -Filter 'AmeliaBugReport_*.png' -ErrorAction SilentlyContinue) {
            if ($shotFile.LastWriteTime -lt $startedAt) { continue }
            $desktopShot = Join-Path $desktopPath $shotFile.Name
            $textPath = [IO.Path]::ChangeExtension($desktopShot, '.txt')
            if (Test-Path -LiteralPath $textPath) { continue }
            try {
                if ($shotFile.FullName -ne $desktopShot) { Copy-Item -LiteralPath $shotFile.FullName -Destination $desktopShot }
                $details = $shotFile.BaseName.Substring('AmeliaBugReport_'.Length) -split '__',2
                $rotation = if ($details.Count -gt 1) { $details[1] -replace '(\.\d{6})\d{5}$', '$1' } else { 'Unavailable' }
                $reportLines = @('AMELIA THE BRAVE - BUG REPORT', 'Game version: 1.0.0', ('Captured: ' + $shotFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss')), ('Screenshot: ' + $shotFile.Name), ('Amelia position: ' + $details[0]), ('Camera rotation: ' + $rotation), '', 'What happened:', '', 'What should have happened:', '', 'Steps to reproduce:', '', 'Attach this text file and matching PNG to your bug report.', 'This report does not change saved adventure progress. Nothing is uploaded automatically.')
                [IO.File]::WriteAllLines($textPath,$reportLines,[Text.UTF8Encoding]::new($false))
            } catch { continue } # A screenshot may still be finishing its write.
        }
    }
    Start-Sleep -Milliseconds 500
    $running = Get-Process -Name 'UnrealGame-Win64-Shipping' -ErrorAction SilentlyContinue
} while ($running -or (Get-Date) -lt $deadline)
$launcherMutex.ReleaseMutex()
$launcherMutex.Dispose()
