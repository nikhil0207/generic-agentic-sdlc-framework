Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-AdoSettings {
    param([string]$ConfigPath = 'config/project.yaml')
    $url = $env:AZDO_URL
    $project = $env:AZDO_PROJECT
    if ([string]::IsNullOrWhiteSpace($url)) {
        return [pscustomobject]@{ Status='DISABLED'; Url=''; Project=$project }
    }
    [pscustomobject]@{ Status='ENABLED'; Url=$url.TrimEnd('/'); Project=$project }
}

function Get-AdoHeaders {
    if ([string]::IsNullOrWhiteSpace($env:AZDO_PAT)) { throw 'AZDO_PAT is required when Azure DevOps integration is enabled.' }
    $bytes = [Text.Encoding]::ASCII.GetBytes(":" + $env:AZDO_PAT)
    @{ Authorization = 'Basic ' + [Convert]::ToBase64String($bytes); Accept='application/json' }
}

function Invoke-AdoReadOnly {
    param([Parameter(Mandatory)][string]$Uri)
    Invoke-RestMethod -Uri $Uri -Headers (Get-AdoHeaders) -Method Get
}

function ConvertTo-AdoSafeError {
    param([Parameter(Mandatory)]$ErrorRecord)
    $message = [string]$ErrorRecord.Exception.Message
    if ($env:AZDO_PAT) { $message = $message.Replace($env:AZDO_PAT, '[REDACTED]') }
    $message
}
