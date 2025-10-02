from __future__ import annotations

import json
from typing import Iterable, List, Optional, Sequence

from interfaces import GitBackend
from providers import build_services
from settings import AppSettings
from render import render_json
from explain import explain_commit


class FakeGit(GitBackend):
    def __init__(self) -> None:
        self._reflog: List[str] = []
        self._parents: dict[str, List[str]] = {}
        self._show: dict[str, str] = {}
        self._name_rev: dict[str, str] = {}
        self._name_status: dict[str, List[str]] = {}
        self._numstat: dict[str, List[str]] = {}

    def seed_reflog(self, lines: List[str]) -> None:
        self._reflog = lines

    def seed_commit(self, sha: str, parents: List[str], show_pretty: str) -> None:
        self._parents[sha] = parents
        self._show[sha] = show_pretty

    def seed_diff(self, sha: str, name_status: List[str], numstat: List[str]) -> None:
        self._name_status[sha] = name_status
        self._numstat[sha] = numstat

    def get_reflog(self, ref: str, range_expr: Optional[str] = None) -> Iterable[str]:
        return list(self._reflog)

    def get_commit_parents(self, sha: str) -> List[str]:
        return list(self._parents.get(sha, []))

    def show_commit_pretty(self, sha: str) -> str:
        return self._show.get(sha, "")

    def name_rev(self, sha: str) -> Optional[str]:
        return self._name_rev.get(sha)

    def diff_name_status(self, sha: str) -> Sequence[str]:
        return list(self._name_status.get(sha, []))

    def diff_numstat(self, sha: str) -> Sequence[str]:
        return list(self._numstat.get(sha, []))


def test_render_json_includes_action_and_stats(monkeypatch):
    fake = FakeGit()
    fake.seed_reflog([
        "HEAD@{0}|rebase -i onto main|a1b2c3d|1700000000|Alice|alice@example.com",
        "HEAD@{1}|commit: add readme|b2c3d4e|1700000100|Bob|bob@example.com",
    ])
    fake.seed_commit("a1b2c3d", ["p1"], "Alice|alice@example.com|now|Alice|alice@example.com|main|rebase commit")
    fake.seed_commit("b2c3d4e", ["p2"], "Bob|bob@example.com|now|Bob|bob@example.com|main|add readme")
    fake.seed_diff("a1b2c3d", ["A file1", "M file2"], ["10\t2\tfile1", "-\t1\tfile2"])
    fake.seed_diff("b2c3d4e", ["M file3", "D file4"], ["3\t7\tfile3", "0\t10\tfile4"])

    cfg = AppSettings(stats=True)

    # monkeypatch services to use FakeGit
    from providers import Services

    def _build_services(_: AppSettings) -> Services:
        from heuristics import Heuristics
        from providers import Parsers

        return Services(git=fake, parsers=Parsers(), heuristics=Heuristics())

    from providers import build_services as real_build
    monkeypatch.setattr("providers.build_services", _build_services)

    services = build_services(cfg)
    timeline = services.git.get_reflog(ref=cfg.ref, range_expr=cfg.range_expr)
    entries = services.parsers.parse_reflog_lines(timeline)
    out = json.loads(render_json(services, entries, cfg))

    assert out[0]["action"] == "rebase"
    assert out[0]["files"]["added"] == 1
    assert out[0]["lines"]["added"] == 10
    assert out[1]["files"]["deleted"] == 1


def test_explain_returns_expected_dict(monkeypatch):
    fake = FakeGit()
    fake.seed_commit("deadbee", ["pa", "pb"], "Ann|ann@x|now|Com|com@x|main|subject")
    fake.seed_diff("deadbee", ["A x", "M y"], ["5\t1\tx", "2\t3\ty"])

    from providers import Services

    def _build_services(_: AppSettings) -> Services:
        from heuristics import Heuristics
        from providers import Parsers

        return Services(git=fake, parsers=Parsers(), heuristics=Heuristics())

    monkeypatch.setattr("providers.build_services", _build_services)

    services = build_services(AppSettings())
    data = explain_commit(services, "deadbee")
    assert data["sha"] == "deadbee"
    assert data["files"]["added"] == 1
    assert data["lines"]["added"] == 7


