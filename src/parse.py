from __future__ import annotations

from typing import Iterable, List

from models import ReflogEntry


def parse_reflog_lines(lines: Iterable[str]) -> List[ReflogEntry]:
    entries: List[ReflogEntry] = []
    for line in lines:
        parts = line.split("|", 5)
        if len(parts) != 6:
            continue
        ref_sel, msg, sha, ts, cn, ce = parts
        try:
            ts_i = int(ts)
        except ValueError:
            continue
        entries.append(
            ReflogEntry(
                ref_selector=ref_sel,
                message=msg,
                sha=sha,
                timestamp=ts_i,
                committer_name=cn,
                committer_email=ce,
            )
        )
    return entries
