---
name: decision-recording
description: Record material software-delivery decisions consistently. Use whenever requirements, architecture, implementation, testing, scope, sequencing, or operational choices are made or reversed.
id: decision-recording
version: 1.1.0
purpose: Record material delivery decisions consistently.
applicability: Requirements, architecture, implementation, testing, and scope decisions.
location: .github/skills/decision-recording/SKILL.md
owner_agent: 00-sdlc-orchestrator
invoking_agent_allowlist: [00-sdlc-orchestrator, 20-solution-architect, 40-developer, 50-reviewer-overseer, 100-documentation]
lifecycle_phases: [REQUIREMENTS, ARCHITECTURE, DEVELOPMENT, REVIEW, DOCUMENTATION]
inputs: [decision_context, alternatives, rationale]
outputs: [decision_record, traceability_update]
evidence_requirements: [FACT, INFERENCE, ASSUMPTION, UNKNOWN, RECOMMENDATION]
allowed_operations: [read, search, edit]
prohibited_operations: [approve, route, merge, deploy, workflow_state_change, database_remediation, security_remediation, silent_handoff, status_coercion]
authority_inheritance: INTERSECTION_REQUIRED
approval_behavior: HUMAN_OR_ORCHESTRATOR_GATE_ONLY
provider_dependencies: []
framework_compatibility: '>=1.1.0 <2.0.0'
metadata_reconciliation: {source: registry, front_matter_required: true, conflict_status: REWORK_REQUIRED}
integrity_metadata: {hash_algorithm: SHA-256, content_hash: NOT_COMPUTED}
lifecycle_status: ACTIVE
---
# Decision Recording

## Choose the record type

Use `docs/project/DECISION-LOG.md` for routine but material project decisions. Use an ADR under `docs/adr/` when a decision affects architecture, security boundaries, persistence, integration contracts, deployment topology, technology selection, or is expensive to reverse.

## Procedure

1. Assign the next stable decision or ADR identifier.
2. State the context/problem, options considered, decision, rationale, consequences, risks, and linked requirement/task/component IDs.
3. Include date and status.
4. Never rewrite a historical decision to make it appear that the earlier choice was different.
5. When reversing a decision, create a new record and mark the old one `Superseded by <new-id>`.
6. Update traceability when the decision changes requirement, architecture, task, or testing mappings.

## Minimum decision-log row

`ID | Date | Phase | Decision | Rationale | Related IDs | Status`
