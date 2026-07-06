"""DevBrew command-line entry point.

Running `devbrew` with no arguments launches the interactive terminal UI.
The full command set (menu, track, history, health) arrives with later stories.
"""

from __future__ import annotations

import typer

from devbrew import __version__

app = typer.Typer(help="DevBrew - order coffee from your terminal.")


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


if __name__ == "__main__":
    app()
