param([string]$EngineRoot = 'C:/Program Files/Epic Games/UE_5.8', [string]$ArchiveDirectory = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ArchiveDirectory) { $ArchiveDirectory = Join-Path (Split-Path -Parent $projectRoot) 'Builds/Chapter1-Windows' }
$projectFile = Join-Path $projectRoot 'ameliasadventure1.uproject'
$automationTool = Join-Path $EngineRoot 'Engine/Build/BatchFiles/RunUAT.bat'
& $automationTool BuildCookRun "-project=$projectFile" -noP4 -platform=Win64 -clientconfig=Shipping -skipbuild -nocompile -nocompileuat -cook -map=/Game/AmeliasAdventure/Lvl_AmeliasAdventure -stage -pak -iostore -archive "-archivedirectory=$ArchiveDirectory" -prereqs -nodebuginfo -unattended -utf8output
if ($LASTEXITCODE -ne 0) { throw "Packaging failed: $LASTEXITCODE" }
