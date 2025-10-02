from __future__ import annotations

from dataclasses import dataclass
import sys

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


def _build_services_impl(config: AppSettings) -> Services:
    _ = configure_logging(config.verbose, config.quiet)
    git = SubprocessGitBackend()
    parsers = Parsers()
    heuristics = Heuristics()
    return Services(git=git, parsers=parsers, heuristics=heuristics)


class _BuildServicesProxy:
    def __call__(self, config: AppSettings) -> Services:
        module = sys.modules[__name__]
        current = getattr(module, "build_services")
        if current is not self:  # delegated/monkeypatched
            return current(config)  # type: ignore[misc]
        return _build_services_impl(config)


# Exported symbol is a proxy that defers to current providers.build_services if replaced
build_services = _BuildServicesProxy()


