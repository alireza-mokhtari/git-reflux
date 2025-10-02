from heuristics import Heuristics
from models import ActionType


def test_classify_action():
    hz = Heuristics()
    assert hz.classify_action_from_message("rebase -i onto main") == ActionType.rebase
    assert hz.classify_action_from_message("Merge branch 'x'") == ActionType.merge
    assert hz.classify_action_from_message("commit: add file") == ActionType.commit

