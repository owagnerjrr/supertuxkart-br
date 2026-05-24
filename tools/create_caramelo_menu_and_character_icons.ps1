$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$repoRoot = Split-Path -Parent $PSScriptRoot
$iconRoot = Join-Path $repoRoot "data\gui\icons"
$characterRoot = Join-Path $iconRoot "characters"
New-Item -ItemType Directory -Path $characterRoot -Force | Out-Null

function New-Bitmap([int]$width, [int]$height) {
    $bitmap = New-Object System.Drawing.Bitmap $width, $height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $bitmap.SetResolution(96, 96)
    return $bitmap
}

function New-Brush([int]$a, [int]$r, [int]$g, [int]$b) {
    return New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb($a, $r, $g, $b))
}

function New-Pen2([int]$a, [int]$r, [int]$g, [int]$b, [float]$w) {
    $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb($a, $r, $g, $b)), $w
    $pen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round
    $pen.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
    $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    return $pen
}

function Save-Png($bitmap, [string]$path) {
    $directory = Split-Path -Parent $path
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
}

function Draw-TireIcon([string]$name, [string]$label, [int[]]$accent) {
    $bitmap = New-Bitmap 256 256
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $shadow = New-Brush 110 0 0 0
    $tire = New-Brush 255 18 18 18
    $rim = New-Brush 255 214 214 214
    $hub = New-Brush 255 $accent[0] $accent[1] $accent[2]
    $white = New-Brush 255 255 255 255
    $orange = New-Pen2 255 255 140 0 10

    $graphics.FillEllipse($shadow, 28, 36, 206, 206)
    $graphics.FillEllipse($tire, 22, 24, 206, 206)
    $graphics.DrawEllipse($orange, 30, 32, 190, 190)
    $graphics.FillEllipse($rim, 72, 74, 106, 106)
    $graphics.FillEllipse($hub, 96, 98, 58, 58)
    for ($i = 0; $i -lt 8; $i++) {
        $angle = $i * [Math]::PI / 4
        $x1 = 125 + [Math]::Cos($angle) * 42
        $y1 = 127 + [Math]::Sin($angle) * 42
        $x2 = 125 + [Math]::Cos($angle) * 65
        $y2 = 127 + [Math]::Sin($angle) * 65
        $graphics.DrawLine((New-Pen2 255 40 40 40 8), [int]$x1, [int]$y1, [int]$x2, [int]$y2)
    }

    $font = New-Object System.Drawing.Font "Arial", 38, ([System.Drawing.FontStyle]::Bold)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF 38, 177, 180, 58
    $graphics.DrawString($label, $font, $white, $rect, $format)

    $shadow.Dispose(); $tire.Dispose(); $rim.Dispose(); $hub.Dispose(); $white.Dispose(); $orange.Dispose()
    $font.Dispose(); $format.Dispose(); $graphics.Dispose()
    Save-Png $bitmap (Join-Path $iconRoot $name)
    $bitmap.Dispose()
}

