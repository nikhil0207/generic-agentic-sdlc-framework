---
name: Requirement-Based Testing
description: Apply requirement traceability and evidence rules when creating or editing automated tests.
applyTo: "**/*.test.*,**/*.spec.*,**/tests/**,**/*Tests.cs,**/test_*.py,**/*_test.py"
---
# Requirement-Based Testing Instructions

- Map material tests to requirement or acceptance-criterion IDs.
- Prefer deterministic tests with explicit setup and cleanup.
- Include negative, boundary, authorization, and failure-path scenarios when relevant.
- Do not weaken assertions to accommodate incorrect implementation behavior.
- Run the test and inspect the real result before recording PASS.
- Update `docs/project/REQUIREMENTS-TRACEABILITY.md` and `docs/project/TEST-RESULTS.md` with material verification evidence.
