---
name: evidence-grounding
description: Classify evidence, preserve provenance, and prevent unsupported conclusions or status coercion.
id: evidence-grounding
version: 1.1.0
purpose: Classify evidence and prevent unsupported conclusions or status coercion.
applicability: Cross-cutting evidence, provenance, and non-success handling.
location: .github/skills/evidence-grounding/SKILL.md
owner_agent: 00-sdlc-orchestrator
invoking_agent_allowlist: [00-sdlc-orchestrator, 10-business-analyst, 15-codebase-analyzer, 20-solution-architect, 40-developer, 50-reviewer-overseer]
lifecycle_phases: [DISCOVERY, REQUIREMENTS, ARCHITECTURE, DEVELOPMENT, REVIEW]
inputs: [source_material, evidence_claim, workflow_state]
outputs: [classified_evidence, provenance_record, status_decision]
evidence_requirements: [FACT, INFERENCE, ASSUMPTION, UNKNOWN, RECOMMENDATION, PROJECT_DECLARED_EVIDENCE, CODE_INTELLIGENCE_EVIDENCE]
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
# Evidence Grounding

1. Classify repository, human-supplied, project-declared, independently verified, historical, generated, provider-derived, and derived-context evidence separately.
2. Preserve exact file paths, references, commands, outputs, errors, exit codes, hashes, approvals, decisions, requirements, criteria, handoffs, provenance, confidence, and checked dates.
3. Record conflicts and reconciliation status; never silently select a conflicting source.
4. Keep FACT, INFERENCE, ASSUMPTION, UNKNOWN, and RECOMMENDATION distinct. Project declarations remain `PROJECT_DECLARED_EVIDENCE`.
5. Treat `CODE_INTELLIGENCE_EVIDENCE` as supplemental and require repository corroboration. Treat Headroom-derived context as non-authoritative and preserve protected raw evidence.
6. Preserve `BLOCKED`, `DEFERRED`, `NOT_TESTED`, `FAILED`, `UNKNOWN`, `REWORK_REQUIRED`, and `PARTIAL`; never convert an unresolved state into `PASS`.
7. Prevent fabricated evidence and require structured handoff evidence. Return evidence only; do not approve, route, mutate workflow state, or authorize implementation.
