from __future__ import annotations

from filters import build_filters
from models import ReflogEntry
from settings import AppSettings
from sessioning import group_sessions


def _e(ts: int, name: str, email: str, msg: str) -> ReflogEntry:
    return ReflogEntry(
        ref_selector="HEAD@{0}",
        message=msg,
        sha=f"sha{ts}",
        timestamp=ts,
        committer_name=name,
        committer_email=email,
    )


def test_author_filter_matches_name_and_email():
    entries = [
        _e(1700000000, "Alice", "alice@example.com", "commit: x"),
        _e(1700000100, "Bob", "bob@example.com", "merge y"),
    ]
    filt = build_filters(AppSettings(author="alice"))
    result = filt(entries)
    assert len(result) == 1 and result[0].committer_name == "Alice"


def test_ops_filter_uses_heuristics():
    entries = [
        _e(1700000000, "Alice", "alice@example.com", "rebase -i onto main"),
        _e(1700000100, "Bob", "bob@example.com", "commit: add"),
    ]
    filt = build_filters(AppSettings(ops=["rebase"]))
    result = filt(entries)
    assert len(result) == 1 and result[0].message.startswith("rebase")


def test_group_sessions_inserts_breaks_for_large_gaps():
    entries = [
        _e(1700000000, "A", "a@x", "c1"),
        _e(1700005000, "B", "b@x", "c2"),  # 5000s gap > 45m
        _e(1700005100, "C", "c@x", "c3"),
    ]
    grouped = group_sessions(entries, idle_seconds=45 * 60)
    kinds = [k for k, _ in grouped]
    assert "break" in kinds


