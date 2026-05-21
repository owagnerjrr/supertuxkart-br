param(
    [string]$AssetsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "..\stk-assets"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$assetsRoot = Resolve-Path -LiteralPath $AssetsPath
$repoRoot = Split-Path -Parent $PSScriptRoot
$script = Join-Path $PSScriptRoot "create_caramelo_pet_models.py"
$args = @($script, "--repo-root", $repoRoot, "--assets-path", $assetsRoot.Path)
if ($Force) {
    $args += "--force"
}

$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw "Python was not found. Install Python or run tools/create_caramelo_pet_models.py with a known Python executable."
}

& $python.Source @args
