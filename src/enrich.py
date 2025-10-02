from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from cache import LRUCache
from interfaces import GitBackend
from models import CommitInfo, ActionType, DiffStats


@dataclass
class Enricher:
    git: GitBackend
    show_cache: LRUCache
    diff_cache: LRUCache

    def get_commit_info(self, sha: str) -> CommitInfo:
        parents = self.git.get_commit_parents(sha)
        key = f"show:{sha}"
        cached = self.show_cache.get(key)
        if cached is None:
            pretty = self.git.show_commit_pretty(sha).strip()
            self.show_cache.set(key, pretty)
        else:
            pretty = cached  # type: ignore[assignment]
        # Format: %an|%ae|%ad|%cn|%ce|%D|%s
        parts = pretty.split("|", 6)
        author_name, author_email, _, committer_name, committer_email, decorations, subject = (
            parts + [""] * (7 - len(parts))
        )[:7]
        action = ActionType.merge if len(parents) >= 2 else ActionType.commit
        return CommitInfo(
            sha=sha,
            parents=parents,
            author_name=author_name,
            author_email=author_email,
            committer_name=committer_name,
            committer_email=committer_email,
            subject=subject,
            decorations=decorations,
            action=action,
        )

    def get_diff_stats(self, sha: str, include_lines: bool = True) -> DiffStats:
        key = f"diff:{sha}:{int(include_lines)}"
        cached = self.diff_cache.get(key)
        if cached is not None:
            return cached  # type: ignore[return-value]

        files_added = files_modified = files_deleted = 0
        for line in self.git.diff_name_status(sha):
            if not line:
                continue
            status = line[0]
            if status == "A":
                files_added += 1
            elif status == "M":
                files_modified += 1
            elif status == "D":
                files_deleted += 1

        lines_added = lines_deleted = 0
        if include_lines:
            for line in self.git.diff_numstat(sha):
                parts = line.split("\t")
                if len(parts) >= 2:
                    try:
                        add = int(parts[0]) if parts[0] != "-" else 0
                        dele = int(parts[1]) if parts[1] != "-" else 0
                    except ValueError:
                        add = dele = 0
                    lines_added += add
                    lines_deleted += dele

        stats = DiffStats(
            files_added=files_added,
            files_modified=files_modified,
            files_deleted=files_deleted,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
        )
        self.diff_cache.set(key, stats)
        return stats



