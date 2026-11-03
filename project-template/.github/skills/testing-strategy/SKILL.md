---
name: testing-strategy
description: Design and execute requirement-based automated testing across unit, integration, API/component, end-to-end, negative, security, boundary, and regression layers.
id: testing-strategy
version: 1.1.0
purpose: Design and execute requirement-based automated testing.
applicability: Unit, integration, negative, boundary, security, and regression testing.
location: .github/skills/testing-strategy/SKILL.md
owner_agent: 60-test-engineer
invoking_agent_allowlist: [50-reviewer-overseer, 60-test-engineer, 70-automation-engineer]
lifecycle_phases: [REVIEW, TEST, AUTOMATION]
inputs: [requirements, acceptance_criteria, risk_register]
outputs: [test_conditions, test_evidence, coverage_traceability]
evidence_requirements: [FACT, INFERENCE, UNKNOWN, RECOMMENDATION]
allowed_operations: [read, search, execute]
prohibited_operations: [approve, route, merge, deploy, workflow_state_change, database_remediation, security_remediation, silent_handoff, status_coercion]
authority_inheritance: INTERSECTION_REQUIRED
approval_behavior: HUMAN_OR_ORCHESTRATOR_GATE_ONLY
provider_dependencies: []
framework_compatibility: '>=1.1.0 <2.0.0'
metadata_reconciliation: {source: registry, front_matter_required: true, conflict_status: REWORK_REQUIRED}
integrity_metadata: {hash_algorithm: SHA-256, content_hash: NOT_COMPUTED}
lifecycle_status: ACTIVE
---
# Testing Strategy

1. Derive test conditions from requirements and acceptance criteria before inspecting whether existing code happens to support them.
2. Choose the lowest-cost test layer that provides reliable evidence; avoid duplicating the same assertion at every layer.
3. Include positive, negative, boundary, authorization, error/retry, and regression scenarios where applicable.
4. Assign stable test IDs and map them in the traceability matrix.
5. Execute commands and record actual results; never infer PASS from code inspection.
6. For web applications, validate critical user journeys with browser/E2E tooling when available.
7. Treat flaky tests as defects to diagnose, not as tests to ignore without a recorded decision.
