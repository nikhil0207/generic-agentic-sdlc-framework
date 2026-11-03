# Structured Handoff Protocol

Every specialist returns control to `00-sdlc-orchestrator`. Agents must not silently invoke one another.

```yaml
source_agent: 40-developer
target_agent: 00-sdlc-orchestrator
objective: Review implementation evidence and select the next permitted step
inputs: []
artifacts: []
decisions: []
constraints: []
assumptions: []
risks: []
open_questions: []
blocking_issues: []
evidence: []
required_approval: null
recommended_next_action: Run independent review
status: AWAITING_HUMAN_APPROVAL
```

Use explicit empty arrays. Never omit unknown or unresolved information. A handoff recommendation cannot approve the originating agent's work.
