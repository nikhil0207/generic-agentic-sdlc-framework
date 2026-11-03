from __future__ import annotations

import json
from pathlib import Path
import sys

REQUIRED_FILES = [
    Path('AGENTS.md'),
    Path('.github/copilot-instructions.md'),
    Path('docs/project/SDLC-STATE.json'),
    Path('docs/project/START-HERE.md'),
    Path('docs/project/PROJECT-CHARTER.md'),
    Path('docs/project/REQUIREMENTS.md'),
    Path('docs/project/REQUIREMENTS-TRACEABILITY.md'),
    Path('docs/project/ARCHITECTURE.md'),
    Path('docs/project/IMPLEMENTATION-PLAN.md'),
    Path('docs/project/TEST-STRATEGY.md'),
    Path('docs/project/TEST-RESULTS.md'),
    Path('docs/project/REVIEW-RESULTS.md'),
    Path('docs/project/DECISION-LOG.md'),
]
VALID_STATUSES = {'PENDING', 'BLOCKED', 'READY_FOR_APPROVAL', 'APPROVED', 'CHANGES_REQUIRED', 'FAILED', 'PASSED'}
REQUIRED_GATES = {'planning', 'requirements', 'architecture', 'implementationPlan', 'testing', 'review'}


def fail(message: str) -> int:
    print(f'ERROR: {message}', file=sys.stderr)
    return 1


def main() -> int:
    missing = [str(p) for p in REQUIRED_FILES if not p.exists()]
    if missing:
        return fail('Missing required SDLC files: ' + ', '.join(missing))

    try:
        state = json.loads(Path('docs/project/SDLC-STATE.json').read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        return fail(f'SDLC-STATE.json is invalid JSON: {exc}')

    gates = state.get('gates')
    if not isinstance(gates, dict):
        return fail('SDLC-STATE.json must contain an object named gates.')

    if set(gates) != REQUIRED_GATES:
        return fail(f'Expected gates {sorted(REQUIRED_GATES)}, got {sorted(gates)}')

    for name, gate in gates.items():
        status = gate.get('status') if isinstance(gate, dict) else None
        if status not in VALID_STATUSES:
            return fail(f'Gate {name} has invalid status {status!r}.')

    if state.get('currentPhase') == 'complete':
        not_approved = [
            name for name, gate in gates.items()
            if name in {'planning', 'requirements', 'architecture', 'implementationPlan'}
            and gate.get('status') != 'APPROVED'
        ]
        if not_approved:
            return fail('A completed lifecycle has unapproved prerequisite gates: ' + ', '.join(not_approved))
        if gates['testing']['status'] != 'PASSED' or gates['review']['status'] != 'PASSED':
            return fail('A completed lifecycle requires testing and review gates to be PASSED.')

    print('SDLC metadata validation passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
