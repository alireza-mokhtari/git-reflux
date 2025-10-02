# git-reflux

Human-friendly reflog. Minimal HEAD-speak. See where a change came from, when, how big, who, and the hash. Includes `--explain <sha>` for deep dives.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e '.[dev]'
```

Usage examples:

```bash
# Pretty list (default)
git reflux --since 3d

# JSON output
git reflux --json --since 1w

# Explain a commit
git reflux --explain <sha>
```

## Features

- Human-first list of reflog entries: when, ref, action, sha, subject, author
- Heuristics: classify commit/merge/rebase/reset/checkout/pull/push/stash
- Filters: `--since`, `--author`, `--ops`
- Session grouping: `--group` adds session break separators
- Explain view: author/committer, parents, decorations, diff stats

## Roadmap

- Perf caching, TUI, multi-platform packaging (brew, deb/rpm, scoop, winget)

