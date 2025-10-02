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


def render_list(services, entries: List[ReflogEntry], config: AppSettings) -> None:
    console = Console(no_color=config.no_color)
    table = Table(show_header=True, header_style="bold")
    table.add_column("when")
    table.add_column("ref")
    table.add_column("action")
    table.add_column("sha")
    table.add_column("subject")
    table.add_column("author")

    now = datetime.now(timezone.utc).timestamp()
    for kind, e in group_sessions(entries[:50]) if config.group_sessions else [("entry", x) for x in entries[:50]]:
        if kind == "break":
            console.print(Rule("— session break —"))
            # fallthrough to render the entry as well
        # naive relative time from unix ts
        delta = int(max(0, now - e.timestamp))
        if delta < 60:
            when = f"{delta}s ago"
        elif delta < 3600:
            when = f"{delta // 60}m ago"
        elif delta < 86400:
            when = f"{delta // 3600}h ago"
        else:
            when = f"{delta // 86400}d ago"
        ref = e.ref_selector
        action = services.heuristics.classify_action_from_message(e.message).value
        sha = e.sha[:7]
        subject = e.message
        author = e.committer_name
        table.add_row(when, ref, action, sha, subject, author)

    console.print(table)


def render_json(services, entries: List[ReflogEntry], config: AppSettings) -> str:
    out = [
        {
            "ref": e.ref_selector,
            "message": e.message,
            "sha": e.sha,
            "timestamp": e.timestamp,
            "committer": {"name": e.committer_name, "email": e.committer_email},
        }
        for e in entries
    ]
    return json.dumps(out, indent=2)

from __future__ import annotations

import json
from typing import List

from rich.console import Console
from rich.table import Table

from .models import ReflogEntry
from .settings import AppSettings


def render_list(services, entries: List[ReflogEntry], config: AppSettings) -> None:
    console = Console(no_color=config.no_color)
    table = Table(show_header=True, header_style="bold")
    table.add_column("when")
    table.add_column("ref")
    table.add_column("action")
    table.add_column("sha")
    table.add_column("subject")
    table.add_column("author")

    for e in entries[:50]:
        # Minimal placeholder until heuristics/enrichment are wired
        when = f"{e.timestamp}"
        ref = e.ref_selector
        action = "commit"
        sha = e.sha[:7]
        subject = e.message
        author = e.committer_name
        table.add_row(when, ref, action, sha, subject, author)

    console.print(table)


def render_json(services, entries: List[ReflogEntry], config: AppSettings) -> str:
    out = [
        {
            "ref": e.ref_selector,
            "message": e.message,
            "sha": e.sha,
            "timestamp": e.timestamp,
            "committer": {"name": e.committer_name, "email": e.committer_email},
        }
        for e in entries
    ]
    return json.dumps(out, indent=2)


