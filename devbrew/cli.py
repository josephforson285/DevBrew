"""DevBrew command-line entry point.

Running `devbrew` with no arguments launches the interactive terminal UI.
`devbrew health` reports application and database status.
"""

from __future__ import annotations

import typer
from rich.console import Console

from devbrew import __version__
from devbrew.services import health_service

app = typer.Typer(help="DevBrew - order coffee from your terminal.")

_DB_COLOURS = {
    health_service.CONNECTED: "green",
    health_service.NOT_CONFIGURED: "yellow",
    health_service.UNAVAILABLE: "red",
}


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the DevBrew version and exit."
    ),
) -> None:
    """DevBrew - order coffee from your terminal."""
    if version:
        typer.echo(f"DevBrew {__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        # No subcommand: launch the interactive TUI.
        from devbrew.main import run

        run()


@app.command()
def health() -> None:
    """Report application and database status."""
    report = health_service.check_health()
    console = Console()

    app_mark = "[green]OK[/]" if report.app_ok else "[red]FAIL[/]"
    db_colour = _DB_COLOURS.get(report.db_status, "red")

    console.print("[bold]DevBrew health[/]")
    console.print(f"  Application   {app_mark}   {report.app_detail}")
    console.print(
        f"  Database      [{db_colour}]{report.db_status.upper()}[/]   {report.db_detail}"
    )

    if not report.healthy:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
