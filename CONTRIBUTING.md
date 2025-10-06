# Contributing to git-reflux

Thank you for your interest! To keep quality high and history clean:

- All changes must go through Pull Requests. No direct pushes to `main`.
- Fork, create a feature branch, and open a PR.
- Run CI locally:
  ```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -U pip
  pip install -e '.[dev]'
  ruff check . && mypy src && pytest -q
  ```
- Keep PRs focused and small. Add tests for new behavior.
- The `CODEOWNERS` team must approve before merge.

## Commit messages

- Use clear, imperative titles. Reference issues if applicable.

## Developer tips

- Use `git reflux --since ...` during development to quickly inspect changes.
