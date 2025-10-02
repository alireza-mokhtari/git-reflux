from __future__ import annotations

from models import ActionType


class Heuristics:
    def classify_action_from_message(self, message: str) -> ActionType:
        m = (message or "").lower()
        # prioritize exact operation words before general substrings
        if m.startswith("pull") or " pull " in m:
            return ActionType.pull
        if m.startswith("push") or " push " in m:
            return ActionType.push
        if m.startswith("stash") or " stash" in m:
            return ActionType.stash
        if m.startswith("checkout") or " checkout " in m or " switch " in m or m.startswith("switch"):
            return ActionType.checkout
        if m.startswith("reset") or " reset " in m:
            return ActionType.reset
        if m.startswith("merge") or " merge " in m:
            return ActionType.merge
        if "rebase" in m:
            return ActionType.rebase
        return ActionType.commit

