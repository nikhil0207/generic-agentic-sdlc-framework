# Generic Agentic SDLC Framework v1.1.0
## Reference and Installation Guide

**Status:** Wave 8 release preparation, not released  
**Observed repository version:** 1.0.1  
**Documentation owner:** Agent 100 Documentation  
**Approval:** Human approval required

## 1. Purpose and audience

This guide describes the project-independent Generic Agentic SDLC Framework: a governed control plane for GitHub Copilot custom agents in Visual Studio Code. It is intended for framework administrators, solution architects, engineering managers, developers, test engineers, assurance teams, release owners, and maintainers of Agent and Skill contracts.

The framework coordinates work. It does not replace project standards, human accountability, source control, security review, release management, or production change approval.

## 2. Verified release-preparation state

Wave 7 has an independent PASS in `docs/framework-work-items/WORK-FWK-SKILLS-001/36-independent-wave-7-explicit-scenario-closure-review.md`. The current repository still reports `VERSION` as `1.0.1`; v1.1.0 is a release-preparation target and is not released, tagged, merged, packaged, or deployed. Agent 90 packaging requires separate authorization.

Verified static test evidence includes 107/107 framework tests, 14 portability fixtures, 14 Agents, seven Skills, provider defaults disabled, and framework validator PASS. Java, Maven, Node, npm, TypeScript, Python package installation, .NET, NuGet, and fixture-project runtime interoperability were not executed by the Wave 7 review.

## 3. Architecture

The operating model has five layers:

1. **User and human authority:** supplies objectives, constraints, approvals, risk decisions, and accountability.
2. **Agent 05 Prompt Router:** converts plain language into a bounded request and explains the route.
3. **Agent 00 SDLC Orchestrator:** controls workflow state, policy, approvals, evidence, routing, and handoffs.
4. **Specialist Agents and Skills:** produce defined analysis, design, implementation, review, test, assurance, build, or documentation artifacts.
5. **Project context and governance:** registries, schemas, workflows, configuration, evidence, memory, status semantics, and hard gates.

Agents represent **WHO** performs a governed responsibility. Skills represent reusable **HOW** procedures. Skill authority is the intersection of the invoking Agent authority, Skill allowlist, project policy, and human/orchestrator gate. A Skill cannot expand Agent authority.

## 4. Directory topology

| Path | Purpose |
| --- | --- |
| `project-template/.github/agents` | 14 Agent contracts |
| `project-template/.github/skills` | Seven reusable Skill definitions |
| `project-template/.github/prompts` | Workflow entry prompts |
| `project-template/registry` | Agent, capability, and Skill registries |
| `project-template/schemas` | Agent, Skill, handoff, evidence, provider, project, state, and memory contracts |
| `project-template/governance` | Execution, grounding, status, and hard-gate policy |
| `project-template/workflows` | Feature, defect, release, assurance, and technology workflows |
| `project-template/config` | Project and optional-provider configuration examples |
| `project-template/providers` | Provider descriptors and boundaries |
| `project-template/tools` | Read-only Azure DevOps and optional-provider tools |
| `scripts` | Bootstrap, global installation, and validation scripts |
| `tests` | Offline framework and portability verification |
| `docs` | Guides, migration, work-item evidence, and release-preparation material |

## 5. Agent catalogue

All 14 Agent contracts are present in numerical order. The required Agents are 00, 05, and 15; 10, 17, 20, 30, 40, 50, 60, 70, 80, 90, and 100 are optional by registry. Agent 80 is manual-only. Every contract uses `agents: []`, `send: false`, governed scope, grounding, prohibited authority escalation, and structured handoffs.

