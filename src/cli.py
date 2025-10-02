from __future__ import annotations

import json
from typing import Optional

import typer

from version import __version__


app = typer.Typer(add_completion=False, help="Human-friendly reflog with explain view.")


def main() -> None:
    app()


def exec_reflux(
    list_mode: bool,
    ref: str,
    since: Optional[str],
    json_out: bool,
    no_color: bool,
    author: Optional[str],
    ops: Optional[str],
    explain: Optional[str],
    range_: Optional[str],
    group_sessions: bool,
    stats: bool,
    verbose: bool,
    quiet: bool,
) -> None:
    try:
        # Deferred imports so `typer --help` remains fast
        import providers
        from settings import AppSettings
        from render import render_list, render_json
        from explain import explain_commit
        from filters import build_filters

        config = AppSettings(
            ref=ref,
            since=since,
            json_out=json_out,
            no_color=no_color,
            author=author,
            ops=[p.strip() for p in ops.split(",") if p.strip()] if ops else None,
            range_expr=range_,
            group_sessions=group_sessions,
            stats=stats,
            verbose=verbose,
            quiet=quiet,
        )

        services = providers.build_services(config)

        if explain:
            result = explain_commit(services, explain)
            if json_out:
                typer.echo(json.dumps(result, indent=2))
            else:
                # explain_commit handles its own rendering with Rich
                pass
            return

        timeline = services.git.get_reflog(ref=config.ref, range_expr=config.range_expr)
        entries = services.parsers.parse_reflog_lines(timeline)
        entries = build_filters(config)(entries)

        if json_out:
            typer.echo(render_json(services, entries, config))
        else:
            render_list(services, entries, config)

    except ModuleNotFoundError:
        typer.echo(
            "git-reflux core not yet fully implemented. Please update to the latest version.",
            err=True,
        )
        raise typer.Exit(code=2)


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", help="Show version and exit", callback=None, is_eager=True
    ),
    list_mode: bool = typer.Option(True, "--list", help="Print timeline list (default)", show_default=False),
    ref: str = typer.Option("HEAD", "--ref", help="Ref to inspect"),
    since: Optional[str] = typer.Option(None, "--since", help="Time filter (e.g., 2w, yesterday)"),
    json_out: bool = typer.Option(False, "--json", help="JSON output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colors"),
    author: Optional[str] = typer.Option(None, "--author", help="Filter by author/actor"),
    ops: Optional[str] = typer.Option(None, "--ops", help="Comma list: commit,merge,rebase,reset,..."),
    explain: Optional[str] = typer.Option(None, "--explain", help="Explain a specific SHA"),
    range_: Optional[str] = typer.Option(None, "--range", help="Reflog range, e.g. HEAD@{yesterday}..HEAD"),
    group_sessions: bool = typer.Option(False, "--group", help="Group sessions by idle gaps"),
    stats: bool = typer.Option(False, "--stats", help="Compute line stats (slower)"),
    verbose: bool = typer.Option(False, "--verbose", help="Verbose logs"),
    quiet: bool = typer.Option(False, "--quiet", help="Quiet mode"),
):
    if version:
        typer.echo(f"git-reflux {__version__}")
        raise typer.Exit(code=0)
    if ctx.invoked_subcommand is None:
        exec_reflux(
            list_mode,
            ref,
            since,
            json_out,
            no_color,
            author,
            ops,
            explain,
            range_,
            group_sessions,
            stats,
            verbose,
            quiet,
        )


@app.command("reflux")
def reflux(
    list_mode: bool = typer.Option(
        True, "--list", help="Print timeline list (default)", show_default=False
    ),
    ref: str = typer.Option("HEAD", "--ref", help="Ref to inspect"),
    since: Optional[str] = typer.Option(None, "--since", help="Time filter (e.g., 2w, yesterday)"),
    json_out: bool = typer.Option(False, "--json", help="JSON output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colors"),
    author: Optional[str] = typer.Option(None, "--author", help="Filter by author/actor"),
    ops: Optional[str] = typer.Option(None, "--ops", help="Comma list: commit,merge,rebase,reset,..."),
    explain: Optional[str] = typer.Option(None, "--explain", help="Explain a specific SHA"),
    range_: Optional[str] = typer.Option(None, "--range", help="Reflog range, e.g. HEAD@{yesterday}..HEAD"),
    group_sessions: bool = typer.Option(False, "--group", help="Group sessions by idle gaps"),
    stats: bool = typer.Option(False, "--stats", help="Compute line stats (slower)"),
    verbose: bool = typer.Option(False, "--verbose", help="Verbose logs"),
    quiet: bool = typer.Option(False, "--quiet", help="Quiet mode"),
):
    """Subcommand alias for the default behavior."""
    exec_reflux(
        list_mode,
        ref,
        since,
        json_out,
        no_color,
        author,
        ops,
        explain,
        range_,
        group_sessions,
        stats,
        verbose,
        quiet,
    )

