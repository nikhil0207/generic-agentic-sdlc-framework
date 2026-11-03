# Generic Agentic SDLC Framework v1.1.0
## User Guide

**Current state:** Wave 8 release preparation; repository VERSION remains 1.0.1.  
**Authority:** Human approval remains authoritative.  
**Provider state:** Graphify and Headroom are optional, disabled, uninstalled, uncontacted, and unexecuted as real providers.

## 1. Start here

Open the project repository in VS Code, open Copilot Chat in Agent mode, and select `00-sdlc-orchestrator`. For a vague request, select `05-prompt-router` first or run `/route-request`. Do not ask a specialist to act before Agent 00 has established the work item, scope, authority, and gate.

The shortest safe start is:

1. State one objective and one WORK-ID.
2. List known constraints, exclusions, evidence, and desired output.
3. Ask Agent 05 to structure the request if the route is unclear.
4. Return the structured request to Agent 00.
5. Review the route, risks, missing information, and required approvals.
6. Approve only the current gate.

## 2. Installation and validation

Use an isolated branch or worktree. Validate the framework before installing:

```powershell
python scripts/validate_framework.py project-template
python -m unittest discover -s tests -v
```

Install a project-local copy:

```powershell
pwsh ./scripts/bootstrap-project.ps1 -ProjectPath 'C:\Projects\YourApplication'
```

Install only Agents and Skills globally when authorized:

```powershell
pwsh ./scripts/install-global.ps1
```

The bootstrap script skips existing files by default and reports conflicts. Review conflicts rather than forcing overwrite. After installation, reload VS Code, confirm 14 Agents are visible, and rerun validation against the target.

## 3. What a governed work item contains

A work item should identify WORK-ID, objective, requestor, owner, scope, exclusions, affected repository, requirements, acceptance criteria, risks, assumptions, evidence, approvals, decisions, test results, artifacts, and final handoff. Keep one objective per work item. If a new request is discovered, record it as a separate bounded item.

## 4. Prompt Router: Agent 05

Agent 05 turns ordinary language into a structured request. It identifies request type, objective, scope, exclusions, dependencies, risks, missing information, evidence needs, approvals, and a recommended route. It does not implement, approve, invoke specialists, or expand scope. Its output is not authorization.

Flow:

`User request -> Agent 05 -> structured SDLC request -> human review -> Agent 00 -> governed workflow -> specialist Agents -> evidence and approval gates`

Use:

```text
Select 05-prompt-router.
Request: <plain-language objective>
Context: <repository, work item, source documents>
Constraints: <must preserve, must not change>
Desired output: <requirements, diagnosis, plan, evidence, or review>
```

Review and correct the Router output, then return it to Agent 00. Do not treat missing information as permission to guess.

## 5. Supplying a prompt to Agent 00

```text
Select 00-sdlc-orchestrator.
WORK-ID: WF-2026-0001
Objective: <one bounded objective>
Source evidence: <paths, ticket, decision, or user statement>
In scope: <specific paths/behavior>
Out of scope: <explicit exclusions>
Constraints: <project standards and approvals>
Requested output: <artifact and evidence>
Known unknowns: <unverified facts>
```

Agent 00 should return the current workflow state, route, included and excluded Agents, risks, evidence requirements, and approval gates. Ask it to stop when the next approval is missing.

## 6. Specialist use

| Need | Agent | Output |
| --- | --- | --- |
| Requirements | 10 | Requirements, rules, acceptance criteria, traceability |
| Repository facts | 15 | Repository context, technology inventory, commands, impact |
| Lifecycle | 17 | Authoritative lifecycle evidence and recommendation |
| Architecture | 20 | Smallest compliant solution and ADR candidates |
| UI | 30 | UI states, accessibility, responsive interaction |
| Implementation | 40 | Approved code change, tests, rationale, limitations |
| Review | 50 | Independent findings and verdict |
| Testing | 60 | Executed test evidence and status |
| Automation | 70 | Approved automation and evidence |
| Security/performance | 80 | Authorized assessment and re-test |
| Build/deploy | 90 | Build/provenance/deployment evidence |
| Documentation | 100 | Verified guides, release notes, operational docs |

Each specialist returns control to Agent 00. A handoff is evidence, not an automated approval.

## 7. Approval gates and statuses

Human approval is required for architecture decisions, implementation authorization where configured, security and performance scope, database schema change, production deployment, provider activation, re-enablement, material scope change, and release decisions.

