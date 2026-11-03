# Generic Agentic SDLC Framework

Package version 1.1.0: a governed, project-independent SDLC control plane for GitHub Copilot custom agents in Visual Studio Code. This local team-handoff distribution is not a published release. Begin with [START-HERE.md](START-HERE.md), then review [validation status](HANDOFF-VALIDATION.md) and [handoff release notes](RELEASE-NOTES.md).

It includes 14 specialist agents, five standard workflows, configurable MANUAL, HYBRID, and AUTONOMOUS execution, immutable human gates, structured handoffs, evidence and memory schemas, lifecycle hooks, Azure DevOps and VSTS read-only defect retrieval, and optional technology EOL and EOS analysis.

## Validate

```powershell
python scripts/validate_framework.py project-template
```

Validation works without credentials or a live Azure DevOps service. The regression suite is repository-only and is not included in this distribution.

## Install into a project

Use an isolated branch or Git worktree, then run:

```powershell
pwsh ./scripts/bootstrap-project.ps1 -ProjectPath "C:\Projects\YourApplication"
```

The script skips existing files by default and reports conflicts for intentional merging. Open the target repository in VS Code, reload the window, open Copilot Chat in Agent mode, and confirm the 14 workspace agents appear.

For a controlled v1.0.1 to v1.1.0 upgrade, use [the migration guide](docs/Generic-Agentic-SDLC-v1.1.0-Migration-Guide.md). It preserves non-force conflict handling and keeps optional providers disabled.

## Start work

Select `00-sdlc-orchestrator` for governed execution or use `/route-request`, `/start-feature`, `/start-defect`, `/technology-health`, `/security-review`, `/performance-review`, or `/prepare-release`.

Every specialist returns control through the Orchestrator. Agents do not freely delegate or self-approve.

## Azure DevOps and VSTS

Leave `work_items.url` empty to disable the integration. When enabled, set `AZDO_URL`, `AZDO_PROJECT`, and `AZDO_PAT` in the current process. Use a PAT with Work Items read permission only.

```powershell
pwsh ./tools/azure-devops/Get-WorkItemBundle.ps1 -Id 18327
```

Version 1 performs GET requests only and never updates or closes a ticket.

## Governance rules

- Discover, do not assume.
- Evidence, do not invent.
- Apply the minimum necessary change and YAGNI.
- Follow project standards before agent preference.
- `UNKNOWN`, `BLOCKED`, `DEFERRED`, `PARTIAL`, `NOT_TESTED`, and `FAILED` never equal `PASS`.
- Production deployment, database schema changes, security-significant changes, failed mandatory tests, material scope changes, and insufficient evidence always stop at a gate.
- Automated approvals, merges, ticket closure, and production deployment are prohibited.

## Documentation

- [Framework Reference and Installation Guide](docs/guides/AGENTIC-SDLC-FRAMEWORK-REFERENCE-AND-INSTALLATION.md)
- [User Guide](docs/guides/AGENTIC-SDLC-USER-GUIDE.md)
- [v1.0.1 to v1.1.0 Migration Guide](docs/Generic-Agentic-SDLC-v1.1.0-Migration-Guide.md)
- [Team installation and handover](START-HERE.md)

The two approved DOCX guides and management PPTX are included unchanged. Publication remains subject to separate authorization.

## Provider defaults

Graphify and Headroom are optional external providers. Both remain uninstalled, uncontacted, unexecuted, and `DISABLED` by default. Graphify is `SUPPLEMENTAL_ONLY`; Headroom has authority `NONE`. Neither provider replaces repository evidence or human approval.

## Governance

Human approval remains authoritative. `UNKNOWN`, `BLOCKED`, `DEFERRED`, `PARTIAL`, `NOT_TESTED`, `FAILED`, and `REWORK_REQUIRED` never equal `PASS`. Automated approvals, merge, ticket closure, deployment, unauthorized remedial database changes, unauthorized remedial security changes, and silent handoff are prohibited.

## Package structure

- `project-template/.github/agents`: 14 Copilot agent contracts
- `project-template/.github/prompts`: 7 workflow entry prompts
- `project-template/registry`: agent and capability registry
- `project-template/workflows`: feature, defect, lifecycle, assurance, and release workflows
- `project-template/governance`: execution, grounding, status, and hard-gate rules
- `project-template/schemas`: agent, handoff, project, state, evidence, and memory contracts
- `project-template/tools/azure-devops`: read-only work-item helpers
- `scripts`: bootstrap, global install, and validation
- `tests`: offline contract tests
- `examples`: worked feature, defect, and technology-health examples
