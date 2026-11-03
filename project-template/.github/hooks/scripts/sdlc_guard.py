from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

STATE_FILE = Path('docs/project/SDLC-STATE.json')
PREREQUISITES = ('planning', 'requirements', 'architecture', 'implementationPlan')
MODIFYING_TOOL_MARKERS = ('editfiles', 'createfile', 'applypatch', 'writefile', 'replaceinfile')
ALLOWED_CONTROL_PREFIXES = (
    'docs/',
    '.github/',
    '.vscode/',
    'agents.md',
)


def all_approved() -> bool:
    if not STATE_FILE.exists():
        return False
    try:
        state = json.loads(STATE_FILE.read_text(encoding='utf-8'))
        gates = state.get('gates', {})
        return all(gates.get(name, {}).get('status') == 'APPROVED' for name in PREREQUISITES)
    except (OSError, json.JSONDecodeError, TypeError):
        return False


def extract_path_candidates(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str) and key.lower() in {'path', 'file', 'filepath', 'filename'}:
                found.append(item)
            else:
                found.extend(extract_path_candidates(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(extract_path_candidates(item))
    elif isinstance(value, str):
        # Some edit tool payloads embed paths in larger strings.
        if '/' in value or '\\' in value:
            for token in re.split(r'[\s,;]+', value):
                if '/' in token or '\\' in token:
                    found.append(token.strip('"\''))
    return found


def normalized(path: str) -> str:
    return path.replace('\\', '/').lstrip('./').lower()


def is_control_file(path: str) -> bool:
    p = normalized(path)
    return any(p == prefix or p.startswith(prefix) for prefix in ALLOWED_CONTROL_PREFIXES)


def response(decision: str, reason: str) -> dict[str, Any]:
    return {
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': decision,
            'permissionDecisionReason': reason,
            'additionalContext': reason,
        }
    }


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print(json.dumps(response('ask', 'SDLC guard could not parse the tool request; require human confirmation.')))
        return 0

    tool_name = str(payload.get('tool_name', '')).lower()
    if not any(marker in tool_name for marker in MODIFYING_TOOL_MARKERS):
        print(json.dumps({'continue': True}))
        return 0

    if all_approved():
        print(json.dumps({'continue': True}))
        return 0

    candidates = extract_path_candidates(payload.get('tool_input', {}))
    if candidates and all(is_control_file(path) for path in candidates):
        print(json.dumps({'continue': True}))
        return 0

    missing = []
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding='utf-8'))
            gates = state.get('gates', {})
            missing = [name for name in PREREQUISITES if gates.get(name, {}).get('status') != 'APPROVED']
        except Exception:
            missing = list(PREREQUISITES)
    else:
        missing = list(PREREQUISITES)

    reason = (
        'Production/workspace edits are blocked by the governed SDLC because prerequisite gates are not approved: '
        + ', '.join(missing)
        + '. Documentation and governance files remain editable. Obtain explicit human approval and update docs/project/SDLC-STATE.json.'
    )
    print(json.dumps(response('deny', reason)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
