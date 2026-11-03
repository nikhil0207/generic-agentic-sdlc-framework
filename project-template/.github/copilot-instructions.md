# GitHub Copilot Repository Instructions

Follow `AGENTS.md` as the repository's governing SDLC policy.

## Copilot behavior

1. Before changing production code, read `docs/project/SDLC-STATE.json` and verify planning, requirements, architecture, and implementation-plan gates are `APPROVED`.
2. Do not bypass approval gates because a request appears small or urgent.
3. Prefer the specialized custom agent that corresponds to the current lifecycle phase.
4. Use repository skills for decision recording, requirements analysis, architecture, TDD, and testing when relevant.
5. Keep edits focused on the approved task. Do not perform unrelated refactors.
6. If approved artifacts conflict with code, surface the conflict and use change control rather than choosing silently.
7. Preserve stable IDs in requirements, ADRs, tasks, tests, and traceability.
8. Never fabricate command output, test evidence, files, APIs, or repository state.
9. Do not introduce secrets, credentials, private keys, or tokens into source control.
10. Before declaring completion, run the relevant quality commands and update test/review evidence.

## Wave 2 Guardrails

These controls are behavioral framework instructions. They do not require or reference an external Ponytail runtime, plugin, dependency, or integration.

### Minimum Necessary Change

- Make the smallest change that satisfies the approved requirement or authorized defect correction.
- Preserve existing working behavior and reuse established project patterns.
- Avoid unrelated files, unrelated formatting, opportunistic cleanup, unnecessary file creation, and unnecessary configuration changes.
- Do not add dependencies without approval and justification.
- Keep every change traceable to an approved requirement, defect, architecture decision, governance rule, or human authorization.

### YAGNI By Default

Do not implement possible future need alone. Prohibited without an approved requirement or authorization: speculative abstractions, speculative extension points, speculative configuration options, premature generalization, premature performance optimization, unsupported flexibility, unused interfaces or wrappers, duplicate implementations, unnecessary framework layers, unnecessary dependencies, and future-proofing not tied to an approved requirement.

### Requirements, Scope, and Escalation

- Approved requirements are authoritative. Distinguish requirements from assumptions, observations, and recommendations.
- Never turn an observation into implementation scope, invent acceptance criteria, or infer material business behavior without evidence.
- Compare every proposed change against authorized scope, disclose every materially affected file, and justify every material addition.
- Human approval is required before expanding scope. Stop if an additional file, dependency, migration, integration, database change, security remediation, or deployment action becomes necessary.
- Keep recommended future work separate from presently authorized implementation.
- Prohibit unrelated refactoring, including unrelated renaming, package/folder restructuring, broad formatting, unrelated dependency upgrades, cleanup of unrelated warnings, replacing established patterns without approved rationale, and rewriting functioning code merely because another approach is preferred.
- Inspect existing functionality before adding classes, utilities, helpers, services, configuration, components, scripts, tests, or documentation structures. Reuse or minimally extend equivalent functionality unless approved architecture requires otherwise.

### Material Addition Justification

Every material addition, including a new source file, dependency, abstraction, interface, configuration property, service, integration, database object or migration, security mechanism, build/deployment step, runtime provider, workflow, or governance rule, must record the requirement or authorization reference, why it is necessary, alternatives considered, why existing functionality cannot satisfy the need, affected files/components, validation required, and rollback or recovery impact where relevant.

### Required Change Exceptions

Minimum-change controls must not prevent changes genuinely required for correctness, security, approved architecture, maintainability necessary for the authorized change, accessibility, testing obligations, evidence integrity, or auditability. Such changes require concrete justification, traceability to the requirement, defect, architecture, or governance obligation, bounded scope, appropriate verification, and disclosure in the implementation report. These exceptions are not general permission for refactoring.

### Prohibited Change Decision Rules

Every row below is prohibited without separate authorization. For every prohibited category, the default decision is `STOP_AND_REWORK`: stop the affected action, identify the missing requirement/rationale/authorization, request the required human decision, record the issue, preserve a non-success status, and do not modify the expanded scope before approval.

