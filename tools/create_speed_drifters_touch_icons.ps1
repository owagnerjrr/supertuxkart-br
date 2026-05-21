$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$repoRoot = Split-Path -Parent $PSScriptRoot
$iconDir = Join-Path $repoRoot "data\gui\icons\android"

function New-IconBitmap {
    $bitmap = New-Object System.Drawing.Bitmap 256, 256, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $bitmap.SetResolution(96, 96)
    return $bitmap
}

function New-Pen($color, $width) {
    $pen = New-Object System.Drawing.Pen $color, $width
    $pen.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
    $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    $pen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round
    return $pen
}

function Save-Icon($bitmap, $name) {
    $path = Join-Path $iconDir $name
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
}

function Draw-Arrow($name, $direction) {
    $bitmap = New-IconBitmap
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $shadow = New-Pen ([System.Drawing.Color]::FromArgb(180, 0, 40, 78)) 34
    $line = New-Pen ([System.Drawing.Color]::FromArgb(255, 210, 242, 255)) 24

    if ($direction -eq "left") {
        $points = @(
            [System.Drawing.Point]::new(150, 62),
            [System.Drawing.Point]::new(84, 128),
            [System.Drawing.Point]::new(150, 194)
        )
    } else {
        $points = @(
            [System.Drawing.Point]::new(106, 62),
            [System.Drawing.Point]::new(172, 128),
            [System.Drawing.Point]::new(106, 194)
        )
    }

    $graphics.DrawLines($shadow, $points)
    $graphics.DrawLines($line, $points)
    $shadow.Dispose()
    $line.Dispose()
    $graphics.Dispose()
    Save-Icon $bitmap $name
    $bitmap.Dispose()
}

function Draw-Brake {
    $bitmap = New-IconBitmap
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $plateBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(245, 210, 244, 255))
    $shadowBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(150, 0, 40, 78))
    $graphics.FillRectangle($shadowBrush, 83, 49, 90, 166)
    $graphics.FillRectangle($plateBrush, 75, 42, 90, 166)

    $slotBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 0, 92, 140))
    foreach ($x in @(94, 121, 148)) {
        $graphics.FillRectangle($slotBrush, $x, 70, 12, 112)
    }

    $plateBrush.Dispose()
    $shadowBrush.Dispose()
    $slotBrush.Dispose()
    $graphics.Dispose()
    Save-Icon $bitmap "brake.png"
    $bitmap.Dispose()
}

Draw-Arrow "left_arrow.png" "left"
Draw-Arrow "right_arrow.png" "right"
Draw-Brake

Write-Host "Speed Drifters touch icons generated."
