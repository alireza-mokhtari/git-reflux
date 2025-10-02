from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class ActionType(str, Enum):
    commit = "commit"
    merge = "merge"
    rebase = "rebase"
    reset = "reset"
    checkout = "checkout"
    pull = "pull"
    push = "push"
    stash = "stash"


@dataclass(frozen=True)
class ReflogEntry:
    ref_selector: str
    message: str
    sha: str
    timestamp: int
    committer_name: str
    committer_email: str


@dataclass(frozen=True)
class CommitInfo:
    sha: str
    parents: List[str]
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    subject: str
    decorations: str
    action: ActionType


@dataclass(frozen=True)
class DiffStats:
    files_added: int = 0
    files_modified: int = 0
    files_deleted: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
