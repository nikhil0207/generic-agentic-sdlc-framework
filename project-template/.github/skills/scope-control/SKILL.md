---
name: scope-control
description: Enforce approved scope, minimum change, and governed stop conditions.
id: scope-control
version: 1.1.0
purpose: Enforce approved scope, minimum change, and governance stops.
applicability: Cross-cutting scope and gate checks.
location: .github/skills/scope-control/SKILL.md
owner_agent: 00-sdlc-orchestrator
invoking_agent_allowlist: [00-sdlc-orchestrator, 05-prompt-router, 40-developer, 50-reviewer-overseer]
lifecycle_phases: [ROUTE, DISCOVERY, REQUIREMENTS, ARCHITECTURE, DEVELOPMENT, REVIEW]
inputs: [approved_scope, requested_change, workflow_state]
outputs: [scope_decision, stop_condition, scope_evidence]
evidence_requirements: [FACT, INFERENCE, UNKNOWN, RECOMMENDATION]
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
# Scope Control

1. Compare the requested action and affected files with approved requirements, architecture, defects, governance rules, and human authorization.
2. Inspect existing functionality before proposing a new file, dependency, abstraction, helper, service, configuration property, test structure, or integration.
3. Detect speculative abstractions, unrelated refactoring, unjustified dependencies, invented requirements, silent scope expansion, duplicate implementation, unsupported flexibility, unjustified pattern replacement, and unjustified material additions.
4. For a prohibited change, return `STOP_AND_REWORK`, identify the missing requirement or authorization, preserve completed authorized work, request the human decision, record the issue, and do not modify expanded scope.
5. For a required change exception, record concrete justification, traceability, bounded scope, affected files, verification, report disclosure, and human approval when scope expands. An exception never grants general refactoring authority.
6. When material behavior, acceptance criteria, or implementation scope is unknown, request clarification rather than infer or invent it.
7. Return evidence only. Do not approve scope, mutate workflow state, route work, or authorize implementation.
