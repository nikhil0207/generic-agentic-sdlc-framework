from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import sys


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {"unparsed": raw}

    record = {
        "recordedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "event": payload,
    }

    target = Path('.copilot/audit/events.jsonl')
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(json.dumps({"continue": True}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
