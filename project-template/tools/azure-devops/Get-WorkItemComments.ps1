param([Parameter(Mandatory)][int]$Id)
. "$PSScriptRoot/Ado.Common.ps1"
$s = Get-AdoSettings
if ($s.Status -eq 'DISABLED') { [pscustomobject]@{status='DISABLED'; comments=@()} | ConvertTo-Json; exit 0 }
$project = [uri]::EscapeDataString($s.Project)
$uri = "$($s.Url)/$project/_apis/wit/workItems/$Id/comments?api-version=7.1-preview.4"
try { Invoke-AdoReadOnly $uri | ConvertTo-Json -Depth 20 } catch { Write-Error (ConvertTo-AdoSafeError $_); exit 1 }
