from __future__ import annotations

from models import ActionType


class Heuristics:
    def classify_action_from_message(self, message: str) -> ActionType:
        m = (message or "").lower()
        if "rebase" in m:
            return ActionType.rebase
        if m.startswith("merge") or " merge " in m:
            return ActionType.merge
        if "reset" in m:
            return ActionType.reset
        if "checkout" in m or "switch" in m:
            return ActionType.checkout
        if "pull" in m:
            return ActionType.pull
        if "push" in m:
            return ActionType.push
        if "stash" in m:
            return ActionType.stash
        return ActionType.commit

