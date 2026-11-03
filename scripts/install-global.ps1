[CmdletBinding()]
param(
    [switch]$Force,
    [string]$CopilotHome
)

$ErrorActionPreference = 'Stop'
$KitRoot = Split-Path -Parent $PSScriptRoot
$SourceAgents = Join-Path $KitRoot 'project-template\.github\agents'
$SourceSkills = Join-Path $KitRoot 'project-template\.github\skills'
if ($null -eq $CopilotHome) {
    $CopilotHome = Join-Path $HOME '.copilot'
} else {
    if ([string]::IsNullOrWhiteSpace($CopilotHome) -or $CopilotHome -match '(^|[\\/])\.\.([\\/]|$)') {
        throw 'CopilotHome must be a non-empty path without parent traversal.'
    }
    $CopilotHome = [System.IO.Path]::GetFullPath($CopilotHome)
    $copilotBase = $CopilotHome.TrimEnd('\', '/')
    $pathRoot = [System.IO.Path]::GetPathRoot($copilotBase).TrimEnd('\', '/')
    if ($copilotBase -eq $pathRoot) {
        throw "CopilotHome must not be a filesystem root: $CopilotHome"
    }
    if (Test-Path -LiteralPath $CopilotHome -PathType Leaf) {
        throw "CopilotHome must identify a directory: $CopilotHome"
    }
    $repoBase = ([System.IO.Path]::GetFullPath($KitRoot)).TrimEnd('\', '/')
    if ($copilotBase -eq $repoBase) {
        throw "CopilotHome must not be the framework repository root: $CopilotHome"
    }
    $profileBase = ([System.IO.Path]::GetFullPath($env:USERPROFILE)).TrimEnd('\', '/')
    if ($copilotBase -eq $profileBase) {
        throw "CopilotHome must be an explicit .copilot directory, not the user profile root: $CopilotHome"
    }
}
$copilotBase = $CopilotHome.TrimEnd('\', '/')
$copilotPrefix = $copilotBase + [System.IO.Path]::DirectorySeparatorChar
$DestAgents = Join-Path $CopilotHome 'agents'
$DestSkills = Join-Path $CopilotHome 'skills'

function Assert-ExistingDestinationParentsSafe {
    param([Parameter(Mandatory)] [string]$Path)

    $current = [System.IO.Path]::GetFullPath($Path)
    while ($true) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Destination reparse-point traversal is not allowed: $current"
            }
        }
        if ($current -eq $copilotBase) {
            break
        }
        $current = [System.IO.Path]::GetFullPath((Split-Path -Parent $current))
    }
}

function Copy-StarterFile {
    param(
        [Parameter(Mandatory)] [string]$Source,
        [Parameter(Mandatory)] [string]$Destination
    )

    $normalizedDestination = [System.IO.Path]::GetFullPath($Destination)
    if (-not $normalizedDestination.StartsWith($copilotPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Managed destination escaped CopilotHome: $normalizedDestination"
    }
    $destinationDirectory = Split-Path -Parent $normalizedDestination
    Assert-ExistingDestinationParentsSafe -Path $destinationDirectory
    New-Item -ItemType Directory -Force -Path $destinationDirectory | Out-Null
    $destinationExisted = Test-Path -LiteralPath $normalizedDestination
    if ($destinationExisted -and -not $Force) {
        Write-Warning "Skipping existing: $Destination (use -Force to replace)"
        return
    }

    Copy-Item -Force $Source $normalizedDestination
    if ($destinationExisted) {
        Write-Host "Overwrote: $normalizedDestination"
    } else {
        Write-Host "Installed: $normalizedDestination"
    }
}

$installPlan = New-Object System.Collections.Generic.List[object]
$sourceItems = @(Get-ChildItem $SourceAgents -File) + @(Get-ChildItem $SourceSkills -Recurse -File)
foreach ($source in $sourceItems) {
    if ($source.FullName.StartsWith(([System.IO.Path]::GetFullPath($SourceAgents) + [System.IO.Path]::DirectorySeparatorChar), [System.StringComparison]::OrdinalIgnoreCase)) {
        $destination = Join-Path $DestAgents $source.Name
    } else {
        $relative = $source.FullName.Substring(([System.IO.Path]::GetFullPath($SourceSkills) + [System.IO.Path]::DirectorySeparatorChar).Length)
        $destination = Join-Path $DestSkills $relative
    }
    $normalizedDestination = [System.IO.Path]::GetFullPath($destination)
    if (-not $normalizedDestination.StartsWith($copilotPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Managed destination escaped CopilotHome: $normalizedDestination"
    }
    Assert-ExistingDestinationParentsSafe -Path (Split-Path -Parent $normalizedDestination)
    if (Test-Path -LiteralPath $normalizedDestination) {
        $destinationItem = Get-Item -LiteralPath $normalizedDestination -Force
        if (($destinationItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Destination reparse-point traversal is not allowed: $normalizedDestination"
        }
    }
    $action = if ((Test-Path -LiteralPath $normalizedDestination) -and -not $Force) { 'SKIP' } elseif (Test-Path -LiteralPath $normalizedDestination) { 'OVERWRITE' } else { 'COPY' }
    $installPlan.Add([pscustomobject]@{ Source = $source.FullName; Destination = $normalizedDestination; Action = $action })
}

New-Item -ItemType Directory -Force -Path $DestAgents, $DestSkills | Out-Null
foreach ($operation in $installPlan) {
    Copy-StarterFile -Source $operation.Source -Destination $operation.Destination
}

Write-Host "Global Copilot agents and skills installed under $CopilotHome"
Write-Host "In VS Code run: Chat: Open Customizations"