| Agent | Responsibility | Typical inputs and outputs | Skills / gates |
| --- | --- | --- | --- |
| 00 SDLC Orchestrator | State, routing, approvals, policy, evidence, handoffs | Work request, configuration, prior evidence -> route, state, handoff | scope-control, decision-recording, evidence-grounding; all hard gates |
| 05 Prompt Router | Bounded request and route explanation | Plain-language request -> structured intake and missing information | scope-control; never executes or authorizes |
| 10 Business Analyst | Requirements and acceptance criteria | Objectives, stakeholder statements -> requirements, rules, traceability | requirements-analysis, evidence-grounding; human approval |
| 15 Codebase Analyzer | Repository and technology discovery | Repository, manifests, tests -> project context, impact, commands | evidence-grounding; no product edits |
| 17 Technology Lifecycle Analyst | Support, deprecation, EOL, EOS assessment | Agent 15 inventory and authoritative sources -> lifecycle report and recommendation | evidence-grounding; UNKNOWN on unavailable evidence |
| 20 Solution Architect | Smallest compliant technical solution | Approved requirements and constraints -> architecture and ADR candidates | architecture-design, requirements-analysis, decision-recording |
| 30 UI/UX Engineer | UI behavior, accessibility, responsive states | UI requirements and existing design -> interaction specification | project UI standards; scope gate |
| 40 Developer | Approved feature or defect implementation | Approved requirements, ADR, tests -> product change and evidence | tdd-implementation, requirements-analysis, architecture-design |
| 50 Reviewer/Overseer | Independent correctness, scope, governance review | Requirements, architecture, diff, tests -> findings and verdict | scope-control, evidence-grounding, decision-recording |
| 60 Test Engineer | Requirement-based test execution | Acceptance criteria, risks, environment -> test evidence and status | testing-strategy, tdd-implementation, requirements-analysis |
| 70 Automation Engineer | Stable test/process automation | Approved test conditions and tooling -> automation and evidence | testing-strategy |
| 80 Security/Performance Engineer | Authorized security and performance assessment | Written scope, safe environment, thresholds -> findings and re-test evidence | manual-only; explicit security/performance authorization |
| 90 Build/Deploy Engineer | Build, provenance, packaging, controlled deployment | Approved commit, environment, rollback -> artifact/build/deploy evidence | separate Agent 90 authorization; production human gate |
| 100 Documentation Agent | Verified technical, user, release, and operational docs | Final artifacts and evidence -> documentation package | decision-recording; documentation authorization |

Every Agent must return a structured handoff to Agent 00. Specialists do not freely delegate, self-approve, merge, close tickets, deploy, or change workflow state outside their contract.

## 6. Skill catalogue

All seven Skills are v1.1.0, ACTIVE, compatible with `>=1.1.0 <2.0.0`, require intersection authority, and use human/orchestrator approval gates. All prohibit approve, merge, deploy, workflow-state change, unauthorized remedial database changes, unauthorized remedial security changes, silent handoff, and status coercion unless a stricter project rule applies.

| Skill | Owner and allowed Agents | Purpose, inputs, outputs |
| --- | --- | --- |
| `architecture-design` | Agent 20; 40, 50 | Traceable architecture from approved requirements; inputs requirements/constraints; outputs design, traceability, ADR candidates |
| `decision-recording` | Agent 00; 20, 40, 50, 100 | Material decision records; inputs context, alternatives, rationale; outputs decision record and traceability update |
| `requirements-analysis` | Agent 10; 20, 40, 60 | Atomic requirements and acceptance criteria; inputs goals/specifications/statements; outputs requirements and traceability |
| `tdd-implementation` | Agent 40; 50, 60 | Red-green-refactor implementation; inputs approved task, criteria, architecture; outputs implementation, test evidence, change traceability |
| `testing-strategy` | Agent 60; 50, 70 | Unit, integration, negative, boundary, security, and regression planning/execution; outputs conditions, evidence, coverage traceability |
| `scope-control` | Agent 00; 05, 40, 50 | Minimum change, scope comparison, and stop conditions; outputs scope decision and evidence |
| `evidence-grounding` | Agent 00, 10, 15, 20, 40, 50 | Evidence classification, provenance, and non-success handling; outputs classified evidence and status decision |

