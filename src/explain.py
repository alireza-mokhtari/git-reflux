from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from enrich import Enricher
from cache import LRUCache


def explain_commit(services, sha: str):
    console = Console()
    enricher = Enricher(services.git, LRUCache(256), LRUCache(256))
    info = enricher.get_commit_info(sha)
    stats = enricher.get_diff_stats(sha, include_lines=True)

    table = Table(show_header=False)
    table.add_row("commit", sha)
    table.add_row("author", f"{info.author_name} <{info.author_email}>")
    table.add_row("committer", f"{info.committer_name} <{info.committer_email}>")
    table.add_row("parents", ", ".join(info.parents) or "(none)")
    table.add_row("subject", info.subject)
    table.add_row("decorations", info.decorations or "")
    table.add_row("files", f"+{stats.files_added}/~{stats.files_modified}/-{stats.files_deleted}")
    table.add_row("lines", f"+{stats.lines_added}/-{stats.lines_deleted}")

    console.print(Panel(table, title=f"Explain {sha[:7]}"))
    return {
        "sha": sha,
        "parents": info.parents,
        "author": {"name": info.author_name, "email": info.author_email},
        "committer": {"name": info.committer_name, "email": info.committer_email},
        "subject": info.subject,
        "decorations": info.decorations,
        "files": {
            "added": stats.files_added,
            "modified": stats.files_modified,
            "deleted": stats.files_deleted,
        },
        "lines": {"added": stats.lines_added, "deleted": stats.lines_deleted},
    }

 


