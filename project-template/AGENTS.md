# Governed Agentic SDLC Rules

These instructions apply to every AI coding agent operating in this repository.

## Mandatory lifecycle

`PLAN -> REQUIREMENTS -> ARCHITECTURE -> IMPLEMENTATION PLAN -> DEVELOP -> TEST -> REVIEW -> COMPLETE`

Do not implement production-code changes directly from an unstructured request.

## Human approval gates

Production implementation is prohibited until all of these gates in `docs/project/SDLC-STATE.json` are explicitly `APPROVED`:

- planning
- requirements
- architecture
- implementationPlan

Only explicit human approval can set a gate to `APPROVED`. Agent recommendations are not approval.

## Change control

If implementation reveals a need to alter approved scope, requirements, architecture, or interfaces:

1. Stop the affected implementation.
2. Record the proposed change and rationale.
3. Mark the affected gate `CHANGES_REQUIRED`.
4. Update the affected artifacts.
5. Obtain explicit human re-approval.
6. Resume implementation only after the dependent gates are valid again.

## Decision records

Record all material decisions.

- Routine project decisions -> `docs/project/DECISION-LOG.md`
- Architectural/difficult-to-reverse decisions -> `docs/adr/ADR-NNNN-*.md`

Never erase or rewrite historical decisions. Supersede them explicitly.

## Requirements and traceability

Requirements and acceptance criteria must have stable identifiers. Maintain the chain:

`Requirement -> Acceptance Criterion -> Architecture/ADR -> TASK -> Code -> Test -> Result`

Update `docs/project/REQUIREMENTS-TRACEABILITY.md` as work progresses.

## Testing evidence

Never state that tests, builds, linting, security checks, or quality gates passed unless the command was actually executed and its result inspected.

The test-engineer role must independently derive tests from requirements and acceptance criteria, rather than merely testing current implementation behavior.

## Review independence

The developer does not provide final independent testing approval. The test engineer does not provide final independent code-review approval. The reviewer reports findings without silently changing production code.

## Definition of Done

A change is done only when all applicable items are satisfied:

- Approved requirement and acceptance criteria exist.
- Architecture and relevant ADRs are approved/current.
- Implementation task is complete.
- Automated tests exist at appropriate layers.
- Relevant tests, build, lint, and security checks pass.
- Test results contain actual execution evidence.
- Traceability is current.
- Decision records are current.
- Documentation/operational notes are current.
- Independent review has no unresolved BLOCKER or CRITICAL finding.
- CI-required checks pass.
