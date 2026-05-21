param(
    [string]$Source = "C:\Users\pvg12207\Downloads\Caramelo Dash.png"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$repoRoot = Split-Path -Parent $PSScriptRoot
$resolvedSource = Resolve-Path -LiteralPath $Source

function New-Bitmap($width, $height) {
    $bitmap = New-Object System.Drawing.Bitmap $width, $height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $bitmap.SetResolution(96, 96)
    return $bitmap
}

function Save-Png($bitmap, $path) {
    $fullPath = Join-Path $repoRoot $path
    $directory = Split-Path -Parent $fullPath
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
    $bitmap.Save($fullPath, [System.Drawing.Imaging.ImageFormat]::Png)
}

function Draw-Fit($graphics, $image, $width, $height) {
    $scale = [Math]::Min($width / $image.Width, $height / $image.Height)
    $drawWidth = [int]($image.Width * $scale)
    $drawHeight = [int]($image.Height * $scale)
    $x = [int](($width - $drawWidth) / 2)
    $y = [int](($height - $drawHeight) / 2)
    $graphics.DrawImage($image, $x, $y, $drawWidth, $drawHeight)
}

function Draw-Cover($graphics, $image, $width, $height) {
    $scale = [Math]::Max($width / $image.Width, $height / $image.Height)
    $srcWidth = [int]($width / $scale)
    $srcHeight = [int]($height / $scale)
    $srcX = [int](($image.Width - $srcWidth) / 2)
    $srcY = [int](($image.Height - $srcHeight) / 2)
    $dest = New-Object System.Drawing.Rectangle 0, 0, $width, $height
    $src = New-Object System.Drawing.Rectangle $srcX, $srcY, $srcWidth, $srcHeight
    $graphics.DrawImage($image, $dest, $src, [System.Drawing.GraphicsUnit]::Pixel)
}

function Export-Square($image, $path, $size) {
    $bitmap = New-Bitmap $size $size
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([System.Drawing.Color]::Black)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    Draw-Fit $graphics $image $size $size
    Save-Png $bitmap $path
    $graphics.Dispose()
    $bitmap.Dispose()
}

function Export-Framed($image, $path, $width, $height) {
    $bitmap = New-Bitmap $width $height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    Draw-Cover $graphics $image $width $height

    $overlay = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(72, 0, 0, 0))
    $graphics.FillRectangle($overlay, 0, 0, $width, $height)
    $overlay.Dispose()

    Draw-Fit $graphics $image $width $height
    Save-Png $bitmap $path
    $graphics.Dispose()
    $bitmap.Dispose()
}

$sourceImage = [System.Drawing.Image]::FromFile($resolvedSource)

Copy-Item -LiteralPath $resolvedSource -Destination (Join-Path $repoRoot "data\gui\icons\caramelo_dash.png") -Force

Export-Square $sourceImage "data\gui\icons\logo.png" 512
Export-Framed $sourceImage "data\gui\icons\logo_slim.png" 512 256

Export-Square $sourceImage "android\icon.png" 256
Export-Square $sourceImage "android\icon-dbg.png" 256
Export-Square $sourceImage "android\icon_adaptive_fg.png" 440
Export-Square $sourceImage "android\icon_adaptive_fg-dbg.png" 440
Export-Framed $sourceImage "android\banner.png" 320 180

$sourceImage.Dispose()

Write-Host "Caramelo Dash brand assets generated from $resolvedSource"