- **PASS/PASSED:** mandatory evidence and gates are satisfied.
- **REWORK_REQUIRED:** a correctable mandatory gap remains.
- **FAILED:** a mandatory check failed.
- **BLOCKED:** an input, environment, dependency, or approval is unavailable.
- **DEFERRED:** work is deliberately moved to a later authorized phase.
- **PARTIAL:** only part of the requested scope is complete.
- **UNKNOWN:** evidence is unavailable or conflicting.
- **NOT_TESTED:** the check did not execute.

Non-success states must never be converted to PASS to keep a workflow moving.

## 8. Feature workflow

1. Start with `/route-request` or Agent 05.
2. Let Agent 00 create or locate the WORK-ID.
3. Run Agent 15 for repository facts.
4. Run Agent 10 when business behavior or acceptance criteria need definition.
5. Run Agent 20 for architecture or ADR impact.
6. Run Agent 30 only for UI impact.
7. Obtain the required human authorization.
8. Run Agent 40 with requirements, architecture, guardrails, and test expectations.
9. Require a failing test or reproducible behavior before implementation where practical.
10. Run Agent 50 independently.
11. Run Agent 60 and record exact commands, results, failures, blocked checks, and untested scope.
12. Use Agent 70 only for stable, approved automation.
13. Use Agent 80 only with written security/performance authorization.
14. Run Agent 100 for documentation when behavior stabilizes.
15. Run Agent 90 only after separate authorization for build or deployment.

## 9. Defect workflow

Use `/start-defect` with a ticket ID or supplied ticket evidence. If Azure DevOps is configured, the adapter is read-only and performs GET operations. If its URL is empty, the integration is disabled. Agent 40 compares the ticket with repository evidence, reproduces or traces the root cause, adds a regression test, applies the minimum fix, and does not close the ticket. Agent 50 reviews and Agent 60 tests before any ticket or release decision.

## 10. Technology-health workflow

Run `/technology-health` after Agent 15 supplies a versioned inventory. Agent 17 checks current authoritative sources for support, deprecation, EOL, EOS, and security lifecycle information. It records source, checked date, exact version, conflict, confidence, and recommendation. Unverified lifecycle evidence remains UNKNOWN. Recommendations start a separate approved work item; Agent 17 does not upgrade dependencies.

## 11. Evidence and handoffs: structured handoff requirements

For every material claim, keep the source path, command, exit code, timestamp, tool version, artifact, approval, hash where relevant, and limitation. Use FACT for direct evidence, INFERENCE for reasoned conclusions, ASSUMPTION for temporary premises, UNKNOWN for unresolved information, and RECOMMENDATION for proposed action. Provider output is supplemental or non-authoritative and must be corroborated.

A handoff should include:

```yaml
source_agent: <producer>
target_agent: 00-sdlc-orchestrator
objective: <bounded objective>
artifacts: [<paths>]
decisions: [<decisions>]
constraints: [<limits>]
blocking_issues: [<exact blockers>]
evidence: [<commands, outputs, sources>]
required_approval: HUMAN_APPROVAL_REQUIRED
status: <current status>
```

## 12. Minimum-change controls

Do not invent requirements, add unrelated refactoring, introduce speculative dependencies, replace an established pattern without evidence, silently expand scope, self-approve, auto-merge, auto-deploy, close a ticket silently, perform unauthorized remedial database or security changes without authority, or treat an Agent 05 route as authorization. Record observations separately from implementation.

## 13. Optional providers

Graphify is optional code intelligence. It is disabled by default, produces `CODE_INTELLIGENCE_EVIDENCE`, has `SUPPLEMENTAL_ONLY` authority, and never overrides repository evidence. Headroom is optional context optimization. It is disabled by default, has `NONE` authority, quarantines SHADOW output, preserves protected evidence, and falls back to original context. Modes are DISABLED, SHADOW, and ENABLED. Human approval is required for SHADOW, ENABLED, and re-enablement. Agent 00 mediates submission and runtime disable.

To return to baseline, set both provider modes to `DISABLED`, remove endpoints/executables, preserve original context/evidence, and validate. No provider trial or activation is included in this Wave 8 package.

## 14. Migration and recovery

For an existing v1.0.1 project:

1. Create a branch or backup and inventory custom files.
2. Run the baseline tests and validator.
3. Run bootstrap non-force into the project.
4. Review every conflict and preserve project-owned files.
5. Reconcile configuration and provider defaults.
6. Validate the target and rerun the full suite.
7. Record evidence before adoption.

