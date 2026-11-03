param([Parameter(Mandatory)][int]$Id)
. "$PSScriptRoot/Ado.Common.ps1"
$s = Get-AdoSettings
if ($s.Status -eq 'DISABLED') { [pscustomobject]@{status='DISABLED'; reason='Azure DevOps URL is empty'; id=$Id} | ConvertTo-Json; exit 0 }
try {
    $project = [uri]::EscapeDataString($s.Project)
    $item = Invoke-AdoReadOnly "$($s.Url)/$project/_apis/wit/workitems/$Id?`$expand=all&api-version=7.1"
    $comments = Invoke-AdoReadOnly "$($s.Url)/$project/_apis/wit/workItems/$Id/comments?api-version=7.1-preview.4"
    [pscustomobject]@{
        status='RETRIEVED'; retrieved_at=(Get-Date).ToUniversalTime().ToString('o'); source=$s.Url
        id=$item.id; revision=$item.rev; fields=$item.fields; relations=$item.relations; comments=$comments.comments
    } | ConvertTo-Json -Depth 30
} catch { Write-Error (ConvertTo-AdoSafeError $_); exit 1 }
