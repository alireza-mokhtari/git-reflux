from __future__ import annotations

import subprocess
from typing import Iterable, List, Optional, Sequence

from .interfaces import GitBackend


class GitCommandError(RuntimeError):
    pass


def _run_git(args: List[str], timeout: int = 10) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.CalledProcessError as exc:
        raise GitCommandError(exc.stderr.strip() or str(exc)) from exc
    except subprocess.TimeoutExpired as exc:
        raise GitCommandError(f"git {' '.join(args)} timed out") from exc
    return proc.stdout


class SubprocessGitBackend(GitBackend):
    def get_reflog(self, ref: str, range_expr: Optional[str] = None) -> Iterable[str]:
        args = ["reflog", "--date=iso", "--format=%gd|%gs|%H|%ct|%cn|%ce", ref]
        if range_expr:
            args = ["reflog", "--date=iso", "--format=%gd|%gs|%H|%ct|%cn|%ce", range_expr]
        out = _run_git(args)
        return out.strip().splitlines()

    def get_commit_parents(self, sha: str) -> List[str]:
        out = _run_git(["cat-file", "-p", sha])
        parents: List[str] = []
        for line in out.splitlines():
            if line.startswith("parent "):
                parents.append(line.split()[1])
        return parents

    def show_commit_pretty(self, sha: str) -> str:
        return _run_git(["show", "--no-patch", "--pretty=%an|%ae|%ad|%cn|%ce|%D|%s", sha])

    def name_rev(self, sha: str) -> Optional[str]:
        out = _run_git(["name-rev", "--name-only", sha]).strip()
        return out or None

    def diff_name_status(self, sha: str) -> Sequence[str]:
        out = _run_git(["diff", "--name-status", f"{sha}^!"])
        return out.strip().splitlines()

    def diff_numstat(self, sha: str) -> Sequence[str]:
        out = _run_git(["diff", "--numstat", f"{sha}^!"])
        return out.strip().splitlines()

from __future__ import annotations

import subprocess
from typing import Iterable, List, Optional, Sequence

from .interfaces import GitBackend


class GitCommandError(RuntimeError):
    pass


def _run_git(args: List[str], timeout: int = 10) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.CalledProcessError as exc:
        raise GitCommandError(exc.stderr.strip() or str(exc)) from exc
    except subprocess.TimeoutExpired as exc:
        raise GitCommandError(f"git {' '.join(args)} timed out") from exc
    return proc.stdout


class SubprocessGitBackend(GitBackend):
    def get_reflog(self, ref: str, range_expr: Optional[str] = None) -> Iterable[str]:
        args = ["reflog", "--date=iso", "--format=%gd|%gs|%H|%ct|%cn|%ce", ref]
        if range_expr:
            args = ["reflog", "--date=iso", "--format=%gd|%gs|%H|%ct|%cn|%ce", range_expr]
        out = _run_git(args)
        return out.strip().splitlines()

    def get_commit_parents(self, sha: str) -> List[str]:
        out = _run_git(["cat-file", "-p", sha])
        parents: List[str] = []
        for line in out.splitlines():
            if line.startswith("parent "):
                parents.append(line.split()[1])
        return parents

    def show_commit_pretty(self, sha: str) -> str:
        return _run_git(["show", "--no-patch", "--pretty=%an|%ae|%ad|%cn|%ce|%D|%s", sha])

    def name_rev(self, sha: str) -> Optional[str]:
        out = _run_git(["name-rev", "--name-only", sha]).strip()
        return out or None

    def diff_name_status(self, sha: str) -> Sequence[str]:
        out = _run_git(["diff", "--name-status", f"{sha}^!"])
        return out.strip().splitlines()

    def diff_numstat(self, sha: str) -> Sequence[str]:
        out = _run_git(["diff", "--numstat", f"{sha}^!"])
        return out.strip().splitlines()


