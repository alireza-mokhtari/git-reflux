from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class AppSettings:
    ref: str = "HEAD"
    since: Optional[str] = None
    json_out: bool = False
    no_color: bool = False
    author: Optional[str] = None
    ops: Optional[List[str]] = None
    range_expr: Optional[str] = None
    group_sessions: bool = False
    stats: bool = False
    verbose: bool = False
    quiet: bool = False

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class AppSettings:
    ref: str = "HEAD"
    since: Optional[str] = None
    json_out: bool = False
    no_color: bool = False
    author: Optional[str] = None
    ops: Optional[List[str]] = None
    range_expr: Optional[str] = None
    group_sessions: bool = False
    stats: bool = False
    verbose: bool = False
    quiet: bool = False