Skill front matter is reconciled with `registry/skills.yaml` and `skill-contract.schema.json`. The registry, not documentation, is authoritative for invocation allowlists.

## 7. Agent-to-Skill relationship matrix

| Agent | Skills |
| --- | --- |
| 00 | decision-recording, scope-control, evidence-grounding |
| 05 | scope-control |
| 10 | requirements-analysis, evidence-grounding |
| 15 | evidence-grounding |
| 17 | evidence-grounding |
| 20 | architecture-design, decision-recording, requirements-analysis, evidence-grounding |
| 30 | project-specific UI contract; no shared Skill currently required |
| 40 | architecture-design, decision-recording, requirements-analysis, tdd-implementation, evidence-grounding, scope-control |
| 50 | architecture-design, decision-recording, requirements-analysis, tdd-implementation, testing-strategy, scope-control, evidence-grounding |
| 60 | requirements-analysis, tdd-implementation, testing-strategy |
| 70 | testing-strategy |
| 80 | explicit manual assurance contract; no shared Skill required |
| 90 | project release contract; no shared Skill required |
| 100 | decision-recording |

## 8. Copilot instructions and precedence

Precedence is: framework governance, current human instruction, project guardrails, approved architecture/ADR, explicit coding standards, requirements and ticket acceptance criteria, repository conventions, framework defaults, then Agent preference. `project-template/.github/copilot-instructions.md` supplies minimum-change, evidence, security, testing, scope, and authority rules. Project-local instructions refine behavior; they cannot weaken hard gates or allow self-approval.

## 9. Governance and status

`MANUAL`, `HYBRID`, and `AUTONOMOUS` execution modes control permitted automation, not authority. Human approval remains authoritative. The framework preserves `PASS`, `PASSED`, `REWORK_REQUIRED`, `FAILED`, `BLOCKED`, `DEFERRED`, `PARTIAL`, `UNKNOWN`, and `NOT_TESTED`; no unresolved state is PASS.

Evidence labels are FACT, INFERENCE, ASSUMPTION, UNKNOWN, RECOMMENDATION, PROJECT_DECLARED_EVIDENCE, and CODE_INTELLIGENCE_EVIDENCE. Preserve source, timestamp, command, exit code, artifact path, approval, hash, confidence, and limitation. A structured handoff includes source/target Agent, objective, inputs, artifacts, decisions, constraints, risks, blockers, evidence, required approval, recommended next action, and status.

Minimum-change/Ponytail/YAGNI controls reject invented requirements, unrelated refactoring, speculative dependencies, unsupported flexibility, duplicate implementation, silent scope expansion, status coercion, automated approvals, automated merges, automated deployments, unauthorized remedial database changes, unauthorized remedial security changes, and silent handoff.

## 10. Installation and bootstrap

### Prerequisites

Use a supported VS Code installation with GitHub Copilot Chat, Git, Python 3 for validation, and PowerShell for scripts. Provider installation is not a prerequisite. Use an isolated branch or worktree.

### Validate

```powershell
python scripts/validate_framework.py project-template
python -m unittest discover -s tests -v
```

Expected output includes `Framework validation passed` and an all-OK test suite. Do not claim PASS for an unexecuted, failed, blocked, partial, or unknown result.

### Project-local bootstrap

```powershell
pwsh ./scripts/bootstrap-project.ps1 -ProjectPath 'C:\Projects\YourApplication'
```

The script copies the generic project template recursively, skips existing files by default, reports conflicts, and preserves project-owned files. Review output and validate the target. Force behavior is a deliberate overwrite path and requires an isolated backup/branch.

### Global Agent/Skill installation

```powershell
pwsh ./scripts/install-global.ps1
```

Global installation is limited to Agents and Skills. Project-local configuration, schemas, workflows, governance, and providers remain project-local.

## 11. Migration, backup, recovery, and removal

For v1.0.1 to v1.1.0 preparation: create a branch or backup, inventory custom files, run the baseline tests, bootstrap non-force, review conflicts, preserve local customizations, validate, then run the full suite. Recovery is a restore of the backup or branch followed by validation. Force mode is only for an intentionally disposable or reconciled target. Remove only files owned by the framework after comparing customized paths; never delete project-owned files automatically.

