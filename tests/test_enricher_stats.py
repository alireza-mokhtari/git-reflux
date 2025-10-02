from __future__ import annotations

from enrich import Enricher
from cache import LRUCache
from interfaces import GitBackend


class FakeGit(GitBackend):
    def __init__(self) -> None:
        self.parents = {"c": ["p"]}

    def get_reflog(self, ref: str, range_expr=None):  # pragma: no cover - not used here
        return []

    def get_commit_parents(self, sha: str):
        return self.parents.get(sha, [])

    def show_commit_pretty(self, sha: str) -> str:
        return "A|a@x|now|C|c@x|main|subj"

    def name_rev(self, sha: str):  # pragma: no cover - not used here
        return None

    def diff_name_status(self, sha: str):
        return ["A f1", "M f2", "D f3"]

    def diff_numstat(self, sha: str):
        return ["10\t2\tf1", "-\t3\tf2", "0\t7\tf3"]


def test_enricher_stats_counts_files_and_lines():
    enr = Enricher(FakeGit(), LRUCache(8), LRUCache(8))
    stats = enr.get_diff_stats("c", include_lines=True)
    assert (stats.files_added, stats.files_modified, stats.files_deleted) == (1, 1, 1)
    assert (stats.lines_added, stats.lines_deleted) == (10, 12)


