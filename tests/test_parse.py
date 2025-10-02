from parse import parse_reflog_lines


def test_parse_basic():
    lines = [
        "HEAD@{0}|commit: init|abcdef1|1690000000|Alice|alice@example.com",
        "HEAD@{1}|rebase -i (start)|1234567|1690000300|Bob|bob@example.com",
    ]
    entries = parse_reflog_lines(lines)
    assert len(entries) == 2
    assert entries[0].sha == "abcdef1"
    assert entries[1].message.startswith("rebase")

