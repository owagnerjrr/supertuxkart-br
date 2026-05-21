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
    @{ Id = "popo";            Source = "kiki";    Name = "Popo";            Type = "light";  Color = "0.64 0.46 0.28" },
    @{ Id = "vira_lata_preto"; Source = "tux";     Name = "Vira-lata Preto"; Type = "medium"; Color = "0.04 0.04 0.04" },
    @{ Id = "gato_rajado";     Source = "kiki";    Name = "Gato Rajado";     Type = "light";  Color = "0.62 0.42 0.24" },
    @{ Id = "capivara";        Source = "puffy";   Name = "Capivara";        Type = "heavy";  Color = "0.46 0.30 0.16" },
    @{ Id = "tucano";          Source = "gnu";     Name = "Tucano";          Type = "medium"; Color = "0.02 0.30 0.70" },
    @{ Id = "arara";           Source = "konqi";   Name = "Arara";           Type = "medium"; Color = "0.00 0.26 0.78" },
    @{ Id = "onca";            Source = "beastie"; Name = "Onca";            Type = "heavy";  Color = "0.95 0.62 0.12" },
    @{ Id = "lobo_guara";      Source = "xue";     Name = "Lobo-guara";      Type = "medium"; Color = "0.88 0.34 0.08" },
    @{ Id = "tamandua";        Source = "pidgin";  Name = "Tamandua";        Type = "heavy";  Color = "0.35 0.26 0.18" },
    @{ Id = "quati";           Source = "wilber";  Name = "Quati";           Type = "light";  Color = "0.52 0.34 0.14" },
    @{ Id = "mico_leao";       Source = "hexley";  Name = "Mico-leao";       Type = "light";  Color = "0.96 0.52 0.04" },
    @{ Id = "jacare";          Source = "amanda";  Name = "Jacare";          Type = "heavy";  Color = "0.10 0.36 0.12" },
    @{ Id = "preguica";        Source = "emule";   Name = "Preguica";        Type = "medium"; Color = "0.55 0.42 0.24" },
    @{ Id = "tatu_bola";       Source = "adiumy";  Name = "Tatu-bola";       Type = "medium"; Color = "0.42 0.34 0.28" }
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
