param(
    [string]$AssetsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "..\stk-assets"),
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$assetsRoot = Resolve-Path -LiteralPath $AssetsPath
$kartsRoot = Join-Path $assetsRoot "karts"
$iconRoot = Join-Path (Split-Path -Parent $PSScriptRoot) "data\gui\icons\characters"
if (-not (Test-Path -LiteralPath $kartsRoot)) {
    throw "Karts folder not found: $kartsRoot"
}

$characters = @(
    @{ Id = "favela";          Source = "tux";     Name = "Favela";          Type = "medium"; Color = "0.92 0.47 0.05" },
    @{ Id = "atho";            Source = "kiki";    Name = "Atho";            Type = "light";  Color = "0.02 0.02 0.02" },
    @{ Id = "nina";            Source = "puffy";   Name = "Nina";            Type = "heavy";  Color = "0.58 0.36 0.18" },
    @{ Id = "popo";            Source = "kiki";    Name = "Popo";            Type = "heavy";  Color = "0.64 0.46 0.28" }
)

$obsoleteCharacters = @(
    "vira_lata_preto",
    "gato_rajado",
    "capivara",
    "tucano",
    "arara",
    "onca",
    "lobo_guara",
    "tamandua",
    "quati",
    "mico_leao",
    "jacare",
    "preguica",
    "tatu_bola",
    "mathias"
)

foreach ($obsolete in $obsoleteCharacters) {
    $target = Join-Path $kartsRoot $obsolete
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
        Write-Host "Removed obsolete Caramelo Dash kart $obsolete."
    }
}

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
    $kartXml.kart.SetAttribute("name", $character.Name)
    $kartXml.kart.SetAttribute("type", $character.Type)
    $kartXml.kart.SetAttribute("rgb", $character.Color)
    $kartXml.kart.SetAttribute("groups", "standard")

    $iconPath = Join-Path $iconRoot ($character.Id + ".png")
    if (Test-Path -LiteralPath $iconPath) {
        Copy-Item -LiteralPath $iconPath -Destination (Join-Path $target "icon.png") -Force
        $kartXml.kart.SetAttribute("icon-file", "icon.png")
        $kartXml.kart.SetAttribute("minimap-icon-file", "icon.png")
    }
    $kartXml.Save($kartXmlPath)

    Write-Host "Prepared $($character.Name) from $($character.Source)."
}
