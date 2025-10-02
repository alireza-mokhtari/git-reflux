from __future__ import annotations

from typing import List, Tuple

from models import ReflogEntry


def group_sessions(entries: List[ReflogEntry], idle_seconds: int = 45 * 60) -> List[Tuple[str, ReflogEntry]]:
    """Return list of (kind, entry) where kind is 'entry' or 'break'."""
    if not entries:
        return []
    result: List[Tuple[str, ReflogEntry]] = []
    last_ts = entries[0].timestamp
    for e in entries:
        if e.timestamp < last_ts - idle_seconds:
            result.append(("break", e))
        result.append(("entry", e))
        last_ts = e.timestamp
    return result


