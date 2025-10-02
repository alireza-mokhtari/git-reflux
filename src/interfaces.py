from __future__ import annotations

from typing import Iterable, List, Optional, Protocol, Sequence, runtime_checkable


@runtime_checkable
class GitBackend(Protocol):
    def get_reflog(self, ref: str, range_expr: Optional[str] = None) -> Iterable[str]:
        ...

    def get_commit_parents(self, sha: str) -> List[str]:
        ...

    def show_commit_pretty(self, sha: str) -> str:
        ...

    def name_rev(self, sha: str) -> Optional[str]:
        ...

    def diff_name_status(self, sha: str) -> Sequence[str]:
        ...

    def diff_numstat(self, sha: str) -> Sequence[str]:
        ...


@runtime_checkable
class Clock(Protocol):
    def now(self) -> float:
        ...


@runtime_checkable
class Cache(Protocol):
    def get(self, key: str) -> Optional[object]:
        ...

    def set(self, key: str, value: object) -> None:
        ...


@runtime_checkable
class Renderer(Protocol):
    def render(self, data: object) -> None:
        ...


