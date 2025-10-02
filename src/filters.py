from __future__ import annotations

from typing import Callable, List, Optional
import re
from datetime import datetime, timezone

from models import ReflogEntry
from settings import AppSettings


def _parse_since(expr: Optional[str]) -> Optional[int]:
    if not expr:
        return None
    m = re.fullmatch(r"(\d+)([smhdw])", expr.strip())
    if not m:
        return None
    qty = int(m.group(1))
    unit = m.group(2)
    seconds = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
    }[unit]
    return int(datetime.now(timezone.utc).timestamp()) - qty * seconds


def build_filters(config: AppSettings) -> Callable[[List[ReflogEntry]], List[ReflogEntry]]:
    def apply(entries: List[ReflogEntry]) -> List[ReflogEntry]:
        result = entries
        cutoff = _parse_since(config.since)
        if cutoff is not None:
            result = [e for e in result if e.timestamp >= cutoff]
        if config.author:
            pat = re.compile(re.escape(config.author), re.IGNORECASE)
            result = [e for e in result if pat.search(e.committer_name) or pat.search(e.committer_email)]
        if config.ops:
            allowed = set([op.strip().lower() for op in config.ops])
            from heuristics import Heuristics

            hz = Heuristics()
            result = [e for e in result if hz.classify_action_from_message(e.message).value in allowed]
        return result

    return apply

 


