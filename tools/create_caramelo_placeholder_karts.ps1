param(
    [string]$AssetsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "..\stk-assets"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$assetsRoot = Resolve-Path -LiteralPath $AssetsPath
$kartsRoot = Join-Path $assetsRoot "karts"
if (-not (Test-Path -LiteralPath $kartsRoot)) {
    throw "Karts folder not found: $kartsRoot"
}

$characters = @(
    @{ Id = "atho";    Source = "puffy";   Name = "Atho";    Type = "light";  Color = "0.04 0.04 0.04" },
    @{ Id = "popo";    Source = "suzanne"; Name = "Popo";    Type = "heavy";  Color = "0.95 0.64 0.35" },
    @{ Id = "favela";  Source = "tux";     Name = "Favela";  Type = "heavy";  Color = "0.78 0.39 0.12" },
    @{ Id = "nina";    Source = "beastie"; Name = "Nina";    Type = "heavy";  Color = "0.34 0.24 0.18" },
    @{ Id = "mathias"; Source = "wilber";  Name = "Mathias"; Type = "medium"; Color = "0.18 0.14 0.12" }
)

foreach ($character in $characters) {
    $source = Join-Path $kartsRoot $character.Source
    $target = Join-Path $kartsRoot $character.Id

    if (-not (Test-Path -LiteralPath $source)) {
        throw "Source kart not found: $source"
    }

    if (Test-Path -LiteralPath $target) {
        if (-not $Force) {
            Write-Host "Skipping existing kart $($character.Id). Use -Force to recreate it."
            continue
        }
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse

    $kartXmlPath = Join-Path $target "kart.xml"
    if (-not (Test-Path -LiteralPath $kartXmlPath)) {
        throw "kart.xml not found after copy: $kartXmlPath"
    }

    [xml]$kartXml = Get-Content -LiteralPath $kartXmlPath
    $kartXml.kart.name = $character.Name
    $kartXml.kart.type = $character.Type
    $kartXml.kart."rgb" = $character.Color
    $kartXml.Save($kartXmlPath)

    Write-Host "Prepared $($character.Name) from $($character.Source)."
}
