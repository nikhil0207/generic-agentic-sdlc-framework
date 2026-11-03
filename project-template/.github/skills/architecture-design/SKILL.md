---
name: architecture-design
description: Design traceable solution architecture from approved requirements, with clear component boundaries, interfaces, security, data flow, deployment concerns, and ADRs.
id: architecture-design
version: 1.1.0
purpose: Design traceable solution architecture from approved requirements.
applicability: Architecture and governed design work.
location: .github/skills/architecture-design/SKILL.md
owner_agent: 20-solution-architect
invoking_agent_allowlist: [20-solution-architect, 40-developer, 50-reviewer-overseer]
lifecycle_phases: [ARCHITECTURE, DEVELOPMENT, REVIEW]
inputs: [approved_requirements, repository_constraints]
outputs: [architecture_design, traceability, adr_candidates]
evidence_requirements: [FACT, INFERENCE, ASSUMPTION, UNKNOWN, RECOMMENDATION]
allowed_operations: [read, search]
prohibited_operations: [approve, route, merge, deploy, workflow_state_change, database_remediation, security_remediation, silent_handoff, status_coercion]
authority_inheritance: INTERSECTION_REQUIRED
approval_behavior: HUMAN_OR_ORCHESTRATOR_GATE_ONLY
provider_dependencies: []
framework_compatibility: '>=1.1.0 <2.0.0'
metadata_reconciliation: {source: registry, front_matter_required: true, conflict_status: REWORK_REQUIRED}
integrity_metadata: {hash_algorithm: SHA-256, content_hash: NOT_COMPUTED}
lifecycle_status: ACTIVE
---
# Architecture Design

1. Begin from approved requirements and existing codebase constraints.
2. Define components with one clear responsibility and explicit dependencies/interfaces.
3. Describe data flow, persistence, APIs/events, authentication/authorization, validation, errors, logging/audit, observability, deployment, scaling, and recovery where applicable.
4. Map architecture elements back to requirement IDs.
5. For difficult-to-reverse choices, compare realistic alternatives and record an ADR.
6. Avoid unrelated redesign. Preserve established patterns unless they prevent the approved requirement or create material risk.
7. Define the testing seams and observability needed to verify the architecture.
