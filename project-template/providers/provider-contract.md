# Optional Provider Contract

Providers are external, optional, project-local integrations. Modes are `DISABLED`, `SHADOW`, and `ENABLED`; default is `DISABLED`. `allowed_agents` means usable-output consumers only. Providers cannot approve, route, merge, deploy, remediate, hand off, mutate workflow state, or coerce status.

Agent 00 mediates submission and runtime disable. Human approval remains required for SHADOW, ENABLED, and re-enablement. Failures use the baseline fallback and preserve non-success status.
