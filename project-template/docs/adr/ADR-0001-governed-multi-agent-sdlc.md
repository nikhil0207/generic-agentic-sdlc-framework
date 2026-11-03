# ADR-0001 — Adopt a Governed Multi-Agent SDLC

**Status:** Accepted

**Date:** 2026-08-24

**Related requirements/tasks:** Repository governance

## Context

AI coding assistants can move from vague requests directly into implementation, which can lose requirement rationale, architectural intent, testing independence, and project decisions. The repository requires a repeatable process that can be used across projects while retaining human control over important transitions.

## Options Considered

### Option A — Single general-purpose coding agent

Simple to operate, but role boundaries, independent verification, and approval gates depend heavily on prompt discipline.

### Option B — Specialized lifecycle agents with persisted gates and evidence

Uses separate planning, requirements, architecture, implementation, testing, and review roles. Persists decisions and approvals in repository artifacts and adds deterministic hooks/CI checks.

## Decision

Adopt Option B.

## Rationale

Specialized roles reduce context mixing and accidental scope expansion, while explicit approvals preserve human authority over scope and architecture. Persisted requirements, ADRs, traceability, and test evidence provide an auditable project history.

## Consequences

### Positive

- More consistent project initiation and delivery.
- Better traceability from requirement to test result.
- Explicit architecture and decision history.
- Independent test and review responsibilities.

### Negative / Trade-offs

- More documentation and lifecycle overhead than direct prompting.
- Hook behavior depends on VS Code preview support and organizational policy.
- Project-specific quality commands may still require customization.

## Risks and Mitigations

- **Risk:** Agents skip instructions. **Mitigation:** use hooks and CI for deterministic controls where practical.
- **Risk:** Process becomes too heavy for trivial changes. **Mitigation:** keep artifacts proportional while retaining approval and evidence requirements.
