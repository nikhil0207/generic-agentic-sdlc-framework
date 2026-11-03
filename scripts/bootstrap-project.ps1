[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$ProjectPath,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$KitRoot = Split-Path -Parent $PSScriptRoot
$TemplateRoot = [System.IO.Path]::GetFullPath((Join-Path $KitRoot 'project-template'))
$rawProjectSegments = $ProjectPath -split '[\\/]'
if ($rawProjectSegments -contains '..') {
    throw "ProjectPath contains a parent traversal segment: $ProjectPath"
}
$TargetRoot = [System.IO.Path]::GetFullPath($ProjectPath)
$separator = [System.IO.Path]::DirectorySeparatorChar
$templateBase = $TemplateRoot.TrimEnd('\', '/')
$targetBase = $TargetRoot.TrimEnd('\', '/')
$templatePrefix = $templateBase + $separator
$targetPrefix = $targetBase + $separator

if ($targetBase -eq $templateBase -or
    $targetBase.StartsWith($templatePrefix, [System.StringComparison]::OrdinalIgnoreCase) -or
    $templateBase.StartsWith($targetPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "ProjectPath/template root overlap is not allowed: $TargetRoot"
}

if ((Test-Path -LiteralPath $TargetRoot) -and -not (Test-Path -LiteralPath $TargetRoot -PathType Container)) {
    throw "ProjectPath must identify a directory: $TargetRoot"
}

$skipped = New-Object System.Collections.Generic.List[string]
$copied = New-Object System.Collections.Generic.List[string]
$copyPlan = New-Object System.Collections.Generic.List[object]

function Assert-ExistingPathParentsContained {
    param([Parameter(Mandatory)] [string]$Path)

    $current = [System.IO.Path]::GetFullPath($Path)
    while ($current -ne $targetBase) {
        if (-not (Test-Path -LiteralPath $current)) {
            $current = [System.IO.Path]::GetFullPath((Split-Path -Parent $current))
            continue
        }
        $item = Get-Item -LiteralPath $current -Force
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Destination reparse-point traversal is not allowed: $current"
        }
        $current = [System.IO.Path]::GetFullPath((Split-Path -Parent $current))
    }
}

$allSourceItems = @(Get-ChildItem -LiteralPath $TemplateRoot -Recurse -Force)
foreach ($sourceItem in $allSourceItems) {
    $sourceItemPath = [System.IO.Path]::GetFullPath($sourceItem.FullName)
    if (($sourceItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Reparse-point traversal is not allowed: $sourceItemPath"
    }
}
$sourceFiles = @($allSourceItems | Where-Object { -not $_.PSIsContainer })
foreach ($source in $sourceFiles) {
    $sourcePath = [System.IO.Path]::GetFullPath($source.FullName)
    if (-not $sourcePath.StartsWith($templatePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Source file is outside the template root: $sourcePath"
    }
    $current = $sourcePath
    while ($true) {
        $item = Get-Item -LiteralPath $current -Force
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Reparse-point traversal is not allowed: $sourcePath"
        }
        if ($current -eq $templateBase) {
            break
        }
        $parent = [System.IO.Path]::GetFullPath((Split-Path -Parent $current))
        if (-not $parent.StartsWith($templatePrefix, [System.StringComparison]::OrdinalIgnoreCase) -and $parent -ne $templateBase) {
            throw "Source path escaped the template root: $sourcePath"
        }
        $current = $parent
    }
    $relative = $sourcePath.Substring($templatePrefix.Length)
    if ([System.IO.Path]::IsPathRooted($relative) -or [string]::IsNullOrWhiteSpace($relative)) {
        throw "Unsafe relative source path: $relative"
    }
    foreach ($segment in ($relative -split '[\\/]')) {
        if ($segment -eq '.' -or $segment -eq '..') {
            throw "Parent traversal is not allowed in source path: $relative"
        }
    }
    if ($relative -ne '.gitignore.sdlc-additions') {
        $destination = [System.IO.Path]::GetFullPath((Join-Path $targetBase $relative))
        if (-not $destination.StartsWith($targetPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Destination escaped the project target: $destination"
        }
        $destinationDir = Split-Path -Parent $destination
        Assert-ExistingPathParentsContained -Path $destinationDir
        $action = if ((Test-Path -LiteralPath $destination) -and -not $Force) { 'SKIP' } elseif (Test-Path -LiteralPath $destination) { 'OVERWRITE' } else { 'COPY' }
        $copyPlan.Add([pscustomobject]@{ Source = $sourcePath; Destination = $destination; Relative = $relative; Action = $action })
    }
}

$gitignore = Join-Path $TargetRoot '.gitignore'
$auditRule = '.copilot/audit/'
if (Test-Path -LiteralPath $gitignore) {
    Assert-ExistingPathParentsContained -Path (Split-Path -Parent $gitignore)
    $existing = Get-Content -Raw $gitignore
    if ($existing -notmatch [regex]::Escape($auditRule)) {
        $copyPlan.Add([pscustomobject]@{ Source = $null; Destination = $gitignore; Relative = '.gitignore'; Action = 'GITIGNORE_UPDATE' })
    }
} else {
    Assert-ExistingPathParentsContained -Path (Split-Path -Parent $gitignore)
    $copyPlan.Add([pscustomobject]@{ Source = $null; Destination = $gitignore; Relative = '.gitignore'; Action = 'GITIGNORE_CREATE' })
}

if (-not (Test-Path -LiteralPath $TargetRoot)) {
    New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
}

foreach ($operation in $copyPlan) {
    if ($operation.Action -eq 'SKIP') {
        $skipped.Add($operation.Relative)
    } elseif ($operation.Action -eq 'GITIGNORE_UPDATE') {
        $existing = Get-Content -Raw $operation.Destination
        Add-Content $operation.Destination "`n# Local Copilot hook audit trail`n$auditRule"
        $copied.Add($operation.Relative)
    } elseif ($operation.Action -eq 'GITIGNORE_CREATE') {
        Set-Content $operation.Destination "# Local Copilot hook audit trail`n$auditRule`n"
        $copied.Add($operation.Relative)
    } else {
        $destinationDir = Split-Path -Parent $operation.Destination
        New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null
        Copy-Item -Force $operation.Source $operation.Destination
        $copied.Add($operation.Relative)
    }
}

<#
The copy plan is fully validated before this execution phase begins.
#>
<# Removed inline copy branches retained only in history. #>

Write-Host "Bootstrapped SDLC files into: $TargetRoot"
Write-Host "Copied: $($copied.Count)"
$copied | ForEach-Object { Write-Host "  + $_" }
if ($skipped.Count -gt 0) {
    Write-Warning "Skipped $($skipped.Count) existing file(s). Review and merge them manually or rerun with -Force:"
    $skipped | ForEach-Object { Write-Host "  - $_" }
}

Write-Host "Next: open the project in VS Code, reload the window, select '00-sdlc-orchestrator', and start or resume a WORK-ID."
