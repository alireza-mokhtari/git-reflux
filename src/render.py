from __future__ import annotations

import json
from typing import List
from datetime import datetime, timezone

from rich.console import Console
from rich.table import Table
from rich.rule import Rule

from models import ReflogEntry
from settings import AppSettings
from sessioning import group_sessions
from enrich import Enricher
from cache import LRUCache


def _format_when(ts_now: float, ts_entry: int) -> str:
    delta = int(max(0, ts_now - ts_entry))
    if delta < 60:
        return f"{delta}s ago"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return f"{delta // 86400}d ago"


def render_list(services, entries: List[ReflogEntry], config: AppSettings) -> None:
    console = Console(no_color=config.no_color)
    table = Table(show_header=True, header_style="bold")
    table.add_column("when")
    table.add_column("ref")
    table.add_column("action")
    table.add_column("sha")
    table.add_column("subject")
    table.add_column("size")
    table.add_column("author")

    enricher = Enricher(services.git, LRUCache(256), LRUCache(256))
    now = datetime.now(timezone.utc).timestamp()
    iterable = group_sessions(entries[:50]) if config.group_sessions else [("entry", x) for x in entries[:50]]
    for kind, e in iterable:
        if kind == "break":
            console.print(Rule("— session break —"))
        when = _format_when(now, e.timestamp)
        ref = e.ref_selector
        act = services.heuristics.classify_action_from_message(e.message).value
        action = "reset!" if act == "reset" else act
        sha = e.sha[:7]
        subject = e.message
        stats = enricher.get_diff_stats(e.sha, include_lines=config.stats)
        size = f"files +{stats.files_added}/~{stats.files_modified}/-{stats.files_deleted}"
        if config.stats:
            size = f"Δ +{stats.lines_added}/-{stats.lines_deleted} {size}"
        author = e.committer_name
        table.add_row(when, ref, action, sha, subject, size, author)

    console.print(table)


def render_json(services, entries: List[ReflogEntry], config: AppSettings) -> str:
    enricher = Enricher(services.git, LRUCache(256), LRUCache(256))
    out = []
    for e in entries:
        act = services.heuristics.classify_action_from_message(e.message).value
        stats = enricher.get_diff_stats(e.sha, include_lines=config.stats)
        item = {
            "ref": e.ref_selector,
            "message": e.message,
            "sha": e.sha,
            "timestamp": e.timestamp,
            "action": "reset!" if act == "reset" else act,
            "committer": {"name": e.committer_name, "email": e.committer_email},
            "files": {
                "added": stats.files_added,
                "modified": stats.files_modified,
                "deleted": stats.files_deleted,
            },
        }
        if config.stats:
            item["lines"] = {"added": stats.lines_added, "deleted": stats.lines_deleted}
        out.append(item)
    return json.dumps(out, indent=2)

 
