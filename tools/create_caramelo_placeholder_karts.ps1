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
    $kartXml.kart.name = $character.Name
    $kartXml.kart.type = $character.Type
    $kartXml.kart."rgb" = $character.Color
    $kartXml.Save($kartXmlPath)

    Write-Host "Prepared $($character.Name) from $($character.Source)."
}
