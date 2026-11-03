# Azure DevOps / VSTS read-only adapter

Set `AZDO_URL`, `AZDO_PROJECT`, and `AZDO_PAT` in the process environment. The PAT needs Work Items read permission only. If `AZDO_URL` is empty, every helper returns `DISABLED` without making a connection. Never commit the PAT or paste it into Copilot chat.

Example: `pwsh ./tools/azure-devops/Get-WorkItemBundle.ps1 -Id 18327`

The helpers perform only HTTP GET requests. They do not update, close, assign, or comment on work items.