function Draw-CharacterIcon([hashtable]$c) {
    $bitmap = New-Bitmap 256 256
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $bg = New-Brush 255 $c.Bg[0] $c.Bg[1] $c.Bg[2]
    $face = New-Brush 255 $c.Face[0] $c.Face[1] $c.Face[2]
    $dark = New-Brush 255 26 26 26
    $white = New-Brush 255 255 255 255
    $accent = New-Brush 255 $c.Accent[0] $c.Accent[1] $c.Accent[2]
    $outline = New-Pen2 255 22 22 22 8

    $graphics.FillEllipse($bg, 8, 8, 240, 240)
    $graphics.DrawEllipse($outline, 8, 8, 240, 240)

    if ($c.Kind -eq "bird") {
        $graphics.FillEllipse($face, 56, 52, 132, 148)
        $beak = @(
            [System.Drawing.Point]::new(138, 110),
            [System.Drawing.Point]::new(220, 132),
            [System.Drawing.Point]::new(138, 154)
        )
        $graphics.FillPolygon($accent, $beak)
        $graphics.FillEllipse($white, 80, 94, 34, 42)
        $graphics.FillEllipse($white, 126, 94, 34, 42)
        $graphics.FillEllipse($dark, 93, 108, 13, 16)
        $graphics.FillEllipse($dark, 139, 108, 13, 16)
        $graphics.DrawArc((New-Pen2 255 255 230 55 14), 42, 40, 100, 128, 210, 95)
    } elseif ($c.Kind -eq "long") {
        $graphics.FillEllipse($face, 50, 54, 154, 142)
        $graphics.FillEllipse($accent, 114, 116, 100, 48)
        $graphics.FillEllipse($white, 82, 96, 32, 38)
        $graphics.FillEllipse($white, 136, 96, 32, 38)
        $graphics.FillEllipse($dark, 94, 110, 12, 14)
        $graphics.FillEllipse($dark, 148, 110, 12, 14)
    } else {
        $graphics.FillEllipse($face, 48, 54, 160, 150)
        $graphics.FillEllipse($face, 42, 44, 54, 62)
        $graphics.FillEllipse($face, 160, 44, 54, 62)
        $graphics.FillEllipse($white, 78, 96, 34, 42)
        $graphics.FillEllipse($white, 142, 96, 34, 42)
        $graphics.FillEllipse($dark, 91, 111, 13, 16)
        $graphics.FillEllipse($dark, 155, 111, 13, 16)
        $graphics.FillEllipse($accent, 113, 132, 32, 24)
    }

    if ($c.Stripes) {
        $stripePen = New-Pen2 180 45 30 18 7
        $graphics.DrawArc($stripePen, 70, 64, 44, 86, 220, 80)
        $graphics.DrawArc($stripePen, 140, 64, 44, 86, 240, 80)
        $stripePen.Dispose()
    }

    $font = New-Object System.Drawing.Font "Arial", 25, ([System.Drawing.FontStyle]::Bold)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $labelRect = New-Object System.Drawing.RectangleF 12, 202, 232, 38
    $graphics.DrawString($c.Label, $font, $white, $labelRect, $format)

    $bg.Dispose(); $face.Dispose(); $dark.Dispose(); $white.Dispose(); $accent.Dispose(); $outline.Dispose()
    $font.Dispose(); $format.Dispose(); $graphics.Dispose()
    Save-Png $bitmap (Join-Path $characterRoot ($c.Id + ".png"))
    $bitmap.Dispose()
}

function Import-CharacterIcon([hashtable]$c) {
    if (-not $c.Source -or -not (Test-Path -LiteralPath $c.Source)) {
        Draw-CharacterIcon $c
        return
    }

    $source = [System.Drawing.Image]::FromFile($c.Source)
    $side = [Math]::Min($source.Width, $source.Height)
    $x = [Math]::Floor(($source.Width - $side) / 2)
    $y = [Math]::Floor(($source.Height - $side) / 2)
    $bitmap = New-Bitmap 512 512
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.DrawImage(
        $source,
        (New-Object System.Drawing.Rectangle 0, 0, 512, 512),
        (New-Object System.Drawing.Rectangle $x, $y, $side, $side),
        [System.Drawing.GraphicsUnit]::Pixel)

    $band = New-Brush 215 18 18 18
    $shadow = New-Brush 255 0 0 0
    $text = New-Brush 255 255 225 130
    $font = New-Object System.Drawing.Font "Arial", 58, ([System.Drawing.FontStyle]::Bold)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $graphics.FillRectangle($band, 0, 410, 512, 102)
    $shadowRect = New-Object System.Drawing.RectangleF 4, 414, 512, 92
    $textRect = New-Object System.Drawing.RectangleF 0, 410, 512, 92
    $graphics.DrawString($c.Label, $font, $shadow, $shadowRect, $format)
    $graphics.DrawString($c.Label, $font, $text, $textRect, $format)

    $graphics.Dispose()
    $format.Dispose()
    $font.Dispose()
    $text.Dispose()
    $shadow.Dispose()
    $band.Dispose()
    Save-Png $bitmap (Join-Path $characterRoot ($c.Id + ".png"))
    $bitmap.Dispose()
    $source.Dispose()
}

