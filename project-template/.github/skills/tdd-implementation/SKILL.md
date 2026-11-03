---
name: tdd-implementation
description: Implement an approved development task using a disciplined red-green-refactor verification loop. Use for business logic, defect fixes, and behavior changes where automated tests are practical.
id: tdd-implementation
version: 1.1.0
purpose: Implement approved work through a red-green-refactor verification loop.
applicability: Approved development and defect-fix work.
location: .github/skills/tdd-implementation/SKILL.md
owner_agent: 40-developer
invoking_agent_allowlist: [40-developer, 50-reviewer-overseer, 60-test-engineer]
lifecycle_phases: [DEVELOPMENT, REVIEW, TEST]
inputs: [approved_task, requirements, acceptance_criteria, architecture]
outputs: [implementation, test_evidence, change_traceability]
evidence_requirements: [FACT, INFERENCE, UNKNOWN, RECOMMENDATION]
allowed_operations: [read, search, edit, execute]
prohibited_operations: [approve, route, merge, deploy, workflow_state_change, database_remediation, security_remediation, silent_handoff, status_coercion]
authority_inheritance: INTERSECTION_REQUIRED
approval_behavior: HUMAN_OR_ORCHESTRATOR_GATE_ONLY
provider_dependencies: []
framework_compatibility: '>=1.1.0 <2.0.0'
metadata_reconciliation: {source: registry, front_matter_required: true, conflict_status: REWORK_REQUIRED}
integrity_metadata: {hash_algorithm: SHA-256, content_hash: NOT_COMPUTED}
lifecycle_status: ACTIVE
---
# TDD Implementation

For each approved task:

1. Read linked requirements, acceptance criteria, architecture, and ADRs.
2. Write the smallest meaningful failing test that demonstrates the required behavior or defect.
3. Run the test and confirm it fails for the expected reason.
4. Implement the minimum coherent production change.
5. Run the targeted test until it passes.
6. Refactor without changing behavior.
7. Run the relevant broader test/build/lint suite.
8. Update traceability and test evidence.
9. Never change the expected behavior merely to make a test pass; if the requirement is wrong, use change control.
