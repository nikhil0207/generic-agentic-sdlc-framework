# Generic Agentic SDLC v1.1.0 — team handoff

This is a locally prepared handoff package, not a published release. Start here after extracting the ZIP into a new folder. Preserve the complete folder structure, including hidden template directories.

## What is included

| Audience | Read or use |
| --- | --- |
| Team lead / management | `docs/management/Agentic-SDLC-Framework-v1.1.0-Management-Roadmap.pptx` |
| Installer / architect | `docs/distributable/Agentic-SDLC-Framework-v1.1.0-Reference-and-Installation.docx` |
| Agent users | `docs/distributable/Agentic-SDLC-v1.1.0-User-Guide.docx` |
| Searchable documentation | Both Markdown guides in `docs/guides/` |
| Existing framework users | `docs/Generic-Agentic-SDLC-v1.1.0-Migration-Guide.md` |
| Project installation | `scripts/bootstrap-project.ps1` |
| Optional user-level installation | `scripts/install-global.ps1` |
| Validation | `scripts/validate_framework.py` |
| Agent and skill definitions | `project-template/.github/agents/` and `project-template/.github/skills/` |

The two Word documents and one presentation are the approved originals, unchanged. References within them to release preparation describe their creation context; this package does not change their approval scope.

## Prerequisites

Use an organization-approved Windows workstation with PowerShell, Python 3, VS Code, and access to GitHub Copilot custom agents. The validator uses the Python standard library. No live provider credentials are required. Follow corporate execution/signing policy: if an unsigned script is blocked, obtain IT-approved signing or execution authorization; do not bypass policy.

## Validate the extracted kit

Open PowerShell in the extracted package root:

```powershell
Get-Content .\VERSION
python .\scripts\validate_framework.py .\project-template
if ($LASTEXITCODE -ne 0) { throw 'Framework validation failed' }
```

Expected package version: `1.1.0`; validator exit: `0`.

## First installation — isolated project

Choose a NEW, empty, explicit project directory outside the kit. Do not begin by overwriting an existing application.

```powershell
$pilotProject = Join-Path $env:TEMP ('sdlc-handoff-' + [guid]::NewGuid().ToString('N'))
& .\scripts\bootstrap-project.ps1 -ProjectPath $pilotProject
python .\scripts\validate_framework.py $pilotProject
if ($LASTEXITCODE -ne 0) { throw 'Installed project validation failed' }
Write-Host "Inspect the installed project at: $pilotProject"
```

Inspect that all 14 agent files and seven skill directories are present. Open that project folder in VS Code and reload the window. Confirm the agents are visible in Copilot customizations. Choose `00-sdlc-orchestrator` and submit a small analysis-only work item with a WORK-ID. Require a plan and explicit human approval before implementation. No application compilation is performed by installing the framework.

The bootstrap script copies framework configuration and scaffolding; it does not install VS Code, Copilot, Python, application dependencies or external providers. It skips existing files without `-Force` and may append the local audit exclusion to the target `.gitignore`.

## Optional global install — sandbox test first

This installs only agents and skills, not the full project governance template. Always pass an explicit destination during testing:

```powershell
$sandboxCopilot = Join-Path $env:TEMP ('sdlc-copilot-' + [guid]::NewGuid().ToString('N'))
& .\scripts\install-global.ps1 -CopilotHome $sandboxCopilot
Get-ChildItem (Join-Path $sandboxCopilot 'agents') -File
Get-ChildItem (Join-Path $sandboxCopilot 'skills') -Directory
```

Expect 14 agents and seven skill directories. An actual user-level install is a separate operator decision; choose the intended Copilot directory explicitly. Never use `-Force` without reviewing affected files and keeping a recoverable backup.

## Upgrade and rollback

For existing projects follow the migration guide. Review local customizations and conflicts, retain a backup, then use non-force installation and merge intentionally. Roll back only the framework changes identified by that comparison; do not reset or delete unrelated project content. Keep temporary smoke-test directories until results are recorded, then remove only those exact directories if authorized.

## Operating boundaries

Graphify and Headroom remain DISABLED. Azure DevOps access is optional and requires separately configured read-only credentials. No credential belongs in this package or in chat. All specialist handoffs return through Agent 00. Installing this kit does not authorize automated approvals, Git commits/tags/pushes, production deployment, or provider activation.

## Troubleshooting and final readiness

- Missing agents: open the installed project root, preserve hidden folders, reload VS Code, then check approved Copilot configuration and access.
- Existing-file warnings: inspect and merge; do not blindly enable force.
- Validator failure: preserve the full output, stop rollout and report the affected path to the owner.
- Script signature error: follow IT execution policy; do not change policy automatically.
- Hash mismatch: stop and obtain a fresh verified ZIP.

See `HANDOFF-VALIDATION.md` for executed checks and remaining Windows acceptance steps. Windows bootstrap/global-install and VS Code discovery tests have NOT been executed in the packaging environment. The owner's Windows source repository was not accessible and its VERSION was not updated by this package assembly. Package VERSION is 1.1.0; source-version reconciliation remains an explicit owner step before official release.
