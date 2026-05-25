param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"
$bytes = [IO.File]::ReadAllBytes((Resolve-Path $Path))

function Read-U32([int]$Offset) {
    [BitConverter]::ToUInt32($bytes, $Offset)
}

function Read-F32([int]$Offset) {
    [BitConverter]::ToSingle($bytes, $Offset)
}

$script:Vertices = 0
$script:Triangles = 0
$script:Min = @([double]::PositiveInfinity, [double]::PositiveInfinity, [double]::PositiveInfinity)
$script:Max = @([double]::NegativeInfinity, [double]::NegativeInfinity, [double]::NegativeInfinity)

function Read-Chunks([int]$Start, [int]$End) {
    $offset = $Start
    while ($offset + 8 -le $End) {
        $tag = [Text.Encoding]::ASCII.GetString($bytes, $offset, 4)
        $length = Read-U32 ($offset + 4)
        $payloadStart = $offset + 8
        $payloadEnd = $payloadStart + $length

        if ($tag -eq "VRTS") {
            $texCoordSets = Read-U32 ($payloadStart + 4)
            $texCoordSize = Read-U32 ($payloadStart + 8)
            $stride = 24 + (8 * $texCoordSets * $texCoordSize)
            $vertexOffset = $payloadStart + 12
            while ($vertexOffset + $stride -le $payloadEnd) {
                $values = @(
                    (Read-F32 $vertexOffset),
                    (Read-F32 ($vertexOffset + 4)),
                    (Read-F32 ($vertexOffset + 8))
                )
                $script:Vertices++
                for ($i = 0; $i -lt 3; $i++) {
                    if ($values[$i] -lt $script:Min[$i]) { $script:Min[$i] = $values[$i] }
                    if ($values[$i] -gt $script:Max[$i]) { $script:Max[$i] = $values[$i] }
                }
                $vertexOffset += $stride
            }
        }
        elseif ($tag -eq "TRIS") {
            $script:Triangles += [Math]::Floor(($length - 4) / 12)
        }

        if ($tag -eq "BB3D") {
            Read-Chunks ($payloadStart + 4) $payloadEnd
        }
        elseif ($tag -eq "NODE") {
            $childStart = $payloadStart
            while ($childStart -lt $payloadEnd -and $bytes[$childStart] -ne 0) {
                $childStart++
            }
            $childStart += 1 + 12 + 12 + 16
            Read-Chunks $childStart $payloadEnd
        }
        elseif ($tag -eq "MESH") {
            Read-Chunks ($payloadStart + 4) $payloadEnd
        }

        $offset = $payloadEnd
    }
}

Read-Chunks 0 $bytes.Length

[pscustomobject]@{
    Path = (Resolve-Path $Path).Path
    Bytes = $bytes.Length
    Vertices = $script:Vertices
    Triangles = $script:Triangles
    MinX = $script:Min[0]
    MinY = $script:Min[1]
    MinZ = $script:Min[2]
    MaxX = $script:Max[0]
    MaxY = $script:Max[1]
    MaxZ = $script:Max[2]
    Width = $script:Max[0] - $script:Min[0]
    Height = $script:Max[1] - $script:Min[1]
    Length = $script:Max[2] - $script:Min[2]
} | Format-List
