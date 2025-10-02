from __future__ import annotations

from dataclasses import dataclass

from interfaces import GitBackend
from git_io import SubprocessGitBackend
from logger import configure_logging
from settings import AppSettings
import parse as parse_mod
from heuristics import Heuristics


@dataclass
class Parsers:
    def parse_reflog_lines(self, lines):
        return parse_mod.parse_reflog_lines(lines)


@dataclass
class Services:
    git: GitBackend
    parsers: Parsers
    heuristics: Heuristics


def build_services(config: AppSettings) -> Services:
    _ = configure_logging(config.verbose, config.quiet)
    git = SubprocessGitBackend()
    parsers = Parsers()
    heuristics = Heuristics()
    return Services(git=git, parsers=parsers, heuristics=heuristics)