function Draw-PowerIcon([string]$file, [string]$label, [int[]]$color) {
    $bitmap = New-Bitmap 256 256
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $shadow = New-Brush 120 0 0 0
    $body = New-Brush 255 $color[0] $color[1] $color[2]
    $gold = New-Brush 255 255 204 40
    $white = New-Brush 255 255 255 255
    $outline = New-Pen2 255 30 30 30 8

    $graphics.FillEllipse($shadow, 26, 30, 210, 210)
    $graphics.FillEllipse($body, 20, 20, 210, 210)
    $graphics.DrawEllipse($outline, 20, 20, 210, 210)
    $graphics.FillPie($gold, 34, 34, 182, 182, 205, 88)

    $fontSize = 36
    if ($label.Length -gt 5) { $fontSize = 28 }
    if ($label.Length -gt 7) { $fontSize = 22 }
    $font = New-Object System.Drawing.Font "Arial", $fontSize, ([System.Drawing.FontStyle]::Bold)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF 28, 82, 198, 86
    $graphics.DrawString($label, $font, $white, $rect, $format)

    $shadow.Dispose(); $body.Dispose(); $gold.Dispose(); $white.Dispose(); $outline.Dispose()
    $font.Dispose(); $format.Dispose(); $graphics.Dispose()
    Save-Png $bitmap (Join-Path $iconRoot $file)
    $bitmap.Dispose()
}

Draw-TireIcon "speed_50.png" "50" @(255, 196, 40)
Draw-TireIcon "speed_100.png" "100" @(42, 202, 72)
Draw-TireIcon "speed_150.png" "150" @(235, 58, 42)

$characters = @(
    @{ Id="favela"; Label="Favela"; Kind="dog"; Face=@(218,126,38); Bg=@(0,138,72); Accent=@(55,35,20); Stripes=$false; Source="$env:USERPROFILE\Downloads\Favela.png" },
    @{ Id="atho"; Label="Atho"; Kind="cat"; Face=@(24,24,26); Bg=@(240,172,35); Accent=@(210,20,20); Stripes=$false; Source="$env:USERPROFILE\Downloads\Atho.png" },
    @{ Id="nina"; Label="Nina"; Kind="dog"; Face=@(139,86,43); Bg=@(30,116,190); Accent=@(55,35,20); Stripes=$false; Source="$env:USERPROFILE\Downloads\Nina.png" },
    @{ Id="popo"; Label="Popo"; Kind="cat"; Face=@(168,116,70); Bg=@(245,148,40); Accent=@(70,42,20); Stripes=$true; Source="$env:USERPROFILE\Downloads\Popo.png" }
)

foreach ($character in $characters) {
    Import-CharacterIcon $character
}

Draw-PowerIcon "zipper_collect.png" "TURBO" @(255, 126, 18)
Draw-PowerIcon "bowling-icon.png" "CASCO" @(48, 150, 70)
Draw-PowerIcon "bubblegum-icon.png" "GOMA" @(230, 70, 150)
Draw-PowerIcon "cake-icon.png" "OSSO" @(235, 80, 40)
Draw-PowerIcon "plunger-icon.png" "LACO" @(65, 150, 230)
Draw-PowerIcon "switch-icon.png" "TROCA" @(70, 60, 180)
Draw-PowerIcon "swatter-icon.png" "MOLA" @(250, 175, 35)
Draw-PowerIcon "rubber_ball-icon.png" "BOLA" @(40, 150, 210)
Draw-PowerIcon "parachute-icon.png" "ASA" @(75, 190, 225)
Draw-PowerIcon "anchor-icon.png" "PESO" @(90, 90, 100)

Write-Host "Caramelo Dash menu and character icons generated."