Rollback to the no-provider baseline means set both modes to `DISABLED`, remove external endpoints/executables, preserve original context/evidence, validate, and rerun tests. VERSION remains a read-only release-control input until separately authorized Agent 90 work.

## 12. Provider boundaries

Graphify is an external optional code-intelligence provider. It is `DISABLED` by default, produces `CODE_INTELLIGENCE_EVIDENCE`, and has `SUPPLEMENTAL_ONLY` authority. Only Agents 15, 20, 40, and 50 may consume corroborated output. Direct repository evidence wins disagreements. Stale, partial, unsupported, malformed, missing-provenance, or unverified output falls back to repository inspection.

Headroom is an external optional context-optimization provider. It is `DISABLED` by default and has authority `NONE`. Only the configured allowlist may consume output after separate human approval. SHADOW output is quarantined and comparison-only. Protected evidence remains retrievable with immutable references and hashes. Failures fall back to original context.

Provider modes are `DISABLED`, `SHADOW`, and `ENABLED`. Agent 00 mediates submission and runtime disable. Human approval is required for SHADOW, ENABLED, and re-enablement. Providers cannot approve, route, merge, deploy, remediate, hand off, mutate workflow state, or coerce status. Wave 8 documentation does not claim a provider trial occurred; both real providers remain uninstalled, uncontacted, and unexecuted.

## 13. Troubleshooting

| Symptom | Action |
| --- | --- |
| Agents missing | Confirm workspace root, `.github/agents`, front matter, Copilot Agent mode, then reload VS Code. |
| Validator failure | Fix the exact reported contract/path/registry error and rerun tests before validation. |
| Existing-file conflict | Review non-force output and merge intentionally; do not force overwrite by default. |
| Azure DevOps disabled | Empty URL is an intentional safe no-op. Configure only with approved read-only access. |
| Missing lifecycle evidence | Return UNKNOWN or REWORK_REQUIRED; do not infer current support. |
| Test environment missing | Return BLOCKED or NOT_TESTED with prerequisite and owner. |
| Provider unavailable | Use direct repository/original-context fallback; preserve non-success provider status. |
| Production request | Stop at the human production gate. Agent 90 authorization is separate. |

## 14. Release and adoption gates

The v1.1.0 package is release preparation only. Required future gates include Agent 50 technical/documentation review, human approval, Agent 90 packaging authorization, version-control decision, clean artifact provenance, and manual deployment approval. No package, release, tag, merge, publication, provider activation, pilot adoption, or consuming-project adoption is claimed here.

## 15. Traceability

FWK-REQ-018 is addressed by migration, backup, recovery, installer, and upgrade documentation. FWK-REQ-021 is addressed by the 25-requirement/98-test traceability baseline and Wave 8 document inventory. FWK-REQ-022 is addressed by this reference, the user guide, migration guide, README, CHANGELOG, and management roadmap, with generated DOCX/PPTX deliverables in the authorized paths. FWK-REQ-023 through FWK-REQ-025 are documented as optional, disabled, non-authoritative provider boundaries with approval, fallback, fidelity, provenance, disablement, and rollback controls.

## 16. Known limitations

This package documents verified repository behavior and explicitly labels untested runtime interoperability. It does not claim release, provider trial, production readiness, or project adoption. Governance logging remains `PENDING_LOG_APPEND`. Human approval remains mandatory.

## Appendix: authoritative sources

- `VERSION`
- `project-template/registry/agents.yaml`
- `project-template/registry/skills.yaml`
- `project-template/config/project.example.yaml`
- `project-template/providers/*.md`
- `project-template/schemas/*.json`
- `scripts/bootstrap-project.ps1`
- `scripts/install-global.ps1`
- `scripts/validate_framework.py`
- `tests/test_framework.py`
- Wave 7 independent PASS report 36
