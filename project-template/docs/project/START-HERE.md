# Start Here — Using the Governed Copilot Lifecycle

## First prompt

Open Copilot Chat, select the `orchestrator` custom agent, and send:

```text
Start the governed project lifecycle.
Project goal: <describe the project or requested change>.
First inspect all relevant existing code, documentation, tests, and architecture.
Do not make production-code changes during planning.
```

## Normal lifecycle

1. `planner` creates/updates the project charter and stops.
2. You review it and explicitly send `APPROVE PLANNING` to the orchestrator.
3. `requirements-analyst` decomposes the approved scope into requirements and acceptance criteria.
4. You send `APPROVE REQUIREMENTS`.
5. `solution-architect` creates the architecture and ADRs.
6. You send `APPROVE ARCHITECTURE`.
7. `implementation-planner` creates small dependency-ordered tasks and test obligations.
8. You send `APPROVE IMPLEMENTATION PLAN`.
9. `developer` implements approved tasks only.
10. `test-engineer` independently executes requirement-based automated verification.
11. `reviewer` independently assesses requirements, architecture, security, maintainability, tests, and Definition of Done.
12. `orchestrator` closes the lifecycle only when the evidence supports completion.

## When scope changes during implementation

Send the change back through the affected lifecycle stage. Do not tell the developer to "just make the change." The affected gate should be marked `CHANGES_REQUIRED`, the baseline updated, and human approval obtained again.

## Decision rule

- Routine material decision -> `docs/project/DECISION-LOG.md`.
- Architectural or expensive-to-reverse decision -> new ADR in `docs/adr/`.

## Testing rule

A statement such as "tests should pass" is not evidence. Record the exact test command and observed result in `TEST-RESULTS.md`.
