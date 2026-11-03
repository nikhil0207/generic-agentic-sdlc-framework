---
name: requirements-analysis
description: Turn project goals, source specifications, issues, and stakeholder statements into atomic, testable requirements and acceptance criteria with traceability.
id: requirements-analysis
version: 1.1.0
purpose: Turn goals and source statements into atomic testable requirements.
applicability: Requirements analysis and acceptance criteria.
location: .github/skills/requirements-analysis/SKILL.md
owner_agent: 10-business-analyst
invoking_agent_allowlist: [10-business-analyst, 20-solution-architect, 40-developer, 60-test-engineer]
lifecycle_phases: [REQUIREMENTS, ARCHITECTURE, DEVELOPMENT, TEST]
inputs: [goals, source_specifications, stakeholder_statements]
outputs: [requirements, acceptance_criteria, traceability]
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
# Requirements Analysis

1. Identify authoritative sources and distinguish them from assumptions.
2. Decompose broad statements until each requirement expresses one testable obligation.
3. Assign stable requirement IDs by type: FR, NFR, SEC, DATA, INT.
4. For behavioral requirements, capture preconditions, trigger, expected outcome, validation/error behavior, and acceptance criteria.
5. Include relevant non-functional requirements: performance, availability, security, privacy, accessibility, auditability, observability, maintainability, and recovery.
6. Identify ambiguity or conflicts rather than inventing hidden business rules.
7. Add every requirement/acceptance criterion to the traceability matrix.
8. Record material interpretation decisions.
