from __future__ import annotations

from interfaces import GitBackend
from enrich import Enricher
from cache import LRUCache
from models import ActionType


class FakeGit(GitBackend):
    def __init__(self, parents):
        self._parents = parents

    def get_reflog(self, ref: str, range_expr=None):  # pragma: no cover
        return []

    def get_commit_parents(self, sha: str):
        return self._parents.get(sha, [])

    def show_commit_pretty(self, sha: str) -> str:
        return "A|a@x|now|C|c@x|main|Merge branch 'feature/x' into main"

    def name_rev(self, sha: str):  # pragma: no cover
        return None

    def diff_name_status(self, sha: str):  # pragma: no cover
        return []

    def diff_numstat(self, sha: str):  # pragma: no cover
        return []


def test_merge_action_inferred_from_parent_count():
    git = FakeGit(parents={"m": ["p1", "p2"], "c": ["p"]})
    enr = Enricher(git, LRUCache(8), LRUCache(8))
    mi_merge = enr.get_commit_info("m")
    mi_commit = enr.get_commit_info("c")
    assert mi_merge.action == ActionType.merge
    assert mi_commit.action == ActionType.commit