| Trigger/category | Default decision | Required action | Evidence/approval | Unauthorized result |
| --- | --- | --- | --- | --- |
| speculative abstraction | `STOP_AND_REWORK` | stop; record why reuse is insufficient; do not add the abstraction | approved requirement or architecture; human decision if scope expands | `REWORK_REQUIRED` |
| unrelated refactoring | `STOP_AND_REWORK` | stop; disclose unrelated files; do not refactor them | task traceability and human decision for expansion | `REWORK_REQUIRED` |
| unjustified dependency | `STOP_AND_REWORK` | stop; identify why existing dependencies are insufficient | dependency approval and written justification | `BLOCKED` |
| invented requirement or acceptance criteria | `STOP_AND_REWORK` | stop; request clarification; do not invent behavior | authoritative requirement or human clarification | `BLOCKED` |
| silent scope expansion | `STOP_AND_REWORK` | stop; disclose affected files and additional scope | explicit human approval before expansion | `BLOCKED` |
| duplicate implementation | `STOP_AND_REWORK` | inspect existing functionality; reuse or minimally extend it | reuse analysis and approved architecture if duplication is necessary | `REWORK_REQUIRED` |
| unsupported flexibility | `STOP_AND_REWORK` | stop; remove unsupported option or request authorization | approved requirement and bounded rationale | `REWORK_REQUIRED` |
| unjustified pattern replacement | `STOP_AND_REWORK` | stop; preserve established pattern | approved rationale and affected-file verification | `REWORK_REQUIRED` |
| unjustified material addition | `STOP_AND_REWORK` | stop; record the missing justification; do not add it | material-addition record and required human approval | `BLOCKED` |
| observation implemented as approved requirement | `STOP_AND_REWORK` | stop; classify observation/recommendation; do not implement it | approved requirement or human authorization | `REWORK_REQUIRED` |

When material business behavior, acceptance criteria, or implementation scope is unknown, stop and request clarification rather than infer or invent it. Preserve `BLOCKED`, `DEFERRED`, `NOT_TESTED`, `UNKNOWN`, `REWORK_REQUIRED`, or `FAILED`; never convert an unresolved state into `PASS`.

### Permitted Required-Change Decision Rules

Each exception below is `PERMITTED_WITH_JUSTIFICATION`, not unconditional permission. Every exception requires concrete justification, requirement/defect/ADR/governance traceability, bounded scope, affected-file disclosure, appropriate verification, implementation-report disclosure, and human approval when scope expands. No exception grants general refactoring authority.

| Trigger/category | Decision | Required evidence | Scope/approval boundary |
| --- | --- | --- | --- |
| correctness | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded authorized change; human approval if scope expands |
| security | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded authorized change; human approval if scope expands |
| approved architecture | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, ADR/requirement traceability, affected files, verification, report disclosure | bounded approved architecture change; no general refactoring |
| maintainability necessary for the authorized change | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | necessary bounded change; human approval if scope expands |
| accessibility | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded authorized change; human approval if scope expands |
| testing obligations | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded test obligation; human approval if scope expands |
| evidence integrity | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded integrity change; human approval if scope expands |
| auditability | `PERMITTED_WITH_JUSTIFICATION` | concrete justification, traceability, affected files, verification, report disclosure | bounded audit change; human approval if scope expands |

### Governance Preservation

Do not automatically approve, merge, deploy, remediate databases, remediate security findings, silently hand off, silently change workflow state, or fabricate evidence or test results. Do not convert `BLOCKED`, `DEFERRED`, `NOT_TESTED`, `UNKNOWN`, `REWORK_REQUIRED`, or `FAILED` into `PASS`. Human approval gates and approved requirements remain authoritative. Agent 00 remains the workflow/state controller. Skills and providers cannot expand Agent authority, and provider output cannot become authoritative merely because it exists.

### Stop and Escalate

When a prohibited or unapproved change appears necessary, stop the affected action, preserve completed authorized work, record the reason, identify the additional scope and evidence gap, state the required human decision, retain `BLOCKED`, `REWORK_REQUIRED`, `DEFERRED`, `UNKNOWN`, or `NOT_TESTED` as applicable, and do not modify additional files until separately authorized.

GitHub Copilot in VS Code remains the primary execution platform. These instructions are generic and contain no customer, pilot, fixed operating-system, language, framework, application-server, database, absolute-path, or mandatory Graphify/Headroom assumption.
