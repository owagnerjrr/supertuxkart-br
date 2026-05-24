param(
    [string]$BlenderPath = "blender"
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$script = Join-Path $repoRoot "art\blender\create_caramelo_dash_models.py"

& $BlenderPath --background --python $script
