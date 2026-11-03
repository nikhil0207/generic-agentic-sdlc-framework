param([Parameter(Mandatory)][int]$Id)
. "$PSScriptRoot/Ado.Common.ps1"
$s = Get-AdoSettings
if ($s.Status -eq 'DISABLED') { [pscustomobject]@{status='DISABLED'; relations=@()} | ConvertTo-Json; exit 0 }
$project = [uri]::EscapeDataString($s.Project)
$uri = "$($s.Url)/$project/_apis/wit/workitems/$Id?`$expand=relations&api-version=7.1"
try { (Invoke-AdoReadOnly $uri).relations | ConvertTo-Json -Depth 20 } catch { Write-Error (ConvertTo-AdoSafeError $_); exit 1 }
