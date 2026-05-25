param(
    [string]$BlenderPath = "blender"
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$script = Join-Path $repoRoot "art\blender\create_favela_arcade_mascot.py"

& $BlenderPath --background --python $script
