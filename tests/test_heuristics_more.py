from __future__ import annotations

from heuristics import Heuristics
from models import ActionType


def test_more_action_types():
    h = Heuristics()
    assert h.classify_action_from_message("reset --hard") == ActionType.reset
    assert h.classify_action_from_message("checkout main") == ActionType.checkout
    assert h.classify_action_from_message("git pull --rebase") == ActionType.pull
    assert h.classify_action_from_message("push origin main") == ActionType.push
    assert h.classify_action_from_message("WIP stash") == ActionType.stash


