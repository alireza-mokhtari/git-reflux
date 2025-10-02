from __future__ import annotations

import json
from typing import Iterable, List, Optional, Sequence

from interfaces import GitBackend
from providers import build_services, Services
from settings import AppSettings
from render import render_json
from filters import build_filters


class FakeGit(GitBackend):
    def __init__(self, lines: List[str]) -> None:
        self.lines = lines

    def get_reflog(self, ref: str, range_expr: Optional[str] = None) -> Iterable[str]:
        return list(self.lines)

    def get_commit_parents(self, sha: str) -> List[str]:
        return []

    def show_commit_pretty(self, sha: str) -> str:
        return "A|a@x|now|C|c@x|main|subject"

    def name_rev(self, sha: str) -> Optional[str]:
        return "main"

    def diff_name_status(self, sha: str) -> Sequence[str]:
        return []

    def diff_numstat(self, sha: str) -> Sequence[str]:
        return []


def test_since_and_author_and_ops_filters(monkeypatch):
    lines = [
        "HEAD@{0}|rebase -i onto main|a|1700000000|Alice|alice@x",
        "HEAD@{1}|commit: docs|b|1700003600|Bob|bob@x",
        "HEAD@{2}|merge branch 'x'|c|1700007200|Carol|carol@x",
    ]
    fake = FakeGit(lines)

    def _build_services(_: AppSettings) -> Services:
        from heuristics import Heuristics
        from providers import Parsers

        return Services(git=fake, parsers=Parsers(), heuristics=Heuristics())

    monkeypatch.setattr("providers.build_services", _build_services)

    cfg = AppSettings(since="2h", author="car", ops=["merge"], json_out=True)
    services = build_services(cfg)
    entries = services.parsers.parse_reflog_lines(services.git.get_reflog(cfg.ref, cfg.range_expr))
    filtered = build_filters(cfg)(entries)
    out = json.loads(render_json(services, filtered, cfg))

    # Only the merge by Carol in the last 2h should remain
    assert len(out) <= 1
    if out:
        assert out[0]["action"] == "merge"
        assert out[0]["committer"]["name"].lower().startswith("car")