Recovery restores the backup or branch, then validates. Force mode is only for a reviewed disposable or reconciled target. Rollback to no-provider baseline is always available by disabling both providers and restoring original context.

## 15. Reusable prompt templates

### Initial framework intake

```text
Start a governed intake for WORK-ID <id>.
Objective: <business objective>
Repository: <path or repository>
In scope: <bounded scope>
Out of scope: <exclusions>
Evidence: <paths or supplied facts>
Risks/unknowns: <list>
Requested output: <intake and next gate>
```

### Requirements analysis authorization

```text
Agent 10 is authorized for WORK-ID <id>.
Use only supplied evidence and repository facts.
Produce stable requirements, acceptance criteria, exclusions, assumptions, risks, and traceability.
Do not invent rules or implement.
Return findings and the next approval gate to Agent 00.
```

### Architecture authorization

```text
Agent 20 is authorized for WORK-ID <id>.
Inputs: approved requirements <paths>, repository analysis <paths>, guardrails <paths>.
Design the minimum compliant solution, alternatives only where material, ADR candidates, migration/rollback, security, test impact, and traceability.
Do not implement or self-approve.
```

### Developer authorization

```text
Agent 40 is authorized for WORK-ID <id>.
Implement only approved requirements <IDs> and architecture <paths>.
Preserve project standards. Add or run the affected tests.
Do not change unrelated files, close the ticket, merge, deploy, or self-approve.
Return exact files, commands, results, limitations, and handoff.
```

### Test authorization

```text
Agent 60 is authorized for WORK-ID <id>.
Execute test IDs <IDs> using approved commands.
Record preconditions, exact commands, exit codes, passes, failures, errors, blocked and NOT_TESTED cases.
Do not convert missing execution or failure into PASS.
```

### Independent review authorization

```text
Agent 50 is authorized for one bounded read-only review of <scope>.
Do not modify prior artifacts. Inspect source and independently execute permitted checks.
Return findings ordered by severity, evidence classification, verdict, limitations, and human handoff.
Do not authorize the next wave.
```

### Rework authorization

```text
Agent 40 or 60 is authorized for one bounded correction of finding IDs <IDs>.
Modify only <authorized paths>. Preserve closed findings and method/test inventories.
Address the exact root cause. Run the focused check immediately, then the required regression checks.
Return a correction report and human handoff; do not claim independent closure.
```

### Build/deployment authorization

```text
A separate human authorization is required before Agent 90 may act on <build or environment>.
Source commit: <approved commit>
Artifact/version: <value>
Environment: <target>
Rollback: <plan>
Required approvals: <list>
Record tool versions, commands, hashes, timestamps, and actual outcomes. Stop before production without the human gate.
```

### Documentation authorization

```text
Agent 100 is authorized for Wave 8 documentation and release preparation.
Use only verified implementation and test evidence. Create/update only approved paths.
Document current capability, deferred work, residual risks, provider inactivity, and observed VERSION.
Do not modify VERSION, package, publish, release, deploy, or authorize Agent 90.
```

### Structured handoff to Agent 00

```yaml
source_agent: <agent>
target_agent: 00-sdlc-orchestrator
objective: <bounded result>
artifacts: [<paths>]
evidence: [<exact commands and outcomes>]
constraints: [<remaining limits>]
blocking_issues: []
required_approval: HUMAN_APPROVAL_REQUIRED
recommended_next_action: <human/orchestrator decision>
status: AWAITING_HUMAN_APPROVAL
```

## 16. Troubleshooting

| Problem | Response |
| --- | --- |
| Agent does not appear | Confirm workspace root, contract front matter, Copilot Agent mode, and reload. |
| Scope feels too broad | Return to Agent 05 and split into one WORK-ID per objective. |
| Evidence conflicts | Preserve both sources, label the conflict, and stop for the accountable decision. |
| Test cannot run | Record BLOCKED or NOT_TESTED, prerequisite, owner, and next action. |
| Provider fails | Use direct repository/original-context fallback and keep provider output non-authoritative. |
| Bootstrap conflict | Use non-force output, compare files, and merge intentionally. |
| Production action requested | Stop and request the explicit production approval. |

## 17. Quick reference

Start: `00-sdlc-orchestrator` or `/route-request`.  
Validate: `python scripts/validate_framework.py project-template`.  
Test: `python -m unittest -v tests.test_framework`.  
Provider baseline: Graphify and Headroom `DISABLED`.  
Current release state: v1.1.0 documentation/release preparation, not released.  
Final authority: human approval.
