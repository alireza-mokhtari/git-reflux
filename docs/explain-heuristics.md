# Heuristics

- Merge: parent count ≥ 2 or message starts with "Merge"
- Rebase: reflog message contains "rebase"
- Reset/checkout: detect via reflog text
- Squash: single parent + message hints (TBD)

These are best-effort and prefer clarity over perfect accuracy.

