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

function Draw-Drift {
    $bitmap = New-IconBitmap
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([System.Drawing.Color]::Transparent)

    $orange = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 255, 126, 16))
    $gold = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 255, 210, 45))
    $white = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
    $dark = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(220, 70, 24, 0))
    $outline = New-Pen ([System.Drawing.Color]::FromArgb(240, 110, 40, 0)) 10
    $arc = New-Pen ([System.Drawing.Color]::White) 14

    $graphics.FillEllipse($dark, 23, 30, 210, 198)
    $graphics.FillEllipse($orange, 18, 22, 210, 198)
    $graphics.FillEllipse($gold, 40, 38, 168, 140)
    $graphics.DrawEllipse($outline, 18, 22, 210, 198)
    $graphics.DrawArc($arc, 61, 60, 135, 100, 205, 245)

    $font = New-Object System.Drawing.Font "Arial", 44, ([System.Drawing.FontStyle]::Bold)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $rect = New-Object System.Drawing.RectangleF 20, 76, 210, 80
    $graphics.DrawString("DRIFT", $font, $dark, $rect, $format)
    $rect.Y -= 5
    $graphics.DrawString("DRIFT", $font, $white, $rect, $format)

    $orange.Dispose(); $gold.Dispose(); $white.Dispose(); $dark.Dispose()
    $outline.Dispose(); $arc.Dispose(); $font.Dispose(); $format.Dispose()
    $graphics.Dispose()
    Save-Icon $bitmap "drift.png"
    $bitmap.Dispose()
}

Draw-Arrow "left_arrow.png" "left"
Draw-Arrow "right_arrow.png" "right"
Draw-Brake
Draw-Drift

Write-Host "Speed Drifters touch icons generated."
