param(
    [string]$BlenderPath = "blender"
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$script = Join-Path $repoRoot "art\blender\export_caramelo_dash_b3d.py"

& $BlenderPath --background --python $script
